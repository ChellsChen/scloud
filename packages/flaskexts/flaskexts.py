#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date       : 2015-06-10 12:23:52
# Author     : 陈小雪
# E-mail     : shell_chen@yeah.net
# Version    : 1.0.1

import os
import logging
import urllib
from flask import request, url_for
from flask.views import MethodView
from plugins import load


class Sunshine(object):
    URLS = [ ]
    PLUGINS = [ ]

    def __init__(self, app, plugin_dir=None, blueprints_dir=None):
        self.app = app
        self.plugin_dir = plugin_dir
        self.blueprints_dir = blueprints_dir

        self.load_plugin()
        self.load_blueprint()

        self.list_routes()

    def load_blueprint(self):
        if self.blueprints_dir is None:
            return

        bps_infos = load(self.blueprints_dir, 'app_bp')
        for name, bps in bps_infos.items():
            bp = bps[1]
            self.app.register_blueprint(bp)

    def load_plugin(self):
        if self.plugin_dir is None:
            return

        mode_infos = load(self.plugin_dir, 'name', 'urls')

        for model, name, urls in mode_infos.values():
            self.init_mode(model, name, urls)

        self.__add_url()

    def init_mode(self, model, name, urls):
        for url, fun in _groups(urls):
            if url.startswith("/"):
                url = "/%s%s"%(name, url)
            else:
                url = os.path.join("/", name, url)

            fun = _get_attr(model, fun)
            if fun is None:
                continue

            self.URLS.append((name, url, fun))

        self.PLUGINS.append((name, model))

    def __add_url(self):
        for mode_name, url, fun in self.URLS:
            self.register_api(mode_name, fun, url)

    def register_api(self,mode_name, view, url):
        endpoint = "%s.%s"%(mode_name, view.__name__)
        view_func = view.as_view(url)
        self.app.add_url_rule(url, view_func=view_func,
                        endpoint = endpoint,
                        methods = ['GET','PUT', 'DELETE','POST'])

    def list_routes(self):
        output = []
        ctx = self.app.test_request_context('/')
        ctx.push()

        for rule in self.app.url_map.iter_rules():
            options = {}
            for arg in rule.arguments:
                options[arg] = "[{0}]".format(arg)

            url = url_for(rule.endpoint, **options)
            output.append((url, rule.endpoint))

        l = 0
        for u, e in output:
            if len(u) > l:
                l = len(u)

        lines = [""]
        for  u, e in sorted(output,key=lambda x:x[1]):
            lines.append("%s ===> %s" %(u.ljust(l), e))

        logging.info("\n".join(lines))

        ctx.pop()


def _get_attr(model, view):
    if isinstance(view, basestring):
        if not hasattr(model, view):
            logging.error("mode %s not hasattr [%s]" %(model, view))
            return None

        view = getattr(model, view)
    return view


def _groups(urls):
    i = 0
    t = []
    while i < len(urls):
        t.append((urls[i], urls[i+1]))
        i = i + 2
    return t

def load_restful(app_api, restful_dir):
    mode_infos = load(restful_dir, "urls")
    for model, urls in mode_infos.values():
        mode_name = model.__name__
        names = mode_name.split("/")[-1:][0]

        for url, view in _groups(urls):
            view = _get_attr(model, view)
            if view is None:
                continue

            endpoint = "%s.%s"%(names, view.__name__)
            app_api.add_resource(view, url, endpoint=endpoint)


class ClassViews(MethodView):
    """
    重构dispatch_request方法, 使其兼容视图函数中方法的大小写

    """
    def dispatch_request(self, *args, **kwargs):
        method = request.method.lower()

        if not hasattr(self, method):
            meth = getattr(self, method.upper(), None)
        else:
            meth = getattr(self, method, None)

        # if the request method is HEAD and we don't have a handler for it
        # retry with GET
        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)
        assert meth is not None, 'Unimplemented method %r' % request.method
        return meth(*args, **kwargs)

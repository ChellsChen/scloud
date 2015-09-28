#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-09-23 17:13:23
# @Author  : 陈小雪 (shell_chen@yeah.net)
# @Version : $Id$

import os
import json

from flask import render_template, request, redirect
from flaskexts import ClassViews

from mdeditor.helper import getid
from setting import STORE_PATH
from mdeditor.storage import STORAGE, get_tex_info

name = "mdeditor"

urls = (
    "/",         "MdEditor",
    )

Storage = STORAGE(STORE_PATH)


class MdEditor(ClassViews):
    def get(self):
        args = request.args
        Id = args.get("id", "")

        if str(Id) not in Storage.index.keys():
            return redirect("/")

        tex_path = os.path.join(STORE_PATH, str(Id))

        md_tex = Storage.get(Id)
        if md_tex == False:
            return "404 not found!"

        info = Storage.index.get(str(Id))
        config = Storage.get_config()

        return render_template("scloud.html", config = config,
            tex = md_tex, info = info)

    def post(self):
        Id = int(getid())
        tpl_path = os.path.join(STORE_PATH, "tmpl")

        with open(tpl_path, "r") as fp:
            tex = fp.read()

        title, tags = get_tex_info(tex)

        Storage.add(Id, title, tags, tex)

        return json.dumps({
                "id":Id,
                "tex": tex,
                "status":0,
            })

    def put(self):
        form = request.form
        Id = int(form.get("id"))
        md = form.get("md")
        html = form.get("html")
        post = int(form.get("post"))

        title, tags = get_tex_info(md)

        res = Storage.update(Id, title, tags, md, html, post)
        if not res:
            return json.dumps({
                    "status":1,
                    "message": "id:%s is not exsit"%Id
                })

        return json.dumps({
                "status":0
            })

    def delete(self):
        Id = request.args.get("id", "")
        Storage.delete(Id)
        return json.dumps({
                "status":0
            })





















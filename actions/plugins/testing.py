#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date    : 2015-08-06 09:22:36
# Author  : 陈小雪
# E-mail  : shell_chen@yeah.net
# Version : v1.0.1

import os
from flask import render_template
from flaskexts import ClassViews

name = "testing"

class Index(ClassViews):
    def GET(self):
        return render_template("base.html")

class Testing(ClassViews):
    def GET(self):
        return "this is testing"

urls = (
    "/", Index,
    "/testing/", Testing
    )

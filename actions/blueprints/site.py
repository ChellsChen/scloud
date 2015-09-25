#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date    : 2015-08-06 14:14:07
# Author  : 陈小雪
# E-mail  : shell_chen@yeah.net
# Version : v1.0.1

import os

from flask.ext.login import login_required
from flask import render_template, redirect, url_for, request,Blueprint
from webapp import BASEPATH

app_bp = Blueprint("site", __name__)

@app_bp.route("/")
@app_bp.route("/index/")
def index():
    # return render_template("index.html")
    return render_template("home.html")

@app_bp.route("/code/")
def code():
    code_path = os.path.join(BASEPATH, "manage.py")
    codes = ""
    with open(code_path, "r") as fp:
        codes = fp.read()

    return codes

@app_bp.route("/strapdown/")
def strapdown():
    return render_template("strapdown.html")

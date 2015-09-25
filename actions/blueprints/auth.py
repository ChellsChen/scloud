#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date       : 2015-06-04 16:33:38
# Author     : 陈小雪
# E-mail     : shell_chen@yeah.net
# Version    : 1.0.1

import logging
import json
from flask import render_template, request, \
                  redirect, url_for, g, \
                  Blueprint

from flask.ext.login import login_user, login_required, logout_user, current_user

from models.user import User
from forms.auth import LoginForm
from webapp import logger, APP_LM

app_bp = Blueprint("auth", __name__)


@APP_LM.user_loader
def load_user(id):
    return User.query.get(int(id))

@app_bp.route("/login/", methods = ["GET", "POST"])
def login():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for("site.index"))

    form = LoginForm()

    error = ""
    while True:
        if request.method == "GET":
            break

        if not form.validate_on_submit():
            error = "validate error!"
            break

        password = form.password.data
        email = form.email.data
        rememberme = form.rememberme.data
        user = User.query.filter_by(email= email).first()

        if not user:
            error = "account %s : unregister."%(email)
            break

        if not user.verify_confirmed():
            error = "account %s : is unconfirmed."%(email)
            unconfirmed = True
            break

        if not user.verify_password(password):
            error = "password error."
            break

        login_user(user, rememberme)

        logger.info("user:%s email:%s login"%(user.name,user.email))

        return redirect(request.args.get('next') or url_for("site.index"))

    return render_template("auth/login.html", error=error, form=form)


@app_bp.route("/userinfo/")
def userinfo():
    usr = {}
    if current_user is not None:
        usr["name"] = current_user.name
        usr["email"] = current_user.email
        return json.dumps(usr)
    return render_template("auth/login.html")

@app_bp.route("/logout/")
def logout():
    logout_user()
    return redirect("/login")

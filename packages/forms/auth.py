#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date       : 2015-04-22 13:51:22
# Author   : xiaoxue-chen
#E-mail     : shell_chen@yeah.net
# Version  : 1.0.1

import os

from flask.ext.wtf import Form
from wtforms import BooleanField,StringField,IntegerField,TextField,PasswordField
from wtforms.validators import Required,EqualTo
from models.user import User

class LoginForm(Form):
    rememberme = BooleanField("rememberme", default = False)
    email = TextField("email", validators=[Required()])
    password = PasswordField("password", validators=[Required()])

class RegisterForm(Form):
    email = TextField("email",validators=[Required()])
    name = StringField("name",validators=[Required()])
    password1 = PasswordField("password1",validators=[Required()])
    password2 = PasswordField("password2",
            validators=[Required(), EqualTo("password1",
            message="Passwords must match")])

    def validate_emails(self):
        user = User.query.filter_by(email= self.email.data).first()
        if not user:
            return True
        else:
            return False


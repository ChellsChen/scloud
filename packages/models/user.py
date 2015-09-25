#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date       : 2015-04-22 14:41:33
# Author     : 陈小雪
#E-mail      : shell_chen@yeah.net
# Version    : 1.0.1


import os
from webapp import APP_DB as db
import hashlib
import time

ROLE_RELEASE = 1
ROLE_MANAGER = 0

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(32), nullable=False)
    role = db.Column(db.SmallInteger, default = ROLE_RELEASE)
    confirmed = db.Column(db.Boolean,default=False)

    def __repr__(self):
        return '<User %r>' % (self.name)

    def __init__(self, username, email, password, role = ROLE_RELEASE ):
        self.name = username
        self.email = email
        self.password= self.password_hash(password)
        self.role = role
        self.confirmed = False

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def verify_password(self, pwd):
        pwds = self.password_hash(pwd)
        if pwds == self.password:
            return True
        else:
            return False

    def verify_confirmed(self):
        if self.confirmed:
            return True
        else:
            return False

    def password_hash(self,password):
        md = hashlib.md5()
        md.update(password)
        return md.hexdigest()

    def is_admin(self):
        if self.role == ROLE_RELEASE:
            return True
        return False

    def add(self):
        db.session.add(self)
        db.session.commit()




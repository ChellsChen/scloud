#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-08-05 18:48:36
# @Author  : 陈小雪 (shell_chen@yeah.net)
# @Version : $Id$

import os
import logging
import logging.handlers
from flask import Flask, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

import imp

from config import load_config
from flaskexts import Sunshine, load_restful


BASEPATH = os.path.dirname(os.path.realpath(__file__))
SHARE_PATH = os.path.join(BASEPATH, "share")
LOG_PATH = os.path.join(BASEPATH, "log")

if not os.path.isdir(LOG_PATH):
    os.mkdir(LOG_PATH, 0777)

LOG_FILE = os.path.join(LOG_PATH, "web.log")

LOG_FORMAT = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
LOG_MAX = 1024*1024*10
BACKUP_COUNT = 5

logger = logging.getLogger()
loghandler = logging.handlers.RotatingFileHandler(
    LOG_FILE,
    maxBytes = LOG_MAX,
    backupCount = BACKUP_COUNT
    )

loghandler.setFormatter(LOG_FORMAT)
logger.addHandler(loghandler)
logger.setLevel(logging.INFO)


APP = Flask(__name__)
APP_DB = SQLAlchemy()
APP_LM = LoginManager()


def init_app():
    APP.config.from_object(load_config())

    APP_DB.init_app(APP)

    APP_LM.init_app(APP)
    APP_LM.login_view = 'auth.login'

    # 加载blueprints, plugins接口
    load_dir = os.path.join(BASEPATH, "actions/plugins")
    blueprints_dir = os.path.join(BASEPATH, "actions/blueprints")
    sunshine = Sunshine(APP, load_dir, blueprints_dir)


if __name__ == '__main__':
    pass








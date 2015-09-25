#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

class BaseConfig(object):
    DEBUG = False
    TESTING = False
    PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
    SECRET_KEY = "nimitz"
    THREADED = True

    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1/nimitz"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True

class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False


def load_config():
    mode = os.environ.get('MODE')
    try:
        if mode == 'PRODUCTION':
            return ProductionConfig
        elif mode == 'TESTING':
            return TestingConfig
        elif mode == "DEVELOPMENT":
            return DevelopmentConfig
        else:
            return BaseConfig
    except ImportError:
        return BaseConfig



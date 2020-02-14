# -*- coding: utf-8 -*-
"""
-------------------------------------------------
Description :
Author : xiaoboli
-------------------------------------------------
Change Activity:
-------------------------------------------------
"""

__author__ = 'xiaoboli'

from flask import Flask


def register_blueprint(app: object) -> object:
    """
    注册蓝图
    :param app:
    :return:
    """
    from app.api.v1 import create_blueprint_v1
    blueprint_v1 = create_blueprint_v1()
    app.register_blueprint(blueprint_v1, url_prefix='/v1')


def create_app() -> object:
    """
    初始化应用程序
    :return:
    """
    app = Flask(__name__)
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')
    register_blueprint(app)
    return app

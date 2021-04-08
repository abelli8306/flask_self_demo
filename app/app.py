# -*- coding: utf-8 -*-
"""
-------------------------------------------------
Description :
Author : xiaoboli
-------------------------------------------------
Change Activity:
-------------------------------------------------
"""
from flask_login import LoginManager
from flask import Flask

# 登录cookie插件
login_manager = LoginManager()

# 初始化访问日志配置
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(name)s|%(module)s|%(lineno)s: %(message)s',
    }},
    'handlers': {
        'wsgi': {
            # 'class': 'logging.StreamHandler',
            # 'stream': 'ext://flask.logging.wsgi_errors_stream',
            'class': 'logging.FileHandler',
            'filename': 'logs/access.log',
            'mode': 'a',
            'formatter': 'default'
        }
        # 'info_rotating_file_handler': {
        #     'level': 'INFO',
        #     'formatter': 'info',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': 'info.log',
        #     'mode': 'a',
        #     'maxBytes': 1048576,
        #     'backupCount': 10
        # },
        # 'error_file_handler': {
        #     'level': 'WARNING',
        #     'formatter': 'error',
        #     'class': 'logging.FileHandler',
        #     'filename': 'error.log',
        #     'mode': 'a',
        # },
        # 'critical_mail_handler': {
        #     'level': 'CRITICAL',
        #     'formatter': 'error',
        #     'class': 'logging.handlers.SMTPHandler',
        #     'mailhost': 'localhost',
        #     'fromaddr': 'monitoring@domain.com',
        #     'toaddrs': ['dev@domain.com', 'qa@domain.com'],
        #     'subject': 'Critical error with application name'
        # }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


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
    login_manager.init_app(app)
    return app

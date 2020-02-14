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

from flask import Blueprint
from app.api.v1 import user, book


def create_blueprint_v1():
    api_v1 = Blueprint('v1', __name__)

    user.api.register(api_v1, url_prefix='/user')
    book.api.register(api_v1, url_prefix='/book')
    return api_v1

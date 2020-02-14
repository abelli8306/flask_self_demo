# -*- coding: utf-8 -*-
"""
-------------------------------------------------
Description :
Author : xiaoboli
-------------------------------------------------
Change Activity:
-------------------------------------------------
"""
import json

from flask import Blueprint
from app.libs.redprint import Redprint

__author__ = 'xiaoboli'

# redprint
api = Redprint('user')


@api.route('/get')
def get_user():
    return json.dumps({"username": 'xiaoboli'}, default=lambda o: o.__dict__), 200, {'content-type': 'text/html'}

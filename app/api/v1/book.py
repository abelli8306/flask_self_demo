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
from flask import current_app

__author__ = 'xiaoboli'

# redprint
api = Redprint('book')


@api.route('/get')
def get_book():
    return json.dumps({"book": 'a pig'}, default=lambda o: o.__dict__), 200, {'content-type': 'text/html'}


@api.route('/create')
def create_book():
    return 'create book'


@api.route('/search/<gid>', methods=['GET', 'POST'])
def search_book(gid):
    current_app.logger.info('Info message: {"book_id": ' + gid + '}')
    return json.dumps({"book_id": gid}), 200, {'content-type': 'text/html'}

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

from flask import request, session, redirect, url_for
from markupsafe import escape
from redis import Redis

from app.libs.redprint import Redprint

__author__ = 'xiaoboli'

# redprint
api = Redprint('user')


@api.route('/get')
def get_user():
    return json.dumps({"username": 'xiaoboli'}, default=lambda o: o.__dict__), 200, {'content-type': 'text/html'}


@api.route('/hello')
def hello():
    redis = Redis(host='redis', port=6379)
    count = redis.incr('hits')
    return 'Hello World! I have been seen {} times.\n'.format(count)


@api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('v1.view'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


@api.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('v1.view'))


@api.route('/view')
def view():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

# -*- coding: utf-8 -*-
"""
-------------------------------------------------
Description :
Author : weseey
-------------------------------------------------
Change Activity:
-------------------------------------------------
"""
from flask_login import login_user, current_user, UserMixin, login_required, logout_user

from app.app import login_manager

__author__ = 'weseey'

from app.libs.redprint import Redprint
from flask import request, redirect, url_for, abort, Response

__author__ = 'xiaoboli'

# redprint
api = Redprint('FlaskLogin')


# silly user model
class User(UserMixin):

    def __init__(self, name):
        # self.id = id
        # self.name = "user" + str(id)
        self.name = name
        self.password = self.name + "_secret"

    def __repr__(self):
        # return "%d/%s/%s" % (self.id, self.name, self.password)
        return "%s/%s" % (self.name, self.password)

    def get_id(self):
        return self.name


# # create some users with ids 1 to 20
# users = [User("user_" + str(id)) for id in range(1, 21)]


# somewhere to login
@api.route("/login", methods=["GET", "POST"])
def FlaskLogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == username + "_secret":
            # id = username.split('user')[1]
            # user = User(id)
            user = User(username)
            login_user(user)
            return redirect(url_for('v1.FlaskLoginView'))
        else:
            return abort(401)
    else:
        return Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=text name=password>
            <p><input type=submit value=Login>
        </form>
        ''')


# somewhere to logout
@api.route("/logout")
@login_required
def FlaskLogout():
    logout_user()
    return Response('<p>Logged out</p>')


# # handle login failed
# @api.errorhandler(401)
# def page_not_found(e):
#     return Response('<p>Login failed</p>')


# callback to reload the user object
# @login_manager.user_loader
# def load_user(userid):
#     return User(userid)

@login_manager.user_loader
def load_user(username):
    return User(username)


@api.route('/view')
# @login_required
def FlaskLoginView():
    if current_user.is_authenticated:
        return {
            "name": current_user.name,
            "password": current_user.password
        }
    return 'You are not logged in'

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

from app import create_app

app = create_app()

# enter function
if __name__ == '__main__':
    # app.config['JSON_AS_ASCII'] = False
    app.run(host=app.config['HOST'],
            debug=app.config['DEBUG'], port=app.config['PORT'])

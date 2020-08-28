"""

 -*- coding: utf-8 -*-
Time    : 2019/7/12 14:18
Author  : Hansybx

"""
from flask import render_template, redirect, request
from flask_cors import CORS

from app import create_app
import logging

from app.utils.xsbook.xslogin import user_query

app = create_app()
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')
    # return 'hello,flask'


# @app.route('/')
@app.route('/xslogin')
def xs_index():
    # return render_template('xslibrary/xslibrary.html')
    return render_template('xslogin/xslogin.html')


@app.route('/xslibrary')
def xs_library():
    username = request.args.get('username')
    password = request.args.get('passwd')
    state = user_query(username, password,MD5=False)
    if state:
        return render_template('xslibrary/xslibrary.html')
    else:
        return redirect('/xslogin')


if __name__ == '__main__':
    app.run(port=8080, debug=app.config['DEBUG'])

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

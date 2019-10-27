"""

 -*- coding: utf-8 -*-
Time    : 2019/7/12 14:18
Author  : Hansybx

"""
from flask import render_template

from app import create_app
import logging

app = create_app()


@app.route('/')
def index():
    # return render_template('index.html')
    return 'hello,flask'


if __name__ == '__main__':
    app.run(port=8080, debug=app.config['DEBUG'])

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

"""

 -*- coding: utf-8 -*-
Time    : 2019/7/12 14:18
Author  : Hansybx

"""

from flask import Flask

from app.models import db


def create_app():
    app = Flask(__name__)

    app.config.from_object('app.settings')
    app.config.from_object('app.secure')

    register_blueprint(app)
    init_db(app)
    return app


def register_blueprint(app):
    from app.api.v1 import v1
    from app.api.v1.stu import stu

    app.register_blueprint(v1, url_prefix='/api/v1')
    app.register_blueprint(stu, url_prefix='/api/v1/stu')


def init_db(app):
    # 注册db
    db.init_app(app)
    # 将代码映射到数据库中
    with app.app_context():
        db.create_all(app=app)

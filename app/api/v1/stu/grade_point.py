"""

 -*- coding: utf-8 -*-
Time    : 2019/7/19 9:55
Author  : Hansybx

"""
from flask import request, jsonify

from app.api.v1.stu import stu
from app.models.error import AuthFailed, PasswordFailed
from app.models.res import Res
from app.utils.score.score_utils import get_score, grade_point_average


@stu.route('/score', methods=['POST'])
def score_get():
    username = request.form['username']
    password = request.form['password']
    try:
        result = get_score(username, password)
        status = 200
        msg = '查询成功'
        info = [
            {
                'result': result
            }
        ]
    except AuthFailed:
        status = 401
        msg = '查询失败'
        info = [
            {
                'result': '未评教'
            }
        ]

    except PasswordFailed:
        status = 401
        msg = '查询失败'
        info = [
            {
                'result': '账号或密码错误'
            }
        ]

    res_json = Res(status, msg, info)
    return jsonify(res_json.__dict__)


@stu.route('/gradepoint', methods=['POST'])
def grade_point_get():
    username = request.form['username']
    password = request.form['password']

    try:
        result = grade_point_average(username, password)
        status = 200
        msg = '查询成功'
        info = [
            {
                'result': result
            }
        ]
    except AuthFailed:
        status = 401
        msg = '查询失败'
        info = [
            {
                'result': '未评教'
            }
        ]

    except PasswordFailed:
        status = 401
        msg = '查询失败'
        info = [
            {
                'result': '账号或密码错误'
            }
        ]

    res_json = Res(status, msg, info)
    return jsonify(res_json.__dict__)

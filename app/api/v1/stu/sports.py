"""

 -*- coding: utf-8 -*-
Time    : 2019/7/20 18:39
Author  : Hansybx

"""
from flask import request, jsonify

from app.api.v1 import stu
from app.models.res import Res
from app.utils.sports.sports_utils import morning_attend, club_attend


@stu.route('/morning/attend')
def morning_attend_get():
    username = request.form['username']
    password = request.form['password']
    try:
        result = morning_attend(username, password)
        status = 200
        msg = '查询成功'
        info = [
            {
                'result': result
            }
        ]
    except Exception:
        status = 500
        msg = '查询失败'
        info = [
            {
                'result': '未知异常'
            }
        ]

    res_json = Res(status, msg, info)
    return jsonify(res_json.__dict__)


@stu.route('/club/attend',methods=['POST'])
def club_attend_get():
    username = request.form['username']
    password = request.form['password']
    try:
        result = club_attend(username, password)
        status = 200
        msg = '查询成功'
        info = [
            {
                'result': result
            }
        ]
    except Exception:
        status = 500
        msg = '查询失败'
        info = [
            {
                'result': '未知异常'
            }
        ]

    res_json = Res(status, msg, info)
    return jsonify(res_json.__dict__)
"""

 -*- coding: utf-8 -*-
Time    : 2019/8/13 22:36
Author  : Hansybx

"""
from flask import request, jsonify

from app.api.v1.stu import stu
from app.models.res import Res
from app.utils.xiaoli.xiaoli_util import get_school_calendar


@stu.route('/school/calendar', methods=['POST'])
def calender_get():
    username = request.form['username']
    password = request.form['password']

    try:
        result = get_school_calendar(username, password)
        code = 200
        msg = '查询成功'
        info = result

    except Exception:
        code = 500
        msg = '查询失败'
        info = {
            'result': '未知异常'
        }

    res_json = Res(code, msg, info)
    return jsonify(res_json.__dict__)

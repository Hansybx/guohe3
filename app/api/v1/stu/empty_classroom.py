"""

 -*- coding: utf-8 -*-
Time    : 2019/7/20 19:05
Author  : Hansybx

"""
from flask import request, jsonify

from app.api.v1.stu import stu
from app.models.error import PasswordFailed
from app.models.res import Res
from app.utils.empty_classroom.empty_classroom_utils import empty_classroom


@stu.route('/classroom/empty', methods=['POST'])
def empty_classroom_get():
    username = request.form['username']
    password = request.form['password']
    semester = request.form['semester']
    area_id = request.form['area_id']
    building_id = request.form['building_id']
    week = request.form['week']

    try:
        result = empty_classroom(username, password, semester, area_id, building_id, week)
        code = 200
        msg = '查询成功'
        info = result

    except PasswordFailed:
        code = 401
        msg = '查询失败'
        info = {
            'result': '账号或密码错误'
        }

    except Exception:
        code = 500
        msg = '查询失败'
        info = {
            'result': '未知异常'
        }

    res_json = Res(code, msg, info)
    return jsonify(res_json.__dict__)

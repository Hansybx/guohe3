"""

 -*- coding: utf-8 -*-
Time    : 2019/7/19 9:37
Author  : Hansybx

"""
from flask import request, jsonify

from app.api.v1.stu import stu
from app.models.error import AuthFailed, PasswordFailed
from app.models.res import Res
from app.utils.class_schedule.class_schedule import get_class_schedule_week


@stu.route('/class/schedule', methods=['POST'])
def get_class_schedule():
    username = request.form['username']
    password = request.form['password']
    semester = request.form['semester']
    result = {}
    try:
        for zc in range(1, 21):
            result[semester + '_' + str(zc)] = get_class_schedule_week(username, password, semester, zc)

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

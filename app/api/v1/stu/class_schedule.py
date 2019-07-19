"""

 -*- coding: utf-8 -*-
Time    : 2019/7/19 9:37
Author  : Hansybx

"""
from flask import request, jsonify

from app.api.v1.stu import stu
from app.models.res import Res
from app.utils.class_schedule.class_schedule import get_class_schedule_week


@stu.route('/class/schedule', methods=['POST'])
def get_class_schedule():
    username = request.form['username']
    password = request.form['password']
    semester = request.form['semester']
    result = {}
    for zc in range(1, 21):
        result[semester + '_' + str(zc)] = get_class_schedule_week(username, password, semester, zc)

    status = 200
    msg = '查询成功'
    info = [
        {
            'result': result
        }
    ]
    res_json = Res(status, msg, info)

    return jsonify(res_json.__dict__)

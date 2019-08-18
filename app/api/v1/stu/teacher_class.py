"""

 -*- coding: utf-8 -*-
Time    : 2019/7/27 16:15
Author  : Hansybx

"""
from flask import request, jsonify

from app.api.v1.stu import stu
from app.models.error import PasswordFailed
from app.models.res import Res
from app.utils.teacher_class.teacher_class_utils import get_teacher_class


@stu.route('/class/teacher', methods=['POST'])
def teacher_class_get():
    username = request.form['username']
    password = request.form['password']
    semester = request.form['semester']
    academy = request.form['academy']
    zc = request.form['zc']

    try:
        result = get_teacher_class(username, password, semester, academy, zc)
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
        info = [
            {
                'result': '未知异常'
            }
        ]

    res_json = Res(code, msg, info)
    return jsonify(res_json.__dict__)

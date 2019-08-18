"""

 -*- coding: utf-8 -*-
Time    : 2019/7/23 20:39
Author  : Hansybx

"""
from flask import request, jsonify

from app.api.v1.stu import stu
from app.models.error import PasswordFailed
from app.models.res import Res
from app.utils.login.login_util import student_info


@stu.route('/info', methods=['POST'])
def student_info_get():
    username = request.form['username']
    password = request.form['password']
    try:
        result = student_info(username, password)
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

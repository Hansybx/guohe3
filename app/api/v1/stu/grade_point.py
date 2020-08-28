"""

 -*- coding: utf-8 -*-
Time    : 2019/7/19 9:55
Author  : Hansybx

"""
from flask import request, jsonify

from app.api.v1.stu import stu
from app.models.error import AuthFailed, PasswordFailed
from app.models.res import Res
from app.utils.score.score_utils import get_score, grade_point_average, query_in_sql, gpa_calculate


@stu.route('/score', methods=['POST'])
def score_get():
    username = request.form['username']
    password = request.form['password']
    try:
        result = get_score(username, password)
        code = 200
        msg = '查询成功'
        info = result

    except AuthFailed:
        code = 402
        msg = '强智系统未评教请在强智教务评教后在查询'

        temp = query_in_sql(username)
        if temp:
            info = temp.json['data']
        else:
            info = {
                'result': '未评教'
            }

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


@stu.route('/gpa', methods=['POST'])
def grade_point_get():
    username = request.form['username']
    password = request.form['password']

    try:
        result = grade_point_average(username, password)
        code = 200
        msg = '查询成功'
        info = result

    except AuthFailed:
        code = 402
        msg = '强智系统未评教请在强智教务评教后在查询'
        temp = query_in_sql(username)
        if temp:
            info = gpa_calculate(temp.json['data'], username)
        else:
            info = {
                'result': '未评教'
            }

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

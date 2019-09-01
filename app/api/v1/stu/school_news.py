"""

 -*- coding: utf-8 -*-
Time    : 2019/8/17 17:25
Author  : Hansybx

"""
from flask import jsonify

from app.api.v1.stu import stu
from app.models.res import Res
from app.utils.news.news_util import get_news_url


@stu.route('/school/news/url', methods=['GET'])
def news_get():
    try:
        result = get_news_url()
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
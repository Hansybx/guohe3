"""

 -*- coding: utf-8 -*-
Time    : 2019/7/19 8:18
Author  : Hansybx

"""
# import re
#
# import requests
# from flask import request, json
#
# from app.api.v1.stu import stu
# from app.utils.login.login_util import login
#
#
# @stu.route('/login', methods=['POST'])
# def stu_login():
#     username = request.form['username']
#     password = request.form['password']
#     reg = r'<font color="red">请先登录系统</font>'
#     session = login(username, password)
#     # paramrs = {'USERNAME:': username, 'PASSWORD': password}
#     response = session.get('http://jwgl.just.edu.cn:8080/jsxsd/kscj/cjcx_list')
#
#     result = {}
#     if re.findall(reg, response.text):
#         result['code'] = 500
#         result['msg'] = '账户或密码错误'
#     else:
#         result['code'] = 200
#         result['msg'] = '登陆成功'
#
#     return json.dumps(result)

"""

 -*- coding: utf-8 -*-
Time    : 2019/7/19 8:25
Author  : Hansybx

"""


class Res:
    code = 200
    msg = ''
    info = {}

    def __init__(self, code, msg, info):
        self.code = code
        self.msg = msg
        self.info = info

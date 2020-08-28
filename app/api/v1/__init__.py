"""

 -*- coding: utf-8 -*-
Time    : 2019/7/16 18:34
Author  : Hansybx

"""

from flask import Blueprint

# 定义一个蓝图
v1 = Blueprint('v1', __name__)

from app.api.v1.stu import stu
from app.api.v1.mobile import mobile
from app.api.v1.xsbook import xsbook
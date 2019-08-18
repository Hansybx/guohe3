"""

 -*- coding: utf-8 -*-
Time    : 2019/7/19 8:15
Author  : Hansybx

"""

from flask import Blueprint

# 定义一个蓝图
stu = Blueprint('stu', __name__)

from app.api.v1.stu import login, class_schedule, grade_point, \
    empty_classroom, sports, student_info, teacher_class, school_calendar,school_news


# 学生接口
@stu.route('/')
def hello():
    return 'hello'

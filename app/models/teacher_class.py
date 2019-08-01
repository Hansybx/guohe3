"""

 -*- coding: utf-8 -*-
Time    : 2019/7/27 15:49
Author  : Hansybx

"""
from sqlalchemy import Column, Integer, String

from app import db


class TeacherClass(db.Model):
    __tablename__ = 'teacher_class'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 周次
    week_time = Column(String(32), nullable=False)
    # 老师
    teacher = Column(String(32), nullable=False)
    # 学院
    academy = Column(String(32), nullable=False)
    # 节次
    class_order = Column(String(32), nullable=False)
    # 周几
    weekday = Column(String(32), nullable=False)
    # 课名
    class_name = Column(String(128), nullable=False)
    # 班级号
    class_num = Column(String(64), nullable=False)
    # 教室
    classroom = Column(String(32), nullable=False)
    semester = Column(String(32), nullable=False)

    def __init__(self, teacher, academy, week_time, class_order,
                 weekday, class_name, class_num, classroom, semester):
        self.teacher = teacher
        self.academy = academy
        self.week_time = week_time
        self.class_order = class_order
        self.weekday = weekday
        self.class_name = class_name
        self.class_num = class_num
        self.classroom = classroom
        self.semester = semester

    def serialize(self):
        return {
            'teacher': self.teacher, 'class_order': self.class_order,
            'class_name': self.class_name, 'class_num': self.class_num,
            'week_time': self.week_time, 'classroom': self.classroom,
            'weekday': self.weekday, 'academy': self.academy
        }

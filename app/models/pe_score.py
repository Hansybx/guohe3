"""

 -*- coding: utf-8 -*-
Time    : 2019/8/2 21:06
Author  : Hansybx

"""

from sqlalchemy import Column, Integer, String

from app import db


class PEScore(db.Model):
    __tablename__ = 'pe_score'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 学号
    uid = Column(String(32), primary_key=True)
    # 学期
    semester = Column(String(32), primary_key=True)
    # 课程名称
    class_name = Column(String(32), primary_key=True)
    # 上课时间
    time = Column(String(32), primary_key=True)
    # 老师
    teacher = Column(String(32), primary_key=True)
    # 体育几
    class_order = Column(String(32), primary_key=True)
    # 成绩
    grade = Column(String(32), primary_key=True)

    def __init__(self, uid, semester, class_name, time, teacher, class_order, grade):
        self.uid = uid
        self.semester = semester
        self.class_name = class_name
        self.time = time
        self.teacher = teacher
        self.class_order = class_order
        self.grade = grade

    def serialize(self):
        return {
            'uid': self.uid,
            'semester': self.semester,
            'class_name': self.class_name,
            'time': self.time,
            'teacher': self.teacher,
            'class_order': self.class_order,
            'grade': self.grade
        }

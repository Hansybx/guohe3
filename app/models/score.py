"""

 -*- coding: utf-8 -*-
Time    : 2019/8/1 9:27
Author  : Hansybx

"""
from sqlalchemy import Column, Integer, String

from app import db


class Score(db.Model):
    __tablename__ = 'score'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 学号
    uid = Column(String(32), primary_key=True)
    # 学期
    semester = Column(String(32), nullable=False)
    # 课名
    class_name = Column(String(32), nullable=False)
    # 成绩
    grade = Column(String(32), nullable=False)
    # 学分
    grade_point = Column(String(32), nullable=False)
    # 考试类型
    class_test_type = Column(String(32), nullable=False)
    # 课程类型
    class_type = Column(String(32), nullable=False)

    def __init__(self, uid, semester, class_name, grade,
                 grade_point, class_test_type, class_type):
        self.uid = uid
        self.semester = semester
        self.class_name = class_name
        self.grade = grade
        self.grade_point = grade_point
        self.class_test_type = class_test_type
        self.class_type = class_type

    def serialize(self):
        return {
            'uid': self.uid,
            'semester': self.semester,
            'class_name': self.class_name,
            'grade': self.grade,
            'grade_point': self.grade_point,
            'class_test_type': self.class_test_type,
            'class_type': self.class_type
        }

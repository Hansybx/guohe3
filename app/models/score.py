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
    start_semester = Column(String(32), nullable=False)
    # 课名
    course_name = Column(String(32), nullable=False)
    # 成绩
    score = Column(String(32), nullable=False)
    # 学分
    credit = Column(String(32), nullable=False)
    # 考试类型
    examination_method = Column(String(32), nullable=False)
    # 课程类型
    course_attribute = Column(String(32), nullable=False)
    alternative_course_number = Column(String(32), nullable=False)
    alternative_course_name = Column(String(32), nullable=False)
    mark_of_score = Column(String(32), nullable=False)

    def __init__(self, uid, start_semester, course_name, score,
                 credit, examination_method, course_attribute,
                 alternative_course_number, alternative_course_name, mark_of_score):
        self.uid = uid
        self.start_semester = start_semester
        self.course_name = course_name
        self.score = score
        self.credit = credit
        self.examination_method = examination_method
        self.course_attribute = course_attribute
        self.alternative_course_number = alternative_course_number
        self.alternative_course_name = alternative_course_name
        self.mark_of_score = mark_of_score

    def serialize(self):
        return {
            'uid': self.uid,
            'start_semester': self.start_semester,
            'course_name': self.course_name,
            'score': self.score,
            'credit': self.credit,
            'examination_method': self.examination_method,
            'course_attribute': self.course_attribute,
            'alternative_course_number': self.alternative_course_number,
            'alternative_course_name': self.alternative_course_name,
            'mark_of_score': self.mark_of_score
        }

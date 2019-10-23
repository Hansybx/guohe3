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
    startSemester = Column(String(32), nullable=False)
    # 课名
    courseName = Column(String(32), nullable=False)
    # 成绩
    score = Column(String(32), nullable=False)
    # 学分
    credit = Column(String(32), nullable=False)
    # 考试类型
    examinationMethod = Column(String(32), nullable=False)
    # 课程类型
    courseAttribute = Column(String(32), nullable=False)
    alternativeCourseNumber = Column(String(32), nullable=False)
    alternativeCourseName = Column(String(32), nullable=False)
    markOfScore = Column(String(32), nullable=False)

    def __init__(self, uid, startSemester, courseName, score,
                 credit, examinationMethod, courseAttribute,
                 alternativeCourseNumber, alternativeCourseName, markOfScore):
        self.uid = uid
        self.startSemester = startSemester
        self.courseName = courseName
        self.score = score
        self.credit = credit
        self.examinationMethod = examinationMethod
        self.courseAttribute = courseAttribute
        self.alternativeCourseNumber = alternativeCourseNumber
        self.alternativeCourseName = alternativeCourseName
        self.markOfScore = markOfScore

    def serialize(self):
        return {
            'uid': self.uid,
            'startSemester': self.startSemester,
            'courseName': self.courseName,
            'score': self.score,
            'credit': self.credit,
            'examinationMethod': self.examinationMethod,
            'courseAttribute': self.courseAttribute,
            'alternativeCourseNumber': self.alternativeCourseNumber,
            'alternativeCourseName': self.alternativeCourseName,
            'markOfScore': self.markOfScore
        }

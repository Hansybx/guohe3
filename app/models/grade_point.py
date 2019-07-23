"""

 -*- coding: utf-8 -*-
Time    : 2019/7/22 0:16
Author  : Hansybx

"""

from sqlalchemy import Column, Integer, String

from app import db


class GradePoint(db.Model):
    __tablename__ = 'GradePoint'
    # 学号
    uid = Column(String(32), primary_key=True)
    semester1 = Column(String(32), nullable=True)
    semester2 = Column(String(32), nullable=True)
    semester3 = Column(String(32), nullable=True)
    semester4 = Column(String(32), nullable=True)
    semester5 = Column(String(32), nullable=True)
    semester6 = Column(String(32), nullable=True)
    semester7 = Column(String(32), nullable=True)
    semester8 = Column(String(32), nullable=True)
    average = Column(String(32), nullable=True)

    def __init__(self, uid, average, semester1, semester2, semester3,
                 semester4, semester5, semester6, semester7, semester8):
        self.uid = uid
        self.average = average
        self.semester1 = semester1
        self.semester2 = semester2
        self.semester3 = semester3
        self.semester4 = semester4
        self.semester5 = semester5
        self.semester6 = semester6
        self.semester7 = semester7
        self.semester8 = semester8

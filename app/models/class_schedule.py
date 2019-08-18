"""

 -*- coding: utf-8 -*-
Time    : 2019/7/28 13:38
Author  : Hansybx

"""
from sqlalchemy import Integer, Column, String, Boolean

from app import db


class ClassSchedule(db.Model):
    __tablename__ = 'class_schedule'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 学号
    uid = Column(String(32), primary_key=True)
    # 周次
    week_time = Column(String(32), nullable=False)
    # 上课周次
    # class_week = Column(String(32), nullable=False)
    # 教室
    # class_address = Column(String(32), nullable=False)
    # 学期
    semester = Column(String(32), nullable=False)
    # 节次
    class_order = Column(String(32), nullable=False)
    # 周几
    weekday = Column(String(32), nullable=False)
    # 课名
    # class_name = Column(String(32), nullable=False)
    # 课程号
    # class_num = Column(String(32), nullable=False)
    # 老师
    # class_teacher = Column(String(32), nullable=False)
    # 状态 标记删除 0未删除 1 删除
    status = Column(Integer, nullable=False)
    news = Column(String(64), nullable=False)

    #  class_address,class_name, class_num, class_teacher,

    def __init__(self, uid, week_time, class_week, semester,
                 class_order, weekday, status, news):
        self.uid = uid
        self.week_time = week_time
        self.class_week = class_week
        # self.class_address = class_address
        self.semester = semester
        self.class_order = class_order
        self.weekday = weekday
        # self.class_name = class_name
        # self.class_num = class_num
        # self.class_teacher = class_teacher
        self.status = status
        self.news = news

    def serialize(self):
        week_list = ['monday', 'tuesday', 'wednesday', 'thursday',
                     'friday', 'saturday', 'sunday']
        return {
            # 'class_name': self.class_name,
            # 'class_address': self.class_address,
            # 'class_teacher': self.class_teacher,
            # 'class_num': self.class_num,
            week_list[int(self.weekday)-1]: self.news,
            # 'weekday': self.weekday,
            # 'class_order': self.class_order
        }

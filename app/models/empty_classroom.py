"""

 -*- coding: utf-8 -*-
Time    : 2019/7/31 21:09
Author  : Hansybx

"""
from sqlalchemy import Column, Integer, String, SmallInteger

from app import db


class ClassroomEmpty(db.Model):
    __bind_key__ = 'guohe'
    __tablename__ = 'empty_classroom'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 周次
    week_time = Column(SmallInteger, nullable=False)
    # 教室
    class_address = Column(String(32), nullable=False)
    # 学期
    semester = Column(String(32), nullable=False)
    # 节次
    class_order = Column(SmallInteger, nullable=False)
    # 周几
    weekday = Column(SmallInteger, nullable=False)
    # 校区
    area = Column(String(32), nullable=False)
    # 教学楼
    building_id = Column(SmallInteger, nullable=False)
    # 状态 标记删除 0未删除 1 删除
    status = Column(Integer, nullable=False)

    def __init__(self, week_time, class_address, semester, area,
                 building_id, class_order, weekday, status):
        self.week_time = week_time
        self.class_address = class_address
        self.semester = semester
        self.class_order = class_order
        self.weekday = weekday
        self.area = area
        self.building_id = building_id
        self.status = status

    def serialize(self):
        return {
            'time': self.class_order,
            'weekday': self.weekday,
            'place': self.class_address
        }

"""

 -*- coding: utf-8 -*-
Time    : 2019/7/21 14:10
Author  : Hansybx

"""
from sqlalchemy import Column, Integer, String

from app import db
from app.utils.common_utils import md5, get_date_now


class StudentInfo(db.Model):
    __tablename__ = 'StudentInfo'
    # 学号
    uid = Column(Integer, primary_key=True)
    # 密码
    password = Column(String(100), nullable=False)
    # 姓名
    name = Column(String(64), nullable=False)
    # 生日
    birthday = Column(String(36), nullable=True)
    # 专业
    major = Column(String(100), nullable=False)
    # 学院
    academy = Column(String(100), nullable=False)
    # 班级
    class_num = Column(String(100), nullable=False)
    # 身份证号
    identity_card_number = Column(String(100), nullable=False)
    # 性别
    sex = Column(String(50), nullable=False)
    # 创建日期
    # create_time = Column(String(100), nullable=False)
    # 更新日期
    updated_time = Column(String(100), nullable=False)

    def __init__(self, uid, password, name, birthday, major, academy,
                 class_num, identity_card_num, sex):
        self.uid = uid
        self.password = md5(password)
        self.name = name
        self.birthday = birthday
        self.major = major
        self.academy = academy
        self.class_num = class_num
        self.identity_card_number = identity_card_num
        self.sex = sex
        # self.create_time = get_date_now()
        self.updated_time = get_date_now()

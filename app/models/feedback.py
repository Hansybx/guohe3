from sqlalchemy import Column, Integer, String

from app.models import db

__author__ = 'lyy'


class FeedBack(db.Model):
    __bind_key__ = 'guohe'
    # 反馈记录的id
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 反馈人的uid
    # uid = Column(String(50), nullable=False)
    # 反馈的内容
    content = Column(String(50), nullable=False)
    # 反馈的图片
    # pic = Column(String(1000), nullable=False)
    # 反馈人的联系方式
    contact = Column(String(50), nullable=False)
    # 反馈的来源
    origin = Column(Integer, nullable=False)

    def __init__(self, content, contact, origin):
        self.content = content
        self.contact = contact
        # self.pic = pic
        self.origin = origin

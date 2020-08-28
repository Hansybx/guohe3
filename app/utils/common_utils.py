"""

 -*- coding: utf-8 -*-
Time    : 2019/7/12 14:25
Author  : Hansybx

"""
import datetime
import hashlib
import random
import time

from sqlalchemy import create_engine

from app import db
from app.secure import SQLALCHEMY_BINDS


def md5(word):
    # 创建md5对象
    h = hashlib.md5()

    # Tips
    # 此处必须声明encode
    # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
    h.update(bytes(word, encoding='utf-8'))

    # print('MD5加密前为 ：' + word)
    # print('MD5加密后为 ：' + h.hexdigest())
    return h.hexdigest()


# 获取今天的日期
def get_today():
    return str(datetime.datetime.now().strftime("%Y/%m/%d"))


# 获取当前时间
def get_date_now():
    return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# 用时间生成一个唯一随机数
def get_ran_dom():
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
    random_num = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
    if random_num <= 10:
        random_num = str(0) + str(random_num)
    unique_num = str(now_time) + str(random_num)
    return unique_num


# 用时间生成一个唯一id
def unique_id():
    t = time.time()
    uid = str(int(t) + random.randrange(100, 999))[-6:] + str(random.randrange(100, 999))
    return int(uid)


# 添加到数据库
def put_to_mysql(key):
    try:
        db.session.add(key)
        db.session.commit()
    except Exception:
        db.session.rollback()


# 数据批量保存
def sql_to_execute(sql, value, bind):
    try:
        engine = create_engine(SQLALCHEMY_BINDS[bind])
        db.session.execute(sql, value, bind=engine)
        db.session.commit()
    except Exception:
        db.session.rollback()


# 获取图片路径
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

if __name__ == '__main__':
    # 待加密信息
    a = 'this is a md5 test.'
    md5(a)

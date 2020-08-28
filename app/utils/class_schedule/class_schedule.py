"""

 -*- coding: utf-8 -*-
Time    : 2019/7/15 21:49
Author  : Hansybx

"""
import re

from bs4 import BeautifulSoup
from flask import jsonify

from app.models import db
from app.models.class_schedule import ClassSchedule
from app.models.error import AuthFailed, PasswordFailed
from app.utils.common_utils import sql_to_execute
from app.utils.login.login_util import login


# 课程是否在数据库中
def class_in_mysql(username, semester):
    data = ClassSchedule.query.filter(ClassSchedule.uid == username,

                                      ClassSchedule.semester == semester).first()
    return data


# 删除原始课表数据
def class_in_sql_update(username, semester):
    ClassSchedule.query.filter(ClassSchedule.uid == username,
                               ClassSchedule.semester == semester,
                               ClassSchedule.status == 0).update({'status': 1})
    db.session.commit()


# 对应星期筛查
def order_query_mysql(username, semester, class_order):
    data = ClassSchedule.query.filter(ClassSchedule.uid == username,
                                      ClassSchedule.semester == semester, ClassSchedule.status == 0,
                                      ClassSchedule.class_order == class_order).all()
    order_dic = {}
    res = jsonify(data=[i.serialize() for i in data]).json['data']
    for temp in res:
        order_dic.update(temp)
    return order_dic


# 课表爬取
def update_class_schedule(username, password, semester):
    reg = r'<font color="red">请先登录系统</font>'
    session = login(username, password)

    url = "http://jwgl.just.edu.cn:8080/jsxsd/xskb/xskb_list.do"
    paramrs = {'xnxq01id': semester}
    response = session.get(url, params=paramrs)

    if re.findall(reg, response.text):
        raise PasswordFailed
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, "html.parser")

    # tr存储每一行的课程
    trs = soup.html.select('#kbtable tr .kbcontent')

    if not trs:
        # 未评价
        raise AuthFailed

    i = 0

    sql = "insert into class_schedule(uid,  semester," \
          "class_order, weekday,status,news)" \
          "values (:uid,  :semester," \
          ":class_order, :weekday,:status,:news)"

    value = []
    for tr in trs:
        i += 1
        # value.append(class_in_tr(tr, zc, i, username, semester))

        temp = class_in_tr(tr, i, username, semester)
        if temp['news']:
            value.append(temp)

    more = soup.html.select('#kbtable tr td ')
    if more[35].text:
        value.append({
            'uid': username,
            'semester': semester,
            'status': 0,
            'news': more[35].text,
            'class_order': 6,
            'weekday': 0
        })
    if value:
        sql_to_execute(sql, value, "guohe")


# 星期几的课
def class_in_weekday(username, semester):
    week_list_class = []
    temp = {}
    for i in range(1, 7):
        week_list_class.append(order_query_mysql(username, semester, i))

    if week_list_class:
        return week_list_class


# 当前周次的课表, 学期 周次 单周
def get_class_schedule_week(username, password, semester):
    week_list = {}
    flag = class_in_mysql(username, semester)
    if flag:
        week_list = class_in_weekday(username, semester)
    else:
        week_list = get_class_schedule_week_update(username, password, semester, True)

    return week_list


# 更新当前周次的课表, 学期 周次 单周
def get_class_schedule_week_update(username, password, semester, update=False):
    if update:
        class_in_sql_update(username, semester)
        update_class_schedule(username, password, semester)
        week_list = class_in_weekday(username, semester)
        return week_list
    else:
        return get_class_schedule_week(username, password, semester)


def class_in_tr(tr, i, username, semester, flag=0):
    class_list = {
        'uid': username,
        # 'week_time': zc,
        'semester': semester,
        # 'class_num': '',
        # 'class_name': '',
        # 'class_teacher': '',
        # 'class_week': '',
        # 'class_address': '',
        'status': 0,
        'news': '',
        'class_order': (i - 1) // 7 + 1 if i % 7 != 0 else i // 7,
        'weekday': i % 7 if i % 7 != 0 else 7
    }

    news = ''
    news = class_in_tr_method(tr, flag)
    # class_in_tr_method
    class_list['news'] = news

    return class_list


# tr 子元素通用减少num
def class_in_tr_method(tr, flag):
    temp = 0
    if len(tr.text) > 1:
        class_info = tr.contents

        # 课程名
        # class_list['class_name'] = class_info[2]
        class_name = class_info[2 - flag]
        # 授课教师
        # class_list['class_teacher'] = class_info[4].text
        class_teacher = class_info[4 - flag].text
        # 上课周次
        # class_list['class_week'] = class_info[6].text
        class_week = class_info[6 - flag].text

        news = '@' + class_name + '@' + class_teacher + '@' + class_week

        class_address = ''
        if len(class_info) > (8 - flag) and '---------------------' not in class_info[8 - flag]:
            # if len(class_info) > 8 - flag:
            # 对应教室
            # class_list['class_address'] = class_info[8].text
            class_address = class_info[8 - flag].text
            news += '@' + class_address
        else:
            temp = 2

        if flag == 0:
            # 课程号
            # class_list['class_num'] = class_info[0]
            class_num = class_info[0]
            news = class_num + news
        a = len(class_info)
        if len(class_info) > (10 - flag - temp) and '---------------------' in class_info[10 - flag - temp]:
            news += '@---------------------' + class_info[12 - flag - temp]
            news += class_in_tr_method(class_info[13 - flag - temp], 2)
        return news

    # class_list = {
    # 'class_num': class_num,
    # 'class_name': class_name,
    # 'class_teacher': class_teacher,
    # 'class_week': class_week,
    # 'class_address': class_address,
    #     'week_time': zc,
    #     'class_order': i % 5 if i % 5 != 0 else 5,
    #     'weekday': i % 5 if i % 5 != 0 else i // 5
    # }

    # sql = "insert into class_schedule(uid, week_time, class_week, class_address, semester," \
    #       "class_order, weekday, class_name, class_num)" \
    #       "values ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
    #       % (uid, week_time, class_list['class_week'], class_list['class_address'],
    #          semester, class_list['class_order'], class_list['weekday'],
    #          class_list['class_name'], class_list['class_num']) % (uid, week_time, class_list['class_week'], class_list['class_address'],semester, class_list['class_order'], class_list['weekday'],class_list['class_name'], class_list['class_num'])
    # db.session.excute(sql)
    # db.session.commit()


if __name__ == '__main__':
    a = get_class_schedule_week('182210711114', 'hanzy2000', '2019-2020-1')
    print(a)

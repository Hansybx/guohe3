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
def class_in_mysql(username, zc, semester):
    data = ClassSchedule.query.filter(ClassSchedule.uid == username,
                                      ClassSchedule.week_time == zc,
                                      ClassSchedule.semester == semester).first()
    return data


# 删除原始课表数据
def class_in_sql_update(username, zc, semester):
    ClassSchedule.query.filter(ClassSchedule.uid == username,
                               ClassSchedule.week_time == zc,
                               ClassSchedule.semester == semester,
                               ClassSchedule.status == 0).update({'status': 1})
    db.session.commit()


# 对应星期筛查
def weekday_query_mysql(username, zc, semester, weekday):
    data = ClassSchedule.query.filter(ClassSchedule.uid == username, ClassSchedule.week_time == zc,
                                      ClassSchedule.semester == semester,
                                      ClassSchedule.weekday == weekday).order_by(ClassSchedule.class_order).all()
    return jsonify(data=[i.serialize() for i in data])


# 课表爬取
def update_class_schedule(username, password, semester, zc):
    reg = r'<font color="red">请先登录系统</font>'
    session = login(username, password)

    url = "http://jwgl.just.edu.cn:8080/jsxsd/xskb/xskb_list.do"
    paramrs = {'zc': str(zc), 'xnxq01id': semester}
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
    sql = "insert into class_schedule(uid, week_time, class_week, class_address, semester," \
          "class_order, weekday, class_name, class_num,class_teacher,status)" \
          "values (:uid, :week_time, :class_week, :class_address, :semester," \
          ":class_order, :weekday, :class_name, :class_num,:class_teacher,:status)"
    value = []
    for tr in trs:
        i += 1
        value.append(class_in_tr(tr, zc, i, username, semester))

    sql_to_execute(sql, value)


# 星期几的课
def class_in_weekday(username, zc, semester):
    monday = weekday_query_mysql(username, zc, semester, 1).json['data']
    tuesday = weekday_query_mysql(username, zc, semester, 2).json['data']
    wednesday = weekday_query_mysql(username, zc, semester, 3).json['data']
    thursday = weekday_query_mysql(username, zc, semester, 4).json['data']
    friday = weekday_query_mysql(username, zc, semester, 5).json['data']
    saturday = weekday_query_mysql(username, zc, semester, 6).json['data']
    sunday = weekday_query_mysql(username, zc, semester, 7).json['data']

    week_list = {'monday': monday,
                 'tuesday': tuesday,
                 'wednesday': wednesday,
                 'thursday': thursday,
                 'friday': friday,
                 'saturday': saturday,
                 'sunday': sunday}
    return week_list


# 当前周次的课表, 学期 周次 单周
def get_class_schedule_week(username, password, semester, zc):
    week_list = {}
    flag = class_in_mysql(username, zc, semester)
    if flag:
        week_list = class_in_weekday(username, zc, semester)
    else:
        week_list = get_class_schedule_week_update(username, password, semester, zc)

    return week_list


# 更新当前周次的课表, 学期 周次 单周
def get_class_schedule_week_update(username, password, semester, zc):
    class_in_sql_update(username, zc, semester)
    update_class_schedule(username, password, semester, zc)
    week_list = class_in_weekday(username, zc, semester)
    return week_list


def class_in_tr(tr, zc, i, username, semester):
    class_list = {
        'uid': username,
        'week_time': zc,
        'semester': semester,
        'class_num': '',
        'class_name': '',
        'class_teacher': '',
        'class_week': '',
        'class_address': '',
        'status': 0,
        'week_time': zc,
        'class_order': (i - 1) // 7 + 1 if i % 7 != 0 else i // 7,
        'weekday': i % 7 if i % 7 != 0 else 7
    }
    if len(tr.text) > 1:
        class_info = tr.contents
        # 课程号
        class_list['class_num'] = class_info[0]
        # 课程名
        class_list['class_name'] = class_info[2]
        # 授课教师
        class_list['class_teacher'] = class_info[4].text
        # 上课周次
        class_list['class_week'] = class_info[6].text

        if len(class_info) > 8:
            # 对应教室
            class_list['class_address'] = class_info[8].text

    return class_list
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
    a = get_class_schedule_week('182210711114', 'hanzy2000', '2019-2020-1', '1')
    print(a)

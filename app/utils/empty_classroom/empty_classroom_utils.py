"""

 -*- coding: utf-8 -*-
Time    : 2019/7/18 17:14
Author  : Hansybx

"""
import re

from bs4 import BeautifulSoup
from flask import jsonify

from app.models.empty_classroom import ClassroomEmpty
from app.models.error import PasswordFailed
from app.utils.common_utils import sql_to_execute
from app.utils.login.login_util import login

"""
jzwid
东区综合楼B ：2
东区综合楼C ：3
东区综合楼D ：4
东区教学楼3 ：5
东区教学楼4 ：6
东区实验楼11 ：7
外训楼 ：17
南区第一综合楼 ：12
南区第二综合楼 ：23
西区综合楼 ：10
西区图书馆 ：11
张教学楼E ：26
张教学楼F ：27
冶材计算机机房 ：F04D29270E084926AA4FB1BC312DFDE7
张教学楼A ：18
张教学楼B : 19
张教学楼C : 20
张教学楼D : 21


xqid
东校区 01
西校区 03
南校区 02
"""


# 学期，校区，教学楼，周次
def empty_classroom(username, password, semester, area_id, building_id, week):
    data_list = []
    data_list = query_empty_classroom(semester, area_id, building_id, week)
    if data_list:
        return data_list.json['data']
    else:
        session = login(username, password)
        room_list = []

        url = "http://jwgl.just.edu.cn:8080/jsxsd/kbcx/kbxx_classroom_ifr"
        week = int(week)
        paramrs = {'xnxqh': semester,
                   'skyx': '',
                   'xqid': area_id,
                   'jzwid': building_id,
                   'zc1': str(week),
                   'zc2': str(week + 1),
                   'jc1': '',
                   'jc2': ''}

        response = session.get(url, params=paramrs)

        reg = r'<font color="red">请先登录系统</font>'
        if re.findall(reg, response.text):
            raise PasswordFailed

        soup = BeautifulSoup(response.text, "html.parser")
        trs = soup.select('table tr')
        room_list = tr_in_trs(trs, semester, area_id, building_id, week)
        if room_list:
            sql = "insert into empty_classroom(class_address,class_order,weekday,status," \
                  "week_time,  semester, area,building_id)" \
                  "values (:classroom, :class_order, :weekday, :status," \
                  ":week_time, :semester, :area,:building_id)"
            sql_to_execute(sql, room_list)
        data_list = query_empty_classroom(semester, area_id, building_id, week)
        return data_list.json['data']


def tr_in_trs(trs, semester, area_id, building_id, week):
    # 空教室列表
    room_list = []

    for tr in trs[2:]:
        tds = tr.select('td')
        i = -1
        classroom = ''
        for td in tds[:1]:
            classroom = td.contents[1].text
        for td in tds[1:]:
            i += 1
            if len(td.contents[1].contents) <= 1:
                # 星期几
                weekday = i // 5 + 1
                # 课节
                class_order = ((i + 1) % 5) if (i + 1) % 5 != 0 else 5
                room_list.append({'classroom': classroom, 'weekday': str(weekday),
                                  'class_order': str(class_order), 'status': 0,
                                  'week_time': str(week), 'semester': semester,
                                  'area': area_id, 'building_id': building_id})

    return room_list


def query_empty_classroom(semester, area_id, building_id, week):
    data = ClassroomEmpty.query.filter(ClassroomEmpty.semester == semester,
                                       ClassroomEmpty.area == area_id,
                                       ClassroomEmpty.building_id == building_id,
                                       ClassroomEmpty.week_time == week,
                                       ClassroomEmpty.status == 0).all()
    if data:
        return jsonify(data=[i.serialize() for i in data])
    else:
        return None


if __name__ == '__main__':
    empty_classroom('182210711114', 'hanzy2000', '2019-2020-1', '01', '5', '1')

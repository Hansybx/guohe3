"""

 -*- coding: utf-8 -*-
Time    : 2019/7/15 21:49
Author  : Hansybx

"""
import re

from bs4 import BeautifulSoup

from app.utils.login.login import login


def get_class_schedule(username, password, semester):
    pass


# 当前周次的课表
def get_class_schedule_week(username, password, semester, zc):
    reg = r'<font color="red">请先登录系统</font>'
    session = login(username, password)
    data_list = []

    url = "http://jwgl.just.edu.cn:8080/jsxsd/xskb/xskb_list.do"
    paramrs = {'zc': str(zc), 'xnxq01id': semester}
    response = session.get(url, params=paramrs)

    if re.findall(reg, response.text):
        print(1)
    response.encoding = 'utf-8'


    soup = BeautifulSoup(response.text, "html.parser")

    # tr存储每一行的课程
    trs = soup.html.select('#kbtable tr .kbcontent')
    if not trs :
        a = 1
        # 未评价
    for tr in trs:
        data_list.append(class_in_tr(tr))

    monday = []
    tuesday = []
    wednesday = []
    thursday = []
    friday = []
    saturday = []
    sunday = []
    for i in range(0, 35, 7):
        monday.append(data_list[i])
        tuesday.append(data_list[i + 1])
        wednesday.append(data_list[i + 2])
        thursday.append(data_list[i + 3])
        friday.append(data_list[i + 4])
        saturday.append(data_list[i + 5])
        sunday.append(data_list[i + 6])

    week_list = {'monday': monday,
                 'tuesday': tuesday,
                 'wednesday': wednesday,
                 'thursday': thursday,
                 'friday': friday,
                 'saturday': saturday,
                 'sunday': sunday}
    return week_list


def class_in_tr(tr):
    class_list = {
        'class_num': '',
        'class_name': '',
        'class_teacher': '',
        'class_week': '',
        'class_address': ''
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




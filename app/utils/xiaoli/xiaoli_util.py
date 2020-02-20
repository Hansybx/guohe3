"""

 -*- coding: utf-8 -*-
Time    : 2019/8/11 16:27
Author  : Hansybx

"""
import datetime
import re

import requests
from bs4 import BeautifulSoup

from app.models.error import PasswordFailed
from app.utils.login.login_util import login


def get_calendar(username, password):
    result = {}
    start_day, end_day = time_get(username, password)
    begin_year, begin_week = str2time(start_day)
    end_year, end_week = str2time(end_day)
    last_week = last_week_get(begin_year)

    temp = datetime.datetime.now().isocalendar()
    now_year = temp[0]
    now_week = temp[1]
    now_day = temp[2]
    result['weekDay'] = to_weekday(now_day)
    result['weekDayNum'] = now_day
    result['today'] = datetime.date.today().isoformat()

    all_year = []
    start = int('20' + username[0:2])
    end = int(begin_year)

    if begin_week > 32:
        all_year.append(str(end) + '-' + str(end + 1) + '-1')

    while start < end:
        all_year.append(str(end - 1) + '-' + str(end) + '-2')
        all_year.append(str(end - 1) + '-' + str(end) + '-1')
        end -= 1
    result['allYear'] = all_year

    if now_year > begin_year:
        current_week = last_week - begin_week + 1 + now_week

    else:
        current_week = now_week - begin_week + 1

    if current_week > 20:
        current_week = 20
    result['weekNum'] = current_week
    return result


def time_get(username, password):
    reg = r'<font color="red">请先登录系统</font>'
    session = login(username, password)
    response = session.get('http://jwgl.just.edu.cn:8080/jsxsd/jxzl/jxzl_query?Ves632DSdyV=NEW_XSD_WDZM')
    if re.findall(reg, response.text):
        raise PasswordFailed
    soup = BeautifulSoup(response.text, "html.parser")
    b = soup.find_all('td', title=True)
    start_day = b[0]['title']
    end_day = b[-1]['title']
    return start_day, end_day


def str2time(time_str):
    time_info = re.split('[\u4e00-\u9fa5]', time_str)
    return int(time_info[0]), datetime.date(int(time_info[0]), int(time_info[1]), int(time_info[2])).isocalendar()[1]


def last_week_get(year):
    day = 31
    month = 12
    week = datetime.date(year, month, day).isocalendar()[1]
    while week == 1:
        day -= 1
        week = datetime.date(year, month, day).isocalendar()[1]
    return week


def to_weekday(tab):
    current_tab = ''
    if tab == 1:
        current_tab = '星期一'
    if tab == 2:
        current_tab = '星期二'
    if tab == 3:
        current_tab = '星期三'
    if tab == 4:
        current_tab = '星期四'
    if tab == 5:
        current_tab = '星期五'
    if tab == 6:
        current_tab = '星期六'
    if tab == 7:
        current_tab = '星期日'

    return current_tab


if __name__ == '__main__':
    a = get_calendar('182210711114', 'hanzy2000')
    print(a)

"""

 -*- coding: utf-8 -*-
Time    : 2019/8/11 16:27
Author  : Hansybx

"""
import datetime

import requests
from bs4 import BeautifulSoup


def get_school_calendar(username, password):
    result = {}
    begintime, endtime = time_get()

    begin_year, begin_week = str_to_time(begintime)
    end_year, end_week = str_to_time(endtime)
    last_week = lastweek_get(begin_year)

    temp = datetime.datetime.now().isocalendar()
    now_week = temp[1]
    now_day = temp[2]
    result['week'] = to_weekday(now_day)
    result['today'] = datetime.date.today().isoformat()

    all_year = []
    start = int('20' + username[0:2])
    end = int(begin_year)
    while start < end:
        all_year.append(str(start) + '-' + str(start + 1) + '-1')
        all_year.append(str(start) + '-' + str(start + 1) + '-2')
        start += 1
    all_year.append(str(start) + '-' + str(start + 1) + '-1')
    result['all_year'] = all_year

    if end_year > begin_year:
        current_week = last_week - begin_week + 1 + now_week

    else:
        current_week = now_week - begin_week + 1

    if current_week > 20:
        current_week = 20
    result['weekNum'] = current_week

    return result


def time_get():
    response = requests.get('http://jwc.just.edu.cn/')
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")
    element = soup.find('div', id='teachWeekly')
    begintime = element['begintime']
    endtime = element['endtime']
    return begintime, endtime


def str_to_time(time_str):
    year = int(time_str[0:4])
    month = int(time_str[4:6])
    day = int(time_str[6:9])
    return year, datetime.date(year, month, day).isocalendar()[1]


def lastweek_get(year):
    day = 31
    month = 12
    week = datetime.date(year, month, day).isocalendar()[1]
    while week == 1:
        day -= 1
        week = datetime.date(year, month, day).isocalendar()[1]
    return week


def to_weekday(tab):
    currentTab = ''
    if tab == 1:
        currentTab = '星期一'
    if tab == 2:
        currentTab = '星期二'
    if tab == 3:
        currentTab = '星期三'
    if tab == 4:
        currentTab = '星期四'
    if tab == 5:
        currentTab = '星期五'
    if tab == 6:
        currentTab = '星期六'
    if tab == 7:
        currentTab = '星期日'

    return currentTab


if __name__ == '__main__':
    get_xiaoli('168888', '2')

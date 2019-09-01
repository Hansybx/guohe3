"""

 -*- coding: utf-8 -*-
Time    : 2019/7/20 15:02
Author  : Hansybx

"""
import re

import requests
from bs4 import BeautifulSoup
from flask import jsonify

from app.models.error import PasswordFailed
from app.models.pe_score import PEScore
from app.utils.common_utils import put_to_mysql

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Origin': 'https://vpn.just.edu.cn',
    'Upgrade-Insecure-Requests': '1'
}


def sports_login(username, password):
    session = requests.session()
    sport_data = {

        'chkuser': 'true',
        'username': username,
        'password': password
    }
    session.post('http://tyxy.just.edu.cn/index1.asp', headers=headers,
                 data=sport_data, verify=False)
    return session


def html_get(username, password, url):
    session = sports_login(username, password)
    response = session.get(url, headers=headers, verify=False)

    response.encoding = 'gb2312'
    soup = BeautifulSoup(response.text, 'html.parser')
    temp = soup.select('body p p p')
    if '第 32 行发生错误 现在不允许操作用户界面' in str(temp[0].contents[0]):
        raise Exception
    trs = soup.select('form tr')

    if len(trs) > 0:
        return trs
    else:
        raise PasswordFailed


def html_get_score(username, password, url):
    session = sports_login(username, password)
    response = session.get(url, headers=headers, verify=False)

    response.encoding = 'gb2312'
    soup = BeautifulSoup(response.text, 'html.parser')
    trs = soup.select('td nobr')
    if len(trs) > 0:
        return trs
    else:
        raise PasswordFailed


def tr_in_trs_score(trs, username):
    data_list = []

    for i in range(int(len(trs)//7)):
        semester = trs[0 + i * 7].text
        class_name = trs[1 + i * 7].text
        time = trs[2 + i * 7].text
        teacher = trs[3 + i * 7].string
        class_order = trs[4 + i * 7].string
        grade = trs[5 + i * 7].string
        data_list.append({
            'uid': username,
            'semester': semester,
            'class_name': class_name,
            'time': time,
            'teacher': teacher,
            'class_order': class_order,
            'grade': grade
        })
        score_temp = PEScore(uid=username, semester=semester, class_name=class_name,time=time,
                             teacher=teacher, class_order=class_order, grade=grade)
        put_to_mysql(score_temp)

    return data_list


def query_in_sql(username):
    data = PEScore.query.filter(PEScore.uid == username).all()
    if data:
        return jsonify(data=[i.serialize() for i in data])
    else:
        return None
# semester
# class_name
# teacher
# class_order
# grade


def tr_in_trs(trs):
    data_list = []

    for tr in trs[1:-1]:
        # 序号
        num = tr.contents[0].text
        # 出勤日期
        date = tr.contents[1].text
        # 考勤时间
        time = tr.contents[2].text
        # 备注
        more = tr.contents[3].text
        data_list.append({
            'number': num,
            'date': date,
            'time': time,
            'more': more
        })
    temp = trs[-1].select('td')
    more = temp[0].contents[0]
    data_list.append({'total': more[:-2]})
    return data_list


# 早操出勤
def morning_attend(username, password):
    morning_attend_list = []
    # session = requests.session()
    # sport_data = {
    #
    #     'chkuser': 'true',
    #     'username': username,
    #     'password': password
    # }
    # session.post('http://tyxy.just.edu.cn/index1.asp', headers=headers,
    #              data=sport_data, verify=False)
    url = 'http://tyxy.just.edu.cn/zcgl/xskwcx.asp?action=zccx'

    trs = html_get(username, password, url)
    morning_attend_list = tr_in_trs(trs)
    return morning_attend_list


# 俱乐部出勤
def club_attend(username, password):
    club_attend_list = []
    url = 'http://tyxy.just.edu.cn/zcgl/xskwcx.asp?action=jlbcx'
    # session = sports_login(username, password)
    # response = session.get('http://tyxy.just.edu.cn/zcgl/xskwcx.asp?action=jlbcx',
    #                        headers=headers, verify=False)
    # response.encoding = 'gb2312'
    # soup = BeautifulSoup(response.text, 'html.parser')
    # trs = soup.select('form tr')

    trs = html_get(username, password, url)
    club_attend_list = tr_in_trs(trs)

    return club_attend_list


def sports_score(username, password):
    score_list = query_in_sql(username)
    if score_list:
        return score_list.json['data']
    else:
        url = 'http://tyxy.just.edu.cn/xsgl/cjcx.asp'
        trs = html_get_score(username, password, url)
        score_list = []
        score_list = tr_in_trs_score(trs, username)
        return score_list


if __name__ == '__main__':
    # morning_attend('182210101312', 'GY')
    # club_attend('172211802117', 'ZQQ')
    # club_attend('17221117', 'ZQQ')
    sports_score('172211802117', 'ZQQ')

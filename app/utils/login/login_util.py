"""

 -*- coding: utf-8 -*-
Time    : 2019/7/13 15:51
Author  : Hansybx

"""

import re

import requests
from bs4 import BeautifulSoup
from flask import jsonify

from app.models.error import PasswordFailed
from app.models.student_info import StudentInfo
from app.utils.common_utils import put_to_mysql

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    , 'Origin': 'https://vpn.just.edu.cn',
    'Upgrade-Insecure-Requests': '1'
}


def login(username, password):
    session = requests.session()
    cookies = {
        'lastRealm': 'LDAP-REALM',
        'DSSIGNIN': 'url_default',
        'WWHTJIKTLSN_Impl': 'javascript',
        'DSLastAccess': '1510459958'
    }
    try:
        session.post('http://jwgl.just.edu.cn:8080/jsxsd/xk/LoginToXk', headers=headers, cookies=cookies,
                     data={'USERNAME': username, 'PASSWORD': password}, verify=False)
    except Exception as e:
        raise e
    return session


def student_info(username, password):
    reg = r'<font color="red">请先登录系统</font>'
    session = login(username, password)
    response = session.get('http://jwgl.just.edu.cn:8080/jsxsd/grxx/xsxx?Ves632DSdyV=NEW_XSD_XJCJ')
    if re.findall(reg, response.text):
        raise PasswordFailed
    info = query_in_mysql(username)
    if info:
        return info
    else:
        return student_info_get(username, password, response)


def student_info_get(username, password, response):
    info = {}
    soup = BeautifulSoup(response.text, "html.parser")
    trs = soup.select('#xjkpTable tr')

    academy = trs[2].contents[1].contents[0][3:]
    info['academy'] = academy
    major = trs[2].contents[3].contents[0][3:]
    info['major'] = major
    classNum = trs[2].contents[7].contents[0][3:]
    info['classNum'] = classNum

    name = trs[3].contents[3].text
    info['name'] = name
    sex = trs[3].contents[7].text
    info['sex'] = sex
    birthday = trs[4].contents[3].text
    info['birthday'] = birthday
    identity_card_number = trs[47].contents[7].text
    info['identity_card_number'] = identity_card_number

    student = StudentInfo(username, password, name, birthday, major, academy,
                          classNum, identity_card_number, sex)
    put_to_mysql(student)

    return info


def query_in_mysql(username):
    data = StudentInfo.query.filter(StudentInfo.uid == username)
    if data:
        return jsonify(data=[i.serialize() for i in data]).json['data']


if __name__ == '__main__':
    student_info('182210711114', 'hanzy2000')

"""

 -*- coding: utf-8 -*-
Time    : 2019/7/13 15:51
Author  : Hansybx

"""
import datetime
import re

import requests
from bs4 import BeautifulSoup

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


if __name__ == '__main__':
    login('182210711114','hanzy200')


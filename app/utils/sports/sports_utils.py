"""

 -*- coding: utf-8 -*-
Time    : 2019/7/20 15:02
Author  : Hansybx

"""

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    , 'Origin': 'https://vpn.just.edu.cn',
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
    session = sports_login(username, password)
    response = session.get('http://tyxy.just.edu.cn/zcgl/xskwcx.asp?action=zccx',
                           headers=headers, verify=False)

    response.encoding = 'gb2312'
    soup = BeautifulSoup(response.text, 'html.parser')
    trs = soup.select('form tr')

    morning_attend_list = tr_in_trs(trs)
    return morning_attend_list


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
            'num': num,
            'date': date,
            'time': time,
            'more': more
        })
    temp = trs[-1].select('td')
    more = temp[0].contents[0]
    data_list.append({'more': more[:-2]})
    return data_list


# 俱乐部出勤
def club_attend(username, password):
    club_attend_list = []
    session = sports_login(username, password)
    response = session.get('http://tyxy.just.edu.cn/zcgl/xskwcx.asp?action=jlbcx',
                           headers=headers, verify=False)
    response.encoding = 'gb2312'
    soup = BeautifulSoup(response.text, 'html.parser')
    trs = soup.select('form tr')
    club_attend_list = tr_in_trs(trs)

    return club_attend_list


if __name__ == '__main__':
    # morning_attend('182210101312', 'GY')
    club_attend('172211802117', 'ZQQ')

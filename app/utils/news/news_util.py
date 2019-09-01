"""

 -*- coding: utf-8 -*-
Time    : 2019/8/11 18:15
Author  : Hansybx

"""
import datetime

import requests
from bs4 import BeautifulSoup


def get_news_url():
    timestamp = str(int(datetime.datetime.today().timestamp()))
    session = requests.session()
    url = 'http://notice.just.edu.cn/mobile/getPortalArticleList_1.mo?siteId=3&columnId=3&timeStamp=' + timestamp + '&beginIndex=0&pageSize=10&isCount=true&keyword=&_=' + timestamp
    response = session.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    news_list = eval(soup.contents[0])['data']['articles']
    url_list = []
    for news in news_list:
        url_list.append({'url': news['articleUrl'], 'title': news['title']})

    return url_list


def get_news_info(url):
    session = requests.session()
    res = session.get(url)
    news_soup = BeautifulSoup(res.text, "html.parser")
    article = str(news_soup.find(class_='article'))
    return article


if __name__ == '__main__':
    get_news_url()
    url = 'http://notice.just.edu.cn/_s3/2019/0722/c3a38930/page.psp'
    # get_news_info(url)

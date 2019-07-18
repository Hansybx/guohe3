"""

 -*- coding: utf-8 -*-
Time    : 2019/7/16 20:53
Author  : Hansybx

"""
import re

from bs4 import BeautifulSoup

from app.utils.login.login import login


# 成绩获取
def get_score(username, password):
    reg = r'<font color="red">请先登录系统</font>'
    session = login(username, password)
    response = session.get('http://jwgl.just.edu.cn:8080/jsxsd/kscj/cjcx_list')
    if re.findall(reg, response.text):
        pass
    soup = BeautifulSoup(response.text, "html.parser")
    trs = soup.select('table tr')[2:]

    a = trs[4].contents[1].contents[0]
    if a == '正在拼命加载中，请稍后...':
        # 未评价
        pass
    score_list = []
    for tr in trs:
        score_list.append(get_tr_in_trs(tr))
    return score_list


def get_tr_in_trs(tr):
    score_info = {'class_semester': '',
                  'class_name': '',
                  'class_score': '',
                  'class_point': '',
                  'class_test_type': '',
                  'class_type': ''}
    # 学期
    score_info['class_semester'] = tr.contents[3].text
    # 课程名
    score_info['class_name'] = tr.contents[7].text
    # 课程得分
    score_info['class_score'] = tr.contents[9].text
    # 学分
    score_info['class_point'] = tr.contents[11].text
    # 考试类型
    score_info['class_test_type'] = tr.contents[15].text
    # 课程类型
    score_info['class_type'] = tr.contents[17].text

    return score_info


# 成绩转换
def grade_to_num(score):
    if score.isdigit():
        grade = float(score) / 10 - 5
        return grade if grade > 0 else 0
    elif score == '优':
        return 4.5
    elif score == '良':
        return 3.5
    elif score == '中':
        return 2.5
    elif score == '及格':
        return 1.5
    elif score == '不及格':
        return 0
    elif score == '通过':
        return 2.5
    elif score == '不通过':
        return 0


# 绩点课程筛选
def grade_point_average(username, password):
    grade_point = 0
    grade = 0
    semester_list = {}
    filter_flag = ''

    score_list = get_score(username, password)
    semester_flag = score_list[0]['class_semester']
    for score in score_list:
        # 重修补考成绩在前，筛选
        if score['class_name'] == filter_flag:
            continue
        filter_flag = score['class_name']

        # 当前学期绩点判断
        if semester_flag != score['class_semester']:
            semester_list[semester_flag] = round((grade / grade_point), 2)
            semester_flag = score['class_semester']
            grade_point = 0
            grade = 0

        if score['class_name'].count('体育') < 1 and score['class_type'].count('任选') < 1:
            grade_point += float(score['class_point'])
            grade += grade_to_num(score['class_score']) * float(score['class_point'])

    semester_list[semester_flag] = round((grade / grade_point), 2)

    temp_grade = 0
    temp_semester = 0
    # 平均学分绩点
    for key, value in semester_list.items():
        temp_grade += value
        temp_semester += 1
    semester_list['all'] = round((temp_grade / temp_semester), 2)
    return semester_list


if __name__ == '__main__':
    # get_score('152210702119', '935377012pxc')
    # grade_point_average('182210711113', 'glhsjhy20010117')
    grade_point_average('182210711114', 'hanzy2000')

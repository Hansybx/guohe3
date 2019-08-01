"""

 -*- coding: utf-8 -*-
Time    : 2019/7/27 13:23
Author  : Hansybx

"""
from flask import jsonify

from app.models.teacher_class import TeacherClass
from app.utils.common_utils import sql_to_execute

import re

from bs4 import BeautifulSoup

from app.models.error import PasswordFailed
from app.utils.login.login_util import login
'''
<option value="01">[101]船舶与海洋工程学院</option>
<option value="02">[102]机械工程学院</option>
<option value="03">[103]电子信息学院</option>
<option value="04">[104]经济管理学院</option>
<option value="05">[105]理学院</option>
<option value="06">[106]材料科学与工程学院</option>
<option value="19">[107]计算机学院</option>
<option value="21">[108]能源与动力学院</option>
<option value="56">[109]土木工程与建筑学院</option>
<option value="08">[111]外国语学院</option>
<option value="09">[112]马克思主义学院、人文社科学院</option>
<option value="07">[114]体育学院</option>
<option value="57">[115]苏州理工学院</option>
<option value="m9hENYKoCc">   [11507]苏州理工学院教务处</option>
<option value="iyiyFni3HN">   [11508]苏州理工学院学生处</option>
<option value="AYGVASi5jD">   [11509]苏州理工学院图书馆</option>
<option value="NjLMBMZtbL">   [11510]苏州理工学院公共教育学院</option>
<option value="y0iB2WvgTy">   [11511]苏州理工学院船舶与建筑工程学院</option>
<option value="8RQCUBZp0Q">   [11512]苏州理工学院机电与动力工程学院</option>
<option value="HeIDTDBwYm">   [11513]苏州理工学院电气与信息工程学院</option>
<option value="Y7oT2nzN7f">   [11514]苏州理工学院商学院</option>
<option value="7D9p9cO1Hy">   [11515]苏州理工学院冶金与材料工程学院</option>
<option value="28">[117]苏州理工学院(镇江)</option>
<option value="31">[118]蚕业研究所、生物技术学院</option>
<option value="32">[119]环境与化学工程学院</option>
<option value="30">[120]生物技术学院</option>
<option value="mo8qYS7Hfh">[121]粮食学院</option>
<option value="16">[405]党委宣传部、统战部、法制办公室、社会主义学院新闻中心</option>
<option value="99">[412]教务处、高教所、工程训练中心</option>
<option value="cvofCBz7Cf">[418]深蓝学院</option>
<option value="77">[430]人民武装部、国防学院</option>
<option value="55">[434]张家港校区管委会</option>
<option value="Fv1v9YMuum">   [43410]张家港校区公共教育学院</option>
<option value="G0ouFOLFWO">   [43411]张家港校区船舶与建筑工程学院</option>
<option value="dCw4YdBhcs">   [43412]张家港校区机电与动力工程学院</option>
<option value="kWGK8x5IC4">   [43413]张家港校区电气与信息工程学院</option>
<option value="HyUfzsQN5r">   [43414]张家港校区商学院</option>
<option value="hMqgf269KJ">   [43415]张家港校区冶金与材料工程学院</option>
<option value="11">[502]后勤集团</option>
<option value="75">[75]工程训练中心</option>
</select>
'''


def tr_in_trs(trs, academy, semester, zc):
    data = []
    for tr in trs:

        tds = tr.select('nobr')
        # info['teacher']
        teacher = tds[0].text
        i = 0
        for td in tds[1:]:

            i += 1
            if '\r' not in td.text:
                # # 课节
                # info['class_order'] = i
                class_order = i if i <= 5 else i % 5
                weekday = (i - 1) // 5 + 1
                # # 课名
                # info['class_name'] = td.contents[1].contents[0]
                class_name = td.contents[1].contents[0]
                temp = td.contents[1].contents[2]
                pos = temp.find('\n')
                # # 班级
                # info['class_num'] = temp[:pos]
                class_num = temp[:pos]
                # # 周次
                # info['week_num'] = temp[pos + 1:]
                # week_num = temp[pos + 1:]
                # # 教室
                # info['classroom'] = td.contents[1].contents[4][1:-1]
                classroom = td.contents[1].contents[4][1:-1]

                data.append({'teacher': teacher, 'class_order': str(class_order),
                             'class_name': class_name, 'class_num': class_num,
                             'week_time': zc, 'classroom': classroom,
                             'weekday': str(weekday), 'academy': academy,
                             'semester': semester})
    return data


def get_teacher_class(username, password, semester, academy, zc):
    data_list = query_in_sql(academy, zc, semester)
    # data_list = None
    if data_list:
        return data_list.json['data']
    else:
        reg = r'<font color="red">请先登录系统</font>'
        session = login(username, password)

        url = "http://jwgl.just.edu.cn:8080/jsxsd/kbcx/kbxx_teacher_ifr"
        paramrs = {'xnxqh': semester, 'skyx': academy, 'zc1': zc, 'zc2': zc}
        response = session.get(url, params=paramrs)

        if re.findall(reg, response.text):
            raise PasswordFailed
        data_list = []
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, "html.parser")
        trs = soup.select(' #kbtable tr ')
        data_list = tr_in_trs(trs[2:], academy, semester, zc)
        sql = "insert into teacher_class( teacher, academy, week_time, class_order," \
              "weekday, class_name, class_num, classroom,semester)" \
              "values ( :teacher, :academy, :week_time, :class_order," \
              ":weekday, :class_name, :class_num, :classroom,:semester)"
        sql_to_execute(sql, data_list)

        return data_list


def query_in_sql(academy, week_time, semester):
    data = TeacherClass.query.filter(TeacherClass.semester == semester,
                                     TeacherClass.academy == academy,
                                     TeacherClass.week_time == week_time).all()
    if data:
        return jsonify(data=[i.serialize() for i in data])
    else:
        return None


if __name__ == '__main__':
    get_teacher_class('182210711114', 'hanzy2000', '2019-2020-1', '19', '1')

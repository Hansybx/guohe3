import json
from threading import Thread

from flask import request, jsonify
from flask_mail import Mail, Message
from flask_script import Manager

from app import create_app
from app.api.v1.stu import stu
from app.models import db
from app.models.feedback import FeedBack
from app.models.res import Res


app = create_app()
manager = Manager(app)
mail = Mail(app)


@stu.route('/feedback/create', methods=['POST'])
def feedback():
    data = request.data

    json_text = json.loads(data)

    print(json_text)

    # 反馈人的uid
    # uid = json_text['uid']
    # 反馈的内容
    content = json_text['content']
    # 反馈人的联系方式
    contact = json_text['contact']
    # 反馈的图片
    # pic = json_text['pic']
    # 反馈的来源
    origin = json_text['origin']

    feedback = FeedBack(content, contact, origin)

    db.session.add(feedback)
    db.session.commit()

    status = 200
    msg = '反馈成功'
    info = {
        'id': 404,
        'created_time': 123
    }

    # 如果反馈成功，异步发送邮件
    if status == 200:
        send_email(app, feedback)

    res_json = Res(status, msg, info)

    return jsonify(res_json.__dict__)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


# 发送邮件
def send_email(app, feedback):
    msg = Message('果核Lite', sender='1579450419@qq.com',
                  recipients=['182210711114@stu.just.edu.cn'])
    msg.body = str(
        '反馈内容：' + str(feedback.content) + '\n反馈来源：'
        + str(feedback.origin) + '\n联系方式：' + str(feedback.contact))

    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return 'ok'

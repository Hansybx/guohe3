"""

 -*- coding: utf-8 -*-
Time    : 2019/7/12 14:18
Author  : Hansybx

"""

from app import create_app

app = create_app()


@app.route('/')
def index():
    return 'Hello World'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=app.config['DEBUG'])

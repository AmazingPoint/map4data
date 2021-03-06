#_*_coding:utf-8_*_
# 一个简单的web服务，只有一个函数返回一个json对象

from flask import Flask
from functools import wraps
from flask import make_response
import json
import sqlite3
import time


def getHouseData():
    conn = sqlite3.connect('house.db')
    sql = 'select * from house;'
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


def getPopData():
    conn = sqlite3.connect('pop.db')
    sql = 'select * from population;'
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


def allow_cross_domain(fun):
    ''' 装饰器：
        为headers添加访问控制信息
        解除web端跨域访问的限制'''
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun

app = Flask(__name__)


@app.route('/')
@allow_cross_domain
def index():
    time.sleep(2)
    data = getHouseData()
    dic = {'data': data}
    return json.dumps(dic)


@app.route('/population')
@allow_cross_domain
def population():
    time.sleep(2)
    data = getPopData()
    dic = {'data': data}
    return json.dumps(dic)


if __name__ == '__main__':
    app.run(port=8000)

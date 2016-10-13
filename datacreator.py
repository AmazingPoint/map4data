# _*_ coding:utf-8 _*_
# 从网站上爬取top358的房价  可以看一下结果
import sqlite3
import sys
from selenium import webdriver
from pyquery import PyQuery as pq
from time import sleep
from location2geo import *

URL = 'http://www.cityhouse.cn/default/forsalerank.html'
LOGIN_URL = 'http://bj.cityhouse.cn/signin.html'


def login():
    browser = webdriver.PhantomJS()
    browser.get(LOGIN_URL)
    account = browser.find_element_by_name("login[uid]")
    password = browser.find_element_by_name("login[pwd]")
    account.send_keys('username')
    password.send_keys('password')
    loginbtn = browser.find_element_by_name("loginsubmit")
    loginbtn.click()
    sleep(3)
    return browser


def getPageSource(browser):
    browser.get(URL)
    sleep(2)
    source = browser.page_source
    return source


def getRows(source):
    psrc = pq(source)
    table = psrc('#order_f')
    rows = pq(table)('tr')
    return rows


def convertRows2list(rows):
    dataList = []
    for row in rows:
        cols = pq(row)('td')
        order = pq(cols[0]).text()
        city = pq(cols[1]).text()
        price = pq(cols[2]).text()
        dic = {'order': order, 'city': city, 'price': price}
        print "%s, %s, %s" % (order, city, price)
        dataList.append(dic)
    return dataList


def Data():
    source = getPageSource(login())
    rows = getRows(source)
    dataList = convertRows2list(rows)
    return dataList


def saveData(dataList):
    for d in dataList:
        cityStr = d['city']
        geo = l2g(cityStr)
        order = d['order']
        city = d['city']
        lat = geo[0]
        lon = geo[1]
        priceStr = d['price']
        priceStr = priceStr.replace(',', '')
        priceStr = priceStr.replace(u'元/㎡', '')
        price = priceStr
        dbWrite(order, city, lat, lon, price)


def dbConn():
    conn = sqlite3.connect("house.db")
    return conn


def dbWrite(order, city, lat, lon, price):
    conn = dbConn()
    sql_c = u"create table if not exists house('order' integer,\
     'city' char(32), 'lat' NUMERIC, 'lon' numeric, 'price' integer);"
    sql_i = u"insert into house values('" + order + u"','" + city + \
        u"','" + str(lat) + u"','" + str(lon) + u"','" + price + u"');"
    conn.cursor().execute(sql_c)
    conn.commit()
    conn.cursor().execute(sql_i)
    conn.commit()


saveData(Data())

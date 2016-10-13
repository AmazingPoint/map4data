# _*_coding:utf-8_*_
from selenium import webdriver
from pyquery import PyQuery as pq
from time import sleep
from location2geo import l2g
import sqlite3
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

URL = 'http://data.stats.gov.cn/easyquery.htm?cn=E0105'


def createBrowser():
    browser = webdriver.PhantomJS()
    return browser


def getPageSource(browser):
    browser.get(URL)
    sleep(2)
    link = browser.find_element_by_id("treeZhiBiao_4_a")
    link.click()
    sleep(1)
    link_1 = browser.find_element_by_class_name('dtHead')
    link_1.click()
    sleep(1)
    links = browser.find_elements_by_tag_name("li")
    link_2 = None
    for link in links:
        if link.text == u'序列':
            link_2 = link
    if link_2 is not None:
        link_2.click()
        sleep(1)
        return browser.page_source


def getRows(page_source):
    pqobj = pq(page_source)
    rows = pqobj(".table_column tbody tr")
    datas = []
    for row in rows:
        datas.append(getColums(row))
    return datas


def getColums(row):
    tdlist = pq(row)('td')
    clos = []
    for td in tdlist:
        value = pq(td).text()
        clos.append(value)
    return clos


def saveData(datas):
    conn = sqlite3.connect('pop.db')
    sql_create = u"create table population('city' char(32),\
     'lat' numeric, 'lon' numeric, 'count' numeric)"
    conn.cursor().execute(sql_create)
    conn.commit()
    for data in datas:
        city = data[0]
        geo = l2g(city)
        lat = geo[0]
        lon = geo[1]
        count = float(data[1])
        sql_save = "insert into population values('%s','%f','%f','%f')" % (
            city, lat, lon, count)
        print sql_save
        conn.cursor().execute(sql_save)
        conn.commit()
    conn.close()

browser = createBrowser()
page_source = getPageSource(browser)
datas = getRows(page_source)
saveData(datas)

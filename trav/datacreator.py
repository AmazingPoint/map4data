# _*_coding:utf-8_*_

import requests
from pyquery import PyQuery as pq
from local2geo import l2g
import sqlite3
import re

URL_5A = 'http://www.cnta.gov.cn/was5/web/search?page=1&channelid=242887&orderby=-AYEAR&perpage=500&outlinepage=5&searchscope=&timescope=&timescopecolumn=&orderby=-AYEAR&andsen=&total=&orsen=&exclude='
URL_4A = 'http://blog.sina.com.cn/s/blog_539b8ff50102v0mp.html'


def getPageSource(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    return r.text


def makeData_5a(page_source):
    addr_list = pq(page_source)(".main1_right_m1 a")
    date_list = pq(page_source)(".main1_right_m3")
    addr_datas = []
    date_datas = []
    for addr in addr_list:
        address = pq(addr).text()
        addr_datas.append(address)
    for date in date_list:
        date_pub = pq(date).text()
        date_datas.append(date_pub)
    datas = []
    for i in range(len(addr_datas)):
        cityStr = addr_datas[i]
        lat, lon = transData(cityStr)
        data = [addr_datas[i], date_datas[i], lat, lon]
        datas.append(data)
    return datas


def makeData_4a(page_source):
    datas = []
    rows_pq = pq(page_source)("tr")
    for row_pq in rows_pq:
        cols = pq(row_pq)('td')
        if len(cols) > 1:
            if pq(cols[0]).text().isdigit():
                addr_html = pq(cols[1]).html()
                pattern = re.compile(r'<[^>]+>|\n+', re.S)
                addr = pattern.sub("", addr_html)
                lat, lon = transData(addr)
                data = [addr, u'不详', lat, lon]
                datas.append(data)
    return datas


def transData(cityStr):
    geo = l2g(cityStr)
    lat = geo[0]
    lon = geo[1]
    return lat, lon


def saveData(datas):
    conn = sqlite3.connect("trav.db")
    sql_create = "create table trav('addr' char(64),\
        'lat' numeric,'lon' numeric, 'date_pub' char(8))"
    conn.cursor().execute(sql_create)
    conn.commit()
    for data in datas:
        addr = data[0]
        date_pub = data[1]
        lat = data[2]
        lon = data[3]
        sql_inster = "insert into trav values('%s','%f','%f','%s')" % (
            addr, lat, lon, date_pub)
        conn.cursor().execute(sql_inster)
        conn.commit()
    conn.close()

page_source_4a = getPageSource(URL_4A)
page_source_5a = getPageSource(URL_5A)
datas_4a = makeData_4a(page_source_4a)
datas_5a = makeData_5a(page_source_5a)
datas = datas_4a + datas_5a
saveData(datas)

# _*_coding:utf-8_*_
# 通过高德地图api获取生活地址的地理编码（address 转 geo）

import requests

API_URL = 'http://restapi.amap.com/v3/geocode/geo'
API_KEY = '47e00f78d5332dbc3220dd9c88edd40f'


def l2g(cityStr):
    url = API_URL + '?key=' + API_KEY + '&address=' + cityStr
    r = requests.get(url)
    dic = r.json()
    if len(dic['geocodes']) != 0:
        geostr = dic['geocodes'][0]['location']
        geo = geostr.split(',')
        geo[0] = float(geo[0])
        geo[1] = float(geo[1])
    else:
        geo = [0, 0]
    return geo

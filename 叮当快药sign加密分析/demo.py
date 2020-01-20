#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
http://www.ddky.com/commodity.html?ddkycache=a7b19e879d2f2f279d356f5afa6d5cff
"""
import time
from hashlib import md5


def get_sign():
    timeStamp = time.time()
    localTime = time.localtime(timeStamp)
    strTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)

    t = {
        'method': 'ddsy.product.query.orgcode.product.list.b2c',
        'orderTypeId': '0',
        'orgcode': '010502,010503,010504,010505,010506,010507',
        'pageNo': '1',
        'pageSize': '100',
        'plat': 'H5',
        'platform': 'H5',
        'shopId': '-1',
        # 't': '2019-9-23 22:4:16',
        't': '{}'.format(strTime),
        'v': '1.0',
        'versionName': '3.2.0'
    }
    l = sorted(t.keys())
    p = ''
    for i in range(0, 11):
        m = l[i]
        p += m + t.get(m)
    f = t['method'] + p + '6C57AB91A1308E26B797F4CD382AC79D'
    sign = md5(f.encode()).hexdigest()
    return sign


if __name__ == '__main__':
    sign = get_sign()
    print(sign)

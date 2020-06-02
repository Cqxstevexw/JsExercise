#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    test.py
    ~~~~~~~~~~~~~~~~~~~~~~~

    Description of this file

    :author: LiYang
    :copyright: (c) 2020, Tungee
    :date created: 2020/3/2
    :python version: 2.7
"""
import requests

s = requests.session()

ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
proxy = {
    # "http": "socks5://127.0.0.1:1080",
    # "https": "socks5://127.0.0.1:1080"
}

import requests

ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'

headers = {
    "User-Agent": ua,
}

s = requests.Session()
url = 'https://www.toutiao.com/a6833309873531257358/'

resp = s.get(url, headers=headers)
print(resp.text)
resp_cookie = resp.cookies.get_dict()
x = resp_cookie['__ac_nonce']

print(x)

data = {
    "cookie": x
}
r = requests.post('http://121.40.96.182:4006/get_sign', data=data) # 此为__ac_signature参数专属接口 随机免费开放
__ac_signature = r.json()['signature']
print('11111:  {}'.format(__ac_signature))
# x='05ed6198b00858e6a7299'
# __ac_signature='QqBNxAAgEBBCoE3ERCb.iUKgzNAABx4'
Cookie = '__ac_nonce=' + x + '; ' + '__ac_signature='+ __ac_signature
print(Cookie)
headers.update(
    {
        "Cookie": Cookie
    }
)

resp = s.get(url=url, headers=headers).text
print(resp)

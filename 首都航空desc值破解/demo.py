#!/usr/bin/env python
# -*- coding:utf-8 -*-
import execjs
import requests

# Init environment
print(execjs.get().name)
node = execjs.get()

# ctx = node.compile(open('encryption.js', 'r', encoding='utf-8').read())
ctx = node.compile(open('encryption2.js', 'r').read())
desc = ctx.call('getParams', 3827967540)
print(desc)

headers = {
    # "Accept": "application/json, text/javascript, */*; q=0.01",
    # "Accept-Encoding": "gzip, deflate",
    # "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    # "Connection": "keep-alive",
    "Content-Type": "application/json;charset=utf-8",
    "Cookie": "_ga=GA1.2.334781382.1560929205; _gid=GA1.2.679732491.1562207300; notice-read-ETweb=false; userId=aa3dcb8ac6e2803e; orgCityCookie=PEK; orgCityCookieCN=%u5317%u4EAC; dstCityCookie=HAK; dstCityCookieCN=%u6D77%u53E3; returnDateCookie=; orgBiao=%20; desBiao=%20; tirpTypeCookie=ONEWAY; flightDateCookie=2019-07-08; JSESSIONID=B8F1E313B8637CB90D8F9D06FF1AC776.d2; _gat_TrueMetrics=1; _pk_id.3.12a1=aa3dcb8ac6e2803e.1560929216.0.1562299727..; pt_s_324d6858=vt=1562299730629&cad=; pt_324d6858=uid=s70i24hK5yW0KzhoOlTzZQ&nid=0&vid=ABBeKwGpTF7nQrqzaoh-pw&vn=8&pvn=1&sact=1562299750382&to_flag=0&pl=FRHvstqOgwkxKT0MjRKMsw*pt*1562299730629; __ozlvd1402=1562299753; N_V_IN=/ieECLAeRLejNpWXVvLvx7BukcpQD0nUDuCq/+vJzSLCIUZSAwtUZRgzbA12WFL0L6ORRljWpryXrLnNy43yMm9cFe2kVp1y3OU/9xAvG12BJPpme2/56D6Dhvi5c3JH",
    "Host": "www.jdair.net",
    "Referer": "http://www.jdair.net/b2c-flight/searchflight.action?&tripType=OW&orgCity=PEK&dstCity=HAK&flightDate=2019-06-20&returnDate=",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    # "X-Requested-With": "XMLHttpRequest"
}
params = {
    'orgCity': 'PEK',
    'dstCity': 'HAK',
    'tripType': 'OW',
    'index': '1',
    'flightDate': '2020-01-20',
    'j_captcha_response': '',
    'fingerPrint': '3827967540',
    'time': '0.19890905686953486',
    'desc': desc,
    # 'desc': 'coBPtm4BZy5Ly7E1arnljwxtqjbEC6bDB76RJZCdIPBo2tz7GPiCNecjXPa7Jydt',
}
response = requests.get('http://www.jdair.net/b2c-flight/search.action', headers=headers, params=params)
print(response.text)

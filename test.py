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
    "http": "socks5://127.0.0.1:1080",
    "https": "socks5://127.0.0.1:1080"
}


def try_get():
    print('请求首页')
    url = 'https://www.yellowpages.net/'
    headers = {
        # "sec-fetch-user": "?1",
        # "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        # "accept-encoding": "gzip, deflate",
        # "sec-fetch-site": "none",
        # "sec-fetch-mode": "navigate",
        # "upgrade-insecure-requests": "1",
        # "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        # "cache-control": "max-age=0",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36",
        # "sec-fetch-dest": "document"
    }
    params = {}
    res = s.get(url=url, params=params, headers=headers, proxies=proxy)
    res.encoding = 'utf-8'
    print('try_get: ', res.status_code)
    print('try_get: ', res.headers)
    print('try_get: ', s.cookies)
    print(type(res.text))
    print(res.text)
    # html = res.content
    # html_doc = str(html, 'utf-8')
    # html_doc=html.decode("utf-8","ignore")
    # print(html_doc)


if __name__ == '__main__':
    try_get()

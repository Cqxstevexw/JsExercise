# -*- coding: utf-8 -*-
import json
import re
import time

text = """
accept: application/json, text/plain, */*
accept-encoding: gzip, deflate, br
accept-language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7
content-length: 378
content-type: application/json;charset=UTF-8
cookie: xhsuid=bMCd0lBd581ve2YD; timestamp2=1597058783904d6ed2bfdebde2d2b; timestamp2.sig=isqvIW_JcDXmMlHn3JS0FgHigOnMgUjE-QpCpPYBvqk; smidV2=20200715205903e5eeefb846a4e1052665d4a6dc3223d60023b1dbaaa6bfba0; xhs_spid.5dde=43b1248d3c75b0d8.1594816905.16.1597118314.1597107897.8255255f-72a2-4c8e-9376-e841c3ed0b3f
origin: https://www.xiaohongshu.com
referer: https://www.xiaohongshu.com/web-login/captcha?redirectPath=https%3A%2F%2Fwww.xiaohongshu.com%2Fuser%2Fprofile%2F559ba95cf5a263177913fb00
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-origin
user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36
x-sign: X0f61f7eb6b2c6201c56354cd8b3718ea


"""


def get_headers(text):
    headers = {}
    for t in text.strip().split('\n'):
        each_line = t.partition(':')
        headers[each_line[0].strip()] = each_line[2].strip()
    print(json.dumps(headers, indent=4, ensure_ascii=False))
    return headers


if __name__ == '__main__':
    get_headers(text)

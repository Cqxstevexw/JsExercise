#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

import execjs
import requests

# Init environment
print(execjs.get().name)
node = execjs.get()
with open('encryption.js', 'r') as f:
    t = f.read()
ctx = node.compile(t)

# Params
method = 'GETCITYWEATHER'
city = '广州'
_type = 'HOUR'
start_time = '2020-01-18 00:00'
end_time = '2019-01-18 20:00'

js_str = 'getEncryptedData("{}", "{}", "{}", "{}", "{}")'.format(method, city, _type, start_time, end_time)
d = ctx.eval(js_str)
print(d)

response = requests.post('https://www.aqistudy.cn/apinew/aqistudyapi.php', data={'d': d})
print(response.text)
# Decode data
js_str = 'decodeData("{}")'.format(response.text)
decrypted_data = ctx.eval(js_str)
print(type(decrypted_data), decrypted_data)
print(json.dumps(json.loads(decrypted_data), indent=4, ensure_ascii=False))

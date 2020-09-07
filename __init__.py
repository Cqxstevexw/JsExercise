#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~~~~~~~~~~~~~

    Description of this file

    :author: LiYang
    :copyright: (c) 2020, Tungee
    :date created: 2020/8/31
    :python version: 2.7
"""
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import execjs
import re
import requests

jsFunc = '''
    function add(x,y){
    return x+y;
    }
'''
jscontext = execjs.compile(jsFunc)
a = jscontext.call('add',3,5)
print(a)
# 可识别字符串，元组，字典，列表等



s = requests.session()


def get_v2(arg1):
    js_text = """
    String["prototype"]["hexXor"] = function (_0x4e08d8) {
    var _0x5a5d3b = '';
    for (var _0xe89588 = 0x0; _0xe89588 < this["length"] && _0xe89588 < _0x4e08d8["length"]; _0xe89588 += 0x2) {
        var _0x401af1 = parseInt(this["slice"](_0xe89588, _0xe89588 + 0x2), 0x10);
        var _0x105f59 = parseInt(_0x4e08d8["slice"](_0xe89588, _0xe89588 + 0x2), 0x10);
        var _0x189e2c = (_0x401af1 ^ _0x105f59)["toString"](0x10);
        if (_0x189e2c["length"] == 0x1) {
            _0x189e2c = '\x30' + _0x189e2c
        }
        _0x5a5d3b += _0x189e2c
    }
    return _0x5a5d3b
};
String["prototype"]["unsbox"] = function () {
    var _0x4b082b = [0xf, 0x23, 0x1d, 0x18, 0x21, 0x10, 0x1, 0x26, 0xa, 0x9, 0x13, 0x1f, 0x28, 0x1b, 0x16, 0x17, 0x19, 0xd, 0x6, 0xb, 0x27, 0x12, 0x14, 0x8, 0xe, 0x15, 0x20, 0x1a, 0x2, 0x1e, 0x7, 0x4, 0x11, 0x5, 0x3, 0x1c, 0x22, 0x25, 0xc, 0x24];
    var _0x4da0dc = [];
    var _0x12605e = '';
    for (var _0x20a7bf = 0x0; _0x20a7bf < this["length"]; _0x20a7bf++) {
        var _0x385ee3 = this[_0x20a7bf];
        for (var _0x217721 = 0x0; _0x217721 < _0x4b082b["length"]; _0x217721++) {
            if (_0x4b082b[_0x217721] == _0x20a7bf + 0x1) {
                _0x4da0dc[_0x217721] = _0x385ee3
            }
        }
    }
    _0x12605e = _0x4da0dc["join"]('');
    return _0x12605e
};


var getArg2 = function (arg1) {
    var _0x5e8b26 = "3000176000856006061501533003690027800375";
    var _0x23a392 = arg1["unsbox"]();
    arg2 = _0x23a392["hexXor"](_0x5e8b26);
    return arg2
};
    """
    ct = execjs.compile(js_text)
    acw_sc__v2 = ct.call('getArg2', arg1)
    return acw_sc__v2


def try_get():
    print '请求首页'
    # url = 'http://company.zhaopin.com/CC406882586.htm'
    url = 'http://jobs.zhaopin.com/CC406882586J00488503302.htm'
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    res = s.get(url=url, headers=headers)
    print 'try_get: ', res.url
    print 'try_get: ', res.status_code
    print 'try_get: ', res.headers
    arg1 = ''.join(re.findall(u"arg1='(.*?)';", res.text))
    acw_sc__v2 = get_v2(arg1)
    # arg1 = re.findall(ur"var arg1='([0-9A-Z]+)';", res.text)
    # key = '3000176000856006061501533003690027800375'
    # _0x23a392 = unsbox(arg1)
    # acw_sc__v2 =  hexXor(key, _0x23a392)
    s.cookies.set('acw_sc__v2', acw_sc__v2)
    print s.cookies


def try_get2():
    print '请求首页'
    # url = 'http://company.zhaopin.com/CC406882586.htm'
    url = 'http://jobs.zhaopin.com/CC406882586J00488503303.htm'
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    }

    res = s.get(url=url, headers=headers)
    print 'try_get2: ', res.status_code
    print 'try_get2: ', res.headers
    print 'try_get2: ', s.cookies
    print res.text


def hexXor(_0x4e08d8, _0x23a392):
    _0x5a5d3b = ''
    _0xe89588 = 0x0
    while _0xe89588 < len(_0x23a392) and _0xe89588 < len(_0x4e08d8):
        _0x401af1 = int(_0x23a392[_0xe89588: _0xe89588 + 0x2], 16)
        _0x105f59 = int(_0x4e08d8[_0xe89588: _0xe89588 + 0x2], 16)
        _0x189e2c = hex(_0x401af1 ^ _0x105f59)
        if len(_0x189e2c) == 0x1:
            _0x189e2c = '\x30' + _0x189e2c
        _0x5a5d3b += _0x189e2c[2:].zfill(2)

        _0xe89588 += 0x2
    return _0x5a5d3b


def unsbox(arg):
    _0x4b082b = [0xf, 0x23, 0x1d, 0x18, 0x21, 0x10, 0x1, 0x26, 0xa, 0x9, 0x13, 0x1f, 0x28, 0x1b, 0x16, 0x17, 0x19, 0xd,
                 0x6, 0xb, 0x27, 0x12, 0x14, 0x8, 0xe, 0x15, 0x20, 0x1a, 0x2, 0x1e, 0x7, 0x4, 0x11, 0x5, 0x3, 0x1c,
                 0x22, 0x25, 0xc, 0x24]
    _0x4da0dc = [''] * 40
    _0x12605e = ''
    for _0x20a7bf in range(0, len(arg)):
        _0x385ee3 = arg[_0x20a7bf]
        for _0x217721 in range(0, len(_0x4b082b)):
            if _0x4b082b[_0x217721] == _0x20a7bf + 0x1:
                _0x4da0dc[_0x217721] = _0x385ee3
    _0x12605e = ''.join(_0x4da0dc)
    return _0x12605e


if __name__ == '__main__':
    # get_v2(1)
    try_get()
    # try_get2()
    # arg1 = 'E6D117511CE1576BED6657BDB9938A7050E212BD'
    # key = '3000176000856006061501533003690027800375'
    # _0x23a392 = unsbox(arg1)
    # arg2 = 'acw_sc__v2=' + hexXor(key, _0x23a392)
    # print arg2


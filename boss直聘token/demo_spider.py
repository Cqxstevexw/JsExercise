#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    clean.py
    ~~~~~~~~~~~~~~~~~~~~~~~

    Description of this file

    :author: LiYang
    :copyright: (c) 2020, Tungee
    :date created: 2020/4/2
    :python version: 2.7
"""
import json
import re
import sys
import time
import urllib

import execjs
import requests

reload(sys)
sys.setdefaultencoding('utf8')
node = execjs.get()
s = requests.session()


def clean_variable(js_source):
    """替换变量,提高可读性"""
    js_clean_str = ''.join(re.findall(u'(var .*?;)function ABC', js_source))
    clean_fun = ''.join(re.findall(u'\)\);var (.*?)=function', js_clean_str))
    print '变量替换函数为:{}'.format(clean_fun)
    js_clean_str += """;function getRealString(parm) {return %s(parm);}""" % (clean_fun)
    ctx = node.compile(js_clean_str)

    res_ls = re.findall(u'{}\(\'(.*?)\'\)'.format(clean_fun), js_source)
    ls = list(set(res_ls))
    for i in ls:
        v = ctx.call('getRealString', i)
        print '{} --> {}'.format("{}('{}')".format(clean_fun, i), "'{}'".format(v))
        js_source = js_source.replace("{}('{}')".format(clean_fun, i), "'{}'".format(v))

    return js_source


def get_zp_stoken(seed, ts, js_source):
    """处理windows,document,this相关属性"""
    windows_text = """
        window = new Object();
        window['outerWidth'] = 1855;
        window['innerWidth'] = 788;
        window['outerHeight'] = 1056;
        window['innerHeight'] = 984;
        window['ActiveXObject'] = undefined;
        window['callPhantom'] = undefined;
        window['_phantom'] = undefined;
        window['Firebug'] = undefined;
        window['screen'] = new Object();
        window['screen']['availHeight'] = 1056;
        window['screen']['availLeft'] = 65;
        window['screen']['availTop'] = 24;
        window['screen']['availWidth'] = 1855;
        window['screen']['colorDepth'] = 24;
        window['screen']['height'] = 1080;
        window['screen']['pixelDepth'] = 24;
        window['screen']['width'] = 1920;
        window['navigator'] = new Object();
        window['navigator']['webdriver'] = undefined;
        window['navigator']['userAgent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36';
        window['navigator']['appVersion'] = '5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36';
        document = new Object();
        document['title'] = "求职|找工作|最新招聘信息-BOSS直聘";
        window['document'] = document;
        """
    # 添加windows属性
    js_source = windows_text + js_source
    # 修改location.href
    js_source = re.sub(ur"=[^=]*?typeof top,[^=]*?&&[^=]*?,null\)\?.*?\[0x0\]:",
                       u"=true?'https://www.zhipin.com/':",
                       js_source)
    # 修改window['moveBy']
    js_source = re.sub(ur"&&/function\|object/[^=]*?\(typeof window[^=]*?\)\?", u"&&true?", js_source)
    # 修改window['moveTo']
    js_source = re.sub(ur"&&window\[[^=\?]+?\]\)\?", u"&&true)?", js_source)
    # 修改window['open']
    js_source = re.sub(ur"!!\([^=!:]+?/function\\[^=!:]+?,null\)\)\?", u"true?", js_source)

    # 修改document['getElementById']
    js_source = re.sub(ur",fff\)\?![^&=!:]+?\?", u",fff)?!false?", js_source)
    js_source = re.sub(ur";[^&=!:]+?&&[^&=!:]+?,fff\)\?!", u";true?!", js_source)
    # 修改document['createElement']
    js_source = re.sub(
        ur":[^&!:]+?typeof document,[^&!:]+?&&[^&!:]+?typeof document[^&!:]+?,fff\)&&[^&!:]+?typeof\(caption=document[^&!:]+?&&[^&!:]+?caption[^&!:]+?\?",
        u":true?",
        js_source)

    # 修改top
    js_source = re.sub(
        ur"=[^&=!:]+?typeof top,[^&=!:]+?&&[^&=!:]+?typeof top[^&=!:]+?&&[^&=!]+?top[^&=!:]+?,null\)\?[^&=!]+?top[^&=!:]+?:",
        u"=true?'https://www.zhipin.com/'",
        js_source)

    # 修改phantomjs
    js_source = re.sub(ur"\?/phantomjs/[^&=!:]+?\?", u"?false?", js_source)

    # 删除setIntervalnew(_0x3fc3aa,0xa);
    js_source = re.sub(ur"}setIntervalnew\(\w+,0xa\);function", u"}function", js_source)
    # 删除setIntervalnew(function()
    js_source = re.sub(ur"setIntervalnew\(function\(\).*?\);ABC", u"ABC", js_source)
    # 删除timer2
    js_source = re.sub(ur"timer2=.*?0x5\);}\(\)\);", u"}());", js_source)

    # setInterval['toString']()['replace'](/\s+/g, '') == 'functionsetInterval(){[nativecode]}' 改为true
    js_source = re.sub(
        ur"if\(typeof setInterval==[^&!:]+?&&setInterval[^&!:]+?==[^&!:]+?\|\|",
        u"if(true||",
        js_source)

    # global,process,child_process,Buffer,sessionStorage相关判断都为改为false
    js_source = re.sub(
        ur"if\([^&!:=]+?typeof global[^&!:=]+?\|\|[^&!:=]+?typeof process[^&!:=]+?\|\|[^&!:=]+?typeof child_process[^&!:=]+?\|\|[^&!:=]+?typeof Buffer[^&!:=]+?\|\|[^&!:=]+?typeof sessionStorage[^&!:=]+?\)\{",
        u"if(false){",
        js_source)

    # 在末尾添加执行函数
    fun_text = """
        function getCode(seed,ts) {
        code = new ABC().z(seed, parseInt(ts));
        return code;
        }
        """
    js_source = js_source + fun_text
    ct = execjs.compile(js_source)
    code = ct.call('getCode', seed, ts)
    return code


def try_get():
    print '请求首页'
    url = 'https://www.zhipin.com/job_detail/abcd2e480b4f8a3e1Hd_09u5Els~.html'
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    }
    response = s.get(url=url, headers=headers, allow_redirects=False)
    response.encoding = 'utf-8'
    print 'try_get: ', response.url
    print 'try_get: ', response.status_code
    print 'try_get: ', response.headers
    if response.status_code == 200:
        print response.text
    if response.status_code == 302:
        security_check_url = 'https://www.zhipin.com' + response.headers["Location"]
        try_get2(security_check_url)


def try_get2(security_check_url):
    print '请求校验文件'
    url = security_check_url
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    }
    response = s.get(url=url, headers=headers, allow_redirects=False)
    response.encoding = 'utf-8'
    print 'try_get2: ', response.url
    print 'try_get2: ', response.status_code
    print 'try_get2: ', response.headers
    seed = re.findall(u'seed=(.*?)&', security_check_url)[0]
    seed = urllib.unquote(seed)
    name = re.findall(u'name=(.*?)&', security_check_url)[0]
    ts = re.findall(u'ts=(.*?)&', security_check_url)[0]
    try_get3(seed, name, ts, security_check_url)


def try_get3(seed, name, ts, security_check_url):
    print '请求加密js文件'
    url = 'https://www.zhipin.com/web/common/security-js/{}.js'.format(name)
    print 'aaaa', url
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    }
    response = s.get(url=url, headers=headers)
    print 'try_get3: ', response.status_code
    print 'try_get3: ', response.headers
    print 'try_get3: ', s.cookies
    print 'try_get3: ', response.text
    if response.status_code == 200:
        time.sleep(0.5)
        zp_stoken = get_zp_stoken(seed, ts, response.text)
        print 'seed: {}'.format(seed)
        print 'ts: {}'.format(ts)
        print '__zp_stoken__: {}'.format(zp_stoken)
        zp_stoken = urllib.quote(zp_stoken)
        print '__zp_stoken__: {}'.format(zp_stoken)
        try_get4(zp_stoken, security_check_url)


def try_get4(zp_stoken, security_check_url):
    print '再次请求详情页'
    # url = 'https://www.zhipin.com/job_detail/?ka=header-job'
    # url = 'https://www.zhipin.com/job_detail/abcd2e480b4f8a3e1Hd_09u5Els~.html'
    url = 'https://www.zhipin.com/wapi/zpCommon/data/position.json'
    headers = {
        "cookie": "__zp_stoken__={}".format(zp_stoken),
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    }
    response = s.get(url=url, headers=headers)
    print 'try_get4: ', response.url
    print 'try_get4: ', response.status_code
    print 'try_get4: ', response.headers
    print 'try_get4: ', s.cookies
    print response.text
    if 'security-check.html' in response.url:
        print '失败'
    else:
        print '成功'
        # json_data = json.loads(response.text)
        # for i in json_data.get('zpData', []):
        #     first_name, first_code = i['name'], i['code']
        #     for i2 in i.get('subLevelModelList', []):
        #         second_name, second_code = i2['name'], i2['code']
        #         for i3 in i2.get('subLevelModelList', []):
        #             third_name, third_code = i3['name'], i3['code']
        #             third_url = 'https://www.zhipin.com/job_detail/?query=&city=100010000&industry=&position={}'.format(
        #                 third_code)
        #             key = '{}|{}|{}\t{}\n'.format(first_name, second_name, third_name, third_url)
        #             print key


if __name__ == '__main__':
    try_get()
    # with open(r'ebc0e06b_source.js', 'r') as f:
    #     js_source = f.read()
    # print type(js_source)
    # seed = "spMLhVQ5czDCIRaMZzPNaQPnq30PMHkzMamtU/WSj28="
    # ts = 1586509436822
    # code = get_zp_stoken(seed, ts, js_source)
    # print code
# f19avvzpCeYWw5d+n5UUAon2mCl4fElgSW9YQjT+CbzgehsRaaVrptCU7QnmR2sHCOtkCmZjopY48HHIblcu579wnm7CLKF4gdB1SEwqFRU9oMOp/OVtfhOLM73O/8QkUF/I
# f19avvzpCeYWw5d+n5UUAon2mCl4fElgSW9YQjT+CbzgehsRaaVrptCU7QnmR2sHCOtkCmZjopY48HHIblcu579wnm7CLKF4gdB1SEwqFRU9oMOp/OVtfhOLM73O/8QkUF/I

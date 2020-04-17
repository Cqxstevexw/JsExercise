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
import re
import sys

import execjs
import requests

reload(sys)
sys.setdefaultencoding('utf8')
node = execjs.get()
s = requests.session()


def clean_variable():
    """替换变量,提高可读性"""
    with open(r'ebc0e06b_source.js', 'r') as f:
        js_str = f.read()

    js_clean_str = ''.join(re.findall(u'(var .*?;)function ABC', js_str))
    clean_fun = ''.join(re.findall(u'\)\);var (.*?)=function', js_clean_str))
    print '变量替换函数为:{}'.format(clean_fun)
    js_clean_str += """;function getRealString(parm) {return %s(parm);}""" % (clean_fun)
    ctx = node.compile(js_clean_str)

    with open(r'ebc0e06b_source.js', 'r') as f:
        js_source = f.read()
    res_ls = re.findall(u'{}\(\'(.*?)\'\)'.format(clean_fun), js_source)
    ls = list(set(res_ls))
    print '共有{}个变量可替换'.format(len(ls))
    for i in ls:
        v = ctx.call('getRealString', i)
        print '{} --> {}'.format("{}('{}')".format(clean_fun, i), "'{}'".format(v))
        js_source = js_source.replace("{}('{}')".format(clean_fun, i), "'{}'".format(v))

    with open(r'ebc0e06b_source_clean.js', 'w') as f:
        f.write(js_source)
    print '已全部替换并保存'


def get_zp_stoken():
    """处理windows,document,this相关属性"""
    with open(r'ebc0e06b_source_clean.js', 'r') as f:
        js_source = f.read()

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
seed="kzL8SuS0oUYuLWWqItAFAtHTYl8/fIZLhyQvbvmMaQA=";
ts=1586403893004;
//console.log(getCode(seed,ts));
//f19ai2KzVQGuz4HAwwMxF29q2IbvCXUQy4YkH%2FkFWStsO51Io3CRcC0l6sVunIeQ9d8sCmZjopY48HHIblcu579wnoIb2vxW2m3YNZIGRIkWmpCp%2FOVtfhOLM73O%2F8QkUF%2FI
//f19ai2KzVQGuz4HAwwMxF29q2IbvCXUQy4YkH/kFWStsO51Io3CRcC0l6sVunIeQ9d8sCmZjopY48HHIblcu579wnoIb2vxW2m3YNZIGRIkWmpCp/OVtfhOLM73O/8QkUF/I
"""
    js_source = js_source + fun_text
    with open(r'ebc0e06b_source_clean_2.js', 'w') as f:
        f.write(js_source)


def get_code(seed, ts):
    with open(r'ebc0e06b_source_clean_2.js', 'r') as f:
        js = f.read()
    ct = execjs.compile(js)
    code = ct.call('getCode', seed, ts)
    return code


if __name__ == '__main__':
    clean_variable()
    get_zp_stoken()
    seed = "Fi7hgMx9KEayxLqbEd/CWY+7b3Xa0IgMzoO99wHt31w="
    ts = 1586512228613
    code = get_code(seed, ts)
    print code

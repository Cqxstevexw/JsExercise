#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    demo.py
    ~~~~~~~~~~~~~~~~~~~~~~~

    Description of this file

    :author: LiYang
    :copyright: (c) 2020, Tungee
    :date created: 2020/9/4
    :python version: 2.7
"""
import re

import execjs
import requests

node = execjs.get()
s = requests.session()


def clean_variable():
    """替换变量,提高可读性"""
    with open(r'source.js', 'r') as f:
        js_str = f.read()

    js_clean_str = js_str.split('window[', 1)[0]
    clean_fun = ''.join(re.findall(u'\)\);var (.*?)=function', js_clean_str))
    print('变量替换函数为:{}'.format(clean_fun))
    if clean_fun:
        js_clean_str += """;function getRealString(parm) {return %s(parm);}""" % (clean_fun)
        print(js_clean_str)
        ctx = node.compile(js_clean_str)

        with open(r'source.js', 'r') as f:
            js_source = f.read()
        res_ls = re.findall(u'{}\(\'(.*?)\'\)'.format(clean_fun), js_source)
        ls = list(set(res_ls))
        print('共有{}个变量可替换'.format(len(ls)))
        for i in ls:
            v = ctx.call('getRealString', i)
            if len(v) <= 20 and ('@' not in v or (len(v) != 6 and v[-1] == '@')):
                v = v.strip('@').replace("'Arial'", '"Arial"')
                print('{} --> {}'.format("{}('{}')".format(clean_fun, i), "'{}'".format(v)))
                js_source = js_source.replace("{}('{}')".format(clean_fun, i), "'{}'".format(v))

        with open(r'source_clean.js', 'w') as f:
            f.write(js_source)
        print('已全部替换并保存')


if __name__ == '__main__':
    clean_variable()

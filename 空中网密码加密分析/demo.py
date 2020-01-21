#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
https://passport.kongzhong.com/login
"""
import execjs


def get_js_function(js_path, func_name, func_args):
    """
    获取指定目录下的js代码, 并且指定js代码中函数的名字以及函数的参数。
    :param js_path: js代码的位置
    :param func_name: js代码中函数的名字
    :param func_args: js代码中函数的参数
    :return: 返回调用js函数的结果
    """

    with open(js_path) as fp:
        js = fp.read()
        ctx = execjs.compile(js)
        return ctx.call(func_name, func_args)


if __name__ == '__main__':
    password = get_js_function('encryption.js', 'get_value', '111111')
    print(password)

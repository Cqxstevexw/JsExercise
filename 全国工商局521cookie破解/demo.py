#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
国家企业信用信息公示系统
http://www.gsxt.gov.cn/index.html
"""
import json
import random
import re
import time

import execjs
import requests
from lxml import etree


class GsxtGovSpider(object):
    def __init__(self):
        self.index_url = 'http://www.gsxt.gov.cn/index.html'
        # self.index_headers = {
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        #     "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        #     "Accept-Encoding": "gzip, deflate",
        #     "Host": "www.gsxt.gov.cn",
        #     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
        # }

        self.index_headers = {
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "Accept-Encoding": "gzip, deflate",
            "Host": "www.gsxt.gov.cn",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Upgrade-Insecure-Requests": "1",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Referer": "http://www.gsxt.gov.cn/SearchItemCaptcha",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            # "Content-Type": "application/x-www-form-urlencoded"
        }

        self.session = requests.session()

        self.timeout = 20

        self.validate_api = "http://120.78.10.176:3000/api/geetest/v3?"

    def get_jsl(self):
        """获取加速乐的两个cookie值"""
        print
        '-' * 90
        # 第一次请求,响应状态码为521,生成__jsluid_h
        response = self.session.get(url=self.index_url, headers=self.index_headers, timeout=self.timeout)

        # 处理第一次请求返回的原始js并执行，返回最终用于生成__jsl_clearance的js
        js_script = response.text
        if re.match("<script>([\s\S]+)while\(z\+\+\)try", js_script):
            js_script = re.match("<script>([\s\S]+)while\(z\+\+\)try", js_script).group(1)
            replace_str = """
                        z++;
                        function getJS(){
                            return y.replace(/\\b\w+\\b/g, function(y){
                                return x[f(y, z) - 1] || ('_' + y)
                                })}"""
            js_script = js_script + replace_str
        else:
            print
            '未成功获取到初始js代码,重试'
            self.get_jsl()
            self.session = requests.session()

        ctx = execjs.compile(js_script)
        js_script2 = ctx.call("getJS")

        # 处理新的js
        # 常规格式：document.cookie = '__jsl_clearance=1575255353.354|0|'
        if 'document.cookie' in js_script2 and re.findall("__jsl_clearance=\d{10}.*?\+';Expires", js_script2):
            js_script2 = re.findall("('__jsl_clearance=.*?)\+';Expires", js_script2)[0]
            js_script2 = js_script2.replace("+(function(){", "+(function(){window = {};")
            r_doc_js = re.search(
                "(var([\s\S]{1,5}?)=document.createElement[\s\S]+firstChild.href[\s\S]+?\[0\])[\s\S]+?;return function\(([\s\S]{1,5})\)",
                js_script2)
            if r_doc_js:
                js_script2 = js_script2.replace(r_doc_js.group(1),
                                                "var {}='http://www.gsxt.gov.cn';var {}='http://'".format(
                                                    r_doc_js.group(2), r_doc_js.group(3)
                                                ))

            js_script2 = re.sub("window.headless", 'undefined', js_script2)
            js_script2 = re.sub("window\['callP'\+'hantom']", 'undefined', js_script2)
            js_script2 = re.sub("window\['_p'\+'hantom']", 'undefined', js_script2)
            js_script2 = re.sub("window\['__p'\+'hantom'\+'as']", "undefined", js_script2)
        # 第二种格式：__jsl_clearance=toString.888|0|
        elif '__jsl_clearance=toString' in js_script2:
            print
            '处理新的js:第二种格式,未成功获取jsl,重试'
            return self.get_jsl()
        # 第三种格式：chars=parseInt.a|window|
        elif 'chars=parseInt.a|window|' in js_script2:
            print
            '处理新的js:第三种格式,未成功获取jsl,重试'
            return self.get_jsl()
        else:
            print
            '处理新的js:其它格式,未成功获取jsl,重试'
            return self.get_jsl()

        # 执行生成__jsl_clearance并赋值给session
        js_script2 = 'function getJSL(){return ' + js_script2 + '}'
        ctx = execjs.compile(js_script2)
        __jsl_clearance = ctx.call("getJSL").split('=')[-1]
        self.session.cookies['__jsl_clearance'] = __jsl_clearance
        print
        'jsl返回值为：{}'.format(requests.utils.dict_from_cookiejar(self.session.cookies))

    def get_index(self):
        """
        请求首页,获取有效cookie
        User-Agent 一定要和第一次访问设置的一模一样，不然照样返回521
        """
        print
        '-' * 90
        self.get_jsl()
        response = self.session.get(url=self.index_url, headers=self.index_headers, timeout=self.timeout)
        if response.status_code == 521:
            print
            '请求首页获取的jsl无效,重试'
            time.sleep(1)
            return self.get_index()
        print
        '获取首页cookies为：{}'.format(requests.utils.dict_from_cookiejar(self.session.cookies))

    def get_image_gif(self):
        """得到ASCII码的JS语句，解析JS语句得到参数location_inf"""
        print
        '-' * 90
        url = "http://www.gsxt.gov.cn/corp-query-custom-geetest-image.gif?v="
        local_time = time.localtime(time.time())
        url = url + str(local_time.tm_min + local_time.tm_sec)
        response = self.session.get(url, headers=self.index_headers, timeout=self.timeout)
        js_script = "function getLocationInfo(){var json=" + response.text + ";return json.map( function(item){ return String.fromCharCode(item);}).join('');}"
        ctx = execjs.compile(js_script)
        js_result = ctx.call("getLocationInfo")
        if re.search('location_info = (\d+);', js_result):
            location_info = re.findall('location_info = (\d+);', js_result)[0]
            print
            '获取corp-query-custom-geetest-image.gif的location_info值:{}'.format(location_info)
            return location_info
        else:
            self.get_index()
            self.get_image_gif()

    def get_validate_input(self, location_info):
        """参数是第4步的location_inf,得到ASCII码的JS语句，解析JS语句得到参数token"""
        print
        '-' * 90
        url = "http://www.gsxt.gov.cn/corp-query-geetest-validate-input.html?token=" + location_info
        response = self.session.get(url, headers=self.index_headers, timeout=self.timeout)
        js_script = "function getToken(){var json=" + response.text + ";return json.map( function(item){ return String.fromCharCode(item);}).join('');}"
        ctx = execjs.compile(js_script)
        js_result = ctx.call("getToken")
        if re.search('value: (\d+)}', js_result):
            token = re.findall('value: (\d+)}', js_result)[0]
            token = str(int(token) ^ 536870911)
            print
            '获取corp-query-geetest-validate-input.html的token值:{}'.format(token)
            return token
        else:
            self.get_index()
            location_info = self.get_image_gif()
            self.get_validate_input(location_info)

    def search_test(self, searchword):
        print
        '-' * 90
        url = "http://www.gsxt.gov.cn/corp-query-search-test.html?searchword=" + searchword
        resp = self.session.get(url, headers=self.index_headers, timeout=self.timeout)
        print
        "请求corp-query-search-test.html页面:", resp.text

    def search_item_captcha(self):
        """获取gt和challenge值"""
        print
        '-' * 90
        geetest_res = {}
        url = 'http://www.gsxt.gov.cn/SearchItemCaptcha?t={}'.format(int(time.time() * 1000))
        response = self.session.get(url=url, headers=self.index_headers, timeout=self.timeout)
        geetest_res['gt'] = response.json()['gt']
        geetest_res['challenge'] = response.json()['challenge']
        geetest_res['validate'] = ''
        validate_api = self.validate_api + 'gt={}&challenge={}'.format(geetest_res['gt'], geetest_res['challenge'])
        response = requests.get(validate_api)
        result = json.loads(response.text)
        if result.get('status', 0) == 1:
            geetest_res['validate'] = result.get('validate', '')
        print
        'geetest相关值:{}'.format(geetest_res)
        if geetest_res['validate'] == '':
            return self.search_item_captcha()
        return geetest_res

    def search_word(self, searchword='广州探迹科技有限公司', geetest_res=None, token=str(random.randint(10000000, 99999999))):
        """
        获取查询结果列表页数据
        :param geetest_res: 包含challenge,validate值的字典
        :return:
        """
        print
        '-' * 90
        if not geetest_res:
            return

        post_data = {
            "province": "",
            "tab": "ent_tab",
            "searchword": searchword,
            "token": token,
            "geetest_challenge": geetest_res['challenge'],
            "geetest_validate": geetest_res['validate'],
            "geetest_seccode": "{}|jordan".format(geetest_res['validate']),
        }
        url = 'http://www.gsxt.gov.cn/corp-query-search-1.html'
        response = self.session.post(url=url, data=post_data, headers=self.index_headers, timeout=self.timeout)
        # print '查询结果列表页:{}'.format(response.text)

        # 获取查询结果数量
        doc = etree.HTML(response.text)
        total = int(doc.xpath('//span[@class="search_result_span1"]/text()')[0])
        page_num = total // 10
        if total % 10:
            page_num += 1
        print
        '查询到{}条信息,共有{}页'.format(total, page_num)
        if total:
            print
            '开始解析第1页结果'
            href_list = doc.xpath('//a[@class="search_list_item db"]')
            for i in href_list:
                item_url = 'http://www.gsxt.gov.cn' + i.xpath('./@href')[0]
                self.parse_detail(item_url)
        if total > 10:
            self.parse_page_num(post_data, page_num)

    def parse_page_num(self, post_data, page_num):
        """请求后续列表页"""
        for page in range(2, page_num + 1):
            print
            '开始请求第{}页'.format(page)
            url = "http://www.gsxt.gov.cn/corp-query-search-advancetest.html"
            post_data['page'] = page
            response = self.session.post(url=url, data=post_data, headers=self.index_headers, timeout=self.timeout)
            doc = etree.HTML(response.text)
            href_list = doc.xpath('//a[@class="search_list_item db"]')
            print
            '开始解析第{}页结果'.format(page)
            for i in href_list:
                item_url = 'http://www.gsxt.gov.cn' + i.xpath('./@href')[0]
                self.parse_detail(item_url)

    def parse_detail(self, url):
        """解析企业详情页"""
        print
        '-' * 90
        print
        '详情页链接:{}'.format(url)
        response = self.session.get(url=url, headers=self.index_headers, timeout=self.timeout)
        print
        '详情页:{}'.format(response.text)

    def run(self):
        # 获取有效cookies
        self.get_index()
        location_info = self.get_image_gif()
        token = self.get_validate_input(location_info)
        searchword = '广州探迹科技有限公司'
        self.search_test(searchword)
        geetest_res = self.search_item_captcha()
        self.search_word(searchword, geetest_res, token)


if __name__ == '__main__':
    GsxtGovSpider().run()

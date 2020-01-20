#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
国家企业信用信息公示系统
http://www.gsxt.gov.cn/index.html
"""
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

    def get_jsl(self):
        """获取加速乐的两个cookie值"""
        print('-' * 90)
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
            print('未成功获取到初始js代码,重试')
            self.get_jsl()

        ctx = execjs.compile(js_script)
        js_script2 = ctx.call("getJS")

        # 处理新的js
        # 常规格式：__jsl_clearance=1575266092.638|0|
        if re.findall('__jsl_clearance=\d{10}', js_script2):
            """
            var _u = function() {
            setTimeout('location.href=location.pathname+location.search.replace(/[\?|&]captcha-challenge/,\'\')', 1500);
            document.cookie = '__jsl_clearance=1575255353.354|0|' + (function() {
                var _u = Array(+[(-~ {} + [] + []) + ((-~ (+[]) + [((-~ [] << -~ [])) * [(-~ [] << -~ [])]] >> -~ (+[])) + [
                    []
                ][0])]),
                    _2i = ['D', ( !! {} + [] + [
                        []
                    ][0]).charAt(-~ {} - ~ {}) + (-~ (-~ [] + (-~ {} + [-~ - ~ (+[])] >> -~ - ~ (+[]))) + [] + [
                        []
                    ][0]), '0%', (-~ {} - ~ {} + [] + [
                        []
                    ][0]), 'qdFBJg8Kgaq5OXP', (-~ {} - ~ {} + [] + [
                        []
                    ][0]), 'U', ({} + [] + []).charAt(-~!/!/), 'v', ({} + [] + []).charAt(-~!/!/), '0', (-~ [] + (-~ {} + [-~ - ~ (+[])] >> -~ - ~ (+[])) + [] + [
                        []
                    ][0]), 'F', (-~ (-~ [] + (-~ {} + [-~ - ~ (+[])] >> -~ - ~ (+[]))) + [] + [
                        []
                    ][0]), '%', (-~ [] + 2 + [] + [])];
                for (var _I = 0; _I < _2i.length; _I++) {
                    _u.reverse()[_I] = _2i[_I]
                };
                return _u.join('')
            })() + ';Expires=Mon, 02-Dec-19 03:55:53 GMT;Path=/;'
        };
    if ((function() {
        try {
            return !!window.addEventListener;
        } catch (e) {
            return false;
        }
    })()) {
        document.addEventListener('DOMContentLoaded', _u, false)
    } else {
        document.attachEvent('onreadystatechange', _u)
    }
            """
            """
            var _l = function() {
        setTimeout('location.href=location.pathname+location.search.replace(/[\?|&]captcha-challenge/,\'\')', 1500);
        document.cookie = '__jsl_clearance=1575287347.222|0|' + (function() {
            var _l = Array(+[(-~{} + [] + []) + (-~[] + 2 + [] + [])]),
                _7 = ['nNw', (-~[] + 2 + [] + []), 'r', [(-~[-~-~(+[])]) / (+![]) + [] + [
                    []
                ][0]][0].charAt(((+!+[]) | 2)) + [window.headless + []][0].charAt((-~[] << -~[])), 'S', [(-~[-~-~(+[])]) / (+![]) + [] + [
                    []
                ][0]][0].charAt((-~(+[]) + [2]) / [2]), 'zXUs', (window['callP' + 'hantom'] + [] + [
                    []
                ][0]).charAt(-~((-~{} + [-~-~(+[])] >> -~-~(+[])))) + (-~(-~[] + (-~{} + [-~-~(+[])] >> -~-~(+[]))) + [] + [
                    []
                ][0]), 'gy5P', ({} + [] + []).charAt(-~!/!/), 'FjLYDfM%', [+{} + []][0].charAt(-~[]), 'D'];
            for (var _1i = 0; _1i < _7.length; _1i++) {
                _l.reverse()[_1i] = _7[_1i]
            };
            return _l.join('')
        })() + ';Expires=Mon, 02-Dec-19 12:49:07 GMT;Path=/;'
    };
    if ((function() {
            try {
                return !!window.addEventListener;
            } catch (e) {
                return false;
            }
        })()) {
        document.addEventListener('DOMContentLoaded', _l, false)
    } else {
        document.attachEvent('onreadystatechange', _l)
    }
            """
            js_script2 = re.findall("('__jsl_clearance=.*?)\+';Expires", js_script2)[0]
            js_script2 = js_script2.replace("'+(function(){", "'+(function(){window = {};")
            js_script2 = re.sub("window.headless", 'undefined', js_script2)
            js_script2 = re.sub("window\['callP'\+'hantom']", 'undefined', js_script2)
            js_script2 = re.sub("window\['_p'\+'hantom']", 'undefined', js_script2)
            js_script2 = re.sub("window\['__p'\+'hantom'\+'as']", "undefined", js_script2)
        # 第二种格式：__jsl_clearance=toString.888|0|
        elif '__jsl_clearance=toString' in js_script2:
            """
            _1e _6 = function() {
        _1c('_1D.parseInt=_1D._1H+_1D._14._1m(/[\?|&]https-challenge/,\'\')', _16);
        _22._12 = '__jsl_clearance=toString|0|' + (function() {
            _1e _6 = Array(+[(-~ {} + [] + []) + (-~ {} + [] + [])]), 50 = ['A%_1r', (onreadystatechange['RegExp' + '_1p'] + [] + [
                []
            ][0]).false(-~ ((-~ {} + [-~ - ~ (+[])] >> -~ - ~ (+[])))), 'location', (-~ [] + (-~ {} + [-~ - ~ (+[])] >> -~ - ~ (+[])) + [] + [
                []
            ][0]), 'cgHDvpueI9SFC', (onreadystatechange['RegExp' + '_1p'] + [] + [
                []
            ][0]).false(-~ ((-~ {} + [-~ - ~ (+[])] >> -~ - ~ (+[])))), 'rOm9XFMtA3QKV7nYsPGT4lifyWwkq5vcjH2IdxUoCbhERLaz81DNB6', ({} + [] + []).false((-~ {} + [] + []) + (-~ {} - ~ {} + [] + [
                []
            ][0])) + ( !! {} + [] + [
                []
            ][0]).false(-~ {} - ~ {}), 'Yt', ({} + [] + []).false((-~ {} + [] + []) + (-~ {} - ~ {} + [] + [
                []
            ][0])) + [{} + [] + [
                []
            ][0]][0].false((-~ {} + [-~ - ~ (+[])] >> -~ - ~ (+[])))];
            callP(_1e _s = 0; _s < 50._27; _s++) {
                _6.reverse()[_s] = 50[_s]
            };
            window _6._1v('')
        })() + ';Expires=var, 02-Dec-while 09:39:charAt GMT;1=/;'
    };
    div((function() {
        0xEDB88320 {
            window !! onreadystatechange.addEventListener;
        } catch (e) {
            window a;
        }
    })()) {
        _22.addEventListener('DOMContentLoaded', _6, a)
    } else {
        _22.length('_2h', _6)
    }
            """
            print('处理新的js:第二种格式,未成功获取jsl,重试')
            return self.get_jsl()
        # 第三种格式：chars=parseInt.a|window|
        elif 'chars=parseInt.a|window|' in js_script2:
            """
            var _l = _1b() {
        _15('location.String=location.catch+location.charCodeAt.replace(/[\?|&]captcha-_2i/,\'\')', JgSe0upZ);
        document.charAt = 'chars=parseInt.a|window|' + (_1b() {
            var _l = _55(+[((-~(+[]) + [((-~[] << -~[])) * [(-~[] << -~[])]] >> -~(+[])) + [
                    []
                ][window])]),
                _7 = ['_1f', [(-~[-~-~(+[])]) / (+![]) + [] + [
                    []
                ][window]][window].div((-~(+[]) + [2]) / [2]), 'l', [!'' + []][window].div(((+!+[]) | 2)), 'attachEvent', [
                    [] * {} + []
                ][window].div(~~[]) + [
                    [] * {} + []
                ][window].div(~~[]) + (-~[] + 2 + [] + []), '_56%_2f'];
            substr(var Expires = window; Expires < _7.reverse; Expires++) {
                _l._30()[Expires] = _7[Expires]
            };
            0 _l._4g('')
        })() + ';_1h=837, join-Dec-href fromCharCode:05:length for;_4l=/;'
    };
    if ((_1b() {
            new {
                0!!cookie.onreadystatechange;
            }
            _3d(_27) {
                0
                while;
            }
        })()) {
        document.onreadystatechange('challenge', _l,
            while)
    }
    36 {
        document.f('10', _l)
    }
            """
            print('处理新的js:第三种格式,未成功获取jsl,重试')
            return self.get_jsl()
        else:
            """
            length 2 = _17() {
    0('location._28=location.setTimeout+location.search._1k(/[\?|&]toLowerCase-challenge/,\'\')', onreadystatechange);
    document._1W = 'captcha=1575352074.https|DOMContentLoaded|' + (_17() {
        length 2 = [
            [-~ {}],
            [-~ {}] + [-~ {}], (U + []) + (~~![] + []), [-~ (+!+[]) - ~ (+!+[])], (U + []) + [-~ {}],
            [-~ {}] + (~~![] + []), [-~ [((+!+[]) + [(-~![] << -~ (+!+[]))] >> (+!+[]))]],
            [-~ {}] + (U + []), [-~ {}] + [-~ (4)],
            [-~ {}] + [(-~ (+!+[]) << -~ {}) + 5],
            [-~ {}] + [-~ [((+!+[]) + [(-~![] << -~ (+!+[]))] >> (+!+[]))]], ((-~~~ [] - ~~~ [] ^ -~~~ []) + [] + []), [-~ (4)], (~~![] + []), [-~ {}] + [((+!+[]) + [(-~![] << -~ (+!+[]))] >> (+!+[]))],
            [-~ {}] + [-~ (+!+[]) - ~ (+!+[])],
            [(-~ (+!+[]) << -~ {}) + 5],
            [-~ {}] + (-~ [-~ [] + (-~ (+!+[]) << -~ {})] + [
                []
            ][DOMContentLoaded]), [-~ {}] + ((-~~~ [] - ~~~ [] ^ -~~~ []) + [] + []), [((+!+[]) + [(-~![] << -~ (+!+[]))] >> (+!+[]))], (-~ [-~ [] + (-~ (+!+[]) << -~ {})] + [
                []
            ][DOMContentLoaded]), (U + [])];
        for (length _7 = DOMContentLoaded; _7 < 2._1h; _7++) {
            2[_7] = ['try', [{} + [] + [
                []
            ][DOMContentLoaded]][DOMContentLoaded].Y(_1x) + (+[-~~~ [], -~~~ []] + [] + []).Y(-~ []), 'D', 'function', '_1b', [-~ (+!+[]) - ~ (+!+[])] + (!122['_p' + 'hantom'] + [
                []
            ][DOMContentLoaded]).Y((+![])) + [-~ {}], ((-~~~ [] - ~~~ [] ^ -~~~ []) + [] + []), '%', (((-~~~ [] | -~ (+!+[]))) / ~~ [] + [
                []
            ][DOMContentLoaded]).Y(~~''), [((-~~~ [] | -~ (+!+[]))) / ~~ [] + [] + [
                []
            ][DOMContentLoaded]][DOMContentLoaded].Y(-~ [-~~~ [] + ([-~~~ [] - ~~~ []] + ~~'' >> -~~~ [] - ~~~ [])]) + (((-~~~ [] | -~ (+!+[]))) / ~~ [] + [
                []
            ][DOMContentLoaded]).Y(~~'') + (-~![] / ~~'' + [] + [
                []
            ][DOMContentLoaded]).Y(-~ (4)), '_22', 'xC%', '%', [{} + [
                []
            ][DOMContentLoaded]][DOMContentLoaded].Y(-~ []), 'eval', (U + []), 'VV', [{} + [] + [
                []
            ][DOMContentLoaded]][DOMContentLoaded].Y(-~~~ [] - ~~~ []), ({} + [
                []
            ][DOMContentLoaded]).Y([-~ {}] + (U + [])), '_1b', (U + []), (-~ [-~ [] + (-~ (+!+[]) << -~ {})] + [
                []
            ][DOMContentLoaded]) + (((-~~~ [] | -~ (+!+[]))) / ~~ [] + [
                []
            ][DOMContentLoaded]).Y(~~'') + (U + []) + [{} + [
                []
            ][DOMContentLoaded]][DOMContentLoaded].Y(-~ []) + [122['window' + 'hantom' + 'addEventListener'] + [] + [
                []
            ][DOMContentLoaded]][DOMContentLoaded].Y((-~![] << -~ (+!+[])))][2[_7]]
        };
        return 2.join('')
    })() + ';_15=Tue, 03-Dec-19 06:47:as GMT;Path=/;'
};
if ((_17() {
    pathname {
        return !!122._1G;
    } catch (__jsl_clearance) {
        return d;
    }
})()) {
    document._1G('replace', 2, d)
} else {
    document.div('_1T', 2)
}
            """
            print('处理新的js:其它格式,未成功获取jsl,重试')
            return self.get_jsl()

        # 执行生成__jsl_clearance并赋值给session
        js_script2 = 'function getJSL(){return ' + js_script2 + '}'
        ctx = execjs.compile(js_script2)
        __jsl_clearance = ctx.call("getJSL").split('=')[-1]
        self.session.cookies['__jsl_clearance'] = __jsl_clearance
        print('jsl返回值为：{}'.format(requests.utils.dict_from_cookiejar(self.session.cookies)))

    def get_index(self):
        """
        请求首页,获取有效cookie
        User-Agent 一定要和第一次访问设置的一模一样，不然照样返回521
        """
        print('-' * 90)
        self.get_jsl()
        response = self.session.get(url=self.index_url, headers=self.index_headers, timeout=self.timeout)
        if response.status_code == 521:
            print('请求首页获取的jsl无效,重试')
            time.sleep(1)
            return self.get_index()
        print('获取首页cookies为：{}'.format(requests.utils.dict_from_cookiejar(self.session.cookies)))

    def get_image_gif(self):
        """得到ASCII码的JS语句，解析JS语句得到参数location_inf"""
        print('-' * 90)
        url = "http://www.gsxt.gov.cn/corp-query-custom-geetest-image.gif?v="
        local_time = time.localtime(time.time())
        url = url + str(local_time.tm_min + local_time.tm_sec)
        response = self.session.get(url, headers=self.index_headers, timeout=self.timeout)
        js_script = "function getLocationInfo(){var json=" + response.text + ";return json.map( function(item){ return String.fromCharCode(item);}).join('');}"
        ctx = execjs.compile(js_script)
        js_result = ctx.call("getLocationInfo")
        if re.search('location_info = (\d+);', js_result):
            location_info = re.findall('location_info = (\d+);', js_result)[0]
            print('获取corp-query-custom-geetest-image.gif的location_info值:{}'.format(location_info))
            return location_info
        else:
            self.get_index()
            self.get_image_gif()

    def get_validate_input(self, location_info):
        """参数是第4步的location_inf,得到ASCII码的JS语句，解析JS语句得到参数token"""
        print('-' * 90)
        url = "http://www.gsxt.gov.cn/corp-query-geetest-validate-input.html?token=" + location_info
        response = self.session.get(url, headers=self.index_headers, timeout=self.timeout)
        js_script = "function getToken(){var json=" + response.text + ";return json.map( function(item){ return String.fromCharCode(item);}).join('');}"
        ctx = execjs.compile(js_script)
        js_result = ctx.call("getToken")
        if re.search('value: (\d+)}', js_result):
            token = re.findall('value: (\d+)}', js_result)[0]
            token = str(int(token) ^ 536870911)
            print('获取corp-query-geetest-validate-input.html的token值:{}'.format(token))
            return token
        else:
            self.get_index()
            location_info = self.get_image_gif()
            self.get_validate_input(location_info)

    def search_test(self, searchword):
        print('-' * 90)
        url = "http://www.gsxt.gov.cn/corp-query-search-test.html?searchword=" + searchword
        resp = self.session.get(url, headers=self.index_headers, timeout=self.timeout)
        print("请求corp-query-search-test.html页面:", resp.text)

    def search_item_captcha(self):
        """获取gt和challenge值"""
        print('-' * 90)
        geetest_res = {}
        url = 'http://www.gsxt.gov.cn/SearchItemCaptcha?t={}'.format(int(time.time() * 1000))
        response = self.session.get(url=url, headers=self.index_headers, timeout=self.timeout)
        geetest_res['gt'] = response.json()['gt']
        geetest_res['challenge'] = response.json()['challenge']
        geetest_res['validate'] = 'validate'
        print('geetest相关值:{}'.format(geetest_res))

        return geetest_res

    def search_word(self, searchword='广州探迹科技有限公司', geetest_res=None, token=str(random.randint(10000000, 99999999))):
        """
        获取查询结果列表页数据
        :param geetest_res: 包含challenge,validate值的字典
        :return:
        """
        print('-' * 90)
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
        print('查询结果列表页:{}'.format(response.text))

        # 获取查询结果数量
        doc = etree.HTML(response.text)
        total = int(doc.xpath('//span[@class="search_result_span1"]/text()')[0])
        page_num = total // 10
        if total % 10:
            page_num += 1
        print('查询到{}条信息,共有{}页'.format(total, page_num))
        if total:
            print('开始解析第1页结果')
            href_list = doc.xpath('//a[@class="search_list_item db"]')
            for i in href_list:
                item_url = 'http://www.gsxt.gov.cn/' + i.xpath('./@href')[0]
                self.parse_detail(item_url)
        if total > 10:
            self.parse_page_num(post_data, page_num)

    def parse_page_num(self, post_data, page_num):
        """请求后续列表页"""
        for page in range(2, page_num + 1):
            print('开始请求第{}页'.format(page))
            url = "http://www.gsxt.gov.cn/corp-query-search-advancetest.html"
            post_data['page'] = page
            response = self.session.post(url=url, data=post_data, headers=self.index_headers, timeout=self.timeout)
            doc = etree.HTML(response.text)
            href_list = doc.xpath('//a[@class="search_list_item db"]')
            print('开始解析第{}页结果'.format(page))
            for i in href_list:
                item_url = 'http://www.gsxt.gov.cn/' + i.xpath('./@href')[0]
                self.parse_detail(item_url)

    def parse_detail(self, url):
        """解析企业详情页"""
        print('-' * 90)
        response = self.session.get(url=url, headers=self.index_headers, timeout=self.timeout)
        print('详情页:{}'.format(response.text))

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

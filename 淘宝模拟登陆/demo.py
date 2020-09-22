#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    demo.py
    ~~~~~~~~~~~~~~~~~~~~~~~

    Description of this file

    :author: LiYang
    :copyright: (c) 2020, Tungee
    :date created: 2020/9/16
    :python version: 2.7
"""
import sys
import asyncio
import random
import time
from pyppeteer import launch
from retrying import retry


async def taobao_login(username, password, url):
    """
    淘宝登录主程序
    :param username: 用户名
    :param password: 密码
    :param url: 登录网址
    :return: 登录cookies
    """
    # 'headless': False如果想要浏览器隐藏更改False为True
    browser = await launch({'headless': False, 'args': ['--no-sandbox']})
    page = await browser.newPage()
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')
    await page.goto(url)

    # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果
    await page.evaluate(
        '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')

    # 点击密码登录
    await page.click('.password-login-tab-item')
    await asyncio.sleep(2)
    # 输入用户名，密码
    await page.type('#fm-login-id', username, {'delay': input_time_random() - 50})  # delay是限制输入的时间
    await page.type('#fm-login-password', password, {'delay': input_time_random()})
    await asyncio.sleep(2)
    # 检测页面是否有滑块。原理是检测页面元素。
    # slider = await page.Jeval('#nocaptcha', 'node => node.style')  # 是否有滑块
    slider = None
    flag = True

    if slider:
        print('当前页面出现滑块')
        # await page.screenshot({'path': './headless-login-slide.png'}) # 截图测试
        flag, page = await try_validation(page=page)  # js拉动滑块过去

    if flag:
        print("点击登录")
        await asyncio.wait([
            page.keyboard.press('Enter'),
            page.waitFor(20),
            page.waitForNavigation(),
        ])

        # 检测是否登录成功
        cookie = ''
        body = await page.content()
        if 'href="//trade.taobao.com/trade/itemlist/list_bought_items.htm"' in body:
            print('登录成功')
            print('当前页面: {}'.format(page.url))
            cookie = await get_cookie(page)
            print('cookie: {}'.format(cookie))

            # 进入店铺查询页

            # search_url = 'https://shopsearch.taobao.com/search?app=shopsearch&q=&js=1&initiative_id=staobaoz_20200916&ie=utf8&s=1'
            await page.click('#J_SearchTab > ul > li.J_SearchTab.shop-search-tab')
            await page.type('input#q', 'janelove', {'delay': input_time_random()})
            await page.click('#J_TSearchForm > div.search-button > button')
            await page.waitFor(20)
            await page.waitForNavigation()

            # 获取滑块标签
            nc_1_n1z = await page.xpath('//span[@id="nc_1_n1z"]')
            if nc_1_n1z:
                print('出现滑块: 亲，小二正忙，滑动一下马上回来')
                flag, page = await try_validation(page=page)
                if flag:
                    cookie = await get_cookie(page)
        else:
            # 程序退出
            print('登录失败')

        return cookie


# 获取登录后cookie
async def get_cookie(page):
    cookies_list = await page.cookies()
    cookies = ''
    for cookie in cookies_list:
        str_cookie = '{0}={1};'
        str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
        cookies += str_cookie
    return cookies


def retry_if_result_none(result):
    return result is None


@retry(retry_on_result=retry_if_result_none)
async def try_validation(page=None, distance=2000):
    try:
        await asyncio.sleep(5)
        # 鼠标移动到滑块，按下，滑动到头（然后延时处理），松开按键
        el = await page.querySelector('#nc_1_n1z')
        box = await el.boundingBox()
        await page.hover('#nc_1_n1z')  # 不同场景的验证码模块能名字不同。
        await page.mouse.down()
        await page.mouse.move(box['x'] + 10000, box['y'], {'delay': random.randint(1000, 2000), 'steps': 20})
        await page.mouse.up()
        time.sleep(9999)

        # # 将距离拆分成两段，模拟正常人的行为
        # distance1 = distance - 10
        # distance2 = 10
        # btn_position = await page.evaluate('''
        #    () =>{
        #     return {
        #      x: document.querySelector('#nc_1_n1z').getBoundingClientRect().x,
        #      y: document.querySelector('#nc_1_n1z').getBoundingClientRect().y,
        #      width: document.querySelector('#nc_1_n1z').getBoundingClientRect().width,
        #      height: document.querySelector('#nc_1_n1z').getBoundingClientRect().height
        #      }}
        #     ''')
        # x = btn_position['x'] + btn_position['width'] / 2
        # y = btn_position['y'] + btn_position['height'] / 2
        # # print(btn_position)
        # await page.mouse.move(x, y)
        # await page.mouse.down()
        # await page.mouse.move(x + distance1, y, {'steps': 30})
        # await page.waitFor(800)
        # await page.mouse.move(x + distance1 + distance2, y, {'steps': 20})
        # await page.waitFor(800)
        # await page.mouse.up()



    except Exception as e:
        print(e, ':验证失败')
        return None, page
    else:
        await asyncio.sleep(2)
        # 判断是否通过
        slider_again = await page.Jeval('.nc-lang-cnt', 'node => node.textContent')
        if slider_again != '验证通过':
            return None, page
        else:
            # await page.screenshot({'path': './headless-slide-result.png'}) # 截图测试
            print('验证通过')
            return 1, page


def input_time_random():
    return random.randint(100, 151)


if __name__ == '__main__':
    username = '969096513@qq.com'
    password = ''
    url = 'https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fwww.taobao.com%2F'
    # url = 'https://shopsearch.taobao.com/search?q=janelove&js=1&initiative_id=staobaoz_20200916&ie=utf8'
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(taobao_login(username, password, url))
    loop.run_until_complete(task)
    new_cookie = task.result()
    print(new_cookie)

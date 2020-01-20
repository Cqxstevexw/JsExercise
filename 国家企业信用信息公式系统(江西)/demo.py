#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
国家企业信用信息公示系统（江西）
http://gsxt.jxaic.gov.cn/indexmain.jsp
"""
import base64
import collections
import datetime
import json
import re

import requests
import urllib3

urllib3.disable_warnings()


def zhuan_time(TIME):
    GMT_FORMAT = '%b%d,%Y%H:%M:%S%p'

    a = datetime.datetime.strptime(TIME, GMT_FORMAT)
    b = str(a).split(' ')
    c = b[0]
    return c


def y_m_d(string):
    if "年" in string or "月" in string or "日" in string:
        pattern = re.compile("(.*?)年(.*?)月(.*?)日")
        rs = re.search(pattern, string)
        year = rs.group(1)
        month = rs.group(2)
        if len(month) < 2:
            month = "0" + month
        day = rs.group(3)
        if len(day) < 2:
            day = "0" + day
        string = year + "-" + month + "-" + day
        return string
    else:
        return string


def spider(data):
    try:
        entname = data["companyName"] if data["companyName"] else data["gongShangZhuCeHao"]
        com1 = str(base64.b64encode(entname.encode('utf-8')))
        com1 = com1.replace("+", "u002B").replace("=", "u002C").replace("/", "u002D")
        com2 = '5' + com1 + 'P'
        proxies = {}
        headers = {
            "Referer": "http://gsxt.jxaic.gov.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        url = 'http://gsxt.jxaic.gov.cn/search/querysearch.do?name={}'.format(com2)
        data1 = {"name": com2}
        s = requests.session()
        c1 = s.get(url='http://gsxt.jxaic.gov.cn/start/querygeetest.do', headers=headers, proxies=proxies, timeout=10)
        con = s.post(url=url, data=data1, headers=headers, proxies=proxies, timeout=10)
        con1 = json.loads(con.content)
        print(con1)

        # 解析详细数据
        if con1["data"]:
            for info in con1["data"]:
                id = info["PRIPID"]
                id1 = base64.b64encode(id.encode('utf-8'))
                id2 = str(id1).replace('+', 'u002B')
                data2 = collections.OrderedDict()

                # 基本信息
                base_url = 'http://gsxt.jxaic.gov.cn/baseinfo/queryenterpriseinfoByRegnore.do?pripid={}'.format(id2)
                proxies = {}
                base_con = s.get(url=base_url, headers=headers, proxies=proxies, timeout=10)
                CompanyBaseInfo = json.loads(base_con.content)
                CompanyBaseInfo1 = collections.OrderedDict()
                CompanyBaseInfo1["companyName"] = CompanyBaseInfo["ENTNAME"]
                CompanyBaseInfo1["address"] = CompanyBaseInfo["DOM"]
                CompanyBaseInfo1["gongShangZhuCeHao"] = CompanyBaseInfo["REGNO"]
                try:
                    if len(CompanyBaseInfo["UNISCID"]) > 17:
                        CompanyBaseInfo1["zuZhiJiGouDaiMa"] = str(CompanyBaseInfo["UNISCID"])[8:17]
                    else:
                        CompanyBaseInfo1["zuZhiJiGouDaiMa"] = None
                except:
                    CompanyBaseInfo1["zuZhiJiGouDaiMa"] = None

                CompanyBaseInfo1["tongYiXinYongDaiMa"] = str(CompanyBaseInfo["UNISCID"]).replace(' ', '')
                CompanyBaseInfo1["companyType"] = CompanyBaseInfo["ENTTYPE_CN"]
                CompanyBaseInfo1["naShuiRenShiBieHao"] = CompanyBaseInfo1["tongYiXinYongDaiMa"]
                # CompanyBaseInfo1["type"] = 0
                CompanyBaseInfo1["yingYeQiXian"] = CompanyBaseInfo["ESTDATE"] + ' ' + '至' + ' ' + CompanyBaseInfo[
                    "OPTO"]
                # k = y_m_d(str(CompanyBaseInfo["APPRDATE"]))

                CompanyBaseInfo1["heZhunRiQi"] = None
                CompanyBaseInfo1["dengJiJiGuan"] = CompanyBaseInfo["REGORG_CN"]
                CompanyBaseInfo1["zhuCeDiZhi"] = CompanyBaseInfo["DOM"]
                CompanyBaseInfo1["jingYinFanWei"] = CompanyBaseInfo["OPSCOPE"]
                CompanyBaseInfo1["faRenName"] = CompanyBaseInfo["NAME"]
                try:
                    CompanyBaseInfo1["zhuCeZiBen"] = int(CompanyBaseInfo["REGCAP"])
                except:
                    CompanyBaseInfo1["zhuCeZiBen"] = -1
                CompanyBaseInfo1["unit"] = '万元'
                CompanyBaseInfo1["currency"] = CompanyBaseInfo["REGCAPCUR_CN"]
                CompanyBaseInfo1["companyStatus"] = CompanyBaseInfo["REGSTATE_CN"]

                if (
                        CompanyBaseInfo1['zhuCeZiBen'] == -1
                        or CompanyBaseInfo1['unit'] is None
                        or CompanyBaseInfo1["currency"] is None
                ):
                    CompanyBaseInfo1["amount"] = None
                else:
                    if CompanyBaseInfo1['unit'] == '万元' and '人民币' in CompanyBaseInfo1["currency"]:
                        amount1 = CompanyBaseInfo1["zhuCeZiBen"] * 10000
                        amount2 = ("%.2f%%" % (amount1))
                        CompanyBaseInfo1["amount"] = (str(amount2).split('%'))[0]

                    elif '万' in CompanyBaseInfo1['unit'] and '美元' in CompanyBaseInfo1["currency"]:
                        amount1 = CompanyBaseInfo1["zhuCeZiBen"] * 10000 * (6.3468)
                        amount2 = ("%.2f%%" % (amount1))
                        CompanyBaseInfo1["amount"] = (str(amount2).split('%'))[0]
                    else:
                        CompanyBaseInfo1["amount"] = (CompanyBaseInfo1["zhuCeZiBen"])

                if CompanyBaseInfo1["tongYiXinYongDaiMa"] != '' and CompanyBaseInfo1["tongYiXinYongDaiMa"] != '未公开':
                    tongyi_haoma1 = CompanyBaseInfo1["tongYiXinYongDaiMa"]
                    tongyi_haoma = tongyi_haoma1[2:8]
                    CompanyBaseInfo1["shengFen"] = tongyi_haoma[0:2]
                    CompanyBaseInfo1["city"] = tongyi_haoma[2:4]
                    CompanyBaseInfo1["district"] = tongyi_haoma[4:6]
                elif CompanyBaseInfo1["gongShangZhuCeHao"] != '' and CompanyBaseInfo1["gongShangZhuCeHao"] != '未公开':
                    gongshang_haoma1 = CompanyBaseInfo1["gongShangZhuCeHao"]
                    gongshang_haoma = gongshang_haoma1[0:6]
                    CompanyBaseInfo1["shengFen"] = gongshang_haoma[0:2]
                    CompanyBaseInfo1["city"] = gongshang_haoma[2:4]
                    CompanyBaseInfo1["district"] = gongshang_haoma[4:6]
                else:
                    CompanyBaseInfo1["shengFen"] = None
                    CompanyBaseInfo1["city"] = None
                    CompanyBaseInfo1["district"] = None

                data2["CompanyBaseInfo"] = CompanyBaseInfo1

                # 股东
                gudong_url = 'http://gsxt.jxaic.gov.cn/einvperson/getqueryeInvPerson.do?pripid={}'.format(
                    id2)
                proxies = {}
                gudong_con = s.get(url=gudong_url, headers=headers, proxies=proxies, timeout=12)
                GuDongInfo = json.loads(gudong_con.content)
                GuDongInfo_list = []
                data2["GuDongInfo"] = GuDongInfo_list
                if len(GuDongInfo) > 0:
                    if len(GuDongInfo) > 0:
                        for gudong in GuDongInfo:
                            GuDongInfo1 = collections.OrderedDict()
                            GuDongInfo1["guDongLeiXing"] = gudong["INVTYPE_CN"]
                            if len(str(gudong["INV"]).decode('utf-8')) > 4:
                                GuDongInfo1["guDongCompanyName"] = gudong["INV"]
                                GuDongInfo1["guDongName"] = None
                            else:
                                GuDongInfo1["guDongCompanyName"] = None
                                GuDongInfo1["guDongName"] = gudong["INV"]
                            GuDongInfo_list.append(GuDongInfo1)
                    else:
                        data2.pop('GuDongInfo')
                else:
                    data2.pop('GuDongInfo')

                # 主要成员
                zhuyao_url = 'http://gsxt.jxaic.gov.cn/epriperson/queryPerson.do?pripid={}'.format(id2)
                proxies = {}
                zhuyao_con = s.get(url=zhuyao_url, headers=headers, proxies=proxies, timeout=12)
                ZhuYaoChengYuan = json.loads(zhuyao_con.content)
                ZhuYaoChengYuan_list = []
                data2["ZhuYaoChengYuan"] = ZhuYaoChengYuan_list
                if len(ZhuYaoChengYuan) > 0:
                    for zhuyao in ZhuYaoChengYuan:
                        ZhuYaoChengYuan1 = collections.OrderedDict()
                        ZhuYaoChengYuan1["chengYuanName"] = zhuyao["NAME"]
                        ZhuYaoChengYuan1["chengYuanZhiWei"] = zhuyao["POSITION_CN"]
                        ZhuYaoChengYuan_list.append(ZhuYaoChengYuan1)
                else:
                    data2.pop('ZhuYaoChengYuan')

                # 变更
                biangeng_url = 'http://gsxt.jxaic.gov.cn/gtalterrecoder/getquerygtalterrecoderinfo.do?pripid={}'.format(
                    id2)
                proxies = {}
                biangeng_con = s.get(url=biangeng_url, headers=headers, proxies=proxies, timeout=12)
                BianGengInfo = json.loads(biangeng_con.content)
                BianGengInfo_list = []
                data2["BianGengInfo"] = BianGengInfo_list
                if len(BianGengInfo) > 0:
                    if len(BianGengInfo) > 0:
                        # BianGengInfo_list = []
                        for biangeng in BianGengInfo:
                            BianGengInfo1 = collections.OrderedDict()

                            BianGengInfo1["bianGengType"] = biangeng["ALTITEM_CN"]
                            try:
                                BianGengInfo1["bianGengQian"] = biangeng["ALTBE"]
                            except:
                                BianGengInfo1["bianGengQian"] = None
                            try:
                                BianGengInfo1["bianGengHou"] = biangeng["ALTAF"]
                            except:
                                BianGengInfo1["bianGengHou"] = None
                            BianGengInfo1["companyName"] = CompanyBaseInfo1["companyName"]
                            BianGengInfo_list.append(BianGengInfo1)
                    else:
                        data2.pop('BianGengInfo')
                else:
                    data2.pop('BianGengInfo')

                # 经营异常
                yichang_url = 'http://gsxt.jxaic.gov.cn/opadetail/getqueryabnoperationinfos.do?pripid={}'.format(id2)
                JingYingYiChang_list = []
                data2["JingYingYiChang"] = JingYingYiChang_list
                proxies = {}
                yichang_con = s.get(url=yichang_url, headers=headers, proxies=proxies, timeout=12)
                yichang_con1 = json.loads(yichang_con.content)
                if len(yichang_con1) > 0:
                    for yichang_info in yichang_con1:
                        JingYingYiChang = collections.OrderedDict()
                        JingYingYiChang = collections.OrderedDict()
                        JingYingYiChang["lieRuYuanYin"] = yichang_info["SPECAUSE_CN"]

                        JingYingYiChang["jueDingJiGuan"] = yichang_info["DECORG_CN"]

                        JingYingYiChang["yiChuYuanYin"] = yichang_info["REMEXCPRES_CN"]

                        JingYingYiChang["yiChuJueDingJiGuan"] = yichang_info["REDECORG_CN"]
                        JingYingYiChang_list.append(JingYingYiChang)
                else:
                    data2.pop('JingYingYiChang')

                # 抽查检查
                ChouChaJianCha_list = []
                data2["ChouChaJianCha"] = ChouChaJianCha_list
                choucha_url = 'http://gsxt.jxaic.gov.cn/epubspotcheck/getSpotcheck2InfoAll.do?pripid={}'.format(id2)
                proxies = {}
                choucha_con = s.get(url=choucha_url, headers=headers, proxies=proxies, timeout=12)
                choucha_con1 = json.loads(choucha_con.content)
                if len(choucha_con1["data"]) > 0:
                    for choucha in choucha_con1["data"]:
                        ChouChaJianCha = collections.OrderedDict()

                        ChouChaJianCha["type"] = choucha["RANINSTYPENAME"]
                        ChouChaJianCha["jianChaJiGuan"] = choucha["INSAUTH"]
                        ChouChaJianCha["jiHuaBianHao"] = choucha["RANINSPLANID"]
                        ChouChaJianCha["jiHuaMingCheng"] = choucha["RANINSPLANNAME"]
                        ChouChaJianCha["renWuBianHao"] = choucha["RANINSTASKID"]
                        ChouChaJianCha["renWuMingCheng"] = choucha["RANINSTASKNAME"]

                        jianChaDetails_list = []
                        ChouChaJianCha["jianChaDetails"] = jianChaDetails_list
                        choucha_detailUrl = 'http://gsxt.jxaic.gov.cn/epubspotcheck/toEntCheckResults.do?C_ENT_ID={}&RANINSTASKID={}'.format(
                            choucha["INSENTERID"], choucha["RANINSTASKID"])
                        choucha_detail = s.get(url=choucha_detailUrl, headers=headers, proxies=proxies, timeout=12)
                        choucha_detailList = re.findall('<td>(.*?)</td><td>(.*?)</td><td>(.*?)</td>',
                                                        choucha_detail.content.replace('\r', '').replace('\t',
                                                                                                         '').replace(
                                                            '\n', ''))
                        for choucha_info in choucha_detailList:
                            jieguo_info1 = collections.OrderedDict()
                            jieguo_info1["jianChaItem"] = choucha_info[1]
                            jieguo_info1["jianChaJieGuo"] = choucha_info[2]
                            jianChaDetails_list.append(jieguo_info1)
                        ChouChaJianCha_list.append(ChouChaJianCha)
                else:
                    data2.pop('ChouChaJianCha')

                # 行政处罚
                XingZhengChuFa_list = []
                data2["XingZhengChuFa"] = XingZhengChuFa_list
                chufa_url = 'http://gsxt.jxaic.gov.cn/casepubbaseinfo/queryCasepubbaseinfos.do?pripid={}'.format(id2)
                proxies = {}
                chufa_con = s.get(url=chufa_url, headers=headers, proxies=proxies, timeout=12)
                chufa_con1 = json.loads(chufa_con.content)
                if len(chufa_con1) > 0:
                    for chufa in chufa_con1:
                        XingZhengChuFa = collections.OrderedDict()
                        XingZhengChuFa["punishNumber"] = chufa["PENDECNO"]
                        XingZhengChuFa["departmentName"] = chufa["PENAUTH_CN"]
                        XingZhengChuFa["type"] = chufa["ILLEGACTTYPE"]
                        XingZhengChuFa["content"] = chufa["PENCONTENT"]
                        XingZhengChuFa["companyName"] = CompanyBaseInfo1["companyName"]

                        XingZhengChuFa_list.append(XingZhengChuFa)
                else:
                    data2.pop('XingZhengChuFa')

                # 司法协助
                SiFaXieZhu_list = []
                data2["SiFaXieZhu"] = SiFaXieZhu_list
                xiezhu_url = 'http://gsxt.jxaic.gov.cn/esfinfo/queryEsfinfos.do?pripid={}'.format(id2)
                proxies = {}
                xiezhu_con = s.get(url=xiezhu_url, headers=headers, proxies=proxies, timeout=12)
                xiezhu_con1 = json.loads(xiezhu_con.content)
                if len(xiezhu_con1) > 0:
                    for xiezhu in xiezhu_con1:
                        SiFaXieZhu = collections.OrderedDict()
                        SiFaXieZhu["companyName"] = CompanyBaseInfo1["companyName"]
                        # SiFaXieZhu["zhiXingFangShi"] = str(xiezhu[11]).replace('&nbsp', '')
                        SiFaXieZhu["type"] = xiezhu["INVTYPE_CN"]
                        guQuanDongJie = []
                        SiFaXieZhu["guQuanDongJie"] = guQuanDongJie
                        xiezhu_detailUrl = 'http://gsxt.jxaic.gov.cn/esfinfo/queryEsfinfoxq.do?FROID={}'.format(
                            xiezhu["FROID"])
                        xiezhu_detail = s.get(url=xiezhu_detailUrl, headers=headers, proxies=proxies, timeout=12)
                        zhiXingFaYuan = re.findall('执行法院</td><td>(.*?)</td>',
                                                   xiezhu_detail.content.replace('\r', '').replace('\t', '').replace(
                                                       '\n', ''))
                        zhiXingShiXiang = re.findall('执行事项</td><td>(.*?)</td>',
                                                     xiezhu_detail.content.replace('\r', '').replace('\t', '').replace(
                                                         '\n', ''))
                        caiDinfWenhao = re.findall('执行裁定书文号</td><td>(.*?)</td>',
                                                   xiezhu_detail.content.replace('\r', '').replace('\t', '').replace(
                                                       '\n', ''))
                        tongZhiWenHao = re.findall('执行通知书文号</td><td>(.*?)</td>',
                                                   xiezhu_detail.content.replace('\r', '').replace('\t', '').replace(
                                                       '\n', ''))
                        beiZhiXingRen = re.findall('被执行人</td><td>(.*?)</td>',
                                                   xiezhu_detail.content.replace('\r', '').replace('\t', '').replace(
                                                       '\n', ''))
                        beiZhiXingRenQuanYi = re.findall('被执行人持有股权、其它投资权益的数额</td><td>(.*?)</td>',
                                                         xiezhu_detail.content.replace('\r', '').replace('\t',
                                                                                                         '').replace(
                                                             '\n', ''))
                        beiZhiXingRenZhengZhaoType = re.findall('被执行人证照种类</td><td>(.*?)</td>',
                                                                xiezhu_detail.content.replace('\r', '').replace('\t',
                                                                                                                '').replace(
                                                                    '\n', ''))
                        beiZhiXingRenZhengHaoNum = re.findall('被执行人证照号码</td><td>(.*?)</td>',
                                                              xiezhu_detail.content.replace('\r', '').replace('\t',
                                                                                                              '').replace(
                                                                  '\n', ''))
                        dongJieFrom = re.findall('冻结期限自</td><td>(.*?)</td>',
                                                 xiezhu_detail.content.replace('\r', '').replace('\t', '').replace('\n',
                                                                                                                   ''))
                        dongJieUnitl = re.findall('冻结期限至</td><td>(.*?)</td>',
                                                  xiezhu_detail.content.replace('\r', '').replace('\t', '').replace(
                                                      '\n', ''))
                        dongJieQiXian = re.findall('冻结期限</td><td>(.*?)</td>',
                                                   xiezhu_detail.content.replace('\r', '').replace('\t', '').replace(
                                                       '\n', ''))
                        gongShiRiQi = re.findall('公示日期</td><td>(.*?)</td>',
                                                 xiezhu_detail.content.replace('\r', '').replace('\t', '').replace('\n',
                                                                                                                   ''))
                        guQuanDongJie_info = collections.OrderedDict()
                        guQuanDongJie_info["zhiXingFaYuan"] = zhiXingFaYuan[0]
                        guQuanDongJie_info["zhiXingShiXiang"] = zhiXingShiXiang[0]
                        guQuanDongJie_info["caiDinfWenhao"] = caiDinfWenhao[0]
                        guQuanDongJie_info["tongZhiWenHao"] = tongZhiWenHao[0]
                        guQuanDongJie_info["beiZhiXingRen"] = beiZhiXingRen[0]
                        guQuanDongJie_info["beiZhiXingRenQuanYi"] = beiZhiXingRenQuanYi[0]
                        guQuanDongJie_info["beiZhiXingRenZhengZhaoType"] = beiZhiXingRenZhengZhaoType[0]
                        guQuanDongJie_info["beiZhiXingRenZhengHaoNum"] = beiZhiXingRenZhengHaoNum[0]

                        try:
                            guQuanDongJie_info["dongJieQiXian"] = dongJieQiXian[0]
                        except:
                            guQuanDongJie_info["dongJieQiXian"] = None
                        guQuanDongJie.append(guQuanDongJie_info)
                        SiFaXieZhu_list.append(SiFaXieZhu)
                else:
                    data2.pop('SiFaXieZhu')

                # 股权出质
                GuQuanChuZhi_list = []
                proxies = {}
                data2["GuQuanChuZhi"] = GuQuanChuZhi_list
                chuzhi_url = 'http://gsxt.jxaic.gov.cn/esppledge/queryEsppledgeinfos.do?pripid={}'.format(id2)
                chuzhi_con = s.get(url=chuzhi_url, headers=headers, proxies=proxies, timeout=12)
                chuzhi_con1 = json.loads(chuzhi_con.content)
                if len(chuzhi_con1) > 0:
                    for chuzhi in chuzhi_con1:
                        chuzhi_url = 'http://gsxt.jxaic.gov.cn/esppledge/queryEsppledgeinfo.do?IMPORGID={}'.format(
                            chuzhi["IMPORGID"])
                        chuzhi_detail = s.get(url=chuzhi_url, headers=headers, proxies=proxies, timeout=12)
                        chuzhi_detail1 = re.findall(
                            '<tr><td>登记编号</td><td>(.*?)</td></tr><tr><td>出质人</td><td>(.*?)</td></tr><tr><td>证照/证件号码</td><td>(.*?)</td></tr><tr><td>出质股权数额</td><td>(.*?)</td></tr><tr><td>质权人</td><td>(.*?)</td></tr><tr><td>证照/证件号码</td><td>(.*?)</td></tr><tr><td>股权出质设立登记日期</td><td>(.*?)</td></tr><tr><td>状态</td><td>(.*?)</td></tr><tr><td>公示日期</td><td>(.*?)</td></tr>',
                            chuzhi_detail.content.replace('\r', '').replace('\t', '').replace('\n', ''))
                        if len(chuzhi_detail1) > 0:
                            GuQuanChuZhi = collections.OrderedDict()
                            try:
                                GuQuanChuZhi["regNumber"] = chuzhi_detail1[0][0]
                            except:
                                GuQuanChuZhi["regNumber"] = None
                            try:
                                GuQuanChuZhi["pledgorNo"] = chuzhi_detail1[0][2]  # 出质人证件号
                            except:
                                GuQuanChuZhi["pledgorNo"] = None
                            try:
                                GuQuanChuZhi["pledgor"] = chuzhi_detail1[0][1]  # 出质人
                            except:
                                GuQuanChuZhi["pledgor"] = None
                            try:
                                GuQuanChuZhi["pledgeeNo"] = chuzhi_detail1[0][5]  # 质权人证件号
                            except:
                                GuQuanChuZhi["pledgeeNo"] = None
                            try:
                                GuQuanChuZhi["pledgee"] = chuzhi_detail1[0][4]  # 质权人
                            except:
                                GuQuanChuZhi["pledgee"] = None

                            try:
                                GuQuanChuZhi["state"] = chuzhi_detail1[0][7]
                            except:
                                GuQuanChuZhi["state"] = None
                            try:
                                GuQuanChuZhi["equityAmount"] = chuzhi_detail1[0][3]
                            except:
                                GuQuanChuZhi["equityAmount"] = None
                            GuQuanChuZhi["companyName"] = CompanyBaseInfo1["companyName"]
                            GuQuanChuZhi_list.append(GuQuanChuZhi)

                        else:
                            data2.pop('GuQuanChuZhi')
                else:
                    data2.pop('GuQuanChuZhi')

                # 动产抵押
                DongChanDiYa_list = []
                data2["DongChanDiYa"] = DongChanDiYa_list
                dongchan_url = 'http://gsxt.jxaic.gov.cn/mortreginfo/getquerymortreginfos.do?pripid={}'.format(id2)
                proxies = {}
                dongchan_con = s.get(url=dongchan_url, headers=headers, proxies=proxies, timeout=12)
                dongchan_con1 = json.loads(dongchan_con.content)
                if len(dongchan_con1) > 0:
                    for diya_info in dongchan_con1:
                        DongChanDiYa = collections.OrderedDict()
                        baseInfo = collections.OrderedDict()
                        DongChanDiYa["baseInfo"] = baseInfo
                        baseInfo["regNum"] = diya_info["MORREGCNO"]

                        baseInfo["regDepartment"] = diya_info["REGORG_CN"]
                        baseInfo["amount"] = str(diya_info["PRICLASECAM"]) + str(diya_info["REGCAPCUR_CN"])
                        a1 = str(diya_info["TYPE"])
                        if a1 == '1':
                            baseInfo["status"] = '有效'
                        else:
                            baseInfo["status"] = None
                        dongchan_deatailUrl = 'http://gsxt.jxaic.gov.cn/mortreginfo/getdcdydetial.do?pripid={}'.format(
                            diya_info["MORREG_ID"])
                        dongchan_detail = s.get(url=dongchan_deatailUrl, headers=headers, proxies=proxies, timeout=12)
                        overviewType = re.findall('种类</td><td(.*?)>(.*?)</td>',
                                                  dongchan_detail.content.replace('\r', '').replace('\t', '').replace(
                                                      '\n', ''))
                        overviewAmount = re.findall('数额</td><td(.*?)>(.*?)</td>',
                                                    dongchan_detail.content.replace('\r', '').replace('\t', '').replace(
                                                        '\n', ''))
                        overviewScope = re.findall('担保的范围</td><td(.*?)>(.*?)</td>',
                                                   dongchan_detail.content.replace('\r', '').replace('\t', '').replace(
                                                       '\n', ''))
                        overviewTerm = re.findall('债务人履行债务的期限</td><td(.*?)>(.*?)</td>',
                                                  dongchan_detail.content.replace('\r', '').replace('\t', '').replace(
                                                      '\n', ''))
                        overviewRemark = re.findall('备注</td><td(.*?)>(.*?)</td>',
                                                    dongchan_detail.content.replace('\r', '').replace('\t', '').replace(
                                                        '\n', ''))
                        baseInfo["overviewType"] = overviewType[0][1]
                        baseInfo["overviewAmount"] = overviewAmount[0][1]
                        baseInfo["overviewScope"] = overviewScope[0][1]
                        baseInfo["overviewTerm"] = overviewTerm[0][1]
                        baseInfo["overviewRemark"] = overviewRemark[0][1]

                        peopleInfo_list = []
                        DongChanDiYa["peopleInfo"] = peopleInfo_list
                        peopleInfo_l1 = re.findall('抵押权人概况</h4>(.*?)</table>',
                                                   dongchan_detail.content.replace('\r', '').replace('\t', '').replace(
                                                       '\n', ''))
                        if len(peopleInfo_l1) > 0:
                            peopleInfo_l2 = re.findall('<td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td>',
                                                       peopleInfo_l1[0])
                            if len(peopleInfo_l2) > 0:
                                for people in peopleInfo_l2:
                                    peopleInfo = collections.OrderedDict()
                                    peopleInfo["licenseNum"] = people[3]
                                    peopleInfo["peopleName"] = people[1]
                                    peopleInfo["liceseType"] = people[2]
                                    peopleInfo["address"] = None
                                    peopleInfo_list.append(peopleInfo)
                            else:
                                DongChanDiYa.pop('peopleInfo')
                        else:
                            DongChanDiYa.pop('peopleInfo')

                        pawnInfoList_list = []
                        DongChanDiYa["pawnInfoList"] = pawnInfoList_list
                        pawnInfoList_l1 = re.findall('抵押物概况</h4><table(.*?)备注(.*?)</table>',
                                                     dongchan_detail.content.replace('\r', '').replace('\t',
                                                                                                       '').replace('\n',
                                                                                                                   ''))
                        if len(pawnInfoList_l1) > 0:
                            pawnInfoList_l2 = re.findall(
                                '<tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>',
                                pawnInfoList_l1[0][1])
                            if len(pawnInfoList_l2) > 0:
                                for pawnInfo in pawnInfoList_l2:
                                    pawnInfoList = collections.OrderedDict()
                                    pawnInfoList["detail"] = pawnInfo[3]
                                    pawnInfoList["ownership"] = pawnInfo[2]
                                    pawnInfoList["pawnName"] = pawnInfo[1]
                                    pawnInfoList_list.append(pawnInfoList)
                            else:
                                DongChanDiYa.pop('pawnInfoList')
                        else:
                            DongChanDiYa.pop('pawnInfoList')

                        DongChanDiYa_list.append(DongChanDiYa)
                else:
                    data2.pop('DongChanDiYa')

                # 行政许可
                XingZhengXuKe_list = []
                data2["XingZhengXuKe"] = XingZhengXuKe_list
                proxies = {}
                xuke_url = 'http://gsxt.jxaic.gov.cn/eotpermitinfo/queryinfoEotpermit.do?pripid={}'.format(id2)
                xuke_con = s.get(url=xuke_url, headers=headers, proxies=proxies, timeout=12)
                xuke_con1 = json.loads(xuke_con.content)
                if len(xuke_con1) > 0:
                    for xinzhengXuKe_info in xuke_con1:
                        # XingZhengXuKe = collections.OrderedDict()
                        XingZhengXuKe = collections.OrderedDict()
                        XingZhengXuKe["xuKeFileName"] = xinzhengXuKe_info["LICNAME_CN"]
                        XingZhengXuKe["xuKeContent"] = xinzhengXuKe_info["LICITEM"]

                        XingZhengXuKe["xuKeFileNo"] = xinzhengXuKe_info["LICNO"]
                        XingZhengXuKe["xuKeOrgan"] = xinzhengXuKe_info["LICANTH"]

                        XingZhengXuKe["companyName"] = CompanyBaseInfo1["companyName"]
                        XingZhengXuKe_list.append(XingZhengXuKe)
                else:
                    data2.pop('XingZhengXuKe')

                # 结果
                print(json.dumps(data2, indent=4, ensure_ascii=False))
                break

    except Exception as e:
        print('解析失败，{}'.format(e))


if __name__ == "__main__":
    try:
        data3 = {
            "id": "1",
            "num": 1,
            "companyName": "新余市赣中汽车配件公司",
            "gongShangZhuCeHao": "360502010006146",
            "tongYiXinYongDaiMa": "360502010006146",
        }
        spider(data3)
    except Exception as e:
        print('采集失败，{}'.format(e))

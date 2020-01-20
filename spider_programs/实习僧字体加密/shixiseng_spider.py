#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re

from fontTools.ttLib import TTFont


# 字体文件转成xml
def ttf2xml(name):
    font = TTFont(name + '.ttf')
    font.saveXML(name.split('.')[0] + '.xml')


# 解析xml文件
def get_font_map(name):
    words = '  0123456789一师X会四计财场DHLPT聘招工d周l端p年hx设程二五天tCG前KO网SWcgkosw广市月个BF告NRVZ作bfjnrvz三互生人政AJEI件M行QUYaeim软qu银y联'
    with open(name + '.xml') as f:
        xml = f.read()
    temp1 = re.findall(r'<GlyphID id="(\d+)" name="(.*?)"/>', xml)
    temp2 = list(set(re.findall(r'<map code="(.*?)" name="(.*?)"/>', xml)))
    d2 = {x[1]: x[0] for x in temp2}
    # print(d2)
    wordtab = {chr(int(d2[x[1]], 16)): words[int(x[0])] for x in temp1 if x[0] not in ['0', '1']}
    print(wordtab)
    for k, v in wordtab.items():
        print([k], v)

    word = '&#xe538&#xe539&#xeee5&#xf26e&#xf258'
    # word = '\ue538\ue539'
    # tab = str.maketrans(''.join(wordtab.keys()),''.join(wordtab.values()))
    # print(word.translate(tab))

    w1 = word.split('&#xe539')[0]
    print('w1:', w1)
    w2 = w1.replace('&#x', '')
    print('w2:', w2)
    w3 = chr(int(w2, 16))
    print('w3:', w3)
    print('res:', wordtab[w3])
    return wordtab


if __name__ == '__main__':
    font_name = 'font_shixiseng'
    ttf2xml(font_name)
    get_font_map(font_name)

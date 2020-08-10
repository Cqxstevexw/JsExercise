# -*- coding: utf-8 -*-
import json
import re
import time

text = """
zy: QNA6H8lZT98=
ly: aSznDKeppSw=
rid: 202008102035536e9df6ee406a5a3fc0
bx: C22bwpGF1gs=
ik: BPYw6OTzSQM=
jr: SJ5zO5byIjM=
nw: PVcTg6vY9/U=
wz: C/pJvd2GxsprrKzY1BiAItPt+sgap9LGBEUHPFcDPp70smuyDT4Nj00FSecFypa/iSCqU4ggak+Tn/pWe4fuQRKJUmjh0yigLd7M2iBwmH4=
organization: eR46sBuqF0fdw7KWFLYa
act.os: web_pc
rversion: 1.0.1
ke: TrqMDt+cB48=
callback: sm_1597062963270
dj: 9CIOZDUPyjA=
protocol: 4
ostype: web
kw: 7xDP3aCmdEA=
be: W5jfUyGuB5w=
sdkver: 1.1.3


"""


def get_headers(text):
    headers = {}
    for t in text.strip().split('\n'):
        each_line = t.partition(':')
        headers[each_line[0].strip()] = each_line[2].strip()
    print(json.dumps(headers, indent=4, ensure_ascii=False))
    return headers


if __name__ == '__main__':
    get_headers(text)

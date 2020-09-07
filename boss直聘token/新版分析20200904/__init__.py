#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~~~~~~~~~~~~~

    Description of this file

    :author: LiYang
    :copyright: (c) 2020, Tungee
    :date created: 2020/9/4
    :python version: 2.7
"""
import sys


"""
window = global;
top = window;
window['decodeURI'] = decodeURI;
window['history'] = {length: 2, scrollRestoration: "auto", state: null};
window['screen'] = {
    availHeight: 1056,
    availLeft: 65,
    availTop: 24,
    availWidth: 1855,
    colorDepth: 24,
    height: 1080,
    pixelDepth: 24,
    width: 1920,
};
window['navigator'] = {
    webdriver: undefined,
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    appVersion: '5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
};

var document = {
    getElementById: function () {
        glcanvaxs = {}
    },
    createElement: function () {
        CanvasRenderingContext2D = {
            arc: function arc() {
            },
            stroke: function stroke() {
            },
            fillText: function fillText() {
            },
            fillRect: function fillRect() {
            },
        };
        canvas = {
            getContext: function getContext() {
                return CanvasRenderingContext2D
            },
            toDataURL: function toDataURL() {
                return "data:image/png;base64,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"
            },
        };
        return canvas;
    },
    title: "求职|找工作|最新招聘信息-BOSS直聘",
    cookie: "",
};

window['document'] = document;
window['location'] = {
    hash: "",
    host: "www.zhipin.com",
    hostname: "www.zhipin.com",
    href: "https://www.zhipin.com/web/common/security-js/bed4fa64.js",
    origin: "https://www.zhipin.com",
    pathname: "/web/common/security-js/bed4fa64.js",
    port: "",
    protocol: "https:",
};
"""

"""
var name = '0f35c990';
seed = 'T0ZKSDv/dj67q0KQ3W7k5ewjgZ9Y1IgsKpPx/rNXObE=';
ts = '1599445237911';
// 35adbWDcKbXUof2hVGUh8JUB2MF9mbwEHWDAiQTkoQx5zJX8ycxkbPzUjO397EG8hJi5wQCB6GGVQbCIaYUd5ZjkVNXIfITZEKTIYfVYvKGNSFG94Eig5BgNMTU4EKx9aIH8NJmQOFxtdR3V5dA%3D%3D
// 35adbWDcKbXUof2hVGUh8JUB2MF9mbwEHWDAiQTkoQx5zJX8ycxkbPzUjO397EG8hJi5wQCB6GGVQbCIaYUd5ZjkVNXIfITZEKTIYfVYvKGNSFG94Eig5BgNMTU4EKx9aIH8NJmQOFxtdR3V5dA==
code = new ABC().z(seed, parseInt(ts) + (480 + new Date().getTimezoneOffset()) * 60 * 1000);
console.log('----------------结果:----------------');
console.log(code);
"""


"""
// window = new Proxy(global, {
//     get: function (target, key, receiver) {
//         console.log("window.get", key, target[key]);
//         if (key == "location") {
//             location = new Proxy(target[key], {
//                 get: function (_target, _key, _receiver) {
//                     console.log("window.get", key, _key, _target[_key]);
//                     if (_key == "port") {
//                         console.log("port")
//                     }
//                     return _target[_key];
//                 }
//             })
//         }
//         return target[key];
//     },
//     set: function (target, key, value, receiver) {
//         console.log("window.set", key, value);
//         target[key] = value;
//     }
// });

window = global;
var document = {
    getElementById: function () {
        glcanvaxs = {}
    },
    createElement: function () {
        CanvasRenderingContext2D = {
            arc: function arc() {
            },
            stroke: function stroke() {
            },
            fillText: function fillText() {
            },
            fillRect: function fillRect() {
            },
        };
        canvas = {
            getContext: function getContext() {
                return CanvasRenderingContext2D
            },
            toDataURL: function toDataURL() {
                return "data:image/png;base64,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"
            },
        };
        return canvas;
    },
    title: "求职|找工作|最新招聘信息-BOSS直聘",
    cookie: "",
};

window['document'] = document;
window['callPhantom'] = undefined;
window['_phantom'] = undefined;
window['length'] = 0;
window['history'] = {length: 2, scrollRestoration: "auto", state: null};
window['screen'] = {
    availHeight: 1056,
    availLeft: 65,
    availTop: 24,
    availWidth: 1855,
    colorDepth: 24,
    height: 1080,
    pixelDepth: 24,
    width: 1920,
};
window['navigator'] = {
    language: "en-US",
    cookieEnabled: true,
    webdriver: undefined,
    appCodeName: "Mozilla",
    appName: "Netscape",
    appVersion: "5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
};
window['location'] = {
    hash: "",
    host: "www.zhipin.com",
    hostname: "www.zhipin.com",
    href: "https://www.zhipin.com/web/common/security-js/bed4fa64.js",
    origin: "https://www.zhipin.com",
    pathname: "/web/common/security-js/bed4fa64.js",
    port: "",
    protocol: "https:",
};
window['atob'] = function (value) {
    return new Buffer(value, 'base64').toString();
};
top = window;

"""

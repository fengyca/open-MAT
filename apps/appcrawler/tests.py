# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
import requests

# s = requests.get('http://www.wanandroid.com/project/list/1/json?cid=1')
# # print s.content
#
# ss = {"datas": [{
#     "status": "",
#     "devices": ""},
# ]}
#
# t = 'http://10.126.1.52/appcrawler/getAppiumList?devices=mobiles'
# print requests.get(t).content


ss = {"status": "01",
      "datas": [{"status": "10", "devices": "2"},
                {"status": "11", "devices": "2"},
                {"status": "111", "devices": "2"},
                {"status": "1111", "devices": "2"},
                {"status": "11111", "devices": "2"}]}


def test(sourceText, key, l, t):
    if type(sourceText) != dict:
        sourceText = eval(sourceText)
    else:
        pass
    for j, q in sourceText.items():
        if j == key:
            l.append(q)
        else:
            if type(q) == list:
                for i in q:
                    t = t + 1
                    test(i, key, l, t)
    return l, t


if __name__ == '__main__':
    l = []
    t = 0
    s = test(ss, 'status', l, t)
    print s

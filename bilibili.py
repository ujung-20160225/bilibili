import requests
from requests import RequestException
from lxml import etree
from contextlib import closing
from pyquery import PyQuery as pq
import re
import os
import json
import subprocess

head = {    #模拟浏览器身份头向对方发送消息
        "user-agent": 'Moz*****************************************************36'
    }

baseurl = 'https://www.bilibili.com/video/BV1C541157xh'
html = requests.get(url = baseurl, headers = head).text
doc = pq(html)
title = doc('#viewbox_report > h1 > span').text()
pattern = r'\<script\>window\.__playinfo__=(.*?)\</script\>'
result = re.findall(pattern, html)[0]
temp = json.loads(result)
print(("开始下载--->")+title)

import urllib3
urllib3.disable_warnings()

headers = {
        'user-agent': 'Moz*****************************************************36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8'
    }
headers.update({'Referer': baseurl})
res = requests.Session()
begin = 0
end = 1024*1024 - 1
flag = 0

filename = "./"+title+".flv"
url = temp["data"]["dash"]["video"][0]['baseUrl']
while True:
    headers.update({'Range': 'bytes=' + str(begin) + '-' + str(end)})
    res = requests.get(url=url, headers=headers,verify=False)
    if res.status_code != 416:
        begin = end + 1
        end = end + 1024*1024
    else:
        headers.update({'Range': str(end + 1) + '-'})
        res = requests.get(url=url, headers=headers,verify=False)
        flag=1
    with open(filename, 'ab') as fp:
        fp.write(res.content)
        fp.flush()
    if flag==1:
        fp.close()
        break

print('--------------------------------------------')
print('视频下载完成')
filename = "./"+title+".mp3"
url = temp["data"]["dash"]["audio"][0]['baseUrl']
while True:
    headers.update({'Range': 'bytes=' + str(begin) + '-' + str(end)})
    res = requests.get(url=url, headers=headers,verify=False)
    if res.status_code != 416:
        begin = end + 1
        end = end + 1024*1024
    else:
        headers.update({'Range': str(end + 1) + '-'})
        res = requests.get(url=url, headers=headers,verify=False)
        flag=1
    with open(filename, 'ab') as fp:
        fp.write(res.content)
        fp.flush()
    if flag==1:
        fp.close()
        break

print('音频下载完成')
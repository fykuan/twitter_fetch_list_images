#!/usr/bin/env python
# -*- coding: utf-8 -*-
from birdy.twitter import UserClient
from threading import Thread
import json
import re
import sys
import time
import urllib
import urllib2


def save_image(tweet):
    if isinstance(s, basestring):
        # 抓出內容中的http://t.co/??????????" URL，該URL會是一個twitter頁面
        re_url = re.match('^.*(http://t.co/..........)\s*.*$', tweet)
        if (re_url != None):
            target_url = re_url.group(1)
            print "parsing: " + target_url
            urldata = urllib.urlopen(target_url)
            for line in urldata.readlines():
                # 從頁面中找出圖片的URL
                img_url = re.match(".*data-resolved-url-large=.(https.*:large)", line)
                if (img_url != None):
                    print ">> Found Image URL: " + img_url.group(1)
                    # 取得副檔名
                    img_file_ext = re.match(".*/(.*)\.(.*):large", img_url.group(1))
                    if(img_file_ext != None):
                        ext = img_file_ext.group(2)
                        fullname = img_file_ext.group(1)+"."+img_file_ext.group(2)
                        # 把圖片存下來
                        print ">>>> Saving "+img_url.group(1)+" to "+fullname
                        if path != '':
                            urllib.urlretrieve(img_url.group(1), path+"/"+fullname)
                        else:
                            urllib.urlretrieve(img_url.group(1), fullname)

path = ''

# 取得argument，作為存檔路徑
if len(sys.argv) == 1:
    path = ''
elif len(sys.argv) == 2:
    path = sys.argv[1]
else:
    print "Please specify file saving directory, or leave blank to save files here"
    sys.exit(0)

# 打開設定檔twitter.json
try:
    with open ('twitter.json'):
        f_twitter = open('twitter.json', 'r')
        json_twitter = json.loads(f_twitter.read())
except IOError:
    print "twitter.json not found"
    sys.exit(0)

client = UserClient(json_twitter['CONSUMER_KEY'], json_twitter['CONSUMER_SECRET'], json_twitter['ACCESS_TOKEN'], json_twitter['ACCESS_TOKEN_SECRET'])

# 取得SCREEN_NAME擁有的所有list
lists = client.api.lists.list.get(screen_name=json_twitter['SCREEN_NAME'])
for i in range(0,len(lists.data)):
    # 抓出listid
    id = lists.data[i].id
    list_statuses = client.api.lists.statuses.get(list_id=id)
    for j in range(0,len(list_statuses.data)-1):
        # 抓出list中tweet的內容
        s = list_statuses.data[j].text
        t = Thread(target=save_image, args=(s,))
        time.sleep(0.2)
        t.start()

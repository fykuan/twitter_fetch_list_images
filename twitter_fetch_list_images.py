#!/usr/bin/env python
# -*- coding: utf-8 -*-
from birdy.twitter import UserClient
import json
import re
import urllib
import urllib2
import imghdr
import random
import string

# 打開設定檔twitter.json
try:
    with open ('twitter.json'):
        f_twitter = open('twitter.json', 'r')
        json_twitter = json.loads(f_twitter.read())
except IOError:
    print "twitter.json not found";
    sys.exit(0)

client = UserClient(json_twitter['CONSUMER_KEY'], json_twitter['CONSUMER_SECRET'], json_twitter['ACCESS_TOKEN'], json_twitter['ACCESS_TOKEN_SECRET'])
lists = client.api.lists.list.get(screen_name=json_twitter['SCREEN_NAME'])
for i in range(0,len(lists.data)):
    id = lists.data[i].id
    list_statuses = client.api.lists.statuses.get(list_id=id)
    for j in range(0,len(list_statuses.data)-1):
        s = list_statuses.data[j].text
        if isinstance(s, basestring):
            re_url = re.match('^.*(http://t.co/..........)\s*.*$', s)
            if (re_url != None):
                # 產生隨機檔名
                rand_str = ''.join(random.choice(string.ascii_lowercase+string.digits) for x in range(10))
                target_url = re_url.group(1)
                print "parsing: " + target_url
                urldata = urllib.urlopen(target_url)
                for line in urldata.readlines():
                    #print line
                    img_url = re.match(".*data-resolved-url-large=.(https.*:large)", line)
                    if (img_url != None):
                        print ">> Found Image URL: " + img_url.group(1)
                        # 取得副檔名
                        img_file_ext = re.match(".*/(.*)\.(.*):large", img_url.group(1))
                        if(img_file_ext != None):
                            ext = img_file_ext.group(2)
                            # 把圖片存下來
                            print ">>>> Saving "+img_url.group(1)+" to "+rand_str+"."+ext
                            urllib.urlretrieve(img_url.group(1), rand_str+"."+ext)

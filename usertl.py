#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import secret
import twitter
import csv
import time
import os

os.chdir('usertweet')



"""
api = twitter.Api(consumer_key= "" ,
                  consumer_secret = "" ,
                  access_token_key = "" ,
                  access_token_secret = ""
                  )

"""
api = twitter.Api(consumer_key = secret.oath_key_dict['consumer_key'],
                  consumer_secret = secret.oath_key_dict['consumer_secret'],
                  access_token_key = secret.oath_key_dict['access_token_key'],
                  access_token_secret = secret.oath_key_dict['access_token_secret']
)


get_user_param = {
    'count': 200,
    'include_rts': False,
    'exclude_replies': True,
}


def gettweet(user_name):

    filename = user_name + ".csv"

    fout = open(filename,'ab')
    csvWriter = csv.writer(fout)

    statuses = api.GetUserTimeline(screen_name = user_name, **get_user_param)
    for s in statuses:
        Unicode = unicode(s.text)
        user_list = []
        user_list.append(Unicode.encode('utf-8'))
        print(s.text)
        csvWriter.writerow(user_list)

    fout.close()


#user_name = raw_input()

user_name = ["t_masahiro18"] #2nd anime 14




print user_name

for i in range(0,len(user_name)):
    gettweet(user_name[i])
    time.sleep(6)




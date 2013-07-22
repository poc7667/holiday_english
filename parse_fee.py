# -*- coding: utf-8 -*-
__author__ = 'Poc'

import  sys
import os
import re
import operator
import texttable as tt
import urllib,urllib2

API_CREATE_URI = "http://tinyurl.com/api-create.php?url=%s"
google_doc_url ="https://docs.google.com/spreadsheet/ccc?key=0Asm6JUPXn9lidHBhazFvOXUxeVdDRUtPMDExV1BQOFE#gid=0"

neg_money={}
pos_money={}

def get_tiny_url(url):
    encoded_url = urllib.urlencode({'url':url})[4:]
    new_url = API_CREATE_URI % (encoded_url)
    tinyurl_request = urllib2.Request(new_url)
    tinyurl_handle = urllib2.urlopen(tinyurl_request)

    return tinyurl_handle.read()

def parse(file_path):

    global  neg_money
    f = open(file_path)
    lines = f.readlines()
    name = lines[0].split()
    value = lines[1].split()

    for i in range(len(name)):
        value[i]=re.sub(',','',value[i])
        neg_money[name[i]] = float(str(value[i]))

    s =sorted(neg_money.items(),key=operator.itemgetter(1))

    print("最新一期資產負載表")
    print "詳細明細表網址=>"+get_tiny_url(google_doc_url)

    tbl = tt.Texttable()
    x =[[]]
    for i, person in enumerate(s):
        x.append([i,s[i][0],s[i][1]]) # RANK NAME AMOUNT

    tbl.add_rows(x)
    tbl.set_chars(['-',' ',' ','-'])
    tbl.set_cols_align(['c','c','r'])
    tbl.set_cols_width([4,7,8])
    tbl.header(['Rank','Name','Amount'])
    print tbl.draw()




    f.close()

def main():
    parse("deposit.txt")

if __name__ == "__main__" :
    main()
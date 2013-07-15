# -*- coding: utf-8 -*-
__author__ = 'Poc'
import re
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from sys import stdout
import httplib
import urllib, urllib2
from lxml import etree
from jianfan import jtof
from pprint import pprint
from common_lib import *

import requests

SITE=[["愛詞霸","dict-co.iciba.com","/api/dictionary.php?w="],
      ["QQ辭典","dict.qq.com","/dict?q="]
      ]


#http://web.iciba.com/partner/api01.shtml
eng_words=[]

def sanitize_word(word):
    rpls_list=['\'',"\"",'.','?','!']
    for rpls in rpls_list:
        word = word.replace(rpls,'')
    return word

def read_file(f_name,eng_words):

    f = open(f_name)
    lines = f.readlines()
    for line in lines:
        print('')
        print(line)
        eng_words.append(line)
        r1 = re.compile("(.*?)\s*[(=/]")
        m1 = r1.match(line)
        if m1 is not None:

            word = sanitize_word(str( m1.group(1).strip() ))
            translate_word(word)
            # eng_pattern="[a-Z]"
            # if re.findall(eng_pattern,word.lower()):
            #     translate_word(word)
            # else:

        else:

            words = line.split()
            word = str(' '.join(words))

            eng_pattern="[a-zA-Z]"
            if re.findall(eng_pattern,word.lower()): # English
                translate_word(word)
            else: # Chinese
                translate_word(word)

def isUni(s):
    if isinstance(s, str):
        print "ordinary string"
    elif isinstance(s, unicode):
        print "unicode string"
    else:
        print "not a string"
def cvt_codec(node):
    if hasattr( node.text, 'encode'):
        val = jtof(node.text.encode('utf-8'))
        # val = (node.text.encode('utf-8'))
    else:
        val = jtof(node.text)
    # print(val)‰
    # isUni(val)
    return val

def got_sentence(sent_node):
    for node in sent_node:
        tag = node.tag

        val = cvt_codec(node)

        if "orig" == tag: # 例句
            stdout.write(val.strip())
        if "trans" == tag: #翻譯
            try:
                stdout.write(val.strip())
            except:
                print("錯誤"+val)
                continue

def conn2Site(base_url,api,word):

    req_url="http://%s%s\"%s\""%(base_url,api,word)

    results = requests.get(req_url,
              headers={'User-Agent': 'Mozilla/5.0'})
    print(req_url)

    print((results.text))
    try:
        #requests , 遇到中文 會自動變成 iso-8859
        return results.text.encode('iso-8859-1')
    except Exception as e:
        return results.text.encode('utf-8')



def translate_word(word):


    dflt_params = conn2Site("dict-co.iciba.com","/api/dictionary.php?w=",word)


    root = etree.fromstring("%s" % dflt_params,
                            parser=etree.XMLParser(recover=True))
    if type(root) == type(None):
        return -1

    if len(root.getchildren()) == 1 :

        dflt_params = conn2Site("dict.qq.com","/dict?q=",word)

        json_data = json.loads(dflt_params)

        if 'err' in json_data:
            return
        else:
            if 'netdes' in json_data:

                for ln in json_data['netdes']:

                    for sub_ln in ln['des']:

                        try:
                            if "mf" in sub_ln:
                                # print("mf")
                                print str(sub_ln['mf']+" "+jtof(sub_ln['d'])).replace('&quot;','')
                            else:
                                    print(sub_ln['d'])
                        except :
                            pass

            if 'netsen' in json_data:
                for ln in json_data['netsen']:
                    continue
                    print ln['cs']
                    print re.sub('<[^<]+?>', '', ln['es'])#escape html tag
                    # for k,v in ln.iteritems():
                    #     print k
                    # print unicode(ln,'utf-8')


        return

    child = root.getchildren()
    for node in child:
        tag = node.tag
        val =  cvt_codec(node)

        if "key"==tag:
            print("")
            if len(val.split()) >=2 :
                stdout.write( "句子/片語:"+str(val)+"\r\n")
            elif len(val.split()) == 1 :
                stdout.write( "單字:"+str(val)+"\r\n")
            else :
                print("Error")

        if "pos"==tag:
            stdout.write( "(%s)"%val)
        if "acceptation"==tag:
            stdout.write(val)
        if "sent" == tag:
            got_sentence(node)


def main():
    global eng_words
    read_file('text.txt',eng_words)


if __name__ == '__main__':
    main()

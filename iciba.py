__author__ = 'poc.hsu'

import re,json,sys,requests,codecs,parse_notes
from BeautifulSoup import BeautifulSoup
from jianfan import jtof

reload(sys)
sys.setdefaultencoding('utf8')

_REQ_HTTP_PREFIX="http://www.iciba.com/"

_REQ_TIMEOUTS=10

def found_result(soup):
    res = soup.find('div',{'class' :'question unfound_tips'})
    if type(res) == type(None):
        return True
    else:
        return False


def fetch_data(word_lst):

    # html_file="./sample.html"
    for word in word_lst:

        if len(word.split()) > 4 : # stop lookup a sentence
            continue

        req_word =str("_".join(word.split()))
        req_url =_REQ_HTTP_PREFIX+req_word

        results = requests.get(req_url,
              headers={'User-Agent': 'Mozilla/5.0'}, timeout=_REQ_TIMEOUTS)

        soup = BeautifulSoup(results.text)

        if not found_result(soup):
            continue

        print("\n[%s]" % word )

        soup_translate =soup.find('div', {'class' :'group_pos'})
        for lbl in soup_translate.findChildren('label'):
            sys.stdout.write( jtof( lbl.getText().strip()))
        print ""
        soup_sent = soup.findAll('dl',{'class':'vDef_list'})


        for each_sent in soup_sent:
            res_word="".join(word.split())
            replace_word=" ".join(word.split())
            sent = each_sent.find('dt').getText().replace(res_word," "+replace_word+" ")
            print sent
            print jtof(each_sent.find('dd').getText())


    pass


def main():
    # print("iciba test")
    note_lst = parse_notes.read_file(sys.argv[2])

    fetch_data(note_lst)



    pass

if __name__ == '__main__':
    main()

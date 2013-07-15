__author__ = 'poc.hsu'

import re,json,sys,requests,codecs,parse_notes
from BeautifulSoup import BeautifulSoup
from jianfan import jtof

reload(sys)
sys.setdefaultencoding('utf8')

_REQ_HTTP_PREFIX="http://www.iciba.com/"
_REQ_TIMEOUTS=10
_DEBUG=True
_result_file=''
_RESULT_FILE_NAME='./result_file.txt'


def found_result(soup):
    res = soup.find('div',{'class' :'question unfound_tips'})
    if type(res) == type(None):
        return True
    else:
        return False


def output_result(line,b_newline=True):
    global  _result_file
    if _DEBUG:
        print(line)
    if b_newline:
        _result_file.write(line+'\n')
    else:
        _result_file.write(line)

def fetch_data(word_lst):


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

        output_result("\n[%s] " % word , False)

        soup_translate =soup.find('div', {'class' :'group_pos'})

        # Chinese meaning
        for lbl in soup_translate.findChildren('label'):
            output_result( jtof( lbl.getText().strip()) , False)
        output_result('')
        soup_sent = soup.findAll('dl',{'class':'vDef_list'})
        # example sentence
        for each_sent in soup_sent:
            res_word="".join(word.split())
            replace_word=" ".join(word.split())
            sent = each_sent.find('dt').getText().replace(res_word," "+replace_word+" ")
            output_result('\t'+sent)
            output_result('\t'+jtof(each_sent.find('dd').getText()))

    pass

def main():
    global  _result_file
    note_lst = parse_notes.read_file(sys.argv[1])

    _result_file=open(_RESULT_FILE_NAME,'w')
    fetch_data(note_lst)
    _result_file.close()



    pass

if __name__ == '__main__':
    main()

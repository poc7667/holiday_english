__author__ = 'poc.hsu'

import os, sys, string, time, math, re

_note_lst=[]


def sanitize_word(word):
    rpls_list=['\'',"\"",'.','?','!']
    for rpls in rpls_list:
        word = word.replace(rpls,'')
    return word

def add_item(word, note_list):
    if len(word) > 2 :
            _note_lst.append(word)


def read_file(f_name):

    f = open(f_name)
    lines = f.readlines()
    for line in lines:

        r1 = re.compile("(.*?)\s*[(=/]")
        m1 = r1.match(line)
        if m1 is not None:
            word = sanitize_word(str( m1.group(1).strip() ))
            # _note_lst.append(word.strip())
            add_item(word,_note_lst)
        else:

            words = line.split()
            word = sanitize_word(str(' '.join(words)))

            eng_pattern="[a-zA-Z]"
            if re.findall(eng_pattern,word.lower()): # English
                add_item(word,_note_lst)
            else: # Chinese
                add_item(word,_note_lst)

    # for lst in _note_lst:
    #     print str(lst)
    #     print str(''.join(lst.split()))
    #     print str('_'.join(lst.split()))

    return _note_lst


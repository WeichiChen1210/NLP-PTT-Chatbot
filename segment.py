# -*- coding：utf-8 -*-
from langconv import *
import jieba
import logging

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)

jieba.set_dictionary('extra_dict/dict.txt.big')
stopword_set = set()
with open('extra_dict/stop_words.txt','r', encoding='utf-8') as stopwords:
    for stopword in stopwords:
        stopword_set.add(stopword.strip('\n'))
output = open('ptt_seg.txt', 'w', encoding='utf-8')
with open('Gossiping-QA-Dataset.txt', 'r', encoding='utf-8') as content :
    for texts_num, line in enumerate(content):
        line = line.strip('\n')
        line = Converter('zh-hant').convert(line)
        words = jieba.cut(line, cut_all=False)
        for word in words:
            if word not in stopword_set:
                output.write(word + ' ')
        output.write('\n')
        if (texts_num + 1) % 10000 == 0:
            logging.info("completed %d lines" % (texts_num + 1))
output.close()
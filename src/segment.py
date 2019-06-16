# -*- coding：utf-8 -*-
from langconv import *
import jieba
import logging

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)

# set dictionary
jieba.set_dictionary('../extra_dict/dict.txt.big')
stopword_set = set()

# load stopwords
with open('../extra_dict/stop_words.txt','r', encoding='utf-8') as stopwords:
    for stopword in stopwords:
        stopword_set.add(stopword.strip('\n'))

# open new file to be written
output = open('../texts/ptt_seg.txt', 'w', encoding='utf-8')

# open dataset to be cut
with open('../texts/Gossiping-QA-Dataset.txt', 'r', encoding='utf-8') as content :
    for texts_num, line in enumerate(content):
        line = line.strip('\n')
        # use re to cut off punctuations, symbols
        line = re.sub(u'([\u0021-\u002f|\u003A-\u0040|\u005B-\u0060|\u007B-\u007E|\uFF01-\uFFEE|\u2600-\u26FF|\t])', r'', line)
        line = line.replace(' ', '')
        line = Converter('zh-hant').convert(line)
        # cut line
        words = jieba.cut(line, cut_all=False)
        # remove stopwords
        for word in words:
            if word not in stopword_set:
                output.write(word + ' ')
        output.write('\n')
        if (texts_num + 1) % 10000 == 0:
            logging.info("completed %d lines" % (texts_num + 1))
output.close()
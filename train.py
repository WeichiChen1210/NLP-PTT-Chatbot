# -*- coding: utf-8 -*-

import logging
from gensim.models import word2vec
from gensim.test.utils import common_texts

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = word2vec.LineSentence("wiki_seg.txt")
model = word2vec.Word2Vec(sentences, size=50, window=5, workers=9, sg=0, min_count=5)

#保存模型，供日後使用
model.save("wiki.word2vec_50.bin")

#模型讀取方式
# model = word2vec.Word2Vec.load("your_model_name")

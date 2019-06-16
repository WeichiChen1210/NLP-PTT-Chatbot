# -*- coding: utf-8 -*-

import logging
from gensim.models import word2vec
from gensim.test.utils import common_texts

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = word2vec.LineSentence("../texts/ptt_seg.txt")
model = word2vec.Word2Vec(sentences, size=200, window=10, workers=10, sg=1, min_count=3, iter=10)

# save model
model.save("../models/ptt.word2vec.bin")

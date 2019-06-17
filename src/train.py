# -*- coding: utf-8 -*-

import logging
from gensim.models import word2vec
from gensim.test.utils import common_texts

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = word2vec.LineSentence("../texts/ptt_seg.txt")
model = word2vec.Word2Vec(sentences, size=300, window=10, workers=10, sg=1, min_count=3, iter=100)

# model = word2vec.Word2Vec(sentences, size=200, window=10, workers=10, sg=1, min_count=5, iter=25) 75.6%
# model = word2vec.Word2Vec(sentences, size=200, window=10, workers=10, sg=1, min_count=3, iter=25) 77%
# model = word2vec.Word2Vec(sentences, size=200, window=10, workers=10, sg=1, min_count=3, iter=50) 80.4%
# model = word2vec.Word2Vec(sentences, size=200, window=10, workers=10, sg=1, min_count=3, iter=70) 82.4%
# model = word2vec.Word2Vec(sentences, size=250, window=10, workers=10, sg=1, min_count=3, iter=100) 82.6%
# model = word2vec.Word2Vec(sentences, size=300, window=10, workers=10, sg=1, min_count=3, iter=100) 84%
# save model
model.save("../models/ptt.word2vec.bin")

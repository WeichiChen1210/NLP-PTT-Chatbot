# -*- coding: utf-8 -*-
import numpy as np
from scipy import spatial
from gensim.models import word2vec
import jieba
import re

# set dictionary
jieba.set_dictionary('../extra_dict/dict.txt.big')

def avg_feature_vector(sentence, model, num_features, index2word_set):
    words = sentence.split()
    feature_vec = np.zeros((num_features, ), dtype='float32')
    n_words = 0
    for word in words:
        if word in index2word_set:
            n_words += 1
            feature_vec = np.add(feature_vec, model[word])
    if (n_words> 0):
        feature_vec = np.divide(feature_vec, n_words)
    return feature_vec

def segment_probs(filename, model):
    # load the problem set to sentence_list
    f = open(filename)
    sentence_list = []
    temp = ''
    for line in f:
        temp = []
        temp = line.strip().split('\t')
        sentence_list.append(temp)        
    f.close()

    problem_list = []
    # for each problem, cut the question and the  candidates
    for sentence in sentence_list:
        question_list = []
        for items in sentence:
            items = items.strip('\n')
            # use re to remove punctuations and meaningless symbols
            items = re.sub(u'([\u0021-\u002f|\u003A-\u0040|\u005B-\u0060|\u007B-\u007E|\uFF01-\uFFEE|\u2600-\u26FF|\t])', r'', items)
            items = items.replace(' ', '')
        # cut the question
        words = list(jieba.cut(sentence[0], cut_all=False))
        word = []
        # check words are in model or not
        for w in words:
            if w in model.wv.vocab:
                word.append(w)
        # if the words are all not in model, store the original list
        if len(word) == 0:
            question = " ".join(words)
        else:
            question = " ".join(word)
        
        question_list.append(question)

        # cut the candidates
        candidate = ""
        for i in range(1, 5):
            seg = []
            # first cut off the (1)(2)(3)(4) and use jieba cut
            candidate_list = list(jieba.cut(sentence[i][3:], cut_all=False))
            for c in candidate_list:
                if c in model.wv.vocab:
                    seg.append(c)
            # this candidate has too few words
            if len(seg) == 0:
                candidate = " ".join(candidate_list)
                #print(candidate)
            else:
                candidate = " ".join(seg)
                     
            question_list.append(candidate)

        # finish question and candidates, store in problem list to be return
        problem_list.append(question_list)
    return problem_list

def main():
    model = word2vec.Word2Vec.load("../models/ptt.word2vec.bin")
    index2word_set = set(model.wv.index2word)
    filename = '../texts/PTT_test_corpus.txt'

    # input problems to sentence_list
    problem_list = []
    problem_list = segment_probs(filename=filename, model=model)

    result = []
    # find out the answer of each problem
    for problems in problem_list:
        res = []
        index = 1
        # get the question's vector
        question = avg_feature_vector(problems[0], model=model, num_features=200, index2word_set=index2word_set)
        # for 4 candidates, calculate the similarity with question
        for i in range(1, 5):
            candidate = avg_feature_vector(problems[i], model=model, num_features=200, index2word_set=index2word_set)
            sim = 1 - spatial.distance.cosine(question, candidate)
            
            resultInfo = {'id': index, 'score': sim}
            # store the similarities
            res.append(resultInfo)
            index += 1
        # sort the similarities to get the highest one
        res.sort(key=lambda x: x['score'], reverse=True)
        ans = "[" + str(res[0]['id']) + "]\n"
        result.append(ans)
    
    # open answer file to write answers in
    fp = open("../texts/myans.txt", "w")
    fp.writelines(result)
    fp.close()
    fp = open("../texts/myans.csv", "w")
    fp.writelines(result)
    fp.close()

if __name__ == "__main__":
    main()

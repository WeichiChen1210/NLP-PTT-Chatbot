# -*- coding: utf-8 -*-
import numpy as np
from scipy import spatial
from gensim.models import word2vec
import jieba

def avg_feature_vector(sentence, model, num_features, index2word_set):
    words = sentence.split()
    print(words)
    feature_vec = np.zeros((num_features, ), dtype='float32')
    n_words = 0
    for word in words:
        if word in index2word_set:
            n_words += 1
            feature_vec = np.add(feature_vec, model[word])
    if (n_words> 0):
        feature_vec = np.divide(feature_vec, n_words)
    return feature_vec

def main():
    model = word2vec.Word2Vec.load("ptt.word2vec_50.bin")
    index2word_set = set(model.wv.index2word)
    f = open('PPT_test_corpus.txt')
    #for line in f:
    sentence_list = []
    temp = ''
    for line in f:
        temp = []
        temp = line.strip().split('\t')
        sentence_list.append(temp)
        
    f.close()
    
    problem_list = []
    for sentence in sentence_list:
        question_list = []
        temp_list = list(jieba.cut(sentence[0], cut_all=False))
        question = " ".join(temp_list)
        # print(question)
        question_list.append(question)
        candidate = ""
        for i in range(1, 5):
            temp_list = list(jieba.cut(sentence[i][3:], cut_all=False))
            candidate = " ".join(temp_list)
            # print(candidate)
            question_list.append(candidate)
        problem_list.append(question_list)
    
    for problems in problem_list:
        print(problems[0])
        s1_afv = avg_feature_vector(problems[0], model=model, num_features=50, index2word_set=index2word_set)
        for i in range(1, 5):
            s2_afv = avg_feature_vector(problems[i], model=model, num_features=50, index2word_set=index2word_set)
            sim = 1 - spatial.distance.cosine(s1_afv, s2_afv)
            print(sim)

if __name__ == "__main__":
    main()
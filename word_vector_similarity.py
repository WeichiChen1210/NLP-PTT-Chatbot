# -*- coding: utf-8 -*-
import numpy as np
from scipy import spatial
from gensim.models import word2vec
import jieba

jieba.set_dictionary('extra_dict/dict.txt.big')

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
    
    # input problems to sentence_list
    f = open('PPT_test_corpus.txt')
    sentence_list = []
    temp = ''
    for line in f:
        temp = []
        temp = line.strip().split('\t')
        sentence_list.append(temp)
        
    f.close()
    count = 1
    problem_list = []
    for sentence in sentence_list:
        question_list = []
        words = list(jieba.cut(sentence[0], cut_all=False))
        word = []
        for w in words:
            if w in model.wv.vocab:
                word.append(w)
        if len(word) == 0:
            print(count)
            print(words)
            question = " ".join(words)
        question = " ".join(word)
        # print(question)
        question_list.append(question)
        candidate = ""
        for i in range(1, 5):
            seg = []
            temp_list = list(jieba.cut(sentence[i][3:], cut_all=False))
            for c in temp_list:
                if c in model.wv.vocab:
                    seg.append(c)
            if len(seg) == 0:
                print(count)
                #print("empty")
                candidate = " ".join(temp_list)
                #print(candidate)
            else:
                candidate = " ".join(seg)
            
            question_list.append(candidate)
        problem_list.append(question_list)
        count += 1
    result = []
    count = 1
    for problems in problem_list:
        res = []
        index = 1
        print(problems[0])
        s1_afv = avg_feature_vector(problems[0], model=model, num_features=150, index2word_set=index2word_set)
        for i in range(1, 5):
            s2_afv = avg_feature_vector(problems[i], model=model, num_features=150, index2word_set=index2word_set)
            sim = 1 - spatial.distance.cosine(s1_afv, s2_afv)
            print(sim)
            resultInfo = {'id': index, 'score': sim}
            res.append(resultInfo)
            index += 1
        res.sort(key=lambda x: x['score'], reverse=True)
        temp = "[" + str(res[0]['id']) + "]\n"
        result.append(temp)
        count += 1
    print(len(result))
    fp = open("myans.txt", "w")
    fp.writelines(result)
    fp.close()
    print(count)

if __name__ == "__main__":
    main()
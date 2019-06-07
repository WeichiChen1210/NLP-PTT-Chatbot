from gensim.models import word2vec
import jieba

model = "wiki.word2vec_50.bin"
model_w2v = word2vec.Word2Vec.load(model)
candidates = []
with open('PPT_test_corpus.txt', encoding='utf-8') as f:
    for line in f:
        candidates.append(line.strip().split("("))

flag = False
res = []
index = 0
for items in candidates:
    print(items)
    # question
    question = items[0]
    words = list(jieba.cut(question.strip()))
    word = []
    for w in words:
        if w not in model_w2v.wv.vocab:
            print("input word %s not in dict. skip this turn" % w)
        else:
            word.append(w)
    print(word)

    # 4 candidates
    # print(len(items))
    candidate = items[1:]
    print(candidate)
    #     if c not in model_w2v.wv.vocab:
    #         print("candidate word %s not in dict. skip this turn" % c)
    #         flag = True
    # if flag:
    #     break
    # score = model_w2v.n_similarity(word, candidate)
    # resultInfo = {'id': index, 'score': score, 'text': " ".join(candidate)}
    # res.append(resultInfo)
    # index += 1
# res.sort(key=lambda x: x['score'], reverse=True)
# result = []
# for i in range(len(res)):
#     if res[i]['score'] > 0.80:
#         dict_temp = {res[i]['id']:res[i]['text'], 'score':res[i]['score']}
#         result.append(dict_temp)
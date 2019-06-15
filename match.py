from gensim.models import word2vec
import jieba

model = "ptt.word2vec_50.bin"
model_w2v = word2vec.Word2Vec.load(model)
candidates = []
with open('PPT_test_corpus.txt', encoding='utf-8') as f:
    for line in f:
        candidates.append(line.strip().split("\t"))
print(len(candidates))
fp = open("myans.txt", "w")

count = 1
result = []
for items in candidates:
    # first cut question and store in word
    question = items[0]
    # print(question)
    words = list(jieba.cut(question.strip()))
    word = []
    for w in words:
        if w not in model_w2v.wv.vocab:
            # print("input word %s not in dict. skip this turn" % w)
            flag = True
        else:
            word.append(w)
    # print(word)
    if len(word) == 0:
        print(count)
        print(question)
        print(words)
        result.append("[1]\n")
        continue

    # 4 candidates
    candidate = items[1:5]
    for i in range(len(candidate)):
        candidate[i] = candidate[i][3:]
    # print(candidate)

    flag = False
    res = []
    index = 1
    for options in candidate:
        seg = []
        # print(options)
        for c in options:
            if c not in model_w2v.wv.vocab:
                # print("candidate word %s not in dict. skip this turn" % c)
                flag = True
            else:
                seg.append(c)
        # print(len(seg))
        print(seg)
        print(word)
        if len(seg) != 0:       
            score = model_w2v.n_similarity(word, seg)
        else:
            score = 0
        # print(score)
        resultInfo = {'id': index, 'score': score, 'text': " ".join(options)}
        res.append(resultInfo)
        index += 1
    res.sort(key=lambda x: x['score'], reverse=True)
    # print(res[0]['text'])
    temp = "[" + str(res[0]['id']) + "]\n"
    result.append(temp)
    count += 1

# print(len(result))
fp = open("myans.txt", "w")
fp.writelines(result)
fp.close()
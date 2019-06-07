import jieba
seg_list = jieba.cut("今天晚餐的牛肉真的太好吃了", cut_all = True)
print("Full Mode: " + "/ ".join(seg_list))
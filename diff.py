correct_ans = open("correct_answer_file.txt", encoding = 'utf-8')
my_ans = open("myans.txt", encoding = 'utf-8')

count = 0
correct_cnt = 0

for line1, line2 in zip(correct_ans, my_ans):
    count += 1
    if line1 == line2:
        correct_cnt += 1
percent = correct_cnt / count
print(percent)

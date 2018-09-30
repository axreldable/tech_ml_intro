# a = 2 - 'fg'.__len__()
#
# slovo = 'word'
# len = slovo.__len__()
# for i in range(0, len-1):
#     print(slovo[:len-i])


def answers_list(sample, dict_with_answers):
    word11, word21 = sample.split(' ')
    rez = []
    len1 = word21.__len__()
    for i in range(0, len1 - 1):
        search_key = word11 + ' ' + word21[:len1 - i]
        if search_key in dict_with_answers:
            rez.append(dict_with_answers[search_key])
    return rez

dict = {'word1 wo': 'word1 wo', 'word1 wor': 'word1 wor', 'word1 worl': 'word1 worl'}

lists = answers_list('word1 world', dict)
for l in lists:
    print(l)

if lists.__len__() > 0:
    print(lists[0])




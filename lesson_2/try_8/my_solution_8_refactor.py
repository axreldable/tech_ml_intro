PATH_TRAIN = 'train.csv'
PATH_TEST = 'test.csv'

PATH_PRED = 'try_8/pred_8.csv'


# уменьшаем второе слово до 2 знаков и находим все совпадение в словаре - первое соответсвует самому длинному совпадению
def answers_list(sample, dict_with_answers):
    word11, word21 = sample.split(' ')
    rez = []
    len1 = word21.__len__()
    for i in range(0, len1 - 1):
        search_key = word11 + ' ' + word21[:len1 - i]
        if search_key in dict_with_answers:
            rez.append(dict_with_answers[search_key])
    return rez


word_stat_dict = {}
all_words_stat_dict = {}

fl = open(PATH_TRAIN, 'rt', encoding='utf-8')
fl.readline()
for line in fl:
    Id, Sample, Prediction = line.strip().split(',')
    ###############################
    # храним все значения слов, а не только первые 2 буквы
    if Sample not in all_words_stat_dict:
        all_words_stat_dict[Sample] = {}
    if Prediction not in all_words_stat_dict[Sample]:
        all_words_stat_dict[Sample][Prediction] = 0
    all_words_stat_dict[Sample][Prediction] += 1
    ##############################
    word1, word2 = Prediction.split(' ')
    key = word1 + ' ' + word2[:2]
    if key not in word_stat_dict:
        word_stat_dict[key] = {}
    if Prediction not in word_stat_dict[key]:
        word_stat_dict[key][Prediction] = 0
    word_stat_dict[key][Prediction] += 1
fl.close()

most_freq_dict = {}
for key in word_stat_dict:
    most_freq_dict[key] = max(word_stat_dict[key], key=word_stat_dict[key].get)

most_freq_dict_all = {}
for key in all_words_stat_dict:
    most_freq_dict_all[key] = max(all_words_stat_dict[key], key=all_words_stat_dict[key].get)

fl = open(PATH_TEST, 'rt', encoding='utf-8')
fl.readline()
out_fl = open(PATH_PRED, 'wt', encoding='utf-8')
out_fl.write('Id,Prediction\n')
for line in fl:
    Id, Sample = line.strip().split(',')
    answe_list = answers_list(Sample, most_freq_dict_all)
    if answe_list.__len__() > 0:
        # первый элемент списка содержит значение для ключа, наиболее близкого к исходному по длине
        out_fl.write('%s,%s\n' % (Id, answe_list[0]))
    else:
        # как в примере
        word1, word2_chunk = Sample.split(' ')
        key = word1 + ' ' + word2_chunk[:2]
        if key in most_freq_dict:
            out_fl.write('%s,%s\n' % (Id, most_freq_dict[key]))
        else:
            out_fl.write('%s,%s\n' % (Id, 'not use this value'))

fl.close()
out_fl.close()

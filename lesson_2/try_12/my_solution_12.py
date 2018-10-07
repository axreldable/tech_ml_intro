import pprint

# объявим где хранятся исходные данные
PATH_TRAIN = 'train.csv'
PATH_TEST = 'test.csv'

# объявим куда сохраним результат
PATH_PRED = 'try_12/pred_12.csv'
PATH_REZ = 'try_12/rez.csv'


## Из тренировочного набора собираем статистику о встречаемости слов

# создаем словарь для хранения статистики
word_stat_dict = {}
all_words_stat_dict = {}

# открываем файл на чтение в режиме текста
fl = open(PATH_TRAIN, 'rt', encoding='utf-8')

# считываем первую строчку - заголовок (она нам не нужна)
fl.readline()
c = 0
# в цикле читаем строчки из файла
for line in fl:
    c += 1
    # разбиваем строчку на три строковые переменные
    Id, Sample, Prediction = line.strip().split(',')
    word1, word2 = Sample.split(' ')
    # all_words_dict[Sample] = Prediction
    ###############################
    while len(word2) != 1:
        key = word1 + ' ' + word2
        if key not in all_words_stat_dict:
            all_words_stat_dict[key] = {}
        if Prediction not in all_words_stat_dict[key]:
            all_words_stat_dict[key][Prediction] = 0
        all_words_stat_dict[key][Prediction] += 1
        word2 = word2[:len(word2)-1]
    ##############################
    # строковая переменная Prediction - содержит в себе словосочетание из 2 слов, разделим их
    word1, word2 = Prediction.split(' ')
    # возьмем в качестве ключа 2 первые буквы, т.к. их наличие гарантировано
    key = word1 + ' ' + word2[:2]
    # если такого ключа еще нет в словаре, то создадим пустой словарь для этого ключа
    if key not in word_stat_dict:
        word_stat_dict[key] = {}
    # если текущее слово еще не встречалось, то добавим его в словарь и установим счетчик этого слова в 0
    if Prediction not in word_stat_dict[key]:
        word_stat_dict[key][Prediction] = 0
    # увеличим значение счетчика по текущему слову на 1
    word_stat_dict[key][Prediction] += 1

# закрываем файл
fl.close()

# print(word_stat_dict)
# print(all_words_dict)
# print(all_words_dict.__len__())
# print(c)
# print(len(all_words_stat_dict))
# pp = pprint.PrettyPrinter()
# pp.pprint(all_words_stat_dict)


##################################
# it's juct for seeing , not logic here
# fl = open(PATH_TRAIN, 'rt', encoding='utf-8')
# dict_with_variants = {}
# # считываем первую строчку - заголовок (она нам не нужна)
# fl.readline()
# c = 0
# # в цикле читаем строчки из файла
# for line in fl:
#     c += 1
#     # разбиваем строчку на три строковые переменные
#     Id, Sample, Prediction = line.strip().split(',')
#     all_words_dict[Sample] = Prediction
#     # строковая переменная Prediction - содержит в себе словосочетание из 2 слов, разделим их
#     word1, word2 = Prediction.split(' ')
#     # возьмем в качестве ключа 2 первые буквы, т.к. их наличие гарантировано
#     key = word1 + ' ' + word2[:2]
#     # если такого ключа еще нет в словаре, то создадим пустой словарь для этого ключа
#     if len(word_stat_dict[key]) > 1:
#         dict_with_variants[key] = word_stat_dict[key]
#
# # закрываем файл
# fl.close()
# print(len(word_stat_dict))
# pp = pprint.PrettyPrinter()
# pp.pprint(word_stat_dict)
##################################

## Строим модель

# создаем словарь для хранения статистики
most_freq_dict = {}
# проходим по словарю word_stat_dict
for key in word_stat_dict:
    # для каждого ключа получаем наиболее часто встречающееся (наиболее вероятное) слово и записываем его в словарь most_freq_dict
    most_freq_dict[key] = max(word_stat_dict[key], key=word_stat_dict[key].get)

most_freq_dict_all = {}
for key in all_words_stat_dict:
    most_freq_dict_all[key] = max(all_words_stat_dict[key], key=all_words_stat_dict[key].get)



## Выполняем предсказание

# открываем файл на чтение в режиме текста
fl = open(PATH_TEST, 'rt', encoding='utf-8')

# считываем первую строчку - заголовок (она нам не нужна)
fl.readline()

# открываем файл на запись в режиме текста
out_fl = open(PATH_PRED, 'wt', encoding='utf-8')

# записываем заголовок таблицы
out_fl.write('Id,Prediction\n')

dict = {}
most_freq_dict_dict = {}
# в цикле читаем строчки из тестового файла
for line in fl:
    # разбиваем строчку на две строковые переменные
    Id, Sample = line.strip().split(',')
    if Sample in most_freq_dict_all:
        out_fl.write('%s,%s\n' % (Id, most_freq_dict_all[Sample]))
    else:
        # только ключи, что длинее здесь
        for key in most_freq_dict_all:
            # print(Sample, ' - ', key)
            if Sample.startswith(key):
                if Sample not in dict:
                    dict[Sample] = {}
                if most_freq_dict_all[key].startswith(Sample): # могут быть лишние слова
                    if most_freq_dict_all[key] not in dict[Sample]:
                        dict[Sample][most_freq_dict_all[key]] = 0
                    dict[Sample][most_freq_dict_all[key]] += 1
        for key in dict:
            # для каждого ключа получаем наиболее часто встречающееся (наиболее вероятное) слово и записываем его в словарь most_freq_dict
            most_freq_dict_dict[key] = max(dict[key], key=dict[key].get)
        if Sample in most_freq_dict_dict:
            # если ключ есть в нашем словаре, пишем в файл предсказаний: Id, первое слово, наиболее вероятное второе слово
            # out_fl.write('%s,%s\n' % (Id, most_freq_dict[key]) )
            out_fl.write('%s,%s\n' % (Id, most_freq_dict_dict[Sample]) ) # здесь записываются только 200 значений
        else:
            # иначе пишем наиболее часто встречающееся словосочетание в целом
            out_fl.write('%s,%s\n' % (Id, 'super') )

# закрываем файлы
fl.close()
out_fl.close()

print(len(dict))
pp = pprint.PrettyPrinter()
pp.pprint(dict)

dict_with_test = {}
fl = open(PATH_TEST, 'rt', encoding='utf-8')
fl.readline()
for line in fl:
    Id, Sample = line.strip().split(',')
    dict_with_test[Id] = Sample
fl.close()

dict_with_rez = {}
fl = open(PATH_PRED, 'rt', encoding='utf-8')
fl.readline()
for line in fl:
    Id, Sample = line.strip().split(',')
    dict_with_rez[Id] = Sample
fl.close()

fl = open(PATH_PRED, 'rt', encoding='utf-8')
flw = open(PATH_REZ, 'wt', encoding='utf-8')
fl.readline()
for line in fl:
    Id, Sample = line.strip().split(',')
    # if dict_with_rez[Id] == 'что она':
    flw.write('%s,%s-%s\n' % (Id, dict_with_test[Id], dict_with_rez[Id]))
fl.close()
flw.close()





















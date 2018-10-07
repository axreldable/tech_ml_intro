import pprint

# объявим где хранятся исходные данные
PATH_TRAIN = 'train.csv'
PATH_TEST = 'test.csv'

# объявим куда сохраним результат
PATH_PRED = 'try_8/pred_8.csv'
PATH_REZ = 'try_8/rez.csv'


def answers_list(sample, dict_with_answers):
    word11, word21 = sample.split(' ')
    rez = []
    len1 = word21.__len__()
    for i in range(0, len1 - 1):
        search_key = word11 + ' ' + word21[:len1 - i]
        if search_key in dict_with_answers:
            rez.append(dict_with_answers[search_key])
    return rez


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
    # all_words_dict[Sample] = Prediction
    ###############################
    if Sample not in all_words_stat_dict:
        all_words_stat_dict[Sample] = {}
    if Prediction not in all_words_stat_dict[Sample]:
        all_words_stat_dict[Sample][Prediction] = 0
    all_words_stat_dict[Sample][Prediction] += 1
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

# в цикле читаем строчки из тестового файла
for line in fl:
    # разбиваем строчку на две строковые переменные
    Id, Sample = line.strip().split(',')
    answe_list = answers_list(Sample, most_freq_dict_all)
    if answe_list.__len__() > 0:
        out_fl.write('%s,%s\n' % (Id, answe_list[0]))
    else:
        # строковая переменная Sample содержит в себе полностью первое слово и кусок второго слова, разделим их
        word1, word2_chunk = Sample.split(' ')
        # вычислим ключ для заданного фрагмента второго слова
        key = word1 + ' ' + word2_chunk[:2]
        if key in most_freq_dict:
            # если ключ есть в нашем словаре, пишем в файл предсказаний: Id, первое слово, наиболее вероятное второе слово
            # out_fl.write('%s,%s\n' % (Id, most_freq_dict[key]) )
            out_fl.write('%s,%s\n' % (Id, 'pup') )
        else:
            # иначе пишем наиболее часто встречающееся словосочетание в целом
            out_fl.write('%s,%s\n' % (Id, 'super') )

# закрываем файлы
fl.close()
out_fl.close()

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





















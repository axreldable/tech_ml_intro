# объявим где хранятся исходные данные
PATH_TRAIN = 'train.csv'
PATH_TEST = 'test.csv'

# объявим куда сохраним результат
PATH_PRED = 'try_4/pred_4.csv'


## Из тренировочного набора собираем статистику о встречаемости слов

# создаем словарь для хранения статистики
word_stat_dict = {}
all_words_dict = {}

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
    # строковая переменная Prediction - содержит в себе словосочетание из 2 слов, разделим их
    word1, word2 = Prediction.split(' ')
    all_words_dict[word1 + ' ' + word2[:2]] = Prediction
    # возьмем в качестве ключа 2 первые буквы, т.к. их наличие гарантировано
    key = word2[:2]
    # если такого ключа еще нет в словаре, то создадим пустой словарь для этого ключа
    if key not in word_stat_dict:
        word_stat_dict[key] = {}
    # если текущее слово еще не встречалось, то добавим его в словарь и установим счетчик этого слова в 0
    if word2 not in word_stat_dict[key]:
        word_stat_dict[key][word2] = 0
    # увеличим значение счетчика по текущему слову на 1
    word_stat_dict[key][word2] += 1

# закрываем файл
fl.close()

print(all_words_dict)
print(all_words_dict.__len__())
print(c)

## Строим модель

# создаем словарь для хранения статистики
most_freq_dict = {}

# проходим по словарю word_stat_dict
for key in word_stat_dict:
    # для каждого ключа получаем наиболее часто встречающееся (наиболее вероятное) слово и записываем его в словарь most_freq_dict
    most_freq_dict[key] = max(word_stat_dict[key], key=word_stat_dict[key].get)


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
    if Sample in all_words_dict:
        out_fl.write('%s,%s\n' % (Id, all_words_dict[Sample]))
    else:
        # строковая переменная Sample содержит в себе полностью первое слово и кусок второго слова, разделим их
        word1, word2_chunk = Sample.split(' ')
        # вычислим ключ для заданного фрагмента второго слова
        key = word2_chunk[:2]
        if key in most_freq_dict:
            # если ключ есть в нашем словаре, пишем в файл предсказаний: Id, первое слово, наиболее вероятное второе слово
            out_fl.write('%s,%s %s\n' % (Id, word1, most_freq_dict[key]) )
        else:
            # иначе пишем наиболее часто встречающееся словосочетание в целом
            out_fl.write('%s,%s\n' % (Id, 'что она') )

# закрываем файлы
fl.close()
out_fl.close()

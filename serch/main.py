import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import pymorphy2
import re


def tokenize_search(file_text):
    tokens = word_tokenize(file_text, language="russian")
    tokens = [i for i in tokens if (i not in string.punctuation)]
    tokens = [i.split('.')[0] for i in tokens]
    tokens = [i.split(',')[0] for i in tokens]
    tokens = [i.split('⋅')[0] for i in tokens]
    tokens = [i.split('°')[0] for i in tokens]
    tokens = [i for i in tokens if i.isdigit() == False]
    stop_words = stopwords.words('russian')
    stop_words_eng = stopwords.words('english')
    stop_words_eng.extend(
        ['Y', 's', 'a', 'v', 'v1', 'v2', 't', 'k', 'A.', 'V', '°C', 'M☉', 'G', 'T', 'K', 'C', 'A', 'j200'])
    stop_words.extend(
        ['что', 'это', 'так', 'вот', 'макс.', 'мин.', 'м/с²', 'км²', 'км³', 'км/ч', 'м/с', ' м/с', 'км/с', 'кг',
         'г/см³', 'быть', 'как', 'в', '—',
         'к', 'на', 'комм.', 'а.е.', 'км', 'см', 'см.', 'У', 'а', 'км/c', 'v', 'Mo', 'отн', 'i', 'сут', 'млрд', 'c',
         'В',
         'с', 'мин', 'ч', '«', '»', 'А'])
    tokens = [i for i in tokens if (i not in stop_words and i not in stop_words_eng)]
    with open("token.txt", "w", encoding='UTF8') as token_file:
        for i in tokens:
            token_file.write(i + '\n')
    return tokens


if __name__ == '__main__':
    dict = {}
    name = "1"
    for i in range(100):
        with open("files/выкачка_" + (i + 1).__str__() + ".txt", "r", encoding='UTF8') as file:
            content = file.read()
            tokenize_search(content)
            # file_token = tokenize_search(content)
            # print(file_token)
        file_token = open("token.txt", "r", encoding='UTF8')
        dict.clear()
        morph = pymorphy2.MorphAnalyzer()
        lines = file_token.readlines()
        for j in lines:
            # print(j)
            j = j.replace('\n', '')
            if (morph.parse(j)[0].tag.POS != ('CONJ' or 'PREP' or 'PRCL' or 'INTJ' or 'ADVB' or 'ADVB' or 'PRED')) and (
                    j != ('еще' or 'ещё')):
                lemma = morph.parse(j)[0].normal_form
            if dict.get(lemma) is None:
                dict[lemma] = [j]
            else:
                dict[lemma].append(j)
        lemma_file = open("lemmas/lemma_" + (i + 1).__str__() + ".txt", "a", encoding='UTF8')
        for k, v in dict.items():
            # print(k, v)
            lemma_file.write(k)
            for a in v:
                lemma_file.write(" " + a)
            lemma_file.write("\n")

#  with open("files/выкачка_1.txt", "r", encoding='UTF8') as file:
# content = file.read(500)
#  file_token = tokenize_search(content)
#  print(file_token)
#  morph = pymorphy2.MorphAnalyzer()
#  for i in file_token:
#     print(morph.parse(i)[0].normal_form)

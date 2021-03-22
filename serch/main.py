import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import pymorphy2


def tokenize_search(file_text):
    tokens = word_tokenize(file_text, language="russian")
    tokens = [i for i in tokens if (i not in string.punctuation)]
    stop_words = stopwords.words('russian')
    stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', 'к', 'на', 'комм.', 'а.е.', 'км', 'см'])
    tokens = [i for i in tokens if (i not in stop_words)]
    with open("token.txt", "a", encoding='UTF8') as token_file:
        for i in tokens:
            token_file.write(i + '\n')
    return tokens


if __name__ == '__main__':
    dict = {}
    for i in range(100):
        with open("files/выкачка_" + (i + 1).__str__() + ".txt", "r", encoding='UTF8') as file:
            content = file.read()
            tokenize_search(content)
            #file_token = tokenize_search(content)
            #print(file_token)
    file_token = open("token.txt", "r", encoding='UTF8')
    morph = pymorphy2.MorphAnalyzer()
    lines = file_token.readlines()
    for j in lines:
        #print(j)
        j = j.replace('\n', '')
        lemma = morph.parse(j)[0].normal_form
        if dict.get(lemma) is None:
            dict[lemma] = [j]
        else:
            dict[lemma].append(j)
    lemma_file = open("lemma.txt", "a", encoding='UTF8')
    for k, v in dict.items():
        #print(k, v)
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

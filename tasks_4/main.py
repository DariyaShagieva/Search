import pandas
import pymorphy2
import math

siteLemmasMap = {}
siteLemmasCountMap = {}
siteMap = {}
tokenLemma = {}
sizeSiteLemma = {}

def createSiteLemmasMap():
    sitesFile = open('sites.txt', 'r')
    for line in sitesFile:
        lemmasMap = {}
        sizeSite = 0
        siteIndex = line.split(' ')[0]
        url = line.split(' ')[1]
        siteMap[siteIndex] = url
        siteLemmas = open("lemmas/lemma_" + siteIndex + ".txt", "r", encoding='UTF8')
        for lineSite in siteLemmas:
            lemmas = lineSite.split(' ')
            lemma = lemmas[0]
            lemmasMap[lemma] = len(lemmas)
            sizeSite += len(lemmas)
        siteLemmasCountMap[siteIndex] = lemmasMap
        sizeSiteLemma[siteIndex] = sizeSite




# Создается инвертированный список
def createSitesIndexMap():
    sitesFile = open('sites.txt', 'r')
    for line in sitesFile:
        siteIndex = line.split(' ')[0]
        url = line.split(' ')[1]
        siteMap[siteIndex] = url
        siteLemmas = open("lemmas/lemma_" + siteIndex + ".txt", "r", encoding='UTF8')
        for lineSite in siteLemmas:
            lemma = lineSite.split(" ")[0]
            if lemma in siteLemmasMap:
                siteLemmasMap.get(lemma).append(siteIndex)
        siteLemmas.close()
    sitesFile.close()


# Получаем список лемм
def getLemmas(fileName):
    lemmasFile = open(fileName, "r", encoding='UTF8')
    for line in lemmasFile:
        lemma = line.split(" ")[0]
        if lemma not in siteLemmasMap:
            siteLemmasMap[lemma] = []


if __name__ == '__main__':
    getLemmas("lemma.txt")
    createSiteLemmasMap()
    createSitesIndexMap()
    #print(siteLemmasMap.get('Земли'))

    # считаем tf для каждого слова в каждом файле
    tfs = {}
    for site in siteMap:
        termins = siteLemmasCountMap.get(site)
        sizeSite = sizeSiteLemma.get(site)
        for termin in termins:
            tf = termins.get(termin) / sizeSite
            if termin not in tfs:
                tfs[termin] = {}
            tfs[termin][siteMap.get(site)] = tf
    # вывод таблицы
    #data_tf = pandas.DataFrame(tfs).T
    #print(data_tf)

    # считаем idf для каждого термина
    idfs = {}
    for termin in siteLemmasMap:
        length_ter = len(siteLemmasMap.get(termin))
        if length_ter == 0:
            length_ter = 1
        idfs[termin] = math.log(len(siteMap) / length_ter)

    # вывод таблицы
    #data_idf = pandas.DataFrame(idfs, index=['']).T
    #print(data_idf)

    # считаем tf-idf для каждого слова
    tf_idfs = {}
    for termin in tfs:
        for site in tfs[termin]:
            tf_idf = idfs[termin] * tfs[termin][site]
            if termin not in tf_idfs:
                tf_idfs[termin] = {}
            tf_idfs[termin][site] = tf_idf
        #print(tf_idfs[termin])

    # вывод таблицы
    #data_tf_idf = pandas.DataFrame(tf_idfs).T
    #print(data_tf_idf)

    # запись в файл
    list_termin = open("list_termin.txt", "a", encoding='UTF8')
    for termin in tfs:
        for s in tfs[termin]:
            list_termin.write(termin + " idf: " + idfs[termin].__str__() + " tf-idf: " + tf_idfs[termin][s].__str__() + "для сайта" + s)

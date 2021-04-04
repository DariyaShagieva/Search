import math

from TfIdfSites import TfIdfSites
import pymorphy2

tf_idf = TfIdfSites()


def countLen(vector):
    sum_len = 0
    for x in vector:
        sum_len += vector[x] ** 2
    return math.sqrt(sum_len)


def find(query):
    query = query.split(' ')
    tfs = {}
    lemmas = list()
    for site in tf_idf.siteMap:
        termins = tf_idf.siteLemmasCountMap.get(site)
        sizeSite = tf_idf.sizeSiteLemma.get(site)
        for word in query:
            word = getLemma(word)
            lemmas.append(word)
            tfs = tf_idf.getTfs(termins, word, tfs, sizeSite, site)

    idfs = tf_idf.getIdfs(lemmas)
    tfIdf = tf_idf.getTfIdf(tfs, idfs)

    cos_sim = {}
    for site in tf_idf.siteMap:
        cs = -10
        for word in lemmas:
            if word in tfs and tf_idf.siteMap.get(site) in tfs[word]:
                cs = math.cos(tf_idf.tfIdfs[word][tf_idf.siteMap.get(site)] * tfIdf[word][tf_idf.siteMap.get(site)])
        cos_sim[site] = cs

    list_d = list(cos_sim.items())
    list_d.sort(key=lambda i: i[1], reverse=True)

    for site in list_d:
        if site[1] != -1:
            print(tf_idf.siteMap.get(site[0]))


def getLemma(word):
    morph = pymorphy2.MorphAnalyzer()
    return morph.parse(word)[0].normal_form


if __name__ == '__main__':
    tf_idf.tf_idf_sites()

    while 1:
        query = input("Введите запрос: ")
        find(query)

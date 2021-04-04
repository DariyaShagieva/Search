import math

import pandas


class TfIdfSites:

    def __init__(self):
        """Constructor"""
        self.siteLemmasMap = {}
        self.siteLemmasCountMap = {}
        self.siteMap = {}
        self.tokenLemma = {}
        self.sizeSiteLemma = {}
        self.tfIdfs = {}

    def createSiteLemmasMap(self):
        sitesFile = open('sites.txt', 'r')
        for line in sitesFile:
            lemmasMap = {}
            sizeSite = 0
            siteIndex = line.split(' ')[0]
            url = line.split(' ')[1]
            self.siteMap[siteIndex] = url
            siteLemmas = open("lemmas/lemma_" + siteIndex + ".txt", "r", encoding='UTF8')
            for lineSite in siteLemmas:
                lemmas = lineSite.split(' ')
                lemma = lemmas[0]
                lemmasMap[lemma] = len(lemmas)
                sizeSite += len(lemmas)
            self.siteLemmasCountMap[siteIndex] = lemmasMap
            self.sizeSiteLemma[siteIndex] = sizeSite

    # Создается инвертированный список
    def createSitesIndexMap(self):
        sitesFile = open('sites.txt', 'r')
        for line in sitesFile:
            siteIndex = line.split(' ')[0]
            url = line.split(' ')[1]
            self.siteMap[siteIndex] = url
            siteLemmas = open("lemmas/lemma_" + siteIndex + ".txt", "r", encoding='UTF8')
            for lineSite in siteLemmas:
                lemma = lineSite.split(" ")[0]
                if lemma in self.siteLemmasMap:
                    self.siteLemmasMap.get(lemma).append(siteIndex)
            siteLemmas.close()
        sitesFile.close()

    # Получаем список лемм
    def getLemmas(self, fileName):
        lemmasFile = open(fileName, "r", encoding='UTF8')
        for line in lemmasFile:
            lemma = line.split(" ")[0]
            if lemma not in self.siteLemmasMap:
                self.siteLemmasMap[lemma] = []

    def getTfsSites(self):
        # считаем tf для каждого слова в каждом файле
        tfs = {}
        for site in self.siteMap:
            termins = self.siteLemmasCountMap.get(site)
            sizeSite = self.sizeSiteLemma.get(site)
            for termin in termins:
                self.getTfs(termins, termin, tfs, sizeSite, site)
        return tfs

    def getTfs(self, termins, termin, tfs, sizeSite, site):
        if termin in termins:
            tf = termins.get(termin) / sizeSite
            if termin not in tfs:
                tfs[termin] = {}
            tfs[termin][self.siteMap.get(site)] = tf
        return tfs

    def getIdfs(self, termins):
        idfs = {}
        for termin in termins:
            if (termin in self.siteLemmasMap):
                length_ter = len(self.siteLemmasMap.get(termin))
                if length_ter == 0:
                    length_ter = 1
                idfs[termin] = math.log(len(self.siteMap) / length_ter)
        return idfs

    def getTfIdf(self, tfs, idfs):
        tf_idfs = {}
        for termin in tfs:
            for site in tfs[termin]:
                tf_idf = idfs[termin] * tfs[termin][site]
                if termin not in tf_idfs:
                    tf_idfs[termin] = {}
                tf_idfs[termin][site] = tf_idf
        return tf_idfs

    def tf_idf_sites(self):
        self.getLemmas("lemma.txt")
        self.createSiteLemmasMap()
        self.createSitesIndexMap()
        # print(siteLemmasMap.get('Земли'))

        # вывод таблицы
        # data_tf = pandas.DataFrame(tfs).T
        # print(data_tf)

        tfs = self.getTfsSites()

        # считаем idf для каждого термина

        idfs = self.getIdfs(self.siteLemmasMap)

        # вывод таблицы
        # data_idf = pandas.DataFrame(idfs, index=['']).T
        # print(data_idf)

        # считаем tf-idf для каждого слова
        tf_idfs = self.getTfIdf(tfs, idfs)
        self.tfIdfs = tf_idfs
            # print(tf_idfs[termin])

        # вывод таблицы
        # data_tf_idf = pandas.DataFrame(tf_idfs).T
        # print(data_tf_idf)

        # запись в файл
        # list_termin = open("list_termin.txt", "a", encoding='UTF8')
        # for termin in tfs:
        #     for s in tfs[termin]:
        #         list_termin.write(termin + " idf: " + idfs[termin].__str__() + " tf-idf: " + tf_idfs[termin][
        #             s].__str__() + "для сайта" + s)

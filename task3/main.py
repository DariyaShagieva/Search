import pymorphy2

siteLemmasMap = {}
siteMap = {}
tokenLemma = {}


# Поиск
def find(query):
    query = query.split(' ')
    for word in query:
        word = getLemma(word)
        answer = set()
        index = 0
        if word in siteLemmasMap:
            sites = set(siteLemmasMap.get(word))
            if index == 0:
                answer = sites
            else:
                answer.intersection(sites)
            index += 1
    return answer


# Создается инвертированный список
def createSitesIndexMap():
    sitesFile = open('sites.txt', 'r')
    for line in sitesFile:
        siteIndex = line.split(' ')[0]
        url = line.split(' ')[1]
        siteMap[siteIndex] = url
        siteLemmas = open("lemmas/lemma_" + siteIndex + ".txt", "r")
        for lineSite in siteLemmas:
            lemma = lineSite.split(" ")[0]
            if lemma in siteLemmasMap:
                siteLemmasMap.get(lemma).append(siteIndex)
        siteLemmas.close()
    sitesFile.close()


# Получаем список лемм
def getLemmas(fileName):
    lemmasFile = open(fileName, "r")
    for line in lemmasFile:
        lemma = line.split(" ")[0]
        if lemma not in siteLemmasMap:
            siteLemmasMap[lemma] = []


def getLemma(word):
    morph = pymorphy2.MorphAnalyzer()
    return morph.parse(word)[0].normal_form


if __name__ == '__main__':
    getLemmas("lemma.txt")
    createSitesIndexMap()

    while 1:
        query = input("Введите запрос: ")
        answer = find(query)
        print(answer)
        for i in answer:
            print(siteMap[i])

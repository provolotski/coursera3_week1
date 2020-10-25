from bs4 import BeautifulSoup
import unittest

def soupiteration(soup):
    tag = ''
    maxiterator = 0
    currentiterator = 0
    for iter in soup.findAll(True):
        if len(iter)>1:
            print(iter.name,len(iter), iter)
        else:
            print(iter.name,len(iter), iter(1,))

def parse(path_to_file):
    # Поместите ваш код здесь.
    # ВАЖНО!!!
    # При открытии файла, добавьте в функцию open необязательный параметр
    # encoding='utf-8', его отсутствие в коде будет вызвать падение вашего
    # решения на грейдере с ошибкой UnicodeDecodeError
    file = open(path_to_file, encoding='utf-8')
    soup = BeautifulSoup(file,"lxml")
    body = soup.html.body
    bodytag = body.find("div", {"id": "bodyContent"})
    imgs, headers, linkslen, lists = 0, 0, 0, 0
    # ищем картинки
    for img in bodytag.findAll('img'):
        print(img)
        imgs += 1 if int(img['width'])>=200 else 0
    # ищем headers
    for header in bodytag.findAll(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        for i in range(len(header)):
            if header.contents[i].string is not None:
                headers += 1 if header.contents[i].string[0] in ('E', 'T', 'C') else 0
    # ищем последовательности

    soupiteration(bodytag)

    #    if header.string is not None:
     #       headers += 1 if header.string[0] in ('E', 'T', 'C') else 0
        #if header.string[0] in ()


    return [imgs, headers, linkslen, lists]

def test_parse():
    test_cases = (
            ('wiki/Stone_Age', [13, 10, 12, 40]),
    #        ('wiki/Brain', [19, 5, 25, 11]),
    #        ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
    #        ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
    #        ('wiki/Spectrogram', [1, 2, 4, 7]),
    )
    for path, expected in test_cases:
        print(parse(path))

if __name__ == '__main__':
    test_parse()
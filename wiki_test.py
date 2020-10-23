from bs4 import BeautifulSoup
import unittest


def get_image_count(soup):
    num: int = 0
    for iterator in soup.findAll(name="img"):
        if not int(iterator["width"]) < 200:
            num += 1
    return num


def get_header_count(soup):
    num = 0
    for iterator in soup.findAll(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        if iterator.string is None:
            for txt in iterator.findAll(True):
                if txt.string is not None and txt.string[0] in ('E', 'T', 'C'):
                    num += 1
        else:
            if iterator.string[0] in ('E', 'T', 'C'):
                num += 1
    return num


def get_max_tag_len(soup):
    list = []
    iterator = 0
    for i in soup:
        if i != '\n' and i.name is not None:
            if i.name == 'a':
                iterator += 1
            else:
                if iterator > 0:
                    list.append(iterator)
                iterator = 1
            list.extend(get_max_tag_len(i))
    if iterator > 0:
        list.append(iterator)
    return list

def get_max_list_len(soup):
    list = []
    iterator = 0
    for i in soup:
        if i != '\n' and i.name is not None:
            if i.name in ('ul','ol'):
                iterator += 1
            else:
                if iterator > 0:
                    list.append(iterator)
                iterator = 1
            list.extend(get_max_tag_len(i))
    if iterator > 0:
        list.append(iterator)
    return list



def parse(path_to_file):
    # Поместите ваш код здесь.
    # ВАЖНО!!!
    # При открытии файла, добавьте в функцию open необязательный параметр
    # encoding='utf-8', его отсутствие в коде будет вызвать падение вашего
    # решения на грейдере с ошибкой UnicodeDecodeError
    page = open(path_to_file, encoding='utf-8')
    soup = BeautifulSoup(page.read(), "lxml")
    body = soup.find(name='div', id="bodyContent")
    imgs = get_image_count(body)
    headers = get_header_count(body)
    linkslen_list = get_max_tag_len(body)
    linkslen_list.sort(reverse=True)
    if len(linkslen_list) > 0:
        linkslen = linkslen_list[0]
    else:
        linkslen = 0

    linkslen_list = get_max_tag_len(body)
    linkslen_list.sort(reverse=True)
    if len(linkslen_list) > 0:
        lists = linkslen_list[0]
    else:
        lists = 0

    lists = 0

    return [imgs, headers, linkslen, lists]


# class TestParse(unittest.TestCase):
#    def test_parse(self):
#        test_cases = (
#            ('wiki/Stone_Age', [13, 10, 12, 40]),
#            ('wiki/Brain', [19, 5, 25, 11]),
#            ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
#            ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
#            ('wiki/Spectrogram', [1, 2, 4, 7]),)

#        for path, expected in test_cases:
#            with self.subTest(path=path, expected=expected):
#                self.assertEqual(parse(path), expected)

def parse_1():
    test_cases = (
        ('wiki/Stone_Age', [13, 10, 12, 40]),
        #   ('wiki/Brain', [19, 5, 25, 11]),
        #   ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
        #   ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
        #   ('wiki/Spectrogram', [1, 2, 4, 7]),
    )
    for path, expected in test_cases:
        print(parse(path))


if __name__ == '__main__':
    parse_1()

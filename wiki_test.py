import unittest
from bs4 import BeautifulSoup
import os


def get_image_count(soup):
    num: int = 0
    for iterator in soup.findAll(name="img"):
        try:
            if not int(iterator["width"], 0) < 200:
                num += 1
        except KeyError:
            pass
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
    tag_list = []
    iterator = 0
    for i in soup:
        if i != '\n' and i.name is not None:
            if i.name == 'a':
                iterator += 1
            else:
                if iterator > 0:
                    tag_list.append(iterator)
                iterator = 0
            tag_list.extend(get_max_tag_len(i))
    if iterator > 0:
        tag_list.append(iterator)
    return tag_list


def get_max_list_len(soup):
    iterator = 0
    for i in soup:
        if i != '\n' and i.name is not None:
            if i.name in ('ul', 'ol'):
                iterator += 1
            else:
                iterator += get_max_list_len(i)
    return iterator


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

    lists = get_max_list_len(body)
    page.close()
    return [imgs, headers, linkslen, lists]


def get_URL_list(path, page):
    if not os.path.isfile(path + page):
        return []
    with open(os.path.join(path, page), encoding="utf-8") as file:
        soup = BeautifulSoup(file.read(), "lxml")
        list = []
        body = soup.find(name='div', id="bodyContent")
        for i in body.findAll(name='a', href=True):
            if i['href'][0:6] == '/wiki/':
                if os.path.isfile('wiki/' + i['href'][6:]) and i['href'][6:] not in list:
                    list.append(i['href'][6:])
        return list



def build_bridge(path, start_page, end_page):
    full = {}
    if start_page == end_page:
        return path
    else:
        flag = True
        count = 1
        full[count] = [[start_page]]
        while flag:
            for item in full[count]:
                for node in get_URL_list(path, item[-1]):
                    if node not in item:
                        if node == end_page:
                            result_path = item.copy()
                            result_path.append(node)
                            flag = False
                        else:
                            item_path = item.copy()
                            item_path.append(node)
                            if full.get(count + 1) is None:
                                full[count + 1] = [item_path]
                            else:
                                lst = full.get(count + 1)
                                lst.append(item_path)
                                full[count + 1] = lst
            count += 1
        return result_path


def get_statistics(path, start_page, end_page):
    """собирает статистику со страниц, возвращает словарь, где ключ - название страницы,
    значение - список со статистикой страницы"""
    # получаем список страниц, с которых необходимо собрать статистику
    pages = build_bridge(path, start_page, end_page)
    # напишите вашу реализацию логики по сбору статистики здесь
    statistic = {}
    for page in pages:
        statistic[page] = parse(path+page)
    return statistic


# class TestParse(unittest.TestCase):
#     def test_parse(self):
#         test_cases = (
#             ('wiki/Stone_Age', [13, 10, 12, 40]),
#             ('wiki/Brain', [19, 5, 25, 11]),
#             ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
#             ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
#             ('wiki/Spectrogram', [1, 2, 4, 7]),)
#
#         for path, expected in test_cases:
#             with self.subTest(path=path, expected=expected):
#                 self.assertEqual(parse(path), expected)

    # def test_path(self):
    #     test_cases = (
    #         (('wiki/', 'The_New_York_Times', 'Stone_Age'),
    #          ['The_New_York_Times', 'London', 'Woolwich', 'Iron_Age', 'Stone_Age']),
    #         (('wiki/', 'The_New_York_Times', 'The_New_York_Times'),
    #          ['The_New_York_Times']),
    #     )
    #     for arg, res in test_cases:
    #         self.assertEqual(generate_bridge(arg), res)



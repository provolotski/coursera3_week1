from bs4 import BeautifulSoup
import unittest
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
    list = []
    iterator = 0
    for i in soup:
        if i != '\n' and i.name is not None:
            if i.name == 'a':
                iterator += 1
            else:
                if iterator > 0:
                    list.append(iterator)
                iterator = 0
            list.extend(get_max_tag_len(i))
    if iterator > 0:
        list.append(iterator)
    return list


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
                if os.path.isfile('wiki/' + i['href'][6:]):
                    list.append(i['href'][6:])
        return list


def update_list(graph, full_list, current_list):
    new_list = []
    for i in current_list:
        if (i not in graph.keys()) and (i not in full_list):
            new_list.append(i)
    return new_list


def build_bridge(path, start_page, end_page):
    """возвращает список страниц, по которым можно перейти по ссылкам со start_page на
    end_page, начальная и конечная страницы включаются в результирующий список"""
    graph = {}
    list_url = []
    graph[start_page] = get_URL_list(path, start_page)
    if end_page not in graph[start_page]:
        list_url += update_list(graph, list_url, graph[start_page])
    while len(list_url) > 0:
        next_url = list_url.pop()
        if len(get_URL_list(path, next_url)) > 0:
            graph[next_url] = get_URL_list(path, next_url)
            if end_page not in graph[start_page]:
                list_url += update_list(graph, list_url, graph[next_url])
        print(f'len of list {len(list_url)}  list is {list_url}')
      #  print(f'dicts is {graph}')

    return graph
    # напишите вашу реализацию логики по вычисления кратчайшего пути здесь


def get_statistics(path, start_page, end_page):
    """собирает статистику со страниц, возвращает словарь, где ключ - название страницы,
    значение - список со статистикой страницы"""

    # получаем список страниц, с которых необходимо собрать статистику
    pages = build_bridge(path, start_page, end_page)
    # напишите вашу реализацию логики по сбору статистики здесь
    statistic = None
    return statistic


class TestParse(unittest.TestCase):
    def test_parse(self):
        test_cases = (
            ('wiki/Stone_Age', [13, 10, 12, 40]),
            ('wiki/Brain', [19, 5, 25, 11]),
            ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
            ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
            ('wiki/Spectrogram', [1, 2, 4, 7]),)

        for path, expected in test_cases:
            with self.subTest(path=path, expected=expected):
                self.assertEqual(parse(path), expected)


def test_case():
    result = build_bridge('wiki/', 'The_New_York_Times', 'Stone_Age')
    print(result)
    print(len(result))


if __name__ == '__main__':
    # unittest.main()
    test_case()

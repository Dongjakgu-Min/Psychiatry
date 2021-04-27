import requests
import kss
from bs4 import BeautifulSoup
from collections import Counter
from tqdm import tqdm


def get_link(keyword):
    links = []
    for i in range(1, 1001, 10):
        links.append("""
        https://search.naver.com/search.naver?where=kin&kin_display=10&qt=&title=0&&answer=0&grade=0&choice=0&sec=0&
        nso=so%3Ar%2Ca%3Aall%2Cp%3Aall&query={0}&c_id=&c_name=&
        sm=tab_pge&kin_start={1}&kin_age=0
        """.format(keyword ,i))

    questions = []

    for link in links:
        html = requests.get(link)
        soup = BeautifulSoup(html.text, 'html.parser')

        urls = soup.select('.question_group > a')
        for url in urls:
            questions.append(url['href'])

    return questions


def kin_parse(url):
    html = requests.get(url)
    # print(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    # Error 1. Title에 content 내용이 있는 경우
    content = soup.select_one('.c-heading__content')
    if content is None:
        content = soup.select_one('.c-heading__title-inner > div')
    return kss.split_sentences(content.text)


class KinParser:
    ner = None
    spacing = None

    def __init__(self, keyword):
        self.keyword = keyword

    @classmethod
    def set_parser(cls, ner, spacing):
        cls.ner = ner
        cls.spacing = spacing

    def get_token(self):
        links = get_link(self.keyword)
        result = {'keyword': self.keyword}
        token = []

        for link in tqdm(links):
            for sentence in kin_parse(link):
                try:
                    token.extend(KinParser.ner(sentence))
                except ValueError:
                    print('초과')

        result['token'] = Counter(token)
        return result

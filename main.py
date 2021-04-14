#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
from pororo import Pororo
from wordcloud import WordCloud
from collections import Counter
import kss


def get_link(url):
    result = []
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    urls = soup.select('.question_group > a')
    for link in urls:
        result.append(link['href'])
    return result


def kin_parse(url):
    html = requests.get(url)
    # print(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    # Error 1. Title에 content 내용이 있는 경우
    content = soup.select_one('.c-heading__content')
    if content is None:
        return ''
    return kss.split_sentences(content.text)


def main():
    ner = Pororo(task="ner", lang="ko")
    links = []
    kin_links = []

    print(Pororo.available_tasks())

    print('load page link...')
    for i in tqdm(range(1, 1000, 10)):
        raw_link = 'https://search.naver.com/search.naver?where=kin&kin_display=10&qt=&title=0&&answer=0&grade=0&choice=0&sec=0&nso=so%3Ar%2Ca%3Aall%2Cp%3Aall&query=%EC%A0%95%EC%8B%A0%EA%B3%BC+%EC%9A%B0%EC%9A%B8%EC%A6%9D&c_id=&c_name=&sm=tab_pge&kin_start={0}&kin_age=0'.format(
            i)
        links.append(raw_link)

    print('get kin link...')
    for naver_link in tqdm(links):
        print(naver_link)
        kin_links.extend(get_link(naver_link))
    questions = []

    for kin_link in tqdm(kin_links):
        # Error 2. 글자 수가 Pororo가 처리할 수 있는 내용 이상
        print(kin_link)
        for line in kin_parse(kin_link):
            if len(line) > 1500:
                pass
            else:
                questions.extend(ner(line))

    result = Counter(questions)
    print(result)

if __name__ == '__main__':
    main()

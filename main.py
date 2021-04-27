#!/usr/bin/python
# -*- coding: utf-8 -*-
from tqdm import tqdm
from pororo import Pororo
from collections import Counter

from Parser import KinParser


def main():
    ner = Pororo(task="ner", lang="ko")
    spacing = Pororo(task="gec", lang="ko")
    KinParser.set_parser(ner, spacing)

    dep = KinParser('우울증')
    result = dep.get_token()

    print(result)

if __name__ == '__main__':
    main()

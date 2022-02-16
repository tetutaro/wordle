#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import annotations
from typing import Optional
import sys
import os
import subprocess
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import re
import gzip
from logging import Logger, getLogger, Formatter, StreamHandler, INFO

IS_5LETTERS = re.compile(r'^[a-z]{5}$')


class Wiktionary(object):
    def __init__(
        self: Wiktionary,
        logger: Logger
    ) -> None:
        self.logger = logger
        self._scrape_wikimedia()
        return

    def _scrape_wikimedia(self: Wiktionary) -> None:
        '''scrape wikimedia and get the latest version
        '''
        # scrape jawiki top page
        url = 'https://dumps.wikimedia.org/enwiktionary/'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        versions = list()
        for a in soup.find_all('a'):
            href = a.get('href')
            if not href.startswith(('.', 'latest')):
                versions.append(href.split(os.sep)[0])
        # get latest and valid version
        found = False
        for version in sorted(versions, reverse=True):
            found = self._scrape_wikimedia_page(version=version)
            if found is True:
                break
        if found is False:
            raise SystemError('valid wikipedia dump version not found')
        return

    def _scrape_wikimedia_page(self: Wiktionary, version: str) -> bool:
        '''scrape wikimedia and get the URL of dump data
        '''
        self.logger.debug(f'check version: {version}')
        filename = (
            f'enwiktionary-{version}-abstract.xml.gz'
        )
        extract_dir = f'enwiktionary_{version}'
        # scrape latest page
        url = f'https://dumps.wikimedia.org/enwiktionary/{version}/'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        fpath = None
        for a in soup.find_all('a'):
            if a.string == filename:
                fpath = a.get('href')
                break
        if fpath is None:
            return False
        self.logger.info(f'latest version: {version}')
        self.version = version
        self.filename = filename
        self.extract_dir = extract_dir
        self.file_url = 'https://dumps.wikimedia.org' + fpath
        return True

    def download(self: Wiktionary) -> None:
        '''downloads english wiktionary
        '''
        if os.path.isdir(self.extract_dir):
            self.logger.info('already extracted. skip download.')
            return
        if os.path.isfile(self.filename):
            self.logger.info('already downloaded. skip download.')
            return
        try:
            subprocess.run(
                ['wget', '-O', self.filename, self.file_url], check=True
            )
        except (subprocess.CalledProcessError, KeyboardInterrupt) as e:
            if os.path.exists(self.filename):
                os.remove(self.filename)
            raise e
        return

    def extract(self: Wiktionary) -> None:
        '''extract word and write
        '''
        words = set()
        assert os.path.exists(self.filename)
        with gzip.open(self.filename, mode='rt') as rf:
            cache = ''
            flag = False
            line = rf.readline()
            while line:
                line = line.strip()
                if line == '<doc>':
                    cache == ''
                    flag = True
                if flag is True:
                    cache += line
                if line == '</doc>':
                    word = self._extract_word(xml=cache)
                    if word is not None:
                        words.add(word)
                    flag = False
                    cache = ''
                line = rf.readline()
        self.words = words
        return

    def _extract_word(self: Wiktionary, xml: str) -> Optional[str]:
        root = ET.fromstring(xml)
        title = root.find('title').text
        abst = root.find('abstract').text
        word = title.split(':', 2)[1].strip()
        if abst == '==English==' and IS_5LETTERS.match(word) is not None:
            return word
        return None

    def freq(self: Wiktionary) -> None:
        word_freq = dict()
        max_freq = 0
        with open('unigram_freq.csv', 'rt') as rf:
            line = rf.readline()
            header = True
            while line:
                if header is True:
                    header = False
                    line = rf.readline()
                    continue
                word, freq = line.strip().split(',')
                word = word.strip()
                if word in self.words:
                    freq = int(freq.strip())
                    if freq > max_freq:
                        max_freq = freq
                    word_freq[word] = freq
                line = rf.readline()
        self.max_freq = max_freq
        self.word_freq = word_freq
        return

    def write(self: Wiktionary) -> None:
        with open('words.py', 'wt') as wf:
            header = '''#!/usr/bin/env python
# -*- coding:utf-8 -*-

words = [
'''
            tailer = ']\n'
            wf.write(header)
            for word, freq in sorted(
                self.word_freq.items(),
                key=lambda x: x[1],
                reverse=True
            ):
                wf.write(
                    '    ('
                    f'"{word}", '
                    f'{round(float(freq) / self.max_freq, 6):.6f}'
                    '),\n'
                )
            wf.write(tailer)
        return

    def remove(self: Wiktionary) -> None:
        os.remove(self.filename)
        return


def main() -> None:
    # setup logger
    logger = getLogger(__file__)
    logger.setLevel(INFO)
    formatter = Formatter('%(asctime)s: %(levelname)s: %(message)s')
    handler = StreamHandler(stream=sys.stdout)
    handler.setLevel(INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    wiktionary = Wiktionary(logger=logger)
    wiktionary.download()
    wiktionary.extract()
    wiktionary.freq()
    wiktionary.write()
    wiktionary.remove()
    return


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import annotations
from typing import List, Dict
from logging import Logger
from enum import Enum
import re
import numpy as np
from pydantic import BaseModel

FREQ_THRESHOLD = 0.0001


class WordleStatus(Enum):
    OPEN = 'open'
    WORD = 'waiting-word'
    RGHT = 'right'
    WRNG = 'wrong'


class LetterStatus(Enum):
    BLNK = 'blank'
    CORR = 'correct'
    SPOT = 'spot'
    MISS = 'miss'


class WordleLetter(BaseModel):
    letter: str = ' '
    status: LetterStatus = LetterStatus.BLNK


class WordleInfo(BaseModel):
    message: str = ''
    status: WordleStatus = WordleStatus.OPEN
    letters: List[WordleLetter] = [WordleLetter() for _ in range(30)]
    keyboards: Dict[str, LetterStatus] = {
        w: LetterStatus.BLNK for w in list('qwertyuiopasdfghjklzxcvbnm')
    }


class Wordle():
    def __init__(self: Wordle, logger: Logger) -> None:
        self.logger = logger
        self.answer = None
        self.offset = 0
        self.info = WordleInfo()
        self._read_words()
        self._choose_answer()
        return

    def _read_words(self: Wordle) -> None:
        words = list()
        freqs = list()
        with open('scripts/words.csv', 'rt') as rf:
            line = rf.readline()
            while line:
                word, freq = line.strip().split(',', 2)
                freq = float(freq)
                if FREQ_THRESHOLD is not None and freq >= FREQ_THRESHOLD:
                    words.append(word)
                    freqs.append(freq)
                line = rf.readline()
        self.num_words = len(words)
        self.words = words
        self.weights = np.array(freqs)
        self.weights /= self.weights.sum()
        self.logger.debug(f'load {self.num_words} words')
        return

    def _choose_answer(self: Wordle) -> None:
        assert(self.answer is None)
        idx = np.random.choice(self.num_words, 1, p=self.weights)[0]
        self.answer = self.words[idx]
        self.logger.debug(f'answer = {self.answer}')
        return

    def append_letter(self: Wordle, key: str) -> None:
        self.logger.debug(f'append_letter: key = {key}')
        self.info.message = ''
        if self.info.status != WordleStatus.OPEN:
            return
        assert(re.match(r'^[a-z]$', key) is not None)
        self.info.letters[self.offset].letter = key
        self.offset += 1
        if self.offset % 5 == 0:
            self.info.status = WordleStatus.WORD
        return

    def confirm_word(self: Wordle) -> None:
        self.logger.debug('confirm_word')
        self.info.message = ''
        if self.info.status != WordleStatus.WORD:
            self.logger.debug(f'status invalid {self.info.status}')
            return
        if self.offset == 0 or self.offset % 5 != 0:
            self.logger.debug(f'offset invalid {self.offset}')
            return
        assert(self.offset > 0 and self.offset % 5 == 0)
        count_corr = 0
        word = ''
        for i in range(5):
            off_letter = self.offset - 5 + i
            word += self.info.letters[off_letter].letter
        self.logger.debug(f'word = {word}')
        if word not in self.words:
            self.info.message = 'Not in word list'
            return
        answers = list(self.answer)
        for i in range(5):
            off_letter = self.offset - 5 + i
            ans_curr = self.answer[i]
            rep_curr = self.info.letters[off_letter].letter
            if ans_curr == rep_curr:
                self.info.letters[off_letter].status = LetterStatus.CORR
                self.info.keyboards[ans_curr] = LetterStatus.CORR
                answers.remove(ans_curr)
                count_corr += 1
        for i in range(5):
            off_letter = self.offset - 5 + i
            if self.info.letters[off_letter].status == LetterStatus.CORR:
                continue
            rep_curr = self.info.letters[off_letter].letter
            if rep_curr in answers:
                self.info.letters[off_letter].status = LetterStatus.SPOT
                if self.info.keyboards[rep_curr] != LetterStatus.CORR:
                    self.info.keyboards[rep_curr] = LetterStatus.SPOT
                answers.remove(rep_curr)
            else:
                self.info.letters[off_letter].status = LetterStatus.MISS
                if self.info.keyboards[rep_curr] == LetterStatus.BLNK:
                    self.info.keyboards[rep_curr] = LetterStatus.MISS
        if count_corr == 5:
            self.info.status = WordleStatus.RGHT
            self.info.message = 'You win.'
        elif self.offset < 30:
            self.info.status = WordleStatus.OPEN
        else:
            self.info.status = WordleStatus.WRNG
            self.info.message = (
                'You lose. answer='
                f'<span class="answer">{self.answer.upper()}</span>'
            )
        return

    def delete_letter(self: Wordle) -> None:
        self.logger.debug('delete_letter')
        self.info.message = ''
        if self.info.status in [WordleStatus.RGHT, WordleStatus.WRNG]:
            self.logger.debug('already finish game')
            return
        if self.offset % 5 == 0 and self.info.status == WordleStatus.OPEN:
            self.logger.debug(f'no remaining letter: {self.offset}')
            return
        self.offset -= 1
        self.info.letters[self.offset].letter = ' '
        self.info.letters[self.offset].status = LetterStatus.BLNK
        self.info.status = WordleStatus.OPEN
        return

    def reset_game(self: Wordle) -> None:
        self.logger.debug('reset_game')
        self.info.message = ''
        if self.info.status not in [WordleStatus.RGHT, WordleStatus.WRNG]:
            self.logger.debug('not finished game')
            return
        self.answer = None
        self.offset = 0
        self.info = WordleInfo()
        self._choose_answer()
        return

    def get_info(self: Wordle) -> WordleInfo:
        return self.info

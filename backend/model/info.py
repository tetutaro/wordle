#!/usr/bin/env python
# -*- coding:utf-8 -*-
from typing import List, Dict
from enum import Enum
from pydantic import BaseModel


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

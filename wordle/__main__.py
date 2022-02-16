#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import annotations
from typing import List, Dict, Callable
import sys
import os
from platform import system
import re
import tkinter as tk
from tkinter import Event
import tkmacosx as tkm
from logging import getLogger, StreamHandler, Formatter, INFO
from wordle.wordle import Wordle, WordleInfo, WordleStatus, LetterStatus


class WordleTk():
    keyboard_letters: List[str] = [
        'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
        'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
        'Enter', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'Del'
    ]
    letter_keymap: Dict[str, int] = dict({
        (x, i) for i, x in enumerate(keyboard_letters)
    })

    def __init__(self: WordleTk) -> None:
        # logger
        logger = getLogger('Wordle')
        logger.setLevel(INFO)
        formatter = Formatter('%(asctime)s: %(levelname)s: %(message)s')
        handler = StreamHandler()
        handler.setLevel(INFO)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.logger = logger
        self.wordle = Wordle(logger=logger)
        # window
        self.root = tk.Tk()
        self.root.title('Wordle')
        self.root.geometry('510x700')
        self.root.configure(bg='#121213')
        self.root.bind('<KeyPress>', self._keyboard_callback)
        # icon
        if system() == 'Windows':
            imgfn = 'icons/wordle.ico'
            if '_MEIPASS2' in os.environ:
                imgfn = os.path.join(os.environ['_MEIPASS2'], imgfn)
            if os.path.exists(imgfn):
                self.root.iconbitmap(imgfn)
        else:
            imgfn = 'icons/wordle.png'
            if not os.path.exists(imgfn):
                imgfn = os.path.join(
                    os.path.dirname(sys.executable), imgfn
                )
            if os.path.exists(imgfn):
                img = tk.Image('photo', file=imgfn)
                self.root.tk.call('wm', 'iconphoto', self.root._w, img)
        # header
        self.header = tk.Label(
            self.root, text='Wordle',
            foreground='#ffffff', background='#121213',
            font=('', 36, 'bold'), pady=10
        )
        self.header.pack(side=tk.TOP)
        # widgets
        self._create_widgets()
        return

    def _create_widgets(self: WordleTk) -> None:
        self._create_letters()
        self._create_messages()
        self._create_keyboards()
        return

    def _create_letters(self: WordleTk) -> None:
        self.letter_rows = list()
        for idx in range(6):
            letter_row = tk.Frame(self.root)
            letter_row.pack(side=tk.TOP)
            self.letter_rows.append(letter_row)
        self.letters = list()
        for idx in range(30):
            letter_row = self.letter_rows[idx // 5]
            letter_pad = tk.Frame(
                letter_row, padx=0, pady=0,
                background='#121213',
                highlightbackground='#121213',
                highlightthickness=3
            )
            letter_pad.pack(side=tk.LEFT)
            text = tk.StringVar()
            text.set(' ')
            letter = tkm.Button(
                letter_pad,
                textvariable=text,
                foreground='#ffffff',
                background='#121213',
                bordercolor='#3a3a3c',
                disabledforeground='#ffffff',
                disabledbackground='#121213',
                borderwidth=2,
                focusthickness=2,
                highlightthickness=2,
                relief=tk.FLAT,
                overrelief=tk.FLAT,
                anchor=tk.CENTER,
                font=('', 36, 'bold'),
                height=50, width=50,
                state=tk.DISABLED
            )
            letter.pack(side=tk.TOP)
            self.letters.append((letter_pad, letter, text))
        return

    def _create_messages(self: WordleTk) -> None:
        self.message_row = tk.Frame(
            self.root, pady=10, background='#121213'
        )
        self.message_row.pack(side=tk.TOP)
        self.message_box_text = tk.StringVar()
        self.message_box_text.set('')
        self.message_box = tk.Label(
            self.message_row,
            textvariable=self.message_box_text,
            foreground='#ffffff', activeforeground='#ffffff',
            background='#121213', activebackground='#121213',
            font=('', 20, 'normal'),
            anchor='w', justify=tk.LEFT, width=18
        )
        self.message_box.pack(side=tk.LEFT)
        self.message_button_text = tk.StringVar()
        self.message_button_text.set('')
        self.message_button = tkm.Button(
            self.message_row,
            textvariable=self.message_button_text,
            foreground='#121213',
            background='#121213',
            activebackground='#121213',
            bordercolor='#121213',
            disabledforeground='#121213',
            disabledbackground='#121213',
            borderwidth=0,
            focusthickness=0,
            highlightthickness=0,
            font=('', 20, 'normal'),
            state=tk.DISABLED, width=120
        )
        self.message_button.pack(side=tk.LEFT)

    def _create_keyboards(self: WordleTk) -> None:
        self.keyboard_rows = list()
        for idx in range(3):
            keyboard_row = tk.Frame(self.root)
            keyboard_row.pack(side=tk.TOP)
            keyboard_row.config()
            self.keyboard_rows.append(keyboard_row)
        self.keys = list()
        for idx in range(28):
            if idx < 10:
                keyboard_row = self.keyboard_rows[0]
            elif idx < 19:
                keyboard_row = self.keyboard_rows[1]
            else:
                keyboard_row = self.keyboard_rows[2]
            let = self.keyboard_letters[idx]
            if len(let) == 1:
                disp_let = let.upper()
                btn_width = 40
            else:
                disp_let = let
                btn_width = 60
            disp_let = let.upper() if len(let) == 1 else let
            key = tkm.Button(
                keyboard_row, text=disp_let,
                foreground='#ffffff',
                activeforeground='#ffffff',
                background='#808384',
                activebackground='#808384',
                bordercolor='#121213',
                font=('', 14, 'normal'),
                anchor='center',
                width=btn_width, pady=12,
                command=self._button_callback(key=let)
            )
            key.pack(side=tk.LEFT)
            key.config()
            self.keys.append(key)
        return

    def _button_callback(self: WordleTk, key: str) -> Callable:
        def button_process() -> None:
            if key == 'Enter':
                self.wordle.confirm_word()
            elif key == 'Del':
                self.wordle.delete_letter()
            else:
                self.wordle.append_letter(key=key)
            info = self.wordle.get_info()
            self._update_widgets(info=info)
        return button_process

    def _keyboard_callback(self: WordleTk, e: Event) -> None:
        key = e.keysym.lower()
        if key == 'return':
            self.wordle.confirm_word()
        elif key == 'backspace':
            self.wordle.delete_letter()
        elif re.match(r'^[a-z]$', key) is not None:
            self.wordle.append_letter(key=key)
        else:
            return
        info = self.wordle.get_info()
        self._update_widgets(info=info)
        return

    def _reset_callback(self: WordleTk) -> Callable:
        def reset_button_process() -> None:
            self.wordle.reset_game()
            info = self.wordle.get_info()
            self._update_widgets(info=info)
        return reset_button_process

    def _update_widgets(self: WordleTk, info: WordleInfo) -> None:
        self._update_letters(info=info)
        self._update_messages(info=info)
        self._update_keyboards(info=info)
        return

    def _update_letters(self: WordleTk, info: WordleInfo) -> None:
        for i, let in enumerate(info.letters):
            letter_pad, letter, text = self.letters[i]
            text.set(let.letter.upper())
            if let.status == LetterStatus.BLNK:
                letter.configure(
                    background='#121213',
                    bordercolor='#3a3a3c',
                    disabledbackground='#121213'
                )
            elif let.status == LetterStatus.SPOT:
                letter.configure(
                    background='#b49f3a',
                    bordercolor='#b49f3a',
                    disabledbackground='#b49f3a'
                )
            elif let.status == LetterStatus.CORR:
                letter.configure(
                    background='#538d4e',
                    bordercolor='#538d4e',
                    disabledbackground='#538d4e'
                )
            else:  # let.status == LetterStatus.MISS
                letter.configure(
                    background='#3a3a3c',
                    bordercolor='#3a3a3c',
                    disabledbackground='#3a3a3c'
                )
        return

    def _update_messages(self: WordleTk, info: WordleInfo) -> None:
        self.message_box_text.set(info.message)
        if info.status in [WordleStatus.RGHT, WordleStatus.WRNG]:
            self.message_button_text.set('New Game')
            self.message_button.configure(
                foreground='#ffffff',
                background='#424e66',
                activebackground='#424e66',
                bordercolor='#121213',
                disabledforeground='#ffffff',
                disabledbackground='#424e66',
                state=tk.NORMAL,
                command=self._reset_callback()
            )
        else:
            self.message_button_text.set('')
            self.message_button.configure(
                foreground='#121213',
                background='#121213',
                activebackground='#121213',
                bordercolor='#121213',
                disabledforeground='#121213',
                disabledbackground='#121213',
                state=tk.DISABLED
            )
        return

    def _update_keyboards(self: WordleTk, info: WordleInfo) -> None:
        for key, status in info.keyboards.items():
            idx = self.letter_keymap[key]
            keybtn = self.keys[idx]
            if status == LetterStatus.BLNK:
                keybtn.configure(
                    background='#808384',
                    disabledbackground='#808384'
                )
            elif status == LetterStatus.SPOT:
                keybtn.configure(
                    background='#b49f3a',
                    disabledbackground='#b49f3a'
                )
            elif status == LetterStatus.CORR:
                keybtn.configure(
                    background='#538d4e',
                    disabledbackground='#538d4e'
                )
            else:  # status == LetterStatus.MISS
                keybtn.configure(
                    background='#3a3a3c',
                    disabledbackground='#3a3a3c'
                )
        return

    def loop(self: WordleTk) -> None:
        self.root.mainloop()
        return


def main() -> None:
    wordletk = WordleTk()
    wordletk.loop()
    return


if __name__ == '__main__':
    main()

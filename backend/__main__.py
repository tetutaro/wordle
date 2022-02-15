#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask, render_template
from backend.wordle import Wordle

app = Flask(__name__, template_folder='templates', static_folder='static')
wordle = Wordle(logger=app.logger)


@app.route('/')
def root():
    info = wordle.get_info()
    return render_template('wordle.html', info=info)


@app.route('/key/<string:key>')
def append_letter(key: str):
    wordle.append_letter(key=key)
    info = wordle.get_info()
    return render_template('wordle.html', info=info)


@app.route('/return')
def confirm_word():
    wordle.confirm_word()
    info = wordle.get_info()
    return render_template('wordle.html', info=info)


@app.route('/delete')
def delete_letter():
    wordle.delete_letter()
    info = wordle.get_info()
    return render_template('wordle.html', info=info)


@app.route('/reset')
def reset_game():
    wordle.reset_game()
    info = wordle.get_info()
    return render_template('wordle.html', info=info)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)

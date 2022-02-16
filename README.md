# Wordle (Tkinter version)

5文字の英単語当てゲーム "Wordle" が面白かったので、
自分で作ってみた。

本家 : The New York Times - "[Wordle](https://www.nytimes.com/games/wordle/index.html)"

## アプリのバイナリを作るための準備

* （無ければ）pyenv 等をインストールする
* 【注意】Python を Framework としてインストールする
    * これをやらないと PyInstaller が動かない
    * `env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.10.2`
* Python 仮想環境を作り、Python パッケージをインストールする
    * `pip install -r requirements.txt`

## 英単語リストの作成

まずは Wordle が使う5文字の英単語のリストを作らなければならない。

### 準備

英単語出現頻度データをダウンロードする。

* [Kaggle](https://www.kaggle.com/) のアカウントが無ければ作る
* Kaggle にログインし、[English Word Frequency](https://www.kaggle.com/rtatman/english-word-frequency) のデータをダウンロードする
* ダウンロードしたファイル (archive.zip) を解凍し、生成された `unigram_freq.csv` を `wordle` ディレクトリの下に置く

### 英単語リスト作成スクリプト

* `make words` もしくは `cd wordle && python ./create_words.py`

### 何をしているのか

* 最新の English Wiktionary のダンプをダウンロードし、そこから5文字の英単語（他の言語の単語や、大文字・記号等が入っているものは除外）を抽出する
* 抽出した単語の出現回数を English Word Frequency のデータから取ってくる
* `wordle/word.py` として、5文字の単語と、最も出現回数の多い単語 (`about`) の出現回数を 1 としたときの、その単語の出現回数の割合のデータを作成する

### なぜこんなことをしているのか

* Wiktionary に出てくる単語をすべて使うようにすると、あまりにもマイナーな単語を正解としてしまい、つまらなくなってしまう
* まずはそもそもマイナーすぎる単語は使わないように、出現回数の割合に閾値（`backend/wordle.py` の `FREQ_THRESHOLD`）を設け、足切りをする
* そして単純にランダムに正解の単語を決めるのではなく、出現回数の割合を重みとしたランダムで正解の単語を決めることで、よく使われる単語を正解とする

### 注意

Wiktionary, そして Kaggle の上記データをそのまま利用しているので、
一部に人名・地名・国名・企業名や性的な意味を持つ言葉があり、
そのまま使われます。

名詞の複数形、動詞の過去形・現在進行形が入っているのは、仕様です。
（本家と同じ）

## 動かし方

### 動かし方１

ローカルでそのまま動かす。

* `make local` もしくは `python -m wordle`

### 動かし方２

バイナリ（アプリ）を作成して動かす。

* Mac OS の場合
    * `make binary-mac`
    * `dist` ディレクトリ下に作られる `Wordle.app` を動かす
* Linux の場合
    * `make binary`
    * `dist` ディレクトリ下に作られる `Wordle` を動かす

## ゲームのルール、やり方

本家と同じ。

# wordle

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
* （無ければ）node, yarn をインストールする
* Node JS パッケージをインストールする
    * `yarn`

## 英単語リストの作成

まずは Wordle が使う5文字の英単語のリストを作らなければならない。

### 準備

英単語出現頻度データをダウンロードする。

* [Kaggle](https://www.kaggle.com/) のアカウントが無ければ作る
* Kaggle にログインし、[English Word Frequency](https://www.kaggle.com/rtatman/english-word-frequency) のデータをダウンロードする
* ダウンロードしたファイル (archive.zip) を解凍し、生成された `unigram_freq.csv` を `scripts` ディレクトリの下に置く

### 英単語リスト作成スクリプト

* `make words` もしくは `cd scripts && python ./create_words.py`

### 何をしているのか

* 最新の English Wiktionary のダンプをダウンロードし、そこから5文字の英単語（他の言語の単語や、大文字・記号等が入っているものは除外）を抽出する
* 抽出した単語の出現回数を English Word Frequency のデータから取ってくる
* `scripts/word.csv` として、5文字の単語と、最も出現回数の多い単語 (`about`) の出現回数を 1 としたときの、その単語の出現回数の割合のデータを作成する

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

Python backend サーバを動かし、そこに Web ブラウザでアクセスする。

* `make http` もしくは `python -m backend`
* Web ブラウザで [localhost:8000](http://localhost:8000) にアクセスする

### 動かし方２

Python backend サーバを動かし、そこに Electron でアクセスする。

* `make http` もしくは `python -m backend`
* その後に `make browse` もしくは `./node_modules/.bin/electron browse.js`

### 動かし方３

Electron を起動すると共に Python backend サーバを動かし、
Electron を閉じると共に Python backend サーバも落とす。

* `make app` もしくは `yarn start`

### 動かし方４

Python backend サーバをバイナリにし、
Electron を起動すると共に backend バイナリを動かし、
Electron を閉じると共に backend バイナリも落とす。

* `make backend`
* その後に `make app` もしくは `yarn start`

### 動かし方５

backend バイナリと共にすべてをひとつのバイナリ（インストーラ）にして、
一般的なアプリのようにインストール・利用する。

* `yarn build`
* build ディレクトリの下に生成される Wordle-X.X.X.dmg をインストール・利用する

（backend バイナリの動作に問題があり、まだ動かない）

## ゲームのルール、やり方

本家と同じ。

## メモ

* FastAPI (Uvicorn?) は PyInstaller でバッチ化した時に動かなかったので、意図的に Flask を使っている

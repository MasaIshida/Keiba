# Keiba

=====

## Overview

ディープラーニングを使った競馬予測ツールです<br>
AllScrapingMainにて学習に必要なデータを取得し、<br>
GetKeibaDataで予測するデータを取得する。<br>
LeaningJsonDataで学習させる為のデータ形成を行う。最終的にはpickelで出力<br>
Kohにて学習と予測を行う<br>

## Requirement
### Pythonモジュール
- pip
- beautifulsoup4
- requests
- numpy
- lxml
- tensorflow
- sklear
- mysql-connector-python

## Usage
AllScrapingMain : 学習に必要なデータを取得する<br>
GetKeibaData    : 予測対象のデータを取得する（昨年の有馬記念のみ対応）<br>
LeaningJsonData : 学習させる為のデータ形成を行う ※Jsonファイルは使用していません。<br>
Koh : ディープラーニング実行ファイル<br>

# pdfigswap

[English](README.md) | **日本語**

原稿 PDF 内の「Insert Figure # here」というプレースホルダを、同じディレクトリにある `fig#.pdf` の**1ページ目**で、**同じ位置・同じサイズ**に差し替えます。図をラスタ化せず、ベクトル PDF のまま重ねて埋め込む方針です。

## 背景・用途

Word から PrimoPDF などで PDF を出力したあと、Word 側で **挿入 → 図形** の四角に「Insert Figure # here」と書いた Box を置いておき、その位置に `fig#.pdf` を当てはめる、というワークフローを PDF 上で自動化するツールです。Word に直接ラスタとベクトルが混在した図を貼り付けて画質が落ちる問題を避け、図は別 PDF として差し替えます。

## 必要なもの

- Python 3
- [PyMuPDF](https://pymupdf.readthedocs.io/)（`pymupdf`）

```bash
pip install pymupdf
```

## 使い方

```bash
python pdfigswap.py manuscript.pdf
```

### ファイルの置き方

入力 PDF と**同じディレクトリ**に、例えば次のように置きます。

- `manuscript.pdf`
- `fig1.pdf`, `fig2.pdf`, `fig6.pdf`, …

プレースホルダの文言は次の形式（大文字・小文字は区別しません）です。

`Insert Figure <番号> here`

例: 「Insert Figure 6 here」→ `fig6.pdf` を使用します。

### 出力

`<元のファイル名_stem>_fig_replaced_<YYYYMMDD_HHMMSS>.pdf` が同じフォルダに出力されます（例: `manuscript_fig_replaced_20260504_161052.pdf`）。タイムスタンプは実行時刻で、拡張子 `.pdf` の直前に入ります。

### 処理の流れ

1. プレースホルダ文字列とその bbox を検出する。
2. その周囲に、Word の図形 Box に近い描画矩形があればそれを採用。なければ文字 bbox を少し拡大する。
3. 白の矩形で元の Box と文字を隠す。
4. `fig#.pdf` の1ページ目を同じ矩形に `keep_proportion=True` で重ねる。

`fig#.pdf` が無い番号は警告を出してスキップします。

## ライセンス

公開時にリポジトリに合わせたライセンスを記載してください。

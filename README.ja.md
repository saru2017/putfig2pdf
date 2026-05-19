# putfig2pdf

[English](README.md) | **日本語**

原稿 PDF 内の「**先頭が `#` の**ファイル名だけ」（例: `#fig6.pdf`）をプレースホルダとみなし、同じディレクトリにある対応PDFの**1ページ目**で、**同じ位置・同じサイズ**に差し替えます。`#` はディスク上のファイル名には含めず、参照時に取り除きます。**`#` が付いていない** `fig6.pdf` などの文字列はプレースホルダとみなさず、置き換えません。図をラスタ化せず、ベクトル PDF のまま重ねて埋め込む方針です。

## 背景・用途

Word から PrimoPDF などで PDF を出力したあと、Word 側で **挿入 → 図形** の四角に `#fig6.pdf` のように **必ず先頭に `#` を付けた** プレースホルダだけを書いた Box を置いておき、その位置に対応する PDF を当てはめる、というワークフローを PDF 上で自動化するツールです。Word に直接ラスタとベクトルが混在した図を貼り付けて画質が落ちる問題を避け、図は別 PDF として差し替えます。

## 必要なもの

- Python 3
- [PyMuPDF](https://pymupdf.readthedocs.io/)（`pymupdf`）

```bash
pip install pymupdf
```

## 使い方

```bash
python putfig2pdf.py manuscript.pdf
```

### ファイルの置き方

入力 PDF と**同じディレクトリ**に、例えば次のように置きます。

- `manuscript.pdf`
- `fig1.pdf`, `fig2.pdf`, `my-plot.pdf`, …

プレースホルダの文言は「**先頭の `#` + ファイル名のみ**」です（大文字・小文字は区別しません）。`#` を除いた名前で同じフォルダ内の PDF を探します。**`#` なし**の `fig6.pdf` などは置き換え対象外です。

例:

- `#fig6` -> `fig6.pdf`
- `#fig6.pdf` -> `fig6.pdf`
- `#fig1.pdf` -> `fig1.pdf`
- `#my-plot.pdf` -> `my-plot.pdf`
- `fig6.pdf`（`#` なし）-> 置き換えない

### 出力

`<元のファイル名_stem>_fig_replaced_<YYYYMMDD_HHMMSS>.pdf` が同じフォルダに出力されます（例: `manuscript_fig_replaced_20260504_161052.pdf`）。タイムスタンプは実行時刻で、拡張子 `.pdf` の直前に入ります。

### 処理の流れ

1. プレースホルダ文字列とその bbox を検出する。
2. その周囲に、Word の図形 Box に近い描画矩形があればそれを採用。なければ文字 bbox を少し拡大する。
3. PDF の redaction により、元の Box と文字（プレースホルダ）を削除する。
4. 対応する PDF の1ページ目を同じ矩形に `keep_proportion=True` で重ねる。

対応する PDF ファイルが見つからない場合は警告を出してスキップします。

## デモ

サンプル原稿・図 PDF・実行結果の例は [`demo/`](demo/) にあります。

- [デモの説明（日本語）](demo/README.ja.md)
- [Demo guide (English)](demo/README.md)

## ライセンス

公開時にリポジトリに合わせたライセンスを記載してください。

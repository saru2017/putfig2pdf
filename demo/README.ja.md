# putfig2pdf デモ

[English](README.md) | **日本語**

このフォルダは [putfig2pdf](../README.ja.md) の最小デモです。原稿 PDF に `#figN.pdf` 形式のプレースホルダを置き、別 PDF の図を同じ位置に埋め込む一連の例が入っています。

## すぐ試す

リポジトリのルートで（[PyMuPDF](https://pymupdf.readthedocs.io/) をインストール済みであること）:

```bash
cd demo
python ../putfig2pdf.py sample.pdf
```

`sample.pdf` と**同じフォルダ**（この `demo` フォルダ）にある `fig1.pdf` / `fig2.pdf` / `fig3.pdf` を参照します。出力は `sample_fig_replaced_YYYYMMDD_HHMMSS.pdf` のような名前になります。

実行結果の例として `sample_fig_replaced_20260519_130734.pdf` を同梱しています。

## ファイル一覧

| ファイル | 説明 |
|----------|------|
| `sample.docx` | **推奨ワークフロー。** 図形ボックスに `#fig1.pdf` / `#fig2.pdf` / `#fig3.pdf` とだけ書いた Word 原稿（図は埋め込まない）。 |
| `sample.pdf` | `sample.docx` を PDF にしたもの（PrimoPDF など）。`putfig2pdf.py` の入力に使う。 |
| `fig1.pdf`, `fig2.pdf`, `fig3.pdf` | プレースホルダが指す図 PDF。各ファイルの 1 ページ目を対応する枠に重ねる。 |
| `figs.pptx` | `fig1.pdf`〜`fig3.pdf` を作る元の PowerPoint。 |
| `sample_fig1.pdf`, `sample_fig2.pdf`, `sample_fig3.pdf` | 上記 3 つの図 PDF のコピー（`fig1.pdf`〜`fig3.pdf` と同内容）。デモ用に同梱。 |
| `sample_fig_replaced_20260519_130734.pdf` | `sample.pdf` に `putfig2pdf` を実行した結果の例。 |
| `sample_broken.docx` | **対照用（非推奨）。** 図を Word 内にベクトル画像（EMF）として埋め込んだ原稿。ファイル名プレースホルダだけの方式ではない。 |
| `sample_broken.pdf` | `sample_broken.docx` から出力した PDF。Word に図を入れたまま PDF 化した場合の例（サイズが大きく、自動差し替えの対象にしない）。 |

## 見比べるポイント

1. `sample.pdf` を開き、3 つの枠に `#fig1.pdf` などと書いてあることを確認する。
2. `putfig2pdf` を実行した出力 PDF で、プレースホルダが消え、図 PDF が重ねられていることを確認する。
3. `sample_broken.pdf` は最初から図がページに含まれており、`putfig2pdf` が想定する使い方ではない。

## 合字（`fi` → `ﬁ`）について

PDF 出力によっては、見た目は `#fig1.pdf` でも内部文字列が `#ﬁg1.pdf`（`fi` が合字 U+FB01）になることがあります。現在の `putfig2pdf.py` はマッチ前に Unicode NFKC で正規化するため、この場合でも `#fig1.pdf` として認識できます。

独自の PDF でマッチしないときは、合字を抑えて再出力するか、`sample.docx` のように**図形のテキストだけ**に `#ファイル名` を書く方式かどうかを確認してください。

## 出力を再生成する

```bash
cd demo
python ../putfig2pdf.py sample.pdf
```

出力ファイル名: `sample_fig_replaced_<YYYYMMDD_HHMMSS>.pdf`

[← メイン README へ](../README.ja.md)

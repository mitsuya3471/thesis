"""Markdown で書いた本文を、卒業論文テンプレートの体裁で .docx に変換する。

使い方:
    python scripts/md2docx.py 論文.md 卒業論文テンプレート.dotx 卒業論文.docx

テンプレートの1ページ目（表題・著者名・概要の表、所属の脚注）はそのまま残り、
「はじめに」以降の本文だけが Markdown の内容に置き換わる。

Markdown の見出しは、テンプレートのスタイルに対応づけられる。

    # 章    → 見出し1
    ## 節   → 見出し2
    ### 項  → 見出し3
    地の文  → 本文

句読点は、手引きの指定に合わせて「。」「、」を「．」「，」へ変換する。
変換後、表題・著者名・概要の記入と、図および番号付けは Word で行う。
"""
import re
import sys
import zipfile

from docx import Document
from docx.oxml.ns import qn

見出し = {1: "heading 1", 2: "heading 2", 3: "heading 3"}


def テンプレートを開く(dotx):
    """python-docx は .dotx を受け付けないので、種別だけ書き換えて読み込む。"""
    tmp = dotx + ".tmp.docx"
    src = zipfile.ZipFile(dotx)
    dst = zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED)
    for item in src.infolist():
        data = src.read(item.filename)
        if item.filename == "[Content_Types].xml":
            data = data.replace(
                b"wordprocessingml.template.main+xml",
                b"wordprocessingml.document.main+xml",
            )
        dst.writestr(item, data)
    dst.close()
    return Document(tmp), tmp


def 句読点(text):
    return text.replace("。", "．").replace("、", "，")


def 変換(md_path, dotx_path, out_path):
    doc, tmp = テンプレートを開く(dotx_path)
    body = doc.element.body

    # 1ページ目はセクション区切りまで。そこまでは触らない
    区切り位置 = None
    for i, el in enumerate(body):
        if el.tag.endswith("}p") and el.find(".//" + qn("w:sectPr")) is not None:
            区切り位置 = i
            break
    if 区切り位置 is None:
        raise SystemExit("セクション区切りが見つかりません")

    # 本文側を消す。ただし枠で配置された段落（所属の脚注）は残す
    残す = []
    for el in list(body)[区切り位置 + 1:]:
        if not (el.tag.endswith("}p") or el.tag.endswith("}tbl")):
            continue
        if el.find(".//" + qn("w:framePr")) is not None:
            残す.append(el)
        body.remove(el)
    for el in 残す:
        body.find(qn("w:sectPr")).addprevious(el)

    # Markdown を流し込む
    for line in open(md_path, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line.strip():
            continue
        m = re.match(r"^(#+)\s+(.*)", line)
        if m:
            doc.add_paragraph(句読点(m.group(2)), style=見出し.get(len(m.group(1)), "heading 3"))
        else:
            doc.add_paragraph(句読点(line), style="Normal")

    doc.save(out_path)
    import os
    os.remove(tmp)
    print("作成しました:", out_path)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    変換(sys.argv[1], sys.argv[2], sys.argv[3])

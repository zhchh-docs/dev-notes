# -*- coding: utf-8 -*-
"""审计各教科书章节是否已有实质内容（按 <main> 内字符数粗判）。"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.join(ROOT, "14_从0到精通")

def audit(book_dir):
    rows = []
    for dirpath, _, files in os.walk(book_dir):
        for fn in files:
            if not fn.lower().endswith(".html"):
                continue
            fp = os.path.join(dirpath, fn)
            txt = open(fp, encoding="utf-8", errors="ignore").read()
            m = re.search(r"<main>([\s\S]*?)</main>", txt)
            main = m.group(1) if m else ""
            # 去掉 toc/script 等，粗略按正文字节
            main_len = len(main)
            # 是否有中文正文（去 nav/toc/footer 后）
            body_txt = re.sub(r"<nav[\s\S]*?</nav>", "", main)
            body_txt = re.sub(r"<[^>]+>", "", body_txt)
            cn = len(re.findall(r"[一-鿿]", body_txt))
            rows.append((os.path.relpath(fp, BOOK), main_len, cn))
    return rows

for name in sorted(os.listdir(BOOK)):
    bd = os.path.join(BOOK, name)
    if not os.path.isdir(bd) or name.startswith("00_"):
        continue
    rows = audit(bd)
    empty = [r for r in rows if r[2] < 200]
    filled = [r for r in rows if r[2] >= 200]
    print("\n=== %s : 总 %d 篇，有内容 %d，空骨架/偏空 %d ===" % (name, len(rows), len(filled), len(empty)))
    for r in sorted(empty):
        print("   EMPTY %6d字 %s" % (r[2], r[0]))

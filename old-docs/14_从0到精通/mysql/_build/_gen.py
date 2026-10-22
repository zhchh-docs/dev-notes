#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""组装章节页：head 模板 + 正文(a+b) + tail 模板。
用法: python _gen.py <编号3位> <输出相对路径(相对 mysql 目录)>
正文文件: _build/<编号>a.html 与 _build/<编号>b.html，按 TITLE/FOOT 行替换占位。
正文首两行约定:
  TITLE: 第 N 章 章名
  FOOT:  第 N 章 章名
"""
import io, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)

def read(p):
    with io.open(p, "r", encoding="utf-8") as f:
        return f.read()

def main():
    num = sys.argv[1]
    out_rel = sys.argv[2]
    a = read(os.path.join(BASE, num + "a.html"))
    b = read(os.path.join(BASE, num + "b.html"))
    body = a.rstrip() + "\n" + b.lstrip()

    # 取 TITLE: 与 FOOT: 行
    title = ""
    foot = ""
    for line in body.splitlines():
        if line.startswith("TITLE:") and not title:
            title = line[6:].strip()
        elif line.startswith("FOOT:") and not foot:
            foot = line[5:].strip()
    # 从正文中移除这两行
    lines = [l for l in body.splitlines()
             if not (l.startswith("TITLE:") or l.startswith("FOOT:"))]
    body = "\n".join(lines)

    head = read(os.path.join(BASE, "_head.html"))
    tail = read(os.path.join(BASE, "_tail.html"))
    html = (head.replace("{{TITLE}}", title) + body.rstrip() + "\n"
            + tail)
    out_path = os.path.join(ROOT, out_rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with io.open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("OK:", out_path, len(html.splitlines()), "lines")

if __name__ == "__main__":
    main()

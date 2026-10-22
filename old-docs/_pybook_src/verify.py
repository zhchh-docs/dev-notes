#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验已生成章节：title / 卡片数 / 行数 / 关键结构是否齐全。"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
BOOK = os.path.join(ROOT, "14_从0到精通", "python")


def main():
    files = []
    for dirpath, _, names in os.walk(BOOK):
        for n in sorted(names):
            if n.endswith(".html") and n != "00_目录.html":
                files.append(os.path.join(dirpath, n))
    files.sort()

    problems = []
    total_lines = 0
    for p in files:
        with open(p, encoding="utf-8") as f:
            html = f.read()
        lines = html.count("\n") + 1
        total_lines += lines
        title = re.search(r"<title>([^<]+)</title>", html)
        title = title.group(1) if title else "!!无title!!"
        cards = len(re.findall(r'<section id="sec', html))
        checks = {
            "hero": '<header class="hero">' in html,
            "toc": '<nav class="toc"' in html,
            "app.js": 'assets/app.js' in html,
            "glossary": 'glossary-data.js' in html,
            "style": "section.card h2 .num" in html,
            "summary": "小结" in html,
            "exercise": "本章习题" in html,
            "code": html.count('<pre class="code"') >= 1,
        }
        bad = [k for k, v in checks.items() if not v]
        flag = "  [!] 缺: %s" % ",".join(bad) if bad else ""
        if bad:
            problems.append(os.path.basename(p) + " -> " + ",".join(bad))
        print("%-44s cards=%d lines=%4d%s" % (title, cards, lines, flag))

    print("-" * 72)
    print("章节数: %d   总行数: %d" % (len(files), total_lines))
    if problems:
        print("存在问题: %s" % "; ".join(problems))
        sys.exit(1)
    print("全部章节结构校验通过")


if __name__ == "__main__":
    main()

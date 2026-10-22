#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 008 提取框架，批量为第 9-58 章生成骨架（正文留空），强制覆盖。"""
import os

ROOT = r"F:\跑路资料整理\技术栈详解DouBao\14_从0到精通\java"
REF = os.path.join(ROOT, r"10_第一篇_入门与语法\008_第8章_数组与多维数组.html")
HERE = os.path.dirname(os.path.abspath(__file__))

with open(REF, encoding="utf-8") as f:
    src = f.read()

head = src.split("<body>", 1)[0] + "<body>\n"
mid = src.split("<body>", 1)[1].split("<main>", 1)[0]   # hero + 顶栏 + container 开头
tail = src.split("</main>", 1)[1]                        # </main> 之后

ns = {}
exec(open(os.path.join(HERE, "_chapters.py"), encoding="utf-8").read(), ns)
CHAPTERS = ns["CHAPTERS"]

def fname(num, slug):
    return "%03d_第%d章_%s.html" % (num, num, slug)

prev = fname(8, "数组与多维数组")
for i, (num, pdir, plabel, slug, title, desc) in enumerate(CHAPTERS):
    nxt = fname(CHAPTERS[i+1][0], CHAPTERS[i+1][3]) if i + 1 < len(CHAPTERS) \
        else "../70_第七篇_JVM/059_第59章_JVM内存区域.html"
    out = head + mid + "<main>\n</main>" + tail
    out = out.replace("<title>第 8 章 数组与多维数组｜Java 从 0 到精通</title>",
                      "<title>第 %d 章 %s｜Java 从 0 到精通</title>" % (num, title))
    out = out.replace("· 第一篇 入门与语法</p>", "· %s</p>" % plabel)
    out = out.replace("<h1>第 8 章 数组与多维数组</h1>", "<h1>第 %d 章 %s</h1>" % (num, title))
    out = out.replace("第 8 章 / 共 112 章 · 预计 40 分钟 · 必须动手",
                      "第 %d 章 / 共 112 章 · 预计 40 分钟 · 边读边练" % num)
    out = out.replace('<p class="hero-desc">数组是"同类型数据的连续编排"：定长、按下标 O(1) 访问。本章掌握三种初始化、length 与下标边界、多维数组与常用操作（遍历、最值、逆序、复制），并解释 Arrays 工具类与"数组是引用类型"带来的别名问题。</p>',
                      "<p class=\"hero-desc\">%s</p>" % desc)
    out = out.replace('href="007_第7章_方法定义参数与重载.html"', 'href="%s"' % prev)
    out = out.replace('href="009_第9章_String深入不可变与常用方法.html"', 'href="%s"' % nxt)
    out = out.replace("<footer>从 0 到精通 · 《Java 从 0 到精通》 · 第 8 章 数组</footer>",
                      "<footer>从 0 到精通 · 《Java 从 0 到精通》 · 第 %d 章 %s</footer>" % (num, title))
    d = os.path.join(ROOT, pdir)
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, fname(num, slug))
    with open(p, "w", encoding="utf-8") as f:
        f.write(out)
    print("OK", os.path.basename(p))
    prev = fname(num, slug)
print("DONE", len(CHAPTERS))

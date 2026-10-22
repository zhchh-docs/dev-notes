#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""《Python 从 0 到精通》成书生成器。

用法：python build.py
- 从 JavaScript 书参考章提取 <style> 样式与页尾脚本样板（只读，不改任何已有文件）；
- 读取同目录 content_*.py 中各章内容定义，按全书顺序拼装章节 HTML；
- 输出到 ../14_从0到精通/python/{篇目录}/{章文件}.html，目标文件已存在则跳过并告警。
"""
import os
import re
import glob
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                      # 技术栈详解DouBao
BOOK = os.path.join(ROOT, "14_从0到精通", "python")
REF = os.path.join(ROOT, "14_从0到精通", "javascript",
                   "10_第一篇_入门与环境", "001_第1章_初识JavaScript.html")

ICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'"
        "%3E%3Crect width='16' height='16' rx='3' fill='%232d6a3f'/%3E%3Crect x='3' y='4'"
        " width='10' height='2' rx='1' fill='%23fff'/%3E%3Crect x='3' y='7' width='7'"
        " height='2' rx='1' fill='%23fff'/%3E%3Crect x='3' y='10' width='9' height='2'"
        " rx='1' fill='%23fff'/%3E%3C/svg%3E")


def extract_boilerplate():
    with open(REF, encoding="utf-8") as f:
        ref = f.read()
    i0 = ref.index("<style>")
    i1 = ref.index("</style>")
    css = ref[i0:i1 + len("</style>")]
    i_btn = ref.index('<button id="backTop"')
    i_scr = ref.index("<script>", i_btn)
    i_map = ref.index("data-lang 映射")
    j_scr = ref.index("</script>", i_map) + len("</script>")
    scripts = ref[i_scr:j_scr]
    return css, scripts


def load_content_modules():
    mods = []
    for p in sorted(glob.glob(os.path.join(HERE, "content_*.py"))):
        name = os.path.splitext(os.path.basename(p))[0]
        spec = importlib.util.spec_from_file_location(name, p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        mods.append(m)
    assert mods, "未找到 content_*.py"
    return mods


def nav_btn(href, label):
    return '<a class="doc-nav-btn" href="%s">%s</a>' % (href, label)


def build_page(ch, part_dir, part_name, prev, nxt, css, scripts):
    toc_items = "\n".join(
        '    <li><a href="#%s">%s</a></li>' % (a, t) for a, t in ch["toc"])
    sections = "\n\n" + "\n\n".join(ch["sections"])
    prev_html = nav_btn(*prev) if prev else ""
    nxt_html = nav_btn(*nxt) if nxt else ""
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}｜Python 从 0 到精通</title>
<link rel="icon" href="{icon}">
{css}
<link rel="stylesheet" href="../../../glossary/glossary.css">
<link rel="stylesheet" href="../../../assets/app.css">
</head>
<header class="hero">
  <div class="container">
    <p class="breadcrumb">从 0 到精通 · 《Python 从 0 到精通》 · {part_name}</p>
    <h1>第 {n} 章 {title}</h1>
    <div class="meta-row">
      <span class="badge std">教科书</span>
      <span class="meta">第 {n} 章 / 共 60 章 · {meta}</span>
    </div>
    <p class="hero-desc">{hero}</p>
  </div>
</header>
<nav class="doc-nav top" aria-label="文档导航">
  {prev_top}
  <a class="doc-nav-btn" href="../../00_目录.html">📖 全书目录</a>
  <a class="doc-nav-btn home" href="../../../index.html">⌂ 返回首页</a>
  {nxt_top}
</nav>
<div class="container">
<nav class="toc" aria-label="本章目录">
  <h2>本章地图</h2>
  <ol>
{toc}
  </ol>
</nav>
<main>{sections}
</main>
</div>
<nav class="doc-nav bottom">
  {prev_top}
  <a class="doc-nav-btn" href="../../00_目录.html">📖 全书目录</a>
  <a class="doc-nav-btn home" href="../../../index.html">⌂ 返回首页</a>
  {nxt_top}
</nav>
<footer>从 0 到精通 · 《Python 从 0 到精通》 · 第 {n} 章 {title}</footer>
<button id="backTop" type="button" aria-label="回到顶部">↑</button>
{scripts}
<script src="../../../glossary/glossary-data.js"></script>
<script src="../../../glossary/glossary.js"></script>
<script src="../../../assets/app.js"></script>
</body>
</html>
""".format(title=ch["title"], icon=ICON, css=css, part_name=part_name,
           n=ch["n"], meta=ch.get("meta", "预计 30 分钟"), hero=ch["hero"],
           toc=toc_items, sections=sections, scripts=scripts,
           prev_top=prev_html, nxt_top=nxt_html)


def _href(cur_part, other_part, other_file):
    if other_part == cur_part:
        return other_file
    return "../%s/%s" % (other_part, other_file)


def main():
    css, scripts = extract_boilerplate()
    entries = []
    for m in load_content_modules():
        for ch in m.CHAPTERS:
            entries.append((ch["n"], m.PART_DIR, m.PART_NAME, ch))
    entries.sort(key=lambda e: e[0])
    built = skipped = 0
    for i, (n, part_dir_name, part_name, ch) in enumerate(entries):
        part_dir = os.path.join(BOOK, part_dir_name)
        os.makedirs(part_dir, exist_ok=True)
        target = os.path.join(part_dir, ch["file"])
        if os.path.exists(target):
            print("[skip] 已存在: %s" % os.path.relpath(target, ROOT))
            skipped += 1
            continue
        prev = nxt = None
        if i > 0:
            pn, ppart, _, pch = entries[i - 1]
            prev = (_href(part_dir_name, ppart, pch["file"]), "← 第 %d 章" % pn)
        if i < len(entries) - 1:
            _, xpart, _, xch = entries[i + 1]
            nxt = (_href(part_dir_name, xpart, xch["file"]), "第 %d 章 →" % xch["n"])
        html = build_page(ch, part_dir_name, part_name, prev, nxt, css, scripts)
        with open(target, "w", encoding="utf-8", newline="\n") as f:
            f.write(html)
        built += 1
        print("[ok] %s" % os.path.relpath(target, ROOT))
    print("done. built=%d skipped=%d" % (built, skipped))


if __name__ == "__main__":
    main()

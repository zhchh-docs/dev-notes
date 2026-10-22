#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""《Nginx 从 0 到精通》章节生成器（临时工具，成书后删除）。
模板：_template.html（第 4 章副本，运行时替换为占位符）
片段：_src/NNN_*.txt，头部 --- 元信息 ---，之后为 <main> 正文 section 列表
用法：python _gen_nginx.py            # 处理 _src 下全部片段
      python _gen_nginx.py 011.txt 012.txt   # 处理指定片段
"""
import os, re, sys, io

ROOT = os.path.dirname(os.path.abspath(__file__))
TPL_PATH = os.path.join(ROOT, "_template.html")
SRC = os.path.join(ROOT, "_src")

def load_template():
    t = io.open(TPL_PATH, "r", encoding="utf-8").read()
    t = t.replace("<title>第 4 章 部署第一个静态站点｜Nginx 从 0 到精通</title>",
                  "<title>{{TITLE}}｜Nginx 从 0 到精通</title>")
    t = t.replace("第一篇 入门与配置体系</p>", "{{PART}}</p>")
    t = t.replace("<h1>第 4 章 部署第一个静态站点</h1>", "<h1>{{TITLE}}</h1>")
    t = t.replace('<span class="meta">第 4 章 / 共 32 章 · 预计 30 分钟 · 动手章节</span>',
                  '<span class="meta">{{META}}</span>')
    t = re.sub(r'<p class="hero-desc">.*?</p>', '<p class="hero-desc">{{DESC}}</p>', t, count=1, flags=re.S)
    t = t.replace('href="003_第3章_配置层级：main_http_server_location.html"', 'href="{{PREV_URL}}"')
    t = t.replace('href="005_第5章_日志：access_error与切分.html"', 'href="{{NEXT_URL}}"')
    t = re.sub(r'(<h2>本章地图</h2>\s*<ol>).*?(</ol>)', r'\1\n{{TOC}}\n  \2', t, count=1, flags=re.S)
    t = re.sub(r'<main>.*?</main>', '<main>\n{{SECTIONS}}\n</main>', t, count=1, flags=re.S)
    t = t.replace("· 第 4 章 部署第一个静态站点</footer>", "· {{TITLE}}</footer>")
    for ph in ("{{TITLE}}", "{{PART}}", "{{META}}", "{{DESC}}", "{{PREV_URL}}",
               "{{NEXT_URL}}", "{{TOC}}", "{{SECTIONS}}"):
        if ph not in t:
            raise SystemExit("模板缺少占位符 " + ph)
    return t

def parse_fragment(path):
    text = io.open(path, "r", encoding="utf-8").read()
    if "\n---\n" in text:
        head, body = text.split("\n---\n", 1)
    else:
        head, body = "", text
    meta = {}
    for line in head.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    toc_lines = []
    for item in meta.get("toc", "").split(";"):
        item = item.strip()
        if not item:
            continue
        sid, name = item.split("|", 1)
        toc_lines.append('    <li><a href="#%s">%s</a></li>' % (sid, name))
    return meta, "\n".join(toc_lines), body.strip("\n")

def build(tpl, frag_path):
    meta, toc, sections = parse_fragment(frag_path)
    html = (tpl
            .replace("{{TITLE}}", meta["title"])
            .replace("{{PART}}", meta["part"])
            .replace("{{META}}", meta["meta"])
            .replace("{{DESC}}", meta["desc"])
            .replace("{{PREV_URL}}", meta["prev"])
            .replace("{{NEXT_URL}}", meta["next"])
            .replace("{{TOC}}", toc)
            .replace("{{SECTIONS}}", sections))
    outdir = os.path.join(ROOT, meta["outdir"])
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, meta["file"])
    io.open(outpath, "w", encoding="utf-8", newline="\n").write(html)
    print("OK", os.path.relpath(outpath, ROOT), len(html.splitlines()), "lines")

def main():
    tpl = load_template()
    args = sys.argv[1:]
    if args:
        stems = args
    else:
        stems = sorted({f[:4] for f in os.listdir(SRC) if f.endswith(".txt")})
    # 同一章节的多段片段（006a/006b）按名排序拼接：头部取自首段，正文依序合并
    for stem in stems:
        parts = sorted(f for f in os.listdir(SRC) if f.startswith(stem) and f.endswith(".txt"))
        head = None
        bodies = []
        for p in parts:
            m, toc, body = parse_fragment(os.path.join(SRC, p))
            if head is None:
                head = (m, toc)
            if not body.startswith("<section"):
                raise SystemExit("片段 %s 正文应以 <section 开头" % p)
            bodies.append(body)
        frag = os.path.join(SRC, stem + ".merged")
        io.open(frag, "w", encoding="utf-8", newline="\n").write("\n---\n".join([""]) + "")
        # 重建一个伪片段文件供 build() 解析
        m, toc = head
        meta_lines = ["%s: %s" % (k, v) for k, v in m.items()]
        merged = "\n".join(meta_lines) + "\n---\n" + "\n\n".join(bodies)
        io.open(frag, "w", encoding="utf-8", newline="\n").write(merged)
        build(tpl, frag)
        os.remove(frag)

if __name__ == "__main__":
    main()

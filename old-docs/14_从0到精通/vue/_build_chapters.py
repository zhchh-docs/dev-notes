# -*- coding: utf-8 -*-
"""《Vue 从 0 到精通》章节包装器。

用法：把「只写正文」的章节文件（首行以 <!--CH 标记开头）放进对应篇目录，
运行本脚本后，文件会被就地替换成完整 HTML 页面（含 CSS / hero / 目录 / 上下章导航）。
已经包装过（不含 <!--CH 标记）的文件会被跳过，因此可以反复运行。

原始文件头部格式：
<!--CH
title: 认识 Vue：声明式与渐进式
part: 第一篇 入门
desc: 一句话简介（显示在 hero）
toc: 本章目标|1.1 什么是 Vue|...|本章小结|本章习题
-->
正文：若干个 <section id="secN" class="card"> ... </section>
"""
import os
import re
import io

ROOT = os.path.dirname(os.path.abspath(__file__))
BOOK = "Vue 从 0 到精通"
TOTAL = 76

CSS = """:root{--bg:#f4f6f9;--surface:#ffffff;--line:#d8e2cc;--line-2:#c2cfb4;--ink:#1f2e1f;--ink-2:#4f6348;--ink-3:#7a8a70;--accent:#2d6a3f;--accent-2:#4f8a63;--accent-soft:#d8e8c8;--warn:#b45309;--warn-soft:#fef3c7;--danger:#b91c1c;--danger-soft:#fee2e2;--ok:#047857;--ok-soft:#d1fae5;--code-bg:#152010;--code-ink:#d8e2cc;--radius:12px;--shadow:0 1px 3px rgba(15,23,42,.08);--font:-apple-system,"Segoe UI","Microsoft YaHei","PingFang SC","Noto Sans SC",sans-serif;--mono:"Cascadia Mono","JetBrains Mono",Consolas,"Courier New",monospace}
*{box-sizing:border-box;max-width:100%}
html{scroll-behavior:smooth}
html,body{max-width:100%!important;overflow-x:hidden!important}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.85 var(--font);-webkit-font-smoothing:antialiased}
.container{max-width:980px;margin:0 auto;padding:0 20px}
.hero{background:linear-gradient(180deg,#22331f 0%,#152010 100%);color:#f8faf0;padding:44px 0 36px}
.hero .breadcrumb{font-size:13px;color:#9cae90;letter-spacing:.04em;margin:0 0 12px}
.hero h1{margin:0 0 10px;font-size:30px;line-height:1.3;font-weight:700}
.hero .meta-row{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:12px}
.badge{display:inline-block;padding:2px 12px;border-radius:999px;font-size:13px;font-weight:600;line-height:1.6}
.badge.std{background:var(--accent-soft);color:var(--accent);border:1px solid #a9c8a2}
.badge.deep{background:var(--danger-soft);color:var(--danger);border:1px solid #fca5a5}
.hero .meta{font-size:14px;color:#c2cfb4}
.hero-desc{max-width:860px;margin:0;font-size:15.5px;color:#c2cfb4}
nav.toc{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 24px;margin:24px 0}
nav.toc h2{margin:0 0 12px;font-size:16px;color:var(--ink)}
nav.toc ol{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,1fr);gap:6px 24px;counter-reset:toc}
nav.toc li{counter-increment:toc;font-size:14px}
nav.toc li::before{content:counter(toc);display:inline-block;min-width:22px;height:22px;line-height:22px;text-align:center;background:var(--accent-soft);color:var(--accent);border-radius:6px;font-size:12px;font-weight:600;margin-right:8px}
nav.toc a{color:var(--accent);text-decoration:none}
nav.toc a:hover{text-decoration:underline}
main{display:block;padding-bottom:40px}
section.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:34px 40px;margin:26px 0}
section.card h2{font-size:24px;margin:0 0 22px;padding-left:14px;border-left:4px solid var(--accent);line-height:1.4}
section.card h2 .num{display:inline-block;min-width:32px;height:32px;line-height:32px;text-align:center;background:var(--accent);color:#fff;border-radius:8px;font-size:14px;font-weight:700;margin-right:10px;vertical-align:1px;letter-spacing:-.02em}
section.card h3{font-size:19px;margin:36px 0 12px;padding-left:10px;border-left:3px solid var(--accent-2);color:var(--accent-2);line-height:1.45}
section.card h4{font-size:16.5px;margin:24px 0 10px;padding-left:8px;border-left:3px solid var(--line-2);color:#354835;font-weight:600;line-height:1.45}
section.card p{margin:12px 0}
section.card ul,section.card ol{margin:12px 0;padding-left:26px}
section.card li{margin:8px 0;line-height:1.8}
section.card ul>li::marker{color:var(--accent);font-size:1.05em}
section.card ol>li::marker{color:var(--accent);font-weight:700}
section.card ul ul>li::marker,section.card ol ol>li::marker{color:var(--accent-2)}
section.card ul ul,section.card ol ol,section.card ul ol,section.card ol ul{padding-left:22px;border-left:2px solid var(--line);margin-left:6px}
strong{color:var(--ink)}
code{font-family:var(--mono);font-size:.92em;background:#eef3e8;color:#0f4c81;padding:1px 6px;border-radius:5px;white-space:normal;word-break:break-all;overflow-wrap:anywhere;max-width:100%;display:inline;overflow:hidden}
p,li,h1,h2,h3,h4,h5,h6{overflow-wrap:break-word;word-wrap:break-word}
pre{max-width:100%;overflow-x:auto}
pre.code{position:relative;background:var(--code-bg);color:var(--code-ink);border-radius:10px;padding:16px 18px;overflow-x:auto;margin:14px 0;line-height:1.65;font-size:13.5px;font-family:var(--mono)}
pre.code::before{content:attr(data-lang);position:absolute;top:8px;right:12px;font-size:11.5px;color:#7a8a70;letter-spacing:.06em}
pre.code code{background:transparent;color:inherit;padding:0;font-size:inherit}
.code-copy{position:absolute;top:6px;right:64px;font-size:12px;color:#c2cfb4;background:#22331f;border:1px solid #354835;border-radius:6px;padding:2px 8px;cursor:pointer}
.code-copy:hover{color:#fff;border-color:#4f6348}
table{width:100%;table-layout:fixed;border-collapse:collapse;margin:14px 0;font-size:14px}
th,td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top;overflow-wrap:break-word}
th{background:#eef3e5;font-weight:600}
tbody tr:nth-child(even){background:#f8faf0}
.diagram{margin:20px 0}
.diagram svg{display:block;width:100%;height:auto;border:1px solid var(--line);border-radius:10px;background:#fbfdff;max-width:100%}
.diagram-caption{margin:8px 0 0;text-align:center;font-size:13px;color:var(--ink-3)}
.note{border-left:4px solid var(--accent);background:#f0f6ff;border-radius:0 8px 8px 0;padding:12px 16px;margin:14px 0;font-size:14px}
.warn-box{border-left:4px solid var(--warn);background:var(--warn-soft);border-radius:0 8px 8px 0;padding:12px 16px;margin:14px 0;font-size:14px}
.danger-box{border-left:4px solid var(--danger);background:var(--danger-soft);border-radius:0 8px 8px 0;padding:12px 16px;margin:14px 0;font-size:14px}
.tag-key,.tag-point,.tag-pit{display:inline-block;font-size:12px;font-weight:700;line-height:1;padding:3px 8px;border-radius:5px;margin-right:6px;vertical-align:2px;white-space:nowrap}
.tag-key{background:var(--accent-soft);color:var(--accent);border:1px solid #a9c8a2}
.tag-point{background:var(--ok-soft);color:var(--ok);border:1px solid #6ee7b7}
.tag-pit{background:var(--warn-soft);color:var(--warn);border:1px solid #fcd34d}
.key-sentence{border-left:4px solid var(--accent);background:#f0f6ff;padding:9px 14px;margin:14px 0;border-radius:0 8px 8px 0;font-weight:600;color:var(--ink);line-height:1.8}
.pit-sentence{border-left:4px solid var(--warn);background:var(--warn-soft);padding:9px 14px;margin:14px 0;border-radius:0 8px 8px 0;font-weight:600;color:var(--ink);line-height:1.8}
.lead{font-size:15.5px;color:var(--ink-2);margin:0 0 14px;padding:10px 14px;background:#f8faf0;border:1px solid var(--line);border-radius:8px;line-height:1.8}
.lead b,.lead strong{color:var(--ink)}
.ex-box{border-left:4px solid var(--ok);background:var(--ok-soft);border-radius:0 8px 8px 0;padding:12px 16px;margin:14px 0;font-size:14px;line-height:1.8}
.ex-box .ex-tag{font-weight:700;color:var(--ok);margin-right:8px;white-space:nowrap}
.doc-nav{display:flex;justify-content:space-between;align-items:center;gap:8px;max-width:980px;margin:0 auto;padding:10px 20px}
.doc-nav.top{position:sticky;top:0;z-index:70;background:var(--surface);border-bottom:1px solid var(--line);box-shadow:var(--shadow)}
.doc-nav.bottom{border-top:1px solid var(--line);padding-top:16px;padding-bottom:16px;margin-top:8px}
.doc-nav-btn{color:var(--accent);text-decoration:none;font-size:14px;font-weight:600;line-height:1;padding:7px 12px;border:1px solid var(--line);border-radius:8px;background:var(--surface);white-space:nowrap;transition:border-color .15s,background .15s}
a.doc-nav-btn:hover{border-color:var(--accent);background:var(--accent-soft)}
.doc-nav-btn.home{color:var(--ink-2)}
.doc-nav-btn.home:hover{color:var(--accent)}
footer{background:#22331f;color:#9cae90;text-align:center;font-size:13px;padding:22px 0;margin-top:8px}
#backTop{position:fixed;right:24px;bottom:32px;width:44px;height:44px;border:none;border-radius:50%;background:var(--accent);color:#fff;font-size:18px;cursor:pointer;box-shadow:0 4px 12px rgba(29,78,216,.35);opacity:0;visibility:hidden;transition:opacity .25s,visibility .25s;z-index:99}
#backTop.show{opacity:1;visibility:visible}
code[class*=language-],pre[class*=language-]{color:#f8f8f2;background:0 0;text-shadow:0 1px rgba(0,0,0,.3);font-family:Consolas,Monaco,'Andale Mono','Ubuntu Mono',monospace;font-size:1em;text-align:left;white-space:pre;word-spacing:normal;word-break:normal;word-wrap:normal;line-height:1.5;tab-size:4;hyphens:none}
pre[class*=language-]{padding:1em;margin:.5em 0;overflow:auto;border-radius:.3em}
:not(pre)>code[class*=language-]{padding:.1em;border-radius:.3em}
.token.cdata,.token.comment,.token.doctype,.token.prolog{color:#8292a2}.token.punctuation{color:#f8f8f2}.token.namespace{opacity:.7}.token.constant,.token.deleted,.token.property,.token.symbol,.token.tag{color:#f92672}.token.boolean,.token.number{color:#ae81ff}.token.attr-name,.token.builtin,.token.char,.token.inserted,.token.selector,.token.string{color:#a6e22e}.language-css .token.string,.style .token.string,.token.entity,.token.operator,.token.url,.token.variable{color:#f8f8f2}.token.atrule,.token.attr-value,.token.class-name,.token.function{color:#e6db74}.token.keyword{color:#66d9ef}.token.important,.token.regex{color:#fd971f}.token.bold,.token.important{font-weight:700}.token.italic{font-style:italic}
pre.code code[class*=language-]{background:transparent;text-shadow:none;font-family:var(--mono);font-size:inherit;padding:0;line-height:inherit;color:inherit;white-space:inherit}
@media(min-width:1024px){nav.toc{position:fixed!important;left:20px;top:80px;width:240px;max-height:calc(100vh - 100px);overflow-y:auto;background:#fff;border:1px solid #d8e2cc;border-radius:12px;padding:16px;z-index:60;box-shadow:0 2px 8px rgba(0,0,0,.06)}nav.toc h2{font-size:14px!important;color:#22331f;margin:0 0 12px 0!important;padding:0 0 8px 0!important;border-bottom:1px solid #d8e2cc!important;font-weight:600!important;background:transparent!important;border-radius:0!important;width:auto!important;height:auto!important;line-height:normal!important}nav.toc ol{list-style:none!important;padding:0!important;margin:0!important;display:block!important;columns:1!important;column-count:1!important}nav.toc ol li{margin:6px 0!important;break-inside:avoid!important}nav.toc ol li a{display:block!important;padding:6px 10px!important;color:#7a8a70!important;text-decoration:none!important;font-size:13px!important;line-height:1.4!important;border-radius:6px!important;transition:all .15s!important;background:transparent!important;border:none!important;font-weight:normal!important}nav.toc ol li a:hover{background:#f0f5e6!important;color:#2d6a3f!important}.container{margin-left:280px!important;max-width:calc(100% - 300px)!important}}
@media(max-width:1023px){nav.toc{position:static!important;width:auto!important}}
@media(max-width:760px){.container{padding:0 12px!important;margin:0!important;max-width:100%!important}.hero{padding:20px 16px}.hero h1{font-size:22px}.hero-desc{font-size:14px;line-height:1.7}.breadcrumb{font-size:12px}nav.toc{margin:0 0 16px 0!important;padding:14px!important;border-radius:10px!important}nav.toc h2{font-size:14px!important;margin-bottom:10px!important}nav.toc ol li a{font-size:13px!important;padding:5px 8px!important}section.card{padding:18px 16px!important;margin:16px 0!important;border-radius:10px}section.card h2{font-size:19px!important;margin-bottom:16px!important}section.card h2 .num{min-width:26px!important;height:26px!important;line-height:26px!important;font-size:13px!important}section.card h3{font-size:16px!important;margin:24px 0 10px!important}section.card h4{font-size:15px!important;margin:16px 0 8px!important}section.card p{font-size:14.5px!important;line-height:1.75!important}section.card li{font-size:14.5px!important;line-height:1.7!important}pre.code{font-size:12px!important;padding:10px 12px!important}.code-copy{position:static;display:block;width:max-content;margin:0 0 10px auto}#backTop{right:16px;bottom:20px}.doc-nav-btn{font-size:12px!important;padding:6px 10px!important}.key-sentence,.pit-sentence{padding:8px 10px!important;margin:10px 0!important;font-size:14px}.lead{padding:8px 10px!important;font-size:13.5px!important;margin:10px 0!important}.diagram{margin:12px 0!important}.doc-nav.bottom{flex-wrap:wrap;padding:12px}}
@media(max-width:640px){.doc-nav{gap:6px;padding-left:14px;padding-right:14px}}"""

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E"
           "%3Crect width='16' height='16' rx='3' fill='%232d6a3f'/%3E"
           "%3Crect x='3' y='4' width='10' height='2' rx='1' fill='%23fff'/%3E"
           "%3Crect x='3' y='7' width='7' height='2' rx='1' fill='%23fff'/%3E"
           "%3Crect x='3' y='10' width='9' height='2' rx='1' fill='%23fff'/%3E%3C/svg%3E")


def collect():
    """按篇目录顺序收集全部章节文件（根目录下的附录排最后）"""
    items = []
    for dn in sorted(os.listdir(ROOT)):
        p = os.path.join(ROOT, dn)
        if not os.path.isdir(p) or dn.startswith(('.', '_')):
            continue
        for fn in sorted(os.listdir(p)):
            if fn.lower().endswith('.html') and not fn.startswith('00_'):
                items.append((dn, fn))
    for fn in sorted(os.listdir(ROOT)):
        if os.path.isfile(os.path.join(ROOT, fn)) and fn.lower().endswith('.html') and not fn.startswith('00_'):
            items.append(('', fn))
    return items


def parse_header(text):
    m = re.search(r'<!--CH(.*?)-->', text, re.S)
    if not m:
        return None, text
    raw = m.group(1)
    meta = {}
    for line in raw.strip().splitlines():
        if ':' not in line:
            continue
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip()
    body = text[m.end():]
    body = re.sub(r'^\s*<!--BODY-->\s*', '', body)
    return meta, body.strip()


def main():
    items = collect()
    up_map = {dn: '../' for dn, _ in items if dn}
    done = 0
    for idx, (dn, fn) in enumerate(items):
        path = os.path.join(ROOT, dn, fn)
        with io.open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        if not text.lstrip().startswith('<!--CH'):
            continue
        meta, body = parse_header(text)
        if not meta:
            continue
        title = meta.get('title', '未命名')
        part = meta.get('part', BOOK)
        desc = meta.get('desc', '')
        toc = [t.strip() for t in meta.get('toc', '').split('|') if t.strip()]
        num_m = re.match(r'^0*(\d+)', fn)
        num = int(num_m.group(1)) if num_m else None
        is_appendix = title.startswith('附录')
        page_title = title if is_appendix else '第 %d 章 %s' % (num, title)
        head_line = title if is_appendix else '第 %d 章 %s' % (num, title)

        # 路径前缀（篇目录下的章节比根目录多一层）
        rel_up = '../../../' if dn else '../../'
        prism = '../_prism.js' if dn else '_prism.js'
        index_url = rel_up + 'index.html'
        catalog_url = '../00_目录.html' if dn else '00_目录.html'

        def link_of(target_dn, target_fn):
            if not target_dn:
                return ('../' if dn else '') + target_fn
            if target_dn == dn:
                return target_fn
            return '../' + target_dn + '/' + target_fn

        prev_dn, prev_fn = items[idx - 1] if idx > 0 else ('', '')
        next_dn, next_fn = items[idx + 1] if idx + 1 < len(items) else ('', '')
        next_url = link_of(next_dn, next_fn) if next_fn else catalog_url
        prev_url = link_of(prev_dn, prev_fn) if prev_fn else catalog_url
        next_label = '下一章 →' if next_fn else '全书目录 →'
        prev_label = '← 上一章' if prev_fn else '← 全书目录'

        toc_html = '\n'.join(
            '    <li><a href="#sec%d">%s</a></li>' % (i + 1, t) for i, t in enumerate(toc))

        html = u"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title}｜{book}</title>
<link rel="icon" href="{favicon}">
<style>
{css}
</style>
<link rel="stylesheet" href="{rel_up}glossary/glossary.css">
<link rel="stylesheet" href="{rel_up}assets/app.css">
</head>
<header class="hero">
  <div class="container">
    <p class="breadcrumb">从 0 到精通 · 《{book}》 · {part}</p>
    <h1>{head_line}</h1>
    <div class="meta-row">
      <span class="badge std">教科书</span>
      <span class="meta">{pos} · 预计 35 分钟 · 示例可直接运行</span>
    </div>
    <p class="hero-desc">{desc}</p>
  </div>
</header>
<nav class="doc-nav top" aria-label="文档导航">
  <a class="doc-nav-btn" href="{catalog_url}">📖 全书目录</a>
  <a class="doc-nav-btn home" href="{index_url}">⌂ 返回首页</a>
  <a class="doc-nav-btn" href="{next_url}">{next_label}</a>
</nav>
<div class="container">
<nav class="toc" aria-label="本章目录">
  <h2>本章地图</h2>
  <ol>
{toc_html}
  </ol>
</nav>
<main>

{body}

</main>
</div>
<nav class="doc-nav bottom">
  <a class="doc-nav-btn" href="{prev_url}">{prev_label}</a>
  <a class="doc-nav-btn home" href="{index_url}">⌂ 返回首页</a>
  <a class="doc-nav-btn" href="{next_url}">{next_label}</a>
</nav>
<footer>从 0 到精通 · 《{book}》 · {head_line}</footer>
<button id="backTop" type="button" aria-label="回到顶部">↑</button>
<script src="{prism}"></script>
<script src="{rel_up}glossary/glossary-data.js"></script>
<script src="{rel_up}glossary/glossary.js"></script>
<script src="{rel_up}assets/app.js"></script>
</body>
</html>
""".format(page_title=page_title, book=BOOK, favicon=FAVICON, css=CSS, rel_up=rel_up,
           part=part, head_line=head_line, desc=desc, catalog_url=catalog_url,
           index_url=index_url, next_url=next_url, next_label=next_label,
           prev_url=prev_url, prev_label=prev_label, toc_html=toc_html,
           body=body, prism=prism,
           pos=('第 %d 章 / 共 %d 章' % (num, TOTAL)) if not is_appendix else '附录')

        with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(html)
        done += 1
        print('OK  %s/%s  (%s)' % (dn or '.', fn, page_title))
    print('done: %d / %d' % (done, len(items)))


if __name__ == '__main__':
    main()

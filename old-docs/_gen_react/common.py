# -*- coding: utf-8 -*-
"""《React 从 0 到精通》章节生成器公共模板。

用法：在各 gen_pX.py 里 from common import build。
所有章节共用同一套内联 CSS 风格（与 reference 章节一致），仅内容不同。
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
BOOK_DIR = r"F:\跑路资料整理\技术栈详解DouBao\14_从0到精通\react"

CSS = """
:root{
  --bg:#f4f6f9; --surface:#ffffff; --line:#d8e2cc; --line-2:#c2cfb4;
  --ink:#1f2e1f; --ink-2:#4f6348; --ink-3:#7a8a70;
  --accent:#2d6a3f; --accent-2:#4f8a63; --accent-soft:#d8e8c8;
  --warn:#b45309; --warn-soft:#fef3c7;
  --danger:#b91c1c; --danger-soft:#fee2e2;
  --ok:#047857; --ok-soft:#d1fae5;
  --code-bg:#152010; --code-ink:#d8e2cc;
  --radius:12px; --shadow:0 1px 3px rgba(15,23,42,.08);
  --font:-apple-system,"Segoe UI","Microsoft YaHei","PingFang SC","Noto Sans SC",sans-serif;
  --mono:"Cascadia Mono","JetBrains Mono",Consolas,"Courier New",monospace;
}
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
.hero .meta{font-size:14px;color:#c2cfb4}
.hero-desc{max-width:860px;margin:0;font-size:15.5px;color:#c2cfb4}
.doc-nav{display:flex;justify-content:space-between;align-items:center;gap:8px;max-width:980px;margin:0 auto;padding:10px 20px}
.doc-nav.top{position:sticky;top:0;z-index:70;background:var(--surface);border-bottom:1px solid var(--line);box-shadow:var(--shadow)}
.doc-nav.bottom{border-top:1px solid var(--line);padding-top:16px;padding-bottom:16px;margin-top:8px}
.doc-nav-btn{color:var(--accent);text-decoration:none;font-size:14px;font-weight:600;line-height:1;padding:7px 12px;border:1px solid var(--line);border-radius:8px;background:var(--surface);white-space:nowrap;transition:border-color .15s,background .15s}
a.doc-nav-btn:hover{border-color:var(--accent);background:var(--accent-soft)}
.doc-nav-btn.home{color:var(--ink-2)}
.doc-nav-btn.home:hover{color:var(--accent)}
.toc{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:16px;margin:24px 0}
.toc h2{margin:0 0 12px;font-size:16px;color:var(--ink)}
.toc ol{list-style:none;margin:0;padding:0;counter-reset:toc}
.toc li{counter-increment:toc;font-size:14px;margin:6px 0}
.toc li::before{content:counter(toc);display:inline-block;min-width:22px;height:22px;line-height:22px;text-align:center;background:var(--accent-soft);color:var(--accent);border-radius:6px;font-size:12px;font-weight:600;margin-right:8px}
.toc a{color:var(--accent);text-decoration:none}
.toc a:hover{text-decoration:underline}
@media(min-width:1024px){
  nav.toc{position:fixed;left:20px;top:80px;width:240px;max-height:calc(100vh - 100px);overflow-y:auto;z-index:60}
  nav.toc h2{font-size:14px;color:#22331f;border-bottom:1px solid var(--line);padding-bottom:8px}
  nav.toc ol li a{display:block;padding:6px 10px;color:#7a8a70;font-size:13px;border-radius:6px;transition:all .15s}
  nav.toc ol li a:hover{background:#f0f5e6;color:#2d6a3f;text-decoration:none}
  .container{margin-left:280px;max-width:calc(100% - 300px)}
}
@media(max-width:1023px){nav.toc{position:static;width:auto}}
main{display:block;padding-bottom:40px}
section.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:34px 40px;margin:26px 0}
section.card h2{font-size:24px;margin:0 0 22px;padding-left:14px;border-left:4px solid var(--accent);line-height:1.4}
section.card h2 .num{display:inline-block;min-width:32px;height:32px;line-height:32px;text-align:center;background:var(--accent);color:#fff;border-radius:8px;font-size:15px;font-weight:700;margin-right:10px;vertical-align:2px}
section.card h3{font-size:19px;margin:36px 0 12px;padding-left:10px;border-left:3px solid var(--accent-2);color:var(--accent-2);line-height:1.45}
section.card h4{font-size:16.5px;margin:24px 0 10px;padding-left:8px;border-left:3px solid var(--line-2);color:#354835;font-weight:600;line-height:1.45}
section.card p{margin:12px 0}
section.card ul,section.card ol{margin:12px 0;padding-left:26px}
section.card li{margin:8px 0;line-height:1.8}
section.card ul ul,section.card ol ol,section.card ul ol,section.card ol ul{margin:6px 0;padding-left:22px;border-left:2px solid var(--line);margin-left:6px}
section.card ul>li::marker{color:var(--accent);font-size:1.05em}
section.card ol>li::marker{color:var(--accent);font-weight:700}
strong{color:var(--ink)}
code{font-family:var(--mono);font-size:.92em;background:#eef3e8;color:#0f4c81;padding:1px 6px;border-radius:5px;white-space:normal;word-break:break-all;overflow-wrap:anywhere}
pre.code{position:relative;background:var(--code-bg);color:var(--code-ink);border-radius:10px;padding:16px 18px;overflow-x:auto;margin:14px 0;line-height:1.65;font-size:13.5px;font-family:var(--mono);max-width:100%}
pre.code::before{content:attr(data-lang);position:absolute;top:8px;right:12px;font-size:11.5px;color:#7a8a70;letter-spacing:.06em}
pre.code code{background:transparent;color:inherit;padding:0;font-size:inherit;word-break:normal;overflow-wrap:normal;white-space:pre;display:block}
.code-copy{position:absolute;top:6px;right:64px;font-size:12px;color:#c2cfb4;background:#22331f;border:1px solid #354835;border-radius:6px;padding:2px 8px;cursor:pointer}
.code-copy:hover{color:#fff;border-color:#4f6348}
table{width:100%;table-layout:fixed;border-collapse:collapse;margin:14px 0;font-size:14px}
th,td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top;overflow-wrap:break-word}
th{background:#eef3e5;font-weight:600}
tbody tr:nth-child(even){background:#f8faf0}
.diagram{margin:20px 0}
.diagram svg{display:block;width:100%;height:auto;border:1px solid var(--line);border-radius:10px;background:#fbfdff}
.diagram-caption{margin:8px 0 0;text-align:center;font-size:13px;color:var(--ink-3)}
.note{border-left:4px solid var(--accent);background:#f0f6ff;border-radius:0 8px 8px 0;padding:12px 16px;margin:14px 0;font-size:14px}
.warn-box{border-left:4px solid var(--warn);background:var(--warn-soft);border-radius:0 8px 8px 0;padding:12px 16px;margin:14px 0;font-size:14px}
.danger-box{border-left:4px solid var(--danger);background:var(--danger-soft);border-radius:0 8px 8px 0;padding:12px 16px;margin:14px 0;font-size:14px}
.key-sentence{border-left:4px solid var(--accent);background:#f0f6ff;padding:9px 14px;margin:14px 0;border-radius:0 8px 8px 0;font-weight:600;line-height:1.8}
.pit-sentence{border-left:4px solid var(--warn);background:var(--warn-soft);padding:9px 14px;margin:14px 0;border-radius:0 8px 8px 0;font-weight:600;line-height:1.8}
.lead{font-size:15.5px;color:var(--ink-2);margin:0 0 14px;padding:10px 14px;background:#f8faf0;border:1px solid var(--line);border-radius:8px;line-height:1.8}
.lead b,.lead strong{color:var(--ink)}
.tag-key,.tag-point,.tag-pit{display:inline-block;font-size:12px;font-weight:700;line-height:1;padding:3px 8px;border-radius:5px;margin-right:6px;vertical-align:2px;white-space:nowrap}
.tag-key{background:var(--accent-soft);color:var(--accent);border:1px solid #a9c8a2}
.tag-point{background:var(--ok-soft);color:var(--ok);border:1px solid #6ee7b7}
.tag-pit{background:var(--warn-soft);color:var(--warn);border:1px solid #fcd34d}
.ex-box{border-left:4px solid var(--ok);background:var(--ok-soft);border-radius:0 8px 8px 0;padding:12px 16px;margin:14px 0;font-size:14px;line-height:1.8}
.ex-box .ex-tag{font-weight:700;color:var(--ok);margin-right:8px;white-space:nowrap}
footer{background:#22331f;color:#9cae90;text-align:center;font-size:13px;padding:22px 0;margin-top:8px}
#backTop{position:fixed;right:24px;bottom:32px;width:44px;height:44px;border:none;border-radius:50%;background:var(--accent);color:#fff;font-size:18px;cursor:pointer;box-shadow:0 4px 12px rgba(45,106,63,.35);opacity:0;visibility:hidden;transition:opacity .25s,visibility .25s;z-index:99}
#backTop.show{opacity:1;visibility:visible}
@media(max-width:760px){
  body{line-height:1.75;font-size:15px}
  .container{padding:0 14px;margin:0;max-width:100%}
  .hero{padding:24px 0 20px}
  .hero h1{font-size:22px}
  section.card{padding:20px 16px;margin:16px 0}
  section.card h2{font-size:19px;margin-bottom:16px}
  section.card h3{font-size:16px;margin:22px 0 10px}
  section.card h4{font-size:15px;margin:18px 0 8px}
  pre.code{font-size:12px;padding:12px}
  code{font-size:13px}
  .doc-nav-btn{font-size:12px;padding:6px 10px}
  .doc-nav.bottom{flex-wrap:wrap}
  #backTop{right:16px;bottom:20px}
}
"""

ICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' rx='3' fill='%232d6a3f'/%3E%3Crect x='3' y='4' width='10' height='2' rx='1' fill='%23fff'/%3E%3Crect x='3' y='7' width='7' height='2' rx='1' fill='%23fff'/%3E%3Crect x='3' y='10' width='9' height='2' rx='1' fill='%23fff'/%3E%3C/svg%3E"

COPY_SCRIPT = """
(function () {
  'use strict';
  try {
    var btn = document.getElementById('backTop');
    if (btn) {
      var toggle = function () { btn.classList.toggle('show', window.scrollY > 480); };
      window.addEventListener('scroll', toggle, { passive: true });
      toggle();
      btn.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
    }
  } catch (e) {}
  try {
    var pres = document.querySelectorAll('pre.code');
    for (var i = 0; i < pres.length; i++) {
      (function (pre) {
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'code-copy'; b.textContent = '复制';
        b.setAttribute('aria-label', '复制代码');
        pre.appendChild(b);
        b.addEventListener('click', function () {
          var codeEl = pre.querySelector('code');
          var text = codeEl ? codeEl.innerText : pre.innerText;
          var done = function () { b.textContent = '已复制'; setTimeout(function () { b.textContent = '复制'; }, 1600); };
          function fb(t, ok) {
            try {
              var ta = document.createElement('textarea');
              ta.value = t; ta.style.position = 'fixed'; ta.style.opacity = '0';
              document.body.appendChild(ta); ta.select();
              document.execCommand('copy'); document.body.removeChild(ta); ok();
            } catch (e2) {}
          }
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text).then(done, function () { fb(text, done); });
          } else { fb(text, done); }
        });
      })(pres[i]);
    }
  } catch (e) {}
})();
"""

PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__｜React 从 0 到精通</title>
<link rel="icon" href="__ICON__">
<style>
__CSS__
</style>
<link rel="stylesheet" href="../../../glossary/glossary.css">
<link rel="stylesheet" href="../../../assets/app.css">
</head>
<body>
<header class="hero">
  <div class="container">
    <p class="breadcrumb">从 0 到精通 · 《React 从 0 到精通》 · __PART__</p>
    <h1>第 __NUM__ 章 __H1__</h1>
    <div class="meta-row">
      <span class="badge std">教科书</span>
      <span class="meta">__META__</span>
    </div>
    <p class="hero-desc">__DESC__</p>
  </div>
</header>
<nav class="doc-nav top" aria-label="文档导航">
  <a class="doc-nav-btn" href="__PREVHREF__">__PREVTXT__</a>
  <a class="doc-nav-btn home" href="../../../index.html">⌂ 返回首页</a>
  <a class="doc-nav-btn" href="__NEXTHREF__">__NEXTTXT__</a>
</nav>
<div class="container">
<nav class="toc" aria-label="本章目录">
  <h2>本章地图</h2>
  <ol>
__TOC__
  </ol>
</nav>
<main>
__BODY__
</main>
</div>
<nav class="doc-nav bottom">
  <a class="doc-nav-btn" href="__PREVHREF__">__PREVTXT2__</a>
  <a class="doc-nav-btn" href="../00_目录.html">📖 全书目录</a>
  <a class="doc-nav-btn" href="__NEXTHREF__">__NEXTTXT2__</a>
</nav>
<footer>从 0 到 精通 · 《React 从 0 到精通》 · 第 __NUM__ 章 __FOOTER__</footer>
<button id="backTop" type="button" aria-label="回到顶部">↑</button>
<script>
__SCRIPT__
</script>
<script src="../../../glossary/glossary-data.js"></script>
<script src="../../../glossary/glossary.js"></script>
<script src="../../../assets/app.js"></script>
</body>
</html>
"""


def build(*, part_dir, fname, num, title, part, meta, desc, toc, sections,
          prev=None, nxt=None, prev_txt=None, next_txt=None, footer=None):
    """写一章。prev / nxt 为同目录文件名；缺省回落到全书目录。"""
    prev_href = prev if prev else "../00_目录.html"
    prev_label = prev_txt if prev_txt else "📖 全书目录"
    prev_bottom = ("← " + prev_txt) if prev_txt else "📖 全书目录"
    if nxt:
        next_href = nxt
        next_label = next_txt or "下一章 →"
        next_bottom = (next_txt or "下一章") + " →"
    else:
        next_href = "../00_目录.html"
        next_label = "📖 全书目录"
        next_bottom = "📖 全书目录"

    toc_html = "\n".join('    <li><a href="#%s">%s</a></li>' % (sid, label) for sid, label in toc)
    body_html = "\n\n".join(sections)

    page = (PAGE
            .replace("__TITLE__", "第 %d 章 %s" % (num, title))
            .replace("__ICON__", ICON)
            .replace("__CSS__", CSS.strip())
            .replace("__PART__", part)
            .replace("__NUM__", str(num))
            .replace("__H1__", title)
            .replace("__META__", meta)
            .replace("__DESC__", desc)
            .replace("__PREVHREF__", prev_href)
            .replace("__PREVTXT__", prev_label)
            .replace("__PREVTXT2__", prev_bottom)
            .replace("__NEXTHREF__", next_href)
            .replace("__NEXTTXT__", next_label)
            .replace("__NEXTTXT2__", next_bottom)
            .replace("__TOC__", toc_html)
            .replace("__BODY__", body_html)
            .replace("__SCRIPT__", COPY_SCRIPT.strip())
            .replace("__FOOTER__", footer or title))

    out_dir = os.path.join(BOOK_DIR, part_dir)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(page)
    lines = page.count("\n") + 1
    print("[%-9s] %s  (%d 行)" % (part_dir[:9], fname, lines))
    return path

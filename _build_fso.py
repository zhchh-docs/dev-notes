#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 docs/ 下的 Full Stack Open 中文 Markdown 全量转换为知识库 HTML 模块 15_全栈公开课/

- 74 篇（14 个部分概览 + 59 个章节）按官方顺序全局编号：00_导览 + 01~73；
- 图片引用 ../images/ 改写为 ../docs/images/（直接复用 docs 镜像，不复制）；
- 官网站内链接 /zh/... 改写为官网绝对链接；
- 每页含：阶段徽标 / 本章目录 / 练习范围 / 出处署名（CC BY-NC-SA 3.0，不可删）；
- 导览页含 4 阶段学习路线 + localStorage 已读进度（复用 app.js 的 kb_read）。
可重复运行（覆盖式生成）。
"""
import os, re, json, html as htmllib
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
OUT = os.path.join(ROOT, "15_全栈公开课")
SITE = "https://fullstackopen.com/zh/"

PART_TITLES = {
    0: "Web 应用的基础设施", 1: "React 入门", 2: "与服务端通信",
    3: "用 NodeJS 和 Express 写服务端程序", 4: "测试 Express 服务端程序，以及用户管理",
    5: "测试 React 应用", 6: "利用 Redux 进行状态管理",
    7: "React router、自定义 hook、CSS 和 webpack 样式", 8: "GraphQL",
    9: "TypeScript", 10: "React Native", 11: "CI/CD",
    12: "容器", 13: "使用关系型数据库",
}
STAGES = [
    dict(no=1, icon="🌱", name="阶段一 · 打地基", weeks="约 2 周",
         desc="理解 Web 应用的运行原理，学会用 React 画界面、管理数据流，理解 SPA 与服务端通信。",
         parts=[0, 1, 2]),
    dict(no=2, icon="🔨", name="阶段二 · 通全栈", weeks="约 3 周",
         desc="写出自己的 NodeJS + Express 后端，接入 MongoDB，前后端正式打通并部署上线，补全测试。",
         parts=[3, 4, 5]),
    dict(no=3, icon="🚀", name="阶段三 · 进阶实战", weeks="约 4 周",
         desc="状态管理升级到 Redux，掌握路由与自定义 hook，体验 GraphQL，全面转向 TypeScript。",
         parts=[6, 7, 8, 9]),
    dict(no=4, icon="🏔️", name="阶段四 · 走向生产", weeks="约 3 周",
         desc="React Native 移动端、GitHub Actions 自动化、Docker 容器化、关系型数据库收尾。",
         parts=[10, 11, 12, 13]),
]
PART_STAGE = {p: s["no"] for s in STAGES for p in s["parts"]}

def stage_of(part):
    return next(s for s in STAGES if part in s["parts"])

def clean_title(t):
    if not t:
        return ""
    m = re.search(r"<!--\s*(.+?)\s*-->", t)
    if m:
        t = m.group(1)
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"#+\s*$", "", t)
    return t.strip()

def slugify(t):
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"[^\w\u4e00-\u9fff]+", "_", t, flags=re.UNICODE)
    t = re.sub(r"_+", "_", t).strip("_")
    return t[:24] or "part"

def split_frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:].lstrip("\n")
    return text

def first_heading(body):
    fence = False
    in_comment = False
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        if in_comment:
            if "-->" in s:
                in_comment = False
            continue
        if s.startswith("<!--") and "-->" not in s:
            in_comment = True
            continue
        m = re.match(r"^(#{2,4})\s+(.+)$", s)
        if m:
            return clean_title(m.group(2))
    return ""

def extract_exercises(body):
    found = []
    for m in re.finditer(r"<h3>\s*练习\s*([0-9][0-9.\-~－至到\s]*)\.?\s*</h3>", body):
        found.append(re.sub(r"\s+", "", m.group(1)).rstrip("."))
    for m in re.finditer(r"^#{2,3}\s+练习\s*([0-9][0-9.\-~－至到\s]*)\.?\s*$", body, re.M):
        found.append(re.sub(r"\s+", "", m.group(1)).rstrip("."))
    return "、".join(dict.fromkeys(found))

def preprocess(body):
    t = body
    t = t.replace("](../images/", "](../docs/images/")
    t = t.replace("](../../assets/", "](../docs/assets/")
    t = t.replace("src='../../assets/", "src='../docs/assets/")
    t = t.replace('src="../../assets/', 'src="../docs/assets/')
    t = re.sub(r"\]\(/zh/", "](%s" % SITE, t)
    t = re.sub(r"\]\(/en/", "](https://fullstackopen.com/en/", t)
    t = re.sub(r"<img[^>]*kuva\.png[^>]*/?>",
               '<p class="missing-img">🖼️ 原文此处有一张示意图（官网源文件已缺失，可在官网原页查看）。</p>', t)
    t = re.sub(r'<div class="(content|tasks|intro)">',
               r'<div class="\1" markdown="1">', t)
    return t

def build_toc_and_ids(body):
    """给 ##/### 标题加 {#secN} 锚点，返回 (新正文, toc 列表)"""
    lines = body.splitlines()
    out, toc, fence, k = [], [], False, 0
    in_comment = False
    for line in lines:
        s = line.strip()
        if s.startswith("```"):
            fence = not fence
            out.append(line)
            continue
        if fence:
            out.append(line)
            continue
        if in_comment:
            if "-->" in s:
                in_comment = False
            out.append(line)
            continue
        if s.startswith("<!--") and "-->" not in s:
            in_comment = True
            out.append(line)
            continue
        m = re.match(r"^(#{2,3})\s+(.+?)\s*$", line)
        if m and not s.startswith("#!"):
            k += 1
            sid = "sec-%d" % k
            title = re.sub(r"<[^>]+>", "", m.group(2)).strip()
            toc.append(dict(level=len(m.group(1)), title=title, id=sid))
            out.append("%s %s {#%s}" % (m.group(1), m.group(2), sid))
        else:
            out.append(line)
    return "\n".join(out), toc

def md_convert(body):
    md = markdown.Markdown(
        extensions=[
            "tables", "fenced_code", "attr_list", "md_in_html",
            CodeHiliteExtension(noclasses=True, pygments_style="monokai", guess_lang=False),
        ],
        output_format="html5",
    )
    return md.convert(body)

PAGE_CSS = """
:root{--ink:#2A3D2A;--ink2:#4F6348;--forest:#3D7A4F;--deep:#255A36;--sun:#F2D06B;--card:#F8FAF0}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;
  background:linear-gradient(180deg,#DCE8D0,#C5DDB0 60%,#B5D0A5);color:var(--ink);line-height:1.85;
  -webkit-font-smoothing:antialiased}
.fso-wrap{max-width:880px;margin:0 auto;padding:32px 20px 40px}
.hero{background:var(--card);border:1px solid rgba(61,122,79,.18);border-radius:18px;
  padding:26px 30px;margin-bottom:22px;box-shadow:0 6px 24px rgba(37,90,54,.08)}
.hero .part-line{font-size:13px;margin-bottom:8px;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.badge{display:inline-block;padding:3px 12px;border-radius:999px;font-size:12.5px;font-weight:600}
.b1{background:#DFF0D8;color:#2E6B3E}.b2{background:#FDF3D1;color:#8A6D1A}
.b3{background:#DDEBFA;color:#2B5C8A}.b4{background:#FBE3D8;color:#9A4A2A}
.hero .part-line a{color:var(--forest);text-decoration:underline}
.hero h1{font-size:26px;line-height:1.35;color:var(--deep);margin-bottom:10px}
.hero .meta{font-size:13px;color:var(--ink2);display:flex;flex-wrap:wrap;gap:14px}
.hero img.main-image{display:block;margin:14px auto 0;max-width:210px;width:100%;height:auto}
nav.toc{background:rgba(255,255,255,.75);border:1px dashed rgba(61,122,79,.35);border-radius:14px;
  padding:16px 22px;margin-bottom:22px}
nav.toc .toc-title{font-weight:700;font-size:14px;color:var(--deep);margin-bottom:6px}
nav.toc a{display:block;color:var(--forest);font-size:13.5px;padding:2px 0;text-decoration:none}
nav.toc a:hover{text-decoration:underline}
nav.toc a.l3{padding-left:18px;color:var(--ink2)}
.fso-body{background:var(--card);border:1px solid rgba(61,122,79,.15);border-radius:18px;
  padding:34px 38px;box-shadow:0 6px 24px rgba(37,90,54,.08)}
.fso-body h2{font-size:22px;color:var(--deep);margin:34px 0 14px;padding-left:12px;
  border-left:4px solid var(--forest);line-height:1.4}
.fso-body h3{font-size:18px;color:var(--deep);margin:26px 0 10px}
.fso-body h4{font-size:15.5px;color:var(--ink2);margin:20px 0 8px}
.fso-body p{margin:10px 0}
.fso-body a{color:#2B6CB0}
.fso-body img{max-width:100%;height:auto;border-radius:8px;margin:8px auto;display:block;
  border:1px solid rgba(61,122,79,.2);padding:4px;background:#fff}
.fso-body code{background:rgba(61,122,79,.1);color:#1F4A2C;padding:1px 6px;border-radius:5px;
  font-family:Consolas,Menlo,monospace;font-size:.9em}
.fso-body pre{background:#272822;border-radius:10px;padding:14px 16px;overflow-x:auto;
  margin:14px 0;line-height:1.6}
.fso-body pre code{background:none;color:#F8F8F2;padding:0;font-size:13px}
.fso-body .codehilite{background:#272822;border-radius:10px;margin:14px 0;overflow-x:auto}
.fso-body .codehilite pre{margin:0;background:none;border-radius:0}
.fso-body blockquote{border-left:4px solid var(--sun);background:rgba(242,208,107,.12);
  padding:8px 16px;border-radius:0 10px 10px 0;margin:14px 0;color:var(--ink2)}
.fso-body table{border-collapse:collapse;width:100%;margin:14px 0;font-size:14px;background:#fff}
.fso-body th,.fso-body td{border:1px solid rgba(61,122,79,.3);padding:7px 12px;text-align:left}
.fso-body th{background:#DFF0D8;color:var(--deep)}
.fso-body ul,.fso-body ol{padding-left:26px;margin:10px 0}
.fso-body hr{border:none;border-top:1px dashed rgba(61,122,79,.4);margin:26px 0}
.fso-body .tasks{background:rgba(242,208,107,.14);border:1px solid rgba(242,208,107,.55);
  border-radius:12px;padding:14px 20px;margin:18px 0}
.fso-body .tasks h3{margin-top:4px;color:#8A6D1A}
.fso-body .intro{background:rgba(61,122,79,.07);border-radius:12px;padding:14px 20px;margin:14px 0}
.fso-body .missing-img{color:var(--ink2);font-size:13px;background:rgba(61,122,79,.06);
  border-radius:8px;padding:8px 14px;text-align:center}
.fso-footer{margin-top:22px;background:rgba(255,255,255,.7);border-radius:14px;
  padding:16px 22px;font-size:12.5px;color:var(--ink2);line-height:1.8}
.fso-footer a{color:var(--forest)}
@media (max-width:640px){.fso-body{padding:22px 18px}.hero{padding:20px 18px}}
"""

def page_html(chapter, body_html, toc, prev_u, next_u):
    st = stage_of(chapter["part"])
    p = chapter["part"]
    toc_html = ""
    if toc:
        items = "".join(
            '<a class="l%d" href="#%s">%s</a>' % (t["level"], t["id"], htmllib.escape(t["title"]))
            for t in toc)
        toc_html = '<nav class="toc"><div class="toc-title">📑 本章目录</div>%s</nav>' % items
    main_img = ""
    if chapter.get("main_image"):
        main_img = '<img class="main-image" src="%s" alt="">' % chapter["main_image"]
    meta = []
    if chapter["exercises"]:
        meta.append("<span>✏️ 练习：%s</span>" % htmllib.escape(chapter["exercises"]))
    meta.append("<span>⏱ 约 %d 分钟</span>" % chapter["minutes"])
    meta.append('<span>🌐 <a href="%spart%d/%s" target="_blank" rel="noopener">官网原文</a></span>'
                % (SITE, p, chapter.get("site_slug") or ""))
    pager = ""
    if prev_u or next_u:
        pager = ('<nav class="doc-nav" style="display:flex;justify-content:space-between;gap:10px;margin-top:22px">'
                 + ('<a class="badge b%d" href="%s">← 上一篇</a>' % (st["no"], prev_u) if prev_u else "<span></span>")
                 + ('<a class="badge b%d" href="%s">下一篇 →</a>' % (st["no"], next_u) if next_u else "<span></span>")
                 + "</nav>")
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Part %d %s｜全栈技术知识库</title>
<link rel="stylesheet" href="../assets/app.css">
<style>%s</style>
</head>
<body>
<div class="fso-wrap">
  <header class="hero">
    <div class="part-line">
      <span class="badge b%d">%s %s</span>
      <span class="badge b2">Part %d · %s</span>
      <span>%s</span>
    </div>
    <h1>%s</h1>
    <div class="meta">%s</div>
    %s
  </header>
  %s
  <main class="fso-body">
%s
  </main>
  %s
  <footer class="fso-footer">
    <p>📖 本文来自 <a href="%s" target="_blank" rel="noopener">Full Stack Open</a>（赫尔辛基大学全栈公开课）中文版离线镜像，作者
    <a href="https://github.com/mluukkai" target="_blank" rel="noopener">Matti Luukkainen</a> 等，中文翻译
    ZhangWei（richardzhangv）。内容遵循 <a href="https://creativecommons.org/licenses/by-nc-sa/3.0/"
    target="_blank" rel="noopener">CC BY-NC-SA 3.0</a> 协议——保留本署名即可自由学习分享，禁止商用。</p>
  </footer>
</div>
<script src="../assets/app.js"></script>
</body>
</html>""" % (
        p, htmllib.escape(chapter["title"]), PAGE_CSS,
        st["no"], st["icon"], htmllib.escape(st["name"]), p, htmllib.escape(PART_TITLES[p]),
        htmllib.escape(chapter.get("site_slug") or "第 %d 篇" % chapter["seq"]),
        htmllib.escape(chapter["title"]),
        "".join(meta), main_img,
        toc_html, body_html, pager, SITE,
    )

def overview_site_slug(entries):
    return ""

# ── 导览页 ─────────────────────────────────────────────
def build_guide(chapters):
    total_min = sum(c["minutes"] for c in chapters)
    total_ex = sum(1 for c in chapters if c["exercises"])
    sec_html = []
    u_list = []
    for s in STAGES:
        parts_html = []
        for p in s["parts"]:
            chs = [c for c in chapters if c["part"] == p]
            rows = "".join(
                '<a href="%s">%02d · %s%s</a>' % (
                    c["fname"], c["seq"], htmllib.escape(c["title"]),
                    ' <small style="color:#8A6D1A">（练习 %s）</small>' % htmllib.escape(c["exercises"]) if c["exercises"] else "")
                for c in chs)
            u_list += ["15_全栈公开课/" + c["fname"] for c in chs]
            parts_html.append(
                '<div class="part-block"><div class="part-head">Part %d · %s <small>（%d 篇）</small></div>%s</div>'
                % (p, htmllib.escape(PART_TITLES[p]), len(chs), rows))
        sec_html.append(
            '<section class="stage s%d" id="stage%d">'
            '<div class="stage-head"><span class="stage-ic">%s</span>'
            '<div><h2>%s <small>%s</small></h2><p>%s</p></div>'
            '<div class="stage-prog"><div class="bar"><i data-stage="%d"></i></div><span class="pt">0/%d</span></div></div>'
            '%s</section>'
            % (s["no"], s["no"], s["icon"], htmllib.escape(s["name"]), s["weeks"],
               htmllib.escape(s["desc"]), s["no"],
               sum(len([c for c in chapters if c["part"] == p]) for p in s["parts"]),
               "".join(parts_html)))
    ch_json = json.dumps(u_list, ensure_ascii=False)
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>课程导览与学习路线｜全栈技术知识库</title>
<link rel="stylesheet" href="../assets/app.css">
<style>%s
.guide-hero{background:linear-gradient(135deg,#255A36,#3D7A4F);color:#fff;border-radius:18px;
  padding:34px 34px 30px;margin-bottom:22px;box-shadow:0 8px 28px rgba(37,90,54,.25)}
.guide-hero h1{font-size:28px;margin-bottom:10px}
.guide-hero p{font-size:14px;opacity:.92;max-width:640px}
.guide-hero .stats{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}
.guide-hero .stats span{background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.3);
  padding:4px 14px;border-radius:999px;font-size:13px}
.howto{background:#FDF3D1;border:1px solid rgba(242,208,107,.7);border-radius:14px;
  padding:16px 22px;margin-bottom:22px;font-size:13.5px;line-height:2}
.howto b{color:#8A6D1A}
.stage{background:var(--card);border:1px solid rgba(61,122,79,.16);border-radius:18px;
  padding:22px 26px;margin-bottom:18px;box-shadow:0 6px 24px rgba(37,90,54,.07)}
.stage-head{display:flex;gap:14px;align-items:flex-start;margin-bottom:14px}
.stage-ic{font-size:30px;line-height:1}
.stage h2{font-size:19px;color:var(--deep)}
.stage h2 small{font-size:12.5px;color:#8A6D1A;background:#FDF3D1;border-radius:999px;
  padding:2px 10px;margin-left:8px;vertical-align:2px}
.stage-head p{font-size:13px;color:var(--ink2);margin-top:4px}
.stage-prog{margin-left:auto;min-width:130px;text-align:right}
.stage-prog .bar{height:8px;background:rgba(61,122,79,.15);border-radius:999px;overflow:hidden}
.stage-prog .bar i{display:block;height:100%%;width:0;transition:.4s;
  background:linear-gradient(90deg,#6BA070,#3D7A4F)}
.stage-prog .pt{font-size:12px;color:var(--forest)}
.part-block{background:rgba(255,255,255,.6);border-radius:12px;padding:12px 18px;margin:10px 0}
.part-head{font-weight:700;font-size:14.5px;color:var(--deep);margin-bottom:6px}
.part-block a{display:block;color:var(--forest);font-size:13.5px;padding:3px 0;text-decoration:none}
.part-block a:hover{text-decoration:underline}
.s1{border-top:4px solid #6BA070}.s2{border-top:4px solid #F2D06B}
.s3{border-top:4px solid #5B8EC9}.s4{border-top:4px solid #E08A5E}
@media (max-width:640px){.stage-prog{display:none}.fso-body,.guide-hero{padding:22px 18px}}
</style>
</head>
<body>
<div class="fso-wrap">
  <header class="guide-hero">
    <h1>🎓 全栈公开课 · 学习路线</h1>
    <p>芬兰赫尔辛基大学《深入浅出现代 WEB 编程》（Full Stack Open）中文版。从 React 到 Node、GraphQL、
    TypeScript、容器化，一条官方认证的循序渐进全栈路线——按下方阶段顺序学习，每章配官方练习。</p>
    <div class="stats">
      <span>📚 %d 篇</span><span>🗂 14 个部分</span><span>✏️ %d 章带练习</span>
      <span>⏱ 约 %d 小时阅读</span><span>🧭 4 个阶段</span>
    </div>
  </header>
  <div class="howto">
    <b>🧭 使用说明：</b>① 按阶段顺序从 Part 0 学到 Part 13，每章学完立刻做章内练习；② 每页底部有
    <b>上一篇 / 下一篇</b>，也可用键盘 <b>← →</b> 翻页；③ 页面顶栏可<b>标记已读</b>，本页进度条会自动点亮；
    ④ 正文中蓝色链接多为官方原文/文档，练习答案参考官网与 Discord 社区。
  </div>
  %s
  <footer class="fso-footer">
    <p>📖 课程内容来自 <a href="%s" target="_blank" rel="noopener">fullstackopen.com/zh</a>
    （赫尔辛基大学 &amp; Houston Inc.），作者 Matti Luukkainen 等，中文翻译 ZhangWei（richardzhangv）。
    遵循 <a href="https://creativecommons.org/licenses/by-nc-sa/3.0/" target="_blank" rel="noopener">CC BY-NC-SA 3.0</a>
    协议：署名-非商业-相同方式共享。原始 Markdown 镜像见仓库 <code>docs/</code> 目录。</p>
  </footer>
</div>
<script src="../assets/app.js"></script>
<script>
(function(){
  var CH = %s;
  var read;
  try { read = JSON.parse(localStorage.getItem('kb_read') || '[]'); } catch(e){ read = []; }
  if(!Array.isArray(read)) read = [];
  var set = {}; read.forEach(function(u){ set[u] = 1; });
  document.querySelectorAll('.bar i').forEach(function(bar){
    var no = bar.getAttribute('data-stage');
    var sec = document.getElementById('stage' + no);
    var links = sec.querySelectorAll('.part-block a');
    var done = 0;
    links.forEach(function(a){
      var href = a.getAttribute('href');
      if(set['15_全栈公开课/' + href]){ done++; a.style.opacity = .62; a.insertAdjacentHTML('beforeend',' <span style="color:#3D7A4F">✓</span>'); }
    });
    bar.style.width = (100 * done / links.length) + '%%';
    sec.querySelector('.pt').textContent = done + '/' + links.length;
  });
})();
</script>
</body>
</html>""" % (
        PAGE_CSS, len(chapters), total_ex, max(1, round(total_min / 60)),
        "".join(sec_html), SITE, ch_json,
    )

# ── 主流程 ─────────────────────────────────────────────
def main():
    with open(os.path.join(DOCS, "_index.json"), encoding="utf-8") as f:
        index = json.load(f)
    os.makedirs(OUT, exist_ok=True)

    chapters, missing_imgs = [], []
    seq = 1
    for pinfo in index:
        part = pinfo["part"]
        for e in pinfo["entries"]:
            fname_md = e["file"]
            src = os.path.join(DOCS, "part%d" % part, fname_md)
            with open(src, encoding="utf-8") as f:
                text = f.read()
            body = split_frontmatter(text)
            main_image = ""
            m = re.search(r"^mainImage:\s*(\S+)\s*$", text, re.M)
            if m:
                main_image = m.group(1).replace("../images/", "../docs/images/")
                if not os.path.exists(os.path.join(ROOT, "docs", "images",
                                                   os.path.basename(main_image))):
                    main_image = ""
            is_overview = fname_md == "part%d.md" % part
            if is_overview:
                title = "部分 %d 概览：%s" % (part, PART_TITLES[part])
            else:
                title = first_heading(body) or clean_title(e.get("title", "")) \
                    or "Part %d 第 %s 节" % (part, e["file"])
            pre = preprocess(body)
            pre, toc = build_toc_and_ids(pre)
            body_html = md_convert(pre)
            # 校验图片存在性
            for im in re.findall(r'src="(../docs/images/[^"]+)"', body_html):
                if not os.path.exists(os.path.normpath(os.path.join(OUT, im))):
                    missing_imgs.append("part%d/%s -> %s" % (part, fname_md, im))
            letter = ""
            if not is_overview:
                m2 = re.match(r"part%d([a-z])\.md" % part, fname_md)
                letter = m2.group(1) if m2 else ""
            fname = "%02d_part%d%s_%s.html" % (seq, part, letter, slugify(title))
            chapters.append(dict(
                seq=seq, part=part, letter=letter, file=fname_md, fname=fname,
                title=title, exercises=extract_exercises(text),
                minutes=max(2, round(len(re.sub(r"<[^>]+>|```[\s\S]*?```", "", body)) / 450)),
                main_image=main_image, is_overview=is_overview,
            ))
            seq += 1

    # 上一篇/下一篇（按全局顺序）+ 逐篇写出
    for i, c in enumerate(chapters):
        c["prev_u"] = chapters[i - 1]["fname"] if i > 0 else None
        c["next_u"] = chapters[i + 1]["fname"] if i < len(chapters) - 1 else None
        c["site_slug"] = ""
        src = os.path.join(DOCS, "part%d" % c["part"], c["file"])
        with open(src, encoding="utf-8") as f:
            body = split_frontmatter(f.read())
        pre, toc = build_toc_and_ids(preprocess(body))
        html_out = page_html(c, md_convert(pre), toc, c["prev_u"], c["next_u"])
        with open(os.path.join(OUT, c["fname"]), "w", encoding="utf-8") as f:
            f.write(html_out)

    with open(os.path.join(OUT, "00_课程导览与学习路线.html"), "w", encoding="utf-8") as f:
        f.write(build_guide(chapters))

    print("pages:", len(chapters) + 1)
    print("missing images:", missing_imgs if missing_imgs else "none")
    for s in STAGES:
        n = sum(1 for c in chapters if c["part"] in s["parts"])
        print("stage%d parts=%s -> %d pages" % (s["no"], s["parts"], n))

if __name__ == "__main__":
    main()

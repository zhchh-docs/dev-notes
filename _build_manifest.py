#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描知识库目录，生成 assets/manifest.js

信息架构（A+ 方案）：大区(groups) → 分类(cats) → 文章(arts)
- 首页展示顺序由 GROUPS / CAT_ORDER 显式控制，与目录编号、字典序彻底解耦；
- 新增分类 SOP：①建目录（编号只当 ID）②在 CAT_META 注册一行 ③重跑本脚本；
- 兜底：未注册分类自动归入 misc 并告警；未列入 CAT_ORDER 的追加到大区末尾。

归属判定规则（新增分类前先读）：
1. 读者动线优先：按"读者带着什么问题找到它"归类，不按技术所属领域；
2. 同变更频率同区：一起学、一起改的放同区；
3. 单篇唯一归属：跨主题内容靠页内"相关阅读"与搜索解决；
4. 新分类三问：谁读？接在哪条大区动线上？与现有分类定义冲突吗？——答不清先不建分类。
"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(ROOT, "assets")
os.makedirs(OUT_DIR, exist_ok=True)

CATS = []
for name in sorted(os.listdir(ROOT)):
    full = os.path.join(ROOT, name)
    if os.path.isdir(full) and re.match(r"^\d+_", name):
        CATS.append((name, full))

# ── 大区定义（order = 首页展示顺序；misc 为未注册分类兜底区）──
GROUPS = [
    # key        名称            图标   order
    ("fe",       "前端开发",     "🧱",  1),
    ("server",   "服务端与数据", "🖥️", 2),
    ("eng",      "工程与交付",   "⚙️",  3),
    ("workflow", "研发与 AI",    "🤝",  4),
    ("meta",     "体系与路线",   "🧭",  5),
    ("misc",     "未分类",       "📁",  99),
]
GROUP_META = {g[0]: (g[1], g[2], g[3]) for g in GROUPS}

# ── 分类注册：目录名 -> (展示名, 图标, 描述, 大区 key) ──
CAT_META = {
    "01_前端基础":           ("前端基础",       "🎨", "HTML5 / CSS3 / JavaScript / TypeScript / 浏览器原理 / HTTP", "fe"),
    "02_前端框架与状态管理": ("框架与状态",     "⚛️", "Vue / React / 组件化 / Pinia / 微前端 / SSR / 跨端", "fe"),
    "03_数据可视化":         ("数据可视化",     "📊", "ECharts / AntV G6 / Three.js / Canvas / SVG / 大屏", "fe"),
    "04_实时通信":           ("实时通信",       "📡", "WebSocket / SSE / WebRTC / Janus / 音视频协议", "fe"),
    "05_前端常用工具库":     ("组件与工具库",   "🧰", "Axios / vxe-table / Monaco / JsPlumb / VueUse / 文件处理", "fe"),
    "06_前端工程化与工具链": ("工程化与工具链", "⚙️", "Vite / Webpack / Git / ESLint / 测试 / Monorepo", "eng"),
    "07_后端开发":           ("后端开发",       "☕", "Java / Spring / Spring Boot / MyBatis / RESTful / JWT", "server"),
    "08_数据库与建模":       ("数据库与建模",   "🗄️", "MySQL / Redis / Oracle / ES / MongoDB / 分库分表 / 建模", "server"),
    "09_DevOps部署与运维":   ("部署与运维",     "🚀", "Nginx / Docker / K8s / CI-CD / Linux / 监控", "eng"),
    "10_研发流程与AI辅助":   ("研发流程与 AI",  "🤖", "敏捷 / 代码评审 / AI 编程 / RAG / 技术选型", "workflow"),
    "11_全面学习":           ("体系精讲",       "🎯", "知识总纲 + 分领域体系化精讲", "meta"),
    "12_全栈技术路线图":     ("技术路线图",     "🗺️", "从计算机底层到项目实战的路线地图", "meta"),
    "13_Python":             ("Python",         "🐍", "入门语法 / 工程化与 FastAPI / GIL 与并发 / 性能调优", "server"),
}

# ── 组内展示顺序（未列出的自动追加到本大区末尾）──
CAT_ORDER = {
    "fe":       ["01_前端基础", "02_前端框架与状态管理", "05_前端常用工具库", "03_数据可视化", "04_实时通信"],
    "server":   ["07_后端开发", "08_数据库与建模", "13_Python"],
    "eng":      ["06_前端工程化与工具链", "09_DevOps部署与运维"],
    "workflow": ["10_研发流程与AI辅助"],
    "meta":     ["11_全面学习", "12_全栈技术路线图"],
}


def depth_of(fname: str) -> str:
    if "深入" in fname: return "deep"
    if "标准" in fname: return "std"
    if "基础" in fname: return "basic"
    return "std"


def pretty_title(fname: str) -> str:
    # 01_HTML5与CSS3【深入】 -> HTML5 与 CSS3
    s = fname
    s = re.sub(r"\.[hH][tT][mM][lL]$", "", s)
    s = re.sub(r"^\d+_", "", s)
    s = re.sub(r"【(深入|标准|基础|精讲|进阶)】", "", s)
    s = s.replace("_", " · ")
    return s.strip()


# 逐分类收集
built = []
total = 0
for cname, cdir in CATS:
    arts = []
    for fn in sorted(os.listdir(cdir)):
        if not fn.lower().endswith(".html"): continue
        # 读 title
        title = None
        try:
            with open(os.path.join(cdir, fn), "r", encoding="utf-8", errors="ignore") as f:
                head = f.read(2000)
            m = re.search(r"<title>([^<]+)</title>", head)
            if m:
                title = m.group(1).strip()
                title = re.sub(r"\s*[-｜—]\s*(全栈技术路线图|全栈技术知识库).*$", "", title).strip()
        except Exception:
            pass
        if not title:
            title = pretty_title(fn)
        arts.append({
            "t": title,
            "f": fn,
            "u": f"{cname}/{fn}",
            "d": depth_of(fn),
        })
    meta = CAT_META.get(cname)
    if meta:
        disp, icon, desc, gkey = meta
    else:
        disp, icon, desc, gkey = pretty_title(cname), "📁", "", "misc"
        print(f"WARN: 未注册分类 {cname} -> 归入 未分类(misc)，请补 CAT_META", file=sys.stderr)
    built.append({"key": cname, "group": gkey, "name": disp, "icon": icon, "desc": desc, "arts": arts})
    total += len(arts)


# 排序：大区 order -> CAT_ORDER 组内序 -> 未列出追加 -> 目录名
def cat_sort_key(c):
    _, _, gorder = GROUP_META.get(c["group"], GROUP_META["misc"])
    lst = CAT_ORDER.get(c["group"], [])
    try:
        idx = lst.index(c["key"])
    except ValueError:
        idx = len(lst)
    return (gorder, idx, c["key"])


cats_sorted = sorted(built, key=cat_sort_key)
for i, c in enumerate(cats_sorted):
    c["order"] = i + 1

manifest = {
    "groups": [{"key": k, "name": n, "icon": i, "order": o} for k, n, i, o in GROUPS],
    "cats": cats_sorted,
    "total": total,
}

out = "// 自动生成的知识库清单，请勿手动编辑\nwindow.KB_MANIFEST = " + json.dumps(manifest, ensure_ascii=False, indent=2) + ";\n"
out_path = os.path.join(OUT_DIR, "manifest.js")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(out)

print(f"OK: {manifest['total']} articles, {len(manifest['cats'])} categories, {len(GROUPS)} groups -> {out_path}")
for g in GROUPS:
    gcats = [c for c in cats_sorted if c["group"] == g[0]]
    if not gcats:
        continue
    n = sum(len(c["arts"]) for c in gcats)
    names = " · ".join(f"{c['name']}({len(c['arts'])})" for c in gcats)
    print(f"  {g[2]} {g[1]} [{g[0]}]: {n} 篇  {names}")

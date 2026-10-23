#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
树荫书房 · 教科书级知识库清单构建
────────────────────────────────
扫描 old-docs/ 归档目录，生成 assets/manifest.js：

  书架(groups) → 书(books) → 章(chapters)

- 教科书：old-docs/14_从0到精通/<slug>/，含篇(parts)结构与进度元数据
- 专题书：old-docs/<模块目录>/ 顶层 HTML = 章节
- 入口书：自有导览站的书（entry 指向其 index.html）

新增一本书：在 BOOKS 注册一行 +（教科书）补 TUTORIAL_BOOKS，重跑本脚本。
"""
import os, re, json, sys
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "old-docs")
OUT_DIR = os.path.join(ROOT, "assets")
os.makedirs(OUT_DIR, exist_ok=True)

# ── 书架大区（order = 展示顺序）──
GROUPS = [
    ("tutorial", "从 0 到精通",  "📚", 1),
    ("fe",       "前端开发",     "🧱", 2),
    ("server",   "服务端与数据", "🖥️", 3),
    ("eng",      "工程与交付",   "⚙️", 4),
    ("workflow", "研发与 AI",    "🤝", 5),
    ("meta",     "体系与路线",   "🧭", 6),
]

# ── 教科书元数据：planned 规划章数 / parts 篇结构(名, 章数, 状态) / status 书状态 ──
TUTORIAL_BOOKS = {
    "javascript": {"planned": 97, "status": "done", "parts": [
        ("第一篇 入门与环境", 8, "done"), ("第二篇 语法核心", 10, "done"),
        ("第三篇 数据集合", 10, "done"), ("第四篇 函数与作用域深潜", 10, "done"),
        ("第五篇 对象与原型", 10, "done"), ("第六篇 异步与事件循环", 10, "done"),
        ("第七篇 DOM 与浏览器", 10, "done"), ("第八篇 现代语法与错误处理", 9, "done"),
        ("第九篇 工程化与进阶", 8, "done"), ("第十篇 性能内存与收官", 12, "done")]},
    "typescript": {"planned": 52, "status": "done", "parts": [
        ("第一篇 入门与类型基础", 8, "done"), ("第二篇 类型系统核心", 9, "done"),
        ("第三篇 泛型与类型编程", 10, "done"), ("第四篇 工程配置与编译", 8, "done"),
        ("第五篇 声明与生态适配", 8, "done"), ("第六篇 类型体操与收官", 9, "done")]},
    "mysql": {"planned": 72, "status": "done", "parts": [
        ("第一篇 入门", 9, "done"), ("第二篇 SQL 进阶", 9, "done"),
        ("第三篇 索引与优化", 10, "done"), ("第四篇 事务与锁", 9, "done"),
        ("第五篇 日志与主从", 8, "done"), ("第六篇 高可用与分库分表", 9, "done"),
        ("第七篇 运维调优", 9, "done"), ("第八篇 综合实战", 9, "done")]},
    "java": {"planned": 112, "status": "done", "parts": [
        ("第一篇 入门与语法", 10, "done"), ("第二篇 面向对象", 10, "done"),
        ("第三篇 核心 API 与集合", 10, "done"), ("第四篇 异常与 IO", 8, "done"),
        ("第五篇 反射注解与函数式", 8, "done"), ("第六篇 并发编程", 12, "done"),
        ("第七篇 JVM", 10, "done"), ("第八篇 数据库与 JDBC", 8, "done"),
        ("第九篇 Spring 核心", 10, "done"), ("第十篇 SpringBoot 与 Web", 10, "done"),
        ("第十一篇 工程化与测试", 8, "done"), ("第十二篇 综合项目收官", 8, "done")]},
    "python": {"planned": 60, "status": "plan", "parts": [
        ("第一篇 入门与语法", 9, "plan"), ("第二篇 函数与进阶语法", 10, "plan"),
        ("第三篇 面向对象与标准库", 10, "plan"), ("第四篇 工程化", 9, "plan"),
        ("第五篇 Web 开发", 12, "plan"), ("第六篇 并发与性能", 10, "plan")]},
    "vue": {"planned": 78, "status": "plan", "parts": [
        ("第一篇 入门", 9, "plan"), ("第二篇 组件化", 10, "plan"),
        ("第三篇 组合式 API", 9, "plan"), ("第四篇 响应式原理", 9, "plan"),
        ("第五篇 状态管理", 8, "plan"), ("第六篇 路由与工程", 10, "plan"),
        ("第七篇 组件设计与模式", 10, "plan"), ("第八篇 原理深潜与性能", 8, "plan")]},
    "react": {"planned": 74, "status": "plan", "parts": [
        ("第一篇 入门", 9, "plan"), ("第二篇 Hooks 核心", 10, "plan"),
        ("第三篇 状态管理", 9, "plan"), ("第四篇 路由与数据", 9, "plan"),
        ("第五篇 渲染原理", 9, "plan"), ("第六篇 性能优化", 9, "plan"),
        ("第七篇 生态与实战", 9, "plan")]},
    "git": {"planned": 40, "status": "plan", "parts": [
        ("第一篇 入门与对象模型", 10, "plan"), ("第二篇 分支与协作", 10, "plan"),
        ("第三篇 历史改写与救援", 10, "plan"), ("第四篇 团队工程", 10, "plan")]},
    "nginx": {"planned": 32, "status": "plan", "parts": [
        ("第一篇 入门与配置体系", 10, "plan"), ("第二篇 反向代理与 HTTPS", 11, "plan"),
        ("第三篇 调优与实战", 11, "plan")]},
    "redis": {"planned": 54, "status": "plan", "parts": [
        ("第一篇 入门与数据结构", 11, "plan"), ("第二篇 持久化与内存", 9, "plan"),
        ("第三篇 缓存策略", 12, "plan"), ("第四篇 分布式锁与原子", 10, "plan"),
        ("第五篇 高可用与集群", 12, "plan")]},
}

# ── 书注册表 ──
# (key, group, name, icon, desc, color, src)
# color：莫兰迪书布色（低饱和、中明度，白字可读、排架和谐）
# src: "dir:<rel>"  收集该目录顶层 HTML 为章节
#      "tree:<rel>" 递归收集该目录全部 HTML
#      "entry:<rel>" 入口书：直接指向其自有导览页
BOOKS = [
    # 📚 从 0 到精通
    ("14_从0到精通",              "tutorial", "书架总导览",              "📚", "教科书模块总入口：每本对应一个技术点的从 0 到精通完整学习线", "#6B5D4F", "dir:14_从0到精通"),
    ("14_从0到精通/javascript",   "tutorial", "《JavaScript 从 0 到精通》", "🟨", "10 篇 · 97 章完稿 + 3 附录 · 全书完", "#A8842C", "tree:14_从0到精通/javascript"),
    ("14_从0到精通/typescript",   "tutorial", "《TypeScript 从 0 到精通》", "🔷", "6 篇 · 52 章完稿 · 全书完", "#33608C", "tree:14_从0到精通/typescript"),
    ("14_从0到精通/java",         "tutorial", "《Java 从 0 到精通》",      "☕", "12 篇 · 112 章完稿 · 全书完", "#B4552D", "tree:14_从0到精通/java"),
    ("14_从0到精通/mysql",        "tutorial", "《MySQL 从 0 到精通》",     "🐬", "8 篇 · 72 章完稿 + 3 附录 · 全书完", "#2E7D74", "tree:14_从0到精通/mysql"),
    ("14_从0到精通/python",       "tutorial", "《Python 从 0 到精通》",    "🐍", "6 篇 · 规划 60 章 · 撰写中", "#3A6B9C", "tree:14_从0到精通/python"),
    ("14_从0到精通/vue",          "tutorial", "《Vue 从 0 到精通》",       "💚", "8 篇 · 规划 78 章 · 撰写中", "#4A8B5C", "tree:14_从0到精通/vue"),
    ("14_从0到精通/react",        "tutorial", "《React 从 0 到精通》",     "⚛️", "7 篇 · 规划 74 章 · 撰写中", "#2E8FA3", "tree:14_从0到精通/react"),
    ("14_从0到精通/git",          "tutorial", "《Git 从 0 到精通》",       "🌿", "4 篇 · 规划 40 章 · 撰写中", "#C07A2E", "tree:14_从0到精通/git"),
    ("14_从0到精通/nginx",        "tutorial", "《Nginx 从 0 到精通》",     "🔁", "3 篇 · 规划 32 章 · 撰写中", "#3D7A4F", "tree:14_从0到精通/nginx"),
    ("14_从0到精通/redis",        "tutorial", "《Redis 从 0 到精通》",     "🧱", "5 篇 · 规划 54 章 · 撰写中", "#B04A4A", "tree:14_从0到精通/redis"),
    ("15_全栈公开课",             "tutorial", "全栈公开课",              "🎓", "赫尔辛基大学 Full Stack Open 中文版 · React / Node / GraphQL / TS 循序渐进全栈实战", "#6E5A8E", "dir:15_全栈公开课"),
    # 🧱 前端开发
    ("01_前端基础",               "fe", "前端基础",       "🎨", "HTML5 / CSS3 / JavaScript / TypeScript / 浏览器原理 / HTTP", "#A05268", "dir:01_前端基础"),
    ("02_前端框架与状态管理",     "fe", "框架与状态",     "⚛️", "Vue / React / 组件化 / Pinia / 微前端 / SSR / 跨端", "#4E7A52", "dir:02_前端框架与状态管理"),
    ("05_前端常用工具库",         "fe", "组件与工具库",   "🧰", "Axios / vxe-table / Monaco / JsPlumb / VueUse / 文件处理", "#4A6FA5", "dir:05_前端常用工具库"),
    ("03_数据可视化",             "fe", "数据可视化",     "📊", "ECharts / AntV G6 / Three.js / Canvas / SVG / 大屏", "#B0763A", "dir:03_数据可视化"),
    ("04_实时通信",               "fe", "实时通信",       "📡", "WebSocket / SSE / WebRTC / Janus / 音视频协议", "#6B5E9E", "dir:04_实时通信"),
    # 🖥️ 服务端与数据
    ("07_后端开发",               "server", "后端开发",     "☕", "Java / Spring / Spring Boot / MyBatis / RESTful / JWT", "#996033", "dir:07_后端开发"),
    ("08_数据库与建模",           "server", "数据库与建模", "🗄️", "MySQL / Redis / Oracle / ES / MongoDB / 分库分表 / 建模", "#35706B", "dir:08_数据库与建模"),
    ("13_Python",                 "server", "Python",       "🐍", "入门语法 / 工程化与 FastAPI / GIL 与并发 / 性能调优", "#35608C", "dir:13_Python"),
    # ⚙️ 工程与交付
    ("06_前端工程化与工具链",     "eng", "工程化与工具链", "⚙️", "Vite / Webpack / Git / ESLint / 测试 / Monorepo", "#A5622F", "dir:06_前端工程化与工具链"),
    ("09_DevOps部署与运维",       "eng", "部署与运维",     "🚀", "Nginx / Docker / K8s / CI-CD / Linux / 监控", "#5E7A3A", "dir:09_DevOps部署与运维"),
    # 🤝 研发与 AI
    ("10_研发流程与AI辅助",       "workflow", "研发流程与 AI", "🤖", "敏捷 / 代码评审 / AI 编程 / RAG / 技术选型", "#7A5E9A", "dir:10_研发流程与AI辅助"),
    # 🧭 体系与路线
    ("11_全面学习",               "meta", "体系精讲",       "🎯", "知识总纲 + 分领域体系化精讲", "#4E5D6B", "dir:11_全面学习"),
    ("12_全栈技术路线图",         "meta", "技术路线图",     "🗺️", "从计算机底层到项目实战的路线地图", "#5E6B5A", "dir:12_全栈技术路线图"),
]


def depth_of(fname: str) -> str:
    if "深入" in fname: return "deep"
    if "标准" in fname: return "std"
    if "基础" in fname: return "basic"
    return "std"


def pretty_title(fname: str) -> str:
    s = fname
    s = re.sub(r"\.[hH][tT][mM][lL]$", "", s)
    s = re.sub(r"^\d+_", "", s)
    s = re.sub(r"【(深入|标准|基础|精讲|进阶)】", "", s)
    s = s.replace("_", " · ")
    return s.strip()


def read_title(fullp: str):
    try:
        with open(fullp, "r", encoding="utf-8", errors="ignore") as f:
            head = f.read(2000)
        m = re.search(r"<title>([^<]+)</title>", head)
        if m:
            t = m.group(1).strip()
            return re.sub(r"\s*[-｜—]\s*(全栈技术路线图|全栈技术知识库).*$", "", t).strip()
    except Exception:
        pass
    return None


def collect(rel_dir: str, recursive: bool):
    """收集 old-docs/<rel_dir> 下的章节，返回 list[chapter]"""
    base = os.path.join(DOCS, rel_dir)
    chapters = []
    if not os.path.isdir(base):
        print(f"WARN: 书源目录不存在 old-docs/{rel_dir}", file=sys.stderr)
        return chapters
    if recursive:
        walker = os.walk(base)
    else:
        top = sorted(f for f in os.listdir(base)
                     if os.path.isfile(os.path.join(base, f)))
        walker = [(base, [], top)]
    for dirpath, dirnames, filenames in walker:
        # 剔除 _build / .git 等临时与隐藏目录
        dirnames[:] = sorted(d for d in dirnames if not d.startswith(("_", ".")))
        for fn in sorted(filenames):
            if fn.startswith("_") or not fn.lower().endswith(".html"):
                continue
            fullp = os.path.join(dirpath, fn)
            rel = os.path.relpath(fullp, DOCS).replace("\\", "/")
            title = read_title(fullp) or pretty_title(fn)
            m = re.match(r"^(\d+)", fn)
            n = int(m.group(1)) if m else len(chapters) + 1
            chapters.append({
                "t": title, "f": fn, "u": "old-docs/" + rel,
                "d": depth_of(fn), "n": n,
            })
    # 按章节编号排序（00_目录等 n=0 排最前，其余 001..N 升序），
    # 避免 os.walk 的目录字符串排序把 100_第十篇 排到 10_第一篇 之前。
    chapters.sort(key=lambda c: c["n"])
    return chapters


# ── 组装 ──
books, total = [], 0
for key, gkey, name, icon, desc, color, src in BOOKS:
    book = {"key": key, "group": gkey, "name": name, "icon": icon,
            "desc": desc, "color": color}
    if src.startswith("entry:"):
        book["entry"] = "old-docs/" + src[len("entry:"):]
        book["chapters"] = []
    else:
        mode, _, rel = src.partition(":")
        chs = collect(rel, recursive=(mode == "tree"))
        book["chapters"] = chs
        total += len(chs)
        tb = TUTORIAL_BOOKS.get(key.partition("/")[2] if key.startswith("14_") and key != "14_从0到精通" else key)
        if tb:
            book["planned"] = tb["planned"]
            book["status"] = tb["status"]
            book["parts"] = [{"name": p[0], "chapters": p[1], "state": p[2]} for p in tb["parts"]]
            book["done"] = sum(1 for c in chs if c["n"] > 0)
    books.append(book)

manifest = {
    "generated": str(date.today()),
    "groups": [{"key": k, "name": n, "icon": i, "order": o} for k, n, i, o in GROUPS],
    "books": books,
    "total": total,
}

out = ("// 自动生成的书房清单（由 _build_library.py 生成，请勿手动编辑）\n"
       "window.KB_MANIFEST = " + json.dumps(manifest, ensure_ascii=False, indent=2) + ";\n")
out_path = os.path.join(OUT_DIR, "manifest.js")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(out)

print(f"OK: {total} 章 · {len(books)} 本书 · {len(GROUPS)} 个书架 -> {out_path}")
for k, n, i, o in GROUPS:
    gb = [b for b in books if b["group"] == k]
    if not gb:
        continue
    cnt = sum(len(b["chapters"]) for b in gb)
    names = " · ".join(f"{b['name']}({len(b['chapters'])})" for b in gb)
    print(f"  {i} {n} [{k}]: {cnt} 章  {names}")

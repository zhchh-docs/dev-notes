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
        # 教科书模块：一层子目录 = 一本书（书内可再分篇子目录，递归收集）
        for sub in sorted(os.listdir(full)):
            subfull = os.path.join(full, sub)
            if os.path.isdir(subfull) and not sub.startswith((".", "_")):
                CATS.append((f"{name}/{sub}", subfull))

# ── 大区定义（order = 首页展示顺序；misc 为未注册分类兜底区）──
GROUPS = [
    # key        名称            图标   order
    ("tutorial", "从 0 到精通",  "📚",  1),
    ("fe",       "前端开发",     "🧱",  2),
    ("server",   "服务端与数据", "🖥️", 3),
    ("eng",      "工程与交付",   "⚙️",  4),
    ("workflow", "研发与 AI",    "🤝",  5),
    ("meta",     "体系与路线",   "🧭",  6),
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
    # ── 教科书模块：书 = 子目录 ──
    "14_从0到精通":              ("书架与总导览",             "📚", "教科书模块：每本对应一个技术点的从 0 到精通完整学习线", "tutorial"),
    "14_从0到精通/javascript":   ("《JavaScript 从 0 到精通》", "🟨", "10 篇 · 97 章完稿 + 3 附录 · 全书完", "tutorial"),
    "14_从0到精通/typescript":   ("《TypeScript 从 0 到精通》", "🔷", "6 篇 · 规划 52 章 · 撰写中", "tutorial"),
    "14_从0到精通/mysql":        ("《MySQL 从 0 到精通》",     "🐬", "8 篇 · 规划 72 章 · 撰写中", "tutorial"),
    "14_从0到精通/java":         ("《Java 从 0 到精通》",      "☕", "12 篇 · 规划 112 章 · 撰写中", "tutorial"),
    "14_从0到精通/python":       ("《Python 从 0 到精通》",    "🐍", "6 篇 · 规划 60 章 · 撰写中", "tutorial"),
    "14_从0到精通/vue":          ("《Vue 从 0 到精通》",       "💚", "8 篇 · 规划 78 章 · 撰写中", "tutorial"),
    "14_从0到精通/react":        ("《React 从 0 到精通》",     "⚛️", "7 篇 · 规划 74 章 · 撰写中", "tutorial"),
    "14_从0到精通/git":          ("《Git 从 0 到精通》",       "🌿", "4 篇 · 规划 40 章 · 撰写中", "tutorial"),
    "14_从0到精通/nginx":        ("《Nginx 从 0 到精通》",     "🔁", "3 篇 · 规划 32 章 · 撰写中", "tutorial"),
    "14_从0到精通/redis":        ("《Redis 从 0 到精通》",     "🧱", "5 篇 · 规划 54 章 · 撰写中", "tutorial"),
}

# ── 组内展示顺序（未列出的自动追加到本大区末尾）──
CAT_ORDER = {
    "tutorial": ["14_从0到精通", "14_从0到精通/javascript", "14_从0到精通/typescript",
                 "14_从0到精通/mysql", "14_从0到精通/java", "14_从0到精通/python",
                 "14_从0到精通/vue", "14_从0到精通/react",
                 "14_从0到精通/git", "14_从0到精通/nginx", "14_从0到精通/redis"],
    "fe":       ["01_前端基础", "02_前端框架与状态管理", "05_前端常用工具库", "03_数据可视化", "04_实时通信"],
    "server":   ["07_后端开发", "08_数据库与建模", "13_Python"],
    "eng":      ["06_前端工程化与工具链", "09_DevOps部署与运维"],
    "workflow": ["10_研发流程与AI辅助"],
    "meta":     ["11_全面学习", "12_全栈技术路线图"],
}

# ── 教科书元数据：planned 规划章数 / parts 篇结构(名,章数,状态) / status 书状态 ──
# 篇状态：plan=规划中 doing=撰写中 done=已完成；每完成一篇批次更新对应状态，首页进度自动反映
TUTORIAL_BOOKS = {
    "14_从0到精通/javascript": {"planned": 97, "status": "done", "parts": [
        ("第一篇 入门与环境", 8, "done"), ("第二篇 语法核心", 10, "done"),
        ("第三篇 数据集合", 10, "done"), ("第四篇 函数与作用域深潜", 10, "done"),
        ("第五篇 对象与原型", 10, "done"), ("第六篇 异步与事件循环", 10, "done"),
        ("第七篇 DOM 与浏览器", 10, "done"), ("第八篇 现代语法与错误处理", 9, "done"),
        ("第九篇 工程化与进阶", 8, "done"), ("第十篇 性能内存与收官", 12, "done")]},
    "14_从0到精通/typescript": {"planned": 52, "status": "plan", "parts": [
        ("第一篇 入门与类型基础", 8, "plan"), ("第二篇 类型系统核心", 9, "plan"),
        ("第三篇 泛型与类型编程", 10, "plan"), ("第四篇 工程配置与编译", 8, "plan"),
        ("第五篇 声明与生态适配", 8, "plan"), ("第六篇 类型体操与收官", 9, "plan")]},
    "14_从0到精通/mysql": {"planned": 72, "status": "plan", "parts": [
        ("第一篇 入门", 9, "plan"), ("第二篇 SQL 进阶", 9, "plan"),
        ("第三篇 索引与优化", 10, "plan"), ("第四篇 事务与锁", 9, "plan"),
        ("第五篇 日志与主从", 8, "plan"), ("第六篇 高可用与分库分表", 9, "plan"),
        ("第七篇 运维调优", 9, "plan"), ("第八篇 综合实战", 9, "plan")]},
    "14_从0到精通/java": {"planned": 112, "status": "plan", "parts": [
        ("第一篇 入门与语法", 10, "plan"), ("第二篇 面向对象", 10, "plan"),
        ("第三篇 核心 API 与集合", 10, "plan"), ("第四篇 异常与 IO", 8, "plan"),
        ("第五篇 反射注解与函数式", 8, "plan"), ("第六篇 并发编程", 12, "plan"),
        ("第七篇 JVM", 10, "plan"), ("第八篇 数据库与 JDBC", 8, "plan"),
        ("第九篇 Spring 核心", 10, "plan"), ("第十篇 SpringBoot 与 Web", 10, "plan"),
        ("第十一篇 工程化与测试", 8, "plan"), ("第十二篇 综合项目收官", 8, "plan")]},
    "14_从0到精通/python": {"planned": 60, "status": "plan", "parts": [
        ("第一篇 入门与语法", 9, "plan"), ("第二篇 函数与进阶语法", 10, "plan"),
        ("第三篇 面向对象与标准库", 10, "plan"), ("第四篇 工程化", 9, "plan"),
        ("第五篇 Web 开发", 12, "plan"), ("第六篇 并发与性能", 10, "plan")]},
    "14_从0到精通/vue": {"planned": 78, "status": "plan", "parts": [
        ("第一篇 入门", 9, "plan"), ("第二篇 组件化", 10, "plan"),
        ("第三篇 组合式 API", 9, "plan"), ("第四篇 响应式原理", 9, "plan"),
        ("第五篇 状态管理", 8, "plan"), ("第六篇 路由与工程", 10, "plan"),
        ("第七篇 组件设计与模式", 10, "plan"), ("第八篇 原理深潜与性能", 8, "plan")]},
    "14_从0到精通/react": {"planned": 74, "status": "plan", "parts": [
        ("第一篇 入门", 9, "plan"), ("第二篇 Hooks 核心", 10, "plan"),
        ("第三篇 状态管理", 9, "plan"), ("第四篇 路由与数据", 9, "plan"),
        ("第五篇 渲染原理", 9, "plan"), ("第六篇 性能优化", 9, "plan"),
        ("第七篇 生态与实战", 9, "plan")]},
    "14_从0到精通/git": {"planned": 40, "status": "plan", "parts": [
        ("第一篇 入门与对象模型", 10, "plan"), ("第二篇 分支与协作", 10, "plan"),
        ("第三篇 历史改写与救援", 10, "plan"), ("第四篇 团队工程", 10, "plan")]},
    "14_从0到精通/nginx": {"planned": 32, "status": "plan", "parts": [
        ("第一篇 入门与配置体系", 10, "plan"), ("第二篇 反向代理与 HTTPS", 11, "plan"),
        ("第三篇 调优与实战", 11, "plan")]},
    "14_从0到精通/redis": {"planned": 54, "status": "plan", "parts": [
        ("第一篇 入门与数据结构", 11, "plan"), ("第二篇 持久化与内存", 9, "plan"),
        ("第三篇 缓存策略", 12, "plan"), ("第四篇 分布式锁与原子", 10, "plan"),
        ("第五篇 高可用与集群", 12, "plan")]},
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
    # 书分类（含 "/"）递归收集（篇子目录）；模块分类只取本层文件，避免重复归属
    if "/" in cname:
        walker = os.walk(cdir)
    else:
        top_files = sorted(f for f in os.listdir(cdir)
                           if os.path.isfile(os.path.join(cdir, f)))
        walker = [(cdir, [], top_files)]
    for dirpath, dirnames, filenames in walker:
        dirnames.sort()
        for fn in sorted(filenames):
            if not fn.lower().endswith(".html"): continue
            fullp = os.path.join(dirpath, fn)
            u = os.path.relpath(fullp, ROOT).replace("\\", "/")
            # 读 title
            title = None
            try:
                with open(fullp, "r", encoding="utf-8", errors="ignore") as f:
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
                "u": u,
                "d": depth_of(fn),
            })
    meta = CAT_META.get(cname)
    if meta:
        disp, icon, desc, gkey = meta
    else:
        disp, icon, desc, gkey = pretty_title(cname), "📁", "", "misc"
        print(f"WARN: 未注册分类 {cname} -> 归入 未分类(misc)，请补 CAT_META", file=sys.stderr)
    built.append({"key": cname, "group": gkey, "name": disp, "icon": icon, "desc": desc, "arts": arts})
    # 教科书附加元数据：planned/status/parts + done（实际已写章数，排除目录页）
    tb = TUTORIAL_BOOKS.get(cname)
    if tb:
        built[-1]["planned"] = tb["planned"]
        built[-1]["status"] = tb["status"]
        built[-1]["parts"] = [{"name": p[0], "chapters": p[1], "state": p[2]} for p in tb["parts"]]
        built[-1]["done"] = sum(1 for a in arts if not a["f"].startswith("00_"))
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

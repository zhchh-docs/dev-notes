# -*- coding: utf-8 -*-
"""第一篇 入门与语法 · 第 1-3 章"""

PART_DIR = "10_第一篇_入门与语法"
PART_NAME = "第一篇 入门与语法"

CHAPTERS = [
# ════════════════════ 第 1 章 ════════════════════
{
"n": 1, "title": "认识 Python：场景、版本与生态",
"file": "001_第1章_认识Python.html",
"meta": "预计 25 分钟 · 零基础可读",
"hero": "在写下第一行 Python 之前，先回答三个问题：Python 是什么？它擅长什么、不擅长什么？该装哪个版本、用哪些生态工具？这一章不写代码，只建立全景地图——之后每一章都在这张地图上添一块拼图。",
"toc": [("sec1", "本章目标"), ("sec2", "1.1 Python 是什么"), ("sec3", "1.2 它能做什么"),
        ("sec4", "1.3 版本抉择：为什么是 Python 3"), ("sec5", "1.4 生态：PyPI 与自带电池"),
        ("sec6", "1.5 代码是怎么跑起来的"), ("sec7", "本章小结"), ("sec8", "本章习题")],
"sections": [
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>能向别人<strong>一句话讲清 Python 是什么</strong>，以及它为什么被称为"胶水语言"；</li>
    <li>能列举 Python 的<strong>至少四个主流应用领域</strong>，并说出它的两个短板；</li>
    <li>分清 <strong>Python 2 / Python 3</strong>、<strong>语言 / 解释器实现 / 发行版</strong> 这三组概念——初学者大量困惑源于混用它们；</li>
    <li>知道 <strong>PyPI</strong> 是什么、为什么"自带电池"是 Python 的核心性格；</li>
    <li>建立全书学习方法的共识：<strong>动手跑 &gt; 只读书</strong>。</li>
  </ul>
  <div class="note"><strong>前置要求</strong>：无。本章不写代码，但建议把环境先按第 2 章装好再回来跑那行 <code>import this</code>。</div>
</section>""",

"""<section id="sec2" class="card">
  <h2><span class="num">1.1</span> Python 是什么</h2>
  <p><strong>一句话定义</strong>：Python 是一门<strong>高级、动态类型、解释执行</strong>的通用编程语言，以"可读性优先"为设计哲学。</p>
  <p>拆开看这三个定语：</p>
  <ul>
    <li><strong>高级</strong>：不用管内存地址与指针，变量即用，内存由解释器的垃圾回收机制（引用计数为主 + 分代回收兜底）代劳；</li>
    <li><strong>动态类型</strong>：变量不声明类型，<code>x = 1</code> 之后 <code>x = "hello"</code> 完全合法。类型检查发生在运行时——第 35 章的类型注解与 mypy 正是给它补上静态检查；</li>
    <li><strong>解释执行</strong>：源码先被编译成字节码，再由 Python 虚拟机逐条执行，因此能一行一行交互式地跑（REPL）。</li>
  </ul>
  <h4>设计哲学：一行命令就能看到</h4>
  <p>1989 年圣诞假期，荷兰人 <strong>Guido van Rossum</strong>（社区尊称"终身仁慈独裁者"）为了打发时间创造了 Python。这个语言把"多写一点是为了让人读懂"写进了骨子里，浓缩成 19 条格言：在任何装好 Python 的机器上输入：</p>
  <pre class="code" data-lang="python"><code>import this</code></pre>
  <p>输出里最值得记住的三条：</p>
  <ul>
    <li><strong>优美胜于丑陋，明了胜于晦涩</strong>——所以 Python 强制缩进、语法贴近自然语言；</li>
    <li><strong>简单胜于复杂</strong>——所以解决一个问题通常只有一种显而易见的写法（社区称之为 TOOWTDI）；</li>
    <li><strong>可读性很重要</strong>——所以 Python 代码读起来几乎像伪代码，这是它成为教学第一语言的原因。</li>
  </ul>
  <p class="key-sentence">Python 的性格：牺牲一点运行速度，换取写代码、读代码、改代码的速度。绝大多数业务场景里，这笔交易稳赚。</p>
</section>""",

"""<section id="sec3" class="card">
  <h2><span class="num">1.2</span> 它能做什么</h2>
  <p>很多人以为 Python 只是"人工智能的语言"，这个印象至少落后了十年。今天的版图：</p>
  <table>
    <colgroup><col style="width:20%"><col style="width:44%"><col style="width:36%"></colgroup>
    <thead><tr><th>领域</th><th>典型产物</th><th>关键角色</th></tr></thead>
    <tbody>
      <tr><td>Web 后端</td><td>API 服务、内容站点、运营后台</td><td>FastAPI / Django / Flask（第五篇专题）</td></tr>
      <tr><td>数据与 AI</td><td>数据分析、机器学习、大模型应用</td><td>pandas / PyTorch / LangChain</td></tr>
      <tr><td>自动化脚本</td><td>批量改名、定时报表、办公自动化</td><td>标准库 + openpyxl 等</td></tr>
      <tr><td>测试与运维</td><td>自动化测试、CI 脚本、基础设施编排</td><td>pytest / Ansible</td></tr>
      <tr><td>爬虫与采集</td><td>页面抓取、接口聚合</td><td>requests / httpx / Scrapy</td></tr>
      <tr><td>科学计算</td><td>仿真、信号处理、生物信息</td><td>NumPy / SciPy</td></tr>
    </tbody>
  </table>
  <h4>它的两个短板（诚实告知）</h4>
  <ol>
    <li><strong>单线程执行速度慢</strong>：纯 Python 循环比 C 慢一到两个数量级。三条出路——把热点交给 NumPy 等 C 扩展、用多进程并行（第六篇）、或直接接受它（多数系统瓶颈在 IO 而非 CPU）；</li>
    <li><strong>移动端与浏览器前端缺席</strong>：App 与网页交互仍是 JavaScript 的地盘，Python 基本不参与。</li>
  </ol>
  <p class="key-sentence">一句话定位：Python 吃下了"数据"与"自动化"两个生态位；人机界面归 JS，极致性能归 C/C++/Rust——而 Python 常常是那层把它们粘起来的胶水。</p>
</section>""",

"""<section id="sec4" class="card">
  <h2><span class="num">1.3</span> 版本抉择：为什么是 Python 3</h2>
  <p>你一定听过"Python 2 和 Python 3 不兼容"。时间线决定了今天的答案：</p>
  <table>
    <colgroup><col style="width:18%"><col style="width:46%"><col style="width:36%"></colgroup>
    <thead><tr><th>时间</th><th>事件</th><th>对你的意义</th></tr></thead>
    <tbody>
      <tr><td>2000</td><td>Python 2.0 发布</td><td>已成历史，仅在老项目里见到</td></tr>
      <tr><td>2008</td><td>Python 3.0 发布，不向后兼容</td><td>打破旧代码，社区花了十年迁移</td></tr>
      <tr><td>2020-01</td><td>Python 2 官方停止维护</td><td>还在教 <code>print</code> 语句的教程，直接换掉</td></tr>
      <tr><td>2022 至今</td><td>3.11 / 3.12 / 3.13 相继发布，每年 10 月一个大版本</td><td>本书面向 3.10+，涉及版本差异处会标注</td></tr>
    </tbody>
  </table>
  <p>选择原则很简单：<strong>跟着官方仍在维护的版本走</strong>。每个大版本约支持 5 年，写新项目选最新稳定版，维护老项目看团队锁定的版本。</p>
  <div class="warn-box"><span class="tag-pit">常见坑</span>网上老教程里的 <code>print "hello"</code>（无括号）、<code>xrange</code>、<code>urllib2</code>、<code>raw_input</code> 都是 Python 2 遗物。看到这些写法，说明教程年纪太大了。</div>
</section>""",

"""<section id="sec5" class="card">
  <h2><span class="num">1.4</span> 生态：PyPI 与自带电池</h2>
  <p>Python 的另一个外号是"<strong>自带电池（batteries included）</strong>"：标准库覆盖文件、网络、并发、压缩、日期、日志、正则……大量脚本<strong>零第三方依赖</strong>就能写完。第四篇工程化的底气就来自这里。</p>
  <p>标准库不够用时去 <strong>PyPI（Python Package Index）</strong>——全球最大的语言包仓库之一，包含几十万个第三方包，用 <code>pip install 包名</code> 安装（第 31 章专题）。几大件先混个脸熟：</p>
  <ul>
    <li><code>requests</code> / <code>httpx</code>：发 HTTP 请求的事实标准；</li>
    <li><code>fastapi</code> + <code>uvicorn</code>：现代 Web API 框架（第五篇主角）；</li>
    <li><code>sqlalchemy</code> + <code>alembic</code>：数据库 ORM 与迁移（第 44-45 章）；</li>
    <li><code>pydantic</code>：数据校验（第 42 章）；</li>
    <li><code>pytest</code>：测试框架（第 34 章）；</li>
    <li><code>pandas</code> / <code>numpy</code>：数据分析与科学计算两块基石。</li>
  </ul>
  <h4>语言、解释器实现与发行版：三组概念</h4>
  <table>
    <colgroup><col style="width:26%"><col style="width:40%"><col style="width:34%"></colgroup>
    <thead><tr><th>概念</th><th>指什么</th><th>例子</th></tr></thead>
    <tbody>
      <tr><td>语言</td><td>语法定义与标准行为</td><td>本书记录的对象</td></tr>
      <tr><td>解释器实现</td><td>按标准造出来的"引擎"</td><td>CPython（官方，本书默认）、PyPy、MicroPython</td></tr>
      <tr><td>发行版</td><td>解释器 + 预装包的打包组合</td><td>Anaconda（数据科学常用）、python.org 官方版</td></tr>
    </tbody>
  </table>
  <div class="note">99% 的场景用<strong>官方 CPython</strong> 即可。没有特殊理由，不要一上来就装 Anaconda——它自带的包管理会和 pip 体系打架，是新手环境混乱的头号来源（第 30 章展开）。</div>
</section>""",

"""<section id="sec6" class="card">
  <h2><span class="num">1.5</span> 代码是怎么跑起来的</h2>
  <p>当你在命令行敲下 <code>python hello.py</code>，背后是四步：</p>
  <div class="diagram">
    <svg viewBox="0 0 800 150" role="img" aria-label="Python 执行流程示意">
      <text x="400" y="24" text-anchor="middle" font-size="14" font-weight="700" fill="#1f2e1f">python hello.py 的执行流程（示意）</text>
      <rect x="40" y="50" width="150" height="50" rx="8" fill="#f0f5e6" stroke="#3d7a4f"/><text x="115" y="80" text-anchor="middle" font-size="12.5" fill="#2d6a3f">① 读取源码</text>
      <rect x="240" y="50" width="150" height="50" rx="8" fill="#f0f5e6" stroke="#3d7a4f"/><text x="315" y="80" text-anchor="middle" font-size="12.5" fill="#2d6a3f">② 编译为字节码</text>
      <rect x="440" y="50" width="150" height="50" rx="8" fill="#fefce8" stroke="#d97706"/><text x="515" y="80" text-anchor="middle" font-size="12.5" fill="#b45309">③ PVM 逐条执行</text>
      <rect x="640" y="50" width="120" height="50" rx="8" fill="#fefce8" stroke="#d97706"/><text x="700" y="80" text-anchor="middle" font-size="12.5" fill="#b45309">④ 输出结果</text>
      <line x1="190" y1="75" x2="240" y2="75" stroke="#7a8a70" stroke-width="1.5"/>
      <line x1="390" y1="75" x2="440" y2="75" stroke="#7a8a70" stroke-width="1.5"/>
      <line x1="590" y1="75" x2="640" y2="75" stroke="#7a8a70" stroke-width="1.5"/>
      <text x="400" y="130" text-anchor="middle" font-size="12" fill="#7a8a70">字节码缓存在 __pycache__ 目录，第二次运行更快；这也是"解释型语言也有编译步骤"的原因</text>
    </svg>
    <p class="diagram-caption">图 1-1 CPython 执行流程（示意）</p>
  </div>
  <p>由此带来两个常见现象：</p>
  <ul>
    <li>项目目录里多出 <code>__pycache__</code> 文件夹——字节码缓存，删掉无妨，会自动重建，应加进 <code>.gitignore</code>；</li>
    <li>错误往往发生在<strong>运行时</strong>而非"编译时"——拼错一个只有某条分支才会走到的变量名，程序跑到那一行才炸。这解释了为什么 Python 世界格外重视测试与类型检查。</li>
  </ul>
</section>""",

"""<section id="sec7" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:34%"><col style="width:66%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>Python 是什么</td><td>高级、动态类型、解释执行的通用语言，可读性优先</td></tr>
      <tr><td>性格</td><td>牺牲一点速度换取开发与阅读效率；标准库"自带电池"</td></tr>
      <tr><td>擅长 / 短板</td><td>擅长数据、AI、自动化、Web 后端；纯 CPU 循环慢，移动端缺席</td></tr>
      <tr><td>版本</td><td>只用 Python 3.10+，Python 2 已于 2020 年停止维护</td></tr>
      <tr><td>三组概念</td><td>语言 / 解释器实现（CPython）/ 发行版，默认选官方 CPython</td></tr>
      <tr><td>执行流程</td><td>源码 → 字节码 → PVM 执行；错误在运行时暴露</td></tr>
    </tbody>
  </table>
</section>""",

"""<section id="sec8" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>用自己的话（不超过三句）向完全不懂编程的朋友解释：Python 是干什么的？它和"人工智能"是什么关系？</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>在你每天使用的软件或服务里，找出两个"背后很可能是 Python 在工作"的场景，并说明判断依据（提示：想想数据、自动化、推荐）。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>访问 pypi.org，分别搜索 <code>requests</code> 与 <code>fastapi</code>，记录它们各自标注的"最近发布日期"与"要求的 Python 版本"——不求看懂，只求见过"包长什么样"。</div>
  <p class="note">参考答案见附录 C（规划中）。下一章我们把环境真正搭起来。</p>
</section>"""
]
},

# ════════════════════ 第 2 章 ════════════════════
{
"n": 2, "title": "安装运行：解释器/REPL/IDE",
"file": "002_第2章_安装运行.html",
"meta": "预计 35 分钟 · 动手章",
"hero": "这一章只做一件事：把 Python 装好、跑通第一个程序，并建立三种写代码的姿势——一次性脚本、交互式 REPL、IDE 工程。环境坑远比语法坑多，跟着本章走一遍，能避开 90% 的「我的 Python 呢」「为什么找不到模块」。",
"toc": [("sec1", "本章目标"), ("sec2", "2.1 安装 Python"), ("sec3", "2.2 三种运行方式"),
        ("sec4", "2.3 选 IDE：VS Code 或 PyCharm"), ("sec5", "2.4 第一个程序与读报错"),
        ("sec6", "2.5 多版本共存与 python -m"), ("sec7", "本章小结"), ("sec8", "本章习题")],
"sections": [
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>在 Windows / macOS / Linux 上装好 Python 3.10+，并能在终端验证版本；</li>
    <li>会用<strong>脚本、REPL、IDE</strong> 三种方式运行代码，知道各自适用场景；</li>
    <li>能处理最常见的三类报错与乱码问题；</li>
    <li>理解 <code>python -m</code> 与多版本启动器，避免"装了 A 跑的是 B"的经典惨案。</li>
  </ul>
</section>""",

"""<section id="sec2" class="card">
  <h2><span class="num">2.1</span> 安装 Python</h2>
  <h4>Windows</h4>
  <ol>
    <li>到 <code>python.org/downloads</code> 下载最新稳定版安装包；</li>
    <li>安装界面<strong>第一步务必勾选 "Add python.exe to PATH"</strong>——这是 Windows 新手第一大坑，漏勾后终端里就没有 <code>python</code> 命令；</li>
    <li>装完<strong>新开一个终端</strong>（PATH 变动不会作用于已开的窗口），验证：</li>
  </ol>
  <pre class="code" data-lang="bash"><code>python --version
# Python 3.13.1   （版本号无所谓，3.10+ 即可）

py --version      # Windows 专属启动器，通常指向最新版</code></pre>
  <h4>macOS</h4>
  <p>系统自带的 <code>python3</code> 是 Apple 维护的旧版，供系统内部使用，别动它。建议用 <strong>Homebrew</strong> 装一个独立的：<code>brew install python</code>，然后用 <code>python3</code> 调用。</p>
  <h4>Linux</h4>
  <pre class="code" data-lang="bash"><code>sudo apt update &amp;&amp; sudo apt install python3 python3-venv python3-pip   # Debian/Ubuntu
python3 --version</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span>Linux 上<strong>不要删除或替换系统自带的 python3</strong>，很多系统工具依赖它。自己装的那套用 <code>python3.13</code> 这样的名字调用，或用 pyenv 管多版本。</div>
  <h4>验证 pip 与 venv 可用</h4>
  <pre class="code" data-lang="bash"><code>python -m pip --version
# pip 25.x from ... (python 3.13)

python -m venv --help     # 能出帮助说明 venv 组件齐全</code></pre>
  <div class="note">注意这里用的是 <code>python -m pip</code> 而不是直接 <code>pip</code>——原因见 2.5 节。</div>
</section>""",

"""<section id="sec3" class="card">
  <h2><span class="num">2.2</span> 三种运行方式</h2>
  <table>
    <colgroup><col style="width:22%"><col style="width:46%"><col style="width:32%"></colgroup>
    <thead><tr><th>方式</th><th>怎么用</th><th>适用场景</th></tr></thead>
    <tbody>
      <tr><td>脚本文件</td><td><code>python hello.py</code></td><td>正式程序、可复用代码</td></tr>
      <tr><td>REPL 交互</td><td>终端输入 <code>python</code> 回车</td><td>试语法、查 API、临时计算</td></tr>
      <tr><td>IDE 运行</td><td>编辑器里点运行/调试</td><td>工程开发、断点调试</td></tr>
    </tbody>
  </table>
  <p>REPL（Read-Eval-Print Loop）里 <code>&gt;&gt;&gt;</code> 是输入提示符，<code>_</code> 保存上一次的结果，非常适合验证"这行代码到底返回什么"：</p>
  <pre class="code" data-lang="python"><code>&gt;&gt;&gt; 1 + 2 * 3
7
&gt;&gt;&gt; "hello".upper()
'HELLO'
&gt;&gt;&gt; _                # 上一个表达式的值
'HELLO'
&gt;&gt;&gt; exit()           # 或 Ctrl+Z(mac/Linux: Ctrl+D) 退出</code></pre>
  <p class="key-sentence">学习期请把 REPL 常驻：任何"这行到底返回什么"的疑问，5 秒内在 REPL 里得到答案，比翻书快得多。</p>
  <p>脚本方式则要注意文件命名：<strong>不要用 <code>json.py</code>、<code>random.py</code>、<code>email.py</code> 这类名字</strong>——它们会顶替标准库同名模块，导致"莫名其妙的报错"（第 19 章详述模块搜索路径）。</p>
</section>""",

"""<section id="sec4" class="card">
  <h2><span class="num">2.3</span> 选 IDE：VS Code 或 PyCharm</h2>
  <table>
    <colgroup><col style="width:20%"><col style="width:42%"><col style="width:38%"></colgroup>
    <thead><tr><th>工具</th><th>优势</th><th>适合谁</th></tr></thead>
    <tbody>
      <tr><td>VS Code</td><td>轻、快，配 Python 扩展后调试与测试齐全</td><td>多语言开发者、喜欢折腾配置的人</td></tr>
      <tr><td>PyCharm</td><td>开箱即用，重构与数据库工具强，社区版免费</td><td>主做 Python 的人、偏好一体化体验的人</td></tr>
      <tr><td>Jupyter</td><td>单元格执行，图表内联</td><td>数据分析、教学演示</td></tr>
    </tbody>
  </table>
  <p>本书推荐 <strong>VS Code + Python 扩展</strong>：装完扩展后做的事情只有一件——<strong>选择解释器</strong>（Cmd/Ctrl+Shift+P → <code>Python: Select Interpreter</code>），选中项目虚拟环境里的那个 python（第 30 章）。IDE 里跑代码和终端跑代码本质一样，它只是帮你填好了命令。</p>
  <div class="note">写第一行代码之前，把格式化工具装上（第 36 章详述）：<code>pip install ruff</code>，然后编辑器里开启保存时格式化。规范从第一天开始养成，成本最低。</div>
</section>""",

"""<section id="sec5" class="card">
  <h2><span class="num">2.4</span> 第一个程序与读报错</h2>
  <p>新建 <code>hello.py</code>：</p>
  <pre class="code" data-lang="python"><code>'''第一个 Python 程序：问候并计算。'''


def greet(name: str) -&gt; str:
    return f"你好，{name}！"


if __name__ == "__main__":
    who = input("你叫什么名字？")
    print(greet(who))
    print("1 到 100 的和是：", sum(range(1, 101)))</code></pre>
  <pre class="code" data-lang="bash"><code>$ python hello.py
你叫什么名字？张三
你好，张三！
1 到 100 的和是： 5050</code></pre>
  <p>这段 12 行代码里已经出现了本书后面会逐一展开的四个要素：<strong>文档字符串</strong>（第 10 章）、<strong>函数与类型注解</strong>（第 10、35 章）、<strong>f-string</strong>（第 4 章）、<strong><code>if __name__ == "__main__"</code></strong>（第 19 章）。</p>
  <h4>三类新手报错，先认脸</h4>
  <pre class="code" data-lang="text"><code># ① SyntaxError：语法写错，代码一行没跑
&gt;&gt;&gt; print("hi"
  File "&lt;stdin&gt;", line 1
    print("hi"
                ^
SyntaxError: '(' was never closed

# ② NameError：名字没定义（八成是拼错或忘了赋值）
&gt;&gt;&gt; print(mesage)
NameError: name 'mesage' is not defined

# ③ IndentationError：缩进不对（Python 的缩进是语法）
&gt;&gt;&gt; if True:
... print("x")
IndentationError: expected an indented block</code></pre>
  <p>读 traceback 的正确姿势：<strong>从最后一行往前看</strong>。最后一行是错误类型与原因，倒数几行是出错的文件与行号。<span class="tag-point">要点</span>报错不是惩罚，是解释器在告诉你它卡在哪一句。</p>
</section>""",

"""<section id="sec6" class="card">
  <h2><span class="num">2.5</span> 多版本共存与 python -m</h2>
  <p>一台机器上装多个 Python 版本很常见。三个关键约定：</p>
  <ol>
    <li><strong>Windows 用 <code>py</code> 启动器</strong>精确指定版本：<code>py -3.11 script.py</code>、<code>py -3.13 -m venv .venv</code>；</li>
    <li><strong>macOS / Linux 用带版本号的命令</strong>：<code>python3.11</code>、<code>python3.13</code>；需要频繁切换时用 <code>pyenv</code>；</li>
    <li><strong>永远优先 <code>python -m pip</code> 而不是 <code>pip</code></strong>。<code>-m 模块名</code> 的意思是"用当前这个解释器去运行该模块"，它保证了三件事一致：<u>装的包进当前解释器、装进当前虚拟环境、装的是当前 Python 版本的包</u>。</li>
  </ol>
  <pre class="code" data-lang="bash"><code># 反例：终端里直接敲 pip，可能装到另一个 Python 上
pip install requests          # 装到哪了？未必是你以为的那个

# 正例：明确"用这个解释器执行 pip 模块"
python -m pip install requests
py -3.12 -m pip install requests

# 其他常用 -m 场景
python -m venv .venv          # 建虚拟环境
python -m http.server 8000    # 起一个静态文件服务器
python -m pytest              # 跑测试（第 34 章）
python -m json.tool data.json # 格式化 JSON</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span>症状"我明明装了 requests，运行时却说 ModuleNotFoundError"——九成是因为 <strong>安装包和运行程序用的是两个不同的 Python</strong>。用 <code>python -m pip</code> 装、用同一个 <code>python</code> 跑，问题就消失。</div>
</section>""",

"""<section id="sec7" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:34%"><col style="width:66%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>安装三注意</td><td>勾 PATH、别动系统自带 python3、新开终端验证</td></tr>
      <tr><td>三种运行方式</td><td>脚本（正式）、REPL（试验）、IDE（工程）</td></tr>
      <tr><td>IDE 唯一必做项</td><td>选对解释器——指向项目虚拟环境</td></tr>
      <tr><td>报错读法</td><td>从最后一行倒着看：类型、原因、文件行号</td></tr>
      <tr><td>多版本</td><td>Windows 用 <code>py -3.xx</code>，其他用 <code>python3.xx</code></td></tr>
      <tr><td>铁律</td><td>用 <code>python -m pip</code>，保证装与跑是同一个解释器</td></tr>
    </tbody>
  </table>
</section>""",

"""<section id="sec8" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>在终端分别执行 <code>python --version</code> 与 <code>python -m pip --version</code>，把两行输出抄下来，确认它们指向同一个 Python 版本。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>把 2.4 节的 <code>hello.py</code> 抄进编辑器，改成：输入两个数字，输出它们的和与积（用 f-string 格式化）。再用 REPL 单独验证 <code>sum(range(1, 101))</code> 的值。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>故意制造三种报错（删掉一个括号、拼错一个变量名、把 <code>if</code> 下面一行的缩进删掉），各截图/记录一次 traceback，标出"最后一行"说了什么。</div>
  <p class="note">参考答案见附录 C（规划中）。下一章开始写真正的语法：变量与基本类型。</p>
</section>"""
]
},

# ════════════════════ 第 3 章 ════════════════════
{
"n": 3, "title": "变量与基本类型：名字贴对象",
"file": "003_第3章_变量与基本类型.html",
"meta": "预计 40 分钟 · 动手章",
"hero": 'Python 里"变量"不是盒子，而是贴在对象上的名字。理解这一点，后面所有"为什么改了 a 也改了 b""为什么这个是 False"的困惑都会自动消失。本章把 int/float/bool/None 讲透，并第一次接触"可变与不可变"这条贯穿全书的分水岭。',
"toc": [("sec1", "本章目标"), ("sec2", "3.1 变量是名字，不是盒子"), ("sec3", "3.2 四大基本类型"),
        ("sec4", "3.3 动态类型与类型查询"), ("sec5", "3.4 可变与不可变：第一条分水岭"),
        ("sec6", "3.5 数字精度与常见坑"), ("sec7", "本章小结"), ("sec8", "本章习题")],
"sections": [
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>能用 <code>id()</code> 与赋值行为解释"名字贴对象"模型，预测 <code>a = b</code> 之后修改其中一个的后果；</li>
    <li>掌握 <code>int</code> / <code>float</code> / <code>bool</code> / <code>NoneType</code> 四种基本类型的写法与转换；</li>
    <li>分清 <code>==</code> 与 <code>is</code>，理解小整数缓存；</li>
    <li>理解<strong>可变 / 不可变</strong>的差异，知道它对函数传参的影响；</li>
    <li>知道浮点数 <code>0.1 + 0.2 != 0.3</code> 的原因与 <code>decimal</code> 的用途。</li>
  </ul>
</section>""",

"""<section id="sec2" class="card">
  <h2><span class="num">3.1</span> 变量是名字，不是盒子</h2>
  <p>很多语言里"变量是一个装值的盒子"。Python 不是：<strong>对象是实体，变量是贴在对象上的标签</strong>。赋值语句 <code>a = 1</code> 读作"把名字 a 贴在对象 1 上"。</p>
  <pre class="code" data-lang="python"><code>a = 1
b = a          # 不是"复制一份 1 给 b"，而是"把名字 b 贴到 a 所指的同一个对象上"
print(a is b)  # True —— 同一个对象

a = a + 1      # 计算 a+1 得到新对象 2，把名字 a 贴到新对象上
print(a, b)    # 2 1 —— b 仍贴着原来的 1</code></pre>
  <p>用 <code>id()</code> 可以看到对象的"身份编号"（CPython 里就是内存地址）：</p>
  <pre class="code" data-lang="python"><code>print(id(1))          # 每次运行可能不同
x = 1
y = 1
print(id(x) == id(y)) # True：同一个对象 1，两个名字都贴着它

x = x + 1
print(id(x) == id(y)) # False：x 换贴到新对象 2 上了</code></pre>
  <div class="diagram">
    <svg viewBox="0 0 800 190" role="img" aria-label="名字贴对象示意">
      <text x="400" y="24" text-anchor="middle" font-size="14" font-weight="700" fill="#1f2e1f">名字贴对象：赋值只是换标签</text>
      <rect x="70" y="60" width="90" height="34" rx="6" fill="#f0f5e6" stroke="#3d7a4f"/><text x="115" y="82" text-anchor="middle" font-size="12.5" fill="#2d6a3f">名字 a</text>
      <rect x="70" y="110" width="90" height="34" rx="6" fill="#f0f5e6" stroke="#3d7a4f"/><text x="115" y="132" text-anchor="middle" font-size="12.5" fill="#2d6a3f">名字 b</text>
      <circle cx="300" cy="100" r="34" fill="#fff" stroke="#b45309" stroke-width="2"/><text x="300" y="106" text-anchor="middle" font-size="14" font-weight="700" fill="#b45309">1</text>
      <line x1="160" y1="77" x2="266" y2="95" stroke="#7a8a70" stroke-width="1.5"/><line x1="160" y1="127" x2="266" y2="106" stroke="#7a8a70" stroke-width="1.5"/>
      <text x="200" y="70" font-size="11.5" fill="#7a8a70">指向</text><text x="200" y="128" font-size="11.5" fill="#7a8a70">指向</text>
      <circle cx="560" cy="100" r="34" fill="#fefce8" stroke="#b45309" stroke-width="2"/><text x="560" y="106" text-anchor="middle" font-size="14" font-weight="700" fill="#b45309">2</text>
      <line x1="160" y1="77" x2="526" y2="88" stroke="#c2cfb4" stroke-width="1.5" stroke-dasharray="4 4"/>
      <text x="330" y="62" font-size="11.5" fill="#7a8a70">执行 a = a + 1 后，a 换贴到新对象 2</text>
      <text x="400" y="170" text-anchor="middle" font-size="12" fill="#7a8a70">对象不动，名字在动；没有名字贴着的 1 会被垃圾回收</text>
    </svg>
    <p class="diagram-caption">图 3-1 赋值 = 贴标签（示意）</p>
  </div>
  <p class="key-sentence">结论：Python 的赋值<strong>从不复制数据</strong>，它只是把名字贴到某个对象上。想复制，要显式调用 <code>list.copy()</code>、<code>copy.deepcopy()</code> 等（第 7 章）。</p>
</section>""",

"""<section id="sec3" class="card">
  <h2><span class="num">3.2</span> 四大基本类型</h2>
  <table>
    <colgroup><col style="width:20%"><col style="width:34%"><col style="width:46%"></colgroup>
    <thead><tr><th>类型</th><th>字面量写法</th><th>说明与常用操作</th></tr></thead>
    <tbody>
      <tr><td><code>int</code></td><td><code>42</code>、<code>0</code>、<code>-7</code>、<code>1_000_000</code></td><td>任意精度整数，不会溢出；下划线增强可读性</td></tr>
      <tr><td><code>float</code></td><td><code>3.14</code>、<code>1e6</code>、<code>-0.5</code></td><td>双精度浮点，有精度误差（见 3.5）</td></tr>
      <tr><td><code>bool</code></td><td><code>True</code> / <code>False</code></td><td>实为 int 的子类，<code>True + 1 == 2</code></td></tr>
      <tr><td><code>NoneType</code></td><td><code>None</code></td><td>唯一的空值对象，表示"没有值"</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="python"><code>age: int = 18            # 冒号后是"类型注解"（第 35 章），不影响运行
price: float = 19.9
is_vip: bool = True
deleted_at = None        # 表示"尚未删除"

print(type(age), type(price), type(is_vip), type(deleted_at))
# &lt;class 'int'&gt; &lt;class 'float'&gt; &lt;class 'bool'&gt; &lt;class 'NoneType'&gt;

print(2 ** 100)          # 1267650600228229401496703205376，int 不会溢出
print(7 / 2, 7 // 2, 7 % 2)   # 3.5 3 1  —— 除法永远得 float，// 是整除
print(round(3.14159, 2))      # 3.14</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span><code>7 / 2</code> 的结果是 <code>3.5</code>（要整除用 <code>//</code>），这是 Python 3 与 Python 2 最容易让人困惑的差异之一。</div>
</section>""",

"""<section id="sec4" class="card">
  <h2><span class="num">3.3</span> 动态类型与类型查询</h2>
  <p>同一个名字可以随时贴到不同类型的对象上，这就是动态类型：</p>
  <pre class="code" data-lang="python"><code>x = 10
x = "现在是字符串了"      # 完全合法
print(x)

# 类型查询
print(type("hi"))                 # &lt;class 'str'&gt;
print(isinstance(10, int))        # True
print(isinstance(True, int))      # True（bool 是 int 子类）
print(isinstance(10, (int, float)))  # 可以是多个类型之一

# 类型转换
print(int("42"), float("3.14"), str(100), bool(""), bool("x"))
# 42 3.14 '100' False True</code></pre>
  <h4>真假值（Truthiness）</h4>
  <p>Python 里任何对象都能当条件用，规则很短——<strong>空的东西和数字 0 为假</strong>：</p>
  <table>
    <colgroup><col style="width:46%"><col style="width:54%"></colgroup>
    <thead><tr><th>假（False）</th><th>真（True）</th></tr></thead>
    <tbody>
      <tr><td><code>False</code>、<code>None</code>、<code>0</code>、<code>0.0</code></td><td>其余数字（含负数）</td></tr>
      <tr><td><code>""</code>（空串）、<code>[]</code>、<code>()</code>、<code>{}</code>、空集合</td><td>非空容器、非空字符串</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="python"><code>name = input("请输入：") or "匿名"      # 空串为假，取默认值
items = []
if not items:                          # 判断空列表，不要写 len(items) == 0
    print("列表是空的")

# == 比较值，is 比较身份（是否同一个对象）
a = [1, 2]; b = [1, 2]
print(a == b, a is b)      # True False —— 值相等但不是同一个对象
print(None is None)        # 判断 None 必须用 is</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span>用 <code>==</code> 判断 <code>None</code> 是坏习惯（可能被自定义 <code>__eq__</code> 篡改），请一律写 <code>if x is None:</code> / <code>if x is not None:</code>。</div>
  <div class="note"><strong>小整数缓存</strong>：CPython 预先缓存了 <code>-5 ~ 256</code> 的整数对象，所以 <code>a = 100; b = 100; a is b</code> 为 True，但 <code>a = 1000; b = 1000; a is b</code> 通常为 False。<u>这是实现细节，不是语言规则</u>——永远只用 <code>is</code> 判 <code>None</code>，用 <code>==</code> 比值。</div>
</section>""",

"""<section id="sec5" class="card">
  <h2><span class="num">3.4</span> 可变与不可变：第一条分水岭</h2>
  <p>对象分成两类，这个区别会反复出现在函数传参、默认参数、字典键、拷贝等几乎所有主题里：</p>
  <table>
    <colgroup><col style="width:30%"><col style="width:34%"><col style="width:36%"></colgroup>
    <thead><tr><th>分类</th><th>代表类型</th><th>修改时的表现</th></tr></thead>
    <tbody>
      <tr><td><strong>不可变</strong></td><td>int、float、bool、str、tuple、frozenset</td><td>任何"修改"都生成新对象，原对象不变</td></tr>
      <tr><td><strong>可变</strong></td><td>list、dict、set、自定义对象（多半）</td><td>原地修改，所有贴着它的名字都看到变化</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="python"><code># 不可变：字符串"改"了，其实是换了个对象
s = "abc"
print(id(s))
s += "d"                 # 等价于 s = s + "d"，得到新对象
print(id(s))             # id 变了

# 可变：列表原地修改，别名"同步"看到变化
a = [1, 2]
b = a                    # b 与 a 指向同一个列表对象
b.append(3)
print(a)                 # [1, 2, 3] —— a 也变了！
print(a is b)            # True</code></pre>
  <p>这条性质直接决定了函数传参的行为（第 11 章展开）：<strong>传入不可变对象，函数内"修改"不会影响外部；传入可变对象并原地修改，外部看得见</strong>。</p>
  <pre class="code" data-lang="python"><code>def add_item(items, x):
    items.append(x)      # 原地修改可变对象 → 外部可见

def add_one(n):
    n = n + 1            # 只是把局部名字贴到新对象 → 外部不可见

lst = [1]; add_item(lst, 2); print(lst)   # [1, 2]
num = 1;  add_one(num);    print(num)     # 1</code></pre>
  <p class="key-sentence">口诀：不可变对象"改"= 换人；可变对象改 = 换内容。想让可变对象不被误改，传副本：<code>add_item(list(lst), 2)</code>。</p>
</section>""",

"""<section id="sec6" class="card">
  <h2><span class="num">3.5</span> 数字精度与常见坑</h2>
  <pre class="code" data-lang="python"><code>&gt;&gt;&gt; 0.1 + 0.2
0.30000000000000004
&gt;&gt;&gt; 0.1 + 0.2 == 0.3
False</code></pre>
  <p>原因不是 Python 的锅，而是<strong>二进制浮点无法精确表示 0.1</strong>（如同十进制无法精确表示 1/3）。这是 IEEE 754 的通用特性，所有语言都一样。</p>
  <p>三种正确处理方式：</p>
  <pre class="code" data-lang="python"><code># ① 比较用容差（最常用）
import math
print(math.isclose(0.1 + 0.2, 0.3))       # True

# ② 金额计算用 Decimal（十进制浮点）
from decimal import Decimal, ROUND_HALF_UP
price = Decimal("19.99")
total = price * Decimal("3")
print(total)                               # 59.97
print(total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))  # 59.97

# ③ 分数用 Fraction
from fractions import Fraction
print(Fraction(1, 3) + Fraction(1, 6))     # 1/2</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span>写 <code>Decimal(19.99)</code>（传 float）会继承浮点误差，必须传字符串 <code>Decimal("19.99")</code>。</div>
  <h4>其他数字技巧</h4>
  <pre class="code" data-lang="python"><code>print(divmod(17, 5))          # (3, 2) 商和余数一起拿
print(abs(-3), pow(2, 10), max(1, 5, 3), min([4, 2]))
print(sum([1, 2, 3]))         # 6
print(bin(10), oct(10), hex(10))   # 0b1010 0o12 0xa
print(int("ff", 16))          # 255  按进制解析
print(round(2.5), round(3.5)) # 2 4 —— 银行家舍入（奇进偶不进）</code></pre>
</section>""",

"""<section id="sec7" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:34%"><col style="width:66%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>变量模型</td><td>对象是实体，变量是名字；赋值 = 贴标签，从不复制</td></tr>
      <tr><td>基本类型</td><td>int（任意精度）、float（双精度）、bool（int 子类）、None（空值）</td></tr>
      <tr><td>除法</td><td><code>/</code> 得 float，<code>//</code> 整除，<code>%</code> 取余，<code>divmod</code> 一次拿俩</td></tr>
      <tr><td>真假值</td><td>空的与 0 为假；用 <code>if not items</code> 判空</td></tr>
      <tr><td><code>==</code> vs <code>is</code></td><td><code>==</code> 比值，<code>is</code> 比身份；判 None 用 is</td></tr>
      <tr><td>可变 / 不可变</td><td>不可变"改"= 换对象；可变原地改，别名同步可见</td></tr>
      <tr><td>浮点</td><td><code>math.isclose</code> 比大小，<code>Decimal</code> 算金额</td></tr>
    </tbody>
  </table>
</section>""",

"""<section id="sec8" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>不用运行，预测以下代码的输出，再上机验证：<code>a = [1]; b = a; b.append(2); print(a)</code>；<code>s = "x"; t = s; s += "y"; print(t)</code>。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>写一个函数 <code>celsius_to_fahrenheit(c)</code>，返回保留一位小数的华氏度；再写 <code>is_adult(age)</code>，年龄为空（None）时返回 False。要求：金额为 19.99 的三倍用 <code>Decimal</code> 算。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>解释为什么 <code>[] is []</code> 是 False 而 <code>"" is ""</code> 通常是 True（提示：小整数与短字符串的驻留机制），并说明为什么生产代码不该依赖这个行为。</div>
  <p class="note">参考答案见附录 C（规划中）。下一章进入字符串：Python 里最"方法多"的类型。</p>
</section>"""
]
}
]

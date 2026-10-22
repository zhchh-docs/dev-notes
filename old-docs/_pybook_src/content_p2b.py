# -*- coding: utf-8 -*-
"""第二篇 函数与进阶语法 · 第 13-16 章"""

PART_DIR = "20_第二篇_函数与进阶语法"
PART_NAME = "第二篇 函数与进阶语法"

CHAPTERS = [
# ════════════════════ 第 13 章 ════════════════════
{
"n": 13, "title": "推导式：列表/字典/集合",
"file": "013_第13章_推导式.html",
"meta": "预计 35 分钟 · 动手章",
"hero": "推导式是 Python 最具辨识度的语法之一：把「建空容器 + for 循环 + append」三行压缩成一行，而且更快、更像人话。本章讲透四种推导式的写法、嵌套与过滤，以及「什么时候不该用推导式」这条重要边界。",
"toc": [("sec1", "本章目标"), ("sec2", "13.1 列表推导式"), ("sec3", "13.2 带条件与嵌套"),
        ("sec4", "13.3 字典与集合推导式"), ("sec5", "13.4 性能与可读性边界"),
        ("sec6", "13.5 常见坑"), ("sec7", "本章小结"), ("sec8", "本章习题")],
"sections": [
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>掌握<strong>列表 / 字典 / 集合</strong>三种推导式与生成器表达式的写法；</li>
    <li>会在推导式里加 <code>if</code> 过滤、加 <code>if-else</code> 三元变换、写多重循环；</li>
    <li>理解推导式为什么<strong>比 append 循环快</strong>；</li>
    <li>知道<strong>什么时候不该用</strong>推导式（可读性边界）；</li>
    <li>理解推导式的<strong>独立作用域</strong>，避开变量泄漏的差异。</li>
  </ul>
</section>""",

"""<section id="sec2" class="card">
  <h2><span class="num">13.1</span> 列表推导式</h2>
  <pre class="code" data-lang="python"><code># 传统写法：建空列表 → 循环 → append
squares = []
for x in range(5):
    squares.append(x ** 2)

# 推导式：一行搞定，语义是"由 x 组成的 x² 的列表"
squares = [x ** 2 for x in range(5)]
print(squares)          # [0, 1, 4, 9, 16]</code></pre>
  <p>通用结构：<code>[表达式 for 变量 in 可迭代对象]</code>。读的时候就把它当一句中文念：<strong>"对每个 x，收集 x²"</strong>。</p>
  <pre class="code" data-lang="python"><code>names = [" 张三 ", "李四", " 王五 "]
cleaned = [n.strip() for n in names]
print(cleaned)                       # ['张三', '李四', '王五']

# 表达式部分可以是任意运算或函数调用
prices = [19.9, 5.5, 100.0]
print([f"¥{p:.2f}" for p in prices])          # ['¥19.90', '¥5.50', '¥100.00']
print([p * 0.8 for p in prices])              # 打八折

# 多个变量（解包）
pairs = [(1, "a"), (2, "b")]
print([f"{num}{ch}" for num, ch in pairs])    # ['1a', '2b']</code></pre>
  <p class="key-sentence">推导式的核心价值不是"少写几行"，而是<strong>把"我要构造一个新列表"这个意图写成了声明式代码</strong>——读代码的人不用追踪 append 的累积过程。</p>
</section>""",

"""<section id="sec3" class="card">
  <h2><span class="num">13.2</span> 带条件与嵌套</h2>
  <h4>过滤：<code>if</code> 放后面</h4>
  <pre class="code" data-lang="python"><code>nums = range(10)
print([n for n in nums if n % 2 == 0])        # [0, 2, 4, 6, 8]
print([n for n in nums if n &gt; 5 if n % 3])    # 多个 if = and 关系：[7]

# 复杂条件可以抽成函数，可读性更好
def is_valid(n):
    return n &gt; 5 and n % 3 != 0

print([n for n in nums if is_valid(n)])       # [7, 8]</code></pre>
  <h4>变换：<code>if-else</code> 放前面（三元表达式）</h4>
  <pre class="code" data-lang="python"><code># 注意位置：if-else 在 for 之前，是"表达式的一部分"
scores = [95, 55, 78, 30]
labels = ["及格" if s &gt;= 60 else "不及格" for s in scores]
print(labels)          # ['及格', '不及格', '及格', '不及格']

# 对比：只过滤不带 else 时，if 在 for 之后
passed = [s for s in scores if s &gt;= 60]
print(passed)          # [95, 78]</code></pre>
  <div class="warn-box"><span class="tag-pit">易混点</span><code>[x if c else y for ...]</code>（三元变换，每个元素都有输出）与 <code>[... for ... if c]</code>（过滤，不满足就不要）是两回事，别写反了。</div>
  <h4>嵌套循环</h4>
  <pre class="code" data-lang="python"><code># 两层循环：顺序与嵌套 for 一致（外层在前）
print([(x, y) for x in range(2) for y in "ab"])
# [(0, 'a'), (0, 'b'), (1, 'a'), (1, 'b')]

# 展开二维列表（扁平化）
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [n for row in matrix for n in row]
print(flat)            # [1, 2, 3, 4, 5, 6]

# 嵌套推导式：转置矩阵（注意可读性）
transposed = [[row[i] for row in matrix] for i in range(2)]
print(transposed)      # [[1, 3, 5], [2, 4, 6]]</code></pre>
</section>""",

"""<section id="sec4" class="card">
  <h2><span class="num">13.3</span> 字典与集合推导式</h2>
  <pre class="code" data-lang="python"><code># 字典推导式：{键表达式: 值表达式 for ...}
words = ["apple", "banana", "cherry"]
print({w: len(w) for w in words})          # {'apple': 5, 'banana': 6, 'cherry': 6}

# 键值互换（值必须唯一，否则后者覆盖）
d = {"a": 1, "b": 2}
print({v: k for k, v in d.items()})        # {1: 'a', 2: 'b'}

# 过滤 + 变换
prices = {"apple": 5, "banana": 2, "cherry": 20}
print({k: v for k, v in prices.items() if v &gt; 3})     # {'apple': 5, 'cherry': 20}

# 集合推导式：自动去重
text = "hello world"
print({ch for ch in text if ch != " "})    # {'h', 'e', 'l', 'o', 'w', 'r', 'd'}

nums = [1, 2, 2, 3, 3, 3]
print({n ** 2 for n in nums})              # {1, 4, 9}</code></pre>
  <h4>实用场景：建索引</h4>
  <pre class="code" data-lang="python"><code>users = [
    {"id": 1, "name": "张三", "city": "北京"},
    {"id": 2, "name": "李四", "city": "上海"},
    {"id": 3, "name": "王五", "city": "北京"},
]

by_id = {u["id"]: u for u in users}        # 主键索引：之后 O(1) 查询
print(by_id[2]["name"])                    # 李四

# 分组：值与列表（比 setdefault 更直观）
from collections import defaultdict
by_city = defaultdict(list)
for u in users:
    by_city[u["city"]].append(u["name"])
print(dict(by_city))   # {'北京': ['张三', '王五'], '上海': ['李四']}</code></pre>
</section>""",

"""<section id="sec5" class="card">
  <h2><span class="num">13.4</span> 性能与可读性边界</h2>
  <p>推导式通常比"append 循环"快 20%~50%，因为它直接在 C 层构造列表，省掉了每次循环的属性查找与方法调用：</p>
  <pre class="code" data-lang="python"><code>import timeit

loop = "res = []\nfor i in range(1000):\n    res.append(i * 2)"
comp = "res = [i * 2 for i in range(1000)]"

print(round(timeit.timeit(loop, number=5000), 3))   # 约 0.45s
print(round(timeit.timeit(comp, number=5000), 3))   # 约 0.28s</code></pre>
  <p>但<strong>可读性优先于那点性能</strong>。下面这些情况请老实用循环：</p>
  <table>
    <colgroup><col style="width:40%"><col style="width:60%"></colgroup>
    <thead><tr><th>不该用推导式的情形</th><th>原因</th></tr></thead>
    <tbody>
      <tr><td>超过两层循环或含复杂逻辑</td><td>一行塞太多，读的人要"解码"</td></tr>
      <tr><td>需要 <code>try/except</code> 处理异常</td><td>推导式里放不下异常处理</td></tr>
      <tr><td>需要中途 <code>break</code> / <code>return</code></td><td>推导式必须跑完整个序列</td></tr>
      <tr><td>有副作用（打印、写文件、改外部状态）</td><td>推导式的语义是"构造新容器"，有副作用就该用 for</td></tr>
      <tr><td>结果非常大且只用一次</td><td>改用生成器表达式（第 14 章），省内存</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="python"><code># 反例：为副作用而用推导式（千万不要）
# [print(x) for x in range(3)]      ← 这会白白构造一个 [None, None, None]

# 正例
for x in range(3):
    print(x)</code></pre>
</section>""",

"""<section id="sec6" class="card">
  <h2><span class="num">13.5</span> 常见坑</h2>
  <h4>① 推导式有自己的作用域（Python 3）</h4>
  <pre class="code" data-lang="python"><code>x = "外层"
lst = [x for x in range(3)]
print(x)          # '外层'   ← Python 3 中推导式的 x 不会泄漏到外部

# 而在 Python 2 里，列表推导式会泄漏变量（历史包袱，了解即可）</code></pre>
  <h4>② 嵌套推导式里的循环变量遮蔽</h4>
  <pre class="code" data-lang="python"><code># lambda 在推导式里同样有 late binding 问题（第 12 章）
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])       # [2, 2, 2]
funcs = [lambda i=i: i for i in range(3)]
print([f() for f in funcs])       # [0, 1, 2]</code></pre>
  <h4>③ 大数据的内存问题 → 用生成器表达式</h4>
  <pre class="code" data-lang="python"><code>import sys
big_list = [x ** 2 for x in range(1_000_000)]      # 立即占用约 40MB
big_gen = (x ** 2 for x in range(1_000_000))       # 几乎不占内存
print(sys.getsizeof(big_list), sys.getsizeof(big_gen))   # 8448728 104</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span>把方括号换成圆括号就是<strong>生成器表达式</strong>——它惰性求值、<strong>只能遍历一次</strong>。用完再遍历会得到空结果（第 14 章详述）。</div>
</section>""",

"""<section id="sec7" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:34%"><col style="width:66%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>列表推导式</td><td><code>[expr for x in seq if cond]</code>，表达"构造新列表"</td></tr>
      <tr><td>两个位置</td><td><code>if</code> 在后=过滤；<code>if-else</code> 在前=三元变换</td></tr>
      <tr><td>字典 / 集合</td><td><code>{k: v for ...}</code> / <code>{expr for ...}</code>，后者自动去重</td></tr>
      <tr><td>嵌套</td><td>外层循环在前，与嵌套 for 顺序一致</td></tr>
      <tr><td>性能</td><td>比 append 快；但可读性优先</td></tr>
      <tr><td>不该用</td><td>复杂逻辑、异常、break、副作用、超大数据</td></tr>
      <tr><td>作用域</td><td>Python 3 推导式独立作用域，不泄漏循环变量</td></tr>
    </tbody>
  </table>
</section>""",

"""<section id="sec8" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>用推导式完成：① 1~100 中能同时被 3 和 5 整除的数；② 把 <code>["a", "bb", "ccc"]</code> 变成 <code>{1: "a", 2: "bb", 3: "ccc"}</code>；③ 把嵌套列表 <code>[[1,2],[3,4]]</code> 扁平化。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>给定日志行列表（每行形如 <code>"2026-10-19 10:00 INFO 登录成功"</code>），用推导式提取所有 ERROR 级别的行，并统计每个级别的条数（字典推导式 + <code>Counter</code> 二选一）。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>用 <code>timeit</code> 对比"append 循环""列表推导式""<code>map()</code>"三者在一百万数据上的耗时并排序，然后解释"为什么 map 有时并不更快"（提示：需要 lambda 时会有额外的函数调用开销）。</div>
  <p class="note">参考答案见附录 C（规划中）。下一章：生成器与 yield。</p>
</section>"""
]
},

# ════════════════════ 第 14 章 ════════════════════
{
"n": 14, "title": "生成器：yield 与惰性求值",
"file": "014_第14章_生成器.html",
"meta": "预计 45 分钟 · 动手章",
"hero": "生成器让 Python 能「边算边给」：不一次性构造整个列表，而是需要时才产出下一个值。这是处理大文件、流式数据、无限序列的核心武器，也是理解 asyncio（第六篇）的必要前置。",
"toc": [("sec1", "本章目标"), ("sec2", "14.1 从内存问题说起"), ("sec3", "14.2 yield 的工作原理"),
        ("sec4", "14.3 生成器表达式与管道"), ("sec5", "14.4 高级：send / throw / close"),
        ("sec6", "14.5 yield from 与常见坑"), ("sec7", "本章小结"), ("sec8", "本章习题")],
"sections": [
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>理解<strong>惰性求值</strong>的价值：省内存、能表达无限序列、可提前退出；</li>
    <li>能用 <code>yield</code> 写生成器函数，讲清它与 <code>return</code> 的区别；</li>
    <li>会用生成器表达式与<strong>管道式</strong>数据处理；</li>
    <li>了解 <code>send()</code> / <code>throw()</code> / <code>close()</code> 与 <code>yield from</code>；</li>
    <li>知道生成器<strong>只能遍历一次</strong>这个高频坑。</li>
  </ul>
</section>""",

"""<section id="sec2" class="card">
  <h2><span class="num">14.1</span> 从内存问题说起</h2>
  <pre class="code" data-lang="python"><code># 需求：处理一个 10GB 的日志文件，统计含 "ERROR" 的行数

# 方案一：一次性读入 → 内存爆炸
def count_errors_bad(path):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()          # 10GB 全进内存 → MemoryError
    return sum(1 for line in lines if "ERROR" in line)

# 方案二：文件对象本身就是迭代器，一次只给一行
def count_errors_good(path):
    with open(path, encoding="utf-8") as f:
        return sum(1 for line in f if "ERROR" in line)   # 内存恒定</code></pre>
  <p>这就是<strong>惰性求值（lazy evaluation）</strong>的力量：数据不是"先准备好再处理"，而是"要一个给一个"。</p>
  <pre class="code" data-lang="python"><code>import sys

# 列表：立即构造，占内存
squares_list = [x ** 2 for x in range(1_000_000)]
print(sys.getsizeof(squares_list))        # 约 8.4 MB

# 生成器表达式：只保存"算法"，几乎不占内存
squares_gen = (x ** 2 for x in range(1_000_000))
print(sys.getsizeof(squares_gen))         # 约 104 字节</code></pre>
  <p class="key-sentence">判断标准：<strong>数据量可能很大 / 无限 / 只需要前几个</strong> → 用生成器；<strong>需要反复遍历、随机访问、求长度</strong> → 用列表。</p>
</section>""",

"""<section id="sec3" class="card">
  <h2><span class="num">14.2</span> yield 的工作原理</h2>
  <p>函数里出现 <code>yield</code>，它就不再是普通函数，而是<strong>生成器函数</strong>：调用它不执行函数体，而是返回一个生成器对象。</p>
  <pre class="code" data-lang="python"><code>def count_up_to(n):
    i = 1
    while i &lt;= n:
        print(f"产出 {i}")
        yield i          # 暂停在这里，把 i 交出去
        i += 1
    print("生成结束")

g = count_up_to(3)
print(g)                 # &lt;generator object count_up_to at 0x...&gt;  ← 函数体一行没跑

print(next(g))           # 产出 1  →  1
print(next(g))           # 产出 2  →  2
print(next(g))           # 产出 3  →  3
# print(next(g))         # 生成结束，然后抛 StopIteration</code></pre>
  <p>执行流程的关键：<strong>yield 是"暂停并交出值"，下次 next() 从暂停处继续</strong>。函数的局部变量被完整保留——这就是"协程"的雏形。</p>
  <div class="diagram">
    <svg viewBox="0 0 800 170" role="img" aria-label="yield 暂停与恢复示意">
      <text x="400" y="22" text-anchor="middle" font-size="14" font-weight="700" fill="#1f2e1f">yield：暂停 → 交出值 → 从暂停处恢复</text>
      <rect x="40" y="50" width="150" height="44" rx="8" fill="#f0f5e6" stroke="#3d7a4f"/><text x="115" y="77" text-anchor="middle" font-size="12.5" fill="#2d6a3f">next(g) 调用</text>
      <rect x="230" y="50" width="150" height="44" rx="8" fill="#f0f5e6" stroke="#3d7a4f"/><text x="305" y="77" text-anchor="middle" font-size="12.5" fill="#2d6a3f">执行到 yield</text>
      <rect x="420" y="50" width="150" height="44" rx="8" fill="#fefce8" stroke="#b45309"/><text x="495" y="77" text-anchor="middle" font-size="12.5" fill="#b45309">交出值并暂停</text>
      <rect x="610" y="50" width="150" height="44" rx="8" fill="#fefce8" stroke="#b45309"/><text x="685" y="77" text-anchor="middle" font-size="12.5" fill="#b45309">下次 next 从此处继续</text>
      <line x1="190" y1="72" x2="230" y2="72" stroke="#7a8a70" stroke-width="1.5"/>
      <line x1="380" y1="72" x2="420" y2="72" stroke="#7a8a70" stroke-width="1.5"/>
      <line x1="570" y1="72" x2="610" y2="72" stroke="#7a8a70" stroke-width="1.5"/>
      <text x="400" y="128" text-anchor="middle" font-size="12" fill="#4f6348">局部变量（i）与执行位置都被保留在生成器对象的帧里</text>
      <text x="400" y="152" text-anchor="middle" font-size="12" fill="#7a8a70">函数结束（或 return）时自动抛 StopIteration，for 循环正是靠它停止的</text>
    </svg>
    <p class="diagram-caption">图 14-1 yield 的暂停 / 恢复（示意）</p>
  </div>
  <pre class="code" data-lang="python"><code># 生成器里也能写 return：它的值会成为 StopIteration.value
def gen():
    yield 1
    return "完成"
    yield 2      # 不会执行

g = gen()
print(next(g))
try:
    next(g)
except StopIteration as e:
    print(e.value)      # 完成</code></pre>
</section>""",

"""<section id="sec4" class="card">
  <h2><span class="num">14.3</span> 生成器表达式与管道</h2>
  <p>生成器表达式语法与列表推导式一样，只是把 <code>[]</code> 换成 <code>()</code>：</p>
  <pre class="code" data-lang="python"><code>gen = (x * 2 for x in range(5))
print(list(gen))              # [0, 2, 4, 6, 8]

# 只有一个参数时，连括号都能省（函数调用里）
print(sum(x ** 2 for x in range(10)))     # 285
print(max(len(w) for w in ["a", "bb", "ccc"]))   # 3</code></pre>
  <h4>管道式数据处理：把每一步串起来</h4>
  <pre class="code" data-lang="python"><code>def read_lines(path):
    with open(path, encoding="utf-8") as f:
        yield from f                  # 逐行产出

def strip_lines(lines):
    for line in lines:
        yield line.strip()

def non_empty(lines):
    for line in lines:
        if line:
            yield line

def numbered(lines):
    for i, line in enumerate(lines, 1):
        yield f"{i:04d} {line}"

# 像搭管道一样组装，全程惰性：内存里永远只有一行
pipeline = numbered(non_empty(strip_lines(read_lines("app.log"))))
for row in pipeline:
    print(row)</code></pre>
  <p class="key-sentence">这就是"Unix 管道"思想在 Python 里的落地：每一步只做一件事、只处理一个元素，串起来后内存占用恒定，且每一步都可单独测试。</p>
  <div class="note">标准库 <code>itertools</code> 提供了大量现成的管道零件（<code>islice</code>、<code>chain</code>、<code>groupby</code>……），第 27 章专题。</div>
</section>""",

"""<section id="sec5" class="card">
  <h2><span class="num">14.4</span> 高级：send / throw / close</h2>
  <p>生成器不仅能"产出"，还能<strong>接收</strong>——<code>yield</code> 是一个表达式，<code>send()</code> 把值送进去：</p>
  <pre class="code" data-lang="python"><code>def accumulator():
    total = 0
    while True:
        value = yield total       # ① 暂停并交出 total；② 收到 send 的值后赋给 value
        if value is None:
            break
        total += value

acc = accumulator()
next(acc)                 # 预激（prime）：先跑到第一个 yield，输出 0
print(acc.send(10))       # 10
print(acc.send(20))       # 30
print(acc.send(5))        # 35
acc.close()               # 关闭生成器（内部抛 GeneratorExit）</code></pre>
  <table>
    <colgroup><col style="width:24%"><col style="width:40%"><col style="width:36%"></colgroup>
    <thead><tr><th>方法</th><th>作用</th><th>说明</th></tr></thead>
    <tbody>
      <tr><td><code>next(g)</code></td><td>推进到下一个 yield</td><td>等价于 <code>g.send(None)</code></td></tr>
      <tr><td><code>g.send(v)</code></td><td>把 v 作为 yield 表达式的值送进去</td><td>必须先 <code>next()</code> 预激</td></tr>
      <tr><td><code>g.throw(exc)</code></td><td>在暂停处抛出异常</td><td>可用于错误注入测试</td></tr>
      <tr><td><code>g.close()</code></td><td>关闭生成器</td><td>内部触发 <code>GeneratorExit</code>，可执行清理</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="python"><code># 用 try/finally 做清理：close() 或 GC 时会执行
def resource_gen():
    print("打开资源")
    try:
        while True:
            yield "数据"
    finally:
        print("释放资源")        # close() / 被回收时执行

g = resource_gen(); next(g); g.close()     # 打开资源 / 释放资源</code></pre>
  <div class="note">现代 Python 里，"协程"已由 <code>async/await</code> 承担（第 55 章），<code>send()</code> 更多出现在框架底层与测试代码中。理解它，你就理解了协程的前世。</div>
</section>""",

"""<section id="sec6" class="card">
  <h2><span class="num">14.5</span> yield from 与常见坑</h2>
  <p><code>yield from</code>（3.3+）用于把"产出"委托给另一个可迭代对象，省掉一层 for：</p>
  <pre class="code" data-lang="python"><code>def chain_manual(*iterables):
    for it in iterables:
        for x in it:            # 两层循环
            yield x

def chain_delegate(*iterables):
    for it in iterables:
        yield from it           # 委托，更简洁且支持 send 透传

print(list(chain_delegate([1, 2], "ab")))      # [1, 2, 'a', 'b']

# 递归展开嵌套结构，yield from 特别优雅
def flatten(items):
    for x in items:
        if isinstance(x, (list, tuple)):
            yield from flatten(x)
        else:
            yield x

print(list(flatten([1, [2, [3, 4]], 5])))      # [1, 2, 3, 4, 5]</code></pre>
  <div class="danger-box"><span class="tag-pit">头号坑</span><strong>生成器只能遍历一次</strong>。用完即空，再遍历得到空结果——这是从"列表思维"转过来时最容易犯的错：</div>
  <pre class="code" data-lang="python"><code>g = (x for x in range(3))
print(list(g))       # [0, 1, 2]
print(list(g))       # []          ← 空了！

# 需要多次遍历 / 随机访问 / 求长度 → 转成列表
data = list(generator)

# 或者需要"两路复用"时用 itertools.tee（本质是缓存，慎用大数据）
from itertools import tee
g1, g2 = tee((x for x in range(3)), 2)
print(list(g1), list(g2))     # [0, 1, 2] [0, 1, 2]</code></pre>
  <p>其他注意点：</p>
  <ul>
    <li>生成器<strong>没有 <code>len()</code></strong>，也不能按下标取值——要统计只能遍历；</li>
    <li>生成器里的错误<strong>惰性触发</strong>：只有推进到那一步才抛异常，调试时留意 traceback 的调用栈；</li>
    <li><code>yield</code> 与 <code>return</code> 不要混在一个函数里表达两种语义（3.3+ 允许 return 值，但可读性差）。</li>
  </ul>
</section>""",

"""<section id="sec7" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:34%"><col style="width:66%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>惰性求值</td><td>要一个算一个；内存恒定，可处理无限序列</td></tr>
      <tr><td>yield</td><td>暂停并交出值；下次从暂停处继续，局部变量保留</td></tr>
      <tr><td>生成器表达式</td><td><code>(expr for x in seq)</code>；单参数时可省括号</td></tr>
      <tr><td>管道</td><td>多个生成器串联，每步只处理一个元素</td></tr>
      <tr><td>send / throw / close</td><td>双向通信；协程的前世</td></tr>
      <tr><td>yield from</td><td>委托产出，递归展开特别好用</td></tr>
      <tr><td>头号坑</td><td>只能遍历一次；没有 len、不能下标访问</td></tr>
    </tbody>
  </table>
</section>""",

"""<section id="sec8" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>写生成器 <code>evens(n)</code> 产出 0~n 的偶数；再写 <code>fib()</code> 无限产出斐波那契数列，用 <code>itertools.islice</code> 取前 20 个打印。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>用管道方式处理一个日志文件：逐行读 → 去空白 → 过滤空行 → 只留 ERROR → 提取时间戳。要求全程惰性，并说明为什么不直接用 <code>readlines()</code>。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>实现一个 <code>chunked(iterable, size)</code> 生成器：每次产出 size 个元素组成的列表（最后一批可以不满）；要求对任意可迭代对象（含生成器）都可用，并写测试证明它对无限序列也安全。</div>
  <p class="note">参考答案见附录 C（规划中）。下一章：迭代器协议——for 循环的底层。</p>
</section>"""
]
},

# ════════════════════ 第 15 章 ════════════════════
{
"n": 15, "title": "迭代器协议：for 的底层",
"file": "015_第15章_迭代器协议.html",
"meta": "预计 40 分钟 · 动手章",
"hero": "为什么 for 能遍历列表、文件、字典、生成器，却不能遍历一个整数？答案是一套只有两个方法的协议。理解迭代器协议，你就掌握了 Python 遍历机制的统一模型，也能让自己的类「可被 for」。",
"toc": [("sec1", "本章目标"), ("sec2", "15.1 可迭代对象 vs 迭代器"), ("sec3", "15.2 for 循环到底做了什么"),
        ("sec4", "15.3 自己实现迭代器"), ("sec5", "15.4 迭代器是一次性的"),
        ("sec6", "15.5 itertools 与常见坑"), ("sec7", "本章小结"), ("sec8", "本章习题")],
"sections": [
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>分清<strong>可迭代对象（Iterable）</strong>与<strong>迭代器（Iterator）</strong>；</li>
    <li>能手工还原 <code>for</code> 循环的等价代码；</li>
    <li>会为自己的类实现 <code>__iter__</code> / <code>__next__</code>；</li>
    <li>理解迭代器"一次性"的设计取舍；</li>
    <li>认识 <code>itertools</code> 里的常用工具与无限迭代器。</li>
  </ul>
</section>""",

"""<section id="sec2" class="card">
  <h2><span class="num">15.1</span> 可迭代对象 vs 迭代器</h2>
  <table>
    <colgroup><col style="width:22%"><col style="width:38%"><col style="width:40%"></colgroup>
    <thead><tr><th>概念</th><th>协议方法</th><th>特点 / 例子</th></tr></thead>
    <tbody>
      <tr><td>可迭代对象 Iterable</td><td><code>__iter__()</code></td><td>能"给出"迭代器：list、str、dict、tuple、set、文件</td></tr>
      <tr><td>迭代器 Iterator</td><td><code>__iter__()</code> + <code>__next__()</code></td><td>能"逐个产出"：生成器、文件对象、<code>iter(list)</code></td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="python"><code>from collections.abc import Iterable, Iterator

print(isinstance([1, 2], Iterable))     # True
print(isinstance([1, 2], Iterator))     # False   ← 列表只是"可迭代"，不是迭代器
print(isinstance(iter([1, 2]), Iterator))  # True  ← iter() 造出来的才是
print(isinstance((x for x in range(2)), Iterator))  # True  生成器是迭代器
print(isinstance(42, Iterable))         # False</code></pre>
  <p class="key-sentence">一句话区分：<strong>可迭代对象 = 能反复取出新迭代器的容器；迭代器 = 记住了"当前位置"、只能走一趟的游标。</strong></p>
  <pre class="code" data-lang="python"><code>lst = [1, 2, 3]

it = iter(lst)            # 从容器拿到迭代器
print(next(it))           # 1
print(next(it))           # 2
print(next(it))           # 3
# print(next(it))         # StopIteration → for 循环靠它结束

print(list(iter(lst)))    # [1, 2, 3]  再取一个新的迭代器，又能从头走</code></pre>
</section>""",

"""<section id="sec3" class="card">
  <h2><span class="num">15.2</span> for 循环到底做了什么</h2>
  <pre class="code" data-lang="python"><code>for item in [1, 2, 3]:
    print(item)

# 等价于下面这段（这就是 for 的全部秘密）：
_iter = iter([1, 2, 3])          # ① 取迭代器
while True:
    try:
        item = next(_iter)       # ② 不断取下一个
    except StopIteration:        # ③ 取完了就停
        break
    print(item)</code></pre>
  <p>由此可以理解几个"为什么"：</p>
  <ul>
    <li><strong>为什么遍历时改列表会出怪事</strong>：列表迭代器按<strong>内部下标</strong>前进，删除元素导致元素前移，于是跳过某些项（第 6 章）；</li>
    <li><strong>为什么文件遍历一次就没了</strong>：文件对象是<strong>迭代器</strong>（自带位置游标），走完就到底了；</li>
    <li><strong>为什么 <code>in</code> 既能判断成员又能遍历</strong>：<code>x in obj</code> 会依次尝试 <code>__contains__</code> → <code>__iter__</code> → <code>__getitem__</code>。</li>
  </ul>
  <pre class="code" data-lang="python"><code># 手动控制迭代器是"批处理"的基础
with open("data.txt", encoding="utf-8") as f:
    while True:
        line = next(f, None)          # 给个哨兵值，避免 try/except
        if line is None:
            break
        print(line.rstrip())</code></pre>
  <div class="note"><code>next(it, default)</code> 的第二个参数是<strong>哨兵值</strong>：迭代器耗尽时返回它而不是抛异常——写"取 N 个"这类逻辑时非常省事。</div>
</section>""",

"""<section id="sec4" class="card">
  <h2><span class="num">15.3</span> 自己实现迭代器</h2>
  <p>让自定义类支持 <code>for</code>，只需实现两个方法：</p>
  <pre class="code" data-lang="python"><code>class Range:
    '''简化版 range：演示迭代器协议。'''

    def __init__(self, start, stop, step=1):
        self.current = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        return self            # 返回自身（迭代器模式）

    def __next__(self):
        if (self.step &gt; 0 and self.current &gt;= self.stop) or \\
           (self.step &lt; 0 and self.current &lt;= self.stop):
            raise StopIteration
        value = self.current
        self.current += self.step
        return value

print(list(Range(1, 5)))          # [1, 2, 3, 4]
for n in Range(5, 0, -2):
    print(n, end=" ")             # 5 3 1</code></pre>
  <p>两种实现路线，选哪个取决于"是否需要多次遍历"：</p>
  <table>
    <colgroup><col style="width:30%"><col style="width:36%"><col style="width:34%"></colgroup>
    <thead><tr><th>路线</th><th>做法</th><th>能否重复遍历</th></tr></thead>
    <tbody>
      <tr><td>容器 + 独立迭代器</td><td><code>__iter__</code> 返回一个新的迭代器对象</td><td>能（推荐）</td></tr>
      <tr><td>自身即迭代器</td><td><code>__iter__</code> 返回 <code>self</code></td><td>不能（一次性）</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="python"><code>class Playlist:
    '''容器：__iter__ 每次返回新的迭代器 → 可反复遍历。'''

    def __init__(self, songs):
        self.songs = list(songs)

    def __iter__(self):
        return iter(self.songs)      # 委托给列表的迭代器

    def __len__(self):
        return len(self.songs)

    def __getitem__(self, index):    # 顺带支持下标与切片
        return self.songs[index]

pl = Playlist(["a", "b", "c"])
print(list(pl), list(pl))            # ['a', 'b', 'c'] ['a', 'b', 'c']  可重复
print(pl[0], len(pl))                # a 3</code></pre>
</section>""",

"""<section id="sec5" class="card">
  <h2><span class="num">15.4</span> 迭代器是一次性的</h2>
  <pre class="code" data-lang="python"><code>nums = map(str, [1, 2, 3])       # map 返回迭代器（不是列表！）
print(list(nums))                # ['1', '2', '3']
print(list(nums))                # []        ← 已经耗尽

# 3.x 里这些内置函数返回的都是迭代器：map / filter / zip / enumerate / range(不是，是可迭代对象)
# 需要复用时：转成列表，或用 itertools.tee 分叉</code></pre>
  <p>判断小技巧：<code>iter(obj) is obj</code> 为 True 说明它自己就是迭代器（一次性）：</p>
  <pre class="code" data-lang="python"><code>lst = [1, 2]
print(iter(lst) is lst)                  # False  → 容器，可重复遍历

gen = (x for x in lst)
print(iter(gen) is gen)                  # True   → 迭代器，一次性</code></pre>
  <div class="warn-box"><span class="tag-pit">高频事故</span>函数参数里传入迭代器，函数内部遍历一次后，调用方再遍历就是空的。若函数要多次遍历入参，请<strong>在函数开头 <code>data = list(data)</code></strong>，或明确文档化"本函数会消耗迭代器"。</div>
</section>""",

"""<section id="sec6" class="card">
  <h2><span class="num">15.5</span> itertools 与常见坑</h2>
  <p><code>itertools</code> 是迭代器工具箱（第 27 章详述），这里先认识与"协议"最相关的几个：</p>
  <table>
    <colgroup><col style="width:26%"><col style="width:40%"><col style="width:34%"></colgroup>
    <thead><tr><th>工具</th><th>作用</th><th>典型场景</th></tr></thead>
    <tbody>
      <tr><td><code>islice(it, n)</code></td><td>取前 n 个</td><td>截断无限序列、分页预览</td></tr>
      <tr><td><code>chain(a, b)</code></td><td>串联多个迭代器</td><td>合并多份数据源</td></tr>
      <tr><td><code>count(start, step)</code></td><td>无限计数</td><td>与 <code>zip</code> 配合生成序号</td></tr>
      <tr><td><code>cycle(it)</code></td><td>无限循环</td><td>轮询、轮播（小心死循环）</td></tr>
      <tr><td><code>repeat(x, n)</code></td><td>重复 n 次</td><td>构造常量序列</td></tr>
      <tr><td><code>tee(it, n)</code></td><td>分成 n 路</td><td>需多次遍历（内部缓存）</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="python"><code>from itertools import islice, count, cycle, chain, repeat

print(list(islice(count(10, 5), 4)))        # [10, 15, 20, 25]  截断无限序列
print(list(islice(cycle("AB"), 5)))         # ['A', 'B', 'A', 'B', 'A']
print(list(chain([1, 2], "ab")))            # [1, 2, 'a', 'b']
print(list(repeat("x", 3)))                 # ['x', 'x', 'x']

# 用 count 给数据编号（比 enumerate 更灵活）
ids = count(1000)
print([(next(ids), n) for n in ["a", "b"]])  # [(1000, 'a'), (1001, 'b')]</code></pre>
  <div class="danger-box"><span class="tag-pit">常见坑</span><code>cycle</code>、<code>count</code> 是<strong>无限迭代器</strong>，直接 <code>list()</code> 会卡死——必须配 <code>islice</code> 或 <code>break</code>。另外 <code>tee</code> 之后<strong>原迭代器不要再用</strong>，否则数据会错乱。</div>
</section>""",

"""<section id="sec7" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:34%"><col style="width:66%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>两个协议</td><td>Iterable 有 <code>__iter__</code>；Iterator 还要有 <code>__next__</code></td></tr>
      <tr><td>区分</td><td>容器能反复取迭代器；迭代器只能走一趟</td></tr>
      <tr><td>for 的本质</td><td><code>iter()</code> → 反复 <code>next()</code> → 捕获 <code>StopIteration</code></td></tr>
      <tr><td>自定义</td><td>实现 <code>__iter__</code>/<code>__next__</code>；容器型应返回新迭代器</td></tr>
      <tr><td>一次性</td><td><code>iter(o) is o</code> 可判断是否一次性</td></tr>
      <tr><td>3.x 变化</td><td><code>map/filter/zip</code> 返回迭代器，不是列表</td></tr>
      <tr><td>工具</td><td><code>islice</code> 截断无限；<code>chain</code> 串联；<code>tee</code> 分叉</td></tr>
    </tbody>
  </table>
</section>""",

"""<section id="sec8" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>不运行，写出输出：<code>it = iter([1,2,3]); print(next(it), next(it)); print(list(it))</code>；并说明 <code>list(it)</code> 为什么只剩一个元素。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>实现 <code>class Paginator</code>：接收任意可迭代对象与页大小，支持 <code>for page in paginator</code> 逐页产出列表，且能被重复遍历（提示：<code>__iter__</code> 用生成器实现）。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>实现 <code>class Peekable</code>：包装任意迭代器，提供 <code>peek()</code>（偷看下一个但不消耗）与 <code>__next__()</code>，并支持 <code>__iter__</code>。用它写一个"按首字符分组"的处理函数。</div>
  <p class="note">参考答案见附录 C（规划中）。下一章：装饰器——Python 最著名的语法糖。</p>
</section>"""
]
},

# ════════════════════ 第 16 章 ════════════════════
{
"n": 16, "title": "装饰器：高阶函数与语法糖",
"file": "016_第16章_装饰器.html",
"meta": "预计 50 分钟 · 动手章 · 重点章",
"hero": "@decorator 是 Python 最出圈的符号。它看起来像魔法，其实只是「函数是一等公民 + 闭包」的必然结果。本章从零手写装饰器，讲到 wraps、带参装饰器、类装饰器与 functools 全家桶，并揭示 FastAPI 路由、pytest 夹具背后的同一套机制。",
"toc": [("sec1", "本章目标"), ("sec2", "16.1 装饰器是什么"), ("sec3", "16.2 functools.wraps 与签名"),
        ("sec4", "16.3 带参数的装饰器"), ("sec5", "16.4 类装饰器与装饰类"),
        ("sec6", "16.5 内置装饰器与实战"), ("sec7", "本章小结"), ("sec8", "本章习题")],
"sections": [
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>能从<strong>高阶函数 + 闭包</strong>推导出装饰器，手写无糖版本；</li>
    <li>理解 <code>@</code> 语法糖的等价展开式与<strong>装饰时机</strong>（定义时立即执行）；</li>
    <li>会用 <code>functools.wraps</code> 保留元信息，避免"函数名丢失"；</li>
    <li>会写<strong>带参数的装饰器</strong>（三层嵌套）与类装饰器；</li>
    <li>认识 <code>@property</code>、<code>@staticmethod</code>、<code>@classmethod</code>、<code>@lru_cache</code> 等内置装饰器。</li>
  </ul>
</section>""",

"""<section id="sec2" class="card">
  <h2><span class="num">16.1</span> 装饰器是什么</h2>
  <p>装饰器的本质是：<strong>接收一个函数，返回一个新函数</strong>。它用于"给函数统一加功能，而不改函数本身的代码"。</p>
  <pre class="code" data-lang="python"><code># 需求：给每个函数加日志，记录调用了谁

def log_call(func):                    # ① 接收函数
    def wrapper(*args, **kwargs):      # ② 新函数（闭包持有 func）
        print(f"调用 {func.__name__}，参数 {args} {kwargs}")
        result = func(*args, **kwargs)  # ③ 执行原函数
        print(f"{func.__name__} 返回 {result!r}")
        return result                   # ④ 返回原结果
    return wrapper                      # ⑤ 返回新函数

def add(a, b):
    return a + b

# 无糖写法：手动包装
logged_add = log_call(add)
print(logged_add(1, 2))
# 调用 add，参数 (1, 2) {}
# add 返回 3
# 3

# 语法糖写法（完全等价）
@log_call
def add(a, b):
    return a + b

print(add(1, 2))       # 同样输出日志与 3</code></pre>
  <p class="key-sentence"><code>@decorator</code> 就等价于 <code>func = decorator(func)</code>——它<strong>在模块加载（函数定义）时立即执行</strong>，而不是在调用时执行。</p>
  <pre class="code" data-lang="python"><code># 多个装饰器：从下往上应用（离函数最近的先执行）
@decorator_a
@decorator_b
def f():
    pass

# 等价于：f = decorator_a(decorator_b(f))

# 执行时的调用顺序：a 的 wrapper → b 的 wrapper → f</code></pre>
</section>""",

"""<section id="sec3" class="card">
  <h2><span class="num">16.2</span> functools.wraps 与签名</h2>
  <p>上例有个副作用：<code>add.__name__</code> 变成了 <code>wrapper</code>，文档字符串也丢了：</p>
  <pre class="code" data-lang="python"><code>print(add.__name__)      # wrapper   ← 元信息被"掉包"了
print(add.__doc__)       # None</code></pre>
  <p>修正方法：<code>functools.wraps</code> 把原函数的元信息复制到包装函数上：</p>
  <pre class="code" data-lang="python"><code>import functools

def log_call(func):
    @functools.wraps(func)                 # ← 关键：保留 __name__/__doc__/__annotations__
    def wrapper(*args, **kwargs):
        print(f"调用 {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_call
def add(a, b):
    '''两数相加。'''
    return a + b

print(add.__name__)      # add
print(add.__doc__)       # 两数相加。
import inspect
print(inspect.signature(add))    # (a, b)   ← 签名也保留（wraps 复制了 __wrapped__）</code></pre>
  <div class="warn-box"><span class="tag-pit">不写 wraps 的后果</span>① 日志与报错里的函数名全是 <code>wrapper</code>，排查困难；② 依赖函数签名的框架（<strong>FastAPI</strong> 的路径函数、<strong>pytest</strong> 的 fixture、<strong>click</strong> 的命令行）会拿错参数；③ <code>help()</code> 与自动文档失效。<u>写装饰器就加 wraps，这是硬性习惯。</u></div>
</section>""",

"""<section id="sec4" class="card">
  <h2><span class="num">16.3</span> 带参数的装饰器</h2>
  <p>想要 <code>@retry(times=3)</code> 这种带配置的装饰器，需要<strong>三层嵌套</strong>：</p>
  <pre class="code" data-lang="python"><code>import functools
import time

def retry(times=3, delay=0.1, exceptions=(Exception,)):
    '''外层：接收装饰器参数，返回真正的装饰器。'''
    def decorator(func):                     # 中层：接收函数
        @functools.wraps(func)
        def wrapper(*args, **kwargs):        # 内层：包装调用
            last_exc = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    print(f"第 {attempt} 次失败：{exc}")
                    time.sleep(delay)
            raise last_exc                   # 全失败：抛出最后一个异常
        return wrapper
    return decorator

@retry(times=3, delay=0.05, exceptions=(ConnectionError,))
def fetch(url):
    import random
    if random.random() &lt; 0.7:
        raise ConnectionError("网络抖动")
    return "数据"

# print(fetch("/api"))</code></pre>
  <p>等价展开帮助理解：</p>
  <pre class="code" data-lang="python"><code># @retry(times=3)
# 展开为：fetch = retry(times=3)(fetch)
#          ↑ 先调用 retry(3) 得到 decorator，再调用 decorator(fetch) 得到 wrapper</code></pre>
  <h4>可选参数的兼容写法</h4>
  <pre class="code" data-lang="python"><code>def flexible(func=None, *, times=3):
    '''既支持 @flexible，也支持 @flexible(times=5)。'''
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                try:
                    return f(*args, **kwargs)
                except Exception:
                    pass
        return wrapper
    if func is None:                 # 带参调用：返回 decorator，等下一次调用
        return decorator
    return decorator(func)           # 无参调用：直接包装</code></pre>
</section>""",

"""<section id="sec5" class="card">
  <h2><span class="num">16.4</span> 类装饰器与装饰类</h2>
  <h4>用类做装饰器（实现 <code>__call__</code>）</h4>
  <pre class="code" data-lang="python"><code>import functools

class CountCalls:
    '''类装饰器：统计函数被调用的次数（状态存在实例属性里）。'''

    def __init__(self, func):
        functools.update_wrapper(self, func)   # 类版 wraps
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):       # 让实例可被调用
        self.count += 1
        print(f"{self.func.__name__} 第 {self.count} 次调用")
        return self.func(*args, **kwargs)

@CountCalls
def greet(name):
    return f"你好 {name}"

print(greet("张三"))      # greet 第 1 次调用 / 你好 张三
print(greet("李四"))      # greet 第 2 次调用 / 你好 李四
print(greet.count)        # 2    状态可查，这点比闭包方便</code></pre>
  <h4>用函数装饰类（给类加功能）</h4>
  <pre class="code" data-lang="python"><code>def add_repr(cls):
    '''给类自动补一个 __repr__。'''
    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"{type(self).__name__}({attrs})"
    cls.__repr__ = __repr__
    return cls

@add_repr
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

print(Point(1, 2))        # Point(x=1, y=2)</code></pre>
  <p class="key-sentence">选型：<strong>无状态</strong>的包装用函数装饰器（更简洁）；<strong>需要保存状态或配置项</strong>时用类装饰器（状态在实例属性里，可查看、可重置）。第 22 章的 <code>dataclass</code> 就是一个官方的"类装饰器"。</p>
</section>""",

"""<section id="sec6" class="card">
  <h2><span class="num">16.5</span> 内置装饰器与实战</h2>
  <table>
    <colgroup><col style="width:28%"><col style="width:38%"><col style="width:34%"></colgroup>
    <thead><tr><th>装饰器</th><th>作用</th><th>说明</th></tr></thead>
    <tbody>
      <tr><td><code>@property</code></td><td>把方法变成属性</td><td>第 23 章专题</td></tr>
      <tr><td><code>@staticmethod</code></td><td>静态方法（无 self）</td><td>第 20 章</td></tr>
      <tr><td><code>@classmethod</code></td><td>类方法（收到 cls）</td><td>常用于替代构造器</td></tr>
      <tr><td><code>@functools.lru_cache</code></td><td>记忆化缓存</td><td>参数须可哈希</td></tr>
      <tr><td><code>@functools.singledispatch</code></td><td>按类型分派</td><td>单分派泛型函数</td></tr>
      <tr><td><code>@contextlib.contextmanager</code></td><td>用生成器写上下文管理器</td><td>第 25 章</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="python"><code>import functools
import time

# lru_cache：一行实现缓存（参数为可哈希对象）
@functools.lru_cache(maxsize=128)
def fib(n):
    return n if n &lt; 2 else fib(n - 1) + fib(n - 2)

print(fib(80))                       # 秒出
print(fib.cache_info())              # CacheInfo(hits=..., misses=81, maxsize=128, currsize=81)
fib.cache_clear()                    # 清空缓存

# 计时装饰器（生产可用版）
def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            print(f"[{func.__name__}] 耗时 {time.perf_counter() - t0:.4f}s")
    return wrapper

@timed
def slow():
    time.sleep(0.1)

slow()      # [slow] 耗时 0.1003s</code></pre>
  <p>装饰器在真实框架里无处不在——理解它，你就理解了这些"魔法"：</p>
  <ul>
    <li><strong>FastAPI</strong>：<code>@app.get("/users")</code> 把函数注册进路由表，并读取它的类型注解生成校验规则与 OpenAPI 文档（第 40-41 章）；</li>
    <li><strong>pytest</strong>：<code>@pytest.fixture</code> 把函数标记为可注入的依赖（第 34 章）；</li>
    <li><strong>Flask / Django</strong>：路由注册与登录校验；</li>
    <li><strong>标准库</strong>：<code>@dataclass</code>、<code>@abstractmethod</code>、<code>@overload</code>（第 24 章）。</li>
  </ul>
  <div class="warn-box"><span class="tag-pit">常见坑</span>① 装饰器在<strong>导入时</strong>执行，不要在装饰器里做耗时或依赖运行时状态的操作；② 装饰后原函数只能通过 <code>func.__wrapped__</code> 访问（<code>wraps</code> 会设置它）；③ <code>lru_cache</code> 的参数必须可哈希，列表/字典做参数会报 <code>TypeError: unhashable type</code>。</div>
</section>""",

"""<section id="sec7" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:34%"><col style="width:66%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>本质</td><td>接收函数、返回函数的高阶函数；<code>@d</code> ≡ <code>f = d(f)</code></td></tr>
      <tr><td>时机</td><td>定义时（模块导入时）立即执行，不是调用时</td></tr>
      <tr><td>多个装饰器</td><td>从下往上应用，从外往内执行</td></tr>
      <tr><td>wraps</td><td>必写：保留 <code>__name__</code>/<code>__doc__</code>/签名，框架依赖它</td></tr>
      <tr><td>带参装饰器</td><td>三层嵌套：<code>参数 → decorator → wrapper</code></td></tr>
      <tr><td>类装饰器</td><td>实现 <code>__init__</code> 收函数 + <code>__call__</code> 执行；适合有状态</td></tr>
      <tr><td>实战</td><td>FastAPI 路由、pytest fixture、<code>lru_cache</code> 全靠它</td></tr>
    </tbody>
  </table>
</section>""",

"""<section id="sec8" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>手写 <code>@uppercase</code> 装饰器：把被装饰函数返回的字符串转成大写（必须加 <code>wraps</code>），并打印 <code>greet.__name__</code> 证明元信息保留。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>实现 <code>@cache_result(ttl=60)</code>：按参数缓存结果，且缓存 60 秒后失效（提示：字典里存 <code>(结果, 时间戳)</code>），并与 <code>lru_cache</code> 对比差异。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>实现 <code>@validate_types</code>：读取函数的类型注解，在运行时校验入参类型（不匹配抛 <code>TypeError</code>），保留原签名。再 Research 一下：为什么 FastAPI 不自己实现这套校验，而是交给 Pydantic（第 42 章）？</div>
  <p class="note">参考答案见附录 C（规划中）。下一章：异常处理与 EAFP 风格。</p>
</section>"""
]
}
]

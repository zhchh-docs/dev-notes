# -*- coding: utf-8 -*-
"""第二篇 函数与进阶语法 · 第 17-19 章"""

PART_DIR = "20_第二篇_函数与进阶语法"
PART_NAME = "第二篇 函数与进阶语法"

CHAPTERS = [
# ════════════════════ 第 17 章 ════════════════════
{
"n": 17, "title": "lambda 与函数式工具",
"file": "017_第17章_lambda与函数式工具.html",
"meta": "预计 35 分钟 · 动手章",
"hero": "lambda 让「临时小函数」可以内联书写，而 map/filter/reduce/partial/operator 这些函数式工具则让数据处理更声明式。本章讲清它们的适用边界——哪些场景让代码变优雅，哪些场景会让代码变难读。",
"toc": [("sec1", "本章目标"), ("sec2", "17.1 lambda 匿名函数"), ("sec3", "17.2 map / filter / reduce"),
        ("sec4", "17.3 sorted 与 key 的艺术"), ("sec5", "17.4 functools 与 operator"),
        ("sec6", "17.5 函数式 vs 推导式"), ("sec7", "本章小结"), ("sec8", "本章习题")],
"sections": [
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>掌握 <code>lambda</code> 语法与它的三个典型用武之地；</li>
    <li>会用 <code>map</code> / <code>filter</code> / <code>reduce</code>，并知道何时改用推导式；</li>
    <li>能用 <code>sorted(key=...)</code> 做单键、多键、混合升降序排序；</li>
    <li>会用 <code>functools.partial</code> / <code>operator</code> 简化回调；</li>
    <li>理解 Python 函数式编程的<strong>边界</strong>：能用，但不极端。</li>
  </ul>
</section>""",

"""<section id="sec2" class="card">
  <h2><span class="num">17.1</span> lambda 匿名函数</h2>
  <p>语法：<code>lambda 参数: 表达式</code>。它返回一个函数对象，<strong>函数体只能是单个表达式</strong>（表达式的值即返回值）。</p>
  <pre class="code" data-lang="python"><code># 对比：普通函数 vs lambda
def square(x):
    return x ** 2

square_lambda = lambda x: x ** 2

print(square(5), square_lambda(5))     # 25 25
print(type(square_lambda))             # &lt;class 'function'&gt;</code></pre>
  <p>lambda 的三个正当用途：</p>
  <pre class="code" data-lang="python"><code># ① 作为排序/提取的 key（最常见）
students = [{"name": "张三", "score": 88}, {"name": "李四", "score": 95}]
print(sorted(students, key=lambda s: s["score"])[-1]["name"])     # 李四

# ② 作为短小的回调
pairs = [(1, "one"), (2, "two"), (3, "three")]
print(sorted(pairs, key=lambda p: p[0]))       # [(1, 'one'), (2, 'two'), (3, 'three')]

# ③ 需要表达式的地方（如 GUI/异步回调、defaultdict 工厂）
from collections import defaultdict
tree = defaultdict(lambda: {"count": 0, "children": {}})
tree["a"]["count"] += 1
print(dict(tree))          # {'a': {'count': 1, 'children': {}}}</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span>① lambda 里<strong>不能写语句</strong>（没有 <code>if/for/return/raise</code>，也没有赋值——要赋值请用 <code>:=</code>）；② 把复杂 lambda 赋给变量是反模式（PEP 8 明确反对 <code>f = lambda x: ...</code>，此时请用 <code>def</code>，因为它有名字、可写文档、能出现在 traceback 里）；③ 循环里定义 lambda 注意 late binding（第 12 章）。</div>
</section>""",

"""<section id="sec3" class="card">
  <h2><span class="num">17.2</span> map / filter / reduce</h2>
  <pre class="code" data-lang="python"><code>nums = [1, 2, 3, 4, 5]

# map：对每个元素应用函数（返回迭代器，惰性）
print(list(map(lambda x: x * 2, nums)))          # [2, 4, 6, 8, 10]
print(list(map(str, nums)))                      # ['1', '2', '3', '4', '5']

# 多个可迭代对象：并行传入，以最短的为准
print(list(map(lambda a, b: a + b, [1, 2, 3], [10, 20, 30])))   # [11, 22, 33]

# filter：保留使函数返回真的元素
print(list(filter(lambda x: x % 2 == 0, nums)))  # [2, 4]
print(list(filter(None, ["a", "", "b", None])))  # ['a', 'b']  None 表示"用真假值过滤"

# reduce：累积归约（需要从 functools 导入）
from functools import reduce
print(reduce(lambda a, b: a * b, nums))          # 120  阶乘
print(reduce(lambda a, b: a + b, nums, 100))     # 115  带初始值</code></pre>
  <table>
    <colgroup><col style="width:24%"><col style="width:38%"><col style="width:38%"></colgroup>
    <thead><tr><th>函数</th><th>等价推导式</th><th>什么时候用它</th></tr></thead>
    <tbody>
      <tr><td><code>map(f, seq)</code></td><td><code>[f(x) for x in seq]</code></td><td>f 是<strong>已有函数</strong>时（如 <code>str</code>、<code>int</code>）更简洁</td></tr>
      <tr><td><code>filter(p, seq)</code></td><td><code>[x for x in seq if p(x)]</code></td><td>同上；多数时候推导式更好读</td></tr>
      <tr><td><code>reduce(f, seq)</code></td><td>无直接等价</td><td>归约成单个值；但 <code>sum</code>/<code>max</code>/<code>any</code> 更快更清晰</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="python"><code># reduce 的替代：内置函数通常更好
from functools import reduce
nums = [1, 2, 3, 4]

print(reduce(lambda a, b: a + b, nums))    # 10
print(sum(nums))                           # 10   ← 更快、更清晰

print(reduce(lambda a, b: a if a &gt; b else b, nums))
print(max(nums))                           # 4    ← 同样

# 真正适合 reduce 的场景：没有内置对应物的自定义归约
print(reduce(lambda acc, x: acc + [x * 2], nums, []))     # [2, 4, 6, 8]</code></pre>
  <p class="key-sentence">经验法则：<strong>有现成的内置函数（sum/max/min/any/all/join）就用内置的</strong>；需要自定义变换时优先推导式；<code>map/filter</code> 只在"直接传已有函数"时更优雅。</p>
</section>""",

"""<section id="sec4" class="card">
  <h2><span class="num">17.3</span> sorted 与 key 的艺术</h2>
  <pre class="code" data-lang="python"><code>people = [
    {"name": "张三", "age": 20, "score": 88},
    {"name": "李四", "age": 18, "score": 95},
    {"name": "王五", "age": 20, "score": 95},
]

# 单键排序
print([p["name"] for p in sorted(people, key=lambda p: p["age"])])
# ['李四', '张三', '王五']

# 多键排序：key 返回元组，按元组逐项比较
print([p["name"] for p in sorted(people, key=lambda p: (p["age"], p["score"]))])
# ['李四', '张三', '王五']

# 混合升降序：数值取负即可让某一键降序
print([p["name"] for p in sorted(people, key=lambda p: (p["age"], -p["score"]))])
# ['李四', '王五', '张三']   同龄者分数高的在前

# 字符串键无法取负 → 分两步排（先次要键，再主要键，利用排序稳定性）
words = ["Banana", "apple", "cherry", "Apple"]
print(sorted(words, key=str.lower))                 # 忽略大小写
print(sorted(words, key=lambda w: (w.lower(), w)))  # 忽略大小写，同词时按原样</code></pre>
  <p>两个重要细节：</p>
  <ul>
    <li><strong>key 函数只调用一次</strong>：Python 会先对每个元素算一次 key（"装饰-排序-去装饰"），所以 key 里可以放较重的操作；</li>
    <li><strong>排序是稳定的</strong>：相等元素保持原有相对顺序，因此"多轮排序"能实现复杂排序需求。</li>
  </ul>
  <pre class="code" data-lang="python"><code># 用稳定性做"先按城市升序、再按年龄降序"
rows = [("北京", 20), ("上海", 18), ("北京", 18), ("上海", 20)]
rows.sort(key=lambda r: r[1], reverse=True)      # 先排次要键：年龄降序
rows.sort(key=lambda r: r[0])                    # 再排主要键：城市升序（稳定，保住上一步顺序）
print(rows)      # [('北京', 20), ('北京', 18), ('上海', 20), ('上海', 18)]</code></pre>
</section>""",

"""<section id="sec5" class="card">
  <h2><span class="num">17.4</span> functools 与 operator</h2>
  <pre class="code" data-lang="python"><code>from functools import partial, reduce
from operator import itemgetter, attrgetter, methodcaller, mul

# partial：冻结部分参数，生成新函数（比 lambda 更明确，且可 pickle）
def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)
print(square(5), cube(2))            # 25 8

# 实战：固定日志前缀
import logging
log_info = partial(logging.getLogger("app").info, "[api]")
# log_info("请求完成")   → 打印 [api] 请求完成

# itemgetter：按下标/键取值，比 lambda 快且支持多键
people = [{"name": "张三", "age": 20}, {"name": "李四", "age": 18}]
print(sorted(people, key=itemgetter("age"))[0]["name"])          # 李四
print([itemgetter("name", "age")(p) for p in people])            # [('张三', 20), ('李四', 18)]

# attrgetter：按属性取值（对象列表排序神器）
class User:
    def __init__(self, name, age): self.name, self.age = name, age

users = [User("张三", 20), User("李四", 18)]
print([u.name for u in sorted(users, key=attrgetter("age"))])    # ['李四', '张三']

# methodcaller：调用指定方法
print(list(map(methodcaller("upper"), ["a", "b"])))              # ['A', 'B']

# operator 模块把运算符变成函数
print(reduce(mul, [1, 2, 3, 4]))     # 24</code></pre>
  <table>
    <colgroup><col style="width:26%"><col style="width:40%"><col style="width:34%"></colgroup>
    <thead><tr><th>工具</th><th>替代的 lambda</th><th>优势</th></tr></thead>
    <tbody>
      <tr><td><code>itemgetter("k")</code></td><td><code>lambda d: d["k"]</code></td><td>更快、支持多键、可复现</td></tr>
      <tr><td><code>attrgetter("x")</code></td><td><code>lambda o: o.x</code></td><td>支持 <code>a.b.c</code> 多级</td></tr>
      <tr><td><code>methodcaller("m")</code></td><td><code>lambda o: o.m()</code></td><td>可带参数</td></tr>
      <tr><td><code>partial(f, x=1)</code></td><td><code>lambda *a: f(*a, x=1)</code></td><td>保留 <code>f.__name__</code>、可序列化</td></tr>
    </tbody>
  </table>
</section>""",

"""<section id="sec6" class="card">
  <h2><span class="num">17.5</span> 函数式 vs 推导式</h2>
  <p>同一需求的四种写法，可读性排序：</p>
  <pre class="code" data-lang="python"><code>nums = [1, 2, 3, 4, 5, 6]

# ① 循环（最啰嗦，但可扩展性最好）
result = []
for n in nums:
    if n % 2 == 0:
        result.append(n ** 2)

# ② 推导式（Python 推荐，多数场景首选）
result = [n ** 2 for n in nums if n % 2 == 0]

# ③ map + filter（函数式风格，需要 lambda 时略绕）
result = list(map(lambda n: n ** 2, filter(lambda n: n % 2 == 0, nums)))

# ④ 已有函数时的 map/filter（此时很优雅）
result = list(map(abs, filter(None, [-1, 0, 2, -3])))      # [1, 2, 3]</code></pre>
  <p>取舍建议：</p>
  <table>
    <colgroup><col style="width:34%"><col style="width:66%"></colgroup>
    <thead><tr><th>场景</th><th>推荐写法</th></tr></thead>
    <tbody>
      <tr><td>变换 + 过滤，逻辑简单</td><td>列表推导式</td></tr>
      <tr><td>只对已有函数做变换/过滤</td><td><code>map</code> / <code>filter</code></td></tr>
      <tr><td>链式多步处理、数据量大</td><td>生成器管道（第 14 章）</td></tr>
      <tr><td>需要异常处理、复杂分支</td><td>普通 for 循环</td></tr>
      <tr><td>需要维护累积状态</td><td>循环 / <code>itertools.accumulate</code></td></tr>
    </tbody>
  </table>
  <p class="key-sentence">Python 是多范式语言，但它<strong>不鼓励极端函数式</strong>：可读性优先，能一眼看懂的写法就是好写法。Guido 甚至一度想把 <code>reduce</code>、<code>lambda</code> 从 Python 3 移除（最终留下了 <code>lambda</code>）。</p>
</section>""",

"""<section id="sec7" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:34%"><col style="width:66%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>lambda</td><td><code>lambda 参: 表达式</code>；只能一行表达式；用于 key 与短回调</td></tr>
      <tr><td>反模式</td><td>把 lambda 赋给变量——请用 <code>def</code></td></tr>
      <tr><td>map / filter</td><td>返回迭代器；传已有函数时优雅</td></tr>
      <tr><td>reduce</td><td>归约；优先用 <code>sum/max/min/any/all</code></td></tr>
      <tr><td>sorted key</td><td>元组多键、数值取负降序、稳定性做多级排序</td></tr>
      <tr><td>operator</td><td><code>itemgetter</code> / <code>attrgetter</code> / <code>methodcaller</code> 替代 lambda</td></tr>
      <tr><td>partial</td><td>冻结参数；比 lambda 更明确且可序列化</td></tr>
    </tbody>
  </table>
</section>""",

"""<section id="sec8" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>用 <code>sorted(key=...)</code> 把 <code>["file10.txt", "file2.txt", "file1.txt"]</code> 按<strong>数字大小</strong>排序（提示：正则或字符串切片提取数字）。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>给定订单列表（含 <code>user_id</code>、<code>amount</code>、<code>created_at</code>），写三个函数分别求：总金额、金额最高的订单、每个用户的消费总额（用 <code>reduce</code> / <code>max</code> / 分组）。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>用 <code>partial</code> + <code>operator</code> 重写一段原本充满 lambda 的排序代码，比较两者的可读性与性能；再说明 <code>partial</code> 相比 lambda 在"可 pickling"这一点上的意义（提示：多进程传参，第 54 章）。</div>
  <p class="note">参考答案见附录 C（规划中）。下一章：异常处理与 EAFP 风格。</p>
</section>"""
]
},

# ════════════════════ 第 18 章 ════════════════════
{
"n": 18, "title": "异常处理与 EAFP 风格",
"file": "018_第18章_异常处理.html",
"meta": "预计 45 分钟 · 动手章 · 重点章",
"hero": "Python 的错误处理哲学是 EAFP——「先做了再说，出事再补救」，与 C/Java 的 LBYL「先检查再动手」截然不同。本章讲透 try/except/else/finally、异常链、自定义异常与上下文管理器，并给出「什么时候该捕获异常」的判断标准。",
"toc": [("sec1", "本章目标"), ("sec2", "18.1 异常是什么"), ("sec3", "18.2 try/except/else/finally"),
        ("sec4", "18.3 EAFP vs LBYL"), ("sec5", "18.4 自定义异常与异常链"),
        ("sec6", "18.5 该不该捕获：判断标准"), ("sec7", "本章小结"), ("sec8", "本章习题")],
"sections": [
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>读懂 traceback，分清常见异常类型；</li>
    <li>掌握 <code>try / except / else / finally</code> 四段的执行时机；</li>
    <li>理解 <strong>EAFP</strong> 风格并能在代码中应用；</li>
    <li>会定义<strong>自定义异常</strong>与异常链（<code>raise ... from</code>）；</li>
    <li>知道"该捕获什么、不该捕获什么"，避免<strong>吞噬异常</strong>这个致命习惯。</li>
  </ul>
</section>""",

"""<section id="sec2" class="card">
  <h2><span class="num">18.1</span> 异常是什么</h2>
  <p>异常是程序运行时发生的<strong>错误事件</strong>。Python 用对象表示它，不处理就沿调用栈向上传播，直到被处理或让程序崩溃并打印 traceback。</p>
  <table>
    <colgroup><col style="width:26%"><col style="width:40%"><col style="width:34%"></colgroup>
    <thead><tr><th>异常</th><th>触发场景</th><th>典型修法</th></tr></thead>
    <tbody>
      <tr><td><code>SyntaxError</code></td><td>语法写错</td><td>代码一行没跑，看箭头位置</td></tr>
      <tr><td><code>IndentationError</code></td><td>缩进不对</td><td>统一 4 空格，别混 Tab</td></tr>
      <tr><td><code>NameError</code></td><td>名字未定义</td><td>检查拼写、导入、定义顺序</td></tr>
      <tr><td><code>TypeError</code></td><td>类型不支持该操作</td><td>检查参数类型与数量</td></tr>
      <tr><td><code>ValueError</code></td><td>类型对但值不合法</td><td>校验取值范围</td></tr>
      <tr><td><code>KeyError</code> / <code>IndexError</code></td><td>键/下标不存在</td><td>用 <code>get</code>、先判长度</td></tr>
      <tr><td><code>AttributeError</code></td><td>对象没有该属性</td><td>检查对象类型、拼写</td></tr>
      <tr><td><code>ZeroDivisionError</code></td><td>除以 0</td><td>先判断分母</td></tr>
      <tr><td><code>ImportError</code></td><td>导入失败</td><td>检查安装与路径（第 19 章）</td></tr>
      <tr><td><code>StopIteration</code></td><td>迭代器耗尽</td><td>for 循环自动处理</td></tr>
    </tbody>
  </table>
  <p>继承关系：所有异常都继承自 <code>BaseException</code>，日常捕获的都继承自 <code>Exception</code>：</p>
  <pre class="code" data-lang="python"><code>BaseException
 ├── SystemExit / KeyboardInterrupt / GeneratorExit   ← 系统级，一般不捕获
 └── Exception
      ├── ArithmeticError → ZeroDivisionError
      ├── LookupError → KeyError, IndexError
      ├── TypeError, ValueError, AttributeError, NameError
      ├── OSError → FileNotFoundError, PermissionError, ConnectionError
      └── 自定义异常继承这里</code></pre>
</section>""",

"""<section id="sec3" class="card">
  <h2><span class="num">18.2</span> try / except / else / finally</h2>
  <pre class="code" data-lang="python"><code>def divide(a, b):
    try:
        result = a / b                       # ① 可能出错的代码
    except ZeroDivisionError as e:           # ② 出错了走这里
        print("除数不能为 0:", e)
        return None
    except (TypeError, ValueError) as e:     # 多个异常用元组
        print("参数类型有误:", e)
        return None
    else:
        print("计算成功")                     # ③ 没出错才执行
        return result
    finally:
        print("清理：无论如何都执行")          # ④ 一定执行（即使有 return）

print(divide(10, 2))
# 计算成功 / 清理：无论如何都执行 / 5.0
print(divide(10, 0))
# 除数不能为 0: division by zero / 清理：无论如何都执行 / None</code></pre>
  <table>
    <colgroup><col style="width:24%"><col style="width:40%"><col style="width:36%"></colgroup>
    <thead><tr><th>子句</th><th>执行时机</th><th>典型用途</th></tr></thead>
    <tbody>
      <tr><td><code>try</code></td><td>监控的代码块</td><td>可能抛异常的操作</td></tr>
      <tr><td><code>except</code></td><td>捕获指定异常</td><td>补救、转换、记录日志</td></tr>
      <tr><td><code>else</code></td><td><u>没有异常时</u></td><td>把"成功后的逻辑"与 try 分开，更清晰</td></tr>
      <tr><td><code>finally</code></td><td>无论如何（含 return/异常）</td><td>释放资源：关闭文件、连接、锁</td></tr>
    </tbody>
  </table>
  <div class="warn-box"><span class="tag-pit">常见坑</span>① <code>except</code> 顺序<strong>从子类到父类</strong>，把 <code>except Exception</code> 写在最前面会让后面的具体分支永远不执行；② <code>finally</code> 里有 <code>return</code> 会<strong>吞掉异常</strong>，千万不要这么写；③ 空的 <code>except:</code>（裸 except）会连 <code>KeyboardInterrupt</code>（Ctrl+C）都捕获。</div>
  <pre class="code" data-lang="python"><code># finally 的"吞异常"演示（反例）
def bad():
    try:
        raise ValueError("原始错误")
    finally:
        return "被 finally 的 return 覆盖"     # 原始错误消失了！

print(bad())        # 被 finally 的 return 覆盖</code></pre>
</section>""",

"""<section id="sec4" class="card">
  <h2><span class="num">18.3</span> EAFP vs LBYL</h2>
  <p>两种错误处理的哲学：</p>
  <table>
    <colgroup><col style="width:22%"><col style="width:40%"><col style="width:38%"></colgroup>
    <thead><tr><th>风格</th><th>含义</th><th>典型代码</th></tr></thead>
    <tbody>
      <tr><td><strong>LBYL</strong><br>Look Before You Leap</td><td>先检查再动手</td><td><code>if key in d: d[key]</code>（C / Java 常见）</td></tr>
      <tr><td><strong>EAFP</strong><br>Easier to Ask Forgiveness than Permission</td><td>先做，出事再补救</td><td><code>try: d[key] except KeyError: ...</code>（Python 推荐）</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="python"><code>d = {"a": 1}

# LBYL：先检查
if "b" in d:
    value = d["b"]
else:
    value = 0

# EAFP：直接试，失败再兜底（更短，且无竞态）
try:
    value = d["b"]
except KeyError:
    value = 0

# 更简洁的写法
value = d.get("b", 0)</code></pre>
  <p>为什么 Python 偏爱 EAFP？</p>
  <ol>
    <li><strong>代码更短</strong>：检查逻辑与业务逻辑分离；</li>
    <li><strong>没有竞态（race condition）</strong>：检查与操作之间状态可能已变（文件、网络尤其明显）；</li>
    <li><strong>一次成功时更快</strong>：<code>try</code> 在无异常时几乎零开销，而"每次都先检查"要付双份代价；</li>
    <li><strong>鸭子类型天然契合</strong>：不关心对象"是什么类型"，只关心它"能不能做这件事"。</li>
  </ol>
  <pre class="code" data-lang="python"><code># 鸭子类型 + EAFP：不追问"你是什么"，只管"你能不能"
def get_total(obj):
    try:
        return sum(obj)          # 列表、元组、集合、生成器都行
    except TypeError:
        return obj               # 单个数字则原样返回

print(get_total([1, 2, 3]), get_total(42))     # 6 42</code></pre>
  <p class="key-sentence">但 EAFP 不是万能的：如果"失败"是<strong>高频且可预期</strong>的正常分支（如用户输入校验），用 <code>if</code> 表达更清晰；只有"异常才是罕见情况"时用 try/except。</p>
</section>""",

"""<section id="sec5" class="card">
  <h2><span class="num">18.4</span> 自定义异常与异常链</h2>
  <pre class="code" data-lang="python"><code>class AppError(Exception):
    '''应用异常的基类：便于上层统一捕获。'''
    pass

class ValidationError(AppError):
    '''数据校验失败。'''
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

class NotFoundError(AppError):
    pass

def get_user(uid):
    if uid &lt;= 0:
        raise ValidationError("uid", "必须为正整数")
    raise NotFoundError(f"用户 {uid} 不存在")

try:
    get_user(-1)
except ValidationError as e:
    print("字段错误:", e.field, e.message)     # 字段错误: uid 必须为正整数
except AppError as e:                          # 捕获整个家族
    print("应用异常:", e)</code></pre>
  <p>为什么要自定义异常？<strong>让调用方能按"业务含义"而不是"技术类型"来捕获</strong>。所有异常都继承同一个业务基类，上层就能用一条 <code>except</code> 兜住整个模块的错误。</p>
  <h4>异常链：保留原始原因</h4>
  <pre class="code" data-lang="python"><code>def load_config(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError as e:
        # raise ... from e  → 保留 __cause__，traceback 里能看到"两层"
        raise AppError(f"配置文件缺失：{path}") from e

try:
    load_config("nope.toml")
except AppError as e:
    print("直接原因:", e)
    print("根本原因:", e.__cause__)     # [Errno 2] No such file or directory: 'nope.toml'

# raise ... from None  → 显式抑制上下文（不想暴露内部细节时）
try:
    1 / 0
except ZeroDivisionError:
    raise AppError("计算失败") from None      # 不再显示 "During handling..."</code></pre>
  <div class="note">在 <code>except</code> 块里直接 <code>raise</code> 新异常时，Python 会自动设置 <code>__context__</code>，traceback 显示"During handling of the above exception, another exception occurred"。用 <code>from</code> 能让因果关系更明确。</div>
</section>""",

"""<section id="sec6" class="card">
  <h2><span class="num">18.5</span> 该不该捕获：判断标准</h2>
  <p>三条判断标准，按顺序问自己：</p>
  <ol>
    <li><strong>我能处理它吗？</strong>（重试、降级、给默认值、转成业务异常）——能就捕获；不能就让它往上抛，交给更懂的上层；</li>
    <li><strong>我有上下文可补充吗？</strong>（哪个文件、哪个用户、哪次请求）——有就 <code>raise ... from e</code> 包装后再抛；</li>
    <li><strong>我要记录日志吗？</strong>——只在"处理掉"的那一层记录一次，避免同一个异常被打印十遍。</li>
  </ol>
  <div class="danger-box"><span class="tag-pit">头号坏习惯</span><strong>吞噬异常</strong>（swallowing）：<code>except Exception: pass</code>。这会让 bug 彻底隐身——程序继续跑，但状态已经错了，排查成本极高。至少要 <code>logging.exception(...)</code> 记录，或重新抛出。</div>
  <pre class="code" data-lang="python"><code>import logging
logger = logging.getLogger(__name__)

# 反例：静默吞掉
def load_bad(path):
    try:
        return open(path).read()
    except Exception:
        pass                      # 出错时返回 None，调用方毫不知情

# 正例一：处理 + 记录 + 明确返回值
def load_ok(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logger.warning("文件不存在，使用默认配置: %s", path)
        return "{}"
    except OSError:
        logger.exception("读取文件失败: %s", path)     # 自动带 traceback
        raise                                          # 处理不了，原样上抛

# 正例二：只在最外层兜底（Web 框架的全局异常处理器，第 43 章）
def handle_request():
    try:
        return do_work()
    except AppError as e:
        logger.error("业务异常: %s", e)
        return {"error": str(e), "code": 400}</code></pre>
  <h4>用上下文管理器自动清理</h4>
  <pre class="code" data-lang="python"><code># 不用 finally 手写关闭，用 with（第 25 章详述）
with open("data.txt", encoding="utf-8") as f:      # 异常也会自动关闭文件
    content = f.read()

# 断言：只用于"绝不该发生"的内部检查，不用于用户输入校验
def apply_discount(price, rate):
    assert 0 &lt;= rate &lt;= 1, f"折扣率非法: {rate}"    # python -O 会跳过 assert
    return price * rate</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span>① <code>assert</code> 在 <code>python -O</code> 下会被移除，<strong>不要用它校验外部输入</strong>；② <code>except Exception</code> 捕获不到 <code>KeyboardInterrupt</code> / <code>SystemExit</code>（它们继承自 <code>BaseException</code>），这正是我们想要的；③ 异常<strong>不适合做流程控制</strong>：用异常跳出深层循环会让代码难以理解。</div>
</section>""",

"""<section id="sec7" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:34%"><col style="width:66%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>异常体系</td><td>继承 <code>Exception</code>；<code>OSError</code> 家族管 IO，<code>LookupError</code> 管查找</td></tr>
      <tr><td>四段结构</td><td>try 监控 / except 补救 / else 成功 / finally 必执行</td></tr>
      <tr><td>顺序</td><td><code>except</code> 从子类到父类；<code>finally</code> 里不要 return</td></tr>
      <tr><td>EAFP</td><td>先做再补救：更短、无竞态、契合鸭子类型</td></tr>
      <tr><td>自定义异常</td><td>继承业务基类，让上层能按语义捕获</td></tr>
      <tr><td>异常链</td><td><code>raise X from e</code> 保留根因；<code>from None</code> 抑制上下文</td></tr>
      <tr><td>铁律</td><td>不吞异常；处理不了就上抛；日志只在处理层记一次</td></tr>
    </tbody>
  </table>
</section>""",

"""<section id="sec8" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>写 <code>safe_int(s, default=0)</code>：把字符串转整数，失败返回默认值（用 EAFP）；再写 <code>read_json(path)</code>：文件不存在返回 <code>{}</code>，JSON 格式错误则包装成 <code>ValidationError</code> 抛出。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>定义业务异常家族：<code>OrderError</code> → <code>OutOfStockError</code> / <code>PaymentError</code>。写 <code>place_order(...)</code>，库存不足时抛前者并保留原始原因（<code>raise ... from</code>），调用方按不同异常给出不同提示。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>写一个 <code>retry</code> 上下文管理器：用 <code>contextlib.contextmanager</code>（第 25 章）实现"最多重试 3 次、每次间隔递增、记录每次失败日志"，并说明为什么它比装饰器版本更灵活（提示：可以包裹任意代码块，而不只是单个函数）。</div>
  <p class="note">参考答案见附录 C（规划中）。下一章：模块与包——import 体系。</p>
</section>"""
]
},

# ════════════════════ 第 19 章 ════════════════════
{
"n": 19, "title": "模块与包：import 体系",
"file": "019_第19章_模块与包.html",
"meta": "预计 45 分钟 · 动手章 · 第二篇收官",
"hero": "一个 .py 文件就是一个模块，一个带 __init__.py 的目录就是一个包。本章讲清 import 的搜索路径、四种导入写法、循环导入、__name__ == \"__main__\" 的真相，以及相对导入的规则——这些是把脚本组织成工程的必修课。",
"toc": [("sec1", "本章目标"), ("sec2", "19.1 模块与包的形态"), ("sec3", "19.2 四种导入写法"),
        ("sec4", "19.3 搜索路径与 sys.path"), ("sec5", "19.4 __name__ 与 __main__"),
        ("sec6", "19.5 循环导入与相对导入"), ("sec7", "第二篇小结"), ("sec8", "本章习题")],
"sections": [
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>分清<strong>模块</strong>（一个 .py）与<strong>包</strong>（一个目录），会写 <code>__init__.py</code>；</li>
    <li>掌握四种 import 写法及其适用场景；</li>
    <li>理解 <code>sys.path</code> 的搜索顺序，能诊断 <code>ModuleNotFoundError</code>；</li>
    <li>讲清 <code>if __name__ == "__main__":</code> 的作用；</li>
    <li>能解决<strong>循环导入</strong>，会用相对导入。</li>
  </ul>
</section>""",

"""<section id="sec2" class="card">
  <h2><span class="num">19.1</span> 模块与包的形态</h2>
  <pre class="code" data-lang="text"><code>myproject/
├── main.py                  ← 入口脚本
├── utils.py                 ← 模块（一个 .py 文件）
└── package/                 ← 包（一个目录）
    ├── __init__.py          ← 包的标识（可为空）
    ├── models.py
    └── services/
        ├── __init__.py
        └── user.py          ← 子包里的模块</code></pre>
  <p>要点：</p>
  <ul>
    <li><strong>模块名 = 文件名</strong>（不含 .py）。<code>utils.py</code> 导入时写作 <code>import utils</code>；</li>
    <li><strong>包 = 含 <code>__init__.py</code> 的目录</strong>。Python 3.3+ 支持"命名空间包"（无 <code>__init__.py</code> 也能导入），但正规项目请保留它；</li>
    <li><code>__init__.py</code> 在<strong>包首次被导入时执行</strong>，常用来导出便捷接口或做初始化。</li>
  </ul>
  <pre class="code" data-lang="python"><code># package/__init__.py
'''用户相关的包。'''
from .models import User          # 相对导入：把常用名字提到包一级

__all__ = ["User", "create_user"]   # 定义 from package import * 时导出什么
__version__ = "1.0.0"

# 使用方
# from package import User        ← 不用知道 User 在哪个子模块</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span>把文件命名为 <code>json.py</code>、<code>random.py</code>、<code>email.py</code>、<code>types.py</code>、<code>test.py</code> 等<strong>标准库同名</strong>的名字，会导致"顶替标准库"的诡异报错。命名前先想想标准库里有没有同名的（第 2 章已提醒）。</div>
</section>""",

"""<section id="sec3" class="card">
  <h2><span class="num">19.2</span> 四种导入写法</h2>
  <pre class="code" data-lang="python"><code># ① 导入整个模块（推荐：命名空间清晰，不会污染当前作用域）
import os
print(os.path.join("a", "b"))

# ② 导入并起别名
import numpy as np
import pandas as pd

# ③ 从模块导入指定名字（用得多，但要注意重名）
from datetime import datetime, timedelta
print(datetime.now())

# ④ 从模块导入并起别名（解决重名、缩短长名字）
from collections import defaultdict as dd
import matplotlib.pyplot as plt</code></pre>
  <table>
    <colgroup><col style="width:30%"><col style="width:36%"><col style="width:34%"></colgroup>
    <thead><tr><th>写法</th><th>优点</th><th>注意</th></tr></thead>
    <tbody>
      <tr><td><code>import mod</code></td><td>来源清晰，无命名冲突</td><td>每次要写模块名前缀</td></tr>
      <tr><td><code>import mod as m</code></td><td>缩短长名字</td><td>约定俗成的别名要遵守（np/pd/plt）</td></tr>
      <tr><td><code>from mod import x</code></td><td>使用时更短</td><td>可能与本文件名字冲突</td></tr>
      <tr><td><code>from mod import *</code></td><td>省事</td><td><strong>禁止在生产代码里用</strong>：污染命名空间、来源不明</td></tr>
    </tbody>
  </table>
  <div class="danger-box"><span class="tag-pit">强烈建议</span>① 标准库、第三方、本地导入<strong>分三组、中间空一行</strong>（PEP 8），组内按字母序；② 不用 <code>import *</code>；③ <code>from x import y</code> 导入的是<strong>值的绑定</strong>——若模块里后来改了 <code>y</code>，你这里的 <code>y</code> 不会跟着变（想跟着变就 <code>import x</code> 再用 <code>x.y</code>）。</div>
  <pre class="code" data-lang="python"><code># 导入顺序示范（isort / ruff 会自动整理，第 36 章）
# ① 标准库
import os
import sys
from pathlib import Path

# ② 第三方
import httpx
from fastapi import FastAPI

# ③ 本地
from myproject.config import settings
from myproject.services import user_service</code></pre>
</section>""",

"""<section id="sec4" class="card">
  <h2><span class="num">19.3</span> 搜索路径与 sys.path</h2>
  <p><code>import foo</code> 时，解释器按顺序在三处找 <code>foo</code>：</p>
  <ol>
    <li><strong>内置模块</strong>（<code>sys.builtin_module_names</code>）；</li>
    <li><strong><code>sys.path</code> 列表里的目录</strong>——依次是：脚本所在目录（或当前工作目录）→ <code>PYTHONPATH</code> 环境变量 → 标准库目录 → <code>site-packages</code>（第三方包）；</li>
    <li>找不到就抛 <code>ModuleNotFoundError</code>。</li>
  </ol>
  <pre class="code" data-lang="python"><code>import sys
print(sys.path[:3])          # 前几项通常是脚本目录与标准库路径
print(sys.builtin_module_names[:5])

# 诊断"明明装了却找不到"的三板斧
import mypkg
print(mypkg.__file__)        # 实际导入的是哪个文件？（关键！）
print(sys.modules["mypkg"])  # 模块对象
print(sys.version)           # 确认解释器版本</code></pre>
  <div class="warn-box"><span class="tag-pit">高频事故</span>"我明明 <code>pip install</code> 了，运行时却 <code>ModuleNotFoundError</code>"——九成是<strong>装到了另一个解释器/环境</strong>。用 <code>python -m pip install</code> 并用同一个 <code>python</code> 运行（第 2 章）；再用 <code>print(mypkg.__file__)</code> 确认导入来源。</div>
  <p>模块被导入时会<strong>执行一遍</strong>顶层代码，并缓存到 <code>sys.modules</code>（同一个进程里只执行一次）：</p>
  <pre class="code" data-lang="python"><code># 只执行一次 → 可以用模块级变量做"单例"
# config.py
print("config 被导入")           # 多次 import 也只打印一次
settings = {"debug": True}

# main.py
import config
import config          # 第二次导入：直接用缓存，不再执行 print
print(config.settings)</code></pre>
</section>""",

"""<section id="sec5" class="card">
  <h2><span class="num">19.4</span> __name__ 与 __main__</h2>
  <p>每个模块都有一个 <code>__name__</code>：</p>
  <ul>
    <li><strong>被导入时</strong>：<code>__name__</code> 等于模块名（如 <code>"utils"</code>）；</li>
    <li><strong>直接运行时</strong>：<code>__name__</code> 等于 <code>"__main__"</code>。</li>
  </ul>
  <pre class="code" data-lang="python"><code># utils.py
def add(a, b):
    return a + b

print("模块名:", __name__)

if __name__ == "__main__":        # 只有"直接运行本文件"时才执行
    print("自检：", add(1, 2))</code></pre>
  <pre class="code" data-lang="bash"><code>$ python utils.py
模块名: __main__
自检： 3

$ python -c "import utils"
模块名: utils</code></pre>
  <p>这个约定的三个价值：</p>
  <ol>
    <li><strong>让文件既是模块又是脚本</strong>：库代码里放自检/演示；</li>
    <li><strong>防止副作用</strong>：被导入时不会自动跑测试或打印；</li>
    <li><strong>多进程必需</strong>：Windows 上 <code>multiprocessing</code> 会重新导入主模块，没有 <code>__main__</code> 守卫会导致无限递归启动子进程（第 54 章）。</li>
  </ol>
  <pre class="code" data-lang="python"><code># 推荐的脚本骨架
'''模块说明：一句话干什么。'''

import logging

logger = logging.getLogger(__name__)      # 用 __name__ 让日志带上模块名


def main():
    logging.basicConfig(level=logging.INFO)
    logger.info("开始执行")
    # ... 业务逻辑


if __name__ == "__main__":
    main()          # 入口逻辑放函数里，便于测试与复用</code></pre>
</section>""",

"""<section id="sec6" class="card">
  <h2><span class="num">19.5</span> 循环导入与相对导入</h2>
  <h4>循环导入：症状与四种解法</h4>
  <pre class="code" data-lang="python"><code># a.py
import b                    # ① 执行到这，开始导入 b
def fa(): return b.fb()

# b.py
import a                    # ② b 又导入 a，而 a 还没执行完 → 部分初始化
def fb(): return a.fa()     # ③ 可能报 AttributeError / ImportError</code></pre>
  <table>
    <colgroup><col style="width:32%"><col style="width:68%"></colgroup>
    <thead><tr><th>解法</th><th>做法</th></tr></thead>
    <tbody>
      <tr><td>① 重构（首选）</td><td>把双方都要用的代码抽到第三个模块 <code>c.py</code>，让 a、b 都依赖 c</td></tr>
      <tr><td>② 延迟导入</td><td>把 <code>import b</code> 移到函数内部，调用时才导入</td></tr>
      <tr><td>③ 改用局部引用</td><td>不改 <code>import</code>，改成 <code>from b import fb</code>（有时可行，有时只是转移问题）</td></tr>
      <tr><td>④ 依赖倒置</td><td>高层定义接口，低层实现；由入口装配（第 24 章协议与依赖注入）</td></tr>
    </tbody>
  </table>
  <p class="key-sentence">循环导入往往是<strong>设计耦合过重的信号</strong>。解法一（抽出公共模块）+ 解法四（依赖倒置）才是治本；延迟导入只是止痛药。</p>
  <h4>相对导入 vs 绝对导入</h4>
  <pre class="code" data-lang="python"><code># 包内模块（package/services/user.py）里：
from ... import config              # 相对导入：. 当前包，.. 上级包，... 上上级
from ..models import User           # 上级包的 models
from . import helpers               # 当前包里的 helpers

# 绝对导入（推荐，尤其在项目内部）
from myproject.models import User
from myproject.config import settings</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span>① 相对导入<strong>只能用在包内</strong>，直接运行一个包内脚本（<code>python package/services/user.py</code>）会报 <code>ImportError: attempted relative import with no known parent package</code>——正确做法是 <code>python -m package.services.user</code>；② 相对导入<strong>不能超出顶层包</strong>（<code>...</code> 越过项目根目录会报错）。</div>
</section>""",

"""<section id="sec7" class="card">
  <h2><span class="num">✓</span> 第二篇小结</h2>
  <p>函数与进阶语法篇（第 10-19 章）到此结束。十章的核心可以收束成五条：</p>
  <table>
    <colgroup><col style="width:26%"><col style="width:74%"></colgroup>
    <thead><tr><th>主题</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>函数（10-11）</td><td>传对象引用：重新绑定外部无感，原地修改外部有感；默认参数用 <code>None</code> 哨兵</td></tr>
      <tr><td>作用域与闭包（12）</td><td>LEGB 查找；闭包携带状态；循环里用 <code>lambda i=i:</code> 冻结</td></tr>
      <tr><td>推导式与生成器（13-15）</td><td>惰性求值省内存；迭代器一次性；<code>for</code> 靠 <code>StopIteration</code> 结束</td></tr>
      <tr><td>装饰器（16）</td><td><code>@d</code> ≡ <code>f = d(f)</code>，定义时执行；必须加 <code>functools.wraps</code></td></tr>
      <tr><td>异常与模块（18-19）</td><td>EAFP 风格、不吞异常；<code>__main__</code> 守卫防副作用</td></tr>
    </tbody>
  </table>
  <p>三条工程习惯，请在这一篇结束时固化下来：</p>
  <ol>
    <li><strong>写装饰器必加 <code>@functools.wraps</code></strong>，否则框架（FastAPI / pytest）会读错函数；</li>
    <li><strong>异常只捕获能处理的</strong>，处理不了就包装后上抛，日志只记一次；</li>
    <li><strong>脚本入口用 <code>if __name__ == "__main__": main()</code></strong>，既方便测试，也是多进程安全的前提。</li>
  </ol>
  <p class="key-sentence">第三篇《面向对象与标准库》将进入类与对象、魔法方法、dataclass、描述符、抽象基类，以及文件、pathlib、collections、datetime、logging、re 这些日常必用的标准库。</p>
</section>""",

"""<section id="sec8" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>建一个包 <code>calc/</code>（含 <code>__init__.py</code>、<code>basic.py</code>、<code>advanced.py</code>），让 <code>from calc import add, power</code> 可用；并在 <code>__init__.py</code> 里定义 <code>__all__</code> 与 <code>__version__</code>。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>构造一个循环导入的最小复现（两个模块互相 import），观察报错；然后用"抽出第三个模块"的方式重构它，并说明为什么这比"函数内延迟导入"更好。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>写一个脚本，用 <code>importlib.import_module</code> 动态加载插件目录下的所有模块（约定：每个模块暴露 <code>register()</code>），实现一个简单的插件系统；说明 <code>sys.path</code> 在这里需要如何调整。</div>
  <p class="note">参考答案见附录 C（规划中）。下一篇：第 20 章 类与实例——self 的真相。</p>
</section>"""
]
}
]

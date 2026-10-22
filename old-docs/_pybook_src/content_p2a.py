# -*- coding: utf-8 -*-
"""第二篇 函数与进阶语法 · 第 10-12 章"""

PART_DIR = "20_第二篇_函数与进阶语法"
PART_NAME = "第二篇 函数与进阶语法"

CHAPTERS = [
# ════════════════════ 第 10 章 ════════════════════
{
"n": 10, "title": "函数：定义、返回与文档字符串",
"file": "010_第10章_函数.html",
"meta": "预计 40 分钟 · 动手章",
"hero": "函数是把「能跑的代码」变成「好用的代码」的第一步。本章讲清函数定义、返回值、None 的隐含行为、类型注解与文档字符串，并第一次回答：Python 的「传参」到底传的是什么。",
"toc": [("sec1", "本章目标"), ("sec2", "10.1 定义与调用"), ("sec3", "10.2 返回值与 None"),
        ("sec4", "10.3 文档字符串与类型注解"), ("sec5", "10.4 传参：传对象引用"),
        ("sec6", "10.5 函数是一等公民"), ("sec7", "本章小结"), ("sec8", "本章习题")],
"sections": [
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>会用 <code>def</code> 定义函数，正确书写<strong>文档字符串</strong>与<strong>类型注解</strong>；</li>
    <li>理解<strong>没有 return 的函数返回 None</strong>，以及多返回值的本质；</li>
    <li>讲清 Python 的传参模型——<strong>传对象引用</strong>，而不是"传值"或"传引用"；</li>
    <li>理解<strong>函数是一等公民</strong>：能赋值、能当参数、能当返回值；</li>
    <li>会写"单一职责、名字动宾结构"的好函数。</li>
  </ul>
</section>""",

"""<section id="sec2" class="card">
  <h2><span class="num">10.1</span> 定义与调用</h2>
  <pre class="code" data-lang="python"><code>def greet(name):
    '''向指定的人问好。'''
    return f"你好，{name}！"


print(greet("张三"))       # 你好，张三！
print(greet)               # &lt;function greet at 0x...&gt;  —— 函数本身也是对象</code></pre>
  <p>语法要点：</p>
  <ul>
    <li><code>def 函数名(参数):</code> + <strong>缩进的函数体</strong>；</li>
    <li>函数必须<strong>先定义后调用</strong>（模块级代码自上而下执行）；</li>
    <li>空的 <code>()</code> 表示无参数，但调用时括号<strong>不能省</strong>——写 <code>greet</code> 只是引用函数对象，写 <code>greet()</code> 才是调用。</li>
  </ul>
  <div class="warn-box"><span class="tag-pit">常见坑</span>把 <code>greet</code>（函数对象）当 <code>greet()</code>（调用结果）用，是新手最常见的一类 bug。典型症状：打印出来是 <code>&lt;function greet at 0x...&gt;</code>，或判断 <code>if greet:</code> 永远为真。</div>
  <p>命名与长度的建议（工程经验）：</p>
  <ul>
    <li>名字用<strong>动词或动宾结构</strong>：<code>get_user</code>、<code>calc_total</code>、<code>is_valid</code>；布尔函数用 <code>is_</code> / <code>has_</code> 前缀；</li>
    <li>一个函数只做一件事；超过一屏就该考虑拆分；</li>
    <li>函数内不要去改全局变量——需要返回值就 <code>return</code>（第 12 章作用域会解释原因）。</li>
  </ul>
</section>""",

"""<section id="sec3" class="card">
  <h2><span class="num">10.2</span> 返回值与 None</h2>
  <pre class="code" data-lang="python"><code>def add(a, b):
    return a + b

def no_return(x):
    print("处理", x)          # 没有 return

print(add(1, 2))               # 3
print(no_return(1))            # 处理 1  然后打印 None</code></pre>
  <p class="key-sentence">铁律：<strong>所有函数都有返回值</strong>。没写 <code>return</code>（或写了裸 <code>return</code>）的函数，返回 <code>None</code>。</p>
  <p>由此产生的高频 bug——把"打印"当"返回"：</p>
  <pre class="code" data-lang="python"><code>def bad_sum(nums):
    print(sum(nums))            # 只打印，不返回

result = bad_sum([1, 2, 3])     # result 是 None！
print(result * 2)               # TypeError

def good_sum(nums):
    return sum(nums)            # 正确：把结果交出去</code></pre>
  <h4>多返回值：本质是元组</h4>
  <pre class="code" data-lang="python"><code>def statistics(nums):
    return min(nums), max(nums), sum(nums) / len(nums)

lo, hi, avg = statistics([1, 2, 3, 4])
print(lo, hi, avg)              # 1 4 2.5

r = statistics([1, 2, 3, 4])
print(type(r), r)               # &lt;class 'tuple'&gt; (1, 4, 2.5)</code></pre>
  <div class="note">返回 3 个以上值时，元组解包容易记错顺序。此时换成 <code>dataclass</code>（第 22 章）或 <code>NamedTuple</code>，可读性好得多。</div>
</section>""",

"""<section id="sec4" class="card">
  <h2><span class="num">10.3</span> 文档字符串与类型注解</h2>
  <pre class="code" data-lang="python"><code>def calc_discount(price: float, is_vip: bool = False) -&gt; float:
    '''计算商品折后价。

    Args:
        price: 原价，必须大于 0
        is_vip: 是否会员，会员额外 9 折

    Returns:
        折后价格，保留两位小数

    Raises:
        ValueError: price 小于等于 0 时抛出

    Example:
        &gt;&gt;&gt; calc_discount(100.0, is_vip=True)
        90.0
    '''
    if price &lt;= 0:
        raise ValueError("price 必须大于 0")
    rate = 0.9 if is_vip else 1.0
    return round(price * rate, 2)


print(calc_discount.__doc__)       # 读文档字符串
help(calc_discount)                # IDE 与 help() 都靠它</code></pre>
  <p>要点：<code>&quot;&quot;&quot;...&quot;&quot;&quot;</code> 写在函数体第一行，就是<strong>文档字符串（docstring）</strong>，它会被存进 <code>__doc__</code>，被 IDE 悬浮提示、<code>help()</code>、文档生成工具（Sphinx / MkDocs）读取。</p>
  <p>类型注解（<code>:</code> 标注参数，<code>-&gt;</code> 标注返回值）<strong>不影响运行</strong>，但有三重价值：IDE 自动补全、<code>mypy</code> 静态检查、接口自解释（第 35 章专题）。</p>
  <div class="warn-box"><span class="tag-pit">常见坑</span>写了注解不等于运行时校验！<code>def f(x: int)</code> 依然能传入字符串。要运行时校验，用 <code>pydantic</code>（第 42 章）或显式 <code>isinstance</code> 检查。</div>
</section>""",

"""<section id="sec5" class="card">
  <h2><span class="num">10.4</span> 传参：传对象引用</h2>
  <p>Python 的参数传递既不是"传值"也不是"传引用"，而是<strong>传对象引用（pass by object reference）</strong>：形参拿到的是实参所指向对象的<strong>引用的副本</strong>。</p>
  <pre class="code" data-lang="python"><code>def rebind(n):
    n = n + 1          # 把形参 n 贴到新对象上 → 外部名字不受影响

def mutate(lst):
    lst.append(99)     # 原地修改同一个对象 → 外部看得见

x = 1;  rebind(x);  print(x)       # 1
a = []; mutate(a);  print(a)       # [99]</code></pre>
  <div class="diagram">
    <svg viewBox="0 0 800 200" role="img" aria-label="传参模型示意">
      <text x="400" y="24" text-anchor="middle" font-size="14" font-weight="700" fill="#1f2e1f">传对象引用：重新绑定 vs 原地修改</text>
      <rect x="60" y="55" width="120" height="40" rx="8" fill="#f0f5e6" stroke="#3d7a4f"/><text x="120" y="80" text-anchor="middle" font-size="12.5" fill="#2d6a3f">外部 x → 1</text>
      <rect x="60" y="115" width="120" height="40" rx="8" fill="#f0f5e6" stroke="#3d7a4f"/><text x="120" y="140" text-anchor="middle" font-size="12.5" fill="#2d6a3f">形参 n → 1</text>
      <circle cx="300" cy="95" r="28" fill="#fff" stroke="#3d7a4f" stroke-width="2"/><text x="300" y="101" text-anchor="middle" font-size="14" font-weight="700" fill="#2d6a3f">1</text>
      <line x1="180" y1="75" x2="272" y2="88" stroke="#7a8a70" stroke-width="1.5"/><line x1="180" y1="135" x2="272" y2="103" stroke="#7a8a70" stroke-width="1.5"/>
      <text x="455" y="60" font-size="12" fill="#4f6348">n = n + 1：形参换贴新对象 2</text>
      <circle cx="500" cy="95" r="28" fill="#fefce8" stroke="#b45309" stroke-width="2"/><text x="500" y="101" text-anchor="middle" font-size="14" font-weight="700" fill="#b45309">2</text>
      <line x1="180" y1="130" x2="472" y2="100" stroke="#c2cfb4" stroke-width="1.5" stroke-dasharray="4 4"/>
      <text x="600" y="140" font-size="12" fill="#4f6348">外部 x 仍贴着 1</text>
      <text x="400" y="180" text-anchor="middle" font-size="12" fill="#7a8a70">可变对象（list/dict/set）原地改 → 外部可见；不可变对象只能重新绑定 → 外部不可见</text>
    </svg>
    <p class="diagram-caption">图 10-1 传参模型的两种后果（示意）</p>
  </div>
  <p class="key-sentence">一句话记忆：<strong>对形参重新赋值，外部无感；对形参所指对象原地修改，外部有感。</strong></p>
  <pre class="code" data-lang="python"><code># 想避免被函数改到：传副本
def safe_process(items):
    items = list(items)       # 复制一份再操作
    items.sort()
    return items

original = [3, 1, 2]
safe_process(original)
print(original)               # [3, 1, 2]  原列表未被动过</code></pre>
</section>""",

"""<section id="sec6" class="card">
  <h2><span class="num">10.5</span> 函数是一等公民</h2>
  <p>函数在 Python 里和整数一样是<strong>对象</strong>，因此拥有"一等公民"的四种能力：</p>
  <pre class="code" data-lang="python"><code># ① 赋值给变量
def shout(text):
    return text.upper() + "!"

speak = shout
print(speak("hello"))          # HELLO!

# ② 存进容器
handlers = [shout, str.lower, len]
print([h("Hi") for h in handlers[:2]])   # ['HI!', 'hi']

# ③ 当参数传递（回调 / 策略模式）
def apply(func, value):
    return func(value)

print(apply(shout, "python"))  # PYTHON!

# ④ 当返回值（闭包与工厂函数，第 12 章详述）
def make_multiplier(n):
    def mul(x):
        return x * n
    return mul

times3 = make_multiplier(3)
print(times3(10))              # 30</code></pre>
  <p>一等公民带来的三个日常写法：</p>
  <pre class="code" data-lang="python"><code># 用字典替代长 if-elif（"分发表"）
def handle_create(data): return "created"
def handle_update(data): return "updated"

handlers = {"create": handle_create, "update": handle_update}
print(handlers["create"]({}))          # created

# sorted 的 key 参数就是"传函数"
users = [{"name": "张三", "age": 20}, {"name": "李四", "age": 18}]
print(sorted(users, key=lambda u: u["age"])[0]["name"])   # 李四

# 函数也可有属性（少见但合法）
shout.times = 0</code></pre>
  <div class="note"><strong>常见函数属性</strong>：<code>func.__name__</code>（名字）、<code>func.__doc__</code>（文档）、<code>func.__defaults__</code>（默认参数元组，第 11 章）、<code>func.__annotations__</code>（类型注解字典）。装饰器正是靠改写这些属性来"伪装"被包装的函数（第 16 章）。</div>
</section>""",

"""<section id="sec7" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:34%"><col style="width:66%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>定义</td><td><code>def 名(参):</code> + 缩进体；调用必须带 <code>()</code></td></tr>
      <tr><td>返回值</td><td>没有 return 就返回 None；多返回值本质是元组</td></tr>
      <tr><td>print vs return</td><td>print 是给人看的，return 是把结果交给调用方</td></tr>
      <tr><td>文档与注解</td><td>docstring 进 <code>__doc__</code>；注解不校验，只服务 IDE 与 mypy</td></tr>
      <tr><td>传参模型</td><td>传对象引用：重新绑定外部无感，原地修改外部有感</td></tr>
      <tr><td>一等公民</td><td>可赋值、可入容器、可当参数、可当返回值</td></tr>
      <tr><td>好函数</td><td>动宾命名、单一职责、不依赖全局变量</td></tr>
    </tbody>
  </table>
</section>""",

"""<section id="sec8" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>写 <code>circle_area(r)</code>，带完整 docstring（Args/Returns/Raises）与类型注解，半径为负时抛 <code>ValueError</code>；然后调用 <code>help(circle_area)</code> 验证文档可见。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>写 <code>apply_all(funcs, value)</code>：依次把 value 传入函数列表，返回结果列表；再用它把 <code>[str.upper, len, str.strip]</code> 作用在 <code>"  hi  "</code> 上。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>实现 <code>make_counter()</code> 返回两个函数 <code>inc()</code> 与 <code>get()</code>，它们共享同一个计数变量（提示：闭包，第 12 章）；并解释为什么把它写成返回整数的普通函数做不到。</div>
  <p class="note">参考答案见附录 C（规划中）。下一章：参数进阶——默认参数那个著名的坑。</p>
</section>"""
]
},

# ════════════════════ 第 11 章 ════════════════════
{
"n": 11, "title": "参数进阶：默认/关键字/解包",
"file": "011_第11章_参数进阶.html",
"meta": "预计 45 分钟 · 动手章",
"hero": "Python 的参数系统非常灵活：位置参数、默认参数、*args、**kwargs、仅限关键字参数一应俱全。灵活意味着容易踩坑——尤其是那个「默认参数是可变对象」的经典陷阱，几乎每个 Python 面试都会问到。",
"toc": [("sec1", "本章目标"), ("sec2", "11.1 参数种类与顺序"), ("sec3", "11.2 默认参数的著名陷阱"),
        ("sec4", "11.3 *args 与 **kwargs"), ("sec5", "11.4 仅限位置与仅限关键字"),
        ("sec6", "11.5 解包传参与常见坑"), ("sec7", "本章小结"), ("sec8", "本章习题")],
"sections": [
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>说清五类参数（位置、默认、<code>*args</code>、仅限关键字、<code>**kwargs</code>）及其<strong>书写顺序</strong>；</li>
    <li>理解并避开<strong>可变默认参数</strong>陷阱，知道正确的 <code>None</code> 哨兵写法；</li>
    <li>会用 <code>*</code> 与 <code>**</code> 做<strong>参数解包</strong>与<strong>转发</strong>；</li>
    <li>知道 <code>/</code> 与 <code>*</code> 如何定义仅限位置 / 仅限关键字参数（3.8+）；</li>
    <li>能读懂 FastAPI、dataclass 等框架的"魔法签名"。</li>
  </ul>
</section>""",

"""<section id="sec2" class="card">
  <h2><span class="num">11.1</span> 参数种类与顺序</h2>
  <pre class="code" data-lang="python"><code>def f(pos1, pos2, default=10, *args, kw_only, kw_only2=5, **kwargs):
    print(pos1, pos2, default, args, kw_only, kw_only2, kwargs)

# 完整顺序（从左到右，不可颠倒）：
#   位置参数 → 默认参数 → *args → 仅限关键字参数 → **kwargs
f(1, 2, 3, 4, 5, kw_only=6, x=7, y=8)
# 输出：1 2 3 (4, 5) 6 5 {'x': 7, 'y': 8}</code></pre>
  <table>
    <colgroup><col style="width:24%"><col style="width:40%"><col style="width:36%"></colgroup>
    <thead><tr><th>种类</th><th>写法</th><th>特点</th></tr></thead>
    <tbody>
      <tr><td>位置参数</td><td><code>def f(a, b)</code></td><td>按位置绑定，必填</td></tr>
      <tr><td>默认参数</td><td><code>def f(a, b=1)</code></td><td>不传则用默认值；<u>必须放在位置参数之后</u></td></tr>
      <tr><td>可变位置</td><td><code>*args</code></td><td>收集多余位置参数成<strong>元组</strong></td></tr>
      <tr><td>仅限关键字</td><td><code>def f(*, a)</code></td><td>必须用 <code>a=1</code> 形式传</td></tr>
      <tr><td>可变关键字</td><td><code>**kwargs</code></td><td>收集多余关键字参数成<strong>字典</strong></td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="python"><code># 关键字参数调用：可读性的关键
def connect(host, port, timeout=5, ssl=False):
    return f"{'https' if ssl else 'http'}://{host}:{port} (timeout={timeout})"

print(connect("api.com", 443, ssl=True))
# 不用记参数顺序；尤其是布尔参数，务必写关键字形式
# 反例：connect("api.com", 443, 30, True)  ← 读代码的人不知道 True 是什么</code></pre>
  <p class="key-sentence">工程习惯：<strong>布尔与数值参数一律用关键字传</strong>。<code>create_user(name, True, False)</code> 是不可读的，<code>create_user(name, is_admin=True, send_email=False)</code> 才是人话。</p>
</section>""",

"""<section id="sec3" class="card">
  <h2><span class="num">11.2</span> 默认参数的著名陷阱</h2>
  <pre class="code" data-lang="python"><code># 危险：默认参数是"可变对象"
def add_item(item, target=[]):
    target.append(item)
    return target

print(add_item("a"))    # ['a']
print(add_item("b"))    # ['a', 'b']   ← 为什么不是 ['b']？！</code></pre>
  <p>原因：<strong>默认参数的值在函数定义时（def 执行那一刻）就被求值一次</strong>，之后所有调用共享同一个列表对象。函数对象把它存在 <code>__defaults__</code> 里：</p>
  <pre class="code" data-lang="python"><code>print(add_item.__defaults__)     # (['a', 'b'],)   ← 共享的同一个列表</code></pre>
  <p>正确写法：用 <code>None</code> 作哨兵，在函数体内创建新对象：</p>
  <pre class="code" data-lang="python"><code>def add_item(item, target=None):
    if target is None:
        target = []          # 每次调用都新建
    target.append(item)
    return target

print(add_item("a"))    # ['a']
print(add_item("b"))    # ['b']   ← 正确</code></pre>
  <div class="danger-box"><span class="tag-pit">铁律</span><strong>默认参数永远用不可变对象</strong>（<code>None</code>、数字、字符串、元组）。想表达"默认空列表/空字典/空集合"，一律写 <code>None</code> 再在函数体内构造。同理，<code>def f(t=datetime.now())</code> 也是错的——那个"当前时间"在定义时就被固定了。</div>
</section>""",

"""<section id="sec4" class="card">
  <h2><span class="num">11.3</span> *args 与 **kwargs</h2>
  <pre class="code" data-lang="python"><code>def log(level, *messages, **meta):
    print(level, messages, meta)

log("INFO", "用户登录", "ip=1.1.1.1", user="张三", retry=0)
# INFO ('用户登录', 'ip=1.1.1.1') {'user': '张三', 'retry': 0}</code></pre>
  <p>命名是约定俗成的（<code>args</code> / <code>kwargs</code> 名字可换，星号才是关键）。两个典型用途：</p>
  <h4>用途一：包装与转发（写装饰器 / 适配器时必用）</h4>
  <pre class="code" data-lang="python"><code>def timed(func):
    def wrapper(*args, **kwargs):          # 接收任意参数
        import time
        t0 = time.perf_counter()
        result = func(*args, **kwargs)     # 原样转发
        print(f"{func.__name__} 耗时 {time.perf_counter() - t0:.4f}s")
        return result
    return wrapper

@timed
def slow(n):
    return sum(range(n))

slow(1_000_000)</code></pre>
  <h4>用途二：子类调用父类、合并配置</h4>
  <pre class="code" data-lang="python"><code>def request(url, **options):
    defaults = {"timeout": 5, "retry": 3, "verify": True}
    final = {**defaults, **options}        # 用户选项覆盖默认值
    return url, final

print(request("/api", timeout=30))
# ('/api', {'timeout': 30, 'retry': 3, 'verify': True})</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span><code>**kwargs</code> 会<strong>静默吞掉拼错的参数名</strong>：<code>request("/api", timeou=30)</code> 不会报错，只是多了一个无效键。对外 API 尽量显式列出参数名，只在转发场景用 <code>**kwargs</code>。</div>
</section>""",

"""<section id="sec5" class="card">
  <h2><span class="num">11.4</span> 仅限位置与仅限关键字</h2>
  <p>Python 3.8 引入两个特殊记号来<strong>限制调用方式</strong>，库作者用它保证"改参数名不会破坏调用方"：</p>
  <pre class="code" data-lang="python"><code>def f(a, b, /, c, d, *, e, f_):
    print(a, b, c, d, e, f_)

# a, b：仅限位置（/ 左边的不能用关键字传）
# c, d：位置或关键字都行
# e, f_：仅限关键字（* 右边的必须写名字）

f(1, 2, 3, 4, e=5, f_=6)          # 正常
# f(a=1, 2, 3, 4, e=5, f_=6)      # TypeError：a 不允许关键字

# 标准库里的真实例子
print(len(obj="abc"))             # TypeError：len 的参数是仅限位置
print(sorted([3, 1], key=None, reverse=True))   # sorted 的 key/reverse 是仅限关键字</code></pre>
  <p>为什么要有这个设计？</p>
  <ul>
    <li><strong>仅限位置（<code>/</code>）</strong>：参数名只是实现细节，将来改名不影响调用方——<code>len(obj)</code> 不会因为内部参数改名而崩；</li>
    <li><strong>仅限关键字（<code>*</code>）</strong>：强制调用方写清楚含义，避免 <code>f(True, False)</code> 这种天书；同时让"同名位置参数"成为可能。</li>
  </ul>
  <div class="note">典型应用：<code>dict.get(key, default)</code>、<code>dataclass</code> 的 <code>field(*, default=...)</code>、FastAPI 的路径参数与查询参数区分（第 41 章）。</div>
</section>""",

"""<section id="sec6" class="card">
  <h2><span class="num">11.5</span> 解包传参与常见坑</h2>
  <p>调用时用 <code>*</code> / <code>**</code> 可以把序列/字典<strong>拆开</strong>传给函数：</p>
  <pre class="code" data-lang="python"><code>def point3d(x, y, z):
    return f"({x}, {y}, {z})"

coords = (1, 2, 3)
print(point3d(*coords))               # (1, 2, 3)    序列 → 位置参数

params = {"x": 10, "y": 20, "z": 30}
print(point3d(**params))              # (10, 20, 30) 字典 → 关键字参数

# 混合使用
print(point3d(0, **{"y": 5, "z": 6})) # (0, 5, 6)

# 合并字典（3.5+）
a = {"timeout": 5}; b = {"retry": 3}
print({**a, **b})                     # {'timeout': 5, 'retry': 3}

# 函数定义里也能用解包：拆包赋值
first, *middle, last = [1, 2, 3, 4, 5]
print(first, middle, last)            # 1 [2, 3, 4] 5</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span>① <code>**</code> 解包的字典<strong>键必须是字符串</strong>且与形参名匹配，否则 TypeError；② <code>*</code> 解包后参数个数必须恰好匹配；③ 同一个位置参数既用位置又用关键字传 → <code>TypeError: got multiple values for argument</code>。</div>
  <pre class="code" data-lang="python"><code># 典型错误
# point3d(1, x=1, y=2, z=3)   → TypeError: multiple values for argument 'x'

# 实用技巧：批量构造配置再一次性传入
config = {"host": "db.local", "port": 5432, "user": "app"}
def connect(host, port, user, password=""):
    return f"连接 {user}@{host}:{port}"

print(connect(**config))              # 键与形参名一一对应</code></pre>
</section>""",

"""<section id="sec7" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:34%"><col style="width:66%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>书写顺序</td><td>位置 → 默认 → <code>*args</code> → 仅限关键字 → <code>**kwargs</code></td></tr>
      <tr><td>默认参数陷阱</td><td>默认值在 def 时求值一次；可变默认值用 <code>None</code> 哨兵</td></tr>
      <tr><td>*args / **kwargs</td><td>收集成元组/字典；主要用于转发与配置合并</td></tr>
      <tr><td>仅限位置 <code>/</code></td><td>参数名是内部细节，改名不影响调用方</td></tr>
      <tr><td>仅限关键字 <code>*</code></td><td>强制写清名字，布尔参数必备</td></tr>
      <tr><td>解包传参</td><td><code>f(*seq)</code> / <code>f(**dict)</code>；键必须是字符串</td></tr>
      <tr><td>工程习惯</td><td>布尔与数值参数一律关键字传，可读性第一</td></tr>
    </tbody>
  </table>
</section>""",

"""<section id="sec8" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>指出下面定义的错误并改正：<code>def f(a=1, b): pass</code>、<code>def g(*args, a): pass</code>、<code>def h(**kwargs, *args): pass</code>。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>写 <code>retry(func, *args, times=3, delay=0.1, **kwargs)</code>：调用 func 失败（抛异常）时重试，全部失败则抛出最后一个异常；用 <code>*args/**kwargs</code> 转发参数。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>实现一个 <code>cached(func)</code> 装饰器：用字典缓存已计算过的参数组合（键用 <code>(args, tuple(sorted(kwargs.items())))</code>），并说明它对不可哈希参数会怎样失败（提示：第 16 章 <code>functools.lru_cache</code> 的答案）。</div>
  <p class="note">参考答案见附录 C（规划中）。下一章：作用域与闭包——LEGB 规则。</p>
</section>"""
]
},

# ════════════════════ 第 12 章 ════════════════════
{
"n": 12, "title": "作用域与闭包：LEGB 规则",
"file": "012_第12章_作用域与闭包.html",
"meta": "预计 45 分钟 · 动手章",
"hero": "变量到底在哪一层被找到？为什么函数里改不了外面的变量？为什么循环里定义的三个函数打印出同一个值？LEGB 规则加上闭包与 late binding，把这几个「Python 玄学」一次性讲清楚。",
"toc": [("sec1", "本章目标"), ("sec2", "12.1 四种作用域与 LEGB"), ("sec3", "12.2 global 与 nonlocal"),
        ("sec4", "12.3 闭包：带着环境跑的函数"), ("sec5", "12.4 late binding 陷阱"),
        ("sec6", "12.5 闭包的工程用法"), ("sec7", "本章小结"), ("sec8", "本章习题")],
"sections": [
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>掌握 <strong>LEGB</strong> 查找顺序，能判断任意一行代码里名字指向谁；</li>
    <li>会用 <code>global</code> 与 <code>nonlocal</code>（并知道它们该少用）；</li>
    <li>理解<strong>闭包</strong>三要素与 <code>__closure__</code> 的本质；</li>
    <li>避开<strong>循环中创建闭包</strong>的经典 late binding 陷阱；</li>
    <li>能用闭包实现计数器、缓存、参数化装饰器等工程结构。</li>
  </ul>
</section>""",

"""<section id="sec2" class="card">
  <h2><span class="num">12.1</span> 四种作用域与 LEGB</h2>
  <p>Python 查找一个名字时，按 <strong>L → E → G → B</strong> 的顺序找，找到即停：</p>
  <table>
    <colgroup><col style="width:14%"><col style="width:26%"><col style="width:60%"></colgroup>
    <thead><tr><th>字母</th><th>作用域</th><th>说明</th></tr></thead>
    <tbody>
      <tr><td><strong>L</strong>ocal</td><td>局部作用域</td><td>函数内部（含参数）</td></tr>
      <tr><td><strong>E</strong>nclosing</td><td>外层函数作用域</td><td>嵌套函数的外层函数（闭包的关键）</td></tr>
      <tr><td><strong>G</strong>lobal</td><td>全局作用域</td><td>模块顶层，整个 .py 文件</td></tr>
      <tr><td><strong>B</strong>uilt-in</td><td>内置作用域</td><td><code>len</code>、<code>print</code>、<code>sum</code> 等内置名字</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="python"><code>x = "global x"          # G：全局

def outer():
    x = "enclosing x"   # E：外层函数
    def inner():
        x = "local x"   # L：局部
        print(x)        # local x

    inner()
    print(x)            # enclosing x

outer()
print(x)                # global x

def use_builtin():
    print(len([1, 2]))  # B：内置作用域里的 len</code></pre>
  <p>关键规则：<strong>赋值决定作用域</strong>。在函数内对某名字赋值，Python 就在编译期把它<strong>整个函数内</strong>都视为局部变量：</p>
  <pre class="code" data-lang="python"><code>count = 0

def bad():
    print(count)     # UnboundLocalError！
    count = 1        # 这一行让 count 成为整个函数的局部变量

# 正确做法：不依赖外部可变状态，用参数与返回值
def good(start):
    return start + 1

count = good(count)</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span><code>UnboundLocalError</code> 的典型成因：函数里先读后写同一个全局名字。错误信息是"local variable 'x' referenced before assignment"，意思是"你后面赋值了，所以前面那次读取也算局部的"。</div>
</section>""",

"""<section id="sec3" class="card">
  <h2><span class="num">12.2</span> global 与 nonlocal</h2>
  <pre class="code" data-lang="python"><code>counter = 0

def bump():
    global counter      # 声明：我要改的是全局那个 counter
    counter += 1

bump(); bump()
print(counter)          # 2</code></pre>
  <p><code>nonlocal</code> 用于<strong>嵌套函数里修改外层函数的变量</strong>（不能用于全局）：</p>
  <pre class="code" data-lang="python"><code>def make_counter():
    n = 0               # 外层函数的变量
    def inc():
        nonlocal n      # 声明：改的是外层那个 n
        n += 1
        return n
    def get():
        return n        # 只读不需要 nonlocal
    return inc, get

inc, get = make_counter()
print(inc(), inc(), get())    # 1 2 2</code></pre>
  <table>
    <colgroup><col style="width:22%"><col style="width:40%"><col style="width:38%"></colgroup>
    <thead><tr><th>关键字</th><th>作用</th><th>建议</th></tr></thead>
    <tbody>
      <tr><td><code>global</code></td><td>声明修改模块级变量</td><td>少用；全局可变状态是 bug 温床</td></tr>
      <tr><td><code>nonlocal</code></td><td>声明修改外层函数变量</td><td>闭包计数器等场景合理</td></tr>
    </tbody>
  </table>
  <p class="key-sentence">工程建议：<strong>能不用 <code>global</code> 就不用</strong>。需要共享状态时，优先用类（第 20 章）、<code>dataclass</code>（第 22 章）或显式传参返回，它们的可测性远好于全局变量。</p>
  <div class="note">注意区分：<strong>读取</strong>外层变量不需要任何声明（闭包天然可读）；只有<strong>重新绑定</strong>（<code>n = n + 1</code>）才需要 <code>nonlocal</code> / <code>global</code>。而"原地修改可变对象"（<code>lst.append(x)</code>）既不需要声明也确实生效。</div>
</section>""",

"""<section id="sec4" class="card">
  <h2><span class="num">12.3</span> 闭包：带着环境跑的函数</h2>
  <p><strong>闭包 = 函数 + 它引用的外层变量</strong>。当内层函数引用了外层函数的变量，并且外层函数返回了这个内层函数，那个"被引用的变量"不会随外层函数结束而消失。</p>
  <pre class="code" data-lang="python"><code>def make_multiplier(n):
    def mul(x):
        return x * n        # 引用了外层变量 n
    return mul              # 返回内层函数（注意：没有括号）

times3 = make_multiplier(3)
times10 = make_multiplier(10)

print(times3(5), times10(5))          # 15 50
print(times3.__closure__[0].cell_contents)   # 3   ← 被"关"起来的变量
print(times3.__code__.co_freevars)    # ('n',)  ← 自由变量的名字</code></pre>
  <p>闭包三要素（缺一不可）：</p>
  <ol>
    <li>有<strong>嵌套函数</strong>（函数里定义函数）；</li>
    <li>内层函数<strong>引用了外层作用域的变量</strong>（不是全局、不是自己的局部）；</li>
    <li>外层函数<strong>返回（或以其他方式传出）内层函数</strong>。</li>
  </ol>
  <div class="diagram">
    <svg viewBox="0 0 800 170" role="img" aria-label="闭包结构示意">
      <text x="400" y="24" text-anchor="middle" font-size="14" font-weight="700" fill="#1f2e1f">闭包：函数对象 + 引用的外层变量（cell）</text>
      <rect x="60" y="52" width="230" height="90" rx="10" fill="#f0f5e6" stroke="#3d7a4f"/>
      <text x="175" y="76" text-anchor="middle" font-size="12.5" font-weight="700" fill="#2d6a3f">外层 make_multiplier(3)</text>
      <text x="175" y="100" text-anchor="middle" font-size="11.5" fill="#4f6348">局部变量 n = 3</text>
      <text x="175" y="122" text-anchor="middle" font-size="11.5" fill="#4f6348">返回后本该销毁，但被引用着</text>
      <rect x="400" y="52" width="200" height="90" rx="10" fill="#fefce8" stroke="#b45309"/>
      <text x="500" y="76" text-anchor="middle" font-size="12.5" font-weight="700" fill="#b45309">返回的函数 mul</text>
      <text x="500" y="100" text-anchor="middle" font-size="11.5" fill="#4f6348">__closure__ → cell(n=3)</text>
      <text x="500" y="122" text-anchor="middle" font-size="11.5" fill="#4f6348">每次调用都读同一个 cell</text>
      <line x1="290" y1="97" x2="400" y2="97" stroke="#7a8a70" stroke-width="1.5"/>
      <text x="345" y="88" font-size="11" fill="#7a8a70">引用</text>
      <text x="660" y="97" font-size="12" fill="#4f6348">times3(5) → 15</text>
      <text x="400" y="162" text-anchor="middle" font-size="12" fill="#7a8a70">闭包让"函数携带状态"，第 16 章的装饰器正是靠它实现</text>
    </svg>
    <p class="diagram-caption">图 12-1 闭包 = 函数 + 自由变量（示意）</p>
  </div>
</section>""",

"""<section id="sec5" class="card">
  <h2><span class="num">12.4</span> late binding 陷阱</h2>
  <pre class="code" data-lang="python"><code># 期望：[0, 2, 4]（0*2, 1*2, 2*2）；实际：？
funcs = []
for i in range(3):
    funcs.append(lambda: i * 2)

print([f() for f in funcs])     # [4, 4, 4]   ← 全是最后一个 i！</code></pre>
  <p>原因：<strong>闭包捕获的是变量本身，不是它当时的值</strong>（late binding / 迟绑定）。循环结束后 <code>i</code> 等于 2，三个 lambda 读到的都是同一个 <code>i</code>。</p>
  <p>两种修法：</p>
  <pre class="code" data-lang="python"><code># 修法一：用默认参数"冻结"当前值（最常用）
funcs = [lambda i=i: i * 2 for i in range(3)]
print([f() for f in funcs])     # [0, 2, 4]

# 修法二：再包一层函数，把值变成新作用域的局部变量
def make_func(n):
    return lambda: n * 2

funcs = [make_func(i) for i in range(3)]
print([f() for f in funcs])     # [0, 2, 4]</code></pre>
  <p>这个陷阱在真实场景里频繁出现——回调、事件绑定、任务列表：</p>
  <pre class="code" data-lang="python"><code># 错误：三个按钮点击后都打印 2
buttons = []
for idx in range(3):
    buttons.append(lambda: print("点击了按钮", idx))

# 正确：用默认参数捕获
buttons = []
for idx in range(3):
    buttons.append(lambda idx=idx: print("点击了按钮", idx))</code></pre>
  <div class="warn-box"><span class="tag-pit">高频事故</span>只要看到"<strong>循环里定义 lambda / 闭包，且闭包里用了循环变量</strong>"，就要立刻警觉：十有八九是 late binding bug。GUI 回调、异步任务、测试用例参数化是三大灾区。</div>
</section>""",

"""<section id="sec6" class="card">
  <h2><span class="num">12.5</span> 闭包的工程用法</h2>
  <h4>① 简单的记忆化缓存</h4>
  <pre class="code" data-lang="python"><code>def memoize(func):
    cache = {}                       # 外层变量，被内层函数持有
    def wrapper(n):
        if n not in cache:
            cache[n] = func(n)       # 只读引用 cache，无需 nonlocal
        return cache[n]
    return wrapper

@memoize
def fib(n):
    return n if n &lt; 2 else fib(n - 1) + fib(n - 2)

print(fib(50))                       # 秒出（无缓存会跑到天荒地老）</code></pre>
  <h4>② 参数化的函数工厂</h4>
  <pre class="code" data-lang="python"><code>def greater_than(threshold):
    def check(value):
        return value &gt; threshold
    return check

is_adult = greater_than(18)
is_heat_wave = greater_than(35)

print(is_adult(20), is_heat_wave(20))     # True False

# 与内置工具搭配：sorted 的 key 也能"工厂化"
students = [("张三", 88), ("李四", 95), ("王五", 70)]
print(sorted(students, key=lambda s: s[1])[0])       # ('王五', 70)</code></pre>
  <h4>③ 用闭包替代小类</h4>
  <pre class="code" data-lang="python"><code>def make_rate_limiter(max_calls, period):
    import time
    calls = []
    def allow():
        now = time.time()
        calls[:] = [t for t in calls if now - t &lt; period]   # 原地修改，无需 nonlocal
        if len(calls) &gt;= max_calls:
            return False
        calls.append(now)
        return True
    return allow

allow = make_rate_limiter(3, 60)
print([allow() for _ in range(4)])   # [True, True, True, False]</code></pre>
  <p class="key-sentence">闭包 vs 类：只有<strong>一个行为</strong>时用闭包（轻量、无需 <code>self</code>）；有<strong>多个行为共享状态</strong>时用类。第 16 章的装饰器与第 43 章的依赖注入，本质都是闭包的应用。</p>
</section>""",

"""<section id="sec7" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:34%"><col style="width:66%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>LEGB</td><td>Local → Enclosing → Global → Built-in，找到即停</td></tr>
      <tr><td>赋值决定作用域</td><td>函数内赋值 ⇒ 整个函数视为局部，先读会 UnboundLocalError</td></tr>
      <tr><td>global / nonlocal</td><td>改全局用 global，改外层函数变量用 nonlocal；都该少用</td></tr>
      <tr><td>闭包三要素</td><td>嵌套 + 引用外层变量 + 外层返回内层</td></tr>
      <tr><td>只读 vs 重绑</td><td>读不需要声明；原地改 list 也不需要；只有 <code>n = ...</code> 需要</td></tr>
      <tr><td>late binding</td><td>闭包捕获变量不是值；循环里用 <code>lambda i=i:</code> 冻结</td></tr>
      <tr><td>工程定位</td><td>闭包 = 携带状态的函数；装饰器的基石</td></tr>
    </tbody>
  </table>
</section>""",

"""<section id="sec8" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>说出下面代码的输出并解释：<code>x = 1</code>；<code>def f(): print(x)</code>；<code>def g(): x = 2; print(x)</code>；<code>def h(): print(x); x = 2</code>。哪个会报错？</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>用闭包实现 <code>make_averager()</code>：不断接收新数值，返回"到目前为止的平均值"（用 <code>nonlocal</code> 维护总和与个数）。再写一个不用 <code>nonlocal</code>、只用原地修改列表的版本，比较两者可读性。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>写 <code>make_validator(*checks)</code>：接收若干校验函数（如 <code>lambda s: len(s) &gt;= 6</code>），返回一个新函数，它对所有 check 依次执行并在首个失败处返回 <code>(False, 第几个失败)</code>。用它校验密码强度，并说明闭包在这里保存了什么状态。</div>
  <p class="note">参考答案见附录 C（规划中）。下一章：推导式——把循环压缩成一行。</p>
</section>"""
]
}
]

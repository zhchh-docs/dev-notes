# -*- coding: utf-8 -*-
"""第三篇 面向对象与标准库 · 第 20-22 章"""

PART_DIR = "30_第三篇_面向对象与标准库"
PART_NAME = "第三篇 面向对象与标准库"

CHAPTERS = [
# ════════════════════ 第 20 章 ════════════════════
{
"n": 20, "title": "类与实例：self 的真相",
"file": "020_第20章_类与实例.html",
"meta": "预计 45 分钟 · 动手章",
"hero": "self 到底是什么？为什么方法第一个参数必须写它？类属性与实例属性有何不同？本章从「类也是对象」这个事实出发，把实例创建、属性查找、实例/静态/类方法讲透，并给出「什么时候该用类」的判断标准。",
"toc": [("sec1", "本章目标"), ("sec2", "20.1 类与实例：蓝图与房子"), ("sec3", "20.2 self 的真相"),
        ("sec4", "20.3 类属性 vs 实例属性"), ("sec5", "20.4 三种方法：实例 / 类 / 静态"),
        ("sec6", "20.5 __init__ 与初始化全家桶"), ("sec7", "本章小结"), ("sec8", "本章习题")],
"sections": [
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>理解<strong>类也是对象</strong>，实例只是"按类这个模板造出来的东西"；</li>
    <li>彻底理解 <code>self</code>：它不是关键字，只是<strong>约定俗成的第一个参数名</strong>；</li>
    <li>分清<strong>类属性</strong>与<strong>实例属性</strong>，避开"类属性是可变对象"的共享陷阱；</li>
    <li>会用<strong>实例方法 / 类方法 / 静态方法</strong>并知道各自用途；</li>
    <li>掌握 <code>__init__</code>、<code>__new__</code>、<code>__slots__</code> 的作用与取舍。</li>
  </ul>
</section>""",

"""<section id="sec2" class="card">
  <h2><span class="num">20.1</span> 类与实例：蓝图与房子</h2>
  <pre class="code" data-lang="python"><code>class User:
    """用户。"""

    def __init__(self, name, age):
        self.name = name          # 实例属性
        self.age = age

    def greet(self):              # 实例方法
        return f"我是{self.name}，今年{self.age}岁"


u1 = User("张三", 20)              # 造一个实例
u2 = User("李四", 18)

print(u1.greet())                 # 我是张三，今年20岁
print(type(u1), isinstance(u1, User))   # &lt;class '__main__.User'&gt; True
print(u1 is u2)                   # False  两个独立实例</code></pre>
  <p>关键认知：<strong>类本身也是对象</strong>——它是 <code>type</code> 的实例，可以有属性、可以当参数传、可以动态修改：</p>
  <pre class="code" data-lang="python"><code>print(type(User))        # &lt;class 'type'&gt;   ← 类的类是 type
print(User.__name__)     # 'User'
print(User.greet)        # &lt;function User.greet at 0x...&gt;

# 等价调用：实例方法其实是"把实例作为第一个参数传进去"
print(User.greet(u1))    # 我是张三，今年20岁
print(u1.greet())        # 完全等价！这就是 self 的来源</code></pre>
  <p class="key-sentence">一句话：<code>u1.greet()</code> 就是 <code>User.greet(u1)</code> 的语法糖。<strong>实例方法的第一个参数是"调用它的那个实例"</strong>，Python 只是自动帮你填了它。</p>
</section>""",

"""<section id="sec3" class="card">
  <h2><span class="num">20.2</span> self 的真相</h2>
  <ol>
    <li><code>self</code> <strong>不是关键字</strong>，只是一个约定名。写成 <code>this</code> 也能运行，但会被所有 Python 程序员讨厌；</li>
    <li>它代表<strong>当前实例</strong>，用于访问该实例的属性与其他方法；</li>
    <li>调用 <code>u.greet()</code> 时，Python 自动传入 <code>u</code> 作为 <code>self</code>；</li>
    <li>定义方法时<strong>必须显式写出</strong>它，这与 Java/C++ 的隐式 <code>this</code> 不同——这是 Python "显式优于隐式"的体现。</li>
  </ol>
  <pre class="code" data-lang="python"><code>class Counter:
    def __init__(self):
        self.value = 0            # 通过 self 挂载实例属性

    def inc(self, step=1):
        self.value += step        # 通过 self 读写
        return self.value         # 返回更新后的值（支持链式）

    def reset(self):
        self.value = 0
        return self               # 返回 self 以支持链式调用

c = Counter()
print(c.inc(), c.inc(5))          # 1 6
c.reset().inc(2)
print(c.value)                    # 2</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span>① 定义方法时忘了写 <code>self</code> → 调用时报 <code>TypeError: greet() takes 0 positional arguments but 1 was given</code>；② 在方法里写 <code>name = "x"</code> 而不写 <code>self.name</code>，只是创建了一个<strong>局部变量</strong>，方法结束就消失。</div>
  <pre class="code" data-lang="python"><code># 验证：属性存在实例的 __dict__ 里
c = Counter(); c.inc(3)
print(c.__dict__)        # {'value': 3}
c.extra = "动态加属性"    # Python 默认允许（可用 __slots__ 禁止）
print(c.__dict__)        # {'value': 3, 'extra': '动态加属性'}</code></pre>
</section>""",

"""<section id="sec4" class="card">
  <h2><span class="num">20.3</span> 类属性 vs 实例属性</h2>
  <pre class="code" data-lang="python"><code>class Dog:
    species = "Canis lupus"       # 类属性：所有实例共享
    count = 0                     # 常用于统计

    def __init__(self, name):
        self.name = name          # 实例属性：每个实例独有
        Dog.count += 1            # 通过类名修改类属性


a, b = Dog("小黑"), Dog("小白")
print(a.name, b.name)             # 小黑 小白
print(a.species, b.species)       # Canis lupus Canis lupus
print(Dog.count)                  # 2</code></pre>
  <p>属性查找顺序：<strong>先实例 <code>__dict__</code>，再类 <code>__dict__</code>，再父类</strong>（第 21 章的 MRO）。给实例赋同名属性只会"遮蔽"类属性，不会改类属性：</p>
  <pre class="code" data-lang="python"><code>a.species = "自定义"              # 只给 a 加了实例属性，遮蔽了类属性
print(a.species)                  # 自定义
print(b.species, Dog.species)     # Canis lupus Canis lupus   ← 没被改</code></pre>
  <div class="danger-box"><span class="tag-pit">头号陷阱</span><strong>类属性是可变对象时被所有实例共享</strong>——等价于"默认参数是可变对象"的翻版：</div>
  <pre class="code" data-lang="python"><code>class BadBucket:
    items = []                    # 所有实例共享同一个列表！

    def add(self, x):
        self.items.append(x)

b1, b2 = BadBucket(), BadBucket()
b1.add("a")
print(b2.items)                   # ['a']   ← b2 也有！

# 正确：在 __init__ 里创建实例属性
class GoodBucket:
    def __init__(self):
        self.items = []

b1, b2 = GoodBucket(), GoodBucket()
b1.items.append("a")
print(b2.items)                   # []     ← 互不影响</code></pre>
</section>""",

"""<section id="sec5" class="card">
  <h2><span class="num">20.4</span> 三种方法：实例 / 类 / 静态</h2>
  <table>
    <colgroup><col style="width:22%"><col style="width:30%"><col style="width:48%"></colgroup>
    <thead><tr><th>类型</th><th>首个参数</th><th>用途</th></tr></thead>
    <tbody>
      <tr><td>实例方法</td><td><code>self</code>（实例）</td><td>读写实例状态（最常见）</td></tr>
      <tr><td>类方法 <code>@classmethod</code></td><td><code>cls</code>（类）</td><td>替代构造器、操作类属性、工厂方法</td></tr>
      <tr><td>静态方法 <code>@staticmethod</code></td><td>无</td><td>与类相关但不依赖实例/类的工具函数</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="python"><code>class DateUtil:
    """日期工具：演示三种方法。"""

    default_format = "%Y-%m-%d"          # 类属性

    def __init__(self, year, month, day):
        self.year, self.month, self.day = year, month, day

    # ① 实例方法：操作实例数据
    def iso(self):
        return f"{self.year:04d}-{self.month:02d}-{self.day:02d}"

    # ② 类方法：替代构造器（"从字符串创建"）
    @classmethod
    def from_string(cls, text):
        y, m, d = map(int, text.split("-"))
        return cls(y, m, d)              # 用 cls 而不是硬编码类名 → 子类友好

    # ③ 类方法：修改类级别配置
    @classmethod
    def set_format(cls, fmt):
        cls.default_format = fmt

    # ④ 静态方法：纯工具函数，不碰实例也不碰类
    @staticmethod
    def is_leap(year):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


d = DateUtil.from_string("2026-10-19")   # 工厂方法
print(d.iso(), DateUtil.is_leap(2024))   # 2026-10-19 True</code></pre>
  <p class="key-sentence">选型口诀：<strong>用得到实例 → 实例方法；用得到类（尤其是构造实例）→ 类方法；两者都不用 → 静态方法</strong>（而都不用时，往往说明它该是个模块级函数）。</p>
  <div class="note"><strong>类方法优于硬编码类名</strong>：<code>cls(...)</code> 让子类继承工厂方法时自动造出子类实例；写成 <code>DateUtil(...)</code> 则子类永远返回父类实例。</div>
</section>""",

"""<section id="sec6" class="card">
  <h2><span class="num">20.5</span> __init__ 与初始化全家桶</h2>
  <table>
    <colgroup><col style="width:26%"><col style="width:40%"><col style="width:34%"></colgroup>
    <thead><tr><th>方法</th><th>时机</th><th>说明</th></tr></thead>
    <tbody>
      <tr><td><code>__new__(cls, ...)</code></td><td>创建实例（最先）</td><td> rarely 需要；单例、不可变子类定制</td></tr>
      <tr><td><code>__init__(self, ...)</code></td><td>初始化实例</td><td>最常用；<u>不能有返回值</u></td></tr>
      <tr><td><code>__slots__</code></td><td>类级声明</td><td>固定属性集合，省内存、禁止动态加属性</td></tr>
      <tr><td><code>__post_init__</code></td><td>dataclass 专用</td><td>第 22 章</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="python"><code>class Connection:
    """演示 __new__ 的单例用法（日常很少需要）。"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, dsn):
        self.dsn = dsn

a, b = Connection("db://a"), Connection("db://b")
print(a is b, a.dsn)      # True db://b   ← 注意：__init__ 仍会执行第二次</code></pre>
  <h4>__slots__：省内存与防手抖</h4>
  <pre class="code" data-lang="python"><code>import sys

class PointNormal:
    def __init__(self, x, y):
        self.x, self.y = x, y

class PointSlots:
    __slots__ = ("x", "y")          # 只允许这两个属性
    def __init__(self, x, y):
        self.x, self.y = x, y

p1, p2 = PointNormal(1, 2), PointSlots(1, 2)
print(sys.getsizeof(p1.__dict__))   # 104  ← 每个实例都带一个字典
# p2.z = 3                          # AttributeError: 'PointSlots' object has no attribute 'z'

# 大量小对象时差距明显：一百万个点可省几十 MB</code></pre>
  <div class="warn-box"><span class="tag-pit">注意</span><code>__slots__</code> 会让实例失去 <code>__dict__</code>，因此<strong>不能动态加属性</strong>，也会影响 <code>copy</code>、<code>pickle</code> 与部分框架。它属于<strong>优化手段</strong>，不要为了"规范"而滥用——需要数据类时优先用 <code>dataclass(slots=True)</code>（第 22 章）。</div>
</section>""",

"""<section id="sec7" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:34%"><col style="width:66%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>self 的真相</td><td><code>u.f()</code> ≡ <code>User.f(u)</code>；self 只是约定的参数名</td></tr>
      <tr><td>类也是对象</td><td>类是 type 的实例，有属性、可传递、可修改</td></tr>
      <tr><td>属性查找</td><td>实例 <code>__dict__</code> → 类 → 父类；给实例赋值只遮蔽</td></tr>
      <tr><td>头号陷阱</td><td>类属性是可变对象 → 被所有实例共享；放进 <code>__init__</code></td></tr>
      <tr><td>三种方法</td><td>用实例→实例方法；要构造→类方法（用 cls）；都不用→静态</td></tr>
      <tr><td>初始化</td><td><code>__init__</code> 无返回值；<code>__new__</code> 极少用；<code>__slots__</code> 是优化</td></tr>
    </tbody>
  </table>
</section>""",

"""<section id="sec8" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>写 <code>BankAccount</code>：属性 <code>owner</code>、<code>balance</code>；方法 <code>deposit</code>、<code>withdraw</code>（余额不足抛 <code>ValueError</code>）、<code>transfer_to(other, amount)</code>。要求 <code>withdraw</code> 返回 self 以支持链式调用。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>给 <code>BankAccount</code> 加类属性 <code>total_accounts</code> 与类方法 <code>from_dict(data)</code>（从字典创建），并验证：创建 3 个账户后 <code>total_accounts == 3</code>，且子类继承 <code>from_dict</code> 时返回的是子类实例。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>用 <code>__slots__</code> 重写一个点类，创建 100 万个实例，对比普通类的内存占用（用 <code>tracemalloc</code> 或任务管理器观察），并说明为什么 <code>__slots__</code> 能省内存（提示：少了每个实例一个 dict 的开销）。</div>
  <p class="note">参考答案见附录 C（规划中）。下一章：继承与魔法方法。</p>
</section>"""
]
},

# ════════════════════ 第 21 章 ════════════════════
{
"n": 21, "title": "继承与魔法方法",
"file": "021_第21章_继承与魔法方法.html",
"meta": "预计 50 分钟 · 动手章 · 重点章",
"hero": "魔法方法（dunder）是 Python 面向对象最迷人的部分：你的类可以像列表一样被下标访问、像数字一样相加、像函数一样被调用。本章讲清继承与 MRO、super() 的协作式调用，以及十几组最常用的魔法方法。",
"toc": [("sec1", "本章目标"), ("sec2", "21.1 继承与 super()"), ("sec3", "21.2 MRO 与多重继承"),
        ("sec4", "21.3 表示类魔法方法"), ("sec5", "21.4 比较与算术魔法方法"),
        ("sec6", "21.5 容器与可调用魔法方法"), ("sec7", "本章小结"), ("sec8", "本章习题")],
"sections": [
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>会用继承复用代码，理解 <code>super()</code> 的<strong>协作式调用</strong>；</li>
    <li>理解 <strong>MRO（方法解析顺序）</strong>与 C3 线性化，能读懂 <code>__mro__</code>；</li>
    <li>掌握表示类魔法方法：<code>__repr__</code> / <code>__str__</code> / <code>__format__</code>；</li>
    <li>会让自定义对象支持比较、算术、容器协议与调用；</li>
    <li>知道<strong>什么时候不该用继承</strong>（组合优先）。</li>
  </ul>
</section>""",

"""<section id="sec2" class="card">
  <h2><span class="num">21.1</span> 继承与 super()</h2>
  <pre class="code" data-lang="python"><code>class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError        # 留给子类实现（第 24 章用 ABC 更规范）

    def info(self):
        return f"动物：{self.name}"


class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)           # ① 调用父类初始化（协作式）
        self.breed = breed

    def speak(self):                     # ② 重写（override）
        return "汪汪"


class Cat(Animal):
    def speak(self):
        return "喵喵"


d = Dog("小黑", "柯基")
print(d.info(), d.speak(), d.breed)      # 动物：小黑 汪汪 柯基

# 多态：不关心具体类型，只管有没有 speak
for a in (Dog("a", "x"), Cat("b")):
    print(a.speak())                     # 汪汪 / 喵喵</code></pre>
  <p><code>super()</code> 的两个要点：</p>
  <ol>
    <li>它返回的不是"父类"，而是<strong>MRO 中的下一个类</strong>——在多重继承里这一点至关重要；</li>
    <li>Python 3 可以省略参数，写 <code>super().__init__()</code> 即可（等价于 <code>super(当前类, self).__init__()</code>）。</li>
  </ol>
  <pre class="code" data-lang="python"><code>class Employee:
    def __init__(self, name, salary):
        self.name, self.salary = name, salary

    def pay(self):
        return self.salary

class Manager(Employee):
    def __init__(self, name, salary, bonus):
        super().__init__(name, salary)   # 复用父类逻辑
        self.bonus = bonus

    def pay(self):
        return super().pay() + self.bonus    # 在父类结果上叠加

print(Manager("张三", 10000, 3000).pay())     # 13000</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span>子类 <code>__init__</code> 里忘了调 <code>super().__init__()</code> → 父类的属性没被设置，访问时 <code>AttributeError</code>。另外 <code>super()</code> 只能在<strong>方法内部</strong>使用（它依赖 <code>__class__</code> 闭包）。</div>
</section>""",

"""<section id="sec3" class="card">
  <h2><span class="num">21.2</span> MRO 与多重继承</h2>
  <p>MRO（Method Resolution Order）决定了"同名方法到底调谁的"。Python 用 <strong>C3 线性化</strong>算法，保证：<strong>子类优先于父类；多个父类按声明顺序</strong>。</p>
  <pre class="code" data-lang="python"><code>class A:
    def hi(self): return "A"

class B(A):
    def hi(self): return "B"

class C(A):
    def hi(self): return "C"

class D(B, C):        # 菱形继承
    pass

print(D().hi())                       # B   （B 在 C 之前）
print([c.__name__ for c in D.__mro__])   # ['D', 'B', 'C', 'A', 'object']
print(D.mro() == D.__mro__)           # 查看 MRO 的两种方式</code></pre>
  <div class="diagram">
    <svg viewBox="0 0 800 190" role="img" aria-label="菱形继承与 MRO 示意">
      <text x="400" y="22" text-anchor="middle" font-size="14" font-weight="700" fill="#1f2e1f">菱形继承：D(B, C)，B、C 都继承 A</text>
      <rect x="360" y="40" width="80" height="34" rx="8" fill="#f0f5e6" stroke="#3d7a4f"/><text x="400" y="62" text-anchor="middle" font-size="13" font-weight="700" fill="#2d6a3f">A</text>
      <rect x="230" y="105" width="80" height="34" rx="8" fill="#f0f5e6" stroke="#3d7a4f"/><text x="270" y="127" text-anchor="middle" font-size="13" font-weight="700" fill="#2d6a3f">B(A)</text>
      <rect x="490" y="105" width="80" height="34" rx="8" fill="#f0f5e6" stroke="#3d7a4f"/><text x="530" y="127" text-anchor="middle" font-size="13" font-weight="700" fill="#2d6a3f">C(A)</text>
      <rect x="360" y="155" width="80" height="26" rx="6" fill="#fefce8" stroke="#b45309"/><text x="400" y="172" text-anchor="middle" font-size="12.5" fill="#b45309">D(B, C)</text>
      <line x1="270" y1="105" x2="385" y2="75" stroke="#7a8a70" stroke-width="1.5"/>
      <line x1="530" y1="105" x2="415" y2="75" stroke="#7a8a70" stroke-width="1.5"/>
      <line x1="385" y1="155" x2="285" y2="140" stroke="#7a8a70" stroke-width="1.5"/>
      <line x1="415" y1="155" x2="515" y2="140" stroke="#7a8a70" stroke-width="1.5"/>
      <text x="620" y="90" font-size="12" fill="#4f6348">MRO: D → B → C → A → object</text>
      <text x="620" y="112" font-size="12" fill="#4f6348">查找 hi() 时在 B 就命中</text>
      <text x="620" y="134" font-size="11.5" fill="#7a8a70">super() = MRO 的下一个</text>
    </svg>
    <p class="diagram-caption">图 21-1 菱形继承与 MRO（示意）</p>
  </div>
  <h4>协作式多重继承（Mixin）</h4>
  <pre class="code" data-lang="python"><code>class JsonMixin:
    """给任意类加 to_json 能力（Mixin：只加功能，不单独实例化）。"""
    def to_json(self):
        import json
        return json.dumps(self.__dict__, ensure_ascii=False)

class LogMixin:
    def log(self, msg):
        print(f"[{type(self).__name__}] {msg}")

class User(JsonMixin, LogMixin):        # Mixin 放前面
    def __init__(self, name):
        self.name = name

u = User("张三")
print(u.to_json())      # {"name": "张三"}
u.log("创建成功")       # [User] 创建成功</code></pre>
  <p class="key-sentence">工程建议：<strong>组合优先于继承</strong>。继承表达"是一种（is-a）"，组合表达"有一个（has-a）"。深层继承树（超过 3 层）几乎总是设计出了问题；Mixin 是多重继承唯一被广泛接受的用法。</p>
</section>""",

"""<section id="sec4" class="card">
  <h2><span class="num">21.3</span> 表示类魔法方法</h2>
  <table>
    <colgroup><col style="width:26%"><col style="width:38%"><col style="width:36%"></colgroup>
    <thead><tr><th>方法</th><th>触发</th><th>目标读者</th></tr></thead>
    <tbody>
      <tr><td><code>__repr__</code></td><td><code>repr()</code>、容器里显示、报错</td><td><strong>开发者</strong>：应"无歧义"，最好能 eval 重建</td></tr>
      <tr><td><code>__str__</code></td><td><code>str()</code>、<code>print()</code></td><td><strong>用户</strong>：应"可读"</td></tr>
      <tr><td><code>__format__</code></td><td><code>f"{obj:spec}"</code></td><td>支持自定义格式规范</td></tr>
      <tr><td><code>__bytes__</code></td><td><code>bytes(obj)</code></td><td>序列化为字节</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="python"><code>class Money:
    def __init__(self, amount, currency="CNY"):
        self.amount, self.currency = amount, currency

    def __repr__(self):
        return f"Money({self.amount!r}, {self.currency!r})"    # 无歧义

    def __str__(self):
        return f"{self.currency} {self.amount:,.2f}"           # 给用户看

    def __format__(self, spec):
        if spec == "plain":
            return f"{self.amount:.2f}"
        return str(self)

m = Money(1234.5)
print(repr(m))            # Money(1234.5, 'CNY')
print(str(m), m)          # CNY 1,234.50  CNY 1,234.50
print(f"{m:plain}")       # 1234.50</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span>只定义了 <code>__str__</code> 时，把它放进列表里打印仍是 <code>&lt;Money object at 0x...&gt;</code>——因为<strong>容器打印用的是 <code>repr()</code></strong>。所以<strong>永远至少实现 <code>__repr__</code></strong>（调试友好度立刻提升一个档次）。</div>
</section>""",

"""<section id="sec5" class="card">
  <h2><span class="num">21.4</span> 比较与算术魔法方法</h2>
  <pre class="code" data-lang="python"><code>import functools

@functools.total_ordering          # 只需 __eq__ + 一个比较，其余自动补全
class Version:
    def __init__(self, text):
        self.parts = tuple(int(p) for p in text.split("."))

    def __eq__(self, other):
        if not isinstance(other, Version):
            return NotImplemented      # ← 交给对方去比，比抛异常优雅
        return self.parts == other.parts

    def __lt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self.parts &lt; other.parts

    def __repr__(self):
        return f"Version({'.'.join(map(str, self.parts))})"

print(Version("1.2.0") &lt; Version("1.10.0"))     # True（元组比较，不是字符串！）
print(sorted([Version("2.0"), Version("1.9")]))  # [Version(1.9), Version(2.0)]

class Vector:
    """二维向量：演示算术魔法方法。"""
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, k):                 # 向量 × 标量
        return Vector(self.x * k, self.y * k)

    __rmul__ = __mul__                    # 支持 k * v（反射运算）

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

print(Vector(1, 2) + Vector(3, 4))    # Vector(4, 6)
print(Vector(1, 2) * 3, 3 * Vector(1, 2))   # Vector(3, 6) Vector(3, 6)
print(abs(Vector(3, 4)))              # 5.0</code></pre>
  <table>
    <colgroup><col style="width:30%"><col style="width:36%"><col style="width:34%"></colgroup>
    <thead><tr><th>类别</th><th>方法</th><th>触发</th></tr></thead>
    <tbody>
      <tr><td>比较</td><td><code>__eq__ __ne__ __lt__ __le__ __gt__ __ge__</code></td><td><code>== != &lt; &lt;= &gt; &gt;=</code></td></tr>
      <tr><td>算术</td><td><code>__add__ __sub__ __mul__ __truediv__ __floordiv__ __mod__ __pow__</code></td><td><code>+ - * / // % **</code></td></tr>
      <tr><td>反射算术</td><td><code>__radd__ __rmul__ ...</code></td><td>左操作数不支持时（<code>3 * v</code>）</td></tr>
      <tr><td>原地算术</td><td><code>__iadd__ __imul__ ...</code></td><td><code>+= *=</code></td></tr>
      <tr><td>一元 / 转换</td><td><code>__neg__ __abs__ __int__ __float__ __bool__</code></td><td><code>-x abs() int() bool()</code></td></tr>
    </tbody>
  </table>
  <div class="note"><strong>黄金法则</strong>：二元运算遇到"不认识的类型"时返回 <code>NotImplemented</code>（<u>不是</u>抛异常、<u>不是</u>返回 False），让 Python 去尝试对方的反射方法，都不行才抛 <code>TypeError</code>。</div>
</section>""",

"""<section id="sec6" class="card">
  <h2><span class="num">21.5</span> 容器与可调用魔法方法</h2>
  <pre class="code" data-lang="python"><code>class Playlist:
    """让自定义类像列表一样工作。"""

    def __init__(self, songs):
        self._songs = list(songs)

    def __len__(self):
        return len(self._songs)                 # len(pl)

    def __getitem__(self, index):
        return self._songs[index]               # pl[0]、切片、迭代、in（退化为遍历）

    def __setitem__(self, index, value):
        self._songs[index] = value              # pl[0] = "x"

    def __contains__(self, item):
        return item in self._songs              # "x" in pl（有了它就不必退化遍历）

    def __iter__(self):
        return iter(self._songs)                # for song in pl

    def __reversed__(self):
        return reversed(self._songs)            # reversed(pl)

    def __repr__(self):
        return f"Playlist({self._songs!r})"


pl = Playlist(["a", "b", "c"])
print(len(pl), pl[0], pl[::-1])       # 3 a ['c', 'b', 'a']
print("a" in pl, list(pl))            # True ['a', 'b', 'c']
for s in pl:                          # 因为实现了 __iter__ / __getitem__
    print(s, end=" ")

class Adder:
    """让实例可以像函数一样被调用。"""
    def __call__(self, x):
        return x + self.base if hasattr(self, "base") else x

add = Adder()
print(callable(add), add(5))          # True 5</code></pre>
  <table>
    <colgroup><col style="width:26%"><col style="width:40%"><col style="width:34%"></colgroup>
    <thead><tr><th>协议</th><th>方法</th><th>效果</th></tr></thead>
    <tbody>
      <tr><td>长度</td><td><code>__len__</code></td><td><code>len()</code>、布尔判断（0 为假）</td></tr>
      <tr><td>索引</td><td><code>__getitem__ / __setitem__ / __delitem__</code></td><td>下标、切片、迭代</td></tr>
      <tr><td>迭代</td><td><code>__iter__ / __next__</code></td><td>for、解包（第 15 章）</td></tr>
      <tr><td>成员</td><td><code>__contains__</code></td><td><code>in</code></td></tr>
      <tr><td>可调用</td><td><code>__call__</code></td><td><code>obj()</code>；<strong>类装饰器正是靠它</strong>（第 16 章）</td></tr>
      <tr><td>哈希</td><td><code>__hash__</code></td><td>可作为 dict 键 / set 元素（配合 <code>__eq__</code>）</td></tr>
    </tbody>
  </table>
  <div class="warn-box"><span class="tag-pit">常见坑</span>① 定义了 <code>__eq__</code> 而没定义 <code>__hash__</code>，类的实例会<strong>变成不可哈希</strong>（<code>__hash__</code> 被置为 None），无法放进 set 或作 dict 键；② 定义了 <code>__getitem__</code> 就能迭代，但推荐显式实现 <code>__iter__</code>，语义更清晰。</div>
</section>""",

"""<section id="sec7" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:34%"><col style="width:66%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>继承</td><td>子类复用父类；<code>super()</code> 走 MRO 的下一个</td></tr>
      <tr><td>MRO</td><td>C3 线性化：子类优先、声明顺序；查 <code>__mro__</code></td></tr>
      <tr><td>Mixin</td><td>多重继承唯一被广泛接受的用法：只加能力</td></tr>
      <tr><td><code>__repr__</code> / <code>__str__</code></td><td>前者给开发者（必写），后者给用户</td></tr>
      <tr><td>比较</td><td>用 <code>total_ordering</code>；不认识的类型返回 <code>NotImplemented</code></td></tr>
      <tr><td>算术</td><td>正向 / 反射（r）/ 原地（i）三套</td></tr>
      <tr><td>容器与调用</td><td>len/getitem/iter/contains；<code>__call__</code> 让对象像函数</td></tr>
      <tr><td>组合优先</td><td>深层继承是设计异味；Mixin 除外</td></tr>
    </tbody>
  </table>
</section>""",

"""<section id="sec8" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>给 <code>Money</code> 加 <code>__add__</code>、<code>__sub__</code>、<code>__eq__</code>、<code>__lt__</code>，并保证不同币种相加时抛 <code>ValueError</code>；实现 <code>__repr__</code> 与 <code>__str__</code>。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>写一个 <code>class Matrix</code>（二维列表为内部存储），实现 <code>__getitem__</code>、<code>__setitem__</code>、<code>__add__</code>、<code>__mul__</code>（矩阵乘）、<code>__repr__</code>，并支持 <code>for row in matrix</code> 迭代。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>实现一个 <code>Observable</code> Mixin：让任意类获得 <code>subscribe(fn)</code> / <code>notify()</code> 能力，且支持多重继承协作（每个 Mixin 的 <code>__init__</code> 都要调 <code>super().__init__()</code>）。用它改造一个订单类，下单成功时通知监听器。</div>
  <p class="note">参考答案见附录 C（规划中）。下一章：dataclass——数据载体。</p>
</section>"""
]
},

# ════════════════════ 第 22 章 ════════════════════
{
"n": 22, "title": "dataclass：数据载体",
"file": "022_第22章_dataclass.html",
"meta": "预计 40 分钟 · 动手章",
"hero": "写「只装数据的类」是日常最高频的重复劳动：__init__、__repr__、__eq__ 一遍遍抄。dataclass 用一行装饰器全部生成，还能排序、冻结、转字典。本章讲透它的全部选项，以及它在 FastAPI 请求体、配置对象里的实战用法。",
"toc": [("sec1", "本章目标"), ("sec2", "22.1 从手写类到 dataclass"), ("sec3", "22.2 field() 与默认值"),
        ("sec4", "22.3 排序、冻结与不可变"), ("sec5", "22.4 转换：asdict / astuple / slots"),
        ("sec6", "22.5 继承、后处理与选型"), ("sec7", "本章小结"), ("sec8", "本章习题")],
"sections": [
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>用 <code>@dataclass</code> 一行替代几十行样板代码；</li>
    <li>会用 <code>field()</code> 处理<strong>可变默认值</strong>与排除字段；</li>
    <li>理解 <code>order=True</code>、<code>frozen=True</code>、<code>slots=True</code> 的作用；</li>
    <li>会在 dataclass / NamedTuple / TypedDict / Pydantic 之间<strong>正确选型</strong>；</li>
    <li>掌握 <code>__post_init__</code> 做派生字段与校验。</li>
  </ul>
</section>""",

"""<section id="sec2" class="card">
  <h2><span class="num">22.1</span> 从手写类到 dataclass</h2>
  <pre class="code" data-lang="python"><code># 手写版：为了装三个字段，写了十几行样板
class UserManual:
    def __init__(self, name, age, email=""):
        self.name = name
        self.age = age
        self.email = email

    def __repr__(self):
        return f"UserManual(name={self.name!r}, age={self.age!r}, email={self.email!r})"

    def __eq__(self, other):
        if not isinstance(other, UserManual):
            return NotImplemented
        return (self.name, self.age, self.email) == (other.name, other.age, other.email)


# dataclass 版：一个装饰器搞定
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    email: str = ""

u = User("张三", 20)
print(u)                       # User(name='张三', age=20, email='')   ← 自动生成 __repr__
print(u == User("张三", 20))   # True                                  ← 自动生成 __eq__</code></pre>
  <p><code>@dataclass</code> 自动生成的内容：<code>__init__</code>、<code>__repr__</code>、<code>__eq__</code>（以及可选的比较、哈希、冻结等）。</p>
  <div class="warn-box"><span class="tag-pit">必备前提</span>字段<strong>必须写类型注解</strong>（<code>name: str</code>）——dataclass 就是靠读取 <code>__annotations__</code> 工作的。写 <code>name = "x"</code> 不带注解，它只是个普通类属性，不会成为构造参数。</div>
  <pre class="code" data-lang="python"><code>from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: float
    stock: int = 0                 # 有默认值 → 构造时可省略
    tags: list = None              # ← 别这么写，见下一节的 field(default_factory=...)

print(Product("键盘", 199.0))
# Product(name='键盘', price=199.0, stock=0, tags=None)</code></pre>
</section>""",

"""<section id="sec3" class="card">
  <h2><span class="num">22.2</span> field() 与默认值</h2>
  <pre class="code" data-lang="python"><code>from dataclasses import dataclass, field

@dataclass
class Product:
    name: str
    price: float
    tags: list[str] = field(default_factory=list)      # 每次新建空列表
    meta: dict = field(default_factory=dict)
    internal_id: int = field(default=0, repr=False)    # 不出现在 repr 里
    version: str = field(default="1.0", compare=False) # 不参与 == 比较

p1, p2 = Product("键盘", 199.0), Product("鼠标", 99.0)
p1.tags.append("外设")
print(p2.tags)          # []      ← 各自独立，正确！
print(p1)               # Product(name='键盘', price=199.0, tags=['外设'], meta={}, version='1.0')
print(p1 == Product("键盘", 199.0))   # True（version 不参与比较）</code></pre>
  <div class="danger-box"><span class="tag-pit">头号坑</span>dataclass 会主动<strong>拒绝</strong>可变默认值：<code>tags: list = []</code> 直接抛 <code>ValueError: mutable default ... use default_factory</code>。这是它比手写类更安全的地方——第 11 章那个"默认参数陷阱"被语言层面挡住了。</div>
  <table>
    <colgroup><col style="width:28%"><col style="width:38%"><col style="width:34%"></colgroup>
    <thead><tr><th><code>field()</code> 参数</th><th>作用</th><th>典型用途</th></tr></thead>
    <tbody>
      <tr><td><code>default</code></td><td>不可变默认值</td><td><code>default=0</code></td></tr>
      <tr><td><code>default_factory</code></td><td>调用工厂造默认值</td><td><code>list</code>、<code>dict</code>、<code>set</code>、<code>datetime.now</code></td></tr>
      <tr><td><code>repr=False</code></td><td>不进 repr</td><td>敏感信息、大字段</td></tr>
      <tr><td><code>compare=False</code></td><td>不参与比较</td><td>ID、时间戳</td></tr>
      <tr><td><code>init=False</code></td><td>不作为构造参数</td><td>由 <code>__post_init__</code> 计算</td></tr>
      <tr><td><code>metadata</code></td><td>附加元数据</td><td>序列化/校验框架读取</td></tr>
    </tbody>
  </table>
</section>""",

"""<section id="sec4" class="card">
  <h2><span class="num">22.3</span> 排序、冻结与不可变</h2>
  <pre class="code" data-lang="python"><code>from dataclasses import dataclass, field

@dataclass(order=True)              # 生成 __lt__ 等，按字段声明顺序比较
class Task:
    priority: int
    title: str = field(compare=False)   # 只按 priority 排，title 不参与

tasks = [Task(3, "写文档"), Task(1, "修 bug"), Task(2, "评审")]
print(sorted(tasks))                # [Task(priority=1...), Task(2...), Task(3...)]

# 只想按某个字段排：sort_index 技巧
@dataclass(order=True)
class Job:
    sort_key: int = field(init=False, repr=False)
    name: str
    cost: int

    def __post_init__(self):
        self.sort_key = -self.cost        # 按 cost 降序

print(sorted([Job("a", 5), Job("b", 9)], key=lambda j: j.sort_key)[0].name)   # b

@dataclass(frozen=True)             # 冻结：属性只读，且可哈希
class Point:
    x: int
    y: int

p = Point(1, 2)
# p.x = 3      # FrozenInstanceError
print({Point(1, 2): "原点附近"})     # 可作字典键（因为可哈希）</code></pre>
  <table>
    <colgroup><col style="width:26%"><col style="width:40%"><col style="width:34%"></colgroup>
    <thead><tr><th>选项</th><th>效果</th><th>何时用</th></tr></thead>
    <tbody>
      <tr><td><code>order=True</code></td><td>生成六個比较方法</td><td>需要排序时</td></tr>
      <tr><td><code>frozen=True</code></td><td>只读 + 可哈希</td><td>值对象、配置、字典键</td></tr>
      <tr><td><code>slots=True</code>（3.10+）</td><td>生成 <code>__slots__</code></td><td>大量小对象，省内存</td></tr>
      <tr><td><code>kw_only=True</code>（3.10+）</td><td>构造只能用关键字</td><td>字段多、防顺序写错</td></tr>
      <tr><td><code>unsafe_hash=True</code></td><td>非冻结也生成 <code>__hash__</code></td><td>明确知道后果时</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="python"><code>@dataclass(frozen=True, slots=True, kw_only=True)
class Settings:
    host: str = "localhost"
    port: int = 8000
    debug: bool = False

s = Settings(host="0.0.0.0", port=9000, debug=True)   # 必须关键字传参
print(s)            # Settings(host='0.0.0.0', port=9000, debug=True)</code></pre>
  <div class="warn-box"><span class="tag-pit">注意</span><code>frozen=True</code> 只保证<strong>顶层属性不可重新绑定</strong>——如果属性本身是列表，列表内容仍可改。要真正不可变，字段类型用 <code>tuple</code> 而非 <code>list</code>。</div>
</section>""",

"""<section id="sec5" class="card">
  <h2><span class="num">22.4</span> 转换：asdict / astuple / slots</h2>
  <pre class="code" data-lang="python"><code>from dataclasses import dataclass, field, asdict, astuple, replace, fields
import json

@dataclass
class Address:
    city: str
    street: str

@dataclass
class Person:
    name: str
    age: int
    address: Address

p = Person("张三", 20, Address("北京", "朝阳"))

print(asdict(p))          # 递归转字典：{'name': '张三', 'age': 20, 'address': {'city': '北京', ...}}
print(astuple(p))         # 递归转元组：('张三', 20, ('北京', '朝阳'))
print(json.dumps(asdict(p), ensure_ascii=False))   # 直接序列化

# replace：基于旧对象造新对象（对 frozen 特别有用）
p2 = replace(p, age=21)
print(p2)                 # Person(name='张三', age=21, address=Address(...))

# fields()：反射字段定义（通用代码很有用）
for f in fields(Person):
    print(f.name, f.type, f.default)</code></pre>
  <div class="note"><code>asdict()</code> 是<strong>深拷贝式</strong>转换（递归处理嵌套 dataclass、列表、字典），但遇到非 dataclass 的自定义对象会用 <code>copy.deepcopy</code>。序列化给 JSON 时非常顺手。</div>
  <p class="key-sentence">与 FastAPI / Pydantic 的关系：<strong>dataclass 负责内部数据载体，Pydantic BaseModel 负责边界校验与序列化</strong>（第 42 章）。API 请求体用 Pydantic，领域对象用 dataclass，是常见且清晰的分工。</p>
</section>""",

"""<section id="sec6" class="card">
  <h2><span class="num">22.5</span> 继承、后处理与选型</h2>
  <pre class="code" data-lang="python"><code>from dataclasses import dataclass, field

@dataclass
class Base:
    id: int = 0

@dataclass
class User(Base):                     # 继承：字段按 MRO 逆序排列
    name: str = ""
    email: str = ""

print(User(1, "张三"))    # User(id=1, name='张三', email='')

@dataclass
class Order:
    items: list[tuple[str, int]]      # [(商品, 数量)]
    discount: float = 0.0
    total: float = field(init=False)  # 不参与构造，由 __post_init__ 算

    def __post_init__(self):          # 在 __init__ 末尾自动调用
        raw = sum(price * qty for _, qty in
                  [(price, qty) for _, (price, qty) in [("", (0, 0))]]  ) if False else \\
              sum(price * qty for price, qty in [(0, 0)])
        self.total = raw

@dataclass
class BetterOrder:
    unit_price: float
    quantity: int
    discount: float = 0.0

    def __post_init__(self):
        if self.unit_price &lt; 0 or self.quantity &lt;= 0:      # 校验
            raise ValueError("单价与数量必须为正")
        self.amount = self.unit_price * self.quantity * (1 - self.discount)

o = BetterOrder(19.9, 3, 0.1)
print(o.amount)           # 53.73</code></pre>
  <h4>四种"数据类"选型表</h4>
  <table>
    <colgroup><col style="width:22%"><col style="width:42%"><col style="width:36%"></colgroup>
    <thead><tr><th>工具</th><th>特点</th><th>何时用</th></tr></thead>
    <tbody>
      <tr><td><code>dataclass</code></td><td>可变（可 frozen）、有默认值、可继承</td><td><strong>默认选择</strong>：领域对象、配置</td></tr>
      <tr><td><code>NamedTuple</code></td><td>不可变、是元组、轻量</td><td>多返回值、需要当字典键时</td></tr>
      <tr><td><code>TypedDict</code></td><td>只是"字典的类型标注"，无运行时行为</td><td>描述 JSON 报文结构</td></tr>
      <tr><td>Pydantic <code>BaseModel</code></td><td>运行时校验 + 序列化 + 文档</td><td><strong>API 边界</strong>（第 42 章）</td></tr>
    </tbody>
  </table>
  <p class="key-sentence">一句话决策：<strong>内部用 dataclass，外部边界用 Pydantic，多返回值用 NamedTuple，描述已有字典结构用 TypedDict。</strong></p>
</section>""",

"""<section id="sec7" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:34%"><col style="width:66%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>价值</td><td>一个装饰器生成 <code>__init__</code>/<code>__repr__</code>/<code>__eq__</code></td></tr>
      <tr><td>前提</td><td>字段必须带类型注解</td></tr>
      <tr><td>可变默认值</td><td>用 <code>field(default_factory=list)</code>；直接写会报错</td></tr>
      <tr><td>常用选项</td><td><code>order</code> 排序、<code>frozen</code> 冻结可哈希、<code>slots</code> 省内存、<code>kw_only</code> 强制关键字</td></tr>
      <tr><td>转换</td><td><code>asdict</code>/<code>astuple</code> 递归转；<code>replace</code> 造新对象</td></tr>
      <tr><td>后处理</td><td><code>__post_init__</code> 做派生字段与校验</td></tr>
      <tr><td>选型</td><td>内部 dataclass、边界 Pydantic、多返回 NamedTuple</td></tr>
    </tbody>
  </table>
</section>""",

"""<section id="sec8" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>用 dataclass 定义 <code>Student</code>（name、age、scores: list），要求：scores 默认空列表且实例间独立；能按 age 排序；打印时不显示内部自增 ID 字段。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>定义嵌套 dataclass：<code>Order</code> 含多个 <code>OrderItem</code>，用 <code>__post_init__</code> 计算总价与折扣，加 <code>asdict()</code> 导出 JSON（中文不转义），再写个函数从 JSON 反向构造回来。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>把 B 题的 <code>Order</code> 改写成 Pydantic <code>BaseModel</code>，对比两者在"校验失败行为""序列化""性能"三方面的差异，并说明你会如何在一个 FastAPI 项目里同时使用它们。</div>
  <p class="note">参考答案见附录 C（规划中）。下一章：属性与描述符协议。</p>
</section>"""
]
}
]

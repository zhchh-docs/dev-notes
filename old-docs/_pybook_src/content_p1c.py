# -*- coding: utf-8 -*-
"""第一篇 入门与语法 · 第 7-9 章"""

PART_DIR = "10_第一篇_入门与语法"
PART_NAME = "第一篇 入门与语法"

CHAPTERS = [
# ════════════════════ 第 7 章 ════════════════════
{
"n": 7, "title": "列表：增删改查与切片",
"file": "007_第7章_列表.html",
"meta": "预计 45 分钟 · 动手章",
"hero": "列表是 Python 的「默认容器」：有序、可变、什么都能装。本章把增删改查、切片赋值、排序与拷贝讲透，并第一次系统回答那个反复出现的问题——为什么 a = b 之后改 b，a 也变了。",
"toc": [("sec1", "本章目标"), ("sec2", "7.1 列表的本质与创建"), ("sec3", "7.2 增：append / extend / insert"),
        ("sec4", "7.3 删：remove / pop / del / clear"), ("sec5", "7.4 查、改与切片赋值"),
        ("sec6", "7.5 排序、拷贝与常见坑"), ("sec7", "本章小结"), ("sec8", "本章习题")],
"sections": [
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>理解列表<strong>有序、可变、可异构</strong>三大特性，以及它的动态数组实现带来的性能特征；</li>
    <li>分清 <code>append</code> 与 <code>extend</code>、<code>remove</code> 与 <code>pop</code> 的差异；</li>
    <li>掌握<strong>切片赋值</strong>与常用切片技巧；</li>
    <li>分清<strong>浅拷贝与深拷贝</strong>，解释"改了 b，a 也变"；</li>
    <li>会用 <code>sort</code> / <code>sorted</code> 与 <code>key</code> 做多条件排序。</li>
  </ul>
</section>""",

"""<section id="sec2" class="card">
  <h2><span class="num">7.1</span> 列表的本质与创建</h2>
  <p>列表是<strong>有序、可变</strong>的容器，元素可以是任意类型（异构）。底层是动态数组，因此<strong>按下标访问是 O(1)，在头部插入是 O(n)</strong>。</p>
  <pre class="code" data-lang="python"><code>nums = [1, 2, 3]
mixed = [1, "two", 3.0, None, [4, 5]]      # 什么都能装
empty = []
from_range = list(range(5))                # [0, 1, 2, 3, 4]
from_str = list("abc")                     # ['a', 'b', 'c']
from_split = "a,b,c".split(",")            # ['a', 'b', 'c']

print(len(nums), nums[0], nums[-1])        # 3 1 3
nums[0] = 100                              # 可变：原地修改

# 嵌套列表 = 二维结构
matrix = [[1, 2, 3], [4, 5, 6]]
print(matrix[1][2])                        # 6</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span><code>[[0] * 3] * 3</code> 创建的二维列表里，三行是<strong>同一个列表对象</strong>——改一行三行全变。正确写法是 <code>[[0] * 3 for _ in range(3)]</code>（每次循环生成新的内层列表）。</div>
  <pre class="code" data-lang="python"><code>wrong = [[0] * 3] * 3
wrong[0][0] = 9
print(wrong)          # [[9, 0, 0], [9, 0, 0], [9, 0, 0]]  ← 三行一起变

right = [[0] * 3 for _ in range(3)]
right[0][0] = 9
print(right)          # [[9, 0, 0], [0, 0, 0], [0, 0, 0]]</code></pre>
</section>""",

"""<section id="sec3" class="card">
  <h2><span class="num">7.2</span> 增：append / extend / insert</h2>
  <table>
    <colgroup><col style="width:24%"><col style="width:42%"><col style="width:34%"></colgroup>
    <thead><tr><th>方法</th><th>行为</th><th>复杂度 / 注意</th></tr></thead>
    <tbody>
      <tr><td><code>append(x)</code></td><td>末尾追加<strong>一个元素</strong></td><td>均摊 O(1)，最常用</td></tr>
      <tr><td><code>extend(iter)</code></td><td>把可迭代对象<strong>逐个元素</strong>并入</td><td>O(k)</td></tr>
      <tr><td><code>insert(i, x)</code></td><td>在下标 i 处插入</td><td>O(n)，头部插入慢</td></tr>
      <tr><td><code>+</code></td><td>拼接生成新列表</td><td>不改动原列表</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="python"><code>a = [1, 2]
a.append(3);        print(a)      # [1, 2, 3]
a.append([4, 5]);   print(a)      # [1, 2, 3, [4, 5]]   ← 整体作为一个元素

b = [1, 2]
b.extend([3, 4]);   print(b)      # [1, 2, 3, 4]        ← 逐元素并入
b.extend("ab");     print(b)      # [1, 2, 3, 4, 'a', 'b']

c = [1, 2, 3]
c.insert(0, 0);     print(c)      # [0, 1, 2, 3]
print(c + [4, 5])                 # [0, 1, 2, 3, 4, 5]（c 本身不变）</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span>想"合并两个列表"时用 <code>append</code> 会把整个列表当成一个元素塞进去，得到嵌套结构；要用 <code>extend</code> 或 <code>+=</code>。</div>
  <p>需要"队列"语义时，别用 <code>pop(0)</code>（O(n)）——用 <code>collections.deque</code>（第 27 章）：</p>
  <pre class="code" data-lang="python"><code>from collections import deque
q = deque(["a", "b", "c"])
q.append("d"); q.popleft()        # 两端操作都是 O(1)
print(q)                          # deque(['b', 'c', 'd'])</code></pre>
</section>""",

"""<section id="sec4" class="card">
  <h2><span class="num">7.3</span> 删：remove / pop / del / clear</h2>
  <pre class="code" data-lang="python"><code>a = ["a", "b", "c", "b"]

a.remove("b")                     # 按值删除，只删第一个匹配
print(a)                          # ['a', 'c', 'b']

last = a.pop()                    # 弹出末尾，返回值
print(last, a)                    # b ['a', 'c']

second = a.pop(0)                 # 按下标弹出（O(n)，慎用）
print(second, a)                  # a ['c']

del a[0]                          # 按下标删除，不返回值
a.clear()                         # 清空（保留列表对象）</code></pre>
  <table>
    <colgroup><col style="width:26%"><col style="width:38%"><col style="width:36%"></colgroup>
    <thead><tr><th>方式</th><th>依据</th><th>注意</th></tr></thead>
    <tbody>
      <tr><td><code>remove(v)</code></td><td>值</td><td>只删第一个；值不存在抛 ValueError</td></tr>
      <tr><td><code>pop([i])</code></td><td>下标（默认末尾）</td><td>返回被删元素；空列表抛 IndexError</td></tr>
      <tr><td><code>del a[i]</code></td><td>下标或切片</td><td>语句而非方法，不返回值</td></tr>
      <tr><td><code>clear()</code></td><td>清空</td><td>等价于 <code>del a[:]</code></td></tr>
    </tbody>
  </table>
  <div class="danger-box"><span class="tag-pit">高频事故</span>在 <code>for</code> 循环里调用 <code>remove()</code> 删除元素会<strong>跳过元素</strong>（因为删除后后续元素前移，而迭代器仍按原下标前进）。要"按条件批量删除"，用列表推导式生成新列表，或遍历副本 <code>for x in a[:]</code>。</div>
  <pre class="code" data-lang="python"><code>nums = [1, 2, 3, 4, 5, 6]
# 目标：删掉所有偶数 → 用推导式最清晰
nums = [n for n in nums if n % 2 != 0]
print(nums)        # [1, 3, 5]</code></pre>
</section>""",

"""<section id="sec5" class="card">
  <h2><span class="num">7.4</span> 查、改与切片赋值</h2>
  <pre class="code" data-lang="python"><code>a = [10, 20, 30, 40, 50]

print(a[1], a[-1], a[1:3])        # 20 50 [20, 30]
print(30 in a)                    # True
print(a.index(30))                # 2   首次出现的下标
print(a.count(20))                # 1

a[0] = 100                        # 单元素改
a[1:3] = [200, 300, 400]          # 切片赋值：长度可以不等！
print(a)                          # [100, 200, 300, 400, 40, 50]

a[::2] = [0, 0, 0]                # 带步长的切片赋值要求长度一致
print(a)                          # [0, 200, 0, 400, 0, 50]

del a[1:]                         # 切片删除
print(a)                          # [0]</code></pre>
  <p>几个每天都在用的切片技巧：</p>
  <pre class="code" data-lang="python"><code>x = [1, 2, 3, 4, 5]
print(x[::-1])        # [5, 4, 3, 2, 1]        反转
print(x[:2], x[-2:])  # [1, 2] [4, 5]          前两个 / 后两个
print(x[:-1])         # [1, 2, 3, 4]           去掉最后一个

# 遍历时同时需要索引：enumerate
for i, v in enumerate(x, start=1):
    print(i, v)</code></pre>
  <p class="key-sentence">切片会<strong>生成新列表</strong>（浅拷贝），所以 <code>x[:]</code> 是复制列表最简洁的写法之一——但它只复制一层，嵌套结构仍共享。</p>
</section>""",

"""<section id="sec6" class="card">
  <h2><span class="num">7.5</span> 排序、拷贝与常见坑</h2>
  <pre class="code" data-lang="python"><code>nums = [3, 1, 2]
nums.sort()                       # 原地排序，返回 None
print(nums)                       # [1, 2, 3]

nums.sort(reverse=True)           # 降序
print(sorted(nums))               # 生成新列表，不改原列表

words = ["banana", "apple", "cherry"]
words.sort(key=len)               # 按长度排
words.sort(key=str.lower)         # 忽略大小写排

# 多条件排序：先按年龄升序，再按姓名降序
people = [("张三", 20), ("李四", 18), ("王五", 20)]
people.sort(key=lambda p: (p[1], p[0]))
print(people)                     # [('李四', 18), ('张三', 20), ('王五', 20)]</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span><code>sorted_nums = nums.sort()</code> 会得到 <code>None</code>！<code>sort()</code> 原地排序并返回 <code>None</code>，要新列表请用 <code>sorted(nums)</code>。</div>
  <h4>浅拷贝 vs 深拷贝</h4>
  <pre class="code" data-lang="python"><code>import copy

a = [[1, 2], [3, 4]]

b = a                # 别名：完全同一个对象
c = a[:]             # 浅拷贝：外层新列表，内层仍共享
d = copy.deepcopy(a) # 深拷贝：完全独立

c[0].append(99)
print(a)             # [[1, 2, 99], [3, 4]]   ← 浅拷贝改内层，a 也变了
print(c)             # [[1, 2, 99], [3, 4]]

d[1].append(0)
print(a)             # [[1, 2, 99], [3, 4]]   ← 深拷贝互不影响
print(d)             # [[1, 2], [3, 4, 0]]</code></pre>
  <table>
    <colgroup><col style="width:26%"><col style="width:38%"><col style="width:36%"></colgroup>
    <thead><tr><th>写法</th><th>含义</th><th>嵌套结构是否独立</th></tr></thead>
    <tbody>
      <tr><td><code>b = a</code></td><td>别名</td><td>否（完全同一对象）</td></tr>
      <tr><td><code>a[:]</code> / <code>list(a)</code> / <code>a.copy()</code></td><td>浅拷贝（一层）</td><td>否（内层共享）</td></tr>
      <tr><td><code>copy.deepcopy(a)</code></td><td>深拷贝（递归）</td><td>是</td></tr>
    </tbody>
  </table>
  <p class="key-sentence">口诀：只想"不被函数改到"用浅拷贝；数据结构是嵌套的且要彻底独立，才用深拷贝（深拷贝较慢，别在循环里滥用）。</p>
</section>""",

"""<section id="sec7" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:34%"><col style="width:66%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>性质</td><td>有序、可变、异构；下标 O(1)，头部插入 O(n)</td></tr>
      <tr><td>增</td><td><code>append</code> 一个元素 / <code>extend</code> 逐元素 / <code>insert</code> 指定位置</td></tr>
      <tr><td>删</td><td><code>remove</code> 按值 / <code>pop</code> 按下标并返回 / <code>del</code> / <code>clear</code></td></tr>
      <tr><td>切片</td><td>切片生成新列表；切片赋值长度可不等</td></tr>
      <tr><td>排序</td><td><code>sort</code> 原地返回 None；<code>sorted</code> 返回新列表；<code>key</code> 支持多条件</td></tr>
      <tr><td>拷贝</td><td>别名 / 浅拷贝（一层）/ <code>deepcopy</code>（递归）</td></tr>
      <tr><td>高频事故</td><td>遍历中删除、<code>[[0]*3]*3</code>、<code>sort()</code> 返回 None</td></tr>
    </tbody>
  </table>
</section>""",

"""<section id="sec8" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>写 <code>chunk(lst, n)</code>：把列表按每 n 个一组切分，如 <code>chunk([1,2,3,4,5], 2)</code> → <code>[[1,2],[3,4],[5]]</code>（用切片）。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>写 <code>dedup_keep_order(lst)</code>：去重但保持原有顺序（不许用 <code>set</code> 直接乱序）；再写 <code>top_k(lst, k)</code> 返回最大的 k 个数，要求说明你用的排序方式复杂度。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>用 <code>copy.deepcopy</code> 与浅拷贝分别处理一个三层嵌套列表，打印各自的 <code>id()</code> 证明独立性；再说明为什么函数默认参数里放可变对象会导致数据"越攒越多"（提示：第 11 章默认参数坑）。</div>
  <p class="note">参考答案见附录 C（规划中）。下一章：元组与集合——不可变与去重。</p>
</section>"""
]
},

# ════════════════════ 第 8 章 ════════════════════
{
"n": 8, "title": "元组与集合：不可变与去重",
"file": "008_第8章_元组与集合.html",
"meta": "预计 35 分钟 · 动手章",
"hero": "元组负责「不会被改的数据」，集合负责「去重与快速判断是否存在」。这两个容器一个保证安全、一个保证速度，是写出既正确又高效代码的关键工具。",
"toc": [("sec1", "本章目标"), ("sec2", "8.1 元组：不可变的列表"), ("sec3", "8.2 元组解包与多返回值"),
        ("sec4", "8.3 命名元组与类型提示"), ("sec5", "8.4 集合：去重与成员判断"),
        ("sec6", "8.5 集合运算与常见坑"), ("sec7", "本章小结"), ("sec8", "本章习题")],
"sections": [
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>理解元组的<strong>不可变性</strong>带来的两个收益：可哈希（能做字典键）、可作固定记录；</li>
    <li>掌握<strong>元组解包</strong>，包括星号解包与多返回值；</li>
    <li>会用 <code>collections.namedtuple</code> 让元组"有名字"；</li>
    <li>理解集合的<strong>哈希实现</strong>与 O(1) 成员判断；</li>
    <li>会用集合做去重、交集并集差集，并知道"元素必须可哈希"这条铁律。</li>
  </ul>
</section>""",

"""<section id="sec2" class="card">
  <h2><span class="num">8.1</span> 元组：不可变的列表</h2>
  <pre class="code" data-lang="python"><code>point = (3, 4)
single = (42,)          # 单元素元组必须带逗号！(42) 只是整数 42
print(type((42)), type((42,)))     # &lt;class 'int'&gt; &lt;class 'tuple'&gt;

print(point[0], point[-1], len(point))   # 3 4 2
point[0] = 10           # TypeError: 'tuple' object does not support item assignment

print(point + (5,))     # (3, 4, 5)   拼接生成新元组
print(point * 2)        # (3, 4, 3, 4)
print((1, 2) &lt; (1, 3))  # True  逐元素比较</code></pre>
  <p>元组的价值不在"不能改"本身，而在它带来的两个能力：</p>
  <ol>
    <li><strong>可哈希</strong>：元素都不可变时，元组能作为字典的键、集合的元素；</li>
    <li><strong>语义承诺</strong>：看到 <code>(lat, lng)</code> 就知道这是"一条固定记录"，不会被意外改写。</li>
  </ol>
  <pre class="code" data-lang="python"><code>locations = {(39.9, 116.4): "北京", (31.2, 121.5): "上海"}
print(locations[(39.9, 116.4)])      # 北京

# 元组里放可变元素 → 失去可哈希性
bad = ([1, 2], "x")
# {bad: 1}  → TypeError: unhashable type: 'list'</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span>"元组不可变"指的是<strong>它装的元素引用不可变</strong>——如果元素本身是列表，这个列表的内容照样能改：<code>t = ([1],); t[0].append(2)</code> 是合法的。</div>
</section>""",

"""<section id="sec3" class="card">
  <h2><span class="num">8.2</span> 元组解包与多返回值</h2>
  <p>解包（unpacking）是 Python 最优雅的语法之一：</p>
  <pre class="code" data-lang="python"><code>x, y = (3, 4)
print(x, y)                    # 3 4

a, b = b, a                    # 交换变量，无需临时变量

# 星号解包：把"剩下的"收进列表
first, *rest = [1, 2, 3, 4]
print(first, rest)             # 1 [2, 3, 4]

head, *mid, tail = [1, 2, 3, 4]
print(head, mid, tail)         # 1 [2, 3] 4

# 函数返回多个值，本质是返回一个元组
def divmod_plus(a, b):
    return a // b, a % b, a / b

q, r, exact = divmod_plus(7, 2)
print(q, r, exact)             # 3 1 3.5

# 忽略某些返回值（约定用 _）
name, _, age = ("张三", "ignore", 18)</code></pre>
  <p>遍历字典、enumerate 结果时也在大量使用解包：</p>
  <pre class="code" data-lang="python"><code>users = {"a": 1, "b": 2}
for key, value in users.items():
    print(key, value)

pairs = [(1, "one"), (2, "two")]
for num, word in pairs:
    print(num, word)</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span>解包时<strong>左右数量必须一致</strong>，否则抛 <code>ValueError</code>；不确定长度时用 <code>*</code> 收集，或用 <code>_, _</code> 显式忽略。</div>
</section>""",

"""<section id="sec4" class="card">
  <h2><span class="num">8.3</span> 命名元组与类型提示</h2>
  <p>普通元组靠下标取值，可读性差。<code>namedtuple</code> 给每个位置起个名字，同时保留元组的全部特性： </p>
  <pre class="code" data-lang="python"><code>from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)

print(p.x, p.y)           # 3 4     ← 属性访问
print(p[0], p == (3, 4))  # 3 True  ← 仍是元组，可下标、可比较
print(p._replace(x=10))   # Point(x=10, y=4)   生成新实例（不可变）

# 用在函数返回值上，可读性立刻提升
def get_user():
    User = namedtuple("User", "id name is_vip")
    return User(1, "张三", True)

u = get_user()
if u.is_vip:
    print(u.name)</code></pre>
  <p class="key-sentence">选型建议：临时小结构用 <code>namedtuple</code>；需要默认值、可变性或方法时，直接用第 22 章的 <code>dataclass</code>——它更现代、更强大。</p>
  <div class="note">Python 3.5+ 的类型注解写法：<code>tuple[int, str]</code> 表示"二元组，第一个 int 第二个 str"；<code>tuple[int, ...]</code> 表示"任意长度的整数元组"（第 35 章详述）。</div>
</section>""",

"""<section id="sec5" class="card">
  <h2><span class="num">8.4</span> 集合：去重与成员判断</h2>
  <p>集合（set）是<strong>无序、元素唯一、必须可哈希</strong>的容器，底层是哈希表：判断"在不在里面"平均 O(1)，而列表是 O(n)。</p>
  <pre class="code" data-lang="python"><code>nums = {1, 2, 3, 3, 2}
print(nums)                  # {1, 2, 3}   自动去重

empty = set()                # 空集合只能用 set()；{} 是空字典！
from_list = set([1, 2, 2, 3])
from_str = set("hello")      # {'h', 'e', 'l', 'o'}   字符去重

nums.add(4)
nums.discard(99)             # 不存在也不报错
# nums.remove(99)            # 不存在则抛 KeyError

print(2 in nums)             # True   O(1) 判断
print(len(nums))</code></pre>
  <p>性能对比能直观说明"为什么该用集合"：</p>
  <pre class="code" data-lang="python"><code>import timeit
big_list = list(range(100_000))
big_set = set(big_list)

print(timeit.timeit(lambda: 99_999 in big_list, number=1000))  # 约 0.05s
print(timeit.timeit(lambda: 99_999 in big_set,  number=1000))  # 约 0.00005s</code></pre>
  <p class="key-sentence">凡是"反复判断某个值是否在一堆值里"的场景（白名单、已处理 ID、权限点），一律换成 set——这是投入产出比最高的一处优化。</p>
  <div class="danger-box"><span class="tag-pit">铁律</span>集合元素必须<strong>可哈希</strong>：int、float、str、tuple（元素全不可变）、frozenset 可以；<strong>list、dict、set 不行</strong>。想放列表进去，先转成 <code>tuple</code>。</div>
</section>""",

"""<section id="sec6" class="card">
  <h2><span class="num">8.5</span> 集合运算与常见坑</h2>
  <table>
    <colgroup><col style="width:26%"><col style="width:38%"><col style="width:36%"></colgroup>
    <thead><tr><th>运算</th><th>运算符 / 方法</th><th>含义</th></tr></thead>
    <tbody>
      <tr><td>交集</td><td><code>a &amp; b</code> / <code>a.intersection(b)</code></td><td>同时存在于两者</td></tr>
      <tr><td>并集</td><td><code>a | b</code> / <code>a.union(b)</code></td><td>两者所有元素</td></tr>
      <tr><td>差集</td><td><code>a - b</code> / <code>a.difference(b)</code></td><td>在 a 不在 b</td></tr>
      <tr><td>对称差</td><td><code>a ^ b</code> / <code>symmetric_difference</code></td><td>只在一个里出现</td></tr>
      <tr><td>子集/超集</td><td><code>a &lt;= b</code> / <code>a.issubset(b)</code></td><td>包含关系判断</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="python"><code>a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(a &amp; b)      # {3, 4}
print(a | b)      # {1, 2, 3, 4, 5, 6}
print(a - b)      # {1, 2}
print(a ^ b)      # {1, 2, 5, 6}
print({1, 2} &lt;= a) # True  子集
print(a.isdisjoint({9, 10}))  # True  无交集

# 典型用法：找出两个列表的差异
old = ["a", "b", "c"]
new = ["b", "c", "d"]
print("新增:", set(new) - set(old))    # {'d'}
print("移除:", set(old) - set(new))    # {'a'}

# 冻结集合：不可变的 set，可作为字典键
frozen = frozenset([1, 2, 3])</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span><strong>集合无序</strong>：不要依赖遍历顺序做逻辑（顺序由哈希决定），需要稳定顺序时用 <code>sorted(集合)</code>。另外 <code>set</code> 的去重结果顺序与输入顺序无关，想"去重且保序"请用 <code>dict.fromkeys</code>（第 9 章）。</div>
</section>""",

"""<section id="sec7" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:34%"><col style="width:66%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>元组</td><td>不可变序列；可哈希、可作字典键；单元素要带逗号</td></tr>
      <tr><td>元组可变性陷阱</td><td>不变的是引用；内嵌列表的内容仍可改</td></tr>
      <tr><td>解包</td><td><code>a, b = b, a</code>；<code>head, *rest = ...</code>；函数多返回值本质即元组</td></tr>
      <tr><td>namedtuple</td><td>给位置起名字，保留元组特性；复杂结构用 dataclass</td></tr>
      <tr><td>集合</td><td>无序唯一、元素可哈希；成员判断 O(1)</td></tr>
      <tr><td>集合运算</td><td><code>&amp; | - ^</code> 交并差对称差；<code>&lt;=</code> 子集</td></tr>
      <tr><td>铁律</td><td>list / dict / set 不可哈希，不能当集合元素或字典键</td></tr>
    </tbody>
  </table>
</section>""",

"""<section id="sec8" class="card">
  <h2><span class="ex-tag">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>写 <code>swap_pairs(lst)</code>：把 <code>[1,2,3,4]</code> 变成 <code>[2,1,4,3]</code>，要求用元组解包而非临时变量。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>给定两份用户 ID 列表（各 1 万个），统计"新增用户数""流失用户数""留存用户数"，要求用集合运算并说明为什么它比列表循环快得多。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>实现 <code>dedup_stable(items)</code>：去重且保持输入顺序，元素可能是不可哈希的字典——请给出两种方案（可哈希时用 <code>dict.fromkeys</code>，不可哈希时用 JSON 序列化做指纹），并说明各自的局限。</div>
  <p class="note">参考答案见附录 C（规划中）。下一章：字典——Python 最重要的容器。</p>
</section>"""
]
},

# ════════════════════ 第 9 章 ════════════════════
{
"n": 9, "title": "字典：键值映射与遍历",
"file": "009_第9章_字典.html",
"meta": "预计 50 分钟 · 动手章 · 第一篇收官",
"hero": "字典是 Python 的心脏：对象属性、模块命名空间、JSON 数据、函数关键字参数，底层全是它。本章讲透增删改查、安全取值、遍历技巧、3.7+ 的有序性保证与 3.9 的合并运算符，并给出第一篇的知识收束。",
"toc": [("sec1", "本章目标"), ("sec2", "9.1 字典的本质与创建"), ("sec3", "9.2 增删改查与安全取值"),
        ("sec4", "9.3 遍历：keys / values / items"), ("sec5", "9.4 高级：默认值、合并、排序、嵌套"),
        ("sec6", "9.5 底层原理与常见坑"), ("sec7", "第一篇小结"), ("sec8", "本章习题")],
"sections": [
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>理解字典是<strong>键值对映射</strong>，键必须可哈希，3.7+ 保证<strong>插入顺序</strong>；</li>
    <li>会用 <code>get</code>、<code>setdefault</code>、<code>defaultdict</code> 写出不抛异常的取值代码；</li>
    <li>掌握三套遍历方式与"遍历中不能改大小"的铁律；</li>
    <li>掌握 3.9 合并运算符 <code>|</code>、字典推导式、按值排序；</li>
    <li>知道字典底层是哈希表，以及它带来的复杂度与限制。</li>
  </ul>
</section>""",

"""<section id="sec2" class="card">
  <h2><span class="num">9.1</span> 字典的本质与创建</h2>
  <pre class="code" data-lang="python"><code>user = {"name": "张三", "age": 18, "vip": True}
empty = {}
from_pairs = dict([("a", 1), ("b", 2)])      # {'a': 1, 'b': 2}
from_kwargs = dict(name="李四", age=20)      # 关键字形式，键自动成字符串
from_keys = dict.fromkeys(["a", "b"], 0)     # {'a': 0, 'b': 0}  批量同默认值

print(user["name"])        # 张三
print(len(user))           # 3
print("age" in user)       # True  判断的是键</code></pre>
  <p>键的要求与限制：</p>
  <ul>
    <li>键必须<strong>可哈希</strong>（同集合）：str、int、tuple（元素全不可变）常用，list/dict/set 不行；</li>
    <li>值<strong>没有限制</strong>，可以是任意对象，包括列表、另一个字典、函数；</li>
    <li>Python <strong>3.7+</strong> 正式保证：字典保持<strong>插入顺序</strong>（3.6 的 CPython 实现已如此，3.7 起成为语言规范）。</li>
  </ul>
  <pre class="code" data-lang="python"><code># 值可以是任何东西
config = {"hosts": ["a", "b"], "retry": {"max": 3}, "on_error": print}

# 常用：用元组做复合键
scores = {("张三", "数学"): 95, ("张三", "英语"): 88}
print(scores[("张三", "数学")])     # 95</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span><code>dict.fromkeys(["a","b"], [])</code> 会让所有键<strong>共享同一个列表</strong>。要各自独立的默认值，用推导式 <code>{k: [] for k in keys}</code> 或 <code>defaultdict(list)</code>。</div>
</section>""",

"""<section id="sec3" class="card">
  <h2><span class="num">9.2</span> 增删改查与安全取值</h2>
  <pre class="code" data-lang="python"><code>d = {"a": 1, "b": 2}

d["c"] = 3                 # 增 / 改（键存在即改）
d.update({"d": 4, "a": 10})  # 批量更新
print(d)                   # {'a': 10, 'b': 2, 'c': 3, 'd': 4}

del d["d"]                 # 删（不存在抛 KeyError）
removed = d.pop("c")       # 删并返回值
d.pop("zz", None)          # 带默认值，不存在也不报错
last = d.popitem()         # 弹出最后插入的一对（LIFO）
d.clear()                  # 清空</code></pre>
  <h4>安全取值：三件套</h4>
  <pre class="code" data-lang="python"><code>d = {"a": 1}

# ① get：取不到给默认值（最常用）
print(d.get("a"), d.get("zz"), d.get("zz", 0))   # 1 None 0

# ② setdefault：取不到就"设进去再返回"（适合分组累加）
groups = {}
for item in ["a", "b", "a"]:
    groups.setdefault(item, []).append(item)
print(groups)              # {'a': ['a', 'a'], 'b': ['b']}

# ③ collections.defaultdict：给所有缺失键一个工厂函数
from collections import defaultdict
counter = defaultdict(int)
for ch in "abracadabra":
    counter[ch] += 1       # 无需先判断键是否存在
print(dict(counter))       # {'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1}</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span><code>setdefault</code> 每次都会<strong>先构造默认值对象</strong>（哪怕是空列表），在热路径上有额外开销；且它把默认值写进字典，可能污染后续判断。分组累加优先用 <code>defaultdict</code> 或第 27 章的 <code>Counter</code>。</div>
</section>""",

"""<section id="sec4" class="card">
  <h2><span class="num">9.3</span> 遍历：keys / values / items</h2>
  <pre class="code" data-lang="python"><code>user = {"name": "张三", "age": 18, "city": "北京"}

for k in user:                  # 默认遍历键
    print(k)

for k in user.keys():           # 同上，显式写法
    print(k)

for v in user.values():         # 只要值
    print(v)

for k, v in user.items():       # 键值一起（最常用，用解包）
    print(f"{k} = {v}")</code></pre>
  <p>视图对象（view）是<strong>动态</strong>的：字典变了，视图跟着变。</p>
  <pre class="code" data-lang="python"><code>keys = user.keys()
user["gender"] = "男"
print(list(keys))          # ['name', 'age', 'city', 'gender']  视图随之更新</code></pre>
  <div class="danger-box"><span class="tag-pit">铁律</span><strong>遍历过程中不能改变字典大小</strong>（增/删键），否则抛 <code>RuntimeError: dictionary changed size during iteration</code>。需要过滤时遍历副本或生成新字典：</div>
  <pre class="code" data-lang="python"><code># 错误
for k in d:
    if d[k] is None:
        del d[k]           # RuntimeError

# 正确一：遍历键的快照
for k in list(d):
    if d[k] is None:
        del d[k]

# 正确二（推荐）：字典推导式生成新字典
d = {k: v for k, v in d.items() if v is not None}</code></pre>
</section>""",

"""<section id="sec5" class="card">
  <h2><span class="num">9.4</span> 高级：默认值、合并、排序、嵌套</h2>
  <h4>合并：3.9+ 的 <code>|</code> 运算符</h4>
  <pre class="code" data-lang="python"><code>base = {"host": "localhost", "port": 8000, "debug": False}
override = {"port": 9000, "debug": True}

merged = base | override        # 后者覆盖前者，生成新字典
print(merged)                   # {'host': 'localhost', 'port': 9000, 'debug': True}

base |= override                # 原地合并

# 老写法（3.5+）：{**a, **b}
print({**base, **override})</code></pre>
  <h4>字典推导式与按值排序</h4>
  <pre class="code" data-lang="python"><code># 推导式：键值互换、过滤、变换
squares = {x: x ** 2 for x in range(5)}          # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
filtered = {k: v for k, v in squares.items() if v % 2 == 0}
inverted = {v: k for k, v in squares.items()}    # 值必须唯一，否则后者覆盖

# 按值排序：key 取元组第 1 项
scores = {"张三": 95, "李四": 88, "王五": 95}
for name, score in sorted(scores.items(), key=lambda kv: (-kv[1], kv[0])):
    print(name, score)          # 王五 95 / 张三 95 / 李四 88（同分按姓名）</code></pre>
  <h4>嵌套结构的安全访问</h4>
  <pre class="code" data-lang="python"><code># 深层取值：一层层判空很啰嗦
data = {"user": {"profile": {"city": "北京"}}}

city = data.get("user", {}).get("profile", {}).get("city", "未知")
print(city)        # 北京；任一层缺失都不会抛异常</code></pre>
  <p class="key-sentence">字典是 JSON 的天然映射：<code>json.loads</code> 出来的就是嵌套字典 + 列表（第 26 章）。处理 API 报文时，<code>get</code> 链 + 类型检查是最实用的防御写法。</p>
</section>""",

"""<section id="sec6" class="card">
  <h2><span class="num">9.5</span> 底层原理与常见坑</h2>
  <p>字典基于<strong>哈希表</strong>实现：对键调用 <code>hash()</code> 得到桶位置，因此：</p>
  <table>
    <colgroup><col style="width:30%"><col style="width:36%"><col style="width:34%"></colgroup>
    <thead><tr><th>操作</th><th>平均复杂度</th><th>说明</th></tr></thead>
    <tbody>
      <tr><td>按键取值 / 赋值</td><td>O(1)</td><td>这就是为什么"用字典做索引"能极大提速</td></tr>
      <tr><td>成员判断 <code>k in d</code></td><td>O(1)</td><td>列表是 O(n)</td></tr>
      <tr><td>遍历</td><td>O(n)</td><td>3.7+ 按插入顺序</td></tr>
      <tr><td>内存开销</td><td>较大</td><td>哈希表需要预留空间，约为元素数的 1/3 闲置</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="python"><code># 经典优化：把"列表里找对象"改成"字典里取对象"
users_list = [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}]
target = next((u for u in users_list if u["id"] == 2), None)   # O(n)

users_index = {u["id"]: u for u in users_list}                 # 建索引 O(n)
print(users_index[2])                                          # 之后每次 O(1)</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span>① <code>d[k]</code> 取不存在的键抛 <code>KeyError</code>，不确定时用 <code>get</code>；② 键的大小写敏感（<code>"Name"</code> 与 <code>"name"</code> 是两个键）；③ 用 <code>1</code> 和 <code>True</code> 当键会冲突（<code>hash(True) == hash(1)</code>）；④ 遍历中禁止改大小。</div>
</section>""",

"""<section id="sec7" class="card">
  <h2><span class="num">✓</span> 第一篇小结</h2>
  <p>入门与语法篇（第 1-9 章）到此结束。请把下面这张"容器选型表"记牢，后面 50 章反复要用：</p>
  <table>
    <colgroup><col style="width:16%"><col style="width:22%"><col style="width:34%"><col style="width:28%"></colgroup>
    <thead><tr><th>容器</th><th>有序 / 可变</th><th>典型用途</th><th>关键操作复杂度</th></tr></thead>
    <tbody>
      <tr><td><code>str</code></td><td>有序 / 不可变</td><td>文本、路径、报文</td><td>切片 O(k)、查找 O(n)</td></tr>
      <tr><td><code>list</code></td><td>有序 / 可变</td><td>序列数据、栈</td><td>下标 O(1)、头部插删 O(n)</td></tr>
      <tr><td><code>tuple</code></td><td>有序 / 不可变</td><td>固定记录、字典键</td><td>同 list 的只读版</td></tr>
      <tr><td><code>set</code></td><td>无序 / 可变</td><td>去重、成员判断</td><td>in / add O(1)</td></tr>
      <tr><td><code>dict</code></td><td>插入序 / 可变</td><td>键值映射、索引、JSON</td><td>取值 O(1)</td></tr>
    </tbody>
  </table>
  <p>三句话复习全篇：</p>
  <ol>
    <li><strong>名字贴对象</strong>：赋值不复制，可变对象被别名共享（第 3 章）；</li>
    <li><strong>遍历中别改容器</strong>：列表用副本或推导式，字典用 <code>list(d)</code> 快照（第 6、9 章）；</li>
    <li><strong>查得快用哈希</strong>：反复判断"在不在"就用 set/dict，别用 list（第 8、9 章）。</li>
  </ol>
  <p class="key-sentence">接下来第二篇《函数与进阶语法》要把这些"能跑的代码"变成"好用的代码"——函数、参数、闭包、推导式、生成器、装饰器、异常处理、模块体系。</p>
</section>""",

"""<section id="sec8" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>写 <code>word_count(text)</code>：统计每个单词出现次数，返回字典（用 <code>defaultdict(int)</code> 或 <code>Counter</code> 均可，并比较两种写法）。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>写 <code>group_by(items, key_func)</code>：按 key_func 的返回值把列表分组，如按城市分组用户；再写 <code>invert_dict(d)</code>，把值相同的键聚成列表（处理重复值）。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>有两个各含 10 万条记录的列表（都有 <code>id</code> 字段），需要找出 id 相同但内容不同的记录。请分别用"双重循环"和"字典建索引"实现，用 <code>time.perf_counter()</code> 测出差距，并说明复杂度从 O(n²) 降到 O(n) 的原因。</div>
  <p class="note">参考答案见附录 C（规划中）。下一篇：第 10 章 函数——把能跑的代码变成好用的代码。</p>
</section>"""
]
}
]

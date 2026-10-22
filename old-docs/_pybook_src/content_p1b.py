# -*- coding: utf-8 -*-
"""第一篇 入门与语法 · 第 4-6 章"""

PART_DIR = "10_第一篇_入门与语法"
PART_NAME = "第一篇 入门与语法"

CHAPTERS = [
# ════════════════════ 第 4 章 ════════════════════
{
"n": 4, "title": "字符串深入：方法与 f-string",
"file": "004_第4章_字符串深入.html",
"meta": "预计 45 分钟 · 动手章",
"hero": "字符串是 Python 里方法最多、用得最勤的类型：日志、路径、接口报文、SQL、配置，处处是它。本章把「不可变序列」的性质、几十个常用方法、三套格式化写法（重点 f-string）以及 UTF-8 编码坑一次讲透。",
"toc": [("sec1", "本章目标"), ("sec2", "4.1 字符串是不可变序列"), ("sec3", "4.2 常用方法速查"),
        ("sec4", "4.3 格式化三剑客"), ("sec5", "4.4 f-string 高级用法"),
        ("sec6", "4.5 编码、字节与常见坑"), ("sec7", "本章小结"), ("sec8", "本章习题")],
"sections": [
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>理解字符串的<strong>不可变性</strong>与<strong>序列性</strong>（可索引、可切片、可遍历）；</li>
    <li>掌握 20 个高频方法，做到"要处理字符串时知道该翻哪个"；</li>
    <li>会用 <strong>f-string</strong> 完成 95% 的格式化需求，包括数字精度、对齐、调试输出；</li>
    <li>分清 <code>str</code> 与 <code>bytes</code>，读写文件指定 <code>encoding="utf-8"</code>；</li>
    <li>避开"拼接字符串用 <code>+</code> 写在循环里"这类性能陷阱。</li>
  </ul>
</section>""",

"""<section id="sec2" class="card">
  <h2><span class="num">4.1</span> 字符串是不可变序列</h2>
  <p>字符串支持索引与切片，但<strong>任何"修改"都会生成新字符串</strong>：</p>
  <pre class="code" data-lang="python"><code>s = "Python"
print(s[0], s[-1], s[2:4], s[::-1])   # P n th nohtyP
print(len(s))                          # 6

s[0] = "p"        # TypeError: 'str' object does not support item assignment
s = "p" + s[1:]   # 正确：构造新字符串</code></pre>
  <p>切片语法 <code>s[start:stop:step]</code> 的三要素：</p>
  <ul>
    <li><code>start</code> 包含，<code>stop</code> <strong>不包含</strong>——这是"前闭后开"，让 <code>s[:n] + s[n:]</code> 恒等于 <code>s</code>；</li>
    <li>索引可为负：<code>-1</code> 是最后一个字符；</li>
    <li><code>step</code> 为负表示倒着取，<code>s[::-1]</code> 是最简洁的反转写法。</li>
  </ul>
  <pre class="code" data-lang="python"><code>text = "2026-10-19"
print(text[:4], text[5:7], text[8:])   # 2026 10 19
print("abcdef"[1:5:2])                 # bd
print("abcdef"[::2])                   # ace
print("abcdef"[-3:])                   # def</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span>切片<strong>越界不报错</strong>（<code>"abc"[0:100]</code> 返回 <code>"abc"</code>），但<strong>索引越界会报错</strong>（<code>"abc"[10]</code> → IndexError）。做校验时别依赖切片报错。</div>
  <p>遍历与成员判断：</p>
  <pre class="code" data-lang="python"><code>for ch in "abc":
    print(ch, end=" ")        # a b c

print("ython" in "Python")    # True
print("JAVA" in "Python")     # False（区分大小写）</code></pre>
</section>""",

"""<section id="sec3" class="card">
  <h2><span class="num">4.2</span> 常用方法速查</h2>
  <p>Python 字符串有四十多个方法，按用途分组记最快：</p>
  <table>
    <colgroup><col style="width:22%"><col style="width:44%"><col style="width:34%"></colgroup>
    <thead><tr><th>分组</th><th>方法</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>大小写</td><td><code>upper/lower/title/capitalize/swapcase</code></td><td>大小写转换，常用于忽略大小写比较</td></tr>
      <tr><td>去空白</td><td><code>strip/lstrip/rstrip</code></td><td>去掉首尾空白，可传字符集</td></tr>
      <tr><td>切分合并</td><td><code>split/rsplit/splitlines/partition/join</code></td><td>字符串 ↔ 列表</td></tr>
      <tr><td>查找替换</td><td><code>find/index/replace/count</code></td><td><code>find</code> 找不到返回 -1，<code>index</code> 抛异常</td></tr>
      <tr><td>判断</td><td><code>startswith/endswith/isdigit/isalpha/isspace</code></td><td>返回 bool，常用于校验</td></tr>
      <tr><td>填充对齐</td><td><code>zfill/ljust/rjust/center</code></td><td>补零与对齐输出</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="python"><code>raw = "  Python,Java,Go  "

print(raw.strip())                     # 'Python,Java,Go'
print(raw.strip().split(","))          # ['Python', 'Java', 'Go']
print(", ".join(["a", "b", "c"]))      # 'a, b, c'

s = "hello world"
print(s.startswith("he"), s.endswith("ld"))   # True True
print(s.find("wo"), s.find("zz"))             # 6 -1
print(s.replace("world", "Python"))           # 'hello Python'
print(s.count("l"))                           # 3
print(s.title())                              # 'Hello World'

print("42".isdigit(), "abc".isalpha())        # True True
print("7".zfill(3), "x".center(5, "-"))       # 007 --x--

# 多行文本：splitlines 与三引号
doc = '''第一行
第二行'''
print(doc.splitlines())                # ['第一行', '第二行']</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span><strong>循环里用 <code>+</code> 拼接字符串是 O(n²)</strong>——每次都生成新对象。正确做法是先收集到列表，最后一次 <code>join</code>：</div>
  <pre class="code" data-lang="python"><code># 反例：数据量大时非常慢
result = ""
for i in range(100_000):
    result += str(i)

# 正例：O(n)
parts = [str(i) for i in range(100_000)]
result = "".join(parts)</code></pre>
</section>""",

"""<section id="sec4" class="card">
  <h2><span class="num">4.3</span> 格式化三剑客</h2>
  <p>Python 历史上有三套字符串格式化方式，今天只需记住一个结论：<strong>新代码一律用 f-string</strong>，另外两种能读懂即可。</p>
  <table>
    <colgroup><col style="width:24%"><col style="width:40%"><col style="width:36%"></colgroup>
    <thead><tr><th>方式</th><th>写法</th><th>评价</th></tr></thead>
    <tbody>
      <tr><td>% 运算符</td><td><code>"%s 有 %d 元" % (name, money)</code></td><td>最老，来自 C，日志模块仍在用</td></tr>
      <tr><td>str.format</td><td><code>"{} 有 {} 元".format(name, money)</code></td><td>功能强，但冗长</td></tr>
      <tr><td>f-string（推荐）</td><td><code>f"{name} 有 {money} 元"</code></td><td>3.6+，最快最直观，可内联表达式</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="python"><code>name, money, rate = "张三", 1234.5, 0.8765

print("%s 有 %.2f 元" % (name, money))              # 张三 有 1234.50 元
print("{} 有 {:.2f} 元".format(name, money))        # 张三 有 1234.50 元
print(f"{name} 有 {money:.2f} 元")                  # 张三 有 1234.50 元  ← 推荐

# f-string 里可以直接写表达式与调用
print(f"税率 {rate:.1%}")                           # 税率 87.6%
print(f"{name.upper()} 明年有 {money * 1.05:.0f} 元")
print(f"列表长度：{len([1, 2, 3])}")</code></pre>
  <p>日志场景保留 % 风格是有原因的——<strong>延迟格式化</strong>：</p>
  <pre class="code" data-lang="python"><code>import logging
logging.warning("用户 %s 登录失败", name)   # 只在真正输出时才格式化
logging.warning(f"用户 {name} 登录失败")     # 即使日志级别不输出，也先拼好了字符串</code></pre>
</section>""",

"""<section id="sec5" class="card">
  <h2><span class="num">4.4</span> f-string 高级用法</h2>
  <p>f-string 的完整语法是 <code>f"{表达式!转换:格式规范}"</code>，其中"格式规范"沿用 <code>str.format</code> 的迷你语言：</p>
  <pre class="code" data-lang="python"><code>value = 12345.6789
name = "bob"

print(f"{value:,.2f}")        # 12,345.68      千分位 + 两位小数
print(f"{value:>15.2f}")      # '       12345.68'  右对齐宽度 15
print(f"{name:<10}|")         # 'bob       |'      左对齐
print(f"{name:*^10}")         # '***bob****'       居中填充 *
print(f"{255:#x} {255:#b}")   # 0xff 0b11111111    进制与前缀
print(f"{0.8765:.2%}")        # 87.65%             百分比
print(f"{value:.2e}")         # 1.23e+04           科学计数法</code></pre>
  <h4>3.8 起的调试神器：<code>=</code></h4>
  <pre class="code" data-lang="python"><code>x, y = 10, 20
print(f"{x + y = }")      # x + y = 30
print(f"{x = }, {y = }")  # x = 10, y = 20

# 转换标志 !r / !s / !a
text = "a\\nb"
print(f"{text!r}")        # 'a\\nb'   调用 repr，调试时看转义最方便
print(f"{text!s}")        # a
b                         # 调用 str</code></pre>
  <h4>多行 f-string 与日期格式化</h4>
  <pre class="code" data-lang="python"><code>from datetime import datetime

user = {"name": "张三", "age": 18}
now = datetime(2026, 10, 19, 14, 30)

msg = (
    f"用户：{user['name']}\\n"
    f"年龄：{user['age']}\\n"
    f"时间：{now:%Y-%m-%d %H:%M}"
)
print(msg)</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span>3.12 之前 f-string 内部<strong>不能</strong>使用与外層相同的引号（<code>f"{d["k"]}"</code> 报错），需换成单引号或改用中间变量；3.12+ 已放宽此项限制。</div>
</section>""",

"""<section id="sec6" class="card">
  <h2><span class="num">4.5</span> 编码、字节与常见坑</h2>
  <p>两条铁律：<strong>程序内部一律用 <code>str</code>（Unicode）；进出外界（文件、网络）才编码成 <code>bytes</code></strong>。</p>
  <pre class="code" data-lang="python"><code>s = "中文"
b = s.encode("utf-8")        # str → bytes
print(b, len(b))             # b'\\xe4\\xb8\\xad\\xe6\\x96\\x87' 6   （一个汉字 3 字节）
print(b.decode("utf-8"))     # bytes → str：'中文'

# 字节前缀与原始字符串
print(b"abc"[0])             # 97  字节是 0-255 的整数序列
print(r"C:\\new\\test")       # 原始字符串：反斜杠不转义</code></pre>
  <table>
    <colgroup><col style="width:26%"><col style="width:40%"><col style="width:34%"></colgroup>
    <thead><tr><th>概念</th><th>含义</th><th>典型场景</th></tr></thead>
    <tbody>
      <tr><td>字符（str）</td><td>Unicode 码位序列，"字"是 1 个字符</td><td>程序内部处理</td></tr>
      <tr><td>字节（bytes）</td><td>0-255 的整数序列，"字"在 UTF-8 下是 3 字节</td><td>文件、网络、加密</td></tr>
      <tr><td>编码格式</td><td>字符 ↔ 字节的映射表</td><td>UTF-8（默认）、GBK（老系统）</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="python"><code># 读写文件永远显式指定编码（第 25 章详述）
with open("data.txt", "w", encoding="utf-8") as f:
    f.write("中文内容")

with open("data.txt", encoding="utf-8") as f:
    print(f.read())</code></pre>
  <div class="danger-box"><span class="tag-pit">高频事故</span>Windows 上不写 <code>encoding="utf-8"</code> 时，默认用系统本地编码（GBK），换台电脑打开就是乱码或 <code>UnicodeDecodeError</code>。把"写文件必带 encoding"练成肌肉记忆。</div>
  <p>其他高频小技巧：</p>
  <pre class="code" data-lang="python"><code># 去掉多行缩进：textwrap.dedent
from textwrap import dedent
sql = dedent('''
    SELECT id, name
    FROM users
    WHERE id = 1
''').strip()
print(sql)

# 模板字符串：用户输入做模板时用 Template 更安全
from string import Template
print(Template("$who 有 $n 元").substitute(who="张三", n=10))</code></pre>
</section>""",

"""<section id="sec7" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:34%"><col style="width:66%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>性质</td><td>不可变的字符序列；可索引切片，"改"= 造新的</td></tr>
      <tr><td>切片</td><td><code>s[start:stop:step]</code>，前闭后开，越界不报错，<code>[::-1]</code> 反转</td></tr>
      <tr><td>方法</td><td>strip / split / join / replace / find / startswith / isdigit 最高频</td></tr>
      <tr><td>格式化</td><td>新代码用 f-string；日志用 % 风格（延迟格式化）</td></tr>
      <tr><td>格式规范</td><td><code>{值:,.2f}</code> 千分位、<code>{x = }</code> 调试、<code>{d:%Y-%m-%d}</code> 日期</td></tr>
      <tr><td>编码</td><td>内部 str、外部 bytes；读写文件显式 <code>encoding="utf-8"</code></td></tr>
      <tr><td>性能坑</td><td>循环里别用 <code>+</code> 拼接，用列表 + <code>join</code></td></tr>
    </tbody>
  </table>
</section>""",

"""<section id="sec8" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>给定 <code>path = "/var/log/app/server.log"</code>，分别取出文件名 <code>server.log</code>、目录 <code>/var/log/app</code>、扩展名 <code>log</code>（提示：<code>rsplit</code> 或第 26 章的 <code>pathlib</code>）。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>写函数 <code>fmt_money(cents: int) -&gt; str</code>：输入分（整数），输出形如 <code>¥1,234.50</code> 的字符串；再写 <code>mask_phone(p)</code>，把 <code>13812345678</code> 变成 <code>138****5678</code>。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>把一段 5000 行的文本用"循环 += "与"列表 + join"两种方式拼接，用 <code>time.perf_counter()</code> 测出耗时差距，并解释原因（提示：不可变对象的重复复制）。</div>
  <p class="note">参考答案见附录 C（规划中）。下一章进入运算符与表达式。</p>
</section>"""
]
},

# ════════════════════ 第 5 章 ════════════════════
{
"n": 5, "title": "运算符与表达式",
"file": "005_第5章_运算符与表达式.html",
"meta": "预计 35 分钟 · 动手章",
"hero": '表达式是程序的最小计算单元。本章把 Python 的七类运算符梳理成一张表，重点讲三个"Python 味"很浓的特性：链式比较、and/or 的返回值、以及 3.8 新增的海象运算符——它们能显著缩短代码，也最容易被误用。',
"toc": [("sec1", "本章目标"), ("sec2", "5.1 七类运算符一览"), ("sec3", "5.2 链式比较与短路求值"),
        ("sec4", "5.3 and / or 的返回值"), ("sec5", "5.4 海象运算符 :="),
        ("sec6", "5.5 优先级与可读性"), ("sec7", "本章小结"), ("sec8", "本章习题")],
"sections": [
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>掌握七类运算符：算术、比较、逻辑、赋值、成员、身份、位运算；</li>
    <li>会用<strong>链式比较</strong>写出更贴近数学的表达式；</li>
    <li>理解 <code>and</code> / <code>or</code> 返回的是<strong>操作数而非布尔值</strong>，并能用它写默认值；</li>
    <li>知道<strong>海象运算符</strong> <code>:=</code> 解决什么问题、什么时候不该用；</li>
    <li>用括号而不是背优先级表来写代码。</li>
  </ul>
</section>""",

"""<section id="sec2" class="card">
  <h2><span class="num">5.1</span> 七类运算符一览</h2>
  <table>
    <colgroup><col style="width:18%"><col style="width:44%"><col style="width:38%"></colgroup>
    <thead><tr><th>类别</th><th>运算符</th><th>说明</th></tr></thead>
    <tbody>
      <tr><td>算术</td><td><code>+ - * / // % **</code></td><td><code>**</code> 是幂；<code>//</code> 向下取整；<code>%</code> 结果与除数同号</td></tr>
      <tr><td>比较</td><td><code>== != &lt; &gt; &lt;= &gt;=</code></td><td>可链式书写：<code>1 &lt; x &lt; 10</code></td></tr>
      <tr><td>逻辑</td><td><code>and or not</code></td><td>用英文单词而非符号</td></tr>
      <tr><td>成员</td><td><code>in</code>、<code>not in</code></td><td>容器/字符串是否包含元素</td></tr>
      <tr><td>身份</td><td><code>is</code>、<code>is not</code></td><td>是否同一个对象（判 None 专用）</td></tr>
      <tr><td>赋值</td><td><code>= += -= *= /= //= %= **= :=</code></td><td>复合赋值对可变对象是原地操作</td></tr>
      <tr><td>位运算</td><td><code>&amp; | ^ ~ &lt;&lt; &gt;&gt;</code></td><td>权限位、标志位场景</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="python"><code>print(2 ** 10)            # 1024
print(-7 // 2, 7 // -2)   # -4 -4   向下取整（向负无穷），非"截断"
print(-7 % 3)             # 2       结果与除数同号
print(divmod(7, 3))       # (2, 1)

# 复合赋值：可变对象原地改，不可变对象换新
lst = [1]; lst += [2]; print(lst)    # [1, 2]
n = 1;    n += 1                     # 等价于 n = n + 1

# 位运算：权限位示例
READ, WRITE, EXEC = 4, 2, 1
perm = READ | WRITE                  # 6
print(bool(perm &amp; READ), bool(perm &amp; EXEC))   # True False</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span><code>a += b</code> 对可变对象是<strong>原地修改</strong>（<code>list</code>、<code>dict</code>、<code>set</code>），因此对别名可见；而 <code>a = a + b</code> 一定生成新对象。第 11 章的默认参数坑就源于此。</div>
</section>""",

"""<section id="sec3" class="card">
  <h2><span class="num">5.2</span> 链式比较与短路求值</h2>
  <p>Python 允许把比较连着写，语义与数学完全一致，这是它"像伪代码"的典型体现：</p>
  <pre class="code" data-lang="python"><code>x = 5
print(1 &lt; x &lt; 10)              # True  等价于 1 &lt; x and x &lt; 10（x 只求值一次）
print(1 &lt; 2 &lt; 3 &lt; 4 &lt; 5)      # True
print(3 &gt; 2 == 2)              # True  等价于 3 &gt; 2 and 2 == 2

# 其他语言里常见的啰嗦写法，Python 不需要
if 18 &lt;= age &lt; 65:
    print("劳动力人口")</code></pre>
  <p><strong>短路求值</strong>：<code>and</code> 左边为假就不再算右边，<code>or</code> 左边为真就不再算右边。这既是优化，也是"安全检查"的常用写法：</p>
  <pre class="code" data-lang="python"><code>def heavy():
    print("执行了重活")
    return True

False and heavy()        # 不打印：左边已决定结果
True or heavy()          # 不打印

# 短路做安全校验（顺序很重要！）
user = None
if user is not None and user.name == "admin":   # 先判空，再取属性
    print("管理员")</code></pre>
  <div class="danger-box"><span class="tag-pit">常见坑</span>把顺序写反（<code>user.name == "admin" and user is not None</code>）依然会抛 <code>AttributeError</code>——短路只在<strong>左边的求值足以决定结果</strong>时才省掉右边。</div>
</section>""",

"""<section id="sec4" class="card">
  <h2><span class="num">5.3</span> and / or 的返回值</h2>
  <p>关键区别：Python 的 <code>and</code> / <code>or</code> <strong>返回操作数本身</strong>，而不是 True/False。</p>
  <table>
    <colgroup><col style="width:26%"><col style="width:40%"><col style="width:34%"></colgroup>
    <thead><tr><th>表达式</th><th>返回规则</th><th>示例</th></tr></thead>
    <tbody>
      <tr><td><code>a or b</code></td><td>a 为真返回 a，否则返回 b</td><td><code>0 or "x"</code> → <code>"x"</code></td></tr>
      <tr><td><code>a and b</code></td><td>a 为假返回 a，否则返回 b</td><td><code>0 and "x"</code> → <code>0</code></td></tr>
      <tr><td><code>not a</code></td><td>永远返回布尔值</td><td><code>not []</code> → <code>True</code></td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="python"><code>name = input("姓名：") or "匿名"       # 空串为假 → 用默认值
config = user_config or default_config

port = env.get("PORT") or 8000         # 注意：0 也会被当成假！

# 想保留 0 / 空列表这类"合法的假值"，要用 if 判断而不是 or
port = int(env["PORT"]) if env.get("PORT") is not None else 8000</code></pre>
  <div class="warn-box"><span class="tag-pit">高频误用</span><code>x = a or b</code> 会把 <code>a</code> 的<strong>所有假值</strong>（0、0.0、""、[]、{}、None）都替换成 b。如果 <code>0</code> 是合法输入，这是 bug 温床。</div>
</section>""",

"""<section id="sec5" class="card">
  <h2><span class="num">5.4</span> 海象运算符 :=</h2>
  <p>Python 3.8 引入的<strong>赋值表达式</strong>，语法 <code>name := expr</code>：既求值，又把结果绑定到名字，让你<strong>在同一个表达式里复用计算结果</strong>。</p>
  <pre class="code" data-lang="python"><code># 传统写法：先算一次，再判断
data = fetch()
if data:
    process(data)

# 海象写法
if data := fetch():
    process(data)

# 典型场景一：正则匹配（第 29 章）
import re
if m := re.search(r"(\\d{4})-(\\d{2})", "2026-10"):
    print(m.group(1))            # 2026

# 典型场景二：while 循环里既要读取又要判断
while (line := f.readline()) != "":
    handle(line)

# 典型场景三：推导式里避免重复计算
values = [y for x in data if (y := transform(x)) is not None]</code></pre>
  <p class="key-sentence">海象运算符的价值只有一个：<strong>消除"算两次"</strong>。用不上这个价值时，普通赋值更清晰。</p>
  <div class="warn-box"><span class="tag-pit">常见坑</span>① <code>:=</code> 必须加括号用在多数上下文里（<code>(n := 10)</code>）；② 不能给属性或下标赋值（<code>d["k"] := 1</code> 非法）；③ 一行里塞两个海象会让代码难以阅读，此时请拆成两行。</div>
</section>""",

"""<section id="sec6" class="card">
  <h2><span class="num">5.5</span> 优先级与可读性</h2>
  <p>优先级从高到低只需记住常用的几层：</p>
  <pre class="code" data-lang="text"><code>**                              幂（最高，且右结合：2 ** 3 ** 2 = 512）
+x  -x  ~x                      一元正负、按位取反
*  /  //  %                     乘除类
+  -                            加减
&lt;&lt;  &gt;&gt;                          移位
&amp;                               按位与
^                               按位异或
|                               按位或
in  not in  is  &lt;  &gt;  &lt;=  &gt;=  ==  !=
not x
and
or                              逻辑或（最低）
:=                              赋值表达式（最低，且需括号）</code></pre>
  <pre class="code" data-lang="python"><code>print(2 ** 3 ** 2)          # 512   右结合：2 ** (3 ** 2)
print(-2 ** 2)              # -4    幂优先于一元负号
print(True or False and False)   # True   and 优先于 or

# 可读性优先：不确定的地方一律加括号
result = (a + b) * c</code></pre>
  <p class="key-sentence">工程建议：<strong>不要背优先级表，用括号表达意图</strong>。括号不消耗性能，却能让下一个读代码的人（包括三个月后的你）少花 10 秒。</p>
  <div class="note"><strong>运算符重载预告</strong>：<code>+</code>、<code>*</code>、<code>&lt;</code> 等在具体类型上的行为由该类型的特殊方法决定（第 21 章魔法方法）。所以 <code>[1] + [2]</code> 是拼接、<code>"a" * 3</code> 是重复——这就是"运算符多态"。</div>
</section>""",

"""<section id="sec7" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:34%"><col style="width:66%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>七类运算符</td><td>算术 / 比较 / 逻辑 / 成员 / 身份 / 赋值 / 位</td></tr>
      <tr><td>链式比较</td><td><code>1 &lt; x &lt; 10</code> 合法且中间值只算一次</td></tr>
      <tr><td>短路求值</td><td>and 见假即停，or 见真即停；可用来做安全校验</td></tr>
      <tr><td>and/or 返回值</td><td>返回操作数而非布尔；<code>or</code> 设默认值时注意 0 与空容器</td></tr>
      <tr><td>海象运算符</td><td><code>:=</code> 用于"算一次、用两次"，否则不如普通赋值</td></tr>
      <tr><td>优先级</td><td>不背表，加括号</td></tr>
      <tr><td><code>+=</code></td><td>可变对象原地改，不可变对象换新</td></tr>
    </tbody>
  </table>
</section>""",

"""<section id="sec8" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>不运行，写出下列表达式的值并说明原因：<code>-7 // 2</code>、<code>-7 % 3</code>、<code>2 ** 3 ** 2</code>、<code>0 or [] or "end"</code>、<code>"a" and 0 and "b"</code>。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>用 <code>:=</code> 改写下面这段"读文件找首个匹配行"的代码，去掉重复的 <code>readline()</code> 调用；再把它改成 <code>for line in f</code> 的写法，比较两者可读性。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>实现 <code>parse_range(text)</code>：输入 <code>"18-65"</code> 返回 <code>(18, 65)</code>，要求用 <code>re</code> + 海象运算符写成 5 行以内，非法输入返回 <code>None</code>。</div>
  <p class="note">参考答案见附录 C（规划中）。下一章进入流程控制：分支与循环。</p>
</section>"""
]
},

# ════════════════════ 第 6 章 ════════════════════
{
"n": 6, "title": "流程控制：分支与循环",
"file": "006_第6章_流程控制.html",
"meta": "预计 45 分钟 · 动手章",
"hero": "程序 = 数据 + 控制流。本章覆盖 if/elif/else、while、for 三大结构，以及 Python 独有的两个语法糖：循环的 else 子句与 3.10 的 match-case。同时讲清遍历中修改容器、死循环、range 用法这些高频事故。",
"toc": [("sec1", "本章目标"), ("sec2", "6.1 分支：if / elif / else"), ("sec3", "6.2 while 循环"),
        ("sec4", "6.3 for 循环与 range / enumerate / zip"), ("sec5", "6.4 break / continue / else"),
        ("sec6", "6.5 match-case 结构模式匹配"), ("sec7", "本章小结"), ("sec8", "本章习题")],
"sections": [
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>用 <code>if</code> 写分支，理解<strong>缩进即代码块</strong>与"扁平优于嵌套"的重构手法；</li>
    <li>用 <code>while</code> 写条件循环，能识别并规避死循环；</li>
    <li>用 <code>for</code> 写遍历循环，熟练使用 <code>range</code>、<code>enumerate</code>、<code>zip</code>；</li>
    <li>理解 <code>break</code> / <code>continue</code> 与<strong>循环的 else</strong> 语义；</li>
    <li>用 <code>match-case</code>（3.10+）替代冗长的 if-elif 链。</li>
  </ul>
</section>""",

"""<section id="sec2" class="card">
  <h2><span class="num">6.1</span> 分支：if / elif / else</h2>
  <pre class="code" data-lang="python"><code>score = 85

if score &gt;= 90:
    grade = "A"
elif score &gt;= 80:
    grade = "B"
elif score &gt;= 60:
    grade = "C"
else:
    grade = "D"

print(grade)      # B</code></pre>
  <p>三条 Python 特有之处：</p>
  <ol>
    <li><strong>没有 switch（3.10 前）</strong>，用字典或 <code>match</code> 替代；</li>
    <li><strong>条件表达式（三元）</strong>写法是 <code>值1 if 条件 else 值2</code>，顺序与 C 的 <code>?:</code> 不同；</li>
    <li>冒号 + 缩进定义代码块，<strong>缩进必须一致</strong>（推荐 4 空格，不要混用 Tab）。</li>
  </ol>
  <pre class="code" data-lang="python"><code>status = "成年" if age &gt;= 18 else "未成年"

# 扁平优于嵌套：提前返回（guard clause）
def calc_discount(user, amount):
    if not user.is_vip:          # 先排除，再处理主流程
        return 0.0
    if amount &gt;= 1000:
        return 0.2
    return 0.05</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span><strong>不要写 <code>if x == True</code></strong>，直接 <code>if x:</code>；<strong>不要写 <code>if len(items) &gt; 0</code></strong>，直接 <code>if items:</code>。前者多余，后者不符合 Python 惯例。</div>
</section>""",

"""<section id="sec3" class="card">
  <h2><span class="num">6.2</span> while 循环</h2>
  <pre class="code" data-lang="python"><code># 计数循环（多数时候 for + range 更好）
i = 0
while i &lt; 3:
    print(i)
    i += 1

# 条件循环：不知道要跑多少次时用它
import random
while True:
    n = random.randint(1, 10)
    print("抽到", n)
    if n == 6:
        break            # 跳出循环</code></pre>
  <p>while 的两个典型用法：<strong>重试</strong>与<strong>事件轮询</strong>：</p>
  <pre class="code" data-lang="python"><code>max_retry, attempt = 3, 0
while attempt &lt; max_retry:
    try:
        result = call_api()
        break
    except ConnectionError:
        attempt += 1
else:
    raise RuntimeError("接口连续 3 次失败")    # while 也支持 else！</code></pre>
  <div class="danger-box"><span class="tag-pit">常见坑</span><code>while True</code> 必须有可达的 <code>break</code>，否则死循环。调试时若卡住，用 Ctrl+C 中断；写脚本时给循环加上<strong>最大次数保护</strong>，是生产代码的良好习惯。</div>
</section>""",

"""<section id="sec4" class="card">
  <h2><span class="num">6.3</span> for 循环与 range / enumerate / zip</h2>
  <p>Python 的 <code>for</code> 是<strong>遍历循环</strong>（for-each），不是 C 风格的计数循环。它依次从可迭代对象里取元素（第 15 章讲底层协议）。</p>
  <pre class="code" data-lang="python"><code>for ch in "abc":
    print(ch, end=" ")          # a b c

for i in range(3):              # 0 1 2
    print(i)

for i in range(1, 10, 2):       # 1 3 5 7 9   start, stop, step
    print(i)</code></pre>
  <p>三个"让 for 更好用"的内置函数，几乎每天都会写到：</p>
  <pre class="code" data-lang="python"><code>names = ["张三", "李四", "王五"]

# ① enumerate：同时拿索引与值（start 可指定起始编号）
for idx, name in enumerate(names, start=1):
    print(idx, name)
# 1 张三   2 李四   3 王五

# ② zip：并行遍历多个序列，以最短的为准
ages = [18, 20, 22]
for name, age in zip(names, ages):
    print(f"{name}: {age}")
print(dict(zip(names, ages)))          # {'张三': 18, '李四': 20, '王五': 22}

# ③ sorted / reversed：不影响原列表地遍历
for name in sorted(names, key=len):
    print(name)</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span><code>zip</code> 会<strong>静默截断</strong>：长度不等时多余元素被丢弃且不报错。要严格校验长度，用 <code>zip(..., strict=True)</code>（Python 3.10+）。</div>
  <p>循环里还需要"跳过某项"时用 <code>continue</code>：</p>
  <pre class="code" data-lang="python"><code>for n in range(10):
    if n % 2 == 0:
        continue            # 跳过偶数
    print(n, end=" ")       # 1 3 5 7 9</code></pre>
</section>""",

"""<section id="sec5" class="card">
  <h2><span class="num">6.4</span> break / continue / else</h2>
  <p><code>break</code> 跳出整个循环，<code>continue</code> 跳过本轮剩余代码进入下一轮。而 <strong><code>else</code> 子句</strong>是 Python 特有的：<strong>循环没有被 break 打断时执行</strong>。</p>
  <pre class="code" data-lang="python"><code># for-else 最典型的用法：找东西，找不到时走 else
def find_user(users, uid):
    for u in users:
        if u["id"] == uid:
            print("找到了")
            break
    else:
        print("查无此人")        # 只有循环正常跑完才执行

# 用 else 判断一个数是否为质数（遍历完都没整除 ⇒ 是质数）
n = 97
for i in range(2, int(n ** 0.5) + 1):
    if n % i == 0:
        print(f"{n} 不是质数，能被 {i} 整除")
        break
else:
    print(f"{n} 是质数")</code></pre>
  <p class="key-sentence">记忆法：<code>else</code> 理解为"<strong>没被 break 打断就执行</strong>"，而不是"循环结束后执行"——它和 <code>if-else</code> 里的 else 含义无关，这是命名上的历史包袱。</p>
  <div class="danger-box"><span class="tag-pit">高频事故</span><strong>遍历时不要修改正在遍历的容器</strong>。删除元素会导致跳过项，正确做法是遍历副本或用推导式过滤：</div>
  <pre class="code" data-lang="python"><code>nums = [1, 2, 3, 4, 5, 6]

# 错误：边遍历边删，会漏掉元素
for n in nums:
    if n % 2 == 0:
        nums.remove(n)        # nums 变成 [1, 3, 5] 只是运气好，换个数据就出错

# 正确一：遍历副本
for n in nums[:]:
    if n % 2 == 0:
        nums.remove(n)

# 正确二（推荐）：生成新列表
nums = [n for n in nums if n % 2 != 0]</code></pre>
</section>""",

"""<section id="sec6" class="card">
  <h2><span class="num">6.5</span> match-case 结构模式匹配</h2>
  <p>Python 3.10 引入 <code>match</code>，它不是简单的 switch——它匹配的是<strong>结构（形状）</strong>，可以解构序列、映射与对象。</p>
  <pre class="code" data-lang="python"><code># 基础：匹配字面量（相当于 switch）
def http_status(code):
    match code:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500 | 502 | 503:          # | 表示"或"
            return "Server Error"
        case _:                        # 兜底，必须放最后
            return "Unknown"

# 进阶：匹配结构并解构
def handle(event):
    match event:
        case {"type": "click", "x": x, "y": y}:
            return f"点击位置 ({x}, {y})"
        case {"type": "key", "key": key} if key in ("w", "a", "s", "d"):
            return f"移动键 {key}"
        case ["move", dx, dy]:
            return f"位移 {dx},{dy}"
        case _:
            return "忽略"

print(handle({"type": "click", "x": 10, "y": 20}))   # 点击位置 (10, 20)
print(handle(["move", 3, 4]))                        # 位移 3,4</code></pre>
  <p>要点：</p>
  <ul>
    <li><code>case _</code> 是通配符，<u>必须放最后</u>，且它<strong>不绑定</strong>变量；</li>
    <li><code>case [x, y]</code>、<code>case {"k": v}</code> 中的 <code>x</code>、<code>v</code> 是<strong>捕获变量</strong>，匹配成功后可直接使用；</li>
    <li><code>case ... if 条件</code> 是守卫（guard），条件不满足则继续匹配下一条；</li>
    <li>常量比较用 <code>case 200</code>，变量比较要写守卫（直接写 <code>case STATUS</code> 会把它当成捕获变量，这是最常见的坑）。</li>
  </ul>
  <div class="warn-box"><span class="tag-pit">常见坑</span><code>case RED</code> 中的 <code>RED</code> 若不是<strong>点号限定的常量</strong>（如 <code>Color.RED</code>）或字面量，就会被当作"捕获任何值并命名为 RED"——静默吞掉所有输入。</div>
</section>""",

"""<section id="sec7" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:34%"><col style="width:66%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>分支</td><td>if/elif/else + 三元表达式；提前返回优于深层嵌套</td></tr>
      <tr><td>while</td><td>条件循环与重试；务必有可达的 break 或次数上限</td></tr>
      <tr><td>for</td><td>遍历循环；<code>range/enumerate/zip</code> 是三件套</td></tr>
      <tr><td>zip 陷阱</td><td>不等长静默截断，需要时用 <code>strict=True</code></td></tr>
      <tr><td>循环 else</td><td>没被 break 打断才执行；常用于"搜索失败"分支</td></tr>
      <tr><td>遍历中修改</td><td>禁止；遍历副本 <code>lst[:]</code> 或生成新列表</td></tr>
      <tr><td>match-case</td><td>3.10+ 结构模式匹配；<code>case _</code> 兜底，常量要点号限定</td></tr>
    </tbody>
  </table>
</section>""",

"""<section id="sec8" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>写 <code>fizzbuzz(n)</code>：遍历 1~n，3 的倍数打印 Fizz，5 的倍数打印 Buzz，15 的倍数打印 FizzBuzz，其余打印数字本身。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>用 <code>for ... else</code> 实现 <code>is_prime(n)</code>；再用它找出 100~200 之间所有质数，存成列表并打印个数。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>用 <code>match-case</code> 写一个命令行解析器 <code>parse(cmd: list[str])</code>：支持 <code>["add", 名称, 数量]</code>、<code>["list", "--all"]</code>、<code>["del", 编号]</code> 三种形态，非法输入返回 <code>None</code>，并说明你为什么用了守卫。</div>
  <p class="note">参考答案见附录 C（规划中）。下一篇第 7 章进入列表——Python 用得最多的容器。</p>
</section>"""
]
}
]

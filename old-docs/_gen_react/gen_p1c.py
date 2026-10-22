# -*- coding: utf-8 -*-
"""第一篇：第 6、7 章"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import build

P = "10_第一篇_入门"

# ─────────────────────────── 第 6 章 ───────────────────────────
ch6 = dict(
    part_dir=P,
    fname="006_第6章_条件渲染与列表key.html",
    num=6,
    title="条件渲染与列表 key",
    part="第一篇 入门",
    meta="第 6 章 / 共 64 章 · 预计 40 分钟 · 承第 3 章",
    desc="界面上「变」的部分无非两件事：这一段要不要显示、这一堆数据怎么逐个渲染。前者是条件渲染，后者是列表渲染与 key。本章把四种条件写法排优劣，把 key 的工作原理讲到能解释「为什么用 index 会出鬼」。",
    prev="005_第5章_事件处理与合成事件.html", prev_txt="第 5 章",
    nxt="007_第7章_useState状态与函数式更新.html", next_txt="第 7 章",
    toc=[("sec1", "本章目标"), ("sec2", "6.1 条件渲染的四种写法"),
         ("sec3", "6.2 复杂分支：先分状态，再谈写法"),
         ("sec4", "6.3 列表渲染：map 与链式处理"),
         ("sec5", "6.4 key 的作用：给节点一个身份证"),
         ("sec6", "6.5 为什么不能用 index 做 key"),
         ("sec7", "6.6 key 的正确来源与常见坑"),
         ("sec8", "本章小结"), ("sec9", "本章习题")],
    sections=[
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>根据复杂度选择合适的条件渲染写法，并敢于重构嵌套三元；</li>
    <li>掌握异步界面的"三态虚线"写法（loading / error / data）；</li>
    <li>解释 <strong>key 在协调（reconcile）阶段的真实作用</strong>——复用 DOM 还是销毁重建；</li>
    <li>能举例说明<strong>用 index 做 key 会出什么 bug</strong>，以及 key 的正确来源；</li>
    <li>记住 key 的作用范围是"兄弟节点之间"，跨层级、跨列表无需唯一。</li>
  </ul>
</section>""",
"""<section id="sec2" class="card">
  <h2><span class="num">6.1</span> 条件渲染的四种写法</h2>
  <pre class="code" data-lang="jsx"><code>// ① 早返回（if）—— 分支逻辑复杂时可读性最好
function Panel({ user }) {
  if (!user) return &lt;Empty /&gt;;
  if (user.banned) return &lt;Banned /&gt;;
  return &lt;Profile user={user} /&gt;;
}

// ② 三元 —— 二选一
&lt;div&gt;{isEdit ? &lt;EditForm /&gt; : &lt;ReadonlyView /&gt;}&lt;/div&gt;

// ③ &amp;&amp; —— 有没有（注意第 3 章讲过的 0 陷阱）
&lt;div&gt;{notifications.length &gt; 0 &amp;&amp; &lt;Bell list={notifications} /&gt;}&lt;/div&gt;

// ④ 查表（映射对象）—— 多分支的优雅解，避免嵌套三元堆砌
const STATUS_VIEW = {
  loading: &lt;Skeleton /&gt;,
  empty: &lt;Empty text="暂无数据" /&gt;,
  error: &lt;ErrorBox /&gt;,
  done: &lt;Content /&gt;,
};
&lt;div&gt;{STATUS_VIEW[status] ?? null}&lt;/div&gt;</code></pre>
  <table>
    <colgroup><col style="width:20%"><col style="width:40%"><col style="width:40%"></colgroup>
    <thead><tr><th>写法</th><th>适用场景</th><th>警告</th></tr></thead>
    <tbody>
      <tr><td>早返回</td><td>分支体量大、逻辑各异</td><td>组件 return 分散，别写太长</td></tr>
      <tr><td>三元</td><td>简单的二选一</td><td>嵌套两层以上立刻重构</td></tr>
      <tr><td>&amp;&amp;</td><td>可选的附加元素</td><td>左侧可能是 0 / NaN</td></tr>
      <tr><td>查表</td><td>状态机式多分支</td><td>分支各自需要独立组件</td></tr>
    </tbody>
  </table>
  <div class="warn-box"><span class="tag-pit">可读性红线</span>嵌套三元："<code>{a ? &lt;A/&gt; : b ? &lt;B/&gt; : c ? &lt;C/&gt; : null}</code>"。改造手法二选一：① 抽成 <code>renderByStatus()</code> 函数返回 JSX；② 拆成多个小组件各自负责一个分支。</div>
  <pre class="code" data-lang="jsx"><code>// 重构示范：把嵌套三元换成"具函数 + switch"
function renderBody(status, data) {
  switch (status) {
    case 'loading': return &lt;Skeleton /&gt;;
    case 'error':   return &lt;ErrorBox retry={refetch} /&gt;;
    case 'empty':   return &lt;Empty /&gt;;
    case 'done':    return &lt;DataView data={data} /&gt;;
    default:        return null;
  }
}

return &lt;section&gt;{renderBody(status, data)}&lt;/section&gt;;</code></pre>
</section>""",
"""<section id="sec3" class="card">
  <h2><span class="num">6.2</span> 复杂分支：先分状态，再谈写法</h2>
  <p>新手写异步页面最常见的错误是"用散落的布尔量表达状态"：<code>loading</code>、<code>isEmpty</code>、<code>hasError</code> 三个变量互相组合，会出现"既加载又空又错误"的非法组合。正确做法是用<strong>单一状态字段</strong>表达互斥状态。</p>
  <pre class="code" data-lang="jsx"><code>// ✗ 三个布尔量：非法组合无穷多
const [loading, setLoading] = useState(false);
const [error, setError] = useState(null);
const [list, setList] = useState([]);

// ✓ 单状态字段：互斥且完整
const [state, setState] = useState({ status: 'loading', data: [], error: null });

async function load() {
  setState({ status: 'loading', data: [], error: null });
  try {
    const data = await api.list();
    setState({ status: data.length ? 'done' : 'empty', data, error: null });
  } catch (error) {
    setState({ status: 'error', data: [], error });
  }
}</code></pre>
  <div class="key-sentence">界面要先"建模"再"写 JSX"：状态机建模清楚，条件渲染自然变简单。第三篇的 TanStack Query 就是把这个模式产品化了。</div>
</section>""",
"""<section id="sec4" class="card">
  <h2><span class="num">6.3</span> 列表渲染：map 与链式处理</h2>
  <pre class="code" data-lang="jsx"><code>function TodoList({ todos }) {
  return (
    &lt;ul&gt;
      {todos
        .filter(t =&gt; !t.done)                       // ①筛选
        .sort((a, b) =&gt; b.priority - a.priority)     // ②排序（注意要拷副本！）
        .slice(0, 20)                                 // ③截断
        .map(t =&gt; (                                   // ④渲染
          &lt;TodoItem key={t.id} todo={t} /&gt;
        ))}
    &lt;/ul&gt;
  );
}

// ⚠ sort 会原地修改数组实例！todos 是 props 时禁止直接用
const sorted = [...todos].sort((a, b) =&gt; b.priority - a.priority);</code></pre>
  <div class="warn-box"><span class="tag-pit">坑 1</span><code>Array.prototype.sort</code> / <code>reverse</code> / <code>splice</code> 会<strong>原地修改数组</strong>。对 props 或 state 里的数组直接调用，等于在数据来源上动手脚（违反第 4 章 props 只读），务必先 <code>[...arr]</code> 拷贝。</div>
  <p>另外，JSX 里的链式运算每次渲染都会重新执行一遍；数据量很大时应把"计算"提前到第 49 章讲的 <code>useMemo</code> 中。</p>
</section>""",
"""<section id="sec5" class="card">
  <h2><span class="num">6.4</span> key 的作用：给节点一个身份证</h2>
  <p>React 更新列表时，要知道"新的这一项和旧的哪一项是同一个东西"。<code>key</code> 就是它的判断依据：</p>
  <ul>
    <li><strong>key 相同</strong> → 判定为同一个元素，复用已有的 DOM 节点与组件状态，只更新变化的属性；</li>
    <li><strong>key 不同或缺失</strong> → 判定为旧节点消失、新节点出现，销毁旧节点并创建新 DOM。</li>
  </ul>
  <div class="diagram">
    <svg viewBox="0 0 800 230" role="img" aria-label="key 决定节点复用">
      <defs><marker id="arrK6" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#7a8a70"/></marker></defs>
      <text x="150" y="26" text-anchor="middle" font-size="13" font-weight="700" fill="#2d6a3f">旧列表</text>
      <text x="650" y="26" text-anchor="middle" font-size="13" font-weight="700" fill="#2d6a3f">新列表（头部插入 X）</text>
      <rect x="60" y="45" width="180" height="30" rx="6" fill="#f0f5e6" stroke="#3d7a4f"/><text x="150" y="65" text-anchor="middle" font-size="11.5" fill="#1f2e1f">key=a · 内容 A</text>
      <rect x="60" y="85" width="180" height="30" rx="6" fill="#f0f5e6" stroke="#3d7a4f"/><text x="150" y="105" text-anchor="middle" font-size="11.5" fill="#1f2e1f">key=b · 内容 B</text>
      <rect x="60" y="125" width="180" height="30" rx="6" fill="#f0f5e6" stroke="#3d7a4f"/><text x="150" y="145" text-anchor="middle" font-size="11.5" fill="#1f2e1f">key=c · 内容 C</text>
      <rect x="560" y="45" width="180" height="30" rx="6" fill="#fefce8" stroke="#d97706"/><text x="650" y="65" text-anchor="middle" font-size="11.5" fill="#b45309">key=x · 内容 X（新建）</text>
      <rect x="560" y="85" width="180" height="30" rx="6" fill="#d8e8c8" stroke="#3d7a4f"/><text x="650" y="105" text-anchor="middle" font-size="11.5" fill="#1f2e1f">key=a · 复用 ✓</text>
      <rect x="560" y="125" width="180" height="30" rx="6" fill="#d8e8c8" stroke="#3d7a4f"/><text x="650" y="145" text-anchor="middle" font-size="11.5" fill="#1f2e1f">key=b · 复用 ✓</text>
      <rect x="560" y="165" width="180" height="30" rx="6" fill="#d8e8c8" stroke="#3d7a4f"/><text x="650" y="185" text-anchor="middle" font-size="11.5" fill="#1f2e1f">key=c · 复用 ✓</text>
      <line x1="244" y1="145" x2="554" y2="185" stroke="#7a8a70" stroke-width="1.2" marker-end="url(#arrK6)"/>
      <text x="400" y="215" text-anchor="middle" font-size="12" fill="#7a8a70">用稳定 key：只新建 1 个 DOM；用 index：3 个节点内容全错位，全部重渲</text>
    </svg>
    <p class="diagram-caption">图 6-1 稳定 key 让 React 精确识别"哪一项是同一项"</p>
  </div>
</section>""",
"""<section id="sec6" class="card">
  <h2><span class="num">6.5</span> 为什么不能用 index 做 key</h2>
  <p>先给一个能复现的真实 bug：</p>
  <pre class="code" data-lang="jsx"><code>function Demo() {
  const [list, setList] = useState([{ id: 1, text: 'A' }, { id: 2, text: 'B' }]);

  return (
    &lt;div&gt;
      &lt;button onClick={() =&gt; setList([{ id: Date.now(), text: 'New' }, ...list])}&gt;
        头部插入
      &lt;/button&gt;
      {list.map((item, index) =&gt; (
        // ✗ 用 index 作 key
        &lt;div key={index}&gt;
          &lt;input defaultValue={item.text} /&gt;
          &lt;span&gt;{item.text}&lt;/span&gt;
        &lt;/div&gt;
      ))}
    &lt;/div&gt;
  );
}</code></pre>
  <p>复现步骤：① 在第一个输入框里把 A 改写成 "AAA"；② 点击"头部插入"。你会看到 <strong>"AAA" 还留在第一个位置，而它本该跟着 id=1 的数据跑到第二行</strong>——输入框里的内容错位了。</p>
  <p>原因：插入后 key 序列仍是 <code>0,1,2</code>。React 认为"下标 0 还是那个节点"，于是只把 0 号节点的显示文本从 A 改成 New，而 <code>&lt;input&gt;</code> 的 DOM 值由浏览器自己维护（非受控），React 不会重置，便留下了旧的用户输入。</p>
  <div class="danger-box">
    <span class="tag-pit">结论</span>只有当列表<strong>永不重排、永不增删、永不插入头部</strong>时 index 才是安全的。而真实业务里这条假设几乎必被打破。默认就用<strong>稳定业务 id</strong>。
  </div>
  <p>同理，<code>key={Math.random()}</code> 更糟：每次渲染 key 都变，React 会销毁重建全部节点，输入焦点丢失、动画重播、性能崩塌。</p>
</section>""",
"""<section id="sec7" class="card">
  <h2><span class="num">6.6</span> key 的正确来源与常见坑</h2>
  <table>
    <colgroup><col style="width:26%"><col style="width:37%"><col style="width:37%"></colgroup>
    <thead><tr><th>key 来源</th><th>是否可用</th><th>说明</th></tr></thead>
    <tbody>
      <tr><td>后端 id / uuid</td><td>最佳</td><td>稳定、与渲染顺序无关</td></tr>
      <tr><td>业务唯一值（邮箱、SKU）</td><td>可用</td><td>保证不重复即可</td></tr>
      <tr><td>数组 index</td><td>仅静态列表</td><td>动态列表会产生状态错位</td></tr>
      <tr><td><code>Math.random()</code></td><td>禁止</td><td>每次渲染都变，等于全量重建</td></tr>
      <tr><td>复合 key</td><td>可用</td><td>如 <code>{row.col}</code>，用于虚拟表格单元格</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="jsx"><code>// 后端没给 id 时：在"数据落地"处一次性生成，而不是渲染时生成
import { nanoid } from 'nanoid';

function addDraft() {
  // ✓ 创建数据时就带上 id，之后永远稳定
  setRows(prev =&gt; [...prev, { id: nanoid(), title: '', qty: 1 }]);
}</code></pre>
  <h4>其余要点</h4>
  <ul>
    <li><strong>key 只在兄弟节点间有意义</strong>：父组件不需要 key；不同数组的 key 重名也无所谓。</li>
    <li><strong>key 会强制组件重建</strong>：想让某组件"彻底重置"（比如切换 tab 后清掉内部状态），改它的 key 是官方推荐手段：<code>&lt;Form key={userId} /&gt;</code>。</li>
    <li><strong>key 不进入 props</strong>：<code>props.key</code> 取不到，它是 React 内部字段；要用请另起一个 prop 名（如 <code>id</code>）。</li>
    <li><strong>Fragment 需要 key 时用全标签</strong>：<code>&lt;React.Fragment key={id}&gt;</code>，短语法 <code>&lt;&gt;</code> 无法加属性。</li>
  </ul>
</section>""",
"""<section id="sec8" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:30%"><col style="width:70%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>条件渲染四写法</td><td>早返回 / 三元 / &amp;&amp; / 查表，按分支复杂度选择</td></tr>
      <tr><td>状态建模</td><td>用单一 status 字段代替多个布尔量，避免非法组合</td></tr>
      <tr><td>列表处理</td><td>map 渲染，sort/reverse 前先拷贝数组</td></tr>
      <tr><td>key 的作用</td><td>决定"复用还是重建"，key 同则复用 DOM 与组件状态</td></tr>
      <tr><td>index 作 key</td><td>动态列表会造成输入态/动画错位，禁用</td></tr>
      <tr><td>key 来源</td><td>稳定业务 id；没有就在创建数据时生成</td></tr>
      <tr><td>改 key 重置组件</td><td><code>&lt;Form key={id} /&gt;</code> 是官方推荐的重置手段</td></tr>
    </tbody>
  </table>
</section>""",
"""<section id="sec9" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>重写这段代码，去掉嵌套三元：<code>{loading ? &lt;Spin/&gt; : error ? &lt;Err/&gt; : list.length ? &lt;List list={list}/&gt; : &lt;Empty/&gt;}</code></div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>一个可拖拽排序的标签列表用 <code>key={index}</code>，每个标签内有一个可改名的 <code>&lt;input&gt;</code>。请描述拖拽排序后会出现什么现象，解释原因，并给出修法。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>实现"切换用户时表单自动清空"：用 <code>key={userId}</code> 与 useEffect 清理两种方案各写一遍，对比代码量与可靠性。</div>
  <p class="note">参考答案见附录 C。下一章：useState——组件的记忆。</p>
</section>""",
    ],
)

# ─────────────────────────── 第 7 章 ───────────────────────────
ch7 = dict(
    part_dir=P,
    fname="007_第7章_useState状态与函数式更新.html",
    num=7,
    title="useState：状态与函数式更新",
    part="第一篇 入门",
    meta="第 7 章 / 共 64 章 · 预计 50 分钟 · 全书最关键的一章之一",
    desc="useState 是 React 里最常用、也最容易被误解的 Hook。本章把它彻底讲清：state 存在哪、为什么 setState 后读到的还是旧值、函数式更新解决什么问题、自动批处理如何改变你的心智模型、以及对象与数组为什么必须「不可变地」更新。",
    prev="006_第6章_条件渲染与列表key.html", prev_txt="第 6 章",
    nxt="008_第8章_受控与非受控表单.html", next_txt="第 8 章",
    toc=[("sec1", "本章目标"), ("sec2", "7.1 useState 的基本形态"),
         ("sec3", "7.2 为什么读到的是旧值：快照模型"),
         ("sec4", "7.3 函数式更新"), ("sec5", "7.4 自动批处理"),
         ("sec6", "7.5 不可变更新：对象与数组"),
         ("sec7", "7.6 什么该放进 state，什么不该"),
         ("sec8", "本章小结"), ("sec9", "本章习题")],
    sections=[
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>理解 state 是<strong>组件实例上的一份记忆</strong>，每次渲染读到的是那次渲染的"快照"；</li>
    <li>能解释<strong>连续 set 同一 state 读到旧值</strong>的原因，并用函数式更新解决；</li>
    <li>掌握 React 18 的<strong>自动批处理</strong>及其对 <code>console.log</code> 结果的影响；</li>
    <li>写出正确的<strong>不可变更新</strong>代码（对象展开、数组 map/filter 返回新值）；</li>
    <li>能判断"某个数据应不应该放进 state"（派生值、DOM 值、定时器 id 各自的去处）。</li>
  </ul>
</section>""",
"""<section id="sec2" class="card">
  <h2><span class="num">7.1</span> useState 的基本形态</h2>
  <pre class="code" data-lang="jsx"><code>import { useState } from 'react';

function Stepper() {
  const [count, setCount] = useState(0);              // 解构：[值, 设置函数]
  const [user, setUser] = useState({ name: '张三', age: 18 });

  return (
    &lt;div&gt;
      &lt;p&gt;{count}&lt;/p&gt;
      &lt;button onClick={() =&gt; setCount(count + 1)}&gt;+1&lt;/button&gt;
      &lt;button onClick={() =&gt; setCount(0)}&gt;重置&lt;/button&gt;
    &lt;/div&gt;
  );
}</code></pre>
  <p>关键点：</p>
  <ul>
    <li><strong>初始值只在首次渲染生效</strong>。之后每次重渲染都会忽略参数（哪怕是昂贵的计算，见下方惰性初始化）。</li>
    <li><strong>必须调用 setter 更新</strong>。直接给变量赋值（<code>count = 1</code>）既不触发更新也无意义——<code>count</code> 是 <code>const</code> 声明的普通变量。</li>
    <li><strong>setter 是稳定引用</strong>：它在组件的整个生命周期中不变，因此可以安全地放进依赖数组。</li>
    <li>多个 state 用多次 <code>useState</code>；相关的数据也可以合并成一个对象（但更新时必须整体替换）。</li>
  </ul>
  <pre class="code" data-lang="jsx"><code>// 惰性初始化：传函数，只在首次渲染执行一次（适合昂贵计算 / 读本地存储）
const [todos, setTodos] = useState(() =&gt; {
  const raw = localStorage.getItem('todos');
  return raw ? JSON.parse(raw) : [];
});

// ✗ 这样写每次渲染都会跑一遍 JSON.parse（浪费）
const [todosWrong, setTodosWrong] = useState(JSON.parse(localStorage.getItem('todos') || '[]'));</code></pre>
</section>""",
"""<section id="sec3" class="card">
  <h2><span class="num">7.2</span> 为什么读到的是旧值：快照模型</h2>
  <pre class="code" data-lang="jsx"><code>function Demo() {
  const [n, setN] = useState(0);

  const handle = () =&gt; {
    setN(n + 1);
    setN(n + 1);
    setN(n + 1);
    console.log(n);     // 打印 0 —— 不是 3，甚至不是 1
  };

  return &lt;button onClick={handle}&gt;点我&lt;/button&gt;;
}</code></pre>
  <p>点击后界面上 n 变成 <strong>1</strong>（不是 3），控制台打印 <strong>0</strong>。这不是 bug，是 React 的核心模型：</p>
  <div class="lead"><strong>快照（snapshot）模型</strong>：每一次渲染都有自己的 props 与 state 常量。事件处理函数里的 <code>n</code>，是<strong>那次渲染捕获的常量值</strong>，不会因为 setTimeout 里修改了同名的 setN 而改变。</div>
  <p>换句话说：<code>setN(n + 1)</code> 调用三次，等价于"请下一次渲染时用值 <code>n+1</code>"重复三遍，结果自然是 1。想要累加，必须让 React 基于"最新值"计算：</p>
  <pre class="code" data-lang="jsx"><code>const handle = () =&gt; {
  setN(prev =&gt; prev + 1);
  setN(prev =&gt; prev + 1);
  setN(prev =&gt; prev + 1);
  // 界面变成 3 ✓
};</code></pre>
  <p class="key-sentence">一句话：值与更新都是"<strong>排入队列</strong>"的语义。传值 → 直接替换；传函数 → React 依次调用，以上一次的结果为参数。</p>
  <div class="note"><strong>为什么 console 打的是旧值</strong>：<code>setN</code> 只是通知 React"待会儿重渲染"，此刻变量不会变。想看新值，请在下一次渲染的函数体里打印（<code>console.log(n)</code> 放在组件顶层）。</div>
</section>""",
"""<section id="sec4" class="card">
  <h2><span class="num">7.3</span> 函数式更新</h2>
  <pre class="code" data-lang="jsx"><code>// 形式：setState(prev =&gt; nextValue)
setCount(c =&gt; c + 1);
setUser(u =&gt; ({ ...u, age: u.age + 1 }));
setList(l =&gt; [...l, newItem]);
setList(l =&gt; l.filter(x =&gt; x.id !== id));
setObj(o =&gt; o.active ? o : { ...o, active: true });   // 也可 return 原值跳过更新</code></pre>
  <table>
    <colgroup><col style="width:26%"><col style="width:37%"><col style="width:37%"></colgroup>
    <thead><tr><th>场景</th><th>传值 <code>setX(v)</code></th><th>传函数 <code>setX(p =&gt; v)</code></th></tr></thead>
    <tbody>
      <tr><td>依赖旧值累加</td><td>❌ 会丢失更新</td><td>✅ 推荐</td></tr>
      <tr><td>同一 tick 内多次更新</td><td>❌ 覆盖</td><td>✅ 依次执行</td></tr>
      <tr><td>异步回调里更新</td><td>⚠ 容易读到过期值</td><td>✅ 安全</td></tr>
      <tr><td>纯替换（如重置）</td><td>✅ 简洁</td><td>✅ 等价</td></tr>
    </tbody>
  </table>
  <p>一个异步场景的对比：</p>
  <pre class="code" data-lang="jsx"><code>// ✗ 慢接口连点两次会丢一次：第二次 setCount 基于的还是旧 count
async function loadMore() {
  const more = await fetchMore();
  setCount(count + more.length);
}

// ✓ 基于最新值计算，永不丢失
async function loadMore() {
  const more = await fetchMore();
  setCount(c =&gt; c + more.length);
}</code></pre>
</section>""",
"""<section id="sec5" class="card">
  <h2><span class="num">7.4</span> 自动批处理</h2>
  <p>多次 setState 会让组件重渲染几次？答案是 <strong>1 次</strong>——React 会把同一个事件里的多次更新合并处理，这就是<strong>批处理（batching）</strong>。</p>
  <pre class="code" data-lang="jsx"><code>const handle = () =&gt; {
  setA(1);
  setB(2);
  setC(3);
  // React 18：只重渲染 1 次（三次 setState 被合并）
};</code></pre>
  <table>
    <colgroup><col style="width:24%"><col style="width:38%"><col style="width:38%"></colgroup>
    <thead><tr><th>版本</th><th>批处理范围</th><th>说明</th></tr></thead>
    <tbody>
      <tr><td>React 17</td><td>仅 React 事件回调内</td><td><code>setTimeout</code>、原生监听、Promise 里<b>不</b>批处理</td></tr>
      <tr><td>React 18</td><td>全部场景（自动批处理）</td><td>定时器、原生事件、异步回调一律合并</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="jsx"><code>// React 18 下这三处都只渲染一次
setTimeout(() =&gt; { setA(1); setB(2); }, 1000);
el.addEventListener('click', () =&gt; { setA(1); setB(2); });
promise.then(() =&gt; { setA(1); setB(2); });

// 极少数场景真的需要同步读取更新后的 DOM：
import { flushSync } from 'react-dom';
flushSync(() =&gt; setA(1));     // 强制立即同步刷新（会伤性能，慎用）
console.log(document.querySelector('#a').textContent);</code></pre>
  <div class="warn-box"><span class="tag-pit">坑</span>升级到 18 后，某些依赖"setTimeout 里多次 setState 会多次渲染"的老代码行为会变化。绝大多数情况是变快了；<strong>若确实需要"每次更新后立即拿到 DOM"</strong>，用 <code>flushSync</code> 并把这段逻辑推到第 12 章讲的 <code>useLayoutEffect</code>。</div>
</section>""",
"""<section id="sec6" class="card">
  <h2><span class="num">7.5</span> 不可变更新：对象与数组</h2>
  <p>React 判断"状态变没变"用的是 <strong>Object.is（近似 ===）浅比较</strong>。因此：<strong>必须替换引用，而不是在原地修改</strong>。</p>
  <pre class="code" data-lang="jsx"><code>// ✗ 原地修改：引用没变，React 认为没变化，界面不更新
function badUpdate() {
  user.age = 19;            setUser(user);        // ❌ 同一个对象引用
  list.push(item);          setList(list);        // ❌
  list[0].done = true;      setList(list);        // ❌ 嵌套也不行
}

// ✓ 创建新引用
setUser(u =&gt; ({ ...u, age: 19 }));                       // 对象：展开 + 覆盖
setList(l =&gt; [...l, item]);                              // 追加
setList(l =&gt; l.map(x =&gt; x.id === id ? { ...x, done: !x.done } : x));  // 修改某项
setList(l =&gt; l.filter(x =&gt; x.id !== id));                // 删除
setList(l =&gt; l.slice(0, -1));                            // 删尾</code></pre>
  <h4>深层嵌套怎么办</h4>
  <pre class="code" data-lang="jsx"><code>// state = { user: { profile: { city: '北京' } }, list: [] }

// 手写层层展开（能用但啰嗦）
setState(s =&gt; ({
  ...s,
  user: { ...s.user, profile: { ...s.user.profile, city: '上海' } },
}));

// 推荐：Immer（写起来像原地修改，内部产出新引用）
import { produce } from 'immer';
setState(produce(s =&gt; { s.user.profile.city = '上海'; }));</code></pre>
  <div class="key-sentence">原则记住一句就够了：<strong>谁被改，就把谁所在的整条路径上的对象都换成新副本</strong>。这也是第 44 章"不可变为什么必须"的原理基础。</div>
  <p class="pit-sentence">别为了"性能"到处深拷贝：<code>JSON.parse(JSON.stringify(x))</code> 会让所有子树失去引用相等性，反而让 memo 全面失效；<strong>精确到被改的那一层</strong>才是正确做法。</p>
</section>""",
"""<section id="sec7" class="card">
  <h2><span class="num">7.6</span> 什么该放进 state，什么不该</h2>
  <table>
    <colgroup><col style="width:26%"><col style="width:37%"><col style="width:37%"></colgroup>
    <thead><tr><th>数据</th><th>该放 state 吗</th><th>放哪</th></tr></thead>
    <tbody>
      <tr><td>用户输入、开关、列表数据</td><td>✅</td><td>useState / 状态库</td></tr>
      <tr><td>可由 props 或 state 算出（全名、总价、过滤结果）</td><td>❌ 派生值</td><td>渲染时直接算；成本高则 useMemo（第 49 章）</td></tr>
      <tr><td>DOM 度量值（宽高、滚动位置）</td><td>❌</td><td>useRef 读取，必要时再同步进 state</td></tr>
      <tr><td>定时器 id、请求取消标记、上一次的值</td><td>❌ 与渲染无关</td><td>useRef（第 13 章）</td></tr>
      <tr><td>服务端返回结果</td><td>❌ 服务端状态</td><td>TanStack Query（第 25 章）</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="jsx"><code>// ✗ 冗余 state：看起来"更清楚"，实际是 bug 温床
const [list, setList] = useState([]);
const [doneCount, setDoneCount] = useState(0);   // 需要在三处手动同步
const toggle = id =&gt; { setList(...); setDoneCount(c =&gt; c + 1); };

// ✓ 派生即可：永远自动一致
const doneCount = list.filter(x =&gt; x.done).length;</code></pre>
  <h4>什么时候该把 state 提到父组件（状态提升）</h4>
  <ul>
    <li>两个及以上兄弟组件都需要这份数据时，把 state 放到最近的公共父组件，通过 props 下发；</li>
    <li>提升过头会让顶层组件臃肿且引发大范围重渲染，此时就该进入第三篇的状态分层设计了。</li>
  </ul>
</section>""",
"""<section id="sec8" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:30%"><col style="width:70%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>快照模型</td><td>每次渲染有自己的常量 state；set 后下次渲染才变</td></tr>
      <tr><td>函数式更新</td><td><code>p =&gt; next</code> 保证基于最新值，多次调用依次生效</td></tr>
      <tr><td>自动批处理</td><td>React 18 全场景合并更新，只渲染一次</td></tr>
      <tr><td>不可变更新</td><td>必须换引用；对象展开、map/filter 返回新数组</td></tr>
      <tr><td>深嵌套</td><td>逐层展开或引入 Immer</td></tr>
      <tr><td>初始化</td><td>昂贵计算用惰性初始化 <code>useState(() =&gt; ...)</code></td></tr>
      <tr><td>不该进 state</td><td>派生值、DOM 度量、timer id、服务端数据</td></tr>
    </tbody>
  </table>
</section>""",
"""<section id="sec9" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>下面代码点击后界面显示几？为什么？如何改成加 3？<code>const h = () =&gt; { setN(n+1); setN(n+1); setN(n+1); }</code></div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>实现购物车行项的数量增减与删除：state 结构为 <code>[{ sku, name, price, qty }]</code>，要求全部使用函数式更新与不可变写法，并给出"总价"的派生实现。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>用 <code>produce</code>（Immer）重写一个三层嵌套的配置对象更新：<code>{ theme: { color: { primary } }, table: { size } }</code>，同时说明 Immer 返回的是新引用，以及为什么不能被 <code>freeze</code> 冻结的数据除外。</div>
  <p class="note">参考答案见附录 C。下一章：表单——受控与非受控之争。</p>
</section>""",
    ],
)

build(**ch6)
build(**ch7)

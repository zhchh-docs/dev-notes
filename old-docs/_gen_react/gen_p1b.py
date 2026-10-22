# -*- coding: utf-8 -*-
"""第一篇：第 4、5 章"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import build

P = "10_第一篇_入门"

# ─────────────────────────── 第 4 章 ───────────────────────────
ch4 = dict(
    part_dir=P,
    fname="004_第4章_组件与props数据下行.html",
    num=4,
    title="组件与 props：数据下行",
    part="第一篇 入门",
    meta="第 4 章 / 共 64 章 · 预计 45 分钟 · 组件化思维起点",
    desc="React 应用的本质是一个组件树。这一章回答组件应该怎么拆、数据怎么往下传：props 为什么必须只读、单向数据流到底单向在哪、children 与「插槽」怎么写、以及 props 设计的六条实战准则。这是从「写页面」迈向「搭架构」的第一步。",
    prev="003_第3章_JSX详解语法与编译产物.html", prev_txt="第 3 章",
    nxt="005_第5章_事件处理与合成事件.html", next_txt="第 5 章",
    toc=[("sec1", "本章目标"), ("sec2", "4.1 为什么要拆组件"),
         ("sec3", "4.2 props：只读的一份入参"), ("sec4", "4.3 默认值与类型约束"),
         ("sec5", "4.4 children 与插槽模式"), ("sec6", "4.5 组合优于继承"),
         ("sec7", "4.6 props 设计六准则与常见坑"),
         ("sec8", "本章小结"), ("sec9", "本章习题")],
    sections=[
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>掌握组件拆分的判断标准：什么时候该拆、什么时候拆早了；</li>
    <li>理解 <strong>props 只读</strong>与<strong>单向数据流</strong>，并知道违反它会得到什么后果；</li>
    <li>会写 props 的<strong>默认值</strong>与<strong>类型检查</strong>（含 TS 写法）；</li>
    <li>掌握 <code>children</code> 实现的三种组合模式：内容分发、布局容器、render props 雏形；</li>
    <li>能用六条准则设计出"三个月后自己还看得懂"的组件 API。</li>
  </ul>
</section>""",
"""<section id="sec2" class="card">
  <h2><span class="num">4.1</span> 为什么要拆组件</h2>
  <p>React 没有告诉你"文件怎么分"，但拆错了会从第一天开始持续付利息。拆组件的收益只有三条，每条都对应一个具体痛点：</p>
  <table>
    <colgroup><col style="width:22%"><col style="width:39%"><col style="width:39%"></colgroup>
    <thead><tr><th>收益</th><th>解决的问题</th><th>判断信号</th></tr></thead>
    <tbody>
      <tr><td>复用</td><td>同一段 UI 在多处重复</td><td>发现自己在复制粘贴 JSX</td></tr>
      <tr><td>单一职责</td><td>一个函数管太多事，改一处牵一片</td><td>组件超过 150 行、混合多种关注点</td></tr>
      <tr><td>渲染边界</td><td>一处小改动导致整页重渲染</td><td>性能优化时需要把"动的部分"隔离出来</td></tr>
    </tbody>
  </table>
  <p>看一个典型"拆之前 vs 拆之后"：一个订单卡片里混合了商品列表、金额汇总和操作按钮。</p>
  <pre class="code" data-lang="jsx"><code>// ✗ 拆之前：一个组件里塞了三件事
function OrderPanel({ order }) {
  return (
    &lt;div className="panel"&gt;
      &lt;h3&gt;订单 {order.no}&lt;/h3&gt;
      {order.items.map(it =&gt; (
        &lt;div key={it.id}&gt;
          &lt;span&gt;{it.name}&lt;/span&gt;&lt;span&gt;x{it.qty}&lt;/span&gt;&lt;span&gt;￥{it.price}&lt;/span&gt;
        &lt;/div&gt;
      ))}
      &lt;div&gt;合计：￥{order.items.reduce((s, i) =&gt; s + i.price * i.qty, 0)}&lt;/div&gt;
      &lt;button&gt;付款&lt;/button&gt;&lt;button&gt;取消&lt;/button&gt;
    &lt;/div&gt;
  );
}

// ✓ 拆之后：每个组件一件事，金额计算也有了"家"
function OrderItem({ item }) {
  return (
    &lt;div className="order-item"&gt;
      &lt;span&gt;{item.name}&lt;/span&gt;
      &lt;span&gt;x{item.qty}&lt;/span&gt;
      &lt;span&gt;￥{item.price}&lt;/span&gt;
    &lt;/div&gt;
  );
}

function OrderSummary({ items }) {
  const total = items.reduce((s, i) =&gt; s + i.price * i.qty, 0);
  return &lt;div className="summary"&gt;合计：￥{total}&lt;/div&gt;;
}

function OrderPanel({ order, onPay, onCancel }) {
  return (
    &lt;div className="panel"&gt;
      &lt;h3&gt;订单 {order.no}&lt;/h3&gt;
      {order.items.map(it =&gt; &lt;OrderItem key={it.id} item={it} /&gt;)}
      &lt;OrderSummary items={order.items} /&gt;
      &lt;button onClick={onPay}&gt;付款&lt;/button&gt;
      &lt;button onClick={onCancel}&gt;取消&lt;/button&gt;
    &lt;/div&gt;
  );
}</code></pre>
  <div class="key-sentence">拆分口诀：凡是"能被起一个业务名字的 UI 片段"，就值得抽成一个组件；凡是"会被复制第二次的 JSX"，必须抽。</div>
  <div class="note"><strong>文件粒度</strong>：本书约定一个组件一个文件，同目录组件 ≤ 12 个、单层目录 ≤ 6 个子目录；组件 script（模板）超过 150 行就该考虑继续拆。</div>
</section>""",
"""<section id="sec3" class="card">
  <h2><span class="num">4.2</span> props：只读的一份入参</h2>
  <p>props 就是组件函数的<strong>第一个参数</strong>，用法：</p>
  <pre class="code" data-lang="jsx"><code>// 写法一：props 对象整体接收
function Avatar(props) {
  return &lt;img src={props.url} alt={props.name} width={props.size} /&gt;;
}

// 写法二：解构（推荐，一眼看全 API）
function Avatar({ url, name, size = 48 }) {
  return &lt;img src={url} alt={name} width={size} /&gt;;
}

// 使用：<Avatar url="" name="张三" />  —— 属性名随意，顺序无关</code></pre>
  <h4>三条铁律</h4>
  <ol>
    <li><strong>props 只读</strong>。组件内部绝不修改 <code>props.xxx</code>。这不是建议，是 React 的强制约定——第 44 章会解释：修改对象型 props（如 <code>props.items.push(x)</code>）会让父组件"看起来没变"从而跳过更新，制造极难排查的 bug。</li>
    <li><strong>单向数据流</strong>：数据只能从父组件流向子组件（父持有 state → 通过 props 下发）。子组件想改数据，只能<strong>调用父组件传下来的回调函数</strong>，由父组件去 setState。</li>
    <li><strong>props 变化引发重渲染</strong>：父重渲染时，子组件默认跟着重渲染（不论 props 是否真的变了）——这是第六篇性能优化要解决的核心现象。</li>
  </ol>
  <pre class="code" data-lang="jsx"><code>// 子组件上传孔子组件的状态变更：回调上行
function TodoItem({ todo, onToggle, onRemove }) {
  return (
    &lt;li&gt;
      &lt;input
        type="checkbox"
        checked={todo.done}
        onChange={() =&gt; onToggle(todo.id)}   {/* 只管通知，数据由父组件改 */}
      /&gt;
      &lt;span&gt;{todo.title}&lt;/span&gt;
      &lt;button onClick={() =&gt; onRemove(todo.id)}&gt;删除&lt;/button&gt;
    &lt;/li&gt;
  );
}

function TodoList({ todos, setTodos }) {
  const toggle = (id) =&gt; setTodos(prev =&gt; prev.map(
    t =&gt; t.id === id ? { ...t, done: !t.done } : t
  ));
  const remove = (id) =&gt; setTodos(prev =&gt; prev.filter(t =&gt; t.id !== id));

  return (
    &lt;ul&gt;
      {todos.map(t =&gt; (
        &lt;TodoItem key={t.id} todo={t} onToggle={toggle} onRemove={remove} /&gt;
      ))}
    &lt;/ul&gt;
  );
}</code></pre>
  <div class="warn-box"><span class="tag-pit">常见坑</span><code>props.xxx = 1</code> 在开发环境直接抛 <em>Cannot assign to read only property</em>；但 <code>props.list.push(1)</code> 不报错——它污染了父组件的数据却不触发更新，属于"静默事故"，务必避免。</div>
</section>""",
"""<section id="sec4" class="card">
  <h2><span class="num">4.3</span> 默认值与类型约束</h2>
  <h4>默认值</h4>
  <pre class="code" data-lang="jsx"><code>// 推荐：解构时给默认值（ES6 语法，直观且与 TS 兼容）
function Button({ type = 'primary', size = 'middle', disabled = false, onClick }) {
  /* ... */
}

// 老写法（类组件时代的 defaultProps）—— 函数组件中已不推荐
Button.defaultProps = { type: 'primary' };</code></pre>
  <h4>类型检查：TypeScript（推荐）</h4>
  <pre class="code" data-lang="ts"><code>type User = { id: number; name: string; avatar?: string };

type Props = {
  user: User;                       // 必传
  size?: 'small' | 'middle' | 'large';  // 可选 + 字面量联合
  onSelect?: (id: number) =&gt; void;  // 函数签名
  children?: React.ReactNode;       // 任意可渲染内容
};

function UserCard({ user, size = 'middle', onSelect, children }: Props) {
  return &lt;div onClick={() =&gt; onSelect?.(user.id)}&gt;{children}&lt;/div&gt;;
}</code></pre>
  <h4>类型检查：propTypes（JS 项目轻量方案）</h4>
  <pre class="code" data-lang="jsx"><code>import PropTypes from 'prop-types';

UserCard.propTypes = {
  user: PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
  }).isRequired,
  size: PropTypes.oneOf(['small', 'middle', 'large']),
  onSelect: PropTypes.func,
};

// 不匹配时控制台会给出清晰警告（仅开发模式生效）</code></pre>
  <p class="key-sentence">类型不是枷锁：它替你拦住"少传一个参数""传错字段名"这两类最高频的低级 bug，是团队规模变大后的必需品。</p>
</section>""",
"""<section id="sec5" class="card">
  <h2><span class="num">4.4</span> children 与插槽模式</h2>
  <p><code>children</code> 是 props 里最特殊的一个：<strong>它表示开标签与闭标签之间的内容</strong>。有了它，组件就能像 HTML 一样"包裹内容"，这就是"插槽"。</p>
  <pre class="code" data-lang="jsx"><code>function Card({ title, children }) {
  return (
    &lt;div className="card"&gt;
      &lt;div className="card-head"&gt;{title}&lt;/div&gt;
      &lt;div className="card-body"&gt;{children}&lt;/div&gt;
    &lt;/div&gt;
  );
}

&lt;Card title="用户信息"&gt;
  &lt;p&gt;姓名：张三&lt;/p&gt;
  &lt;Avatar url="/a.png" /&gt;
&lt;/Card&gt;</code></pre>
  <h4>多插槽：用"具名 props 传 JSX"</h4>
  <pre class="code" data-lang="jsx"><code>// 把 JSX 当作普通值塞进任意 prop —— React 没有真正的"具名插槽"
&lt;Layout
  header={&lt;SiteHeader /&gt;}
  sidebar={&lt;Nav /&gt;}
  footer={&lt;Copyright /&gt;}
&gt;
  &lt;Article /&gt;
&lt;/Layout&gt;

function Layout({ header, sidebar, footer, children }) {
  return (
    &lt;div className="layout"&gt;
      &lt;header&gt;{header}&lt;/header&gt;
      &lt;aside&gt;{sidebar}&lt;/aside&gt;
      &lt;main&gt;{children}&lt;/main&gt;
      &lt;footer&gt;{footer}&lt;/footer&gt;
    &lt;/div&gt;
  );
}</code></pre>
  <h4>函数式插槽（render props 雏形）</h4>
  <pre class="code" data-lang="jsx"><code>// 子组件把内部数据"吐"出来给调用方决定怎么渲染
&lt;DataProvider url="/api/user"&gt;
  {({ data, loading }) =&gt; loading ? &lt;Spinner /&gt; : &lt;UserCard user={data} /&gt;}
&lt;/DataProvider&gt;

function DataProvider({ url, children }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  useEffect(() =&gt; {
    fetch(url).then(r =&gt; r.json()).then(d =&gt; { setData(d); setLoading(false); });
  }, [url]);
  return children({ data, loading });   // children 是函数，调用它
}</code></pre>
  <p>这个模式在 Hooks 出现前是逻辑复用的主力；今天多数场景被自定义 Hook（第 16 章）取代，但 Ant Design、React Router 等库中仍大量存在，必须认识。</p>
</section>""",
"""<section id="sec6" class="card">
  <h2><span class="num">4.5</span> 组合优于继承</h2>
  <p>React 官方文档的态度非常明确：<strong>你没有继承组件的必要</strong>。类继承带来的层级耦合在 UI 这种"结构多变"的领域弊大于利，React 提供的组合能力已经覆盖全部场景。</p>
  <table>
    <colgroup><col style="width:26%"><col style="width:37%"><col style="width:37%"></colgroup>
    <thead><tr><th>需求</th><th>继承思路（不推荐）</th><th>组合思路（推荐）</th></tr></thead>
    <tbody>
      <tr><td>复用外框</td><td>所有页面继承 BasePage</td><td><code>&lt;Layout&gt;&lt;Page /&gt;&lt;/Layout&gt;</code></td></tr>
      <tr><td>注入通用能力</td><td>多层 Mixin / 抽象基类</td><td>自定义 Hook（第 16 章）</td></tr>
      <tr><td>局部差异常</td><td>子类覆写 render 碎片</td><td>props 开关 + <code>children</code> 插槽</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="jsx"><code>// 一个"具备边框和标题的通用容器"，通过 children 容纳任意内容
function Panel({ title, extra, children }) {
  return (
    &lt;section className="panel"&gt;
      &lt;header&gt;
        &lt;h3&gt;{title}&lt;/h3&gt;
        &lt;div className="extra"&gt;{extra}&lt;/div&gt;
      &lt;/header&gt;
      {children}
    &lt;/section&gt;
  );
}

&lt;Panel title="待办" extra={&lt;Button&gt;新建&lt;/Button&gt;}&gt;
  &lt;TodoList todos={todos} /&gt;
&lt;/Panel&gt;</code></pre>
  <div class="pit-sentence">判断标准：如果你打算"继承一个组件只为改它的一部分 UI"，那就应该把它拆成"容器 + children"，而不是开继承链。</div>
</section>""",
"""<section id="sec7" class="card">
  <h2><span class="num">4.6</span> props 设计六准则与常见坑</h2>
  <ol>
    <li><strong>命名对齐：数据用名词，事件用 on 前缀</strong>：<code>value / items / user</code> 表示数据，<code>onChange / onSubmit / onSelect</code> 表示回调，前者不加前缀，后者必须 <code>on</code> 开头。</li>
    <li><strong>受控 vs 非受控要统一</strong>：一个组件要么全受控（<code>value + onChange</code>），要么全非受控（<code>defaultValue</code>），不要两套并存——第 8 章详述。</li>
    <li><strong>扁平优先</strong>：<code>&lt;Avatar user={user} /&gt;</code> 比 <code>&lt;Avatar user={user} size={size} theme={theme} className={c} /&gt;</code> 更好维护吗？不一定——props 超过 7 个就该考虑是否要拆组件；而"整对象传入"会带来无谓重渲染，需权衡。</li>
    <li><strong>谨慎使用 spread 透传</strong>：<code>&lt;input {...inputProps} /&gt;</code> 很方便，但会把未知属性一起送进 DOM，React 会给出 <em>Unknown prop</em> 警告；可用 ESLint 规则 <code>react/jsx-props-no-spreading</code> 约束。</li>
    <li><strong>加 key 而不是 index</strong>：列表渲染的 props 里必须有稳定 <code>key</code>（第 6 章）。</li>
    <li><strong>className / style 要可覆盖</strong>：组件内部接收外部传入的 <code>className</code> 并合并，否则调用方永远改不了样式。</li>
  </ol>
  <pre class="code" data-lang="jsx"><code>// 准则 1 + 6 的示范
function Tag({ text, color = 'green', className = '', style, onClick }) {
  const cls = ['tag', 'tag-' + color, className].filter(Boolean).join(' ');
  return &lt;span className={cls} style={style} onClick={onClick}&gt;{text}&lt;/span&gt;;
}</code></pre>
  <div class="warn-box"><span class="tag-pit">坑清单</span>
    <ul>
      <li><code>props</code> 名字拼错不报错，只是得到 <code>undefined</code>——用 TS 或 propTypes 兜住；</li>
      <li>回调写成 <code>onClick={remove(id)}</code>（立即执行）而不是 <code>onClick={() =&gt; remove(id)}</code>（传引用），导致渲染时就删除；</li>
      <li>把对象/数组直接写在 JSX 里作为 props（<code>style={{...}}</code>、<code>&lt;C items={[...]}&gt;</code>），每次渲染都是新引用，会让下游 memo 失效——第 48、49 章解释。</li>
    </ul>
  </div>
</section>""",
"""<section id="sec8" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:30%"><col style="width:70%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>拆分标准</td><td>可复用、单一职责、隔离渲染；JSX 被复制第二次就抽</td></tr>
      <tr><td>props 本质</td><td>组件函数的第一个参数，只读</td></tr>
      <tr><td>单向数据流</td><td>state 在父组件，props 下行，事件回调上行</td></tr>
      <tr><td>默认值/类型</td><td>解构默认值；TS 优先，propTypes 为 JS 备选</td></tr>
      <tr><td>children</td><td>内容分发（插槽），多插槽用 props 传 JSX</td></tr>
      <tr><td>render props</td><td>children 为函数，把内部数据交还调用方</td></tr>
      <tr><td>组合优于继承</td><td>容器 + children + 自定义 Hook 覆盖全部复用需求</td></tr>
    </tbody>
  </table>
</section>""",
"""<section id="sec9" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>把习题 B 里的 OrderPanel 继续拆分：抽出 <code>OrderActions</code>（按钮区），并把"合计金额"的计算抽成独立函数放在组件外的工具模块。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>实现一个 <code>&lt;Modal title visible onClose footer&gt;&lt;/Modal&gt;</code>：title / footer 用具名 props，body 用 children，visible 为 false 时不渲染任何 DOM。要求 footer 支持外部传入自定义按钮。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>用 TS 为一个分页器 <code>Pagination</code> 定义 Props（current / pageSize / total / showSizeChanger? / onChange / onShowSizeChange），要求 onChange 与 onShowSizeChange 参数类型准确，并写出使用端代码。</div>
  <p class="note">参考答案见附录 C。下一章：让组件"活"起来——事件处理与合成事件。</p>
</section>""",
    ],
)

# ─────────────────────────── 第 5 章 ───────────────────────────
ch5 = dict(
    part_dir=P,
    fname="005_第5章_事件处理与合成事件.html",
    num=5,
    title="事件处理与合成事件",
    part="第一篇 入门",
    meta="第 5 章 / 共 64 章 · 预计 40 分钟 · 承第 4 章",
    desc="点一下为什么界面会变？这一章把 React 的事件机制讲透：绑定的正确写法、为什么要传函数引用、SyntheticEvent 是什么、如何传参、如何阻止默认行为与冒泡，以及 React 17 之后事件委托到了哪里——这些都是面试与调试的高频点。",
    prev="004_第4章_组件与props数据下行.html", prev_txt="第 4 章",
    nxt="006_第6章_条件渲染与列表key.html", next_txt="第 6 章",
    toc=[("sec1", "本章目标"), ("sec2", "5.1 绑定的三种写法"),
         ("sec3", "5.2 SyntheticEvent 合成事件"),
         ("sec4", "5.3 传参的三种姿势"), ("sec5", "5.4 阻止默认行为与冒泡"),
         ("sec6", "5.5 事件委托：React 到底把监听挂在哪"),
         ("sec7", "5.6 常见坑清单"),
         ("sec8", "本章小结"), ("sec9", "本章习题")],
    sections=[
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>写出不会"渲染时就被执行"的事件绑定，理解<strong>传引用 vs 传调用</strong>的区别；</li>
    <li>认识 <strong>SyntheticEvent</strong>：为什么 React 要包一层、它能干什么、什么时候必须用原生事件；</li>
    <li>掌握三种传参方式并知道各自的代价；</li>
    <li>正确使用 <code>preventDefault</code>、<code>stopPropagation</code>、捕获阶段与 <code>passive</code>；</li>
    <li>讲清 React 17+ 的事件委托位置变化及其意义。</li>
  </ul>
</section>""",
"""<section id="sec2" class="card">
  <h2><span class="num">5.1</span> 绑定的三种写法</h2>
  <pre class="code" data-lang="jsx"><code>function Toolbar() {
  // ① 具名函数 + 传引用（最推荐：可读、可做依赖优化）
  const handleSave = () =&gt; {
    console.log('save');
  };

  return (
    &lt;div&gt;
      &lt;button onClick={handleSave}&gt;保存 ①&lt;/button&gt;

      {/* ② 内联箭头函数：需要传参或逻辑极简时用 */}
      &lt;button onClick={() =&gt; console.log('save inline')}&gt;保存 ②&lt;/button&gt;

      {/* ③ 直接内联语句：不推荐，可读性差 */}
      &lt;button onClick={console.log('bad')}&gt;不要这样 ③&lt;/button&gt;
    &lt;/div&gt;
  );
}</code></pre>
  <div class="danger-box"><span class="tag-pit">头号坑</span>写法 ③ 是错的：<code>onClick={fn()}</code> 会在<strong>渲染过程中立刻执行</strong> fn，把它的返回值（通常是 <code>undefined</code>）赋给 onClick。现象是"页面一打开就触发一次，之后点击毫无反应"。口诀：<strong>onClick 后面一定是函数本身，不是函数调用</strong>。</div>
  <h4>为什么不涉及 this</h4>
  <p>类组件时代需要用 <code>this.handleClick = this.handleClick.bind(this)</code> 或箭头函数属性来锁死 this；函数组件里根本没有 this，这一整类问题自动消失——这是 Hooks 被广泛接受的直接原因之一。</p>
</section>""",
"""<section id="sec3" class="card">
  <h2><span class="num">5.2</span> SyntheticEvent 合成事件</h2>
  <p>你拿到的 event 对象并不是浏览器原生的 Event，而是 React 包装的 <strong>SyntheticEvent（合成事件）</strong>。它做两件事：</p>
  <ol>
    <li><strong>抹平浏览器差异</strong>：<code>target</code>、<code>currentTarget</code>、<code>preventDefault()</code> 等在各浏览器表现一致；</li>
    <li><strong>统一接口</strong>：所有事件类型（鼠标、键盘、表单、触摸）都继承自同一 <code>SyntheticEvent</code>，都有同样的 <code>stopPropagation</code> 等方法。</li>
  </ol>
  <pre class="code" data-lang="jsx"><code>function SearchInput() {
  const handleChange = (e) =&gt; {
    console.log(e.target.value);      // 输入值
    console.log(e.target.name);       // 表单控件 name，常用于一个 handler 管多个字段
    console.log(e.type);              // 'change'
    console.log(e.nativeEvent);       // 需要时用这个拿原生事件
  };

  const handleKeyDown = (e) =&gt; {
    if (e.key === 'Enter') console.log('回车提交');
    if (e.key === 'Escape') e.currentTarget.blur();
  };

  return &lt;input name="kw" onChange={handleChange} onKeyDown={handleKeyDown} /&gt;;
}</code></pre>
  <table>
    <colgroup><col style="width:26%"><col style="width:74%"></colgroup>
    <thead><tr><th>常用属性/方法</th><th>说明</th></tr></thead>
    <tbody>
      <tr><td><code>e.target</code></td><td>触发事件的真实 DOM 元素（可能是子元素）</td></tr>
      <tr><td><code>e.currentTarget</code></td><td>绑定事件处理器的那个元素（本组件内的节点）</td></tr>
      <tr><td><code>e.preventDefault()</code></td><td>阻止默认行为（表单提交跳转、链接跳转）</td></tr>
      <tr><td><code>e.stopPropagation()</code></td><td>阻止继续冒泡</td></tr>
      <tr><td><code>e.nativeEvent</code></td><td>原生 Event，需要 <code>passive</code>、<code>isTrusted</code> 等特性时用</td></tr>
    </tbody>
  </table>
  <h4>历史遗留：事件池（event pooling）</h4>
  <p>React 16 及以前复用事件对象以节省内存，因此在 <code>setTimeout</code> 里访问 <code>e.target</code> 会得到 null，必须 <code>e.persist()</code>。<strong>React 17 起事件池已被移除</strong>，现在你可以安全地异步访问事件对象。老教程里的 <code>persist()</code> 在现代代码里不需要了。</p>
</section>""",
"""<section id="sec4" class="card">
  <h2><span class="num">5.3</span> 传参的三种姿势</h2>
  <pre class="code" data-lang="jsx"><code>function List({ items, onRemove }) {
  return (
    &lt;ul&gt;
      {/* ① 内联箭头包装：最直观，最常用 */}
      {items.map(it =&gt; (
        &lt;li key={it.id}&gt;
          {it.title}
          &lt;button onClick={() =&gt; onRemove(it.id)}&gt;删除 ①&lt;/button&gt;

          {/* ② bind：可以在定义处固定部分参数 */}
          &lt;button onClick={onRemove.bind(null, it.id)}&gt;删除 ②&lt;/button&gt;

          {/* ③ data-* + 事件委托：大量同构子项时的性能写法 */}
          &lt;button data-id={it.id} onClick={handleClickDelegated}&gt;删除 ③&lt;/button&gt;
        &lt;/li&gt;
      ))}
    &lt;/ul&gt;
  );

  function handleClickDelegated(e) {
    onRemove(Number(e.target.dataset.id));
  }
}</code></pre>
  <table>
    <colgroup><col style="width:20%"><col style="width:40%"><col style="width:40%"></colgroup>
    <thead><tr><th>方式</th><th>优点</th><th>代价</th></tr></thead>
    <tbody>
      <tr><td>内联箭头</td><td>直观、灵活</td><td>每次渲染产生新函数，会让 memo 子组件失效（第 48 章）</td></tr>
      <tr><td>bind</td><td>语法紧凑</td><td>同样产生新函数，可读性一般</td></tr>
      <tr><td>data-*</td><td>父层一个 handler，子项零函数</td><td>类型信息丢失，需转字符串</td></tr>
    </tbody>
  </table>
  <div class="note"><strong>实践建议</strong>：普通列表用 ①；成千上万行表格的行操作用 ③ 或虚拟列表（第 50 章）；性能敏感且需要固定引用时配合 <code>useCallback</code>（第 49 章）。</div>
</section>""",
"""<section id="sec5" class="card">
  <h2><span class="num">5.4</span> 阻止默认行为与冒泡</h2>
  <pre class="code" data-lang="jsx"><code>function FormDemo() {
  const handleSubmit = (e) =&gt; {
    e.preventDefault();        // 阻止表单默认提交导致的整页刷新
    // e.stopPropagation();    // 阻止向父元素冒泡（极少需要）
    const data = new FormData(e.target);
    console.log(Object.fromEntries(data));
  };

  return (
    &lt;form onSubmit={handleSubmit}&gt;
      &lt;input name="username" /&gt;
      &lt;button type="submit"&gt;提交&lt;/button&gt;   {/* type="submit" 才触发 */}
    &lt;/form&gt;
  );
}</code></pre>
  <h4>三个阶段与 React 的对应属性</h4>
  <table>
    <colgroup><col style="width:24%"><col style="width:38%"><col style="width:38%"></colgroup>
    <thead><tr><th>阶段</th><th>原生写法</th><th>React JSX 属性</th></tr></thead>
    <tbody>
      <tr><td>捕获（Capture）</td><td><code>addEventListener(..., true)</code></td><td><code>onClickCapture</code></td></tr>
      <tr><td>目标（Target）</td><td>—</td><td><code>onClick</code></td></tr>
      <tr><td>冒泡（Bubble）</td><td>默认 false</td><td><code>onClick</code></td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="jsx"><code>// 典型场景：点击卡片任意处跳转，但点内部按钮不跳转
function Card({ onClick }) {
  return (
    &lt;div onClick={onClick}&gt;
      &lt;h4&gt;标题&lt;/h4&gt;
      &lt;button onClick={(e) =&gt; { e.stopPropagation(); doDelete(); }}&gt;删除&lt;/button&gt;
    &lt;/div&gt;
  );
}</code></pre>
  <div class="warn-box"><span class="tag-pit">坑</span>原生 <code>addEventListener</code> 里写的监听器<strong>不受 React 合成事件约束</strong>：<code>e.stopPropagation()</code> 能阻止 React 内部冒泡，但无法阻止挂在 document 上的原生监听；反之用原生 <code>stopPropagation</code> 会同时挡住 React 事件。混合使用时务必清楚两套体系的先后顺序（下一节）。</div>
  <h4>滚动 / 触摸与 passive</h4>
  <p><code>touchmove</code>、<code>wheel</code>、<code>scroll</code> 等事件里调用 <code>preventDefault</code> 在现代浏览器中需要 <code>{ passive: false }</code>，而 React 的 <code>onWheel</code> 等默认是 passive。确实要阻止滚动时，用 <code>useEffect + el.addEventListener('touchmove', fn, { passive: false })</code>。</p>
</section>""",
"""<section id="sec6" class="card">
  <h2><span class="num">5.5</span> 事件委托：React 到底把监听挂在哪</h2>
  <p>不是给每个 <code>&lt;button onClick&gt;</code> 都挂一个真实监听器——React 用的是<strong>事件委托</strong>：在容器上挂少量监听器，由它统一分发。</p>
  <div class="diagram">
    <svg viewBox="0 0 800 220" role="img" aria-label="React 事件委托位置示意">
      <rect x="120" y="20" width="560" height="40" rx="8" fill="#fefce8" stroke="#d97706"/>
      <text x="400" y="45" text-anchor="middle" font-size="12.5" fill="#b45309">React 17+：所有事件委托到 createRoot 的根容器 #root</text>
      <rect x="200" y="80" width="400" height="34" rx="8" fill="#f0f5e6" stroke="#3d7a4f"/>
      <text x="400" y="102" text-anchor="middle" font-size="12" fill="#2d6a3f">App（根容器）</text>
      <rect x="260" y="130" width="120" height="32" rx="8" fill="#fff" stroke="#4f6348"/>
      <text x="320" y="151" text-anchor="middle" font-size="11.5" fill="#1f2e1f">&lt;Card&gt;</text>
      <rect x="420" y="130" width="120" height="32" rx="8" fill="#fff" stroke="#4f6348"/>
      <text x="480" y="151" text-anchor="middle" font-size="11.5" fill="#1f2e1f">&lt;Card&gt;</text>
      <rect x="300" y="176" width="80" height="30" rx="6" fill="#fff" stroke="#4f6348"/>
      <text x="340" y="195" text-anchor="middle" font-size="11" fill="#1f2e1f">&lt;button&gt;</text>
      <rect x="450" y="176" width="80" height="30" rx="6" fill="#fff" stroke="#4f6348"/>
      <text x="490" y="195" text-anchor="middle" font-size="11" fill="#1f2e1f">&lt;button&gt;</text>
      <path d="M340 176 L340 165 L400 165 L400 60" fill="none" stroke="#7a8a70" stroke-width="1.2" stroke-dasharray="4 3"/>
      <text x="410" y="90" font-size="11" fill="#7a8a70">冒泡到根容器后由 React 分发给对应组件的 handler</text>
    </svg>
    <p class="diagram-caption">图 5-1 React 17+ 事件委托到根容器（16 及以前委托到 document）</p>
  </div>
  <p><strong>为什么要改</strong>（React 17 的重要变更）：</p>
  <ul>
    <li>一个页面<strong>存在多个 React 版本/多个根</strong>时，旧方案事件都挂在 document 上会互相干扰；改到根容器后天然隔离；</li>
    <li>混用其他库（jQuery）时，在 <code>#root</code> 外层 <code>stopPropagation</code> 就能彻底阻止 React 收到事件，行为可预测。</li>
  </ul>
  <pre class="code" data-lang="jsx"><code>// 委托带来的一个重要现象：多个同类型 handler 按 React 树顺序执行
&lt;div onClick={() =&gt; console.log('父')}&gt;     {/* 后执行 */}
  &lt;button onClick={() =&gt; console.log('子')} /&gt;  {/* 先执行 */}
&lt;/div&gt;</code></pre>
  <p class="key-sentence">调试价值：在 DevTools 的 Elements 面板看 <code>#root</code> 的 Event Listeners，你会发现只有 React 挂的少数几个监听器——所有 onClick 都在数据流里，不在 DOM 上。</p>
</section>""",
"""<section id="sec7" class="card">
  <h2><span class="num">5.6</span> 常见坑清单</h2>
  <table>
    <colgroup><col style="width:34%"><col style="width:66%"></colgroup>
    <thead><tr><th>现象</th><th>原因 / 解法</th></tr></thead>
    <tbody>
      <tr><td>页面一加载就自动执行点击逻辑</td><td><code>onClick={fn()}</code> 传成了调用结果；改为 <code>onClick={fn}</code> 或箭头包装</td></tr>
      <tr><td>表单提交后整页刷新</td><td>没有 <code>e.preventDefault()</code>，或按钮缺 <code>type="button"</code></td></tr>
      <tr><td>异步里读 <code>e.target</code> 为 null</td><td>React 16 事件池遗留；17+ 已修复，升级即可（老项目可 <code>e.persist()</code>）</td></tr>
      <tr><td>子元素点击导致父元素同时响应</td><td>冒泡；在子元素 handler 里 <code>e.stopPropagation()</code></td></tr>
      <tr><td><code>onScroll</code> 不触发</td><td>滚动容器必须真的可滚动且有固定高度；监听 window 滚动要用原生监听</td></tr>
      <tr><td>移动端滚动里阻止默认无效</td><td>passive 限制，改用原生监听并显式 <code>{ passive: false }</code></td></tr>
      <tr><td>给自定义组件写 <code>onClick</code> 无效</td><td>自定义组件上的 onClick 只是普通 props，需在内部转发到真实 DOM：<code>&lt;div onClick={props.onClick}&gt;</code></td></tr>
    </tbody>
  </table>
</section>""",
"""<section id="sec8" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:30%"><col style="width:70%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>绑定写法</td><td>onClick 后传函数引用；传调用会渲染时立即执行</td></tr>
      <tr><td>合成事件</td><td>React 包装的事件对象，跨浏览器一致，17+ 无事件池</td></tr>
      <tr><td>target vs currentTarget</td><td>前者是真实触发者，后者是绑定者</td></tr>
      <tr><td>传参</td><td>箭头包装 / bind / data-* 委托，按列表规模选择</td></tr>
      <tr><td>三阶段</td><td>捕获用 <code>onClickCapture</code>，默认走冒泡</td></tr>
      <tr><td>事件委托位置</td><td>React 17+ 挂在 <code>createRoot</code> 的根容器上</td></tr>
    </tbody>
  </table>
</section>""",
"""<section id="sec9" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>下面代码有什么问题？修好后说明现象：<code>&lt;button onClick={remove(id)}&gt;删除&lt;/button&gt;</code></div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>写一个搜索框组件：按回车提交；按 Esc 清空；输入时用 <code>e.target.name</code> 支持多个输入框共用一个 handleChange（配合 useState 对象）</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>实现一个"点击外部关闭"的下拉菜单：在 useEffect 里用原生 <code>document.addEventListener('click')</code>，说明为什么这里不能用 React 的 onClick，以及卸载时如何正确清理。</div>
  <p class="note">参考答案见附录 C。下一章：条件渲染的写法演进与 key 的真相。</p>
</section>""",
    ],
)

build(**ch4)
build(**ch5)

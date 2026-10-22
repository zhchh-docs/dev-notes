# -*- coding: utf-8 -*-
"""第一篇：第 8、9 章（收尾）"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import build

P = "10_第一篇_入门"

# ─────────────────────────── 第 8 章 ───────────────────────────
ch8 = dict(
    part_dir=P,
    fname="008_第8章_受控与非受控表单.html",
    num=8,
    title="受控与非受控表单",
    part="第一篇 入门",
    meta="第 8 章 / 共 64 章 · 预计 45 分钟 · 承第 7 章",
    desc="表单是前端最常见的复杂交互，也是 React 里唯一需要「双向」思考的地方。本章讲清受控与非受控的分野、各类表单元素的正确写法、一个 handler 管多字段的技巧，以及为什么企业级项目最终会走向 react-hook-form + zod。",
    prev="007_第7章_useState状态与函数式更新.html", prev_txt="第 7 章",
    nxt="009_第9章_样式方案CSSModules与原子类.html", next_txt="第 9 章",
    toc=[("sec1", "本章目标"), ("sec2", "8.1 受控组件：数据唯一真源"),
         ("sec3", "8.2 非受控组件：让 DOM 自己管"),
         ("sec4", "8.3 各类表单元素的正确写法"),
         ("sec5", "8.4 一个 handler 管多个字段"),
         ("sec6", "8.5 提交、校验与错误提示"),
         ("sec7", "8.6 选型建议与常见坑"),
         ("sec8", "本章小结"), ("sec9", "本章习题")],
    sections=[
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>说出<strong>受控 / 非受控</strong>的定义与各自的适用场景；</li>
    <li>正确书写 text / checkbox / radio / select / textarea / file 六类控件；</li>
    <li>用<strong>一个 handler</strong>管理多个字段（含 TS 写法），避免每个输入框一个 useState；</li>
    <li>实现基础表单校验与错误提示，理解"提交时校验 / 输入时校验 / 失焦校验"的差别；</li>
    <li>知道为什么大型表单要用 <code>react-hook-form</code> + <code>zod</code>（第 35、36 章）。</li>
  </ul>
</section>""",
"""<section id="sec2" class="card">
  <h2><span class="num">8.1</span> 受控组件：数据唯一真源</h2>
  <p><strong>受控组件</strong>：表单元素的值由 React 的 state 决定，用户输入通过 <code>onChange</code> 写回 state。它完全符合第 1 章的 <code>UI = f(state)</code>——输入框显示的永远是 state 的投影。</p>
  <pre class="code" data-lang="jsx"><code>function LoginForm() {
  const [form, setForm] = useState({ username: '', password: '' });

  const update = (key) =&gt; (e) =&gt; setForm(f =&gt; ({ ...f, [key]: e.target.value }));

  return (
    &lt;form onSubmit={submit}&gt;
      &lt;input value={form.username} onChange={update('username')} placeholder="用户名" /&gt;
      &lt;input type="password" value={form.password} onChange={update('password')} /&gt;
      &lt;button type="submit"&gt;登录&lt;/button&gt;
    &lt;/form&gt;
  );
}</code></pre>
  <div class="lead">受控的收益：<strong>值随时可用、可随时改写</strong>。因为输入框内容就是 state，你可以轻松做"输入即时转大写""禁用某些字符""根据 A 字段自动填 B 字段"，甚至做"撤销/重做"。</div>
  <div class="warn-box"><span class="tag-pit">坑 1</span>给了 <code>value</code> 却没给 <code>onChange</code>，输入框会变成<strong>只读且带警告</strong>（You provided a `value` prop to a form field without an `onChange` handler）。若还需要"多个更新累加"，务必用第 7 章讲的函数式更新。</div>
</section>""",
"""<section id="sec3" class="card">
  <h2><span class="num">8.2</span> 非受控组件：让 DOM 自己管</h2>
  <p><strong>非受控组件</strong>：不给 <code>value</code>，只给 <code>defaultValue</code>，值由 DOM 自己维护，需要时用 ref 读取。</p>
  <pre class="code" data-lang="jsx"><code>function SearchBar({ onSearch }) {
  const inputRef = useRef(null);

  const submit = (e) =&gt; {
    e.preventDefault();
    onSearch(inputRef.current.value);   // 用时才读，渲染期间不参与
  };

  return (
    &lt;form onSubmit={submit}&gt;
      &lt;input ref={inputRef} defaultValue="" placeholder="输入关键词" /&gt;
      &lt;button&gt;搜索&lt;/button&gt;
    &lt;/form&gt;
  );
}</code></pre>
  <table>
    <colgroup><col style="width:20%"><col style="width:40%"><col style="width:40%"></colgroup>
    <thead><tr><th>维度</th><th>受控</th><th>非受控</th></tr></thead>
    <tbody>
      <tr><td>值存在哪</td><td>React state</td><td>DOM 节点</td></tr>
      <tr><td>每次输入是否重渲染</td><td>是</td><td>否</td></tr>
      <tr><td>值能否被程序随时改写</td><td>可以</td><td>只能操作 DOM</td></tr>
      <tr><td>适合场景</td><td>需要联动/校验/格式化的表单</td><td>搜索框、第三方插件嵌入、大表单性能敏感</td></tr>
    </tbody>
  </table>
  <p class="key-sentence">默认选择受控；只有当你明确意识到"每次输入都重渲染"成为瓶颈，或必须与某个直接操作 DOM 的第三方库协作时，才考虑非受控。</p>
  <div class="note"><strong>file input 只能非受控</strong>：出于安全，浏览器不允许 JS 设置 <code>&lt;input type="file"&gt;</code> 的值，只能用 ref 读取 <code>files[0]</code>，或第 61 章讲的拖拽/粘贴上传。</div>
</section>""",
"""<section id="sec4" class="card">
  <h2><span class="num">8.3</span> 各类表单元素的正确写法</h2>
  <table>
    <colgroup><col style="width:20%"><col style="width:40%"><col style="width:40%"></colgroup>
    <thead><tr><th>元素</th><th>取值</th><th>受控写法要点</th></tr></thead>
    <tbody>
      <tr><td>input[type=text]</td><td><code>e.target.value</code></td><td><code>value + onChange</code></td></tr>
      <tr><td>textarea</td><td><code>e.target.value</code></td><td>用 <code>value</code> 属性，而不是子节点</td></tr>
      <tr><td>checkbox</td><td><code>e.target.checked</code></td><td><code>checked + onChange</code></td></tr>
      <tr><td>radio</td><td><code>e.target.value</code></td><td>同组 name 相同，<code>checked={val===item.value}</code></td></tr>
      <tr><td>select</td><td><code>e.target.value</code></td><td>写在 <code>&lt;select value&gt;</code> 上，而非 option 的 selected</td></tr>
      <tr><td>select multiple</td><td>Array.from(target.selectedOptions).map(o =&gt; o.value)</td><td>value 为数组</td></tr>
      <tr><td>file</td><td><code>e.target.files[0]</code></td><td>只能非受控</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="jsx"><code>function ProfileForm() {
  const [form, setForm] = useState({
    name: '', gender: 'male', agree: false, city: 'bj', tags: [], avatar: null,
  });
  const patch = (k, v) =&gt; setForm(f =&gt; ({ ...f, [k]: v }));

  return (
    &lt;form&gt;
      &lt;input value={form.name} onChange={e =&gt; patch('name', e.target.value)} /&gt;

      &lt;label&gt;&lt;input type="radio" name="gender" value="male"
        checked={form.gender === 'male'} onChange={e =&gt; patch('gender', e.target.value)} /&gt;男&lt;/label&gt;
      &lt;label&gt;&lt;input type="radio" name="gender" value="female"
        checked={form.gender === 'female'} onChange={e =&gt; patch('gender', e.target.value)} /&gt;女&lt;/label&gt;

      &lt;label&gt;&lt;input type="checkbox"
        checked={form.agree} onChange={e =&gt; patch('agree', e.target.checked)} /&gt;同意条款&lt;/label&gt;

      &lt;select value={form.city} onChange={e =&gt; patch('city', e.target.value)}&gt;
        &lt;option value="bj"&gt;北京&lt;/option&gt;
        &lt;option value="sh"&gt;上海&lt;/option&gt;
      &lt;/select&gt;

      &lt;select multiple value={form.tags}
        onChange={e =&gt; patch('tags', Array.from(e.target.selectedOptions, o =&gt; o.value))}&gt;
        &lt;option value="js"&gt;JS&lt;/option&gt;&lt;option value="ts"&gt;TS&lt;/option&gt;
      &lt;/select&gt;

      &lt;input type="file" onChange={e =&gt; patch('avatar', e.target.files[0])} /&gt;
    &lt;/form&gt;
  );
}</code></pre>
</section>""",
"""<section id="sec5" class="card">
  <h2><span class="num">8.4</span> 一个 handler 管多个字段</h2>
  <p>给十个字段写十个 <code>useState</code> 是典型的新手代码。更合适的做法有两种：</p>
  <h4>方案一：name 属性 + 计算属性名</h4>
  <pre class="code" data-lang="jsx"><code>const [form, setForm] = useState({ username: '', email: '', phone: '' });

const handleChange = (e) =&gt; {
  const { name, value, type, checked } = e.target;
  setForm(f =&gt; ({ ...f, [name]: type === 'checkbox' ? checked : value }));
};

&lt;input name="username" value={form.username} onChange={handleChange} /&gt;
&lt;input name="email"    value={form.email}    onChange={handleChange} /&gt;</code></pre>
  <h4>方案二：FormData（原生 API，适合字段多且无需即时联动）</h4>
  <pre class="code" data-lang="jsx"><code>function submit(e) {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.target));
  // { username: 'zs', email: 'a@b.com', ... }
  onSubmit(data);
}</code></pre>
  <p class="pit-sentence">注意：<code>FormData</code> 只能拿到带 <code>name</code> 且<strong>非禁用</strong>的字段；<code>checkbox</code> 未勾选时不出现在结果里，需要的话显式处理。</p>
</section>""",
"""<section id="sec6" class="card">
  <h2><span class="num">8.5</span> 提交、校验与错误提示</h2>
  <pre class="code" data-lang="jsx"><code>function RegisterForm() {
  const [form, setForm] = useState({ email: '', password: '', confirm: '' });
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);

  const validate = (f) =&gt; {
    const err = {};
    if (!/^\\S+@\\S+\\.\\S+$/.test(f.email)) err.email = '邮箱格式不正确';
    if (f.password.length &lt; 8) err.password = '密码至少 8 位';
    if (f.password !== f.confirm) err.confirm = '两次输入不一致';
    return err;
  };

  const submit = async (e) =&gt; {
    e.preventDefault();
    const err = validate(form);
    setErrors(err);
    if (Object.keys(err).length) return;      // 校验不过不提交

    setSubmitting(true);
    try {
      await api.register(form);
    } finally {
      setSubmitting(false);                   // 无论成败都要结束提交态
    }
  };

  return (
    &lt;form onSubmit={submit} noValidate&gt;
      &lt;input name="email" value={form.email}
        onChange={e =&gt; setForm(f =&gt; ({ ...f, email: e.target.value }))} /&gt;
      {errors.email &amp;&amp; &lt;p className="error"&gt;{errors.email}&lt;/p&gt;}
      &lt;button disabled={submitting}&gt;{submitting ? '提交中…' : '注册'}&lt;/button&gt;
    &lt;/form&gt;
  );
}</code></pre>
  <table>
    <colgroup><col style="width:24%"><col style="width:38%"><col style="width:38%"></colgroup>
    <thead><tr><th>校验时机</th><th>优点</th><th>缺点</th></tr></thead>
    <tbody>
      <tr><td>提交时</td><td>实现最简单，不打断输入</td><td>反馈滞后</td></tr>
      <tr><td>失焦时（onBlur）</td><td>体验好，干扰小</td><td>需额外状态记录 touched</td></tr>
      <tr><td>输入时（onChange）</td><td>反馈即时</td><td>刚输第一个字符就报红，体验差</td></tr>
    </tbody>
  </table>
  <div class="note"><strong>实践推荐</strong>：<code>touched</code> 之后才报错（首次不改脏不提示）。这套"touched + dirty + errors"的组合正是 <code>react-hook-form</code> 的核心，详见第 35、36 章（与 zod 配合做到"校验规则即类型"）。</div>
</section>""",
"""<section id="sec7" class="card">
  <h2><span class="num">8.6</span> 选型建议与常见坑</h2>
  <ul>
    <li><strong>小表单（≤ 5 个字段）</strong>：手写受控即可，代码量比引入库还少。</li>
    <li><strong>中大型表单</strong>：<code>react-hook-form</code>（非受控思路 + 精确重渲染）性能与开发体验双优。</li>
    <li><strong>跨字段联动强的动态表单</strong>：受控 + 状态机心智，或 RHF 的 <code>watch</code>。</li>
    <li><strong>校验库</strong>：zod / yup，产出 schema 同时喂给 TS 类型。</li>
  </ul>
  <div class="warn-box"><span class="tag-pit">坑清单</span>
    <ul>
      <li><code>value</code> 忘了配 <code>onChange</code> → 输入框不能打字；</li>
      <li><code>defaultValue</code> 初始值来自异步数据时：<strong>数据回来再渲染也改不动默认值</strong>，需 <code>key={data.id}</code> 重置或改为受控；</li>
      <li>把受控值初始化为 <code>null</code>（而非空字符串）会报 <em>changing an uncontrolled input to be controlled</em>；</li>
      <li><code>disabled</code> 的字段不会被 FormData 收集；</li>
      <li>提交后 <code>finally</code> 里还原 <code>submitting</code>，否则按钮永久 loading。</li>
    </ul>
  </div>
</section>""",
"""<section id="sec8" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:30%"><col style="width:70%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>受控</td><td>value + onChange，state 是唯一真源，默认方案</td></tr>
      <tr><td>非受控</td><td>defaultValue + ref，DOM 自管；file input 只能非受控</td></tr>
      <tr><td>checkbox/radio</td><td>取 <code>checked</code>；radio 靠 name 分组</td></tr>
      <tr><td>select</td><td>value 写在 select 上，多选取 selectedOptions</td></tr>
      <tr><td>多字段技巧</td><td>name + 计算属性名，或 FormData 一次性收集</td></tr>
      <tr><td>校验时机</td><td>touched 后再报错；复杂表单交给 RHF + zod</td></tr>
    </tbody>
  </table>
</section>""",
"""<section id="sec9" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>把一个有三个字段的搜索表单改造成"一个 handler 管全部"，要求支持 checkbox 类型。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>实现带 touched 语义的注册表单：邮箱、密码、确认密码三字段，首次不改脏不报错，失焦后才提示；提交时全量校验，失败则聚焦第一个错误字段。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>把一个 20 字段的表单从"每字段一个 useState"重构成"单一 form 对象 + 通用 patch 函数"，并说明：为什么 RHF 用非受控能避免每次输入带来的整表单重渲染。</div>
  <p class="note">参考答案见附录 C。下一章：样式方案——CSS Modules 与原子类。</p>
</section>""",
    ],
)

# ─────────────────────────── 第 9 章 ───────────────────────────
ch9 = dict(
    part_dir=P,
    fname="009_第9章_样式方案CSSModules与原子类.html",
    num=9,
    title="样式方案：CSS Modules 与原子类",
    part="第一篇 入门",
    meta="第 9 章 / 共 64 章 · 预计 40 分钟 · 第一篇收尾",
    desc="React 不负责写样式，但怎么写样式直接决定项目的可维护性。本章把五种主流方案放在同一张表上对比，重点讲 CSS Modules（中文项目默认推荐）与 Tailwind 原子类（新项目增长最快），以及动态类名、主题变量与样式冲突的处理。",
    prev="008_第8章_受控与非受控表单.html", prev_txt="第 8 章",
    nxt="../20_第二篇_Hooks核心/010_第10章_useEffect同步器心智.html", next_txt="第 10 章",
    toc=[("sec1", "本章目标"), ("sec2", "9.1 五种样式方案横向对比"),
         ("sec3", "9.2 CSS Modules 完整用法"),
         ("sec4", "9.3 动态类名：clsx / classnames"),
         ("sec5", "9.4 原子类：Tailwind 的心智模型"),
         ("sec6", "9.5 CSS 变量与主题切换"),
         ("sec7", "9.6 常见坑与选型清单"),
         ("sec8", "本章小结"), ("sec9", "本章习题")],
    sections=[
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>在一个表格里看清五种样式方案的取舍：内联、普通 CSS、CSS Modules、CSS-in-JS、原子类；</li>
    <li>熟练使用 <strong>CSS Modules</strong>：<code>composes</code>、<code>:global</code>、哈希类名规则；</li>
    <li>会用 <code>clsx</code> 处理条件类名，避免字符串拼接的脏代码；</li>
    <li>理解 <strong>Tailwind</strong> 的设计哲学与适用边界，能判断要不要用；</li>
    <li>实现基于 <strong>CSS 变量</strong>的主题切换。</li>
  </ul>
  <div class="note">本书第七篇第 56 章会落到具体组件库（Ant Design）的定制方案，本章只打地基。</div>
</section>""",
"""<section id="sec2" class="card">
  <h2><span class="num">9.1</span> 五种样式方案横向对比</h2>
  <table>
    <colgroup><col style="width:16%"><col style="width:22%"><col style="width:22%"><col style="width:22%"><col style="width:18%"></colgroup>
    <thead><tr><th>方案</th><th>作用域</th><th>动态样式</th><th>上手成本</th><th>适合</th></tr></thead>
    <tbody>
      <tr><td>内联 style</td><td>单节点</td><td>天然支持</td><td>极低</td><td>少量动态值<br>（宽高、定位）</td></tr>
      <tr><td>普通 CSS</td><td>全局</td><td>差</td><td>低</td><td>小型 Demo</td></tr>
      <tr><td>CSS Modules</td><td>组件级</td><td>中</td><td>低</td><td>中后台、设计规范明确</td></tr>
      <tr><td>CSS-in-JS<br>（styled / emotion）</td><td>组件级</td><td>强（可用 props）</td><td>中</td><td>主题强、<br>组件库产品</td></tr>
      <tr><td>原子类 Tailwind</td><td>原子</td><td>中</td><td>中</td><td>快速迭代、<br>设计一致性差时</td></tr>
    </tbody>
  </table>
  <p>判断的第一性问题其实是：<strong>这个项目的样式规范由谁定义？</strong></p>
  <ul>
    <li>有专职 UI/设计并且要长期维护 → <strong>CSS Modules / CSS-in-JS</strong>，语义类名便于对话与迭代；</li>
    <li>快速出原型、追求跨项目视觉一致 → <strong>Tailwind</strong>；</li>
    <li>同时使用组件库 → 以组件库主题为主，业务代码用 Modules 兜细节。</li>
  </ul>
</section>""",
"""<section id="sec3" class="card">
  <h2><span class="num">9.2</span> CSS Modules 完整用法</h2>
  <p>Vite 内置支持：文件名带 <code>.module.css</code> 即自动启用，无需任何配置。</p>
  <pre class="code" data-lang="css"><code>/* Button.module.css */
.btn { padding: 6px 16px; border: 1px solid #d8e2cc; border-radius: 6px; }
.primary { background: #2d6a3f; color: #fff; }
/* 组合：复用其它类的规则 */
.large { composes: btn; padding: 10px 22px; }
/* 引用全局类 */
.icon { composes: app-icon from global; }
/* 局部作用域里写全局选择器 */
.card :global(.ant-btn) { margin-left: 8px; }</code></pre>
  <pre class="code" data-lang="jsx"><code>import styles from './Button.module.css';

export default function Button({ type = 'primary', size, children }) {
  const cls = [styles.btn, styles[type], size === 'large' &amp;&amp; styles.large]
    .filter(Boolean).join(' ');
  return &lt;button className={cls}&gt;{children}&lt;/button&gt;;
}</code></pre>
  <p>构建后类名会变成 <code>_btn_1a2b3</code> 这类哈希串，因此<strong>不同文件中的同名类不会互相污染</strong>。</p>
  <div class="warn-box"><span class="tag-pit">坑 1</span>选择器里写标签选择器（<code>.btn span</code>）没问题，但<strong>不能靠外部覆写模块类</strong>：哈希类名对外不可见。组件应当在 props 上开放 <code>className</code> 让外部合并（第 4 章准则 6）。</div>
  <div class="warn-box"><span class="tag-pit">坑 2</span><code>styles['primary']</code> 能用，但 <code>styles.primary</code> 更利于 IDE 补全；连字符类名只能用方括号：<code>styles['btn-lg']</code>。建议统一用 camelCase 命名。</div>
</section>""",
"""<section id="sec4" class="card">
  <h2><span class="num">9.3</span> 动态类名：clsx / classnames</h2>
  <pre class="code" data-lang="bash"><code>npm install clsx</code></pre>
  <pre class="code" data-lang="jsx"><code>import clsx from 'clsx';

function Alert({ type = 'info', muted, className, children }) {
  return (
    &lt;div className={clsx(styles.alert, styles[type], muted &amp;&amp; styles.muted, className)}&gt;
      {children}
    &lt;/div&gt;
  );
}

// 也支持对象形式，条件复杂时更易读
clsx({
  [styles.btn]: true,
  [styles.disabled]: disabled,
  [styles.large]: size === 'large',
});</code></pre>
  <p class="key-sentence">原则：类名组装逻辑放进 clsx，JSX 里只留一行。这样 review 时一眼能看出"哪些类在哪些条件下生效"。</p>
</section>""",
"""<section id="sec5" class="card">
  <h2><span class="num">9.4</span> 原子类：Tailwind 的心智模型</h2>
  <p>Tailwind 提供大量<strong>单一职责的工具类</strong>，直接在 JSX 里组合出样式：</p>
  <pre class="code" data-lang="jsx"><code>// 不再先写 CSS 再起类名，而是"所见即所得"
&lt;button className="px-4 py-2 rounded-md bg-green-700 text-white hover:bg-green-800
                   disabled:opacity-50 transition-colors"&gt;
  提交
&lt;/button&gt;</code></pre>
  <pre class="code" data-lang="bash"><code># Vite + React 接入（Tailwind v3）
npm i -D tailwindcss postcss autoprefixer
npx tailwindcss init -p</code></pre>
  <pre class="code" data-lang="js"><code>// tailwind.config.js
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],  // 据此摇树，务必写全
  theme: { extend: { colors: { brand: '#2d6a3f' } } },
  plugins: [],
};</code></pre>
  <table>
    <colgroup><col style="width:24%"><col style="width:38%"><col style="width:38%"></colgroup>
    <thead><tr><th>维度</th><th>收益</th><th>代价</th></tr></thead>
    <tbody>
      <tr><td>开发速度</td><td>不用起类名、不用切文件</td><td>JSX 变长，可读性两极分化</td></tr>
      <tr><td>一致性</td><td>配色/间距被约束在几档</td><td>设计师给的任意像素值难以还原</td></tr>
      <tr><td>产物体积</td><td>摇树后很小</td><td><code>content</code> 配错会导致样式全丢</td></tr>
      <tr><td>动态类</td><td>可用模板字符串</td><td><strong>不能拼接</strong>：<code>`text-${color}`</code> 会被摇树删掉</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="jsx"><code>// ✗ 动态拼接无效（构建时扫不到完整类名）
&lt;span className={`text-${size}`} /&gt;

// ✓ 建映射表，写出完整字符串
const SIZE = { sm: 'text-sm', md: 'text-base', lg: 'text-lg' };
&lt;span className={SIZE[size]} /&gt;</code></pre>
</section>""",
"""<section id="sec6" class="card">
  <h2><span class="num">9.5</span> CSS 变量与主题切换</h2>
  <p>主题切换最省心的实现是 <strong>CSS 自定义属性</strong>：变量随根节点切换而全局生效，无需 React 重渲染。</p>
  <pre class="code" data-lang="css"><code>/* theme.css */
:root {
  --color-bg: #ffffff;
  --color-text: #1f2e1f;
  --color-primary: #2d6a3f;
}
[data-theme='dark'] {
  --color-bg: #152010;
  --color-text: #d8e2cc;
  --color-primary: #4f8a63;
}
.card { background: var(--color-bg); color: var(--color-text); }</code></pre>
  <pre class="code" data-lang="jsx"><code>function ThemeToggle() {
  const [dark, setDark] = useState(false);

  useEffect(() =&gt; {
    document.documentElement.dataset.theme = dark ? 'dark' : 'light';
  }, [dark]);

  return &lt;button onClick={() =&gt; setDark(d =&gt; !d)}&gt;切换主题&lt;/button&gt;;
}</code></pre>
  <p>关键点：<strong>把主题写在 DOM 属性上，而不是往每个组件传 props</strong>——后者会让主题变更引发全树重渲染。这一点在第 21 章（Context 粒度）会再回来。</p>
</section>""",
"""<section id="sec7" class="card">
  <h2><span class="num">9.6</span> 常见坑与选型清单</h2>
  <ol>
    <li><strong>样式不生效</strong>：检查优先级（第三方库用 <code>!important</code> 时，业务侧可用 <code>:where()</code> 降低自身优先级、或提高层级）；</li>
    <li><strong>CSS Modules 类名冲突</strong>：只可能发生在同一文件内；<code>:global</code> 声明的类会逃逸出作用域，慎用；</li>
    <li><strong>全局样式放哪</strong>：<code>src/index.css</code>（reset、字体、变量），组件样式一律 Modules；</li>
    <li><strong>动态内联值的性能</strong>：拖拽/动画场景直接改 <code>style</code> 会频繁触发样式计算，宜用 CSS 变量 + transform；</li>
    <li><strong>产物体积</strong>：Tailwind 配好 <code>content</code>；Modules 天然按需。</li>
  </ol>
  <div class="note"><strong>本书默认</strong>：后续章节示例统一使用 CSS Modules 的类名写法（如 <code>&lt;div className={styles.panel}&gt;</code>），并在必要时加一行 Tailwind 等价写法。</div>
</section>""",
"""<section id="sec8" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:30%"><col style="width:70%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>方案选择</td><td>有设计规范用 Modules，快速迭代用 Tailwind，动态主题用 CSS-in-JS</td></tr>
      <tr><td>CSS Modules</td><td>Vite 零配置，<code>.module.css</code> 出哈希类名，天然隔离</td></tr>
      <tr><td>composes</td><td>类之间复用；<code>from global</code> 引入全局类</td></tr>
      <tr><td>动态类名</td><td>clsx 组装，组件开放 className 让外部合并</td></tr>
      <tr><td>Tailwind 注意</td><td>动态类名必须完整出现，禁止字符串拼接</td></tr>
      <tr><td>主题</td><td>CSS 变量 + 根节点 data-theme，避免全树重渲染</td></tr>
    </tbody>
  </table>
</section>""",
"""<section id="sec9" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>用 CSS Modules 写一个 <code>Tag</code> 组件（三种颜色 + 两种尺寸），并允许外部通过 <code>className</code> 追加类名。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>用 CSS 变量实现明暗主题：要求切换时不触发任何 React 重渲染（除 Toggle 自身），并说明为什么不把 theme 放进 Context 传给所有组件。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>把同一张"数据统计卡片"分别用 CSS Modules 与 Tailwind 实现，对比：代码行数、可复用方式、设计还原成本、新手上手难度，写下你的选型结论。</div>
  <p class="note">参考答案见附录 C。<strong>下一篇</strong>：进入本书最核心的一段——Hooks 体系。</p>
</section>""",
    ],
)

build(**ch8)
build(**ch9)

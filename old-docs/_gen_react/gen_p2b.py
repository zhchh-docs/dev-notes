# -*- coding: utf-8 -*-
"""第二篇：第 12、13 章"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import build

P = "20_第二篇_Hooks核心"

# ─────────────────────────── 第 12 章 ──────────────────────────
ch12 = dict(
    part_dir=P,
    fname="012_第12章_useLayoutEffect与绘制时机.html",
    num=12,
    title="useLayoutEffect 与绘制时机",
    part="第二篇 Hooks 核心",
    meta="第 12 章 / 共 64 章 · 预计 40 分钟 · 承第 10 章",
    desc="为什么有些"闪烁问题"加了 useEffect 怎么都修不好？因为 useEffect 在浏览器绘制之后才跑。本章讲清 useLayoutEffect 与 useEffect 的差别、应同步修改 DOM 的三类场景、以及它在 SSR 与性能上的代价。",
    prev="011_第11章_依赖数组与cleanup三时机.html", prev_txt="第 11 章",
    nxt="013_第13章_useRefDOM引用与可变值.html", next_txt="第 13 章",
    toc=[("sec1", "本章目标"), ("sec2", "12.1 两个 effect 的时序差异"),
         ("sec3", "12.2 必须用 layout effect 的三类场景"),
         ("sec4", "12.3 案例：Tooltip 定位"),
         ("sec5", "12.4 案例：滚动位置恢复与自适应高度"),
         ("sec6", "12.5 SSR 警告与替代方案"),
         ("sec7", "12.6 性能代价与使用守则"),
         ("sec8", "本章小结"), ("sec9", "本章习题")],
    sections=[
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>能画出 <code>useLayoutEffect</code> 与 <code>useEffect</code> 在浏览器渲染管线上的确切位置；</li>
    <li>知道什么时候"必须用"layout effect：<strong>测量 DOM 后同步改动 DOM</strong>；</li>
    <li>能实现 Tooltip 定位、滚动恢复、自适应高度三个典型案例；</li>
    <li>讲清它在 <strong>SSR 下的警告</strong>与替代写法；</li>
    <li>知道它的性能代价——<strong>会阻塞绘制</strong>，并据此克制使用。</li>
  </ul>
</section>""",
"""<section id="sec2" class="card">
  <h2><span class="num">12.1</span> 两个 effect 的时序差异</h2>
  <div class="diagram">
    <svg viewBox="0 0 800 200" role="img" aria-label="两种 effect 的时序对比">
      <rect x="30" y="26" width="130" height="30" rx="6" fill="#f0f5e6" stroke="#3d7a4f"/>
      <text x="95" y="46" text-anchor="middle" font-size="11.5" fill="#1f2e1f">① 渲染组件</text>
      <rect x="180" y="26" width="130" height="30" rx="6" fill="#f0f5e6" stroke="#3d7a4f"/>
      <text x="245" y="46" text-anchor="middle" font-size="11.5" fill="#1f2e1f">② 提交 DOM 更新</text>
      <rect x="330" y="26" width="140" height="30" rx="6" fill="#fefce8" stroke="#d97706"/>
      <text x="400" y="46" text-anchor="middle" font-size="11.5" fill="#b45309">③ useLayoutEffect</text>
      <rect x="490" y="26" width="120" height="30" rx="6" fill="#d8e8c8" stroke="#3d7a4f"/>
      <text x="550" y="46" text-anchor="middle" font-size="11.5" fill="#1f2e1f">④ 浏览器绘制</text>
      <rect x="630" y="26" width="140" height="30" rx="6" fill="#eef3e8" stroke="#047857"/>
      <text x="700" y="46" text-anchor="middle" font-size="11.5" fill="#047857">⑤ useEffect</text>
      <line x1="162" y1="41" x2="176" y2="41" stroke="#7a8a70" stroke-width="1.4"/>
      <line x1="312" y1="41" x2="326" y2="41" stroke="#7a8a70" stroke-width="1.4"/>
      <line x1="472" y1="41" x2="486" y2="41" stroke="#7a8a70" stroke-width="1.4"/>
      <line x1="612" y1="41" x2="626" y2="41" stroke="#7a8a70" stroke-width="1.4"/>
      <text x="60" y="94" font-size="12" fill="#b45309">useLayoutEffect：同帧同步执行，DOM 已更新但屏幕尚未画出；</text>
      <text x="60" y="116" font-size="12" fill="#b45309">在里面改 DOM ⇒ 用户看到的是「改完之后」的画面，不会闪烁</text>
      <text x="60" y="142" font-size="12" fill="#047857">useEffect：绘制之后才执行；在里面改 DOM ⇒ 用户可能看到一帧中间状态</text>
      <text x="60" y="168" font-size="12" fill="#4f6348">代价：layout effect 阻塞绘制，代码又长又重会导致掉帧</text>
    </svg>
    <p class="diagram-caption">图 12-1 两种 effect 在渲染管线上的位置</p>
  </div>
  <pre class="code" data-lang="jsx"><code>useLayoutEffect(() =&gt; {
  // DOM 已更新，但浏览器还没绘制 —— 最后一道修改机会
  const h = boxRef.current.offsetHeight;
  if (h &gt; 200) boxRef.current.style.height = '200px';   // 用户看不到 200px 前的样子
}, [deps]);</code></pre>
</section>""",
"""<section id="sec3" class="card">
  <h2><span class="num">12.2</span> 必须用 layout effect 的三类场景</h2>
  <ol>
    <li><strong>测量后立刻校正</strong>：读 <code>getBoundingClientRect</code> / <code>offsetHeight</code>，据此调整位置或尺寸（Tooltip、Popover、虚拟列表计算可视区）。</li>
    <li><strong>避免首帧闪烁</strong>：元素初始位置未知，必须先算再显示（如吸附开始的动画起点）。</li>
    <li><strong>恢复/保持滚动位置</strong>：列表更新后希望保持在原位置，必须在绘制前写回 scrollTop。</li>
  </ol>
  <div class="warn-box"><span class="tag-pit">判断方法</span>把代码放进 useEffect 后如果看到"闪一下再变好"的现象，就说明它应当在 <code>useLayoutEffect</code> 里做。<strong>先用 useEffect，出问题再升级</strong>，因为后者有性能代价。</div>
</section>""",
"""<section id="sec4" class="card">
  <h2><span class="num">12.3</span> 案例：Tooltip 定位</h2>
  <p>需求：鼠标悬停在按钮上时，Tooltip 出现在按钮正上方且水平居中；空间不足时自动翻转到下方。</p>
  <pre class="code" data-lang="jsx"><code>function Tooltip({ anchorRef, children }) {
  const tipRef = useRef(null);
  const [pos, setPos] = useState({ top: 0, left: 0, ready: false });

  useLayoutEffect(() =&gt; {
    const anchor = anchorRef.current.getBoundingClientRect();
    const tip = tipRef.current.getBoundingClientRect();

    let top = anchor.top - tip.height - 8;      // 默认上方
    if (top &lt; 8) top = anchor.bottom + 8;        // 上不去就翻到下方
    const left = anchor.left + anchor.width / 2 - tip.width / 2;

    setPos({ top, left, ready: true });          // 同步更新 → 不会闪
  }, [anchorRef]);

  return (
    &lt;div ref={tipRef}
      style={{
        position: 'fixed', top: pos.top, left: pos.left,
        visibility: pos.ready ? 'visible' : 'hidden',   // 定位好之前先藏起来
      }}&gt;
      {children}
    &lt;/div&gt;
  );
}</code></pre>
  <p>关键点：<code>visibility: hidden</code> 而非 <code>display: none</code>——元素仍需参与布局才有可测量的尺寸。</p>
</section>""",
"""<section id="sec5" class="card">
  <h2><span class="num">12.4</span> 案例：滚动位置恢复与自适应高度</h2>
  <h4>聊天窗口：新消息到达时保持滚动位置</h4>
  <pre class="code" data-lang="jsx"><code>function MessageList({ messages }) {
  const boxRef = useRef(null);
  const prevHeight = useRef(0);

  useLayoutEffect(() =&gt; {
    const el = boxRef.current;
    if (prevHeight.current) {
      // 保证视觉上"不动"：把因内容变高而多出的部分从底部让出去
      el.scrollTop += el.scrollHeight - prevHeight.current;
    }
    prevHeight.current = el.scrollHeight;
  }, [messages]);

  return &lt;div ref={boxRef} className="msg-box"&gt;{/* ... */}&lt;/div&gt;;
}</code></pre>
  <h4>自适应高度 textarea</h4>
  <pre class="code" data-lang="jsx"><code>function AutoTextarea({ value, onChange }) {
  const ref = useRef(null);

  useLayoutEffect(() =&gt; {
    const el = ref.current;
    el.style.height = 'auto';             // 先还原才能正确测量收缩后的高度
    el.style.height = el.scrollHeight + 'px';
  }, [value]);

  return &lt;textarea ref={ref} value={value} onChange={onChange} /&gt;;
}</code></pre>
  <p class="key-sentence">两个案例的共同点：<strong>先读后写，且写必须在用户看到之前完成</strong>——这正是 useLayoutEffect 存在的唯一理由。</p>
</section>""",
"""<section id="sec6" class="card">
  <h2><span class="num">12.5</span> SSR 警告与替代方案</h2>
  <p>在服务端渲染时没有 DOM，<code>useLayoutEffect</code> 不会执行，React 会给出警告：<em>useLayoutEffect does nothing on the server</em>。</p>
  <pre class="code" data-lang="jsx"><code>// 方案：SSR 环境下退化为 useEffect
const useIsomorphicLayoutEffect =
  typeof window !== 'undefined' ? useLayoutEffect : useEffect;</code></pre>
  <p>但更好的思路是：<strong>如果必须在 SSR 里依赖 DOM 测量，说明这个 UI 设计本身依赖浏览器测量</strong>。可用 CSS 方案（<code>position: fixed</code> + transform + 容器查询）或在客户端 <code>hidden</code> 直到测量完成。</p>
  <div class="note">现代 React 18 的 <code>useInsertionEffect</code>（给 CSS-in-JS 库专用）更早于 layout effect 执行，业务代码基本用不到，只需知道存在。</div>
</section>""",
"""<section id="sec7" class="card">
  <h2><span class="num">12.6</span> 性能代价与使用守则</h2>
  <table>
    <colgroup><col style="width:26%"><col style="width:37%"><col style="width:37%"></colgroup>
    <thead><tr><th>维度</th><th>useEffect</th><th>useLayoutEffect</th></tr></thead>
    <tbody>
      <tr><td>执行时机</td><td>绘制之后（异步）</td><td>绘制之前（同步阻塞）</td></tr>
      <tr><td>是否会卡顿</td><td>不会阻塞绘制</td><td>代码重则掉帧</td></tr>
      <tr><td>SSR 友好</td><td>友好</td><td>报警告</td></tr>
      <tr><td>默认值</td><td><strong>默认用它</strong></td><td>闪烁问题出现才升级</td></tr>
    </tbody>
  </table>
  <p><strong>守则</strong>：</p>
  <ol>
    <li>默认 <code>useEffect</code>；出现视觉闪烁再切 <code>useLayoutEffect</code>；</li>
    <li>layout effect 里只做"测量 + 必要的 DOM 写入"，不要发网络请求；</li>
    <li>依赖写全，避免每次渲染都跑测量（代价高）——必要时缓存测量结果。</li>
  </ol>
</section>""",
"""<section id="sec8" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:30%"><col style="width:70%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>时序</td><td>layout effect 在绘制前、useEffect 在绘制后</td></tr>
      <tr><td>使用场景</td><td>测量后同步校正 DOM、防闪烁、恢复滚动</td></tr>
      <tr><td>默认选择</td><td>先 useEffect，闪了再升级</td></tr>
      <tr><td>性能</td><td>layout effect 阻塞绘制，别在里面做重活</td></tr>
      <tr><td>SSR</td><td>无 DOM 会告警；用同构封装或改设计</td></tr>
    </tbody>
  </table>
</section>""",
"""<section id="sec9" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>说明下列现象的原因并修复：一个 Popover 首次出现时先在左上角"闪一下"才飞到正确位置。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>实现"列表项高度自适应 + 滚动位置保持"：新增 20 条数据后，可视区域仍停留在用户原先看到的位置（提示：记录 scrollHeight 差值）。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>把 Tooltip 改写成不用 useLayoutEffect 也能不闪烁的方案（提示：CSS <code>transform</code> + <code>anchor</code> 定位 / 先用 CSS 隐藏再显示），对比两种实现的复杂度。</div>
  <p class="note">参考答案见附录 C。下一章：useRef——DOM 引用与可变容器。</p>
</section>""",
    ],
)

# ─────────────────────────── 第 13 章 ──────────────────────────
ch13 = dict(
    part_dir=P,
    fname="013_第13章_useRefDOM引用与可变值.html",
    num=13,
    title="useRef：DOM 引用与可变值",
    part="第二篇 Hooks 核心",
    meta="第 13 章 / 共 64 章 · 预计 40 分钟 · 承第 12 章",
    desc="ref 是 React 里唯一能"跨渲染持久化、且不触发重新渲染"的地方。本章讲清它的两大用途——拿 DOM 节点、以及与界面无关的通用容器；并区分哪些数据该放 ref、哪些必须放 state。",
    prev="012_第12章_useLayoutEffect与绘制时机.html", prev_txt="第 12 章",
    nxt="014_第14章_useContext与Provider.html", next_txt="第 14 章",
    toc=[("sec1", "本章目标"), ("sec2", "13.1 ref 是什么：跨渲染的可变盒子"),
         ("sec3", "13.2 获取 DOM 节点"),
         ("sec4", "13.3 ref 列表、回调 ref 与 forwardRef"),
         ("sec5", "13.4 通用可变容器：timer / prev / 锁"),
         ("sec6", "13.5 ref 与 state 的取舍"),
         ("sec7", "13.6 常见坑清单"),
         ("sec8", "本章小结"), ("sec9", "本章习题")],
    sections=[
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>理解 ref 的本质：<code>{ current: xxx }</code> 这个<strong>每次渲染拿到同一个对象</strong>的容器；</li>
    <li>熟练获取 DOM：聚焦、选中、测量、调用原生方法（<code>scrollIntoView</code> 等）；</li>
    <li>掌握<strong>回调 ref</strong>、ref 列表、以及把 ref 转发给子组件；</li>
    <li>用 ref 保存 timer id、上一次的值、请求锁等与渲染无关的数据；</li>
    <li>清楚 ref 与 state 的分工边界，不再用 ref 保存需要显示在界面上的数据。</li>
  </ul>
</section>""",
"""<section id="sec2" class="card">
  <h2><span class="num">13.1</span> ref 是什么：跨渲染的可变盒子</h2>
  <pre class="code" data-lang="jsx"><code>const ref = useRef(initialValue);
// ref 永远是同一个对象：{ current: initialValue }</code></pre>
  <p>两个关键特性：</p>
  <ol>
    <li><strong>跨渲染保持不变</strong>：组件重渲染不会重建 ref，<code>ref.current</code> 的值得以延续；</li>
    <li><strong>修改它不触发渲染</strong>：React 不追踪 ref 的变化，这一点与 state 截然不同。</li>
  </ol>
  <pre class="code" data-lang="jsx"><code>function Demo() {
  const [count, setCount] = useState(0);
  const refCount = useRef(0);

  return (
    &lt;div&gt;
      &lt;p&gt;state: {count}&lt;/p&gt;
      &lt;p&gt;ref: {refCount.current}&lt;/p&gt;   {/* 永远是第一次渲染时的 0 */}
      &lt;button onClick={() =&gt; setCount(c =&gt; c + 1)}&gt;改 state（界面更新）&lt;/button&gt;
      &lt;button onClick={() =&gt; { refCount.current += 1; }}&gt;改 ref（界面不动）&lt;/button&gt;
    &lt;/div&gt;
  );
}</code></pre>
  <div class="key-sentence">一句话：ref 是"绕过渲染机制保存数据的抽屉"，它不是响应式数据，只适合放与界面展示无关的东西。</div>
</section>""",
"""<section id="sec3" class="card">
  <h2><span class="num">13.2</span> 获取 DOM 节点</h2>
  <pre class="code" data-lang="jsx"><code>function SearchInput() {
  const inputRef = useRef(null);

  return (
    &lt;div&gt;
      &lt;input ref={inputRef} /&gt;
      &lt;button onClick={() =&gt; inputRef.current.focus()}&gt;聚焦&lt;/button&gt;
      &lt;button onClick={() =&gt; inputRef.current.select()}&gt;全选&lt;/button&gt;
      &lt;button onClick={() =&gt; inputRef.current.scrollIntoView({ behavior: 'smooth' })}&gt;滚动到&lt;/button&gt;
    &lt;/div&gt;
  );
}</code></pre>
  <p>React 会在<strong>提交阶段</strong>把 DOM 节点填入 <code>ref.current</code>（卸载时置回 null），因此：</p>
  <ul>
    <li><strong>渲染期间 <code>ref.current</code> 不可信</strong>（首次渲染时为 null），只能在事件处理函数或 effect 里读；</li>
    <li>条件渲染的元素只在存在时有值：<code>{open &amp;&amp; &lt;input ref={r} /&gt;}</code>，关闭后为 null。</li>
  </ul>
  <pre class="code" data-lang="jsx"><code>// 常见组合：挂载后自动聚焦（用 useEffect 保证 DOM 已就位）
useEffect(() =&gt; {
  inputRef.current?.focus();
}, []);</code></pre>
  <div class="warn-box"><span class="tag-pit">坑</span>不要把 ref 用在<strong>函数组件</strong>上而不做任何处理：<code>&lt;MyInput ref={r} /&gt;</code> 默认拿不到 DOM，需要 forwardRef（见下节），否则控制台会报 <em>Function components cannot be given refs</em>。</div>
</section>""",
"""<section id="sec4" class="card">
  <h2><span class="num">13.3</span> ref 列表、回调 ref 与 forwardRef</h2>
  <h4>ref 列表：给每个列表项一个 ref</h4>
  <pre class="code" data-lang="jsx"><code>function RowList({ items }) {
  const mapRef = useRef(new Map());   // 用 Map 按 id 存，避免数组下标错乱

  const scrollTo = (id) =&gt; {
    mapRef.current.get(id)?.scrollIntoView({ block: 'nearest' });
  };

  return (
    &lt;ul&gt;
      {items.map(it =&gt; (
        &lt;li key={it.id}
            ref={el =&gt; {
              if (el) mapRef.current.set(it.id, el);
              else mapRef.current.delete(it.id);   // 卸载时清理，防内存泄漏
            }}&gt;
          {it.title}
        &lt;/li&gt;
      ))}
    &lt;/ul&gt;
  );
}</code></pre>
  <h4>回调 ref 的额外价值</h4>
  <p>除了 <code>ref={el =&gt; ...}</code> 的形式，回调 ref 还能在<strong>节点出现/消失时立刻得到通知</strong>（而对象 ref 只设置 current，不会有通知），适合触发动画或测量。</p>
  <h4>forwardRef：把 ref 转发给内部 DOM</h4>
  <pre class="code" data-lang="jsx"><code>const MyInput = forwardRef(function MyInput(props, ref) {
  return &lt;input ref={ref} className="my-input" {...props} /&gt;;
});

// 使用方拿到了真正的 input 节点
const r = useRef(null);
&lt;MyInput ref={r} /&gt;;
r.current.focus();</code></pre>
  <p class="note">React 19 起可以直接把 ref 当普通 props 传递（不再强制 forwardRef）；在 React 18 中请继续使用 <code>forwardRef</code>。需要限制暴露的方法时用 <code>useImperativeHandle</code>（如暴露 <code>focus/reset</code> 而不是整个 DOM）。</p>
</section>""",
"""<section id="sec5" class="card">
  <h2><span class="num">13.4</span> 通用可变容器：timer / prev / 锁</h2>
  <h4>① 存定时器 ID</h4>
  <pre class="code" data-lang="jsx"><code>const timerRef = useRef(null);
const start = () =&gt; { timerRef.current = setTimeout(tick, 1000); };
const stop = () =&gt; { clearTimeout(timerRef.current); };
useEffect(() =&gt; () =&gt; clearTimeout(timerRef.current), []);   // 卸载兜底</code></pre>
  <h4>② 记住上一次的值</h4>
  <pre class="code" data-lang="jsx"><code>function PriceRow({ value }) {
  const prev = useRef(value);
  const [diff, setDiff] = useState(null);

  useEffect(() =&gt; {
    if (prev.current !== value) {
      setDiff(value &gt; prev.current ? 'up' : 'down');
      prev.current = value;
    }
  }, [value]);

  return &lt;span className={diff}&gt;{value}&lt;/span&gt;;
}</code></pre>
  <h4>③ 请求幂等锁</h4>
  <pre class="code" data-lang="jsx"><code>const submittingRef = useRef(false);

async function submit() {
  if (submittingRef.current) return;     // 连点保护
  submittingRef.current = true;
  try { await api.save(data); } finally { submittingRef.current = false; }
}</code></pre>
  <p class="pit-sentence">为什么这些场景不用 state？因为它们<strong>不参与界面渲染</strong>；放进 state 只会白白多一次渲染，还可能引入"旧值"问题。</p>
</section>""",
"""<section id="sec6" class="card">
  <h2><span class="num">13.5</span> ref 与 state 的取舍</h2>
  <table>
    <colgroup><col style="width:24%"><col style="width:38%"><col style="width:38%"></colgroup>
    <thead><tr><th>数据</th><th>用 state</th><th>用 ref</th></tr></thead>
    <tbody>
      <tr><td>出现在界面上</td><td>✅ 唯一选择</td><td>❌ 改了不重渲染</td></tr>
      <tr><td>触发 UI 更新</td><td>✅</td><td>❌</td></tr>
      <tr><td>DOM 节点引用</td><td>❌</td><td>✅</td></tr>
      <tr><td>timer id / 订阅句柄</td><td>❌ 会多余渲染</td><td>✅</td></tr>
      <tr><td>上一次的值（比较用）</td><td>❌</td><td>✅</td></tr>
      <tr><td>需放进依赖数组</td><td>✅ 自动参与</td><td>❌ React 不追踪</td></tr>
    </tbody>
  </table>
  <p class="key-sentence">判断句：<strong>界面要不要跟着它变？</strong>要 → state；不要 → ref。</p>
</section>""",
"""<section id="sec7" class="card">
  <h2><span class="num">13.6</span> 常见坑清单</h2>
  <table>
    <colgroup><col style="width:34%"><col style="width:66%"></colgroup>
    <thead><tr><th>坑</th><th>说明 / 解法</th></tr></thead>
    <tbody>
      <tr><td>渲染期读写 <code>ref.current</code></td><td>违反纯渲染原则，严格模式下行为反复；改到 effect 或事件里</td></tr>
      <tr><td>把 <code>ref.current</code> 当依赖</td><td>React 不追踪 ref，永远拿不到"变化通知"；要触发更新请用 state</td></tr>
      <tr><td>ref 内容变了但界面没变</td><td>设计如此；需要显示请改为 state</td></tr>
      <tr><td>ref 列表写成 <code>useRef([])</code> 后下标错乱</td><td>改用 Map + 回调 ref 并及时 delete</td></tr>
      <tr><td>给函数组件加 ref 报错</td><td>用 forwardRef 转发，或限制暴露方法（useImperativeHandle）</td></tr>
      <tr><td>条件渲染时 ref 为 null</td><td>用可选链 <code>ref.current?.x</code> 或先判断</td></tr>
    </tbody>
  </table>
</section>""",
"""<section id="sec8" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:30%"><col style="width:70%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>本质</td><td>跨渲染不变的 <code>{ current }</code> 容器，改它不重渲染</td></tr>
      <tr><td>DOM 用途</td><td>聚焦/测量/调用原生 API；提交阶段填充，卸载置 null</td></tr>
      <tr><td>ref 列表</td><td>Map + 回调 ref，卸载时 delete</td></tr>
      <tr><td>转发</td><td>forwardRef（React 18）/ 直接 props（19）</td></tr>
      <tr><td>通用容器</td><td>timer id、上一次的值、请求锁</td></tr>
      <tr><td>取舍准则</td><td>界面要不要跟着变：要 state，不要 ref</td></tr>
    </tbody>
  </table>
</section>""",
"""<section id="sec9" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>实现一个"验证码倒计时"：点击后 60s 倒计时，期间禁用按钮；要求用 ref 保存 timer id，卸载时清理。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>实现一个 <code>usePrevious(value)</code>，返回上一次渲染时的值；说明它为什么必须用 ref 而不是 state。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>封装一个 <code>&lt;Form ref={formRef} /&gt;</code>，用 <code>useImperativeHandle</code> 只暴露 <code>submit()</code>、<code>reset()</code>、<code>getValues()</code> 三个方法（不暴露 DOM），并写出使用端代码。</div>
  <p class="note">参考答案见附录 C。下一章：useContext 与 Provider。</p>
</section>""",
    ],
)

build(**ch12)
build(**ch13)

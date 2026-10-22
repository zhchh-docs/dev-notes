# -*- coding: utf-8 -*-
"""第二篇：第 10、11 章"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import build

P = "20_第二篇_Hooks核心"

# ─────────────────────────── 第 10 章 ──────────────────────────
ch10 = dict(
    part_dir=P,
    fname="010_第10章_useEffect同步器心智.html",
    num=10,
    title="useEffect：同步器心智",
    part="第二篇 Hooks 核心",
    meta="第 10 章 / 共 64 章 · 预计 55 分钟 · 全书分水岭",
    desc="useEffect 是 React 里最容易用错的 API，错因几乎都源于心智模型的偏差：把它当成「生命周期钩子」，而不是「与外部系统保持同步」。本章重构这套心智——effect 何时执行、什么时候根本不需要写 effect、以及四类典型用例的规范写法。",
    prev="../10_第一篇_入门/009_第9章_样式方案CSSModules与原子类.html", prev_txt="第 9 章",
    nxt="011_第11章_依赖数组与cleanup三时机.html", next_txt="第 11 章",
    toc=[("sec1", "本章目标"), ("sec2", "10.1 effect 不是生命周期钩子"),
         ("sec3", "10.2 从生命周期到同步：对照表"),
         ("sec4", "10.3 执行时机与 pitfall 顺序图"),
         ("sec5", "10.4 什么时候不该写 effect"),
         ("sec6", "10.5 四类典型用例的规范写法"),
         ("sec7", "10.6 常见坑清单"),
         ("sec8", "本章小结"), ("sec9", "本章习题")],
    sections=[
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>建立正确心智：<strong>useEffect 是"让组件与 React 之外的系统保持同步"的通道</strong>，不是 mounted/updated hook；</li>
    <li>能对 effect 与现实副作用（订阅、计时器、DOM 操作、请求）逐一写出规范代码；</li>
    <li>记住"三个时机"与"提交后才异步执行"这两条时序规则；</li>
    <li>能识别<strong>根本不需要 effect</strong>的场景（派生值、在事件里做事）并用正确写法替代；</li>
    <li>知道 effect 里常见的三类错误：陈旧闭包、无限循环、重复请求。</li>
  </ul>
</section>""",
"""<section id="sec2" class="card">
  <h2><span class="num">10.1</span> effect 不是生命周期钩子</h2>
  <p>Vue 的 <code>onMounted</code>、老版本 React 的 <code>componentDidMount</code> 让很多人带着"在挂载那一刻做点事"的思维写 effect。这个模型在 React 里<strong>会持续出错</strong>，因为 effect 真正关心的是：</p>
  <div class="lead">React 官方定义：<code>useEffect</code> 让你<strong>把组件与外部系统同步起来</strong>。所谓"外部系统"是指 React 渲染管不到的东西：浏览器 API、第三方 Widget、WebSocket、定时器、后台服务的 Actor 等等。</div>
  <p>之所以叫"Effect（副作用）"，是因为这些操作在渲染期间禁止执行（渲染必须是纯的，见第 41 章）。effect 的作用就是：<strong>把渲染之外的事情推迟到提交之后再做。</strong></p>
  <pre class="code" data-lang="jsx"><code>useEffect(() =&gt; {
  // 建立连接（同步开始）
  const conn = createConnection(serverUrl, roomId);
  conn.connect();
  // 断开连接（同步结束）—— cleanup
  return () =&gt; conn.disconnect();
}, [serverUrl, roomId]);   // 依赖：这两个值变了就重新同步</code></pre>
  <p>这段代码的语义是"只要 serverUrl 或 roomId 变化，就重新建立一次连接"，与"挂载"毫无关系。你用"挂载时连接、卸载时断开"去理解它，就会在 roomId 变化时漏掉重建逻辑——这就是大量"聊天室串线""数据显示滞后" bug 的源头。</p>
  <div class="key-sentence">Effect 的心智模型：<strong>建立 → 清理 → 再建立</strong>的循环，而不是"一次性的挂载钩子"。</div>
</section>""",
"""<section id="sec3" class="card">
  <h2><span class="num">10.2</span> 从生命周期到同步：对照表</h2>
  <table>
    <colgroup><col style="width:24%"><col style="width:38%"><col style="width:38%"></colgroup>
    <thead><tr><th>场景</th><th>生命周期思维（易错）</th><th>同步思维（正确）</th></tr></thead>
    <tbody>
      <tr><td>房间切换</td><td>挂载时连 / 卸载时断，切换时忘了重连</td><td>依赖 [roomId]，变化时先断旧的再连新的</td></tr>
      <tr><td>搜索请求</td><td>输入时发请求，结果乱序返回的竞态</td><td>依赖 [keyword] + cleanup 忽略过期响应</td></tr>
      <tr><td>监听事件</td><td>重复 addEventListener 不移除</td><td>cleanup 里 removeEventListener</td></tr>
      <tr><td>定时器</td><td>多次 setInterval 叠加</td><td>cleanup 里 clearInterval</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="jsx"><code>// 典型 bug：以生命周期思维写的聊天室
function ChatRoom({ roomId }) {
  const [messages, setMessages] = useState([]);
  useEffect(() =&gt; {
    const conn = createConnection(roomId);
    conn.on('message', m =&gt; setMessages(prev =&gt; [...prev, m]));
    conn.connect();
    return () =&gt; conn.disconnect();
  }, [roomId]);   // ← 依赖写对就自动支持"切换房间"，无需任何额外代码
}</code></pre>
</section>""",
"""<section id="sec4" class="card">
  <h2><span class="num">10.3</span> 执行时机与时序图</h2>
  <div class="diagram">
    <svg viewBox="0 0 800 240" role="img" aria-label="useEffect 执行时机">
      <rect x="30" y="30" width="160" height="34" rx="6" fill="#f0f5e6" stroke="#3d7a4f"/>
      <text x="110" y="52" text-anchor="middle" font-size="12" fill="#1f2e1f">① 渲染（计算 JSX）</text>
      <rect x="210" y="30" width="160" height="34" rx="6" fill="#f0f5e6" stroke="#3d7a4f"/>
      <text x="290" y="52" text-anchor="middle" font-size="12" fill="#1f2e1f">② 提交到 DOM</text>
      <rect x="390" y="30" width="160" height="34" rx="6" fill="#fefce8" stroke="#d97706"/>
      <text x="470" y="52" text-anchor="middle" font-size="12" fill="#b45309">③ 浏览器绘制</text>
      <rect x="570" y="30" width="180" height="34" rx="6" fill="#eef3e8" stroke="#047857"/>
      <text x="660" y="52" text-anchor="middle" font-size="12" fill="#047857">④ useEffect 执行（异步）</text>
      <line x1="192" y1="47" x2="206" y2="47" stroke="#7a8a70" stroke-width="1.4"/>
      <line x1="372" y1="47" x2="386" y2="47" stroke="#7a8a70" stroke-width="1.4"/>
      <line x1="552" y1="47" x2="566" y2="47" stroke="#7a8a70" stroke-width="1.4" stroke-dasharray="4 3"/>
      <text x="400" y="98" text-anchor="middle" font-size="12" fill="#4f6348">useEffect 在绘制之后才跑，因此不会阻塞首屏</text>
      <text x="400" y="118" text-anchor="middle" font-size="12" fill="#4f6348">若必须在绘制前同步修改 DOM（如测量后立刻调整），用 useLayoutEffect（第 12 章）</text>
      <rect x="30" y="140" width="720" height="80" rx="8" fill="#fff" stroke="#d8e2cc"/>
      <text x="46" y="164" font-size="12" fill="#1f2e1f">依赖变化时：</text>
      <text x="46" y="186" font-size="12" fill="#2d6a3f">先执行上一个 effect 的 cleanup（清理旧的同步）→ 再执行新的 effect（建立新的同步）</text>
      <text x="46" y="206" font-size="12" fill="#2d6a3f">组件卸载时：只执行 cleanup（不再建立新同步）</text>
    </svg>
    <p class="diagram-caption">图 10-1 useEffect 的执行时机：渲染 → 提交 → 绘制 → 异步执行</p>
  </div>
  <p>三条必须记住的时序规则：</p>
  <ol>
    <li><strong>effect 在每次渲染后都可能执行</strong>，是否执行取决于依赖数组是否变化；</li>
    <li><strong>effect 是异步执行的</strong>（晚于浏览器绘制），因此不能在里面指望"用户看不到中间状态"；</li>
    <li><strong>cleanup 先于新 effect 执行</strong>，且<strong>组件卸载时必定执行</strong>——这是所有资源释放的地方。</li>
  </ol>
</section>""",
"""<section id="sec5" class="card">
  <h2><span class="num">10.4</span> 什么时候不该写 effect</h2>
  <p>官方给出的三条"你不需要 Effect"的场景，能删掉半数以上新手代码：</p>
  <h4>① 根据 props/state 计算显示值 → 别放进 state，直接算</h4>
  <pre class="code" data-lang="jsx"><code>// ✗ 多余：effect 里 set 另一个 state，等于渲染两遍
const [fullName, setFullName] = useState('');
useEffect(() =&gt; setFullName(first + ' ' + last), [first, last]);

// ✓ 派生即可
const fullName = first + ' ' + last;</code></pre>
  <h4>② 事件里要做的事 → 放进事件处理函数</h4>
  <pre class="code" data-lang="jsx"><code>// ✗ 把"提交后弹提示"写成 effect + flag
const [submitted, setSubmitted] = useState(false);
useEffect(() =&gt; { if (submitted) toast('提交成功'); }, [submitted]);

// ✓ 直接在提交的地方做
async function submit() {
  await api.save(data);
  toast('提交成功');
}</code></pre>
  <h4>③ 重置子组件状态 → 用 key</h4>
  <pre class="code" data-lang="jsx"><code>// ✗ effect 里手动清空子组件状态
useEffect(() =&gt; { setComment(''); }, [userId]);

// ✓ 换 key 让 React 重建它
&lt;CommentBox key={userId} /&gt;</code></pre>
  <p class="key-sentence">每次准备写 <code>useEffect(() =&gt; setState(...), [deps])</code> 时，先停三秒：这其实是"把一个值同步到另一个值"吗？如果是，几乎总能通过直接计算省掉它。</p>
</section>""",
"""<section id="sec6" class="card">
  <h2><span class="num">10.5</span> 四类典型用例的规范写法</h2>
  <h4>① 浏览器 API 事件监听</h4>
  <pre class="code" data-lang="jsx"><code>useEffect(() =&gt; {
  const handler = (e) =&gt; { if (!ref.current.contains(e.target)) onClose(); };
  document.addEventListener('pointerdown', handler);
  return () =&gt; document.removeEventListener('pointerdown', handler);
}, [onClose]);</code></pre>
  <h4>② 定时器</h4>
  <pre class="code" data-lang="jsx"><code>useEffect(() =&gt; {
  const id = setInterval(() =&gt; setTick(t =&gt; t + 1), 1000);
  return () =&gt; clearInterval(id);      // 不清会导致切换后多个定时器并存
}, []);</code></pre>
  <h4>③ 网络请求（含竞态处理）</h4>
  <pre class="code" data-lang="jsx"><code>useEffect(() =&gt; {
  let ignore = false;                  // 本次请求是否已过期
  setLoading(true);
  fetch(`/api/users?q=${keyword}`)
    .then(r =&gt; r.json())
    .then(data =&gt; { if (!ignore) setUsers(data); })   // 过期响应直接丢弃
    .finally(() =&gt; { if (!ignore) setLoading(false); });

  return () =&gt; { ignore = true; };
}, [keyword]);</code></pre>
  <h4>④ 操作 DOM（第三方库）</h4>
  <pre class="code" data-lang="jsx"><code>useEffect(() =&gt; {
  const chart = echarts.init(elRef.current);
  chart.setOption(option);
  return () =&gt; chart.dispose();        // 防止内存泄漏与重复初始化
}, [option]);</code></pre>
  <div class="note"><strong>关于请求</strong>：以上写法用于理解原理；生产请用第 25 章的 TanStack Query，它自带缓存、去重、竞态与重试。</div>
</section>""",
"""<section id="sec7" class="card">
  <h2><span class="num">10.6</span> 常见坑清单</h2>
  <table>
    <colgroup><col style="width:30%"><col style="width:70%"></colgroup>
    <thead><tr><th>现象</th><th>原因 / 解法</th></tr></thead>
    <tbody>
      <tr><td>页面卡死 / 疯狂请求</td><td>effect 里 setState 而依赖包含这个 state → 无限循环；检查是否真的需要写 effect（见 10.4）</td></tr>
      <tr><td>拿到的是旧数据</td><td>陈旧闭包：依赖数组漏写变量；把用到的响应式值全写进依赖</td></tr>
      <tr><td>请求结果覆盖顺序错乱</td><td>竞态；用 ignore 标记或 AbortController（第 11 章）</td></tr>
      <tr><td>监听器越加越多</td><td>没写 cleanup；严格模式下会立刻暴露（双倍报警）</td></tr>
      <tr><td>开发环境请求发两次</td><td>StrictMode 故意双调用，生产不会发生（第 19 章）</td></tr>
      <tr><td>effect 里读到旧 DOM 尺寸</td><td>绘制后才执行是设计如此；需同步测量请用 useLayoutEffect（第 12 章）</td></tr>
    </tbody>
  </table>
</section>""",
"""<section id="sec8" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:30%"><col style="width:70%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>心智模型</td><td>effect = 与外部系统同步，而非生命周期钩子</td></tr>
      <tr><td>执行时机</td><td>渲染 → 提交 → 绘制 → 异步执行 effect</td></tr>
      <tr><td>cleanup</td><td>依赖变化前与卸载时执行，负责断开同步</td></tr>
      <tr><td>依赖的意义</td><td>决定"什么时候需要重新同步"</td></tr>
      <tr><td>三种不需要 effect</td><td>派生值 / 事件逻辑 / 重置状态用 key</td></tr>
      <tr><td>典型用例</td><td>监听、定时器、请求（带 ignore）、第三方实例 dispose</td></tr>
    </tbody>
  </table>
</section>""",
"""<section id="sec9" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>用同步思维重写这段需求：聊天组件根据 <code>roomId</code> 切换房间，要求在房间切换时先离开旧房间、再进入新房间，卸载时彻底断开。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>下面代码有什么问题？修好后说明原因：<code>const [list, setList] = useState([]); useEffect(() =&gt; { fetch('/api').then(r =&gt; r.json()).then(setList); }, []);</code> 当 keyword props 变化时它并不重新请求。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>把"依赖数组省略"（即第二个参数不传）的行为写出来：它何时执行？为什么通常应该避免？请结合 StrictMode 描述开发体验上的差异。</div>
  <p class="note">参考答案见附录 C。下一章：依赖数组的正确写法与 cleanup 的三个时机。</p>
</section>""",
    ],
)

# ─────────────────────────── 第 11 章 ──────────────────────────
ch11 = dict(
    part_dir=P,
    fname="011_第11章_依赖数组与cleanup三时机.html",
    num=11,
    title="依赖数组与 cleanup 三时机",
    part="第二篇 Hooks 核心",
    meta="第 11 章 / 共 64 章 · 预计 50 分钟 · 承第 10 章",
    desc="90% 的 effect bug 出在两处：依赖数组写错、cleanup 没写对。本章把依赖数组的三种形态、取依赖的原则、函数/对象依赖的处理办法，以及 cleanup 生效的三个时机逐条讲清，并给出竞态处理的标准答案。",
    prev="010_第10章_useEffect同步器心智.html", prev_txt="第 10 章",
    nxt="012_第12章_useLayoutEffect与绘制时机.html", next_txt="第 12 章",
    toc=[("sec1", "本章目标"), ("sec2", "11.1 依赖数组的三种形态"),
         ("sec3", "11.2 取依赖的唯一原则"),
         ("sec4", "11.3 函数依赖与对象依赖"),
         ("sec5", "11.4 cleanup 的三个时机"),
         ("sec6", "11.5 竞态：ignore 与 AbortController"),
         ("sec7", "11.6 常见坑与排查清单"),
         ("sec8", "本章小结"), ("sec9", "本章习题")],
    sections=[
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>说清依赖数组<strong>省略 / 空数组 / 有值</strong>三种形态各自的执行语义；</li>
    <li>掌握取依赖的唯一原则：<strong>effect 中用到的所有响应式值都要写进去</strong>；</li>
    <li>处理函数与对象依赖：搬进 effect、<code>useCallback</code>、或改用 <code>useEffectEvent</code> 思路；</li>
    <li>记住 cleanup 的三个时机，并能用它解释 StrictMode 下的双次调用；</li>
    <li>会用 <code>ignore</code> 标记与 <code>AbortController</code> 处理请求竞态。</li>
  </ul>
</section>""",
"""<section id="sec2" class="card">
  <h2><span class="num">11.1</span> 依赖数组的三种形态</h2>
  <table>
    <colgroup><col style="width:22%"><col style="width:38%"><col style="width:40%"></colgroup>
    <thead><tr><th>写法</th><th>何时执行 effect</th><th>用途 / 风险</th></tr></thead>
    <tbody>
      <tr><td><code>useEffect(fn)</code><br>（不传）</td><td>每次渲染后</td><td>极少正确；通常意味着"忘了写依赖"，容易自激循环</td></tr>
      <tr><td><code>useEffect(fn, [])</code></td><td>仅挂载后（严格模式下还要吃一次双调用）</td><td>一次性订阅、全局监听；注意它会捕获首次渲染的变量</td></tr>
      <tr><td><code>useEffect(fn, [a, b])</code></td><td>a 或 b 的引用/值变化后</td><td>标准写法；依赖是自己声明的"同步条件"</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="jsx"><code>// 场景演示：count 变化时的三种表现
useEffect(() =&gt; { console.log('每次都跑', count); });              // 每次渲染
useEffect(() =&gt; { console.log('只跑一次', count); }, []);          // count 永远停在初始值
useEffect(() =&gt; { console.log('count 变了才跑', count); }, [count]);</code></pre>
  <div class="warn-box"><span class="tag-pit">坑 1</span><code>[]</code> 不代表"只关心挂载"，而代表"<strong>我确定这里用到的值永远不会变</strong>"。若 effect 里读了 props/state 却写空数组，就必然产生<strong>陈旧闭包</strong>（读到的永远是第一次渲染的值）。</div>
</section>""",
"""<section id="sec3" class="card">
  <h2><span class="num">11.2</span> 取依赖的唯一原则</h2>
  <div class="lead"><strong>原则</strong>：effect 内部用到的<strong>所有"响应式值"</strong>（props、state、以及由它们派生出的函数/对象）都必须出现在依赖数组中；不需要响应式的值（refs、模块级常量、setState 函数）不写。</div>
  <pre class="code" data-lang="jsx"><code>function Timer({ interval, onTick }) {
  const [count, setCount] = useState(0);
  const len = interval.length;   // 派生变量

  useEffect(() =&gt; {
    const id = setInterval(() =&gt; {
      setCount(c =&gt; c + 1);     // setCount 稳定，不必写进依赖
      console.log(len);          // len 是派生值 → 必须进依赖
    }, interval);                // interval 来自 props → 必须进依赖
    return () =&gt; clearInterval(id);
  }, [interval, len]);           // ✓ 依赖 = effect 里用到的全部响应式值
}</code></pre>
  <p>判断某个东西要不要进依赖，只需问一句：<strong>它会随渲染变化吗？</strong></p>
  <table>
    <colgroup><col style="width:28%"><col style="width:36%"><col style="width:36%"></colgroup>
    <thead><tr><th>值</th><th>是否响应式</th><th>进依赖？</th></tr></thead>
    <tbody>
      <tr><td>props / state</td><td>是</td><td>✅</td></tr>
      <tr><td>组件内计算出的对象/函数</td><td>是</td><td>✅</td></tr>
      <tr><td><code>setXxx</code>（useState 的 setter）</td><td>否（引用稳定）</td><td>❌</td></tr>
      <tr><td><code>ref.current</code></td><td>否（React 不追踪）</td><td>❌</td></tr>
      <tr><td>模块级常量、导入的函数</td><td>否</td><td>❌</td></tr>
    </tbody>
  </table>
  <div class="note"><strong>工具</strong>：把 ESLint 插件 <code>eslint-plugin-react-hooks</code>（Vite 模板默认启用）的 <code>exhaustive-deps</code> 规则当作硬约束。它比人脑可靠得多。</div>
</section>""",
"""<section id="sec4" class="card">
  <h2><span class="num">11.3</span> 函数依赖与对象依赖</h2>
  <p>对象/函数每次渲染都是新引用，放进依赖会导致 effect 每次都跑。三种正解：</p>
  <h4>方案一：把函数搬进 effect（首选，最简单）</h4>
  <pre class="code" data-lang="jsx"><code>// ✗ onTick 每次渲染都是新函数 → effect 每次都重建定时器
useEffect(() =&gt; {
  const id = setInterval(() =&gt; onTick(), 1000);
  return () =&gt; clearInterval(id);
}, [onTick]);

// ✓ 把逻辑搬进来
useEffect(() =&gt; {
  const id = setInterval(() =&gt; {
    setCount(c =&gt; c + 1);      // 直接用 setter，无需依赖外部函数
  }, 1000);
  return () =&gt; clearInterval(id);
}, []);</code></pre>
  <h4>方案二：useCallback / useMemo 稳定引用</h4>
  <pre class="code" data-lang="jsx"><code>const fetchUser = useCallback(async () =&gt; {
  const r = await fetch(`/api/users/${id}`);
  setUser(await r.json());
}, [id]);                       // 只有 id 变才换新函数

useEffect(() =&gt; { fetchUser(); }, [fetchUser]);</code></pre>
  <h4>方案三：把不需要触发重新同步的"最新值"放进 ref</h4>
  <pre class="code" data-lang="jsx"><code>function Chat({ toUser }) {
  const themeRef = useRef(theme);      // 只想读最新值，不希望它参与依赖
  useEffect(() =&gt; { themeRef.current = theme; }, [theme]);

  useEffect(() =&gt; {
    const conn = createConnection(toUser);
    conn.on('msg', m =&gt; showToast(themeRef.current, m));  // 不用进依赖
    return () =&gt; conn.disconnect();
  }, [toUser]);                          // 只有换人才重连 ✓
}</code></pre>
  <div class="key-sentence">选择顺序：<strong>搬进来 &gt; useCallback 稳定 &gt; ref 兜底</strong>。不要为了消除 lint 警告而用 <code>// eslint-disable-next-line</code> 屏蔽规则——那等于关掉火警报警器。</div>
</section>""",
"""<section id="sec5" class="card">
  <h2><span class="num">11.4</span> cleanup 的三个时机</h2>
  <ol>
    <li><strong>依赖变化前</strong>：先执行上一次 effect 的 cleanup，再执行新的 effect（断开旧连接 → 建立新连接）；</li>
    <li><strong>组件卸载时</strong>：执行最后一次 cleanup，且不再建立新 effect；</li>
    <li><strong>严格模式下的挂载前</strong>：开发环境中 React 会"挂载 → 卸载 → 再挂载"一次，因此你会看到 cleanup 在首次 effect 之后立刻被调用（第 19 章详解）。</li>
  </ol>
  <pre class="code" data-lang="jsx"><code>useEffect(() =&gt; {
  console.log('effect: 建立');
  return () =&gt; console.log('cleanup: 断开');
}, [dep]);

// dep 从 a 变为 b 时的控制台顺序：
// cleanup: 断开      ← 清理 a 那次
// effect: 建立       ← 为 b 建立新的

// StrictMode 首次挂载时：
// effect: 建立 → cleanup: 断开 → effect: 建立</code></pre>
  <p>它解决了什么实际问题？看一个"不写 cleanup 就漏 table 请求"的例子：</p>
  <pre class="code" data-lang="jsx"><code>useEffect(() =&gt; {
  const socket = io(url);
  socket.on('data', setData);
  // ✗ 没写 cleanup：切换路由后旧 socket 仍在收数据并 setState
  //    → 内存泄漏 + 报错 "Can't perform a React state update on an unmounted component"
  return () =&gt; socket.disconnect();   // ✓ 卸载/换依赖时断开
}, [url]);</code></pre>
  <p class="pit-sentence">记住：effect 里每建立一样东西（监听、订阅、timer、连接、第三方实例），cleanup 里就必须有对应的"反向操作"。</p>
</section>""",
"""<section id="sec6" class="card">
  <h2><span class="num">11.5</span> 竞态：ignore 与 AbortController</h2>
  <p>快速输入关键词 abc → ab → a，三个请求几乎同时发出，但返回顺序不可控。若不加处理，<strong>后返回的老结果会覆盖先返回的新结果</strong>，界面显示与输入对不上。</p>
  <pre class="code" data-lang="jsx"><code>// 方案一：布尔标记（最简洁）
useEffect(() =&gt; {
  let ignore = false;
  setLoading(true);
  api.search(keyword).then(res =&gt; {
    if (ignore) return;             // 已过期，丢弃
    setData(res); setLoading(false);
  });
  return () =&gt; { ignore = true; };  // 依赖变化/卸载时作废本次请求
}, [keyword]);</code></pre>
  <pre class="code" data-lang="jsx"><code>// 方案二：AbortController（真正取消请求，省流量）
useEffect(() =&gt; {
  const ctrl = new AbortController();
  api.search(keyword, { signal: ctrl.signal })
    .then(setData)
    .catch(e =&gt; { if (e.name !== 'CanceledError') report(e); });

  return () =&gt; ctrl.abort();        // 真正中断 HTTP 请求
}, [keyword]);</code></pre>
  <table>
    <colgroup><col style="width:22%"><col style="width:39%"><col style="width:39%"></colgroup>
    <thead><tr><th>方式</th><th>是否真正取消请求</th><th>适用</th></tr></thead>
    <tbody>
      <tr><td>ignore 标记</td><td>否（只是不采纳结果）</td><td>简单场景、fetch 封装不统一时</td></tr>
      <tr><td>AbortController</td><td>是</td><td>请求体量大、弱网、需要省带宽</td></tr>
      <tr><td>TanStack Query</td><td>是（内建）</td><td>第 25 章，生产默认方案</td></tr>
    </tbody>
  </table>
</section>""",
"""<section id="sec7" class="card">
  <h2><span class="num">11.6</span> 常见坑与排查清单</h2>
  <ol>
    <li><strong>effect 反复执行</strong> → 依赖里有每次都变的对象/内联数组；把它提到外面、<code>useMemo</code>、或只依赖原始值（如 <code>dep: obj.id</code>）。</li>
    <li><strong>取到旧值</strong> → 依赖漏写；开启 <code>exhaustive-deps</code> 并按提示修正。</li>
    <li><strong>自激循环</strong> → effect 里 setState，而 state 又出现在依赖里；先判断是否根本不需要 effect（第 10 章 10.4）。</li>
    <li><strong>StrictMode 下双调用</strong> → 不是 bug，是在提醒你"cleanup 写得不干净"。</li>
    <li><strong>请求散落在各处 effect</strong> → 各自重写 loading/error/竞态逻辑，行为不一致且难维护；统一收敛到数据层（第 25 章）。</li>
  </ol>
  <div class="warn-box"><span class="tag-pit">排查套路</span>遇到 effect 异常，按三步定位：① 打印 <code>console.log('run', deps)</code> 看触发频率；② 检查 cleanup 是否成对；③ 临时把依赖数组写成 <code>[]</code> 若能修好，说明是引用不稳定问题而非逻辑问题。</div>
</section>""",
"""<section id="sec8" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:30%"><col style="width:70%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>三种形态</td><td>省略=每次渲染；[] =挂载一次；有值=依赖变化时</td></tr>
      <tr><td>取依赖原则</td><td>用到的响应式值全写进去；setter / ref 不用写</td></tr>
      <tr><td>函数对象依赖</td><td>搬进 effect → useCallback 稳定 → ref 兜底</td></tr>
      <tr><td>cleanup 三时机</td><td>依赖变化前、卸载时、StrictMode 首挂载</td></tr>
      <tr><td>竞态</td><td>ignore 标记或 AbortController 取消旧请求</td></tr>
      <tr><td>lint</td><td>exhaustive-deps 当作硬约束，不许 disable 了事</td></tr>
    </tbody>
  </table>
</section>""",
"""<section id="sec9" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>说出下列三种写法下 effect 的触发时机：<code>useEffect(fn)</code>、<code>useEffect(fn, [])</code>、<code>useEffect(fn, [a])</code>；并说明 <code>[]</code> 里读 props 会有什么后果。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>修复这段 count 永远停在 1 的定时器代码：<code>useEffect(() =&gt; { const id = setInterval(() =&gt; setCount(count + 1), 1000); return () =&gt; clearInterval(id); }, []);</code> 要求每秒 +1，且不把 count 写进依赖。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>实现一个搜索建议组件：输入 300ms 后触发请求；切换关键词时取消上一次未完成的请求；组件卸载时不产生任何 setState 警告。</div>
  <p class="note">参考答案见附录 C。下一章：绘制时机与 useLayoutEffect。</p>
</section>""",
    ],
)

build(**ch10)
build(**ch11)

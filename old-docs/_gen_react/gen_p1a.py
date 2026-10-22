# -*- coding: utf-8 -*-
"""第一篇：第 2、3 章"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import build

P = "10_第一篇_入门"

# ─────────────────────────── 第 2 章 ───────────────────────────
ch2 = dict(
    part_dir=P,
    fname="002_第2章_环境搭建Vite与项目结构.html",
    num=2,
    title="环境搭建：Vite 与项目结构",
    part="第一篇 入门",
    meta="第 2 章 / 共 64 章 · 预计 40 分钟 · 跟着做即可出 Hello World",
    desc="工欲善其事。这一章把现代 React 的标准开发环境彻底讲清：Node 与包管理器怎么选、Vite 为什么快、脚手架生成的每一个文件是干什么的、从 index.html 到 App.jsx 的启动链路如何走通，以及团队项目里必须配好的 ESLint / 别名 / 环境变量。",
    prev="001_第1章_认识React.html", prev_txt="第 1 章",
    nxt="003_第3章_JSX详解语法与编译产物.html", next_txt="第 3 章",
    toc=[("sec1", "本章目标"), ("sec2", "2.1 前置：Node 与包管理器"),
         ("sec3", "2.2 用 Vite 创建第一个项目"), ("sec4", "2.3 项目结构逐项解读"),
         ("sec5", "2.4 启动链路：index.html → main.jsx → App"),
         ("sec6", "2.5 dev / build / preview 三条命令"),
         ("sec7", "2.6 团队项目必配：别名、ESLint、环境变量"),
         ("sec8", "本章小结"), ("sec9", "本章习题")],
    sections=[
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>独立使用 <strong>Vite</strong> 创建 React 项目，并能说出 <code>npm</code> / <code>pnpm</code> / <code>yarn</code> 的差异与选型理由；</li>
    <li>看懂脚手架生成的<strong>每一个文件的作用</strong>，删掉一个文件能立刻知道会影响到什么；</li>
    <li>能画出并讲清启动链路：<code>index.html</code> → <code>main.jsx</code> → <code>App.jsx</code> → React 挂载根 DOM；</li>
    <li>分清 <strong>dev / build / preview</strong> 三条命令分别做了什么，以及为什么部署必须用 build 产物；</li>
    <li>为后续 62 章准备好统一可复用的工程底座：路径别名、lint 规则、环境变量。</li>
  </ul>
  <div class="note"><strong>动手约定</strong>：本书所有示例代码均可直接粘贴到 Vite 项目中运行。示例默认使用 JS 版 React 模板；涉及类型的关键章节会额外给出 TS 写法。</div>
</section>""",
"""<section id="sec2" class="card">
  <h2><span class="num">2.1</span> 前置：Node 与包管理器</h2>
  <p>React 项目虽然跑在浏览器里，但代码需要"编译打包"，这一步发生在你的电脑上因此必须先有 <strong>Node.js 运行环境</strong>。</p>
  <h4>版本选择</h4>
  <table>
    <colgroup><col style="width:22%"><col style="width:38%"><col style="width:40%"></colgroup>
    <thead><tr><th>组件</th><th>推荐版本</th><th>说明</th></tr></thead>
    <tbody>
      <tr><td>Node.js</td><td>18 LTS 及以上（推荐 20 LTS）</td><td>Vite 5+ 要求 Node 18+；偶数版本为长期支持</td></tr>
      <tr><td>npm</td><td>Node 自带</td><td>最省心，默认选项，生态最全</td></tr>
      <tr><td>pnpm</td><td>8+</td><td>硬链接复用依赖，磁盘占用小、安装快，monorepo 首选</td></tr>
      <tr><td>yarn</td><td>4.x</td><td>历史包袱多的团队仍在用，新项目一般不选</td></tr>
    </tbody>
  </table>
  <p>本书命令统一用 <code>npm</code>（保证任何机器都能直接跑）；如果你用 pnpm，把 <code>npm install</code> 换成 <code>pnpm install</code>、<code>npm run dev</code> 换成 <code>pnpm dev</code> 即可，语义完全一致。</p>
  <pre class="code" data-lang="bash"><code># 装好后先确认版本（三条命令都应该正常输出版本号）
node -v      # v20.x.x
npm -v       # 10.x.x
where npm    # Windows 用 where；macOS/Linux 用 which npm</code></pre>
  <div class="warn-box"><span class="tag-pit">坑 1</span>国内网络下 <code>npm install</code> 慢或超时：换源即可——<code>npm config set registry https://registry.npmmirror.com</code>。团队合作建议写入 <code>.npmrc</code> 文件并提交仓库，避免每人各配一套。</div>
  <h4>编辑器</h4>
  <p>推荐 VS Code，并安装三个插件就够用全书：<strong>ESLint</strong>（实时报错）、<strong>Prettier</strong>（自动格式化）、<strong>ES7+ React/Redux snippets</strong>（输入 <code>rfce</code> 回车生成组件骨架）。React 官方另有 <strong>React Developer Tools</strong> 浏览器扩展，第六篇性能分析时会重度使用。</p>
</section>""",
"""<section id="sec3" class="card">
  <h2><span class="num">2.2</span> 用 Vite 创建第一个项目</h2>
  <p><span class="tag-key">为什么是 Vite</span>老教材用的是 <code>create-react-app</code>（CRA），它基于 webpack，冷启动动辄 30 秒以上，且已停止维护。<strong>Vite</strong> 的做法截然不同：开发时不打包整个项目，而是利用浏览器原生 ESM，只编译当前用到的模块，因此冷启动常在 <strong>300ms</strong> 内，热更新几乎瞬时。Vite 也是 Vue / React / Svelte 官方推荐的现代起点。</p>
  <pre class="code" data-lang="bash"><code># 交互式创建（推荐第一次用，能看到所有模板选项）
npm create vite@latest my-app

# 一步到位：指定项目名 + React 模板
npm create vite@latest my-app -- --template react

# 想要 TypeScript？
npm create vite@latest my-app -- --template react-ts

cd my-app
npm install
npm run dev</code></pre>
  <p>执行后终端会打印 <code>Local: http://localhost:5173/</code>，浏览器打开即可看到 React 的旋转 logo 页面——<strong>你的第一个 React 应用已经跑起来了</strong>。</p>
  <div class="diagram">
    <svg viewBox="0 0 800 210" role="img" aria-label="Vite dev server 工作原理">
      <defs><marker id="arrV2" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#7a8a70"/></marker></defs>
      <rect x="40" y="60" width="150" height="70" rx="10" fill="#f0f5e6" stroke="#3d7a4f"/>
      <text x="115" y="88" text-anchor="middle" font-size="13" font-weight="700" fill="#2d6a3f">浏览器</text>
      <text x="115" y="110" text-anchor="middle" font-size="11" fill="#4f6348">请求 /src/main.jsx</text>
      <rect x="290" y="52" width="210" height="86" rx="10" fill="#fefce8" stroke="#d97706"/>
      <text x="395" y="80" text-anchor="middle" font-size="13" font-weight="700" fill="#b45309">Vite dev server</text>
      <text x="395" y="102" text-anchor="middle" font-size="11" fill="#b45309">按需编译（esbuild 转译）</text>
      <text x="395" y="122" text-anchor="middle" font-size="11" fill="#b45309">JSX → JS，秒级完成</text>
      <rect x="600" y="60" width="160" height="70" rx="10" fill="#f0fdf4" stroke="#047857"/>
      <text x="680" y="88" text-anchor="middle" font-size="13" font-weight="700" fill="#047857">源码模块</text>
      <text x="680" y="110" text-anchor="middle" font-size="11" fill="#4f6348">只编译被请求的那个</text>
      <line x1="192" y1="95" x2="284" y2="95" stroke="#7a8a70" stroke-width="1.5" marker-end="url(#arrV2)"/>
      <line x1="502" y1="95" x2="594" y2="95" stroke="#7a8a70" stroke-width="1.5" marker-end="url(#arrV2)"/>
      <text x="400" y="180" text-anchor="middle" font-size="12" fill="#7a8a70">对比：webpack 启动时必须先把全部模块打包成 bundle，项目越大越慢</text>
    </svg>
    <p class="diagram-caption">图 2-1 Vite 开发模式：按需编译 vs 全量打包</p>
  </div>
  <p class="pit-sentence">判断题："Vite 只是快，功能少"——错。<code>dev</code> 用按需编译，<code>build</code> 依然走 Rollup 产出压缩过的静态产物，功能与 webpack 等价。</p>
</section>""",
"""<section id="sec4" class="card">
  <h2><span class="num">2.3</span> 项目结构逐项解读</h2>
  <p>Vite React 模板生成的目录很小，但每个文件都有明确职责：</p>
  <pre class="code" data-lang="text"><code>my-app/
├── index.html            # 唯一的 HTML 页面（SPA 入口）
├── package.json          # 依赖清单 + 脚本命令
├── package-lock.json     # 依赖版本锁定（务必提交仓库）
├── vite.config.js        # Vite 配置：插件、别名、代理、端口
├── .eslintrc.cjs         # 代码规范配置（新版可能是 eslint.config.js）
├── public/
│   └── vite.svg          # 原样拷贝、不参与编译的静态资源（favicon 等）
└── src/
    ├── main.jsx          # JS 入口：把组件挂载到 DOM
    ├── App.jsx           # 根组件
    ├── App.css           # App 组件样式
    ├── index.css         # 全局样式
    └── assets/
        └── react.svg     # 参与编译的资源（import 后会得到 URL）</code></pre>
  <table>
    <colgroup><col style="width:26%"><col style="width:74%"></colgroup>
    <thead><tr><th>文件</th><th>一句话职责</th></tr></thead>
    <tbody>
      <tr><td><code>index.html</code></td><td>项目唯一的真实 HTML；里面只有一个空的 <code>&lt;div id="root"&gt;</code> 和一条 <code>&lt;script type="module"&gt;</code> 引用。所有界面都由 JS 动态塞进去——这就是 SPA（单页应用）。</td></tr>
      <tr><td><code>package.json</code></td><td>声明依赖与脚本。<code>dependencies</code> 是运行必需（react、react-dom），<code>devDependencies</code> 只在开发期用（vite、eslint）。</td></tr>
      <tr><td><code>vite.config.js</code></td><td>此处配置 <code>@vitejs/plugin-react</code> 插件（它负责 JSX 转译与热更新），我们会在 2.6 节往里加别名。</td></tr>
      <tr><td><code>public/</code></td><td>不参与构建的资源，引用时用绝对路径 <code>/vite.svg</code>。适合放 favicon、robots.txt。</td></tr>
      <tr><td><code>src/assets/</code></td><td>参与构建的资源，必须 <code>import</code> 使用，构建时会被加哈希重命名，利于 CDN 缓存。</td></tr>
    </tbody>
  </table>
  <div class="warn-box"><span class="tag-pit">坑 2</span>把 public 和 assets 用反，是新手最常见的"图片本地能显示、构建后 404"。判断标准很简单：<strong>需要被 <code>import</code> 参与打包的放 assets，需要原样保留路径的放 public</strong>。</div>
</section>""",
"""<section id="sec5" class="card">
  <h2><span class="num">2.4</span> 启动链路：index.html → main.jsx → App</h2>
  <p>看懂这条链路，你就知道"页面到底是怎么出现的"，以后遇到白屏也能秒定位。</p>
  <h4>第 1 环：index.html</h4>
  <pre class="code" data-lang="html"><code>&lt;!doctype html&gt;
&lt;html lang="en"&gt;
  &lt;head&gt;
    &lt;meta charset="UTF-8" /&gt;
    &lt;link rel="icon" type="image/svg+xml" href="/vite.svg" /&gt;
    &lt;title&gt;Vite + React&lt;/title&gt;
  &lt;/head&gt;
  &lt;body&gt;
    &lt;div id="root"&gt;&lt;/div&gt;
    &lt;script type="module" src="/src/main.jsx"&gt;&lt;/script&gt;
  &lt;/body&gt;
&lt;/html&gt;</code></pre>
  <p>注意 <code>&lt;script type="module"&gt;</code>——它让浏览器以 ES Module 方式加载 <code>main.jsx</code>，这正是 Vite 能按需编译的前提。</p>
  <h4>第 2 环：main.jsx（真正创造 React 应用的地方）</h4>
  <pre class="code" data-lang="jsx"><code>import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

// 1. 找到 index.html 里那个空的 div
const container = document.getElementById('root')

// 2. 创建根实例并渲染 &lt;App /&gt; 到里面
ReactDOM.createRoot(container).render(
  &lt;React.StrictMode&gt;
    &lt;App /&gt;
  &lt;/React.StrictMode&gt;
)</code></pre>
  <p>逐层解释：</p>
  <ul>
    <li><strong><code>createRoot()</code></strong> 是 React 18 的新 API（老版本的 <code>ReactDOM.render</code> 已废弃）。拿到 root 对象后才有并发渲染能力。</li>
    <li><strong><code>.render(&lt;App /&gt;)</code></strong> 表示"请把 App 组件渲染出来的界面放进这个容器"。React 从这里开始递归执行所有组件函数。</li>
    <li><strong><code>&lt;React.StrictMode&gt;</code></strong> 严格模式：开发环境下的"放大镜"，会把开发期常见错误（副作用未清理、废弃 API）暴露出来。<span class="tag-pit">坑提示</span>它会导致开发环境 effect 执行两次——这不是 bug，第 19 章专门讲。</li>
    <li><strong><code>import './index.css'</code></strong> 直接 import CSS：Vite 会把它注入页面。这是"构建工具提供的能力"，不是 JS 语法。</li>
  </ul>
  <h4>第 3 环：App.jsx</h4>
  <pre class="code" data-lang="jsx"><code>import { useState } from 'react'
import reactLogo from './assets/react.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    &lt;&gt;
      &lt;div&gt;
        &lt;a href="https://vite.dev" target="_blank"&gt;
          &lt;img src={reactLogo} className="logo react" alt="React logo" /&gt;
        &lt;/a&gt;
      &lt;/div&gt;
      &lt;h1&gt;Vite + React&lt;/h1&gt;
      &lt;div className="card"&gt;
        &lt;button onClick={() =&gt; setCount((c) =&gt; c + 1)}&gt;
          count is {count}
        &lt;/button&gt;
      &lt;/div&gt;
    &lt;/&gt;
  )
}

export default App</code></pre>
  <p>三个值得记的点：<code>&lt;&gt; ... &lt;/&gt;</code> 是 Fragment（空标签，允许返回多个并列节点）；<code>{count}</code> 是在 JSX 里嵌入 JS 表达式；<code>export default</code> 让 main.jsx 能 <code>import App from './App.jsx'</code>。这些细节第 3 章展开。</p>
  <div class="key-sentence">一句话串起来：浏览器加载 index.html → 加载 main.jsx → createRoot + render(&lt;App /&gt;) → React 执行 App 函数得到 JSX → 生成真实 DOM 插入 #root → 界面出现。</div>
</section>""",
"""<section id="sec6" class="card">
  <h2><span class="num">2.5</span> dev / build / preview 三条命令</h2>
  <table>
    <colgroup><col style="width:24%"><col style="width:38%"><col style="width:38%"></colgroup>
    <thead><tr><th>命令</th><th>做了什么</th><th>什么时候用</th></tr></thead>
    <tbody>
      <tr><td><code>npm run dev</code></td><td>启动开发服务器（默认 5173），带热更新 HMR，代码不压缩、错误信息友好</td><td>日常写代码</td></tr>
      <tr><td><code>npm run build</code></td><td>生产构建：压缩、去 dead code、生成带哈希文件名，输出到 <code>dist/</code></td><td>部署前</td></tr>
      <tr><td><code>npm run preview</code></td><td>本地起静态服务预览 dist 产物（验证打包结果）</td><td>部署前自检</td></tr>
      <tr><td><code>npm run lint</code></td><td>跑 ESLint 检查规范</td><td>提交前 / CI</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="bash"><code>npm run build
# vite v5.x.x building for production...
# dist/index.html                  0.46 kB │ gzip:  0.30 kB
# dist/assets/index-a1b2c3d4.css   1.20 kB │ gzip:  0.62 kB
# dist/assets/index-e5f6g7h8.js  143.21 kB │ gzip: 46.05 kB
# ✓ built in 1.24s</code></pre>
  <p><code>dist/</code> 目录就是<strong>可以丢给 Nginx / 静态托管的一堆静态文件</strong>。文件名里的哈希用于长效缓存：内容变了哈希就变，用户浏览器会自动拉新文件。</p>
  <div class="warn-box"><span class="tag-pit">坑 3</span>直接双击 <code>dist/index.html</code> 用浏览器打开通常白屏——它以绝对路径 <code>/assets/xxx.js</code> 引用资源，必须放在服务器根路径下（用 <code>npm run preview</code> 或 Nginx）。若必须支持子目录部署，需在 <code>vite.config.js</code> 设 <code>base: './'</code>。</div>
</section>""",
"""<section id="sec7" class="card">
  <h2><span class="num">2.6</span> 团队项目必配：别名、ESLint、环境变量</h2>
  <h4>路径别名 @</h4>
  <p>避免出现 <code>../../../components/Button</code> 这种"一层层往上翻"的相对路径地狱。两处同时配置（Vite 负责构建，编辑器负责跳转）：</p>
  <pre class="code" data-lang="js"><code>// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'node:path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { '@': path.resolve(__dirname, './src') },
  },
  server: { port: 5173, open: true },
})</code></pre>
  <pre class="code" data-lang="js"><code>// jsconfig.json（TS 项目用 tsconfig.json 的 paths）
{
  "compilerOptions": { "baseUrl": ".", "paths": { "@/*": ["src/*"] } },
  "include": ["src"]
}</code></pre>
  <p>配好后：<code>import Button from '@/components/Button'</code>。</p>
  <h4>环境变量</h4>
  <p>Vite 规定只有以 <code>VITE_</code> 开头的变量才会被注入前端代码里（防止私钥泄露）：</p>
  <pre class="code" data-lang="bash"><code># .env.development（会被 git 忽略之外的版本提交，注意别放密钥）
VITE_API_BASE=https://dev-api.example.com

# .env.production
VITE_API_BASE=https://api.example.com</code></pre>
  <pre class="code" data-lang="js"><code>// 使用：import.meta.env.VITE_API_BASE
const res = await fetch(import.meta.env.VITE_API_BASE + '/users')
console.log(import.meta.env.MODE)  // 'development' | 'production'</code></pre>
  <div class="danger-box"><span class="tag-pit">坑 4</span>前端环境变量<strong>没有任何保密性</strong>——它会原封不动出现在打包产物里，任何人都能从 JS 文件翻出来。数据库密码、第三方 Secret 必须放后端。</div>
  <h4>ESLint 与格式化</h4>
  <p>模板已自带 ESLint。团队里建议统一：安装 Prettier，在 VS Code 设置 <code>editor.formatOnSave: true</code>，并把 <code>.vscode/settings.json</code> 提交仓库。这样"代码风格争论"从第一天就被消灭。</p>
</section>""",
"""<section id="sec8" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:32%"><col style="width:68%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>技术栈</td><td>Node 18+ / npm / Vite + React 18 是当前创建 React 项目的标准姿势</td></tr>
      <tr><td>Vite 快的原理</td><td>开发态不打包，用浏览器原生 ESM 按需编译；生产态用 Rollup 打包</td></tr>
      <tr><td>index.html</td><td>SPA 里只有一个空 <code>#root</code> 和一条 module 脚本</td></tr>
      <tr><td>main.jsx</td><td><code>createRoot(container).render(&lt;App /&gt;)</code> 是整个应用的起点</td></tr>
      <tr><td>StrictMode</td><td>开发期放大镜，会导致 effect 双调用，不是 bug</td></tr>
      <tr><td>三条命令</td><td>dev 开发、build 产出 dist、preview 本地验产物</td></tr>
      <tr><td>工程化</td><td>别名 @ + VITE_ 前缀环境变量 + 统一 lint/format</td></tr>
    </tbody>
  </table>
</section>""",
"""<section id="sec9" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>新建 Vite React 项目，改掉 App.jsx 里的标题为"我的第一个 React 应用"，用 <code>npm run build</code> 产出 dist，再用 <code>npm run preview</code> 打开确认。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>配置路径别名 <code>@</code> 指向 src，新建 <code>src/components/HelloCard.jsx</code>，在 App.jsx 中用 <code>import HelloCard from '@/components/HelloCard'</code> 引入并渲染成功。</div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>项目白屏了。列出至少 4 种可能原因及各自的排查手段（提示：从 index.html、main.jsx、控制台报错、构建 base 路径四个角度思考）。</div>
  <p class="note">参考答案见附录 C。下一章：把 JSX 这门"看起来像 HTML 的 JS"彻底拆开看。</p>
</section>""",
    ],
)

# ─────────────────────────── 第 3 章 ───────────────────────────
ch3 = dict(
    part_dir=P,
    fname="003_第3章_JSX详解语法与编译产物.html",
    num=3,
    title="JSX 详解：语法与编译产物",
    part="第一篇 入门",
    meta="第 3 章 / 共 64 章 · 预计 45 分钟 · 承第 1 章 · 起以后所有章",
    desc="JSX 是 React 最容易被误解的东西：它长得像 HTML，骨子里却是 JavaScript。这一章把 JSX 拆到见底——它编译成什么、三种插值写法各自用在哪、className/style/Fragment 为什么那样写、以及那些让人一头雾水的报错为什么会发生。",
    prev="002_第2章_环境搭建Vite与项目结构.html", prev_txt="第 2 章",
    nxt="004_第4章_组件与props数据下行.html", next_txt="第 4 章",
    toc=[("sec1", "本章目标"), ("sec2", "3.1 JSX 不是模板，是语法糖"),
         ("sec3", "3.2 看编译产物：jsx() 调用"),
         ("sec4", "3.3 三种插值写法"), ("sec5", "3.4 属性命名规则"),
         ("sec6", "3.5 子节点、Fragment 与渲染规则"),
         ("sec7", "3.6 报错清单与常见坑"),
         ("sec8", "本章小结"), ("sec9", "本章习题")],
    sections=[
"""<section id="sec1" class="card">
  <h2><span class="num">◆</span>本章目标</h2>
  <ul>
    <li>明确回答"JSX 到底是什么"——它不是模板引擎、不是字符串，而是<strong>编译成函数调用的语法糖</strong>；</li>
    <li>能手写 JSX 对应的 <code>jsx()</code> 调用产物，看得懂 <code>type</code>/<code>props</code>/<code>children</code> 三层结构；</li>
    <li>熟练使用<strong>插值表达式</strong>的三种形态，并知道 JSX 里只能写"表达式"不能写"语句"；</li>
    <li>掌握属性命名差异（<code>className</code>、<code>htmlFor</code>、<code>style</code> 双花括号、布尔属性）及其原因；</li>
    <li>记住渲染真值表：<code>false / null / undefined</code> 会被忽略，<code>0</code> 和空字符串会显示。</li>
  </ul>
</section>""",
"""<section id="sec2" class="card">
  <h2><span class="num">3.1</span> JSX 不是模板，是语法糖</h2>
  <p>先摆三条容易混淆的事实：</p>
  <ol>
    <li><strong>JSX 不是 HTML 字符串</strong>。<code>&lt;h1&gt;Hi&lt;/h1&gt;</code> 编译后不是 <code>"&lt;h1&gt;Hi&lt;/h1&gt;"</code>，而是一个描述界面的 JS 对象（React 元素）。</li>
    <li><strong>JSX 没有被浏览器直接支持</strong>。浏览器只认识 JS 编译器插件（Babel / SWC / esbuild）在运行前把它转成普通 JS。这就是为什么"不配插件就无法使用 JSX"。</li>
    <li><strong>它不是必需品，但很难不用</strong>。你可以完全不用 JSX 写 React（第 2 点的函数调用形式），只是可读性极差。</li>
  </ol>
  <p>JSX 的设计初衷是：<strong>把"描述 UI 结构"这件事的语法成本降到接近 HTML</strong>，同时保留 JS 的全部能力（变量、循环、条件、函数）。</p>
  <div class="lead"><strong>一句话</strong>：JSX = 用 XML 风格写 JS 函数调用。看清这一层，后面的写法与报错都不再神秘。</div>
</section>""",
"""<section id="sec3" class="card">
  <h2><span class="num">3.2</span> 看编译产物：jsx() 调用</h2>
  <p>这段 JSX：</p>
  <pre class="code" data-lang="jsx"><code>const el = &lt;h1 className="title"&gt;Hello, {name}&lt;/h1&gt;;</code></pre>
  <p>在 React 17 之后（<strong>automatic runtime</strong>，也是 Vite 模板默认）被编译为：</p>
  <pre class="code" data-lang="js"><code>import { jsx as _jsx } from 'react/jsx-runtime';

const el = _jsx('h1', { className: 'title', children: ['Hello, ', name] });</code></pre>
  <p>而更早的 <strong>classic runtime</strong>（React 16 及以前、部分老教程）会编译为：</p>
  <pre class="code" data-lang="js"><code>const el = React.createElement('h1', { className: 'title' }, 'Hello, ', name);</code></pre>
  <p>两者差别：</p>
  <table>
    <colgroup><col style="width:26%"><col style="width:37%"><col style="width:37%"></colgroup>
    <thead><tr><th>模式</th><th>automatic（17+ 默认）</th><th>classic（老版）</th></tr></thead>
    <tbody>
      <tr><td>需要手写 import React</td><td>不需要</td><td>必须 <code>import React from 'react'</code></td></tr>
      <tr><td>编译函数</td><td><code>react/jsx-runtime</code> 的 <code>jsx()</code></td><td><code>React.createElement()</code></td></tr>
      <tr><td>性能</td><td>略优（减少一层属性处理）</td><td>—</td></tr>
    </tbody>
  </table>
  <div class="warn-box"><span class="tag-pit">坑 1</span>网上老教程里"必须写 <code>import React from 'react'</code> 否则报 <code>React is not defined</code>"的说法，在现代 + Vite 项目中<strong>已不成立</strong>。反过来，如果你在 Vite 项目里删掉这行却报错，说明配的是 classic runtime（检查构建配置或老版 babel 配置）。</div>
  <h4>深入理解 Element 对象</h4>
  <pre class="code" data-lang="js"><code>const el = &lt;button disabled&gt;确定&lt;/button&gt;;

console.log(el);
// {
//   type: 'button',                 // 标签名 / 组件函数
//   key: null,
//   ref: null,
//   props: { disabled: true, children: '确定' },
//   $$typeof: Symbol(react.element) // 防 XSS 的内部标记
// }</code></pre>
  <p>记住这个结构：<strong>元素 = type（是什么）+ props（属性与子节点）+ key/ref</strong>。第五篇讲 Fiber（{#sec}第 39 章）时，会发现 Fiber 节点正是基于这些信息生成的。</p>
  <pre class="code" data-lang="jsx"><code>// 完全不用 JSX 也能写 React —— 证明 JSX 只是糖
const el2 = { type: 'button', props: { children: '确定', disabled: true } };

// 嵌套结构的写法
const list = _jsx('ul', { children: [
  _jsx('li', { children: 'A' }),
  _jsx('li', { children: 'B' }),
]});</code></pre>
</section>""",
"""<section id="sec4" class="card">
  <h2><span class="num">3.3</span> 三种插值写法</h2>
  <p>JSX 里用 <code>{ }</code> 进入"JS 世界"，且<strong>只能放表达式</strong>（能求值出结果的代码片段），不能放语句（<code>if</code>、<code>for</code>、<code>switch</code> 直接写会报错）。</p>
  <h4>① 内容插值</h4>
  <pre class="code" data-lang="jsx"><code>const user = { name: '张三', vip: true, score: 88 };

&lt;p&gt;姓名：{user.name}&lt;/p&gt;
&lt;p&gt;等级：{user.vip ? 'VIP' : '普通'}&lt;/p&gt;
&lt;p&gt;学分：{user.score + 2}&lt;/p&gt;
&lt;p&gt;标签：{formatTag(user)}&lt;/p&gt;   {/* 函数调用也可以，只要是表达式 */}</code></pre>
  <h4>② 属性插值（引号换成花括号）</h4>
  <pre class="code" data-lang="jsx"><code>const avatar = 'https://x.com/a.png';
const id = 'user-1';

&lt;img src={avatar} alt="头像" data-id={id} /&gt;
&lt;div title={undefined}&gt;title 为 undefined 时不出现在 DOM 上&lt;/div&gt;</code></pre>
  <p class="pit-sentence">写法区分：<code>src="abc"</code> 传的是字符串字面量；<code>src={avatar}</code> 传的是变量的值。写错就会把变量名当成字面字符串传下去。</p>
  <h4>③ 样式插值（两个花括号不是语法特殊）</h4>
  <pre class="code" data-lang="jsx"><code>// 外层 {}：进入 JS；内层 { color: 'red' }：一个普通对象字面量
&lt;p style={{ color: 'red', fontSize: 18 }}&gt;红色 18px&lt;/p&gt;

// 提取出来更清晰（推荐）
const dangerStyle = { color: '#b91c1c', fontWeight: 700 };
&lt;p style={dangerStyle}&gt;危险&lt;/p&gt;</code></pre>
  <p><code>style</code> 用 camelCase（<code>fontSize</code> 而非 <code>font-size</code>），数字会被自动加上 <code>px</code>（<code>0</code> 不加）。</p>
  <h4>为什么 for 不能直接写在 JSX 里</h4>
  <pre class="code" data-lang="jsx"><code>// ✗ 错误：for 是语句，JSX 里放不了
&lt;ul&gt;{ for (let i = 0; i &lt; 3; i++) &lt;li&gt;{i}&lt;/li&gt; }&lt;/ul&gt;

// ✓ 正确：用表达式产出数组 —— map
&lt;ul&gt;{ [0, 1, 2].map(i =&gt; &lt;li key={i}&gt;{i}&lt;/li&gt;) }&lt;/ul&gt;</code></pre>
  <p class="key-sentence">判断口诀："能不能被 <code>const x = &lt;这里&gt;</code> 承接？" —— 能就是表达式，可以放进 <code>{}</code>。</p>
</section>""",
"""<section id="sec5" class="card">
  <h2><span class="num">3.4</span> 属性命名规则</h2>
  <p>JSX 属性名用 <code>camelCase</code>，与 HTML 习惯不同。差异来自"JSX 最终是 JS 对象属性"这一事实——JS 里保留字、连字符都不友好。</p>
  <table>
    <colgroup><col style="width:26%"><col style="width:37%"><col style="width:37%"></colgroup>
    <thead><tr><th>HTML 写法</th><th>JSX 写法</th><th>原因</th></tr></thead>
    <tbody>
      <tr><td><code>class="box"</code></td><td><code>className="box"</code></td><td><code>class</code> 是 JS 关键字</td></tr>
      <tr><td><code>for="name"</code></td><td><code>htmlFor="name"</code></td><td><code>for</code> 是 JS 关键字</td></tr>
      <tr><td><code>onclick="fn()"</code></td><td><code>onClick={fn}</code></td><td>React 合成事件统一 camelCase，且传函数本身而非调用</td></tr>
      <tr><td><code>tabindex="1"</code></td><td><code>tabIndex={1}</code></td><td>camelCase 统一</td></tr>
      <tr><td><code>readonly</code></td><td><code>readOnly</code></td><td>同上</td></tr>
      <tr><td><code>data-id="1"</code></td><td><code>data-id="1"</code>（不变）</td><td>自定义属性保持原样</td></tr>
      <tr><td><code>&lt;input disabled&gt;</code></td><td><code>&lt;input disabled /&gt;</code> 或 <code>disabled={true}</code></td><td>布尔属性：给值即为真</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="jsx"><code>// 常见坑：值是 false 时 attribute 不会出现在 DOM 上
&lt;input disabled={false} /&gt;        // DOM：&lt;input&gt;（无 disabled）
&lt;input disabled={'false'} /&gt;      // DOM：&lt;input disabled&gt;（字符串 'false' 是真值！）

// spread 批量传属性（写组件封装时高频）
const inputProps = { type: 'text', placeholder: '请输入', maxLength: 20 };
&lt;input {...inputProps} value={v} onChange={handle} /&gt;</code></pre>
  <div class="warn-box"><span class="tag-pit">坑 2</span><code>checked</code>/<code>value</code> 这类"受控属性"一旦给了值就必须配 <code>onChange</code>，否则会报 <em>You provided a `value` prop to a form field without an `onChange` handler</em>——第 8 章详解。</div>
</section>""",
"""<section id="sec6" class="card">
  <h2><span class="num">3.5</span> 子节点、Fragment 与渲染规则</h2>
  <h4>组件必须返回单个根（或用 Fragment）</h4>
  <pre class="code" data-lang="jsx"><code>// ✗ 报错：Adjacent JSX elements must be wrapped in an enclosing tag
function Bad() {
  return &lt;h1&gt;标题&lt;/h1&gt;&lt;p&gt;正文&lt;/p&gt;;
}

// ✓ 方案一： Fragment 全标签
function Good1() {
  return (
    &lt;React.Fragment&gt;
      &lt;h1&gt;标题&lt;/h1&gt;
      &lt;p&gt;正文&lt;/p&gt;
    &lt;/React.Fragment&gt;
  );
}

// ✓ 方案二：语法糖（最常用），唯一可用属性是 key
function Good2() {
  return (
    &lt;&gt;
      &lt;h1&gt;标题&lt;/h1&gt;
      &lt;p&gt;正文&lt;/p&gt;
    &lt;/&gt;
  );
}</code></pre>
  <p>Fragment 的价值：<strong>不在真实 DOM 里多产生一层 <code>div</code></strong>。写表格、Flex 布局时这一层多余容器会破坏样式和结构。</p>
  <h4>渲染真值表（务必背下来）</h4>
  <table>
    <colgroup><col style="width:28%"><col style="width:34%"><col style="width:38%"></colgroup>
    <thead><tr><th>插值内容</th><th>渲染结果</th><th>典型踩坑</th></tr></thead>
    <tbody>
      <tr><td><code>{false}</code></td><td>什么都不渲染</td><td>本想显示 "false"</td></tr>
      <tr><td><code>{null}</code> / <code>{undefined}</code></td><td>什么都不渲染</td><td>条件渲染的自然用法</td></tr>
      <tr><td><code>{0}</code></td><td><strong>渲染出 0</strong></td><td>见下方劝退表</td></tr>
      <tr><td><code>{''}</code> / <code>{[]}</code></td><td>渲染空内容</td><td>—</td></tr>
      <tr><td><code>{NaN}</code></td><td>渲染 "NaN"</td><td>计算错误直接上屏</td></tr>
      <tr><td><code>{{ a: 1 }}</code></td><td>报错</td><td>对象不能作为 React 子节点</td></tr>
    </tbody>
  </table>
  <pre class="code" data-lang="jsx"><code>const items = [];

// ✗ 经典 bug：空列表时屏幕上赫然显示一个 "0"
&lt;div&gt;{items.length &amp;&amp; &lt;List items={items} /&gt;}&lt;/div&gt;

// ✓ 修法一：布尔化
&lt;div&gt;{items.length &gt; 0 &amp;&amp; &lt;List items={items} /&gt;}&lt;/div&gt;
// ✓ 修法二：!! 转 Boolean
&lt;div&gt;{!!items.length &amp;&amp; &lt;List items={items} /&gt;}&lt;/div&gt;</code></pre>
  <h4>条件渲染的三种写法</h4>
  <pre class="code" data-lang="jsx"><code>// 1. 三元：二选一
{isLogin ? &lt;UserPanel /&gt; : &lt;LoginBtn /&gt;}

// 2. &amp;&amp;：要不要（注意上面说的 0 陷阱）
{hasMore &amp;&amp; &lt;LoadMore /&gt;}

// 3. 早返回 / 提取变量：分支复杂时使用
if (loading) return &lt;Skeleton /&gt;;
if (error) return &lt;ErrorBox msg={error} /&gt;;
return &lt;Content data={data} /&gt;;</code></pre>
  <div class="danger-box"><span class="tag-pit">坑 3</span>嵌套三元才是可读性的头号杀手。"<code>{a ? &lt;X/&gt; : b ? &lt;Y/&gt; : c ? &lt;Z/&gt; : null}</code>" 这种写法一旦出现就该拆函数调用或组件。第 6 章给重构手法。</div>
</section>""",
"""<section id="sec7" class="card">
  <h2><span class="num">3.6</span> 报错清单与常见坑</h2>
  <table>
    <colgroup><col style="width:44%"><col style="width:56%"></colgroup>
    <thead><tr><th>报错信息（关键词）</th><th>原因与解法</th></tr></thead>
    <tbody>
      <tr><td>Adjacent JSX elements must be wrapped</td><td>返回了多个并列根元素，用 <code>&lt;&gt;&lt;/&gt;</code> 包一层</td></tr>
      <tr><td>Objects are not valid as a React child</td><td>误把对象/数组元素当内容渲染，检查 <code>{obj}</code> 处</td></tr>
      <tr><td>Expected corresponding JSX closing tag</td><td>标签没闭合或拼写大小写不一致</td></tr>
      <tr><td>React is not defined</td><td>用了 classic runtime 却没 import React；检查构建配置</td></tr>
      <tr><td>Each child in a list should have a unique key</td><td><code>map</code> 渲染忘了加 <code>key</code>（第 6 章详解）</td></tr>
      <tr><td>Style prop value must be an object</td><td><code>style="color:red"</code> 写成字符串了，应该用对象</td></tr>
      <tr><td>Invalid DOM property <code>class</code></td><td>HTML 习惯犯了：应为 <code>className</code></td></tr>
    </tbody>
  </table>
  <p>统一对策：<strong>浏览器控制台的 React 报错通常带具体组件名与行号，且多数附有大文档链接</strong>。养成读完整报错的习惯，效率会高于任何搜索。</p>
</section>""",
"""<section id="sec8" class="card">
  <h2><span class="num">✓</span> 本章小结</h2>
  <table>
    <colgroup><col style="width:32%"><col style="width:68%"></colgroup>
    <thead><tr><th>要点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>JSX 本质</td><td>编译成 <code>jsx(type, props, children)</code> 函数调用的语法糖</td></tr>
      <tr><td>两代 runtime</td><td>17+ 默认 automatic，不用手写 import React</td></tr>
      <tr><td>元素结构</td><td><code>type + props + key/ref</code>，是普通的 JS 对象</td></tr>
      <tr><td>插值规则</td><td><code>{}</code> 内只能是表达式；style 用 camelCase + 对象</td></tr>
      <tr><td>属性差异</td><td>className / htmlFor / 布尔属性 / spread</td></tr>
      <tr><td>渲染真值表</td><td>false/null/undefined 不渲染，0 会渲染——条件渲染头号坑</td></tr>
      <tr><td>Fragment</td><td>不产生多余 DOM 节点的包裹容器</td></tr>
    </tbody>
  </table>
</section>""",
"""<section id="sec9" class="card">
  <h2><span class="num">✎</span> 本章习题</h2>
  <div class="ex-box"><span class="ex-tag">A 基础</span>手写出这段 JSX 的编译产物：<code>const el = &lt;li id="a"&gt;任务 {1 + 1}&lt;/li&gt;;</code>（写出 <code>_jsx(...)</code> 调用的完整参数）。</div>
  <div class="ex-box"><span class="ex-tag">B 进阶</span>下面代码在空列表时屏幕上会出现什么？为什么？如何修？<code>&lt;div&gt;{todos.length &amp;&amp; &lt;TodoList todos={todos} /&gt;}&lt;/div&gt;</code></div>
  <div class="ex-box"><span class="ex-tag">C 挑战</span>用 map + Fragment(<code>&lt;React.Fragment key={id}&gt;</code>) 渲染一张两列的"定义列表"（词 + 释义），要求不产生多余的包裹 div，并说明为什么这里 Fragment 需要 key 而短语法 <code>&lt;&gt;</code> 加不了 key。</div>
  <p class="note">参考答案见附录 C。下一章：组件拆分与 props —— 数据如何从上往下流。</p>
</section>""",
    ],
)

build(**ch2)
build(**ch3)

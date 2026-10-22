/* ============================================================
   知识库阅读外壳 app.js
   自动注入顶栏 / 目录栏 / 进度条 / 上下篇 / 暗色模式
   目录栏与正文双栏各自独立滚动，点目录平滑跳转正文
   支持 SPA 无刷新导航
   ============================================================ */
(function(){
  // 深度自适应：计算“页面 → 仓库根”的相对前缀（app.js 固定位于 根/assets/）
  let UP = '../';
  try{
    const appUrl = new URL(document.currentScript.src, location.href);
    const rootPath = decodeURIComponent(new URL('../', appUrl).pathname);   // 去掉 assets/app.js → 根/
    const hereDir  = decodeURIComponent(location.pathname.replace(/[^/]*$/, ''));
    const rel = hereDir.startsWith(rootPath) ? hereDir.slice(rootPath.length) : '';
    UP = '../'.repeat(rel.split('/').filter(Boolean).length);
    window.__KB_ROOT_PATH = rootPath;
    window.__KB_UP = UP;
  }catch(e){}

  // 页面内任意 href → 相对仓库根的路径（与 manifest 的 u 匹配）
  window.__KB_REL = function(u){
    try{
      const p = decodeURIComponent(new URL(u, location.href).pathname);
      const rootPath = window.__KB_ROOT_PATH || '';
      return p.startsWith(rootPath) ? p.slice(rootPath.length) : p;
    }catch(e){ return u; }
  };

  // 外壳样式自动补注（部分页面只注入了 app.js，缺 app.css）
  try{
    if(!document.querySelector('link[href*="app.css"]')){
      const l = document.createElement('link');
      l.rel = 'stylesheet';
      l.href = new URL('app.css', document.currentScript.src).href;
      document.head.appendChild(l);
    }
  }catch(e){}

  // 动态加载 manifest.js（路径随页面深度自适应）
  const s = document.createElement('script');
  s.src = UP + 'assets/manifest.js';
  s.onload = init;
  document.head.appendChild(s);

  // 提前应用主题（避免闪烁）
  try{
    let t = localStorage.getItem('kb_theme');
    if(!t) t = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', t);
  }catch(e){}

  function init(){
    const M = window.KB_MANIFEST;
    if(!M) return;

    const SHELL_IDS = ['kb-progress','kb-topbar','kb-toc','kb-content','kb-pager'];

    let here = window.__KB_REL(location.href);
    let curIdx = -1, prev = null, next = null, curCat = null;
    let flat = [];
    M.cats.forEach(c => c.arts.forEach(a => flat.push(a)));
    flat.forEach((a,i) => {
      if(a.u === here){ curIdx = i; prev = flat[i-1] || null; next = flat[i+1] || null; }
    });
    M.cats.forEach(c => c.arts.forEach(a => { if(a.u === here) curCat = c; }));

    /* ---------- 1. 进度条 ---------- */
    const prog = document.createElement('div');
    prog.id = 'kb-progress';
    document.body.appendChild(prog);

    /* ---------- 2. 顶栏 ---------- */
    const bar = document.createElement('header');
    bar.id = 'kb-topbar';
    bar.innerHTML = `
      <a class="kb-btn" href="${UP}../index.html#/book/${curCat ? encodeURIComponent(curCat.key) : ''}" title="返回本书目录" style="text-decoration:none">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m12 19-7-7 7-7"/><path d="M19 12H5"/></svg>
      </a>
      <div id="kb-crumb">
        ${curCat ? `<a class="kb-cat" href="${UP}../index.html#/book/${encodeURIComponent(curCat.key)}" title="回到书架 · 「${curCat.name}」这本书">${curCat.icon} ${curCat.name}</a><span class="kb-sep">·</span>` : ''}
        <span class="kb-title">${document.title.replace('｜全栈技术知识库','')}</span>
      </div>
      <div class="kb-right">
        <span class="kb-pos" id="kbPos"></span>
        <button class="kb-btn kb-read-btn" id="kbReadBtn" title="标记已读">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
        </button>
        <button class="kb-btn" id="kbThemeBtn" title="切换主题">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        </button>
      </div>`;
    document.body.appendChild(bar);

    /* ---------- 2.5 已读打卡 / 模块内进度 / 继续阅读 ---------- */
    const READ_KEY = 'kb_read';
    let readSet;
    try{ readSet = new Set(JSON.parse(localStorage.getItem(READ_KEY) || '[]')); }
    catch(e){ readSet = new Set(); }
    function saveRead(){ try{ localStorage.setItem(READ_KEY, JSON.stringify([...readSet])); }catch(e){} }
    function syncReadBtn(){
      const btn = document.getElementById('kbReadBtn');
      if(!btn) return;
      const on = readSet.has(here);
      btn.classList.toggle('on', on);
      btn.title = on ? '已读（点击取消）' : '标记已读';
    }
    document.getElementById('kbReadBtn').onclick = () => {
      readSet.has(here) ? readSet.delete(here) : readSet.add(here);
      saveRead();
      syncReadBtn();
    };
    function syncPos(){
      const pos = document.getElementById('kbPos');
      if(!pos) return;
      if(curCat){
        const i = curCat.arts.findIndex(a => a.u === here);
        pos.textContent = (i >= 0) ? `${i+1} / ${curCat.arts.length} 篇` : '';
      }else{
        pos.textContent = '';
      }
    }
    try{ localStorage.setItem('kb_last', JSON.stringify({ u: here })); }catch(e){}
    syncPos();
    syncReadBtn();

    /* ---------- 内容包装：右侧独立滚动容器 ---------- */
    let content = document.getElementById('kb-content');
    if(!content){
      content = document.createElement('div');
      content.id = 'kb-content';
      Array.from(document.body.children).forEach(el => { if(!isShell(el)) content.appendChild(el); });
      document.body.appendChild(content);
    }
    // 外壳就绪：解锁 app.css 中“外壳接管滚动”的规则（未注入时页面保持原生滚动）
    document.body.classList.add('kb-shell-on');

    /* ---------- 3. 目录栏：把文章自带目录提取到左侧固定栏，独立滚动 ---------- */
    function extractToc(){
      const oldPanel = document.getElementById('kb-toc');
      if(oldPanel) oldPanel.remove();
      document.body.classList.remove('has-kb-toc');
      const tocEl = content.querySelector('nav.toc') || content.querySelector('aside.sidebar');
      if(!tocEl) return;
      const panel = document.createElement('div');
      panel.id = 'kb-toc';
      panel.appendChild(tocEl);
      document.body.appendChild(panel);
      document.body.classList.add('has-kb-toc');
    }
    extractToc();

    /* ---------- 4. 暗色切换 ---------- */
    document.getElementById('kbThemeBtn').onclick = () => {
      const cur = document.documentElement.getAttribute('data-theme');
      const next = cur === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      try{ localStorage.setItem('kb_theme', next); }catch(e){}
    };

    /* ---------- 5. 上下篇：底部卡片 + 两侧悬停箭头 + 键盘 ←/→ ---------- */
    function buildPager(){
      // 移除旧 pager 与旧侧边箭头
      ['kb-pager','kb-edge-prev','kb-edge-next'].forEach(id => {
        const el = document.getElementById(id);
        if(el) el.remove();
      });

      if(prev || next){
        const pager = document.createElement('div');
        pager.id = 'kb-pager';
        const pos = (curIdx >= 0) ? `<div class="kb-pager-pos">第 ${curIdx + 1} / ${flat.length} 篇</div>` : '';
        const arrowL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 19-7-7 7-7"/><path d="M19 12H5"/></svg>';
        const arrowR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>';
        pager.innerHTML = pos + `
          ${prev
            ? `<a class="prev" href="${UP}${encodeURI(prev.u)}"><div class="dir">${arrowL} 上一篇</div><div class="name">${prev.t}</div></a>`
            : `<div class="none">已是第一篇</div>`}
          ${next
            ? `<a class="next" href="${UP}${encodeURI(next.u)}"><div class="dir">下一篇 ${arrowR}</div><div class="name">${next.t}</div></a>`
            : `<div class="none">已是最后一篇</div>`}`;
        const footer = content.querySelector('footer');
        if(footer && footer.parentElement === content) content.insertBefore(pager, footer);
        else content.appendChild(pager);
      }

      // 屏幕两侧悬停翻页箭头
      function makeEdge(isPrev, art){
        const edge = document.createElement('a');
        edge.id = isPrev ? 'kb-edge-prev' : 'kb-edge-next';
        edge.className = 'kb-edge ' + (isPrev ? 'left' : 'right');
        edge.href = UP + encodeURI(art.u);
        edge.title = (isPrev ? '上一篇（←）' : '下一篇（→）') + art.t;
        edge.innerHTML = `
          <span class="chev">${isPrev
            ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>'
            : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>'}</span>
          <span class="meta"><em>${isPrev ? '上一篇' : '下一篇'}</em><b>${art.t}</b></span>`;
        document.body.appendChild(edge);
      }
      if(prev) makeEdge(true, prev);
      if(next) makeEdge(false, next);
    }
    buildPager();

    // 键盘 ←/→ 翻页（输入框内、术语弹窗打开时不触发）
    document.addEventListener('keydown', e => {
      if(e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
      const t = e.target;
      if(t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.tagName === 'SELECT' || t.isContentEditable)) return;
      if(document.querySelector('.gloss-overlay')) return;
      const art = e.key === 'ArrowLeft' ? prev : next;
      if(!art) return;
      e.preventDefault();
      const href = UP + encodeURI(art.u);
      const base = location.pathname.replace(/\/[^/]*$/, '/');
      updateHere(art.u);
      navigateTo(base + href, href);
    });

    /* ---------- 6. 滚动：进度条（监听内容容器） ---------- */
    content.addEventListener('scroll', () => {
      const max = content.scrollHeight - content.clientHeight;
      prog.style.width = (max > 0 ? (content.scrollTop / max) * 100 : 0) + '%';
    }, {passive:true});

    /* ---------- 7. 目录点击：平滑跳转正文 ---------- */
    document.addEventListener('click', e => {
      const a = e.target.closest('#kb-toc a, .toc a');
      if(!a) return;
      const href = a.getAttribute('href');
      if(!href || !href.startsWith('#')) return;
      const target = document.querySelector(href);
      if(!target) return;
      e.preventDefault();
      target.scrollIntoView({behavior:'smooth', block:'start'});
      history.replaceState(null, '', href);
    });

    /* ============================================================
       SPA 无刷新导航：拦截内部链接，只替换文章内容
       ============================================================ */

    function isShell(el){
      if(el.id && SHELL_IDS.includes(el.id)) return true;
      if(el.id === 'gloss-overlay') return true;
      return false;
    }

    // 重新初始化术语系统
    function reinitGlossary(){
      if(typeof window.initGlossary === 'function'){
        try{ window.initGlossary(); }catch(e){}
      }
    }

    // 更新当前文章索引
    function updateHere(path){
      here = path;
      curIdx = -1; prev = null; next = null; curCat = null;
      flat.forEach((a,i) => { if(a.u === here){ curIdx = i; prev = flat[i-1]||null; next = flat[i+1]||null; } });
      M.cats.forEach(c => c.arts.forEach(a => { if(a.u === here) curCat = c; }));
    }

    // 切换到新页面内容
    function navigateTo(url, pushUrl){
      // 进度条动画
      prog.style.width = '20%';
      prog.style.transition = 'width 0.2s ease';

      fetch(url)
        .then(r => r.text())
        .then(html => {
          const doc = new DOMParser().parseFromString(html, 'text/html');
          // 更新标题
          document.title = doc.title;
          // 更新面包屑
          const crumb = document.getElementById('kb-crumb');
          if(crumb && curCat){
            crumb.innerHTML = `<a class="kb-cat" href="${UP}../index.html#/book/${encodeURIComponent(curCat.key)}" title="回到书架 · 「${curCat.name}」这本书">${curCat.icon} ${curCat.name}</a><span class="kb-sep">·</span><span class="kb-title">${doc.title.replace('｜全栈技术知识库','')}</span>`;
          }
          // 先把新内容准备好
          const temp = document.createElement('div');
          Array.from(doc.body.children).forEach(el => {
            if(isShell(el)) return;
            if(el.tagName === 'SCRIPT' && el.src && el.src.includes('app.js')) return;
            temp.appendChild(document.importNode(el, true));
          });
          // 一次性替换（在内容容器内）
          Array.from(content.children).forEach(el => el.remove());
          Array.from(temp.children).forEach(el => {
            content.appendChild(el);
            el.classList.add('kb-article-in');
          });
          // 重新提取目录栏
          extractToc();
          // 重建 pager
          buildPager();
          // 更新进度/已读状态与继续阅读记录
          try{ localStorage.setItem('kb_last', JSON.stringify({ u: here })); }catch(e){}
          syncPos();
          syncReadBtn();
          // 重新初始化术语
          reinitGlossary();
          // 滚动到顶（内容容器）
          content.scrollTop = 0;
          prog.style.width = '100%';
          setTimeout(() => { prog.style.width = '0'; }, 200);
        })
        .catch(() => {
          location.href = url;
        });
    }

    // 拦截所有内部链接点击（事件委托）
    document.addEventListener('click', e => {
      const a = e.target.closest('a');
      if(!a) return;
      const href = a.getAttribute('href');
      if(!href || href.startsWith('#') || href.startsWith('javascript:') || href.startsWith('http')) return;
      if(a.target === '_blank') return;
      // 只拦截 .html 链接
      if(!href.endsWith('.html')) return;
      // 首页链接不拦截（整页跳）
      if(href.includes('index.html')) return;

      e.preventDefault();
      // 计算相对路径
      const base = location.pathname.replace(/\/[^/]*$/, '/');
      const url = base + href;
      const path = window.__KB_REL(href);
      updateHere(path);
      navigateTo(url, href);
    });

    // 浏览器前进/后退
    window.addEventListener('popstate', e => {
      location.reload();
    });
  }
})();

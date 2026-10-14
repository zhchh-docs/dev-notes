/* ============================================================
   知识库阅读外壳 app.js
   自动注入顶栏 / 目录栏 / 进度条 / 上下篇 / 暗色模式
   目录栏与正文双栏各自独立滚动，点目录平滑跳转正文
   支持 SPA 无刷新导航
   ============================================================ */
(function(){
  // 动态加载 manifest.js
  const s = document.createElement('script');
  s.src = '../assets/manifest.js';
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

    let here = decodeURIComponent(location.pathname.split('/').slice(-2).join('/'));
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
      <a class="kb-btn" href="../index.html" title="返回首页" style="text-decoration:none">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m12 19-7-7 7-7"/><path d="M19 12H5"/></svg>
      </a>
      <div id="kb-crumb">
        ${curCat ? `<a class="kb-cat" href="../index.html#cat-${encodeURIComponent(curCat.key)}" title="回到首页 · 定位到「${curCat.name}」模块">${curCat.icon} ${curCat.name}</a><span class="kb-sep">·</span>` : ''}
        <span class="kb-title">${document.title.replace('｜全栈技术知识库','')}</span>
      </div>
      <div class="kb-right">
        <button class="kb-btn" id="kbThemeBtn" title="切换主题">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        </button>
      </div>`;
    document.body.appendChild(bar);

    /* ---------- 内容包装：右侧独立滚动容器 ---------- */
    let content = document.getElementById('kb-content');
    if(!content){
      content = document.createElement('div');
      content.id = 'kb-content';
      Array.from(document.body.children).forEach(el => { if(!isShell(el)) content.appendChild(el); });
      document.body.appendChild(content);
    }

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
            ? `<a class="prev" href="../${encodeURI(prev.u)}"><div class="dir">${arrowL} 上一篇</div><div class="name">${prev.t}</div></a>`
            : `<div class="none">已是第一篇</div>`}
          ${next
            ? `<a class="next" href="../${encodeURI(next.u)}"><div class="dir">下一篇 ${arrowR}</div><div class="name">${next.t}</div></a>`
            : `<div class="none">已是最后一篇</div>`}`;
        const footer = content.querySelector('footer');
        if(footer) content.insertBefore(pager, footer);
        else content.appendChild(pager);
      }

      // 屏幕两侧悬停翻页箭头
      function makeEdge(isPrev, art){
        const edge = document.createElement('a');
        edge.id = isPrev ? 'kb-edge-prev' : 'kb-edge-next';
        edge.className = 'kb-edge ' + (isPrev ? 'left' : 'right');
        edge.href = '../' + encodeURI(art.u);
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
      const href = '../' + encodeURI(art.u);
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
            crumb.innerHTML = `<a class="kb-cat" href="../index.html#cat-${encodeURIComponent(curCat.key)}" title="回到首页 · 定位到「${curCat.name}」模块">${curCat.icon} ${curCat.name}</a><span class="kb-sep">·</span><span class="kb-title">${doc.title.replace('｜全栈技术知识库','')}</span>`;
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
      const path = decodeURIComponent(href.replace(/^\.\.\//,''));
      updateHere(path);
      navigateTo(url, href);
    });

    // 浏览器前进/后退
    window.addEventListener('popstate', e => {
      location.reload();
    });
  }
})();

# 深入浅出现代 WEB 编程 —— 全栈公开课（Full Stack Open 中文版 · 离线全量镜像）

> **📖 阅读入口**：本镜像已转换为排版友好的 HTML 模块并接入知识库首页 → 返回根目录打开 `index.html`，选择「🎓 全栈公开课」，或直接打开 `../15_全栈公开课/00_课程导览与学习路线.html`（含 4 阶段学习路线与进度追踪）。

> 原站：<https://fullstackopen.com/zh/> （已验证可正常访问）
> 本目录为该开源课程中文内容的全量本地副本，原封不动保留了正文、代码示例、练习与图片。

## 出处与版权（请勿删除）

- 课程由芬兰**赫尔辛基大学**（University of Helsinki）与 **Houston Inc.** 合作推出。
- 课程材料的 0-8 章节和第 13 章节是 [Matti Luukkainen](https://github.com/mluukkai) 所写。第 9 章节的内容由 [Terveystalo](https://www.terveystalo.com/fi/Yritystietoa/Terveystalo-tyontantajana/Digital-Health/) 的开发者所著。第 10 部分由 [Kalle Ilves](https://github.com/Kaltsoon) 编写。第 11 部分由 [Smartly](https://www.smartly.io/) 的开发人员编写，第 12 部分由 [Jami Kousa](https://github.com/jakousa) 编写。众多[开发者](https://github.com/fullstack-hy2020/misc/blob/master/contributors.md)为课程材料做出了贡献。
- **中文版由 [ZhangWei（微信：richardzhangv）](https://zhangwei.online/blog)翻译**。
- 内容版权在 [Creative Commons BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/) 协议框架下执行：可自由使用和分发，但须保留原作者信息；修改后分发同样需遵循该协议；未经许可禁止用于商业目的。
- 内容源码仓库：<https://github.com/fullstack-hy2020/fullstack-hy2020.github.io>（`src/content/*/zh/`，浅克隆于主分支）。

## 目录结构

```
docs/
├── README.md          # 本文件（索引）
├── part0/ ... part13/ # 各部分章节（Markdown，原文件名不变）
├── images/            # 全部章节引用的图片（523 张，路径已改写为 ../images/... 可离线直接阅读）
└── site-pages/        # 官网首页/关于/FAQ 等页面的中文文案（JSON）
```

## 课程内容总目录

### 部分 0：Web 应用的基础设施
- [part0.md](part0/part0.md)（课程概述/通用信息）
- [part0a.md](part0/part0a.md) — Prerequisites（预备知识）
- [part0b.md](part0/part0b.md) — HTTP GET（Web 应用的基础知识）

### 部分 1：React 入门
- [part1.md](part1/part1.md)（概述）
- [part1a.md](part1/part1a.md) — 组件
- [part1b.md](part1/part1b.md) — 变量（JavaScript）
- [part1c.md](part1/part1c.md) — 组件的辅助函数
- [part1d.md](part1/part1d.md) — 复杂状态（调试 React 应用）

### 部分 2：与服务端通信
- [part2.md](part2/part2.md)（概述）
- [part2a.md](part2/part2a.md) — console.log（渲染集合与模块）
- [part2b.md](part2/part2b.md) — 在组件状态中保存笔记（表单）
- [part2c.md](part2/part2c.md) — 浏览器作为运行环境（获取数据）
- [part2d.md](part2/part2d.md) — REST（Alter 数据）
- [part2e.md](part2/part2e.md) — 改进错误信息（CSS 样式）

### 部分 3：用 NodeJS 和 Express 写服务端程序
- [part3.md](part3/part3.md)（概述）
- [part3a.md](part3/part3a.md) — 简单的 web 服务端（Node.js 与 Express）
- [part3b.md](part3/part3b.md) — 同源策略和 CORS（将应用部署到互联网）
- [part3c.md](part3/part3c.md) — 调试 Node 程序（保存数据到 MongoDB）
- [part3d.md](part3/part3d.md) — 将数据库后端部署到生产环境（练习与校验/Eslint）

### 部分 4：测试 Express 服务端程序，以及用户管理
- [part4.md](part4/part4.md)（概述）
- [part4a.md](part4/part4a.md) — Project structure（后端项目结构）
- [part4b.md](part4/part4b.md) — Test environment（测试 Node 应用）
- [part4c.md](part4/part4c.md) — References across collections（用户管理）
- [part4d.md](part4/part4d.md) — Limiting creating new notes to logged in users（Token 认证）

### 部分 5：测试 React 应用
- [part5.md](part5/part5.md)（概述）
- [part5a.md](part5/part5a.md) — Adding a Login Form（登录表单）
- [part5b.md](part5/part5b.md) — Displaying the login form only when appropriate（props.children 与 propTypes）
- [part5c.md](part5/part5c.md) — Rendering the component for tests（测试 React 应用）
- [part5d.md](part5/part5d.md) — Playwright（端到端测试）
- [part5e.md](part5/part5e.md) — Cypress（端到端测试）

### 部分 6：利用 Redux 进行状态管理
- [part6.md](part6/part6.md)（概述）
- [part6a.md](part6/part6a.md) — Flux-architecture（Flux 架构与 Redux）
- [part6b.md](part6/part6b.md) — Store with complex state（拆分 reducer、connect）
- [part6c.md](part6/part6c.md) — Exercises 6.13.-6.14.（React Query）
- [part6d.md](part6/part6d.md) — Managing data on the server with the React Query library（context API）
- [part6e.md](part6/part6e.md) — react-redux hooks（useDispatch/useSelector）

### 部分 7：React router、自定义 hook、CSS 和 webpack 样式
- [part7.md](part7/part7.md)（概述）
- [part7a.md](part7/part7a.md) — Application navigation structure（React Router）
- [part7b.md](part7/part7b.md) — Hooks（自定义 hook）
- [part7c.md](part7/part7c.md) — Ready-made UI libraries（UI 组件库）
- [part7d.md](part7/part7d.md) — Bundling（Webpack/Vite 打包）
- [part7e.md](part7/part7e.md) — Class Components（类组件、E2E 与杂项）
- [part7f.md](part7/part7f.md) — Exercises 7.9.-7.21.

### 部分 8：GraphQL
- [part8.md](part8/part8.md)（概述）
- [part8a.md](part8/part8a.md) — Schemas and queries（Schema 与查询）
- [part8b.md](part8/part8b.md) — Apollo client（Apollo Client）
- [part8c.md](part8/part8c.md) — Mongoose and Apollo（React 与 GraphQL）
- [part8d.md](part8/part8d.md) — User login（数据库与用户登录）
- [part8e.md](part8/part8e.md) — Fragments（Fragments 与订阅）

### 部分 9：TypeScript
- [part9.md](part9/part9.md)（概述）
- [part9a.md](part9/part9a.md) — Main principle（背景与基本原则）
- [part9b.md](part9/part9b.md) — Setting things up（TypeScript 基础）
- [part9c.md](part9/part9c.md) — Setting up the project（第一个 TypeScript 应用）
- [part9d.md](part9/part9d.md) — Create React App with TypeScript（React + TS 实战）

### 部分 10：React Native
- [part10.md](part10/part10.md)（概述）
- [part10a.md](part10/part10a.md) — About this part（介绍与基础）
- [part10b.md](part10/part10b.md) — Core components（核心组件）
- [part10c.md](part10/part10c.md) — HTTP requests（网络请求与移动端导航）
- [part10d.md](part10/part10d.md) — Testing React Native applications（测试与发布）

### 部分 11：CI/CD
- [part11.md](part11/part11.md)（概述）
- [part11a.md](part11/part11a.md) — Getting software to production（CI/CD 入门）
- [part11b.md](part11/part11b.md) — Basic needs（GitHub Actions 基础）
- [part11c.md](part11/part11c.md) — Anything that can go wrong...（部署与监控）
- [part11d.md](part11/part11d.md) — Working with Pull Requests（PR 工作流）
- [part11e.md](part11/part11e.md) — Visibility and Understanding（可见性与理解）

### 部分 12：容器
- [part12.md](part12/part12.md)（概述）
- [part12a.md](part12/part12a.md) — About this part（容器介绍与 Docker 基础）
- [part12b.md](part12/part12b.md) — Dockerfile（配置 web 应用容器）
- [part12c.md](part12/part12c.md) — React in container（容器化实践）

### 部分 13：使用关系型数据库
- [part13.md](part13/part13.md)（概述）
- [part13a.md](part13/part13a.md) — Advantages and disadvantages of document databases（关系型数据库与 Sequelize）
- [part13b.md](part13/part13b.md) — Application structuring（join 表与查询）
- [part13c.md](part13/part13c.md) — Migrations（迁移与 Session 认证）

## 说明

- 各部分正文文件（`partXa.md` 等）为官网页面原文，包含全部讲解、代码与练习；`partX.md` 为该部分概述页。
- 文件中夹杂的英文 HTML 注释为官网翻译源文件格式，原样保留。
- 图片均已复制到 `docs/images/` 并改写了 Markdown 中的相对路径，任意 Markdown 阅读器（如 VS Code、Typora）打开即可离线阅读。
- 部分内容（如部分 4-8、10-13 的标题）在中文翻译源文件中仍为英文标题，与官网显示一致（官网页面标题即沿用英文）。
- 更新至官方仓库主分支当前版本（2026-10 克隆）。

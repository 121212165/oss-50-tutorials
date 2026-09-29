---
num: 08
title: WXT：10.5k star 的现代扩展框架，"Nuxt 之于网站，WXT 之于扩展"
repo: wxt-dev/wxt
category: 浏览器扩展 / 油猴
audio: 08.mp3
minutes: 7
---

## 它是什么（30 秒版）

WXT 是"下一代浏览器扩展框架"（10.5k+ star，MIT 协议，Nuxt 式理念）：基于 Vite 的构建工具 + 开发框架，支持 MV2/MV3 和所有主流浏览器，提供文件即入口（entrypoints）、热更新（HMR）、TypeScript 开箱即用、自动导入、一键发布到各应用商店。官方口号是 "It's like Nuxt, but for Web Extensions"。

## 为什么对你超有帮助

你手写过 MV3 扩展（bili-scanner 的 MV3 渠道），对原生开发的痛有体感：manifest.json 手写、background/content script/popup 每改一次手动 reload、没有热更新、多浏览器兼容靠条件分支。WXT 把这些全解决了，而且对你有三个具体升级点：①**文件即入口**——你不用再写 manifest.json，建一个 `content.ts` 或 `background.ts` 文件，WXT 自动生成对应配置，扩展结构一目了然；②**开发体验**——`wxt` 命令起 dev server，content script 改动自动注入刷新，popup 支持 HMR，扫榜脚本的"改→看榜单渲染→再改"循环从分钟级缩到秒级；③**自动发布**——它内置 BPP 体系把扩展自动提交到 Chrome Web Store 和 Firefox Add-ons，你双渠道发布（油猴 + 商店）里"商店"那一半可以从手工上传变成 CI 自动化。还有一点：你是 JS 开发者学 Vite 生态，用熟悉的扩展领域切入，学习成本几乎为零。

## 架构拆解

WXT 本质是"Vite 之上的多层封装"：最底层 Vite 负责打包（你 Obsidian 插件里见过的 esbuild 同门兄弟，同属 Vite 系）；第二层是**入口解析器**，扫描 `entrypoints/` 目录，按文件名约定（`background.ts`、`content.ts`、`popup/index.html`、`options/index.html`）推导出 manifest 的每个字段，多浏览器差异（MV2/MV3、service worker vs background page）在这一层自动处理；第三层是**开发服务器**，管理 HMR 通道和"扩展 reload"——扩展和普通网页不同，改代码后要重新加载扩展本身，WXT 通过和浏览器扩展管理页通信把这步自动化了；最外层是**模块系统**和**存储/API 封装**（`wxt/utils/storage` 这类工具函数），以及统一的 `wxt build -b firefox` 多目标构建。整体思路：把"扩展开发的杂活"全部下沉到框架，业务代码只关心逻辑。

## 上手路径

第一步：`npx wxt@latest init`，选 vanilla-ts 模板建项目。第二步：看生成的 `entrypoints/` 目录，对照你 MV3 扩展的 manifest.json，找到每个字段"消失到了哪里"——这一步是理解 WXT 的关键。第三步：把你 bili-scanner 的 content script 逻辑搬进 `entrypoints/bilibili-scanner.content.ts`，`wxt` 起 dev，打开 B 站榜单页验证注入。第四步：`wxt build` 出包，浏览器手动加载一次确认功能等价。第五步：读 `wxt.config.ts`，补上 name/version/permissions。

## 进阶玩法 / 避坑

避坑一：WXT 的 auto-imports 会自动引入 `defineContentScript` 等函数，编辑器没提示时先跑一次 `postinstall`。避坑二：MV3 的 service worker 会被浏览器休眠，长驻定时器逻辑（比如定时扫榜）要用 alarms API，WXT 不替你做这个决定。进阶：用它的 module 机制把你的"匿名请求工具箱"抽成可复用模块；再配 GitHub Actions 跑 `wxt build + zip`，加 BPP 做全自动双渠道发布——这一套跑通，你的扩展开发效率会断档领先手写时代。

## 横向对比：为什么是这个不是别的

WXT vs Plasmo vs CRXJS 三选一：WXT 赢在 Vite 生态 + 灵活 + 全浏览器支持，Plasmo 赢在 React 全家桶 + 托管服务，CRXJS 赢在"只做插件不做框架"。你的画像（已有项目要渐进迁移、JS 老手、讨厌被框架接管）指向 WXT——它是三者里"框架感"和"自由度"平衡最好的。

## 认知红利：这篇能改变你什么

"文件即入口"的设计会让你重新理解约定优于配置：manifest.json 本质是"用 JSON 描述目录结构的冗余写法"。凡是"配置文件描述的东西其实可以从目录推导"的场景（路由、入口、菜单），都可以用同一招消灭配置——这是现代工具链的通用减法。

> 冷知识：WXT 的作者 aklinker1 同时是另一款开源扩展框架的作者——做扩展工具的人自己就是扩展重度用户，这是开源生态里最健康的创作者画像。

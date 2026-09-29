---
num: 10
title: CRXJS：给"手写 manifest"的你补上 Vite 的全部红利的 Vite 插件
repo: crxjs/chrome-extension-tools
category: 浏览器扩展 / 油猴
audio: 10.mp3
minutes: 6
---

## 它是什么（30 秒版）

CRXJS（4.1k+ star，包名 `@crxjs/vite-plugin`）不是一个框架，而是一个 **Vite 插件**：你在手写 manifest.json 的基础上加它进来，立刻获得零配置打包、原生 HMR 热更新、content script/HTML 页面的自动处理。它的哲学是"不接管你的项目，只补齐工具链"——框架（WXT/Plasmo）之外的第二条路。

## 为什么对你超有帮助

你手里有两条现成的升级路径对比：bili-scanner 的 MV3 渠道目前是手写 manifest + 手动 reload；08/09 篇的 WXT、Plasmo 是整项目迁移框架。而 CRXJS 是第三条——**渐进式**：保留你现有 manifest.json 和项目结构，只引入 Vite。适合你的三个场景：①你的扩展已经写好、不想大动结构，只想让开发体验现代化，CRXJS 改动成本最小；②你正在学 Vercel/现代前端工具链，而 Vite 是这个生态的通用底座（Vite、esbuild、Rollup 插件协议），通过自己最熟的扩展项目学它，学到的能力直接迁移到 Next.js、静界、portfolio-site 所有项目；③manifest 还是你亲手维护的——WXT/Plasmo 把 manifest 藏起来换开发效率，但官方审核和疑难排查时 manifest 是第一现场，CRXJS 让你继续掌控它。适合不喜欢"约定魔法"、想看清每一层发生了什么的开发者——从你的风格（纯匿名硬约束、亲力亲为的架构偏好）看，这条路线气质上很合。

## 架构拆解

CRXJS 的工作原理一句话：**它读你的 manifest.json，把里面声明的每个入口变成 Vite 构建图的一部分**。拆开三层：①入口转换层——manifest 里的 background service worker、content script、popup HTML 被它拦截，改写为 Vite 可处理的模块（比如 content script 会包一层供注入的 wrapper）；②HMR 层——dev 模式下它注入一个桥接脚本，content script 和页面文件改动通过 WebSocket 推送，扩展不用手动 reload（MV3 service worker 的限制下，它尽量做到部分热更新，个别情况仍需重载扩展，这是所有框架共有的物理限制）；③资源层——CSS、图片、动态 import 都按 Vite 习惯处理，最终 `vite build` 产出和 manifest 声明一致的 dist 目录，直接可加载可上架。没有目录约定、没有框架强加的 API，你的代码就是普通前端代码。

## 上手路径

第一步：在 bili-scanner 的 MV3 项目里 `npm i -D @crxjs/vite-plugin vite`。第二步：新建 `vite.config.ts`，三行核心：导入 crxjs 插件、传 manifest 路径、导出。第三步：`npx vite` 起 dev，把 dist 加载进浏览器，改一次 content script 看自动生效。第四步：`npx vite build` 出生产包，对照旧包确认功能一致。第五步：把 popup 页也迁进来，体验 HTML 直接 import 模块。

## 进阶玩法 / 避坑

避坑一：CRXJS 对 manifest 某些冷门字段（如 `web_accessible_resources` 的复杂写法）处理有历史坑，迁移后全功能回归一遍；遇到问题先去它 GitHub issue 区搜，近年更新节奏偏慢，锁版本用。避坑二：dev 模式下 content script 的 HMR 不是万能的，改 background 逻辑后仍要重载扩展。进阶：配 Tailwind（第 30 篇）给扩展 UI 升级样式系统；把 `vite build` 接进你已有的发布脚本，形成"手写 manifest + 现代工具链"的混合工作流——这套组合会让你对扩展构建的理解超过 90% 的框架用户。

## 横向对比：为什么是这个不是别的

三条扩展工具路线的终局对比：CRXJS（渐进增强，保留手写 manifest）是"保守疗法"，WXT/Plasmo（框架接管）是"根治手术"。CRXJS 近年更新偏慢是它的隐忧，但"你对每一层都看得见"这个特质没有替代品——先走 CRXJS 摸清构建本质，再上框架，顺序反了会一直被框架的黑盒困住。

## 认知红利：这篇能改变你什么

CRXJS 教的是"寄生式现代化"：不重写项目，把新工具作为插件嫁接到旧结构上。这套思路适用于你的一切存量资产——老脚本、老插件、老站点，都可以先问"有没有一个 Vite 插件/包装层能让它提速"，而不是推倒重来。渐进优于重写，是工程的一级结论。

> 冷知识：CRXJS 仓库原名 crxjs/vite-plugin，后更名为 crxjs/chrome-extension-tools——开源项目把自己的定位从"插件"升级成"品牌"的典型一跃。

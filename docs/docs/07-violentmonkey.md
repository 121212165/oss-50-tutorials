---
num: 07
title: Violentmonkey：开源油猴脚本管理器，看看你的脚本运行在什么"地基"上
repo: violentmonkey/violentmonkey
category: 浏览器扩展 / 油猴
audio: 07.mp3
minutes: 6
---

## 它是什么（30 秒版）

Violentmonkey（8.9k+ star）是一个完全开源的油猴（userscript）管理器，Chrome/Edge/Firefox 全支持，功能对标 Tampermonkey 但代码透明。它负责解析用户脚本的 `==UserScript==` 元数据头、决定脚本在哪个页面注入、提供 GM_* 特权 API（跨域请求、存储、菜单），是数以万计用户脚本的"运行时操作系统"。

## 为什么对你超有帮助

你的 B 站扫榜脚本（油猴渠道）每天都在 Violentmonkey 这类管理器里跑，但多数人只知其然：为什么 `@grant GM_xmlhttpRequest` 之后就能绕过页面同源限制、匿名发请求？为什么 `@match` 写错脚本就不注入？为什么脚本有时"提前跑了"拿不到页面元素？——把 Violentmonkey 当教材读一遍，这些全有答案，而且直接决定你脚本的健壮性。三个具体点：①它的沙箱与注入时机实现，解释了 `document-idle` 和 `run-at` 的真实语义，你抓 card 接口那种"要在列表渲染后才能拿到数据"的时序问题根源在此；②GM_xmlhttpRequest 的跨域实现走的是扩展后台进程，这就是你"纯匿名硬约束"（不带页面 cookie、自己发请求）能成立的技术前提，弄懂它你才知道这个约束的边界在哪；③它的打包与多浏览器构建流程（`pnpm dev` 监听、load unpacked、Firefox 临时加载）就是你 MV2/MV3 双渠道调试流程的范本。

## 架构拆解

它是标准 WebExtension（MV2 结构），三块进程各司其职：**后台脚本**（background）常驻，管 GM API 权限授予、跨域请求代理、脚本状态存储——你的跨域请求实际上是"内容脚本发消息 → 后台代为发出 → 结果传回"，所以能绕过页面同源；**内容脚本**（injected）注入到匹配页面，先把 userscript 包在一个沙箱函数里再 eval 执行，既隔离变量污染又暴露 GM API；**注入器**用两个通道：页面 DOM 直接注入（快但拿不到 GM API）和扩展注入（完整 API），@grant 的有无决定走哪条通道——这就是"加了 @grant 之后 window 行为变了"的原理。脚本管理器部分则是常规的代码编辑器（CodeMirror）、存储（IndexedDB）与更新检查器。

## 上手路径

第一步：先把它当用户：装好，把你 B 站脚本导出备份（设置里有 Export）。第二步：读自己的脚本的元数据头，逐行弄懂 @match/@grant/@run-at 每个声明现在是谁在解释执行。第三步：clone 仓库，`pnpm ci` 装依赖、`pnpm dev` 编译，Chrome 里 load unpacked 加载 dist 目录——你在跑自己改过的脚本管理器。第四步：在源码里全局搜 `GM_xmlhttpRequest`，找到它在后台脚本的实现，读一遍请求转发链路。

## 进阶玩法 / 避坑

避坑一：改完自己的版本记得先停用官方安装的实例，两个管理器同时注入会重复执行脚本。避坑二：它的 nightly 构建有 bug 属正常，别当生产环境。进阶方向：给 Violentmonkey 提一个你踩过的 bug PR——它 issue 区活跃，中文用户多；另外读它的 sandbox 实现（injected/web 目录）之后，你会对"扩展如何安全运行第三方代码"有体系认知，这正是你从写脚本迈向写扩展的分水岭。

## 横向对比：为什么是这个不是别的

油猴管理器三巨头：Tampermonkey（闭源、功能最全）、Violentmonkey（开源、轻快）、Greasemonkey（鼻祖、已衰落）。选 Violentmonkey 的理由是"能读的源码"：闭源的 Tampermonkey 对你是黑盒，而 Violentmonkey 让你能看到"我写的脚本到底跑在什么环境里"——对你这种要把原理摸透的人，开源即正义。

## 认知红利：这篇能改变你什么

读它的沙箱实现会让你重新理解"权限"：你的脚本能跨域，不是因为浏览器慷慨，而是因为扩展后台替你转发。特权从来是被授权的——这个认知在你写任何"越权"功能（本地工具访问系统资源）时都适用：特权要走显式通道，才能可审计、可撤销。

> 冷知识：Violentmonkey 的 Discord 里中文用户占比惊人——userscript 文化在国内二次元、追剧、比价场景里格外繁荣，你的 B 站脚本正是这个传统的延续。

---
num: 09
title: Plasmo：13k star 的"扩展版 Next.js"，带 UI 框架和云服务的全家桶
repo: PlasmoHQ/plasmo
category: 浏览器扩展 / 油猴
audio: 09.mp3
minutes: 6
---

## 它是什么（30 秒版）

Plasmo（13.1k+ star）自称 "Next.js for browser extensions"，是一个"电池全带"的扩展 SDK：React + TypeScript 一等公民、声明式开发（基本不用碰 manifest）、Content Scripts UI（在别人网页里渲染 React 组件）、跨浏览器多目标构建、`.env` 环境变量、内置 Storage 和 Messaging API，还配套官方的自动提交服务 BPP 和测试云 Itero。它比 WXT 更"框架"，约定更多、替你决定的也更多。

## 为什么对你超有帮助

关键看你对扩展现阶段的规划。你 bili-scanner 目前是"轻 UI"形态（数据卡片），但如果下一步要做"扫榜控制台"——带筛选、收藏、多标签对比的重 UI——纯 TS + 原生 DOM 会越写越痛，这时候 Plasmo 的两个杀手锏直接命中：①**CSUI（Content Scripts UI）**：在 B 站页面里挂一个 React 组件、还带 Shadow DOM 隔离（页面样式污染不了你），这是扩展开发里公认最难啃的部分，Plasmo 一行配置解决；②**Messaging API**：background 和 content script 之间的消息通信被封装成带类型的函数调用，你扫榜时"content 抓数据 → background 转发/存储"的双进程协作不再是手写 chrome.runtime.sendMessage 大杂烩。另外它的官方示例库（React+Tailwind、Supabase、Firebase 登录等）质量很高，等你做"扫榜云同步""多设备收藏"这类功能时可以直接抄作业。一句话选型：重 UI、React 熟、想要约定式全托管 → Plasmo；要灵活轻量、贴 Vite 生态 → WXT（第 08 篇）。

## 架构拆解

Plasmo 的架构心智模型是"**把扩展当 Next.js 应用写**"：①入口系统——`popup.tsx`、`content.ts`、`background.ts` 按文件约定生成 manifest，和 WXT 同思路但强绑 React；②CSUI 渲染管线——content script 里创建 Shadow DOM 容器，把 React 组件渲染进去，宿主页面的 CSS 被隔离层挡住，你的 UI 想用什么组件库都行；③存储层——`@plasmohq/storage` 包装 chrome.storage，暴露成类 localStorage 的同步 API，还支持监控变化；④消息层——类型化消息定义，编译期检查发送方与接收方对得上；⑤构建层——底层用 Parcel（不是 Vite），多目标构建 `-b firefox` 一条命令出对应平台包。理解了这五层，你就明白"框架化的扩展开发"到底框架了什么：约定目录、UI 隔离、状态同步、多平台打包。

## 上手路径

第一步：`pnpm dlx plasmo init`（建议先装 pnpm），选 React + TypeScript 模板。第二步：`pnpm dev`，浏览器加载 build 目录，改 popup 内容看热更新效果。第三步：在 `content.tsx` 里写一个 React 组件挂到任意网页，体验 CSUI——这是 Plasmo 最值得一看的瞬间。第四步：把你扫榜的卡片 UI 用 React 重写一版，感受组件化的可维护性差距。第五步：接 `@plasmohq/storage` 把扫榜历史存本地。

## 进阶玩法 / 避坑

避坑一：Plasmo 约定优先，想高度自定义构建流程会觉得"框架在挡路"，这类需求选 WXT。避坑二：CSUI 的 anchor 定位（组件挂在页面哪个位置）在目标网站改版时要跟着调，B 站页面结构更新后记得回归测试。进阶：用它的 Tab Pages 做扫榜控制台独立页；用 BPP 把商店发布接进 GitHub Actions，实现"git push 即上架"——这是你正在学的自动化部署在扩展领域最爽的应用。

## 横向对比：为什么是这个不是别的

同为"扩展框架"，Plasmo 与 WXT 的分野是商业策略：Plasmo 用框架引流、靠云服务（BPP/Itero）变现，所以它"电池全带、约定严格"；WXT 纯社区驱动，更中立轻量。要"团队级工程规范 + 发布自动化"选 Plasmo，要"工具链干净、自己说了算"选 WXT。

## 认知红利：这篇能改变你什么

CSUI（在别人网页里渲染你的 React 组件）暴露了一个通用难题：如何在不可控的宿主环境里安全地渲染自己的 UI？Shadow DOM 隔离只是表象，本质是"样式主权、事件主权、生命周期主权"三权分立——这个模型在所有"嵌入型 UI"（插件面板、小程序卡片、嵌入式 SDK）里都成立。

> 冷知识：Plasmo 团队写过一本免费的《The Browser Extensions Book》——框架公司发书教生态，是最聪明的开发者关系投资。

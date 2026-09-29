---
num: 46
title: React Native：12.6 万 star 的"用 React 写原生 App"，你最短学习曲线的移动端路线
repo: facebook/react-native
category: 跨平台 / 鸿蒙 / 移动
audio: 46.mp3
minutes: 5
---

## 它是什么（30 秒版）

React Native 是 Meta 出品的跨平台移动框架（12.6 万 star）：用 React 语法写 Android/iOS 原生应用，口号 "Learn once, write anywhere"。与 Flutter 的"自绘引擎"路线不同，RN 渲染的是**真实原生控件**（新版架构用 JSI 直连原生，性能已大幅改善）。Instagram、Discord、Shopify 等重度产品在用，MIT 协议。

## 为什么对你超有帮助

对你而言 RN 是"移动端学习曲线最短"的一条路，原因只有一个：**你已经会 React**。你的 sleepquiz、portfolio-site、my-app-nextjs 全是 React/Next.js——RN 的组件、hooks、状态管理和你写 Web 的肌肉记忆几乎 1:1（diff 是：div 换 View、img 换 Image、CSS 换 StyleSheet），真实成本大约一到两周。三个决策价值：①**对照决策**：花语助手这类"有原生功能（通知、传感器）+ 重 UI"的应用，RN 比 Web 更合适；和 Flutter 比，RN 赢在"React 知识复用 + Web 生态共享（状态库、工具链）"，输在多端覆盖（Flutter 六端 vs RN 双端为主）。②**新版架构红利**：RN 0.7x+ 的新架构（JSI + Fabric 渲染器）解决了旧版"JS 桥"的性能骂名，现在的 RN 和你听过的旧印象完全不同，选型判断要用新信息。③**迁移思维**：你已有的 React 组件逻辑（比如词源应用的思维导图交互）大部分可移植——先 Web 后 RN 是"渐进上移动端"的省钱路线。

## 架构拆解

三层心智模型：①**JS/TS 层**：你的业务代码（React 组件 + 逻辑），跑在独立 JS 引擎（Hermes，Meta 自研的轻量 JS 引擎，启动快、内存省）；②**JSI 直连层（新架构核心）**：旧版 JS 与原生通信走"异步消息桥"（序列化开销大、易卡顿），新架构 JSI 让 JS 持有原生对象的引用、同步直接调用——这是近年 RN 性能口碑逆转的技术根源；③**原生渲染层（Fabric）**：React 的"影子树"（shadow tree）在 C++ 层与原生 UI 管理器对接，渲染的是平台真实控件——所以 RN 应用的滚动、文字、无障碍体验是"原生级"的，但跨端像素一致性不如 Flutter 自绘。开发流：Metro 打包器（类似 Vite 角色）+ Fast Refresh 热更新 + Expo 工具链（官方现在推荐用 Expo 起 RN 项目，托管原生构建、OTA 更新，新手友好度质变）。

## 上手路径

第一步：`npx create-expo-app@latest my-rn-app`（Expo 是当前官方推荐入口），`npx expo start`，手机装 Expo Go 扫码真机预览——五分钟看到 App 跑在手机上。第二步：把 Web React 组件思维翻译过来：写一个花语列表页（FlatList + Image + Text），体会 RN 组件对照表。第三步：加一个按钮跳转（expo-router 文件路由，和 Next.js App Router 思路同构）。第四步：把 sleepquiz 的一道题做成 RN 卡片组件，验证"React 知识平移"的真实成色。

## 进阶玩法 / 避坑

避坑一：Expo Go 沙箱外需要 dev client/原生构建时（用第三方原生模块），坑会变多，新手期尽量选 Expo SDK 内置能力。避坑二：别把 Web 包（window、DOM API）直接搬进 RN，运行时没有浏览器，用 RN 等价 API。避坑三：RN 与鸿蒙：社区有第三方适配探索但非官方路线，鸿蒙仍走 ArkTS。进阶：用 expo-router 重构一个你现有 Web 应用的移动版最小内核，跑通"同一业务逻辑、Web/RN 双端复用"——这会让你对"学一次写多端"的判断从听说变成体验。

## 横向对比：为什么是这个不是别的

"会 React 的你"的移动端选择：RN（知识直接复用、原生控件）、Flutter（要学 Dart、自绘）、Capacitor（套壳 WebView、最快但体验打折）。如果你的目标是"花最少的时间把产品送上手机"，RN + Expo 是你的最短路径——因为最贵的成本从来不是框架，是你的学习时间。

## 认知红利：这篇能改变你什么

RN 新架构（JSI 直连）的翻身史说明：技术选型的判断有保质期。"RN 性能差"是旧桥时代的结论，如今已过时——定期给"自己以为的知识"做版本更新，和给依赖库升级一样重要。

> 冷知识：Meta 给 RN 配的自研 JS 引擎叫 Hermes（赫尔墨斯，希腊神话的信使之神）——为"通信"命名的引擎，名字里就写着它的使命。

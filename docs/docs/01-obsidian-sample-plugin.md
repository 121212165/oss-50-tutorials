---
num: 01
title: obsidian-sample-plugin：你所有插件的"标准答案"起点
repo: obsidianmd/obsidian-sample-plugin
category: Obsidian 插件开发
audio: 01.mp3
minutes: 6
---

## 它是什么（30 秒版）

这是 Obsidian 官方维护的插件模板仓库，TypeScript 编写，4.5k+ star。它自带一套完整的开发脚手架：TypeScript 编译配置、`manifest.json` 插件清单、示例代码、ESLint 检查、GitHub Actions 自动化。你可以用"Use this template"按钮一键复制成自己的插件项目，省掉从零搭环境的全部痛苦。

## 为什么对你超有帮助

你已经写了 8 个 Obsidian 插件（qs8-panel、daoyu-studio、ai-flavor-checker 等），但你大概率没有系统地对照过官方模板——每次上架 Obsidian 官方插件市场（community plugins）时，审核员检查的第一件事就是你的项目结构符不符合这个模板的规范。三点直接收益：第一，它的 manifest.json 里 `minAppVersion` 与 `versions.json` 的版本映射写法，决定老版本 Obsidian 用户能不能下载到兼容版本，很多人第一次提审就栽在这里；第二，它预置了 Obsidian 官方专属的 ESLint 规则集（`npm run lint` 一条命令），能在提交前查出"内存泄漏的事件监听""未清理的 interval"这类审核硬伤；第三，它演示了发布 Release 时必须同时附上 `manifest.json`、`main.js`、`styles.css` 三个附件——这正是你 obsidian-releases 相关工作里最常出错的环节。

## 架构拆解

整个仓库的核心只有一个文件：`src/main.ts`。TypeScript 写完后，esbuild 把它打包成单个 `main.js`，Obsidian 只认这个文件。拆开看模板演示的五个 API 入口：`onload()` 是插件生命周期的起点，所有初始化必须写在这里；`addRibbonIcon()` 在左侧栏加图标；`addCommand()` 注册命令（Ctrl+P 里能搜到的就是它）；`PluginSettingTab` 渲染设置页；`registerEvent()` / `registerInterval()` 注册的监听必须在插件卸载时自动清理——这个"注册即托管"的设计是 Obsidian 插件架构的灵魂，你的 qs8-panel 这类常驻面板插件全靠它保证关闭笔记时不出幽灵进程。

数据流一句话讲完：用户操作 → 触发 command/event → main.ts 调用 Vault/MetadataCache API 读写笔记 → Notice 或 View 渲染反馈。你的 AI 味检测插件本质上就是"读笔记文本 → 调检测逻辑 → Notice 弹结果"这条链。

## 上手路径

第一步：打开仓库页面点 "Use this template"，得到你自己的新插件仓库。第二步：把它 clone 到 `你的库/.obsidian/plugins/你的插件id/` 目录下（这是模板 README 明确推荐的位置，改完代码 Obsidian 直接能加载）。第三步：`npm i` 装依赖，`npm run dev` 进入监听模式——改一次代码自动编译一次。第四步：设置里启用插件，关掉再开就加载新版本。第五步：想发版时改 manifest 版本号，跑 `npm version patch`，它会同时更新 manifest、package.json 并自动往 versions.json 里补条目。

## 进阶玩法 / 避坑

避坑一：GitHub Release 的 tag 必须是纯版本号 `1.0.1`，不能带 `v` 前缀，否则社区市场抓不到。避坑二：提审到官方市场需要先在 obsidianmd/obsidian-releases 仓库发 PR——你 fork 过这个仓库，正好可以照着别人的 PR 格式写。进阶：把模板里的 GitHub Actions 保留下来，它每次 push 自动跑 lint，等于免费帮你做审核预检。建议下一步拿你的下一个插件想法，严格从这个模板起步，感受一次"完全按官方路子走"的流程差异。

## 横向对比：为什么是这个不是别的

社区里现成的插件模板不止一家（Yeoman 生成器、第三方 boilerplate），但只有官方模板是"审核员亲儿子"——它随 Obsidian API 同步更新、随审核标准变化调整，别家模板多半停更在你用的时候。做插件想上架，官方模板是唯一不会过期的选择。

## 认知红利：这篇能改变你什么

"模板"这个词容易被看轻，但大项目工程化后最重要的恰恰是"一致性"：你的 8 个插件如果共用同一套模板结构，将来任何插件的问题你都能在 3 分钟内定位——因为你不用重新理解项目布局。从下一插起，把"从模板创建"当成纪律而不是偷懒。

> 冷知识：这个仓库的 star 数（4500+）在"模板类"项目里几乎是最高的——说明"官方示范怎么做"本身就是被全球开发者反复需要的公共品。

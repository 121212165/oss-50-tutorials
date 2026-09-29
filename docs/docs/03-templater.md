---
num: 03
title: Templater：会执行 JavaScript 的模板引擎，批量生成笔记的瑞士军刀
repo: SilentVoid13/Templater
category: Obsidian 插件开发
audio: 03.mp3
minutes: 6
---

## 它是什么（30 秒版）

Templater（5.3k+ star）是 Obsidian 的模板插件，定义了一套 `<% %>` 语法：在模板里插入动态变量（今天日期、文件名）、调用内置函数（移动文件、弹输入框）、甚至直接执行 JavaScript 代码来操纵笔记。新建笔记时自动套模板，一键把一个空文件变成结构化的章节卡、人物卡或读书笔记。

## 为什么对你超有帮助

你的创作流程里有大量"固定结构 + 动态内容"的重复劳动：章节卡要带状态字段和字数统计区、人物卡要带性格/口癖/AI 味雷区字段。这些全是 Templater 的主场——写一次模板，每次新建自动生成，frontmatter 都帮你填好。更实际的收益在插件开发层面：你写的 obsidian-fanqie-drafter、obsidian-scan-card-box 都有"从模板生成笔记"的需求，Templater 展示了完整实现路径——`tp.system.prompt()` 怎么安全地拿用户输入、`tp.file.create_new()` 怎么以编程方式创建并填充文件、`app.fileManager.processFrontMatter()` 怎么原子性地写 frontmatter。另外它对你那套 prompt-vault 提示词库也有启发：把"提示词模板 + 变量槽位"的思路用到写作提示词管理上，一条提示词就能批量变体。

## 架构拆解

理解 Templater 只需要抓住三层语法：

**变量层**：`<% tp.date.now("YYYY-MM-DD") %>` 这类，插入动态值。tp 是"templater plugin"对象，下挂 date、file、system、web、frontmatter 等命名空间，每个命名空间是一组函数。

**命令层**：`<%+ %>`、`<%* %>` 变体控制"是否换行/是否只执行不输出"。`<%* %>` 里可以写完整 JavaScript：循环、if、await，用 `tR` 变量拼接输出内容——模板在这里变成了一门"笔记生成编程语言"。

**触发层**：三种执行时机——手动触发（Alt+E）、文件夹触发（进入某文件夹自动应用指定模板）、核心"Templates"插件的日常笔记触发。这个"按文件夹挂模板"的钩子设计值得你抄：drafter 插件完全可以按目录自动给新章节卡挂对应书的世界观模板。

安全模型也值得注意：README 明确警告它可执行任意 JS 和系统命令，所以模板是"信任边界内的代码"。你写插件如果允许用户自定义模板片段，要做同样的风险评估说明。

## 上手路径

第一步：市场安装 Templater，设置里指定模板文件夹（比如 `90-模板`）。第二步：在该文件夹新建 `章节卡.md`，写入：

```markdown
---
书名: <% tp.system.prompt("书名") %>
章节: <% tp.file.title %>
状态: 未写
字数: 0
---
# <% tp.file.title %>

<% tp.date.now("YYYY-MM-DD") %> 开工。
```

第三步：在任何地方新建"第41章"并手动触发模板，看着输入框弹出、frontmatter 自动填好。第四步：进阶一个 `<%* %>` 例子——用 JS 循环生成 10 个空章节卡的雏形，体会它作为"生成器"的一面。

## 进阶玩法 / 避坑

避坑一：模板里不要放 `---` 分隔线以外的 frontmatter 内容，YAML 解析错一个空格整篇字段失效。避坑二：`tp.system.suggester()` 比纯文本输入框更适合"从固定选项里选"（比如选 POV 人物），体验好得多。进阶方向：把 Templater 与 Dataview 组合——模板里内联查询本章在 story-ledger 里的关联伏笔；再读它的 parser 源码（parsers 目录），看一个lexer/解释器怎么把 `<% %>` 语法翻译成 AST，这是你第一次近距离看"小语言"是怎么实现的。

## 横向对比：为什么是这个不是别的

Templater vs 核心模板插件 vs QuickAdd：核心模板只做静态替换，QuickAdd 强在"快速捕获"但生成逻辑弱，Templater 是唯一把"模板当编程语言"的——变量、循环、用户交互俱全。三者其实互补：QuickAdd 负责入口，Templater 负责生成，静态模板负责简单场景。

## 认知红利：这篇能改变你什么

`<%* %>` 里可以写完整 JS——这意味着你的"模板"可以调用 Obsidian 全部 API：读别的笔记、查数据、弹选择框。当你意识到模板=程序，"重复劳动该不该自动化"这个问题就永远消失了：问自己"这个动作模板能不能写出来"，不能，才轮到手做。

> 冷知识：Templater 的原作者是 SilentVoid13（他同时也是日历插件 Days、时间线插件的作者），项目后来交由社区接手——开源项目的"接力棒"文化在这里很典型。

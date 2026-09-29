---
num: 02
title: obsidian-dataview：把整个笔记库变成能查询的数据库
repo: blacksmithgu/obsidian-dataview
category: Obsidian 插件开发
audio: 02.mp3
minutes: 7
---

## 它是什么（30 秒版）

Dataview（9.3k+ star）是 Obsidian 生态里仅次于核心插件的存在：它把你的整个笔记库当作一个数据库，支持用类 SQL 的查询语言（DQL）和 JavaScript API，对笔记的元数据进行筛选、排序、汇总、渲染成表格和列表。一行代码就能"列出 games 文件夹里评分超过 8 分的所有游戏，按评分倒序"。

## 为什么对你超有帮助

两层价值。使用层：你的小说创作系统有大量"元数据密集"的场景——每章笔记标上 status/字数/视角人物，每本书标上题材/完结状态/QS-8 评分。有了 Dataview，一个查询块就能自动生成"未完结书目 + 卡文预警 + 本周产出字数统计"的面板，不用再手工维护表格，这能直接嵌入你的 qs8-panel 仪表盘设想。架构层（更重要）：你要写 obsidian-story-ledger 这种"自动汇总剧情要素"的插件，而 Dataview 就是最标准的参考实现——它示范了怎么监听 vault 的文件变更事件、怎么增量解析 frontmatter 和 `Key:: Value` 内联字段、怎么建内存索引、怎么在 Markdown 渲染时劫持代码块替换成自己的 UI。这一套"Markdown 之上的数据层"思路，可以原样搬进你的插件。

## 架构拆解

核心分两半：**数据**和**查询**。

数据层：来源有三处——YAML frontmatter（笔记开头的 `---` 块）、内联字段（正文里的 `字段:: 值` 写法）、文件自身属性（file.name、file.mtime、file.tasks 等）。Dataview 启动时全库扫描建索引，之后靠事件增量更新，所以大库也不会每次重扫。

查询层有四种模式，难度递进：① DQL，类 SQL 的声明式查询（`TABLE rating FROM #book SORT rating DESC`），写在一个 \`\`\`dataview 代码块里即可；② 内联表达式，`=` 开头嵌在正文里取单个值；③ DataviewJS，一个 \`\`\`dataviewjs 代码块里写完整 JavaScript，拿到 `dv` 对象后随便筛选分组——你会 JS，直接从这档开始用；④ 内联 JS。整个管线是"取页面 → 过滤 where → 分组 groupBy → 排序 sort → 渲染 table/list/taskList"，跟函数式编程的管道一模一样。

## 上手路径

第一步：社区插件市场搜 Dataview 安装启用。第二步：任选一本你的小说笔记，frontmatter 里加 `status: 完结`、`字数: 330000`、`评分: 8`。第三步：新建空白笔记，贴入第一个查询：

````markdown
```dataview
TABLE status, 字数, 评分
FROM #书
SORT 评分 DESC
```
````

（前提是给书目笔记打上 #书 标签。）第四步：升级到 dataviewjs，用 `dv.pages('#书').where(p => p.status != '完结')` 列出未完结清单。第五步：把你手头手工维护的任何一张进度表，用一条查询替代掉。

## 进阶玩法 / 避坑

避坑一：中文键名（如 `字数`）在 DQL 里要写成 `字数` 直引号包裹，DataviewJS 里用 `p["字数"]` 访问，别用点号。避坑二：查询块只读，想改数据得回源笔记，这个心智模型一开始就要建立。进阶方向：读它的源码目录结构——index（索引）、query（查询解析）、data-model（数据模型）分层清晰，是你给 story-ledger 做架构设计时最好的抄作业对象；`dv.view()` 还能把常用查询封装成可复用脚本，做成你的"创作驾驶舱"组件库。

## 横向对比：为什么是这个不是别的

Obsidian 元数据生态三国杀：Dataview、Datacore（它的继任者，还在打磨）、和核心属性 + Bases（官方方案）。Dataview 赢在十年沉淀的稳定性、海量教程和 DQL+JS 双轨——生产环境用它，前瞻布局可以盯 Datacore。而"把 Markdown 当数据库"这个思路本身，无论工具怎么换都值钱。

## 认知红利：这篇能改变你什么

你过去大概把笔记当"文档"，Dataview 的世界观是"每篇笔记都是一行记录"。视角一换，很多事情自动降维：找、统计、汇总不再是"翻"，而是"查"。这也是你做 story-ledger 最该偷走的一个心智模型——先想数据模型，再想界面。

> 冷知识：Dataview 的内联字段 `字段:: 值` 语法被整个社区反向吸收成了"事实标准"，连后来者工具都默认兼容——一个插件定义了一种写笔记的方式。

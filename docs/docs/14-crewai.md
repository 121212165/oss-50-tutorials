---
num: 14
title: crewAI：5.9 万 star 的"角色分工式"多 Agent 框架，把协作写成剧组
repo: crewAIInc/crewAI
category: AI Agent / 编码智能体
audio: 14.mp3
minutes: 6
---

## 它是什么（30 秒版）

crewAI（5.9 万 star，MIT 协议，Python）是目前主流的多 Agent 编排框架里**心智模型最直白**的一个：把任务交给一个"剧组（Crew）"——每个 Agent 有角色（role）、目标（goal）、背景故事（backstory），任务（Task）按流程分配给成员，产出（Output）层层传递。它商业公司化运营，社区活跃、文档商业级，README 上现在就挂着 Trendshift 热度徽章。

## 为什么对你超有帮助

对比第 12、13 篇会更清楚：AutoGen 是"对话编排"，LangGraph 是"状态图编排"，crewAI 是"**角色编排**"——这三种心智模型里，角色制和你每天做的事最同构。你的审稿引擎 v4 本质就是一个剧组：审稿人（挑剧情漏洞）、AI 味检测员（挑腔调问题）、规则检查员（对照规则 v1）、主编（终审拍板）。crewAI 让你用一天时间把这套"编制"真的跑起来：每个角色一段提示词、一个目标，任务链串起来，输出格式声明成 JSON——它内置了任务间上下文传递（上一个任务的 output 自动注入下一个任务的 context），你手工粘来粘去的中间产物传递第一次变成声明式配置。另外它对"输出结构化"的支持（expected_output + Pydantic 模型校验）直接可用在你"评分必须返回规定字段"的场景。学习它的过程中你对"提示词角色化"的手感也会显著变好——backstory 写得好不好，直接决定 Agent 表现，这就是提示词工程的实战课。

## 架构拆解

五个积木：①**Agent**：role/goal/backstory 三元组 + 挂模型（任何 OpenAI 兼容 API，DeepSeek 可用）+ 可选工具；②**Task**：描述、执行者、expected_output（期望输出格式），任务可以串行也可以并行（`process="hierarchical"` 时由一个"经理 Agent"动态分派，`process="sequential"` 按顺序流水线）；③**Crew**：把 Agents 和 Tasks 组装成编队，是执行入口；④**Flow**（较新的能力）：crewAI 自己的结构化编排层，用装饰器写带分支和状态的流程——定位类似 LangGraph 但更轻，当 Crew 的固定流水线不够用时升级到 Flow；⑤**Tools**：标准工具协议，也兼容 MCP。执行链一句话：Crew.kickoff() → 按 process 模式逐个/动态执行 Task → 每个 Task 的产出注入后续 context → 最终聚合成 CrewOutput。

## 上手路径

第一步：`pip install crewai`（建议先建 venv），配好一个兼容模型的 key。第二步：定义你写作系统的四人剧组：AI 味检测员、剧情审稿人、规则检查员、主编，各写一段 backstory（可以直接从你审稿引擎的提示词改写）。第三步：串三个 Task：检测 → 审稿 → 终审汇总，expected_output 要求 JSON。第四步：跑一章稿子，对比它和你现有脚本的产出质量。第五步：把"低分重审"改用 hierarchical 模式让经理 Agent 自动决定要不要打回。

## 进阶玩法 / 避坑

避坑一：crewAI 免费开源部分够用，但官网会引导你上云付费版，个人管线没必要。避坑二：Agent 数量不是越多越好，每加一个角色 token 成本和失控风险都上升，先从两人剧组起步。进阶：把剧组的每轮输出落盘成 JSONL 台账（对齐你的归档习惯），跑一个完整的"审稿剧组 vs 单提示词审稿"对比实验——胜出条件很简单：哪个返工率低用哪个。做这个实验本身，就是你从"用 Agent"到"设计 Agent 系统"的分界线。

## 横向对比：为什么是这个不是别的

同是多 Agent 框架，crewAI 的护城河是"上手曲线"：AutoGen 要设计对话规则，LangGraph 要画图，crewAI 只要写四段人物小传。代价是灵活性封顶——当你的流程出现复杂分支和动态调度时，还是要下沉到 Flow 或换 LangGraph。原型期用 crewAI，生产期按需下沉，是低风险路径。

## 认知红利：这篇能改变你什么

role/goal/backstory 三元组是提示词工程的最佳实践模板：角色定义"我是谁"，目标定义"要什么结果"，背景故事注入"判断标准"。回头看你 vault 里的 36 条提示词，多半只做了后两件事——补上"角色"，同一条提示词的表现会明显变稳。

> 冷知识：crewAI 是巴西开发者 João Moura 的个人项目起家，如今公司化运营——多 Agent 框架这场竞赛里跑出来的，是独立开发者而非大厂，这对你的项目是个信号。

---
num: 12
title: AutoGen：微软多智能体框架的"退役经典"，读它理解 Agent 协作的本质
repo: microsoft/autogen
category: AI Agent / 编码智能体
audio: 12.mp3
minutes: 6
---

## 它是什么（30 秒版）

AutoGen（6.1 万 star）是微软出品的**多智能体**框架：让多个各司其职的 AI Agent（写代码的、审代码的、执行代码的）以对话方式协作完成任务。要划重点的是：README 顶部现在挂着橙色横幅——**进入维护模式**，微软已转向后继项目 Microsoft Agent Framework（MAF）。但这不减少它的学习价值：作为多 Agent 协作这个范式的奠基者，它的概念模型已经被整个行业吸收。

## 为什么对你超有帮助

对你这个"用 Agent 干活、也在做 Agent 周边（agent-quota）"的用户，AutoGen 的价值恰恰是"教材式经典"：它稳定、不再变动，适合系统阅读而不怕追着 API 变更跑。三个收获点：①**对话即编排**的思想——它把多 Agent 协作建模成 Agent 之间的消息传递，谁说话、谁响应、何时终止，全是对话规则的设计，这套心智模型能反哺你使用任何多 Agent 工具（比如你现在用的 subagent）时的"拆任务直觉"：为什么一次给 subagent 的指令要自包含？因为消息传递模型里上下文不共享。②**MCP 集成范本**：README 里就有 Agent 挂 Playwright MCP server 的标准代码——你自己在做 MCP Server（agent-quota），看主流框架怎么消费 MCP 工具，等于从"供给侧"换到"需求侧"审视自己的 MCP 设计。③**教训样本**：一个 6 万 star 的明星项目也会"被后继者取代"，它 README 里那篇迁移指南本身是行业架构演进的一手史料——你做技术选型（比如自研写作管线要不要依赖某个框架）时该有的风险评估心态，这里有现成案例。

## 架构拆解

当前版本（autogen-agentchat）的关键概念只有四个：①**Agent**：最小单元，`AssistantAgent("assistant", model_client=...)` 一行就是一个能对话、能调工具的智能体；②**Team**：多个 Agent 组成的编队，内置几种协作模式——RoundRobinGroupChat（轮流发言）、SelectorGroupChat（由模型选下一个发言者）、Swarm（基于交接 handoff 的流转）、MagenticOneGroupChat（任务规划式）；③**Termination**：终止条件（最多 N 轮、出现某关键词、外部批准），多 Agent 系统最容易"聊到天荒地老烧光 token"，终止条件设计是工程重点——这也是你的 agent-quota"预算硬阻断"思想在框架层的镜像；④**工具与模型客户端**：模型走 OpenAI 兼容接口（你完全可以指向 DeepSeek 或任何兼容 API），工具走标准函数调用或 MCP Workbench。整条链：任务进 → Team 按规则让 Agent 们轮流处理 → 每次响应可调工具 → 满足终止条件出结果。

## 上手路径

第一步：`pip install -U "autogen-agentchat" "autogen-ext[openai]"`（Python 3.10+）。第二步：跑 README 的 Hello World，把 model 换成你能用的兼容模型。第三步：升级到双 Agent：一个"写手"一个"审稿人"跑 RoundRobinGroupChat，让它俩互改一段小说开头——这个实验对你去 AI 味管线有直接启发。第四步：挂一个 MCP server 工具再跑一次。第五步：想无代码体验就装 `autogenstudio` 图形界面。

## 进阶玩法 / 避坑

避坑一：网上一半的 AutoGen 教程讲的是旧版 0.2 API，已经对不上当前代码，认准官方文档 stable 版。避坑二：新项目别再基于 AutoGen 起步，学概念用它、写生产用 MAF 或 LangGraph。进阶：把"写手/审稿人"双 Agent 实验扩展成你审稿引擎 v4 的框架级原型，用终止条件控制审稿轮数和 token 预算——概念你全都见过，就差拼起来。

## 横向对比：为什么是这个不是别的

多 Agent 框架三强的本质区别：AutoGen 对话流、LangGraph 状态图、crewAI 角色制。AutoGen 虽进维护模式，但"对话即编排"的心智模型被所有后来者继承——学它是学概念原型，成本低、过期慢，教科书的价值不因绝版而消失。

## 认知红利：这篇能改变你什么

终止条件（Termination）是多 Agent 系统里最容易被忽视的设计。任何协作系统——Agent 剧组、审稿流水线、甚至人与人——没有明确的"何时停"，就会在无效循环里烧资源。你的 agent-quota 做的"预算硬阻断"，本质上就是给系统装 Termination。

> 冷知识：微软把 AutoGen 的后继者命名为 Microsoft Agent Framework，并公开迁移指南——巨头也会"项目送终"，看到维护模式横幅就该停止投入新项目，这是 README 教给你的选型纪律。

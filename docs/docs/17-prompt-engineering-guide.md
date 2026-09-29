---
num: 17
title: Prompt-Engineering-Guide：把"会写提示词"变成一门有教材的手艺
repo: dair-ai/Prompt-Engineering-Guide
category: AI 写作 / 中文文本处理
audio: 17.mp3
minutes: 8
---

## 它是什么（30 秒版）

dair-ai/Prompt-Engineering-Guide 是目前最系统的开源提示词工程知识库，已有数万星。它不是零散 prompt 集合，而是一套带目录的"教材"：从零样本/少样本、思维链（CoT）、ReAct，到 RAG、对抗攻击与防御，每章都有讲解、论文链接和可运行的 Colab 笔记本，支持在线阅读（promptingguide.ai）。你可以把它当成提示词工程的"科班课程大纲"。

## 为什么对你超有帮助（结合你的具体项目说）

你的 novel-ai-writing-system 本质上就是一套"提示词工厂"：审稿引擎 v4、QS-8 评分、去 AI 味管线、作者指纹，每一环的核心资产都是 prompt。这本书直接补你三块短板：

1. **审稿引擎 v4 的可复现性**。QS-8 八个维度要打分稳定，最怕模型随口打分。指南里"结构化输出 + few-shot + 思维链"几章，正好教你怎么让评分 prompt 输出稳定的 JSON：先给两个标准打分范例，再要求模型逐维度给证据再给分，方差会显著下降。
2. **去 AI 味管线的理论依据**。你目前大概靠经验归纳"AI 味特征"（排比堆砌、破折号滥用、"她知道……"句式）。指南里关于 prompting vs fine-tuning 边界的章节，能帮你判断哪些去味规则适合留在 prompt 层（便宜、可迭代），哪些值得沉淀成微调数据集。
3. **prompt-vault 的分类学**。你的提示词沉淀库需要一个组织骨架，这份指南的章节结构（技巧 → 应用 → 风险 → 工具）就是现成的三级目录，比你自己拍脑袋分类靠谱。

## 架构拆解（核心模块 + 数据流）

仓库结构极简单，几乎全是 Markdown + Notebook：

- **introduction/**：什么是提示工程、LLM 基本设置（temperature、top-p 怎么影响写作的"发散度"——低温度适合审稿打分，高温度适合情节头脑风暴）。
- **techniques/**：核心技术，按"从简到繁"排列——zero-shot（直接下指令）→ few-shot（给例子）→ chain-of-thought（"一步一步想"）→ self-consistency（多次采样取多数）→ ReAct（推理与工具调用交替）。每节都有 prompt 示例，能直接抄结构。
- **applications/**：把技巧落到微调、RAG、对话等场景。审稿引擎以后要引用你的"AI 味规则库"，就是最小 RAG。
- **risks/**：对抗攻击（提示注入）、幻觉、偏见。你会意识到：去 AI 味和"防提示注入"是同类问题——都是在对抗模型输出分布。
- **papers/**：每个技巧对应原论文链接，深挖时从这里走。

数据流就是"读文章 → 跑配套 notebook → 改成自己的 prompt"。

## 上手路径（第一步做什么，命令级）

不用 clone 也能读，但建议 clone 一份做笔记：

```bash
git clone https://github.com/dair-ai/Prompt-Engineering-Guide.git
cd Prompt-Engineering-Guide
# 直接用编辑器打开 introduction/ 下的 Markdown 阅读即可
```

第一步：只读 `introduction/` 和 `techniques/zero_shot.md`、`techniques/few_shot.md` 三篇（约 40 分钟）。第二步：打开任一 techniques 下的 Colab 笔记本，把示例 prompt 换成你的审稿引擎 v4 的一个维度（比如"逻辑自洽性"），对比有无 few-shot 示例时打分的稳定性。第三步：把学到的技巧逐条记进 prompt-vault，每条附"在哪个模块验证过"。

## 进阶玩法 / 避坑

- **进阶**：读 self-consistency 一章后，给 QS-8 打分做成"三次采样取中位数"，成本涨三倍但评分更稳；给去 AI 味管线加"反例 few-shot"——喂两段文字，一段标"AI 味重"一段标"人味"，比只说"自然一点"有效得多。
- **避坑**：① 不要把整本读完才动手，技巧篇的 30% 就够覆盖你 90% 的需求；② 论文链接跳的 arXiv 页面有新版旧版，引用时注意版本号；③ 网站有社区翻译，中文版个别术语（如 temperature 译"温度"）保留英文搜索更容易；④ 教程里的 prompt 多针对老模型写的，直接抄效果可能差，抄"结构"而不是抄"原文"。

## 横向对比：为什么是这个不是别的

提示词知识库的三个层级： awesome-chatgpt-prompts 是"句料库"（拿来即用）、你的 prompt-vault 是"私房拳谱"（从实战归纳）、Prompt-Engineering-Guide 是"教材"（理论体系）。三者是谱系不是竞品——缺哪层补哪层，你缺的是最上层。

## 认知红利：这篇能改变你什么

指南会教给你"把提示词当实验"的心态：改一个变量、跑多次、看方差——这和你做 Jev 评测是同一种科学方法。写提示词的巅峰状态不是"灵感"，而是"控制变量"。

> 冷知识：这个项目 2023 年 2 月上过 Hacker News 第一名，比"提示词工程"成为职业词还早——它自己就是这门学科编年史的活化石。

# OSS-50 项目清单（面向用户 GitHub 画像定制）

用户画像：女频网文 AI 写作系统作者、Obsidian 插件开发者（8 个自研插件）、B站扫榜/浏览器扩展作者、
AI Agent 工具链用户（agent-quota/dsh）、学习类应用开发者（FSRS/词源/中医口诀）、归档控、Python+TypeScript 主力、正在学 Git/Vercel/部署。

教程统一格式（每篇 1300-1800 字，零基础可读，Markdown）：

```
---
num: NN
title: <项目名：一句话价值>
repo: <owner/name>
category: <分类名>
audio: <NN>.mp3
minutes: <预估阅读分钟数>
---

## 它是什么（30 秒版）
## 为什么对你超有帮助（结合你的具体项目说）
## 架构拆解（核心模块 + 数据流，用零基础语言讲）
## 上手路径（第一步做什么，命令级）
## 进阶玩法 / 避坑
```

## 分组与项目

### A. Obsidian 插件开发（你的 8 个插件的老师）
1. obsidianmd/obsidian-sample-plugin — 官方插件模板，你所有插件的起点
2. blacksmithgu/obsidian-dataview — 元数据查询王者，学它怎么解析 Markdown
3. SilentVoid13/Templater — 模板引擎，学它的命令注册与用户配置
4. Vinzent03/obsidian-git — 你的自动备份方案，学 Git 自动化
5. zsviczian/obsidian-excalidraw-plugin — 最大最复杂的插件，学架构组织
6. mgmeyers/obsidian-kanban — 看板，学 View 视图类插件怎么写

### B. 浏览器扩展 / 油猴（B站扫榜插件进阶）
7. violentmonkey/violentmonkey — 开源油猴，学 userscript 运行时
8. wxt-dev/wxt — 现代扩展框架，比手写 MV3 舒服十倍
9. PlasmoHQ/plasmo — React 写扩展的框架
10. crxjs/vite-plugin — Vite 打包扩展，接入你熟悉的工具链

### C. AI Agent / 编码智能体（agent-quota、dsh 生态）
11. All-Hands-AI/OpenHands — 开源全自动编码 Agent 全景
12. microsoft/autogen — 多智能体协作框架
13. langchain-ai/langgraph — 状态图编排 Agent 的标准答案
14. crewAIInc/crewAI — 角色分工式多 Agent
15. geekan/MetaGPT — 软件公司式 Agent 编排
16. anthropics/skills — 官方 Agent Skills 规范与示例

### D. AI 写作 / 中文文本处理（novel-ai-writing-system 军火库）
17. dair-ai/Prompt-Engineering-Guide — 提示词工程系统知识库
18. f/awesome-chatgpt-prompts — 经典提示词集合，学分类组织
19. openai/tiktoken — token 计数，字数预算管线的底层
20. fxsjy/jieba — 中文分词，AI 味检测的基础件
21. chinese-poetry/chinese-poetry — 50 万条中文语料，作者指纹训练素材
22. python-openxml/python-docx — Word 导出，交稿管线的最后一公里

### E. TTS / 音频 / 多媒体（本教程站就是它做的）
23. rany2/edge-tts — 免费微软 TTS，本站音频引擎
24. RVC-Boss/GPT-SoVITS — 少样本声音克隆，做你的"作者声音"
25. fishaudio/fish-speech — 开源 TTS 新星
26. 2noise/ChatTTS — 对话感 TTS
27. yt-dlp/yt-dlp — 视频音频下载，素材采集

### F. Web 开发 / 部署（正在学的方向）
28. vercel/next.js — 你的 sleepquiz/portfolio 用的框架
29. vitejs/vite — 静界在用的构建器
30. tailwindlabs/tailwindcss — 快速做教程站 UI
31. expressjs/express — 后端最小核心
32. tiangolo/fastapi — 你的动物园导览在用
33. vercel/ai — AI SDK，给 Web 应用接模型

### G. Python 工具链 / 自动化
34. psf/requests — HTTP 请求第一课
35. encode/httpx — 异步版 requests
36. microsoft/playwright — 浏览器自动化，扫榜的终极形态
37. Textualize/rich — 终端美化，你的 CLI 工具颜值担当
38. pydantic/pydantic — 数据校验，配置不炸
39. pandas-dev/pandas — 表格数据处理

### H. 学习科学 / 算法（FSRS/词源/方诀游戏）
40. open-spaced-repetition/fsrs4anki — 你 formula-challenge 用的算法本体
41. ankitects/anki — 全平台记忆卡，学同步架构
42. krahets/hello-algo — 动画图解数据结构与算法
43. ossu/computer-science — 免费计算机本科课程体系
44. freeCodeCamp/freeCodeCamp — 最大的免费编程学习平台

### I. 跨平台 / 鸿蒙 / 移动（花语助手方向）
45. flutter/flutter — 一套代码全平台
46. facebook/react-native — React 写原生 App
47. electron/electron — 桌面应用，把工具做成产品

### J. 归档 / 图表 / 效率（归档控的浪漫）
48. restic/restic — 加密增量备份，归档管线终局
49. mermaid-js/mermaid — 代码画图，写文档必备
50. excalidraw/excalidraw — 手绘白板，拆解画架构图神器

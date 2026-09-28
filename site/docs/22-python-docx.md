---
num: 22
title: python-docx：纯 Python 读写 Word 文档，交稿管线最后一公里
repo: python-openxml/python-docx
category: AI 写作 / 中文文本处理
audio: 22.mp3
minutes: 8
---

## 它是什么（30 秒版）

python-docx 是操作 Microsoft Word（.docx）文档的官方级 Python 库，属于 python-openxml 组织。它能创建和修改文档：段落、标题、样式、加粗斜体、表格、图片都能读写。.docx 本质是 zip 包里塞了一堆 XML，python-docx 把这层封装消化掉，让你用 `doc.add_heading()` 这样的友好 API 操作 Word。`pip install python-docx` 即装即用，无需安装 Word 本体。

## 为什么对你超有帮助（结合你的具体项目说）

novel-ai-writing-system 管线的起点和终点都是文本文件，但**网文作者的交稿世界是 Word 文档**：编辑收稿、合同附件、全本归档，十有八九要 .docx。python-docx 补上你管线的最后一公里：

1. **导出模块从零到一**。AI 改写完的章节目前大概率是 Markdown。写一个 50 行的导出器：章标题生成 Heading 1、正文两字缩进，一键产出符合投稿规范的 .docx——这是编辑对你系统的"第一印象"。
2. **审稿引擎 v4 的输入适配**。作者的真实存稿常是带批注的 Word。python-docx 能读段落文本，做成 `load_docx()` 适配层后，审稿管线才能吃进真实数据。
3. **μ̂ 字数统计的真实口径**。网文行业按"字符数（含标点）"计费，接近 Word 状态栏口径。导出后用 python-docx 读回文档统计段落字数，校准 μ̂ 与编辑那边看到的数字一致，避免"字数纠纷"。
4. **去 AI 味的交付形态**。改写稿以"原文/改写"双栏表格的 Word 交付，作者核对效率大幅提升——表格能力正好用上。

## 架构拆解（核心模块 + 数据流）

- **文档对象模型**：核心层次是 `Document → 段落(Paragraph) → 文本块(Run)`。样式（标题、正文、缩进）挂在段落级；段落内的不同格式（比如中间几个字加粗）拆成多个 Run。理解"样式在段落、加粗在 Run"是入门关键。
- **样式体系**：文档自带 named styles（Normal、Heading 1..9 等）。`add_heading('第1章', level=1)` 就是套用 Heading 1。统一改中文字体时要注意额外设置 East Asian 字体属性（rFonts 的 eastAsia），这是最常见的坑。
- **表格与图片**：`add_table(rows, cols)` 逐 cell 填充；`add_picture()` 插图。对写作系统来说表格主要用于双栏对照。
- **底层机制**：python-docx 基于 .docx 的 OOXML 结构，只暴露 XML 已定义的能力——页眉页脚、脚注支持有限，自动目录等模板级操作要绕道。
- **数据流**：Markdown 章节 → 解析 → Document 构建 → save('.docx')；反向流则是 load → 遍历 paragraphs → 拼回纯文本进管线。

## 上手路径（第一步做什么，命令级）

```bash
pip install python-docx
python -c "
from docx import Document
from docx.shared import Pt
doc = Document()
doc.add_heading('第一章 雪夜', level=1)
p = doc.add_paragraph('她推开门，雪落满了肩头。')
p.paragraph_format.first_line_indent = Pt(24)
doc.save('test.docx')
"
```

第一步：跑通上面 5 行，用 Word/WPS 打开确认样式。第二步：写 `md2docx.py`，把一章 Markdown（`#` 标题 + 正文 + 对话）转成带缩进和标题层级的 Word。第三步：反向写 `docx2md.py`，读取你的旧存稿转成 Markdown 进管线，打通"读 Word → 审稿 → 写 Word"闭环。

## 进阶玩法 / 避坑

- **进阶**：用模板法做"投稿规范模板"——字体、页边距全在模板 .docx 里调好，代码只 `Document('模板.docx')` 后填内容，比代码调格式省十倍；用 add_table 生成"原文/AI 改写/AI 味评分"三栏校对稿；遍历 paragraphs 统计"字符数（计空格）"，对齐编辑口径。
- **避坑**：① 只支持 .docx，不支持老 .doc——先用 Word 另存或用 LibreOffice 转换；② 中文字体必须同时设 `font.name` 和 eastAsia 属性，只设前者中文会显示成默认字体；③ 复杂 Word（嵌套表格、修订记录）解析易丢信息，读带批注的文档建议先清稿；④ 无法生成自动目录，交稿前可能仍需手动一步；⑤ Word 的软换行（Shift+Enter）是 Run 内的 `<w:br/>`，统计时别漏。

## 横向对比：为什么是这个不是别的

Word 处理三路线：python-docx（纯 Python、稳、只管 docx）、docxtpl（模板占位符流，套模板快）、pandoc（万能转换、样式控制粗）。交稿场景的最优组合：模板用 docxtpl 填空，正文与结构用 python-docx 精修，全格式转换用 pandoc 兜底——三条路各司其职。

## 认知红利：这篇能改变你什么

"管线的终点是编辑的 Word 文档"这件事值得所有工具开发者深思：你的产出形态不由你的技术栈决定，由下游的接收方决定。写作系统的最后一公里不是代码问题，是"对齐行业口径"的问题——字数统计口径就是最典型的例子。

> 冷知识：.docx 本质是一个 zip 包——把后缀改成 zip 解开，里面全是 XML。理解这一点，你就理解了为什么 python-docx 能"不装 Word 也能操作 Word"。

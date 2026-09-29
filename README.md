# 开源军火库 50 课

50 个开源项目的零基础拆解教程，每篇配 MP3 音频版。

**在线站点：<https://121212165.github.io/oss-50-tutorials/>**

## 每篇讲什么

统一 7 段结构，可核对、可跳过：

| 段落 | 回答的问题 |
|---|---|
| 它是什么（30 秒版） | 一句话能不能说清这个项目的价值 |
| 为什么对你超有帮助 | 它替你解决哪一类具体麻烦 |
| 架构拆解 | 核心模块、数据流、为什么这样分层 |
| 上手路径 | 命令级的第一步到第五步 |
| 进阶玩法 / 避坑 | 会踩的坑和它的解法 |
| 横向对比 | 同一条路上为什么选它不选别的 |
| 认知红利 | 读完能迁移走的思维模型 |

覆盖方向：Obsidian 插件开发、浏览器扩展与油猴、AI Agent、AI 写作与中文文本处理、TTS 与多媒体、Web 开发与部署、Python 工具链、学习科学与算法、跨平台与移动、归档与图表。

## 目录结构

```
docs/
  index.html     # 站点（GitHub Pages 从 /docs 发布，纯静态无构建）
  data.json      # 目录索引，由 scripts/build_data.py 生成，不要手改
  docs/*.md      # 50 篇教程原文，可离线读
  audio/NN.mp3   # 50 条音频版
scripts/
  build_data.py      # 从 Markdown frontmatter + 实测字数/音频时长生成 data.json
  check_upstream.py  # 核对 50 个上游仓库：改名、归档、停更、star 标称漂移
make_audio.py    # Markdown -> MP3（edge-tts，中文女声，+12% 语速）
manifest.md      # 50 个项目的选题清单与分组
```

## 站点功能

- 搜索（标题/仓库/方向）、按方向筛选、未读筛选
- 深浅色主题，跟随 `localStorage` 记忆
- 「标记为已读」+ 顶栏 `已读 N/50` 进度，只存在你本机浏览器，不上传
- 文章页右侧小节目录（≥1100px）、顶部阅读进度条、上一课/下一课
- 音频倍速 0.75×–1.75× 与断点续听（按篇记忆进度）
- 键盘：`/` 聚焦搜索、`←` `→` 翻页、`Esc` 返回目录
- 320px 宽无横向溢出，`prefers-reduced-motion` 与打印样式

## 本地跑

Pages 站点用 `fetch()` 取 `data.json`，直接双击 `index.html`（`file://`）会被浏览器拦掉，需要一个本地 HTTP：

```bash
cd docs && python -m http.server 8016
# 打开 http://127.0.0.1:8016
```

只读某一篇不用跑站点：`docs/docs/07-violentmonkey.md`。

## 重新生成

```bash
py -3.12 -m pip install edge-tts
py make_audio.py 07            # 补某几篇音频
py scripts/build_data.py       # 重算 data.json（字数、音频时长、文件名）
py scripts/check_upstream.py   # 核对上游仓库（有 GITHUB_TOKEN 就不怕限流）
```

站点上的「字数」与「音频分钟」不是手填的：字数 = 中文字符 + 英文词元，去掉代码块与 Markdown 标记；音频时长由 `build_data.py` 逐帧解析 MP3 头算出。这两项与人工标称值曾经偏差近 2 倍，所以现在由脚本产出、CI 校验。

## CI

`.github/workflows/ci.yml` 每次推送跑三件事：`data.json` 与文件实际内容一致（否则失败）、50 个上游仓库没有改名或消失（失败）、归档/停更/star 漂移（告警）。

## 许可

- 站点代码（`index.html`、`scripts/`、`make_audio.py`）：MIT，见 [LICENSE](LICENSE)
- 教程文字：CC-BY-4.0 —— 转载请注明来源并保留此链接
- 50 个项目自身的许可证见各项目仓库；清单里 Templater / obsidian-excalidraw-plugin / ChatTTS 是 **AGPL-3.0**，闭源商用请先读它们的条款

## 已知问题

- 行文是「第二人称定制版」（为你现有的项目选型），对无关读者会显得突兀；通用化改写在 Issue 里跟踪
- 音频与正文存在轻微不同步：正文改动后只有重跑 `make_audio.py` 才会更新对应 MP3
- 50 条 MP3（约 84 MB）直接进 Git，克隆偏重；量级再翻倍时应转 Git LFS 或 Releases
- 无 JS 或搜索引擎抓不到正文（运行时渲染 Markdown）；要 SEO 就得构建期预渲染成 50 个静态 HTML

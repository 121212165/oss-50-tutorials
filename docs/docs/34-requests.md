---
num: 34
title: requests：Python HTTP 请求第一课，你所有采集脚本的地基
repo: psf/requests
category: Python 工具链 / 自动化
audio: 34.mp3
minutes: 5
---

## 它是什么（30 秒版）

requests 是 Python 世界最著名的 HTTP 客户端库，官方口号 "HTTP for Humans"（给人类用的 HTTP）：`requests.get(url)` 一行发请求，返回的 response 对象直接给你 .status_code、.json()、.text。它不是最快的，也不是最新的，但它是**几乎所有 Python 教程、文档、接口示例的默认写法**——学它不是为了酷，是为了读懂全世界。

## 为什么对你超有帮助

你的 Python 脚本群（bili-daily、multi-account-checkin、x-collector、扫榜）全靠 HTTP 请求吃饭，requests 是这个领域的"普通话"。三个层面的收益：①**把"能跑"变成"懂跑"**：你可能复制过很多 requests 片段，但这篇要你吃透四个基本件——headers（你"纯匿名"的核心手段：自定义 User-Agent、控制 Cookie 带不带）、params（URL 查询参数）、timeout（没有它脚本会无限挂起，这是新手脚本"卡死"的第一原因）、Session 对象（复用连接、跨请求保持状态，多账号签到这种"登录一次操作多次"场景的正确姿势）；②**对照升级**：懂了 requests 再看第 35 篇 httpx（异步版）和第 36 篇 Playwright（浏览器级），你就有了"请求三件套"的完整决策树——接口级请求能解决就用 requests，要并发用 httpx，页面是 JS 渲染的才上 Playwright；③**读得懂别人的代码**：搜任何 Python 采集方案，示例代码 90% 用 requests，这是你扫榜拆解时读他人实现的基础设施。

## 架构拆解

一次 get() 背后发生四件事：①**构造 Request**：把 URL、method、headers、params、body 组装成请求对象；②**经 Session 发送**：Session 管理连接池（HTTP keep-alive 复用 TCP 连接，批量请求快数倍）和 cookie jar；③**urllib3 执行传输**：requests 底层委托给 urllib3 处理真正的 socket、TLS、重试——requests 是"人体工学层"，不是"传输层"；④**构造 Response**：状态码、响应头、content（字节）/text（按编码解码的字符串）、json() 全部封装好。异常体系也重要：raise_for_status() 把 4xx/5xx 变成 HTTPError 异常、ConnectionError/Timeout 独立成类——生产脚本必须 try/except 这几类，再配 Retry 策略（urllib3 的 Retry 挂进 HTTPAdapter），这才算"健壮的采集脚本"。

## 上手路径

第一步：`pip install requests`。第二步：请求一个公开 API（如 GitHub API），打印状态码和 JSON。第三步：加 headers 伪装 User-Agent 再请求一次，对比响应差异——理解"服务器怎么区分你是什么客户端"。第四步：用 Session 连续请求三个页面，体会连接复用。第五步：给你的 bili-daily 补上 timeout + raise_for_status + 三类异常捕获 + 失败重试，重构一次。

## 进阶玩法 / 避坑

避坑一：永不裸调 requests.get——不设 timeout 的脚本等于定时炸弹。避坑二：response.text 的编码猜测偶尔翻车，中文乱码时手动 response.encoding = 'utf-8'。避坑三：别在循环里新建 Session，连不上时先检查代理环境变量（requests 会读 HTTP_PROXY）。进阶：把"请求 → 解析 → 落 JSONL 台账"封装成你的标准采集模板，配上 rich（第 37 篇）的进度条——工具链化之后，你所有采集脚本就是同一套骨架的不同参数，维护成本指数下降。

## 横向对比：为什么是这个不是别的

Python HTTP 客户端家族：requests（人读第一、同步）、httpx（异步+HTTP2、现代）、aiohttp（老牌异步、API 更硬）、urllib3（底层引擎，requests 的地基）。学 requests 不是因为它最好，而是因为它最"通用语文"——所有教程、SDK 文档、示例代码都默认你认识它。

## 认知红利：这篇能改变你什么

"requests 的两个参数，headers 和 timeout，决定了脚本的生死"——headers 决定服务器怎么看你，timeout 决定你出不出事故。新手与老手的差距往往不在框架，而在这些"第一屏参数"的肌肉记忆。

> 冷知识：requests 的 slogan 是 "HTTP for Humans"——它开创了"给人类的 API"这种叙事，后来的 httpx、edge-tts 全在沿用这个人本主义的 marketing 传统。

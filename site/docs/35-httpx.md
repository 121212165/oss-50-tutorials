---
num: 35
title: httpx：1.5 万 star 的"下一代" HTTP 客户端，requests 的异步继任者
repo: encode/httpx
category: Python 工具链 / 自动化
audio: 35.mp3
minutes: 6
---

## 它是什么（30 秒版）

httpx（1.5 万 star，encode 组织出品——就是 Starlette/uvicorn 背后那家）自称"next-generation HTTP client"：API 与 requests 高度兼容，同时补上了三块 requests 没有的能力——**原生异步**（async/await）、**HTTP/2 支持**、**内置命令行客户端**。一句话定位：写惯 requests 的人零成本升级，还白拿异步。

## 为什么对你超有帮助

你的采集脚本即将遇到两堵墙，httpx 是标准答案：①**并发墙**：bili-daily 或多账号签到要同时打几十个请求，requests 的路线是线程池（能跑但线程切换和连接管理都别扭），httpx 的 `async with httpx.AsyncClient() as client: await asyncio.gather(*[client.get(u) for u in urls])` 十行原生并发——IO 密集的采集场景 asyncio 是正解；②**工程化墙**：你正在给管线做服务化（FastAPI 第 32 篇就是异步优先），async def 接口里必须用异步客户端（同步的 requests 会卡死事件循环），httpx 就是 FastAPI 官方示例里的搭档；③**测试利器**：httpx 自带 MockTransport，能把真实 HTTP 调用替换成预设响应——你的扫榜逻辑从此可以不联网做单元测试，这在"接口经常变"的采集领域是工程质量的分水岭。迁移成本几乎为零：`import httpx as requests` 大部分代码直接能跑（当然别真这么干）。

## 架构拆解

与 requests 的架构对照着看：①**API 双轨**：`httpx.get()` 同步快写，`httpx.AsyncClient` 异步正式用法——同一个库两种模式，语义一致；②**Client 是核心**：连接池、cookie、默认 headers、超时策略全部挂在 Client 上，官方推荐永远显式用 Client 而不是模块级函数（复用连接、可控配置）；③**HTTP/2**：`httpx.Client(http2=True)`（装 httpx[http2]），对支持的服务端多路复用同一条连接——高频请求同一站点时延迟更低，也更容易"长得像现代浏览器"（现代浏览器都走 h2）；④**扩展点**：Event hooks（请求前后回调，统一打日志/统计）、Auth 流（自定义鉴权）、**MockTransport**（测试替换层）——这三件套构成它的工程化骨架。数据流：Client 配置 → 请求组装 → 传输适配（httpcore 层）→ Response（同步/异步两种消费方式）。

## 上手路径

第一步：`pip install "httpx[http2]"`。第二步：把 requests 的 GET 示例用 httpx 同步 API 复写一遍，确认"无缝"。第三步：写异步并发版：AsyncClient + asyncio.gather 抓 20 个 URL，用 time 对比串行版耗时——这一步你会记住 asyncio 的价值。第四步：给并发版加 semaphore 限速（每秒 N 个），采集的礼仪。第五步：用 MockTransport 给你的解析函数写两个单测（正常响应/接口报错）。

## 进阶玩法 / 避坑

避坑一：async 里混用同步 IO 是事故之王——httpx 的异步 Client 和 requests/文件同步读不要出现在同一个 async def 里。避坑二：并发不限速会触发风控甚至封 IP，gather + Semaphore + 重试退避是采集三件套。避坑三：httpx 默认不跟随部分重定向场景与 requests 有细微差异，迁移后跑回归。进阶：把你的采集模板升级成"双引擎"——小脚本用 requests 直白，常驻服务与并发任务用 httpx 异步，选择标准写进你 prompt-vault 的决策框架里。

## 横向对比：为什么是这个不是别的

异步 HTTP 双雄：httpx（requests 血统、迁移顺滑）和 aiohttp（更老、更快、API 更底层）。迁移成本和可读性优先选 httpx；极致吞吐才值得学 aiohttp 的另一套 API。你的场景（几十并发的采集）远没到 aiohttp 的性能边界，可读性赢。

## 认知红利：这篇能改变你什么

asyncio 的价值要在 IO 密集场景才能体会：一次 await 让出控制权，CPU 不空转。理解这个之后，你所有"for 循环里逐个请求"的代码都会自动被标记为"待优化项"——并发意识，是采集类工具的性能天花板。

> 冷知识：httpx 的 logo 是一只蝴蝶（HTTPX 的 X 挥出来的）——Python 库圈的审美传统：再硬核的库也要有一只吉祥物。

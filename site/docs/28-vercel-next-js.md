---
num: 28
title: Next.js：让你 sleepquiz 和 portfolio 直接上线的全栈框架
repo: vercel/next.js
category: Web 开发 / 部署
audio: 28.mp3
minutes: 8
---

## 它是什么（30 秒版）

Next.js 是 Vercel 公司出品的 React 全栈框架。普通 React 项目只负责"页面长什么样"，服务器和打包这些脏活要自己搭；Next.js 把路由、打包、服务端渲染、接口（API 路由）、部署全部打包成一套约定。你写的 sleepquiz 和 portfolio-site 就是基于它——所以这篇不是"介绍一个新工具"，而是把你每天都在用的东西拆开看明白。

GitHub 上的 vercel/next.js 是前端领域星标最多的项目之一，文档（nextjs.org/docs）有官方中文版，质量极高。

## 为什么对你超有帮助（结合你的具体项目说）

你正在学部署，这正好命中 Next.js 最强的一点：它是 Vercel 的亲儿子，`npm i -g vercel` 之后在项目目录敲一个 `vercel`，几十秒后你就得到一个 https 开头的线上网址。不需要买服务器、不需要配 Nginx、不需要懂 HTTPS 证书。对"代码能跑但不知道怎么让别人访问到"这个阶段的人来说，这是最短路径。

具体到你的项目：

- **sleepquiz**：这种"答几道题出结果"的页面，最适合 Next.js 的静态生成（SSG）——构建时就把页面算好，访客打开几乎是秒开，Vercel 免费额度完全够用。
- **portfolio-site**：个人作品集最怕慢和丑链接。Next.js 的文件路由让你一个文件夹一个页面，`app/about/page.tsx` 自动就是 `/about`，URL 干净，面试官看着舒服。
- 你后面想给写作系统做个 Web 界面时，Next.js 的 API Routes 能让你前端后端写在同一个项目里，不用再开一个 Express 服务。

## 架构拆解（核心模块 + 数据流）

零基础视角下，Next.js 只有四个概念要懂：

1. **App Router（app/ 目录）**：新版本的核心。文件夹就是路由——`app/page.tsx` 是首页，`app/quiz/page.tsx` 是 `/quiz` 页。文件里写的就是 React 组件，你已有的 React 知识直接复用。
2. **服务端组件 vs 客户端组件**：默认写的组件在服务器上渲染好再发给浏览器（快、利于 SEO）；文件顶部加一行 `"use client"`，它就变回你熟悉的普通 React 组件（可以有按钮点击、useState）。新手最容易懵的就是这一行，记住口诀："要交互就 use client"。
3. **API 路由（route.ts）**：在 `app/api/hello/route.ts` 里导出一个函数，就得到了 `/api/hello` 接口。数据流是：浏览器页面 → fetch 自己项目的 /api/xxx → 你在里面调数据库或调大模型 API → 返回 JSON。
4. **渲染时机**：构建时算好叫 SSG（适合 sleepquiz），每次请求时算叫 SSR（适合带用户数据的天），两者可以按页面混用。

## 上手路径（第一步做什么）

不用新建项目，直接拿 portfolio-site 练：

```bash
cd portfolio-site
npm run dev        # 本地开发，localhost:3000
```

然后试三个动作：① 在 `app/` 下新建一个文件夹加 `page.tsx`，刷新浏览器看新页面自动出现；② 建 `app/api/health/route.ts`，导出一个返回 `{ ok: true }` 的 GET 函数，浏览器访问 `/api/health` 验证；③ 部署：

```bash
npm i -g vercel
vercel             # 首次会问几个问题，一路回车
```

完成后终端会打印线上地址，发给朋友试试。以后每次 `git push`（如果连了 GitHub），Vercel 会自动重新部署——这就是"持续部署"，你正在学的部署到此闭环。

## 进阶玩法 / 避坑

- **避坑：环境变量前缀**。浏览器能看到的变量必须以 `NEXT_PUBLIC_` 开头；API 密钥绝不能加这个前缀，否则会被打包进前端代码，等于公开。
- **避坑：别在服务端组件里写 onClick**。会报错，加 `"use client"` 即可。
- **进阶**：`next/image` 自动压缩图片，portfolio 换上它加载速度肉眼可见变快；`revalidate` 控制页面多久重新生成一次。
- **进阶**：读官方的 "Learn" 交互教程（nextjs.org/learn），免费、一步步带你做 dashboard 项目，比任何二手教程都准。

## 横向对比：为什么是这个不是别的

React 全栈框架之争：Next.js（生态最大、Vercel 加持、约定多）、Remix/React Router v7（Web 标准派）、TanStack Start（新锐）。对你的现实建议：继续用 Next——不是因为理论最优，而是因为它的文档、教程、AI 训练语料和 Vercel 部署路径都是最多的，学错成本最低的就是最主流的。

## 认知红利：这篇能改变你什么

SSG/SSR/ISR 的选择本质是"内容新鲜度与速度的定价"——这个框架会训练你以"渲染时机"思考 Web：内容什么时候算好、算好了活多久。用这个视角看你的教程站（纯 SSG）、扫榜页（ISR 更合适），技术选型就从感觉题变成了算术题。

> 冷知识：Next.js 的 App Router 让"文件夹即路由"——URL 结构从此由目录结构决定，你的网站架构和文件架构合二为一。

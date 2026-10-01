# 中英互译（DeepL 版）

仿 DeepL 的双栏实时中英互译网页：自动检测语言、550ms 防抖实时翻译、明亮/暗黑主题、额度条。

## 架构

- `index.html` — 纯静态前端（无构建步骤）
- `api/translate.py` — Vercel Python Serverless Function，代理 `POST /v2/translate`
- `api/usage.py` — Vercel Python Serverless Function，代理 `GET /v2/usage`

浏览器不能直调 DeepL（DeepL 接口不返回 CORS 头），所以翻译请求走同源的 `/api/*` 由函数转发。
API key 由使用者在页面顶部输入，只保存在**自己浏览器**的 localStorage，每次请求随请求转发，
服务端不做任何持久化——**不要把 key 提交进仓库**。

## 部署（Vercel，免费）

1. 把本目录所有文件 push 到 GitHub 仓库（public/private 均可）。
2. 打开 [vercel.com](https://vercel.com) → Add New → Project → Import 你的仓库。
3. 保持默认配置，直接点 **Deploy**（无需环境变量、无需构建命令）。
4. 打开分配到的 `https://xxx.vercel.app`，在页面顶部粘贴 DeepL API key 并保存，即可使用。

## 本地开发

```bash
# 任选其一
npx vercel dev
```

## 费用

DeepL API Free：每月 50 万字符免费额度，额度条在页面上实时显示。
Vercel Hobby：个人项目的流量和函数调用额度足够日常使用。

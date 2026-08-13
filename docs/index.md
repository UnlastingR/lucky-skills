---
layout: home

hero:
  name: Lucky Skills
  text: Lucky v3 OpenToken API 与安全自动化
  tagline: 从前端静态分析、脱敏运行时验证到 OpenAPI、CLI 和 Agent Skill，一套可复现的 Lucky v3 管理接口文档。
  actions:
    - theme: brand
      text: 快速开始
      link: /quickstart
    - theme: alt
      text: 查看 API 路由
      link: /generated/api-routes
    - theme: alt
      text: GitHub 仓库
      link: https://github.com/UnlastingR/lucky-skills

features:
  - title: 安全优先
    details: OpenToken 视为管理员密钥；客户端默认只读，写操作需要显式授权、风险分级与精确确认。
  - title: 可验证的接口目录
    details: 静态快照与版本、SHA-256 精确绑定的运行时证据合并，避免把 HTTP 方法简单等同于风险等级。
  - title: Agent Skill
    details: 内置 Lucky Skill，可由 Codex / DevSpace 自动发现，并统一调用仓库内的受保护 OpenToken 客户端。
  - title: OpenAPI 3.1
    details: 自动生成 OpenAPI 文档，可用于检索、客户端生成和进一步的接口集成。
---

## 当前覆盖

当前快照目标为 **Lucky 3.0.0 wanji / Linux x86_64**。仓库以 Lucky v3 Web 前端的静态调用面为基础，再叠加获授权实例上的脱敏运行时核验结果。

默认合并目录已经把静态快照中的 `UNKNOWN` 路由完成归类或确认为字面量误报；对写接口的请求体字段与 JSON Schema 也持续补充。详细数字、证据等级与限制请以[证据与覆盖范围](./evidence-and-limitations.md)和[完整 API 路由](./generated/api-routes.md)为准。

## 最常用的入口

| 目标 | 文档 |
| --- | --- |
| 第一次连接 Lucky | [快速开始](./quickstart.md) |
| 安全保存 OpenToken | [凭据管理](./credentials.md) |
| 理解安全入口与鉴权 | [鉴权与安全](./authentication.md) |
| 使用 Python 客户端 / CLI | [API 客户端与 CLI](./api-client.md) |
| 找具体接口 | [完整 API 路由](./generated/api-routes.md) |
| 导入接口定义 | [OpenAPI 3.1](https://github.com/UnlastingR/lucky-skills/blob/main/openapi/lucky-v3.openapi.json) |

## 安全调用模型

```bash
python3 tools/lucky_credentials.py install
python3 tools/lucky_credentials.py doctor
python3 tools/lucky_api.py status
```

请求地址必须包含 Lucky 的**安全入口**。推荐通过 `openToken` 请求头传递密钥，不要把 Token 放进查询参数、命令行历史、日志或仓库。

::: warning 不要仅凭 GET / POST 判断安全性
Lucky 存在具有副作用或敏感输出的 `GET` 接口。仓库客户端会结合已验证的路由风险覆盖层进行判断，并对未知、写入和危险调用 fail-closed。
:::

## GitHub

源码、Skill、OpenAPI、测试与证据文件统一维护在：

**[UnlastingR/lucky-skills](https://github.com/UnlastingR/lucky-skills)**

本项目与 Lucky 作者无隶属关系。Lucky 官方项目见 [gdy666/lucky](https://github.com/gdy666/lucky)。

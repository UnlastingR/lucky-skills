# 证据与覆盖范围

## 证据等级

自动生成快照中的 `confidence` 有两种主要值：

- `frontend-call`：在前端请求对象中同时发现 URL 表达式和 HTTP 方法，可信度较高；
- `route-literal-only`：只发现 `/api/...` 字面量，常见于 WebSocket、下载辅助函数或间接封装，方法未知。

手写文档还使用三类说明：

- **实测**：在获授权的本机实例上执行无副作用请求并观察响应；
- **当前前端推断**：从 Lucky v3 页面实际加载的构建文件中提取；
- **历史源码**：来自 Lucky 1.4.10 前后公开代码，只用于解释延续性，不能证明 v3 行为。

## 当前实测基线

| 项目 | 结果 |
|---|---|
| 产品 | Lucky |
| 版本 | 3.0.0 wanji |
| 平台 | Linux x86_64 |
| Go | 1.26.5 |
| 构建日期 | 2026-07-09 |
| 容器镜像 | `gdy666/lucky:v3` |
| 成功只读请求 | `/api/status`、`/api/info`、`/api/modules/list`；新客户端再次验证均为 HTTP 200、业务成功 |
| 可逆写入实测 | Web 规则 `POST /api/webservice/rules` → `GET /api/webservice/rule/{key}` → `DELETE /api/webservice/rule/{key}`；禁用回读成功且基线恢复 |
| 308 重定向实测 | 经明确授权，用 `POST /api/webservice/rules` 创建启用的 80 端口 redirect 规则；`DefaultProxy.OtherParams.RedirectType="308"` 被 API 回读保留，GET/POST 均实测返回 `308 Permanent Redirect` |
| 认证 | 安全入口 + `openToken` 请求头 |
| 状态接口限流 | 实测响应头显示 20 请求/秒窗口 |

未在仓库记录实例的 OpenToken、安全入口、域名、配置或业务数据。

最初的通用 Web 规则写入 smoke test 使用唯一名称、禁用状态、回环地址、关闭自动防火墙和空代理列表；测试完成后独立确认规则无残留、测试端口未监听、iptables/nftables 无匹配规则。后续在同一获授权测试实例上另行通过 OpenToken API 创建了一条启用的 80 → HTTPS 308 重定向规则，用本机 GET/POST 请求验证状态码和 `Location`，不涉及业务后端代理。

## 静态快照

[端点证据 JSON](../evidence/lucky-v3-endpoints.json)记录：

- 目标产品与版本；
- 分析时间；
- 每个前端 bundle 的 SHA-256；
- 归一化路径、HTTP 方法、有限的查询字段和请求体字段；
- 提供证据的 bundle 文件名；
- 推断可信度。

构建文件本身不提交仓库，避免复制上游前端代码和意外带入运行时信息。

生成的路由表额外包含客户端风险等级。该等级是本仓库的保守调用策略，不是 Lucky 上游提供的权限声明；升级后必须重新审核。

## 已知限制

1. 前端未调用的后端路由无法通过此方法发现。
2. 动态字符串拼接只能归一化为 `{param}`，真实参数语义可能未知。
3. 请求体若通过变量传递，只能确定“存在请求体”，无法自动恢复完整 schema。
4. 运行时生成的 WebSocket URL 和二进制协议需要单独抓包。
5. 条件编译模块、特殊镜像和授权模块会改变路由集合。
6. 错误码、并发控制和事务语义不能仅从前端可靠推导。
7. Lucky 闭源版本可能随时改变接口，不承诺向后兼容。

## 为什么不自动调用全部接口

路由中存在删除容器、执行任务、关机、重启、导入配置、终端和文件写入等操作。即使请求方法是 GET，也未必只读。为了不改变用户环境，本次只实测明确的状态、应用信息和模块清单，其余以静态分析为主。

## 更新快照

拿到新版本前端 bundle 后运行：

```bash
python3 tools/extract_lucky_frontend.py /path/to/lucky-js-assets \
  --version <版本号> \
  --output evidence/lucky-v3-endpoints.json \
  --markdown docs/generated/api-routes.md \
  --openapi openapi/lucky-v3.openapi.json
python3 tools/verify_repository.py
```

更新时必须检查 diff 中是否出现真实安全入口、token、域名或配置值。

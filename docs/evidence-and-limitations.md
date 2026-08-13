# 证据与覆盖范围

## 证据等级

证据目录中的 `confidence` 目前有三种主要值：

- `frontend-call`：在前端请求对象中同时发现 URL 表达式和 HTTP 方法，可信度较高；
- `route-literal-only`：只发现 `/api/...` 字面量，常见于 WebSocket、下载辅助函数、字符串前缀或间接封装，方法未知；
- `runtime-verified`：在获授权 Lucky 3.0.0 实例上通过运行时方法探针或受控只读 OpenToken 请求确认。

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
| unknown 运行时核验 | 静态快照中的 41 条 `UNKNOWN` 已通过前缀误报识别、未认证方法探针和选定只读 OpenToken 请求完成归类；默认合并目录当前为 0 条 `unknown` |
| 认证 | 安全入口 + `openToken` 请求头 |
| 状态接口限流 | 实测响应头显示 20 请求/秒窗口 |

未在仓库记录实例的 OpenToken、安全入口、域名、配置或业务数据。

最初的通用 Web 规则写入 smoke test 使用唯一名称、禁用状态、回环地址、关闭自动防火墙和空代理列表；测试完成后独立确认规则无残留、测试端口未监听、iptables/nftables 无匹配规则。后续在同一获授权测试实例上另行通过 OpenToken API 创建了一条启用的 80 → HTTPS 308 重定向规则，用本机 GET/POST 请求验证状态码和 `Location`，不涉及业务后端代理。

## 静态快照与运行时覆盖层

[端点证据 JSON](../evidence/lucky-v3-endpoints.json)保留前端静态分析结果，记录：

- 目标产品与版本；
- 分析时间；
- 每个前端 bundle 的 SHA-256；
- 归一化路径、HTTP 方法、有限的查询字段和请求体字段；
- 提供证据的 bundle 文件名；
- 推断可信度。

构建文件本身不提交仓库，避免复制上游前端代码和意外带入运行时信息。

[运行时验证 JSON](../evidence/lucky-v3-runtime-verification.json)保存脱敏后的方法、查询键、风险覆盖、验证说明、请求/响应 schema 补充和需要抑制的字面量误报。它同时记录静态端点快照的 SHA-256；`RouteCatalog.load_default()` 只有在 Lucky 版本和**精确静态快照哈希**都一致时才合并两层证据，并要求每个 suppression/runtime route 都能在该静态快照中找到对应证据。`schema_evidence` 单独描述字段来源，例如前端显式对象、前端模型直传、只读 GET 的字段形状或二者交叉验证；它不把未执行的写接口伪装成运行时成功验证。运行时层不会修改原始静态快照。仓库 verifier 强制检查这些绑定、重复项、风险值和 schema 元数据格式，并要求合并后的默认目录不再残留 `unknown`。

运行时方法探针不发送 OpenToken：对已知 GET/POST/PUT/DELETE/PATCH 做过校准后，确认“路由+方法存在”会先进入 Lucky 鉴权并返回 `login invalid`，而不存在的方法返回 404。校准过程中还通过正常 OpenToken API 比较 Web 规则数量，确认未认证 POST 没有产生配置变化。危险 handler 的**方法发现**因此停在鉴权层，不执行实际动作。请求/响应 schema 验证另行区分证据强度：本轮嵌套类型补全只读取当前 Lucky 3.0.0 前端 bundle 和获授权 GET 响应，并把响应即时压缩成字段名/JSON 类型树；动态 RuleKey、域名、容器/网络标识、路径、地址和秘密值不会写入证据。仅最后 6 条缺少当前 UI 调用点的 Docker legacy wrapper 在用户明确授权后使用专用临时资源、校验失败路径或 mock Docker API 做了隔离写验证，具体边界记录在每条 `schema_evidence` 中。

生成的静态路由表额外包含客户端风险等级；默认 CLI 目录再叠加运行时风险覆盖。风险等级是本仓库的保守调用策略，不是 Lucky 上游提供的权限声明；升级后必须重新审核。

## 已知限制

1. 前端未调用的后端路由无法通过此方法发现。
2. 动态字符串拼接只能归一化为 `{param}`，真实参数语义可能未知。
3. 请求体若通过变量传递，静态提取器本身通常只能确定“存在请求体”；本仓库会对高价值接口再用前端编辑器模型、显式对象构造和授权只读 GET 的字段形状补充 schema，但这仍不等于后端正式协议定义，尤其不能据此擅自标记必填字段。
4. WebSocket 路由可以确认 HTTP 握手方法，但当前通用 CLI 不建立 WebSocket 会话；`status/ws`、`natdetect/ws`、Docker upgrade-check WS 只验证到路由/鉴权层。
5. 条件编译模块、特殊镜像和授权模块会改变路由集合。
6. 错误码、并发控制和事务语义不能仅从前端或路由存在性可靠推导。
7. 运行时方法探针只能证明 `METHOD + path` 被路由器接受；除明确执行的只读 GET 外，不证明请求体 schema 或业务成功语义。请求 schema 的可信度应以每条记录的 `schema_evidence` 为准。
8. Lucky 闭源版本可能随时改变接口，不承诺向后兼容。
9. 当前“有请求体但字段/schema 为空”的 122 条原始缺口已缩减到 0 条；更严格地看，当前 merged catalog 共有 **242 条 POST/PUT/PATCH**，其中 **218 条**标记 `has_body=true` 并在 OpenAPI 生成 `requestBody`。这 218 条中仅剩 **1 条**在 OpenAPI 顶层保留至少一个未类型化属性，后续应继续下降。全路由显式 response schema 当前为 **323 条**。递归统计所有已存在 schema 中仍以 `{}` 表示“尚未定型”的叶子，request 侧现为 **40 个**、response 侧为 **121 个**，verifier 已把这两个数字设为只降不升的回归门槛。当前已优先补深 DDNS Task/DNS Callback、WebService DefaultProxy/ProxyList、Docker container/config/network/volume、FRP proxy/visitor，以及 SSL/ACME、Security Groups、IPFilter/PortTrap、PortForward、STUN，并继续覆盖 Rclone、Cron、WOL、StorageManagement、FileBrowser、Status、IPDB、IconLib、Modules/About 与 Frontend Preferences 的运行时响应。本轮进一步把 Docker Compose `config_file_name` 的客户端契约收口为字符串，并用只读类型树补齐 Status 主机进程监听端口/端点的嵌套 items。受保护的响应 schema 会主动省略 password/secret/private-key 字段，并由 repository verifier 递归检查对象和 `anyOf`/`oneOf`/`allOf` 等 list-valued schema 分支，防止秘密字段因后续 enrichment 被重新文档化。最后 6 条 Docker legacy wrapper 缺少当前 UI 调用点，因此采用额外隔离验证：临时 BusyBox 容器/镜像只用于 `upgrade`/`build` 成功路径；Git/ZIP/import 通过后端校验差异确认最小必填字段；`prune` 则在第二个临时 Lucky 实例连接到非破坏性 mock Docker API 后验证 `{all, volumes}` 行为，真实 Docker daemon 从未收到 prune 请求。

## 为什么不自动调用全部接口

路由中存在删除容器、执行任务、关机、重启、导入配置、终端和文件写入等操作。即使请求方法是 GET，也未必只读；例如 `GET /api/configure` 已实测返回完整 ZIP 配置备份，因此被显式标为 `dangerous`。危险 unknown 的方法发现优先使用不带认证的路由探针，只有明确只读或使用不存在对象可安全失败的 GET 才进入已认证验证。

## 更新快照

拿到新版本前端 bundle 后运行：

```bash
python3 tools/extract_lucky_frontend.py /path/to/lucky-js-assets \
  --version <版本号> \
  --output evidence/lucky-v3-endpoints.json

# 审核新静态快照，重新核验/重绑 runtime evidence 后再生成合并产物。
python3 tools/render_lucky_artifacts.py evidence/lucky-v3-endpoints.json \
  --markdown docs/generated/api-routes.md \
  --openapi openapi/lucky-v3.openapi.json
python3 tools/verify_repository.py
```

更新时必须检查 diff 中是否出现真实安全入口、token、域名或配置值。只要静态端点快照发生变化（即使 Lucky 仍显示 3.0.0），现有运行时验证文件都不会自动套用；必须重新审核/核验并更新 `static_snapshot_sha256`，然后使用 `render_lucky_artifacts.py` 生成绑定覆盖层已合并的提交产物。Lucky 版本变化时还必须重新执行方法核验并更新 `target.version`。任一绑定不一致都会直接 fail-closed。

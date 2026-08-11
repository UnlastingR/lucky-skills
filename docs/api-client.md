# 安全 API 客户端与 CLI

`lucky_api` 是无第三方依赖的 Python 客户端，`tools/lucky_api.py` 是它的命令行入口。两者共同解决鉴权注入、路径拼接、错误判断、限流重试、响应上限和写操作保护；它们不会把 OpenToken 放进 URL 或命令行参数。

## 能力与边界

当前客户端支持：

- `GET`、`POST`、`PUT`、`DELETE` 和 `PATCH`；
- 重复查询参数、JSON 请求体、原始文件请求体和二进制下载；
- HTTP 错误、Lucky `ret` 业务错误、JSON 解码错误、传输错误和响应过大错误；
- `RateLimit-Limit`、`RateLimit-Remaining` 和 `RateLimit-Reset` 元数据；
- 只读请求遇到 429/502/503/504 时的有限重试；
- 基于当前 v3 路由快照的路径模板匹配与风险分级。

客户端不提供“自动猜测配置字段”、网页登录模拟、模块 2FA 绕过或批量试探接口。multipart 表单可作为原始请求体发送，但客户端不会替你构造包含密钥或文件的表单。

## 风险模型

每个实际的 `METHOD + path` 会先与当前证据快照匹配，再分为：

| 等级 | 含义 | 默认行为 |
|---|---|---|
| `read-only` | 快照中存在，且未识别出副作用 | 允许 |
| `mutating` | 修改配置、执行动作，或有副作用的 GET | 拒绝 |
| `dangerous` | 删除、重启、文件写入、恢复、Docker 操作等 | 拒绝 |
| `unknown` | 当前快照没有对应方法和路径 | 拒绝 |

这是保守策略，不是权限系统。`read-only` 仍可能返回日志、路径、IP、容器信息等敏感数据；Lucky 升级后也可能改变端点行为。

## CLI 快速使用

先安装凭据，再通过单个子进程注入：

```bash
python3 tools/lucky_credentials.py install
python3 tools/lucky_credentials.py run -- python3 tools/lucky_api.py status
python3 tools/lucky_credentials.py run -- python3 tools/lucky_api.py info
python3 tools/lucky_credentials.py run -- python3 tools/lucky_api.py modules
```

查看状态码、内容类型和限流元数据：

```bash
python3 tools/lucky_credentials.py run -- \
  python3 tools/lucky_api.py status --show-meta
```

## 查询路由目录

目录查询不需要 OpenToken：

```bash
python3 tools/lucky_api.py catalog --search docker --method GET
python3 tools/lucky_api.py catalog --module ddns --risk mutating
python3 tools/lucky_api.py catalog --search logs --json
```

目录输出包括方法、路径模板、模块、风险、查询字段、请求体字段、响应类型和证据等级。字段为空表示前端静态分析无法恢复，不代表请求体确实没有字段。

## 查询参数与二进制响应

重复使用 `--query KEY=VALUE`，客户端负责 URL 编码：

```bash
python3 tools/lucky_credentials.py run -- \
  python3 tools/lucky_api.py call /api/docker/containers \
  --query all=true --query includeStats=false
```

下载端点应写入文件；二进制内容默认不会直接打印到交互终端：

```bash
python3 tools/lucky_credentials.py run -- \
  python3 tools/lucky_api.py call '/api/docker/containers/ID/export' \
  --method POST --output container.tar \
  --allow-write --confirm 'POST /api/docker/containers/ID/export'
```

上例只是调用语法，导出操作可能很耗资源；请把 `ID` 替换为已核对的目标，并先确认磁盘空间和数据处理要求。

## JSON 与原始请求体

请求体优先从文件或标准输入读取，避免敏感字段出现在 shell 历史和进程参数中：

```bash
python3 tools/lucky_credentials.py run -- \
  python3 tools/lucky_api.py call /api/ddns --method PUT \
  --json-file reviewed-ddns.json \
  --allow-write --confirm 'PUT /api/ddns'

python3 tools/lucky_credentials.py run -- \
  python3 tools/lucky_api.py call /api/ddns --method PUT --json-stdin \
  --allow-write --confirm 'PUT /api/ddns' < reviewed-ddns.json
```

写操作需要两个独立条件：`--allow-write`，以及与实际请求完全相同的 `--confirm 'METHOD /api/path'`。这只能防止误操作，不能替代备份、差异审阅和回滚计划。

原始内容可通过 `--raw-file` 和 `--content-type` 发送。JSON 与原始请求体互斥。

## Python 调用

```python
from lucky_api import LuckyClient, RouteCatalog

catalog = RouteCatalog.load_default()
client = LuckyClient.from_environment(
    catalog=catalog,
    timeout=10,
    retries=2,
    max_response_bytes=16 * 1024 * 1024,
)

status = client.request_json("GET", "/api/status")
print(status["ret"])
```

调用方必须显式批准非只读操作：

```python
result = client.request_json(
    "PUT",
    "/api/ddns",
    json_body=reviewed_complete_object,
    allow_unsafe=True,
)
```

库层的 `allow_unsafe=True` 只表示调用代码已经完成外部审批；它不会弹出确认提示。面向人工操作时优先使用 CLI 的双重确认。

## 错误类型

调用方可分别处理：

- `UnsafeOperationError`：目录未知或操作不是只读；
- `TransportError`：DNS、连接、TLS 或超时失败；
- `HTTPStatusError`：HTTP 非成功状态；
- `LuckyAPIError`：HTTP 可为 200，但 JSON 中 `ret` 非零；
- `ResponseDecodeError`：预期读取 JSON，但响应不是合法 JSON；
- `ResponseTooLargeError`：响应超过配置上限。

异常消息只包含 API 路径，不包含基础 URL、安全入口或 OpenToken。HTTP 错误正文最多保留一小段，并再次替换可能出现的 Token。

## 重试规则

只有风险为 `read-only` 的请求才会自动重试 429、502、503 和 504。客户端优先遵守 `Retry-After`，其次使用 `RateLimit-Reset`，否则指数退避；单次等待上限为 30 秒。

写操作、危险操作和未知操作永不自动重试。它们超时后应先查询当前状态，避免重复创建、重复触发或部分写入。

## 版本漂移

路由目录目标版本为 Lucky 3.0.0。升级 Lucky 后应重新提取前端资产、审核路由差异并重新生成文档；在新版本完成验证前，不应批准写操作。可用 `LUCKY_API_CATALOG` 指向另一个经过审核的证据 JSON。

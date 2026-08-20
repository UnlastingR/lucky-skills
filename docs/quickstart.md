# 快速开始

> 第一次使用？建议先按[安装指南](installation.md)完成项目获取、凭据安装和连通性验证。本页专注于完成第一个安全 API 请求。

## 前置条件

你需要知道三个值：

- Lucky 面板的协议、主机和端口，例如 `http://127.0.0.1:16601`；
- Lucky 设置中的“安全入口”；
- 已启用的 OpenToken。

推荐使用统一凭据安装器。基础地址应设置到安全入口这一层，不要以 `/api` 结尾：

```bash
python3 tools/lucky_credentials.py install
python3 tools/lucky_credentials.py doctor
```

安装器隐藏 token 输入，将凭据原子写入仅当前用户可读的文件。完整说明见[统一安全凭据安装与调用](credentials.md)。

## 第一个只读请求

```bash
python3 tools/lucky_api.py status
```

典型成功响应是 JSON 对象，并包含 `ret: 0`。本机 Lucky 3.0.0 的状态响应还包含 CPU、内存、网络累计流量、连接数、运行时间和查询时间等字段。

继续检查应用信息与模块：

```bash
python3 tools/lucky_api.py status
python3 tools/lucky_api.py info
python3 tools/lucky_api.py modules
```

## Python 示例

```bash
python3 tools/lucky_api.py status
python3 tools/lucky_api.py info
python3 tools/lucky_api.py modules
```

客户端会将实际路径与证据目录匹配。未知端点、非 GET 请求和已知有副作用的 GET 默认拒绝；写请求还需要精确确认。完整用法见[安全 API 客户端与 CLI](api-client.md)。

## 常见失败

| 现象 | 最可能原因 | 处理 |
|---|---|---|
| 404，正文提示请求路径不存在 | URL 缺少安全入口，或入口拼接错误 | 检查 `LUCKY_BASE_URL` 是否已包含安全入口 |
| 认证失败 | 请求头名不对、OpenToken 未启用、token 已轮换 | 使用原样的 `openToken` 请求头，不加 `Bearer` |
| 429 或限流头余量为 0 | 请求过密 | 降低轮询频率并采用退避 |
| 浏览器跨域失败，但 curl 成功 | CORS 可信来源未配置 | 在开发者设置中加入明确的前端来源；不要无必要开放任意来源 |
| 模块要求额外验证 | 模块级 2FA 已启用 | 先完成该模块验证流程，不要尝试绕过 |

## URL 拼接检查

正确：

```text
http://127.0.0.1:16601/<安全入口>/api/status
```

错误：

```text
http://127.0.0.1:16601/api/status
http://127.0.0.1:16601/<安全入口>/api/api/status
```

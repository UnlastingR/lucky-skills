# 快速开始

## 前置条件

你需要知道三个值：

- Lucky 面板的协议、主机和端口，例如 `http://127.0.0.1:16601`；
- Lucky 设置中的“安全入口”；
- 已启用的 OpenToken。

将基础地址设置到安全入口这一层，不要以 `/api` 结尾：

```bash
export LUCKY_BASE_URL='http://127.0.0.1:16601/<安全入口>'
read -rsp 'Lucky OpenToken: ' LUCKY_OPEN_TOKEN
export LUCKY_OPEN_TOKEN
printf '\n'
```

`read -s` 可以避免密钥出现在终端回显和 shell 历史中。也可以由系统密钥管理器或 CI secret 注入环境变量。

## 第一个只读请求

```bash
curl --fail-with-body --silent --show-error \
  --header "openToken: ${LUCKY_OPEN_TOKEN}" \
  "${LUCKY_BASE_URL}/api/status"
```

典型成功响应是 JSON 对象，并包含 `ret: 0`。本机 Lucky 3.0.0 的状态响应还包含 CPU、内存、网络累计流量、连接数、运行时间和查询时间等字段。

继续检查应用信息与模块：

```bash
examples/lucky-readonly.sh status
examples/lucky-readonly.sh info
examples/lucky-readonly.sh modules
```

## Python 示例

```bash
python3 examples/lucky_api.py /api/status
python3 examples/lucky_api.py /api/info
python3 examples/lucky_api.py /api/modules/list
```

示例客户端默认只允许 `GET`，并额外拦截名称上明显有副作用的 GET 路径。写请求必须显式添加 `--allow-write`；执行前仍应查看[模块指南](modules.md)和[完整路由表](generated/api-routes.md)。

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

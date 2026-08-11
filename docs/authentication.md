# 鉴权与安全

## OpenToken 的位置

推荐形式：

```http
GET /<安全入口>/api/status HTTP/1.1
Host: 127.0.0.1:16601
openToken: <你的 OpenToken>
```

Lucky 前端说明还支持 `?openToken=<token>`，但查询字符串常被反向代理、浏览器历史、监控系统和访问日志保存，所以本仓库所有示例默认使用请求头。

以下形式不是 OpenToken 鉴权：

```http
Authorization: Bearer <token>
Authorization: <token>
```

`Authorization` 在 Lucky 中还可能用于网页登录会话或上传流程，不能与 OpenToken 混用。

## 安全入口仍是地址的一部分

OpenToken 不替代安全入口。请求仍应发往：

```text
<面板地址>/<安全入口>/api/<端点>
```

把安全入口视为第二个秘密并不充分：它会出现在 URL 中，可能被访问日志记录。真正的认证边界仍是 OpenToken、面板网络边界和必要时的模块级 2FA。

## 权限模型

当前证据没有显示 OpenToken 具备细粒度 scope。只要相应模块可用，它可能触达：

- Lucky 全局配置、备份恢复与进程重启；
- DDNS、端口转发、Web 服务、STUN、WOL 和计划任务；
- 证书、IP 过滤、安全组和 WAF；
- Docker 容器、镜像、网络、卷和 Compose；
- 本地路径浏览、Web 终端、SFTP 及文件操作；
- Cloudflared、FRP、Rclone 与第三方网盘授权。

因此 OpenToken 应按管理员密钥管理，不能放到公开前端、移动 App 包、浏览器 localStorage、Git 仓库或聊天记录中。

## 轮换清单

当 token 曾被粘贴到聊天、Issue、日志或命令行参数中时：

1. 在 Lucky 的开发者设置中生成新的 OpenToken；
2. 更新服务端 secret 或密码管理器；
3. 重启或保存配置，使旧 token 失效；
4. 检查反向代理与 Lucky 日志中是否记录了查询参数形式的 token；
5. 检查 Git 历史，而不只是当前工作树；
6. 用新的 token 执行一次 `GET /api/status`，随后确认旧 token 失败。

Lucky v2 更新日志说明，连续 OpenToken 验证失败超过阈值后会自动禁用 OpenToken 并要求重启。这意味着客户端必须避免用空值或错误值无限重试。

## 推荐部署边界

- 面板优先只监听内网或回环地址，通过 VPN、SSH 隧道或受控反向代理访问。
- 外网访问必须使用 HTTPS；HTTP 会明文传输 token。
- CORS 只允许明确的可信来源，不建议开启“任意跨域源”。
- 给自动化客户端设置低并发、短超时、退避和审计日志，但审计日志不得记录请求头。
- 对写操作做调用方二次确认；对容器、终端、文件和恢复配置接口做独立封装和白名单。

## 日志脱敏

应删除或替换以下内容：

```text
openToken: <redacted>
?openToken=<redacted>
Authorization: <redacted>
SafeURL: <redacted>
```

本仓库的原始响应只存放在临时目录，提交的是端点路径、方法、有限参数名和 bundle 哈希等派生证据。

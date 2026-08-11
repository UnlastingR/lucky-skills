# 统一安全凭据安装与调用

本仓库的统一方式是 `tools/lucky_credentials.py`。它把基础 URL 和 OpenToken 存入用户私有配置文件，并只在启动一个子命令时注入：

```text
凭据文件（600） → lucky_credentials.py run → 子进程环境变量
                                           ├─ LUCKY_BASE_URL
                                           └─ LUCKY_OPEN_TOKEN
```

不把 token 写入命令行参数、shell 历史、Git、`.env` 或全局 shell 启动文件。

## 1. 安装凭据

从仓库根目录运行：

```bash
python3 tools/lucky_credentials.py install
```

安装器会依次询问：

1. 包含安全入口的 Lucky 基础 URL；
2. OpenToken；
3. 再次输入 OpenToken。

token 输入不回显。默认文件位置：

- Linux/macOS：`$XDG_CONFIG_HOME/lucky-skills/credentials.json`，未设置时使用 `~/.config/lucky-skills/credentials.json`；
- Windows：`%APPDATA%\lucky-skills\credentials.json`；
- 自定义：设置 `LUCKY_CREDENTIALS_FILE`，或给命令传 `--file`。

POSIX 系统上目录权限设置为 `700`，文件权限设置为 `600`。写入使用同目录临时文件、`fsync` 和原子替换，并拒绝符号链接目标。

凭据文件是权限隔离的明文 JSON，并非加密保险库。设备应启用磁盘加密；多人共享机器或更高安全等级环境应改用操作系统密钥环或专用 secret manager。

默认只允许 HTTPS；仅回环地址允许 HTTP。例如：

```text
http://127.0.0.1:16601/<安全入口>       允许
https://lucky.example.com/<安全入口>    允许
http://192.168.1.2:16601/<安全入口>     默认拒绝
```

如果受控局域网环境暂时只能使用 HTTP，必须明确添加 `--allow-http`，但这仍会让 token 在网络上明文传输：

```bash
python3 tools/lucky_credentials.py install --allow-http
```

## 2. 检查安装

```bash
python3 tools/lucky_credentials.py doctor
```

该命令只显示文件位置、权限、已隐藏安全入口的基础 URL，以及 token 的 SHA-256 短指纹，不显示 token 本身。指纹可用于确认两台机器是否装了同一个 token，而无需复制密钥。

## 3. 统一调用

只读状态：

```bash
python3 tools/lucky_credentials.py run -- \
  python3 tools/lucky_api.py status
```

应用信息与模块清单：

```bash
python3 tools/lucky_credentials.py run -- python3 tools/lucky_api.py info
python3 tools/lucky_credentials.py run -- python3 tools/lucky_api.py modules
```

不建议使用 `sh -c` 拼接 curl 鉴权头：shell 展开后，Token 可能短暂出现在 curl 的进程参数中。仓库 CLI 直接从子进程环境读取凭据并在进程内部构造请求。

## 4. 更新或轮换

重新执行安装并确认覆盖：

```bash
python3 tools/lucky_credentials.py install
python3 tools/lucky_credentials.py doctor
```

然后用新 token 调用 `GET /api/status`，确认成功；旧 token 应在 Lucky 中失效。不要把旧 token 留在备份、Issue、聊天记录或 Actions 日志中。

## 临时调用，不落盘

在一次性维护终端中，也可只为当前 shell 读取 token：

```bash
export LUCKY_BASE_URL='https://lucky.example.com/<安全入口>'
read -rsp 'Lucky OpenToken: ' LUCKY_OPEN_TOKEN
export LUCKY_OPEN_TOKEN
printf '\n'
python3 tools/lucky_api.py status
unset LUCKY_OPEN_TOKEN LUCKY_BASE_URL
```

这种方式不会写文件，但环境变量会保留到 `unset` 或 shell 退出。

## GitHub Actions

把 OpenToken 放入 GitHub Actions Secret，把基础 URL 放入 Secret 或 Variable。不要在来自 fork 的 PR 上暴露 secret，也不要让 GitHub 托管 runner 直接访问内网 Lucky。

```yaml
env:
  LUCKY_BASE_URL: ${{ secrets.LUCKY_BASE_URL }}
  LUCKY_OPEN_TOKEN: ${{ secrets.LUCKY_OPEN_TOKEN }}
```

只有在受控的 self-hosted runner、受保护环境和人工批准后，才应执行实际 Lucky 调用。当前仓库的 `docs-ci` 不读取或使用任何 Lucky secret。

## 安全边界

- 子进程必须获得 token 才能调用 API，因此同一用户或 root 仍可能通过进程环境读取它。
- Windows 上 Python 的 `chmod` 不能完整表达 ACL；安装后应确认只有当前账号可以读取文件。
- 备份软件可能复制凭据文件；应对备份加密并限制访问。
- OpenToken 权限很高。业务服务最好通过只暴露允许接口的代理调用，而不是直接获得 token。

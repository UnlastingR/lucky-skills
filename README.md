# Lucky OpenToken API 文档（非官方）

这是面向 Lucky 管理后台 OpenToken 的可复现、尽可能完整的中文 API 文档仓库。它不是 Lucky 上游发布的稳定接口规范，而是基于以下证据整理：

- Lucky v3 Web 前端构建产物的静态调用分析；
- 获授权 Lucky v3 实例上的脱敏运行时路由/方法核验与受控只读请求；
- Lucky 最后公开源码及官方更新日志的交叉核对。

当前快照目标为 **Lucky 3.0.0 wanji / Linux x86_64**。已静态提取 600 余条“HTTP 方法 + 路径”调用记录，并生成 OpenAPI 3.1 文档；默认客户端还会叠加与 Lucky 版本及**静态快照 SHA-256 精确匹配**的脱敏运行时验证覆盖层。静态快照原有的 41 条 `UNKNOWN` 已完成归类或确认是字面量误报，当前默认合并目录为 **0 条 unknown**。真实 OpenToken、安全入口、运行配置和业务数据均未写入仓库。

## 从这里开始

1. 阅读[快速开始](docs/quickstart.md)，完成第一个只读请求。
2. 使用[统一安全凭据安装与调用](docs/credentials.md)保存并注入 OpenToken。
3. 阅读[鉴权与安全](docs/authentication.md)，理解 OpenToken、安全入口和轮换要求。
4. 查看[接口约定](docs/conventions.md)和[模块指南](docs/modules.md)。
5. 使用[安全 API 客户端与 CLI](docs/api-client.md)进行受控调用。
6. 在[完整路由表](docs/generated/api-routes.md)中查找具体接口。
7. 将 [OpenAPI 3.1](openapi/lucky-v3.openapi.json) 导入支持 OpenAPI 的客户端。

## Codex / ChatGPT Skill

仓库内置标准 Agent Skill：`.agents/skills/lucky/SKILL.md`。当 Codex/devspace 在本仓库中工作时，会按官方仓库级 Skill 发现规则自动加载它；可显式使用 `$lucky`，也可由模型根据描述自动匹配 Lucky 管理任务。

同时提供 `.codex-plugin/plugin.json`，插件安装使用规范要求的 `skills/lucky/SKILL.md`。仓库级发现继续使用 `.agents/skills/lucky/SKILL.md`；CI 会强制两份 Skill 内容完全一致，避免维护过程中漂移。完整插件安装应包含整个仓库/插件目录，因为 Skill 会调用本仓库的 `tools/lucky_credentials.py`、`tools/lucky_api.py`、路由证据和文档。

Skill 的安全约束与客户端一致：默认只读；修改操作必须是用户明确请求，并通过路由风险分级、`--allow-write` 与精确 `--confirm` 才会执行。OpenToken 仍由[统一安全凭据安装与调用](docs/credentials.md)管理，不写入 Skill 或插件清单。

## 最重要的结论

- 请求地址必须包含 Lucky 的安全入口：`http://主机:端口/<安全入口>/api/...`。
- 推荐使用请求头 `openToken: <token>`；查询参数 `?openToken=...` 虽受支持，但容易泄露到日志和历史记录，不推荐。
- `openToken` 不是 `Authorization: Bearer ...`，也不是网页登录产生的会话令牌。
- OpenToken 应视为管理员密钥。前端暴露的接口包含改配置、执行任务、管理容器、读写文件和打开终端等高权限操作。
- 不要仅凭 HTTP 方法判断安全性；Lucky 的部分有副作用操作历史上使用过 `GET`。
- 本机实测 `GET /api/status`、`GET /api/info`、`GET /api/modules/list` 成功；状态接口响应显示每秒 20 次的限流头。
- Web 服务规则已完成一次可逆实测：创建禁用规则、详情回读、删除、基线恢复；测试端口和防火墙均无残留。
- 内置客户端综合前端静态快照和与其 SHA-256 精确绑定的运行时验证做模板匹配与风险分级；当前 Lucky 3.0.0 默认目录为 0 条 unknown，未收录端点、写请求及危险 GET 仍默认拒绝。
- 不要把 `GET` 等同于安全读取：`GET /api/configure` 已实测返回 Lucky 配置 ZIP 备份，因此运行时覆盖会把这类反常 GET 显式标为 `dangerous`。

## 统一安全调用

```bash
python3 tools/lucky_credentials.py install
python3 tools/lucky_credentials.py doctor
python3 tools/lucky_api.py status
```

安装器隐藏输入、原子写入用户私有凭据文件，并设置 POSIX `700/600` 权限。API CLI 仅在 `LUCKY_BASE_URL` 与 `LUCKY_OPEN_TOKEN` 同时非空时使用环境凭据；两者都为空/未设置时自动读取当前平台/配置对应的默认凭据文件，只有一个非空则 fail-closed。不会把 token 放进命令行参数或子进程环境；可用 `--credentials-file PATH` 显式覆盖，旧 `run -- ...` 方式仍保留兼容。

## 仓库结构

```text
.agents/skills/lucky/  Codex/devspace 仓库级自动发现的 Lucky Agent Skill
skills/lucky/          Codex 插件安装器使用的 Lucky Skill 镜像
.codex-plugin/         Codex 插件 manifest
lucky_api/             可复用的无依赖 Python 客户端与路由风险策略
docs/                 手写指南与自动生成路由表
evidence/             前端静态端点快照 + 脱敏运行时验证覆盖层
examples/             默认只读、从环境变量取密钥的客户端
openapi/              自动生成的 OpenAPI 3.1
tests/fixtures/        提取器的最小测试夹具
tools/                 API CLI、路由提取、产物生成和仓库验证脚本
.github/workflows/     GitHub Actions 云端验证
```

## 本地验证

```bash
python3 tools/verify_repository.py
python3 tools/extract_lucky_frontend.py tests/fixtures \
  --version test \
  --output /tmp/lucky-fixture.json \
  --markdown /tmp/lucky-fixture.md \
  --openapi /tmp/lucky-fixture.openapi.json
```

GitHub Actions 会在 Python 3.10–3.13 上云端编译并运行全部测试，同时执行密钥误提交检测、文档本地链接检查、端点快照/OpenAPI 一致性检查和生成产物可复现性检查。

## 准确性边界

“完整”在此表示尽可能覆盖当前前端实际调用面，不表示上游兼容性承诺。闭源版本的后端可能还存在前端未使用的接口；静态分析也无法完整推导所有 JSON 字段、条件分支、WebSocket 消息和错误码。每条记录都带有证据等级，详见[证据与覆盖范围](docs/evidence-and-limitations.md)。

## 上游

- [Lucky 官方仓库](https://github.com/gdy666/lucky)
- [Lucky 官方文档](https://lucky666.cn/)
- [Lucky v2 更新日志](https://lucky666.cn/docs/updatelogs/v2.X/)

本仓库与 Lucky 作者无隶属关系。请仅对你拥有或获授权管理的实例调用接口。

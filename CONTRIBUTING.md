# Contributing

## 原则

- 只对你拥有或获授权的 Lucky 实例采集证据。
- 默认只执行明确无副作用的 GET；不要批量探测全部路由。
- 不提交前端 bundle、原始配置、原始响应或访问日志。
- 示例只能使用占位符和环境变量。
- 新结论应标注为实测、当前前端推断或历史源码。

## 更新流程

1. 将目标版本页面引用的 JavaScript bundle 放在仓库外的临时目录。
2. 运行 `tools/extract_lucky_frontend.py` 更新 JSON、Markdown 和 OpenAPI。
3. 审核生成 diff，特别注意 URL、token、域名和配置值。
4. 运行 `python3 tools/verify_repository.py`。
5. 在 PR 中写明 Lucky 版本、镜像类型、bundle 数量和只读实测范围。

不要仅为了让快照“更完整”而调用删除、启停、同步、触发任务、终端、上传、下载、恢复或 Docker 写操作。

# Contributing

## 原则

- 只对你拥有或获授权的 Lucky 实例采集证据。
- 默认只执行明确无副作用的 GET；不要携带 OpenToken 批量试探未知路由或未知方法。
- 不提交前端 bundle、原始配置、原始响应或访问日志。
- 示例只能使用占位符和环境变量。
- 新结论应标注为 `runtime-verified`、当前前端推断或历史源码，并区分“方法/路由存在”与“业务行为已执行验证”。

## 更新流程

1. 将目标版本页面引用的 JavaScript bundle 放在仓库外的临时目录。
2. 运行 `tools/extract_lucky_frontend.py` 更新证据 JSON。
3. 审核 `evidence/lucky-v3-runtime-verification.json`：只保留脱敏后的方法、查询键、风险覆盖、验证说明和已确认的字面量误报；版本变化时不得沿用旧版运行时结论。
4. 运行 `tools/render_lucky_artifacts.py` 从静态证据生成 Markdown 和 OpenAPI。
5. 审核生成 diff，特别注意 URL、token、域名、配置值和风险等级变化。
6. 运行 `python3 -m unittest discover -s tests -v` 和 `python3 tools/verify_repository.py`；verifier 必须确认默认合并目录不残留 `unknown`。
7. 在 PR 中写明 Lucky 版本、镜像类型、bundle 数量、运行时验证方法和实际执行过的只读请求范围。

不要仅为了让快照“更完整”而调用删除、启停、同步、触发任务、终端、上传、下载、恢复或 Docker 写操作。恢复未知 HTTP 方法时，若已经在目标版本上校准确认路由器会在业务 handler 前执行鉴权，可优先使用**不带 OpenToken**的 method probe；非 404 只能证明 `METHOD + path` 被路由接受，不能证明请求体或业务成功语义。

`tools/lucky_web_rule_smoke.py` 不属于常规 CI：它会真实创建并删除一条禁用 Web 规则。只有实例所有者明确授权、已有配置基线并准备人工处理清理失败时才能运行。

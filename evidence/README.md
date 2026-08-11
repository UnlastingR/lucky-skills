# Evidence

`lucky-v3-endpoints.json` 是从获授权本机 Lucky v3 前端 bundle 派生的端点元数据，不包含 bundle 内容、OpenToken、安全入口、主机名或 API 原始响应。

字段说明：

- `target`：分析目标版本；
- `bundle_sha256`：用于判断前端是否变化；
- `path` / `method`：归一化路径与推断方法；
- `query_keys` / `body_keys`：能够从字面量恢复的字段，不保证完整；
- `evidence`：提供调用证据的 bundle 文件名；
- `confidence`：`frontend-call` 或 `route-literal-only`。

该文件由 [extract_lucky_frontend.py](../tools/extract_lucky_frontend.py) 生成。

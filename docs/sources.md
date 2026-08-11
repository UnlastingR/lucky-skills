# 资料来源

## 官方来源

- [Lucky 官方仓库](https://github.com/gdy666/lucky)：说明 Lucky 的功能、默认端口、前后端分离架构，以及第三方开发者可使用 OpenToken 调用接口。仓库也声明后续版本不再继续开源。
- [Lucky 官方文档](https://lucky666.cn/)：安装、模块与基础使用说明。
- [Lucky v2 更新日志](https://lucky666.cn/docs/updatelogs/v2.X/)：OpenToken 失败保护、CORS 策略和各模块版本演进。
- [Lucky 官方安装文件仓库](https://github.com/gdy666/lucky-files)：用于历史版本交叉核对。

## 本机派生证据

在用户授权下，文档基线来自本机 Docker 中运行的 Lucky v3 实例。只执行了状态、应用信息和模块清单三类只读 API。随后从该实例返回的前端入口递归获取 JavaScript bundle，在临时目录中做静态分析。

仓库只保留派生端点快照和 bundle 哈希，不保留 bundle 内容、OpenToken、安全入口或原始 API 响应。

## 历史源码的使用方式

Lucky 官方仓库公开到较早版本。历史源码可证明某些长期约定，例如 `/api/...` 路由、JSON `ret` 包络和前后端分离模式，但不能用来断言 Lucky v3 的当前请求体或权限行为。v3 结论优先使用当前前端证据与只读实测。

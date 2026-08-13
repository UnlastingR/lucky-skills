# 文档站部署

本仓库使用 [VitePress](https://vitepress.dev/) 构建文档站，并由 **Cloudflare Worker + Static Assets** 提供服务。公开路径固定为：

```text
https://docs.fyzure.fyi/lucky-skills/
```

## 本地开发

```bash
npm install --include=dev --no-package-lock
npm run docs:dev
```

## 构建 Worker 静态资源

```bash
npm install --include=dev --no-package-lock
npm run docs:worker
```

最终静态资源目录是 `dist/`。VitePress 站点本体位于 `dist/lucky-skills/`，Worker 通过 Static Assets binding 读取这些文件。

Worker 统一处理整个 `docs.fyzure.fyi/*`：

- `/` 重定向到 `/lucky-skills/`；
- `/lucky-skills` 规范化到带尾斜杠路径；
- VitePress 带哈希静态资源使用长期 immutable 缓存；
- HTML 使用短缓存，便于文档更新快速生效；
- 以后可以继续在同一 Worker 下挂载其它 `/项目名/` 文档。

## CDN 拓扑

文档的正式入口与 CDN 桥接域名分离：

```text
docs.fyzure.fyi/*               Worker 统一文档入口
cdn.fyzure.fyi                  CDN 桥接域名
saas.sin.fan                    外部 SaaS CDN 接入点
```

`cdn.fyzure.fyi` 仅承担 CDN 桥接角色，不在仓库中保存任何第三方 CDN 密钥或控制面配置。Worker 本身可独立提供文档服务，避免第三方 CDN 控制面异常时导致文档源站不可用。

## 部署 Worker

使用 Wrangler 构建并发布 Worker：

```bash
npm run worker:deploy
```

部署后应分别验证：

1. `docs.fyzure.fyi/lucky-skills/` 正式入口；
2. `docs.fyzure.fyi/*` 是否全部命中 Worker；
3. `cdn.fyzure.fyi` 的 DNS 链与 SaaS CDN 状态；
4. HTML 与带哈希静态资源的 `Cache-Control` 响应头。

# API 路由参考

> 目标版本：Lucky 3.0.0。共收录 623 个“路径 + 方法”记录。
> 此表由前端构建产物静态生成，不代表上游承诺的稳定公共 API；`UNKNOWN` 表示只发现路径字面量。

## `2fa`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `PUT` | `/api/2fa/setting` | `mutating` | — | 有 | `json` | `frontend-call` |

## `about-content`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/about-content` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/about-content` | `mutating` | — | 有 | `json` | `frontend-call` |

## `baseconfigure`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/baseconfigure` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/baseconfigure` | `mutating` | — | 有 | `json` | `frontend-call` |

## `cloudflared`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `UNKNOWN` | `/api/cloudflared` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `GET` | `/api/cloudflared/list` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/cloudflared/list` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/cloudflared/list` | `mutating` | — | 有 | `json` | `frontend-call` |
| `DELETE` | `/api/cloudflared/list/{param}` | `mutating` | — | — | `json` | `frontend-call` |
| `GET` | `/api/cloudflared/list/{param}` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/cloudflared/list/{param}/{param2}` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/cloudflared/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `PUT` | `/api/cloudflared/orderadjustment` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/cloudflared/{param}/cname/check` | `read-only` | `hostname` | — | `json` | `frontend-call` |
| `POST` | `/api/cloudflared/{param}/cname/create` | `mutating` | — | 有 | `json` | `frontend-call` |
| `DELETE` | `/api/cloudflared/{param}/cname/delete` | `dangerous` | `hostname` | — | `json` | `frontend-call` |
| `DELETE` | `/api/cloudflared/{param}/ingress` | `mutating` | `hostname`, `path` | — | `json` | `frontend-call` |
| `GET` | `/api/cloudflared/{param}/ingress` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/cloudflared/{param}/ingress` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/cloudflared/{param}/ingress` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/cloudflared/{param}/lastlogs` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/cloudflared/{param}/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |

## `configure`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `UNKNOWN` | `/api/configure` | `unknown` | — | — | `unknown` | `route-literal-only` |

## `coraza`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/coraza/OWASPCoreRuleset` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/coraza/instancelist` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/coraza/instanceorderadjustment` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/coraza/list` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/coraza/list` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/coraza/list` | `mutating` | — | 有 | `json` | `frontend-call` |
| `DELETE` | `/api/coraza/list/{param}` | `mutating` | — | — | `json` | `frontend-call` |
| `GET` | `/api/coraza/list/{param}` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/coraza/list/{param}/{param2}` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/coraza/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |

## `cron`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/cron/dojobs` | `mutating` | `key` | — | `json` | `frontend-call` |
| `GET` | `/api/cron/enable` | `mutating` | `enable`, `key` | — | `json` | `frontend-call` |
| `GET` | `/api/cron/expressioncheck` | `read-only` | `expression` | — | `json` | `frontend-call` |
| `DELETE` | `/api/cron/groups` | `mutating` | `key` | — | `json` | `frontend-call` |
| `GET` | `/api/cron/groups` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/cron/groups` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/cron/groups` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/cron/groups/collapsed` | `mutating` | — | `collapsed`, `key` | `json` | `frontend-call` |
| `GET` | `/api/cron/groups/collapsed/states` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/cron/groups/orderadjustment` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/cron/groups/taskcount` | `read-only` | `groupKey` | — | `json` | `frontend-call` |
| `POST` | `/api/cron/jobs/trigger` | `mutating` | — | `cronKey`, `jobIndex` | `json` | `frontend-call` |
| `GET` | `/api/cron/lastlogs` | `read-only` | — | — | `json` | `frontend-call` |
| `DELETE` | `/api/cron/list` | `mutating` | `key` | — | `json` | `frontend-call` |
| `GET` | `/api/cron/list` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/cron/list` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/cron/list` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/cron/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `PUT` | `/api/cron/taskgrouporderupdate` | `mutating` | — | 有 | `json` | `frontend-call` |

## `ddns`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `DELETE` | `/api/ddns` | `mutating` | `key` | — | `json` | `frontend-call` |
| `POST` | `/api/ddns` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/ddns` | `mutating` | `key` | 有 | `json` | `frontend-call` |
| `GET` | `/api/ddns/configure` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/ddns/configure` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/ddns/credential-sources` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/ddns/enable` | `mutating` | `enable`, `key` | — | `json` | `frontend-call` |
| `GET` | `/api/ddns/expanded` | `mutating` | `expanded`, `key` | — | `json` | `frontend-call` |
| `GET` | `/api/ddns/getipfromcmdtest` | `read-only` | `command`, `iptype` | — | `json` | `frontend-call` |
| `GET` | `/api/ddns/ipsectionexpanded` | `mutating` | `expanded`, `key` | — | `json` | `frontend-call` |
| `GET` | `/api/ddns/lastlogs` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/ddns/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `UNKNOWN` | `/api/ddns/manualSync` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `GET` | `/api/ddns/manualSync/{param}` | `mutating` | — | — | `json` | `frontend-call` |
| `GET` | `/api/ddns/odhcpdclients` | `read-only` | — | — | `json` | `frontend-call` |
| `UNKNOWN` | `/api/ddns/recordOrderadjustment` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `PUT` | `/api/ddns/recordOrderadjustment/{param}` | `mutating` | — | 有 | `json` | `frontend-call` |
| `UNKNOWN` | `/api/ddns/task` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `GET` | `/api/ddns/task/{param}` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/ddns/taskorderadjustment` | `mutating` | — | 有 | `json` | `frontend-call` |
| `POST` | `/api/ddns/webhooktest` | `mutating` | `key` | 有 | `json` | `frontend-call` |
| `DELETE` | `/api/ddns/{param}/{param2}` | `mutating` | — | `deleteFromProvider` | `json` | `frontend-call` |
| `PUT` | `/api/ddns/{param}/{param2}/option/{param3}` | `mutating` | — | — | `json` | `frontend-call` |

## `ddnstasklist`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/ddnstasklist` | `read-only` | — | — | `json` | `frontend-call` |

## `describeviewtree`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `UNKNOWN` | `/api/describeviewtree` | `unknown` | — | — | `unknown` | `route-literal-only` |

## `dlnaservice`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/dlnaservice/configure` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/dlnaservice/configure` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/dlnaservice/lastlogs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `GET` | `/api/dlnaservice/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `GET` | `/api/dlnaservice/status` | `read-only` | — | — | `json` | `frontend-call` |

## `docker`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `POST` | `/api/docker/compose/backup` | `dangerous` | — | `project_name`, `project_path` | `json` | `frontend-call` |
| `GET` | `/api/docker/compose/backup/status` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/docker/compose/config` | `mutating` | — | `project_path` | `json` | `frontend-call` |
| `GET` | `/api/docker/compose/containers-for-cron` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/docker/compose/discover` | `mutating` | — | `scan_path` | `json` | `frontend-call` |
| `POST` | `/api/docker/compose/dockerfile` | `mutating` | — | `project_path` | `json` | `frontend-call` |
| `POST` | `/api/docker/compose/down` | `dangerous` | — | 有 | `json` | `frontend-call` |
| `POST` | `/api/docker/compose/down-async` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/docker/compose/projects` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/docker/compose/read-file` | `mutating` | — | `filename`, `working_dir` | `json` | `frontend-call` |
| `POST` | `/api/docker/compose/restart` | `dangerous` | — | 有 | `json` | `frontend-call` |
| `POST` | `/api/docker/compose/restore` | `dangerous` | — | 有 | `json` | `frontend-call` |
| `POST` | `/api/docker/compose/start` | `dangerous` | — | 有 | `json` | `frontend-call` |
| `POST` | `/api/docker/compose/stop` | `dangerous` | — | 有 | `json` | `frontend-call` |
| `POST` | `/api/docker/compose/stop-async` | `mutating` | — | 有 | `json` | `frontend-call` |
| `POST` | `/api/docker/compose/up` | `mutating` | — | 有 | `json` | `frontend-call` |
| `POST` | `/api/docker/compose/up-async` | `mutating` | — | 有 | `json` | `frontend-call` |
| `POST` | `/api/docker/compose/update-config` | `mutating` | — | `content`, `project_path` | `json` | `frontend-call` |
| `POST` | `/api/docker/compose/update-dockerfile` | `mutating` | — | `content`, `project_path` | `json` | `frontend-call` |
| `DELETE` | `/api/docker/compose/{param}/backup/cancel` | `dangerous` | — | — | `json` | `frontend-call` |
| `DELETE` | `/api/docker/compose/{param}/backups` | `mutating` | — | `backup` | `json` | `frontend-call` |
| `GET` | `/api/docker/compose/{param}/backups` | `read-only` | — | — | `json` | `frontend-call` |
| `DELETE` | `/api/docker/compose/{param}/backups/all` | `mutating` | — | — | `json` | `frontend-call` |
| `GET` | `/api/docker/compose/{param}/backups/download.tar.gz` | `read-only` | `backup` | — | `blob` | `frontend-call` |
| `POST` | `/api/docker/compose/{param}/backups/restore` | `dangerous` | — | `backup` | `json` | `frontend-call` |
| `POST` | `/api/docker/compose/{param}/backups/upload` | `dangerous` | — | 有 | `json` | `frontend-call` |
| `POST` | `/api/docker/compose/{param}/logs` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/docker/compose/{param}/ps` | `read-only` | `name`, `path` | — | `json` | `frontend-call` |
| `GET` | `/api/docker/config` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/docker/config` | `mutating` | — | 有 | `json` | `frontend-call` |
| `DELETE` | `/api/docker/container-groups` | `mutating` | `key` | — | `json` | `frontend-call` |
| `GET` | `/api/docker/container-groups` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/docker/container-groups` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/docker/container-groups` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/docker/container-groups/collapsed` | `mutating` | — | `collapsed`, `key` | `json` | `frontend-call` |
| `GET` | `/api/docker/container-groups/collapsed/states` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/docker/container-groups/count` | `read-only` | `groupKey` | — | `json` | `frontend-call` |
| `GET` | `/api/docker/containers` | `read-only` | `all`, `filters`, `includeNetworkMode`, `includeStats` | — | `json` | `frontend-call` |
| `POST` | `/api/docker/containers` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/docker/containers/group` | `mutating` | — | `containerName`, `groupKey` | `json` | `frontend-call` |
| `GET` | `/api/docker/containers/sort-config` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/docker/containers/sort/compose` | `mutating` | — | `containerOrders`, `groupOrder` | `json` | `frontend-call` |
| `PUT` | `/api/docker/containers/sort/custom` | `mutating` | — | `containerGroupMap`, `containerOrders`, `groupOrder` | `json` | `frontend-call` |
| `PUT` | `/api/docker/containers/sort/flat` | `mutating` | — | `orderList` | `json` | `frontend-call` |
| `GET` | `/api/docker/containers/stats-cached` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/docker/containers/switch-version` | `mutating` | — | `container_ids`, `target_image_ref` | `json` | `frontend-call` |
| `DELETE` | `/api/docker/containers/{param}` | `mutating` | `force`, `remove_volumes` | — | `json` | `frontend-call` |
| `GET` | `/api/docker/containers/{param}` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/commit` | `dangerous` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/docker/containers/{param}/compose-config` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/copy` | `dangerous` | — | `name` | `json` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/edit` | `dangerous` | — | 有 | `json` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/export` | `dangerous` | — | — | `blob` | `frontend-call` |
| `DELETE` | `/api/docker/containers/{param}/files` | `mutating` | — | `path`, `recursive` | `json` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/files/chmod` | `dangerous` | — | `path`, `permissions` | `json` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/files/compress` | `dangerous` | — | `output_name`, `output_path`, `paths` | `json` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/files/compress-async` | `mutating` | — | `output_name`, `output_path`, `paths` | `json` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/files/copy` | `dangerous` | — | `dst_path`, `src_path` | `json` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/files/decompress` | `dangerous` | — | `file_path`, `output_path` | `json` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/files/decompress-async` | `mutating` | — | `file_path`, `output_path` | `json` | `frontend-call` |
| `GET` | `/api/docker/containers/{param}/files/download` | `read-only` | `path` | — | `blob` | `frontend-call` |
| `GET` | `/api/docker/containers/{param}/files/list` | `read-only` | `path` | — | `json` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/files/mkdir` | `mutating` | — | `path` | `json` | `frontend-call` |
| `GET` | `/api/docker/containers/{param}/files/preview-archive` | `read-only` | `path` | — | `json` | `frontend-call` |
| `GET` | `/api/docker/containers/{param}/files/read` | `read-only` | `path` | — | `json` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/files/rename` | `dangerous` | — | `new_path`, `old_path` | `json` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/files/search` | `mutating` | — | `file_type`, `keyword`, `max_depth`, `max_result`, `path` | `json` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/files/touch` | `mutating` | — | `path` | `json` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/files/upload` | `dangerous` | — | 有 | `json` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/files/write` | `dangerous` | — | `content`, `path` | `json` | `frontend-call` |
| `DELETE` | `/api/docker/containers/{param}/label` | `mutating` | — | — | `json` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/label` | `mutating` | — | `label` | `json` | `frontend-call` |
| `GET` | `/api/docker/containers/{param}/logs` | `read-only` | `tail`, `timestamps` | — | `json` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/pause` | `mutating` | — | — | `json` | `frontend-call` |
| `GET` | `/api/docker/containers/{param}/processes` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/rename` | `dangerous` | — | `name` | `json` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/restart` | `dangerous` | — | `timeout` | `json` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/start` | `dangerous` | — | — | `json` | `frontend-call` |
| `GET` | `/api/docker/containers/{param}/stats` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/docker/containers/{param}/stats-cached` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/stop` | `dangerous` | — | `timeout` | `json` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/unpause` | `dangerous` | — | — | `json` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/upgrade` | `dangerous` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/docker/containers/{param}/upgrade-check` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/docker/disk-usage` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/docker/images` | `read-only` | `all` | — | `json` | `frontend-call` |
| `POST` | `/api/docker/images/backup-tag` | `mutating` | — | `image_ref` | `json` | `frontend-call` |
| `POST` | `/api/docker/images/build` | `mutating` | — | 有 | `json` | `frontend-call` |
| `POST` | `/api/docker/images/build-from-git` | `mutating` | — | 有 | `json` | `frontend-call` |
| `POST` | `/api/docker/images/build-from-zip` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/docker/images/containers` | `read-only` | `image_ref` | — | `json` | `frontend-call` |
| `POST` | `/api/docker/images/import` | `dangerous` | — | 有 | `json` | `frontend-call` |
| `POST` | `/api/docker/images/load` | `mutating` | — | 有 | `json` | `frontend-call` |
| `POST` | `/api/docker/images/pull` | `mutating` | — | `image`, `tag` | `json` | `frontend-call` |
| `POST` | `/api/docker/images/pull-async` | `mutating` | — | `architecture`, `image`, `tag` | `json` | `frontend-call` |
| `POST` | `/api/docker/images/pull-with-backup` | `mutating` | — | `architecture`, `backup_tag`, `image_ref` | `json` | `frontend-call` |
| `POST` | `/api/docker/images/pull-with-backup-async` | `mutating` | — | `architecture`, `backup_tag`, `image_ref` | `json` | `frontend-call` |
| `POST` | `/api/docker/images/push` | `mutating` | — | `image`, `tag` | `json` | `frontend-call` |
| `DELETE` | `/api/docker/images/remove` | `dangerous` | `force`, `noprune`, `tag` | — | `json` | `frontend-call` |
| `POST` | `/api/docker/images/remove-saved-digest` | `mutating` | — | `image_id` | `json` | `frontend-call` |
| `UNKNOWN` | `/api/docker/images/save.withoutcompression` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `POST` | `/api/docker/images/search` | `mutating` | — | `limit`, `term` | `json` | `frontend-call` |
| `POST` | `/api/docker/images/upgrade-check` | `mutating` | — | `image_ref` | `json` | `frontend-call` |
| `UNKNOWN` | `/api/docker/images/upgrade-check-ws` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `POST` | `/api/docker/images/upgrade-containers` | `mutating` | — | `container_ids`, `image_ref`, `upgrade_compose`, `upgrade_standalone` | `json` | `frontend-call` |
| `POST` | `/api/docker/images/upgrade-containers-async` | `mutating` | — | `container_ids`, `image_ref`, `upgrade_compose`, `upgrade_standalone` | `json` | `frontend-call` |
| `POST` | `/api/docker/images/upgrade-dismiss` | `mutating` | — | `image_id`, `image_ref` | `json` | `frontend-call` |
| `DELETE` | `/api/docker/images/upgrade-status` | `mutating` | — | — | `json` | `frontend-call` |
| `GET` | `/api/docker/images/upgrade-status` | `read-only` | — | — | `json` | `frontend-call` |
| `DELETE` | `/api/docker/images/{param}` | `mutating` | `force`, `noprune` | — | `json` | `frontend-call` |
| `GET` | `/api/docker/images/{param}` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/docker/images/{param}/filesystem` | `read-only` | `path` | — | `json` | `frontend-call` |
| `GET` | `/api/docker/images/{param}/history` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/docker/images/{param}/tag` | `mutating` | — | `repository`, `tag` | `json` | `frontend-call` |
| `GET` | `/api/docker/images/{param}/tags` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/docker/info` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/docker/labels` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/docker/labels/{param}/containers` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/docker/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `GET` | `/api/docker/monitor/status` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/docker/networks` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/docker/networks` | `mutating` | — | 有 | `json` | `frontend-call` |
| `DELETE` | `/api/docker/networks/{param}` | `mutating` | — | — | `json` | `frontend-call` |
| `POST` | `/api/docker/prune` | `dangerous` | — | 有 | `json` | `frontend-call` |
| `DELETE` | `/api/docker/registry/mirrors` | `mutating` | — | `mirror` | `json` | `frontend-call` |
| `GET` | `/api/docker/registry/mirrors` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/docker/registry/mirrors` | `mutating` | — | `mirror` | `json` | `frontend-call` |
| `GET` | `/api/docker/self-container` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/docker/summary` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/docker/system-info` | `read-only` | — | — | `json` | `frontend-call` |
| `DELETE` | `/api/docker/tasks` | `mutating` | — | — | `json` | `frontend-call` |
| `GET` | `/api/docker/tasks` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/docker/tasks/image-pull/active` | `read-only` | — | — | `json` | `frontend-call` |
| `DELETE` | `/api/docker/tasks/{param}` | `mutating` | — | — | `json` | `frontend-call` |
| `GET` | `/api/docker/tasks/{param}` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/docker/version` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/docker/volumes` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/docker/volumes` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/docker/volumes/backup/status` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/docker/volumes/export` | `read-only` | `name` | — | `blob` | `frontend-call` |
| `POST` | `/api/docker/volumes/import` | `dangerous` | — | 有 | `json` | `frontend-call` |
| `DELETE` | `/api/docker/volumes/{param}` | `mutating` | — | — | `json` | `frontend-call` |
| `POST` | `/api/docker/volumes/{param}/backup` | `dangerous` | — | — | `json` | `frontend-call` |
| `DELETE` | `/api/docker/volumes/{param}/backup/cancel` | `dangerous` | — | — | `json` | `frontend-call` |
| `DELETE` | `/api/docker/volumes/{param}/backups` | `mutating` | — | `backup` | `json` | `frontend-call` |
| `GET` | `/api/docker/volumes/{param}/backups` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/docker/volumes/{param}/backups/restore` | `dangerous` | — | `backup` | `json` | `frontend-call` |
| `POST` | `/api/docker/volumes/{param}/backups/upload` | `dangerous` | — | 有 | `json` | `frontend-call` |

## `frontend-preferences`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `PUT` | `/api/frontend-preferences` | `mutating` | — | 有 | `json` | `frontend-call` |

## `frp`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `UNKNOWN` | `/api/frp` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `GET` | `/api/frp/list` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/frp/list` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/frp/list` | `mutating` | — | 有 | `json` | `frontend-call` |
| `DELETE` | `/api/frp/list/{param}` | `mutating` | — | — | `json` | `frontend-call` |
| `GET` | `/api/frp/list/{param}` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/frp/list/{param}/{param2}` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/frp/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `PUT` | `/api/frp/orderadjustment` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/frp/{param}/lastlogs` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/frp/{param}/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `GET` | `/api/frp/{param}/proxies` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/frp/{param}/proxies` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/frp/{param}/proxies` | `mutating` | — | 有 | `json` | `frontend-call` |
| `DELETE` | `/api/frp/{param}/proxies/{param2}` | `mutating` | — | — | `json` | `frontend-call` |
| `GET` | `/api/frp/{param}/status` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/frp/{param}/visitors` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/frp/{param}/visitors` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/frp/{param}/visitors` | `mutating` | — | 有 | `json` | `frontend-call` |
| `DELETE` | `/api/frp/{param}/visitors/{param2}` | `mutating` | — | — | `json` | `frontend-call` |

## `ftpserver`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/ftpserver/configure` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/ftpserver/configure` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/ftpserver/lastlogs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `GET` | `/api/ftpserver/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `GET` | `/api/ftpserver/status` | `read-only` | — | — | `json` | `frontend-call` |

## `get-lines`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `UNKNOWN` | `/api/get-lines` | `unknown` | — | — | `unknown` | `route-literal-only` |

## `iconlib`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `UNKNOWN` | `/api/iconlib/icon` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `GET` | `/api/iconlib/icons` | `read-only` | `source` | — | `json` | `frontend-call` |
| `GET` | `/api/iconlib/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `GET` | `/api/iconlib/search` | `read-only` | `keyword`, `source` | — | `json` | `frontend-call` |
| `GET` | `/api/iconlib/sources` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/iconlib/sources` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/iconlib/sources` | `mutating` | — | 有 | `json` | `frontend-call` |
| `DELETE` | `/api/iconlib/sources/{param}` | `mutating` | — | — | `json` | `frontend-call` |
| `GET` | `/api/iconlib/sources/{param}/enable/{param2}` | `mutating` | — | — | `json` | `frontend-call` |

## `info`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/info` | `read-only` | — | — | `json` | `frontend-call` |

## `ipdb`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/ipdb/avalidDBFiles` | `read-only` | `key` | — | `json` | `frontend-call` |
| `GET` | `/api/ipdb/configure` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/ipdb/configure` | `mutating` | — | 有 | `json` | `frontend-call` |
| `DELETE` | `/api/ipdb/dbfile` | `mutating` | `file`, `key` | — | `json` | `frontend-call` |
| `UNKNOWN` | `/api/ipdb/download` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `PUT` | `/api/ipdb/instanceorderadjustment` | `mutating` | — | 有 | `json` | `frontend-call` |
| `DELETE` | `/api/ipdb/item` | `mutating` | `key` | — | `json` | `frontend-call` |
| `POST` | `/api/ipdb/item` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/ipdb/item` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/ipdb/item/{param}/{param2}` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/ipdb/items` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/ipdb/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `GET` | `/api/ipdb/query` | `read-only` | `ip` | — | `json` | `frontend-call` |

## `ipfliter`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/ipfliter/autorecordipconf` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/ipfliter/autorecordipconf` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/ipfliter/list` | `read-only` | — | — | `json` | `frontend-call` |
| `UNKNOWN` | `/api/ipfliter/list/subrulelist` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `UNKNOWN` | `/api/ipfliter/list/subrulelist/order` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `PUT` | `/api/ipfliter/list/subrulelist/order/{param}` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/ipfliter/list/subrulelist/{param}` | `read-only` | — | — | `json` | `frontend-call` |
| `DELETE` | `/api/ipfliter/list/{param}` | `mutating` | — | — | `json` | `frontend-call` |
| `GET` | `/api/ipfliter/list/{param}` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/ipfliter/list/{param}` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/ipfliter/list/{param}` | `mutating` | — | 有 | `json` | `frontend-call` |
| `DELETE` | `/api/ipfliter/list/{param}/{param2}` | `mutating` | — | — | `json` | `frontend-call` |
| `GET` | `/api/ipfliter/list/{param}/{param2}` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/ipfliter/list/{param}/{param2}` | `mutating` | — | 有 | `json` | `frontend-call` |
| `POST` | `/api/ipfliter/list/{param}/{param2}/match` | `mutating` | — | `ip` | `json` | `frontend-call` |
| `GET` | `/api/ipfliter/list/{param}/{param2}/{param3}` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/ipfliter/listlite` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/ipfliter/oneclickrecord` | `read-only` | `ip` | — | `json` | `frontend-call` |
| `GET` | `/api/ipfliter/porttrap/blockedips` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `POST` | `/api/ipfliter/porttrap/blockedips/batch-delete` | `mutating` | — | `ips` | `json` | `frontend-call` |
| `POST` | `/api/ipfliter/porttrap/blockedips/clear` | `dangerous` | — | — | `json` | `frontend-call` |
| `GET` | `/api/ipfliter/porttrap/blockedips/export` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/ipfliter/porttrap/blockedips/refresh-ipinfo` | `mutating` | — | — | `json` | `frontend-call` |
| `GET` | `/api/ipfliter/porttrap/blockedips/search` | `read-only` | `page`, `pageSize`, `q`, `type` | — | `json` | `frontend-call` |
| `DELETE` | `/api/ipfliter/porttrap/blockedips/{param}` | `mutating` | — | — | `json` | `frontend-call` |
| `GET` | `/api/ipfliter/porttrap/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `GET` | `/api/ipfliter/porttrap/stats` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/ipfliter/porttrap/stats/reset` | `dangerous` | — | — | `json` | `frontend-call` |
| `GET` | `/api/ipfliter/porttrapconf` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/ipfliter/porttrapconf` | `mutating` | — | 有 | `json` | `frontend-call` |

## `ipregtest`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/ipregtest` | `read-only` | `ipreg`, `iptype`, `netinterface` | — | `json` | `frontend-call` |

## `local-path-browser`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/local-path-browser/list` | `read-only` | `path`, `showFiles` | — | `json` | `frontend-call` |
| `POST` | `/api/local-path-browser/mkdir` | `mutating` | — | `path` | `json` | `frontend-call` |
| `DELETE` | `/api/local-path-browser/path` | `mutating` | — | `confirmName`, `path` | `json` | `frontend-call` |
| `PUT` | `/api/local-path-browser/rename` | `dangerous` | — | `newName`, `path` | `json` | `frontend-call` |
| `GET` | `/api/local-path-browser/roots` | `read-only` | — | — | `json` | `frontend-call` |

## `login`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `POST` | `/api/login` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/login/challenge` | `read-only` | — | — | `json` | `frontend-call` |

## `logout`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `PUT` | `/api/logout` | `mutating` | — | — | `json` | `frontend-call` |

## `logs`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/logs` | `read-only` | `pre` | — | `json` | `frontend-call` |

## `logscenter`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `UNKNOWN` | `/api/logscenter` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `UNKNOWN` | `/api/logscenter/query` | `unknown` | — | — | `unknown` | `route-literal-only` |

## `lucky`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `PUT` | `/api/lucky/service` | `mutating` | `option` | — | `json` | `frontend-call` |

## `modules`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `PUT` | `/api/modules/hidden` | `mutating` | — | `hiddenModules` | `json` | `frontend-call` |
| `GET` | `/api/modules/list` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/modules/{param}/2fa/config` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/modules/{param}/2fa/config` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/modules/{param}/2fa/status` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/modules/{param}/verify2fa` | `mutating` | — | `code` | `json` | `frontend-call` |

## `natdetect`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `UNKNOWN` | `/api/natdetect/ws` | `unknown` | — | — | `unknown` | `route-literal-only` |

## `netinterfaces`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/netinterfaces` | `read-only` | — | — | `json` | `frontend-call` |

## `oauth`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `POST` | `/api/oauth/login` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/oauth/status` | `read-only` | `code`, `type` | — | `json` | `frontend-call` |
| `UNKNOWN` | `/api/oauth/tmpcode` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `GET` | `/api/oauth/userinfo` | `read-only` | `code`, `type` | — | `json` | `frontend-call` |

## `password`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `PUT` | `/api/password/verify` | `mutating` | — | 有 | `json` | `frontend-call` |

## `portforward`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `DELETE` | `/api/portforward` | `mutating` | `key` | — | `json` | `frontend-call` |
| `POST` | `/api/portforward` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/portforward` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/portforward/configure` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/portforward/configure` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/portforward/enable` | `mutating` | `enable`, `key` | — | `json` | `frontend-call` |
| `PUT` | `/api/portforward/ruleorderadjustment` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/portforward/{param}` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/portforward/{param}/lastlogs` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/portforward/{param}/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |

## `portforwards`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/portforwards` | `read-only` | — | — | `json` | `frontend-call` |

## `portforwards_lite`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/portforwards_lite` | `read-only` | — | — | `json` | `frontend-call` |

## `rclone`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/rclone/globalconfig` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/rclone/globalconfig` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/rclone/itemorderadjustment` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/rclone/lastlogs` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/rclone/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `UNKNOWN` | `/api/rclone/remote` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `GET` | `/api/rclone/remote/{param}` | `read-only` | — | — | `json` | `frontend-call` |
| `DELETE` | `/api/rclone/remotelist` | `mutating` | `key` | — | `json` | `frontend-call` |
| `GET` | `/api/rclone/remotelist` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/rclone/remotelist` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/rclone/remotelist` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/rclone/remotelist/option` | `read-only` | `enable`, `key` | — | `json` | `frontend-call` |
| `GET` | `/api/rclone/remotelistlite` | `read-only` | `vfs` | — | `json` | `frontend-call` |
| `UNKNOWN` | `/api/rclone/sync` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `DELETE` | `/api/rclone/sync/list` | `mutating` | `key` | — | `json` | `frontend-call` |
| `GET` | `/api/rclone/sync/list` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/rclone/sync/list` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/rclone/sync/list` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/rclone/sync/option` | `read-only` | `enable`, `key` | — | `json` | `frontend-call` |
| `UNKNOWN` | `/api/rclone/sync/run` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `POST` | `/api/rclone/sync/run/{param}` | `mutating` | `resync` | — | `json` | `frontend-call` |
| `UNKNOWN` | `/api/rclone/sync/stop` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `POST` | `/api/rclone/sync/stop/{param}` | `dangerous` | — | — | `json` | `frontend-call` |
| `GET` | `/api/rclone/sync/{param}` | `read-only` | — | — | `json` | `frontend-call` |
| `UNKNOWN` | `/api/rclone/third/115pan/authcheck` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `GET` | `/api/rclone/third/115pan/authcheck/{param}` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/rclone/third/115pan/authurl` | `read-only` | `cburl`, `lkbaseurl` | — | `json` | `frontend-call` |
| `GET` | `/api/rclone/third/115pan/authuserlist` | `read-only` | — | — | `json` | `frontend-call` |
| `UNKNOWN` | `/api/rclone/third/115pan/user` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `UNKNOWN` | `/api/rclone/third/alipan/authcheck` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `GET` | `/api/rclone/third/alipan/authcheck/{param}` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/rclone/third/alipan/authurl` | `read-only` | `cburl`, `lkbaseurl` | — | `json` | `frontend-call` |
| `GET` | `/api/rclone/third/alipan/authuserlist` | `read-only` | — | — | `json` | `frontend-call` |
| `UNKNOWN` | `/api/rclone/third/alipan/user` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `UNKNOWN` | `/api/rclone/third/baidupan/authcheck` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `GET` | `/api/rclone/third/baidupan/authcheck/{param}` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/rclone/third/baidupan/authurl` | `read-only` | `cburl`, `lkbaseurl` | — | `json` | `frontend-call` |
| `GET` | `/api/rclone/third/baidupan/authuserlist` | `read-only` | — | — | `json` | `frontend-call` |
| `UNKNOWN` | `/api/rclone/third/baidupan/user` | `unknown` | — | — | `unknown` | `route-literal-only` |

## `reboot_program`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/reboot_program` | `dangerous` | — | — | `json` | `frontend-call` |

## `restoreconfigureconfirm`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/restoreconfigureconfirm` | `mutating` | `key` | — | `json` | `frontend-call` |

## `security-groups`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/security-groups` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/security-groups` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/security-groups/grants` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/security-groups/grants/delete` | `dangerous` | — | `grantKeys` | `json` | `frontend-call` |
| `DELETE` | `/api/security-groups/grants/{param}` | `mutating` | — | — | `json` | `frontend-call` |
| `GET` | `/api/security-groups/lite` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/security-groups/oauth-users` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/security-groups/oauth-users` | `mutating` | — | 有 | `json` | `frontend-call` |
| `DELETE` | `/api/security-groups/oauth-users/{param}` | `mutating` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/security-groups/oauth-users/{param}` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/security-groups/users` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/security-groups/users` | `mutating` | — | 有 | `json` | `frontend-call` |
| `DELETE` | `/api/security-groups/users/{param}` | `mutating` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/security-groups/users/{param}` | `mutating` | — | 有 | `json` | `frontend-call` |
| `DELETE` | `/api/security-groups/{param}` | `mutating` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/security-groups/{param}` | `mutating` | — | 有 | `json` | `frontend-call` |

## `smb`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/smb/configure` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/smb/configure` | `mutating` | — | 有 | `json` | `frontend-call` |
| `POST` | `/api/smb/connections/{param}/disconnect` | `dangerous` | — | — | `json` | `frontend-call` |
| `GET` | `/api/smb/lastlogs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `GET` | `/api/smb/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `GET` | `/api/smb/runtime` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/smb/status` | `read-only` | — | — | `json` | `frontend-call` |

## `ssl`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `DELETE` | `/api/ssl` | `mutating` | `key` | — | `json` | `frontend-call` |
| `GET` | `/api/ssl` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/ssl` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/ssl` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/ssl/credential-sources` | `read-only` | — | — | `json` | `frontend-call` |
| `UNKNOWN` | `/api/ssl/download` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `PUT` | `/api/ssl/flush` | `mutating` | `key` | — | `json` | `frontend-call` |
| `GET` | `/api/ssl/lastlogs` | `read-only` | `key` | — | `json` | `frontend-call` |
| `GET` | `/api/ssl/logs` | `read-only` | `key`, `page`, `pageSize` | — | `json` | `frontend-call` |
| `UNKNOWN` | `/api/ssl/manualsync` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `GET` | `/api/ssl/manualsync/{param}` | `mutating` | — | — | `json` | `frontend-call` |
| `GET` | `/api/ssl/setting` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/ssl/setting` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/ssl/sslorderadjustment` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/ssl/syncclients` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/ssl/{param}` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/ssl/{param}` | `mutating` | `enable` | — | `json` | `frontend-call` |
| `DELETE` | `/api/ssl/{param}/acmecancel` | `mutating` | — | — | `json` | `frontend-call` |

## `status`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/status` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/status/history` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/status/history/clear` | `dangerous` | — | — | `json` | `frontend-call` |
| `GET` | `/api/status/history/meta` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/status/host-connections` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/status/host-overview` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/status/host-process-kill` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/status/host-processes` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/status/module-overview` | `read-only` | — | — | `json` | `frontend-call` |
| `UNKNOWN` | `/api/status/ws` | `unknown` | — | — | `unknown` | `route-literal-only` |

## `storagemanagement`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/storagemanagement/aliyunpan_auth` | `read-only` | `cburl`, `lkurl` | — | `json` | `frontend-call` |
| `UNKNOWN` | `/api/storagemanagement/aliyunpan_auth_check` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `GET` | `/api/storagemanagement/aliyunpan_auth_check/{param}` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/storagemanagement/enable` | `mutating` | `enable`, `key` | — | `json` | `frontend-call` |
| `PUT` | `/api/storagemanagement/itemorderadjustment` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/storagemanagement/lastlogs` | `read-only` | — | — | `json` | `frontend-call` |
| `DELETE` | `/api/storagemanagement/list` | `mutating` | `key` | — | `json` | `frontend-call` |
| `POST` | `/api/storagemanagement/list` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/storagemanagement/list` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/storagemanagement/litelist` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/storagemanagement/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |

## `stun`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `UNKNOWN` | `/api/stun` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `GET` | `/api/stun/configure` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/stun/configure` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/stun/ruleorderadjustment` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/stun/{param}` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/stun/{param}/lastlogs` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/stun/{param}/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |

## `stunrule`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `DELETE` | `/api/stunrule` | `mutating` | `key` | — | `json` | `frontend-call` |
| `POST` | `/api/stunrule` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/stunrule` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/stunrule/enable` | `mutating` | `enable`, `key` | — | `json` | `frontend-call` |
| `POST` | `/api/stunrule/webhooktest` | `mutating` | `key` | 有 | `json` | `frontend-call` |

## `stunrulelist`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/stunrulelist` | `read-only` | — | — | `json` | `frontend-call` |

## `stunrulelist_lite`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/stunrulelist_lite` | `read-only` | — | — | `json` | `frontend-call` |

## `temp-access-tickets`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `UNKNOWN` | `/api/temp-access-tickets` | `unknown` | — | — | `unknown` | `route-literal-only` |

## `third`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `UNKNOWN` | `/api/third/filebrowser/backupdb` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `GET` | `/api/third/filebrowser/configure` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/third/filebrowser/configure` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/third/filebrowser/lastlogs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `GET` | `/api/third/filebrowser/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `GET` | `/api/third/filebrowser/resetadmin` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/third/filebrowser/status` | `read-only` | — | — | `json` | `frontend-call` |

## `thirdPartyAuthManager`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/thirdPartyAuthManager/config` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/thirdPartyAuthManager/config` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/thirdPartyAuthManager/list` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/thirdPartyAuthManager/list` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/thirdPartyAuthManager/list` | `mutating` | — | 有 | `json` | `frontend-call` |
| `DELETE` | `/api/thirdPartyAuthManager/list/{param}` | `mutating` | — | — | `json` | `frontend-call` |
| `GET` | `/api/thirdPartyAuthManager/list/{param}` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/thirdPartyAuthManager/list/{param}/{param2}` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/thirdPartyAuthManager/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `PUT` | `/api/thirdPartyAuthManager/orderadjustment` | `mutating` | — | 有 | `json` | `frontend-call` |

## `twofapassword`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/twofapassword` | `read-only` | — | — | `json` | `frontend-call` |

## `update`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/update/cancel` | `dangerous` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/update/comfire` | `dangerous` | — | 有 | `json` | `frontend-call` |

## `upload`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `UNKNOWN` | `/api/upload` | `unknown` | — | — | `unknown` | `route-literal-only` |

## `user`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `UNKNOWN` | `/api/user` | `unknown` | — | — | `unknown` | `route-literal-only` |

## `v2l`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `POST` | `/api/v2l` | `mutating` | — | 有 | `json` | `frontend-call` |

## `webdav`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/webdav/configure` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/webdav/configure` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/webdav/lastlogs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `GET` | `/api/webdav/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `GET` | `/api/webdav/status` | `read-only` | — | — | `json` | `frontend-call` |

## `webservice`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `UNKNOWN` | `/api/webservice` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `POST` | `/api/webservice/cgi` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/webservice/cgi/list` | `read-only` | — | — | `json` | `frontend-call` |
| `DELETE` | `/api/webservice/cgi/{param}` | `mutating` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/webservice/cgi/{param}` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/webservice/cgi/{param}/{param2}` | `mutating` | — | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/discovery/active` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/webservice/discovery/cancel` | `mutating` | — | `jobId` | `json` | `frontend-call` |
| `GET` | `/api/webservice/discovery/latest` | `read-only` | `ruleKey` | — | `json` | `frontend-call` |
| `POST` | `/api/webservice/discovery/start` | `dangerous` | — | 有 | `json` | `frontend-call` |
| `UNKNOWN` | `/api/webservice/discovery/status` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `GET` | `/api/webservice/discovery/status/{param}` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/frontend-state` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/webservice/frontend-state` | `mutating` | — | 有 | `json` | `frontend-call` |
| `DELETE` | `/api/webservice/groups` | `mutating` | `key` | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/groups` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/webservice/groups` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/webservice/groups` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/webservice/groups/orderadjustment` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/webservice/groups/subrulecount` | `read-only` | `groupKey` | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/lastlogs` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/webservice/lightpanel/configtemplate` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/webservice/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `UNKNOWN` | `/api/webservice/rule` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `DELETE` | `/api/webservice/rule/{param}` | `mutating` | — | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/rule/{param}` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/webservice/rule/{param}` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/webservice/rule/{param}/{param2}/{param3}` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/webservice/ruleorderadjustment` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/webservice/rules` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/webservice/rules` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/webservice/rules_lite` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/settings` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/webservice/settings` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/webservice/statistics/capabilities` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/webservice/statistics/clear` | `dangerous` | — | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/statistics/daily` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/statistics/events` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/statistics/export` | `read-only` | — | — | `blob` | `frontend-call` |
| `GET` | `/api/webservice/statistics/geo/aggregate` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/webservice/statistics/geo/rebuild` | `mutating` | — | 有 | `json` | `frontend-call` |
| `POST` | `/api/webservice/statistics/geo/rebuild/cancel` | `mutating` | — | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/statistics/geo/rebuild/status` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/statistics/history` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/webservice/statistics/import` | `dangerous` | `mode` | 有 | `json` | `frontend-call` |
| `POST` | `/api/webservice/statistics/import/cancel` | `dangerous` | — | — | `json` | `frontend-call` |
| `POST` | `/api/webservice/statistics/import/start` | `dangerous` | `mode` | 有 | `json` | `frontend-call` |
| `GET` | `/api/webservice/statistics/import/status` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/statistics/ip-info-refresh` | `mutating` | — | — | `json` | `frontend-call` |
| `POST` | `/api/webservice/statistics/ip-info-refresh` | `mutating` | — | 有 | `json` | `frontend-call` |
| `POST` | `/api/webservice/statistics/ip-info-refresh/cancel` | `mutating` | — | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/statistics/ip-profile` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/statistics/meta` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/statistics/rankings` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/statistics/realtime` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/statistics/recent-ips` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/statistics/recent-ips/visits` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/statistics/summary` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/statistics/waf/events` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/statistics/waf/summary` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/webauth/sessions` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/webservice/webauth/sessions/clear-subrule` | `mutating` | — | `ruleKey`, `subRuleKey` | `json` | `frontend-call` |
| `POST` | `/api/webservice/webauth/sessions/delete` | `dangerous` | — | 有 | `json` | `frontend-call` |
| `DELETE` | `/api/webservice/webauth/sessions/{param}` | `mutating` | — | — | `json` | `frontend-call` |
| `DELETE` | `/api/webservice/{param}/disconnect/{param2}` | `dangerous` | — | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/{param}/httpserver/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `PUT` | `/api/webservice/{param}/subrulegrouporderupdate` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/webservice/{param}/{param2}/accessdetail` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/{param}/{param2}/corazalogs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/{param}/{param2}/lastlogs` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/webservice/{param}/{param2}/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `DELETE` | `/api/webservice/{param}/{param2}/updatefolder/cancel/{param3}` | `mutating` | — | — | `json` | `frontend-call` |
| `POST` | `/api/webservice/{param}/{param2}/updatefolder/confirm` | `mutating` | — | `tempId` | `json` | `frontend-call` |
| `POST` | `/api/webservice/{param}/{param2}/updatefolder/upload` | `dangerous` | — | 有 | `json` | `frontend-call` |

## `webterminal`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/webterminal/config` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/webterminal/config` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/webterminal/connectionorderadjustment` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/webterminal/connections` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/webterminal/connections` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/webterminal/connections` | `mutating` | — | 有 | `json` | `frontend-call` |
| `POST` | `/api/webterminal/connections/test` | `mutating` | — | 有 | `json` | `frontend-call` |
| `DELETE` | `/api/webterminal/connections/{param}` | `mutating` | — | — | `json` | `frontend-call` |
| `GET` | `/api/webterminal/connections/{param}` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/webterminal/connections/{param}/quickaccess` | `mutating` | — | `quickAccessDirs` | `json` | `frontend-call` |
| `DELETE` | `/api/webterminal/connections/{param}/ssh-host-key` | `mutating` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/webterminal/connections/{param}/ssh-host-key` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/webterminal/globalshortcuts` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/webterminal/globalshortcuts` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/webterminal/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `GET` | `/api/webterminal/sessions` | `read-only` | — | — | `json` | `frontend-call` |
| `DELETE` | `/api/webterminal/sessions/{param}` | `mutating` | — | — | `json` | `frontend-call` |
| `GET` | `/api/webterminal/sessions/{param}` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/webterminal/sessions/{param}/remark` | `mutating` | — | `remark` | `json` | `frontend-call` |
| `GET` | `/api/webterminal/sessions/{param}/stats` | `read-only` | — | — | `json` | `frontend-call` |
| `UNKNOWN` | `/api/webterminal/sftp` | `unknown` | — | — | `unknown` | `route-literal-only` |
| `POST` | `/api/webterminal/sftp/{param}/chmod` | `dangerous` | — | `path`, `permissions` | `json` | `frontend-call` |
| `POST` | `/api/webterminal/sftp/{param}/compress` | `dangerous` | — | `output_name`, `output_path`, `paths` | `json` | `frontend-call` |
| `POST` | `/api/webterminal/sftp/{param}/copy` | `dangerous` | — | `dst_path`, `src_path` | `json` | `frontend-call` |
| `POST` | `/api/webterminal/sftp/{param}/decompress` | `dangerous` | — | `file_path`, `output_path` | `json` | `frontend-call` |
| `GET` | `/api/webterminal/sftp/{param}/list` | `read-only` | `path` | — | `json` | `frontend-call` |
| `POST` | `/api/webterminal/sftp/{param}/mkdir` | `mutating` | — | `path` | `json` | `frontend-call` |
| `GET` | `/api/webterminal/sftp/{param}/preview-archive` | `read-only` | `path` | — | `json` | `frontend-call` |
| `GET` | `/api/webterminal/sftp/{param}/read` | `read-only` | `path` | — | `json` | `frontend-call` |
| `DELETE` | `/api/webterminal/sftp/{param}/remove` | `dangerous` | `path` | — | `json` | `frontend-call` |
| `POST` | `/api/webterminal/sftp/{param}/rename` | `dangerous` | — | `newPath`, `oldPath` | `json` | `frontend-call` |
| `POST` | `/api/webterminal/sftp/{param}/touch` | `mutating` | — | `path` | `json` | `frontend-call` |
| `POST` | `/api/webterminal/sftp/{param}/upload` | `dangerous` | — | 有 | `json` | `frontend-call` |
| `POST` | `/api/webterminal/sftp/{param}/upload-streaming` | `mutating` | `filename`, `path` | 有 | `json` | `frontend-call` |
| `POST` | `/api/webterminal/sftp/{param}/write` | `dangerous` | — | `content`, `path` | `json` | `frontend-call` |
| `GET` | `/api/webterminal/shells` | `read-only` | — | — | `json` | `frontend-call` |
| `DELETE` | `/api/webterminal/splitlayout` | `mutating` | — | — | `json` | `frontend-call` |
| `GET` | `/api/webterminal/splitlayout` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/webterminal/splitlayout` | `mutating` | — | 有 | `json` | `frontend-call` |

## `wol`

| 方法 | 路径 | 风险 | 查询字段 | 请求体 | 响应 | 证据等级 |
|---|---|---|---|---|---|---|
| `GET` | `/api/wol/client/state` | `read-only` | — | — | `json` | `frontend-call` |
| `DELETE` | `/api/wol/device` | `mutating` | `key` | — | `json` | `frontend-call` |
| `POST` | `/api/wol/device` | `mutating` | — | 有 | `json` | `frontend-call` |
| `PUT` | `/api/wol/device` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/wol/device/shutdown` | `dangerous` | `key` | — | `json` | `frontend-call` |
| `GET` | `/api/wol/device/wakeup` | `mutating` | `key` | — | `json` | `frontend-call` |
| `PUT` | `/api/wol/deviceorderadjustment` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/wol/devices` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/wol/devices_lite` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/wol/lastlogs` | `read-only` | — | — | `json` | `frontend-call` |
| `GET` | `/api/wol/logs` | `read-only` | `page`, `pageSize` | — | `json` | `frontend-call` |
| `GET` | `/api/wol/service/configure` | `read-only` | — | — | `json` | `frontend-call` |
| `PUT` | `/api/wol/service/configure` | `mutating` | — | 有 | `json` | `frontend-call` |
| `GET` | `/api/wol/service/getipv4interface` | `read-only` | — | — | `json` | `frontend-call` |
| `POST` | `/api/wol/webhooktest` | `mutating` | — | 有 | `json` | `frontend-call` |

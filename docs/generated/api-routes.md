# API 路由参考

> 目标版本：Lucky 3.0.0。共收录 623 个“路径 + 方法”记录。
> 此表由前端构建产物静态生成，不代表上游承诺的稳定公共 API；`UNKNOWN` 表示只发现路径字面量。

## `2fa`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `PUT` | `/api/2fa/setting` | — | 有 | `frontend-call` |

## `about-content`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/about-content` | — | — | `frontend-call` |
| `PUT` | `/api/about-content` | — | 有 | `frontend-call` |

## `baseconfigure`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/baseconfigure` | — | — | `frontend-call` |
| `PUT` | `/api/baseconfigure` | — | 有 | `frontend-call` |

## `cloudflared`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `UNKNOWN` | `/api/cloudflared` | — | — | `route-literal-only` |
| `GET` | `/api/cloudflared/list` | — | — | `frontend-call` |
| `POST` | `/api/cloudflared/list` | — | 有 | `frontend-call` |
| `PUT` | `/api/cloudflared/list` | — | 有 | `frontend-call` |
| `DELETE` | `/api/cloudflared/list/{param}` | — | — | `frontend-call` |
| `GET` | `/api/cloudflared/list/{param}` | — | — | `frontend-call` |
| `GET` | `/api/cloudflared/list/{param}/{param2}` | — | — | `frontend-call` |
| `GET` | `/api/cloudflared/logs` | `page`, `pageSize` | — | `frontend-call` |
| `PUT` | `/api/cloudflared/orderadjustment` | — | 有 | `frontend-call` |
| `GET` | `/api/cloudflared/{param}/cname/check` | `hostname` | — | `frontend-call` |
| `POST` | `/api/cloudflared/{param}/cname/create` | — | 有 | `frontend-call` |
| `DELETE` | `/api/cloudflared/{param}/cname/delete` | `hostname` | — | `frontend-call` |
| `DELETE` | `/api/cloudflared/{param}/ingress` | `hostname`, `path` | — | `frontend-call` |
| `GET` | `/api/cloudflared/{param}/ingress` | — | — | `frontend-call` |
| `POST` | `/api/cloudflared/{param}/ingress` | — | 有 | `frontend-call` |
| `PUT` | `/api/cloudflared/{param}/ingress` | — | 有 | `frontend-call` |
| `GET` | `/api/cloudflared/{param}/lastlogs` | — | — | `frontend-call` |
| `GET` | `/api/cloudflared/{param}/logs` | `page`, `pageSize` | — | `frontend-call` |

## `configure`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `UNKNOWN` | `/api/configure` | — | — | `route-literal-only` |

## `coraza`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/coraza/OWASPCoreRuleset` | — | — | `frontend-call` |
| `GET` | `/api/coraza/instancelist` | — | — | `frontend-call` |
| `PUT` | `/api/coraza/instanceorderadjustment` | — | 有 | `frontend-call` |
| `GET` | `/api/coraza/list` | — | — | `frontend-call` |
| `POST` | `/api/coraza/list` | — | 有 | `frontend-call` |
| `PUT` | `/api/coraza/list` | — | 有 | `frontend-call` |
| `DELETE` | `/api/coraza/list/{param}` | — | — | `frontend-call` |
| `GET` | `/api/coraza/list/{param}` | — | — | `frontend-call` |
| `GET` | `/api/coraza/list/{param}/{param2}` | — | — | `frontend-call` |
| `GET` | `/api/coraza/logs` | `page`, `pageSize` | — | `frontend-call` |

## `cron`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/cron/dojobs` | `key` | — | `frontend-call` |
| `GET` | `/api/cron/enable` | `enable`, `key` | — | `frontend-call` |
| `GET` | `/api/cron/expressioncheck` | `expression` | — | `frontend-call` |
| `DELETE` | `/api/cron/groups` | `key` | — | `frontend-call` |
| `GET` | `/api/cron/groups` | — | — | `frontend-call` |
| `POST` | `/api/cron/groups` | — | 有 | `frontend-call` |
| `PUT` | `/api/cron/groups` | — | 有 | `frontend-call` |
| `PUT` | `/api/cron/groups/collapsed` | — | `collapsed`, `key` | `frontend-call` |
| `GET` | `/api/cron/groups/collapsed/states` | — | — | `frontend-call` |
| `PUT` | `/api/cron/groups/orderadjustment` | — | 有 | `frontend-call` |
| `GET` | `/api/cron/groups/taskcount` | `groupKey` | — | `frontend-call` |
| `POST` | `/api/cron/jobs/trigger` | — | `cronKey`, `jobIndex` | `frontend-call` |
| `GET` | `/api/cron/lastlogs` | — | — | `frontend-call` |
| `DELETE` | `/api/cron/list` | `key` | — | `frontend-call` |
| `GET` | `/api/cron/list` | — | — | `frontend-call` |
| `POST` | `/api/cron/list` | — | 有 | `frontend-call` |
| `PUT` | `/api/cron/list` | — | 有 | `frontend-call` |
| `GET` | `/api/cron/logs` | `page`, `pageSize` | — | `frontend-call` |
| `PUT` | `/api/cron/taskgrouporderupdate` | — | 有 | `frontend-call` |

## `ddns`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `DELETE` | `/api/ddns` | `key` | — | `frontend-call` |
| `POST` | `/api/ddns` | — | 有 | `frontend-call` |
| `PUT` | `/api/ddns` | `key` | 有 | `frontend-call` |
| `GET` | `/api/ddns/configure` | — | — | `frontend-call` |
| `PUT` | `/api/ddns/configure` | — | 有 | `frontend-call` |
| `GET` | `/api/ddns/credential-sources` | — | — | `frontend-call` |
| `GET` | `/api/ddns/enable` | `enable`, `key` | — | `frontend-call` |
| `GET` | `/api/ddns/expanded` | `expanded`, `key` | — | `frontend-call` |
| `GET` | `/api/ddns/getipfromcmdtest` | `command`, `iptype` | — | `frontend-call` |
| `GET` | `/api/ddns/ipsectionexpanded` | `expanded`, `key` | — | `frontend-call` |
| `GET` | `/api/ddns/lastlogs` | — | — | `frontend-call` |
| `GET` | `/api/ddns/logs` | `page`, `pageSize` | — | `frontend-call` |
| `UNKNOWN` | `/api/ddns/manualSync` | — | — | `route-literal-only` |
| `GET` | `/api/ddns/manualSync/{param}` | — | — | `frontend-call` |
| `GET` | `/api/ddns/odhcpdclients` | — | — | `frontend-call` |
| `UNKNOWN` | `/api/ddns/recordOrderadjustment` | — | — | `route-literal-only` |
| `PUT` | `/api/ddns/recordOrderadjustment/{param}` | — | 有 | `frontend-call` |
| `UNKNOWN` | `/api/ddns/task` | — | — | `route-literal-only` |
| `GET` | `/api/ddns/task/{param}` | — | — | `frontend-call` |
| `PUT` | `/api/ddns/taskorderadjustment` | — | 有 | `frontend-call` |
| `POST` | `/api/ddns/webhooktest` | `key` | 有 | `frontend-call` |
| `DELETE` | `/api/ddns/{param}/{param2}` | — | `deleteFromProvider` | `frontend-call` |
| `PUT` | `/api/ddns/{param}/{param2}/option/{param3}` | — | — | `frontend-call` |

## `ddnstasklist`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/ddnstasklist` | — | — | `frontend-call` |

## `describeviewtree`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `UNKNOWN` | `/api/describeviewtree` | — | — | `route-literal-only` |

## `dlnaservice`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/dlnaservice/configure` | — | — | `frontend-call` |
| `PUT` | `/api/dlnaservice/configure` | — | 有 | `frontend-call` |
| `GET` | `/api/dlnaservice/lastlogs` | `page`, `pageSize` | — | `frontend-call` |
| `GET` | `/api/dlnaservice/logs` | `page`, `pageSize` | — | `frontend-call` |
| `GET` | `/api/dlnaservice/status` | — | — | `frontend-call` |

## `docker`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `POST` | `/api/docker/compose/backup` | — | `project_name`, `project_path` | `frontend-call` |
| `GET` | `/api/docker/compose/backup/status` | — | — | `frontend-call` |
| `POST` | `/api/docker/compose/config` | — | `project_path` | `frontend-call` |
| `GET` | `/api/docker/compose/containers-for-cron` | — | — | `frontend-call` |
| `POST` | `/api/docker/compose/discover` | — | `scan_path` | `frontend-call` |
| `POST` | `/api/docker/compose/dockerfile` | — | `project_path` | `frontend-call` |
| `POST` | `/api/docker/compose/down` | — | 有 | `frontend-call` |
| `POST` | `/api/docker/compose/down-async` | — | 有 | `frontend-call` |
| `GET` | `/api/docker/compose/projects` | — | — | `frontend-call` |
| `POST` | `/api/docker/compose/read-file` | — | `filename`, `working_dir` | `frontend-call` |
| `POST` | `/api/docker/compose/restart` | — | 有 | `frontend-call` |
| `POST` | `/api/docker/compose/restore` | — | 有 | `frontend-call` |
| `POST` | `/api/docker/compose/start` | — | 有 | `frontend-call` |
| `POST` | `/api/docker/compose/stop` | — | 有 | `frontend-call` |
| `POST` | `/api/docker/compose/stop-async` | — | 有 | `frontend-call` |
| `POST` | `/api/docker/compose/up` | — | 有 | `frontend-call` |
| `POST` | `/api/docker/compose/up-async` | — | 有 | `frontend-call` |
| `POST` | `/api/docker/compose/update-config` | — | `content`, `project_path` | `frontend-call` |
| `POST` | `/api/docker/compose/update-dockerfile` | — | `content`, `project_path` | `frontend-call` |
| `DELETE` | `/api/docker/compose/{param}/backup/cancel` | — | — | `frontend-call` |
| `DELETE` | `/api/docker/compose/{param}/backups` | — | `backup` | `frontend-call` |
| `GET` | `/api/docker/compose/{param}/backups` | — | — | `frontend-call` |
| `DELETE` | `/api/docker/compose/{param}/backups/all` | — | — | `frontend-call` |
| `GET` | `/api/docker/compose/{param}/backups/download.tar.gz` | `backup` | — | `frontend-call` |
| `POST` | `/api/docker/compose/{param}/backups/restore` | — | `backup` | `frontend-call` |
| `POST` | `/api/docker/compose/{param}/backups/upload` | — | 有 | `frontend-call` |
| `POST` | `/api/docker/compose/{param}/logs` | — | 有 | `frontend-call` |
| `GET` | `/api/docker/compose/{param}/ps` | `name`, `path` | — | `frontend-call` |
| `GET` | `/api/docker/config` | — | — | `frontend-call` |
| `POST` | `/api/docker/config` | — | 有 | `frontend-call` |
| `DELETE` | `/api/docker/container-groups` | `key` | — | `frontend-call` |
| `GET` | `/api/docker/container-groups` | — | — | `frontend-call` |
| `POST` | `/api/docker/container-groups` | — | 有 | `frontend-call` |
| `PUT` | `/api/docker/container-groups` | — | 有 | `frontend-call` |
| `PUT` | `/api/docker/container-groups/collapsed` | — | `collapsed`, `key` | `frontend-call` |
| `GET` | `/api/docker/container-groups/collapsed/states` | — | — | `frontend-call` |
| `GET` | `/api/docker/container-groups/count` | `groupKey` | — | `frontend-call` |
| `GET` | `/api/docker/containers` | `all`, `filters`, `includeNetworkMode`, `includeStats` | — | `frontend-call` |
| `POST` | `/api/docker/containers` | — | 有 | `frontend-call` |
| `PUT` | `/api/docker/containers/group` | — | `containerName`, `groupKey` | `frontend-call` |
| `GET` | `/api/docker/containers/sort-config` | — | — | `frontend-call` |
| `PUT` | `/api/docker/containers/sort/compose` | — | `containerOrders`, `groupOrder` | `frontend-call` |
| `PUT` | `/api/docker/containers/sort/custom` | — | `containerGroupMap`, `containerOrders`, `groupOrder` | `frontend-call` |
| `PUT` | `/api/docker/containers/sort/flat` | — | `orderList` | `frontend-call` |
| `GET` | `/api/docker/containers/stats-cached` | — | — | `frontend-call` |
| `POST` | `/api/docker/containers/switch-version` | — | `container_ids`, `target_image_ref` | `frontend-call` |
| `DELETE` | `/api/docker/containers/{param}` | `force`, `remove_volumes` | — | `frontend-call` |
| `GET` | `/api/docker/containers/{param}` | — | — | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/commit` | — | 有 | `frontend-call` |
| `GET` | `/api/docker/containers/{param}/compose-config` | — | — | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/copy` | — | `name` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/edit` | — | 有 | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/export` | — | — | `frontend-call` |
| `DELETE` | `/api/docker/containers/{param}/files` | — | `path`, `recursive` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/files/chmod` | — | `path`, `permissions` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/files/compress` | — | `output_name`, `output_path`, `paths` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/files/compress-async` | — | `output_name`, `output_path`, `paths` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/files/copy` | — | `dst_path`, `src_path` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/files/decompress` | — | `file_path`, `output_path` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/files/decompress-async` | — | `file_path`, `output_path` | `frontend-call` |
| `GET` | `/api/docker/containers/{param}/files/download` | `path` | — | `frontend-call` |
| `GET` | `/api/docker/containers/{param}/files/list` | `path` | — | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/files/mkdir` | — | `path` | `frontend-call` |
| `GET` | `/api/docker/containers/{param}/files/preview-archive` | `path` | — | `frontend-call` |
| `GET` | `/api/docker/containers/{param}/files/read` | `path` | — | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/files/rename` | — | `new_path`, `old_path` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/files/search` | — | `file_type`, `keyword`, `max_depth`, `max_result`, `path` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/files/touch` | — | `path` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/files/upload` | — | 有 | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/files/write` | — | `content`, `path` | `frontend-call` |
| `DELETE` | `/api/docker/containers/{param}/label` | — | — | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/label` | — | `label` | `frontend-call` |
| `GET` | `/api/docker/containers/{param}/logs` | `tail`, `timestamps` | — | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/pause` | — | — | `frontend-call` |
| `GET` | `/api/docker/containers/{param}/processes` | — | — | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/rename` | — | `name` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/restart` | — | `timeout` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/start` | — | — | `frontend-call` |
| `GET` | `/api/docker/containers/{param}/stats` | — | — | `frontend-call` |
| `GET` | `/api/docker/containers/{param}/stats-cached` | — | — | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/stop` | — | `timeout` | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/unpause` | — | — | `frontend-call` |
| `POST` | `/api/docker/containers/{param}/upgrade` | — | 有 | `frontend-call` |
| `GET` | `/api/docker/containers/{param}/upgrade-check` | — | — | `frontend-call` |
| `GET` | `/api/docker/disk-usage` | — | — | `frontend-call` |
| `GET` | `/api/docker/images` | `all` | — | `frontend-call` |
| `POST` | `/api/docker/images/backup-tag` | — | `image_ref` | `frontend-call` |
| `POST` | `/api/docker/images/build` | — | 有 | `frontend-call` |
| `POST` | `/api/docker/images/build-from-git` | — | 有 | `frontend-call` |
| `POST` | `/api/docker/images/build-from-zip` | — | 有 | `frontend-call` |
| `GET` | `/api/docker/images/containers` | `image_ref` | — | `frontend-call` |
| `POST` | `/api/docker/images/import` | — | 有 | `frontend-call` |
| `POST` | `/api/docker/images/load` | — | 有 | `frontend-call` |
| `POST` | `/api/docker/images/pull` | — | `image`, `tag` | `frontend-call` |
| `POST` | `/api/docker/images/pull-async` | — | `architecture`, `image`, `tag` | `frontend-call` |
| `POST` | `/api/docker/images/pull-with-backup` | — | `architecture`, `backup_tag`, `image_ref` | `frontend-call` |
| `POST` | `/api/docker/images/pull-with-backup-async` | — | `architecture`, `backup_tag`, `image_ref` | `frontend-call` |
| `POST` | `/api/docker/images/push` | — | `image`, `tag` | `frontend-call` |
| `DELETE` | `/api/docker/images/remove` | `force`, `noprune`, `tag` | — | `frontend-call` |
| `POST` | `/api/docker/images/remove-saved-digest` | — | `image_id` | `frontend-call` |
| `UNKNOWN` | `/api/docker/images/save.withoutcompression` | — | — | `route-literal-only` |
| `POST` | `/api/docker/images/search` | — | `limit`, `term` | `frontend-call` |
| `POST` | `/api/docker/images/upgrade-check` | — | `image_ref` | `frontend-call` |
| `UNKNOWN` | `/api/docker/images/upgrade-check-ws` | — | — | `route-literal-only` |
| `POST` | `/api/docker/images/upgrade-containers` | — | `container_ids`, `image_ref`, `upgrade_compose`, `upgrade_standalone` | `frontend-call` |
| `POST` | `/api/docker/images/upgrade-containers-async` | — | `container_ids`, `image_ref`, `upgrade_compose`, `upgrade_standalone` | `frontend-call` |
| `POST` | `/api/docker/images/upgrade-dismiss` | — | `image_id`, `image_ref` | `frontend-call` |
| `DELETE` | `/api/docker/images/upgrade-status` | — | — | `frontend-call` |
| `GET` | `/api/docker/images/upgrade-status` | — | — | `frontend-call` |
| `DELETE` | `/api/docker/images/{param}` | `force`, `noprune` | — | `frontend-call` |
| `GET` | `/api/docker/images/{param}` | — | — | `frontend-call` |
| `GET` | `/api/docker/images/{param}/filesystem` | `path` | — | `frontend-call` |
| `GET` | `/api/docker/images/{param}/history` | — | — | `frontend-call` |
| `POST` | `/api/docker/images/{param}/tag` | — | `repository`, `tag` | `frontend-call` |
| `GET` | `/api/docker/images/{param}/tags` | — | — | `frontend-call` |
| `GET` | `/api/docker/info` | — | — | `frontend-call` |
| `GET` | `/api/docker/labels` | — | — | `frontend-call` |
| `GET` | `/api/docker/labels/{param}/containers` | — | — | `frontend-call` |
| `GET` | `/api/docker/logs` | `page`, `pageSize` | — | `frontend-call` |
| `GET` | `/api/docker/monitor/status` | — | — | `frontend-call` |
| `GET` | `/api/docker/networks` | — | — | `frontend-call` |
| `POST` | `/api/docker/networks` | — | 有 | `frontend-call` |
| `DELETE` | `/api/docker/networks/{param}` | — | — | `frontend-call` |
| `POST` | `/api/docker/prune` | — | 有 | `frontend-call` |
| `DELETE` | `/api/docker/registry/mirrors` | — | `mirror` | `frontend-call` |
| `GET` | `/api/docker/registry/mirrors` | — | — | `frontend-call` |
| `POST` | `/api/docker/registry/mirrors` | — | `mirror` | `frontend-call` |
| `GET` | `/api/docker/self-container` | — | — | `frontend-call` |
| `GET` | `/api/docker/summary` | — | — | `frontend-call` |
| `GET` | `/api/docker/system-info` | — | — | `frontend-call` |
| `DELETE` | `/api/docker/tasks` | — | — | `frontend-call` |
| `GET` | `/api/docker/tasks` | — | — | `frontend-call` |
| `GET` | `/api/docker/tasks/image-pull/active` | — | — | `frontend-call` |
| `DELETE` | `/api/docker/tasks/{param}` | — | — | `frontend-call` |
| `GET` | `/api/docker/tasks/{param}` | — | — | `frontend-call` |
| `GET` | `/api/docker/version` | — | — | `frontend-call` |
| `GET` | `/api/docker/volumes` | — | — | `frontend-call` |
| `POST` | `/api/docker/volumes` | — | 有 | `frontend-call` |
| `GET` | `/api/docker/volumes/backup/status` | — | — | `frontend-call` |
| `GET` | `/api/docker/volumes/export` | `name` | — | `frontend-call` |
| `POST` | `/api/docker/volumes/import` | — | 有 | `frontend-call` |
| `DELETE` | `/api/docker/volumes/{param}` | — | — | `frontend-call` |
| `POST` | `/api/docker/volumes/{param}/backup` | — | — | `frontend-call` |
| `DELETE` | `/api/docker/volumes/{param}/backup/cancel` | — | — | `frontend-call` |
| `DELETE` | `/api/docker/volumes/{param}/backups` | — | `backup` | `frontend-call` |
| `GET` | `/api/docker/volumes/{param}/backups` | — | — | `frontend-call` |
| `POST` | `/api/docker/volumes/{param}/backups/restore` | — | `backup` | `frontend-call` |
| `POST` | `/api/docker/volumes/{param}/backups/upload` | — | 有 | `frontend-call` |

## `frontend-preferences`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `PUT` | `/api/frontend-preferences` | — | 有 | `frontend-call` |

## `frp`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `UNKNOWN` | `/api/frp` | — | — | `route-literal-only` |
| `GET` | `/api/frp/list` | — | — | `frontend-call` |
| `POST` | `/api/frp/list` | — | 有 | `frontend-call` |
| `PUT` | `/api/frp/list` | — | 有 | `frontend-call` |
| `DELETE` | `/api/frp/list/{param}` | — | — | `frontend-call` |
| `GET` | `/api/frp/list/{param}` | — | — | `frontend-call` |
| `GET` | `/api/frp/list/{param}/{param2}` | — | — | `frontend-call` |
| `GET` | `/api/frp/logs` | `page`, `pageSize` | — | `frontend-call` |
| `PUT` | `/api/frp/orderadjustment` | — | 有 | `frontend-call` |
| `GET` | `/api/frp/{param}/lastlogs` | — | — | `frontend-call` |
| `GET` | `/api/frp/{param}/logs` | `page`, `pageSize` | — | `frontend-call` |
| `GET` | `/api/frp/{param}/proxies` | — | — | `frontend-call` |
| `POST` | `/api/frp/{param}/proxies` | — | 有 | `frontend-call` |
| `PUT` | `/api/frp/{param}/proxies` | — | 有 | `frontend-call` |
| `DELETE` | `/api/frp/{param}/proxies/{param2}` | — | — | `frontend-call` |
| `GET` | `/api/frp/{param}/status` | — | — | `frontend-call` |
| `GET` | `/api/frp/{param}/visitors` | — | — | `frontend-call` |
| `POST` | `/api/frp/{param}/visitors` | — | 有 | `frontend-call` |
| `PUT` | `/api/frp/{param}/visitors` | — | 有 | `frontend-call` |
| `DELETE` | `/api/frp/{param}/visitors/{param2}` | — | — | `frontend-call` |

## `ftpserver`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/ftpserver/configure` | — | — | `frontend-call` |
| `PUT` | `/api/ftpserver/configure` | — | 有 | `frontend-call` |
| `GET` | `/api/ftpserver/lastlogs` | `page`, `pageSize` | — | `frontend-call` |
| `GET` | `/api/ftpserver/logs` | `page`, `pageSize` | — | `frontend-call` |
| `GET` | `/api/ftpserver/status` | — | — | `frontend-call` |

## `get-lines`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `UNKNOWN` | `/api/get-lines` | — | — | `route-literal-only` |

## `iconlib`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `UNKNOWN` | `/api/iconlib/icon` | — | — | `route-literal-only` |
| `GET` | `/api/iconlib/icons` | `source` | — | `frontend-call` |
| `GET` | `/api/iconlib/logs` | `page`, `pageSize` | — | `frontend-call` |
| `GET` | `/api/iconlib/search` | `keyword`, `source` | — | `frontend-call` |
| `GET` | `/api/iconlib/sources` | — | — | `frontend-call` |
| `POST` | `/api/iconlib/sources` | — | 有 | `frontend-call` |
| `PUT` | `/api/iconlib/sources` | — | 有 | `frontend-call` |
| `DELETE` | `/api/iconlib/sources/{param}` | — | — | `frontend-call` |
| `GET` | `/api/iconlib/sources/{param}/enable/{param2}` | — | — | `frontend-call` |

## `info`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/info` | — | — | `frontend-call` |

## `ipdb`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/ipdb/avalidDBFiles` | `key` | — | `frontend-call` |
| `GET` | `/api/ipdb/configure` | — | — | `frontend-call` |
| `PUT` | `/api/ipdb/configure` | — | 有 | `frontend-call` |
| `DELETE` | `/api/ipdb/dbfile` | `file`, `key` | — | `frontend-call` |
| `UNKNOWN` | `/api/ipdb/download` | — | — | `route-literal-only` |
| `PUT` | `/api/ipdb/instanceorderadjustment` | — | 有 | `frontend-call` |
| `DELETE` | `/api/ipdb/item` | `key` | — | `frontend-call` |
| `POST` | `/api/ipdb/item` | — | 有 | `frontend-call` |
| `PUT` | `/api/ipdb/item` | — | 有 | `frontend-call` |
| `GET` | `/api/ipdb/item/{param}/{param2}` | — | — | `frontend-call` |
| `GET` | `/api/ipdb/items` | — | — | `frontend-call` |
| `GET` | `/api/ipdb/logs` | `page`, `pageSize` | — | `frontend-call` |
| `GET` | `/api/ipdb/query` | `ip` | — | `frontend-call` |

## `ipfliter`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/ipfliter/autorecordipconf` | — | — | `frontend-call` |
| `PUT` | `/api/ipfliter/autorecordipconf` | — | 有 | `frontend-call` |
| `GET` | `/api/ipfliter/list` | — | — | `frontend-call` |
| `UNKNOWN` | `/api/ipfliter/list/subrulelist` | — | — | `route-literal-only` |
| `UNKNOWN` | `/api/ipfliter/list/subrulelist/order` | — | — | `route-literal-only` |
| `PUT` | `/api/ipfliter/list/subrulelist/order/{param}` | — | 有 | `frontend-call` |
| `GET` | `/api/ipfliter/list/subrulelist/{param}` | — | — | `frontend-call` |
| `DELETE` | `/api/ipfliter/list/{param}` | — | — | `frontend-call` |
| `GET` | `/api/ipfliter/list/{param}` | — | — | `frontend-call` |
| `POST` | `/api/ipfliter/list/{param}` | — | 有 | `frontend-call` |
| `PUT` | `/api/ipfliter/list/{param}` | — | 有 | `frontend-call` |
| `DELETE` | `/api/ipfliter/list/{param}/{param2}` | — | — | `frontend-call` |
| `GET` | `/api/ipfliter/list/{param}/{param2}` | — | — | `frontend-call` |
| `PUT` | `/api/ipfliter/list/{param}/{param2}` | — | 有 | `frontend-call` |
| `POST` | `/api/ipfliter/list/{param}/{param2}/match` | — | `ip` | `frontend-call` |
| `GET` | `/api/ipfliter/list/{param}/{param2}/{param3}` | — | — | `frontend-call` |
| `GET` | `/api/ipfliter/listlite` | — | — | `frontend-call` |
| `GET` | `/api/ipfliter/oneclickrecord` | `ip` | — | `frontend-call` |
| `GET` | `/api/ipfliter/porttrap/blockedips` | `page`, `pageSize` | — | `frontend-call` |
| `POST` | `/api/ipfliter/porttrap/blockedips/batch-delete` | — | `ips` | `frontend-call` |
| `POST` | `/api/ipfliter/porttrap/blockedips/clear` | — | — | `frontend-call` |
| `GET` | `/api/ipfliter/porttrap/blockedips/export` | — | — | `frontend-call` |
| `POST` | `/api/ipfliter/porttrap/blockedips/refresh-ipinfo` | — | — | `frontend-call` |
| `GET` | `/api/ipfliter/porttrap/blockedips/search` | `page`, `pageSize`, `q`, `type` | — | `frontend-call` |
| `DELETE` | `/api/ipfliter/porttrap/blockedips/{param}` | — | — | `frontend-call` |
| `GET` | `/api/ipfliter/porttrap/logs` | `page`, `pageSize` | — | `frontend-call` |
| `GET` | `/api/ipfliter/porttrap/stats` | — | — | `frontend-call` |
| `POST` | `/api/ipfliter/porttrap/stats/reset` | — | — | `frontend-call` |
| `GET` | `/api/ipfliter/porttrapconf` | — | — | `frontend-call` |
| `PUT` | `/api/ipfliter/porttrapconf` | — | 有 | `frontend-call` |

## `ipregtest`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/ipregtest` | `ipreg`, `iptype`, `netinterface` | — | `frontend-call` |

## `local-path-browser`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/local-path-browser/list` | `path`, `showFiles` | — | `frontend-call` |
| `POST` | `/api/local-path-browser/mkdir` | — | `path` | `frontend-call` |
| `DELETE` | `/api/local-path-browser/path` | — | `confirmName`, `path` | `frontend-call` |
| `PUT` | `/api/local-path-browser/rename` | — | `newName`, `path` | `frontend-call` |
| `GET` | `/api/local-path-browser/roots` | — | — | `frontend-call` |

## `login`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `POST` | `/api/login` | — | 有 | `frontend-call` |
| `GET` | `/api/login/challenge` | — | — | `frontend-call` |

## `logout`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `PUT` | `/api/logout` | — | — | `frontend-call` |

## `logs`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/logs` | `pre` | — | `frontend-call` |

## `logscenter`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `UNKNOWN` | `/api/logscenter` | — | — | `route-literal-only` |
| `UNKNOWN` | `/api/logscenter/query` | — | — | `route-literal-only` |

## `lucky`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `PUT` | `/api/lucky/service` | `option` | — | `frontend-call` |

## `modules`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `PUT` | `/api/modules/hidden` | — | `hiddenModules` | `frontend-call` |
| `GET` | `/api/modules/list` | — | — | `frontend-call` |
| `GET` | `/api/modules/{param}/2fa/config` | — | — | `frontend-call` |
| `PUT` | `/api/modules/{param}/2fa/config` | — | 有 | `frontend-call` |
| `GET` | `/api/modules/{param}/2fa/status` | — | — | `frontend-call` |
| `POST` | `/api/modules/{param}/verify2fa` | — | `code` | `frontend-call` |

## `natdetect`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `UNKNOWN` | `/api/natdetect/ws` | — | — | `route-literal-only` |

## `netinterfaces`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/netinterfaces` | — | — | `frontend-call` |

## `oauth`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `POST` | `/api/oauth/login` | — | 有 | `frontend-call` |
| `GET` | `/api/oauth/status` | `code`, `type` | — | `frontend-call` |
| `UNKNOWN` | `/api/oauth/tmpcode` | — | — | `route-literal-only` |
| `GET` | `/api/oauth/userinfo` | `code`, `type` | — | `frontend-call` |

## `password`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `PUT` | `/api/password/verify` | — | 有 | `frontend-call` |

## `portforward`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `DELETE` | `/api/portforward` | `key` | — | `frontend-call` |
| `POST` | `/api/portforward` | — | 有 | `frontend-call` |
| `PUT` | `/api/portforward` | — | 有 | `frontend-call` |
| `GET` | `/api/portforward/configure` | — | — | `frontend-call` |
| `PUT` | `/api/portforward/configure` | — | 有 | `frontend-call` |
| `GET` | `/api/portforward/enable` | `enable`, `key` | — | `frontend-call` |
| `PUT` | `/api/portforward/ruleorderadjustment` | — | 有 | `frontend-call` |
| `GET` | `/api/portforward/{param}` | — | — | `frontend-call` |
| `GET` | `/api/portforward/{param}/lastlogs` | — | — | `frontend-call` |
| `GET` | `/api/portforward/{param}/logs` | `page`, `pageSize` | — | `frontend-call` |

## `portforwards`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/portforwards` | — | — | `frontend-call` |

## `portforwards_lite`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/portforwards_lite` | — | — | `frontend-call` |

## `rclone`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/rclone/globalconfig` | — | — | `frontend-call` |
| `PUT` | `/api/rclone/globalconfig` | — | 有 | `frontend-call` |
| `PUT` | `/api/rclone/itemorderadjustment` | — | 有 | `frontend-call` |
| `GET` | `/api/rclone/lastlogs` | — | — | `frontend-call` |
| `GET` | `/api/rclone/logs` | `page`, `pageSize` | — | `frontend-call` |
| `UNKNOWN` | `/api/rclone/remote` | — | — | `route-literal-only` |
| `GET` | `/api/rclone/remote/{param}` | — | — | `frontend-call` |
| `DELETE` | `/api/rclone/remotelist` | `key` | — | `frontend-call` |
| `GET` | `/api/rclone/remotelist` | — | — | `frontend-call` |
| `POST` | `/api/rclone/remotelist` | — | 有 | `frontend-call` |
| `PUT` | `/api/rclone/remotelist` | — | 有 | `frontend-call` |
| `GET` | `/api/rclone/remotelist/option` | `enable`, `key` | — | `frontend-call` |
| `GET` | `/api/rclone/remotelistlite` | `vfs` | — | `frontend-call` |
| `UNKNOWN` | `/api/rclone/sync` | — | — | `route-literal-only` |
| `DELETE` | `/api/rclone/sync/list` | `key` | — | `frontend-call` |
| `GET` | `/api/rclone/sync/list` | — | — | `frontend-call` |
| `POST` | `/api/rclone/sync/list` | — | 有 | `frontend-call` |
| `PUT` | `/api/rclone/sync/list` | — | 有 | `frontend-call` |
| `GET` | `/api/rclone/sync/option` | `enable`, `key` | — | `frontend-call` |
| `UNKNOWN` | `/api/rclone/sync/run` | — | — | `route-literal-only` |
| `POST` | `/api/rclone/sync/run/{param}` | `resync` | — | `frontend-call` |
| `UNKNOWN` | `/api/rclone/sync/stop` | — | — | `route-literal-only` |
| `POST` | `/api/rclone/sync/stop/{param}` | — | — | `frontend-call` |
| `GET` | `/api/rclone/sync/{param}` | — | — | `frontend-call` |
| `UNKNOWN` | `/api/rclone/third/115pan/authcheck` | — | — | `route-literal-only` |
| `GET` | `/api/rclone/third/115pan/authcheck/{param}` | — | — | `frontend-call` |
| `GET` | `/api/rclone/third/115pan/authurl` | `cburl`, `lkbaseurl` | — | `frontend-call` |
| `GET` | `/api/rclone/third/115pan/authuserlist` | — | — | `frontend-call` |
| `UNKNOWN` | `/api/rclone/third/115pan/user` | — | — | `route-literal-only` |
| `UNKNOWN` | `/api/rclone/third/alipan/authcheck` | — | — | `route-literal-only` |
| `GET` | `/api/rclone/third/alipan/authcheck/{param}` | — | — | `frontend-call` |
| `GET` | `/api/rclone/third/alipan/authurl` | `cburl`, `lkbaseurl` | — | `frontend-call` |
| `GET` | `/api/rclone/third/alipan/authuserlist` | — | — | `frontend-call` |
| `UNKNOWN` | `/api/rclone/third/alipan/user` | — | — | `route-literal-only` |
| `UNKNOWN` | `/api/rclone/third/baidupan/authcheck` | — | — | `route-literal-only` |
| `GET` | `/api/rclone/third/baidupan/authcheck/{param}` | — | — | `frontend-call` |
| `GET` | `/api/rclone/third/baidupan/authurl` | `cburl`, `lkbaseurl` | — | `frontend-call` |
| `GET` | `/api/rclone/third/baidupan/authuserlist` | — | — | `frontend-call` |
| `UNKNOWN` | `/api/rclone/third/baidupan/user` | — | — | `route-literal-only` |

## `reboot_program`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/reboot_program` | — | — | `frontend-call` |

## `restoreconfigureconfirm`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/restoreconfigureconfirm` | `key` | — | `frontend-call` |

## `security-groups`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/security-groups` | — | — | `frontend-call` |
| `POST` | `/api/security-groups` | — | 有 | `frontend-call` |
| `GET` | `/api/security-groups/grants` | — | — | `frontend-call` |
| `POST` | `/api/security-groups/grants/delete` | — | `grantKeys` | `frontend-call` |
| `DELETE` | `/api/security-groups/grants/{param}` | — | — | `frontend-call` |
| `GET` | `/api/security-groups/lite` | — | — | `frontend-call` |
| `GET` | `/api/security-groups/oauth-users` | — | — | `frontend-call` |
| `POST` | `/api/security-groups/oauth-users` | — | 有 | `frontend-call` |
| `DELETE` | `/api/security-groups/oauth-users/{param}` | — | — | `frontend-call` |
| `PUT` | `/api/security-groups/oauth-users/{param}` | — | 有 | `frontend-call` |
| `GET` | `/api/security-groups/users` | — | — | `frontend-call` |
| `POST` | `/api/security-groups/users` | — | 有 | `frontend-call` |
| `DELETE` | `/api/security-groups/users/{param}` | — | — | `frontend-call` |
| `PUT` | `/api/security-groups/users/{param}` | — | 有 | `frontend-call` |
| `DELETE` | `/api/security-groups/{param}` | — | — | `frontend-call` |
| `PUT` | `/api/security-groups/{param}` | — | 有 | `frontend-call` |

## `smb`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/smb/configure` | — | — | `frontend-call` |
| `PUT` | `/api/smb/configure` | — | 有 | `frontend-call` |
| `POST` | `/api/smb/connections/{param}/disconnect` | — | — | `frontend-call` |
| `GET` | `/api/smb/lastlogs` | `page`, `pageSize` | — | `frontend-call` |
| `GET` | `/api/smb/logs` | `page`, `pageSize` | — | `frontend-call` |
| `GET` | `/api/smb/runtime` | — | — | `frontend-call` |
| `GET` | `/api/smb/status` | — | — | `frontend-call` |

## `ssl`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `DELETE` | `/api/ssl` | `key` | — | `frontend-call` |
| `GET` | `/api/ssl` | — | — | `frontend-call` |
| `POST` | `/api/ssl` | — | 有 | `frontend-call` |
| `PUT` | `/api/ssl` | — | 有 | `frontend-call` |
| `GET` | `/api/ssl/credential-sources` | — | — | `frontend-call` |
| `UNKNOWN` | `/api/ssl/download` | — | — | `route-literal-only` |
| `PUT` | `/api/ssl/flush` | `key` | — | `frontend-call` |
| `GET` | `/api/ssl/lastlogs` | `key` | — | `frontend-call` |
| `GET` | `/api/ssl/logs` | `key`, `page`, `pageSize` | — | `frontend-call` |
| `UNKNOWN` | `/api/ssl/manualsync` | — | — | `route-literal-only` |
| `GET` | `/api/ssl/manualsync/{param}` | — | — | `frontend-call` |
| `GET` | `/api/ssl/setting` | — | — | `frontend-call` |
| `PUT` | `/api/ssl/setting` | — | 有 | `frontend-call` |
| `PUT` | `/api/ssl/sslorderadjustment` | — | 有 | `frontend-call` |
| `GET` | `/api/ssl/syncclients` | — | — | `frontend-call` |
| `GET` | `/api/ssl/{param}` | — | — | `frontend-call` |
| `PUT` | `/api/ssl/{param}` | `enable` | — | `frontend-call` |
| `DELETE` | `/api/ssl/{param}/acmecancel` | — | — | `frontend-call` |

## `status`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/status` | — | — | `frontend-call` |
| `GET` | `/api/status/history` | — | — | `frontend-call` |
| `POST` | `/api/status/history/clear` | — | — | `frontend-call` |
| `GET` | `/api/status/history/meta` | — | — | `frontend-call` |
| `GET` | `/api/status/host-connections` | — | — | `frontend-call` |
| `GET` | `/api/status/host-overview` | — | — | `frontend-call` |
| `POST` | `/api/status/host-process-kill` | — | 有 | `frontend-call` |
| `GET` | `/api/status/host-processes` | — | — | `frontend-call` |
| `GET` | `/api/status/module-overview` | — | — | `frontend-call` |
| `UNKNOWN` | `/api/status/ws` | — | — | `route-literal-only` |

## `storagemanagement`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/storagemanagement/aliyunpan_auth` | `cburl`, `lkurl` | — | `frontend-call` |
| `UNKNOWN` | `/api/storagemanagement/aliyunpan_auth_check` | — | — | `route-literal-only` |
| `GET` | `/api/storagemanagement/aliyunpan_auth_check/{param}` | — | — | `frontend-call` |
| `GET` | `/api/storagemanagement/enable` | `enable`, `key` | — | `frontend-call` |
| `PUT` | `/api/storagemanagement/itemorderadjustment` | — | 有 | `frontend-call` |
| `GET` | `/api/storagemanagement/lastlogs` | — | — | `frontend-call` |
| `DELETE` | `/api/storagemanagement/list` | `key` | — | `frontend-call` |
| `POST` | `/api/storagemanagement/list` | — | 有 | `frontend-call` |
| `PUT` | `/api/storagemanagement/list` | — | 有 | `frontend-call` |
| `GET` | `/api/storagemanagement/litelist` | — | — | `frontend-call` |
| `GET` | `/api/storagemanagement/logs` | `page`, `pageSize` | — | `frontend-call` |

## `stun`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `UNKNOWN` | `/api/stun` | — | — | `route-literal-only` |
| `GET` | `/api/stun/configure` | — | — | `frontend-call` |
| `PUT` | `/api/stun/configure` | — | 有 | `frontend-call` |
| `PUT` | `/api/stun/ruleorderadjustment` | — | 有 | `frontend-call` |
| `GET` | `/api/stun/{param}` | — | — | `frontend-call` |
| `GET` | `/api/stun/{param}/lastlogs` | — | — | `frontend-call` |
| `GET` | `/api/stun/{param}/logs` | `page`, `pageSize` | — | `frontend-call` |

## `stunrule`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `DELETE` | `/api/stunrule` | `key` | — | `frontend-call` |
| `POST` | `/api/stunrule` | — | 有 | `frontend-call` |
| `PUT` | `/api/stunrule` | — | 有 | `frontend-call` |
| `GET` | `/api/stunrule/enable` | `enable`, `key` | — | `frontend-call` |
| `POST` | `/api/stunrule/webhooktest` | `key` | 有 | `frontend-call` |

## `stunrulelist`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/stunrulelist` | — | — | `frontend-call` |

## `stunrulelist_lite`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/stunrulelist_lite` | — | — | `frontend-call` |

## `temp-access-tickets`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `UNKNOWN` | `/api/temp-access-tickets` | — | — | `route-literal-only` |

## `third`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `UNKNOWN` | `/api/third/filebrowser/backupdb` | — | — | `route-literal-only` |
| `GET` | `/api/third/filebrowser/configure` | — | — | `frontend-call` |
| `PUT` | `/api/third/filebrowser/configure` | — | 有 | `frontend-call` |
| `GET` | `/api/third/filebrowser/lastlogs` | `page`, `pageSize` | — | `frontend-call` |
| `GET` | `/api/third/filebrowser/logs` | `page`, `pageSize` | — | `frontend-call` |
| `GET` | `/api/third/filebrowser/resetadmin` | — | — | `frontend-call` |
| `GET` | `/api/third/filebrowser/status` | — | — | `frontend-call` |

## `thirdPartyAuthManager`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/thirdPartyAuthManager/config` | — | — | `frontend-call` |
| `PUT` | `/api/thirdPartyAuthManager/config` | — | 有 | `frontend-call` |
| `GET` | `/api/thirdPartyAuthManager/list` | — | — | `frontend-call` |
| `POST` | `/api/thirdPartyAuthManager/list` | — | 有 | `frontend-call` |
| `PUT` | `/api/thirdPartyAuthManager/list` | — | 有 | `frontend-call` |
| `DELETE` | `/api/thirdPartyAuthManager/list/{param}` | — | — | `frontend-call` |
| `GET` | `/api/thirdPartyAuthManager/list/{param}` | — | — | `frontend-call` |
| `GET` | `/api/thirdPartyAuthManager/list/{param}/{param2}` | — | — | `frontend-call` |
| `GET` | `/api/thirdPartyAuthManager/logs` | `page`, `pageSize` | — | `frontend-call` |
| `PUT` | `/api/thirdPartyAuthManager/orderadjustment` | — | 有 | `frontend-call` |

## `twofapassword`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/twofapassword` | — | — | `frontend-call` |

## `update`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/update/cancel` | — | — | `frontend-call` |
| `PUT` | `/api/update/comfire` | — | 有 | `frontend-call` |

## `upload`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `UNKNOWN` | `/api/upload` | — | — | `route-literal-only` |

## `user`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `UNKNOWN` | `/api/user` | — | — | `route-literal-only` |

## `v2l`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `POST` | `/api/v2l` | — | 有 | `frontend-call` |

## `webdav`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/webdav/configure` | — | — | `frontend-call` |
| `PUT` | `/api/webdav/configure` | — | 有 | `frontend-call` |
| `GET` | `/api/webdav/lastlogs` | `page`, `pageSize` | — | `frontend-call` |
| `GET` | `/api/webdav/logs` | `page`, `pageSize` | — | `frontend-call` |
| `GET` | `/api/webdav/status` | — | — | `frontend-call` |

## `webservice`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `UNKNOWN` | `/api/webservice` | — | — | `route-literal-only` |
| `POST` | `/api/webservice/cgi` | — | 有 | `frontend-call` |
| `GET` | `/api/webservice/cgi/list` | — | — | `frontend-call` |
| `DELETE` | `/api/webservice/cgi/{param}` | — | — | `frontend-call` |
| `PUT` | `/api/webservice/cgi/{param}` | — | 有 | `frontend-call` |
| `PUT` | `/api/webservice/cgi/{param}/{param2}` | — | — | `frontend-call` |
| `GET` | `/api/webservice/discovery/active` | — | — | `frontend-call` |
| `POST` | `/api/webservice/discovery/cancel` | — | `jobId` | `frontend-call` |
| `GET` | `/api/webservice/discovery/latest` | `ruleKey` | — | `frontend-call` |
| `POST` | `/api/webservice/discovery/start` | — | 有 | `frontend-call` |
| `UNKNOWN` | `/api/webservice/discovery/status` | — | — | `route-literal-only` |
| `GET` | `/api/webservice/discovery/status/{param}` | — | — | `frontend-call` |
| `GET` | `/api/webservice/frontend-state` | — | — | `frontend-call` |
| `PUT` | `/api/webservice/frontend-state` | — | 有 | `frontend-call` |
| `DELETE` | `/api/webservice/groups` | `key` | — | `frontend-call` |
| `GET` | `/api/webservice/groups` | — | — | `frontend-call` |
| `POST` | `/api/webservice/groups` | — | 有 | `frontend-call` |
| `PUT` | `/api/webservice/groups` | — | 有 | `frontend-call` |
| `PUT` | `/api/webservice/groups/orderadjustment` | — | 有 | `frontend-call` |
| `GET` | `/api/webservice/groups/subrulecount` | `groupKey` | — | `frontend-call` |
| `GET` | `/api/webservice/lastlogs` | — | — | `frontend-call` |
| `POST` | `/api/webservice/lightpanel/configtemplate` | — | 有 | `frontend-call` |
| `GET` | `/api/webservice/logs` | `page`, `pageSize` | — | `frontend-call` |
| `UNKNOWN` | `/api/webservice/rule` | — | — | `route-literal-only` |
| `DELETE` | `/api/webservice/rule/{param}` | — | — | `frontend-call` |
| `GET` | `/api/webservice/rule/{param}` | — | — | `frontend-call` |
| `PUT` | `/api/webservice/rule/{param}` | — | 有 | `frontend-call` |
| `GET` | `/api/webservice/rule/{param}/{param2}/{param3}` | — | — | `frontend-call` |
| `PUT` | `/api/webservice/ruleorderadjustment` | — | 有 | `frontend-call` |
| `GET` | `/api/webservice/rules` | — | — | `frontend-call` |
| `POST` | `/api/webservice/rules` | — | 有 | `frontend-call` |
| `GET` | `/api/webservice/rules_lite` | — | — | `frontend-call` |
| `GET` | `/api/webservice/settings` | — | — | `frontend-call` |
| `PUT` | `/api/webservice/settings` | — | 有 | `frontend-call` |
| `GET` | `/api/webservice/statistics/capabilities` | — | — | `frontend-call` |
| `POST` | `/api/webservice/statistics/clear` | — | — | `frontend-call` |
| `GET` | `/api/webservice/statistics/daily` | — | — | `frontend-call` |
| `GET` | `/api/webservice/statistics/events` | — | — | `frontend-call` |
| `GET` | `/api/webservice/statistics/export` | — | — | `frontend-call` |
| `GET` | `/api/webservice/statistics/geo/aggregate` | — | — | `frontend-call` |
| `POST` | `/api/webservice/statistics/geo/rebuild` | — | 有 | `frontend-call` |
| `POST` | `/api/webservice/statistics/geo/rebuild/cancel` | — | — | `frontend-call` |
| `GET` | `/api/webservice/statistics/geo/rebuild/status` | — | — | `frontend-call` |
| `GET` | `/api/webservice/statistics/history` | — | — | `frontend-call` |
| `POST` | `/api/webservice/statistics/import` | `mode` | 有 | `frontend-call` |
| `POST` | `/api/webservice/statistics/import/cancel` | — | — | `frontend-call` |
| `POST` | `/api/webservice/statistics/import/start` | `mode` | 有 | `frontend-call` |
| `GET` | `/api/webservice/statistics/import/status` | — | — | `frontend-call` |
| `GET` | `/api/webservice/statistics/ip-info-refresh` | — | — | `frontend-call` |
| `POST` | `/api/webservice/statistics/ip-info-refresh` | — | 有 | `frontend-call` |
| `POST` | `/api/webservice/statistics/ip-info-refresh/cancel` | — | — | `frontend-call` |
| `GET` | `/api/webservice/statistics/ip-profile` | — | — | `frontend-call` |
| `GET` | `/api/webservice/statistics/meta` | — | — | `frontend-call` |
| `GET` | `/api/webservice/statistics/rankings` | — | — | `frontend-call` |
| `GET` | `/api/webservice/statistics/realtime` | — | — | `frontend-call` |
| `GET` | `/api/webservice/statistics/recent-ips` | — | — | `frontend-call` |
| `GET` | `/api/webservice/statistics/recent-ips/visits` | — | — | `frontend-call` |
| `GET` | `/api/webservice/statistics/summary` | — | — | `frontend-call` |
| `GET` | `/api/webservice/statistics/waf/events` | — | — | `frontend-call` |
| `GET` | `/api/webservice/statistics/waf/summary` | — | — | `frontend-call` |
| `GET` | `/api/webservice/webauth/sessions` | — | — | `frontend-call` |
| `POST` | `/api/webservice/webauth/sessions/clear-subrule` | — | `ruleKey`, `subRuleKey` | `frontend-call` |
| `POST` | `/api/webservice/webauth/sessions/delete` | — | 有 | `frontend-call` |
| `DELETE` | `/api/webservice/webauth/sessions/{param}` | — | — | `frontend-call` |
| `DELETE` | `/api/webservice/{param}/disconnect/{param2}` | — | — | `frontend-call` |
| `GET` | `/api/webservice/{param}/httpserver/logs` | `page`, `pageSize` | — | `frontend-call` |
| `PUT` | `/api/webservice/{param}/subrulegrouporderupdate` | — | 有 | `frontend-call` |
| `GET` | `/api/webservice/{param}/{param2}/accessdetail` | `page`, `pageSize` | — | `frontend-call` |
| `GET` | `/api/webservice/{param}/{param2}/corazalogs` | `page`, `pageSize` | — | `frontend-call` |
| `GET` | `/api/webservice/{param}/{param2}/lastlogs` | — | — | `frontend-call` |
| `GET` | `/api/webservice/{param}/{param2}/logs` | `page`, `pageSize` | — | `frontend-call` |
| `DELETE` | `/api/webservice/{param}/{param2}/updatefolder/cancel/{param3}` | — | — | `frontend-call` |
| `POST` | `/api/webservice/{param}/{param2}/updatefolder/confirm` | — | `tempId` | `frontend-call` |
| `POST` | `/api/webservice/{param}/{param2}/updatefolder/upload` | — | 有 | `frontend-call` |

## `webterminal`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/webterminal/config` | — | — | `frontend-call` |
| `PUT` | `/api/webterminal/config` | — | 有 | `frontend-call` |
| `PUT` | `/api/webterminal/connectionorderadjustment` | — | 有 | `frontend-call` |
| `GET` | `/api/webterminal/connections` | — | — | `frontend-call` |
| `POST` | `/api/webterminal/connections` | — | 有 | `frontend-call` |
| `PUT` | `/api/webterminal/connections` | — | 有 | `frontend-call` |
| `POST` | `/api/webterminal/connections/test` | — | 有 | `frontend-call` |
| `DELETE` | `/api/webterminal/connections/{param}` | — | — | `frontend-call` |
| `GET` | `/api/webterminal/connections/{param}` | — | — | `frontend-call` |
| `PUT` | `/api/webterminal/connections/{param}/quickaccess` | — | `quickAccessDirs` | `frontend-call` |
| `DELETE` | `/api/webterminal/connections/{param}/ssh-host-key` | — | — | `frontend-call` |
| `PUT` | `/api/webterminal/connections/{param}/ssh-host-key` | — | 有 | `frontend-call` |
| `GET` | `/api/webterminal/globalshortcuts` | — | — | `frontend-call` |
| `PUT` | `/api/webterminal/globalshortcuts` | — | 有 | `frontend-call` |
| `GET` | `/api/webterminal/logs` | `page`, `pageSize` | — | `frontend-call` |
| `GET` | `/api/webterminal/sessions` | — | — | `frontend-call` |
| `DELETE` | `/api/webterminal/sessions/{param}` | — | — | `frontend-call` |
| `GET` | `/api/webterminal/sessions/{param}` | — | — | `frontend-call` |
| `PUT` | `/api/webterminal/sessions/{param}/remark` | — | `remark` | `frontend-call` |
| `GET` | `/api/webterminal/sessions/{param}/stats` | — | — | `frontend-call` |
| `UNKNOWN` | `/api/webterminal/sftp` | — | — | `route-literal-only` |
| `POST` | `/api/webterminal/sftp/{param}/chmod` | — | `path`, `permissions` | `frontend-call` |
| `POST` | `/api/webterminal/sftp/{param}/compress` | — | `output_name`, `output_path`, `paths` | `frontend-call` |
| `POST` | `/api/webterminal/sftp/{param}/copy` | — | `dst_path`, `src_path` | `frontend-call` |
| `POST` | `/api/webterminal/sftp/{param}/decompress` | — | `file_path`, `output_path` | `frontend-call` |
| `GET` | `/api/webterminal/sftp/{param}/list` | `path` | — | `frontend-call` |
| `POST` | `/api/webterminal/sftp/{param}/mkdir` | — | `path` | `frontend-call` |
| `GET` | `/api/webterminal/sftp/{param}/preview-archive` | `path` | — | `frontend-call` |
| `GET` | `/api/webterminal/sftp/{param}/read` | `path` | — | `frontend-call` |
| `DELETE` | `/api/webterminal/sftp/{param}/remove` | `path` | — | `frontend-call` |
| `POST` | `/api/webterminal/sftp/{param}/rename` | — | `newPath`, `oldPath` | `frontend-call` |
| `POST` | `/api/webterminal/sftp/{param}/touch` | — | `path` | `frontend-call` |
| `POST` | `/api/webterminal/sftp/{param}/upload` | — | 有 | `frontend-call` |
| `POST` | `/api/webterminal/sftp/{param}/upload-streaming` | `filename`, `path` | 有 | `frontend-call` |
| `POST` | `/api/webterminal/sftp/{param}/write` | — | `content`, `path` | `frontend-call` |
| `GET` | `/api/webterminal/shells` | — | — | `frontend-call` |
| `DELETE` | `/api/webterminal/splitlayout` | — | — | `frontend-call` |
| `GET` | `/api/webterminal/splitlayout` | — | — | `frontend-call` |
| `PUT` | `/api/webterminal/splitlayout` | — | 有 | `frontend-call` |

## `wol`

| 方法 | 路径 | 查询字段 | 请求体 | 证据等级 |
|---|---|---|---|---|
| `GET` | `/api/wol/client/state` | — | — | `frontend-call` |
| `DELETE` | `/api/wol/device` | `key` | — | `frontend-call` |
| `POST` | `/api/wol/device` | — | 有 | `frontend-call` |
| `PUT` | `/api/wol/device` | — | 有 | `frontend-call` |
| `GET` | `/api/wol/device/shutdown` | `key` | — | `frontend-call` |
| `GET` | `/api/wol/device/wakeup` | `key` | — | `frontend-call` |
| `PUT` | `/api/wol/deviceorderadjustment` | — | 有 | `frontend-call` |
| `GET` | `/api/wol/devices` | — | — | `frontend-call` |
| `GET` | `/api/wol/devices_lite` | — | — | `frontend-call` |
| `GET` | `/api/wol/lastlogs` | — | — | `frontend-call` |
| `GET` | `/api/wol/logs` | `page`, `pageSize` | — | `frontend-call` |
| `GET` | `/api/wol/service/configure` | — | — | `frontend-call` |
| `PUT` | `/api/wol/service/configure` | — | 有 | `frontend-call` |
| `GET` | `/api/wol/service/getipv4interface` | — | — | `frontend-call` |
| `POST` | `/api/wol/webhooktest` | — | 有 | `frontend-call` |

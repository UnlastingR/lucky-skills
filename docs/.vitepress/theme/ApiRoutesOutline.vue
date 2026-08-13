<script setup lang="ts">
import { useRoute } from 'vitepress'
import { computed } from 'vue'

const route = useRoute()

const groups = [
  {
    label: '基础与系统',
    modules: [
      'about-content',
      'baseconfigure',
      'configure',
      'frontend-preferences',
      'info',
      'lucky',
      'modules',
      'reboot_program',
      'restoreconfigureconfirm',
      'status',
      'update'
    ]
  },
  {
    label: '认证与安全',
    modules: [
      '2fa',
      'coraza',
      'ipfliter',
      'login',
      'logout',
      'oauth',
      'password',
      'security-groups',
      'ssl',
      'temp-access-tickets',
      'third',
      'thirdPartyAuthManager',
      'twofapassword'
    ]
  },
  {
    label: '网络与穿透',
    modules: [
      'cloudflared',
      'ddns',
      'ddnstasklist',
      'frp',
      'ipregtest',
      'natdetect',
      'netinterfaces',
      'portforward',
      'portforwards',
      'portforwards_lite',
      'stun',
      'stunrule',
      'stunrulelist',
      'stunrulelist_lite',
      'v2l',
      'wol'
    ]
  },
  {
    label: '文件与存储',
    modules: [
      'dlnaservice',
      'ftpserver',
      'local-path-browser',
      'rclone',
      'smb',
      'storagemanagement',
      'webdav'
    ]
  },
  {
    label: '服务与自动化',
    modules: ['cron', 'docker', 'webservice', 'webterminal']
  },
  {
    label: '日志与资源',
    modules: ['iconlib', 'ipdb', 'logs', 'logscenter']
  }
] as const

const visible = computed(() => route.path.includes('/generated/api-routes'))

function moduleLink(module: string) {
  const slug = module
    .replace(/_/g, '-')
    .replace(/^(\d)/, '_$1')
    .toLowerCase()
  return `#${slug}`
}
</script>

<template>
  <nav v-if="visible" class="ApiRoutesOutline" aria-labelledby="api-routes-outline-title">
    <div id="api-routes-outline-title" class="outline-title">本页目录</div>
    <div class="outline-groups">
      <details v-for="group in groups" :key="group.label">
        <summary>{{ group.label }}</summary>
        <ul>
          <li v-for="module in group.modules" :key="module">
            <a :href="moduleLink(module)">{{ module }}</a>
          </li>
        </ul>
      </details>
    </div>
  </nav>
</template>

<style scoped>
.ApiRoutesOutline {
  border-left: 1px solid var(--vp-c-divider);
  padding-left: 16px;
  font-size: 13px;
  font-weight: 500;
}

.outline-title {
  line-height: 32px;
  font-size: 14px;
  font-weight: 600;
}

.outline-groups {
  display: grid;
  gap: 2px;
}

details {
  min-width: 0;
}

summary {
  cursor: pointer;
  color: var(--vp-c-text-2);
  line-height: 30px;
  list-style-position: inside;
  user-select: none;
}

summary:hover,
details[open] > summary {
  color: var(--vp-c-text-1);
}

ul {
  margin: 0;
  padding: 0 0 6px 16px;
  list-style: none;
}

a {
  display: block;
  overflow: hidden;
  color: var(--vp-c-text-2);
  font-size: 13px;
  font-weight: 400;
  line-height: 28px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

a:hover {
  color: var(--vp-c-text-1);
}
</style>

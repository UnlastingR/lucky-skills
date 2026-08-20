<script setup lang="ts">
import { Content, useData, useRoute, withBase } from 'vitepress'
import { computed } from 'vue'
import ApiRoutesOutline from './ApiRoutesOutline.vue'

const { frontmatter, page, theme } = useData()
const route = useRoute()

const repository = 'https://github.com/fyzure/lucky-skills'
const isHome = computed(() => frontmatter.value.layout === 'home')
const isApiRoutes = computed(() => route.path.includes('/generated/api-routes'))
const navItems = computed(() => theme.value.nav ?? [])
const sidebarGroups = computed(() => Array.isArray(theme.value.sidebar) ? theme.value.sidebar : [])

const external = (link: string) => /^(?:https?:|mailto:)/.test(link)
const href = (link: string) => external(link) || link.startsWith('#') ? link : withBase(link)
const normalizedPath = (link: string) => href(link).replace(/\.html$/, '').replace(/\/$/, '') || '/'
const active = (link: string) => !external(link) && normalizedPath(link) === route.path.replace(/\.html$/, '').replace(/\/$/, '')

const sidebarItems = computed(() => sidebarGroups.value.flatMap((group: any) => group.items ?? []))
const currentIndex = computed(() => sidebarItems.value.findIndex((item: any) => active(item.link)))
const previous = computed(() => currentIndex.value > 0 ? sidebarItems.value[currentIndex.value - 1] : undefined)
const next = computed(() => currentIndex.value >= 0 && currentIndex.value < sidebarItems.value.length - 1
  ? sidebarItems.value[currentIndex.value + 1]
  : undefined)

const hero = computed<any>(() => frontmatter.value.hero ?? {})
const features = computed<any[]>(() => frontmatter.value.features ?? [])

const updatedAt = computed(() => {
  if (!page.value.lastUpdated) return ''
  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  }).format(page.value.lastUpdated)
})
</script>

<template>
  <a class="skip-link" href="#VPContent">跳到正文</a>

  <header class="site-header">
    <div class="header-inner">
      <a class="brand" :href="withBase('/')" aria-label="Lucky Skills 首页">
        <img :src="withBase('/favicon.svg')" alt="" width="28" height="28">
        <span>Lucky Skills</span>
      </a>

      <nav class="top-nav" aria-label="主导航">
        <a
          v-for="item in navItems"
          :key="item.text"
          :href="href(item.link)"
          :class="{ active: active(item.link) }"
          :target="external(item.link) ? '_blank' : undefined"
          :rel="external(item.link) ? 'noopener noreferrer' : undefined"
        >{{ item.text }}</a>
      </nav>

      <div class="header-actions">
        <button class="DocSearch-Button" type="button">
          <span aria-hidden="true">⌕</span>
          <span class="search-label">搜索</span>
          <kbd>⌘K</kbd>
        </button>
        <button
          class="VPSwitchAppearance theme-toggle"
          type="button"
          role="switch"
          aria-checked="false"
          aria-label="切换深浅色主题"
          title="切换深浅色主题"
        ><span aria-hidden="true">◐</span></button>
        <a class="github-link" :href="repository" target="_blank" rel="noopener noreferrer" aria-label="GitHub 仓库">
          <span aria-hidden="true">GitHub</span>
        </a>
      </div>
    </div>
  </header>

  <template v-if="isHome">
    <main id="VPContent" class="home-main">
      <section class="hero" aria-labelledby="hero-title">
        <p class="hero-eyebrow">Lucky v3 · OpenToken API · Agent Skill</p>
        <h1 id="hero-title">
          <span class="hero-name">{{ hero.name }}</span>
          <span>{{ hero.text }}</span>
        </h1>
        <p class="hero-tagline">{{ hero.tagline }}</p>
        <div class="hero-actions" aria-label="快速入口">
          <a
            v-for="action in hero.actions ?? []"
            :key="action.text"
            :class="['hero-button', action.theme === 'brand' ? 'primary' : 'secondary']"
            :href="href(action.link)"
            :target="external(action.link) ? '_blank' : undefined"
            :rel="external(action.link) ? 'noopener noreferrer' : undefined"
          >{{ action.text }}</a>
        </div>
      </section>

      <section v-if="features.length" class="features" aria-label="项目能力">
        <article v-for="feature in features" :key="feature.title" class="feature-card">
          <div v-if="feature.icon" class="feature-icon" aria-hidden="true">{{ feature.icon }}</div>
          <h2>{{ feature.title }}</h2>
          <p>{{ feature.details }}</p>
          <a
            v-if="feature.link"
            :href="href(feature.link)"
            :target="external(feature.link) ? '_blank' : undefined"
            :rel="external(feature.link) ? 'noopener noreferrer' : undefined"
          >{{ feature.linkText ?? '了解更多' }} →</a>
        </article>
      </section>

      <Content class="doc-content home-content" />
    </main>
  </template>

  <template v-else>
    <div class="docs-shell" :class="{ 'api-routes-page': isApiRoutes }">
      <aside class="desktop-sidebar" aria-label="文档导航">
        <nav>
          <section v-for="group in sidebarGroups" :key="group.text" class="sidebar-group">
            <h2>{{ group.text }}</h2>
            <a
              v-for="item in group.items ?? []"
              :key="item.text"
              :href="href(item.link)"
              :class="{ active: active(item.link) }"
              :target="external(item.link) ? '_blank' : undefined"
              :rel="external(item.link) ? 'noopener noreferrer' : undefined"
            >{{ item.text }}</a>
          </section>
        </nav>
      </aside>

      <div class="mobile-nav-wrap">
        <details class="mobile-doc-nav">
          <summary>文档导航</summary>
          <nav>
            <section v-for="group in sidebarGroups" :key="group.text" class="sidebar-group">
              <h2>{{ group.text }}</h2>
              <a
                v-for="item in group.items ?? []"
                :key="item.text"
                :href="href(item.link)"
                :class="{ active: active(item.link) }"
                :target="external(item.link) ? '_blank' : undefined"
                :rel="external(item.link) ? 'noopener noreferrer' : undefined"
              >{{ item.text }}</a>
            </section>
          </nav>
        </details>
      </div>

      <main id="VPContent" class="main-content">
        <Content class="doc-content" />

        <div class="page-meta">
          <span v-if="updatedAt">最后更新：{{ updatedAt }}</span>
          <a :href="`${repository}/edit/main/docs/${page.filePath}`" target="_blank" rel="noopener noreferrer">在 GitHub 上编辑此页</a>
        </div>

        <nav v-if="previous || next" class="pager" aria-label="上下页">
          <a v-if="previous" class="pager-link previous" :href="href(previous.link)" rel="prev">
            <small>上一页</small><strong>{{ previous.text }}</strong>
          </a>
          <span v-else></span>
          <a v-if="next" class="pager-link next" :href="href(next.link)" rel="next">
            <small>下一页</small><strong>{{ next.text }}</strong>
          </a>
        </nav>
      </main>

      <aside v-if="isApiRoutes" class="right-outline" aria-label="API 路由目录">
        <ApiRoutesOutline />
      </aside>
    </div>
  </template>

  <footer class="site-footer">
    <p>非 Lucky 官方项目。仅对你拥有或获授权管理的实例使用。</p>
    <p>Lucky Skills · Open source documentation</p>
  </footer>
</template>

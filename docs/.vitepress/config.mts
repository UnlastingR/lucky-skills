import { defineConfig } from 'vitepress'

const repository = 'https://github.com/UnlastingR/lucky-skills'

export default defineConfig({
  lang: 'zh-CN',
  title: 'Lucky Skills',
  description: 'Lucky v3 OpenToken API、Agent Skill 与安全自动化文档',
  base: '/lucky-skills/',
  cleanUrls: true,
  lastUpdated: true,
  outDir: '../dist/lucky-skills',
  sitemap: {
    hostname: 'https://docs.fyzure.fyi/lucky-skills/'
  },
  head: [
    ['meta', { name: 'theme-color', content: '#3451b2' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:site_name', content: 'Lucky Skills' }]
  ],
  themeConfig: {
    nav: [
      { text: '指南', link: '/quickstart' },
      { text: 'API', link: '/generated/api-routes' },
      { text: 'OpenAPI', link: `${repository}/blob/main/openapi/lucky-v3.openapi.json` }
    ],
    sidebar: [
      {
        text: '开始使用',
        items: [
          { text: '项目概览', link: '/' },
          { text: '快速开始', link: '/quickstart' },
          { text: '凭据管理', link: '/credentials' },
          { text: '鉴权与安全', link: '/authentication' }
        ]
      },
      {
        text: '使用指南',
        items: [
          { text: 'API 客户端与 CLI', link: '/api-client' },
          { text: '接口约定', link: '/conventions' },
          { text: '模块指南', link: '/modules' }
        ]
      },
      {
        text: '参考',
        items: [
          { text: '完整 API 路由', link: '/generated/api-routes' },
          { text: '证据与覆盖范围', link: '/evidence-and-limitations' },
          { text: '资料来源', link: '/sources' }
        ]
      },
      {
        text: '项目',
        items: [
          { text: '部署说明', link: '/deployment' },
          { text: 'GitHub 仓库', link: repository },
          { text: '贡献指南', link: `${repository}/blob/main/CONTRIBUTING.md` },
          { text: '安全策略', link: `${repository}/blob/main/SECURITY.md` }
        ]
      }
    ],
    socialLinks: [
      { icon: 'github', link: repository }
    ],
    editLink: {
      pattern: `${repository}/edit/main/docs/:path`,
      text: '在 GitHub 上编辑此页'
    },
    search: {
      provider: 'local'
    },
    outline: {
      level: [2, 3],
      label: '本页目录'
    },
    docFooter: {
      prev: '上一页',
      next: '下一页'
    },
    lastUpdated: {
      text: '最后更新'
    },
    footer: {
      message: '非 Lucky 官方项目。仅对你拥有或获授权管理的实例使用。',
      copyright: 'Lucky Skills'
    }
  }
})

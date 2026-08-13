import DefaultTheme from 'vitepress/theme'
import { h } from 'vue'
import ApiRoutesOutline from './ApiRoutesOutline.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  Layout: () =>
    h(DefaultTheme.Layout, null, {
      'aside-outline-before': () => h(ApiRoutesOutline)
    })
}

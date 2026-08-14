const base = '/lucky-skills/'

const setAppearanceLabels = () => {
  const dark = document.documentElement.classList.contains('dark')
  document.querySelectorAll('.VPSwitchAppearance').forEach((button) => {
    button.setAttribute('aria-label', dark ? '切换到浅色主题' : '切换到深色主题')
    button.setAttribute('title', dark ? '切换到浅色主题' : '切换到深色主题')
    button.setAttribute('aria-checked', String(dark))
  })
}

const toggleAppearance = () => {
  const dark = !document.documentElement.classList.contains('dark')
  document.documentElement.classList.toggle('dark', dark)
  localStorage.setItem('vitepress-theme-appearance', dark ? 'dark' : 'light')
  setAppearanceLabels()
}

const copyCode = async (button) => {
  const code = button.parentElement?.querySelector('code')?.textContent
  if (!code) return

  try {
    await navigator.clipboard.writeText(code)
    button.classList.add('copied')
    button.title = '已复制'
    setTimeout(() => {
      button.classList.remove('copied')
      button.title = '复制代码'
    }, 1500)
  } catch {
    button.title = '复制失败'
  }
}

let searchIndexPromise

const pageRecord = async (url) => {
  const response = await fetch(url, { credentials: 'same-origin' })
  if (!response.ok) return null

  const documentText = await response.text()
  const parsed = new DOMParser().parseFromString(documentText, 'text/html')
  const main = parsed.querySelector('#VPContent')
  const title = parsed.querySelector('h1')?.textContent?.trim() || parsed.title.replace(/ \| Lucky Skills$/, '')
  const text = main?.textContent?.replace(/\s+/g, ' ').trim() || ''

  return { url, title, text, haystack: `${title} ${text}`.toLocaleLowerCase() }
}

const loadSearchIndex = async () => {
  const sitemapResponse = await fetch(`${base}sitemap.xml`, { credentials: 'same-origin' })
  if (!sitemapResponse.ok) throw new Error('无法载入站点地图')

  const sitemap = new DOMParser().parseFromString(await sitemapResponse.text(), 'application/xml')
  const urls = [...sitemap.querySelectorAll('loc')]
    .map((node) => node.textContent?.trim())
    .filter(Boolean)
    .map((absoluteUrl) => {
      const url = new URL(absoluteUrl)
      return `${url.pathname}${url.search}${url.hash}`
    })
    .filter((url) => url.startsWith(base))

  const records = await Promise.all(urls.map(pageRecord))
  return records.filter(Boolean)
}

const excerpt = (text, query) => {
  const normalized = text.toLocaleLowerCase()
  const index = normalized.indexOf(query)
  const start = Math.max(0, index === -1 ? 0 : index - 70)
  const end = Math.min(text.length, start + 190)
  return `${start ? '…' : ''}${text.slice(start, end)}${end < text.length ? '…' : ''}`
}

const createSearchDialog = () => {
  const dialog = document.createElement('dialog')
  dialog.className = 'LuckySearchDialog'
  dialog.setAttribute('aria-label', '站内搜索')
  dialog.innerHTML = `
    <form class="LuckySearchForm" method="dialog" role="search">
      <input class="LuckySearchInput" type="search" autocomplete="off" enterkeyhint="search" placeholder="搜索 Lucky Skills 文档…" aria-label="搜索文档">
      <button class="LuckySearchClose" type="submit" value="close">关闭</button>
    </form>
    <div class="LuckySearchStatus" aria-live="polite">输入关键词开始搜索</div>
    <ol class="LuckySearchResults"></ol>
  `
  document.body.append(dialog)

  const input = dialog.querySelector('.LuckySearchInput')
  const status = dialog.querySelector('.LuckySearchStatus')
  const results = dialog.querySelector('.LuckySearchResults')

  const render = async () => {
    const query = input.value.trim().toLocaleLowerCase()
    results.replaceChildren()
    if (!query) {
      status.hidden = false
      status.textContent = '输入关键词开始搜索'
      return
    }

    status.hidden = false
    status.textContent = '正在搜索…'

    try {
      searchIndexPromise ||= loadSearchIndex()
      const index = await searchIndexPromise
      const matches = index
        .filter((item) => item.haystack.includes(query))
        .sort((a, b) => Number(b.title.toLocaleLowerCase().includes(query)) - Number(a.title.toLocaleLowerCase().includes(query)))
        .slice(0, 20)

      if (!matches.length) {
        status.textContent = '没有找到相关结果'
        return
      }

      status.hidden = true
      const fragment = document.createDocumentFragment()
      for (const item of matches) {
        const li = document.createElement('li')
        li.className = 'LuckySearchResult'
        const link = document.createElement('a')
        link.href = item.url
        const strong = document.createElement('strong')
        strong.textContent = item.title
        const small = document.createElement('small')
        small.textContent = excerpt(item.text, query)
        link.append(strong, small)
        li.append(link)
        fragment.append(li)
      }
      results.append(fragment)
    } catch (error) {
      status.textContent = error instanceof Error ? error.message : '搜索暂时不可用'
    }
  }

  input.addEventListener('input', render)
  dialog.addEventListener('click', (event) => {
    if (event.target === dialog) dialog.close()
  })

  return { dialog, input }
}

let searchDialog

const openSearch = () => {
  searchDialog ||= createSearchDialog()
  if (typeof searchDialog.dialog.showModal === 'function') searchDialog.dialog.showModal()
  else searchDialog.dialog.setAttribute('open', '')
  searchDialog.input.focus()
}

setAppearanceLabels()

document.addEventListener('click', (event) => {
  const target = event.target
  if (!(target instanceof Element)) return

  if (target.closest('.VPSwitchAppearance')) {
    toggleAppearance()
    return
  }

  const copyButton = target.closest('button.copy')
  if (copyButton) {
    void copyCode(copyButton)
    return
  }

  if (target.closest('.DocSearch-Button')) openSearch()
})

document.addEventListener('keydown', (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key.toLocaleLowerCase() === 'k') {
    event.preventDefault()
    openSearch()
  }
})

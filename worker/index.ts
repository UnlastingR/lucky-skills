interface Env {
  ASSETS: Fetcher
}

type WorkerResponseInit = ResponseInit & {
  encodeBody?: 'automatic' | 'manual'
}

const IMMUTABLE_ASSET = /\/lucky-skills\/assets\/.*\.[A-Za-z0-9_-]{8,}\.(?:css|js|woff2?|png|jpe?g|gif|svg|webp|avif)$/i
const STATIC_ASSET = /\.(?:css|js|json|woff2?|png|jpe?g|gif|svg|webp|avif|ico|xml|txt)$/i

const LEGACY_EVIDENCE_PATHS = new Set([
  '/evidence/lucky-v3-endpoints.json',
  '/evidence/lucky-v3-runtime-verification.json'
])

function acceptsEncoding(request: Request, wanted: string): boolean {
  const header = request.headers.get('accept-encoding')
  if (!header) return false

  return header.split(',').some((entry) => {
    const [name, ...parameters] = entry.trim().toLowerCase().split(';')
    if (name !== wanted && name !== '*') return false

    const quality = parameters
      .map((parameter) => parameter.trim())
      .find((parameter) => parameter.startsWith('q='))
    return quality ? Number(quality.slice(2)) > 0 : true
  })
}

function isDocumentPath(pathname: string): boolean {
  if (!pathname.startsWith('/lucky-skills/')) return false
  if (pathname.endsWith('/') || pathname.endsWith('.html')) return true
  return !/\.[^/]+$/.test(pathname)
}

function assetRequest(request: Request): Request {
  const url = new URL(request.url)
  if (!['GET', 'HEAD'].includes(request.method) || !isDocumentPath(url.pathname)) return request

  const headers = new Headers(request.headers)
  headers.set('Accept-Encoding', 'identity')
  return new Request(request, { headers })
}

function withHeaders(response: Response, request: Request): Response {
  const requestUrl = new URL(request.url)
  const headers = new Headers(response.headers)
  let body = response.body

  headers.set('X-Content-Type-Options', 'nosniff')
  headers.set('X-Frame-Options', 'DENY')
  headers.set('Referrer-Policy', 'strict-origin-when-cross-origin')
  headers.set('Strict-Transport-Security', 'max-age=63072000; includeSubDomains')
  headers.set('Cross-Origin-Opener-Policy', 'same-origin')
  headers.set('Permissions-Policy', 'camera=(), microphone=(), geolocation=(), payment=(), usb=()')

  const isHtml = response.ok && headers.get('content-type')?.includes('text/html')

  if (response.ok && IMMUTABLE_ASSET.test(requestUrl.pathname)) {
    headers.set('Cache-Control', 'public, max-age=31536000, immutable')
  } else if (isHtml) {
    // Prevent edge HTML rewriting (notably injected analytics). Compress the
    // current HTML in the Worker so no-transform does not cost transfer size.
    headers.set('Cache-Control', 'public, max-age=600, stale-while-revalidate=86400, no-transform')
    if (!headers.get('Vary')?.toLowerCase().includes('accept-encoding')) {
      headers.append('Vary', 'Accept-Encoding')
    }

    if (
      request.method === 'GET' &&
      body &&
      !headers.has('Content-Encoding') &&
      acceptsEncoding(request, 'gzip')
    ) {
      body = body.pipeThrough(new CompressionStream('gzip'))
      headers.delete('Content-Length')
      headers.set('Content-Encoding', 'gzip')
    }
  } else if (response.ok && requestUrl.pathname === '/lucky-skills/enhance.js') {
    headers.set('Cache-Control', 'public, max-age=600, must-revalidate')
  } else if (response.ok && STATIC_ASSET.test(requestUrl.pathname)) {
    headers.set('Cache-Control', 'public, max-age=86400, stale-while-revalidate=604800')
  }

  const init: WorkerResponseInit = {
    status: response.status,
    statusText: response.statusText,
    headers
  }

  if (headers.has('Content-Encoding')) init.encodeBody = 'manual'

  return new Response(body, init)
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url)

    if (url.pathname === '/robots.txt') {
      return withHeaders(
        new Response(
          'User-agent: *\nAllow: /lucky-skills/\nSitemap: https://docs.fyzure.fyi/lucky-skills/sitemap.xml\n',
          { headers: { 'Content-Type': 'text/plain; charset=utf-8' } }
        ),
        request
      )
    }

    if (url.pathname === '/') {
      return Response.redirect(new URL('/lucky-skills/', url), 308)
    }

    if (url.pathname === '/lucky-skills') {
      return Response.redirect(new URL('/lucky-skills/', url), 308)
    }

    if (LEGACY_EVIDENCE_PATHS.has(url.pathname)) {
      return Response.redirect(new URL(`/lucky-skills${url.pathname}`, url), 308)
    }

    const response = await env.ASSETS.fetch(assetRequest(request))
    return withHeaders(response, request)
  }
} satisfies ExportedHandler<Env>

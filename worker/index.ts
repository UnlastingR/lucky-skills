interface Env {
  ASSETS: Fetcher
}

const IMMUTABLE_ASSET = /\/lucky-skills\/assets\/.*\.[A-Za-z0-9_-]{8,}\.(?:css|js|woff2?|png|jpe?g|gif|svg|webp|avif)$/i

function withHeaders(response: Response, requestUrl: URL): Response {
  const headers = new Headers(response.headers)

  headers.set('X-Content-Type-Options', 'nosniff')
  headers.set('Referrer-Policy', 'strict-origin-when-cross-origin')

  if (response.ok && IMMUTABLE_ASSET.test(requestUrl.pathname)) {
    headers.set('Cache-Control', 'public, max-age=31536000, immutable')
  } else if (response.ok && headers.get('content-type')?.includes('text/html')) {
    headers.set('Cache-Control', 'public, max-age=300, must-revalidate')
  }

  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers
  })
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url)

    if (url.pathname === '/') {
      return Response.redirect(new URL('/lucky-skills/', url), 302)
    }

    if (url.pathname === '/lucky-skills') {
      return Response.redirect(new URL('/lucky-skills/', url), 301)
    }

    const response = await env.ASSETS.fetch(request)
    return withHeaders(response, url)
  }
} satisfies ExportedHandler<Env>

export const API_BASE = 'http://localhost:8000'

export class ApiError extends Error {
  constructor(status, detail) {
    super(typeof detail === 'string' ? detail : JSON.stringify(detail))
    this.status = status
    this.detail = detail
  }
}

let accessToken = null

export function setAccessToken(token) {
  accessToken = token
}

async function rawRequest(path, { method = 'GET', body, useAuth = true } = {}) {
  const headers = {}
  if (body !== undefined) headers['Content-Type'] = 'application/json'
  if (useAuth && accessToken) headers['Authorization'] = `Bearer ${accessToken}`

  let res
  try {
    res = await fetch(`${API_BASE}${path}`, {
      method,
      headers,
      credentials: 'include',
      body: body !== undefined ? JSON.stringify(body) : undefined,
    })
  } catch {
    throw new ApiError(0, 'Не удалось подключиться к серверу. Проверьте подключение к интернету или попробуйте позже.')
  }

  const text = await res.text()
  const data = text ? JSON.parse(text) : null

  if (!res.ok) {
    throw new ApiError(res.status, data?.detail ?? res.statusText)
  }
  return data
}

let refreshPromise = null

export function refreshSession() {
  if (!refreshPromise) {
    refreshPromise = rawRequest('/auth/refresh', { method: 'POST', useAuth: false })
      .then((data) => {
        setAccessToken(data.access_token)
        return data
      })
      .finally(() => {
        refreshPromise = null
      })
  }
  return refreshPromise
}

const NO_RETRY_PATHS = ['/auth/login', '/auth/register', '/auth/refresh']

async function request(path, options = {}) {
  try {
    return await rawRequest(path, options)
  } catch (err) {
    const canRetry = options.useAuth !== false && !NO_RETRY_PATHS.includes(path)
    if (err instanceof ApiError && err.status === 401 && canRetry) {
      await refreshSession()
      return rawRequest(path, options)
    }
    throw err
  }
}

export const api = {
  register: (username, password) =>
    request('/auth/register', { method: 'POST', useAuth: false, body: { username, password } }),

  login: (username, password) =>
    request('/auth/login', { method: 'POST', useAuth: false, body: { username, password } }),

  logout: () => request('/auth/logout', { method: 'POST' }),

  me: () => request('/me'),

  getProducts: (skip = 0, limit = 20, q) => {
    const params = new URLSearchParams({ skip, limit })
    if (q) params.set('q', q)
    return request(`/products?${params.toString()}`, { useAuth: false })
  },

  getProduct: (id) => request(`/products/${id}`, { useAuth: false }),

  createProduct: (product) => request('/admin/products', { method: 'POST', body: product }),

  getCart: () => request('/cart'),

  addCartItem: (productId, quantity) =>
    request('/cart/items', { method: 'POST', body: { product_id: productId, quantity } }),

  updateCartItem: (productId, quantity) =>
    request(`/cart/items/${productId}`, { method: 'PATCH', body: { quantity } }),

  removeCartItem: (productId) => request(`/cart/items/${productId}`, { method: 'DELETE' }),

  createOrder: () => request('/orders', { method: 'POST' }),

  getOrders: () => request('/orders'),

  getOrder: (id) => request(`/orders/${id}`),

  getAllOrders: () => request('/admin/orders'),

  completeOrder: (id) => request(`/admin/orders/${id}/complete`, { method: 'PATCH' }),
}

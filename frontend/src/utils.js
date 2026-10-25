import { API_BASE } from './api'

export function resolveImageUrl(url) {
  if (!url) return url
  return /^https?:\/\//.test(url) ? url : `${API_BASE}${url}`
}

const STATUS_MESSAGES = {
  401: 'Сессия истекла, войдите снова',
  502: 'Сервис временно недоступен, попробуйте позже',
  503: 'Сервис временно недоступен, попробуйте позже',
  504: 'Сервис временно недоступен, попробуйте позже',
}

export function formatApiError(err) {
  if (STATUS_MESSAGES[err?.status]) return STATUS_MESSAGES[err.status]
  const detail = err?.detail ?? err?.message ?? 'Что-то пошло не так'
  if (Array.isArray(detail)) {
    return detail.map((d) => d.msg).join('; ')
  }
  return String(detail)
}

export function formatDate(isoString) {
  return new Date(isoString).toLocaleString()
}

const STATUS_LABELS = {
  pending: 'В ожидании',
  completed: 'Готово',
}

export function formatStatus(status) {
  return STATUS_LABELS[status] ?? status
}

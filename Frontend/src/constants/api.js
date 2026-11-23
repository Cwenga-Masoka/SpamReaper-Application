export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

const API_PREFIX = '/api'

export const API_ENDPOINT = Object.freeze({
  FLAGGED_EMAILS: `${API_PREFIX}/flagged`,
  SCAN: `${API_PREFIX}/scan`,
  KEEP_EMAIL: (id) => `${API_PREFIX}/keep/${id}`,
  KEEP_EMAILS: `${API_PREFIX}/keep/bulk`,
  TRASH_EMAIL: (id) => `${API_PREFIX}/trash/${id}`,
  TRASH_EMAILS: `${API_PREFIX}/trash/bulk`,
  UNTRASH_EMAIL: (id) => `${API_PREFIX}/untrash/${id}`,
  UNTRASH_EMAILS: `${API_PREFIX}/untrash/bulk`,
  AUTH_LOGIN: `${API_PREFIX}/auth/login`,
  AUTH_ME: `${API_PREFIX}/auth/me`,
})

export const HTTP_METHOD = Object.freeze({
  GET: 'GET',
  POST: 'POST',
})

export const JSON_HEADERS = Object.freeze({
  'Content-Type': 'application/json',
})

export const BULK_IDS_KEY = 'email_ids'

export const BULK_RESPONSE_KEY = Object.freeze({
  RESULT: 'result',
  FAILED: 'failed',
})

export const HTTP_STATUS = Object.freeze({ UNAUTHORIZED: 401 })

export const LOGIN_URL = `${API_BASE_URL}${API_ENDPOINT.AUTH_LOGIN}`
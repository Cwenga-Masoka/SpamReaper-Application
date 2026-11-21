export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export const API_ENDPOINT = Object.freeze({
  CURRENT_USER: '/user',
  SPAM_EMAILS: '/emails/spam',
  KEEP_EMAIL: (id) => `/emails/${id}/keep`,
  TRASH_EMAIL: (id) => `/emails/${id}/trash`,
  SCAN: '/scan',
})

export const HTTP_METHOD = Object.freeze({
  GET: 'GET',
  POST: 'POST',
})
import { API_BASE_URL, API_ENDPOINT, HTTP_METHOD } from '../constants/api'

async function request(path, method = HTTP_METHOD.GET) {
  const response = await fetch(`${API_BASE_URL}${path}`, { method })

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`)
  }

  return response.json()
}

export const fetchCurrentUser = () => request(API_ENDPOINT.CURRENT_USER)

export const fetchSpamEmails = () => request(API_ENDPOINT.SPAM_EMAILS)

export const keepEmail = (id) =>
  request(API_ENDPOINT.KEEP_EMAIL(id), HTTP_METHOD.POST)

export const trashEmail = (id) =>
  request(API_ENDPOINT.TRASH_EMAIL(id), HTTP_METHOD.POST)

export const scanInbox = () => request(API_ENDPOINT.SCAN, HTTP_METHOD.POST)
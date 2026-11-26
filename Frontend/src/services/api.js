import { NotLoggedInError } from './errors'

import {
  API_BASE_URL,
  API_ENDPOINT,
  BULK_IDS_KEY,
  HTTP_METHOD,
  JSON_HEADERS,
  HTTP_STATUS,
  FETCH_CREDENTIALS
} from '../constants/api'

async function request(path, method = HTTP_METHOD.GET, body) {
  const options = { method, credentials: FETCH_CREDENTIALS }

  if (body !== undefined) {
    options.headers = JSON_HEADERS
    options.body = JSON.stringify(body)
  }

  const response = await fetch(`${API_BASE_URL}${path}`, options)

  if (response.status === HTTP_STATUS.UNAUTHORIZED) {
    throw new NotLoggedInError()
  }
  
  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`)
  }

  return response.json()
}

const toBulkBody = (ids) => ({ [BULK_IDS_KEY]: ids })

export const fetchFlaggedEmails = () => request(API_ENDPOINT.FLAGGED_EMAILS)

export const scanInbox = () => request(API_ENDPOINT.SCAN, HTTP_METHOD.POST)

export const keepEmail = (id) =>
  request(API_ENDPOINT.KEEP_EMAIL(id), HTTP_METHOD.POST)

export const keepEmails = (ids) =>
  request(API_ENDPOINT.KEEP_EMAILS, HTTP_METHOD.POST, toBulkBody(ids))

export const trashEmail = (id) =>
  request(API_ENDPOINT.TRASH_EMAIL(id), HTTP_METHOD.POST)

export const trashEmails = (ids) =>
  request(API_ENDPOINT.TRASH_EMAILS, HTTP_METHOD.POST, toBulkBody(ids))

export const untrashEmail = (id) =>
  request(API_ENDPOINT.UNTRASH_EMAIL(id), HTTP_METHOD.POST)

export const untrashEmails = (ids) =>
  request(API_ENDPOINT.UNTRASH_EMAILS, HTTP_METHOD.POST, toBulkBody(ids))

export function fetchCurrentUser() {
  return request(API_ENDPOINT.AUTH_ME, HTTP_METHOD.GET)
}
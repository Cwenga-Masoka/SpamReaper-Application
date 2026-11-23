import { fetchCurrentUser } from '../services/api'
import { NotLoggedInError } from '../services/errors'
import { useFetch } from './useFetch'

const NO_USER = null

export function useCurrentUser() {
  const { data, error, reload } = useFetch(fetchCurrentUser, NO_USER)
  const isLoggedOut = error instanceof NotLoggedInError

  return {
    user: data,
    isLoggedOut,
    hasError: error !== null && !isLoggedOut,
    reload,
  }
}
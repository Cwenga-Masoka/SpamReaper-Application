import { useCallback, useEffect, useState } from 'react'

export function useFetch(fetcher, initialData) {
  const [data, setData] = useState(initialData)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)

  const load = useCallback(async () => {
    try {
      setData(await fetcher())
      setError(null)
    } catch (caughtError) {
      setError(caughtError)
    } finally {
      setIsLoading(false)
    }
  }, [fetcher])

  useEffect(() => {
    load()
  }, [load])

  return { data, isLoading, error, hasError: error !== null, reload: load }
}
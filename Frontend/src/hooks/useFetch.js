import { useCallback, useEffect, useState } from 'react'

export function useFetch(fetcher, initialData) {
  const [data, setData] = useState(initialData)
  const [isLoading, setIsLoading] = useState(true)
  const [hasError, setHasError] = useState(false)

  const load = useCallback(async () => {
    try {
      setData(await fetcher())
      setHasError(false)
    } catch {
      setHasError(true)
    } finally {
      setIsLoading(false)
    }
  }, [fetcher])

  useEffect(() => {
    load()
  }, [load])

  return { data, isLoading, hasError, reload: load }
}
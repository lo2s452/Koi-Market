import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'
import { formatApiError, resolveImageUrl } from '../utils'
import { PhotoIcon } from '../components/icons'
import { Reveal } from '../components/Reveal'

const SUGGESTIONS_LIMIT = 4
const SEARCH_LIMIT = 20
const DEBOUNCE_MS = 350

export function SearchPage() {
  const [query, setQuery] = useState('')
  const [debouncedQuery, setDebouncedQuery] = useState('')
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedQuery(query.trim()), DEBOUNCE_MS)
    return () => clearTimeout(timer)
  }, [query])

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    setError(null)
    api
      .getProducts(0, debouncedQuery ? SEARCH_LIMIT : SUGGESTIONS_LIMIT, debouncedQuery || undefined)
      .then((data) => {
        if (!cancelled) setProducts(data)
      })
      .catch((err) => !cancelled && setError(formatApiError(err)))
      .finally(() => !cancelled && setLoading(false))
    return () => {
      cancelled = true
    }
  }, [debouncedQuery])

  const isSearching = debouncedQuery.length > 0

  return (
    <div className="search-page">
      <div className="search-page-inner">
        <input
          autoFocus
          type="text"
          className="search-input"
          placeholder="Что вы ищете?"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </div>

      {error && <p className="form-error">{error}</p>}

      <h3 className="search-suggestions-title">
        {isSearching ? 'Результаты поиска' : 'Вас также может заинтересовать'}
      </h3>

      {loading ? (
        <p className="page-status">Загрузка...</p>
      ) : products.length === 0 ? (
        <p className="page-status">Ничего не найдено.</p>
      ) : (
        <div className="search-results-row">
          {products.map((p, i) => (
            <Reveal key={p.id} delay={(i % SUGGESTIONS_LIMIT) * 40}>
              <Link to={`/products/${p.id}`} className="product-card">
                {p.image_url ? (
                  <img
                    className="product-photo"
                    src={resolveImageUrl(p.image_url)}
                    alt={p.name}
                    loading="lazy"
                  />
                ) : (
                  <div className="product-glyph product-glyph-lg">
                    <PhotoIcon />
                  </div>
                )}
                <p className="search-result-name">{p.name}</p>
              </Link>
            </Reveal>
          ))}
        </div>
      )}
    </div>
  )
}

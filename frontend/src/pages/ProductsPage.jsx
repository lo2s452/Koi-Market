import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { api } from '../api'
import { formatApiError, resolveImageUrl } from '../utils'
import { MinusIcon, PlusIcon, PhotoIcon } from '../components/icons'
import { PageHero } from '../components/PageHero'
import { Reveal } from '../components/Reveal'

const PAGE_SIZE = 20

export function ProductsPage() {
  const { user } = useAuth()
  const [products, setProducts] = useState([])
  const [skip, setSkip] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [cartQuantities, setCartQuantities] = useState({})

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    api
      .getProducts(skip, PAGE_SIZE)
      .then((data) => {
        if (!cancelled) setProducts(data)
      })
      .catch((err) => !cancelled && setError(formatApiError(err)))
      .finally(() => !cancelled && setLoading(false))
    return () => {
      cancelled = true
    }
  }, [skip])

  useEffect(() => {
    if (!user) return
    let cancelled = false
    api.getCart().then((cart) => {
      if (cancelled) return
      const quantities = {}
      cart.items.forEach((item) => {
        quantities[item.product_id] = item.quantity
      })
      setCartQuantities(quantities)
    })
    return () => {
      cancelled = true
    }
  }, [user])

  async function handleAddToCart(productId) {
    setError(null)
    try {
      await api.addCartItem(productId, 1)
      setCartQuantities((prev) => ({ ...prev, [productId]: 1 }))
    } catch (err) {
      setError(formatApiError(err))
    }
  }

  async function handleIncrement(productId) {
    setError(null)
    try {
      const quantity = cartQuantities[productId] + 1
      await api.updateCartItem(productId, quantity)
      setCartQuantities((prev) => ({ ...prev, [productId]: quantity }))
    } catch (err) {
      setError(formatApiError(err))
    }
  }

  async function handleDecrement(productId) {
    setError(null)
    try {
      const quantity = cartQuantities[productId] - 1
      if (quantity <= 0) {
        await api.removeCartItem(productId)
        setCartQuantities((prev) => {
          const next = { ...prev }
          delete next[productId]
          return next
        })
      } else {
        await api.updateCartItem(productId, quantity)
        setCartQuantities((prev) => ({ ...prev, [productId]: quantity }))
      }
    } catch (err) {
      setError(formatApiError(err))
    }
  }

  return (
    <div>
      <PageHero
        size="lg"
        eyebrow="Одежда для повседневной жизни"
        title="Koi Market"
        subtitle="Футболки, лонгсливы и джинсы — подборка базового гардероба в одном месте."
      />
      <div className="page">
        <h2>Каталог</h2>
        {error && <p className="form-error">{error}</p>}
        {loading ? (
          <p className="page-status">Загрузка...</p>
        ) : (
          <div className="product-grid">
            {products.map((p, i) => {
              return (
                <Reveal key={p.id} className="product-card" delay={(i % PAGE_SIZE) * 40}>
                  <Link to={`/products/${p.id}`} className="product-photo-link">
                    {p.image_url ? (
                      <img className="product-photo" src={resolveImageUrl(p.image_url)} alt={p.name} loading="lazy" />
                    ) : (
                      <div className="product-glyph product-glyph-lg">
                        <PhotoIcon />
                      </div>
                    )}
                  </Link>
                  <div className="product-info">
                    <h3>
                      <Link to={`/products/${p.id}`}>{p.name}</Link>
                    </h3>
                    <p className="product-desc">{p.description}</p>
                    <div className="product-card-footer">
                      <p className="product-price">{p.price} ₽</p>
                      <p className="product-stock">
                        {p.stock === 0 ? 'Нет в наличии' : `В наличии: ${p.stock}`}
                      </p>
                      {user && (p.id in cartQuantities ? (
                        <div className="qty-control">
                          <button type="button" onClick={() => handleDecrement(p.id)}>
                            <MinusIcon width={14} height={14} />
                          </button>
                          <span>{cartQuantities[p.id]}</span>
                          <button
                            type="button"
                            disabled={cartQuantities[p.id] >= p.stock}
                            onClick={() => handleIncrement(p.id)}
                          >
                            <PlusIcon width={14} height={14} />
                          </button>
                        </div>
                      ) : (
                        <button
                          type="button"
                          className="btn-link"
                          disabled={p.stock === 0}
                          onClick={() => handleAddToCart(p.id)}
                        >
                          В корзину
                        </button>
                      ))}
                    </div>
                  </div>
                </Reveal>
              )
            })}
            {products.length === 0 && <p>Товаров нет.</p>}
          </div>
        )}
        <div className="pagination">
          <button disabled={skip === 0} onClick={() => setSkip((s) => Math.max(0, s - PAGE_SIZE))}>
            Назад
          </button>
          <button disabled={products.length < PAGE_SIZE} onClick={() => setSkip((s) => s + PAGE_SIZE)}>
            Вперёд
          </button>
        </div>
      </div>
    </div>
  )
}

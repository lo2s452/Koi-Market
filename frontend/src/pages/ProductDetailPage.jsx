import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { api } from '../api'
import { formatApiError, resolveImageUrl } from '../utils'
import { MinusIcon, PlusIcon, PhotoIcon } from '../components/icons'
import { PageHero } from '../components/PageHero'

export function ProductDetailPage() {
  const { id } = useParams()
  const { user } = useAuth()
  const [product, setProduct] = useState(null)
  const [quantity, setQuantity] = useState(1)
  const [error, setError] = useState(null)
  const [message, setMessage] = useState(null)
  const [notFound, setNotFound] = useState(false)

  useEffect(() => {
    api
      .getProduct(id)
      .then(setProduct)
      .catch((err) => (err.status === 404 ? setNotFound(true) : setError(formatApiError(err))))
  }, [id])

  async function handleAddToCart(e) {
    e.preventDefault()
    setMessage(null)
    setError(null)
    try {
      await api.addCartItem(product.id, quantity)
      setMessage('Товар добавлен в корзину')
    } catch (err) {
      setError(formatApiError(err))
    }
  }

  if (notFound) return <p className="page-status">Товар не найден. <Link to="/products">Ко всем товарам</Link></p>
  if (error && !product) return <p className="form-error">{error}</p>
  if (!product) return <p className="page-status">Загрузка...</p>

  return (
    <div>
      <PageHero eyebrow="Товар" title={product.name} />
      <div className="page">
        <p><Link to="/products">← Ко всем товарам</Link></p>
        <div className="product-detail-head">
          {product.image_url ? (
            <img className="product-photo-lg" src={resolveImageUrl(product.image_url)} alt={product.name} />
          ) : (
            <div className="product-glyph">
              <PhotoIcon />
            </div>
          )}
          <p className="product-stock">
            {product.stock === 0 ? 'Нет в наличии' : `В наличии: ${product.stock}`}
          </p>
        </div>
        <p>{product.description}</p>
        <p className="product-price">{product.price} ₽</p>

        {user && product.stock > 0 && (
          <form onSubmit={handleAddToCart} className="form form-inline">
            <label>
              Количество
              <div className="qty-control">
                <button
                  type="button"
                  onClick={() => setQuantity((q) => Math.max(1, q - 1))}
                >
                  <MinusIcon width={14} height={14} />
                </button>
                <span>{quantity}</span>
                <button
                  type="button"
                  onClick={() => setQuantity((q) => Math.min(product.stock, q + 1))}
                >
                  <PlusIcon width={14} height={14} />
                </button>
              </div>
            </label>
            <button type="submit">В корзину</button>
          </form>
        )}
        {message && <p className="form-success">{message}</p>}
        {error && <p className="form-error">{error}</p>}
      </div>
    </div>
  )
}

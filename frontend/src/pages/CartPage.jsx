import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api'
import { formatApiError } from '../utils'
import { CartIcon, MinusIcon, PlusIcon, TrashIcon } from '../components/icons'
import { PageHero } from '../components/PageHero'

export function CartPage() {
  const navigate = useNavigate()
  const [cart, setCart] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [checkingOut, setCheckingOut] = useState(false)

  function loadCart() {
    setLoading(true)
    return api
      .getCart()
      .then(setCart)
      .catch((err) => setError(formatApiError(err)))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    loadCart()
  }, [])

  async function handleUpdateQuantity(productId, quantity) {
    setError(null)
    try {
      const updated = await api.updateCartItem(productId, quantity)
      setCart(updated)
    } catch (err) {
      setError(formatApiError(err))
    }
  }

  async function handleRemove(productId) {
    setError(null)
    try {
      const updated = await api.removeCartItem(productId)
      setCart(updated)
    } catch (err) {
      setError(formatApiError(err))
    }
  }

  async function handleCheckout() {
    setError(null)
    setCheckingOut(true)
    try {
      const order = await api.createOrder()
      navigate(`/orders/${order.id}`)
    } catch (err) {
      setError(formatApiError(err))
    } finally {
      setCheckingOut(false)
    }
  }

  if (loading) return <p className="page-status">Загрузка...</p>

  return (
    <div>
      <PageHero eyebrow="Ваш выбор" title="Корзина" />
      <div className="page">
      {error && <p className="form-error">{error}</p>}
      {cart.items.length === 0 ? (
        <div className="empty-state">
          <CartIcon />
          <p>Корзина пуста.</p>
        </div>
      ) : (
        <>
          <table className="cart-table">
            <thead>
              <tr>
                <th>Товар</th>
                <th>Цена</th>
                <th>Количество</th>
                <th>Сумма</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {cart.items.map((item) => (
                <tr key={item.product_id}>
                  <td>{item.name}</td>
                  <td>{item.price} ₽</td>
                  <td>
                    <div className="qty-control">
                      <button
                        type="button"
                        disabled={item.quantity <= 1}
                        onClick={() => handleUpdateQuantity(item.product_id, item.quantity - 1)}
                      >
                        <MinusIcon width={14} height={14} />
                      </button>
                      <span>{item.quantity}</span>
                      <button
                        type="button"
                        onClick={() => handleUpdateQuantity(item.product_id, item.quantity + 1)}
                      >
                        <PlusIcon width={14} height={14} />
                      </button>
                    </div>
                  </td>
                  <td>{item.subtotal} ₽</td>
                  <td>
                    <button
                      className="btn-danger icon-btn"
                      aria-label="Удалить товар"
                      onClick={() => handleRemove(item.product_id)}
                    >
                      <TrashIcon />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <p className="cart-total">Итого: {cart.total} ₽</p>
          <button onClick={handleCheckout} disabled={checkingOut}>
            {checkingOut ? 'Оформляем...' : 'Оформить заказ'}
          </button>
        </>
      )}
      </div>
    </div>
  )
}

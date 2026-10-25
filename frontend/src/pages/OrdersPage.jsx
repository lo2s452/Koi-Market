import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'
import { formatApiError, formatDate, formatStatus } from '../utils'
import { CartIcon } from '../components/icons'
import { PageHero } from '../components/PageHero'

export function OrdersPage() {
  const [orders, setOrders] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    api.getOrders().then(setOrders).catch((err) => setError(formatApiError(err)))
  }, [])

  if (error) return <p className="form-error">{error}</p>
  if (!orders) return <p className="page-status">Загрузка...</p>

  return (
    <div>
      <PageHero eyebrow="История" title="Мои заказы" />
      <div className="page">
      {orders.length === 0 ? (
        <div className="empty-state">
          <CartIcon />
          <p>Заказов пока нет.</p>
        </div>
      ) : (
        <ul className="order-list">
          {orders.map((order) => (
            <li key={order.id}>
              <Link to={`/orders/${order.id}`}>
                Заказ #{order.id} — {formatDate(order.created_at)}
                <span className={`status-badge${order.status === 'completed' ? ' completed' : ''}`}>
                  {formatStatus(order.status)}
                </span>
              </Link>
            </li>
          ))}
        </ul>
      )}
      </div>
    </div>
  )
}

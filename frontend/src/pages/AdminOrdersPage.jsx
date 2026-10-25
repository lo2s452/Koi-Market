import { useEffect, useState } from 'react'
import { api } from '../api'
import { formatApiError, formatDate, formatStatus } from '../utils'
import { PageHero } from '../components/PageHero'

export function AdminOrdersPage() {
  const [orders, setOrders] = useState(null)
  const [error, setError] = useState(null)

  function loadOrders() {
    api.getAllOrders().then(setOrders).catch((err) => setError(formatApiError(err)))
  }

  useEffect(() => {
    loadOrders()
  }, [])

  async function handleComplete(orderId) {
    setError(null)
    try {
      await api.completeOrder(orderId)
      loadOrders()
    } catch (err) {
      setError(formatApiError(err))
    }
  }

  if (error && !orders) return <p className="form-error">{error}</p>
  if (!orders) return <p className="page-status">Загрузка...</p>

  return (
    <div>
      <PageHero eyebrow="Управление" title="Админ: все заказы" />
      <div className="page">
      {error && <p className="form-error">{error}</p>}
      {orders.length === 0 ? (
        <p>Заказов нет.</p>
      ) : (
        <table className="cart-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Статус</th>
              <th>Создан</th>
              <th>Позиции</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order) => (
              <tr key={order.id}>
                <td>{order.id}</td>
                <td>
                  <span className={`status-badge${order.status === 'completed' ? ' completed' : ''}`}>
                    {formatStatus(order.status)}
                  </span>
                </td>
                <td>{formatDate(order.created_at)}</td>
                <td>
                  {order.items.map((item) => `${item.product_name} × ${item.quantity}`).join(', ')}
                </td>
                <td>
                  {order.status !== 'completed' && (
                    <button onClick={() => handleComplete(order.id)}>Завершить</button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      </div>
    </div>
  )
}

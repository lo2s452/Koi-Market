import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api } from '../api'
import { formatApiError, formatDate, formatStatus } from '../utils'
import { PageHero } from '../components/PageHero'

export function OrderDetailPage() {
  const { id } = useParams()
  const [order, setOrder] = useState(null)
  const [error, setError] = useState(null)
  const [notFound, setNotFound] = useState(false)

  useEffect(() => {
    api
      .getOrder(id)
      .then(setOrder)
      .catch((err) => (err.status === 404 ? setNotFound(true) : setError(formatApiError(err))))
  }, [id])

  if (notFound) return <p className="page-status">Заказ не найден. <Link to="/orders">Ко всем заказам</Link></p>
  if (error) return <p className="form-error">{error}</p>
  if (!order) return <p className="page-status">Загрузка...</p>

  return (
    <div>
      <PageHero eyebrow="Детали заказа" title={`Заказ #${order.id}`} />
      <div className="page">
      <p><Link to="/orders">← Ко всем заказам</Link></p>
      <p>
        Статус:{' '}
        <span className={`status-badge${order.status === 'completed' ? ' completed' : ''}`}>
          {formatStatus(order.status)}
        </span>
      </p>
      <p>Оформлен: {formatDate(order.created_at)}</p>
      <table className="cart-table">
        <thead>
          <tr>
            <th>Товар</th>
            <th>Цена на момент покупки</th>
            <th>Количество</th>
          </tr>
        </thead>
        <tbody>
          {order.items.map((item) => (
            <tr key={item.product_id}>
              <td>{item.product_name}</td>
              <td>{item.price} ₽</td>
              <td>{item.quantity}</td>
            </tr>
          ))}
        </tbody>
      </table>
      </div>
    </div>
  )
}

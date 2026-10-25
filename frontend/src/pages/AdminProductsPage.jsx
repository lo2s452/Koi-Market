import { useState } from 'react'
import { api } from '../api'
import { formatApiError } from '../utils'
import { PageHero } from '../components/PageHero'

export function AdminProductsPage() {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [price, setPrice] = useState('')
  const [stock, setStock] = useState('')
  const [imageUrl, setImageUrl] = useState('')
  const [error, setError] = useState(null)
  const [created, setCreated] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError(null)
    setCreated(null)
    setSubmitting(true)
    try {
      const product = await api.createProduct({
        name,
        description,
        price,
        stock: Number(stock),
        image_url: imageUrl || null,
      })
      setCreated(product)
      setName('')
      setDescription('')
      setPrice('')
      setStock('')
      setImageUrl('')
    } catch (err) {
      setError(formatApiError(err))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div>
      <PageHero eyebrow="Управление" title="Админ: новый товар" />
      <div className="page">
      <form onSubmit={handleSubmit} className="form">
        <label>
          Название
          <input value={name} onChange={(e) => setName(e.target.value)} required />
        </label>
        <label>
          Описание
          <textarea value={description} onChange={(e) => setDescription(e.target.value)} required />
        </label>
        <label>
          Цена
          <input
            type="text"
            inputMode="decimal"
            placeholder="9.99"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            required
          />
        </label>
        <label>
          Остаток на складе
          <input
            type="number"
            min={0}
            value={stock}
            onChange={(e) => setStock(e.target.value)}
            required
          />
        </label>
        <label>
          Ссылка на картинку (необязательно)
          <input
            type="url"
            placeholder="https://..."
            value={imageUrl}
            onChange={(e) => setImageUrl(e.target.value)}
          />
        </label>
        {error && <p className="form-error">{error}</p>}
        {created && (
          <p className="form-success">
            Товар «{created.name}» создан (id {created.id})
          </p>
        )}
        <button type="submit" disabled={submitting}>
          {submitting ? 'Создаём...' : 'Создать товар'}
        </button>
      </form>
      </div>
    </div>
  )
}

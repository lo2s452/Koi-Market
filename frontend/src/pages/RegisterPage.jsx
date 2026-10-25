import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { formatApiError } from '../utils'
import { UserIcon } from '../components/icons'
import { PageHero } from '../components/PageHero'

export function RegisterPage() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError(null)
    setSubmitting(true)
    try {
      await register(username, password)
      navigate('/login', { state: { justRegistered: true } })
    } catch (err) {
      setError(err.status === 409 ? 'Это имя пользователя уже занято' : formatApiError(err))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div>
      <PageHero eyebrow="Присоединяйтесь" title="Регистрация" />
      <div className="form-page">
      <div className="product-glyph" style={{ marginBottom: '0.75rem' }}>
        <UserIcon />
      </div>
      <form onSubmit={handleSubmit} className="form">
        <label>
          Имя пользователя
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            minLength={3}
            maxLength={32}
            pattern="[A-Za-z0-9_]+"
            title="От 3 до 32 символов: латинские буквы, цифры и _"
            required
          />
        </label>
        <label>
          Пароль
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            minLength={8}
            maxLength={128}
            required
          />
        </label>
        {error && <p className="form-error">{error}</p>}
        <button type="submit" disabled={submitting}>
          {submitting ? 'Регистрируем...' : 'Зарегистрироваться'}
        </button>
      </form>
      <p>
        Уже есть аккаунт? <Link to="/login">Войти</Link>
      </p>
      </div>
    </div>
  )
}

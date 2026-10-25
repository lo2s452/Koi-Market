import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { formatApiError } from '../utils'
import { UserIcon } from '../components/icons'
import { PageHero } from '../components/PageHero'

export function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError(null)
    setSubmitting(true)
    try {
      await login(username, password)
      navigate('/products')
    } catch (err) {
      const wrongCredentials = err.status === 401 || err.status === 422
      setError(wrongCredentials ? 'Неверное имя пользователя или пароль' : formatApiError(err))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div>
      <PageHero eyebrow="Добро пожаловать" title="Вход" />
      <div className="form-page">
      <div className="product-glyph" style={{ marginBottom: '0.75rem' }}>
        <UserIcon />
      </div>
      {location.state?.justRegistered && (
        <p className="form-success">Аккаунт создан, теперь войдите.</p>
      )}
      <form onSubmit={handleSubmit} className="form">
        <label>
          Имя пользователя
          <input value={username} onChange={(e) => setUsername(e.target.value)} required />
        </label>
        <label>
          Пароль
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
        {error && <p className="form-error">{error}</p>}
        <button type="submit" disabled={submitting}>
          {submitting ? 'Входим...' : 'Войти'}
        </button>
      </form>
      <p>
        Нет аккаунта? <Link to="/register">Зарегистрироваться</Link>
      </p>
      </div>
    </div>
  )
}

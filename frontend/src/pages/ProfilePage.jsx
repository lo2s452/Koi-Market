import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { PageHero } from '../components/PageHero'

export function ProfilePage() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  async function handleLogout() {
    await logout()
    navigate('/login')
  }

  return (
    <div>
      <PageHero eyebrow="Аккаунт" title="Профиль" />
      <div className="page form-page">
        <div className="profile-card">
          <div className="profile-row">
            <span className="profile-label">Имя пользователя</span>
            <span className="profile-value">{user.username}</span>
          </div>
          {user.role === 'admin' && <span className="profile-badge">Администратор</span>}
        </div>
        <button type="button" className="btn-danger" onClick={handleLogout}>
          Выйти
        </button>
      </div>
    </div>
  )
}

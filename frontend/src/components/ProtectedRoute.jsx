import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export function ProtectedRoute() {
  const { user, status } = useAuth()

  if (status === 'loading') return <p className="page-status">Загрузка...</p>
  if (!user) return <Navigate to="/login" replace />

  return <Outlet />
}

export function AdminRoute() {
  const { user, status } = useAuth()

  if (status === 'loading') return <p className="page-status">Загрузка...</p>
  if (!user) return <Navigate to="/login" replace />
  if (user.role !== 'admin') return <p className="page-status">403 — доступ только для администратора</p>

  return <Outlet />
}

import { NavLink } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { SearchIcon } from './icons'

export function Navbar() {
  const { user, status } = useAuth()

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <NavLink to="/products">Koi Market</NavLink>
      </div>
      <div className="navbar-links">
        <NavLink to="/products">Товары</NavLink>
        {user && <NavLink to="/cart">Корзина</NavLink>}
        {user && <NavLink to="/orders">Мои заказы</NavLink>}
        {user?.role === 'admin' && <NavLink to="/admin/products">Админ: товары</NavLink>}
        {user?.role === 'admin' && <NavLink to="/admin/orders">Админ: заказы</NavLink>}
      </div>
      <div className="navbar-user">
        <NavLink to="/search" className="navbar-search" aria-label="Поиск">
          <SearchIcon className="navbar-search-icon" width={24} height={24} />
        </NavLink>
        {status === 'loading' && <span>...</span>}
        {status === 'anonymous' && (
          <>
            <NavLink to="/login">Войти</NavLink>
            <NavLink to="/register">Регистрация</NavLink>
          </>
        )}
        {user && <NavLink to="/profile" className="navbar-username">{user.username}</NavLink>}
      </div>
    </nav>
  )
}

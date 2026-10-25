import { createContext, useContext, useEffect, useState, useCallback } from 'react'
import { api, setAccessToken, refreshSession } from '../api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [status, setStatus] = useState('loading')

  useEffect(() => {
    async function restoreSession() {
      try {
        await refreshSession()
        const me = await api.me()
        setUser(me)
        setStatus('authenticated')
      } catch {
        setAccessToken(null)
        setUser(null)
        setStatus('anonymous')
      }
    }
    restoreSession()
  }, [])

  const login = useCallback(async (username, password) => {
    const data = await api.login(username, password)
    setAccessToken(data.access_token)
    const me = await api.me()
    setUser(me)
    setStatus('authenticated')
  }, [])

  const register = useCallback((username, password) => api.register(username, password), [])

  const logout = useCallback(async () => {
    try {
      await api.logout()
    } finally {
      setAccessToken(null)
      setUser(null)
      setStatus('anonymous')
    }
  }, [])

  return (
    <AuthContext.Provider value={{ user, status, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within an AuthProvider')
  return ctx
}

import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { createClient } from '@/lib/supabase/client'
import type { User, AuthState, LoginCredentials, RegisterCredentials } from '@/types/auth'

interface AuthStore extends AuthState {
  // Actions
  login: (credentials: LoginCredentials) => Promise<void>
  register: (credentials: RegisterCredentials) => Promise<void>
  logout: () => Promise<void>
  resetPassword: (email: string) => Promise<void>
  updatePassword: (password: string) => Promise<void>
  refreshSession: () => Promise<void>
  setUser: (user: User | null) => void
  setError: (error: string | null) => void
  clearError: () => void
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      // Initial state
      user: null,
      session: null,
      isLoading: false,
      error: null,

      // Actions
      login: async (credentials) => {
        set({ isLoading: true, error: null })
        try {
          // Handle demo login
          if (credentials.email === 'demo@demo.com' && credentials.password === 'password') {
            const demoUser: User = {
              id: 'demo-user-id',
              email: 'demo@demo.com',
              fullName: 'Demo User',
              avatarUrl: null,
              createdAt: new Date().toISOString(),
              updatedAt: new Date().toISOString(),
            }
            set({ user: demoUser, session: null, isLoading: false })
            return
          }

          const supabase = createClient()
          const { data, error } = await supabase.auth.signInWithPassword({
            email: credentials.email,
            password: credentials.password,
          })

          if (error) throw error

          if (data.user) {
            const user: User = {
              id: data.user.id,
              email: data.user.email!,
              fullName: data.user.user_metadata?.full_name,
              avatarUrl: data.user.user_metadata?.avatar_url,
              createdAt: data.user.created_at,
              updatedAt: data.user.updated_at || data.user.created_at,
            }
            set({ user, session: data.session, isLoading: false })
          }
        } catch (error: any) {
          set({ error: error.message, isLoading: false })
          throw error
        }
      },

      register: async (credentials) => {
        set({ isLoading: true, error: null })
        try {
          const supabase = createClient()
          const { data, error } = await supabase.auth.signUp({
            email: credentials.email,
            password: credentials.password,
            options: {
              data: {
                full_name: credentials.fullName,
              },
            },
          })

          if (error) throw error

          if (data.user) {
            const user: User = {
              id: data.user.id,
              email: data.user.email!,
              fullName: credentials.fullName,
              avatarUrl: null,
              createdAt: data.user.created_at,
              updatedAt: data.user.created_at,
            }
            set({ user, session: data.session, isLoading: false })
          }
        } catch (error: any) {
          set({ error: error.message, isLoading: false })
          throw error
        }
      },

      logout: async () => {
        set({ isLoading: true })
        try {
          const { user } = get()
          
          // Handle demo user logout
          if (user?.id === 'demo-user-id') {
            set({ user: null, session: null, isLoading: false })
            return
          }

          const supabase = createClient()
          const { error } = await supabase.auth.signOut()
          if (error) throw error
          set({ user: null, session: null, isLoading: false })
        } catch (error: any) {
          set({ error: error.message, isLoading: false })
          throw error
        }
      },

      resetPassword: async (email) => {
        set({ isLoading: true, error: null })
        try {
          const supabase = createClient()
          const { error } = await supabase.auth.resetPasswordForEmail(email, {
            redirectTo: `${window.location.origin}/auth/reset-password`,
          })
          if (error) throw error
          set({ isLoading: false })
        } catch (error: any) {
          set({ error: error.message, isLoading: false })
          throw error
        }
      },

      updatePassword: async (password) => {
        set({ isLoading: true, error: null })
        try {
          const supabase = createClient()
          const { error } = await supabase.auth.updateUser({
            password,
          })
          if (error) throw error
          set({ isLoading: false })
        } catch (error: any) {
          set({ error: error.message, isLoading: false })
          throw error
        }
      },

      refreshSession: async () => {
        try {
          const supabase = createClient()
          const { data, error } = await supabase.auth.refreshSession()
          if (error) throw error
          if (data.session) {
            set({ session: data.session })
          }
        } catch (error: any) {
          console.error('Session refresh failed:', error)
          set({ user: null, session: null })
        }
      },

      setUser: (user) => set({ user }),
      setError: (error) => set({ error }),
      clearError: () => set({ error: null }),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ user: state.user }),
    }
  )
)
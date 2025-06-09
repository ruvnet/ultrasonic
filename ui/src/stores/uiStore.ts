import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import { immer } from 'zustand/middleware/immer'

export interface Notification {
  id: string
  type: 'info' | 'success' | 'warning' | 'error'
  title: string
  message?: string
  duration?: number
  timestamp: number
}

interface UIState {
  // Theme
  theme: 'light' | 'dark' | 'system'
  
  // Modals
  modals: {
    settings: boolean
    help: boolean
    about: boolean
    encodingPresets: boolean
    decodingSettings: boolean
  }
  
  // Layout
  sidebarCollapsed: boolean
  activeView: 'encode' | 'decode' | 'analyze' | 'history'
  
  // Notifications
  notifications: Notification[]
  
  // Loading states
  globalLoading: boolean
  loadingMessage: string | null
  
  // Actions
  setTheme: (theme: UIState['theme']) => void
  toggleSidebar: () => void
  setActiveView: (view: UIState['activeView']) => void
  openModal: (modal: keyof UIState['modals']) => void
  closeModal: (modal: keyof UIState['modals']) => void
  showNotification: (notification: Omit<Notification, 'id' | 'timestamp'>) => void
  dismissNotification: (id: string) => void
  clearAllNotifications: () => void
  setGlobalLoading: (loading: boolean, message?: string) => void
}

export const useUIStore = create<UIState>()(
  devtools(
    persist(
      immer((set, get) => ({
        // Initial state
        theme: 'system',
        modals: {
          settings: false,
          help: false,
          about: false,
          encodingPresets: false,
          decodingSettings: false
        },
        sidebarCollapsed: false,
        activeView: 'encode',
        notifications: [],
        globalLoading: false,
        loadingMessage: null,
        
        // Actions
        setTheme: (theme: UIState['theme']) => {
          set(state => {
            state.theme = theme
          })
          
          // Apply theme to document
          if (theme === 'system') {
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
            document.documentElement.classList.toggle('dark', prefersDark)
          } else {
            document.documentElement.classList.toggle('dark', theme === 'dark')
          }
        },
        
        toggleSidebar: () => {
          set(state => {
            state.sidebarCollapsed = !state.sidebarCollapsed
          })
        },
        
        setActiveView: (view: UIState['activeView']) => {
          set(state => {
            state.activeView = view
          })
        },
        
        openModal: (modal: keyof UIState['modals']) => {
          set(state => {
            state.modals[modal] = true
          })
        },
        
        closeModal: (modal: keyof UIState['modals']) => {
          set(state => {
            state.modals[modal] = false
          })
        },
        
        showNotification: (notification: Omit<Notification, 'id' | 'timestamp'>) => {
          const id = `notification-${Date.now()}-${Math.random()}`
          const timestamp = Date.now()
          const duration = notification.duration || (notification.type === 'error' ? 10000 : 5000)
          
          set(state => {
            state.notifications.push({
              ...notification,
              id,
              timestamp,
              duration
            })
          })
          
          // Auto dismiss after duration
          if (duration > 0) {
            setTimeout(() => {
              get().dismissNotification(id)
            }, duration)
          }
        },
        
        dismissNotification: (id: string) => {
          set(state => {
            state.notifications = state.notifications.filter(n => n.id !== id)
          })
        },
        
        clearAllNotifications: () => {
          set(state => {
            state.notifications = []
          })
        },
        
        setGlobalLoading: (loading: boolean, message?: string) => {
          set(state => {
            state.globalLoading = loading
            state.loadingMessage = message || null
          })
        }
      })),
      {
        name: 'ui-store',
        partialize: (state) => ({
          theme: state.theme,
          sidebarCollapsed: state.sidebarCollapsed,
          activeView: state.activeView
        })
      }
    ),
    { name: 'ui-store' }
  )
)
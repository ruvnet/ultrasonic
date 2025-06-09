import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useEffect } from 'react'
import { DashboardLayout } from '@/components/layouts/DashboardLayout'
import { RegisterPage } from '@/pages/auth/RegisterPage'
import { ForgotPasswordPage } from '@/pages/auth/ForgotPasswordPage'
import { DashboardPage } from '@/pages/dashboard/DashboardPage'
import { EmbedPage } from '@/pages/dashboard/EmbedPage'
import { DecodePage } from '@/pages/dashboard/DecodePage'
import { AnalyzePage } from '@/pages/dashboard/AnalyzePage'
import { HistoryPage } from '@/pages/dashboard/HistoryPage'
import { SettingsPage } from '@/pages/settings/SettingsPage'
import { ProfilePage } from '@/pages/settings/ProfilePage'
import { SecurityPage } from '@/pages/settings/SecurityPage'
import { PreferencesPage } from '@/pages/settings/PreferencesPage'
import { HelpPage } from '@/pages/help/HelpPage'
import { ApiDocsPage } from '@/pages/help/ApiDocsPage'
import { TutorialsPage } from '@/pages/help/TutorialsPage'
import { FaqPage } from '@/pages/help/FaqPage'
import { WelcomePage } from '@/pages/WelcomePage'
import { ModernLoginPage } from '@/pages/auth/ModernLoginPage'
import { ModernDashboardPage } from '@/pages/dashboard/ModernDashboardPage'
import { ProtectedRoute } from '@/components/auth/ProtectedRoute'
import { useAuthStore } from '@/stores/auth-store'
import { createClient } from '@/lib/supabase/client'

// MSW temporarily disabled to fix service worker issues
// TODO: Re-enable MSW after proper setup
// if (import.meta.env.VITE_ENABLE_MOCK_API === 'true') {
//   import('./mocks/browser').then(({ worker }) => {
//     worker.start({
//       onUnhandledRequest: 'bypass',
//     }).catch(console.error)
//   }).catch(console.error)
// }

function App() {
  const { setUser, refreshSession } = useAuthStore()

  useEffect(() => {
    // Check for existing session
    const supabase = createClient()
    
    supabase.auth.getSession().then(({ data: { session } }) => {
      if (session?.user) {
        setUser({
          id: session.user.id,
          email: session.user.email!,
          fullName: session.user.user_metadata?.full_name,
          avatarUrl: session.user.user_metadata?.avatar_url,
          createdAt: session.user.created_at,
          updatedAt: session.user.updated_at || session.user.created_at,
        })
      }
    })

    // Listen for auth changes
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      if (session?.user) {
        setUser({
          id: session.user.id,
          email: session.user.email!,
          fullName: session.user.user_metadata?.full_name,
          avatarUrl: session.user.user_metadata?.avatar_url,
          createdAt: session.user.created_at,
          updatedAt: session.user.updated_at || session.user.created_at,
        })
      } else {
        setUser(null)
      }
    })

    // Refresh session periodically
    const interval = setInterval(() => {
      refreshSession()
    }, 30 * 60 * 1000) // 30 minutes

    return () => {
      subscription.unsubscribe()
      clearInterval(interval)
    }
  }, [setUser, refreshSession])

  return (
    <Router>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<WelcomePage />} />
        <Route path="/welcome" element={<WelcomePage />} />
        <Route path="/login" element={<ModernLoginPage />} />
        <Route path="/auth/login" element={<ModernLoginPage />} />
        <Route path="/auth/register" element={<RegisterPage />} />
        <Route path="/auth/forgot-password" element={<ForgotPasswordPage />} />

        {/* Protected routes */}
        <Route element={<ProtectedRoute />}>
          <Route element={<DashboardLayout />}>
            {/* Dashboard */}
            <Route path="/dashboard" element={<ModernDashboardPage />} />
            <Route path="/dashboard/embed" element={<EmbedPage />} />
            <Route path="/dashboard/decode" element={<DecodePage />} />
            <Route path="/dashboard/analyze" element={<AnalyzePage />} />
            <Route path="/dashboard/history" element={<HistoryPage />} />

            {/* Settings */}
            <Route path="/settings" element={<SettingsPage />} />
            <Route path="/settings/profile" element={<ProfilePage />} />
            <Route path="/settings/security" element={<SecurityPage />} />
            <Route path="/settings/preferences" element={<PreferencesPage />} />

            {/* Help */}
            <Route path="/help" element={<HelpPage />} />
            <Route path="/help/api" element={<ApiDocsPage />} />
            <Route path="/help/tutorials" element={<TutorialsPage />} />
            <Route path="/help/faq" element={<FaqPage />} />
          </Route>
        </Route>

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  )
}

export default App
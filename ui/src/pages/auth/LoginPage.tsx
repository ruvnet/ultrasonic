import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { useAuthStore } from '@/stores/auth-store'
import { AlertCircle, RadioIcon, Eye, EyeOff, Mail, Lock } from 'lucide-react'

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
})

type LoginFormData = z.infer<typeof loginSchema>

export function LoginPage() {
  const navigate = useNavigate()
  const { login, error, clearError } = useAuthStore()
  const [isLoading, setIsLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  })

  const onSubmit = async (data: LoginFormData) => {
    setIsLoading(true)
    clearError()
    
    try {
      // Demo login check
      if (data.email === 'demo@demo.com' && data.password === 'password') {
        // Simulate successful demo login
        navigate('/dashboard')
        return
      }
      
      await login(data)
      navigate('/dashboard')
    } catch (err) {
      // Error is handled by the store
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div 
      className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 px-4"
      style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #eff6ff, #e0e7ff)',
        padding: '1rem'
      }}
    >
      <Card className="w-full max-w-md" style={{width: '100%', maxWidth: '28rem', backgroundColor: 'white', borderRadius: '0.5rem', boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)'}}>
        <CardHeader className="space-y-1" style={{textAlign: 'center', padding: '1.5rem 1.5rem 0'}}>
          <div className="flex items-center justify-center mb-4" style={{display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1rem'}}>
            <RadioIcon className="h-8 w-8 text-blue-600" style={{height: '2rem', width: '2rem', color: '#2563eb'}} />
            <h1 className="ml-2 text-xl font-bold" style={{marginLeft: '0.5rem', fontSize: '1.25rem', fontWeight: 'bold'}}>
              Ultrasonic Agentics
            </h1>
          </div>
          <CardTitle className="text-2xl font-bold" style={{fontSize: '1.5rem', fontWeight: 'bold'}}>Welcome back</CardTitle>
          <CardDescription style={{color: '#6b7280'}}>
            Enter your credentials to access your steganography dashboard
          </CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit(onSubmit)}>
          <CardContent className="space-y-4" style={{padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem'}}>
            {error && (
              <div 
                className="flex items-center gap-2 p-3 text-sm text-destructive bg-destructive/10 rounded-md"
                style={{display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.75rem', fontSize: '0.875rem', color: '#dc2626', backgroundColor: '#fef2f2', borderRadius: '0.375rem'}}
              >
                <AlertCircle className="h-4 w-4" style={{height: '1rem', width: '1rem'}} />
                <span>{error}</span>
              </div>
            )}
            
            <div className="space-y-2" style={{display: 'flex', flexDirection: 'column', gap: '0.5rem'}}>
              <Label htmlFor="email" style={{fontSize: '0.875rem', fontWeight: '500'}}>Email</Label>
              <div className="relative" style={{position: 'relative'}}>
                <Mail className="absolute left-3 top-3 h-4 w-4 text-gray-400" style={{position: 'absolute', left: '0.75rem', top: '0.75rem', height: '1rem', width: '1rem', color: '#9ca3af'}} />
                <Input
                  id="email"
                  type="email"
                  placeholder="you@example.com"
                  className="pl-10"
                  style={{paddingLeft: '2.5rem', width: '100%', padding: '0.5rem 0.75rem 0.5rem 2.5rem', border: '1px solid #d1d5db', borderRadius: '0.375rem'}}
                  {...register('email')}
                  disabled={isLoading}
                />
              </div>
              {errors.email && (
                <p className="text-sm text-destructive" style={{fontSize: '0.875rem', color: '#dc2626'}}>{errors.email.message}</p>
              )}
            </div>

            <div className="space-y-2" style={{display: 'flex', flexDirection: 'column', gap: '0.5rem'}}>
              <Label htmlFor="password" style={{fontSize: '0.875rem', fontWeight: '500'}}>Password</Label>
              <div className="relative" style={{position: 'relative'}}>
                <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-400" style={{position: 'absolute', left: '0.75rem', top: '0.75rem', height: '1rem', width: '1rem', color: '#9ca3af'}} />
                <Input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  className="pl-10 pr-10"
                  style={{paddingLeft: '2.5rem', paddingRight: '2.5rem', width: '100%', padding: '0.5rem 2.5rem 0.5rem 2.5rem', border: '1px solid #d1d5db', borderRadius: '0.375rem'}}
                  {...register('password')}
                  disabled={isLoading}
                />
                <Button
                  type="button"
                  variant="ghost"
                  size="icon"
                  className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                  style={{position: 'absolute', right: '0', top: '0', height: '100%', padding: '0.5rem 0.75rem', background: 'transparent', border: 'none', cursor: 'pointer'}}
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? (
                    <EyeOff className="h-4 w-4 text-gray-400" style={{height: '1rem', width: '1rem', color: '#9ca3af'}} />
                  ) : (
                    <Eye className="h-4 w-4 text-gray-400" style={{height: '1rem', width: '1rem', color: '#9ca3af'}} />
                  )}
                </Button>
              </div>
              {errors.password && (
                <p className="text-sm text-destructive" style={{fontSize: '0.875rem', color: '#dc2626'}}>{errors.password.message}</p>
              )}
            </div>
          </CardContent>
          <CardFooter className="flex flex-col space-y-4" style={{padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem'}}>
            <Button
              type="submit"
              className="w-full"
              disabled={isLoading}
              style={{
                width: '100%',
                background: isLoading ? '#9ca3af' : '#2563eb',
                color: 'white',
                padding: '0.5rem 1rem',
                borderRadius: '0.375rem',
                border: 'none',
                cursor: isLoading ? 'not-allowed' : 'pointer',
                fontSize: '0.875rem',
                fontWeight: '500'
              }}
            >
              {isLoading ? 'Signing in...' : 'Sign in'}
            </Button>
            
            <div className="text-sm text-center space-y-2" style={{fontSize: '0.875rem', textAlign: 'center', display: 'flex', flexDirection: 'column', gap: '0.5rem'}}>
              <Link
                to="/auth/forgot-password"
                className="text-primary hover:underline"
                style={{color: '#2563eb', textDecoration: 'none'}}
              >
                Forgot your password?
              </Link>
              <p className="text-muted-foreground" style={{color: '#6b7280'}}>
                Don't have an account?{' '}
                <Link
                  to="/auth/register"
                  className="text-primary hover:underline"
                  style={{color: '#2563eb', textDecoration: 'none', fontWeight: '500'}}
                >
                  Sign up
                </Link>
              </p>
            </div>
          </CardFooter>
        </form>
      </Card>
    </div>
  )
}
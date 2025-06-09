import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { useAuthStore } from '@/stores/auth-store'
import { AlertCircle, RadioIcon, Eye, EyeOff, Mail, Lock, ArrowRight, CheckCircle } from 'lucide-react'

const loginSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(1, 'Password is required'),
})

type LoginFormData = z.infer<typeof loginSchema>

export function ModernLoginPage() {
  const navigate = useNavigate()
  const { login, error, clearError } = useAuthStore()
  const [isLoading, setIsLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  })

  const onSubmit = async (data: LoginFormData) => {
    setIsLoading(true)
    clearError()
    
    try {
      await login(data)
      navigate('/dashboard')
    } catch (err) {
      // Error is handled by the store
    } finally {
      setIsLoading(false)
    }
  }

  const fillDemoCredentials = () => {
    setValue('email', 'demo@demo.com')
    setValue('password', 'password')
  }

  return (
    <div 
      style={{
        minHeight: '100vh',
        display: 'flex',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
      }}
    >
      {/* Left Panel - Branding */}
      <div 
        style={{
          flex: '1',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          padding: '3rem',
          color: 'white',
          position: 'relative',
          overflow: 'hidden'
        }}
      >
        {/* Background Pattern */}
        <div 
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            opacity: 0.1,
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='4'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
          }}
        />
        
        <div style={{ position: 'relative', textAlign: 'center', maxWidth: '400px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '2rem' }}>
            <div 
              style={{
                width: '60px',
                height: '60px',
                background: 'rgba(255, 255, 255, 0.2)',
                borderRadius: '12px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginRight: '1rem'
              }}
            >
              <RadioIcon style={{ width: '32px', height: '32px', color: 'white' }} />
            </div>
            <h1 style={{ fontSize: '28px', fontWeight: '700', margin: 0 }}>
              Ultrasonic Agentics
            </h1>
          </div>
          
          <h2 style={{ fontSize: '24px', fontWeight: '600', marginBottom: '1rem', lineHeight: '1.2' }}>
            Advanced Steganography Platform
          </h2>
          
          <p style={{ fontSize: '18px', opacity: 0.9, lineHeight: '1.6', marginBottom: '2rem' }}>
            Hide encrypted commands in audio and video files using cutting-edge ultrasonic technology and military-grade encryption.
          </p>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', textAlign: 'left' }}>
            {[
              'AES-256 Military-grade encryption',
              'Ultrasonic frequency embedding (18-22kHz)',
              'Support for multiple media formats',
              'Real-time analysis and detection'
            ].map((feature, index) => (
              <div key={index} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <CheckCircle style={{ width: '20px', height: '20px', color: '#4ade80' }} />
                <span style={{ fontSize: '16px' }}>{feature}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Right Panel - Login Form */}
      <div 
        style={{
          flex: '1',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '2rem',
          backgroundColor: '#fafafa'
        }}
      >
        <div style={{ width: '100%', maxWidth: '400px' }}>
          <Card 
            style={{
              backgroundColor: 'white',
              border: 'none',
              borderRadius: '16px',
              boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
              padding: '0'
            }}
          >
            <CardHeader style={{ padding: '2rem 2rem 1rem', textAlign: 'center' }}>
              <CardTitle style={{ fontSize: '28px', fontWeight: '700', color: '#1f2937', marginBottom: '0.5rem' }}>
                Welcome back
              </CardTitle>
              <CardDescription style={{ fontSize: '16px', color: '#6b7280' }}>
                Sign in to your steganography dashboard
              </CardDescription>
            </CardHeader>

            <CardContent style={{ padding: '0 2rem 2rem' }}>
              {/* Demo Banner */}
              <div 
                style={{
                  background: 'linear-gradient(90deg, #fef3c7, #fde68a)',
                  border: '1px solid #f59e0b',
                  borderRadius: '8px',
                  padding: '1rem',
                  marginBottom: '1.5rem',
                  textAlign: 'center'
                }}
              >
                <p style={{ margin: '0 0 0.5rem', fontSize: '14px', fontWeight: '600', color: '#92400e' }}>
                  🚀 Try the demo
                </p>
                <button
                  type="button"
                  onClick={fillDemoCredentials}
                  style={{
                    background: 'none',
                    border: 'none',
                    color: '#1d4ed8',
                    fontSize: '14px',
                    fontWeight: '500',
                    cursor: 'pointer',
                    textDecoration: 'underline'
                  }}
                >
                  Click here to fill demo credentials
                </button>
                <p style={{ margin: '0.25rem 0 0', fontSize: '12px', color: '#78716c' }}>
                  demo@demo.com / password
                </p>
              </div>

              <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                {error && (
                  <div 
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.75rem',
                      padding: '1rem',
                      backgroundColor: '#fef2f2',
                      border: '1px solid #fecaca',
                      borderRadius: '8px',
                      color: '#dc2626'
                    }}
                  >
                    <AlertCircle style={{ width: '16px', height: '16px', flexShrink: 0 }} />
                    <span style={{ fontSize: '14px' }}>{error}</span>
                  </div>
                )}
                
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  <Label htmlFor="email" style={{ fontSize: '14px', fontWeight: '500', color: '#374151' }}>
                    Email address
                  </Label>
                  <div style={{ position: 'relative' }}>
                    <Mail 
                      style={{
                        position: 'absolute',
                        left: '12px',
                        top: '50%',
                        transform: 'translateY(-50%)',
                        width: '18px',
                        height: '18px',
                        color: '#9ca3af'
                      }} 
                    />
                    <Input
                      id="email"
                      type="email"
                      placeholder="Enter your email"
                      style={{
                        paddingLeft: '40px',
                        height: '48px',
                        border: '2px solid #e5e7eb',
                        borderRadius: '8px',
                        fontSize: '16px',
                        transition: 'border-color 0.15s ease-in-out',
                        backgroundColor: 'white'
                      }}
                      {...register('email')}
                      disabled={isLoading}
                    />
                  </div>
                  {errors.email && (
                    <p style={{ fontSize: '14px', color: '#dc2626', margin: 0 }}>
                      {errors.email.message}
                    </p>
                  )}
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  <Label htmlFor="password" style={{ fontSize: '14px', fontWeight: '500', color: '#374151' }}>
                    Password
                  </Label>
                  <div style={{ position: 'relative' }}>
                    <Lock 
                      style={{
                        position: 'absolute',
                        left: '12px',
                        top: '50%',
                        transform: 'translateY(-50%)',
                        width: '18px',
                        height: '18px',
                        color: '#9ca3af'
                      }} 
                    />
                    <Input
                      id="password"
                      type={showPassword ? 'text' : 'password'}
                      placeholder="Enter your password"
                      style={{
                        paddingLeft: '40px',
                        paddingRight: '40px',
                        height: '48px',
                        border: '2px solid #e5e7eb',
                        borderRadius: '8px',
                        fontSize: '16px',
                        transition: 'border-color 0.15s ease-in-out',
                        backgroundColor: 'white'
                      }}
                      {...register('password')}
                      disabled={isLoading}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      style={{
                        position: 'absolute',
                        right: '12px',
                        top: '50%',
                        transform: 'translateY(-50%)',
                        background: 'none',
                        border: 'none',
                        cursor: 'pointer',
                        padding: '4px'
                      }}
                    >
                      {showPassword ? (
                        <EyeOff style={{ width: '18px', height: '18px', color: '#9ca3af' }} />
                      ) : (
                        <Eye style={{ width: '18px', height: '18px', color: '#9ca3af' }} />
                      )}
                    </button>
                  </div>
                  {errors.password && (
                    <p style={{ fontSize: '14px', color: '#dc2626', margin: 0 }}>
                      {errors.password.message}
                    </p>
                  )}
                </div>

                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <input 
                      type="checkbox" 
                      id="remember" 
                      style={{ width: '16px', height: '16px' }}
                    />
                    <label htmlFor="remember" style={{ fontSize: '14px', color: '#6b7280', cursor: 'pointer' }}>
                      Remember me
                    </label>
                  </div>
                  <Link 
                    to="/auth/forgot-password" 
                    style={{ fontSize: '14px', color: '#4f46e5', textDecoration: 'none', fontWeight: '500' }}
                  >
                    Forgot password?
                  </Link>
                </div>

                <Button
                  type="submit"
                  disabled={isLoading}
                  style={{
                    width: '100%',
                    height: '48px',
                    background: isLoading ? '#9ca3af' : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    color: 'white',
                    border: 'none',
                    borderRadius: '8px',
                    fontSize: '16px',
                    fontWeight: '600',
                    cursor: isLoading ? 'not-allowed' : 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '0.5rem',
                    transition: 'all 0.15s ease-in-out'
                  }}
                >
                  {isLoading ? (
                    <>
                      <div 
                        style={{
                          width: '20px',
                          height: '20px',
                          border: '2px solid #ffffff',
                          borderTop: '2px solid transparent',
                          borderRadius: '50%',
                          animation: 'spin 1s linear infinite'
                        }}
                      />
                      Signing in...
                    </>
                  ) : (
                    <>
                      Sign in to dashboard
                      <ArrowRight style={{ width: '18px', height: '18px' }} />
                    </>
                  )}
                </Button>
              </form>

              <div style={{ marginTop: '2rem', textAlign: 'center' }}>
                <p style={{ fontSize: '14px', color: '#6b7280', margin: 0 }}>
                  Don't have an account?{' '}
                  <Link 
                    to="/auth/register" 
                    style={{ color: '#4f46e5', textDecoration: 'none', fontWeight: '600' }}
                  >
                    Sign up for free
                  </Link>
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Add keyframes for spinner animation */}
      <style>
        {`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}
      </style>
    </div>
  )
}
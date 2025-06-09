import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { 
  Upload, 
  Download, 
  BarChart3, 
  Activity,
  FileAudio,
  FileVideo,
  Shield,
  Zap,
  TrendingUp,
  Clock,
  CheckCircle,
  AlertTriangle,
  RadioIcon,
  Settings,
  LogOut,
  User,
  Bell
} from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

interface Stats {
  totalOperations: number
  embedOperations: number
  decodeOperations: number
  successRate: number
}

export function ModernDashboardPage() {
  const [stats, setStats] = useState<Stats>({
    totalOperations: 0,
    embedOperations: 0,
    decodeOperations: 0,
    successRate: 0,
  })
  const [isHealthy, setIsHealthy] = useState(true)

  useEffect(() => {
    // Simulate loading stats
    setTimeout(() => {
      setStats({
        totalOperations: 142,
        embedOperations: 89,
        decodeOperations: 53,
        successRate: 98.5,
      })
    }, 500)
  }, [])

  const quickActions = [
    {
      title: 'Embed Command',
      description: 'Hide encrypted commands in audio/video files',
      icon: Upload,
      href: '/dashboard/embed',
      color: '#3b82f6',
      bgColor: '#eff6ff',
    },
    {
      title: 'Decode File',
      description: 'Extract and decrypt hidden commands',
      icon: Download,
      href: '/dashboard/decode',
      color: '#10b981',
      bgColor: '#f0fdf4',
    },
    {
      title: 'Analyze Media',
      description: 'Detect steganographic content',
      icon: BarChart3,
      href: '/dashboard/analyze',
      color: '#8b5cf6',
      bgColor: '#faf5ff',
    },
  ]

  const recentActivity = [
    { action: 'Embedded command in audio.mp3', time: '2 minutes ago', status: 'success' },
    { action: 'Decoded message from video.mp4', time: '15 minutes ago', status: 'success' },
    { action: 'Failed to decode corrupt_file.wav', time: '1 hour ago', status: 'error' },
    { action: 'Analyzed suspicious_audio.mp3', time: '2 hours ago', status: 'warning' },
  ]

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f8fafc', fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' }}>
      {/* Header */}
      <header 
        style={{
          backgroundColor: 'white',
          borderBottom: '1px solid #e2e8f0',
          padding: '1rem 2rem',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <RadioIcon style={{ width: '32px', height: '32px', color: '#4f46e5' }} />
            <h1 style={{ fontSize: '24px', fontWeight: '700', color: '#1e293b', margin: 0 }}>
              Ultrasonic Agentics
            </h1>
          </div>
        </div>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <Button 
            variant="outline" 
            style={{ background: 'none', border: '1px solid #e2e8f0', padding: '0.5rem', borderRadius: '0.5rem' }}
          >
            <Bell style={{ width: '18px', height: '18px', color: '#64748b' }} />
          </Button>
          <Button 
            variant="outline" 
            style={{ background: 'none', border: '1px solid #e2e8f0', padding: '0.5rem', borderRadius: '0.5rem' }}
          >
            <Settings style={{ width: '18px', height: '18px', color: '#64748b' }} />
          </Button>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div 
              style={{
                width: '40px',
                height: '40px',
                borderRadius: '50%',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              <User style={{ width: '20px', height: '20px', color: 'white' }} />
            </div>
            <div>
              <p style={{ margin: 0, fontSize: '14px', fontWeight: '600', color: '#1e293b' }}>Demo User</p>
              <p style={{ margin: 0, fontSize: '12px', color: '#64748b' }}>demo@demo.com</p>
            </div>
          </div>
        </div>
      </header>

      <div style={{ padding: '2rem' }}>
        {/* Welcome Section */}
        <div style={{ marginBottom: '2rem' }}>
          <h2 style={{ fontSize: '32px', fontWeight: '700', color: '#1e293b', margin: '0 0 0.5rem 0' }}>
            Welcome back, Demo User! 👋
          </h2>
          <p style={{ fontSize: '18px', color: '#64748b', margin: 0 }}>
            Manage your steganographic operations from your dashboard
          </p>
        </div>

        {/* System Status */}
        <Card style={{ backgroundColor: 'white', borderRadius: '16px', border: '1px solid #e2e8f0', boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)', marginBottom: '2rem' }}>
          <CardHeader style={{ padding: '1.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <CardTitle style={{ fontSize: '18px', fontWeight: '600', color: '#1e293b' }}>System Status</CardTitle>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <div 
                  style={{
                    width: '8px',
                    height: '8px',
                    borderRadius: '50%',
                    backgroundColor: isHealthy ? '#10b981' : '#ef4444'
                  }}
                />
                <span style={{ fontSize: '14px', fontWeight: '500', color: isHealthy ? '#10b981' : '#ef4444' }}>
                  {isHealthy ? 'All Systems Operational' : 'Service Degraded'}
                </span>
              </div>
            </div>
          </CardHeader>
        </Card>

        {/* Stats Grid */}
        <div style={{ display: 'grid', gap: '1.5rem', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', marginBottom: '2rem' }}>
          {[
            { title: 'Total Operations', value: stats.totalOperations, icon: Activity, change: '+12%', color: '#3b82f6' },
            { title: 'Embed Operations', value: stats.embedOperations, icon: Upload, change: '+8%', color: '#10b981' },
            { title: 'Decode Operations', value: stats.decodeOperations, icon: Download, change: '+15%', color: '#f59e0b' },
            { title: 'Success Rate', value: `${stats.successRate}%`, icon: TrendingUp, change: '+0.3%', color: '#8b5cf6' },
          ].map((stat, index) => (
            <Card key={index} style={{ backgroundColor: 'white', borderRadius: '16px', border: '1px solid #e2e8f0', boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)' }}>
              <CardContent style={{ padding: '1.5rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
                  <div 
                    style={{
                      width: '48px',
                      height: '48px',
                      borderRadius: '12px',
                      backgroundColor: `${stat.color}15`,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center'
                    }}
                  >
                    <stat.icon style={{ width: '24px', height: '24px', color: stat.color }} />
                  </div>
                  <span style={{ fontSize: '12px', fontWeight: '500', color: '#10b981' }}>
                    {stat.change}
                  </span>
                </div>
                <h3 style={{ fontSize: '28px', fontWeight: '700', color: '#1e293b', margin: '0 0 0.25rem 0' }}>
                  {stat.value}
                </h3>
                <p style={{ fontSize: '14px', color: '#64748b', margin: 0 }}>
                  {stat.title}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>

        <div style={{ display: 'grid', gap: '2rem', gridTemplateColumns: '2fr 1fr' }}>
          {/* Quick Actions */}
          <div>
            <h3 style={{ fontSize: '20px', fontWeight: '600', color: '#1e293b', marginBottom: '1rem' }}>
              Quick Actions
            </h3>
            <div style={{ display: 'grid', gap: '1rem', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))' }}>
              {quickActions.map((action, index) => (
                <Card key={index} style={{ backgroundColor: 'white', borderRadius: '16px', border: '1px solid #e2e8f0', boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)', cursor: 'pointer', transition: 'all 0.2s ease' }}>
                  <CardContent style={{ padding: '1.5rem' }}>
                    <div 
                      style={{
                        width: '56px',
                        height: '56px',
                        borderRadius: '12px',
                        backgroundColor: action.bgColor,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        marginBottom: '1rem'
                      }}
                    >
                      <action.icon style={{ width: '28px', height: '28px', color: action.color }} />
                    </div>
                    <h4 style={{ fontSize: '18px', fontWeight: '600', color: '#1e293b', margin: '0 0 0.5rem 0' }}>
                      {action.title}
                    </h4>
                    <p style={{ fontSize: '14px', color: '#64748b', margin: '0 0 1rem 0' }}>
                      {action.description}
                    </p>
                    <Button 
                      style={{
                        background: action.color,
                        color: 'white',
                        border: 'none',
                        borderRadius: '8px',
                        padding: '0.5rem 1rem',
                        fontSize: '14px',
                        fontWeight: '500',
                        cursor: 'pointer'
                      }}
                    >
                      Get Started
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>

          {/* Recent Activity */}
          <div>
            <h3 style={{ fontSize: '20px', fontWeight: '600', color: '#1e293b', marginBottom: '1rem' }}>
              Recent Activity
            </h3>
            <Card style={{ backgroundColor: 'white', borderRadius: '16px', border: '1px solid #e2e8f0', boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)' }}>
              <CardContent style={{ padding: '1.5rem' }}>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                  {recentActivity.map((activity, index) => (
                    <div key={index} style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem' }}>
                      <div 
                        style={{
                          width: '32px',
                          height: '32px',
                          borderRadius: '50%',
                          backgroundColor: activity.status === 'success' ? '#10b981' : activity.status === 'error' ? '#ef4444' : '#f59e0b',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          flexShrink: 0
                        }}
                      >
                        {activity.status === 'success' ? (
                          <CheckCircle style={{ width: '16px', height: '16px', color: 'white' }} />
                        ) : activity.status === 'error' ? (
                          <AlertTriangle style={{ width: '16px', height: '16px', color: 'white' }} />
                        ) : (
                          <Clock style={{ width: '16px', height: '16px', color: 'white' }} />
                        )}
                      </div>
                      <div style={{ flex: 1 }}>
                        <p style={{ fontSize: '14px', fontWeight: '500', color: '#1e293b', margin: '0 0 0.25rem 0' }}>
                          {activity.action}
                        </p>
                        <p style={{ fontSize: '12px', color: '#64748b', margin: 0 }}>
                          {activity.time}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
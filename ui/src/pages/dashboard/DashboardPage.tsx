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
  Zap
} from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { apiClient } from '@/lib/api/client'
import { useAuthStore } from '@/stores/auth-store'
import { cn } from '@/lib/utils'

interface Stats {
  totalOperations: number
  embedOperations: number
  decodeOperations: number
  successRate: number
}

export function DashboardPage() {
  const { user } = useAuthStore()
  const [stats, setStats] = useState<Stats>({
    totalOperations: 0,
    embedOperations: 0,
    decodeOperations: 0,
    successRate: 0,
  })
  const [isHealthy, setIsHealthy] = useState(true)

  useEffect(() => {
    // Check API health
    apiClient.getHealth().then((response) => {
      setIsHealthy(response.status === 'healthy')
    }).catch(() => {
      setIsHealthy(false)
    })

    // Simulate loading stats
    // In a real app, this would fetch from your backend
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
      description: 'Hide a command in audio or video',
      icon: Upload,
      href: '/dashboard/embed',
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
    },
    {
      title: 'Decode File',
      description: 'Extract hidden commands',
      icon: Download,
      href: '/dashboard/decode',
      color: 'text-green-600',
      bgColor: 'bg-green-50',
    },
    {
      title: 'Analyze Media',
      description: 'Detect steganographic content',
      icon: BarChart3,
      href: '/dashboard/analyze',
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
    },
  ]

  const features = [
    {
      icon: FileAudio,
      title: 'Audio Processing',
      description: 'Support for MP3, WAV, FLAC, and more',
    },
    {
      icon: FileVideo,
      title: 'Video Support',
      description: 'Embed in MP4, AVI, MOV, MKV files',
    },
    {
      icon: Shield,
      title: 'AES-256 Encryption',
      description: 'Military-grade security for your commands',
    },
    {
      icon: Zap,
      title: 'Ultrasonic FSK',
      description: 'Inaudible 18-22 kHz frequency range',
    },
  ]

  return (
    <div 
      className="p-6 space-y-6" 
      style={{
        padding: '1.5rem',
        display: 'flex',
        flexDirection: 'column',
        gap: '1.5rem',
        minHeight: '100vh',
        backgroundColor: '#f9fafb'
      }}
    >
      {/* Header */}
      <div style={{marginBottom: '1rem'}}>
        <h1 className="text-3xl font-bold" style={{fontSize: '1.875rem', fontWeight: 'bold', color: '#111827'}}>
          Welcome back, {user?.fullName || 'User'}
        </h1>
        <p className="text-muted-foreground mt-1" style={{marginTop: '0.25rem', color: '#6b7280'}}>
          Manage your steganographic operations from your dashboard
        </p>
      </div>

      {/* API Status */}
      <Card style={{backgroundColor: 'white', borderRadius: '0.5rem', boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)', border: '1px solid #e5e7eb'}}>
        <CardHeader className="pb-3" style={{padding: '1.5rem 1.5rem 0.75rem'}}>
          <div className="flex items-center justify-between" style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
            <CardTitle className="text-base font-medium" style={{fontSize: '1rem', fontWeight: '500'}}>System Status</CardTitle>
            <div className="flex items-center gap-2" style={{display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
              <Activity 
                className={cn("h-4 w-4", isHealthy ? "text-green-600" : "text-red-600")} 
                style={{height: '1rem', width: '1rem', color: isHealthy ? '#059669' : '#dc2626'}}
              />
              <span 
                className={cn("text-sm font-medium", isHealthy ? "text-green-600" : "text-red-600")}
                style={{fontSize: '0.875rem', fontWeight: '500', color: isHealthy ? '#059669' : '#dc2626'}}
              >
                {isHealthy ? 'Operational' : 'Degraded'}
              </span>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Operations</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalOperations}</div>
            <p className="text-xs text-muted-foreground">All time</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Embed Operations</CardTitle>
            <Upload className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.embedOperations}</div>
            <p className="text-xs text-muted-foreground">Commands embedded</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Decode Operations</CardTitle>
            <Download className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.decodeOperations}</div>
            <p className="text-xs text-muted-foreground">Commands decoded</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Success Rate</CardTitle>
            <BarChart3 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.successRate}%</div>
            <p className="text-xs text-muted-foreground">Operation success</p>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
        <div className="grid gap-4 md:grid-cols-3">
          {quickActions.map((action) => (
            <Link key={action.href} to={action.href}>
              <Card className="hover:shadow-lg transition-shadow cursor-pointer h-full">
                <CardHeader>
                  <div className={cn("w-12 h-12 rounded-lg flex items-center justify-center mb-4", action.bgColor)}>
                    <action.icon className={cn("h-6 w-6", action.color)} />
                  </div>
                  <CardTitle>{action.title}</CardTitle>
                  <CardDescription>{action.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <Button variant="outline" className="w-full">
                    Get Started
                  </Button>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      </div>

      {/* Features */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Key Features</h2>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {features.map((feature, index) => (
            <Card key={index}>
              <CardHeader>
                <feature.icon className="h-8 w-8 text-primary mb-2" />
                <CardTitle className="text-base">{feature.title}</CardTitle>
                <CardDescription className="text-sm">{feature.description}</CardDescription>
              </CardHeader>
            </Card>
          ))}
        </div>
      </div>
    </div>
  )
}


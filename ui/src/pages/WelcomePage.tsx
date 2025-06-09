import { RadioIcon, Upload, Download, BarChart3, Shield, Zap } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Link } from 'react-router-dom'

// Modern SaaS styling system
const styles = {
  container: {
    minHeight: '100vh',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    position: 'relative' as const,
    overflow: 'hidden',
  },
  backgroundPattern: {
    position: 'absolute' as const,
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    opacity: 0.1,
    backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='4'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
  },
  header: {
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    backdropFilter: 'blur(10px)',
    borderBottom: '1px solid rgba(255, 255, 255, 0.2)',
    position: 'sticky' as const,
    top: 0,
    zIndex: 50,
  },
  headerContainer: {
    maxWidth: '1280px',
    margin: '0 auto',
    padding: '0 2rem',
  },
  headerContent: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '1.5rem 0',
  },
  logo: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.75rem',
  },
  logoIcon: {
    width: '40px',
    height: '40px',
    color: '#667eea',
  },
  logoText: {
    fontSize: 'clamp(1.5rem, 3vw, 2rem)',
    fontWeight: '700',
    color: '#1e293b',
    margin: 0,
  },
  buttonGroup: {
    display: 'flex',
    gap: '1rem',
    alignItems: 'center',
  },
  primaryButton: {
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    border: 'none',
    borderRadius: '12px',
    padding: '0.75rem 2rem',
    fontSize: '1rem',
    fontWeight: '600',
    cursor: 'pointer',
    textDecoration: 'none',
    display: 'inline-flex',
    alignItems: 'center',
    transition: 'all 0.3s ease',
    boxShadow: '0 4px 15px rgba(102, 126, 234, 0.4)',
  },
  secondaryButton: {
    background: 'transparent',
    color: '#667eea',
    border: '2px solid #667eea',
    borderRadius: '12px',
    padding: '0.75rem 2rem',
    fontSize: '1rem',
    fontWeight: '600',
    cursor: 'pointer',
    textDecoration: 'none',
    display: 'inline-flex',
    alignItems: 'center',
    transition: 'all 0.3s ease',
  },
  hero: {
    maxWidth: '1280px',
    margin: '0 auto',
    padding: '0 2rem',
    paddingTop: '4rem',
    paddingBottom: '6rem',
    textAlign: 'center' as const,
    position: 'relative' as const,
    zIndex: 1,
  },
  heroTitle: {
    fontSize: 'clamp(3rem, 6vw, 5rem)',
    fontWeight: '800',
    color: 'white',
    margin: '0 0 1.5rem 0',
    lineHeight: '1.1',
    letterSpacing: '-0.02em',
  },
  heroSubtitle: {
    fontSize: 'clamp(1.25rem, 2.5vw, 1.5rem)',
    color: 'rgba(255, 255, 255, 0.9)',
    maxWidth: '800px',
    margin: '0 auto 3rem auto',
    lineHeight: '1.6',
  },
  heroButtons: {
    display: 'flex',
    gap: '1.5rem',
    justifyContent: 'center',
    alignItems: 'center',
    flexWrap: 'wrap' as const,
  },
  content: {
    backgroundColor: 'white',
    position: 'relative' as const,
    zIndex: 1,
  },
  section: {
    padding: '5rem 2rem',
    maxWidth: '1280px',
    margin: '0 auto',
  },
  sectionTitle: {
    fontSize: 'clamp(2rem, 4vw, 3rem)',
    fontWeight: '700',
    textAlign: 'center' as const,
    color: '#1e293b',
    margin: '0 0 3rem 0',
  },
  featuresGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
    gap: '2rem',
    marginBottom: '4rem',
  },
  featureCard: {
    backgroundColor: 'white',
    borderRadius: '20px',
    padding: '2rem',
    border: '1px solid #e2e8f0',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)',
    transition: 'all 0.3s ease',
    cursor: 'pointer',
  },
  featureIcon: {
    width: '60px',
    height: '60px',
    borderRadius: '16px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: '1.5rem',
  },
  featureTitle: {
    fontSize: '1.5rem',
    fontWeight: '600',
    color: '#1e293b',
    margin: '0 0 1rem 0',
  },
  featureDescription: {
    fontSize: '1rem',
    color: '#64748b',
    lineHeight: '1.6',
    margin: 0,
  },
  techSpecs: {
    backgroundColor: '#f8fafc',
    borderRadius: '20px',
    padding: '3rem',
    marginBottom: '4rem',
  },
  techSpecsTitle: {
    fontSize: '2rem',
    fontWeight: '700',
    textAlign: 'center' as const,
    color: '#1e293b',
    margin: '0 0 2rem 0',
  },
  specsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '2rem',
  },
  specItem: {
    textAlign: 'center' as const,
  },
  specValue: {
    fontSize: '2.5rem',
    fontWeight: '700',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text',
    margin: '0 0 0.5rem 0',
  },
  specLabel: {
    fontSize: '0.875rem',
    color: '#64748b',
    fontWeight: '500',
    margin: 0,
  },
  footer: {
    backgroundColor: '#1e293b',
    color: 'white',
    padding: '3rem 2rem',
    textAlign: 'center' as const,
  },
  footerContent: {
    maxWidth: '1280px',
    margin: '0 auto',
  },
  footerLogo: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '0.75rem',
    marginBottom: '1rem',
  },
  footerText: {
    color: '#94a3b8',
    fontSize: '1rem',
    margin: 0,
  },
}

export function WelcomePage() {
  const features = [
    {
      icon: Upload,
      title: 'Embed Commands',
      description: 'Hide encrypted commands in audio/video files using ultrasonic frequencies',
    },
    {
      icon: Download,
      title: 'Decode Messages', 
      description: 'Extract and decrypt hidden commands from multimedia files',
    },
    {
      icon: BarChart3,
      title: 'Analyze Content',
      description: 'Detect steganographic content and analyze signal quality',
    },
    {
      icon: Shield,
      title: 'AES-256 Encryption',
      description: 'Military-grade security with advanced encryption standards',
    },
    {
      icon: Zap,
      title: 'Ultrasonic FSK',
      description: 'Frequency Shift Keying in the 18-22 kHz inaudible range',
    },
  ]

  return (
    <div style={styles.container}>
      {/* Background Pattern */}
      <div style={styles.backgroundPattern} />
      
      {/* Header */}
      <header style={styles.header}>
        <div style={styles.headerContainer}>
          <div style={styles.headerContent}>
            <div style={styles.logo}>
              <RadioIcon style={styles.logoIcon} />
              <h1 style={styles.logoText}>Ultrasonic Agentics</h1>
            </div>
            <div style={styles.buttonGroup}>
              <Link to="/login" style={styles.primaryButton}>
                Sign In
              </Link>
              <Link to="/login" style={styles.secondaryButton}>
                Try Demo
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main style={styles.hero}>
        <h2 style={styles.heroTitle}>
          Covert Communication
        </h2>
        <p style={styles.heroSubtitle}>
          Advanced steganography system for embedding encrypted commands in multimedia files
          using ultrasonic frequencies and state-of-the-art signal processing techniques.
        </p>
        <div style={styles.heroButtons}>
          <Link to="/login" style={styles.primaryButton}>
            Start Embedding
          </Link>
          <Link to="/login" style={styles.secondaryButton}>
            Learn More
          </Link>
        </div>
      </main>

      {/* Content Section */}
      <div style={styles.content}>
        <section style={styles.section}>
          {/* Features Grid */}
          <h3 style={styles.sectionTitle}>
            Powerful Features
          </h3>
          <div style={styles.featuresGrid}>
            {features.map((feature, index) => (
              <div 
                key={index} 
                style={{
                  ...styles.featureCard,
                  ':hover': {
                    transform: 'translateY(-8px)',
                    boxShadow: '0 20px 25px rgba(0, 0, 0, 0.1)',
                  }
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateY(-8px)'
                  e.currentTarget.style.boxShadow = '0 20px 25px rgba(0, 0, 0, 0.1)'
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'translateY(0)'
                  e.currentTarget.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.05)'
                }}
              >
                <div 
                  style={{
                    ...styles.featureIcon,
                    background: index === 0 ? 'linear-gradient(135deg, #3b82f6, #1d4ed8)' :
                               index === 1 ? 'linear-gradient(135deg, #10b981, #047857)' :
                               index === 2 ? 'linear-gradient(135deg, #8b5cf6, #7c3aed)' :
                               index === 3 ? 'linear-gradient(135deg, #f59e0b, #d97706)' :
                               'linear-gradient(135deg, #ef4444, #dc2626)',
                  }}
                >
                  <feature.icon style={{ width: '28px', height: '28px', color: 'white' }} />
                </div>
                <h4 style={styles.featureTitle}>{feature.title}</h4>
                <p style={styles.featureDescription}>
                  {feature.description}
                </p>
              </div>
            ))}
          </div>

          {/* Technical Specs */}
          <div style={styles.techSpecs}>
            <h3 style={styles.techSpecsTitle}>
              Technical Specifications
            </h3>
            <div style={styles.specsGrid}>
              <div style={styles.specItem}>
                <div style={styles.specValue}>18-22kHz</div>
                <div style={styles.specLabel}>Frequency Range</div>
              </div>
              <div style={styles.specItem}>
                <div style={styles.specValue}>AES-256</div>
                <div style={styles.specLabel}>Encryption</div>
              </div>
              <div style={styles.specItem}>
                <div style={styles.specValue}>FSK</div>
                <div style={styles.specLabel}>Modulation</div>
              </div>
              <div style={styles.specItem}>
                <div style={styles.specValue}>98.5%</div>
                <div style={styles.specLabel}>Success Rate</div>
              </div>
            </div>
          </div>

          {/* Supported Formats */}
          <div style={{ textAlign: 'center' as const }}>
            <h3 style={styles.sectionTitle}>
              Supported Formats
            </h3>
            <div style={{
              display: 'flex',
              flexWrap: 'wrap',
              justifyContent: 'center',
              gap: '1rem',
              marginTop: '2rem',
            }}>
              {['MP3', 'WAV', 'FLAC', 'MP4', 'AVI', 'MOV', 'MKV'].map((format) => (
                <span
                  key={format}
                  style={{
                    padding: '0.75rem 1.5rem',
                    backgroundColor: '#f1f5f9',
                    borderRadius: '50px',
                    fontSize: '0.875rem',
                    fontWeight: '600',
                    color: '#475569',
                    border: '2px solid #e2e8f0',
                    transition: 'all 0.3s ease',
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.backgroundColor = '#667eea'
                    e.currentTarget.style.color = 'white'
                    e.currentTarget.style.borderColor = '#667eea'
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.backgroundColor = '#f1f5f9'
                    e.currentTarget.style.color = '#475569'
                    e.currentTarget.style.borderColor = '#e2e8f0'
                  }}
                >
                  {format}
                </span>
              ))}
            </div>
          </div>
        </section>
      </div>

      {/* Footer */}
      <footer style={styles.footer}>
        <div style={styles.footerContent}>
          <div style={styles.footerLogo}>
            <RadioIcon style={{ width: '32px', height: '32px', color: '#9ca3af' }} />
            <span style={{ fontSize: '1.25rem', fontWeight: '600', color: 'white' }}>
              Ultrasonic Agentics
            </span>
          </div>
          <p style={styles.footerText}>
            Advanced steganography for secure covert communication
          </p>
        </div>
      </footer>
    </div>
  )
}
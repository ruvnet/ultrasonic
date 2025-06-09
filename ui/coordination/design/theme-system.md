# Theme System Documentation

## Overview
The Ultrasonic-Agentics UI uses a comprehensive theming system built on Tailwind CSS with custom extensions for ultrasonic-specific design needs.

## Color System

### Brand Colors
The primary color palette is based on ultrasonic/audio wave imagery.

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        // Primary - Ultrasonic Blue
        ultrasonic: {
          50:  '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9', // Primary
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
          950: '#082f49'
        },
        
        // Signal Quality Indicators
        signal: {
          excellent: '#10b981', // Green
          good:      '#3b82f6', // Blue
          fair:      '#f59e0b', // Amber
          poor:      '#ef4444', // Red
          none:      '#6b7280'  // Gray
        },
        
        // Semantic Colors
        semantic: {
          success: '#10b981',
          warning: '#f59e0b',
          error:   '#ef4444',
          info:    '#3b82f6'
        },
        
        // Dark Mode Specific
        dark: {
          bg: {
            primary:   '#0f172a',
            secondary: '#1e293b',
            tertiary:  '#334155'
          },
          border: '#475569'
        }
      }
    }
  }
}
```

### Color Usage Guidelines

#### Primary Actions
```jsx
// Primary buttons and CTAs
<Button className="bg-ultrasonic-500 hover:bg-ultrasonic-600">
  Encode Message
</Button>

// Primary links
<a className="text-ultrasonic-600 hover:text-ultrasonic-700">
  Learn more
</a>
```

#### Signal Quality
```jsx
// Signal strength indicators
function SignalIndicator({ quality }) {
  const colors = {
    excellent: 'bg-signal-excellent',
    good: 'bg-signal-good',
    fair: 'bg-signal-fair',
    poor: 'bg-signal-poor'
  }
  
  return <div className={`h-4 w-4 rounded-full ${colors[quality]}`} />
}
```

## Typography System

### Font Stack
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Monaco', 'Consolas', 'monospace'],
        display: ['Lexend', 'Inter', 'sans-serif']
      }
    }
  }
}
```

### Typography Scale
```css
/* Base typography classes */
.text-display-lg { @apply text-5xl font-display font-bold tracking-tight; }
.text-display-md { @apply text-4xl font-display font-bold tracking-tight; }
.text-display-sm { @apply text-3xl font-display font-semibold tracking-tight; }

.text-heading-lg { @apply text-2xl font-semibold; }
.text-heading-md { @apply text-xl font-semibold; }
.text-heading-sm { @apply text-lg font-semibold; }

.text-body-lg { @apply text-base; }
.text-body-md { @apply text-sm; }
.text-body-sm { @apply text-xs; }

.text-label { @apply text-sm font-medium text-gray-700; }
.text-caption { @apply text-xs text-gray-500; }
.text-code { @apply font-mono text-sm; }
```

### Usage Examples
```jsx
// Page titles
<h1 className="text-display-lg text-gray-900 dark:text-white">
  Ultrasonic Encoder
</h1>

// Section headers
<h2 className="text-heading-lg text-gray-800 dark:text-gray-100">
  Audio Settings
</h2>

// Body text
<p className="text-body-lg text-gray-600 dark:text-gray-400">
  Configure encoding parameters for optimal signal quality.
</p>
```

## Spacing System

### Spacing Scale
Based on a 4px grid system for consistency.

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    spacing: {
      px: '1px',
      0: '0',
      0.5: '0.125rem', // 2px
      1: '0.25rem',    // 4px
      1.5: '0.375rem', // 6px
      2: '0.5rem',     // 8px
      2.5: '0.625rem', // 10px
      3: '0.75rem',    // 12px
      4: '1rem',       // 16px
      5: '1.25rem',    // 20px
      6: '1.5rem',     // 24px
      8: '2rem',       // 32px
      10: '2.5rem',    // 40px
      12: '3rem',      // 48px
      16: '4rem',      // 64px
      20: '5rem',      // 80px
      24: '6rem',      // 96px
    }
  }
}
```

### Spacing Patterns
```jsx
// Component spacing
<Card className="p-6 space-y-4">
  <CardHeader className="pb-4 border-b">
    <h3 className="text-heading-md">Settings</h3>
  </CardHeader>
  <CardBody className="space-y-3">
    {/* Content */}
  </CardBody>
</Card>

// Layout spacing
<div className="container mx-auto px-4 py-8 lg:px-6 lg:py-12">
  <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 lg:gap-8">
    {/* Grid items */}
  </div>
</div>
```

## Shadow System

### Shadow Scale
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      boxShadow: {
        'xs': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'sm': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1)',
        'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)',
        '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        'inner': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.05)',
        'ultrasonic': '0 10px 40px -10px rgba(14, 165, 233, 0.5)',
        'none': 'none'
      }
    }
  }
}
```

### Shadow Usage
```jsx
// Elevated components
<Card className="shadow-lg hover:shadow-xl transition-shadow">
  {/* Content */}
</Card>

// Floating elements
<Modal className="shadow-2xl">
  {/* Modal content */}
</Modal>

// Brand shadow for CTAs
<Button className="shadow-ultrasonic hover:shadow-lg">
  Start Encoding
</Button>
```

## Border Radius System

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      borderRadius: {
        'none': '0',
        'sm': '0.125rem',  // 2px
        'DEFAULT': '0.25rem', // 4px
        'md': '0.375rem',  // 6px
        'lg': '0.5rem',    // 8px
        'xl': '0.75rem',   // 12px
        '2xl': '1rem',     // 16px
        '3xl': '1.5rem',   // 24px
        'full': '9999px'
      }
    }
  }
}
```

## Animation System

### Transition Utilities
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      transitionTimingFunction: {
        'ultrasonic': 'cubic-bezier(0.4, 0.0, 0.2, 1)',
        'bounce-in': 'cubic-bezier(0.68, -0.55, 0.265, 1.55)'
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'ping-slow': 'ping 2s cubic-bezier(0, 0, 0.2, 1) infinite',
        'wave': 'wave 2s ease-in-out infinite',
        'shimmer': 'shimmer 2s ease-in-out infinite',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
        'fade-in': 'fadeIn 0.3s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out'
      },
      keyframes: {
        wave: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' }
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' }
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: 0 },
          '100%': { transform: 'translateY(0)', opacity: 1 }
        },
        slideDown: {
          '0%': { transform: 'translateY(-10px)', opacity: 0 },
          '100%': { transform: 'translateY(0)', opacity: 1 }
        },
        fadeIn: {
          '0%': { opacity: 0 },
          '100%': { opacity: 1 }
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: 0 },
          '100%': { transform: 'scale(1)', opacity: 1 }
        }
      }
    }
  }
}
```

### Animation Usage
```jsx
// Loading states
<div className="animate-pulse-slow">
  <Skeleton className="h-48 w-full" />
</div>

// Hover effects
<Button className="transition-all duration-200 hover:scale-105 active:scale-95">
  Click me
</Button>

// Entry animations
<Card className="animate-slide-up">
  {/* Content */}
</Card>

// Signal indicators
<div className="relative">
  <div className="animate-ping absolute inset-0 rounded-full bg-ultrasonic-400 opacity-75" />
  <div className="relative rounded-full bg-ultrasonic-500 h-3 w-3" />
</div>
```

## Dark Mode Implementation

### CSS Variables
```css
/* styles/globals.css */
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --card: 0 0% 100%;
  --card-foreground: 222.2 84% 4.9%;
  --popover: 0 0% 100%;
  --popover-foreground: 222.2 84% 4.9%;
  --primary: 199 89% 48%;
  --primary-foreground: 210 40% 98%;
  --secondary: 210 40% 96.1%;
  --secondary-foreground: 222.2 47.4% 11.2%;
  --muted: 210 40% 96.1%;
  --muted-foreground: 215.4 16.3% 46.9%;
  --accent: 210 40% 96.1%;
  --accent-foreground: 222.2 47.4% 11.2%;
  --destructive: 0 84.2% 60.2%;
  --destructive-foreground: 210 40% 98%;
  --border: 214.3 31.8% 91.4%;
  --input: 214.3 31.8% 91.4%;
  --ring: 199 89% 48%;
  --radius: 0.5rem;
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  --card: 222.2 84% 4.9%;
  --card-foreground: 210 40% 98%;
  --popover: 222.2 84% 4.9%;
  --popover-foreground: 210 40% 98%;
  --primary: 199 89% 48%;
  --primary-foreground: 222.2 47.4% 11.2%;
  --secondary: 217.2 32.6% 17.5%;
  --secondary-foreground: 210 40% 98%;
  --muted: 217.2 32.6% 17.5%;
  --muted-foreground: 215 20.2% 65.1%;
  --accent: 217.2 32.6% 17.5%;
  --accent-foreground: 210 40% 98%;
  --destructive: 0 62.8% 30.6%;
  --destructive-foreground: 210 40% 98%;
  --border: 217.2 32.6% 17.5%;
  --input: 217.2 32.6% 17.5%;
  --ring: 199 89% 48%;
}
```

### Dark Mode Toggle
```jsx
// components/ThemeToggle.tsx
function ThemeToggle() {
  const [theme, setTheme] = useState('system')
  
  useEffect(() => {
    const root = window.document.documentElement
    
    if (theme === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'dark'
        : 'light'
      root.classList.toggle('dark', systemTheme === 'dark')
    } else {
      root.classList.toggle('dark', theme === 'dark')
    }
  }, [theme])
  
  return (
    <Select value={theme} onValueChange={setTheme}>
      <SelectTrigger className="w-32">
        <SelectValue />
      </SelectTrigger>
      <SelectContent>
        <SelectItem value="light">Light</SelectItem>
        <SelectItem value="dark">Dark</SelectItem>
        <SelectItem value="system">System</SelectItem>
      </SelectContent>
    </Select>
  )
}
```

## Responsive Design

### Breakpoints
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    screens: {
      'xs': '475px',
      'sm': '640px',
      'md': '768px',
      'lg': '1024px',
      'xl': '1280px',
      '2xl': '1536px',
      '3xl': '1920px'
    }
  }
}
```

### Responsive Patterns
```jsx
// Mobile-first responsive design
<div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
  {/* Grid items */}
</div>

// Responsive typography
<h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-display">
  Ultrasonic Steganography
</h1>

// Responsive spacing
<div className="p-4 sm:p-6 lg:p-8">
  {/* Content */}
</div>

// Conditional visibility
<div className="hidden lg:block">
  {/* Desktop only */}
</div>
<div className="lg:hidden">
  {/* Mobile/tablet only */}
</div>
```

## Component Theming

### Theme Provider
```jsx
// contexts/ThemeContext.tsx
interface ThemeContextValue {
  theme: 'light' | 'dark' | 'system'
  setTheme: (theme: ThemeContextValue['theme']) => void
  resolvedTheme: 'light' | 'dark'
}

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState<ThemeContextValue['theme']>('system')
  const [resolvedTheme, setResolvedTheme] = useState<'light' | 'dark'>('light')
  
  useEffect(() => {
    // Theme resolution logic
  }, [theme])
  
  return (
    <ThemeContext.Provider value={{ theme, setTheme, resolvedTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}
```

### Themed Components
```jsx
// Example of theme-aware component
function ThemedCard({ children, ...props }) {
  return (
    <div
      className={cn(
        'rounded-lg border p-6',
        'bg-white dark:bg-gray-800',
        'border-gray-200 dark:border-gray-700',
        'text-gray-900 dark:text-gray-100'
      )}
      {...props}
    >
      {children}
    </div>
  )
}
```

## Accessibility Considerations

### Focus Styles
```css
/* Global focus styles */
.focus-visible:focus {
  @apply outline-none ring-2 ring-ultrasonic-500 ring-offset-2;
}

.dark .focus-visible:focus {
  @apply ring-offset-gray-900;
}
```

### High Contrast Mode
```css
@media (prefers-contrast: high) {
  :root {
    --primary: 0 100% 50%;
    --secondary: 0 0% 0%;
    --background: 0 0% 100%;
    --foreground: 0 0% 0%;
  }
}
```

### Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Custom Utilities

### Gradient Utilities
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'gradient-ultrasonic': 'linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%)',
        'gradient-signal': 'linear-gradient(to right, #ef4444 0%, #f59e0b 50%, #10b981 100%)'
      }
    }
  }
}
```

### Custom Classes
```css
/* Custom utility classes */
@layer utilities {
  .text-balance {
    text-wrap: balance;
  }
  
  .scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
  
  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }
  
  .glow-ultrasonic {
    box-shadow: 0 0 20px rgba(14, 165, 233, 0.5);
  }
  
  .text-gradient-ultrasonic {
    @apply bg-gradient-to-r from-ultrasonic-400 to-ultrasonic-600 bg-clip-text text-transparent;
  }
}
```

## Performance Considerations

### CSS Optimization
```javascript
// postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
    ...(process.env.NODE_ENV === 'production' ? {
      cssnano: {
        preset: ['default', {
          discardComments: {
            removeAll: true,
          },
        }],
      },
    } : {})
  },
}
```

### Purge Configuration
```javascript
// tailwind.config.js
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  safelist: [
    'bg-signal-excellent',
    'bg-signal-good',
    'bg-signal-fair',
    'bg-signal-poor',
    {
      pattern: /bg-ultrasonic-(50|100|200|300|400|500|600|700|800|900)/,
    },
  ],
}
```
# UI Patterns and Component Library

## Overview
This document defines reusable UI patterns and components for consistent user experience across the Ultrasonic-Agentics application.

## Core UI Components

### Button Variants
Consistent button styles for different actions and contexts.

```typescript
// components/ui/Button.tsx
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        primary: 'bg-ultrasonic-500 text-white hover:bg-ultrasonic-600 active:bg-ultrasonic-700',
        secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200 active:bg-gray-300',
        ghost: 'hover:bg-gray-100 hover:text-gray-900',
        danger: 'bg-red-500 text-white hover:bg-red-600 active:bg-red-700',
        success: 'bg-green-500 text-white hover:bg-green-600 active:bg-green-700'
      },
      size: {
        sm: 'h-8 px-3 text-xs',
        md: 'h-10 px-4 py-2',
        lg: 'h-12 px-6 text-base',
        icon: 'h-10 w-10'
      }
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md'
    }
  }
)

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>,
  VariantProps<typeof buttonVariants> {
  loading?: boolean
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
}

export function Button({
  className,
  variant,
  size,
  loading,
  leftIcon,
  rightIcon,
  children,
  disabled,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size }), className)}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? (
        <Spinner className="mr-2 h-4 w-4" />
      ) : leftIcon ? (
        <span className="mr-2">{leftIcon}</span>
      ) : null}
      {children}
      {rightIcon && <span className="ml-2">{rightIcon}</span>}
    </button>
  )
}
```

### Form Components

#### Input Field
```typescript
// components/ui/Input.tsx
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  hint?: string
  leftAddon?: React.ReactNode
  rightAddon?: React.ReactNode
}

export function Input({
  label,
  error,
  hint,
  leftAddon,
  rightAddon,
  className,
  ...props
}: InputProps) {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-gray-700 mb-1">
          {label}
          {props.required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}
      
      <div className="relative">
        {leftAddon && (
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            {leftAddon}
          </div>
        )}
        
        <input
          className={cn(
            'block w-full rounded-md border-gray-300 shadow-sm',
            'focus:border-ultrasonic-500 focus:ring-ultrasonic-500',
            'disabled:bg-gray-50 disabled:text-gray-500',
            error && 'border-red-300 focus:border-red-500 focus:ring-red-500',
            leftAddon && 'pl-10',
            rightAddon && 'pr-10',
            className
          )}
          aria-invalid={!!error}
          aria-describedby={error ? `${props.id}-error` : undefined}
          {...props}
        />
        
        {rightAddon && (
          <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
            {rightAddon}
          </div>
        )}
      </div>
      
      {error && (
        <p className="mt-1 text-sm text-red-600" id={`${props.id}-error`}>
          {error}
        </p>
      )}
      
      {hint && !error && (
        <p className="mt-1 text-sm text-gray-500">{hint}</p>
      )}
    </div>
  )
}
```

#### Select Component
```typescript
// components/ui/Select.tsx
interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string
  error?: string
  options: Array<{ value: string; label: string; disabled?: boolean }>
  placeholder?: string
}

export function Select({
  label,
  error,
  options,
  placeholder = 'Select an option',
  className,
  ...props
}: SelectProps) {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-gray-700 mb-1">
          {label}
        </label>
      )}
      
      <select
        className={cn(
          'block w-full rounded-md border-gray-300 shadow-sm',
          'focus:border-ultrasonic-500 focus:ring-ultrasonic-500',
          error && 'border-red-300',
          className
        )}
        {...props}
      >
        <option value="" disabled>
          {placeholder}
        </option>
        {options.map(option => (
          <option
            key={option.value}
            value={option.value}
            disabled={option.disabled}
          >
            {option.label}
          </option>
        ))}
      </select>
      
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
    </div>
  )
}
```

### Card Components

#### Basic Card
```typescript
// components/ui/Card.tsx
interface CardProps {
  children: React.ReactNode
  className?: string
  variant?: 'default' | 'bordered' | 'elevated'
  padding?: 'none' | 'sm' | 'md' | 'lg'
}

export function Card({
  children,
  className,
  variant = 'default',
  padding = 'md'
}: CardProps) {
  return (
    <div
      className={cn(
        'bg-white rounded-lg',
        variant === 'bordered' && 'border border-gray-200',
        variant === 'elevated' && 'shadow-lg',
        padding === 'sm' && 'p-4',
        padding === 'md' && 'p-6',
        padding === 'lg' && 'p-8',
        className
      )}
    >
      {children}
    </div>
  )
}

Card.Header = function CardHeader({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={cn('border-b border-gray-200 pb-4 mb-4', className)}>
      {children}
    </div>
  )
}

Card.Body = function CardBody({ children, className }: { children: React.ReactNode; className?: string }) {
  return <div className={className}>{children}</div>
}

Card.Footer = function CardFooter({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={cn('border-t border-gray-200 pt-4 mt-4', className)}>
      {children}
    </div>
  )
}
```

### Modal System

```typescript
// components/ui/Modal.tsx
interface ModalProps {
  isOpen: boolean
  onClose: () => void
  title?: string
  size?: 'sm' | 'md' | 'lg' | 'xl'
  children: React.ReactNode
  closeOnOverlayClick?: boolean
}

export function Modal({
  isOpen,
  onClose,
  title,
  size = 'md',
  children,
  closeOnOverlayClick = true
}: ModalProps) {
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }
    
    if (isOpen) {
      document.addEventListener('keydown', handleEscape)
      document.body.style.overflow = 'hidden'
    }
    
    return () => {
      document.removeEventListener('keydown', handleEscape)
      document.body.style.overflow = ''
    }
  }, [isOpen, onClose])
  
  if (!isOpen) return null
  
  const sizeClasses = {
    sm: 'max-w-md',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl'
  }
  
  return createPortal(
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex min-h-screen items-center justify-center p-4">
        <div
          className="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
          onClick={closeOnOverlayClick ? onClose : undefined}
        />
        
        <div
          className={cn(
            'relative bg-white rounded-lg shadow-xl',
            'transform transition-all',
            sizeClasses[size],
            'w-full'
          )}
        >
          {title && (
            <div className="border-b border-gray-200 px-6 py-4">
              <h3 className="text-lg font-semibold">{title}</h3>
              <button
                onClick={onClose}
                className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
          )}
          
          <div className="px-6 py-4">{children}</div>
        </div>
      </div>
    </div>,
    document.body
  )
}
```

### Loading States

#### Skeleton Loader
```typescript
// components/ui/Skeleton.tsx
interface SkeletonProps {
  className?: string
  variant?: 'text' | 'rect' | 'circle'
  animation?: 'pulse' | 'wave' | 'none'
}

export function Skeleton({
  className,
  variant = 'rect',
  animation = 'pulse'
}: SkeletonProps) {
  return (
    <div
      className={cn(
        'bg-gray-200',
        variant === 'text' && 'h-4 rounded',
        variant === 'rect' && 'rounded',
        variant === 'circle' && 'rounded-full',
        animation === 'pulse' && 'animate-pulse',
        animation === 'wave' && 'animate-shimmer',
        className
      )}
    />
  )
}

// Usage for loading states
export function AudioPlayerSkeleton() {
  return (
    <div className="space-y-4">
      <Skeleton className="h-48 w-full" /> {/* Waveform */}
      <div className="flex items-center space-x-4">
        <Skeleton variant="circle" className="h-10 w-10" /> {/* Play button */}
        <Skeleton className="h-4 flex-1" /> {/* Progress bar */}
        <Skeleton className="h-4 w-16" /> {/* Time */}
      </div>
    </div>
  )
}
```

### Toast Notifications

```typescript
// components/ui/Toast.tsx
interface ToastProps {
  id: string
  type: 'info' | 'success' | 'warning' | 'error'
  title: string
  message?: string
  duration?: number
  onDismiss: (id: string) => void
}

export function Toast({
  id,
  type,
  title,
  message,
  duration = 5000,
  onDismiss
}: ToastProps) {
  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(() => onDismiss(id), duration)
      return () => clearTimeout(timer)
    }
  }, [duration, id, onDismiss])
  
  const icons = {
    info: <Info className="h-5 w-5" />,
    success: <CheckCircle className="h-5 w-5" />,
    warning: <AlertCircle className="h-5 w-5" />,
    error: <XCircle className="h-5 w-5" />
  }
  
  const colors = {
    info: 'bg-blue-50 text-blue-800 border-blue-200',
    success: 'bg-green-50 text-green-800 border-green-200',
    warning: 'bg-yellow-50 text-yellow-800 border-yellow-200',
    error: 'bg-red-50 text-red-800 border-red-200'
  }
  
  return (
    <div
      className={cn(
        'flex items-start p-4 rounded-lg border',
        colors[type],
        'shadow-lg transition-all'
      )}
    >
      <div className="flex-shrink-0">{icons[type]}</div>
      <div className="ml-3 flex-1">
        <p className="font-medium">{title}</p>
        {message && <p className="mt-1 text-sm opacity-90">{message}</p>}
      </div>
      <button
        onClick={() => onDismiss(id)}
        className="ml-4 flex-shrink-0 text-current opacity-70 hover:opacity-100"
      >
        <X className="h-4 w-4" />
      </button>
    </div>
  )
}
```

### Data Display

#### Table Component
```typescript
// components/ui/Table.tsx
interface TableProps<T> {
  data: T[]
  columns: Column<T>[]
  onRowClick?: (row: T) => void
  className?: string
}

interface Column<T> {
  key: keyof T | string
  label: string
  render?: (value: any, row: T) => React.ReactNode
  sortable?: boolean
  width?: string
}

export function Table<T extends Record<string, any>>({
  data,
  columns,
  onRowClick,
  className
}: TableProps<T>) {
  return (
    <div className={cn('overflow-x-auto', className)}>
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            {columns.map(column => (
              <th
                key={column.key}
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                style={{ width: column.width }}
              >
                {column.label}
                {column.sortable && (
                  <button className="ml-2 text-gray-400 hover:text-gray-600">
                    <ArrowUpDown className="h-3 w-3" />
                  </button>
                )}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {data.map((row, index) => (
            <tr
              key={index}
              onClick={() => onRowClick?.(row)}
              className={cn(
                onRowClick && 'cursor-pointer hover:bg-gray-50'
              )}
            >
              {columns.map(column => (
                <td
                  key={column.key}
                  className="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                >
                  {column.render
                    ? column.render(row[column.key], row)
                    : row[column.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
```

### Progress Indicators

#### Progress Bar
```typescript
// components/ui/Progress.tsx
interface ProgressProps {
  value: number
  max?: number
  label?: string
  showValue?: boolean
  variant?: 'default' | 'success' | 'warning' | 'error'
  size?: 'sm' | 'md' | 'lg'
}

export function Progress({
  value,
  max = 100,
  label,
  showValue = false,
  variant = 'default',
  size = 'md'
}: ProgressProps) {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100)
  
  const colors = {
    default: 'bg-ultrasonic-500',
    success: 'bg-green-500',
    warning: 'bg-yellow-500',
    error: 'bg-red-500'
  }
  
  const sizes = {
    sm: 'h-2',
    md: 'h-4',
    lg: 'h-6'
  }
  
  return (
    <div className="w-full">
      {(label || showValue) && (
        <div className="flex justify-between mb-1">
          {label && <span className="text-sm text-gray-700">{label}</span>}
          {showValue && (
            <span className="text-sm text-gray-500">{percentage.toFixed(0)}%</span>
          )}
        </div>
      )}
      
      <div className={cn('bg-gray-200 rounded-full overflow-hidden', sizes[size])}>
        <div
          className={cn(
            'h-full transition-all duration-300 ease-out',
            colors[variant]
          )}
          style={{ width: `${percentage}%` }}
          role="progressbar"
          aria-valuenow={value}
          aria-valuemin={0}
          aria-valuemax={max}
        />
      </div>
    </div>
  )
}
```

### Empty States

```typescript
// components/ui/EmptyState.tsx
interface EmptyStateProps {
  icon?: React.ReactNode
  title: string
  description?: string
  action?: {
    label: string
    onClick: () => void
  }
}

export function EmptyState({
  icon,
  title,
  description,
  action
}: EmptyStateProps) {
  return (
    <div className="text-center py-12">
      {icon && (
        <div className="mx-auto h-12 w-12 text-gray-400 mb-4">
          {icon}
        </div>
      )}
      
      <h3 className="text-lg font-medium text-gray-900 mb-2">{title}</h3>
      
      {description && (
        <p className="text-sm text-gray-500 mb-6 max-w-md mx-auto">
          {description}
        </p>
      )}
      
      {action && (
        <Button onClick={action.onClick} variant="primary">
          {action.label}
        </Button>
      )}
    </div>
  )
}
```

## Animation Patterns

### Transition Components
```typescript
// components/ui/Transition.tsx
interface TransitionProps {
  show: boolean
  children: React.ReactNode
  enter?: string
  enterFrom?: string
  enterTo?: string
  leave?: string
  leaveFrom?: string
  leaveTo?: string
}

export function Transition({
  show,
  children,
  enter = 'transition-all duration-300',
  enterFrom = 'opacity-0 scale-95',
  enterTo = 'opacity-100 scale-100',
  leave = 'transition-all duration-200',
  leaveFrom = 'opacity-100 scale-100',
  leaveTo = 'opacity-0 scale-95'
}: TransitionProps) {
  // Implementation using React Transition Group or similar
}
```

## Accessibility Patterns

### Focus Management
```typescript
// hooks/useFocusTrap.ts
export function useFocusTrap(ref: React.RefObject<HTMLElement>) {
  useEffect(() => {
    const element = ref.current
    if (!element) return
    
    const focusableElements = element.querySelectorAll(
      'a[href], button, textarea, input[type="text"], input[type="radio"], input[type="checkbox"], select'
    )
    
    const firstFocusable = focusableElements[0] as HTMLElement
    const lastFocusable = focusableElements[focusableElements.length - 1] as HTMLElement
    
    const handleTabKey = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return
      
      if (e.shiftKey) {
        if (document.activeElement === firstFocusable) {
          lastFocusable.focus()
          e.preventDefault()
        }
      } else {
        if (document.activeElement === lastFocusable) {
          firstFocusable.focus()
          e.preventDefault()
        }
      }
    }
    
    element.addEventListener('keydown', handleTabKey)
    firstFocusable?.focus()
    
    return () => {
      element.removeEventListener('keydown', handleTabKey)
    }
  }, [ref])
}
```

## Responsive Patterns

### Responsive Grid
```typescript
// components/ui/Grid.tsx
interface GridProps {
  children: React.ReactNode
  cols?: {
    default?: number
    sm?: number
    md?: number
    lg?: number
    xl?: number
  }
  gap?: number
  className?: string
}

export function Grid({
  children,
  cols = { default: 1, md: 2, lg: 3 },
  gap = 4,
  className
}: GridProps) {
  const gridCols = cn(
    'grid',
    cols.default && `grid-cols-${cols.default}`,
    cols.sm && `sm:grid-cols-${cols.sm}`,
    cols.md && `md:grid-cols-${cols.md}`,
    cols.lg && `lg:grid-cols-${cols.lg}`,
    cols.xl && `xl:grid-cols-${cols.xl}`,
    `gap-${gap}`,
    className
  )
  
  return <div className={gridCols}>{children}</div>
}
```

## Theme Variables

```css
/* styles/theme.css */
:root {
  /* Colors */
  --color-ultrasonic-50: #f0f9ff;
  --color-ultrasonic-500: #0ea5e9;
  --color-ultrasonic-900: #0c4a6e;
  
  /* Spacing */
  --spacing-unit: 0.25rem;
  
  /* Breakpoints */
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  
  /* Animations */
  --animation-duration: 200ms;
  --animation-timing: cubic-bezier(0.4, 0, 0.2, 1);
}
```
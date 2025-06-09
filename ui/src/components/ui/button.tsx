import * as React from "react"

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link'
  size?: 'default' | 'sm' | 'lg' | 'icon'
}

const getButtonStyles = (variant: string = 'default', size: string = 'default'): React.CSSProperties => {
  const baseStyles: React.CSSProperties = {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '8px',
    whiteSpace: 'nowrap',
    fontSize: '14px',
    fontWeight: '500',
    border: 'none',
    cursor: 'pointer',
    transition: 'all 0.2s ease',
    fontFamily: 'inherit',
  }

  const sizeVariants = {
    default: { height: '40px', padding: '0 16px', borderRadius: '6px' },
    sm: { height: '36px', padding: '0 12px', borderRadius: '6px' },
    lg: { height: '44px', padding: '0 32px', borderRadius: '6px' },
    icon: { height: '40px', width: '40px', padding: '0', borderRadius: '6px' },
  }
  const sizeStyles: React.CSSProperties = sizeVariants[size] || sizeVariants.default

  const variantVariants = {
    default: { 
      backgroundColor: '#1e293b', 
      color: 'white',
    },
    destructive: { 
      backgroundColor: '#ef4444', 
      color: 'white',
    },
    outline: { 
      backgroundColor: 'transparent', 
      color: '#1e293b', 
      border: '1px solid #e2e8f0',
    },
    secondary: { 
      backgroundColor: '#f1f5f9', 
      color: '#1e293b',
    },
    ghost: { 
      backgroundColor: 'transparent', 
      color: '#1e293b',
    },
    link: { 
      backgroundColor: 'transparent', 
      color: '#1e293b', 
      textDecoration: 'underline',
      textUnderlineOffset: '4px',
    },
  }
  const variantStyles: React.CSSProperties = variantVariants[variant] || variantVariants.default

  return { ...baseStyles, ...sizeStyles, ...variantStyles }
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'default', size = 'default', style, ...props }, ref) => {
    return (
      <button
        ref={ref}
        style={{
          ...getButtonStyles(variant, size),
          ...style
        }}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button }
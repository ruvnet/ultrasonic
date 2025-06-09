/**
 * Inline Styled Button Component
 * Demonstrates proper usage of the inline styling system with state management and accessibility
 */

import React, { useState, useCallback, forwardRef } from 'react'
import {
  primaryButtonStyles,
  secondaryButtonStyles,
  variantButtonStyles,
  ghostButtonStyles,
  linkButtonStyles,
  loadingSpinnerStyles,
  styleUtils,
  type ButtonSize,
  type ButtonVariant,
  keyframes
} from '@/lib/inline-styles'

// Inject keyframes into document head if not already present
if (typeof document !== 'undefined' && !document.querySelector('#inline-styles-keyframes')) {
  const style = document.createElement('style')
  style.id = 'inline-styles-keyframes'
  style.textContent = keyframes
  document.head.appendChild(style)
}

export interface InlineStyledButtonProps extends Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, 'style'> {
  variant?: ButtonVariant
  size?: ButtonSize
  loading?: boolean
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
  fullWidth?: boolean
  customStyle?: React.CSSProperties
}

export const InlineStyledButton = forwardRef<HTMLButtonElement, InlineStyledButtonProps>(
  ({
    variant = 'primary',
    size = 'md',
    loading = false,
    disabled = false,
    leftIcon,
    rightIcon,
    fullWidth = false,
    customStyle = {},
    children,
    onMouseEnter,
    onMouseLeave,
    onFocus,
    onBlur,
    onMouseDown,
    onMouseUp,
    ...props
  }, ref) => {
    const [isHovered, setIsHovered] = useState(false)
    const [isFocused, setIsFocused] = useState(false)
    const [isActive, setIsActive] = useState(false)

    // Determine if button should be disabled
    const isDisabled = disabled || loading

    // Get the appropriate style variant
    const getStyleVariant = useCallback(() => {
      switch (variant) {
        case 'primary':
          return primaryButtonStyles
        case 'secondary':
          return secondaryButtonStyles
        case 'success':
          return variantButtonStyles.success
        case 'warning':
          return variantButtonStyles.warning
        case 'danger':
          return variantButtonStyles.danger
        case 'ghost':
          return ghostButtonStyles
        case 'link':
          return linkButtonStyles
        default:
          return primaryButtonStyles
      }
    }, [variant])

    // Build the complete style object
    const buildStyles = useCallback(() => {
      const styleVariant = getStyleVariant()
      let baseStyle = styleVariant.base(size)
      
      // Apply full width if specified
      if (fullWidth) {
        baseStyle = { ...baseStyle, width: '100%' }
      }

      // Apply state-based styles
      if (isDisabled && styleVariant.disabled) {
        baseStyle = styleUtils.combine(baseStyle, styleVariant.disabled())
      } else {
        if (isActive && styleVariant.active) {
          baseStyle = styleUtils.combine(baseStyle, styleVariant.active())
        } else if (isHovered && styleVariant.hover) {
          baseStyle = styleUtils.combine(baseStyle, styleVariant.hover())
        }
        
        if (isFocused && styleVariant.focus) {
          baseStyle = styleUtils.combine(baseStyle, styleVariant.focus())
        }
      }

      // Apply loading styles
      if (loading && styleVariant.loading) {
        baseStyle = styleUtils.combine(baseStyle, styleVariant.loading())
      }

      // Apply custom styles last
      return styleUtils.combine(baseStyle, customStyle)
    }, [variant, size, isHovered, isFocused, isActive, isDisabled, loading, fullWidth, customStyle, getStyleVariant])

    // Event handlers
    const handleMouseEnter = useCallback((event: React.MouseEvent<HTMLButtonElement>) => {
      if (!isDisabled) {
        setIsHovered(true)
      }
      onMouseEnter?.(event)
    }, [isDisabled, onMouseEnter])

    const handleMouseLeave = useCallback((event: React.MouseEvent<HTMLButtonElement>) => {
      setIsHovered(false)
      setIsActive(false)
      onMouseLeave?.(event)
    }, [onMouseLeave])

    const handleFocus = useCallback((event: React.FocusEvent<HTMLButtonElement>) => {
      if (!isDisabled) {
        setIsFocused(true)
      }
      onFocus?.(event)
    }, [isDisabled, onFocus])

    const handleBlur = useCallback((event: React.FocusEvent<HTMLButtonElement>) => {
      setIsFocused(false)
      setIsActive(false)
      onBlur?.(event)
    }, [onBlur])

    const handleMouseDown = useCallback((event: React.MouseEvent<HTMLButtonElement>) => {
      if (!isDisabled) {
        setIsActive(true)
      }
      onMouseDown?.(event)
    }, [isDisabled, onMouseDown])

    const handleMouseUp = useCallback((event: React.MouseEvent<HTMLButtonElement>) => {
      setIsActive(false)
      onMouseUp?.(event)
    }, [onMouseUp])

    // Render loading spinner
    const renderLoadingSpinner = () => (
      <div style={loadingSpinnerStyles} />
    )

    return (
      <button
        ref={ref}
        disabled={isDisabled}
        style={buildStyles()}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        onFocus={handleFocus}
        onBlur={handleBlur}
        onMouseDown={handleMouseDown}
        onMouseUp={handleMouseUp}
        aria-disabled={isDisabled}
        aria-busy={loading}
        {...props}
      >
        {loading && renderLoadingSpinner()}
        {leftIcon && !loading && (
          <span style={{ display: 'flex', alignItems: 'center' }}>
            {leftIcon}
          </span>
        )}
        <span style={{ 
          opacity: loading ? 0 : 1,
          display: 'flex',
          alignItems: 'center',
          gap: '8px'
        }}>
          {children}
        </span>
        {rightIcon && !loading && (
          <span style={{ display: 'flex', alignItems: 'center' }}>
            {rightIcon}
          </span>
        )}
      </button>
    )
  }
)

InlineStyledButton.displayName = 'InlineStyledButton'

// Higher-order component for creating themed buttons
export const createThemedButton = (
  defaultVariant: ButtonVariant,
  defaultSize: ButtonSize,
  defaultCustomStyle: React.CSSProperties = {}
) => {
  return forwardRef<HTMLButtonElement, Partial<InlineStyledButtonProps>>(
    ({ variant = defaultVariant, size = defaultSize, customStyle = {}, ...props }, ref) => (
      <InlineStyledButton
        ref={ref}
        variant={variant}
        size={size}
        customStyle={styleUtils.combine(defaultCustomStyle, customStyle)}
        {...props}
      />
    )
  )
}

// Pre-configured button variants
export const PrimaryButton = createThemedButton('primary', 'md')
export const SecondaryButton = createThemedButton('secondary', 'md')
export const SuccessButton = createThemedButton('success', 'md')
export const WarningButton = createThemedButton('warning', 'md')
export const DangerButton = createThemedButton('danger', 'md')
export const GhostButton = createThemedButton('ghost', 'md')
export const LinkButton = createThemedButton('link', 'md')

// Specialized button variants
export const SmallPrimaryButton = createThemedButton('primary', 'sm')
export const LargePrimaryButton = createThemedButton('primary', 'lg')
export const IconButton = createThemedButton('ghost', 'icon')

// Button group component for consistent spacing
export interface ButtonGroupProps {
  children: React.ReactNode
  spacing?: 'sm' | 'md' | 'lg'
  orientation?: 'horizontal' | 'vertical'
  style?: React.CSSProperties
}

export const ButtonGroup: React.FC<ButtonGroupProps> = ({
  children,
  spacing = 'md',
  orientation = 'horizontal',
  style = {}
}) => {
  const spacingMap = {
    sm: '8px',
    md: '12px',
    lg: '16px'
  }

  const groupStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: orientation === 'vertical' ? 'column' : 'row',
    gap: spacingMap[spacing],
    alignItems: orientation === 'vertical' ? 'stretch' : 'center',
    ...style
  }

  return (
    <div style={groupStyle}>
      {children}
    </div>
  )
}

// Input field component using inline styles
export interface InlineStyledInputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'style'> {
  error?: boolean
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
  customStyle?: React.CSSProperties
}

export const InlineStyledInput = forwardRef<HTMLInputElement, InlineStyledInputProps>(
  ({
    error = false,
    disabled = false,
    leftIcon,
    rightIcon,
    customStyle = {},
    onFocus,
    onBlur,
    onMouseEnter,
    onMouseLeave,
    ...props
  }, ref) => {
    const [isHovered, setIsHovered] = useState(false)
    const [isFocused, setIsFocused] = useState(false)

    const buildInputStyles = useCallback(() => {
      const { inputFieldStyles } = require('@/lib/inline-styles')
      let baseStyle = inputFieldStyles.base()

      if (disabled) {
        baseStyle = styleUtils.combine(baseStyle, inputFieldStyles.disabled())
      } else {
        if (error) {
          baseStyle = styleUtils.combine(baseStyle, inputFieldStyles.error())
        } else if (isFocused) {
          baseStyle = styleUtils.combine(baseStyle, inputFieldStyles.focus())
        } else if (isHovered) {
          baseStyle = styleUtils.combine(baseStyle, inputFieldStyles.hover())
        }
      }

      // Adjust padding if icons are present
      if (leftIcon) {
        baseStyle = { ...baseStyle, paddingLeft: '40px' }
      }
      if (rightIcon) {
        baseStyle = { ...baseStyle, paddingRight: '40px' }
      }

      return styleUtils.combine(baseStyle, customStyle)
    }, [isHovered, isFocused, error, disabled, leftIcon, rightIcon, customStyle])

    const containerStyle: React.CSSProperties = {
      position: 'relative',
      display: 'inline-block',
      width: '100%'
    }

    const iconStyle = (isLeft: boolean): React.CSSProperties => ({
      position: 'absolute',
      top: '50%',
      transform: 'translateY(-50%)',
      [isLeft ? 'left' : 'right']: '12px',
      display: 'flex',
      alignItems: 'center',
      pointerEvents: 'none',
      color: error ? '#ef4444' : (isFocused ? '#3b82f6' : '#6b7280'),
    })

    return (
      <div style={containerStyle}>
        {leftIcon && (
          <div style={iconStyle(true)}>
            {leftIcon}
          </div>
        )}
        <input
          ref={ref}
          disabled={disabled}
          style={buildInputStyles()}
          onFocus={(e) => {
            setIsFocused(true)
            onFocus?.(e)
          }}
          onBlur={(e) => {
            setIsFocused(false)
            onBlur?.(e)
          }}
          onMouseEnter={(e) => {
            if (!disabled) setIsHovered(true)
            onMouseEnter?.(e)
          }}
          onMouseLeave={(e) => {
            setIsHovered(false)
            onMouseLeave?.(e)
          }}
          {...props}
        />
        {rightIcon && (
          <div style={iconStyle(false)}>
            {rightIcon}
          </div>
        )}
      </div>
    )
  }
)

InlineStyledInput.displayName = 'InlineStyledInput'
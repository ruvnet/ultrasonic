/**
 * Custom hook for managing button interactive states
 * Provides centralized state management for hover, focus, active, and loading states
 */

import { useState, useCallback, useRef, useEffect } from 'react'
import { 
  styleUtils,
  type ButtonVariant,
  type ButtonSize,
  type InteractiveState
} from '@/lib/inline-styles'

export interface UseButtonStateOptions {
  variant?: ButtonVariant
  size?: ButtonSize
  disabled?: boolean
  loading?: boolean
  autoLoadingTimeout?: number // Auto-disable loading after X milliseconds
  onStateChange?: (state: InteractiveState) => void
}

export interface UseButtonStateReturn {
  // State values
  isHovered: boolean
  isFocused: boolean
  isActive: boolean
  isLoading: boolean
  isDisabled: boolean
  currentState: InteractiveState
  
  // Event handlers
  handleMouseEnter: (event: React.MouseEvent) => void
  handleMouseLeave: (event: React.MouseEvent) => void
  handleMouseDown: (event: React.MouseEvent) => void
  handleMouseUp: (event: React.MouseEvent) => void
  handleFocus: (event: React.FocusEvent) => void
  handleBlur: (event: React.FocusEvent) => void
  handleKeyDown: (event: React.KeyboardEvent) => void
  handleKeyUp: (event: React.KeyboardEvent) => void
  
  // Actions
  setLoading: (loading: boolean) => void
  resetState: () => void
  
  // Style helpers
  getButtonStyles: () => React.CSSProperties
  getStateClasses: () => string[]
}

export const useButtonState = (options: UseButtonStateOptions = {}): UseButtonStateReturn => {
  const {
    variant = 'primary',
    size = 'md',
    disabled = false,
    loading = false,
    autoLoadingTimeout,
    onStateChange
  } = options

  // Internal state
  const [isHovered, setIsHovered] = useState(false)
  const [isFocused, setIsFocused] = useState(false)
  const [isActive, setIsActive] = useState(false)
  const [isLoading, setIsLoading] = useState(loading)
  
  // Refs for cleanup
  const loadingTimeoutRef = useRef<NodeJS.Timeout>()
  const stateChangeTimeoutRef = useRef<NodeJS.Timeout>()

  // Computed values
  const isDisabled = disabled || isLoading
  
  // Determine current state
  const getCurrentState = useCallback((): InteractiveState => {
    if (isDisabled) return 'disabled'
    if (isLoading) return 'loading'
    if (isActive) return 'active'
    if (isFocused) return 'focus'
    if (isHovered) return 'hover'
    return 'base'
  }, [isDisabled, isLoading, isActive, isFocused, isHovered])

  const currentState = getCurrentState()

  // Notify state changes
  useEffect(() => {
    if (onStateChange) {
      // Debounce state changes to avoid excessive calls
      if (stateChangeTimeoutRef.current) {
        clearTimeout(stateChangeTimeoutRef.current)
      }
      
      stateChangeTimeoutRef.current = setTimeout(() => {
        onStateChange(currentState)
      }, 16) // ~1 frame at 60fps
    }
  }, [currentState, onStateChange])

  // Auto-disable loading
  useEffect(() => {
    if (isLoading && autoLoadingTimeout) {
      loadingTimeoutRef.current = setTimeout(() => {
        setIsLoading(false)
      }, autoLoadingTimeout)
    }
    
    return () => {
      if (loadingTimeoutRef.current) {
        clearTimeout(loadingTimeoutRef.current)
      }
    }
  }, [isLoading, autoLoadingTimeout])

  // Sync external loading state
  useEffect(() => {
    setIsLoading(loading)
  }, [loading])

  // Event handlers
  const handleMouseEnter = useCallback((event: React.MouseEvent) => {
    if (!isDisabled) {
      setIsHovered(true)
    }
  }, [isDisabled])

  const handleMouseLeave = useCallback((event: React.MouseEvent) => {
    setIsHovered(false)
    setIsActive(false)
  }, [])

  const handleMouseDown = useCallback((event: React.MouseEvent) => {
    if (!isDisabled) {
      setIsActive(true)
    }
  }, [isDisabled])

  const handleMouseUp = useCallback((event: React.MouseEvent) => {
    setIsActive(false)
  }, [])

  const handleFocus = useCallback((event: React.FocusEvent) => {
    if (!isDisabled) {
      setIsFocused(true)
    }
  }, [isDisabled])

  const handleBlur = useCallback((event: React.FocusEvent) => {
    setIsFocused(false)
    setIsActive(false)
  }, [])

  const handleKeyDown = useCallback((event: React.KeyboardEvent) => {
    if (!isDisabled && (event.key === ' ' || event.key === 'Enter')) {
      setIsActive(true)
    }
  }, [isDisabled])

  const handleKeyUp = useCallback((event: React.KeyboardEvent) => {
    if (event.key === ' ' || event.key === 'Enter') {
      setIsActive(false)
    }
  }, [])

  // Actions
  const setLoadingState = useCallback((loading: boolean) => {
    setIsLoading(loading)
    
    if (loading && autoLoadingTimeout) {
      loadingTimeoutRef.current = setTimeout(() => {
        setIsLoading(false)
      }, autoLoadingTimeout)
    }
  }, [autoLoadingTimeout])

  const resetState = useCallback(() => {
    setIsHovered(false)
    setIsFocused(false)
    setIsActive(false)
    setIsLoading(false)
    
    // Clear timeouts
    if (loadingTimeoutRef.current) {
      clearTimeout(loadingTimeoutRef.current)
    }
    if (stateChangeTimeoutRef.current) {
      clearTimeout(stateChangeTimeoutRef.current)
    }
  }, [])

  // Style helpers
  const getButtonStyles = useCallback((): React.CSSProperties => {
    // Import styles dynamically to avoid circular dependencies
    const {
      primaryButtonStyles,
      secondaryButtonStyles,
      variantButtonStyles,
      ghostButtonStyles,
      linkButtonStyles
    } = require('@/lib/inline-styles')

    const getStyleVariant = () => {
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
    }

    const styleVariant = getStyleVariant()
    let baseStyle = styleVariant.base(size)

    // Apply state-based styles in order of precedence
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

    if (isLoading && styleVariant.loading) {
      baseStyle = styleUtils.combine(baseStyle, styleVariant.loading())
    }

    return baseStyle
  }, [variant, size, isHovered, isFocused, isActive, isDisabled, isLoading])

  const getStateClasses = useCallback((): string[] => {
    const classes: string[] = [`variant-${variant}`, `size-${size}`]
    
    if (isHovered) classes.push('hovered')
    if (isFocused) classes.push('focused')
    if (isActive) classes.push('active')
    if (isDisabled) classes.push('disabled')
    if (isLoading) classes.push('loading')
    
    return classes
  }, [variant, size, isHovered, isFocused, isActive, isDisabled, isLoading])

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (loadingTimeoutRef.current) {
        clearTimeout(loadingTimeoutRef.current)
      }
      if (stateChangeTimeoutRef.current) {
        clearTimeout(stateChangeTimeoutRef.current)
      }
    }
  }, [])

  return {
    // State values
    isHovered,
    isFocused,
    isActive,
    isLoading,
    isDisabled,
    currentState,
    
    // Event handlers
    handleMouseEnter,
    handleMouseLeave,
    handleMouseDown,
    handleMouseUp,
    handleFocus,
    handleBlur,
    handleKeyDown,
    handleKeyUp,
    
    // Actions
    setLoading: setLoadingState,
    resetState,
    
    // Style helpers
    getButtonStyles,
    getStateClasses
  }
}

/**
 * Hook for managing input field states
 */
export interface UseInputStateOptions {
  disabled?: boolean
  error?: boolean
  onStateChange?: (state: 'idle' | 'hover' | 'focus' | 'error' | 'disabled') => void
}

export const useInputState = (options: UseInputStateOptions = {}) => {
  const { disabled = false, error = false, onStateChange } = options
  
  const [isHovered, setIsHovered] = useState(false)
  const [isFocused, setIsFocused] = useState(false)

  const currentState = disabled ? 'disabled' : 
                      error ? 'error' : 
                      isFocused ? 'focus' : 
                      isHovered ? 'hover' : 'idle'

  useEffect(() => {
    onStateChange?.(currentState)
  }, [currentState, onStateChange])

  const getInputStyles = useCallback(() => {
    const { inputFieldStyles, styleUtils } = require('@/lib/inline-styles')
    
    let baseStyle = inputFieldStyles.base()
    
    if (disabled) {
      baseStyle = styleUtils.combine(baseStyle, inputFieldStyles.disabled())
    } else if (error) {
      baseStyle = styleUtils.combine(baseStyle, inputFieldStyles.error())
    } else if (isFocused) {
      baseStyle = styleUtils.combine(baseStyle, inputFieldStyles.focus())
    } else if (isHovered) {
      baseStyle = styleUtils.combine(baseStyle, inputFieldStyles.hover())
    }
    
    return baseStyle
  }, [isHovered, isFocused, error, disabled])

  return {
    isHovered,
    isFocused,
    currentState,
    
    handleMouseEnter: () => !disabled && setIsHovered(true),
    handleMouseLeave: () => setIsHovered(false),
    handleFocus: () => !disabled && setIsFocused(true),
    handleBlur: () => setIsFocused(false),
    
    getInputStyles
  }
}

export default useButtonState
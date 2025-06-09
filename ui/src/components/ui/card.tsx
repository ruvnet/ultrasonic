import * as React from "react"

const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & { style?: React.CSSProperties }
>(({ style, ...props }, ref) => (
  <div
    ref={ref}
    style={{
      borderRadius: '8px',
      border: '1px solid #e2e8f0',
      backgroundColor: 'white',
      color: '#1e293b',
      boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
      ...style
    }}
    {...props}
  />
))
Card.displayName = "Card"

const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & { style?: React.CSSProperties }
>(({ style, ...props }, ref) => (
  <div
    ref={ref}
    style={{
      display: 'flex',
      flexDirection: 'column',
      gap: '6px',
      padding: '24px',
      ...style
    }}
    {...props}
  />
))
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & { style?: React.CSSProperties }
>(({ style, ...props }, ref) => (
  <h3
    ref={ref}
    style={{
      fontSize: '24px',
      fontWeight: '600',
      lineHeight: '1',
      letterSpacing: '-0.025em',
      color: '#1e293b',
      margin: 0,
      ...style
    }}
    {...props}
  />
))
CardTitle.displayName = "CardTitle"

const CardDescription = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & { style?: React.CSSProperties }
>(({ style, ...props }, ref) => (
  <p
    ref={ref}
    style={{
      fontSize: '14px',
      color: '#64748b',
      margin: 0,
      ...style
    }}
    {...props}
  />
))
CardDescription.displayName = "CardDescription"

const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & { style?: React.CSSProperties }
>(({ style, ...props }, ref) => (
  <div 
    ref={ref} 
    style={{
      padding: '24px',
      paddingTop: 0,
      ...style
    }} 
    {...props} 
  />
))
CardContent.displayName = "CardContent"

const CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & { style?: React.CSSProperties }
>(({ style, ...props }, ref) => (
  <div
    ref={ref}
    style={{
      display: 'flex',
      alignItems: 'center',
      padding: '24px',
      paddingTop: 0,
      ...style
    }}
    {...props}
  />
))
CardFooter.displayName = "CardFooter"

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent }
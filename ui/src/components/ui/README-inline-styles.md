# Inline Styling System Documentation

This document provides comprehensive guidance on using the inline styling system for buttons and interactive elements.

## Overview

The inline styling system provides a complete set of reusable style objects that can be applied directly to React components without external CSS dependencies. This ensures consistent rendering across different environments and eliminates style conflicts.

## Key Features

### 1. Primary Button Styles with Gradients
- Modern gradient backgrounds for main actions
- Smooth hover transitions with elevation effects
- Built-in loading states with spinner animations
- Proper focus indicators for accessibility

### 2. Secondary Button Styles with Borders
- Clean border-based design for secondary actions
- Subtle hover effects with background changes
- Consistent spacing and typography
- Disabled state handling

### 3. Hover State Effects
- CSS-in-JS patterns for dynamic state management
- Smooth transitions between states
- Transform effects for interactive feedback
- Shadow animations for depth perception

### 4. Loading States and Disabled States
- Built-in loading spinner with proper positioning
- Text hiding during loading state
- Disabled state styling with reduced opacity
- Proper cursor management

### 5. Consistent Sizing and Typography
- Five size variants: xs, sm, md, lg, xl
- Icon button variant for square buttons
- Consistent font weights and line heights
- Responsive padding and spacing

### 6. Accessibility Considerations
- WCAG compliant color contrast ratios
- Proper ARIA attributes (aria-disabled, aria-busy)
- Focus management and keyboard navigation
- Screen reader friendly implementations

## Usage Examples

### Basic Button Usage

```tsx
import { PrimaryButton, SecondaryButton } from '@/components/ui/button'

function MyComponent() {
  return (
    <div>
      <PrimaryButton onClick={handleSubmit}>
        Submit Form
      </PrimaryButton>
      <SecondaryButton onClick={handleCancel}>
        Cancel
      </SecondaryButton>
    </div>
  )
}
```

### Advanced Button with States

```tsx
import { InlineStyledButton } from '@/components/ui/button'
import { PlayIcon } from '@/components/icons'

function AdvancedButton() {
  const [isLoading, setIsLoading] = useState(false)
  
  return (
    <InlineStyledButton
      variant="primary"
      size="lg"
      loading={isLoading}
      leftIcon={<PlayIcon />}
      onClick={() => setIsLoading(true)}
      disabled={someCondition}
    >
      Start Process
    </InlineStyledButton>
  )
}
```

### Custom Styling

```tsx
import { primaryButtonStyles, styleUtils } from '@/components/ui/button'

function CustomButton() {
  const [isHovered, setIsHovered] = useState(false)
  
  const customStyle = {
    borderRadius: '20px',
    fontSize: '18px'
  }
  
  const buttonStyle = styleUtils.combine(
    primaryButtonStyles.base('md'),
    isHovered ? primaryButtonStyles.hover() : {},
    customStyle
  )
  
  return (
    <button
      style={buttonStyle}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      Custom Button
    </button>
  )
}
```

### Button Groups

```tsx
import { ButtonGroup, PrimaryButton, SecondaryButton } from '@/components/ui/button'

function FormActions() {
  return (
    <ButtonGroup spacing="md" orientation="horizontal">
      <PrimaryButton type="submit">Save Changes</PrimaryButton>
      <SecondaryButton type="button">Cancel</SecondaryButton>
      <SecondaryButton type="button">Reset</SecondaryButton>
    </ButtonGroup>
  )
}
```

### Input Fields with Inline Styles

```tsx
import { InlineStyledInput } from '@/components/ui/button'
import { SearchIcon } from '@/components/icons'

function SearchInput() {
  const [value, setValue] = useState('')
  const [hasError, setHasError] = useState(false)
  
  return (
    <InlineStyledInput
      placeholder="Search..."
      value={value}
      onChange={(e) => setValue(e.target.value)}
      leftIcon={<SearchIcon />}
      error={hasError}
      disabled={isLoading}
    />
  )
}
```

## Styling API Reference

### Button Variants
- `primary`: Main action buttons with gradient backgrounds
- `secondary`: Secondary actions with border styling
- `success`: Positive actions (save, confirm)
- `warning`: Cautionary actions (proceed with warning)
- `danger`: Destructive actions (delete, remove)
- `ghost`: Minimal styling for subtle actions
- `link`: Link-style buttons with underlines

### Button Sizes
- `xs`: 28px height, extra small padding
- `sm`: 32px height, small padding
- `md`: 40px height, medium padding (default)
- `lg`: 48px height, large padding
- `xl`: 56px height, extra large padding
- `icon`: 40x40px square for icons

### State Management
- `base`: Default appearance
- `hover`: Mouse hover state
- `active`: Mouse press state
- `focus`: Keyboard focus state
- `disabled`: Disabled state
- `loading`: Loading state with spinner

## Style Utilities

### styleUtils.combine()
Merge multiple style objects safely:
```tsx
const combinedStyle = styleUtils.combine(
  baseStyle,
  hoverStyle,
  customStyle
)
```

### styleUtils.withHover()
Apply hover effects conditionally:
```tsx
const style = styleUtils.withHover(
  baseStyle,
  hoverStyle,
  isHovered
)
```

### styleUtils.createColorVariant()
Create custom color variants:
```tsx
const customVariant = styleUtils.createColorVariant(
  '#ff6b6b',  // main color
  '#ff5252'   // hover color
)
```

## Color Palette

The system includes a comprehensive color palette:

```tsx
import { colors } from '@/lib/inline-styles'

// Primary colors
colors.primary.main      // #3b82f6
colors.primary.dark      // #2563eb
colors.primary.gradient  // CSS gradient string

// Semantic colors
colors.success.main      // #10b981
colors.warning.main      // #f59e0b
colors.danger.main       // #ef4444

// Neutral colors
colors.neutral.white     // #ffffff
colors.neutral.gray100   // #f3f4f6
colors.text.primary      // #111827
```

## Typography Scale

```tsx
import { typography } from '@/lib/inline-styles'

typography.fontSize.xs    // 12px
typography.fontSize.sm    // 14px
typography.fontSize.base  // 16px
typography.fontWeight.medium  // 500
```

## Spacing System

```tsx
import { spacing } from '@/lib/inline-styles'

spacing.xs    // 4px
spacing.sm    // 8px
spacing.md    // 12px
spacing.lg    // 16px
spacing.xl    // 20px
```

## Best Practices

### 1. Consistent Usage
- Use pre-built components when possible
- Stick to the defined color palette
- Follow size hierarchy guidelines

### 2. Performance
- Memoize computed styles in components
- Use React.useCallback for event handlers
- Avoid creating new style objects on every render

### 3. Accessibility
- Always include proper ARIA attributes
- Test with keyboard navigation
- Ensure sufficient color contrast
- Provide loading state feedback

### 4. Customization
- Use styleUtils.combine() for style composition
- Create reusable custom variants
- Maintain consistency with the design system

## Migration Guide

### From CSS Classes to Inline Styles

**Before:**
```tsx
<button className="btn btn-primary btn-lg">
  Click me
</button>
```

**After:**
```tsx
<PrimaryButton size="lg">
  Click me
</PrimaryButton>
```

### From Styled Components

**Before:**
```tsx
const StyledButton = styled.button`
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  padding: 12px 20px;
  border-radius: 6px;
  
  &:hover {
    background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
  }
`
```

**After:**
```tsx
<InlineStyledButton variant="primary" size="md">
  Button Text
</InlineStyledButton>
```

## Troubleshooting

### Common Issues

1. **Styles not applying**: Ensure you're importing from the correct path
2. **State not updating**: Check if event handlers are properly bound
3. **Accessibility warnings**: Add required ARIA attributes
4. **Performance issues**: Memoize style computations

### Debug Mode

Enable debug logging for style calculations:
```tsx
// Add to your development environment
const debugStyle = (styleName: string, style: CSSProperties) => {
  console.log(`${styleName}:`, style)
  return style
}

const buttonStyle = debugStyle('primary-button', primaryButtonStyles.base('md'))
```

## Browser Support

The inline styling system supports:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- iOS Safari 14+
- Android Chrome 90+

## Contributing

When adding new styles:
1. Follow the existing naming conventions
2. Include all interactive states
3. Add TypeScript definitions
4. Update documentation
5. Add demo examples
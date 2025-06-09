# Responsive Layout System

A comprehensive responsive layout system using inline styles for React applications. This system provides mobile-first responsive design patterns with TypeScript support.

## Features

- 🏗️ **Container max-widths and centering**
- 📱 **Mobile-first responsive breakpoints**
- 🔧 **Grid layouts for different screen sizes**
- 📏 **Comprehensive spacing and padding scales**
- 📝 **Typography responsive scaling**
- 🎯 **Flexbox layouts for alignment**
- 🎣 **React hooks for runtime responsiveness**

## Quick Start

```tsx
import {
  containerStyles,
  gridStyles,
  flexStyles,
  paddingStyles,
  getResponsiveText,
  mergeStyles,
} from './styles/responsiveStyles';

// Basic responsive container
const MyComponent = () => (
  <div style={mergeStyles(
    containerStyles.base,
    containerStyles.lg,
    paddingStyles.y(8)
  )}>
    <h1 style={getResponsiveText('3xl')}>
      Responsive Title
    </h1>
  </div>
);
```

## Breakpoints

The system uses a mobile-first approach with these breakpoints:

- **Base**: 0px (mobile)
- **sm**: 640px (small tablets)
- **md**: 768px (tablets)
- **lg**: 1024px (small desktops)
- **xl**: 1280px (large desktops)

## Container System

### Basic Usage

```tsx
import { containerStyles, mergeStyles } from './styles/responsiveStyles';

// Responsive container that centers content
const Container = ({ children }) => (
  <div style={mergeStyles(
    containerStyles.base,    // Base styles (width: 100%, auto margins, padding)
    containerStyles.lg       // Large screen max-width
  )}>
    {children}
  </div>
);
```

### Available Container Styles

- `containerStyles.base` - Base container with auto margins and padding
- `containerStyles.sm` - Max-width: 640px
- `containerStyles.md` - Max-width: 768px
- `containerStyles.lg` - Max-width: 1024px + increased padding
- `containerStyles.xl` - Max-width: 1280px
- `containerStyles.fluid` - Max-width: 100%

## Grid System

### Responsive Grid Columns

```tsx
import { gridStyles } from './styles/responsiveStyles';

// Grid that adapts: 1 col → 2 cols → 3 cols → 4 cols
const ResponsiveGrid = () => (
  <div style={mergeStyles(
    gridStyles.container({ base: 1, sm: 2, md: 3, lg: 4 }),
    gridStyles.gap(4)
  )}>
    {items.map(item => <div key={item.id}>{item.content}</div>)}
  </div>
);
```

### Grid Utilities

- `gridStyles.container(cols)` - Creates responsive grid with specified columns
- `gridStyles.gap(size)` - Sets gap between grid items
- `gridStyles.rowGap(size)` - Sets row gap only
- `gridStyles.columnGap(size)` - Sets column gap only

## Flexbox Layouts

### Basic Flexbox

```tsx
import { flexStyles } from './styles/responsiveStyles';

const FlexContainer = () => (
  <div style={mergeStyles(
    flexStyles.container,
    flexStyles.direction.row,
    flexStyles.justify.between,
    flexStyles.align.center,
    flexStyles.gap(4)
  )}>
    <div>Left content</div>
    <div>Right content</div>
  </div>
);
```

### Available Flex Utilities

#### Direction
- `flexStyles.direction.row`
- `flexStyles.direction.col`
- `flexStyles.direction.rowReverse`
- `flexStyles.direction.colReverse`

#### Justify Content
- `flexStyles.justify.start`
- `flexStyles.justify.end`
- `flexStyles.justify.center`
- `flexStyles.justify.between`
- `flexStyles.justify.around`
- `flexStyles.justify.evenly`

#### Align Items
- `flexStyles.align.start`
- `flexStyles.align.end`
- `flexStyles.align.center`
- `flexStyles.align.baseline`
- `flexStyles.align.stretch`

## Typography System

### Responsive Text Sizing

```tsx
import { getResponsiveText, typography } from './styles/responsiveStyles';

const ResponsiveHeading = () => (
  <h1 style={mergeStyles(
    getResponsiveText('4xl'),  // Scales: 36px → 48px → 56px
    {
      fontWeight: typography.fontWeight.bold,
      lineHeight: typography.lineHeight.tight,
    }
  )}>
    Responsive Heading
  </h1>
);
```

### Font Sizes

All font sizes automatically scale on larger screens:

- `xs`: 12px
- `sm`: 14px
- `base`: 16px
- `lg`: 18px → 20px
- `xl`: 20px → 24px
- `2xl`: 24px → 32px
- `3xl`: 30px → 40px
- `4xl`: 36px → 56px
- `5xl`: 48px → 72px
- `6xl`: 60px → 96px

## Spacing System

### Spacing Scale

The spacing system uses a consistent scale based on rem units:

```tsx
import { spacing, paddingStyles, marginStyles } from './styles/responsiveStyles';

// Using spacing directly
const customStyles = {
  padding: spacing[4],        // 1rem (16px)
  margin: spacing[8],         // 2rem (32px)
};

// Using utility functions
const utilityStyles = mergeStyles(
  paddingStyles.all(4),       // padding: 1rem
  marginStyles.x(8),          // margin-left and margin-right: 2rem
);
```

### Padding Utilities

- `paddingStyles.all(size)` - All sides
- `paddingStyles.x(size)` - Left and right
- `paddingStyles.y(size)` - Top and bottom
- `paddingStyles.top(size)` - Top only
- `paddingStyles.right(size)` - Right only
- `paddingStyles.bottom(size)` - Bottom only
- `paddingStyles.left(size)` - Left only

### Margin Utilities

- `marginStyles.all(size)` - All sides
- `marginStyles.x(size)` - Left and right
- `marginStyles.y(size)` - Top and bottom
- `marginStyles.top(size)` - Top only
- `marginStyles.right(size)` - Right only
- `marginStyles.bottom(size)` - Bottom only
- `marginStyles.left(size)` - Left only
- `marginStyles.auto` - Auto left and right margins (centering)

## Common Patterns

### Pre-built Responsive Patterns

```tsx
import { patterns } from './styles/responsiveStyles';

// Stack on mobile, side-by-side on desktop
<div style={patterns.stackToSideBySide}>
  <div>Content</div>
  <div>Sidebar</div>
</div>

// Card grid that adapts
<div style={patterns.cardGrid}>
  {cards.map(card => <CardComponent key={card.id} {...card} />)}
</div>

// Hide on mobile
<div style={patterns.hideOnMobile}>
  Desktop-only content
</div>

// Show only on mobile
<div style={patterns.showOnlyMobile}>
  Mobile-only content
</div>
```

## React Hooks for Runtime Responsiveness

### useBreakpoint Hook

```tsx
import { useBreakpoint } from './styles/useMediaQuery';

const ResponsiveComponent = () => {
  const { isMobile, isTablet, isDesktop, isSm, isMd, isLg, isXl } = useBreakpoint();

  return (
    <div>
      {isMobile && <MobileNav />}
      {isDesktop && <DesktopNav />}
    </div>
  );
};
```

### useResponsiveValue Hook

```tsx
import { useResponsiveValue } from './styles/useMediaQuery';

const ResponsiveComponent = () => {
  const columns = useResponsiveValue({
    base: 1,
    sm: 2,
    md: 3,
    lg: 4,
  });

  const gridStyle = {
    display: 'grid',
    gridTemplateColumns: `repeat(${columns}, 1fr)`,
    gap: '1rem',
  };

  return <div style={gridStyle}>{/* content */}</div>;
};
```

### useResponsiveStyles Hook

```tsx
import { useResponsiveStyles } from './styles/useMediaQuery';

const ResponsiveComponent = () => {
  const styles = useResponsiveStyles({
    base: {
      padding: '1rem',
      fontSize: '1rem',
    },
    md: {
      padding: '2rem',
      fontSize: '1.25rem',
    },
    lg: {
      padding: '3rem',
      fontSize: '1.5rem',
    },
  });

  return <div style={styles}>Responsive content</div>;
};
```

## Advanced Usage

### Custom Responsive Utilities

```tsx
import { responsive, breakpoints } from './styles/responsiveStyles';

// Create custom responsive styles
const customResponsiveStyle = responsive({
  base: { fontSize: '1rem', padding: '0.5rem' },
  md: { fontSize: '1.25rem', padding: '1rem' },
  lg: { fontSize: '1.5rem', padding: '1.5rem' },
});

// Use in component
<div style={customResponsiveStyle}>Custom responsive element</div>
```

### Merging Multiple Style Objects

```tsx
import { mergeStyles } from './styles/responsiveStyles';

const combinedStyles = mergeStyles(
  containerStyles.base,
  containerStyles.lg,
  paddingStyles.y(8),
  flexStyles.container,
  flexStyles.direction.col,
  { backgroundColor: 'white', borderRadius: '0.5rem' }
);
```

## CSS-in-JS Alternative

For environments that support CSS-in-JS with media queries:

```tsx
import styled from 'styled-components'; // or emotion
import { breakpoints } from './styles/responsiveStyles';

const ResponsiveDiv = styled.div`
  padding: 1rem;
  
  @media (min-width: ${breakpoints.md}px) {
    padding: 2rem;
  }
  
  @media (min-width: ${breakpoints.lg}px) {
    padding: 3rem;
  }
`;
```

## Best Practices

1. **Start Mobile-First**: Always define base styles for mobile, then enhance for larger screens
2. **Use Semantic Breakpoints**: Choose breakpoints based on content, not device sizes
3. **Consistent Spacing**: Use the provided spacing scale for consistency
4. **Performance**: Prefer CSS over JavaScript for static responsive behavior
5. **Testing**: Test on actual devices, not just browser dev tools

## Examples

See the complete examples in:
- `/src/styles/examples.tsx` - Comprehensive component examples
- `/src/pages/demo/ResponsiveLayoutDemo.tsx` - Interactive demo page

## Type Safety

All utilities are fully typed with TypeScript, providing:
- Autocomplete for spacing values
- Type-safe breakpoint configuration
- Proper typing for style objects
- IntelliSense support in VS Code
// Responsive Layout System with Inline Styles
// Mobile-first approach with breakpoints at 640px (sm), 768px (md), 1024px (lg), 1280px (xl)

// Breakpoint utilities
export const breakpoints = {
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
} as const;

// Media query helper
export const mediaQuery = (minWidth: number) => `@media (min-width: ${minWidth}px)`;

// Responsive container styles
export const containerStyles = {
  base: {
    width: '100%',
    marginLeft: 'auto',
    marginRight: 'auto',
    paddingLeft: '1rem',
    paddingRight: '1rem',
  },
  sm: {
    maxWidth: '640px',
  },
  md: {
    maxWidth: '768px',
  },
  lg: {
    maxWidth: '1024px',
    paddingLeft: '2rem',
    paddingRight: '2rem',
  },
  xl: {
    maxWidth: '1280px',
  },
  fluid: {
    maxWidth: '100%',
  },
};

// Spacing scale (based on rem units)
export const spacing = {
  0: '0',
  px: '1px',
  0.5: '0.125rem', // 2px
  1: '0.25rem',    // 4px
  1.5: '0.375rem', // 6px
  2: '0.5rem',     // 8px
  2.5: '0.625rem', // 10px
  3: '0.75rem',    // 12px
  3.5: '0.875rem', // 14px
  4: '1rem',       // 16px
  5: '1.25rem',    // 20px
  6: '1.5rem',     // 24px
  7: '1.75rem',    // 28px
  8: '2rem',       // 32px
  9: '2.25rem',    // 36px
  10: '2.5rem',    // 40px
  11: '2.75rem',   // 44px
  12: '3rem',      // 48px
  14: '3.5rem',    // 56px
  16: '4rem',      // 64px
  20: '5rem',      // 80px
  24: '6rem',      // 96px
  28: '7rem',      // 112px
  32: '8rem',      // 128px
  36: '9rem',      // 144px
  40: '10rem',     // 160px
  44: '11rem',     // 176px
  48: '12rem',     // 192px
  52: '13rem',     // 208px
  56: '14rem',     // 224px
  60: '15rem',     // 240px
  64: '16rem',     // 256px
  72: '18rem',     // 288px
  80: '20rem',     // 320px
  96: '24rem',     // 384px
} as const;

// Typography scale with responsive sizing
export const typography = {
  // Font sizes with responsive scaling
  fontSize: {
    xs: { base: '0.75rem', sm: '0.75rem', md: '0.75rem' },      // 12px
    sm: { base: '0.875rem', sm: '0.875rem', md: '0.875rem' },   // 14px
    base: { base: '1rem', sm: '1rem', md: '1rem' },             // 16px
    lg: { base: '1.125rem', sm: '1.125rem', md: '1.25rem' },    // 18px -> 20px
    xl: { base: '1.25rem', sm: '1.25rem', md: '1.5rem' },       // 20px -> 24px
    '2xl': { base: '1.5rem', sm: '1.75rem', md: '2rem' },       // 24px -> 32px
    '3xl': { base: '1.875rem', sm: '2.25rem', md: '2.5rem' },   // 30px -> 40px
    '4xl': { base: '2.25rem', sm: '3rem', md: '3.5rem' },       // 36px -> 56px
    '5xl': { base: '3rem', sm: '4rem', md: '4.5rem' },          // 48px -> 72px
    '6xl': { base: '3.75rem', sm: '5rem', md: '6rem' },         // 60px -> 96px
  },
  // Line heights
  lineHeight: {
    none: '1',
    tight: '1.25',
    snug: '1.375',
    normal: '1.5',
    relaxed: '1.625',
    loose: '2',
  },
  // Font weights
  fontWeight: {
    thin: '100',
    extralight: '200',
    light: '300',
    normal: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
    extrabold: '800',
    black: '900',
  },
};

// Grid system with responsive columns
export const gridStyles = {
  // Grid container
  container: (cols: { base?: number; sm?: number; md?: number; lg?: number; xl?: number }) => ({
    display: 'grid',
    gridTemplateColumns: `repeat(${cols.base || 1}, minmax(0, 1fr))`,
    [mediaQuery(breakpoints.sm)]: cols.sm ? {
      gridTemplateColumns: `repeat(${cols.sm}, minmax(0, 1fr))`,
    } : undefined,
    [mediaQuery(breakpoints.md)]: cols.md ? {
      gridTemplateColumns: `repeat(${cols.md}, minmax(0, 1fr))`,
    } : undefined,
    [mediaQuery(breakpoints.lg)]: cols.lg ? {
      gridTemplateColumns: `repeat(${cols.lg}, minmax(0, 1fr))`,
    } : undefined,
    [mediaQuery(breakpoints.xl)]: cols.xl ? {
      gridTemplateColumns: `repeat(${cols.xl}, minmax(0, 1fr))`,
    } : undefined,
  }),
  // Gap utilities
  gap: (size: keyof typeof spacing) => ({
    gap: spacing[size],
  }),
  rowGap: (size: keyof typeof spacing) => ({
    rowGap: spacing[size],
  }),
  columnGap: (size: keyof typeof spacing) => ({
    columnGap: spacing[size],
  }),
};

// Flexbox layouts
export const flexStyles = {
  // Flex container
  container: {
    display: 'flex',
  },
  // Direction
  direction: {
    row: { flexDirection: 'row' as const },
    rowReverse: { flexDirection: 'row-reverse' as const },
    col: { flexDirection: 'column' as const },
    colReverse: { flexDirection: 'column-reverse' as const },
  },
  // Wrap
  wrap: {
    wrap: { flexWrap: 'wrap' as const },
    nowrap: { flexWrap: 'nowrap' as const },
    wrapReverse: { flexWrap: 'wrap-reverse' as const },
  },
  // Justify content
  justify: {
    start: { justifyContent: 'flex-start' },
    end: { justifyContent: 'flex-end' },
    center: { justifyContent: 'center' },
    between: { justifyContent: 'space-between' },
    around: { justifyContent: 'space-around' },
    evenly: { justifyContent: 'space-evenly' },
  },
  // Align items
  align: {
    start: { alignItems: 'flex-start' },
    end: { alignItems: 'flex-end' },
    center: { alignItems: 'center' },
    baseline: { alignItems: 'baseline' },
    stretch: { alignItems: 'stretch' },
  },
  // Gap
  gap: (size: keyof typeof spacing) => ({
    gap: spacing[size],
  }),
};

// Padding utilities
export const paddingStyles = {
  all: (size: keyof typeof spacing) => ({
    padding: spacing[size],
  }),
  x: (size: keyof typeof spacing) => ({
    paddingLeft: spacing[size],
    paddingRight: spacing[size],
  }),
  y: (size: keyof typeof spacing) => ({
    paddingTop: spacing[size],
    paddingBottom: spacing[size],
  }),
  top: (size: keyof typeof spacing) => ({
    paddingTop: spacing[size],
  }),
  right: (size: keyof typeof spacing) => ({
    paddingRight: spacing[size],
  }),
  bottom: (size: keyof typeof spacing) => ({
    paddingBottom: spacing[size],
  }),
  left: (size: keyof typeof spacing) => ({
    paddingLeft: spacing[size],
  }),
};

// Margin utilities
export const marginStyles = {
  all: (size: keyof typeof spacing) => ({
    margin: spacing[size],
  }),
  x: (size: keyof typeof spacing) => ({
    marginLeft: spacing[size],
    marginRight: spacing[size],
  }),
  y: (size: keyof typeof spacing) => ({
    marginTop: spacing[size],
    marginBottom: spacing[size],
  }),
  top: (size: keyof typeof spacing) => ({
    marginTop: spacing[size],
  }),
  right: (size: keyof typeof spacing) => ({
    marginRight: spacing[size],
  }),
  bottom: (size: keyof typeof spacing) => ({
    marginBottom: spacing[size],
  }),
  left: (size: keyof typeof spacing) => ({
    marginLeft: spacing[size],
  }),
  auto: {
    marginLeft: 'auto',
    marginRight: 'auto',
  },
};

// Responsive utilities helper
export const responsive = <T extends Record<string, any>>(
  styles: {
    base?: T;
    sm?: T;
    md?: T;
    lg?: T;
    xl?: T;
  }
): Record<string, any> => {
  const result: Record<string, any> = styles.base || {};
  
  if (styles.sm) {
    result[mediaQuery(breakpoints.sm)] = styles.sm;
  }
  if (styles.md) {
    result[mediaQuery(breakpoints.md)] = styles.md;
  }
  if (styles.lg) {
    result[mediaQuery(breakpoints.lg)] = styles.lg;
  }
  if (styles.xl) {
    result[mediaQuery(breakpoints.xl)] = styles.xl;
  }
  
  return result;
};

// Common responsive patterns
export const patterns = {
  // Stack on mobile, side-by-side on desktop
  stackToSideBySide: {
    ...flexStyles.container,
    ...flexStyles.direction.col,
    ...flexStyles.gap(4),
    [mediaQuery(breakpoints.md)]: {
      ...flexStyles.direction.row,
      ...flexStyles.align.center,
    },
  },
  
  // Hide on mobile
  hideOnMobile: {
    display: 'none',
    [mediaQuery(breakpoints.md)]: {
      display: 'block',
    },
  },
  
  // Show only on mobile
  showOnlyMobile: {
    display: 'block',
    [mediaQuery(breakpoints.md)]: {
      display: 'none',
    },
  },
  
  // Responsive card grid
  cardGrid: {
    ...gridStyles.container({ base: 1, sm: 2, md: 3, lg: 4 }),
    ...gridStyles.gap(4),
  },
  
  // Centered content
  centeredContent: {
    ...flexStyles.container,
    ...flexStyles.direction.col,
    ...flexStyles.justify.center,
    ...flexStyles.align.center,
    minHeight: '100vh',
    ...paddingStyles.all(4),
  },
  
  // Two column layout
  twoColumnLayout: {
    ...gridStyles.container({ base: 1, md: 2 }),
    ...gridStyles.gap(6),
  },
  
  // Sidebar layout
  sidebarLayout: {
    display: 'grid',
    gridTemplateColumns: '1fr',
    [mediaQuery(breakpoints.lg)]: {
      gridTemplateColumns: '16rem 1fr',
      gap: spacing[6],
    },
  },
};

// Typography responsive helpers
export const getResponsiveText = (size: keyof typeof typography.fontSize) => {
  const sizes = typography.fontSize[size];
  return {
    fontSize: sizes.base,
    [mediaQuery(breakpoints.sm)]: sizes.sm !== sizes.base ? {
      fontSize: sizes.sm,
    } : undefined,
    [mediaQuery(breakpoints.md)]: sizes.md !== sizes.sm ? {
      fontSize: sizes.md,
    } : undefined,
  };
};

// Merge styles utility
export const mergeStyles = (...styles: Array<Record<string, any> | undefined>): Record<string, any> => {
  return styles.filter(Boolean).reduce((acc, style) => {
    return { ...acc, ...style };
  }, {});
};
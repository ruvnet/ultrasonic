// Custom hook for responsive behavior with inline styles
import { useState, useEffect } from 'react';
import { breakpoints } from './responsiveStyles';

// Media query hook for runtime responsive behavior
export const useMediaQuery = (query: string): boolean => {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia(query);
    const handler = (event: MediaQueryListEvent) => setMatches(event.matches);
    
    // Set initial value
    setMatches(mediaQuery.matches);
    
    // Listen for changes
    mediaQuery.addEventListener('change', handler);
    
    return () => mediaQuery.removeEventListener('change', handler);
  }, [query]);

  return matches;
};

// Breakpoint-specific hooks
export const useBreakpoint = () => {
  const isSm = useMediaQuery(`(min-width: ${breakpoints.sm}px)`);
  const isMd = useMediaQuery(`(min-width: ${breakpoints.md}px)`);
  const isLg = useMediaQuery(`(min-width: ${breakpoints.lg}px)`);
  const isXl = useMediaQuery(`(min-width: ${breakpoints.xl}px)`);

  return {
    isSm,
    isMd,
    isLg,
    isXl,
    isMobile: !isSm,
    isTablet: isSm && !isLg,
    isDesktop: isLg,
  };
};

// Responsive value hook - returns different values based on screen size
export const useResponsiveValue = <T>(values: {
  base: T;
  sm?: T;
  md?: T;
  lg?: T;
  xl?: T;
}): T => {
  const { isSm, isMd, isLg, isXl } = useBreakpoint();

  if (isXl && values.xl !== undefined) return values.xl;
  if (isLg && values.lg !== undefined) return values.lg;
  if (isMd && values.md !== undefined) return values.md;
  if (isSm && values.sm !== undefined) return values.sm;
  
  return values.base;
};

// Window size hook
export const useWindowSize = () => {
  const [windowSize, setWindowSize] = useState({
    width: typeof window !== 'undefined' ? window.innerWidth : 0,
    height: typeof window !== 'undefined' ? window.innerHeight : 0,
  });

  useEffect(() => {
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return windowSize;
};

// Dynamic styles based on screen size
export const useResponsiveStyles = <T extends Record<string, any>>(
  styleMap: {
    base: T;
    sm?: Partial<T>;
    md?: Partial<T>;
    lg?: Partial<T>;
    xl?: Partial<T>;
  }
): T => {
  const { isSm, isMd, isLg, isXl } = useBreakpoint();

  let styles = { ...styleMap.base };

  if (isSm && styleMap.sm) {
    styles = { ...styles, ...styleMap.sm };
  }
  if (isMd && styleMap.md) {
    styles = { ...styles, ...styleMap.md };
  }
  if (isLg && styleMap.lg) {
    styles = { ...styles, ...styleMap.lg };
  }
  if (isXl && styleMap.xl) {
    styles = { ...styles, ...styleMap.xl };
  }

  return styles;
};
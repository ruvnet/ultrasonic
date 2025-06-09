// Comprehensive demo of the responsive layout system
import React from 'react';
import {
  containerStyles,
  spacing,
  gridStyles,
  flexStyles,
  paddingStyles,
  marginStyles,
  patterns,
  getResponsiveText,
  typography,
  mergeStyles,
  responsive,
} from '../../styles/responsiveStyles';
import {
  useBreakpoint,
  useResponsiveValue,
  useResponsiveStyles,
} from '../../styles/useMediaQuery';

export const ResponsiveLayoutDemo: React.FC = () => {
  const breakpoint = useBreakpoint();
  
  // Dynamic column count based on screen size
  const columns = useResponsiveValue({
    base: 1,
    sm: 2,
    md: 3,
    lg: 4,
  });

  // Dynamic padding based on screen size
  const sectionPadding = useResponsiveValue({
    base: 4,
    md: 8,
    lg: 12,
  } as const);

  // Responsive styles using hook
  const heroStyles = useResponsiveStyles({
    base: {
      backgroundColor: '#1e40af',
      color: 'white',
      textAlign: 'center' as const,
      padding: spacing[8],
    },
    md: {
      padding: spacing[16],
    },
    lg: {
      padding: spacing[20],
    },
  });

  const pageStyles = {
    minHeight: '100vh',
    backgroundColor: '#f8fafc',
  };

  const sectionStyles = mergeStyles(
    containerStyles.base,
    containerStyles.xl,
    paddingStyles.y(sectionPadding)
  );

  return (
    <div style={pageStyles}>
      {/* Hero Section */}
      <section style={heroStyles}>
        <div style={mergeStyles(containerStyles.base, containerStyles.lg)}>
          <h1 style={mergeStyles(
            getResponsiveText('5xl'),
            {
              fontWeight: typography.fontWeight.bold,
              marginBottom: spacing[4],
            }
          )}>
            Responsive Layout Demo
          </h1>
          <p style={mergeStyles(
            getResponsiveText('xl'),
            {
              opacity: 0.9,
              marginBottom: spacing[8],
              maxWidth: '600px',
              marginLeft: 'auto',
              marginRight: 'auto',
            }
          )}>
            A comprehensive demonstration of responsive design patterns using inline styles
          </p>
          <div style={{
            ...flexStyles.container,
            ...flexStyles.justify.center,
            ...flexStyles.gap(4),
            flexWrap: 'wrap',
          }}>
            <button style={{
              ...paddingStyles.x(6),
              ...paddingStyles.y(3),
              backgroundColor: 'white',
              color: '#1e40af',
              border: 'none',
              borderRadius: '0.5rem',
              fontWeight: typography.fontWeight.semibold,
              cursor: 'pointer',
            }}>
              Get Started
            </button>
            <button style={{
              ...paddingStyles.x(6),
              ...paddingStyles.y(3),
              backgroundColor: 'transparent',
              color: 'white',
              border: '2px solid white',
              borderRadius: '0.5rem',
              fontWeight: typography.fontWeight.semibold,
              cursor: 'pointer',
            }}>
              Learn More
            </button>
          </div>
        </div>
      </section>

      {/* Breakpoint Info */}
      <section style={sectionStyles}>
        <div style={{
          backgroundColor: 'white',
          ...paddingStyles.all(6),
          borderRadius: '0.75rem',
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
          marginBottom: spacing[8],
        }}>
          <h2 style={mergeStyles(
            getResponsiveText('2xl'),
            {
              fontWeight: typography.fontWeight.bold,
              marginBottom: spacing[4],
            }
          )}>
            Current Breakpoint Information
          </h2>
          <div style={{
            ...gridStyles.container({ base: 2, md: 4 }),
            ...gridStyles.gap(4),
          }}>
            <div>
              <strong>Mobile:</strong> {breakpoint.isMobile ? '✅' : '❌'}
            </div>
            <div>
              <strong>Small:</strong> {breakpoint.isSm ? '✅' : '❌'}
            </div>
            <div>
              <strong>Medium:</strong> {breakpoint.isMd ? '✅' : '❌'}
            </div>
            <div>
              <strong>Large:</strong> {breakpoint.isLg ? '✅' : '❌'}
            </div>
          </div>
          <p style={marginStyles.top(4)}>
            <strong>Active columns:</strong> {columns} | 
            <strong> Device type:</strong> {
              breakpoint.isMobile ? 'Mobile' :
              breakpoint.isTablet ? 'Tablet' : 'Desktop'
            }
          </p>
        </div>
      </section>

      {/* Grid Examples */}
      <section style={sectionStyles}>
        <h2 style={mergeStyles(
          getResponsiveText('3xl'),
          {
            fontWeight: typography.fontWeight.bold,
            marginBottom: spacing[8],
            textAlign: 'center',
          }
        )}>
          Responsive Grid Layouts
        </h2>

        {/* Card Grid */}
        <div style={marginStyles.bottom(12)}>
          <h3 style={mergeStyles(
            getResponsiveText('xl'),
            {
              fontWeight: typography.fontWeight.semibold,
              marginBottom: spacing[4],
            }
          )}>
            Card Grid (1→2→3→4 columns)
          </h3>
          <div style={patterns.cardGrid}>
            {Array.from({ length: 8 }, (_, i) => (
              <div key={i} style={{
                backgroundColor: 'white',
                ...paddingStyles.all(6),
                borderRadius: '0.5rem',
                boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
                border: '1px solid #e5e7eb',
              }}>
                <h4 style={{
                  fontWeight: typography.fontWeight.semibold,
                  marginBottom: spacing[2],
                }}>
                  Card {i + 1}
                </h4>
                <p style={{
                  color: '#6b7280',
                  fontSize: typography.fontSize.sm.base,
                }}>
                  This card adapts to different screen sizes automatically.
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Two Column Layout */}
        <div style={marginStyles.bottom(12)}>
          <h3 style={mergeStyles(
            getResponsiveText('xl'),
            {
              fontWeight: typography.fontWeight.semibold,
              marginBottom: spacing[4],
            }
          )}>
            Two Column Layout (Stack on Mobile)
          </h3>
          <div style={patterns.twoColumnLayout}>
            <div style={{
              backgroundColor: 'white',
              ...paddingStyles.all(6),
              borderRadius: '0.5rem',
              boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
            }}>
              <h4 style={{
                fontWeight: typography.fontWeight.semibold,
                marginBottom: spacing[3],
              }}>
                Left Column
              </h4>
              <p style={{ lineHeight: typography.lineHeight.relaxed }}>
                This column stacks on top on mobile devices and appears on the left
                on larger screens. The layout automatically adjusts based on available space.
              </p>
            </div>
            <div style={{
              backgroundColor: 'white',
              ...paddingStyles.all(6),
              borderRadius: '0.5rem',
              boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
            }}>
              <h4 style={{
                fontWeight: typography.fontWeight.semibold,
                marginBottom: spacing[3],
              }}>
                Right Column
              </h4>
              <p style={{ lineHeight: typography.lineHeight.relaxed }}>
                This column appears below the left column on mobile and to the right
                on larger screens. Perfect for content that needs to be accessible on all devices.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Flexbox Examples */}
      <section style={sectionStyles}>
        <h2 style={mergeStyles(
          getResponsiveText('3xl'),
          {
            fontWeight: typography.fontWeight.bold,
            marginBottom: spacing[8],
            textAlign: 'center',
          }
        )}>
          Flexbox Layouts
        </h2>

        {/* Stack to Side-by-Side */}
        <div style={marginStyles.bottom(12)}>
          <h3 style={mergeStyles(
            getResponsiveText('xl'),
            {
              fontWeight: typography.fontWeight.semibold,
              marginBottom: spacing[4],
            }
          )}>
            Stack to Side-by-Side Pattern
          </h3>
          <div style={{
            backgroundColor: 'white',
            ...paddingStyles.all(6),
            borderRadius: '0.5rem',
            boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
          }}>
            <div style={patterns.stackToSideBySide}>
              <div style={{ flex: 1 }}>
                <h4 style={{
                  fontWeight: typography.fontWeight.semibold,
                  marginBottom: spacing[3],
                }}>
                  Content Section
                </h4>
                <p style={{
                  lineHeight: typography.lineHeight.relaxed,
                  marginBottom: spacing[4],
                }}>
                  This content stacks vertically on mobile devices and appears
                  side-by-side with the image on larger screens. This pattern is
                  perfect for feature sections and product showcases.
                </p>
                <button style={{
                  ...paddingStyles.x(4),
                  ...paddingStyles.y(2),
                  backgroundColor: '#3b82f6',
                  color: 'white',
                  border: 'none',
                  borderRadius: '0.25rem',
                  fontWeight: typography.fontWeight.medium,
                  cursor: 'pointer',
                }}>
                  Call to Action
                </button>
              </div>
              <div style={{
                flex: 1,
                backgroundColor: '#f3f4f6',
                borderRadius: '0.5rem',
                minHeight: '200px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#6b7280',
                fontWeight: typography.fontWeight.medium,
              }}>
                Image Placeholder
              </div>
            </div>
          </div>
        </div>

        {/* Centered Content */}
        <div style={marginStyles.bottom(12)}>
          <h3 style={mergeStyles(
            getResponsiveText('xl'),
            {
              fontWeight: typography.fontWeight.semibold,
              marginBottom: spacing[4],
            }
          )}>
            Centered Content Layout
          </h3>
          <div style={{
            backgroundColor: 'white',
            ...paddingStyles.all(6),
            borderRadius: '0.5rem',
            boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
            minHeight: '300px',
            ...flexStyles.container,
            ...flexStyles.direction.col,
            ...flexStyles.justify.center,
            ...flexStyles.align.center,
            textAlign: 'center',
          }}>
            <h4 style={mergeStyles(
              getResponsiveText('2xl'),
              {
                fontWeight: typography.fontWeight.bold,
                marginBottom: spacing[4],
              }
            )}>
              Perfectly Centered
            </h4>
            <p style={{
              color: '#6b7280',
              marginBottom: spacing[6],
              maxWidth: '400px',
            }}>
              This content is perfectly centered both horizontally and vertically
              using flexbox utilities. Great for hero sections and modal content.
            </p>
            <button style={{
              ...paddingStyles.x(6),
              ...paddingStyles.y(3),
              backgroundColor: '#10b981',
              color: 'white',
              border: 'none',
              borderRadius: '0.5rem',
              fontWeight: typography.fontWeight.semibold,
              cursor: 'pointer',
            }}>
              Get Started
            </button>
          </div>
        </div>
      </section>

      {/* Typography Scale */}
      <section style={sectionStyles}>
        <h2 style={mergeStyles(
          getResponsiveText('3xl'),
          {
            fontWeight: typography.fontWeight.bold,
            marginBottom: spacing[8],
            textAlign: 'center',
          }
        )}>
          Responsive Typography
        </h2>
        <div style={{
          backgroundColor: 'white',
          ...paddingStyles.all(8),
          borderRadius: '0.75rem',
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        }}>
          {(['6xl', '5xl', '4xl', '3xl', '2xl', 'xl', 'lg', 'base', 'sm', 'xs'] as const).map((size) => (
            <div key={size} style={marginStyles.bottom(4)}>
              <span style={mergeStyles(
                getResponsiveText(size),
                { fontWeight: typography.fontWeight.semibold }
              )}>
                {size.toUpperCase()} - This text scales responsively
              </span>
            </div>
          ))}
        </div>
      </section>

      {/* Spacing Examples */}
      <section style={sectionStyles}>
        <h2 style={mergeStyles(
          getResponsiveText('3xl'),
          {
            fontWeight: typography.fontWeight.bold,
            marginBottom: spacing[8],
            textAlign: 'center',
          }
        )}>
          Spacing System
        </h2>
        <div style={{
          backgroundColor: 'white',
          ...paddingStyles.all(8),
          borderRadius: '0.75rem',
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        }}>
          <h3 style={marginStyles.bottom(6)}>Padding Examples</h3>
          <div style={{
            ...gridStyles.container({ base: 1, sm: 2, md: 4 }),
            ...gridStyles.gap(4),
            marginBottom: spacing[8],
          }}>
            {[2, 4, 6, 8].map((size) => (
              <div key={size} style={{
                backgroundColor: '#dbeafe',
                border: '2px dashed #3b82f6',
                borderRadius: '0.25rem',
                textAlign: 'center',
                color: '#1e40af',
                fontWeight: typography.fontWeight.medium,
                ...paddingStyles.all(size as keyof typeof spacing),
              }}>
                p-{size}
              </div>
            ))}
          </div>

          <h3 style={marginStyles.bottom(6)}>Margin Examples</h3>
          <div style={{ backgroundColor: '#f3f4f6', padding: spacing[4], borderRadius: '0.25rem' }}>
            {[2, 4, 6, 8].map((size) => (
              <div key={size} style={{
                backgroundColor: '#fef3c7',
                border: '2px solid #f59e0b',
                borderRadius: '0.25rem',
                textAlign: 'center',
                color: '#92400e',
                fontWeight: typography.fontWeight.medium,
                padding: spacing[2],
                ...marginStyles.bottom(size as keyof typeof spacing),
              }}>
                mb-{size}
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default ResponsiveLayoutDemo;
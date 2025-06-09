// Examples of using the responsive layout system
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
  breakpoints,
} from './responsiveStyles';

// Example 1: Responsive Container with Typography
export const ResponsiveHero: React.FC = () => {
  const heroStyles = mergeStyles(
    containerStyles.base,
    containerStyles.lg,
    paddingStyles.y(16),
    {
      textAlign: 'center' as const,
      background: 'linear-gradient(to right, #3b82f6, #8b5cf6)',
      color: 'white',
    }
  );

  const titleStyles = mergeStyles(
    getResponsiveText('4xl'),
    {
      fontWeight: typography.fontWeight.bold,
      lineHeight: typography.lineHeight.tight,
      marginBottom: spacing[4],
    }
  );

  const subtitleStyles = mergeStyles(
    getResponsiveText('lg'),
    {
      opacity: 0.9,
      marginBottom: spacing[8],
    }
  );

  return (
    <section style={heroStyles}>
      <h1 style={titleStyles}>
        Responsive Design System
      </h1>
      <p style={subtitleStyles}>
        A comprehensive layout system with inline styles for React applications
      </p>
      <button
        style={{
          ...paddingStyles.x(6),
          ...paddingStyles.y(3),
          backgroundColor: 'white',
          color: '#3b82f6',
          borderRadius: '0.5rem',
          border: 'none',
          fontWeight: typography.fontWeight.semibold,
          cursor: 'pointer',
        }}
      >
        Get Started
      </button>
    </section>
  );
};

// Example 2: Card Grid Layout
export const ResponsiveCardGrid: React.FC = () => {
  const cards = [
    { title: 'Performance', description: 'Fast and optimized for all devices' },
    { title: 'Responsive', description: 'Works perfectly on mobile and desktop' },
    { title: 'Accessible', description: 'Built with accessibility in mind' },
    { title: 'Modern', description: 'Uses latest web technologies' },
  ];

  const containerStyle = mergeStyles(
    containerStyles.base,
    containerStyles.xl,
    paddingStyles.y(12)
  );

  const gridStyle = patterns.cardGrid;

  const cardStyle = {
    backgroundColor: 'white',
    borderRadius: '0.75rem',
    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    ...paddingStyles.all(6),
    border: '1px solid #e5e7eb',
  };

  const titleStyle = mergeStyles(
    getResponsiveText('xl'),
    {
      fontWeight: typography.fontWeight.semibold,
      marginBottom: spacing[2],
      color: '#1f2937',
    }
  );

  const descriptionStyle = {
    color: '#6b7280',
    lineHeight: typography.lineHeight.relaxed,
  };

  return (
    <section style={containerStyle}>
      <div style={gridStyle}>
        {cards.map((card, index) => (
          <div key={index} style={cardStyle}>
            <h3 style={titleStyle}>{card.title}</h3>
            <p style={descriptionStyle}>{card.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

// Example 3: Sidebar Layout
export const ResponsiveSidebarLayout: React.FC = () => {
  const layoutStyle = mergeStyles(
    containerStyles.base,
    containerStyles.xl,
    patterns.sidebarLayout,
    { minHeight: '80vh' }
  );

  const sidebarStyle = {
    backgroundColor: '#f9fafb',
    ...paddingStyles.all(4),
    borderRadius: '0.5rem',
    ...marginStyles.bottom(4),
    [`@media (min-width: ${breakpoints.lg}px)`]: {
      marginBottom: 0,
    },
  };

  const mainStyle = {
    ...paddingStyles.all(4),
  };

  const navItemStyle = {
    display: 'block',
    ...paddingStyles.all(2),
    marginBottom: spacing[1],
    color: '#374151',
    textDecoration: 'none',
    borderRadius: '0.25rem',
    ':hover': {
      backgroundColor: '#e5e7eb',
    },
  };

  return (
    <div style={layoutStyle}>
      <aside style={sidebarStyle}>
        <nav>
          <a href="#" style={navItemStyle}>Dashboard</a>
          <a href="#" style={navItemStyle}>Projects</a>
          <a href="#" style={navItemStyle}>Team</a>
          <a href="#" style={navItemStyle}>Settings</a>
        </nav>
      </aside>
      <main style={mainStyle}>
        <h1 style={getResponsiveText('3xl')}>Main Content</h1>
        <p style={{ ...marginStyles.top(4), lineHeight: typography.lineHeight.relaxed }}>
          This is the main content area that adapts to different screen sizes.
          On mobile devices, the sidebar appears above the content, while on
          larger screens, it's positioned to the left.
        </p>
      </main>
    </div>
  );
};

// Example 4: Flex Layout with Responsive Stacking
export const ResponsiveFeatureSection: React.FC = () => {
  const sectionStyle = mergeStyles(
    containerStyles.base,
    containerStyles.lg,
    paddingStyles.y(16)
  );

  const stackToRowStyle = patterns.stackToSideBySide;

  const contentStyle = {
    flex: '1',
  };

  const imageStyle = {
    flex: '1',
    backgroundColor: '#e5e7eb',
    borderRadius: '0.75rem',
    minHeight: '300px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    color: '#6b7280',
  };

  return (
    <section style={sectionStyle}>
      <div style={stackToRowStyle}>
        <div style={contentStyle}>
          <h2 style={mergeStyles(
            getResponsiveText('3xl'),
            {
              fontWeight: typography.fontWeight.bold,
              marginBottom: spacing[4],
              color: '#1f2937',
            }
          )}>
            Flexible Layout System
          </h2>
          <p style={{
            ...marginStyles.bottom(6),
            lineHeight: typography.lineHeight.relaxed,
            color: '#6b7280',
          }}>
            Our responsive layout system automatically adapts to different screen
            sizes, ensuring your content looks great on all devices. Stack elements
            vertically on mobile and arrange them horizontally on larger screens.
          </p>
          <button style={{
            ...paddingStyles.x(4),
            ...paddingStyles.y(2),
            backgroundColor: '#3b82f6',
            color: 'white',
            border: 'none',
            borderRadius: '0.5rem',
            fontWeight: typography.fontWeight.medium,
            cursor: 'pointer',
          }}>
            Learn More
          </button>
        </div>
        <div style={imageStyle}>
          Image Placeholder
        </div>
      </div>
    </section>
  );
};

// Example 5: Complex Responsive Grid
export const ResponsiveDashboard: React.FC = () => {
  const dashboardStyle = mergeStyles(
    containerStyles.base,
    containerStyles.xl,
    paddingStyles.all(4)
  );

  const headerStyle = {
    ...marginStyles.bottom(8),
  };

  const statsGridStyle = responsive({
    base: gridStyles.container({ base: 1 }),
    sm: gridStyles.container({ sm: 2 }),
    lg: gridStyles.container({ lg: 4 }),
  });

  const statsCardStyle = {
    backgroundColor: 'white',
    ...paddingStyles.all(6),
    borderRadius: '0.5rem',
    boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
    border: '1px solid #e5e7eb',
  };

  const chartAreaStyle = responsive({
    base: {
      ...gridStyles.container({ base: 1 }),
      ...gridStyles.gap(6),
      ...marginStyles.top(8),
    },
    lg: {
      ...gridStyles.container({ lg: 3 }),
      gridTemplateColumns: '2fr 1fr',
    },
  });

  const chartStyle = {
    backgroundColor: 'white',
    ...paddingStyles.all(6),
    borderRadius: '0.5rem',
    boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
    border: '1px solid #e5e7eb',
    minHeight: '300px',
  };

  return (
    <div style={dashboardStyle}>
      <header style={headerStyle}>
        <h1 style={mergeStyles(
          getResponsiveText('3xl'),
          { fontWeight: typography.fontWeight.bold }
        )}>
          Dashboard
        </h1>
      </header>

      {/* Stats Grid */}
      <div style={mergeStyles(statsGridStyle, gridStyles.gap(4))}>
        {['Users', 'Revenue', 'Orders', 'Growth'].map((stat, index) => (
          <div key={index} style={statsCardStyle}>
            <h3 style={{
              fontSize: typography.fontSize.sm.base,
              fontWeight: typography.fontWeight.medium,
              color: '#6b7280',
              marginBottom: spacing[2],
            }}>
              {stat}
            </h3>
            <p style={mergeStyles(
              getResponsiveText('2xl'),
              { fontWeight: typography.fontWeight.bold }
            )}>
              {Math.floor(Math.random() * 1000)}
            </p>
          </div>
        ))}
      </div>

      {/* Chart Area */}
      <div style={chartAreaStyle}>
        <div style={chartStyle}>
          <h3 style={{
            ...marginStyles.bottom(4),
            fontWeight: typography.fontWeight.semibold,
          }}>
            Analytics Chart
          </h3>
          <div style={{
            backgroundColor: '#f3f4f6',
            height: '250px',
            borderRadius: '0.25rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#6b7280',
          }}>
            Chart Placeholder
          </div>
        </div>
        <div style={chartStyle}>
          <h3 style={{
            ...marginStyles.bottom(4),
            fontWeight: typography.fontWeight.semibold,
          }}>
            Recent Activity
          </h3>
          <div style={{
            ...flexStyles.container,
            ...flexStyles.direction.col,
            ...flexStyles.gap(3),
          }}>
            {['User signed up', 'Order completed', 'Payment received'].map((activity, index) => (
              <div key={index} style={{
                ...paddingStyles.all(3),
                backgroundColor: '#f9fafb',
                borderRadius: '0.25rem',
                fontSize: typography.fontSize.sm.base,
              }}>
                {activity}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

// Example 6: Mobile-First Navigation
export const ResponsiveNavigation: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = React.useState(false);

  const navStyle = {
    backgroundColor: 'white',
    boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
    position: 'sticky' as const,
    top: 0,
    zIndex: 50,
  };

  const containerStyle = mergeStyles(
    containerStyles.base,
    containerStyles.xl,
    {
      ...flexStyles.container,
      ...flexStyles.justify.between,
      ...flexStyles.align.center,
      ...paddingStyles.y(4),
    }
  );

  const logoStyle = mergeStyles(
    getResponsiveText('xl'),
    { fontWeight: typography.fontWeight.bold }
  );

  const menuButtonStyle = {
    ...paddingStyles.all(2),
    border: 'none',
    backgroundColor: 'transparent',
    cursor: 'pointer',
    [`@media (min-width: ${breakpoints.md}px)`]: {
      display: 'none',
    },
  };

  const desktopMenuStyle = {
    ...flexStyles.container,
    ...flexStyles.gap(6),
    ...patterns.hideOnMobile,
  };

  const mobileMenuStyle = {
    ...patterns.showOnlyMobile,
    position: 'absolute' as const,
    top: '100%',
    left: 0,
    right: 0,
    backgroundColor: 'white',
    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    ...paddingStyles.all(4),
    display: isMenuOpen ? 'block' : 'none',
  };

  const navLinkStyle = {
    color: '#374151',
    textDecoration: 'none',
    fontWeight: typography.fontWeight.medium,
    ...paddingStyles.y(2),
    display: 'block',
  };

  return (
    <nav style={navStyle}>
      <div style={containerStyle}>
        <div style={logoStyle}>Brand</div>
        
        <button
          style={menuButtonStyle}
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        >
          ☰
        </button>

        <div style={desktopMenuStyle}>
          <a href="#" style={navLinkStyle}>Home</a>
          <a href="#" style={navLinkStyle}>About</a>
          <a href="#" style={navLinkStyle}>Services</a>
          <a href="#" style={navLinkStyle}>Contact</a>
        </div>
      </div>

      <div style={mobileMenuStyle}>
        <a href="#" style={navLinkStyle}>Home</a>
        <a href="#" style={navLinkStyle}>About</a>
        <a href="#" style={navLinkStyle}>Services</a>
        <a href="#" style={navLinkStyle}>Contact</a>
      </div>
    </nav>
  );
};

export default {
  ResponsiveHero,
  ResponsiveCardGrid,
  ResponsiveSidebarLayout,
  ResponsiveFeatureSection,
  ResponsiveDashboard,
  ResponsiveNavigation,
};
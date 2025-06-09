/**
 * Comprehensive demo page showcasing the inline styling system
 * Demonstrates all button variants, states, and accessibility features
 */

import React, { useState } from 'react'
import {
  InlineStyledButton,
  PrimaryButton,
  SecondaryButton,
  SuccessButton,
  WarningButton,
  DangerButton,
  GhostButton,
  LinkButton,
  SmallPrimaryButton,
  LargePrimaryButton,
  IconButton,
  ButtonGroup,
  InlineStyledInput
} from '@/components/ui/InlineStyledButton'
import { colors, spacing, borderRadius } from '@/lib/inline-styles'

// Demo icons (you can replace with your preferred icon library)
const PlayIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
    <path d="M8 5v14l11-7z"/>
  </svg>
)

const DownloadIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
    <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
  </svg>
)

const SearchIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
    <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
  </svg>
)

const HeartIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
  </svg>
)

const InlineStylesDemo: React.FC = () => {
  const [loadingStates, setLoadingStates] = useState<Record<string, boolean>>({})
  const [inputValue, setInputValue] = useState('')

  const toggleLoading = (buttonId: string) => {
    setLoadingStates(prev => ({
      ...prev,
      [buttonId]: !prev[buttonId]
    }))
    
    // Auto-disable loading after 3 seconds
    setTimeout(() => {
      setLoadingStates(prev => ({
        ...prev,
        [buttonId]: false
      }))
    }, 3000)
  }

  const demoSectionStyle: React.CSSProperties = {
    marginBottom: spacing['3xl'],
    padding: spacing.xl,
    border: `1px solid ${colors.neutral.gray200}`,
    borderRadius: borderRadius.lg,
    background: colors.neutral.white,
  }

  const headingStyle: React.CSSProperties = {
    fontSize: '24px',
    fontWeight: 600,
    marginBottom: spacing.xl,
    color: colors.text.primary,
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  }

  const subHeadingStyle: React.CSSProperties = {
    fontSize: '18px',
    fontWeight: 500,
    marginBottom: spacing.lg,
    marginTop: spacing.xl,
    color: colors.text.primary,
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  }

  const descriptionStyle: React.CSSProperties = {
    fontSize: '14px',
    color: colors.text.secondary,
    marginBottom: spacing.lg,
    lineHeight: 1.5,
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  }

  const codeBlockStyle: React.CSSProperties = {
    background: colors.neutral.gray100,
    padding: spacing.md,
    borderRadius: borderRadius.md,
    fontFamily: 'ui-monospace, SFMono-Regular, "SF Mono", Consolas, monospace',
    fontSize: '12px',
    color: colors.text.primary,
    marginTop: spacing.md,
    overflow: 'auto',
  }

  const containerStyle: React.CSSProperties = {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: spacing.xl,
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    background: colors.neutral.gray50,
    minHeight: '100vh',
  }

  return (
    <div style={containerStyle}>
      <h1 style={{ 
        fontSize: '32px', 
        fontWeight: 700, 
        marginBottom: spacing['3xl'],
        textAlign: 'center',
        color: colors.text.primary,
      }}>
        Inline Styling System Demo
      </h1>

      {/* Primary Buttons */}
      <section style={demoSectionStyle}>
        <h2 style={headingStyle}>Primary Buttons</h2>
        <p style={descriptionStyle}>
          Primary buttons use gradient backgrounds and are designed for main actions.
          They include hover effects, focus states, and loading indicators.
        </p>
        
        <ButtonGroup spacing="md">
          <PrimaryButton onClick={() => toggleLoading('primary-1')}>
            Primary Button
          </PrimaryButton>
          <PrimaryButton 
            loading={loadingStates['primary-loading']}
            onClick={() => toggleLoading('primary-loading')}
          >
            {loadingStates['primary-loading'] ? 'Loading...' : 'Click to Load'}
          </PrimaryButton>
          <PrimaryButton disabled>
            Disabled Primary
          </PrimaryButton>
          <PrimaryButton leftIcon={<PlayIcon />}>
            With Icon
          </PrimaryButton>
        </ButtonGroup>

        <h3 style={subHeadingStyle}>Sizes</h3>
        <ButtonGroup spacing="md">
          <InlineStyledButton variant="primary" size="xs">Extra Small</InlineStyledButton>
          <InlineStyledButton variant="primary" size="sm">Small</InlineStyledButton>
          <InlineStyledButton variant="primary" size="md">Medium</InlineStyledButton>
          <InlineStyledButton variant="primary" size="lg">Large</InlineStyledButton>
          <InlineStyledButton variant="primary" size="xl">Extra Large</InlineStyledButton>
        </ButtonGroup>

        <div style={codeBlockStyle}>
          {`<PrimaryButton onClick={handleClick}>Primary Button</PrimaryButton>
<PrimaryButton loading={isLoading}>Loading Button</PrimaryButton>
<PrimaryButton disabled>Disabled Button</PrimaryButton>`}
        </div>
      </section>

      {/* Secondary Buttons */}
      <section style={demoSectionStyle}>
        <h2 style={headingStyle}>Secondary Buttons</h2>
        <p style={descriptionStyle}>
          Secondary buttons use borders and subtle backgrounds for secondary actions.
        </p>
        
        <ButtonGroup spacing="md">
          <SecondaryButton>Secondary Button</SecondaryButton>
          <SecondaryButton 
            loading={loadingStates['secondary-loading']}
            onClick={() => toggleLoading('secondary-loading')}
          >
            {loadingStates['secondary-loading'] ? 'Loading...' : 'Click to Load'}
          </SecondaryButton>
          <SecondaryButton disabled>Disabled Secondary</SecondaryButton>
          <SecondaryButton rightIcon={<DownloadIcon />}>
            Download
          </SecondaryButton>
        </ButtonGroup>

        <div style={codeBlockStyle}>
          {`<SecondaryButton onClick={handleClick}>Secondary Button</SecondaryButton>
<SecondaryButton rightIcon={<DownloadIcon />}>Download</SecondaryButton>`}
        </div>
      </section>

      {/* Variant Buttons */}
      <section style={demoSectionStyle}>
        <h2 style={headingStyle}>Semantic Variants</h2>
        <p style={descriptionStyle}>
          Semantic button variants for different contexts and meanings.
        </p>
        
        <ButtonGroup spacing="md">
          <SuccessButton>Success</SuccessButton>
          <WarningButton>Warning</WarningButton>
          <DangerButton>Danger</DangerButton>
        </ButtonGroup>

        <h3 style={subHeadingStyle}>With Loading States</h3>
        <ButtonGroup spacing="md">
          <SuccessButton 
            loading={loadingStates['success-loading']}
            onClick={() => toggleLoading('success-loading')}
          >
            Save Changes
          </SuccessButton>
          <WarningButton 
            loading={loadingStates['warning-loading']}
            onClick={() => toggleLoading('warning-loading')}
          >
            Proceed with Caution
          </WarningButton>
          <DangerButton 
            loading={loadingStates['danger-loading']}
            onClick={() => toggleLoading('danger-loading')}
          >
            Delete Item
          </DangerButton>
        </ButtonGroup>

        <div style={codeBlockStyle}>
          {`<SuccessButton>Save Changes</SuccessButton>
<WarningButton>Proceed with Caution</WarningButton>
<DangerButton>Delete Item</DangerButton>`}
        </div>
      </section>

      {/* Ghost and Link Buttons */}
      <section style={demoSectionStyle}>
        <h2 style={headingStyle}>Ghost and Link Buttons</h2>
        <p style={descriptionStyle}>
          Minimal styling for subtle actions and navigation.
        </p>
        
        <ButtonGroup spacing="md">
          <GhostButton>Ghost Button</GhostButton>
          <GhostButton disabled>Disabled Ghost</GhostButton>
          <LinkButton>Link Button</LinkButton>
          <LinkButton disabled>Disabled Link</LinkButton>
        </ButtonGroup>

        <div style={codeBlockStyle}>
          {`<GhostButton>Ghost Button</GhostButton>
<LinkButton>Link Button</LinkButton>`}
        </div>
      </section>

      {/* Icon Buttons */}
      <section style={demoSectionStyle}>
        <h2 style={headingStyle}>Icon Buttons</h2>
        <p style={descriptionStyle}>
          Square buttons designed for icons and compact interfaces.
        </p>
        
        <ButtonGroup spacing="md">
          <IconButton aria-label="Search">
            <SearchIcon />
          </IconButton>
          <IconButton aria-label="Favorite">
            <HeartIcon />
          </IconButton>
          <IconButton disabled aria-label="Disabled">
            <PlayIcon />
          </IconButton>
          <IconButton 
            loading={loadingStates['icon-loading']}
            onClick={() => toggleLoading('icon-loading')}
            aria-label="Loading"
          >
            {!loadingStates['icon-loading'] && <DownloadIcon />}
          </IconButton>
        </ButtonGroup>

        <div style={codeBlockStyle}>
          {`<IconButton aria-label="Search">
  <SearchIcon />
</IconButton>`}
        </div>
      </section>

      {/* Button Groups */}
      <section style={demoSectionStyle}>
        <h2 style={headingStyle}>Button Groups</h2>
        <p style={descriptionStyle}>
          Organized button layouts with consistent spacing.
        </p>
        
        <h3 style={subHeadingStyle}>Horizontal Group</h3>
        <ButtonGroup spacing="md" orientation="horizontal">
          <PrimaryButton>Primary</PrimaryButton>
          <SecondaryButton>Secondary</SecondaryButton>
          <GhostButton>Cancel</GhostButton>
        </ButtonGroup>

        <h3 style={subHeadingStyle}>Vertical Group</h3>
        <ButtonGroup spacing="sm" orientation="vertical" style={{ maxWidth: '200px' }}>
          <PrimaryButton fullWidth>Full Width Primary</PrimaryButton>
          <SecondaryButton fullWidth>Full Width Secondary</SecondaryButton>
          <GhostButton fullWidth>Full Width Ghost</GhostButton>
        </ButtonGroup>

        <div style={codeBlockStyle}>
          {`<ButtonGroup spacing="md" orientation="horizontal">
  <PrimaryButton>Primary</PrimaryButton>
  <SecondaryButton>Secondary</SecondaryButton>
  <GhostButton>Cancel</GhostButton>
</ButtonGroup>`}
        </div>
      </section>

      {/* Input Fields */}
      <section style={demoSectionStyle}>
        <h2 style={headingStyle}>Input Fields</h2>
        <p style={descriptionStyle}>
          Consistent input styling with icon support and validation states.
        </p>
        
        <div style={{ display: 'grid', gap: spacing.lg, maxWidth: '400px' }}>
          <InlineStyledInput
            placeholder="Basic input"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
          />
          
          <InlineStyledInput
            placeholder="Search..."
            leftIcon={<SearchIcon />}
          />
          
          <InlineStyledInput
            placeholder="Input with error"
            error={true}
            rightIcon={<HeartIcon />}
          />
          
          <InlineStyledInput
            placeholder="Disabled input"
            disabled={true}
            leftIcon={<SearchIcon />}
          />
        </div>

        <div style={codeBlockStyle}>
          {`<InlineStyledInput
  placeholder="Search..."
  leftIcon={<SearchIcon />}
/>
<InlineStyledInput
  placeholder="Input with error"
  error={true}
/>`}
        </div>
      </section>

      {/* Accessibility Features */}
      <section style={demoSectionStyle}>
        <h2 style={headingStyle}>Accessibility Features</h2>
        <p style={descriptionStyle}>
          All components include proper ARIA attributes, keyboard navigation, and focus management.
        </p>
        
        <ul style={{ 
          listStyle: 'disc',
          paddingLeft: spacing.xl,
          color: colors.text.secondary,
          lineHeight: 1.6
        }}>
          <li>Proper focus indicators with high contrast outlines</li>
          <li>ARIA attributes for screen readers (aria-disabled, aria-busy, aria-label)</li>
          <li>Keyboard navigation support</li>
          <li>Color contrast ratios meet WCAG guidelines</li>
          <li>Loading states with proper accessibility feedback</li>
          <li>Semantic HTML structure</li>
        </ul>

        <h3 style={subHeadingStyle}>Try Tab Navigation</h3>
        <p style={descriptionStyle}>
          Use Tab key to navigate through these buttons and see the focus indicators:
        </p>
        <ButtonGroup spacing="md">
          <PrimaryButton>Tab 1</PrimaryButton>
          <SecondaryButton>Tab 2</SecondaryButton>
          <SuccessButton>Tab 3</SuccessButton>
          <GhostButton>Tab 4</GhostButton>
        </ButtonGroup>
      </section>

      {/* Usage Examples */}
      <section style={demoSectionStyle}>
        <h2 style={headingStyle}>Usage Examples</h2>
        <p style={descriptionStyle}>
          Common patterns and implementations using the inline styling system.
        </p>
        
        <h3 style={subHeadingStyle}>Form Actions</h3>
        <ButtonGroup spacing="md">
          <PrimaryButton type="submit">Save Changes</PrimaryButton>
          <SecondaryButton type="button">Cancel</SecondaryButton>
        </ButtonGroup>

        <h3 style={subHeadingStyle}>Card Actions</h3>
        <div style={{
          background: colors.neutral.white,
          border: `1px solid ${colors.neutral.gray200}`,
          borderRadius: borderRadius.lg,
          padding: spacing.xl,
          marginTop: spacing.md,
        }}>
          <h4 style={{ marginBottom: spacing.md, color: colors.text.primary }}>
            Project Card
          </h4>
          <p style={{ marginBottom: spacing.lg, color: colors.text.secondary }}>
            This is a sample project card with action buttons.
          </p>
          <ButtonGroup spacing="sm">
            <SmallPrimaryButton>View Details</SmallPrimaryButton>
            <InlineStyledButton variant="ghost" size="sm">
              Share
            </InlineStyledButton>
            <IconButton aria-label="More options">
              <HeartIcon />
            </IconButton>
          </ButtonGroup>
        </div>

        <div style={codeBlockStyle}>
          {`// Form actions
<ButtonGroup spacing="md">
  <PrimaryButton type="submit">Save Changes</PrimaryButton>
  <SecondaryButton type="button">Cancel</SecondaryButton>
</ButtonGroup>

// Card actions
<ButtonGroup spacing="sm">
  <SmallPrimaryButton>View Details</SmallPrimaryButton>
  <GhostButton size="sm">Share</GhostButton>
  <IconButton aria-label="More options">
    <MoreIcon />
  </IconButton>
</ButtonGroup>`}
        </div>
      </section>
    </div>
  )
}

export default InlineStylesDemo
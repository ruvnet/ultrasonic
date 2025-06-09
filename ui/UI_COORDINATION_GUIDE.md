# UI Development Coordination Guide for Ultrasonic-Agentics

## Overview
This coordination system enables efficient collaboration on the Ultrasonic-Agentics UI, a React/TypeScript/Vite application that provides the frontend interface for the steganography framework.

## Directory Structure
```
ui/
├── UI_COORDINATION_GUIDE.md       # This file - UI-specific coordination guide
├── coordination/                  # UI development coordination
│   ├── components/               # Component development tracking
│   │   ├── audio-controls.md    # Audio player/recorder components
│   │   ├── waveform-display.md  # Signal visualization components
│   │   ├── encoding-panel.md    # Message encoding interface
│   │   └── decoding-panel.md    # Message decoding interface
│   ├── features/                 # Feature implementation plans
│   │   ├── real-time-encoding.md   # Live audio encoding feature
│   │   ├── file-processing.md      # Batch file processing
│   │   ├── signal-analysis.md      # Audio signal analysis tools
│   │   └── api-integration.md      # Backend API integration
│   ├── design/                   # Design decisions and patterns
│   │   ├── component-architecture.md  # Component structure decisions
│   │   ├── state-management.md       # Zustand store architecture
│   │   ├── ui-patterns.md            # Reusable UI patterns
│   │   └── theme-system.md           # Tailwind theming approach
│   └── integration/              # Backend integration points
│       ├── api-contracts.md      # API endpoint specifications
│       ├── websocket-events.md   # Real-time communication
│       ├── data-models.md        # TypeScript interfaces
│       └── error-handling.md     # Error handling strategies
```

## UI-Specific Development Workflow

### 1. Component Development Process
1. **Planning Phase**
   - Check `coordination/components/` for existing work
   - Create/update component specification in relevant `.md` file
   - Define props interface and state requirements

2. **Implementation Phase**
   - Follow atomic design principles (atoms → molecules → organisms)
   - Use TypeScript strict mode for type safety
   - Implement with accessibility (a11y) in mind

3. **Testing Phase**
   - Write Vitest unit tests for logic
   - Add React Testing Library tests for interactions
   - Ensure responsive design across breakpoints

### 2. State Management Approach

#### Zustand Store Structure
```typescript
// stores/ultrasonicStore.ts
interface UltrasonicState {
  // Audio state
  audioContext: AudioContext | null
  currentAudio: AudioBuffer | null
  isProcessing: boolean
  
  // Encoding state
  encodingSettings: EncodingSettings
  messageToEncode: string
  
  // Decoding state
  decodedMessage: string | null
  confidence: number
  
  // Actions
  actions: {
    initializeAudio: () => void
    encodeMessage: (message: string, audio: File) => Promise<void>
    decodeAudio: (audio: File) => Promise<void>
  }
}
```

#### State Management Rules
1. **Local Component State**: Use for UI-only state (modals, form inputs)
2. **Zustand Store**: Use for shared state and business logic
3. **React Query**: Use for server state and caching (if needed)

### 3. Component Architecture Decisions

#### Folder Structure
```
src/
├── components/
│   ├── common/              # Shared UI components
│   │   ├── Button/
│   │   ├── Card/
│   │   └── Modal/
│   ├── audio/              # Audio-specific components
│   │   ├── AudioPlayer/
│   │   ├── WaveformVisualizer/
│   │   └── FrequencyAnalyzer/
│   ├── encoding/           # Encoding feature components
│   │   ├── MessageInput/
│   │   ├── SettingsPanel/
│   │   └── EncodeButton/
│   └── decoding/           # Decoding feature components
│       ├── AudioUploader/
│       ├── DecodingProgress/
│       └── ResultDisplay/
├── hooks/                  # Custom React hooks
│   ├── useAudioContext.ts
│   ├── useWebSocket.ts
│   └── useUltrasonicApi.ts
├── services/              # API and external services
│   ├── api/
│   │   ├── client.ts
│   │   ├── encoding.ts
│   │   └── decoding.ts
│   └── audio/
│       ├── processor.ts
│       └── analyzer.ts
├── stores/                # Zustand stores
│   └── ultrasonicStore.ts
├── types/                 # TypeScript type definitions
│   ├── api.types.ts
│   ├── audio.types.ts
│   └── ui.types.ts
└── utils/                 # Utility functions
    ├── audio.utils.ts
    ├── validation.utils.ts
    └── format.utils.ts
```

### 4. Integration Points with Backend

#### API Endpoints
```typescript
// Base URL: http://localhost:8000/api

// Encoding endpoints
POST   /encode/audio     - Encode message into audio file
POST   /encode/realtime  - Start real-time encoding session

// Decoding endpoints
POST   /decode/audio     - Decode message from audio file
POST   /decode/realtime  - Start real-time decoding session

// Configuration endpoints
GET    /config/defaults  - Get default encoding parameters
POST   /config/validate  - Validate encoding configuration

// WebSocket endpoints
WS     /ws/encode        - Real-time encoding stream
WS     /ws/decode        - Real-time decoding stream
```

#### Data Flow Architecture
```
UI Component → Hook → API Service → Backend
     ↓           ↓          ↓          ↓
Local State  Zustand   Transform   Response
     ↓           ↓          ↓          ↓
   Render    Global    Validate    Update
            State               Global State
```

### 5. Testing Strategies

#### Component Testing Hierarchy
1. **Unit Tests** (Vitest)
   - Utility functions
   - Custom hooks
   - Store actions

2. **Component Tests** (React Testing Library)
   - User interactions
   - Accessibility
   - Error states

3. **Integration Tests**
   - API integration
   - Full user flows
   - Error handling

#### Test File Structure
```
component/
├── Component.tsx
├── Component.test.tsx      # Unit/component tests
├── Component.stories.tsx   # Storybook stories (if using)
└── Component.module.css    # Styles (if not using Tailwind exclusively)
```

### 6. Design System Documentation

#### Color Palette
```css
/* Tailwind config extension */
colors: {
  ultrasonic: {
    50:  '#f0f9ff',  /* Lightest blue */
    100: '#e0f2fe',
    200: '#bae6fd',
    300: '#7dd3fc',
    400: '#38bdf8',  /* Primary */
    500: '#0ea5e9',
    600: '#0284c7',
    700: '#0369a1',
    800: '#075985',
    900: '#0c4a6e',  /* Darkest blue */
  },
  signal: {
    low:    '#10b981',  /* Green - Good signal */
    medium: '#f59e0b',  /* Amber - Average signal */
    high:   '#ef4444',  /* Red - Poor signal */
  }
}
```

#### Component Variants
```typescript
// Button variants
type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'danger'
type ButtonSize = 'sm' | 'md' | 'lg'

// Card variants
type CardVariant = 'default' | 'bordered' | 'elevated'

// Input variants
type InputVariant = 'default' | 'filled' | 'error'
```

## Communication Standards

### Status Markers (UI-Specific)
- 🎨 DESIGN - In design/planning phase
- 🏗️ BUILD - Component being built
- 🧪 TEST - Writing/running tests
- ✅ READY - Component complete and tested
- 🔄 REFACTOR - Improving existing component
- 🐛 BUG - Fixing issues

### Update Format
```markdown
## [Timestamp] Component: [ComponentName]
**Developer**: [Name/ID]
**Status**: [Status marker]
**Changes**: [What was implemented/changed]
**Props**: [New/changed props interface]
**Tests**: [Test coverage status]
**Next**: [What needs to happen next]
```

## UI Development Rules

1. **TypeScript First** - All components must be properly typed
2. **Accessibility Always** - WCAG 2.1 AA compliance minimum
3. **Mobile Responsive** - Test on mobile viewports first
4. **Performance Matters** - Lazy load heavy components
5. **Consistent Styling** - Use Tailwind utilities, avoid inline styles
6. **Error Boundaries** - Wrap feature components in error boundaries
7. **Loading States** - Always show loading feedback
8. **Empty States** - Design for when there's no data
9. **Error Messages** - User-friendly, actionable error messages
10. **Documentation** - Props documentation and usage examples

## Quick Start for New Features

1. **Create Feature Plan**
   ```bash
   touch ui/coordination/features/new-feature.md
   ```

2. **Define Component Structure**
   ```bash
   mkdir -p ui/src/components/new-feature
   touch ui/src/components/new-feature/NewFeature.tsx
   touch ui/src/components/new-feature/NewFeature.test.tsx
   ```

3. **Add to Coordination**
   - Update relevant coordination files
   - Define API contracts if needed
   - Plan state management approach

4. **Implement with TDD**
   - Write tests first
   - Implement component
   - Connect to store/API
   - Add to routing

## Integration Checklist

- [ ] TypeScript interfaces defined
- [ ] API endpoints documented
- [ ] Error handling implemented
- [ ] Loading states added
- [ ] Tests written and passing
- [ ] Accessibility checked
- [ ] Responsive design verified
- [ ] Documentation updated
- [ ] Code reviewed

## Resources

- [React Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/guide/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Zustand Documentation](https://docs.pmnd.rs/zustand/getting-started/introduction)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)
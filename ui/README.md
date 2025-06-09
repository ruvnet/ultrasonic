# Ultrasonic Agentics UI

A modern, responsive web application for the Agentic Commands Steganography framework built with Vite, React, TypeScript, and shadcn/ui.

## 🚀 Features

- **Modern Tech Stack**: Vite + React 18 + TypeScript
- **Beautiful UI**: shadcn/ui components with Tailwind CSS
- **Authentication**: Supabase auth with protected routes
- **Mock API**: MSW for development without backend
- **TDD Approach**: Vitest + React Testing Library
- **Responsive Design**: Mobile-first approach
- **Dark/Light Mode**: System preference aware

## 📋 Prerequisites

- Node.js 18+ and npm
- Supabase account (for authentication)
- Basic knowledge of React and TypeScript

## 🛠️ Installation

1. **Clone the repository**
```bash
cd ui
```

2. **Install dependencies**
```bash
npm install
```

3. **Set up environment variables**
```bash
cp .env.example .env.local
# Edit .env.local with your Supabase credentials
```

4. **Start development server**
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## 🧪 Testing

Run tests with Vitest:

```bash
# Run tests
npm test

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage
```

## 🏗️ Project Structure

```
ui/
├── src/
│   ├── components/     # Reusable components
│   │   ├── ui/        # shadcn/ui components
│   │   ├── auth/      # Authentication components
│   │   ├── layouts/   # Layout components
│   │   └── ...
│   ├── pages/         # Page components
│   │   ├── auth/      # Authentication pages
│   │   ├── dashboard/ # Dashboard pages
│   │   ├── settings/  # Settings pages
│   │   └── help/      # Help pages
│   ├── lib/           # Utility libraries
│   │   ├── api/       # API client
│   │   ├── supabase/  # Supabase configuration
│   │   └── utils.ts   # Helper functions
│   ├── stores/        # State management (Zustand)
│   ├── types/         # TypeScript types
│   ├── mocks/         # MSW mock handlers
│   └── test/          # Test utilities
├── public/            # Static assets
└── ...config files
```

## 🎨 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm test` - Run tests
- `npm run test:ui` - Run tests with UI
- `npm run test:coverage` - Run tests with coverage
- `npm run type-check` - Run TypeScript type checking

## 🔧 Configuration

### Environment Variables

```env
# Supabase
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key

# API
VITE_API_URL=http://localhost:8000
VITE_API_TIMEOUT=30000

# Features
VITE_ENABLE_MOCK_API=true
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_DEBUG=true
```

### Mock API

The app uses MSW (Mock Service Worker) for API mocking in development. Set `VITE_ENABLE_MOCK_API=true` to enable it.

## 📱 Features Overview

### Authentication
- Email/password login and registration
- Password reset functionality
- Session management
- Protected routes

### Dashboard
- Overview with statistics
- Quick action cards
- System status indicator
- Recent operations

### Steganography Operations
- **Embed**: Upload audio/video files and embed commands
- **Decode**: Extract hidden commands from files
- **Analyze**: Detect steganographic content
- **History**: View past operations

### Settings
- Profile management
- Security settings
- Frequency configuration
- User preferences

### Help Center
- API documentation
- Tutorials
- FAQ
- Support resources

## 🚀 Production Build

1. **Build the app**
```bash
npm run build
```

2. **Preview locally**
```bash
npm run preview
```

3. **Deploy**
The `dist` folder contains the production build ready for deployment.

### Deployment Options
- **Vercel**: `npx vercel`
- **Netlify**: Drop the `dist` folder
- **Docker**: Use the provided Dockerfile
- **Traditional hosting**: Upload `dist` contents

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Ensure all tests pass (`npm test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [shadcn/ui](https://ui.shadcn.com/) for the beautiful components
- [Vite](https://vitejs.dev/) for the blazing fast build tool
- [Tailwind CSS](https://tailwindcss.com/) for the utility-first CSS framework
- [Supabase](https://supabase.com/) for authentication and database
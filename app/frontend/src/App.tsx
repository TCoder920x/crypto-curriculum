import { Routes, Route, Navigate } from 'react-router-dom'
import { Suspense, lazy } from 'react'
import { Box } from '@mui/material'
import { ThemeContextProvider, useThemeMode } from './contexts/ThemeContext'
import { ProtectedRoute } from './components/auth/ProtectedRoute'
import { Navigation } from './components/layout/Navigation'
import { Sidebar } from './components/layout/Sidebar'
import { Footer } from './components/layout/Footer'
import { PageSkeleton } from './components/common/LoadingSkeleton'
import { LoginPage } from './pages/LoginPage'
import { RegisterPage } from './pages/RegisterPage'
import './App.css'

// Lazy load page components for code splitting
const HomePage = lazy(() => import('./pages/HomePage').then(m => ({ default: m.HomePage })))
const ModulesListPage = lazy(() => import('./pages/ModulesListPage').then(m => ({ default: m.ModulesListPage })))
const AssessmentsListPage = lazy(() => import('./pages/AssessmentsListPage').then(m => ({ default: m.AssessmentsListPage })))
const ModulePage = lazy(() => import('./pages/ModulePage').then(m => ({ default: m.ModulePage })))
const AssessmentPage = lazy(() => import('./pages/AssessmentPage').then(m => ({ default: m.AssessmentPage })))
const ProgressPage = lazy(() => import('./pages/ProgressPage').then(m => ({ default: m.ProgressPage })))
const ProfileSettingsPage = lazy(() => import('./pages/ProfileSettingsPage').then(m => ({ default: m.ProfileSettingsPage })))
const InstructorDashboardPage = lazy(() => import('./pages/InstructorDashboardPage').then(m => ({ default: m.InstructorDashboardPage })))
const CohortsPage = lazy(() => import('./pages/CohortsPage').then(m => ({ default: m.CohortsPage })))
const ForumPage = lazy(() => import('./pages/ForumPage').then(m => ({ default: m.ForumPage })))
const ForumPostPage = lazy(() => import('./pages/ForumPostPage').then(m => ({ default: m.ForumPostPage })))
const AIAssistantPage = lazy(() => import('./pages/AIAssistantPage').then(m => ({ default: m.AIAssistantPage })))
const AccessibilityPage = lazy(() => import('./pages/AccessibilityPage').then(m => ({ default: m.AccessibilityPage })))

function AppContent() {
  const { mode } = useThemeMode();
  const backgroundColor = mode === 'light' ? '#f8f9fa' : '#0a0e27';

  return (
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route
          path="/*"
          element={
            <ProtectedRoute>
            <Box sx={{ minHeight: '100vh', backgroundColor, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
                <a href="#main-content" className="skip-nav-link">Skip to main content</a>
                <Navigation />
                <Box sx={{ flexGrow: 1, minWidth: 0, overflow: 'hidden', position: 'relative' }}>
                  <Sidebar />
                  <Box 
                    sx={{ 
                      flexGrow: 1, 
                      display: 'flex', 
                      flexDirection: 'column', 
                      minWidth: 0,
                      overflowY: 'auto',
                      overflowX: 'hidden',
                      height: 'calc(100vh - 64px)',
                      position: 'relative',
                      width: { xs: '100%', md: 'calc(100% - 240px)' },
                      ml: { xs: 0, md: '240px' },
                    }}
                  >
                    <Box id="main-content" sx={{ flexGrow: 1, pb: 4 }} role="main">
                      <Suspense fallback={<PageSkeleton />}>
                      <Routes>
                        <Route path="/" element={<HomePage />} />
                        <Route path="/modules" element={<ModulesListPage />} />
                        <Route path="/assessments" element={<AssessmentsListPage />} />
                        <Route path="/progress" element={<ProgressPage />} />
                        <Route path="/profile" element={<ProfileSettingsPage />} />
                        <Route path="/settings" element={<ProfileSettingsPage />} />
                        <Route path="/instructor" element={<InstructorDashboardPage />} />
                        <Route path="/cohorts" element={<CohortsPage />} />
                        <Route path="/modules/:moduleId" element={<ModulePage />} />
                        <Route path="/modules/:moduleId/assessments" element={<AssessmentPage />} />
                        <Route path="/modules/:moduleId/forums" element={<ForumPage />} />
                        <Route path="/modules/:moduleId/forums/posts/:postId" element={<ForumPostPage />} />
                        <Route path="/ai-assistant" element={<AIAssistantPage />} />
                          <Route path="/accessibility" element={<AccessibilityPage />} />
                        <Route path="*" element={<Navigate to="/" replace />} />
                      </Routes>
                      </Suspense>
                    </Box>
                    <Footer />
                  </Box>
                </Box>
              </Box>
            </ProtectedRoute>
          }
        />
      </Routes>
  )
}

function App() {
  return (
    <ThemeContextProvider>
      <AppContent />
    </ThemeContextProvider>
  )
}

export default App

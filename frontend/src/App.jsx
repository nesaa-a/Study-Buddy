import React, { useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/auth/ProtectedRoute';
import Navbar from './components/layout/Navbar';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import Dashboard from './components/dashboard/Dashboard';
import { studyAPI } from './services/api';

function App() {
  useEffect(() => {
    let stopped = false;

    // Try immediate heartbeat if token is present now
    if (localStorage.getItem('access_token')) {
      studyAPI.heartbeat().catch(() => {});
    }

    // Every 60s, if token exists, send heartbeat
    const id = setInterval(() => {
      if (stopped) return;
      if (localStorage.getItem('access_token')) {
        studyAPI.heartbeat().catch(() => {});
      }
    }, 60000);

    const handleUnload = () => {
      try {
        const blob = new Blob([JSON.stringify({})], { type: 'application/json' });
        navigator.sendBeacon('/api/study/heartbeat', blob);
      } catch {}
    };
    window.addEventListener('beforeunload', handleUnload);

    return () => {
      stopped = true;
      clearInterval(id);
      window.removeEventListener('beforeunload', handleUnload);
    };
  }, []);

  return (
    <AuthProvider>
      <div className="App">
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          {/* Protected Routes */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Navbar />
                <Dashboard />
              </ProtectedRoute>
            }
          />
          
          {/* Redirect root to dashboard */}
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          
          {/* Catch all route */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </div>
    </AuthProvider>
  );
}

export default App;

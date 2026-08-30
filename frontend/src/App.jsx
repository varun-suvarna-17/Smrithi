import React from 'react';
import { Routes, Route, useLocation } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';

import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import OfflineIndicator from './components/OfflineIndicator';

import LoginSignup from './pages/LoginSignup';
import Home from './pages/Home';
import DailyCare from './pages/DailyCare';
import Games from './pages/Games';
import ActivityHub from './pages/ActivityHub';
import Memories from './pages/Memories';
import CaregiverDashboard from './pages/CaregiverDashboard';

export default function App() {
  const location = useLocation();

  return (
    <>
      <OfflineIndicator />

      <Routes location={location} key={location.pathname}>
        {/* Public route — no layout */}
        <Route path="/login-signup" element={<LoginSignup />} />

        {/* Protected routes — with layout */}
        <Route
          path="*"
          element={
            <ProtectedRoute>
              <Layout>
                <AnimatePresence mode="wait">
                  <Routes location={location} key={location.pathname}>
                    <Route path="/" element={<PageTransition><Home /></PageTransition>} />
                    <Route path="/schedule" element={<PageTransition><DailyCare /></PageTransition>} />
                    <Route path="/games" element={<PageTransition><Games /></PageTransition>} />
                    <Route path="/activities" element={<PageTransition><ActivityHub /></PageTransition>} />
                    <Route path="/memories" element={<PageTransition><Memories /></PageTransition>} />
                    <Route path="/caregiver" element={<PageTransition><CaregiverDashboard /></PageTransition>} />
                  </Routes>
                </AnimatePresence>
              </Layout>
            </ProtectedRoute>
          }
        />
      </Routes>
    </>
  );
}

// Reusable transition wrapper
function PageTransition({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={{ duration: 0.2, ease: "easeInOut" }}
      style={{ width: '100%', height: '100%' }}
    >
      {children}
    </motion.div>
  );
}

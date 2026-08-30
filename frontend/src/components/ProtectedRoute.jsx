import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../firebase/useAuth';

/**
 * ProtectedRoute — wraps a component and redirects to login if not authenticated
 * Also shows a loading spinner while auth state is being determined
 */
export default function ProtectedRoute({ children }) {
  const { currentUser, authLoading } = useAuth();

  if (authLoading) {
    return (
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '100vh',
          backgroundColor: 'var(--bg-color, #eaf5ea)',
        }}
      >
        <div
          style={{
            textAlign: 'center',
          }}
        >
          <div
            style={{
              display: 'inline-block',
              width: '40px',
              height: '40px',
              border: '4px solid var(--border-color, #d2ebd4)',
              borderTop: '4px solid var(--primary-green, #1e6535)',
              borderRadius: '50%',
              animation: 'spin 1s linear infinite',
            }}
          />
          <p
            style={{
              marginTop: '16px',
              color: 'var(--text-muted, #526356)',
              fontSize: '14px',
            }}
          >
            Loading...
          </p>
        </div>
      </div>
    );
  }

  if (!currentUser) {
    return <Navigate to="/login-signup" replace />;
  }

  return children;
}

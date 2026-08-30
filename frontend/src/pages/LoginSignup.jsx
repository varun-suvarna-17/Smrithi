import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../firebase/useAuth';
import { registerWithEmail, loginWithEmail } from '../firebase/auth';
import { AlertCircle, Eye, EyeOff, Loader } from 'lucide-react';
import '../styles/LoginSignup.css';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export default function LoginSignup() {
  const navigate = useNavigate();
  const { currentUser } = useAuth();
  const [activeTab, setActiveTab] = useState('login'); // 'login' or 'signup'
  const [isLoading, setIsLoading] = useState(false);

  // Login form state
  const [loginEmail, setLoginEmail] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  const [loginErrors, setLoginErrors] = useState({});
  const [showLoginPassword, setShowLoginPassword] = useState(false);

  // Signup form state
  const [signupEmail, setSignupEmail] = useState('');
  const [signupPassword, setSignupPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [role, setRole] = useState('patient');
  const [phone, setPhone] = useState('');
  const [signupErrors, setSignupErrors] = useState({});
  const [showSignupPassword, setShowSignupPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  // Redirect if already logged in
  React.useEffect(() => {
    if (currentUser) {
      navigate('/');
    }
  }, [currentUser, navigate]);

  // Firebase error message mapping
  const getFirebaseErrorMessage = (errorCode) => {
    const errorMap = {
      'auth/email-already-in-use': 'This email is already registered. Please log in instead.',
      'auth/invalid-email': 'Please enter a valid email address.',
      'auth/weak-password': 'Password must be at least 6 characters long.',
      'auth/user-not-found': 'No account found with this email address.',
      'auth/wrong-password': 'Incorrect password. Please try again.',
      'auth/too-many-requests': 'Too many failed attempts. Please try again later.',
      'auth/operation-not-allowed': 'This operation is not allowed. Please contact support.',
    };
    return errorMap[errorCode] || 'An authentication error occurred. Please try again.';
  };

  // Login validation
  const validateLogin = () => {
    const errors = {};
    if (!loginEmail.trim()) {
      errors.email = 'Email is required.';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(loginEmail)) {
      errors.email = 'Please enter a valid email address.';
    }
    if (!loginPassword) {
      errors.password = 'Password is required.';
    }
    return errors;
  };

  // Signup validation
  const validateSignup = () => {
    const errors = {};
    if (!signupEmail.trim()) {
      errors.email = 'Email is required.';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(signupEmail)) {
      errors.email = 'Please enter a valid email address.';
    }
    if (!signupPassword) {
      errors.password = 'Password is required.';
    } else if (signupPassword.length < 6) {
      errors.password = 'Password must be at least 6 characters.';
    }
    if (!confirmPassword) {
      errors.confirmPassword = 'Please confirm your password.';
    } else if (confirmPassword !== signupPassword) {
      errors.confirmPassword = 'Passwords do not match.';
    }
    if (!fullName.trim()) {
      errors.fullName = 'Full name is required.';
    }
    if (role === 'caregiver' && !phone.trim()) {
      errors.phone = 'Phone is required for caregivers.';
    } else if (phone && !/^\d{10}$/.test(phone.replace(/\D/g, ''))) {
      errors.phone = 'Please enter a valid 10-digit phone number.';
    }
    return errors;
  };

  // Handle login
  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    const errors = validateLogin();
    setLoginErrors(errors);

    if (Object.keys(errors).length > 0) {
      return;
    }

    setIsLoading(true);
    try {
      await loginWithEmail(loginEmail, loginPassword);
      navigate('/');
    } catch (error) {
      setLoginErrors({
        submit: getFirebaseErrorMessage(error.code),
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Handle signup
  const handleSignupSubmit = async (e) => {
    e.preventDefault();
    const errors = validateSignup();
    setSignupErrors(errors);

    if (Object.keys(errors).length > 0) {
      return;
    }

    setIsLoading(true);
    try {
      // Create Firebase user
      const userCredential = await registerWithEmail(signupEmail, signupPassword);
      const userId = userCredential.user.uid;

      // Create backend record (patient or caregiver)
      const backendData =
        role === 'patient'
          ? {
              name: fullName,
              age: 65, // TODO: get from form if needed
              gender: 'Other',
              dementia_stage: 'Early Stage',
              preferred_language: 'en',
              caregiver_id: null,
            }
          : {
              name: fullName,
              relationship: 'Primary Caregiver',
              phone: phone.replace(/\D/g, ''),
              email: signupEmail,
              user_id: userId,
            };

      const endpoint =
        role === 'patient' ? `${API_BASE_URL}/api/patients/` : `${API_BASE_URL}/api/caregivers/`;
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(backendData),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Failed to create profile on backend');
      }

      // Signup successful, redirect to dashboard
      navigate('/');
    } catch (error) {
      const errorMessage = error.code
        ? getFirebaseErrorMessage(error.code)
        : error.message || 'Signup failed. Please try again.';

      setSignupErrors({
        submit: errorMessage,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-signup-container">
      <div className="login-signup-card">
        <div className="login-signup-header">
          <h1 className="login-signup-title">SMRITHI</h1>
          <p className="login-signup-subtitle">Your caring cognitive companion</p>
        </div>

        {/* Tab Toggle */}
        <div className="login-signup-tabs">
          <button
            type="button"
            className={`tab-button ${activeTab === 'login' ? 'active' : ''}`}
            onClick={() => {
              setActiveTab('login');
              setLoginErrors({});
            }}
          >
            Log In
          </button>
          <button
            type="button"
            className={`tab-button ${activeTab === 'signup' ? 'active' : ''}`}
            onClick={() => {
              setActiveTab('signup');
              setSignupErrors({});
            }}
          >
            Sign Up
          </button>
        </div>

        {/* Login Form */}
        {activeTab === 'login' && (
          <form onSubmit={handleLoginSubmit} className="form-container">
            {loginErrors.submit && (
              <div className="error-banner">
                <AlertCircle size={20} />
                <span>{loginErrors.submit}</span>
              </div>
            )}

            <div className="form-group">
              <label htmlFor="login-email">Email Address</label>
              <input
                id="login-email"
                type="email"
                placeholder="Enter your email"
                value={loginEmail}
                onChange={(e) => {
                  setLoginEmail(e.target.value);
                  if (loginErrors.email) {
                    setLoginErrors({ ...loginErrors, email: '' });
                  }
                }}
                className={`form-input ${loginErrors.email ? 'error' : ''}`}
                disabled={isLoading}
              />
              {loginErrors.email && <p className="error-text">{loginErrors.email}</p>}
            </div>

            <div className="form-group">
              <label htmlFor="login-password">Password</label>
              <div className="password-input-wrapper">
                <input
                  id="login-password"
                  type={showLoginPassword ? 'text' : 'password'}
                  placeholder="Enter your password"
                  value={loginPassword}
                  onChange={(e) => {
                    setLoginPassword(e.target.value);
                    if (loginErrors.password) {
                      setLoginErrors({ ...loginErrors, password: '' });
                    }
                  }}
                  className={`form-input ${loginErrors.password ? 'error' : ''}`}
                  disabled={isLoading}
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowLoginPassword(!showLoginPassword)}
                  disabled={isLoading}
                >
                  {showLoginPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
              {loginErrors.password && <p className="error-text">{loginErrors.password}</p>}
            </div>

            <a href="#" className="forgot-password-link">
              Forgot password?
            </a>

            <button
              type="submit"
              className="submit-button"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Loader size={18} className="spinner" />
                  Logging in...
                </>
              ) : (
                'Log In'
              )}
            </button>
          </form>
        )}

        {/* Signup Form */}
        {activeTab === 'signup' && (
          <form onSubmit={handleSignupSubmit} className="form-container">
            {signupErrors.submit && (
              <div className="error-banner">
                <AlertCircle size={20} />
                <span>{signupErrors.submit}</span>
              </div>
            )}

            <div className="form-group">
              <label>I am a...</label>
              <div className="role-selector">
                <button
                  type="button"
                  className={`role-button ${role === 'patient' ? 'active' : ''}`}
                  onClick={() => {
                    setRole('patient');
                    setPhone('');
                  }}
                >
                  👤 Patient
                </button>
                <button
                  type="button"
                  className={`role-button ${role === 'caregiver' ? 'active' : ''}`}
                  onClick={() => setRole('caregiver')}
                >
                  👥 Caregiver
                </button>
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="signup-fullname">Full Name</label>
              <input
                id="signup-fullname"
                type="text"
                placeholder="Jane Doe"
                value={fullName}
                onChange={(e) => {
                  setFullName(e.target.value);
                  if (signupErrors.fullName) {
                    setSignupErrors({ ...signupErrors, fullName: '' });
                  }
                }}
                className={`form-input ${signupErrors.fullName ? 'error' : ''}`}
                disabled={isLoading}
              />
              {signupErrors.fullName && <p className="error-text">{signupErrors.fullName}</p>}
            </div>

            <div className="form-group">
              <label htmlFor="signup-email">Email Address</label>
              <input
                id="signup-email"
                type="email"
                placeholder="jane.doe@example.com"
                value={signupEmail}
                onChange={(e) => {
                  setSignupEmail(e.target.value);
                  if (signupErrors.email) {
                    setSignupErrors({ ...signupErrors, email: '' });
                  }
                }}
                className={`form-input ${signupErrors.email ? 'error' : ''}`}
                disabled={isLoading}
              />
              {signupErrors.email && <p className="error-text">{signupErrors.email}</p>}
            </div>

            <div className="form-group">
              <label htmlFor="signup-password">Password</label>
              <div className="password-input-wrapper">
                <input
                  id="signup-password"
                  type={showSignupPassword ? 'text' : 'password'}
                  placeholder="Create a password"
                  value={signupPassword}
                  onChange={(e) => {
                    setSignupPassword(e.target.value);
                    if (signupErrors.password) {
                      setSignupErrors({ ...signupErrors, password: '' });
                    }
                  }}
                  className={`form-input ${signupErrors.password ? 'error' : ''}`}
                  disabled={isLoading}
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowSignupPassword(!showSignupPassword)}
                  disabled={isLoading}
                >
                  {showSignupPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
              {signupErrors.password && <p className="error-text">{signupErrors.password}</p>}
            </div>

            <div className="form-group">
              <label htmlFor="signup-confirm-password">Confirm Password</label>
              <div className="password-input-wrapper">
                <input
                  id="signup-confirm-password"
                  type={showConfirmPassword ? 'text' : 'password'}
                  placeholder="Confirm your password"
                  value={confirmPassword}
                  onChange={(e) => {
                    setConfirmPassword(e.target.value);
                    if (signupErrors.confirmPassword) {
                      setSignupErrors({ ...signupErrors, confirmPassword: '' });
                    }
                  }}
                  className={`form-input ${signupErrors.confirmPassword ? 'error' : ''}`}
                  disabled={isLoading}
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  disabled={isLoading}
                >
                  {showConfirmPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
              {signupErrors.confirmPassword && (
                <p className="error-text">{signupErrors.confirmPassword}</p>
              )}
            </div>

            {role === 'caregiver' && (
              <div className="form-group">
                <label htmlFor="signup-phone">Phone Number</label>
                <input
                  id="signup-phone"
                  type="tel"
                  placeholder="10-digit phone number"
                  value={phone}
                  onChange={(e) => {
                    setPhone(e.target.value);
                    if (signupErrors.phone) {
                      setSignupErrors({ ...signupErrors, phone: '' });
                    }
                  }}
                  className={`form-input ${signupErrors.phone ? 'error' : ''}`}
                  disabled={isLoading}
                />
                {signupErrors.phone && <p className="error-text">{signupErrors.phone}</p>}
              </div>
            )}

            <button
              type="submit"
              className="submit-button"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Loader size={18} className="spinner" />
                  Signing up...
                </>
              ) : (
                <>
                  Sign Up <span className="arrow">→</span>
                </>
              )}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}

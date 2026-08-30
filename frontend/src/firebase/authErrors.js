const AUTH_ERROR_MESSAGES = {
  'auth/email-already-in-use': 'An account with this email already exists',
  'auth/invalid-email': 'Enter a valid email address',
  'auth/invalid-credential': 'Incorrect email or password',
  'auth/user-not-found': 'No account found with this email',
  'auth/wrong-password': 'Incorrect password',
  'auth/weak-password': 'Use a stronger password',
  'auth/missing-password': 'Enter your password',
  'auth/too-many-requests': 'Too many attempts. Please try again later',
  'auth/network-request-failed': 'Network error. Check your connection and try again',
};

export function getAuthErrorMessage(error) {
  return AUTH_ERROR_MESSAGES[error?.code] || 'Authentication failed. Please try again';
}

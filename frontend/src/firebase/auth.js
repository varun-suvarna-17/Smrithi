import {
  createUserWithEmailAndPassword,
  onAuthStateChanged,
  signInWithEmailAndPassword,
  signOut,
} from 'firebase/auth';

import { auth } from './config';

// Mock auth state fallback
let mockUser = null;
try {
  const stored = localStorage.getItem('mock_user');
  if (stored) {
    const parsed = JSON.parse(stored);
    if (parsed) {
      mockUser = {
        ...parsed,
        getIdToken: async () => 'mock_token_' + Date.now(),
      };
    }
  }
} catch (e) {
  console.error("Failed to load mock user from localStorage", e);
}

const authListeners = new Set();

const notifyListeners = (user) => {
  mockUser = user;
  if (user) {
    localStorage.setItem('mock_user', JSON.stringify({
      uid: user.uid,
      email: user.email,
      displayName: user.displayName,
    }));
  } else {
    localStorage.removeItem('mock_user');
  }
  authListeners.forEach((listener) => listener(user));
};

export function registerWithEmail(email, password) {
  if (!auth) {
    const fakeUser = {
      uid: 'mock_uid_' + Math.random().toString(36).substring(2, 9),
      email: email,
      displayName: email.split('@')[0],
      getIdToken: async () => 'mock_token_' + Date.now(),
    };
    return new Promise((resolve) => {
      setTimeout(() => {
        notifyListeners(fakeUser);
        resolve({ user: fakeUser });
      }, 500);
    });
  }
  return createUserWithEmailAndPassword(auth, email, password);
}

export function loginWithEmail(email, password) {
  if (!auth) {
    const fakeUser = {
      uid: 'mock_uid_123',
      email: email,
      displayName: email.split('@')[0],
      getIdToken: async () => 'mock_token_123',
    };
    return new Promise((resolve) => {
      setTimeout(() => {
        notifyListeners(fakeUser);
        resolve({ user: fakeUser });
      }, 500);
    });
  }
  return signInWithEmailAndPassword(auth, email, password);
}

export function logout() {
  if (!auth) {
    return new Promise((resolve) => {
      setTimeout(() => {
        notifyListeners(null);
        resolve();
      }, 300);
    });
  }
  return signOut(auth);
}

export function onAuthChange(callback) {
  if (!auth) {
    authListeners.add(callback);
    // Call callback immediately with current state
    callback(mockUser);
    return () => {
      authListeners.delete(callback);
    };
  }
  return onAuthStateChanged(auth, callback);
}


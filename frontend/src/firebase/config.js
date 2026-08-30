import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
};

let app = null;
let authInstance = null;

const hasFirebaseConfig = firebaseConfig.apiKey && firebaseConfig.apiKey.trim() !== "";

if (hasFirebaseConfig) {
  try {
    app = initializeApp(firebaseConfig);
    authInstance = getAuth(app);
  } catch (error) {
    console.warn("Failed to initialize Firebase app. Falling back to mock auth mode.", error);
  }
} else {
  console.warn("No Firebase API key found. Falling back to mock auth mode.");
}

export const auth = authInstance;
export default app;


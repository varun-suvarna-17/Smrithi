import React, { createContext, useEffect, useMemo, useState } from 'react';

import { onAuthChange } from './auth';

export const AuthContext = createContext({
  currentUser: null,
  authLoading: true,
  idToken: null,
});

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [idToken, setIdToken] = useState(null);
  const [authLoading, setAuthLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthChange(async (user) => {
      setCurrentUser(user);
      setIdToken(user ? await user.getIdToken() : null);
      setAuthLoading(false);
    });

    return unsubscribe;
  }, []);

  const value = useMemo(
    () => ({ currentUser, authLoading, idToken }),
    [currentUser, authLoading, idToken],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

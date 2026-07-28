"use client";

import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import { getAuthBootstrap, getAuthMe, logout as apiLogout } from "@/lib/api";
import type { AuthConfig, AuthUser } from "@/lib/authTypes";
import { clearSessionActivity, useIdleLogout } from "@/hooks/useIdleLogout";

interface AuthContextType {
  oauthEnabled: boolean;
  authConfig: AuthConfig | null;
  user: AuthUser | null;
  loading: boolean;
  login: () => void;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [authConfig, setAuthConfig] = useState<AuthConfig | null>(null);
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);

  const refreshUser = useCallback(async () => {
    try {
      const me = await getAuthMe();
      setUser(me);
    } catch {
      setUser(null);
    }
  }, []);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      setLoading(true);
      try {
        const bootstrap = await getAuthBootstrap();
        if (cancelled) return;
        setAuthConfig(bootstrap.config);
        setUser(bootstrap.user);
      } catch {
        // Bootstrap failed (backend down / proxy error). Still try /config so
        // the login button can appear; never treat as "SSO disabled".
        try {
          const { getAuthConfig } = await import("@/lib/api");
          const config = await getAuthConfig();
          if (cancelled) return;
          setAuthConfig(config);
          setUser(null);
        } catch {
          if (!cancelled) {
            setAuthConfig({
              enabled: true,
              button_label: "Log in with Microsoft Entra",
              idle_timeout_seconds: 86400,
            });
            setUser(null);
          }
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const login = useCallback(() => {
    window.location.href = "/api/auth/login";
  }, []);

  const logout = useCallback(async () => {
    try {
      await apiLogout();
    } finally {
      clearSessionActivity();
      setUser(null);
    }
  }, []);

  const logoutRef = useRef(logout);
  logoutRef.current = logout;

  const idleTimeoutMs = (authConfig?.idle_timeout_seconds ?? 86400) * 1000;
  useIdleLogout(Boolean(authConfig?.enabled && user), idleTimeoutMs, () => {
    void logoutRef.current();
  });

  const value = useMemo(
    () => ({
      oauthEnabled: Boolean(authConfig?.enabled),
      authConfig,
      user,
      loading,
      login,
      logout,
      refreshUser,
    }),
    [authConfig, user, loading, login, logout, refreshUser]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return ctx;
};

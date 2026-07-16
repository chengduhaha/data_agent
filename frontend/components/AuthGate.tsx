"use client";

import { useAuth } from "@/context/AuthContext";
import { LoginPage, LoginPageShell } from "@/components/LoginPage";

export function AuthGate({ children }: { children: React.ReactNode }) {
  const { oauthEnabled, user, loading } = useAuth();

  if (loading) {
    return <LoginPageShell message="Checking sign-in…" />;
  }

  if (oauthEnabled && !user) {
    return <LoginPage />;
  }

  return <>{children}</>;
}

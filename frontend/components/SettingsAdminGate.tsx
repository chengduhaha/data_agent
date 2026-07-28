"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { isAdminUser } from "@/lib/roles";

export function SettingsAdminGate({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { user, oauthEnabled, loading } = useAuth();
  const allowed = isAdminUser(user, oauthEnabled);

  useEffect(() => {
    if (!loading && !allowed) {
      router.replace("/");
    }
  }, [allowed, loading, router]);

  if (loading) {
    return (
      <div className="flex flex-1 items-center justify-center text-sm text-ink-500">
        Loading…
      </div>
    );
  }

  if (!allowed) return null;

  return <>{children}</>;
}

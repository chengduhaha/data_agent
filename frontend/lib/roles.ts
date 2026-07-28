import type { AuthUser } from "@/lib/authTypes";

/** Admins see Settings; regular users get Chat only. Dev (SSO off) is treated as admin. */
export function isAdminUser(
  user: AuthUser | null,
  oauthEnabled: boolean
): boolean {
  if (!oauthEnabled) return true;
  return user?.role === "admin";
}

export type AuthConfig = {
  enabled: boolean;
  button_label: string;
  idle_timeout_seconds: number;
};

export type UiBranding = {
  title_suffix?: string | null;
};

export type AuthUser = {
  sub: string;
  cis_login_id?: string | null;
  email?: string | null;
  name?: string | null;
  workspace_slug: string;
  role?: "admin" | "user";
};

export type AuthBootstrap = {
  config: AuthConfig;
  user: AuthUser | null;
  branding?: UiBranding;
};

export function getUserDisplayName(user: AuthUser): string {
  const name = user.name?.trim();
  if (name) return name;
  const cis = user.cis_login_id?.trim();
  if (cis) return cis;
  const email = user.email?.trim();
  if (email) return email.split("@")[0] || email;
  return user.sub;
}

export function getUserInitials(user: AuthUser): string {
  const display = getUserDisplayName(user);
  const parts = display.split(/[\s._-]+/).filter(Boolean);
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase();
  }
  return display.slice(0, 2).toUpperCase();
}

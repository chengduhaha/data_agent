"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { UserMenu } from "@/components/UserMenu";
import { useAuth } from "@/context/AuthContext";
import { isAdminUser } from "@/lib/roles";

const NAV = [
  { href: "/", label: "Chat", adminOnly: false },
  { href: "/settings/account", label: "Settings", adminOnly: true },
] as const;

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { user, oauthEnabled, branding } = useAuth();
  const showSettings = isAdminUser(user, oauthEnabled);
  const navItems = NAV.filter((item) => !item.adminOnly || showSettings);
  const titleSuffix = branding?.title_suffix?.trim();

  return (
    <div className="mx-auto flex h-dvh max-h-dvh max-w-[1400px] flex-col overflow-hidden px-4 py-3 md:px-6">
      <header className="mb-3 flex shrink-0 items-center justify-between gap-3 border-b border-ink-200/50 pb-3">
        <div className="min-w-0">
          <p className="font-display text-xl font-semibold tracking-tight text-ink-900 md:text-2xl">
            Data Agent
          </p>
          {titleSuffix ? (
            <p className="text-[11px] font-medium uppercase tracking-wide text-ink-400">
              {titleSuffix}
            </p>
          ) : null}
          <p className="hidden text-xs text-ink-500 sm:block">
            Developed and supported by the BigData Platform team
          </p>
        </div>
        <div className="flex shrink-0 items-center gap-2">
          <nav className="flex items-center gap-1 rounded-2xl border border-ink-200/70 bg-white/60 p-1 backdrop-blur">
            {navItems.map((item) => {
              const active =
                item.href === "/"
                  ? pathname === "/"
                  : pathname.startsWith("/settings");
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`rounded-xl px-3 py-1.5 text-sm font-medium transition ${
                    active
                      ? "bg-ink-900 text-white"
                      : "text-ink-600 hover:bg-white hover:text-ink-900"
                  }`}
                >
                  {item.label}
                </Link>
              );
            })}
          </nav>
          <UserMenu />
        </div>
      </header>
      <main className="flex min-h-0 flex-1 flex-col">{children}</main>
    </div>
  );
}

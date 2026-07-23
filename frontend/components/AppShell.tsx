"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { UserMenu } from "@/components/UserMenu";

const NAV = [
  { href: "/", label: "Chat" },
  { href: "/settings/account", label: "Settings" },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  return (
    <div className="mx-auto flex h-dvh max-h-dvh max-w-[1400px] flex-col overflow-hidden px-4 py-3 md:px-6">
      <header className="mb-3 flex shrink-0 items-center justify-between gap-3 border-b border-ink-200/50 pb-3">
        <div className="min-w-0">
          <p className="font-display text-xl font-semibold tracking-tight text-ink-900 md:text-2xl">
            Data Agent
          </p>
          <p className="hidden text-xs text-ink-500 sm:block">
            Your personal agent workspace
          </p>
        </div>
        <div className="flex shrink-0 items-center gap-2">
          <nav className="flex items-center gap-1 rounded-2xl border border-ink-200/70 bg-white/60 p-1 backdrop-blur">
            {NAV.map((item) => {
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

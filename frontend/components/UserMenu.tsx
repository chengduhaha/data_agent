"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { getUserDisplayName, getUserInitials } from "@/lib/authTypes";

export function UserMenu() {
  const { user, oauthEnabled, logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") setIsOpen(false);
    };
    document.addEventListener("keydown", handleEscape);
    return () => document.removeEventListener("keydown", handleEscape);
  }, []);

  if (!oauthEnabled || !user) return null;

  const displayName = getUserDisplayName(user);
  const initials = getUserInitials(user);
  const email = user.email?.trim() || null;
  const workspace = user.workspace_slug?.trim() || null;
  const cis = user.cis_login_id?.trim() || null;

  return (
    <div className="relative shrink-0" ref={menuRef}>
      <button
        type="button"
        className="flex h-9 w-9 items-center justify-center rounded-full bg-ink-900 text-xs font-semibold text-white transition hover:bg-ink-800"
        onClick={() => setIsOpen((open) => !open)}
        aria-expanded={isOpen}
        aria-haspopup="menu"
        aria-label={`Signed in as ${displayName}`}
        title={displayName}
      >
        {initials}
      </button>

      {isOpen && (
        <div
          className="absolute right-0 top-11 z-[100] w-[min(360px,calc(100vw-2rem))] rounded-2xl border border-ink-200/80 bg-white shadow-xl"
          role="menu"
        >
          <div className="space-y-2 px-4 py-4">
            <div className="flex items-start gap-3">
              <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-ink-100 text-sm font-semibold text-ink-700">
                {initials}
              </span>
              <div className="min-w-0 flex-1 space-y-1">
                <p className="break-words text-sm font-semibold leading-snug text-ink-900">
                  {displayName}
                </p>
                {email && (
                  <p className="break-all text-xs leading-relaxed text-ink-500">{email}</p>
                )}
              </div>
            </div>
            <dl className="space-y-1.5 rounded-xl bg-ink-50/80 px-3 py-2.5 text-xs">
              {workspace && (
                <div className="flex gap-2">
                  <dt className="shrink-0 font-medium text-ink-500">Workspace</dt>
                  <dd className="break-all font-mono text-ink-800">{workspace}</dd>
                </div>
              )}
              {cis && (
                <div className="flex gap-2">
                  <dt className="shrink-0 font-medium text-ink-500">CIS ID</dt>
                  <dd className="break-all font-mono text-ink-800">{cis}</dd>
                </div>
              )}
            </dl>
          </div>
          <div className="border-t border-ink-100" />
          <Link
            href="/settings/account"
            role="menuitem"
            className="block px-4 py-2.5 text-sm text-ink-700 transition hover:bg-ink-50"
            onClick={() => setIsOpen(false)}
          >
            Account & settings
          </Link>
          <button
            type="button"
            className="w-full px-4 py-2.5 text-left text-sm text-ink-700 transition hover:bg-ink-50"
            role="menuitem"
            onClick={() => {
              setIsOpen(false);
              void logout();
            }}
          >
            Log out
          </button>
        </div>
      )}
    </div>
  );
}

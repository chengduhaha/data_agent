"use client";

import { useAuth } from "@/context/AuthContext";

function MicrosoftIcon() {
  return (
    <svg className="h-5 w-5 shrink-0" viewBox="0 0 21 21" aria-hidden>
      <rect x="1" y="1" width="9" height="9" fill="#f25022" />
      <rect x="11" y="1" width="9" height="9" fill="#7fba00" />
      <rect x="1" y="11" width="9" height="9" fill="#00a4ef" />
      <rect x="11" y="11" width="9" height="9" fill="#ffb900" />
    </svg>
  );
}

export function LoginPageShell({ message = "Checking sign-in…" }: { message?: string }) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-[radial-gradient(ellipse_at_top,_#f8fafc,_#eef2ff_45%,_#f1f5f9)]">
      <div className="flex flex-col items-center gap-4 text-ink-600">
        <div className="h-10 w-10 animate-spin rounded-full border-2 border-ink-200 border-t-ink-900" />
        <p className="text-sm">{message}</p>
      </div>
    </div>
  );
}

export function LoginPage() {
  const { authConfig, login } = useAuth();
  const label = authConfig?.button_label || "Log in with Microsoft Entra";

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-[radial-gradient(ellipse_at_top,_#f8fafc,_#eef2ff_45%,_#f1f5f9)] px-4">
      <div className="pointer-events-none absolute -left-24 top-16 h-72 w-72 rounded-full bg-teal-200/30 blur-3xl" />
      <div className="pointer-events-none absolute -right-16 bottom-10 h-80 w-80 rounded-full bg-indigo-200/30 blur-3xl" />

      <div className="relative grid w-full max-w-4xl gap-8 md:grid-cols-[1.1fr_0.9fr] md:items-center">
        <section className="animate-fade-up">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-ink-500">
            Data Agent Platform
          </p>
          <h1 className="mt-3 font-display text-4xl font-semibold tracking-tight text-ink-900 md:text-5xl">
            Your workspace agent, secured by company SSO
          </h1>
          <p className="mt-4 max-w-lg text-sm leading-relaxed text-ink-600">
            Sign in once to access your personal agent workspace — MCP tools, skills, rules,
            and files scoped to your account.
          </p>
        </section>

        <section className="animate-fade-up rounded-3xl border border-white/70 bg-white/80 p-8 shadow-[0_24px_80px_rgba(15,23,42,0.08)] backdrop-blur">
          <h2 className="text-lg font-semibold text-ink-900">Sign in</h2>
          <p className="mt-1 text-sm text-ink-500">Use your company Microsoft account to continue.</p>
          <button
            type="button"
            onClick={login}
            className="mt-6 flex w-full items-center justify-center gap-3 rounded-2xl border border-ink-200 bg-white px-4 py-3 text-sm font-medium text-ink-900 transition hover:border-ink-300 hover:bg-ink-50"
          >
            <MicrosoftIcon />
            <span>{label}</span>
          </button>
          <p className="mt-4 text-center text-xs text-ink-400">
            Secure SSO via Microsoft Entra ID
          </p>
        </section>
      </div>
    </div>
  );
}

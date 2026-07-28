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
        <p className="text-xs text-ink-400">BigData Platform team</p>
      </div>
    </div>
  );
}

export function LoginPage() {
  const { authConfig, login } = useAuth();
  const label = authConfig?.button_label || "Log in with Microsoft Entra";

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-[radial-gradient(ellipse_at_top,_#f8fafc,_#eef2ff_45%,_#f1f5f9)] px-4 py-10">
      <div className="pointer-events-none absolute -left-24 top-16 h-72 w-72 rounded-full bg-teal-200/30 blur-3xl" />
      <div className="pointer-events-none absolute -right-16 bottom-10 h-80 w-80 rounded-full bg-indigo-200/30 blur-3xl" />

      <div className="relative w-full max-w-4xl">
        <div className="mb-8 flex flex-col items-center gap-2 text-center md:mb-10">
          <p className="text-xs font-semibold uppercase tracking-[0.22em] text-teal-700">
            BigData Platform
          </p>
          <p className="text-sm text-ink-500">
            Developed and supported by the BigData Platform team
          </p>
        </div>

        <div className="grid gap-8 md:grid-cols-[1.1fr_0.9fr] md:items-center">
          <section className="animate-fade-up">
            <h1 className="font-display text-4xl font-semibold tracking-tight text-ink-900 md:text-5xl">
              Data Agent
            </h1>
            <p className="mt-4 max-w-lg text-base leading-relaxed text-ink-700">
              Enterprise AI workspace for data analysis, skills, and MCP tools — scoped to your
              account and secured with company SSO.
            </p>
            <ul className="mt-6 space-y-2 text-sm text-ink-600">
              <li className="flex items-start gap-2">
                <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-teal-600" />
                Contract-guided analysis and Vertica query workflows
              </li>
              <li className="flex items-start gap-2">
                <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-teal-600" />
                Personal skills, rules, and workspace files
              </li>
              <li className="flex items-start gap-2">
                <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-teal-600" />
                Admin-managed MCP and platform capabilities
              </li>
            </ul>
          </section>

          <section className="animate-fade-up rounded-3xl border border-white/70 bg-white/85 p-8 shadow-[0_24px_80px_rgba(15,23,42,0.08)] backdrop-blur">
            <h2 className="text-lg font-semibold text-ink-900">Sign in to continue</h2>
            <p className="mt-2 text-sm leading-relaxed text-ink-500">
              Use your company Microsoft account. Access is provisioned per user workspace.
            </p>
            <button
              type="button"
              onClick={login}
              className="mt-6 flex w-full items-center justify-center gap-3 rounded-2xl border border-ink-200 bg-white px-4 py-3.5 text-sm font-medium text-ink-900 shadow-sm transition hover:border-ink-300 hover:bg-ink-50"
            >
              <MicrosoftIcon />
              <span>{label}</span>
            </button>
            <p className="mt-5 text-center text-xs leading-relaxed text-ink-400">
              Microsoft Entra ID · Single sign-on
              <br />
              <span className="text-ink-500">BigData Platform team</span>
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}

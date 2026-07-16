"use client";

import { useAuth } from "@/context/AuthContext";
import { getUserDisplayName } from "@/lib/authTypes";

export default function AccountSettingsPage() {
  const { user, oauthEnabled } = useAuth();

  if (!oauthEnabled) {
    return (
      <div className="space-y-4 animate-fade-up">
        <h1 className="font-display text-2xl text-ink-900">Account</h1>
        <p className="text-sm text-ink-500">
          SSO is disabled. Using local development workspace.
        </p>
      </div>
    );
  }

  if (!user) return null;

  const displayName = getUserDisplayName(user);

  return (
    <div className="mx-auto max-w-2xl space-y-6 animate-fade-up">
      <div>
        <h1 className="font-display text-2xl text-ink-900">Account</h1>
        <p className="mt-1 text-sm text-ink-500">
          Your identity and personal workspace on Data Agent.
        </p>
      </div>
      <section className="panel space-y-4 p-5">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-ink-400">
            Signed in as
          </p>
          <p className="mt-1 text-lg font-medium text-ink-900">{displayName}</p>
        </div>
        <dl className="grid gap-3 text-sm">
          {user.email && (
            <div>
              <dt className="text-ink-500">Email</dt>
              <dd className="mt-0.5 break-all font-mono text-ink-800">{user.email}</dd>
            </div>
          )}
          <div>
            <dt className="text-ink-500">Workspace</dt>
            <dd className="mt-0.5 break-all font-mono text-ink-800">
              {user.workspace_slug}
            </dd>
          </div>
          {user.cis_login_id && (
            <div>
              <dt className="text-ink-500">CIS login ID</dt>
              <dd className="mt-0.5 break-all font-mono text-ink-800">
                {user.cis_login_id}
              </dd>
            </div>
          )}
        </dl>
        <p className="text-xs leading-relaxed text-ink-500">
          Chats, personal skills, rules, MCP overrides, and files are stored under your
          workspace directory. Organization skills and knowledge are shared read-only for
          all users.
        </p>
      </section>
    </div>
  );
}

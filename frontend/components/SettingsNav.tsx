"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const ACCOUNT_LINK = { href: "/settings/account", label: "Account" };

const AGENT_LINKS = [
  { href: "/settings/model", label: "Model" },
  { href: "/settings/mcp", label: "MCP" },
  { href: "/settings/skills", label: "Skills" },
  { href: "/settings/rules", label: "Rules" },
  { href: "/settings/subagents", label: "Subagents" },
  { href: "/settings/tools", label: "Tools" },
  { href: "/settings/files", label: "Files" },
];

function NavSection({
  title,
  links,
}: {
  title: string;
  links: { href: string; label: string }[];
}) {
  const pathname = usePathname();
  return (
    <div>
      <p className="px-3 pb-1 pt-2 text-[11px] font-semibold uppercase tracking-wider text-ink-400">
        {title}
      </p>
      <ul className="space-y-0.5">
        {links.map((l) => {
          const active = pathname === l.href;
          return (
            <li key={l.href}>
              <Link
                href={l.href}
                className={`block rounded-xl px-3 py-2 text-sm transition ${
                  active
                    ? "bg-accent-soft font-medium text-accent-strong"
                    : "text-ink-600 hover:bg-ink-50"
                }`}
              >
                {l.label}
              </Link>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

export function SettingsNav() {
  return (
    <aside className="panel w-full shrink-0 p-2 md:w-52">
      <NavSection title="Account" links={[ACCOUNT_LINK]} />
      <NavSection title="Agent" links={AGENT_LINKS} />
    </aside>
  );
}

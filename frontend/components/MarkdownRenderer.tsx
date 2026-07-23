"use client";

import type { Components } from "react-markdown";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { normalizeNarrativeMarkdown, shouldUnwrapFence } from "@/lib/markdownOutput";

function buildComponents(nested: boolean): Components {
  return {
    h1: ({ children }) => (
      <h1 className="mb-3 mt-5 border-b border-ink-200/70 pb-2 font-display text-xl font-semibold text-ink-900 first:mt-0">
        {children}
      </h1>
    ),
    h2: ({ children }) => (
      <h2 className="mb-2.5 mt-5 font-display text-lg font-semibold text-ink-900 first:mt-0">
        {children}
      </h2>
    ),
    h3: ({ children }) => (
      <h3 className="mb-2 mt-4 text-base font-semibold text-ink-800 first:mt-0">
        {children}
      </h3>
    ),
    h4: ({ children }) => (
      <h4 className="mb-1.5 mt-3 text-sm font-semibold text-ink-800 first:mt-0">
        {children}
      </h4>
    ),
    p: ({ children }) => (
      <p className="mb-3 leading-relaxed text-ink-800 last:mb-0">{children}</p>
    ),
    strong: ({ children }) => (
      <strong className="font-semibold text-ink-900">{children}</strong>
    ),
    em: ({ children }) => <em className="italic text-ink-700">{children}</em>,
    ul: ({ children }) => (
      <ul className="mb-3 list-disc space-y-1.5 pl-5 text-ink-800 last:mb-0">{children}</ul>
    ),
    ol: ({ children }) => (
      <ol className="mb-3 list-decimal space-y-1.5 pl-5 text-ink-800 last:mb-0">{children}</ol>
    ),
    li: ({ children }) => <li className="leading-relaxed">{children}</li>,
    blockquote: ({ children }) => (
      <blockquote className="mb-3 border-l-4 border-accent/40 bg-accent-soft/30 py-2 pl-4 pr-2 text-ink-700 last:mb-0">
        {children}
      </blockquote>
    ),
    hr: () => <hr className="my-5 border-ink-200/80" />,
    a: ({ href, children }) => (
      <a
        href={href}
        target="_blank"
        rel="noopener noreferrer"
        className="font-medium text-accent underline decoration-accent/30 underline-offset-2 hover:decoration-accent"
      >
        {children}
      </a>
    ),
    code: ({ className, children, ...props }) => {
      const isBlock = Boolean(className);
      const text = String(children).replace(/\n$/, "");
      const lang = className?.replace(/^language-/, "") || "";

      if (isBlock && !nested && shouldUnwrapFence(lang, text)) {
        return (
          <div className="mb-3 rounded-xl border border-ink-200/60 bg-white/70 p-3 last:mb-0">
            <MarkdownRenderer content={text} nested normalize={false} />
          </div>
        );
      }

      if (isBlock) {
        return (
          <code className={`${className} font-mono text-[0.85em]`} {...props}>
            {children}
          </code>
        );
      }
      return (
        <code
          className="rounded-md bg-ink-100/80 px-1.5 py-0.5 font-mono text-[0.85em] text-ink-800"
          {...props}
        >
          {children}
        </code>
      );
    },
    pre: ({ children }) => (
      <pre className="mb-3 overflow-x-auto rounded-xl border border-ink-200/70 bg-ink-950 p-4 text-[0.82em] leading-relaxed text-ink-50 last:mb-0">
        {children}
      </pre>
    ),
    table: ({ children }) => (
      <div className="mb-4 overflow-x-auto rounded-xl border border-ink-200/70 last:mb-0">
        <table className="min-w-full border-collapse text-left text-sm">{children}</table>
      </div>
    ),
    thead: ({ children }) => (
      <thead className="bg-ink-50 text-xs font-semibold uppercase tracking-wide text-ink-600">
        {children}
      </thead>
    ),
    tbody: ({ children }) => <tbody className="divide-y divide-ink-200/60">{children}</tbody>,
    tr: ({ children }) => <tr className="hover:bg-ink-50/60">{children}</tr>,
    th: ({ children }) => (
      <th className="whitespace-nowrap px-3 py-2.5 font-semibold">{children}</th>
    ),
    td: ({ children }) => (
      <td className="whitespace-nowrap px-3 py-2.5 text-ink-800">{children}</td>
    ),
  };
}

export function MarkdownRenderer({
  content,
  className = "",
  streaming = false,
  nested = false,
  normalize = true,
}: {
  content: string;
  className?: string;
  streaming?: boolean;
  nested?: boolean;
  normalize?: boolean;
}) {
  const body = normalize ? normalizeNarrativeMarkdown(content, streaming) : content;
  return (
    <div className={`markdown-body ${className}`}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={buildComponents(nested)}
      >
        {body}
      </ReactMarkdown>
    </div>
  );
}

"use client";

import { useEffect, useState } from "react";
import { apiGet, apiSend, apiUpload } from "@/lib/api";

type Entry = {
  name: string;
  path: string;
  is_dir: boolean;
  size?: number | null;
};

export default function FilesSettingsPage() {
  const [path, setPath] = useState("");
  const [entries, setEntries] = useState<Entry[]>([]);
  const [filePath, setFilePath] = useState<string | null>(null);
  const [content, setContent] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<string | null>(null);

  async function loadDir(p: string) {
    setError(null);
    const data = await apiGet<{ path?: string; entries: Entry[] }>(
      `/api/files?path=${encodeURIComponent(p)}`
    );
    setPath(data.path || p);
    setEntries(data.entries || []);
  }

  useEffect(() => {
    void loadDir("").catch((e) => setError((e as Error).message));
  }, []);

  async function openEntry(e: Entry) {
    if (e.is_dir) {
      setFilePath(null);
      await loadDir(e.path);
      return;
    }
    const data = await apiGet<{ path: string; content: string }>(
      `/api/files/content?path=${encodeURIComponent(e.path)}`
    );
    setFilePath(data.path);
    setContent(data.content);
  }

  async function saveFile() {
    if (!filePath) return;
    setStatus(null);
    try {
      await apiSend("/api/files/content", "PUT", { path: filePath, content });
      setStatus("Saved.");
    } catch (e) {
      setError((e as Error).message);
    }
  }

  async function upload(file: File) {
    const fd = new FormData();
    fd.append("file", file);
    await apiUpload("/api/files/upload", fd, path ? { path } : undefined);
    await loadDir(path);
  }

  function goUp() {
    if (!path) return;
    const parts = path.split("/").filter(Boolean);
    parts.pop();
    void loadDir(parts.join("/"));
  }

  return (
    <div className="space-y-6 animate-fade-up">
      <div>
        <h1 className="font-display text-2xl text-ink-900">Workspace files</h1>
        <p className="mt-1 text-sm text-ink-500">
          Files under the agent&apos;s <code className="font-mono text-xs">/workspace/</code> root.
        </p>
      </div>
      <div className="grid gap-4 lg:grid-cols-[280px_1fr]">
        <div>
          <div className="mb-2 flex items-center justify-between gap-2">
            <p className="font-mono text-xs text-ink-500">/{path || ""}</p>
            <button type="button" className="btn-ghost !py-1 text-xs" onClick={goUp} disabled={!path}>
              Up
            </button>
          </div>
          <ul className="max-h-[480px] space-y-0.5 overflow-auto rounded-2xl border border-ink-200/70 bg-white/60 p-2">
            {entries.map((e) => (
              <li key={e.path}>
                <button
                  type="button"
                  className="w-full rounded-lg px-2 py-1.5 text-left text-sm hover:bg-ink-50"
                  onClick={() => void openEntry(e).catch((err) => setError((err as Error).message))}
                >
                  <span className="mr-2 font-mono text-[10px] uppercase text-ink-400">
                    {e.is_dir ? "dir" : "file"}
                  </span>
                  {e.name}
                </button>
              </li>
            ))}
            {entries.length === 0 && (
              <li className="px-2 py-3 text-xs text-ink-400">Empty</li>
            )}
          </ul>
          <label className="btn-ghost mt-3 inline-flex cursor-pointer">
            Upload
            <input
              type="file"
              className="hidden"
              onChange={(ev) => {
                const f = ev.target.files?.[0];
                if (f) void upload(f).catch((e) => setError((e as Error).message));
              }}
            />
          </label>
        </div>
        <div>
          {filePath ? (
            <>
              <p className="mb-2 font-mono text-xs text-ink-500">{filePath}</p>
              <textarea
                className="input min-h-[420px] font-mono text-xs"
                value={content}
                onChange={(e) => setContent(e.target.value)}
                spellCheck={false}
              />
              <div className="mt-3 flex gap-2">
                <button type="button" className="btn-primary" onClick={() => void saveFile()}>
                  Save
                </button>
                {status && <span className="text-sm text-accent">{status}</span>}
              </div>
            </>
          ) : (
            <p className="text-sm text-ink-400">Select a file to edit.</p>
          )}
          {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
        </div>
      </div>
    </div>
  );
}

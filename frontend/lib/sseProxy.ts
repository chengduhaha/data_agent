/** Server-side SSE proxy to the FastAPI backend (avoids Next rewrite buffering). */

const BACKEND =
  process.env.DATA_AGENT_BACKEND_URL?.replace(/\/$/, "") || "http://127.0.0.1:8000";

export async function proxySse(req: Request, backendPath: string): Promise<Response> {
  const incoming = new URL(req.url);
  const target = new URL(backendPath, `${BACKEND}/`);
  incoming.searchParams.forEach((v, k) => target.searchParams.set(k, v));

  const headers: Record<string, string> = {
    Accept: "text/event-stream",
    "Content-Type": "application/json",
  };
  const cookie = req.headers.get("cookie");
  if (cookie) headers.Cookie = cookie;

  const upstream = await fetch(target.toString(), {
    method: "POST",
    headers,
    body: await req.text(),
    cache: "no-store",
  });

  if (!upstream.ok || !upstream.body) {
    const text = await upstream.text().catch(() => upstream.statusText);
    return new Response(text || "Upstream error", {
      status: upstream.status || 502,
      headers: { "Content-Type": "text/plain; charset=utf-8" },
    });
  }

  return new Response(upstream.body, {
    status: 200,
    headers: {
      "Content-Type": "text/event-stream; charset=utf-8",
      "Cache-Control": "no-cache, no-transform",
      Connection: "keep-alive",
      "X-Accel-Buffering": "no",
      ...(upstream.headers.get("X-Thread-Id")
        ? { "X-Thread-Id": upstream.headers.get("X-Thread-Id")! }
        : {}),
    },
  });
}

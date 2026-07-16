import { proxySse } from "@/lib/sseProxy";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

/** Streaming proxy — avoids Next rewrite buffering of SSE. */
export async function POST(req: Request) {
  return proxySse(req, "/api/chat/stream");
}

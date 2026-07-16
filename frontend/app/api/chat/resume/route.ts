import { proxySse } from "@/lib/sseProxy";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

export async function POST(req: Request) {
  return proxySse(req, "/api/chat/resume");
}

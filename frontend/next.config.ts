import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // Hide the Next.js Dev Tools badge/Preferences (Theme there only styles the
  // overlay, not Data Agent). App theming is separate if/when added.
  devIndicators: false,
  async rewrites() {
    const backend = process.env.DATA_AGENT_BACKEND_URL || "http://127.0.0.1:8000";
    return [
      { source: "/api/auth/:path*", destination: `${backend}/api/auth/:path*` },
      // Chat SSE is handled by app/api/chat/*/route.ts (streaming proxy).
      // Keep other API paths on the rewrite.
      { source: "/api/chat/threads", destination: `${backend}/api/chat/threads` },
      { source: "/api/chat/threads/:path*", destination: `${backend}/api/chat/threads/:path*` },
      { source: "/api/config/:path*", destination: `${backend}/api/config/:path*` },
      { source: "/api/config", destination: `${backend}/api/config` },
      { source: "/api/mcp/:path*", destination: `${backend}/api/mcp/:path*` },
      { source: "/api/mcp", destination: `${backend}/api/mcp` },
      { source: "/api/skills/:path*", destination: `${backend}/api/skills/:path*` },
      { source: "/api/skills", destination: `${backend}/api/skills` },
      { source: "/api/rules/:path*", destination: `${backend}/api/rules/:path*` },
      { source: "/api/rules", destination: `${backend}/api/rules` },
      { source: "/api/subagents/:path*", destination: `${backend}/api/subagents/:path*` },
      { source: "/api/subagents", destination: `${backend}/api/subagents` },
      { source: "/api/tools/:path*", destination: `${backend}/api/tools/:path*` },
      { source: "/api/tools", destination: `${backend}/api/tools` },
      { source: "/api/files/:path*", destination: `${backend}/api/files/:path*` },
      { source: "/api/files", destination: `${backend}/api/files` },
      { source: "/api/providers", destination: `${backend}/api/providers` },
      { source: "/api/model-catalog", destination: `${backend}/api/model-catalog` },
      { source: "/health", destination: `${backend}/health` },
      { source: "/docs", destination: `${backend}/docs` },
      { source: "/openapi.json", destination: `${backend}/openapi.json` },
    ];
  },
};

export default nextConfig;

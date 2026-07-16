import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        ink: {
          50: "#f4f6f8",
          100: "#e8ecf0",
          200: "#d0d8e0",
          300: "#a8b5c2",
          400: "#7a8b9c",
          500: "#5a6b7c",
          600: "#445260",
          700: "#343f4a",
          800: "#242c34",
          900: "#171c22",
          950: "#0e1216",
        },
        accent: {
          DEFAULT: "#0f6b66",
          soft: "#d8efec",
          strong: "#0a4f4b",
        },
        warn: {
          DEFAULT: "#b45309",
          soft: "#fef3c7",
        },
      },
      fontFamily: {
        sans: ["var(--font-sora)", "system-ui", "sans-serif"],
        mono: ["var(--font-plex)", "ui-monospace", "monospace"],
        display: ["var(--font-fraunces)", "Georgia", "serif"],
      },
      boxShadow: {
        soft: "0 1px 2px rgba(23,28,34,0.04), 0 8px 24px rgba(23,28,34,0.06)",
      },
      keyframes: {
        fadeUp: {
          "0%": { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        pulseDot: {
          "0%, 100%": { opacity: "0.35", transform: "scale(0.9)" },
          "50%": { opacity: "1", transform: "scale(1)" },
        },
        shimmer: {
          "0%": { backgroundPosition: "200% 0" },
          "100%": { backgroundPosition: "-200% 0" },
        },
      },
      animation: {
        "fade-up": "fadeUp 0.35s ease-out both",
        "pulse-dot": "pulseDot 1.2s ease-in-out infinite",
        shimmer: "shimmer 2.4s linear infinite",
      },
    },
  },
  plugins: [],
};

export default config;

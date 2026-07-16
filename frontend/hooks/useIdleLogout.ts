"use client";

import { useEffect, useRef } from "react";

const LAST_ACTIVITY_KEY = "da_last_activity_ts";
const ACTIVITY_THROTTLE_MS = 30_000;
const CHECK_INTERVAL_MS = 60_000;

export function touchSessionActivity(): void {
  try {
    localStorage.setItem(LAST_ACTIVITY_KEY, String(Date.now()));
  } catch {
    /* private mode / storage disabled */
  }
}

export function clearSessionActivity(): void {
  try {
    localStorage.removeItem(LAST_ACTIVITY_KEY);
  } catch {
    /* ignore */
  }
}

function readLastActivity(): number | null {
  try {
    const raw = localStorage.getItem(LAST_ACTIVITY_KEY);
    if (!raw) return null;
    const ts = Number(raw);
    return Number.isFinite(ts) ? ts : null;
  } catch {
    return null;
  }
}

/** Log out after `idleTimeoutMs` without mouse/keyboard/scroll activity (cross-tab). */
export function useIdleLogout(
  enabled: boolean,
  idleTimeoutMs: number,
  onIdle: () => void
): void {
  const onIdleRef = useRef(onIdle);
  onIdleRef.current = onIdle;

  useEffect(() => {
    if (!enabled || idleTimeoutMs <= 0) return;

    const last = readLastActivity();
    const now = Date.now();
    if (last === null) {
      touchSessionActivity();
    } else if (now - last >= idleTimeoutMs) {
      clearSessionActivity();
      onIdleRef.current();
      return;
    }

    let lastWrite = now;
    const recordActivity = () => {
      const ts = Date.now();
      if (ts - lastWrite < ACTIVITY_THROTTLE_MS) return;
      lastWrite = ts;
      touchSessionActivity();
    };

    const events = ["mousedown", "keydown", "touchstart", "scroll", "click"] as const;
    for (const ev of events) {
      window.addEventListener(ev, recordActivity, { passive: true });
    }

    const timer = window.setInterval(() => {
      const activityAt = readLastActivity();
      if (activityAt === null) return;
      if (Date.now() - activityAt >= idleTimeoutMs) {
        clearSessionActivity();
        onIdleRef.current();
      }
    }, CHECK_INTERVAL_MS);

    return () => {
      for (const ev of events) {
        window.removeEventListener(ev, recordActivity);
      }
      window.clearInterval(timer);
    };
  }, [enabled, idleTimeoutMs]);
}

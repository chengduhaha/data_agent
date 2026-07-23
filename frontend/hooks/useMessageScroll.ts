"use client";

import { useCallback, useEffect, useLayoutEffect, useRef, useState } from "react";

const NEAR_BOTTOM_PX = 48;

/**
 * Scroll a message-list container (not the window) and only auto-follow
 * new content while the user is already near the bottom. Avoids the
 * "page jumps around while streaming" problem caused by window-level
 * `scrollIntoView({ behavior: "smooth" })` on every token/tool update.
 */
export function useMessageScroll<T extends HTMLElement = HTMLDivElement>(
  deps: unknown[],
  { threshold = 0.85, streaming = false }: { threshold?: number; streaming?: boolean } = {}
) {
  const scrollableRef = useRef<T | null>(null);
  const contentRef = useRef<HTMLDivElement | null>(null);
  const bottomSentinelRef = useRef<HTMLDivElement | null>(null);
  const [isNearBottom, setIsNearBottom] = useState(true);
  const userScrolledAwayRef = useRef(false);

  const scrollToBottom = useCallback((behavior: ScrollBehavior = "auto") => {
    const root = scrollableRef.current;
    if (!root) return;
    root.scrollTo({ top: root.scrollHeight, behavior });
  }, []);

  const readNearBottom = useCallback(() => {
    const root = scrollableRef.current;
    if (!root) return true;
    const distance = root.scrollHeight - root.scrollTop - root.clientHeight;
    return distance < NEAR_BOTTOM_PX;
  }, []);

  const resetFollow = useCallback(() => {
    userScrolledAwayRef.current = false;
    setIsNearBottom(true);
    scrollToBottom("auto");
  }, [scrollToBottom]);

  const shouldAutoFollow = useCallback(() => {
    return !userScrolledAwayRef.current || readNearBottom();
  }, [readNearBottom]);

  useEffect(() => {
    const sentinel = bottomSentinelRef.current;
    const root = scrollableRef.current;
    if (!sentinel || !root) return;
    const observer = new IntersectionObserver(
      ([entry]) => setIsNearBottom(entry.isIntersecting),
      { root, threshold }
    );
    observer.observe(sentinel);
    return () => observer.disconnect();
  }, [threshold]);

  useEffect(() => {
    const root = scrollableRef.current;
    if (!root) return;
    const onScroll = () => {
      const near = readNearBottom();
      userScrolledAwayRef.current = !near;
      setIsNearBottom(near);
    };
    root.addEventListener("scroll", onScroll, { passive: true });
    return () => root.removeEventListener("scroll", onScroll);
  }, [readNearBottom]);

  // Only auto-follow when the user has not scrolled away — never yank the view
  // while the user is reading scrollback.
  useLayoutEffect(() => {
    if (shouldAutoFollow()) scrollToBottom("auto");
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  // Follow streaming content growth (tokens, tool cards, etc.) via ResizeObserver.
  useEffect(() => {
    const content = contentRef.current;
    if (!content || !streaming) return;

    let lastRun = 0;
    const throttleMs = 100;

    const observer = new ResizeObserver(() => {
      const now = Date.now();
      if (now - lastRun < throttleMs) return;
      lastRun = now;
      if (shouldAutoFollow()) scrollToBottom("auto");
    });

    observer.observe(content);
    return () => observer.disconnect();
  }, [streaming, scrollToBottom, shouldAutoFollow]);

  return {
    scrollableRef,
    contentRef,
    bottomSentinelRef,
    isNearBottom,
    scrollToBottom,
    resetFollow,
  };
}

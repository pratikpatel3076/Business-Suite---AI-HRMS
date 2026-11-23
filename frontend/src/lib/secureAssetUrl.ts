import { useCallback, useEffect, useRef, useState } from "react";
import { getApiBaseUrl } from "@/config/runtime";
import { api } from "@/services/api";

const STORED_UPLOAD_PREFIX = "/uploads/";
const API_UPLOAD_PREFIX = "/api/v1/uploads/";
const SIGNED_URL_TTL_MS = 55_000;

type CachedUrl = { url: string; expiresAt: number };

/**
 * Resolve a stored `/uploads/...` URL to a short-lived signed URL.
 *
 * Signing requires an authenticated API call, so the returned function stays
 * synchronous for existing callers: it returns a cached signed URL immediately
 * and triggers a background signing request on first use, re-rendering when
 * the URL arrives. Access tokens are never placed in query strings.
 */
export function useAssetUrl(): (path?: string | null) => string | undefined {
  const cache = useRef<Map<string, CachedUrl>>(new Map());
  const pending = useRef<Set<string>>(new Set());
  const mounted = useRef(true);
  const [, forceRender] = useState(0);

  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
    };
  }, []);

  return useCallback((path?: string | null) => {
    if (!path) return undefined;
    const isStored = path.startsWith(STORED_UPLOAD_PREFIX) || path.startsWith(API_UPLOAD_PREFIX);
    if (!isStored) return path;

    const cached = cache.current.get(path);
    if (cached && cached.expiresAt > Date.now()) return cached.url;

    if (!pending.current.has(path)) {
      pending.current.add(path);
      api
        .post<{ url: string }>("/uploads/sign", { path })
        .then(({ data }) => {
          const apiBase = getApiBaseUrl().replace(/\/+$/, "");
          cache.current.set(path, {
            url: `${apiBase}${data.url}`,
            expiresAt: Date.now() + SIGNED_URL_TTL_MS,
          });
          pending.current.delete(path);
          if (mounted.current) forceRender((value) => value + 1);
        })
        .catch(() => {
          pending.current.delete(path);
        });
    }
    return undefined;
  }, []);
}

import { useCallback } from "react";
import { getApiBaseUrl } from "@/config/runtime";
import { useAuthStore } from "@/store/authStore";

const STORED_UPLOAD_PREFIX = "/uploads/";

/** Convert a stored `/uploads/...` URL into an authenticated API download URL. */
export function buildAssetUrl(path?: string | null, token?: string | null): string | undefined {
  if (!path) return undefined;
  if (/^https?:\/\//i.test(path)) return path;

  let url = path;
  if (path.startsWith(STORED_UPLOAD_PREFIX)) {
    const apiBase = getApiBaseUrl().replace(/\/+$/, "");
    url = `${apiBase}${path}`;
  }

  // Native <img>/<a> requests cannot send an Authorization header. The upload
  // endpoint accepts this token only on its own route and it is never logged.
  if (token) {
    url += `${url.includes("?") ? "&" : "?"}token=${encodeURIComponent(token)}`;
  }
  return url;
}

/** Subscribe to auth state so asset URLs refresh after login/logout. */
export function useAssetUrl(): (path?: string | null) => string | undefined {
  const token = useAuthStore((state) => state.accessToken);
  return useCallback((path?: string | null) => buildAssetUrl(path, token), [token]);
}

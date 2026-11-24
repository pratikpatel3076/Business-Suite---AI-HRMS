type RuntimeConfig = {
  apiBaseUrl?: string;
};

declare global {
  interface Window {
    __GEMEINSAM_CONFIG__?: RuntimeConfig;
  }
}

function cleanUrl(value?: string | null): string | undefined {
  const trimmed = value?.trim();
  if (!trimmed) return undefined;
  return trimmed.replace(/\/+$/, "");
}

export function getApiBaseUrl(): string {
  return (
    cleanUrl(window.__GEMEINSAM_CONFIG__?.apiBaseUrl) ||
    cleanUrl(import.meta.env.VITE_API_BASE_URL) ||
    cleanUrl(import.meta.env.VITE_API_URL) ||
    "/api/v1"
  );
}

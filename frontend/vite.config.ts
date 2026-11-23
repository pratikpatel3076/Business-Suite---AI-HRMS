import { fileURLToPath } from "url";
import react from "@vitejs/plugin-react";
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const apiProxyTarget = env.VITE_DEV_API_PROXY_TARGET || env.VITE_BACKEND_URL || "http://localhost:8001";

  return {
    plugins: [react()],
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("./src", import.meta.url)),
      },
    },
    server: {
      port: 5173,
      proxy: {
        "/api": {
          target: apiProxyTarget,
          changeOrigin: true,
        },
      },
    },
    build: {
      sourcemap: false,
      chunkSizeWarningLimit: 800,
      rollupOptions: {
        output: {
          manualChunks(id) {
            if (!id.includes("node_modules")) return undefined;
            if (
              id.includes("/react/") ||
              id.includes("/react-dom/") ||
              id.includes("/react-router/") ||
              id.includes("/react-router-dom/")
            ) return "vendor";
            if (id.includes("/@radix-ui/")) return "ui";
            if (id.includes("/recharts/")) return "charts";
            if (id.includes("/@tanstack/react-query/")) return "query";
            if (id.includes("/react-hook-form/") || id.includes("/zod/")) return "form";
            return undefined;
          },
        },
      },
    },
  };
});

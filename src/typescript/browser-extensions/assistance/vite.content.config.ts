import { resolve } from "path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  define: {
    "process.env": {},
  },
  build: {
    emptyOutDir: true,
    outDir: resolve(__dirname, "dist"),
    lib: {
      formats: ["iife"],
      entry: resolve(__dirname, "./src/index.tsx"),
      name: "Assistance",
    },
    rollupOptions: {
      output: {
        entryFileNames: "index.global.js",
        extend: true,
      },
    },
  },
});

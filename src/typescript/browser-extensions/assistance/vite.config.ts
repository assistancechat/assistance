import { resolve } from "path";
import { defineConfig } from "vite";

export default defineConfig({
  build: {
    emptyOutDir: true,
    outDir: resolve(__dirname, "dist"),
    lib: {
      entry: resolve(__dirname, "./src/main.ts"),
      name: "AI Assistance GMail Extension",
    },
    rollupOptions: {
      output: {
        entryFileNames: "main.js",
        extend: true,
      },
    },
  },
});

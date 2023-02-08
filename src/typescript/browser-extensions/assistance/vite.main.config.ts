import { resolve } from "path";
import { defineConfig } from "vite";

export default defineConfig({
  define: {
    "process.env": {},
  },
  build: {
    emptyOutDir: false,
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

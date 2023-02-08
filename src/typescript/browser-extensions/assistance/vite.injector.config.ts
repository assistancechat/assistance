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
      entry: resolve(__dirname, "./src/loader/extension-injector.js"),
      name: "Gmail JS & Extension Injector",
    },
    rollupOptions: {
      output: {
        entryFileNames: "extension-injector.js",
        extend: true,
      },
    },
  },
});

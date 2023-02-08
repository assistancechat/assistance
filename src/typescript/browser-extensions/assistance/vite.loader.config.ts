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
      entry: resolve(__dirname, "./src/loader/gmail-js-loader.js"),
      name: "Gmail JS Loader",
    },
    rollupOptions: {
      output: {
        entryFileNames: "gmail-js-loader.js",
        extend: true,
      },
    },
  },
});

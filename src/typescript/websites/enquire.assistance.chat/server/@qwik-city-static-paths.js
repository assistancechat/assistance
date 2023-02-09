const staticPaths = new Set(["/_headers","/favicon.svg","/manifest.json","/q-manifest.json","/robots.txt","/service-worker.js","/sitemap.xml"]);
function isStaticPath(p) {
  if (p.startsWith("/build/")) {
    return true;
  }
  if (p.startsWith("/assets/")) {
    return true;
  }
  if (staticPaths.has(p)) {
    return true;
  }
  return false;
}
export { isStaticPath };

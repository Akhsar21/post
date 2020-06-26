const staticCacheName = "bahutara-v" + new Date().getTime();
const filesToCache = [
  "/offline",
  "/static/images/icons/icon-192x192.png",
  "/static/images/icons/icon-512x512.png",
  "/static/images/icons/splash-2048x2732.png",
  "/static/css/github.css",
  "/static/js/highlight.pack.js",
  "/static/js/smooth-scrollbar.js",
];

self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "SKIP_WAITING") {
    self.skipWaiting();
  }
});

// Cache on install
self.addEventListener("install", async (event) => {
  event.waitUntil(
    caches.open(staticCacheName).then((cache) => {
      return cache.addAll(filesToCache);
    })
  );
});

// Clear cache on activate
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((cacheName) => cacheName.startsWith("bahutara-"))
          .filter((cacheName) => cacheName !== staticCacheName)
          .map((cacheName) => caches.delete(cacheName))
      );
    })
  );
});

// Serve from Cache
self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches
      .match(event.request)
      .then((response) => {
        return response || fetch(event.request);
      })
      .catch(() => {
        return caches.match("offline");
      })
  );
});

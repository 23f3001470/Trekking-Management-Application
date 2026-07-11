const CACHE_NAME = 'trekapp-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/manifest.json',
  '/img/icons/android-chrome-192x192.png',
  '/img/icons/android-chrome-512x512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(ASSETS_TO_CACHE))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.filter(name => name !== CACHE_NAME)
          .map(name => caches.delete(name))
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  // Pass through non-GET requests and API requests
  if (event.request.method !== 'GET' || event.request.url.includes('/auth') || event.request.url.includes('/admin') || event.request.url.includes('/staff') || event.request.url.includes('/user')) {
    return;
  }
  
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        return response || fetch(event.request);
      })
  );
});

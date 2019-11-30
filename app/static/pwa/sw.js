var cacheName = 'grapes-cache';
var filesToCache = [
  '/',
  '/master.css',
  '/splash.css',
  '/home.css',
  '/home',
  'https://fonts.googleapis.com/css?family=Merriweather:400&amp;display=swap',
  'https://use.typekit.net/izd0goo.css',
];self.addEventListener('install', function(e) {
  console.log('[ServiceWorker] Install');
  e.waitUntil(
    caches.open(cacheName).then(function(cache) {
      console.log('[ServiceWorker] Caching app shell');
      return cache.addAll(filesToCache);
    })
  );
});self.addEventListener('activate',  event => {
  event.waitUntil(self.clients.claim());
});self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request, {ignoreSearch:true}).then(response => {
      return response || fetch(event.request);
    })
  );
});

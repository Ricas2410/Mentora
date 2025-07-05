// Service Worker for Pentora PWA
const CACHE_NAME = 'Pentora-v1.0.0';
const OFFLINE_URL = '/offline/';

// Files to cache for offline functionality
const STATIC_CACHE_URLS = [
  '/',
  '/offline/',
  '/static/css/main.css',
  '/static/js/main.js',
  '/static/images/logo.png',
  '/static/images/icons/icon-192x192.png',
  '/static/images/icons/icon-512x512.png',
  'https://cdn.jsdelivr.net/npm/daisyui@4.12.10/dist/full.min.css',
  'https://cdn.tailwindcss.com',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
];

// Dynamic cache patterns
const CACHE_PATTERNS = [
  /^https:\/\/cdn\.jsdelivr\.net\//,
  /^https:\/\/cdnjs\.cloudflare\.com\//,
  /^https:\/\/fonts\.googleapis\.com\//,
  /^https:\/\/fonts\.gstatic\.com\//
];

// Install event - cache static resources
self.addEventListener('install', event => {
  console.log('Service Worker installing...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Caching static resources');
        return cache.addAll(STATIC_CACHE_URLS);
      })
      .then(() => {
        console.log('Service Worker installed successfully');
        return self.skipWaiting();
      })
      .catch(error => {
        console.error('Service Worker installation failed:', error);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  console.log('Service Worker activating...');
  
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => {
            if (cacheName !== CACHE_NAME) {
              console.log('Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('Service Worker activated');
        return self.clients.claim();
      })
  );
});

// Fetch event - serve cached content when offline
self.addEventListener('fetch', event => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') {
    return;
  }

  // Skip chrome-extension and other non-http requests
  if (!event.request.url.startsWith('http')) {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then(cachedResponse => {
        // Return cached version if available
        if (cachedResponse) {
          return cachedResponse;
        }

        // Try to fetch from network
        return fetch(event.request)
          .then(response => {
            // Don't cache non-successful responses
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Check if we should cache this resource
            const shouldCache = CACHE_PATTERNS.some(pattern => 
              pattern.test(event.request.url)
            ) || event.request.url.includes('/static/');

            if (shouldCache) {
              // Clone the response before caching
              const responseToCache = response.clone();
              
              caches.open(CACHE_NAME)
                .then(cache => {
                  cache.put(event.request, responseToCache);
                });
            }

            return response;
          })
          .catch(() => {
            // Network failed, try to serve offline page for navigation requests
            if (event.request.mode === 'navigate') {
              return caches.match(OFFLINE_URL);
            }
            
            // For other requests, return a generic offline response
            return new Response('Offline', {
              status: 503,
              statusText: 'Service Unavailable',
              headers: new Headers({
                'Content-Type': 'text/plain'
              })
            });
          });
      })
  );
});

// Background sync for offline actions
self.addEventListener('sync', event => {
  console.log('Background sync triggered:', event.tag);
  
  if (event.tag === 'quiz-submission') {
    event.waitUntil(syncQuizSubmissions());
  } else if (event.tag === 'progress-update') {
    event.waitUntil(syncProgressUpdates());
  }
});

// Push notifications
self.addEventListener('push', event => {
  console.log('Push notification received');
  
  const options = {
    body: event.data ? event.data.text() : 'New content available!',
    icon: '/static/images/icons/icon-192x192.png',
    badge: '/static/images/icons/badge-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'Explore',
        icon: '/static/images/icons/explore-32x32.png'
      },
      {
        action: 'close',
        title: 'Close',
        icon: '/static/images/icons/close-32x32.png'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('Pentora Learning', options)
  );
});

// Notification click handling
self.addEventListener('notificationclick', event => {
  console.log('Notification clicked:', event.action);
  
  event.notification.close();

  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/dashboard/')
    );
  } else if (event.action === 'close') {
    // Just close the notification
    return;
  } else {
    // Default action - open the app
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Helper functions for background sync
async function syncQuizSubmissions() {
  try {
    // Get pending quiz submissions from IndexedDB
    const pendingSubmissions = await getPendingQuizSubmissions();
    
    for (const submission of pendingSubmissions) {
      try {
        const response = await fetch('/api/quiz/submit/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': submission.csrfToken
          },
          body: JSON.stringify(submission.data)
        });
        
        if (response.ok) {
          await removePendingQuizSubmission(submission.id);
          console.log('Quiz submission synced successfully');
        }
      } catch (error) {
        console.error('Failed to sync quiz submission:', error);
      }
    }
  } catch (error) {
    console.error('Background sync failed:', error);
  }
}

async function syncProgressUpdates() {
  try {
    // Get pending progress updates from IndexedDB
    const pendingUpdates = await getPendingProgressUpdates();
    
    for (const update of pendingUpdates) {
      try {
        const response = await fetch('/api/progress/update/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': update.csrfToken
          },
          body: JSON.stringify(update.data)
        });
        
        if (response.ok) {
          await removePendingProgressUpdate(update.id);
          console.log('Progress update synced successfully');
        }
      } catch (error) {
        console.error('Failed to sync progress update:', error);
      }
    }
  } catch (error) {
    console.error('Progress sync failed:', error);
  }
}

// IndexedDB helper functions (simplified)
async function getPendingQuizSubmissions() {
  // Implementation would use IndexedDB to retrieve pending submissions
  return [];
}

async function removePendingQuizSubmission(id) {
  // Implementation would remove the submission from IndexedDB
}

async function getPendingProgressUpdates() {
  // Implementation would use IndexedDB to retrieve pending updates
  return [];
}

async function removePendingProgressUpdate(id) {
  // Implementation would remove the update from IndexedDB
}

console.log('Service Worker loaded successfully');

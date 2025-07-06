/**
 * Performance Optimization Script for Pentora Platform
 * Handles lazy loading, image optimization, and performance monitoring
 */

class PerformanceOptimizer {
    constructor() {
        this.init();
    }

    init() {
        this.setupLazyLoading();
        this.setupImageOptimization();
        this.setupPreloading();
        this.setupCaching();
        this.setupPerformanceMonitoring();
        this.setupLoadingStates();
    }

    setupLazyLoading() {
        // Intersection Observer for lazy loading
        if ('IntersectionObserver' in window) {
            this.setupIntersectionObserver();
        } else {
            // Fallback for older browsers
            this.loadAllImages();
        }
    }

    setupIntersectionObserver() {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    this.loadImage(img);
                    observer.unobserve(img);
                }
            });
        }, {
            rootMargin: '50px 0px', // Start loading 50px before the image enters viewport
            threshold: 0.01
        });

        // Observe all images with data-src
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });

        // Observe content sections for progressive loading
        const contentObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('content-visible');
                    this.loadSectionContent(entry.target);
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.lazy-section').forEach(section => {
            contentObserver.observe(section);
        });
    }

    loadImage(img) {
        const src = img.dataset.src;
        if (!src) return;

        // Create a new image to preload
        const imageLoader = new Image();
        
        imageLoader.onload = () => {
            img.src = src;
            img.classList.remove('lazy');
            img.classList.add('loaded');
            
            // Add fade-in animation
            img.style.opacity = '0';
            img.style.transition = 'opacity 0.3s ease';
            
            requestAnimationFrame(() => {
                img.style.opacity = '1';
            });
        };

        imageLoader.onerror = () => {
            img.src = '/static/images/placeholder.jpg'; // Fallback image
            img.classList.add('error');
        };

        imageLoader.src = src;
    }

    loadAllImages() {
        // Fallback for browsers without Intersection Observer
        document.querySelectorAll('img[data-src]').forEach(img => {
            this.loadImage(img);
        });
    }

    loadSectionContent(section) {
        const contentUrl = section.dataset.contentUrl;
        if (contentUrl && !section.dataset.loaded) {
            this.fetchSectionContent(section, contentUrl);
        }
    }

    async fetchSectionContent(section, url) {
        try {
            section.dataset.loaded = 'true';
            
            const response = await fetch(url);
            if (response.ok) {
                const content = await response.text();
                section.innerHTML = content;
                
                // Initialize any new components in the loaded content
                this.initializeLoadedContent(section);
            }
        } catch (error) {
            console.error('Failed to load section content:', error);
            section.innerHTML = '<p class="text-gray-500">Failed to load content. Please refresh the page.</p>';
        }
    }

    initializeLoadedContent(container) {
        // Re-initialize lazy loading for new images
        container.querySelectorAll('img[data-src]').forEach(img => {
            this.loadImage(img);
        });

        // Initialize any interactive components
        this.initializeInteractiveElements(container);
    }

    setupImageOptimization() {
        // Add responsive image loading
        this.setupResponsiveImages();
        
        // Add WebP support detection
        this.detectWebPSupport();
    }

    setupResponsiveImages() {
        document.querySelectorAll('img[data-sizes]').forEach(img => {
            const sizes = JSON.parse(img.dataset.sizes);
            const currentWidth = window.innerWidth;
            
            let bestSize = sizes[0];
            for (const size of sizes) {
                if (currentWidth >= size.minWidth) {
                    bestSize = size;
                }
            }
            
            if (img.dataset.src) {
                img.dataset.src = bestSize.url;
            } else {
                img.src = bestSize.url;
            }
        });
    }

    detectWebPSupport() {
        const webP = new Image();
        webP.onload = webP.onerror = () => {
            const isSupported = webP.height === 2;
            document.documentElement.classList.toggle('webp-supported', isSupported);
            
            if (isSupported) {
                this.convertToWebP();
            }
        };
        webP.src = 'data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA';
    }

    convertToWebP() {
        document.querySelectorAll('img[data-webp]').forEach(img => {
            const webpSrc = img.dataset.webp;
            if (webpSrc) {
                if (img.dataset.src) {
                    img.dataset.src = webpSrc;
                } else {
                    img.src = webpSrc;
                }
            }
        });
    }

    setupPreloading() {
        // Preload critical resources
        this.preloadCriticalResources();
        
        // Preload next page content on hover
        this.setupHoverPreloading();
    }

    preloadCriticalResources() {
        // Disable preloading to avoid console warnings
        // Scripts are already loaded in the correct order in base.html
        console.log('Preloading disabled to prevent console warnings');
        return;

        const criticalResources = [
            '/static/css/enhanced-ui.css'
        ];

        criticalResources.forEach(resource => {
            const link = document.createElement('link');
            link.rel = 'preload';

            if (resource.endsWith('.css')) {
                link.as = 'style';
            } else if (resource.endsWith('.js')) {
                link.as = 'script';
            } else if (resource.match(/\.(jpg|jpeg|png|gif|webp)$/)) {
                link.as = 'image';
            }

            link.href = resource;
            document.head.appendChild(link);
        });
    }

    setupHoverPreloading() {
        let preloadTimeout;
        
        document.addEventListener('mouseover', (e) => {
            const link = e.target.closest('a[href]');
            if (link && this.shouldPreload(link.href)) {
                preloadTimeout = setTimeout(() => {
                    this.preloadPage(link.href);
                }, 100); // Small delay to avoid preloading on quick mouse movements
            }
        });

        document.addEventListener('mouseout', () => {
            if (preloadTimeout) {
                clearTimeout(preloadTimeout);
            }
        });
    }

    shouldPreload(url) {
        // Only preload internal links
        return url.startsWith(window.location.origin) && 
               !url.includes('#') && 
               !url.includes('?') &&
               !url.endsWith('.pdf') &&
               !url.endsWith('.zip');
    }

    preloadPage(url) {
        if (this.preloadedPages?.has(url)) return;
        
        if (!this.preloadedPages) {
            this.preloadedPages = new Set();
        }

        const link = document.createElement('link');
        link.rel = 'prefetch';
        link.href = url;
        document.head.appendChild(link);
        
        this.preloadedPages.add(url);
    }

    setupCaching() {
        // Setup service worker caching strategy
        if ('serviceWorker' in navigator) {
            this.setupServiceWorkerCaching();
        }
        
        // Setup localStorage caching for API responses
        this.setupLocalStorageCaching();
    }

    setupServiceWorkerCaching() {
        // Send cache strategy to service worker
        if (navigator.serviceWorker.controller) {
            navigator.serviceWorker.controller.postMessage({
                type: 'CACHE_STRATEGY',
                strategy: {
                    images: 'cache-first',
                    api: 'network-first',
                    static: 'cache-first'
                }
            });
        }
    }

    setupLocalStorageCaching() {
        // Cache API responses in localStorage with expiration
        this.apiCache = {
            set: (key, data, ttl = 300000) => { // 5 minutes default TTL
                const item = {
                    data: data,
                    timestamp: Date.now(),
                    ttl: ttl
                };
                localStorage.setItem(`api_cache_${key}`, JSON.stringify(item));
            },
            
            get: (key) => {
                const item = localStorage.getItem(`api_cache_${key}`);
                if (!item) return null;
                
                const parsed = JSON.parse(item);
                if (Date.now() - parsed.timestamp > parsed.ttl) {
                    localStorage.removeItem(`api_cache_${key}`);
                    return null;
                }
                
                return parsed.data;
            },
            
            clear: () => {
                Object.keys(localStorage).forEach(key => {
                    if (key.startsWith('api_cache_')) {
                        localStorage.removeItem(key);
                    }
                });
            }
        };
    }

    setupPerformanceMonitoring() {
        // Only enable monitoring in production or when explicitly enabled
        const shouldMonitor = window.location.hostname !== '127.0.0.1' &&
                             window.location.hostname !== 'localhost' ||
                             localStorage.getItem('enableDetailedMonitoring') === 'true';

        if (!shouldMonitor) {
            console.log('Detailed performance monitoring disabled for development');
            return;
        }

        // Monitor Core Web Vitals (stores locally, doesn't send immediately)
        this.monitorCoreWebVitals();

        // Monitor resource loading (less frequent)
        this.monitorResourceLoading();

        // User interactions disabled to prevent spam
        // this.monitorUserInteractions();
    }

    monitorCoreWebVitals() {
        // DISABLED: Consolidated into main app.js to prevent duplicate requests
        // Core Web Vitals are now collected and sent in batch with other metrics
        console.log('Core Web Vitals monitoring disabled - handled by consolidated system');

        // Store metrics locally for batch reporting
        if ('PerformanceObserver' in window) {
            // LCP - only store, don't send immediately
            new PerformanceObserver((entryList) => {
                const entries = entryList.getEntries();
                const lastEntry = entries[entries.length - 1];
                if (!window.performanceMetrics) window.performanceMetrics = {};
                window.performanceMetrics.LCP = lastEntry.startTime;
            }).observe({ entryTypes: ['largest-contentful-paint'] });

            // FID - only store, don't send immediately
            new PerformanceObserver((entryList) => {
                const firstInput = entryList.getEntries()[0];
                if (!window.performanceMetrics) window.performanceMetrics = {};
                window.performanceMetrics.FID = firstInput.processingStart - firstInput.startTime;
            }).observe({ entryTypes: ['first-input'] });
        }
    }

    monitorResourceLoading() {
        window.addEventListener('load', () => {
            const navigation = performance.getEntriesByType('navigation')[0];
            const resources = performance.getEntriesByType('resource');

            // Store metrics locally instead of sending immediately
            if (!window.performanceMetrics) window.performanceMetrics = {};

            window.performanceMetrics.pageLoadTime = navigation.loadEventEnd - navigation.fetchStart;
            window.performanceMetrics.domContentLoaded = navigation.domContentLoadedEventEnd - navigation.fetchStart;
            window.performanceMetrics.resourceCount = resources.length;

            // Find slow resources and log them
            const slowResources = resources.filter(resource => resource.duration > 1000);
            if (slowResources.length > 0) {
                console.warn('Slow loading resources:', slowResources.map(r => r.name));
                window.performanceMetrics.slowResourceCount = slowResources.length;
            }
        });
    }

    monitorUserInteractions() {
        // DISABLED: Reduced monitoring to prevent excessive requests
        // User interaction monitoring is now handled by analytics middleware
        console.log('User interaction monitoring disabled - handled by server-side analytics');
    }

    reportMetric(name, value) {
        // DISABLED: Consolidated into main app.js performance monitoring
        // This prevents duplicate requests to the analytics endpoint
        console.log(`Performance metric: ${name} = ${value}`);

        // Store metrics locally for the main monitoring system to collect
        if (!window.performanceMetrics) {
            window.performanceMetrics = {};
        }
        window.performanceMetrics[name] = {
            value: value,
            timestamp: Date.now(),
            url: window.location.href
        };
    }

    setupLoadingStates() {
        // Add loading states to forms and buttons
        this.setupFormLoadingStates();
        
        // Add page transition loading
        this.setupPageTransitionLoading();
    }

    setupFormLoadingStates() {
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', (e) => {
                const submitButton = form.querySelector('button[type="submit"], input[type="submit"]');
                if (submitButton) {
                    this.showButtonLoading(submitButton);
                }
            });
        });
    }

    showButtonLoading(button) {
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Loading...';
        button.disabled = true;
        
        // Store original text for restoration
        button.dataset.originalText = originalText;
    }

    hideButtonLoading(button) {
        if (button.dataset.originalText) {
            button.innerHTML = button.dataset.originalText;
            button.disabled = false;
            delete button.dataset.originalText;
        }
    }

    setupPageTransitionLoading() {
        // Show loading indicator during page transitions
        let loadingIndicator;
        
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a[href]');
            if (link && this.isInternalLink(link.href)) {
                loadingIndicator = this.showPageLoading();
            }
        });

        window.addEventListener('beforeunload', () => {
            if (!loadingIndicator) {
                loadingIndicator = this.showPageLoading();
            }
        });

        window.addEventListener('load', () => {
            if (loadingIndicator) {
                this.hidePageLoading(loadingIndicator);
            }
        });
    }

    isInternalLink(url) {
        return url.startsWith(window.location.origin) || url.startsWith('/');
    }

    showPageLoading() {
        const loader = document.createElement('div');
        loader.className = 'page-loader fixed top-0 left-0 w-full h-1 bg-blue-600 z-50 transform scale-x-0 origin-left';
        loader.style.animation = 'loading-progress 2s ease-out forwards';
        
        document.body.appendChild(loader);
        return loader;
    }

    hidePageLoading(loader) {
        if (loader && loader.parentNode) {
            loader.style.transform = 'scaleX(1)';
            setTimeout(() => {
                loader.remove();
            }, 200);
        }
    }

    initializeInteractiveElements(container = document) {
        // Initialize tooltips
        container.querySelectorAll('[data-tooltip]').forEach(element => {
            this.initializeTooltip(element);
        });

        // Initialize modals
        container.querySelectorAll('[data-modal]').forEach(trigger => {
            this.initializeModal(trigger);
        });
    }

    initializeTooltip(element) {
        const tooltip = element.dataset.tooltip;
        element.title = tooltip;
    }

    initializeModal(trigger) {
        const modalId = trigger.dataset.modal;
        const modal = document.getElementById(modalId);
        
        if (modal) {
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                modal.classList.add('modal-open');
            });
        }
    }
}

// Initialize performance optimizer
document.addEventListener('DOMContentLoaded', () => {
    new PerformanceOptimizer();
});

// Add performance-related CSS
const performanceStyles = document.createElement('style');
performanceStyles.textContent = `
    @keyframes loading-progress {
        0% { transform: scaleX(0); }
        50% { transform: scaleX(0.7); }
        100% { transform: scaleX(1); }
    }
    
    .lazy {
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .lazy.loaded {
        opacity: 1;
    }
    
    .content-visible {
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .page-loader {
        transition: transform 0.2s ease;
    }
`;
document.head.appendChild(performanceStyles);

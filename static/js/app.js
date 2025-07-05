/**
 * Pentora Platform - Enhanced JavaScript Application
 * Modern UI/UX interactions, PWA functionality, and performance optimizations
 */

class PentoraApp {
    constructor() {
        this.isOnline = navigator.onLine;
        this.installPrompt = null;
        this.notificationPermission = 'default';
        
        this.init();
    }

    async init() {
        console.log('🎓 Pentora App initializing...');
        
        // Initialize core features
        this.setupEventListeners();
        this.setupPWA();
        this.setupPerformanceMonitoring();
        this.setupAccessibility();
        this.setupAnimations();
        
        // Initialize offline functionality
        if ('serviceWorker' in navigator) {
            await this.registerServiceWorker();
        }
        
        // Setup notifications
        await this.setupNotifications();
        
        console.log('✅ Pentora App initialized successfully');
    }

    setupEventListeners() {
        // Online/Offline status
        window.addEventListener('online', () => {
            this.isOnline = true;
            this.showNotification('You\'re back online!', 'success');
            this.syncOfflineData();
        });

        window.addEventListener('offline', () => {
            this.isOnline = false;
            this.showNotification('You\'re offline. Some features may be limited.', 'warning');
        });

        // PWA install prompt
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            this.installPrompt = e;
            this.showInstallButton();
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            this.handleKeyboardShortcuts(e);
        });

        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });

        // Enhanced form handling
        this.setupFormEnhancements();
        
        // Lazy loading for images
        this.setupLazyLoading();
    }

    async registerServiceWorker() {
        try {
            const registration = await navigator.serviceWorker.register('/static/sw.js');
            console.log('Service Worker registered:', registration);
            
            // Listen for updates
            registration.addEventListener('updatefound', () => {
                const newWorker = registration.installing;
                newWorker.addEventListener('statechange', () => {
                    if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                        this.showUpdateAvailable();
                    }
                });
            });
        } catch (error) {
            console.error('Service Worker registration failed:', error);
        }
    }

    setupPWA() {
        // Add to home screen prompt
        const installButton = document.getElementById('install-app');
        if (installButton) {
            installButton.addEventListener('click', () => {
                this.installApp();
            });
        }

        // Handle app shortcuts
        if ('navigator' in window && 'shortcuts' in navigator) {
            // PWA shortcuts are handled by the manifest
        }
    }

    async installApp() {
        if (this.installPrompt) {
            this.installPrompt.prompt();
            const result = await this.installPrompt.userChoice;
            
            if (result.outcome === 'accepted') {
                console.log('PWA installed');
                this.showNotification('App installed successfully!', 'success');
            }
            
            this.installPrompt = null;
            this.hideInstallButton();
        }
    }

    showInstallButton() {
        const installButton = document.getElementById('install-app');
        if (installButton) {
            installButton.style.display = 'block';
            installButton.classList.add('animate-bounce');
        }
    }

    hideInstallButton() {
        const installButton = document.getElementById('install-app');
        if (installButton) {
            installButton.style.display = 'none';
        }
    }

    async setupNotifications() {
        if ('Notification' in window) {
            this.notificationPermission = await Notification.requestPermission();
        }
    }

    showNotification(message, type = 'info', duration = 5000) {
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} fixed top-4 right-4 z-50 max-w-sm shadow-lg transform translate-x-full transition-transform duration-300`;
        toast.innerHTML = `
            <div class="flex items-center">
                <span>${message}</span>
                <button class="btn btn-sm btn-ghost ml-2" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        // Animate in
        setTimeout(() => {
            toast.classList.remove('translate-x-full');
        }, 100);
        
        // Auto remove
        setTimeout(() => {
            toast.classList.add('translate-x-full');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }

    setupFormEnhancements() {
        // Auto-save form data
        const forms = document.querySelectorAll('form[data-autosave]');
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                input.addEventListener('input', () => {
                    this.saveFormData(form.id, input.name, input.value);
                });
            });
            
            // Restore saved data
            this.restoreFormData(form);
        });

        // Enhanced validation
        const validatedForms = document.querySelectorAll('form[data-validate]');
        validatedForms.forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!this.validateForm(form)) {
                    e.preventDefault();
                }
            });
        });
    }

    saveFormData(formId, fieldName, value) {
        const key = `form_${formId}_${fieldName}`;
        localStorage.setItem(key, value);
    }

    restoreFormData(form) {
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            const key = `form_${form.id}_${input.name}`;
            const savedValue = localStorage.getItem(key);
            if (savedValue && !input.value) {
                input.value = savedValue;
            }
        });
    }

    validateForm(form) {
        let isValid = true;
        const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                this.showFieldError(input, 'This field is required');
                isValid = false;
            } else {
                this.clearFieldError(input);
            }
        });
        
        return isValid;
    }

    showFieldError(input, message) {
        input.classList.add('input-error');
        
        let errorElement = input.parentNode.querySelector('.field-error');
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.className = 'field-error text-red-500 text-sm mt-1';
            input.parentNode.appendChild(errorElement);
        }
        errorElement.textContent = message;
    }

    clearFieldError(input) {
        input.classList.remove('input-error');
        const errorElement = input.parentNode.querySelector('.field-error');
        if (errorElement) {
            errorElement.remove();
        }
    }

    setupLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        observer.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }

    setupPerformanceMonitoring() {
        // Only track performance on production or when explicitly enabled
        const shouldTrack = window.location.hostname !== '127.0.0.1' &&
                           window.location.hostname !== 'localhost' ||
                           localStorage.getItem('enablePerformanceTracking') === 'true';

        if (!shouldTrack) {
            console.log('Performance tracking disabled for development');
            return;
        }

        // Monitor page load performance (once per page load)
        window.addEventListener('load', () => {
            if ('performance' in window) {
                const perfData = performance.getEntriesByType('navigation')[0];
                const loadTime = perfData.loadEventEnd - perfData.fetchStart;
                console.log('Page load time:', loadTime, 'ms');

                // Only track if load time is significant (avoid noise)
                if (loadTime > 100) {
                    // Delay tracking to avoid interfering with page load
                    setTimeout(() => {
                        this.trackPerformance(perfData);
                    }, 2000);
                }
            }
        });

        // Monitor long tasks (less aggressive)
        if ('PerformanceObserver' in window) {
            const observer = new PerformanceObserver((list) => {
                list.getEntries().forEach((entry) => {
                    if (entry.duration > 100) { // Increased threshold
                        console.warn('Long task detected:', entry.duration, 'ms');

                        // Store for batch reporting
                        if (!window.performanceMetrics) {
                            window.performanceMetrics = {};
                        }
                        window.performanceMetrics.longTaskCount =
                            (window.performanceMetrics.longTaskCount || 0) + 1;
                    }
                });
            });
            observer.observe({ entryTypes: ['longtask'] });
        }
    }

    setupAccessibility() {
        // Skip link removed - handled by template if needed

        // Keyboard navigation improvements
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-navigation');
            }
        });

        document.addEventListener('mousedown', () => {
            document.body.classList.remove('keyboard-navigation');
        });
    }

    setupAnimations() {
        // Intersection Observer for scroll animations
        if ('IntersectionObserver' in window) {
            const animationObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('animate-in');
                    }
                });
            }, { threshold: 0.1 });

            document.querySelectorAll('.animate-on-scroll').forEach(el => {
                animationObserver.observe(el);
            });
        }
    }

    handleKeyboardShortcuts(e) {
        // Ctrl/Cmd + K for search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('#search-input');
            if (searchInput) {
                searchInput.focus();
            }
        }

        // Escape to close modals
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal.modal-open');
            if (openModal) {
                openModal.classList.remove('modal-open');
            }
        }
    }

    async syncOfflineData() {
        if ('serviceWorker' in navigator && 'sync' in window.ServiceWorkerRegistration.prototype) {
            const registration = await navigator.serviceWorker.ready;
            await registration.sync.register('quiz-submission');
            await registration.sync.register('progress-update');
        }
    }

    trackPerformance(perfData) {
        // Consolidated performance tracking with proper CSRF handling
        if (!this.isOnline) return;

        const csrfToken = this.getCSRFToken();
        if (!csrfToken) {
            console.warn('CSRF token not found, skipping performance tracking');
            return;
        }

        // Collect metrics from other monitoring systems
        const additionalMetrics = window.performanceMetrics || {};

        const performanceData = {
            // Core metrics
            loadTime: perfData.loadEventEnd - perfData.fetchStart,
            domContentLoaded: perfData.domContentLoadedEventEnd - perfData.fetchStart,
            firstPaint: performance.getEntriesByType('paint')[0]?.startTime || 0,

            // Additional metrics from performance optimizer
            ...additionalMetrics,

            // Page context
            url: window.location.href,
            timestamp: Date.now()
        };

        // Send with proper error handling and retry logic
        this.sendPerformanceData(performanceData, csrfToken);

        // Clear collected metrics
        window.performanceMetrics = {};
    }

    async sendPerformanceData(data, csrfToken, retryCount = 0) {
        try {
            const response = await fetch('/api/analytics/performance/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            console.log('Performance data sent successfully');
        } catch (error) {
            console.error('Performance tracking error:', error);

            // Retry once if it's a network error
            if (retryCount === 0 && error.name === 'TypeError') {
                setTimeout(() => {
                    this.sendPerformanceData(data, csrfToken, 1);
                }, 2000);
            }
        }
    }

    getCSRFToken() {
        // Try multiple methods to get CSRF token

        // Method 1: Form input
        const formToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
        if (formToken) return formToken;

        // Method 2: Meta tag
        const metaToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
        if (metaToken) return metaToken;

        // Method 3: Cookie
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }

        console.warn('CSRF token not found in form, meta tag, or cookie');
        return '';
    }

    showUpdateAvailable() {
        const updateBanner = document.createElement('div');
        updateBanner.className = 'fixed bottom-4 left-4 right-4 bg-blue-600 text-white p-4 rounded-lg shadow-lg z-50';
        updateBanner.innerHTML = `
            <div class="flex items-center justify-between">
                <span>A new version is available!</span>
                <button class="btn btn-sm btn-ghost text-white" onclick="window.location.reload()">
                    Update Now
                </button>
            </div>
        `;
        document.body.appendChild(updateBanner);
    }
}

// Initialize the app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.PentoraApp = new PentoraApp();
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PentoraApp;
}

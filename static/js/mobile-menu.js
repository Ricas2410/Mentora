/**
 * Professional Mobile Menu Handler
 * Handles mobile navigation with smooth animations and proper accessibility
 */

class MobileMenu {
    constructor() {
        this.isOpen = false;
        this.init();
    }

    init() {
        // Only initialize on mobile/tablet screens
        if (window.innerWidth < 1280) {
            this.bindEvents();
            this.setupAccessibility();
        }

        // Re-initialize on window resize if needed
        window.addEventListener('resize', () => {
            if (window.innerWidth >= 1280) {
                this.forceClose();
            }
        });
    }

    bindEvents() {
        // Mobile menu toggle button
        const toggleBtn = document.getElementById('mobile-menu-toggle');
        const closeBtn = document.getElementById('mobile-menu-close');
        const overlay = document.getElementById('mobile-menu-overlay');
        const sidebar = document.getElementById('mobile-menu-sidebar');

        if (toggleBtn) {
            toggleBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.toggle();
            });
        }

        if (closeBtn) {
            closeBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.close();
            });
        }

        if (overlay) {
            overlay.addEventListener('click', () => {
                this.close();
            });
        }

        // Close menu when clicking on navigation links
        const navLinks = document.querySelectorAll('.mobile-nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                // Small delay to allow navigation to start
                setTimeout(() => this.close(), 100);
            });
        });

        // Handle escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });

        // Handle window resize
        window.addEventListener('resize', () => {
            if (window.innerWidth >= 1280 && this.isOpen) {
                this.close();
            }
        });

        // Prevent body scroll when menu is open
        document.addEventListener('touchmove', (e) => {
            if (this.isOpen && !sidebar?.contains(e.target)) {
                e.preventDefault();
            }
        }, { passive: false });
    }

    setupAccessibility() {
        const toggleBtn = document.getElementById('mobile-menu-toggle');
        const sidebar = document.getElementById('mobile-menu-sidebar');

        if (toggleBtn && sidebar) {
            toggleBtn.setAttribute('aria-expanded', 'false');
            toggleBtn.setAttribute('aria-controls', 'mobile-menu-sidebar');
            sidebar.setAttribute('aria-hidden', 'true');
        }
    }

    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }

    open() {
        if (this.isOpen) return;

        const overlay = document.getElementById('mobile-menu-overlay');
        const sidebar = document.getElementById('mobile-menu-sidebar');
        const toggleBtn = document.getElementById('mobile-menu-toggle');
        const hamburgerIcon = document.getElementById('hamburger-icon');
        const closeIcon = document.getElementById('close-icon');

        // Show overlay
        if (overlay) {
            overlay.classList.remove('hidden');
            // Force reflow for animation
            overlay.offsetHeight;
            overlay.classList.add('opacity-50');
        }

        // Show sidebar
        if (sidebar) {
            sidebar.classList.remove('-translate-x-full');
            sidebar.setAttribute('aria-hidden', 'false');
        }

        // Update toggle button
        if (toggleBtn) {
            toggleBtn.setAttribute('aria-expanded', 'true');
        }

        // Switch icons
        if (hamburgerIcon && closeIcon) {
            hamburgerIcon.classList.add('hidden');
            closeIcon.classList.remove('hidden');
        }

        // Prevent body scroll
        document.body.style.overflow = 'hidden';
        
        this.isOpen = true;

        // Focus management
        setTimeout(() => {
            const firstFocusable = sidebar?.querySelector('a, button');
            if (firstFocusable) {
                firstFocusable.focus();
            }
        }, 300);
    }

    close() {
        if (!this.isOpen) return;

        const overlay = document.getElementById('mobile-menu-overlay');
        const sidebar = document.getElementById('mobile-menu-sidebar');
        const toggleBtn = document.getElementById('mobile-menu-toggle');
        const hamburgerIcon = document.getElementById('hamburger-icon');
        const closeIcon = document.getElementById('close-icon');

        // Hide overlay
        if (overlay) {
            overlay.classList.remove('opacity-50');
            setTimeout(() => {
                overlay.classList.add('hidden');
            }, 300);
        }

        // Hide sidebar
        if (sidebar) {
            sidebar.classList.add('-translate-x-full');
            sidebar.setAttribute('aria-hidden', 'true');
        }

        // Update toggle button
        if (toggleBtn) {
            toggleBtn.setAttribute('aria-expanded', 'false');
        }

        // Switch icons
        if (hamburgerIcon && closeIcon) {
            closeIcon.classList.add('hidden');
            hamburgerIcon.classList.remove('hidden');
        }

        // Restore body scroll
        document.body.style.overflow = '';
        
        this.isOpen = false;

        // Return focus to toggle button
        if (toggleBtn) {
            toggleBtn.focus();
        }
    }

    forceClose() {
        // Force close menu without animations for desktop
        const overlay = document.getElementById('mobile-menu-overlay');
        const sidebar = document.getElementById('mobile-menu-sidebar');
        const toggleBtn = document.getElementById('mobile-menu-toggle');
        const hamburgerIcon = document.getElementById('hamburger-icon');
        const closeIcon = document.getElementById('close-icon');

        if (overlay) {
            overlay.classList.add('hidden');
            overlay.classList.remove('opacity-50');
        }

        if (sidebar) {
            sidebar.classList.add('-translate-x-full');
            sidebar.setAttribute('aria-hidden', 'true');
        }

        if (toggleBtn) {
            toggleBtn.setAttribute('aria-expanded', 'false');
        }

        if (hamburgerIcon && closeIcon) {
            closeIcon.classList.add('hidden');
            hamburgerIcon.classList.remove('hidden');
        }

        document.body.style.overflow = '';
        this.isOpen = false;
    }
}

// Initialize mobile menu when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new MobileMenu();
});

// Handle page navigation - close menu if open
window.addEventListener('beforeunload', () => {
    document.body.style.overflow = '';
});

// Export for potential external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MobileMenu;
}

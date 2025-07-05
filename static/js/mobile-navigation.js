/**
 * Mobile Navigation Enhancement for Pentora Platform
 * Improves mobile user experience with better navigation patterns
 */

class MobileNavigationEnhancer {
    constructor() {
        this.init();
    }

    init() {
        this.setupMobileMenu();
        this.setupSwipeGestures();
        this.setupBottomNavigation();
        this.setupPullToRefresh();
        this.setupMobileSearch();
    }

    setupMobileMenu() {
        // Enhanced mobile menu with better UX
        const mobileMenuButton = document.querySelector('[data-mobile-menu-button]');
        const mobileMenu = document.querySelector('[data-mobile-menu]');
        
        if (mobileMenuButton && mobileMenu) {
            mobileMenuButton.addEventListener('click', () => {
                this.toggleMobileMenu(mobileMenu);
            });

            // Close menu when clicking outside
            document.addEventListener('click', (e) => {
                if (!mobileMenu.contains(e.target) && !mobileMenuButton.contains(e.target)) {
                    this.closeMobileMenu(mobileMenu);
                }
            });

            // Close menu on escape key
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    this.closeMobileMenu(mobileMenu);
                }
            });
        }
    }

    toggleMobileMenu(menu) {
        const isOpen = menu.classList.contains('open');
        
        if (isOpen) {
            this.closeMobileMenu(menu);
        } else {
            this.openMobileMenu(menu);
        }
    }

    openMobileMenu(menu) {
        menu.classList.add('open');
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
        
        // Add backdrop
        const backdrop = document.createElement('div');
        backdrop.className = 'mobile-menu-backdrop fixed inset-0 bg-black bg-opacity-50 z-40';
        backdrop.addEventListener('click', () => this.closeMobileMenu(menu));
        document.body.appendChild(backdrop);
        
        // Animate menu items
        const menuItems = menu.querySelectorAll('li');
        menuItems.forEach((item, index) => {
            item.style.animationDelay = `${index * 0.1}s`;
            item.classList.add('animate-slide-in');
        });
    }

    closeMobileMenu(menu) {
        menu.classList.remove('open');
        document.body.style.overflow = ''; // Restore scrolling
        
        // Remove backdrop
        const backdrop = document.querySelector('.mobile-menu-backdrop');
        if (backdrop) {
            backdrop.remove();
        }
        
        // Remove animations
        const menuItems = menu.querySelectorAll('li');
        menuItems.forEach(item => {
            item.classList.remove('animate-slide-in');
            item.style.animationDelay = '';
        });
    }

    setupSwipeGestures() {
        let startX = 0;
        let startY = 0;
        let isSwipeDetected = false;

        document.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
            isSwipeDetected = false;
        });

        document.addEventListener('touchmove', (e) => {
            if (!startX || !startY) return;

            const currentX = e.touches[0].clientX;
            const currentY = e.touches[0].clientY;
            
            const diffX = startX - currentX;
            const diffY = startY - currentY;

            // Detect horizontal swipe
            if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
                isSwipeDetected = true;
                
                if (diffX > 0) {
                    // Swipe left - next page/section
                    this.handleSwipeLeft();
                } else {
                    // Swipe right - previous page/section or open menu
                    this.handleSwipeRight();
                }
            }
        });

        document.addEventListener('touchend', () => {
            startX = 0;
            startY = 0;
            isSwipeDetected = false;
        });
    }

    handleSwipeLeft() {
        // Handle swipe left gesture
        const nextButton = document.querySelector('.btn-next, [data-next]');
        if (nextButton && !nextButton.disabled) {
            nextButton.click();
        }
    }

    handleSwipeRight() {
        // Handle swipe right gesture
        if (window.innerWidth <= 768) {
            const mobileMenu = document.querySelector('[data-mobile-menu]');
            if (mobileMenu && !mobileMenu.classList.contains('open')) {
                this.openMobileMenu(mobileMenu);
                return;
            }
        }
        
        const prevButton = document.querySelector('.btn-prev, [data-prev]');
        if (prevButton && !prevButton.disabled) {
            prevButton.click();
        }
    }

    setupBottomNavigation() {
        // Create floating bottom navigation for mobile
        if (window.innerWidth <= 768) {
            this.createBottomNavigation();
        }

        // Update on resize
        window.addEventListener('resize', () => {
            const existingBottomNav = document.querySelector('.bottom-navigation');
            if (window.innerWidth <= 768 && !existingBottomNav) {
                this.createBottomNavigation();
            } else if (window.innerWidth > 768 && existingBottomNav) {
                existingBottomNav.remove();
            }
        });
    }

    createBottomNavigation() {
        const bottomNav = document.createElement('div');
        bottomNav.className = 'bottom-navigation fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-50 safe-area-bottom';
        
        const navItems = [
            { icon: 'fas fa-home', label: 'Home', url: '/', active: window.location.pathname === '/' },
            { icon: 'fas fa-book', label: 'Learn', url: '/subjects/', active: window.location.pathname.includes('/subjects/') },
            { icon: 'fas fa-quiz', label: 'Quiz', url: '/quiz/', active: window.location.pathname.includes('/quiz/') },
            { icon: 'fas fa-user', label: 'Profile', url: '/profile/', active: window.location.pathname.includes('/profile/') }
        ];

        bottomNav.innerHTML = `
            <div class="flex justify-around items-center py-2">
                ${navItems.map(item => `
                    <a href="${item.url}" class="bottom-nav-item flex flex-col items-center py-1 px-2 text-xs ${item.active ? 'text-blue-600' : 'text-gray-600'} transition-colors">
                        <i class="${item.icon} text-lg mb-1"></i>
                        <span>${item.label}</span>
                    </a>
                `).join('')}
            </div>
        `;

        document.body.appendChild(bottomNav);

        // Add padding to body to account for bottom navigation
        document.body.style.paddingBottom = '70px';
    }

    setupPullToRefresh() {
        let startY = 0;
        let pullDistance = 0;
        let isPulling = false;
        let refreshThreshold = 80;

        const pullToRefreshIndicator = document.createElement('div');
        pullToRefreshIndicator.className = 'pull-to-refresh fixed top-0 left-0 right-0 bg-blue-600 text-white text-center py-2 transform -translate-y-full transition-transform z-50';
        pullToRefreshIndicator.innerHTML = '<i class="fas fa-arrow-down mr-2"></i>Pull to refresh';
        document.body.appendChild(pullToRefreshIndicator);

        document.addEventListener('touchstart', (e) => {
            if (window.scrollY === 0) {
                startY = e.touches[0].clientY;
                isPulling = true;
            }
        });

        document.addEventListener('touchmove', (e) => {
            if (!isPulling || window.scrollY > 0) return;

            const currentY = e.touches[0].clientY;
            pullDistance = Math.max(0, currentY - startY);

            if (pullDistance > 10) {
                e.preventDefault(); // Prevent default scroll behavior
                
                const progress = Math.min(pullDistance / refreshThreshold, 1);
                pullToRefreshIndicator.style.transform = `translateY(${progress * 100 - 100}%)`;
                
                if (pullDistance >= refreshThreshold) {
                    pullToRefreshIndicator.innerHTML = '<i class="fas fa-sync-alt mr-2"></i>Release to refresh';
                    pullToRefreshIndicator.classList.add('bg-green-600');
                    pullToRefreshIndicator.classList.remove('bg-blue-600');
                } else {
                    pullToRefreshIndicator.innerHTML = '<i class="fas fa-arrow-down mr-2"></i>Pull to refresh';
                    pullToRefreshIndicator.classList.add('bg-blue-600');
                    pullToRefreshIndicator.classList.remove('bg-green-600');
                }
            }
        });

        document.addEventListener('touchend', () => {
            if (isPulling && pullDistance >= refreshThreshold) {
                this.performRefresh();
            }
            
            isPulling = false;
            pullDistance = 0;
            pullToRefreshIndicator.style.transform = 'translateY(-100%)';
            pullToRefreshIndicator.classList.add('bg-blue-600');
            pullToRefreshIndicator.classList.remove('bg-green-600');
        });
    }

    performRefresh() {
        const indicator = document.querySelector('.pull-to-refresh');
        indicator.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Refreshing...';
        indicator.style.transform = 'translateY(0%)';
        
        // Simulate refresh (replace with actual refresh logic)
        setTimeout(() => {
            window.location.reload();
        }, 1000);
    }

    setupMobileSearch() {
        // Enhanced mobile search experience
        const searchInput = document.querySelector('input[type="search"], #search-input');
        
        if (searchInput) {
            // Create mobile search overlay
            const searchOverlay = document.createElement('div');
            searchOverlay.className = 'mobile-search-overlay fixed inset-0 bg-white z-50 transform translate-y-full transition-transform';
            searchOverlay.innerHTML = `
                <div class="p-4">
                    <div class="flex items-center mb-4">
                        <button class="mobile-search-close mr-3 p-2">
                            <i class="fas fa-arrow-left text-xl"></i>
                        </button>
                        <input type="search" class="mobile-search-input flex-1 p-3 border border-gray-300 rounded-lg text-lg" placeholder="Search...">
                    </div>
                    <div class="mobile-search-results">
                        <!-- Search results will be populated here -->
                    </div>
                </div>
            `;
            
            document.body.appendChild(searchOverlay);
            
            const mobileSearchInput = searchOverlay.querySelector('.mobile-search-input');
            const closeButton = searchOverlay.querySelector('.mobile-search-close');
            
            // Show mobile search on focus (mobile only)
            if (window.innerWidth <= 768) {
                searchInput.addEventListener('focus', (e) => {
                    e.preventDefault();
                    searchInput.blur();
                    this.showMobileSearch(searchOverlay, mobileSearchInput);
                });
            }
            
            closeButton.addEventListener('click', () => {
                this.hideMobileSearch(searchOverlay);
            });
            
            // Handle search input
            mobileSearchInput.addEventListener('input', (e) => {
                this.handleMobileSearch(e.target.value, searchOverlay);
            });
        }
    }

    showMobileSearch(overlay, input) {
        overlay.style.transform = 'translateY(0)';
        document.body.style.overflow = 'hidden';
        
        // Focus input after animation
        setTimeout(() => {
            input.focus();
        }, 300);
    }

    hideMobileSearch(overlay) {
        overlay.style.transform = 'translateY(100%)';
        document.body.style.overflow = '';
    }

    handleMobileSearch(query, overlay) {
        const resultsContainer = overlay.querySelector('.mobile-search-results');
        
        if (query.length < 2) {
            resultsContainer.innerHTML = '';
            return;
        }
        
        // Show loading state
        resultsContainer.innerHTML = '<div class="text-center py-4"><i class="fas fa-spinner fa-spin"></i> Searching...</div>';
        
        // Simulate search (replace with actual search API call)
        setTimeout(() => {
            const mockResults = [
                { title: 'Mathematics - Grade 5', url: '/subjects/math/grade-5/' },
                { title: 'English Grammar', url: '/subjects/english/grammar/' },
                { title: 'Science Basics', url: '/subjects/science/basics/' }
            ];
            
            resultsContainer.innerHTML = mockResults.map(result => `
                <a href="${result.url}" class="block p-3 border-b border-gray-200 hover:bg-gray-50">
                    <div class="font-medium">${result.title}</div>
                </a>
            `).join('');
        }, 500);
    }
}

// Initialize mobile navigation enhancements
document.addEventListener('DOMContentLoaded', () => {
    new MobileNavigationEnhancer();
});

// Add mobile-specific CSS
const mobileStyles = document.createElement('style');
mobileStyles.textContent = `
    @media (max-width: 768px) {
        .animate-slide-in {
            animation: slideInFromRight 0.3s ease-out forwards;
        }
        
        @keyframes slideInFromRight {
            from {
                opacity: 0;
                transform: translateX(20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .bottom-nav-item:active {
            transform: scale(0.95);
        }
        
        .safe-area-bottom {
            padding-bottom: env(safe-area-inset-bottom);
        }
        
        .mobile-search-overlay {
            top: 0;
            height: 100vh;
            height: 100dvh; /* Dynamic viewport height for mobile */
        }
        
        .pull-to-refresh {
            backdrop-filter: blur(10px);
        }
    }
    
    /* Improve touch targets */
    @media (pointer: coarse) {
        button, .btn, a {
            min-height: 44px;
            min-width: 44px;
        }
    }
    
    /* Reduce motion for users who prefer it */
    @media (prefers-reduced-motion: reduce) {
        * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
`;
document.head.appendChild(mobileStyles);

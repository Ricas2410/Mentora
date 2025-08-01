/**
 * UX/UI Enhancement Script for Pentora Platform
 * Adds interactive features, accessibility improvements, and user experience enhancements
 */

class PentoraUXEnhancements {
    constructor() {
        this.init();
    }

    init() {
        this.setupAccessibilityFeatures();
        this.setupInteractiveElements();
        this.setupFormEnhancements();
        this.setupNavigationEnhancements();
        this.setupProgressTracking();
        this.setupTooltips();
        this.setupKeyboardShortcuts();
        this.setupScrollEnhancements();
        this.addEnhancementStyles();
    }

    setupAccessibilityFeatures() {
        // Add skip links for keyboard navigation
        this.addSkipLinks();
        
        // Enhance focus management
        this.enhanceFocusManagement();
        
        // Add ARIA labels where missing
        this.addAriaLabels();
        
        // High contrast mode toggle removed
    }

    addSkipLinks() {
        // Skip links removed - handled by template
    }

    enhanceFocusManagement() {
        // Add visible focus indicators
        const style = document.createElement('style');
        style.textContent = `
            .focus-visible:focus {
                outline: 2px solid #3b82f6;
                outline-offset: 2px;
                border-radius: 4px;
            }
            
            .keyboard-navigation *:focus {
                outline: 2px solid #3b82f6;
                outline-offset: 2px;
            }
        `;
        document.head.appendChild(style);

        // Track keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-navigation');
            }
        });

        document.addEventListener('mousedown', () => {
            document.body.classList.remove('keyboard-navigation');
        });
    }

    addAriaLabels() {
        // Add aria-labels to buttons without text
        document.querySelectorAll('button:not([aria-label])').forEach(button => {
            const icon = button.querySelector('i[class*="fa-"]');
            if (icon && !button.textContent.trim()) {
                const iconClass = Array.from(icon.classList).find(cls => cls.startsWith('fa-'));
                if (iconClass) {
                    const label = this.getAriaLabelFromIcon(iconClass);
                    if (label) {
                        button.setAttribute('aria-label', label);
                    }
                }
            }
        });
    }

    getAriaLabelFromIcon(iconClass) {
        const iconLabels = {
            'fa-home': 'Home',
            'fa-user': 'User profile',
            'fa-search': 'Search',
            'fa-menu': 'Menu',
            'fa-close': 'Close',
            'fa-edit': 'Edit',
            'fa-delete': 'Delete',
            'fa-play': 'Play',
            'fa-pause': 'Pause',
            'fa-heart': 'Like',
            'fa-share': 'Share',
            'fa-download': 'Download',
            'fa-upload': 'Upload',
            'fa-settings': 'Settings',
            'fa-help': 'Help',
            'fa-info': 'Information'
        };
        return iconLabels[iconClass] || null;
    }



    setupInteractiveElements() {
        // Add loading states to buttons
        this.enhanceButtons();
        
        // Add hover effects to cards
        this.enhanceCards();
        
        // Add smooth transitions
        this.addSmoothTransitions();
    }

    enhanceButtons() {
        // Disable automatic button loading to prevent conflicts
        // Individual forms will handle their own loading states
        console.log('Button enhancements disabled to prevent conflicts with form-specific handlers');
        return;

        document.querySelectorAll('button[type="submit"], .btn-primary').forEach(button => {
            // Only add loading if the button doesn't have a custom handler
            if (!button.hasAttribute('data-custom-loading')) {
                button.addEventListener('click', (e) => {
                    if (!button.disabled) {
                        button.classList.add('loading');
                        button.disabled = true;

                        const originalText = button.innerHTML;
                        button.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Loading...';

                        // Re-enable after 3 seconds (adjust based on your needs)
                        setTimeout(() => {
                            button.classList.remove('loading');
                            button.disabled = false;
                            button.innerHTML = originalText;
                        }, 3000);
                    }
                });
            }
        });
    }

    enhanceCards() {
        document.querySelectorAll('.card, .subject-card, .dashboard-card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-2px)';
                card.style.boxShadow = '0 10px 25px rgba(0,0,0,0.15)';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0)';
                card.style.boxShadow = '';
            });
        });
    }

    addSmoothTransitions() {
        const style = document.createElement('style');
        style.textContent = `
            * {
                transition: transform 0.2s ease, box-shadow 0.2s ease, opacity 0.2s ease;
            }
            
            .smooth-scroll {
                scroll-behavior: smooth;
            }
        `;
        document.head.appendChild(style);
        document.documentElement.classList.add('smooth-scroll');
    }

    setupNavigationEnhancements() {
        // Add mobile menu toggle functionality
        this.setupMobileMenu();

        // Add breadcrumb navigation
        this.setupBreadcrumbs();

        // Add active navigation highlighting
        this.highlightActiveNavigation();

        // Add navigation keyboard support
        this.setupNavigationKeyboard();
    }

    setupMobileMenu() {
        const mobileMenuToggle = document.querySelector('.mobile-menu-toggle, .navbar-toggler');
        const mobileMenu = document.querySelector('.mobile-menu, .navbar-collapse');

        if (mobileMenuToggle && mobileMenu) {
            mobileMenuToggle.addEventListener('click', () => {
                mobileMenu.classList.toggle('show');
                mobileMenuToggle.setAttribute('aria-expanded',
                    mobileMenu.classList.contains('show') ? 'true' : 'false'
                );
            });

            // Close mobile menu when clicking outside
            document.addEventListener('click', (e) => {
                if (!mobileMenuToggle.contains(e.target) && !mobileMenu.contains(e.target)) {
                    mobileMenu.classList.remove('show');
                    mobileMenuToggle.setAttribute('aria-expanded', 'false');
                }
            });
        }
    }

    setupBreadcrumbs() {
        // Add breadcrumb navigation based on current page
        const breadcrumbContainer = document.querySelector('.breadcrumb-container');
        if (breadcrumbContainer) {
            const currentPath = window.location.pathname;
            const breadcrumbs = this.generateBreadcrumbs(currentPath);
            breadcrumbContainer.innerHTML = breadcrumbs;
        }
    }

    generateBreadcrumbs(path) {
        const pathSegments = path.split('/').filter(segment => segment);
        let breadcrumbHTML = '<nav aria-label="breadcrumb"><ol class="breadcrumb">';

        breadcrumbHTML += '<li class="breadcrumb-item"><a href="/">Home</a></li>';

        let currentPath = '';
        pathSegments.forEach((segment, index) => {
            currentPath += '/' + segment;
            const isLast = index === pathSegments.length - 1;
            const segmentName = this.formatBreadcrumbName(segment);

            if (isLast) {
                breadcrumbHTML += `<li class="breadcrumb-item active" aria-current="page">${segmentName}</li>`;
            } else {
                breadcrumbHTML += `<li class="breadcrumb-item"><a href="${currentPath}">${segmentName}</a></li>`;
            }
        });

        breadcrumbHTML += '</ol></nav>';
        return breadcrumbHTML;
    }

    formatBreadcrumbName(segment) {
        const nameMap = {
            'dashboard': 'Dashboard',
            'quiz': 'Quiz',
            'learn': 'Learn',
            'profile': 'Profile',
            'settings': 'Settings'
        };

        return nameMap[segment] || segment.charAt(0).toUpperCase() + segment.slice(1);
    }

    highlightActiveNavigation() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.nav-link, .navbar-nav a');

        navLinks.forEach(link => {
            const linkPath = new URL(link.href).pathname;
            if (linkPath === currentPath || (currentPath.startsWith(linkPath) && linkPath !== '/')) {
                link.classList.add('active');
                link.setAttribute('aria-current', 'page');
            }
        });
    }

    setupNavigationKeyboard() {
        // Add keyboard navigation support for dropdown menus
        const dropdownToggles = document.querySelectorAll('.dropdown-toggle');

        dropdownToggles.forEach(toggle => {
            toggle.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    toggle.click();
                }

                if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    const dropdown = toggle.nextElementSibling;
                    if (dropdown) {
                        const firstLink = dropdown.querySelector('a, button');
                        if (firstLink) firstLink.focus();
                    }
                }
            });
        });
    }

    setupFormEnhancements() {
        // Add real-time validation
        this.addRealTimeValidation();

        // Add password strength indicator
        this.addPasswordStrengthIndicator();

        // Add form auto-save
        this.addFormAutoSave();
    }

    addRealTimeValidation() {
        document.querySelectorAll('input[required]').forEach(input => {
            input.addEventListener('blur', () => {
                this.validateField(input);
            });
            
            input.addEventListener('input', () => {
                if (input.classList.contains('invalid')) {
                    this.validateField(input);
                }
            });
        });
    }

    validateField(input) {
        const isValid = input.checkValidity();
        
        if (isValid) {
            input.classList.remove('invalid');
            input.classList.add('valid');
            this.removeFieldError(input);
        } else {
            input.classList.remove('valid');
            input.classList.add('invalid');
            this.showFieldError(input, input.validationMessage);
        }
    }

    showFieldError(input, message) {
        this.removeFieldError(input);
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error text-red-500 text-sm mt-1';
        errorDiv.textContent = message;
        
        input.parentNode.appendChild(errorDiv);
    }

    removeFieldError(input) {
        const existingError = input.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
    }

    addPasswordStrengthIndicator() {
        document.querySelectorAll('input[type="password"]').forEach(passwordInput => {
            if (passwordInput.name === 'password1' || passwordInput.name === 'password') {
                const strengthIndicator = document.createElement('div');
                strengthIndicator.className = 'password-strength mt-2';
                strengthIndicator.innerHTML = `
                    <div class="strength-bar">
                        <div class="strength-fill"></div>
                    </div>
                    <div class="strength-text text-sm mt-1"></div>
                `;
                
                passwordInput.parentNode.appendChild(strengthIndicator);
                
                passwordInput.addEventListener('input', () => {
                    this.updatePasswordStrength(passwordInput, strengthIndicator);
                });
            }
        });
    }

    updatePasswordStrength(input, indicator) {
        const password = input.value;
        const strength = this.calculatePasswordStrength(password);
        
        const fill = indicator.querySelector('.strength-fill');
        const text = indicator.querySelector('.strength-text');
        
        fill.style.width = `${strength.percentage}%`;
        fill.className = `strength-fill ${strength.class}`;
        text.textContent = strength.text;
        text.className = `strength-text text-sm mt-1 ${strength.class}`;
    }

    calculatePasswordStrength(password) {
        let score = 0;
        
        if (password.length >= 8) score += 25;
        if (/[a-z]/.test(password)) score += 25;
        if (/[A-Z]/.test(password)) score += 25;
        if (/[0-9]/.test(password)) score += 25;
        if (/[^A-Za-z0-9]/.test(password)) score += 25;
        
        if (score <= 25) return { percentage: 25, class: 'text-red-500', text: 'Weak' };
        if (score <= 50) return { percentage: 50, class: 'text-orange-500', text: 'Fair' };
        if (score <= 75) return { percentage: 75, class: 'text-yellow-500', text: 'Good' };
        return { percentage: 100, class: 'text-green-500', text: 'Strong' };
    }

    addFormAutoSave() {
        document.querySelectorAll('form[data-autosave]').forEach(form => {
            const inputs = form.querySelectorAll('input, textarea, select');
            
            inputs.forEach(input => {
                input.addEventListener('input', () => {
                    this.saveFormData(form.id, input.name, input.value);
                });
            });
            
            this.restoreFormData(form);
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

    setupTooltips() {
        // Add tooltips to elements with title attributes
        document.querySelectorAll('[title]').forEach(element => {
            this.createTooltip(element);
        });
    }

    createTooltip(element) {
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip absolute bg-gray-800 text-white text-sm px-2 py-1 rounded shadow-lg z-50 opacity-0 pointer-events-none transition-opacity';
        tooltip.textContent = element.title;
        
        document.body.appendChild(tooltip);
        
        element.addEventListener('mouseenter', (e) => {
            const rect = element.getBoundingClientRect();
            tooltip.style.left = `${rect.left + rect.width / 2}px`;
            tooltip.style.top = `${rect.top - tooltip.offsetHeight - 5}px`;
            tooltip.style.transform = 'translateX(-50%)';
            tooltip.style.opacity = '1';
        });
        
        element.addEventListener('mouseleave', () => {
            tooltip.style.opacity = '0';
        });
        
        // Remove title to prevent default tooltip
        element.removeAttribute('title');
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + K for search
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                const searchInput = document.querySelector('#search-input, input[type="search"]');
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
        });
    }

    setupScrollEnhancements() {
        // Scroll-to-top button removed

        // Add scroll progress indicator
        this.addScrollProgressIndicator();
    }

  

    addScrollProgressIndicator() {
        const progressBar = document.createElement('div');
        progressBar.className = 'fixed top-0 left-0 w-full h-1 bg-blue-600 z-50 transform scale-x-0 origin-left transition-transform';
        
        window.addEventListener('scroll', () => {
            const scrollPercent = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
            progressBar.style.transform = `scaleX(${scrollPercent / 100})`;
        });
        
        document.body.appendChild(progressBar);
    }

    setupProgressTracking() {
        // Track reading progress on long content
        this.trackReadingProgress();
    }

    trackReadingProgress() {
        const contentElements = document.querySelectorAll('.content, .study-content, article');
        
        contentElements.forEach(content => {
            if (content.scrollHeight > window.innerHeight * 2) {
                this.addReadingProgressBar(content);
            }
        });
    }

    addReadingProgressBar(content) {
        const progressBar = document.createElement('div');
        progressBar.className = 'reading-progress fixed top-16 left-0 w-full h-1 bg-green-500 z-40 transform scale-x-0 origin-left transition-transform';
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const rect = entry.boundingClientRect;
                    const progress = Math.max(0, Math.min(1, (window.innerHeight - rect.top) / rect.height));
                    progressBar.style.transform = `scaleX(${progress})`;
                }
            });
        }, { threshold: 0 });
        
        observer.observe(content);
        document.body.appendChild(progressBar);
    }

    // Add CSS for enhanced styles
    addEnhancementStyles() {
        const enhancementStyles = document.createElement('style');
        enhancementStyles.textContent = `
            .field-error {
                animation: shake 0.3s ease-in-out;
            }

            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-5px); }
                75% { transform: translateX(5px); }
            }

            .strength-bar {
                width: 100%;
                height: 4px;
                background: #e5e7eb;
                border-radius: 2px;
                overflow: hidden;
            }

            .strength-fill {
                height: 100%;
                transition: width 0.3s ease, background-color 0.3s ease;
                background: #ef4444;
            }

            .strength-fill.text-orange-500 { background: #f97316; }
            .strength-fill.text-yellow-500 { background: #eab308; }
            .strength-fill.text-green-500 { background: #22c55e; }

            .loading {
                pointer-events: none;
                opacity: 0.7;
            }

            input.valid {
                border-color: #22c55e;
                box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1);
            }

            input.invalid {
                border-color: #ef4444;
                box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
            }
        `;
        document.head.appendChild(enhancementStyles);
    }
}

// Initialize UX enhancements when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new PentoraUXEnhancements();
});

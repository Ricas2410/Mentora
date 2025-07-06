/**
 * Enhanced UI Interactions for Pentora Platform
 * Adds modern micro-interactions and improved user feedback
 */

class UIInteractions {
    constructor() {
        this.init();
    }

    init() {
        this.setupCardInteractions();
        this.setupButtonInteractions();
        this.setupFormEnhancements();
        this.setupLoadingStates();
        this.setupTooltips();
        this.setupProgressAnimations();
        this.setupMicroInteractions();
    }

    setupCardInteractions() {
        // Enhanced card hover effects
        document.querySelectorAll('.quiz-card, .subject-card, .topic-card, .feature-card').forEach(card => {
            card.addEventListener('mouseenter', (e) => {
                this.addCardHoverEffect(e.target);
            });

            card.addEventListener('mouseleave', (e) => {
                this.removeCardHoverEffect(e.target);
            });

            // Touch feedback for mobile
            card.addEventListener('touchstart', (e) => {
                this.addTouchFeedback(e.target);
            });

            card.addEventListener('touchend', (e) => {
                this.removeTouchFeedback(e.target);
            });
        });
    }

    addCardHoverEffect(card) {
        card.style.transform = 'translateY(-4px) scale(1.02)';
        card.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(59, 130, 246, 0.2)';
        card.style.borderColor = 'rgba(59, 130, 246, 0.3)';
    }

    removeCardHoverEffect(card) {
        card.style.transform = '';
        card.style.boxShadow = '';
        card.style.borderColor = '';
    }

    addTouchFeedback(element) {
        element.style.transform = 'scale(0.98)';
        element.style.transition = 'transform 0.1s ease';
    }

    removeTouchFeedback(element) {
        setTimeout(() => {
            element.style.transform = '';
            element.style.transition = '';
        }, 100);
    }

    setupButtonInteractions() {
        // Enhanced button interactions
        document.querySelectorAll('.btn, .start-exam-btn, button[type="submit"]').forEach(button => {
            button.addEventListener('click', (e) => {
                this.createRippleEffect(e);
                this.addButtonClickFeedback(e.target);
            });

            // Disable automatic loading state to prevent conflicts
            // Individual forms will handle their own loading states
            if (button.type === 'submit' && button.hasAttribute('data-auto-loading')) {
                button.addEventListener('click', (e) => {
                    this.showButtonLoading(e.target);
                });
            }
        });
    }

    createRippleEffect(e) {
        const button = e.currentTarget;
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        const ripple = document.createElement('span');
        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s ease-out;
            pointer-events: none;
        `;

        // Add ripple animation CSS if not exists
        if (!document.querySelector('#ripple-styles')) {
            const style = document.createElement('style');
            style.id = 'ripple-styles';
            style.textContent = `
                @keyframes ripple {
                    to {
                        transform: scale(2);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }

        button.style.position = 'relative';
        button.style.overflow = 'hidden';
        button.appendChild(ripple);

        setTimeout(() => {
            ripple.remove();
        }, 600);
    }

    addButtonClickFeedback(button) {
        button.classList.add('micro-bounce');
        setTimeout(() => {
            button.classList.remove('micro-bounce');
        }, 600);
    }

    showButtonLoading(button) {
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Loading...';
        button.disabled = true;
        button.dataset.originalText = originalText;

        // Auto-restore after 3 seconds (adjust based on your needs)
        setTimeout(() => {
            this.hideButtonLoading(button);
        }, 3000);
    }

    hideButtonLoading(button) {
        if (button.dataset.originalText) {
            button.innerHTML = button.dataset.originalText;
            button.disabled = false;
            delete button.dataset.originalText;
        }
    }

    setupFormEnhancements() {
        // Enhanced form field interactions
        document.querySelectorAll('input, textarea, select').forEach(field => {
            field.addEventListener('focus', (e) => {
                this.addFieldFocusEffect(e.target);
            });

            field.addEventListener('blur', (e) => {
                this.removeFieldFocusEffect(e.target);
                this.validateField(e.target);
            });

            field.addEventListener('input', (e) => {
                this.addFieldInputEffect(e.target);
            });
        });
    }

    addFieldFocusEffect(field) {
        field.classList.add('form-input-enhanced');
        field.style.transform = 'scale(1.02)';
        field.style.transition = 'all 0.3s ease';
    }

    removeFieldFocusEffect(field) {
        field.style.transform = '';
    }

    addFieldInputEffect(field) {
        // Add subtle glow effect while typing
        field.style.boxShadow = '0 0 0 4px rgba(59, 130, 246, 0.1)';
        
        clearTimeout(field.inputTimeout);
        field.inputTimeout = setTimeout(() => {
            field.style.boxShadow = '';
        }, 1000);
    }

    validateField(field) {
        if (field.required && !field.value.trim()) {
            field.classList.add('error');
            field.classList.remove('success');
        } else if (field.value.trim()) {
            field.classList.add('success');
            field.classList.remove('error');
        } else {
            field.classList.remove('error', 'success');
        }
    }

    setupLoadingStates() {
        // Add loading skeletons for dynamic content
        this.createLoadingSkeletons();
        
        // Intersection Observer for lazy loading animations
        if ('IntersectionObserver' in window) {
            this.setupLazyAnimations();
        }
    }

    createLoadingSkeletons() {
        document.querySelectorAll('[data-loading]').forEach(element => {
            if (element.children.length === 0) {
                element.classList.add('loading-skeleton');
            }
        });
    }

    setupLazyAnimations() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.quiz-card, .subject-card, .topic-card').forEach(card => {
            observer.observe(card);
        });
    }

    setupTooltips() {
        // Enhanced tooltips
        document.querySelectorAll('[title]').forEach(element => {
            const title = element.title;
            element.removeAttribute('title');
            element.setAttribute('data-tooltip', title);
            element.classList.add('tooltip-enhanced');
        });

        // Add tooltips to buttons without text
        document.querySelectorAll('button:not([data-tooltip])').forEach(button => {
            const icon = button.querySelector('i[class*="fa-"]');
            if (icon && !button.textContent.trim()) {
                const tooltip = this.getTooltipFromIcon(icon.className);
                if (tooltip) {
                    button.setAttribute('data-tooltip', tooltip);
                    button.classList.add('tooltip-enhanced');
                }
            }
        });
    }

    getTooltipFromIcon(iconClass) {
        const tooltips = {
            'fa-play': 'Start',
            'fa-pause': 'Pause',
            'fa-stop': 'Stop',
            'fa-edit': 'Edit',
            'fa-delete': 'Delete',
            'fa-trash': 'Delete',
            'fa-heart': 'Like',
            'fa-share': 'Share',
            'fa-download': 'Download',
            'fa-upload': 'Upload',
            'fa-search': 'Search',
            'fa-filter': 'Filter',
            'fa-sort': 'Sort',
            'fa-refresh': 'Refresh',
            'fa-sync': 'Sync',
            'fa-settings': 'Settings',
            'fa-cog': 'Settings',
            'fa-user': 'Profile',
            'fa-home': 'Home',
            'fa-back': 'Back',
            'fa-forward': 'Forward',
            'fa-close': 'Close',
            'fa-times': 'Close'
        };

        for (const [iconName, tooltip] of Object.entries(tooltips)) {
            if (iconClass.includes(iconName)) {
                return tooltip;
            }
        }
        return null;
    }

    setupProgressAnimations() {
        // Animate progress bars
        document.querySelectorAll('.progress-bar, .progress-bar-enhanced').forEach(progressBar => {
            const fill = progressBar.querySelector('.progress-fill, .progress-fill-enhanced');
            if (fill) {
                const targetWidth = fill.style.width || fill.getAttribute('data-width') || '0%';
                fill.style.width = '0%';
                
                setTimeout(() => {
                    fill.style.width = targetWidth;
                }, 100);
            }
        });
    }

    setupMicroInteractions() {
        // Add micro-interactions to various elements
        this.setupHoverGlow();
        this.setupClickPulse();
        this.setupScrollAnimations();
    }

    setupHoverGlow() {
        document.querySelectorAll('.btn-primary, .start-exam-btn').forEach(element => {
            element.addEventListener('mouseenter', () => {
                element.classList.add('micro-glow');
            });

            element.addEventListener('mouseleave', () => {
                element.classList.remove('micro-glow');
            });
        });
    }

    setupClickPulse() {
        document.querySelectorAll('.quiz-card, .subject-card, .topic-card').forEach(card => {
            card.addEventListener('click', () => {
                card.classList.add('micro-pulse');
                setTimeout(() => {
                    card.classList.remove('micro-pulse');
                }, 2000);
            });
        });
    }

    setupScrollAnimations() {
        // Add scroll-triggered animations
        if ('IntersectionObserver' in window) {
            const scrollObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }
                });
            }, { threshold: 0.1 });

            document.querySelectorAll('.quiz-card, .subject-card, .topic-card').forEach((card, index) => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                card.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
                scrollObserver.observe(card);
            });
        }
    }

    // Utility methods
    showSuccessFeedback(message, element = document.body) {
        const feedback = document.createElement('div');
        feedback.className = 'success-feedback fixed top-4 right-4 z-50 max-w-sm';
        feedback.innerHTML = `
            <div class="flex items-center">
                <i class="fas fa-check-circle mr-2"></i>
                <span>${message}</span>
            </div>
        `;
        
        element.appendChild(feedback);
        
        setTimeout(() => {
            feedback.remove();
        }, 3000);
    }

    showErrorFeedback(message, element = document.body) {
        const feedback = document.createElement('div');
        feedback.className = 'error-feedback fixed top-4 right-4 z-50 max-w-sm';
        feedback.innerHTML = `
            <div class="flex items-center">
                <i class="fas fa-exclamation-circle mr-2"></i>
                <span>${message}</span>
            </div>
        `;
        
        element.appendChild(feedback);
        
        setTimeout(() => {
            feedback.remove();
        }, 3000);
    }
}

// Initialize UI interactions when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new UIInteractions();
});

// Add CSS for animations if not already present
if (!document.querySelector('#ui-interactions-styles')) {
    const style = document.createElement('style');
    style.id = 'ui-interactions-styles';
    style.textContent = `
        .animate-in {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
        
        .form-input-enhanced {
            transition: all 0.3s ease;
        }
        
        .form-input-enhanced.error {
            border-color: #ef4444;
            box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.1);
        }
        
        .form-input-enhanced.success {
            border-color: #10b981;
            box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.1);
        }
    `;
    document.head.appendChild(style);
}

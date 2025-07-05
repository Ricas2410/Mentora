/**
 * Page-specific UI enhancements for Pentora Platform
 * Adds targeted improvements for specific pages
 */

class PageSpecificEnhancements {
    constructor() {
        this.currentPage = this.detectCurrentPage();
        this.init();
    }

    detectCurrentPage() {
        const path = window.location.pathname;
        
        if (path.includes('/quiz/')) return 'quiz';
        if (path.includes('/learn/')) return 'learn';
        if (path.includes('/topics/') && path.split('/').length > 4) return 'topic-detail';
        if (path.includes('/topics/')) return 'topics';
        if (path.includes('/exam/')) return 'exam';
        
        return 'general';
    }

    init() {
        // First, clean up any duplicate progress bars
        this.cleanupDuplicateProgressBars();

        switch (this.currentPage) {
            case 'quiz':
                this.enhanceQuizPage();
                break;
            case 'learn':
                this.enhanceLearnPage();
                break;
            case 'topics':
                this.enhanceTopicsPage();
                break;
            case 'topic-detail':
                this.enhanceTopicDetailPage();
                break;
            case 'exam':
                this.enhanceExamPage();
                break;
        }

        this.addGlobalEnhancements();
    }

    cleanupDuplicateProgressBars() {
        // Remove any JavaScript-added progress bars that might be duplicates
        document.querySelectorAll('.js-added-progress, .js-added-circular-progress').forEach(element => {
            element.remove();
        });

        // More aggressive cleanup - remove progress bars that show 0.0% or incorrect data
        document.querySelectorAll('.quiz-card, .subject-card').forEach(card => {
            const progressElements = card.querySelectorAll('[class*="progress"]');
            const progressTexts = Array.from(card.querySelectorAll('*')).filter(el =>
                el.textContent && el.textContent.includes('0.0%')
            );

            // Remove elements showing 0.0% progress
            progressTexts.forEach(el => {
                const parent = el.closest('[class*="progress"]');
                if (parent) parent.remove();
            });

            // If there are still multiple progress bars, keep only the template-generated ones
            const remainingProgressBars = card.querySelectorAll('.bg-gray-200, .bg-blue-600');
            if (remainingProgressBars.length > 1) {
                // Remove the ones that are likely JavaScript-generated (usually at the bottom)
                for (let i = 1; i < remainingProgressBars.length; i++) {
                    const progressContainer = remainingProgressBars[i].closest('div');
                    if (progressContainer && progressContainer.classList.contains('mt-4')) {
                        progressContainer.remove();
                    }
                }
            }
        });

        // Remove any progress elements that contain "Progress" text twice
        document.querySelectorAll('.quiz-card, .subject-card').forEach(card => {
            const progressTexts = Array.from(card.querySelectorAll('*')).filter(el =>
                el.textContent && el.textContent.toLowerCase().includes('progress')
            );

            if (progressTexts.length > 2) {
                // Keep only the first two progress-related elements
                for (let i = 2; i < progressTexts.length; i++) {
                    progressTexts[i].remove();
                }
            }
        });
    }

    enhanceQuizPage() {
        console.log('Enhancing quiz page - CONSERVATIVE MODE...');

        // DISABLED: Skip all progress bar modifications to prevent duplicates
        // this.addQuizProgressIndicators();
        // this.enhanceExistingProgressBars();

        // Only add non-progress enhancements
        this.addQuickStartFeature();
        this.addDifficultyIndicators();

        console.log('Quiz page enhancement completed (progress bars skipped)');
    }

    enhanceLearnPage() {
        console.log('Enhancing learn page - CONSERVATIVE MODE...');

        // DISABLED: Skip all progress modifications to prevent duplicates
        // this.addSubjectProgressVisualization();
        // this.enhanceExistingProgressBars();

        // Only add non-progress enhancements
        this.addQuickNavigation();
        this.addStudyStreakIndicators();

        console.log('Learn page enhancement completed (progress bars skipped)');
    }

    enhanceTopicsPage() {
        console.log('Enhancing topics page...');
        
        // Add topic completion status
        this.addTopicCompletionStatus();
        
        // Add estimated reading time
        this.addEstimatedReadingTime();
        
        // Add topic difficulty indicators
        this.addTopicDifficultyIndicators();
    }

    enhanceTopicDetailPage() {
        console.log('Enhancing topic detail page...');
        
        // Add reading progress tracker
        this.addReadingProgressTracker();
        
        // Add note-taking functionality
        this.addNoteTakingFeature();
        
        // Add related topics suggestions
        this.addRelatedTopicsSuggestions();
    }

    enhanceExamPage() {
        console.log('Enhancing exam page...');
        
        // Add exam preparation checklist
        this.addExamPreparationChecklist();
        
        // Add confidence meter
        this.addConfidenceMeter();
        
        // Add last attempt information
        this.addLastAttemptInfo();
    }

    addQuizProgressIndicators() {
        // DISABLED: Template already has progress bars
        // This function is disabled to prevent duplicate progress bars
        console.log('Quiz progress indicators disabled - using template progress bars');
        return;
    }

    enhanceExistingProgressBars() {
        // Enhance existing progress bars with better animations for all cards
        document.querySelectorAll('.quiz-card, .subject-card').forEach(card => {
            const progressBars = card.querySelectorAll('.progress-fill, [class*="progress"]:not(.js-added-progress)');
            progressBars.forEach(bar => {
                if (!bar.classList.contains('progress-fill-enhanced')) {
                    bar.classList.add('progress-fill-enhanced');
                }
            });
        });
    }

    addQuickStartFeature() {
        // Add quick start buttons to quiz cards
        document.querySelectorAll('.quiz-card').forEach(card => {
            const quickStartBtn = document.createElement('button');
            quickStartBtn.className = 'absolute top-4 right-4 bg-blue-600 hover:bg-blue-700 text-white p-2 rounded-full opacity-0 group-hover:opacity-100 transition-all duration-300 transform scale-90 group-hover:scale-100';
            quickStartBtn.innerHTML = '<i class="fas fa-play text-sm"></i>';
            quickStartBtn.setAttribute('data-tooltip', 'Quick Start');
            
            card.style.position = 'relative';
            card.appendChild(quickStartBtn);
        });
    }

    addDifficultyIndicators() {
        document.querySelectorAll('.quiz-card').forEach(card => {
            // Simulate difficulty data
            const difficulties = ['Easy', 'Medium', 'Hard'];
            const difficulty = difficulties[Math.floor(Math.random() * difficulties.length)];
            const colors = {
                'Easy': 'bg-green-100 text-green-800',
                'Medium': 'bg-yellow-100 text-yellow-800',
                'Hard': 'bg-red-100 text-red-800'
            };
            
            const difficultyBadge = document.createElement('span');
            difficultyBadge.className = `inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${colors[difficulty]} ml-2`;
            difficultyBadge.textContent = difficulty;
            
            const title = card.querySelector('h3');
            if (title) {
                title.appendChild(difficultyBadge);
            }
        });
    }

    addSubjectProgressVisualization() {
        // DISABLED: Template already has progress indicators
        // This function is disabled to prevent duplicate progress elements
        console.log('Subject progress visualization disabled - using template progress');
        return;
    }

    addReadingProgressTracker() {
        // Add reading progress tracker for long content
        const content = document.querySelector('.study-content');
        if (content) {
            const progressBar = document.createElement('div');
            progressBar.className = 'fixed top-0 left-0 w-full h-1 bg-gray-200 z-50';
            progressBar.innerHTML = '<div class="progress-fill-enhanced h-full bg-blue-600" style="width: 0%"></div>';
            
            document.body.appendChild(progressBar);
            
            const updateProgress = () => {
                const scrollTop = window.pageYOffset;
                const docHeight = document.body.scrollHeight - window.innerHeight;
                const scrollPercent = (scrollTop / docHeight) * 100;
                
                const fill = progressBar.querySelector('.progress-fill-enhanced');
                fill.style.width = Math.min(scrollPercent, 100) + '%';
            };
            
            window.addEventListener('scroll', updateProgress);
            updateProgress();
        }
    }

    addExamPreparationChecklist() {
        const examSection = document.querySelector('.start-exam-section');
        if (examSection) {
            const checklist = document.createElement('div');
            checklist.className = 'bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6 max-w-md mx-auto';
            checklist.innerHTML = `
                <h4 class="font-bold text-blue-800 mb-3 flex items-center">
                    <i class="fas fa-clipboard-check mr-2"></i>
                    Pre-Exam Checklist
                </h4>
                <div class="space-y-2 text-sm">
                    <label class="flex items-center text-blue-700">
                        <input type="checkbox" class="mr-2 rounded border-blue-300">
                        Stable internet connection
                    </label>
                    <label class="flex items-center text-blue-700">
                        <input type="checkbox" class="mr-2 rounded border-blue-300">
                        Quiet environment
                    </label>
                    <label class="flex items-center text-blue-700">
                        <input type="checkbox" class="mr-2 rounded border-blue-300">
                        Sufficient time available
                    </label>
                    <label class="flex items-center text-blue-700">
                        <input type="checkbox" class="mr-2 rounded border-blue-300">
                        Reviewed study materials
                    </label>
                </div>
            `;
            
            const startButton = examSection.querySelector('.start-exam-btn');
            if (startButton) {
                examSection.insertBefore(checklist, startButton.parentElement);
                
                // Enable start button only when all items are checked
                const checkboxes = checklist.querySelectorAll('input[type="checkbox"]');
                const updateButtonState = () => {
                    const allChecked = Array.from(checkboxes).every(cb => cb.checked);
                    startButton.disabled = !allChecked;
                    startButton.style.opacity = allChecked ? '1' : '0.6';
                };
                
                checkboxes.forEach(cb => cb.addEventListener('change', updateButtonState));
                updateButtonState();
            }
        }
    }

    addGlobalEnhancements() {
        // Add smooth scrolling to all internal links
        document.querySelectorAll('a[href^="#"]').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(link.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
        
        // Add loading states to all forms
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', () => {
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn && !submitBtn.disabled) {
                    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Processing...';
                    submitBtn.disabled = true;
                }
            });
        });
        
        // Add keyboard shortcuts
        this.addKeyboardShortcuts();
    }

    addKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + K for search (if search exists)
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                const searchInput = document.querySelector('input[type="search"], input[placeholder*="search" i]');
                if (searchInput) {
                    searchInput.focus();
                }
            }
            
            // Escape to close modals
            if (e.key === 'Escape') {
                const modals = document.querySelectorAll('.modal, .popup, [data-modal]');
                modals.forEach(modal => {
                    if (modal.style.display !== 'none') {
                        modal.style.display = 'none';
                    }
                });
            }
        });
    }
}

// Initialize page-specific enhancements
document.addEventListener('DOMContentLoaded', () => {
    new PageSpecificEnhancements();
});

// Add visual feedback for user interactions
document.addEventListener('click', (e) => {
    // Add ripple effect to clickable elements
    if (e.target.matches('button, .btn, .card, a')) {
        const ripple = document.createElement('span');
        const rect = e.target.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
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
            z-index: 1000;
        `;
        
        e.target.style.position = 'relative';
        e.target.style.overflow = 'hidden';
        e.target.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
    }
});

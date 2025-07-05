/**
 * Cleanup Unwanted Elements
 * Removes any unwanted buttons, links, or elements that shouldn't be visible
 */

(function() {
    'use strict';

    function removeUnwantedElements() {
        // Remove any "Clean Duplicates" buttons
        const cleanupButtons = document.querySelectorAll('button');
        cleanupButtons.forEach(button => {
            if (button.textContent && 
                (button.textContent.includes('Clean Duplicates') || 
                 button.textContent.includes('Cleaned!'))) {
                console.log('Removing cleanup button:', button);
                button.remove();
            }
        });

        // Remove any skip links that are visible
        const skipLinks = document.querySelectorAll('.skip-link, a[href="#main-content"]');
        skipLinks.forEach(link => {
            if (link.style.opacity !== '0' && link.style.top !== '-40px') {
                console.log('Removing visible skip link:', link);
                link.remove();
            }
        });

        // Remove any fixed position elements that look like debugging tools
        const fixedElements = document.querySelectorAll('*');
        fixedElements.forEach(element => {
            const style = window.getComputedStyle(element);
            if (style.position === 'fixed' && 
                style.zIndex > 9000 && 
                element.tagName === 'BUTTON' &&
                element.textContent &&
                (element.textContent.includes('Clean') || 
                 element.textContent.includes('Debug') ||
                 element.textContent.includes('Test'))) {
                console.log('Removing fixed debug element:', element);
                element.remove();
            }
        });
    }

    // Run cleanup when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', removeUnwantedElements);
    } else {
        removeUnwantedElements();
    }

    // Run cleanup periodically to catch dynamically added elements
    setInterval(removeUnwantedElements, 2000);

    // Run cleanup when page becomes visible (tab switching)
    document.addEventListener('visibilitychange', () => {
        if (!document.hidden) {
            setTimeout(removeUnwantedElements, 100);
        }
    });

})();

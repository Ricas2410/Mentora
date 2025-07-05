/**
 * Ultra-Conservative Progress Bar Cleanup Script for Pentora Platform
 * ONLY removes elements explicitly marked with .js-added-progress class
 * Preserves ALL template-generated content
 */

(function() {
    'use strict';

    function cleanupDuplicateProgressBars() {
        console.log('Running ultra-conservative progress bar cleanup...');

        // ONLY remove elements explicitly marked as JavaScript-added
        const jsAddedElements = document.querySelectorAll('.js-added-progress, .js-added-circular-progress');

        if (jsAddedElements.length > 0) {
            console.log(`Found ${jsAddedElements.length} JavaScript-added elements to remove`);

            jsAddedElements.forEach(element => {
                console.log('Removing JS-added element:', element);
                element.remove();
            });

            console.log('Cleanup completed - removed only JS-added elements');
        } else {
            console.log('No JavaScript-added elements found - nothing to clean up');
        }
    }

    // Run cleanup immediately if DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', cleanupDuplicateProgressBars);
    } else {
        cleanupDuplicateProgressBars();
    }

    // Run cleanup after page enhancement scripts have run
    setTimeout(cleanupDuplicateProgressBars, 1000);

    // Expose cleanup function globally for manual cleanup
    window.cleanupProgressBars = cleanupDuplicateProgressBars;

    // Cleanup button removed for production

})();

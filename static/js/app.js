/**
 * Main application JavaScript file
 * 
 * This file contains core functionality used across the entire LUMAURA x XUVE platform.
 */

// Initialize the application when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('LUMAURA x XUVE application initialized');
    
    // Check for API status
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            console.log('API Status:', data);
        })
        .catch(error => {
            console.error('Error checking API status:', error);
        });
});

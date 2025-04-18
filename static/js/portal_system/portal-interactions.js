/**
 * Portal Interactions
 * 
 * This file contains functions for interactions with portals
 * in the LUMAURA x XUVE ecosystem.
 */

// Add event listeners for portal cards when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Portal cards in the dashboard
    const portalCards = document.querySelectorAll('.portal-card');
    
    portalCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            // Add glow effect
            this.style.boxShadow = 'var(--hologram-glow)';
            
            // Get the portal hologram
            const hologram = this.querySelector('.portal-hologram');
            if (hologram) {
                // Add pulse effect
                hologram.classList.add('pulse');
            }
        });
        
        card.addEventListener('mouseleave', function() {
            // Remove glow effect
            this.style.boxShadow = '';
            
            // Get the portal hologram
            const hologram = this.querySelector('.portal-hologram');
            if (hologram) {
                // Remove pulse effect
                hologram.classList.remove('pulse');
            }
        });
    });
    
    // Recommendation implementation
    const implementButtons = document.querySelectorAll('.implement-btn');
    
    implementButtons.forEach(button => {
        button.addEventListener('click', function() {
            const recId = this.getAttribute('data-id');
            implementRecommendation(recId);
        });
    });
});

/**
 * Implement a portal recommendation
 * @param {string} recommendationId - ID of the recommendation to implement
 */
function implementRecommendation(recommendationId) {
    fetch('/api/portal-evolution/implement-recommendation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            recommendation_id: recommendationId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'ok') {
            // Find the recommendation card
            const recCard = document.querySelector(`.recommendation-card[data-id="${recommendationId}"]`);
            
            if (recCard) {
                // Add implemented class for animation
                recCard.classList.add('implemented');
                
                // Remove card after animation completes
                setTimeout(() => {
                    recCard.remove();
                    
                    // Check if there are no more recommendations
                    const remainingRecs = document.querySelectorAll('.recommendation-card');
                    if (remainingRecs.length === 0) {
                        const recsList = document.querySelector('.recommendations-list');
                        if (recsList) {
                            recsList.innerHTML = '<p class="no-recommendations">No pending recommendations for this portal.</p>';
                        }
                    }
                }, 1000);
                
                // Update evolution score and stage if provided
                if (data.result && data.result.new_stage) {
                    updateEvolutionStage(data.result.portal, data.result.new_stage);
                }
            }
        } else {
            console.error('Error implementing recommendation:', data.error);
            alert('Error implementing recommendation: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error implementing recommendation:', error);
        alert('Error implementing recommendation');
    });
}

/**
 * Update the UI to reflect a new evolution stage
 * @param {string} portalName - Name of the portal
 * @param {string} newStage - New evolution stage
 */
function updateEvolutionStage(portalName, newStage) {
    // In a real application, you would update the UI to reflect
    // the new evolution stage. For now, just reload the page.
    window.location.reload();
}

/**
 * Record portal activity
 * @param {string} portalName - Name of the portal
 * @param {string} activity - Activity description
 */
function recordPortalActivity(portalName, activity) {
    fetch('/api/portal-evolution/record-activity', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            portal_name: portalName,
            activity: activity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'ok') {
            console.log('Activity recorded:', data.activity);
        } else {
            console.error('Error recording activity:', data.error);
        }
    })
    .catch(error => {
        console.error('Error recording activity:', error);
    });
}

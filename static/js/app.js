document.addEventListener('DOMContentLoaded', function() {
  // Fetch portal data from API
  fetch('/api/portals')
    .then(response => response.json())
    .then(portals => {
      const portalGrid = document.querySelector('.portal-grid');
      
      // Clear existing portals
      portalGrid.innerHTML = '';
      
      // Add portals from API
      portals.forEach(portal => {
        const portalElement = document.createElement('div');
        portalElement.className = 'portal';
        portalElement.dataset.level = portal.level.toLowerCase();
        
        portalElement.innerHTML = `
          <h3>${portal.name}</h3>
          <div class="portal-level">${portal.level}</div>
          <div class="portal-activity">${portal.activity}</div>
        `;
        
        portalGrid.appendChild(portalElement);
      });
    })
    .catch(error => {
      console.error('Error fetching portals:', error);
    });
    
  // Add status indicator
  fetch('/api/status')
    .then(response => response.json())
    .then(status => {
      const footer = document.createElement('footer');
      footer.innerHTML = `
        <div class="status">
          <span class="status-indicator ${status.status === 'online' ? 'online' : 'offline'}"></span>
          <span class="status-text">${status.status}</span>
          <span class="version">v${status.version}</span>
        </div>
      `;
      document.body.appendChild(footer);
    });
});

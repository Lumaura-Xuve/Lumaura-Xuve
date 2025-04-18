/**
 * Holographic UI System
 * 
 * This file contains functions for rendering holographic UI elements.
 */

/**
 * Initialize a holographic UI element
 * @param {string} selector - CSS selector for the container element
 */
function initHolographicUI(selector) {
    const container = document.querySelector(selector);
    if (!container) return;
    
    // Create canvas for holographic effect
    const canvas = document.createElement('canvas');
    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;
    container.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    
    // Create particle system
    const particles = [];
    const particleCount = 100;
    
    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 3 + 1,
            speedX: (Math.random() - 0.5) * 0.5,
            speedY: (Math.random() - 0.5) * 0.5,
            opacity: Math.random() * 0.5 + 0.25
        });
    }
    
    // Animation loop
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Create gradient background
        const gradient = ctx.createRadialGradient(
            canvas.width / 2, canvas.height / 2, 0,
            canvas.width / 2, canvas.height / 2, canvas.width / 2
        );
        gradient.addColorStop(0, 'rgba(98, 0, 234, 0.2)');
        gradient.addColorStop(1, 'rgba(3, 218, 198, 0.05)');
        
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Draw and update particles
        for (let particle of particles) {
            ctx.fillStyle = `rgba(255, 255, 255, ${particle.opacity})`;
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            ctx.fill();
            
            // Update position
            particle.x += particle.speedX;
            particle.y += particle.speedY;
            
            // Bounce off edges
            if (particle.x < 0 || particle.x > canvas.width) {
                particle.speedX *= -1;
            }
            
            if (particle.y < 0 || particle.y > canvas.height) {
                particle.speedY *= -1;
            }
        }
        
        // Add pulsing glow effect
        const time = Date.now() / 1000;
        const pulseSize = (Math.sin(time) * 0.1) + 0.9;
        
        ctx.beginPath();
        ctx.arc(canvas.width / 2, canvas.height / 2, 
                (canvas.width / 3) * pulseSize, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(3, 218, 198, 0.2)';
        ctx.lineWidth = 2;
        ctx.stroke();
        
        requestAnimationFrame(animate);
    }
    
    animate();
    
    // Resize handling
    window.addEventListener('resize', function() {
        canvas.width = container.clientWidth;
        canvas.height = container.clientHeight;
    });
}

/**
 * Initialize a portal hologram visualization
 * @param {HTMLElement} element - Container element
 * @param {string} portalName - Name of the portal (e.g., 'xuvebanker')
 * @param {boolean} detailed - Whether to show a detailed visualization
 */
function initPortalHologram(element, portalName, detailed = false) {
    if (!element) return;
    
    // Create canvas for holographic effect
    const canvas = document.createElement('canvas');
    canvas.width = element.clientWidth;
    canvas.height = element.clientHeight;
    element.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    
    // Define colors based on portal name
    let primaryColor = 'rgba(98, 0, 234, 0.7)';
    let secondaryColor = 'rgba(3, 218, 198, 0.5)';
    
    // Custom colors for specific portals
    const portalColors = {
        'xuvebanker': {
            primary: 'rgba(123, 31, 162, 0.7)',
            secondary: 'rgba(156, 39, 176, 0.5)'
        },
        'xuvemark': {
            primary: 'rgba(0, 145, 234, 0.7)',
            secondary: 'rgba(3, 169, 244, 0.5)'
        },
        'xuveteam': {
            primary: 'rgba(0, 200, 83, 0.7)',
            secondary: 'rgba(76, 175, 80, 0.5)'
        },
        'xuvecode': {
            primary: 'rgba(255, 214, 0, 0.7)',
            secondary: 'rgba(255, 235, 59, 0.5)'
        },
        'xuvevault': {
            primary: 'rgba(213, 0, 0, 0.7)',
            secondary: 'rgba(244, 67, 54, 0.5)'
        }
    };
    
    if (portalColors[portalName]) {
        primaryColor = portalColors[portalName].primary;
        secondaryColor = portalColors[portalName].secondary;
    }
    
    // Create particles specific to this portal
    const particles = [];
    const particleCount = detailed ? 150 : 75;
    
    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 3 + 1,
            speedX: (Math.random() - 0.5) * 0.5,
            speedY: (Math.random() - 0.5) * 0.5,
            opacity: Math.random() * 0.5 + 0.25,
            color: Math.random() > 0.5 ? primaryColor : secondaryColor
        });
    }
    
    // Animation state
    let angle = 0;
    
    // Animation loop
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Create gradient background
        const gradient = ctx.createRadialGradient(
            canvas.width / 2, canvas.height / 2, 0,
            canvas.width / 2, canvas.height / 2, canvas.width / 2
        );
        
        // Extract primary color for gradient
        const primaryRgba = primaryColor.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([.\d]+))?\)/);
        if (primaryRgba) {
            const r = primaryRgba[1];
            const g = primaryRgba[2];
            const b = primaryRgba[3];
            gradient.addColorStop(0, `rgba(${r}, ${g}, ${b}, 0.2)`);
            gradient.addColorStop(1, `rgba(${r}, ${g}, ${b}, 0.05)`);
        } else {
            gradient.addColorStop(0, 'rgba(30, 30, 30, 0.2)');
            gradient.addColorStop(1, 'rgba(30, 30, 30, 0.05)');
        }
        
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Draw portal specific shape
        drawPortalShape(ctx, portalName, canvas.width / 2, canvas.height / 2, 
                      canvas.width / 3, angle, detailed);
        
        // Draw and update particles
        for (let particle of particles) {
            ctx.fillStyle = particle.color;
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            ctx.fill();
            
            // Update position
            particle.x += particle.speedX;
            particle.y += particle.speedY;
            
            // Bounce off edges
            if (particle.x < 0 || particle.x > canvas.width) {
                particle.speedX *= -1;
            }
            
            if (particle.y < 0 || particle.y > canvas.height) {
                particle.speedY *= -1;
            }
        }
        
        // Update animation state
        angle += 0.01;
        
        requestAnimationFrame(animate);
    }
    
    animate();
    
    // Resize handling
    window.addEventListener('resize', function() {
        canvas.width = element.clientWidth;
        canvas.height = element.clientHeight;
    });
}

/**
 * Draw a shape specific to a portal
 * @param {CanvasRenderingContext2D} ctx - Canvas context
 * @param {string} portalName - Name of the portal
 * @param {number} x - Center X coordinate
 * @param {number} y - Center Y coordinate
 * @param {number} radius - Base radius for the shape
 * @param {number} angle - Current animation angle
 * @param {boolean} detailed - Whether to show a detailed visualization
 */
function drawPortalShape(ctx, portalName, x, y, radius, angle, detailed) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(angle);
    
    // Default shape - hexagon
    let sides = 6;
    let sizeScale = 0.8;
    let innerRatio = 0.6;
    
    // Custom shapes for specific portals
    switch (portalName) {
        case 'xuvebanker':
            sides = 8;  // Octagon for banker
            sizeScale = 0.7;
            break;
        case 'xuvemark':
            sides = 3;  // Triangle for marketing
            sizeScale = 0.9;
            innerRatio = 0.7;
            break;
        case 'xuveteam':
            sides = 5;  // Pentagon for team
            sizeScale = 0.8;
            break;
        case 'xuvecode':
            sides = 4;  // Square for code
            sizeScale = 0.75;
            ctx.rotate(Math.PI / 4);  // Rotate to make it a diamond
            break;
        case 'xuvevault':
            sides = 6;  // Hexagon for vault
            sizeScale = 0.7;
            innerRatio = 0.5;
            break;
        default:
            sides = 6;  // Default hexagon
            break;
    }
    
    // Draw outer shape
    ctx.beginPath();
    for (let i = 0; i < sides; i++) {
        const a = (i / sides) * Math.PI * 2;
        const px = Math.cos(a) * radius * sizeScale;
        const py = Math.sin(a) * radius * sizeScale;
        
        if (i === 0) {
            ctx.moveTo(px, py);
        } else {
            ctx.lineTo(px, py);
        }
    }
    ctx.closePath();
    
    // Style based on portal
    let strokeColor = 'rgba(3, 218, 198, 0.6)';
    let fillColor = 'rgba(3, 218, 198, 0.1)';
    
    // Custom colors for specific portals
    switch (portalName) {
        case 'xuvebanker':
            strokeColor = 'rgba(156, 39, 176, 0.6)';
            fillColor = 'rgba(156, 39, 176, 0.1)';
            break;
        case 'xuvemark':
            strokeColor = 'rgba(3, 169, 244, 0.6)';
            fillColor = 'rgba(3, 169, 244, 0.1)';
            break;
        case 'xuveteam':
            strokeColor = 'rgba(76, 175, 80, 0.6)';
            fillColor = 'rgba(76, 175, 80, 0.1)';
            break;
        case 'xuvecode':
            strokeColor = 'rgba(255, 235, 59, 0.6)';
            fillColor = 'rgba(255, 235, 59, 0.1)';
            break;
        case 'xuvevault':
            strokeColor = 'rgba(244, 67, 54, 0.6)';
            fillColor = 'rgba(244, 67, 54, 0.1)';
            break;
    }
    
    ctx.strokeStyle = strokeColor;
    ctx.lineWidth = 2;
    ctx.fillStyle = fillColor;
    ctx.fill();
    ctx.stroke();
    
    // Draw inner shape (rotated in opposite direction)
    ctx.rotate(-angle * 2);
    
    ctx.beginPath();
    for (let i = 0; i < sides; i++) {
        const a = (i / sides) * Math.PI * 2;
        const px = Math.cos(a) * radius * sizeScale * innerRatio;
        const py = Math.sin(a) * radius * sizeScale * innerRatio;
        
        if (i === 0) {
            ctx.moveTo(px, py);
        } else {
            ctx.lineTo(px, py);
        }
    }
    ctx.closePath();
    
    ctx.strokeStyle = strokeColor;
    ctx.lineWidth = 1;
    ctx.fillStyle = fillColor;
    ctx.fill();
    ctx.stroke();
    
    // Add additional details if requested
    if (detailed) {
        // Draw connecting lines
        ctx.beginPath();
        for (let i = 0; i < sides; i++) {
            const a = (i / sides) * Math.PI * 2;
            const outerX = Math.cos(a) * radius * sizeScale;
            const outerY = Math.sin(a) * radius * sizeScale;
            const innerX = Math.cos(a) * radius * sizeScale * innerRatio;
            const innerY = Math.sin(a) * radius * sizeScale * innerRatio;
            
            ctx.moveTo(outerX, outerY);
            ctx.lineTo(innerX, innerY);
        }
        
        ctx.strokeStyle = `${strokeColor.slice(0, -4)}0.3)`;
        ctx.lineWidth = 1;
        ctx.stroke();
        
        // Draw center point
        ctx.beginPath();
        ctx.arc(0, 0, radius * 0.1, 0, Math.PI * 2);
        ctx.fillStyle = strokeColor;
        ctx.fill();
        
        // Draw animated ripple effect
        const time = Date.now() / 1000;
        const pulseSize = (Math.sin(time * 2) * 0.2) + 0.8;
        
        ctx.beginPath();
        ctx.arc(0, 0, radius * pulseSize * 0.3, 0, Math.PI * 2);
        ctx.strokeStyle = `${strokeColor.slice(0, -4)}0.2)`;
        ctx.lineWidth = 2;
        ctx.stroke();
    }
    
    ctx.restore();
}

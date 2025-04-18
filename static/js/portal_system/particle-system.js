/**
 * Particle System for Portal Visualizations
 * 
 * This file contains functions for creating particle effects
 * used in portal visualizations.
 */

/**
 * Create a particle system within a container
 * @param {HTMLElement} container - Container element
 * @param {Object} options - Configuration options
 */
function createParticleSystem(container, options = {}) {
    if (!container) return null;
    
    // Default options
    const defaults = {
        particleCount: 100,
        particleColor: 'rgba(255, 255, 255, 0.5)',
        particleSize: [1, 3],
        particleSpeed: 0.5,
        backgroundColor: 'rgba(0, 0, 0, 0)'
    };
    
    // Merge options
    const config = { ...defaults, ...options };
    
    // Create canvas
    const canvas = document.createElement('canvas');
    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;
    canvas.style.position = 'absolute';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.pointerEvents = 'none';
    container.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    
    // Create particles
    const particles = [];
    
    for (let i = 0; i < config.particleCount; i++) {
        const size = config.particleSize[0] + Math.random() * 
                    (config.particleSize[1] - config.particleSize[0]);
        
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: size,
            speedX: (Math.random() - 0.5) * config.particleSpeed,
            speedY: (Math.random() - 0.5) * config.particleSpeed,
            color: config.particleColor,
            opacity: Math.random() * 0.5 + 0.25
        });
    }
    
    // Animation loop
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Fill background if needed
        if (config.backgroundColor !== 'rgba(0, 0, 0, 0)') {
            ctx.fillStyle = config.backgroundColor;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        }
        
        // Update and draw particles
        for (let particle of particles) {
            // Calculate color with opacity
            let color = particle.color;
            if (color.startsWith('rgba')) {
                color = color.replace(/[\d\.]+\)$/, `${particle.opacity})`);
            } else if (color.startsWith('rgb')) {
                color = color.replace('rgb', 'rgba').replace(')', `, ${particle.opacity})`);
            }
            
            ctx.fillStyle = color;
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            ctx.fill();
            
            // Update position
            particle.x += particle.speedX;
            particle.y += particle.speedY;
            
            // Wrap around edges
            if (particle.x < -particle.size) particle.x = canvas.width + particle.size;
            if (particle.x > canvas.width + particle.size) particle.x = -particle.size;
            if (particle.y < -particle.size) particle.y = canvas.height + particle.size;
            if (particle.y > canvas.height + particle.size) particle.y = -particle.size;
        }
        
        requestAnimationFrame(animate);
    }
    
    animate();
    
    // Handle window resize
    window.addEventListener('resize', function() {
        canvas.width = container.clientWidth;
        canvas.height = container.clientHeight;
    });
    
    // Return control object
    return {
        canvas: canvas,
        setParticleCount: function(count) {
            // Adjust particle count
            const currentCount = particles.length;
            
            if (count > currentCount) {
                // Add particles
                for (let i = 0; i < count - currentCount; i++) {
                    const size = config.particleSize[0] + Math.random() * 
                                (config.particleSize[1] - config.particleSize[0]);
                    
                    particles.push({
                        x: Math.random() * canvas.width,
                        y: Math.random() * canvas.height,
                        size: size,
                        speedX: (Math.random() - 0.5) * config.particleSpeed,
                        speedY: (Math.random() - 0.5) * config.particleSpeed,
                        color: config.particleColor,
                        opacity: Math.random() * 0.5 + 0.25
                    });
                }
            } else if (count < currentCount) {
                // Remove particles
                particles.splice(count, currentCount - count);
            }
        },
        setParticleSpeed: function(speed) {
            config.particleSpeed = speed;
            
            // Update existing particles
            for (let particle of particles) {
                particle.speedX = (Math.random() - 0.5) * config.particleSpeed;
                particle.speedY = (Math.random() - 0.5) * config.particleSpeed;
            }
        },
        setParticleColor: function(color) {
            config.particleColor = color;
            
            // Update existing particles
            for (let particle of particles) {
                particle.color = color;
            }
        }
    };
}

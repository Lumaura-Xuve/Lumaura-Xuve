"""
Portal Activity Generator

This module generates simulated activities for portals in the LUMAURA AI System.
This creates the appearance of an active, evolving ecosystem of portals.
"""

import logging
import random
import threading
import time
from datetime import datetime

logger = logging.getLogger(__name__)

# Lists of actions, targets, and contexts for generating varied activities
ACTIONS = [
    "Analyzing", "Processing", "Generating", "Optimizing", "Managing", 
    "Tracking", "Monitoring", "Automating", "Building", "Controlling",
    "Coordinating", "Scheduling", "Curating", "Testing", "Routing", 
    "Personalizing", "Matching", "Identifying", "Calculating", "Creating"
]

TARGETS = [
    "metrics", "data", "content", "reports", "resources", "asset inventory",
    "performance metrics", "security threats", "encryption keys", "backup processes",
    "marketing metrics", "audience metrics", "creative trends", "campaign strategies",
    "partnership proposals", "relationship data", "sponsor metrics", "job opportunities",
    "skill requirements", "workforce analytics", "status reports", "error patterns",
    "system resources", "delivery schedules", "tutorial sequences", "knowledge retention",
    "legal requirements", "policy updates", "regulatory changes", "legal documentation",
    "navigation systems", "notification sequences", "dashboard displays", "user experiences",
    "membership data", "social relationships", "engagement metrics", "community connections",
    "health recommendations", "wellness metrics", "work-life balance", "routine tasks",
    "habit formation systems", "processes", "workflows", "operations", "deployments",
    "scaling operations", "sound assets", "audio patterns", "sonic branding", "voice content",
    "educational content", "training materials", "onboarding progress", "assistance",
    "feedback", "partnership opportunities", "ROI projections"
]

CONTEXTS = [
    "for API services", "for platform services", "for system operations", 
    "for content distribution", "for security protocols", "for transaction processing",
    "for blockchain integration", "for smart contracts", "for wallet integrations", 
    "for token holders", "for community members", "for enterprise clients",
    "for partner networks", "for mobile interface", "for desktop portal", 
    "for developer resources", "for user profiles", "for user experience",
    "for XUVE ecosystem", "for data analytics"
]

def _generate_activity(portal_name):
    """Generate a random activity description for a portal."""
    action = random.choice(ACTIONS)
    target = random.choice(TARGETS)
    context = random.choice(CONTEXTS)
    
    return f"{action} {target} {context}"

def _activity_generation_loop(portal_system):
    """Background loop that generates activities for random portals."""
    while True:
        try:
            # Select a random portal
            portal_names = list(portal_system.portals.keys())
            if not portal_names:
                time.sleep(10)
                continue
                
            portal_name = random.choice(portal_names)
            
            # Generate and record activity
            activity = _generate_activity(portal_name)
            portal_system.record_portal_activity(portal_name, activity)
            
            # Sleep for a random interval (1-5 seconds)
            time.sleep(random.uniform(1, 5))
        except Exception as e:
            logger.error(f"Error in activity generation: {e}")
            time.sleep(10)

def _recommendation_generation_loop(portal_system):
    """Background loop that occasionally generates recommendations between portals."""
    while True:
        try:
            # Only generate recommendations occasionally
            if random.random() < 0.1:
                portal_names = list(portal_system.portals.keys())
                if len(portal_names) < 2:
                    time.sleep(30)
                    continue
                
                # Select random source and target portals (different from each other)
                source_portal = random.choice(portal_names)
                target_portal = random.choice([p for p in portal_names if p != source_portal])
                
                # Generate recommendation type
                rec_types = ["System Upgrade", "Collaboration Opportunity", "Optimization Strategy", 
                            "Resource Allocation", "Integration Enhancement"]
                rec_type = random.choice(rec_types)
                
                # Create the recommendation
                portal_system.create_recommendation(
                    source_portal=source_portal,
                    target_portal=target_portal,
                    recommendation_type=rec_type,
                    details=f"Consider {rec_type} for portal {target_portal}"
                )
            
            # Sleep for a longer interval (recommendations are less frequent)
            time.sleep(random.uniform(30, 120))
        except Exception as e:
            logger.error(f"Error in recommendation generation: {e}")
            time.sleep(30)

def start_activity_generation(portal_system):
    """Start background threads for generating portal activities and recommendations."""
    # Start activity generation thread
    activity_thread = threading.Thread(
        target=_activity_generation_loop,
        args=(portal_system,),
        daemon=True
    )
    activity_thread.start()
    
    # Start recommendation generation thread
    recommendation_thread = threading.Thread(
        target=_recommendation_generation_loop,
        args=(portal_system,),
        daemon=True
    )
    recommendation_thread.start()
    
    logger.info("Portal activity and recommendation generation started")

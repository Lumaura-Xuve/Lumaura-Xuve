"""
Portal Evolution System

This module manages the evolution of AI portals within the LUMAURA x XUVE ecosystem.
It tracks portal development, facilitates interactions, and manages the evolution process.
"""

import os
import logging
import json
import random
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class PortalEvolutionSystem:
    """Main class for managing the Portal Evolution System."""
    
    def __init__(self):
        """Initialize the Portal Evolution System."""
        self.portals = {}
        self.interactions = []
        self.recommendations = []
        self.initialized = False
        logger.info("Portal Evolution System created")
    
    def initialize(self):
        """Initialize all portals in the system."""
        if self.initialized:
            logger.warning("Portal Evolution System already initialized")
            return
        
        try:
            # Import portal modules
            from lumaura_ai_system.portals import (
                xuvebanker, xuvemark, xuveteam, xuvevault, xuveops, xuvecode,
                xuvecast, xuvemirror, xuvehome, xuvewisdom, xuveteach, xuveritual,
                xuveonboard, xuvewell, xuvefamily, xuvejobs, xuvefleet,
                xuvesponsorship, xuvesound, xuvecreator, xuvepulse, xuvelegal
            )
            
            # Create instances of each portal
            portal_classes = [
                (xuvebanker, "XuvebankerPortal"),
                (xuvemark, "XuvemarkPortal"),
                (xuveteam, "XuveteamPortal"),
                (xuvevault, "XuvevaultPortal"),
                (xuveops, "XuveopsPortal"),
                (xuvecode, "XuvecodePortal"),
                (xuvecast, "XuvecastPortal"),
                (xuvemirror, "XuvemirrorPortal"),
                (xuvehome, "XuvehomePortal"),
                (xuvewisdom, "XuvewisdomPortal"),
                (xuveteach, "XuveteachPortal"),
                (xuveritual, "XuverirtualPortal"),
                (xuveonboard, "XuveonboardPortal"),
                (xuvewell, "XuvewellPortal"),
                (xuvefamily, "XuvefamilyPortal"),
                (xuvejobs, "XuvejobsPortal"),
                (xuvefleet, "XuvefleetPortal"),
                (xuvesponsorship, "XuvesponsorshipPortal"),
                (xuvesound, "XuvesoundPortal"),
                (xuvecreator, "XuvecreatorPortal"),
                (xuvepulse, "XuvepulsePortal"),
                (xuvelegal, "XuvelegalPortal"),
            ]
            
            for module, class_name in portal_classes:
                portal_class = getattr(module, class_name, None)
                if portal_class:
                    portal_instance = portal_class()
                    self.portals[portal_instance.name] = portal_instance
                else:
                    logger.warning(f"Could not find class {class_name} in module {module.__name__}")
            
            # Load evolution data if available
            self._load_evolution_data()
            
            self.initialized = True
            logger.info(f"Loaded evolution data for {len(self.portals)} portals")
            
            # Start portal activity generator
            from lumaura_ai_system.portal_activity_generator import start_activity_generation
            start_activity_generation(self)
        except Exception as e:
            logger.error(f"Error initializing Portal Evolution System: {e}")
    
    def _load_evolution_data(self):
        """Load stored evolution data for portals."""
        data_dir = Path("data/portal_evolution")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        evolution_file = data_dir / "evolution_data.json"
        if evolution_file.exists():
            try:
                with open(evolution_file, "r") as f:
                    data = json.load(f)
                
                for portal_name, portal_data in data.get("portals", {}).items():
                    if portal_name in self.portals:
                        self.portals[portal_name].evolution_score = portal_data.get("evolution_score", 0)
                        # Update other attributes as needed
                
                logger.info(f"Loaded evolution data for {len(data.get('portals', {}))} portals")
            except Exception as e:
                logger.error(f"Error loading evolution data: {e}")
    
    def _save_evolution_data(self):
        """Save evolution data for all portals."""
        data_dir = Path("data/portal_evolution")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        evolution_file = data_dir / "evolution_data.json"
        
        portal_data = {}
        for name, portal in self.portals.items():
            portal_data[name] = {
                "evolution_score": portal.evolution_score,
                "evolution_stage": portal.evolution_stage.value,
                "last_updated": datetime.now().isoformat()
            }
        
        data = {
            "portals": portal_data,
            "last_saved": datetime.now().isoformat()
        }
        
        try:
            with open(evolution_file, "w") as f:
                json.dump(data, f, indent=2)
            logger.info(f"Saved evolution data for {len(portal_data)} portals")
        except Exception as e:
            logger.error(f"Error saving evolution data: {e}")
    
    def record_portal_activity(self, portal_name, activity_description):
        """Record activity for a specific portal."""
        if portal_name in self.portals:
            activity = self.portals[portal_name].record_activity(activity_description)
            # Save periodically
            if random.random() < 0.1:
                self._save_evolution_data()
            return activity
        else:
            logger.warning(f"Cannot record activity - portal not found: {portal_name}")
            return None
    
    def get_portal_status(self, portal_name):
        """Get the current status of a specific portal."""
        if portal_name in self.portals:
            return self.portals[portal_name].get_status()
        else:
            logger.warning(f"Portal not found: {portal_name}")
            return None
    
    def get_all_portals_status(self):
        """Get the status of all portals."""
        return {name: portal.to_dict() for name, portal in self.portals.items()}
    
    def create_recommendation(self, source_portal, target_portal, recommendation_type, details):
        """Create a recommendation from one portal to another."""
        recommendation = {
            "id": f"rec-{len(self.recommendations) + 1}",
            "source_portal": source_portal,
            "target_portal": target_portal,
            "type": recommendation_type,
            "details": details,
            "created_at": datetime.now().isoformat(),
            "status": "pending"
        }
        
        self.recommendations.append(recommendation)
        logger.info(f"Created new recommendation: {recommendation_type} for portal {target_portal}")
        return recommendation
    
    def get_recommendations_for_portal(self, portal_name):
        """Get all recommendations targeting a specific portal."""
        return [r for r in self.recommendations if r["target_portal"] == portal_name]
    
    def implement_recommendation(self, recommendation_id):
        """Implement a recommendation, potentially evolving a portal."""
        for i, rec in enumerate(self.recommendations):
            if rec["id"] == recommendation_id and rec["status"] == "pending":
                # Mark as implemented
                self.recommendations[i]["status"] = "implemented"
                self.recommendations[i]["implemented_at"] = datetime.now().isoformat()
                
                # Apply evolution boost to target portal
                target = rec["target_portal"]
                if target in self.portals:
                    boost = random.uniform(0.5, 2.0)
                    new_stage = self.portals[target].update_evolution_score(boost)
                    
                    # Record the implementation
                    self.record_portal_activity(
                        target, 
                        f"Implemented recommendation '{rec['type']}' from {rec['source_portal']}"
                    )
                    
                    # Save evolution data
                    self._save_evolution_data()
                    
                    logger.info(f"Implemented recommendation {recommendation_id} for portal {target}")
                    return {"success": True, "portal": target, "new_stage": new_stage.value}
                
                return {"success": True, "portal": target}
        
        logger.warning(f"Recommendation not found or already implemented: {recommendation_id}")
        return {"success": False, "error": "Recommendation not found or already implemented"}

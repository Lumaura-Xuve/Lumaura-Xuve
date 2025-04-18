"""
Portal Evolution Routes

This module defines the API routes for the Portal Evolution System.
"""

import logging
from flask import jsonify, request, render_template, abort

logger = logging.getLogger(__name__)

def register_routes(app, portal_system):
    """Register Portal Evolution System routes with the Flask app."""
    logger.info("Portal Evolution routes registered at /portal-evolution")
    
    @app.route('/portal-evolution')
    def portal_evolution_dashboard():
        """Render the Portal Evolution dashboard."""
        portals = portal_system.get_all_portals_status()
        return render_template('portal_evolution/dashboard.html', portals=portals)
    
    @app.route('/portal-evolution/portal/<portal_name>')
    def portal_detail(portal_name):
        """Render the detail page for a specific portal."""
        portal_status = portal_system.get_portal_status(portal_name)
        if not portal_status:
            abort(404)
        
        recommendations = portal_system.get_recommendations_for_portal(portal_name)
        return render_template('portal_evolution/portal_detail.html', 
                               portal=portal_status, 
                               recommendations=recommendations)
    
    @app.route('/api/portal-evolution/status')
    def portal_evolution_status():
        """Get the status of all portals."""
        portals = portal_system.get_all_portals_status()
        return jsonify({
            "status": "ok",
            "portals": portals
        })
    
    @app.route('/api/portal-evolution/portal/<portal_name>')
    def portal_status(portal_name):
        """Get the status of a specific portal."""
        portal_status = portal_system.get_portal_status(portal_name)
        if not portal_status:
            return jsonify({"error": "Portal not found"}), 404
        
        return jsonify({
            "status": "ok",
            "portal": portal_status
        })
    
    @app.route('/api/portal-evolution/recommendations/<portal_name>')
    def portal_recommendations(portal_name):
        """Get recommendations for a specific portal."""
        recommendations = portal_system.get_recommendations_for_portal(portal_name)
        
        return jsonify({
            "status": "ok",
            "portal_name": portal_name,
            "recommendations": recommendations
        })
    
    @app.route('/api/portal-evolution/implement-recommendation', methods=['POST'])
    def implement_recommendation():
        """Implement a recommendation."""
        data = request.json
        recommendation_id = data.get('recommendation_id')
        
        if not recommendation_id:
            return jsonify({"error": "Missing recommendation_id"}), 400
        
        result = portal_system.implement_recommendation(recommendation_id)
        
        if result.get('success'):
            return jsonify({
                "status": "ok",
                "result": result
            })
        else:
            return jsonify({
                "status": "error",
                "error": result.get('error', 'Unknown error')
            }), 400
    
    @app.route('/api/portal-evolution/record-activity', methods=['POST'])
    def record_portal_activity():
        """Record activity for a portal."""
        data = request.json
        portal_name = data.get('portal_name')
        activity = data.get('activity')
        
        if not portal_name or not activity:
            return jsonify({"error": "Missing portal_name or activity"}), 400
        
        activity = portal_system.record_portal_activity(portal_name, activity)
        
        if activity:
            return jsonify({
                "status": "ok",
                "activity": activity
            })
        else:
            return jsonify({
                "status": "error",
                "error": "Failed to record activity"
            }), 400

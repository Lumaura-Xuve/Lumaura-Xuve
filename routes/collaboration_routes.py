"""
Collaboration Routes

This module defines the API routes for the Collaboration System.
"""

import logging
from flask import jsonify, request, render_template, abort
import os
import json
from datetime import datetime

logger = logging.getLogger(__name__)

def register_routes(app):
    """Register Collaboration System routes with the Flask app."""
    logger.info("Collaboration routes registered")
    
    # Create data directory if it doesn't exist
    os.makedirs("data/collaboration", exist_ok=True)
    
    @app.route('/collaboration')
    def collaboration_dashboard():
        """Render the Collaboration dashboard."""
        workspaces = _get_all_workspaces()
        return render_template('collaboration/dashboard.html', workspaces=workspaces)
    
    @app.route('/collaboration/workspace/<workspace_id>')
    def workspace_detail(workspace_id):
        """Render the detail page for a specific workspace."""
        workspace = _get_workspace(workspace_id)
        if not workspace:
            abort(404)
        
        return render_template('collaboration/workspace_detail.html', workspace=workspace)
    
    @app.route('/api/collaboration/workspaces')
    def get_workspaces():
        """Get all workspaces."""
        workspaces = _get_all_workspaces()
        return jsonify({
            "status": "ok",
            "workspaces": workspaces
        })
    
    @app.route('/api/collaboration/workspace/<workspace_id>')
    def get_workspace(workspace_id):
        """Get a specific workspace."""
        workspace = _get_workspace(workspace_id)
        if not workspace:
            return jsonify({"error": "Workspace not found"}), 404
        
        return jsonify({
            "status": "ok",
            "workspace": workspace
        })
    
    @app.route('/api/collaboration/workspace', methods=['POST'])
    def create_workspace():
        """Create a new workspace."""
        data = request.json
        workspace_name = data.get('name')
        
        if not workspace_name:
            return jsonify({"error": "Missing workspace name"}), 400
        
        workspace = {
            "id": f"ws-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "name": workspace_name,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "members": data.get('members', []),
            "resources": []
        }
        
        _save_workspace(workspace)
        
        return jsonify({
            "status": "ok",
            "workspace": workspace
        })
    
    @app.route('/api/collaboration/workspace/<workspace_id>', methods=['PUT'])
    def update_workspace(workspace_id):
        """Update a workspace."""
        data = request.json
        workspace = _get_workspace(workspace_id)
        
        if not workspace:
            return jsonify({"error": "Workspace not found"}), 404
        
        if 'name' in data:
            workspace['name'] = data['name']
        
        if 'members' in data:
            workspace['members'] = data['members']
        
        workspace['updated_at'] = datetime.now().isoformat()
        
        _save_workspace(workspace)
        
        return jsonify({
            "status": "ok",
            "workspace": workspace
        })
    
    @app.route('/api/collaboration/workspace/<workspace_id>/resource', methods=['POST'])
    def add_resource(workspace_id):
        """Add a resource to a workspace."""
        data = request.json
        workspace = _get_workspace(workspace_id)
        
        if not workspace:
            return jsonify({"error": "Workspace not found"}), 404
        
        resource_name = data.get('name')
        resource_type = data.get('type')
        resource_url = data.get('url')
        
        if not resource_name or not resource_type:
            return jsonify({"error": "Missing resource name or type"}), 400
        
        resource = {
            "id": f"res-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "name": resource_name,
            "type": resource_type,
            "url": resource_url,
            "created_at": datetime.now().isoformat()
        }
        
        workspace['resources'].append(resource)
        workspace['updated_at'] = datetime.now().isoformat()
        
        _save_workspace(workspace)
        
        return jsonify({
            "status": "ok",
            "resource": resource
        })

def _get_all_workspaces():
    """Get all workspaces from disk."""
    workspaces = []
    workspace_dir = "data/collaboration"
    
    try:
        for filename in os.listdir(workspace_dir):
            if filename.endswith(".json") and filename.startswith("workspace-"):
                workspace_path = os.path.join(workspace_dir, filename)
                with open(workspace_path, "r") as f:
                    workspace = json.load(f)
                    workspaces.append(workspace)
    except Exception as e:
        logger.error(f"Error loading workspaces: {e}")
    
    return workspaces

def _get_workspace(workspace_id):
    """Get a specific workspace from disk."""
    workspace_path = os.path.join("data/collaboration", f"workspace-{workspace_id}.json")
    
    if os.path.exists(workspace_path):
        try:
            with open(workspace_path, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading workspace: {e}")
    
    return None

def _save_workspace(workspace):
    """Save a workspace to disk."""
    workspace_path = os.path.join("data/collaboration", f"workspace-{workspace['id']}.json")
    
    try:
        with open(workspace_path, "w") as f:
            json.dump(workspace, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving workspace: {e}")

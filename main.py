import os
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")
CORS(app)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# API routes
@app.route('/api/portals', methods=['GET'])
def get_portals():
    portals = [
        {"id": "xuveteam", "name": "XuveTeam", "level": "Advanced", "activity": "Managing collaboration workflow"},
        {"id": "xuvecode", "name": "XuveCode", "level": "Mastery", "activity": "Building secure smart contracts"},
        {"id": "xuvevision", "name": "XuveVision", "level": "Advanced", "activity": "Processing video content"},
        {"id": "xuvebanker", "name": "XuveBank", "level": "Mastery", "activity": "Managing token distribution"},
        {"id": "xuveops", "name": "XuveOps", "level": "Advanced", "activity": "Optimizing system performance"},
        {"id": "xuvelegal", "name": "XuveLegal", "level": "Basic", "activity": "Updating compliance documentation"},
        {"id": "xuvehome", "name": "XuveHome", "level": "Advanced", "activity": "Personalizing user environment"},
        {"id": "xuvefleet", "name": "XuveFleet", "level": "Basic", "activity": "Coordinating resource allocation"}
    ]
    return jsonify(portals)

# Status endpoint
@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "environment": "production"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

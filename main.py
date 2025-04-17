import os
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime

# Initialize logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")
CORS(app)

# Configure upload folder
app.config['UPLOAD_FOLDER'] = 'uploads/videos'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///lumaura.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Import and register XuveVision module
try:
    from xuvision import register_xuvision
    app = register_xuvision(app)
    logger.info("XuveVision module registered successfully")
except ImportError:
    logger.warning("XuveVision module not found or could not be registered")

# Import and register XuveCode module
try:
    from xuvecode import register_xuvecode
    app = register_xuvecode(app)
    logger.info("XuveCode module registered successfully")
except ImportError:
    logger.warning("XuveCode module not found or could not be registered")

# Import portal evolution system if available
try:
    from lumaura_ai_system.portal_evolution_system import PortalEvolutionSystem
    from routes.portal_evolution_routes import portal_evolution_bp
    
    # Initialize portal evolution system
    portal_evolution = PortalEvolutionSystem()
    portal_evolution.initialize()
    logger.info("Portal Evolution System initialized")
    
    # Register portal evolution routes
    app.register_blueprint(portal_evolution_bp, url_prefix='/portal-evolution')
    logger.info("Portal Evolution routes registered at /portal-evolution")
except ImportError:
    logger.warning("Portal Evolution System not found or could not be registered")

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# API Status route
@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "environment": os.environ.get("FLASK_ENV", "production"),
        "modules": {
            "xuvevision": "xuvision" in globals(),
            "xuvecode": "xuvecode" in globals(),
            "portal_evolution": "portal_evolution" in globals()
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

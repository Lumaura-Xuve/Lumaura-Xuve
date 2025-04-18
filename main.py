"""
LUMAURA x XUVE Main Application

This is the main entry point for the LUMAURA x XUVE platform.
It initializes all components and starts the Flask web server.
"""

import os
import logging
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if os.environ.get("FLASK_ENV") == "development" else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "lumaura-xuve-dev-key")

# Enable CORS
CORS(app)

# Configure database if needed
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data/lumaura_xuve.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Initialize database if needed
# from models import db
# db.init_app(app)
# with app.app_context():
#     db.create_all()

# Import and register routes
try:
    # Portal Evolution System
    from lumaura_ai_system.portal_evolution_system import PortalEvolutionSystem
    portal_system = PortalEvolutionSystem()
    portal_system.initialize()
    
    from routes.portal_evolution_routes import register_routes as register_portal_routes
    register_portal_routes(app, portal_system)
    logger.info("Portal Evolution System initialized and routes registered at /portal-evolution")
except Exception as e:
    logger.error(f"Error initializing Portal Evolution System: {str(e)}")
    portal_system = None

try:
    # Collaboration System
    from routes.collaboration_routes import register_routes as register_collaboration_routes
    register_collaboration_routes(app)
    logger.info("Collaboration routes registered at /collaboration")
except Exception as e:
    logger.error(f"Error registering collaboration routes: {str(e)}")

try:
    # AI Services
    from routes.ai_routes import register_routes as register_ai_routes
    register_ai_routes(app)
    logger.info("AI routes registered at /ai")
except Exception as e:
    logger.error(f"Error registering AI routes: {str(e)}")

# Check AI providers availability
try:
    from services.ai.openai_service import is_available as is_openai_available
    from services.ai.anthropic_service import is_available as is_anthropic_available
    
    if not (is_openai_available() or is_anthropic_available()):
        logger.warning("No AI providers available")
except Exception as e:
    logger.error(f"Error checking AI providers: {str(e)}")

# Initialize XuveVision module if available
try:
    from xuvevision import register_app as register_xuvevision
    register_xuvevision(app)
    logger.info("XuveVision module registered at /xuvevision")
except ImportError:
    logger.warning("XuveVision module not found or could not be registered")
except Exception as e:
    logger.error(f"Error registering XuveVision module: {str(e)}")

# Initialize XuveCode module if available
try:
    from xuvecode import register_app as register_xuvecode
    register_xuvecode(app)
    logger.info("XuveCode module registered successfully")
except ImportError:
    logger.warning("XuveCode module not found or could not be registered")
except Exception as e:
    logger.error(f"Error registering XuveCode module: {str(e)}")

# Initialize blockchain services
try:
    from services.blockchain_service import initialize_blockchain
    from services.token_service import initialize_token_contract
    from services.token_metadata_service import get_token_metadata
    
    # Initialize blockchain connection
    blockchain_provider = initialize_blockchain()
    
    # Initialize token contract
    token_contract = None
    if blockchain_provider:
        token_address = os.environ.get("XUVE_TOKEN_ADDRESS")
        token_contract = initialize_token_contract(blockchain_provider, token_address)
    
    # Get token metadata
    token_metadata = get_token_metadata(token_contract) if token_contract else None
    logger.info(f"XUVE token metadata: {token_metadata}")
    
    # Initialize bridge services
    try:
        from services.auto_bridge_service import initialize_bridge
        bridge_initialized = initialize_bridge(blockchain_provider)
        if not bridge_initialized:
            logger.warning("Real blockchain bridge not initialized")
    except ImportError:
        logger.warning("Blockchain bridge service not found")
    
    logger.info("Blockchain services initialized successfully")
except ImportError:
    logger.warning("Blockchain services not found")
except Exception as e:
    logger.error(f"Error initializing blockchain services: {str(e)}")

# Initialize Wise and direct CAD services
try:
    from services.wise_service import WiseService
    wise_service = WiseService()
    logger.info("Wise service initialized")
    
    from services.direct_cad_bridge import DirectCADBridge
    direct_cad_bridge = DirectCADBridge()
    logger.info("Direct CAD bridge initialized and ready")
except ImportError:
    logger.warning("Wise services not found")
except Exception as e:
    logger.error(f"Error initializing Wise services: {str(e)}")

# Define base routes
@app.route('/')
def index():
    """Main landing page."""
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    """API status endpoint."""
    return jsonify({
        "status": "ok",
        "version": "0.1.0",
        "portal_system": bool(portal_system),
        "ai_providers": {
            "openai": is_openai_available() if 'is_openai_available' in locals() else False,
            "anthropic": is_anthropic_available() if 'is_anthropic_available' in locals() else False
        }
    })

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    logger.error(f"Server error: {str(e)}")
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

"""
LUMAURA AI System

This package contains the core AI ecosystem that powers the LUMAURA x XUVE platform.
It manages the evolution and interaction of the various AI portals.
"""

import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if os.environ.get("FLASK_ENV") == "development" else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

logger.info("Initializing LUMAURA AI System")

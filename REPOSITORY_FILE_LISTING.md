# LUMAURA x XUVE Repository File Structure

This document provides an overview of all key files and directories in the repository for easy reference.

## Root Files

- **main.py** - Main Flask application entry point
- **requirements.txt** - Python dependencies
- **README.md** - Project overview
- **.env.example** - Environment variable template
- **initialize.sh** - System initialization script

## Core AI Portal System

### Portal Evolution Framework
- **/lumaura_ai_system/__init__.py** - System initialization
- **/lumaura_ai_system/portal_evolution_system.py** - Core evolution engine 
- **/lumaura_ai_system/portal_activity_generator.py** - Activity simulation engine

### Portal Implementations
Each portal follows the same structure with specialized functionality:

- **/lumaura_ai_system/portals/xuvebanker/** - Financial operations portal
  - **__init__.py** - Portal class definition
  - **functions.py** - Banking-specific functions

- **/lumaura_ai_system/portals/xuvemark/** - Marketing intelligence portal
  - **__init__.py** - Portal class definition
  - **functions.py** - Marketing-specific functions

- **/lumaura_ai_system/portals/xuveteam/** - Team collaboration portal
  - **__init__.py** - Portal class definition
  - **functions.py** - Team-specific functions

- **/lumaura_ai_system/portals/xuvecode/** - Code generation portal
  - **__init__.py** - Portal class definition
  - **functions.py** - Code-specific functions

- **/lumaura_ai_system/portals/xuvevault/** - Security management portal
  - **__init__.py** - Portal class definition
  - **functions.py** - Security-specific functions

- **/lumaura_ai_system/portals/xuveops/** - Operations management portal
  - **__init__.py** - Portal class definition
  - **functions.py** - Operations-specific functions

- **/lumaura_ai_system/portals/xuvecast/** - Media distribution portal
  - **__init__.py** - Portal class definition
  - **functions.py** - Media-specific functions

- **/lumaura_ai_system/portals/xuvemirror/** - System monitoring portal
  - **__init__.py** - Portal class definition
  - **functions.py** - Monitoring-specific functions

- **/lumaura_ai_system/portals/xuvehome/** - Home dashboard portal
  - **__init__.py** - Portal class definition
  - **functions.py** - Dashboard-specific functions

- **/lumaura_ai_system/portals/xuvewisdom/** - Knowledge management portal
  - **__init__.py** - Portal class definition
  - **functions.py** - Knowledge-specific functions

- **/lumaura_ai_system/portals/xuveteach/** - Educational portal
  - **__init__.py** - Portal class definition
  - **functions.py** - Learning-specific functions

- **/lumaura_ai_system/portals/xuveritual/** - Routine management portal
  - **__init__.py** - Portal class definition
  - **functions.py** - Habit formation functions

- **/lumaura_ai_system/portals/xuveonboard/** - Onboarding portal
  - **__init__.py** - Portal class definition
  - **functions.py** - Onboarding-specific functions

- **/lumaura_ai_system/portals/xuvewell/** - Wellness portal
  - **__init__.py** - Portal class definition
  - **functions.py** - Wellness-specific functions

- **/lumaura_ai_system/portals/xuvefamily/** - Community management portal
  - **__init__.py** - Portal class definition
  - **functions.py** - Community-specific functions

- **/lumaura_ai_system/portals/xuvejobs/** - Career opportunities portal
  - **__init__.py** - Portal class definition
  - **functions.py** - Job-specific functions

- **/lumaura_ai_system/portals/xuvefleet/** - Resource management portal
  - **__init__.py** - Portal class definition
  - **functions.py** - Resource-specific functions

- **/lumaura_ai_system/portals/xuvesponsorship/** - Partnership portal
  - **__init__.py** - Portal class definition
  - **functions.py** - Partnership-specific functions

- **/lumaura_ai_system/portals/xuvesound/** - Audio processing portal
  - **__init__.py** - Portal class definition
  - **functions.py** - Audio-specific functions

- **/lumaura_ai_system/portals/xuvecreator/** - Creative design portal
  - **__init__.py** - Portal class definition
  - **functions.py** - Creative-specific functions

- **/lumaura_ai_system/portals/xuvepulse/** - Analytics portal
  - **__init__.py** - Portal class definition
  - **functions.py** - Analytics-specific functions

- **/lumaura_ai_system/portals/xuvelegal/** - Legal compliance portal
  - **__init__.py** - Portal class definition
  - **functions.py** - Legal-specific functions

## API Integration Services

### AI Services
- **/services/ai/ai_factory.py** - Factory pattern for AI services
- **/services/ai/openai_service.py** - OpenAI integration (GPT-4o)
- **/services/ai/anthropic_service.py** - Anthropic integration (Claude)

### Financial Services
- **/services/wise_service.py** - Wise API integration
- **/services/direct_cad_bridge.py** - CAD transfer bridge
- **/services/transaction_service.py** - Transaction management

### Blockchain Services
- **/services/blockchain_service.py** - Web3 integration
- **/services/token_service.py** - XUVE token management
- **/services/token_metadata_service.py** - Token metadata
- **/services/polygonscan_service.py** - Polygonscan API
- **/services/gasless_transaction_service.py** - Gasless transactions

### Additional Services
- **/services/tax_tracking_service.py** - Tax compliance
- **/services/voice_service.py** - Voice processing
- **/services/dashboard_data.py** - Dashboard data provider

## Web Routes

- **/routes/portal_evolution_routes.py** - Portal evolution API
- **/routes/collaboration_routes.py** - Team collaboration API
- **/routes/ai_routes.py** - AI service API
- **/routes/transfer_status_routes.py** - Financial transfer API

## Feature Modules

### XuveVision Module
- **/xuvevision/__init__.py** - Module initialization
- **/xuvevision/api/routes.py** - Video API routes
- **/xuvevision/utils/transcription.py** - Video transcription

### XuveCode Module
- **/xuvecode/__init__.py** - Module initialization
- **/xuvecode/api/routes.py** - Code API routes
- **/xuvecode/utils/ai_generation.py** - AI code generation

## Frontend Assets

### Stylesheets
- **/static/css/styles.css** - Main stylesheet

### JavaScript
- **/static/js/app.js** - Main JavaScript
- **/static/js/portal_system/holographic-ui.js** - Holographic effects
- **/static/js/portal_system/particle-system.js** - Particle visualizations
- **/static/js/portal_system/portal-interactions.js** - Portal interactivity

### Images
- **/static/img/lumaura-xuve-logo.svg** - Main logo
- **/static/img/xuve-token-logo.svg** - Token logo
- **/static/img/video-placeholder.svg** - Video placeholder
- **/static/img/portal_avatars/** - Portal avatar images

## HTML Templates

- **/templates/index.html** - Main landing page
- **/templates/portal_dashboard.html** - Portal evolution dashboard
- **/templates/collaboration_dashboard.html** - Team collaboration
- **/templates/xuvevision/dashboard.html** - XuveVision dashboard
- **/templates/xuvecode/dashboard.html** - XuveCode dashboard

## Blockchain Contracts

- **/contracts/XuveToken.sol** - XUVE token contract (ERC-20)
- **/contracts/README.md** - Contract documentation

## Documentation

- **/docs/PORTAL_EVOLUTION_SYSTEM.md** - Portal evolution docs
- **/docs/HOLOGRAPHIC_UI_SYSTEM.md** - Holographic UI docs
- **/SYSTEM_USAGE_GUIDE.md** - Complete usage guide
- **/REPOSITORY_DOWNLOAD_INSTRUCTIONS.md** - Download instructions

## Deployment Scripts

- **/scripts/deploy_token.js** - Token deployment script
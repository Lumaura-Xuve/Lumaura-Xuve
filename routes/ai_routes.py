"""
AI Routes

This module defines the API routes for AI services.
"""

import logging
from flask import jsonify, request, render_template
import base64
import os

logger = logging.getLogger(__name__)

def register_routes(app):
    """Register AI routes with the Flask app."""
    logger.info("AI routes registered")
    
    @app.route('/ai')
    def ai_dashboard():
        """Render the AI dashboard."""
        return render_template('ai/dashboard.html')
    
    @app.route('/api/ai/generate-text', methods=['POST'])
    def generate_text():
        """Generate text using AI."""
        data = request.json
        prompt = data.get('prompt')
        provider = data.get('provider')
        use_case = data.get('use_case')
        max_tokens = data.get('max_tokens', 500)
        
        if not prompt:
            return jsonify({"error": "Missing prompt"}), 400
        
        try:
            from services.ai.ai_factory import AIFactory
            
            ai_service = AIFactory.get_provider(provider, use_case)
            
            if not ai_service:
                return jsonify({"error": "No AI service available"}), 503
            
            text = ai_service.generate_text(prompt, max_tokens)
            
            return jsonify({
                "status": "ok",
                "text": text
            })
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/ai/generate-json', methods=['POST'])
    def generate_json():
        """Generate JSON using AI."""
        data = request.json
        prompt = data.get('prompt')
        schema = data.get('schema')
        provider = data.get('provider')
        use_case = data.get('use_case')
        
        if not prompt:
            return jsonify({"error": "Missing prompt"}), 400
        
        try:
            from services.ai.ai_factory import AIFactory
            
            ai_service = AIFactory.get_provider(provider, use_case)
            
            if not ai_service:
                return jsonify({"error": "No AI service available"}), 503
            
            result = ai_service.generate_json(prompt, schema)
            
            return jsonify({
                "status": "ok",
                "result": result
            })
        except Exception as e:
            logger.error(f"Error generating JSON: {e}")
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/ai/analyze-image', methods=['POST'])
    def analyze_image():
        """Analyze an image using AI."""
        # Check if files were uploaded
        if 'image' in request.files:
            file = request.files['image']
            image_data = base64.b64encode(file.read()).decode('utf-8')
            prompt = request.form.get('prompt', 'Describe this image in detail')
            provider = request.form.get('provider')
            use_case = request.form.get('use_case', 'image_analysis')
        else:
            # Handle JSON payload
            data = request.json
            image_data = data.get('image_data')
            prompt = data.get('prompt', 'Describe this image in detail')
            provider = data.get('provider')
            use_case = data.get('use_case', 'image_analysis')
        
        if not image_data:
            return jsonify({"error": "Missing image data"}), 400
        
        try:
            from services.ai.ai_factory import AIFactory
            
            ai_service = AIFactory.get_provider(provider, use_case)
            
            if not ai_service:
                return jsonify({"error": "No AI service available"}), 503
            
            analysis = ai_service.analyze_image(image_data, prompt)
            
            return jsonify({
                "status": "ok",
                "analysis": analysis
            })
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            return jsonify({"error": str(e)}), 500

"""
OpenAI Service Integration

This module provides integration with OpenAI's AI services for the LUMAURA x XUVE platform.
"""

import os
import logging
import json

logger = logging.getLogger(__name__)

# Check if OpenAI Python package is installed
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI Python package not installed")

def is_available():
    """Check if OpenAI service is available."""
    api_key = os.environ.get("OPENAI_API_KEY")
    return OPENAI_AVAILABLE and api_key is not None

class OpenAIService:
    """Service for OpenAI integration."""
    
    def __init__(self):
        """Initialize the OpenAI service."""
        if not is_available():
            raise ValueError("OpenAI service is not available")
        
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.default_model = "gpt-4o"  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024
        logger.info("OpenAI service initialized")
    
    def generate_text(self, prompt, max_tokens=1000, model=None):
        """Generate text from a prompt."""
        try:
            model = model or self.default_model
            
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating text with OpenAI: {e}")
            return f"Error generating text: {str(e)}"
    
    def generate_json(self, prompt, schema=None, model=None):
        """Generate JSON-formatted response from a prompt."""
        try:
            model = model or self.default_model
            
            system_message = "You are a helpful AI assistant. Respond with valid JSON."
            if schema:
                system_message += f" Use this schema: {json.dumps(schema)}"
            
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                max_tokens=1000
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Error generating JSON with OpenAI: {e}")
            return {"error": str(e)}
    
    def analyze_image(self, image_data, prompt="Describe this image in detail"):
        """Analyze an image and provide a description."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",  # GPT-4o required for vision capabilities
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                            }
                        ]
                    }
                ],
                max_tokens=500
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error analyzing image with OpenAI: {e}")
            return f"Error analyzing image: {str(e)}"

def get_service():
    """Get an instance of the OpenAI service."""
    if is_available():
        try:
            return OpenAIService()
        except Exception as e:
            logger.error(f"Error creating OpenAI service: {e}")
    
    return None

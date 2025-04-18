"""
Anthropic Service Integration

This module provides integration with Anthropic's Claude AI services for the LUMAURA x XUVE platform.
"""

import os
import logging
import json

logger = logging.getLogger(__name__)

# Check if Anthropic Python package is installed
try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logger.warning("Anthropic Python package not installed")

def is_available():
    """Check if Anthropic service is available."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    return ANTHROPIC_AVAILABLE and api_key is not None

class AnthropicService:
    """Service for Anthropic integration."""
    
    def __init__(self):
        """Initialize the Anthropic service."""
        if not is_available():
            raise ValueError("Anthropic service is not available")
        
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=self.api_key)
        self.default_model = "claude-3-5-sonnet-20241022"  # the newest Anthropic model is "claude-3-5-sonnet-20241022"
        logger.info("Anthropic service initialized")
    
    def generate_text(self, prompt, max_tokens=1000, model=None):
        """Generate text from a prompt."""
        try:
            model = model or self.default_model
            
            message = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return message.content[0].text
        except Exception as e:
            logger.error(f"Error generating text with Anthropic: {e}")
            return f"Error generating text: {str(e)}"
    
    def generate_json(self, prompt, schema=None, model=None):
        """Generate JSON-formatted response from a prompt."""
        try:
            model = model or self.default_model
            
            system_prompt = "Respond with valid JSON."
            if schema:
                system_prompt += f" Use this schema: {json.dumps(schema)}"
            
            # Anthropic needs explicit instructions for JSON format in the prompt
            json_prompt = f"{prompt}\n\nPlease format your entire response as a valid JSON object."
            
            message = self.client.messages.create(
                model=model,
                max_tokens=1000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": json_prompt}
                ]
            )
            
            # Extract JSON from response text
            response_text = message.content[0].text
            
            # Find and extract JSON
            import re
            json_match = re.search(r'```json\s*([\s\S]*?)\s*```', response_text)
            if json_match:
                json_str = json_match.group(1)
            else:
                json_str = response_text
            
            # Clean and parse
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                # Try to fix common JSON issues
                fixed_json = re.sub(r'([{,])\s*([a-zA-Z0-9_]+)\s*:', r'\1"\2":', json_str)
                return json.loads(fixed_json)
        except Exception as e:
            logger.error(f"Error generating JSON with Anthropic: {e}")
            return {"error": str(e)}
    
    def analyze_image(self, image_data, prompt="Describe this image in detail"):
        """Analyze an image and provide a description."""
        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",  # Claude 3 required for vision
                max_tokens=1000,
                messages=[
                    {
                        "role": "user", 
                        "content": [
                            {
                                "type": "text", 
                                "text": prompt
                            },
                            {
                                "type": "image", 
                                "source": {
                                    "type": "base64", 
                                    "media_type": "image/jpeg", 
                                    "data": image_data
                                }
                            }
                        ]
                    }
                ]
            )
            
            return message.content[0].text
        except Exception as e:
            logger.error(f"Error analyzing image with Anthropic: {e}")
            return f"Error analyzing image: {str(e)}"

def get_service():
    """Get an instance of the Anthropic service."""
    if is_available():
        try:
            return AnthropicService()
        except Exception as e:
            logger.error(f"Error creating Anthropic service: {e}")
    
    return None

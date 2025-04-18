"""
AI Factory Module

This module provides a factory pattern for creating AI service instances.
The factory determines which AI provider to use based on available credentials and use case.
"""

import os
import logging
import importlib

logger = logging.getLogger(__name__)

class AIFactory:
    """Factory for creating AI service instances."""
    
    PROVIDERS = ["openai", "anthropic"]
    
    @staticmethod
    def get_provider(provider_name=None, use_case=None):
        """
        Get an AI provider service.
        
        Args:
            provider_name (str, optional): Specific provider to use
            use_case (str, optional): Use case to determine best provider
            
        Returns:
            object: AI provider service or None if not available
        """
        # If provider specified, attempt to use that one
        if provider_name and provider_name.lower() in AIFactory.PROVIDERS:
            return AIFactory._get_specific_provider(provider_name.lower())
        
        # Otherwise, try each provider in order of preference based on use case
        preferred_order = AIFactory._get_preferred_order(use_case)
        
        for provider in preferred_order:
            service = AIFactory._get_specific_provider(provider)
            if service:
                logger.info(f"Using {provider} for AI service")
                return service
        
        logger.warning("No AI providers available")
        return None
    
    @staticmethod
    def _get_specific_provider(provider_name):
        """Get a specific AI provider service."""
        try:
            # Import the provider module
            module_name = f"services.ai.{provider_name}_service"
            provider_module = importlib.import_module(module_name)
            
            # Check if provider is available
            is_available_func = getattr(provider_module, "is_available", None)
            if is_available_func and is_available_func():
                # Get the service
                get_service_func = getattr(provider_module, "get_service", None)
                if get_service_func:
                    return get_service_func()
                else:
                    logger.warning(f"No get_service function in {provider_name}_service")
            else:
                logger.debug(f"{provider_name} is not available")
        except ImportError:
            logger.warning(f"Could not import {provider_name}_service")
        except Exception as e:
            logger.error(f"Error getting {provider_name} service: {e}")
        
        return None
    
    @staticmethod
    def _get_preferred_order(use_case):
        """Get preferred provider order based on use case."""
        # Default order
        default_order = ["openai", "anthropic"]
        
        # Different order for specific use cases
        use_case_preferences = {
            "code_generation": ["openai", "anthropic"],
            "content_creation": ["anthropic", "openai"],
            "image_analysis": ["openai", "anthropic"],
            "financial_analysis": ["openai", "anthropic"],
            "marketing": ["anthropic", "openai"],
        }
        
        return use_case_preferences.get(use_case, default_order)

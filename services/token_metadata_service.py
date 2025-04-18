"""
Token Metadata Service

This module provides services for fetching and managing XUVE token metadata.
"""

import os
import logging
import json
import requests

logger = logging.getLogger(__name__)

def get_token_metadata(contract):
    """Get token metadata from the contract."""
    if not contract:
        logger.error("Token contract address not provided")
        return None
    
    try:
        # Get basic token info
        name = contract.functions.name().call()
        symbol = contract.functions.symbol().call()
        decimals = contract.functions.decimals().call()
        total_supply = contract.functions.totalSupply().call()
        
        # Format total supply with proper decimal places
        formatted_total_supply = total_supply / (10 ** decimals)
        
        metadata = {
            "name": name,
            "symbol": symbol,
            "decimals": decimals,
            "total_supply": total_supply,
            "formatted_total_supply": formatted_total_supply
        }
        
        logger.info(f"Retrieved token metadata: {metadata}")
        return metadata
    except Exception as e:
        logger.error(f"Error getting token metadata: {e}")
        return None

def save_token_logo(logo_url, save_path="static/img/token-logo.png"):
    """Save token logo from URL to local file."""
    try:
        response = requests.get(logo_url, stream=True)
        response.raise_for_status()
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Save the file
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        logger.info(f"Token logo saved to {save_path}")
        return save_path
    except Exception as e:
        logger.error(f"Error saving token logo: {e}")
        return None

def get_token_price(token_symbol="XUVE", currency="USD"):
    """Get token price from external API."""
    # This would typically fetch from a price API like CoinGecko
    # For now, we'll return a mock price
    logger.info(f"Fetching price for {token_symbol}/{currency}")
    return {
        "symbol": token_symbol,
        "price": 0.15,  # Mock price
        "currency": currency,
        "timestamp": "2023-09-01T12:00:00Z",  # Mock timestamp
        "source": "mock"
    }

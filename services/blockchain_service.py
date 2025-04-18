"""
Blockchain Service

This module provides integration with the Polygon blockchain network for
XUVE token operations and other blockchain interactions.
"""

import os
import logging
import json
from web3 import Web3

logger = logging.getLogger(__name__)

def initialize_blockchain():
    """Initialize connection to the blockchain network."""
    # Get RPC URL from environment variable or use default
    rpc_url = os.environ.get("POLYGON_RPC_URL", "https://polygon-rpc.com")
    
    try:
        # Create Web3 provider
        provider = Web3.HTTPProvider(rpc_url)
        web3 = Web3(provider)
        
        # Check connection
        if not web3.is_connected():
            logger.error(f"Failed to connect to Polygon node at {rpc_url}")
            return None
        
        logger.info(f"Connected to Polygon network: {web3.net.version}")
        return web3
    except Exception as e:
        logger.error(f"Failed to connect to Polygon node at {rpc_url}")
        logger.error(str(e))
        return None

def get_gas_price(web3):
    """Get current gas price on the network."""
    if not web3:
        return None
    
    try:
        gas_price = web3.eth.gas_price
        return gas_price
    except Exception as e:
        logger.error(f"Error getting gas price: {e}")
        return None

def get_transaction_receipt(web3, tx_hash):
    """Get transaction receipt for a given transaction hash."""
    if not web3:
        return None
    
    try:
        receipt = web3.eth.get_transaction_receipt(tx_hash)
        return receipt
    except Exception as e:
        logger.error(f"Error getting transaction receipt: {e}")
        return None

def estimate_gas(web3, transaction):
    """Estimate gas for a transaction."""
    if not web3:
        return None
    
    try:
        gas_estimate = web3.eth.estimate_gas(transaction)
        return gas_estimate
    except Exception as e:
        logger.error(f"Error estimating gas: {e}")
        return None

def send_transaction(web3, transaction, private_key):
    """Send a transaction to the blockchain."""
    if not web3:
        return None
    
    try:
        # Sign transaction
        signed_tx = web3.eth.account.sign_transaction(transaction, private_key)
        
        # Send transaction
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        return tx_hash.hex()
    except Exception as e:
        logger.error(f"Error sending transaction: {e}")
        return None

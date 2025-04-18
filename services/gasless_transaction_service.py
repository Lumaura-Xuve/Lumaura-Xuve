"""
Gasless Transaction Service

This module provides a service for executing gasless transactions on behalf of users.
This allows users to interact with the blockchain without needing to pay for gas.
"""

import os
import logging
import json
from web3 import Web3

logger = logging.getLogger(__name__)

class GaslessTransactionService:
    """Service for handling gasless transactions."""
    
    def __init__(self, web3, relayer_private_key):
        """Initialize the gasless transaction service."""
        self.web3 = web3
        self.relayer_private_key = relayer_private_key
        
        if not web3:
            logger.error("Cannot initialize gasless transaction service: Web3 not initialized")
            return
        
        if not relayer_private_key:
            logger.error("Cannot initialize gasless transaction service: Relayer private key not provided")
            return
        
        # Get relayer address from private key
        try:
            self.relayer_address = self.web3.eth.account.from_key(relayer_private_key).address
            logger.info(f"Gasless transaction service initialized with relayer: {self.relayer_address}")
        except Exception as e:
            logger.error(f"Error initializing gasless transaction service: {e}")
            self.relayer_address = None
    
    def is_available(self):
        """Check if the gasless transaction service is available."""
        return self.web3 is not None and self.relayer_private_key is not None and self.relayer_address is not None
    
    def execute_transaction(self, contract, function_name, function_args, user_signature, user_address):
        """Execute a transaction on behalf of a user who has signed the intent."""
        if not self.is_available():
            return {"error": "Gasless transaction service not available"}
        
        try:
            # Verify signature
            if not self._verify_signature(user_signature, user_address, function_name, function_args):
                return {"error": "Invalid signature"}
            
            # Get function from contract
            contract_function = getattr(contract.functions, function_name)
            
            # Build transaction
            nonce = self.web3.eth.get_transaction_count(self.relayer_address)
            
            tx = contract_function(*function_args).build_transaction({
                'chainId': int(self.web3.net.version),
                'gas': 200000,
                'gasPrice': self.web3.eth.gas_price,
                'nonce': nonce,
                'from': self.relayer_address
            })
            
            # Sign and send transaction
            signed_tx = self.web3.eth.account.sign_transaction(tx, self.relayer_private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            logger.info(f"Gasless transaction executed. Transaction hash: {tx_hash.hex()}")
            return {"success": True, "tx_hash": tx_hash.hex()}
        except Exception as e:
            logger.error(f"Error executing gasless transaction: {e}")
            return {"error": str(e)}
    
    def _verify_signature(self, signature, user_address, function_name, function_args):
        """Verify that the signature matches the user intent."""
        try:
            # Create message hash
            message = self.web3.keccak(text=f"{function_name}({','.join(map(str, function_args))})")
            
            # Recover signer address
            signature_bytes = self.web3.to_bytes(hexstr=signature)
            recovered_address = self.web3.eth.account.recover_message(
                message_hash=message,
                signature=signature_bytes
            )
            
            # Check if recovered address matches user address
            return recovered_address.lower() == user_address.lower()
        except Exception as e:
            logger.error(f"Error verifying signature: {e}")
            return False

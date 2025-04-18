"""
Direct CAD Bridge Service

This module provides a bridge between crypto assets and CAD via the Wise API.
It handles the direct sending of CAD to recipients based on token ownership.
"""

import os
import logging
import json
from datetime import datetime
import random
import uuid

from services.wise_service import WiseService

logger = logging.getLogger(__name__)

class DirectCADBridge:
    """Service for bridging between crypto and CAD."""
    
    def __init__(self):
        """Initialize the Direct CAD bridge."""
        self.wise_service = WiseService()
        self.transaction_log_dir = "data/direct_cad_bridge"
        
        # Create log directory if it doesn't exist
        os.makedirs(self.transaction_log_dir, exist_ok=True)
        
        logger.info("Direct CAD bridge initialized")
    
    def is_available(self):
        """Check if the bridge is available and properly configured."""
        return self.wise_service.is_available()
    
    def check_cad_balance(self):
        """Check the available CAD balance."""
        return self.wise_service.get_balance_for_currency("CAD")
    
    def send_cad_to_recipient(self, recipient_id, amount, description=None):
        """Send CAD to a recipient."""
        if not self.is_available():
            return {"error": "Direct CAD bridge not properly configured"}
        
        # Create a unique transaction ID
        transaction_id = f"DIRECT-{uuid.uuid4().hex[:8]}"
        
        # Create a quote for CAD
        quote = self.wise_service.create_quote("CAD", "CAD", source_amount=amount)
        if "error" in quote:
            self._log_transaction(transaction_id, "FAILED", "quote_error", {
                "recipient_id": recipient_id,
                "amount": amount,
                "error": quote.get("error")
            })
            return quote
        
        # Create the transfer
        transfer = self.wise_service.create_transfer(quote.get("id"), recipient_id)
        if "error" in transfer:
            self._log_transaction(transaction_id, "FAILED", "transfer_error", {
                "recipient_id": recipient_id,
                "amount": amount,
                "quote_id": quote.get("id"),
                "error": transfer.get("error")
            })
            return transfer
        
        # Fund the transfer from Wise balance
        funding = self.wise_service.fund_transfer(transfer.get("id"))
        if "error" in funding:
            self._log_transaction(transaction_id, "FAILED", "funding_error", {
                "recipient_id": recipient_id,
                "amount": amount,
                "transfer_id": transfer.get("id"),
                "error": funding.get("error")
            })
            return funding
        
        # Log the successful transaction
        transaction_data = {
            "recipient_id": recipient_id,
            "amount": amount,
            "quote_id": quote.get("id"),
            "transfer_id": transfer.get("id"),
            "description": description or "Direct CAD transfer"
        }
        self._log_transaction(transaction_id, "COMPLETED", "direct_transfer", transaction_data)
        
        return {
            "success": True,
            "transaction_id": transaction_id,
            "transfer_id": transfer.get("id"),
            "amount": amount,
            "status": "completed"
        }
    
    def get_transaction_status(self, transaction_id):
        """Get the status of a transaction."""
        transaction_log = self._get_transaction_log(transaction_id)
        
        if transaction_log:
            # If transaction was completed, check the status in Wise
            if transaction_log.get("status") == "COMPLETED" and "transfer_id" in transaction_log.get("data", {}):
                transfer_id = transaction_log["data"]["transfer_id"]
                wise_status = self.wise_service.get_transfer_status(transfer_id)
                
                if "error" not in wise_status:
                    return {
                        "transaction_id": transaction_id,
                        "status": wise_status.get("status", "UNKNOWN"),
                        "wise_details": wise_status
                    }
            
            # Return the logged status
            return {
                "transaction_id": transaction_id,
                "status": transaction_log.get("status"),
                "data": transaction_log.get("data")
            }
        
        return {"error": f"Transaction not found: {transaction_id}"}
    
    def create_recipient(self, recipient_data):
        """Create a new recipient account in Wise."""
        if not self.is_available():
            return {"error": "Direct CAD bridge not properly configured"}
        
        return self.wise_service.create_recipient(recipient_data)
    
    def get_recipients(self):
        """Get all recipient accounts."""
        if not self.is_available():
            return {"error": "Direct CAD bridge not properly configured"}
        
        return self.wise_service.get_recipients()
    
    def _log_transaction(self, transaction_id, status, type, data):
        """Log a transaction to disk."""
        log_file = os.path.join(self.transaction_log_dir, f"{transaction_id}.json")
        
        log_data = {
            "transaction_id": transaction_id,
            "status": status,
            "type": type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            with open(log_file, "w") as f:
                json.dump(log_data, f, indent=2)
            logger.info(f"Transaction logged: {transaction_id} ({status})")
        except Exception as e:
            logger.error(f"Error logging transaction: {e}")
    
    def _get_transaction_log(self, transaction_id):
        """Get a transaction log from disk."""
        log_file = os.path.join(self.transaction_log_dir, f"{transaction_id}.json")
        
        if os.path.exists(log_file):
            try:
                with open(log_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error reading transaction log: {e}")
        
        return None

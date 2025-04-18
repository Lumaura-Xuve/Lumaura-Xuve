"""
Wise API Service

This module provides integration with the Wise (formerly TransferWise) API
for managing international money transfers, particularly CAD transfers.
"""

import os
import requests
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class WiseService:
    """Service for interacting with the Wise API."""
    
    BASE_URL = "https://api.wise.com"
    API_VERSION = "v1"
    
    def __init__(self):
        """Initialize the Wise service."""
        self.api_token = os.environ.get("WISE_API_TOKEN")
        self.profile_id = os.environ.get("WISE_PROFILE_ID")
        
        if not self.api_token:
            logger.warning("Wise API token not set")
        
        if not self.profile_id:
            logger.warning("Wise profile ID not set")
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        })
        
        logger.info("Wise service initialized")
    
    def is_available(self):
        """Check if the Wise service is available and properly configured."""
        return bool(self.api_token and self.profile_id)
    
    def _make_request(self, method, endpoint, data=None, params=None):
        """Make a request to the Wise API."""
        url = f"{self.BASE_URL}/{self.API_VERSION}/{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request to Wise API: {e}")
            return {"error": str(e)}
    
    def get_profile(self):
        """Get the profile information."""
        if not self.is_available():
            return {"error": "Wise service not properly configured"}
        
        endpoint = f"profiles/{self.profile_id}"
        return self._make_request("GET", endpoint)
    
    def get_balances(self):
        """Get account balances."""
        if not self.is_available():
            return {"error": "Wise service not properly configured"}
        
        endpoint = f"profiles/{self.profile_id}/balances"
        return self._make_request("GET", endpoint)
    
    def get_balance_for_currency(self, currency="CAD"):
        """Get balance for a specific currency."""
        balances = self.get_balances()
        
        if "error" in balances:
            return balances
        
        for balance in balances:
            if balance.get("currency") == currency:
                return balance
        
        return {"error": f"No balance found for currency: {currency}"}
    
    def create_quote(self, source_currency, target_currency, source_amount=None, target_amount=None):
        """Create a quote for currency conversion."""
        if not self.is_available():
            return {"error": "Wise service not properly configured"}
        
        endpoint = "quotes"
        data = {
            "profile": self.profile_id,
            "sourceCurrency": source_currency,
            "targetCurrency": target_currency,
        }
        
        if source_amount:
            data["sourceAmount"] = source_amount
        elif target_amount:
            data["targetAmount"] = target_amount
        else:
            return {"error": "Either source_amount or target_amount must be provided"}
        
        return self._make_request("POST", endpoint, data=data)
    
    def create_transfer(self, quote_id, recipient_id):
        """Create a transfer based on a quote."""
        if not self.is_available():
            return {"error": "Wise service not properly configured"}
        
        endpoint = "transfers"
        data = {
            "targetAccount": recipient_id,
            "quoteUuid": quote_id,
            "customerTransactionId": f"TX-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        }
        
        return self._make_request("POST", endpoint, data=data)
    
    def get_transfer_status(self, transfer_id):
        """Get the status of a transfer."""
        if not self.is_available():
            return {"error": "Wise service not properly configured"}
        
        endpoint = f"transfers/{transfer_id}"
        return self._make_request("GET", endpoint)
    
    def create_recipient(self, account_data):
        """Create a recipient account."""
        if not self.is_available():
            return {"error": "Wise service not properly configured"}
        
        endpoint = f"accounts"
        account_data["profile"] = self.profile_id
        
        return self._make_request("POST", endpoint, data=account_data)
    
    def get_recipients(self):
        """Get all recipient accounts."""
        if not self.is_available():
            return {"error": "Wise service not properly configured"}
        
        endpoint = f"accounts?profile={self.profile_id}"
        return self._make_request("GET", endpoint)
    
    def get_recipient_by_id(self, recipient_id):
        """Get a specific recipient account."""
        if not self.is_available():
            return {"error": "Wise service not properly configured"}
        
        endpoint = f"accounts/{recipient_id}"
        return self._make_request("GET", endpoint)
    
    def fund_transfer(self, transfer_id, type="BALANCE"):
        """Fund a transfer from your Wise balance."""
        if not self.is_available():
            return {"error": "Wise service not properly configured"}
        
        endpoint = f"transfers/{transfer_id}/payments"
        data = {
            "type": type
        }
        
        return self._make_request("POST", endpoint, data=data)

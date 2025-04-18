"""
Token Service

This module provides services for interacting with the XUVE token contract.
"""

import os
import logging
import json
from web3 import Web3

logger = logging.getLogger(__name__)

# ABI for the XUVE token contract
TOKEN_ABI = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            }
        ],
        "name": "allowance",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "internalType": "uint8",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "transferFrom",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

def initialize_token_contract(web3, contract_address):
    """Initialize the XUVE token contract."""
    if not web3:
        logger.error("Cannot initialize token contract: Web3 not initialized")
        return None
    
    if not contract_address:
        logger.error("Cannot initialize token contract: Contract address not provided")
        return None
    
    try:
        # Create contract instance
        contract = web3.eth.contract(address=contract_address, abi=TOKEN_ABI)
        logger.info(f"Token contract initialized at address: {contract_address}")
        return contract
    except Exception as e:
        logger.error(f"Error initializing token contract: {e}")
        return None

def get_token_balance(contract, address):
    """Get token balance for an address."""
    if not contract:
        return None
    
    try:
        balance = contract.functions.balanceOf(address).call()
        return balance
    except Exception as e:
        logger.error(f"Error getting token balance: {e}")
        return None

def transfer_tokens(web3, contract, sender_private_key, sender_address, recipient_address, amount):
    """Transfer tokens from one address to another."""
    if not web3 or not contract:
        return None
    
    try:
        # Get nonce
        nonce = web3.eth.get_transaction_count(sender_address)
        
        # Build transaction
        tx = contract.functions.transfer(
            recipient_address,
            amount
        ).build_transaction({
            'chainId': int(web3.net.version),
            'gas': 200000,
            'gasPrice': web3.eth.gas_price,
            'nonce': nonce,
        })
        
        # Sign and send transaction
        signed_tx = web3.eth.account.sign_transaction(tx, sender_private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        logger.info(f"Tokens transferred. Transaction hash: {tx_hash.hex()}")
        return tx_hash.hex()
    except Exception as e:
        logger.error(f"Error transferring tokens: {e}")
        return None

def approve_spender(web3, contract, owner_private_key, owner_address, spender_address, amount):
    """Approve a spender to spend tokens on behalf of the owner."""
    if not web3 or not contract:
        return None
    
    try:
        # Get nonce
        nonce = web3.eth.get_transaction_count(owner_address)
        
        # Build transaction
        tx = contract.functions.approve(
            spender_address,
            amount
        ).build_transaction({
            'chainId': int(web3.net.version),
            'gas': 200000,
            'gasPrice': web3.eth.gas_price,
            'nonce': nonce,
        })
        
        # Sign and send transaction
        signed_tx = web3.eth.account.sign_transaction(tx, owner_private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        logger.info(f"Spender approved. Transaction hash: {tx_hash.hex()}")
        return tx_hash.hex()
    except Exception as e:
        logger.error(f"Error approving spender: {e}")
        return None

def get_token_info(contract):
    """Get basic information about the token."""
    if not contract:
        return None
    
    try:
        name = contract.functions.name().call()
        symbol = contract.functions.symbol().call()
        decimals = contract.functions.decimals().call()
        total_supply = contract.functions.totalSupply().call()
        
        return {
            "name": name,
            "symbol": symbol,
            "decimals": decimals,
            "total_supply": total_supply
        }
    except Exception as e:
        logger.error(f"Error getting token info: {e}")
        return None

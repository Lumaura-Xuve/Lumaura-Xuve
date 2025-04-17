# XUVE Token Smart Contracts

This directory contains the Solidity smart contracts for the XUVE token ecosystem.

## XuveToken.sol

The main ERC-20 token contract with the following features:
- 80 million total supply
- Mintable and burnable
- Pausable for emergency situations
- Vesting schedules for team and investor allocations
- Token distribution:
  - 20% Team allocation (16M tokens)
  - 15% Reserve allocation (12M tokens) 
  - 30% Ecosystem allocation (24M tokens)
  - 20% Presale allocation (16M tokens)
  - 15% Staking allocation (12M tokens)

## Deployment

The token is deployed on the Polygon network. See the `scripts/deploy_token.js` file for deployment instructions.

## Security

All contracts use OpenZeppelin's battle-tested contract libraries and follow security best practices.

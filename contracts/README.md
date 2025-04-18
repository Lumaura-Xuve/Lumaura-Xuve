# XUVE Token Contracts

This directory contains the smart contracts for the XUVE token and related functionality.

## Token Details

- **Name**: XUVE Token
- **Symbol**: XUVE
- **Decimals**: 18
- **Total Supply**: 80,000,000 XUVE

## Contract Structure

- `XUVEToken.sol`: The main ERC-20 token contract with vesting functionality
- Other contracts will be added as needed

## Deployment

The token is deployed on the Polygon network. To deploy to a local development environment or testnet:

```
npx hardhat run scripts/deploy_token.js --network <network-name>
```

## Testing

Run tests with:

```
npx hardhat test
```

## Security

The XUVE token contract uses OpenZeppelin's audited and battle-tested contracts as a base, enhancing security and reducing the risk of vulnerabilities.

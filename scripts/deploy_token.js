// Script to deploy the XUVE Token contract

const { ethers } = require("hardhat");

async function main() {
  console.log("Deploying XUVE Token contract...");

  // Get the contract factory
  const XUVEToken = await ethers.getContractFactory("XUVEToken");
  
  // Get signers
  const [deployer] = await ethers.getSigners();
  
  // For development, we'll use the deployer as all the wallets
  // In production, you would use different addresses
  const teamWallet = deployer.address;
  const treasuryWallet = deployer.address;
  const reserveWallet = deployer.address;
  const presaleWallet = deployer.address;
  
  // Deploy the token contract
  const token = await XUVEToken.deploy(
    teamWallet,
    treasuryWallet,
    reserveWallet,
    presaleWallet
  );
  
  await token.deployed();
  
  console.log("XUVE Token deployed to:", token.address);
  console.log("Total supply:", await token.totalSupply());
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });

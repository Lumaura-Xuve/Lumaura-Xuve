// This script deploys the XUVE token to the Polygon network

const hre = require("hardhat");

async function main() {
  // Deploy the XUVE token contract
  const XuveToken = await hre.ethers.getContractFactory("XuveToken");
  console.log("Deploying XUVE Token...");
  const token = await XuveToken.deploy();
  await token.deployed();
  
  console.log("XUVE Token deployed to:", token.address);
  
  // Wait for a few block confirmations to ensure the contract is confirmed
  console.log("Waiting for block confirmations...");
  await token.deployTransaction.wait(5);
  
  // Verify the contract on Polygonscan
  console.log("Verifying contract on Polygonscan...");
  try {
    await hre.run("verify:verify", {
      address: token.address,
      constructorArguments: [],
    });
    console.log("Contract verified on Polygonscan");
  } catch (error) {
    console.error("Error verifying contract:", error);
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });

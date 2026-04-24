const hre = require("hardhat");

async function main() {
  console.log("Deploying FraudLedger contract...");

  const FraudLedger = await hre.ethers.getContractFactory("FraudLedger");
  const fraudLedger = await FraudLedger.deploy();

  await fraudLedger.waitForDeployment();

  const address = await fraudLedger.getAddress();
  console.log("FraudLedger deployed to:", address);
  console.log("\nUpdate your backend/.env file with:");
  console.log(`CONTRACT_ADDRESS=${address}`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });

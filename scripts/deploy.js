async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);

  // Deploy HabitatProof with the new verifier address
  const verifierAddress = "0x411e5cd2473bf83792346bb174e0684dc9ac36ff";
  const HabitatProof = await ethers.getContractFactory("HabitatProof");
  const habitatProof = await HabitatProof.deploy(verifierAddress);
  await habitatProof.waitForDeployment();

  const address = await habitatProof.getAddress();
  console.log("HabitatProof deployed to:", address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  }); 
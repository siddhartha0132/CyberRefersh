const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("FraudLedger", function () {
  let fraudLedger;
  let owner;

  beforeEach(async function () {
    [owner] = await ethers.getSigners();
    const FraudLedger = await ethers.getContractFactory("FraudLedger");
    fraudLedger = await FraudLedger.deploy();
    await fraudLedger.waitForDeployment();
  });

  it("Should add a fraud event", async function () {
    const userHash = ethers.keccak256(ethers.toUtf8Bytes("9999999999"));
    const deviceHash = ethers.keccak256(ethers.toUtf8Bytes("device123"));
    const addressHash = ethers.keccak256(ethers.toUtf8Bytes("123 Main St"));
    const eventHash = ethers.keccak256(ethers.toUtf8Bytes("event1"));

    await fraudLedger.addFraudEvent(
      userHash,
      deviceHash,
      addressHash,
      "REFUND_ABUSE",
      3,
      eventHash
    );

    const count = await fraudLedger.getRiskEventCount(userHash);
    expect(count).to.equal(1);
  });

  it("Should retrieve user events", async function () {
    const userHash = ethers.keccak256(ethers.toUtf8Bytes("9999999999"));
    const deviceHash = ethers.keccak256(ethers.toUtf8Bytes("device123"));
    const addressHash = ethers.keccak256(ethers.toUtf8Bytes("123 Main St"));
    const eventHash = ethers.keccak256(ethers.toUtf8Bytes("event1"));

    await fraudLedger.addFraudEvent(
      userHash,
      deviceHash,
      addressHash,
      "FAKE_ORDER",
      3,
      eventHash
    );

    const events = await fraudLedger.getUserEvents(userHash);
    expect(events.length).to.equal(1);
    expect(events[0].eventType).to.equal("FAKE_ORDER");
  });

  it("Should emit FraudEventAdded event", async function () {
    const userHash = ethers.keccak256(ethers.toUtf8Bytes("9999999999"));
    const deviceHash = ethers.keccak256(ethers.toUtf8Bytes("device123"));
    const addressHash = ethers.keccak256(ethers.toUtf8Bytes("123 Main St"));
    const eventHash = ethers.keccak256(ethers.toUtf8Bytes("event1"));

    await expect(
      fraudLedger.addFraudEvent(
        userHash,
        deviceHash,
        addressHash,
        "CANCELLED",
        2,
        eventHash
      )
    ).to.emit(fraudLedger, "FraudEventAdded");
  });
});

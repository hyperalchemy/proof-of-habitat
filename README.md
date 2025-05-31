# Proof of Habitat 🛖

*This project is a privacy-first protocol developed as a proof of concept (PoC) for the ETHGlobal Prague 2025 hackathon. \
It was inspired by a thought provoking talk from [ETHPrague conference 2025](https://ethprague.com/schedule?talk=1009-proof-of-habitat-a-proposal-for-decentralized-wayfinding-and-local-first-community).*

## Overview

This is a proof-of-concept (POC) for a privacy-preserving decentralized protocol that uses RF fingerprinting—specifically Bluetooth Low Energy (BLE) signals—to passively validate location without relying on GPS or centralized systems. Using zero-knowledge proofs (zkSNARKs) generated with ZoKrates, the protocol ensures complete privacy by proving habitat presence without revealing any device identifiers, exact locations, or distances. Proof verification is performed on-chain via a Solidity verifier contract.

## Privacy-First Design

The protocol is built with privacy as the core principle:

1. **Device Privacy**: All device IDs are hashed before being used in proofs, ensuring that actual device identifiers are never exposed.

2. **Location Privacy**: Instead of revealing exact locations or distances:
   - Distances are bucketed into three ranges (0-5m, 5-15m, 15m+)
   - Location data is combined into a single "location bucket" using device hashes and distance buckets
   - The location bucket is a privacy-preserving identifier that only matches for users in very close proximity

3. **Temporal Privacy**: Timestamps are bucketed into 15-minute windows to prevent exact timing correlation

4. **Zero-Knowledge Proofs**: The ZoKrates circuit proves presence without revealing:
   - Actual device IDs or MAC addresses
   - Exact distances to devices
   - Precise timing information
   - Geographic coordinates

## How it works

1. Users collect BLE fingerprint data locally from nearby devices
2. The data is processed locally:
   - Device IDs are hashed
   - Distances are converted to buckets
   - A privacy-preserving location bucket is computed
3. A zero-knowledge proof is generated proving:
   - The user observed valid BLE devices
   - The devices were within reasonable distances
   - The location bucket was correctly computed
4. The proof is submitted to the verifier contract which:
   - Verifies the cryptographic proof
   - Stores only the privacy-preserving location bucket and time bucket
5. Co-location is determined by matching location buckets within the same time bucket

This process enables users to prove they were in the same general area without revealing exactly where they were or which devices they observed.

## Repository Structure

```
proof-of-habitat/
├── contracts/              # Smart contracts
│   └── HabitatProof.sol   # Main contract for proof verification
├── frontend/              # Web interface
│   ├── public/           # Static files
│   └── README.md         # Frontend documentation
├── scripts/              # Utility scripts
│   └── generate_proof_input.py  # Generate proof inputs from BLE data
├── test/                 # Contract tests
├── data/                 # Input and raw data
│   ├── input-*.json     # Generated proof inputs
│   └── raw_ble_data-*.json  # Raw BLE scan data
├── zokrates/            # ZoKrates circuits and proofs
├── hardhat.config.js    # Hardhat configuration
└── package.json         # Project dependencies
```

## Implementation Details

### Off-Chain Proof Generation

For the Proof-of-Habitat protocol POC, the script collects six nearby BLE devices with their associated distances, strategically selected to improve location matching reliability. The data is then formatted for zero-knowledge proof generation.

#### Device Selection Strategy
The script selects 6 devices across different distance ranges to improve location matching:
- 2 devices from close range (0-5 meters)
- 2 devices from medium range (5-15 meters)
- 2 devices from far range (15+ meters)

This diverse selection strategy helps ensure that:
1. Close devices provide precise location information
2. Medium-range devices add context about the surrounding area
3. Far devices help establish broader location context
4. Multiple devices in each range improve reliability

### Smart Contracts

#### Verifier Contract
The verifier smart contract has been deployed to Sepolia testnet:
- Verifier Contract: `0xddaa0bcbab7ea345ba1a815df22982f992f02255`

#### HabitatProof Contract
The HabitatProof contract provides privacy-preserving location verification by comparing location buckets. It implements:

**Privacy Parameters:**
- Time Bucket Size: 15 minutes (granularity of temporal matching)
- Location Buckets: 1000 possible values (granularity of spatial matching)
- No device IDs or distances stored on-chain

**Key Features:**
1. **Privacy-Preserving Storage**: Stores only:
   - Location bucket (computed from hashed devices and distance buckets)
   - Time bucket (15-minute window)
   - Prover's address

2. **Co-Location Detection**: Two proofs indicate co-location if:
   - They share the same location bucket
   - They were submitted in the same time bucket
   - Proofs are from different provers

3. **Events:**
   - `ProofSubmitted`: Emitted when a new proof is submitted
   - `CoLocationFound`: Emitted when co-location is detected

Contract Address: `0x4e062e65fe85bb47fcbe4d8f8331fc1d158db123`

## Development Setup

1. Install dependencies:
```
# ZoKrates Zero-Knowledge Proof Generation

This directory contains the ZoKrates implementation for generating and verifying zero-knowledge proofs for the Proof of Habitat protocol.

## Setup

Run the ZoKrates Docker container:
```bash
docker run -it --rm --platform linux/amd64 -v $(pwd):/home/zokrates/code -w /home/zokrates/code zokrates/zokrates /bin/bash
```

## Proof Generation Steps

1. **Generate Input Data**:
First, run the Python script to scan BLE devices and generate formatted input:
```bash
python3 scripts/generate_proof_input.py
```
This will create `input.json` with the following format:
```json
{
    "device1": "integer (hex device ID)",
    "distance1": "integer (distance in cm)",
    "device2": "integer (hex device ID)",
    "distance2": "integer (distance in cm)",
    "device3": "integer (hex device ID)",
    "distance3": "integer (distance in cm)",
    "device4": "integer (hex device ID)",
    "distance4": "integer (distance in cm)",
    "device5": "integer (hex device ID)",
    "distance5": "integer (distance in cm)",
    "device6": "integer (hex device ID)",
    "distance6": "integer (distance in cm)",
    "rfmedium": 1
}
```

2. **Compile the circuit**:
```bash
zokrates compile -i proof_of_habitat.zok
```

3. **Setup the proving system** (only needed once per circuit):
```bash
zokrates setup
```

4. **Format Witness Input**:
The witness input must be a space-separated list of values in this order:
```
<device1> <distance1> <device2> <distance2> <device3> <distance3> <device4> <distance4> <device5> <distance5> <device6> <distance6> <rfmedium>
```

For example, if your `input.json` contains:
```json
{
    "device1": "2869785",
    "distance1": "161",
    "device2": "4395913",
    "distance2": "527",
    ...
}
```

Your witness command would be:
```bash
zokrates compute-witness -a 2869785 161 4395913 527 1916176 785 3012946 1513 2501505 2344 3052927 4510 1
```

5. **Generate the proof**:
```bash
zokrates generate-proof
```
This creates `proof.json` with the following format:
```json
{
  "scheme": "g16",
  "curve": "bn128",
  "proof": {
    "a": ["0x...", "0x..."],
    "b": [["0x...", "0x..."], ["0x...", "0x..."]],
    "c": ["0x...", "0x..."]
  },
  "inputs": ["0x...", "0x..."]
}
```

6. **Verify the proof locally**:
```bash
zokrates verify
```

7. **Export the Solidity verifier**:
```bash
zokrates export-verifier
```
This generates `verifier.sol`, a Solidity smart contract containing the verification key and logic for your zk-SNARK proof.

## Submitting the Proof

1. Copy the entire contents of `proof.json`
2. Go to the Proof of Habitat frontend
3. Paste the proof JSON into the "Submit Proof" text area
4. Click "Submit Proof"

## Files in this Directory

- `proof_of_habitat.zok`: The ZoKrates circuit definition
- `out`: Compiled circuit output
- `out.r1cs`: R1CS constraint system
- `proof.json`: Generated zero-knowledge proof
- `verifier.sol`: Generated Solidity verifier contract
- `witness`: Computed witness
- `abi.json`: ABI for the verifier contract

## Troubleshooting

If your proof is rejected by the contract, check:
1. The proof was generated using the correct verifier contract (currently `0x411e5cd2473bf83792346bb174e0684dc9ac36ff`)
2. The input values are within valid ranges:
   - All distances must be < 5000 cm (50m)
   - The computed location bucket must be < 1000
3. The proof JSON format exactly matches the expected format shown above
4. You're connected to the correct network (Sepolia) in your wallet 
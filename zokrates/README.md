# ZoKrates Zero-Knowledge Proof Generation

This directory contains the ZoKrates implementation for generating and verifying zero-knowledge proofs for the Proof of Habitat protocol.

## Setup

Run the ZoKrates Docker container:
```bash
docker run -it --rm --platform linux/amd64 -v $(pwd):/home/zokrates/code -w /home/zokrates/code zokrates/zokrates /bin/bash
```

## Proof Generation Steps

1. **Compile the circuit**:
```bash
zokrates compile -i proof_of_habitat.zok
```

2. **Setup the proving system** (only needed once per circuit):
```bash
zokrates setup
```

3. **Compute witness** (using your BLE data inputs):
```bash
zokrates compute-witness -a <device1> <distance1> <device2> <distance2> <device3> <distance3> <device4> <distance4> <device5> <distance5> <device6> <distance6> <rfmedium>
```
Example:
```bash
zokrates compute-witness -a 2869785 161 4395913 527 1916176 785 3012946 1513 2501505 2344 3052927 4510 1
```

4. **Generate the proof**:
```bash
zokrates generate-proof
```

5. **Verify the proof locally**:
```bash
zokrates verify
```

6. **Export the Solidity verifier**:
```bash
zokrates export-verifier
```
This generates `verifier.sol`, a Solidity smart contract containing the verification key and logic for your zk-SNARK proof.

## Files in this Directory

- `proof_of_habitat.zok`: The ZoKrates circuit definition
- `out`: Compiled circuit output
- `out.r1cs`: R1CS constraint system
- `proof.json`: Generated zero-knowledge proof
- `verifier.sol`: Generated Solidity verifier contract
- `witness`: Computed witness
- `abi.json`: ABI for the verifier contract 
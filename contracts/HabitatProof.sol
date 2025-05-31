// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IVerifier {
    struct G1Point {
        uint X;
        uint Y;
    }

    struct G2Point {
        uint[2] X;
        uint[2] Y;
    }

    struct Proof {
        G1Point a;
        G2Point b;
        G1Point c;
    }

    function verifyTx(Proof memory proof, uint[2] memory input) external view returns (bool);
}

contract HabitatProof {
    IVerifier public verifier;
    
    struct ProofData {
        uint256 timestamp;  // Block timestamp when proof was submitted
        uint256 location_bucket;   // Privacy-preserving location identifier
        address prover;            // Address that submitted the proof
    }
    
    ProofData[] public proofs;
    
    // Configurable parameters
    uint256 public constant TIME_BUCKET_SIZE = 15 minutes;  // Size of time buckets
    uint256 public constant MAX_LOCATION_BUCKET = 1000;     // Maximum location bucket value
    
    event ProofSubmitted(address indexed prover, uint256 proofIndex);
    event CoLocationFound(uint256 proof1Index, uint256 proof2Index);
    
    constructor(address _verifier) {
        verifier = IVerifier(_verifier);
    }
    
    function submitProof(
        IVerifier.Proof memory _proof,
        uint256[2] memory _inputs  // [location_bucket, 0]
    ) public returns (uint256 proofIndex) {
        // Verify the proof
        require(verifier.verifyTx(_proof, _inputs), "Invalid proof");
        
        // Verify input ranges
        require(_inputs[0] < MAX_LOCATION_BUCKET, "Invalid location bucket");
        
        // Store the proof data with current block timestamp
        proofs.push(ProofData({
            timestamp: block.timestamp,
            location_bucket: _inputs[0],
            prover: msg.sender
        }));
        
        proofIndex = proofs.length - 1;
        emit ProofSubmitted(msg.sender, proofIndex);
        
        // Check for co-location with recent proofs
        checkCoLocation(proofIndex);
        
        return proofIndex;
    }
    
    function checkCoLocation(uint256 newProofIndex) internal {
        ProofData storage newProof = proofs[newProofIndex];
        
        // Compare with recent proofs
        for (uint256 i = 0; i < proofs.length - 1; i++) {
            ProofData storage oldProof = proofs[i];
            
            // Skip if time difference is too large
            if (newProof.timestamp - oldProof.timestamp > TIME_BUCKET_SIZE) {
                continue;
            }
            
            // Skip if same prover
            if (newProof.prover == oldProof.prover) {
                continue;
            }
            
            // Check if in same location bucket
            if (newProof.location_bucket == oldProof.location_bucket) {
                emit CoLocationFound(i, newProofIndex);
            }
        }
    }
    
    function getProof(uint256 index) public view returns (
        uint256 timestamp,
        uint256 location_bucket,
        address prover
    ) {
        ProofData storage proof = proofs[index];
        return (
            proof.timestamp,
            proof.location_bucket,
            proof.prover
        );
    }
    
    function getProofsCount() public view returns (uint256) {
        return proofs.length;
    }
} 
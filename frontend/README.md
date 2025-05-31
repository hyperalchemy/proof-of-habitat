# Proof of Habitat Frontend

Web interface for submitting and viewing zero-knowledge proofs for privacy-preserving location verification.

## Quick Start

1. **Start the development server**:
```bash
cd frontend/public
python3 -m http.server 3000
```

2. **Open in browser**: Navigate to http://localhost:3000

3. **Connect wallet**: Click "Connect Wallet" and connect your MetaMask wallet configured for Sepolia testnet

4. **Submit proof**: 
   - Generate a proof using ZoKrates (see `../zokrates/README.md`)
   - Paste the proof JSON into the text area
   - Click "Submit Proof"

5. **View proofs**: Click "Refresh Proofs" to see submitted proofs and any co-location matches

## Requirements

- MetaMask or compatible Web3 wallet
- Sepolia testnet configuration
- ETH for gas fees (get from Sepolia faucet)

## Contract Addresses (Sepolia)

- **HabitatProof Contract**: `0x73133830c8b55f21f6ccf4b672a54bb4a96ef0ff`
- **Verifier Contract**: `0x411e5cd2473bf83792346bb174e0684dc9ac36ff`

## Proof Format

The frontend expects proof data in the following JSON format:

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

## Features

- **Wallet Integration**: Connect MetaMask or compatible wallets
- **Proof Submission**: Submit zero-knowledge proofs to the contract
- **Proof Verification**: Automatically verifies proofs before submission
- **Co-location Display**: Shows detected co-locations grouped by time and location buckets
- **Error Handling**: Detailed error messages for debugging

## Development

The frontend is a single-page application using:
- Vanilla JavaScript
- Web3.js for blockchain interaction
- No build process required

### File Structure

```
frontend/
├── public/
│   └── index.html     # Main application file
├── package.json       # Dependencies for dev server
└── README.md         # This file
```

### Using with npm

Alternatively, you can use npm for development:

```bash
npm install
npm start
```

This will start an http-server on port 3000 with CORS enabled.

## Troubleshooting

### Common Issues

1. **"Please connect wallet first"**
   - Make sure MetaMask is installed and unlocked
   - Click "Connect Wallet" button

2. **"Contract rejected proof"**
   - Verify proof format is correct
   - Check that the proof was generated with valid inputs
   - Ensure location bucket is within valid range (0-999)

3. **"Insufficient ETH for gas fees"**
   - Get Sepolia ETH from a faucet
   - Typical transaction costs ~0.001-0.005 ETH

4. **Network errors**
   - Ensure MetaMask is configured for Sepolia testnet
   - Check internet connection
   - Try refreshing the page

### Debugging

The frontend includes extensive console logging:
- Open browser developer tools (F12)
- Check the Console tab for detailed logs
- Look for "Proof verification result" to see if proof is valid
- Check "Gas estimation" logs for transaction details 
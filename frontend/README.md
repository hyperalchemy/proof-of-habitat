# Proof of Habitat Frontend

This is the web interface for the Proof of Habitat project, allowing users to submit and view zero-knowledge proofs of presence.

## Features

### 🔑 Wallet Connection
- Supports multiple wallet connections through WalletConnect
- Compatible with mobile wallets and browser extensions
- Automatically handles network switching to Sepolia
- Displays your connected wallet address
- Handles network and account changes automatically

### 📤 Submit Proofs
- Paste your ZK proof JSON into the text area
- The proof format should include:
  ```json
  {
    "proof": {
      "a": [...],
      "b": [[...], [...]],
      "c": [...]
    },
    "inputs": [...]
  }
  ```
- Submits the proof to the smart contract at `0x8d9ae23DEccA195DFC8bE5509677d4fFdb94FFCa` on Sepolia
- Shows submission status and any errors

### 📥 View Proofs
- Lists all submitted proofs with:
  - Proof number
  - Submitter's address
  - Timestamp
  - Device IDs and their distances
- Auto-refreshes when new proofs are submitted
- Manual refresh button available

### 🔍 Proof Similarity Detection
- The smart contract verifies ZK proofs and checks for similarities
- Similar proofs are visually highlighted:
  - Proofs with matches have a green background
  - A "📍 Similar Proofs Found!" section appears under the proof details
  - Each similar proof is listed with its details in this section
- Under each matching proof, you'll see:
  - The matching proof number (e.g., "Proof #42")
  - The address of who submitted that proof
  - When that proof was submitted
- Example of what you'll see:
  ```
  Proof #42
  From: 0x1234...5678
  Time: March 21, 2024, 15:30:45
  Devices:
  • Device 123: 2.50m
  • Device 456: 1.75m
  
  📍 Similar Proofs Found!
  • Proof #43 by 0x9876...4321
    Time: March 21, 2024, 15:32:10
  • Proof #45 by 0xabcd...ef01
    Time: March 21, 2024, 15:33:22
  ```
- The similarity detection happens automatically:
  - When you submit a new proof
  - When others submit proofs
  - When you load or refresh the page

## Technical Details

- Uses ethers.js v6 for blockchain interaction
- Connects to Sepolia testnet
- Contract Address: `0x8d9ae23DEccA195DFC8bE5509677d4fFdb94FFCa`
- Listens for `SimilarityFound` events from the smart contract
- Maintains a client-side map of proof similarities for efficient display

## Getting Started

1. Have a Web3 wallet ready (mobile or browser)
2. Get some Sepolia ETH from a faucet
3. Open the application in your browser
4. Click "Connect Wallet" and choose your preferred wallet
5. The app will automatically switch to or add the Sepolia network
6. You can now submit proofs or view existing ones

## Error Handling

The interface provides clear error messages for common issues:
- Wallet connection issues
- Wrong network selected
- Failed proof submissions
- Invalid proof format
- Network connection issues

## Development

To run locally:
1. Ensure you have Node.js installed
2. Install dependencies: `pnpm install`
3. Get a WalletConnect Project ID from https://cloud.walletconnect.com
4. Add your Project ID to the `projectId` variable in `index.html`
5. Start the local server: `pnpm start`
6. Open `http://localhost:8080` in your browser

## Security Notes

- Never share your private keys
- The application only interacts with the specified contract on Sepolia
- All proof verifications happen on-chain
- Similarity checking is performed by the smart contract, not the frontend 
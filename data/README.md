# Data Directory

This directory is used to store:
- Raw BLE scan data (`raw_ble_data_*.json`)
- Generated proof inputs (`input_*.json`)
- Generated ZK proofs (`proof_*.json`)

These files are generated locally and should not be committed to the repository.

## File Formats

### Raw BLE Data
```json
[
  {
    "NearbyDevice": "device_mac_address",
    "RSSI": -70,
    "Distance": 5.2
  }
]
```

### Proof Input
```json
{
  "device1": 123456,
  "distance1": 520,
  "device2": 234567,
  "distance2": 1200,
  ...
  "rfmedium": 1
}
```

### ZK Proof
```json
{
  "proof": {
    "a": [uint256, uint256],
    "b": [[uint256, uint256], [uint256, uint256]],
    "c": [uint256, uint256]
  },
  "inputs": [uint256, ..., uint256]
}
``` 
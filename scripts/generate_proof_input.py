import asyncio
from bleak import BleakScanner
import json

devices = {}

def detection_callback(device, advertisement_data):
    devices[device.address] = {
        'rssi': advertisement_data.rssi
    }

def uuid_to_int(uuid_str):
    """
    Convert MAC address (hex string without colons) to integer.
    Uses first 8 hex chars for consistency.
    """
    hex_str = uuid_str.replace(':', '').lower()[:8]
    return int(hex_str, 16)

def rssi_to_distance(rssi):
    """
    Convert RSSI to approximate distance in meters.
    This can be adjusted or replaced with your preferred model.
    """
    tx_power = -59  # Typical BLE transmit power at 1 meter
    if rssi == 0:
        return 0  # Unknown distance, treat as zero
    ratio = rssi / tx_power
    if ratio < 1.0:
        distance = ratio ** 10
    else:
        distance = (0.89976) * (ratio ** 7.7095) + 0.111
    return round(distance, 2)

async def scan_ble(duration=10):
    print(f"Scanning BLE devices for {duration} seconds...")
    scanner = BleakScanner(detection_callback)
    await scanner.start()
    await asyncio.sleep(duration)
    await scanner.stop()

    results = []
    for address, info in devices.items():
        results.append({
            'NearbyDevice': address.replace(':', '').lower(),
            'RSSI': info['rssi'],
            'Distance': rssi_to_distance(info['rssi'])
        })
    return results

def select_diverse_devices(devices_list, num_ranges=3, devices_per_range=2):
    """
    Select devices from different distance ranges.
    Returns a list of devices with a mix of distances:
    - Close range (0-5m)
    - Medium range (5-15m)
    - Far range (15m+)
    """
    # Sort devices by distance
    sorted_devices = sorted(devices_list, key=lambda d: d['Distance'])
    
    # Define distance ranges
    ranges = [
        (0, 5),    # Close range: 0-5 meters
        (5, 15),   # Medium range: 5-15 meters
        (15, float('inf'))  # Far range: 15+ meters
    ]
    
    selected_devices = []
    for range_start, range_end in ranges:
        # Filter devices in this range
        range_devices = [d for d in sorted_devices if range_start <= d['Distance'] < range_end]
        # Take up to devices_per_range devices from this range
        selected_devices.extend(range_devices[:devices_per_range])
    
    # If we don't have enough devices in some ranges, pad with dummy devices
    while len(selected_devices) < num_ranges * devices_per_range:
        selected_devices.append({"NearbyDevice": "00000000", "Distance": 0.0})
    
    return selected_devices[:num_ranges * devices_per_range]

def generate_zokrates_input(devices_list):
    """
    Convert devices list to ZoKrates input JSON format with 6 devices:
    2 closest, 2 medium-range, and 2 further devices.
    """
    # Select 6 devices with diverse distances
    selected_devices = select_diverse_devices(devices_list, num_ranges=3, devices_per_range=2)

    input_json = {
        "device1": uuid_to_int(selected_devices[0]['NearbyDevice']),
        "distance1": int(selected_devices[0]['Distance'] * 100),
        "device2": uuid_to_int(selected_devices[1]['NearbyDevice']),
        "distance2": int(selected_devices[1]['Distance'] * 100),
        "device3": uuid_to_int(selected_devices[2]['NearbyDevice']),
        "distance3": int(selected_devices[2]['Distance'] * 100),
        "device4": uuid_to_int(selected_devices[3]['NearbyDevice']),
        "distance4": int(selected_devices[3]['Distance'] * 100),
        "device5": uuid_to_int(selected_devices[4]['NearbyDevice']),
        "distance5": int(selected_devices[4]['Distance'] * 100),
        "device6": uuid_to_int(selected_devices[5]['NearbyDevice']),
        "distance6": int(selected_devices[5]['Distance'] * 100),
        "rfmedium": 1  # Bluetooth
    }

    return input_json

async def main():
    detected_devices = await scan_ble()
    if not detected_devices:
        print("No BLE devices found.")
        return

    # Save raw human-readable data
    with open("raw_ble_data.json", "w") as f:
        json.dump(detected_devices, f, indent=4)
    print("Raw BLE data saved to 'raw_ble_data.json'.")

    # Generate and save ZoKrates input
    zokrates_input = generate_zokrates_input(detected_devices)
    with open("input.json", "w") as f:
        json.dump(zokrates_input, f, indent=4)
    print("ZoKrates input JSON saved to 'input.json'.")

if __name__ == "__main__":
    asyncio.run(main())

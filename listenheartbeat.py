import socket
from config import UDP_CONNECTION_STRING
import binascii
import time

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Extract port from UDP_CONNECTION_STRING
# Format is 'udpin:host:port'
_, host_port = UDP_CONNECTION_STRING.split('udpin:')
_, port = host_port.split(':')
port = int(port)

# Bind the socket to listen on all interfaces
host = '0.0.0.0'
udp_socket.bind((host, port))

# Set a timeout for the socket
timeout_seconds = 5
udp_socket.settimeout(timeout_seconds)

# Dictionary to map autopilot types to human-readable names
AUTOPILOT_TYPES = {
    0: "Generic",
    1: "Reserved",
    2: "SLUGS",
    3: "ArduPilotMega",
    4: "OpenPilot",
    5: "Generic Waypoints Only",
    6: "Generic Waypoints and Simple Navigation Only",
    7: "Generic Mission Full",
    8: "Invalid",
    9: "PPZ",
    10: "UDB",
    11: "FP",
    12: "PX4",
    13: "SMACCMPILOT",
    14: "AUTOQUAD",
    15: "ARMAZILA",
    16: "AEROB",
    17: "ASLUAV",
    18: "SmartAP",
    19: "AirRails"
}

# Dictionary to map vehicle types to human-readable names
VEHICLE_TYPES = {
    0: "Generic",
    1: "Fixed Wing",
    2: "Quadrotor",
    3: "Coaxial",
    4: "Helicopter",
    5: "Antenna Tracker",
    6: "GCS",
    7: "Airship",
    8: "Free Balloon",
    9: "Rocket",
    10: "Ground Rover",
    11: "Surface Boat",
    12: "Submarine",
    13: "Hexarotor",
    14: "Octorotor",
    15: "Tricopter",
    16: "Flapping Wing",
    17: "Kite",
    18: "Onboard Companion Controller",
    19: "Two-rotor VTOL",
    20: "Quad-rotor VTOL",
    21: "Tiltrotor VTOL",
    22: "VTOL Reserved 2",
    23: "VTOL Reserved 3",
    24: "VTOL Reserved 4",
    25: "VTOL Reserved 5",
    26: "Gimbal",
    27: "ADSB system",
    28: "Steerable, 2-axis Gimbal",
    29: "Onboard IO Controller",
    30: "Vectored 6 DOF UUV",
    31: "Onboard Companion Computer"
}

try:
    print(f"Listening for heartbeat messages on port {port}...")
    while True:
        # Receive data and address with a timeout
        data, addr = udp_socket.recvfrom(1024)
        
        # Check if this is a heartbeat message (message ID 0)
        if data[0] == 0xFD and data[1] == 0x09 and data[2] == 0x00 and data[3] == 0x00:
            # Extract heartbeat information
            autopilot = data[8]
            base_mode = data[9]
            custom_mode = int.from_bytes(data[10:14], byteorder='little')
            system_status = data[14]
            mavlink_version = data[15]
            
            # Convert base_mode to binary to check flags
            base_mode_bin = format(base_mode, '08b')
            
            # Print heartbeat information in human-readable format
            print("\n=== Heartbeat Message ===")
            print(f"From: {addr[0]}:{addr[1]}")
            print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Autopilot: {AUTOPILOT_TYPES.get(autopilot, 'Unknown')} ({autopilot})")
            print(f"Vehicle Type: {VEHICLE_TYPES.get(data[7], 'Unknown')} ({data[7]})")
            print(f"System Status: {system_status}")
            print(f"MAVLink Version: {mavlink_version}")
            print("Base Mode Flags:")
            print(f"  - Custom Mode: {base_mode_bin[0] == '1'}")
            print(f"  - Test Mode: {base_mode_bin[1] == '1'}")
            print(f"  - Auto Mode: {base_mode_bin[2] == '1'}")
            print(f"  - Guided Mode: {base_mode_bin[3] == '1'}")
            print(f"  - Stabilize Mode: {base_mode_bin[4] == '1'}")
            print(f"  - Hardware in Loop: {base_mode_bin[5] == '1'}")
            print(f"  - Manual Input: {base_mode_bin[6] == '1'}")
            print(f"  - Safety Armed: {base_mode_bin[7] == '1'}")
            print(f"Custom Mode: {custom_mode}")
            print("=======================\n")

except socket.timeout:
    print(f"Timeout ({timeout_seconds} seconds) reached. No data received.")

except KeyboardInterrupt:
    print("\nStopping heartbeat listener...")

except Exception as e:
    print(f"Error receiving data: {e}")

finally:
    # Close the socket
    udp_socket.close() 
# MAVLink connection settings
MAVLINK_IP = '192.168.193.46'  # Target IP address

# UDP settings
UDP_PORT = 14552  # Default UDP port
UDP_HOST = MAVLINK_IP  # Use MAVLINK_IP for UDP connections
UDP_CONNECTION_STRING = f'udpin:{UDP_HOST}:{UDP_PORT}'

# TCP settings
TCP_PORT = 5678  # Default TCP port
TCP_HOST = MAVLINK_IP
TCP_CONNECTION_STRING = f'tcp:{TCP_HOST}:{TCP_PORT}'

# Default connection string (can be changed based on preference)
CONNECTION_STRING = UDP_CONNECTION_STRING

# You can add more configuration settings here as needed
# For example:
# MAVLINK_SYSTEM_ID = 1
# MAVLINK_COMPONENT_ID = 1 
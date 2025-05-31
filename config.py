# MAVLink connection settings
MAVLINK_IP = '192.168.193.63'  # Updated to actual system IP address

# UDP settings
UDP_PORT = 14550  # Default UDP port
UDP_HOST = MAVLINK_IP  # Use MAVLINK_IP for UDP connections

# Different UDP connection options:
# Option 1: Listen on specific IP (original behavior)
UDP_CONNECTION_STRING_SPECIFIC = f'udpin:{UDP_HOST}:{UDP_PORT}'

# Option 2: Listen on all interfaces (more flexible)
UDP_CONNECTION_STRING_ALL = f'udpin:0.0.0.0:{UDP_PORT}'

# Option 3: Connect out to a MAVLink source (for SITL or real drone)
UDP_CONNECTION_STRING_OUT = f'udpout:127.0.0.1:{UDP_PORT}'

# Default to listening on all interfaces (most flexible for debugging)
UDP_CONNECTION_STRING = UDP_CONNECTION_STRING_ALL

# TCP settings
#TCP_PORT = 5678  # Default TCP port
TCP_PORT = 6789  # Default TCP port
TCP_HOST = MAVLINK_IP
TCP_CONNECTION_STRING = f'tcp:{TCP_HOST}:{TCP_PORT}'

# Default connection string (can be changed based on preference)
CONNECTION_STRING = UDP_CONNECTION_STRING

# You can add more configuration settings here as needed
# For example:
# MAVLINK_SYSTEM_ID = 1
# MAVLINK_COMPONENT_ID = 1 
import socket
from config import MAVLINK_HOST, MAVLINK_PORT

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a specific address and port
host = MAVLINK_HOST
port = MAVLINK_PORT
udp_socket.bind((host, port))

# Set a timeout for the socket
timeout_seconds = 5
udp_socket.settimeout(timeout_seconds)

try:
    # Receive data and address with a timeout
    data, addr = udp_socket.recvfrom(1024)

    # Print the received data and address
    print(f"Received data: {data.decode('utf-8')}")
    print(f"From address: {addr}")

except socket.timeout:
    print(f"Timeout ({timeout_seconds} seconds) reached. No data received.")

except Exception as e:
    print(f"Error receiving data: {e}")

finally:
    # Close the socket
    udp_socket.close()

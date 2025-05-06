import socket
from config import UDP_CONNECTION_STRING
import binascii

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

try:
    print(f"Listening for UDP messages on port {port}...")
    while True:
        # Receive data and address with a timeout
        data, addr = udp_socket.recvfrom(1024)

        # Print the received data as hex and the sender's address
        hex_data = binascii.hexlify(data).decode('ascii')
        print(f"Received data: {hex_data}")
        print(f"From address: {addr}")
        print("---")

except socket.timeout:
    print(f"Timeout ({timeout_seconds} seconds) reached. No data received.")

except KeyboardInterrupt:
    print("\nStopping UDP listener...")

except Exception as e:
    print(f"Error receiving data: {e}")

finally:
    # Close the socket
    udp_socket.close()

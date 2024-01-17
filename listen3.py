import socket
from pymavlink import mavutil

# Set the UDP port to listen on
udp_port = 14555

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('0.0.0.0', udp_port))

print(f"Listening for UDP packets on port {udp_port}")

while True:
    # Receive UDP packet and get sender's address
    data, addr = udp_socket.recvfrom(1024)

    # Create MAVLink message object and decode the packet
    msg = mavutil.mavlink.MAVLink(None)
    msg.decode(data)

    # Print sender's IP address
    print(f"Received UDP packet from {addr[0]}:{addr[1]} - MAVLink Message: {msg}")

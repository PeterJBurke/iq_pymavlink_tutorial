import socket



def find_IP_ADDRESS_sending_to_port(port_to_receive_on):
    # Set the UDP port to listen on
    udp_port = port_to_receive_on

    # Create a UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('0.0.0.0', udp_port))
    IP_FOUND=False
    IP_RECEIVED_ON='0.0.0.0'

    while IP_FOUND==False:
        # Receive UDP packet and get sender's address
        data, addr = udp_socket.recvfrom(1024)
        # Print sender's IP address
    #    print(f"Received UDP packet from {addr[0]}:{addr[1]} - Data: {data}")
        print(f"Received UDP packet from {addr[0]}:{addr[1]}")
        IP_FOUND=addr[0]

    udp_socket.close()
    return IP_FOUND




udp_port=14555

print(f"Listening for UDP packets on port {udp_port}")

my_found_ip=find_IP_ADDRESS_sending_to_port(udp_port)

print('found IP address of ',my_found_ip)

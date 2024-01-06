import socket
import time

def receive_udp_messages(port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind(("0.0.0.0", port))
        print(f"Listening for UDP messages on port {port}...")

        message_count = 0
        start_time = time.time()

        while True:
            data, addr = udp_socket.recvfrom(1024)
            message_count += 1

            elapsed_time = time.time() - start_time
            if elapsed_time >= 1:
                messages_per_second = message_count / elapsed_time
                print(f"Received {message_count} UDP messages in {elapsed_time:.2f} seconds "
                      f"({messages_per_second:.2f} messages/second)")
                # Reset counters for the next second
                message_count = 0
                start_time = time.time()

if __name__ == "__main__":
    UDP_PORT = 14559  # Change this to the desired UDP port
    receive_udp_messages(UDP_PORT)

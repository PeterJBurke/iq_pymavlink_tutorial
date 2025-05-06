import socket
import time
from pymavlink import mavutil
from config import CONNECTION_STRING

def receive_mavlink_messages(port):
    print(f"Listening for mavlink messages on port {port}...")
    message_count = 0
    start_time = time.time()

    while True:
        msg = the_connection.recv_match(blocking=True)
        #print(msg)
        message_count += 1

        elapsed_time = time.time() - start_time
        if elapsed_time >= 1:
            messages_per_second = message_count / elapsed_time
            print('--------------------------------------------------------------------')
            print(f"Received {message_count} Mavlink messages in {elapsed_time:.2f} seconds "
                    f"({messages_per_second:.2f} messages/second)")
            print('--------------------------------------------------------------------')
            # Reset counters for the next second
            message_count = 0
            start_time = time.time()

if __name__ == "__main__":
    # Start a connection listening to a UDP port
    the_connection = mavutil.mavlink_connection(CONNECTION_STRING)

    # Wait for the first heartbeat
    #   This sets the system and component ID of remote system for the link
    the_connection.wait_heartbeat()
    print("Heartbeat from system (system %u component %u)" %
        (the_connection.target_system, the_connection.target_component))
    current_time_seconds =  time.time()

    receive_mavlink_messages(MAVLINK_PORT)

from pymavlink import mavutil
import time
import sys
from config import UDP_CONNECTION_STRING, UDP_CONNECTION_STRING_ALL, UDP_CONNECTION_STRING_OUT

def print_debug(message):
    """Print debug message with timestamp"""
    timestamp = time.strftime("%H:%M:%S", time.localtime())
    print(f"[{timestamp}] DEBUG: {message}")

def test_connection(connection_string, timeout=10):
    """Test a MAVLink connection with timeout"""
    print_debug(f"Testing connection: {connection_string}")
    
    try:
        # Start a connection
        the_connection = mavutil.mavlink_connection(connection_string)
        print_debug("Connection object created successfully")
        
        # Wait for the first heartbeat with timeout
        print_debug(f"Waiting for heartbeat (timeout: {timeout}s)...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            # Check for heartbeat with short timeout
            msg = the_connection.recv_match(type='HEARTBEAT', blocking=False, timeout=1)
            if msg:
                print_debug("Heartbeat received!")
                print(f"Heartbeat from system (system {the_connection.target_system} component {the_connection.target_component})")
                return the_connection, True
            else:
                print_debug(f"Still waiting... ({time.time() - start_time:.1f}s elapsed)")
        
        print_debug("Timeout waiting for heartbeat")
        return the_connection, False
        
    except Exception as e:
        print_debug(f"Connection failed: {e}")
        return None, False

def listen_messages(connection, duration=30):
    """Listen to MAVLink messages for a specified duration"""
    print_debug(f"Starting message listening for {duration} seconds...")
    
    current_time_seconds = time.time()
    start_time_seconds = time.time()
    message_count = 0
    message_types = {}

    while time.time() - start_time_seconds < duration:
        msg = connection.recv_match(blocking=False, timeout=1)
        
        if msg:
            message_type = msg.get_type()
            message_id = msg.get_msgId()
            
            # Count message types
            message_types[message_type] = message_types.get(message_type, 0) + 1
            
            # Special handling for position messages
            if msg.get_type() == 'GLOBAL_POSITION_INT':
                lat = msg.lat / 1e7  # Latitude in degrees
                lon = msg.lon / 1e7  # Longitude in degrees
                print_debug(f"Position - Latitude: {lat}, Longitude: {lon}")

            message_count += 1
            
            # Calculate timing
            delta_time_seconds = time.time() - current_time_seconds
            current_time_seconds = time.time()
            rate_hz_float = 1 / delta_time_seconds if delta_time_seconds > 0 else 0
            time_since_start_seconds = current_time_seconds - start_time_seconds
            
            # Print message info
            print(f"{message_count},{time_since_start_seconds:.3f},{message_id},{message_type}")
        else:
            time.sleep(0.1)  # Small delay when no messages
    
    print_debug(f"Listening complete. Total messages: {message_count}")
    print_debug("Message type summary:")
    for msg_type, count in sorted(message_types.items()):
        print_debug(f"  {msg_type}: {count}")

def main():
    print_debug("=== MAVLink UDP Listener Debug Tool ===")
    
    # Test different connection options
    connections_to_test = [
        ("Default (Listen all interfaces)", UDP_CONNECTION_STRING),
        ("Listen all interfaces", UDP_CONNECTION_STRING_ALL),
        ("Connect out to localhost", UDP_CONNECTION_STRING_OUT),
    ]
    
    successful_connection = None
    
    for name, conn_str in connections_to_test:
        print_debug(f"\n--- Testing {name} ---")
        connection, success = test_connection(conn_str, timeout=5)
        
        if success:
            print_debug(f"SUCCESS: {name} connected!")
            successful_connection = connection
            break
        else:
            print_debug(f"FAILED: {name} did not connect")
            if connection:
                connection.close()
    
    if successful_connection:
        print_debug("\n--- Starting message monitoring ---")
        try:
            listen_messages(successful_connection, duration=30)
        except KeyboardInterrupt:
            print_debug("Interrupted by user")
        finally:
            successful_connection.close()
            print_debug("Connection closed")
    else:
        print_debug("\n=== TROUBLESHOOTING TIPS ===")
        print_debug("No MAVLink source detected. To fix this:")
        print_debug("1. Start a MAVLink simulator (SITL):")
        print_debug("   sim_vehicle.py --mavlink-bind=0.0.0.0:14550")
        print_debug("2. Or connect a real drone/flight controller")
        print_debug("3. Or use MAVProxy to bridge connections:")
        print_debug("   mavproxy.py --master=<source> --out=udp:localhost:14550")
        
        # Check if port is in use
        import socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(('0.0.0.0', 14550))
            sock.close()
            print_debug("Port 14550 is available")
        except Exception as e:
            print_debug(f"Port 14550 status: {e}")

if __name__ == "__main__":
    main() 
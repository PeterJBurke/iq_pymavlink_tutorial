from pymavlink import mavutil
import time

# Start a connection listening to a UDP port
the_connection = mavutil.mavlink_connection('192.168.1.229:14555')
# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" %
      (the_connection.target_system, the_connection.target_component))


current_time_seconds =  time.time()
start_time_seconds =  time.time()
message_count = 0

while True:
      msg = the_connection.recv_match(blocking=True)
      message_type = msg.get_type()
      message_id = msg.get_msgId()
#      print(f"Received MAVLink message - Type: {message_type}, ID: {message_id}")
#      print(f"{message_type}, {message_id}")

      message_count += 1
      #print(msg)
      #msg = the_connection.recv_match(type='ATTITUDE', blocking=True)
      delta_time_seconds=time.time() -current_time_seconds
      #delta_time_microseconds_char=str(delta_time_seconds*1e6)
      delta_time_microseconds_char=f"{delta_time_seconds*1e6:.0f}"
      current_time_seconds =  time.time()
      #rate_hz=str(1e6/delta_time_microseconds)
      rate_hz_float=1/delta_time_seconds
      rate_hz=f"{rate_hz_float:.1f}"
      #print('--------------------------------------------------------------------')
      #print('[MESSAGE COUNT]: ' +str(message_count))
      #    print("[TIME] the time now is: " +str(time.time()))
      #    print("rate (Hz) = " + rate_hz)
      #if rate_hz_float<1000:
            #print('*********************************************************')        
      #    print("delta time (microseconds)"+delta_time_microseconds_char)
      #    print(delta_time_microseconds_char)
      time_since_start_seconds=current_time_seconds -start_time_seconds
      print(message_count,',',time_since_start_seconds,',',message_id, ',',message_type)

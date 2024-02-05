from pymavlink import mavutil
import time

# Start a connection listening to a UDP port
#the_connection = mavutil.mavlink_connection('192.168.1.158:14555')
the_connection = mavutil.mavlink_connection('192.168.1.124:14559')
#the_connection = mavutil.mavlink_connection('127.0.0.1:14555')
#the_connection = mavutil.mavlink_connection('localhost:14558')
#the_connection = mavutil.mavlink_connection('172.16.86.224:14559')
#the_connection = mavutil.mavlink_connection('52.13.24.228:14558')
#the_connection = mavutil.mavlink_connection('10.50.20.6:61545')
#the_connection = mavutil.mavlink_connection('172.16.1.16:55180')

#the_connection = mavutil.mavlink_connection('172.16.1.16:14550')

#the_connection = mavutil.mavlink_connection('0.0.0.0:14558')
# 52.13.24.228.14558 from sudo tcpdump -n udp port 14558 -X  gives lots of packets in terminal
#the_connection = mavutil.mavlink_connection('10.50.20.6:14558')
#the_connection = mavutil.mavlink_connection('udpout:52.13.24.228:14558')
#the_connection = mavutil.mavlink_connection('udpout:ec2-52-13-24-228.us-west-2.compute.amazonaws.com:14558')
#the_connection = mavutil.mavlink_connection('udpout:52.13.24.228:14558')
#the_connection = mavutil.mavlink_connection('udpout:127.0.0.1:14558')

try:
      # Receive a message
      msg = the_connection.recv_msg()
      
      #if msg:
            #print(f"Received message: {msg}")
      
      # Send a message (example: HEARTBEAT)
      # master.mav.heartbeat_send(type=6, autopilot=8, base_mode=0, custom_mode=0, system_status=3)

except Exception as e:
      print(f"Error: {e}")


# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
print('initiating connection')
the_connection.wait_heartbeat()
print('did initiate connection')
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

      if msg.get_type() == 'ADSB_VEHICLE':
            print("[ADSB_VEHICLE] message received")
            lat = msg.lat / 1e7  # Latitude in degrees
            lon = msg.lon / 1e7  # Longitude in degrees
            print(f"Latitude: {lat}, Longitude: {lon}")
            print("ICAO_address=",msg.ICAO_address)
            print("ADSB_ALTITUDE_TYPE=",msg.altitude_type)
            print("Altitude(ASL)=",msg.altitude)
            print("Course over ground=",msg.heading)
            print("The horizontal velocity=",msg.hor_velocity)
            print("The vertical velocity=",msg.ver_velocity)
            print("The callsign, 8+null=",msg.callsign)
            print("ADSB_EMITTER_TYPE=",msg.emitter_type)
            print("Time since last communication in seconds=",msg.tslc)
            print("ADSB_FLAGS=",msg.flags)
            print("Squawk code=",msg.squawk)


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
      #print(message_count,',',time_since_start_seconds,',',message_id, ',',message_type)

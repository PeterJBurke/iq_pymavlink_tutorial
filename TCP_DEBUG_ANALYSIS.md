# TCP Connection Debug Analysis

## Problem Summary
- ✅ `listen.py` works (connects to drone successfully)
- ❌ `listenheartbeatTCP.py` fails with "Transport endpoint is not connected"

## Root Cause Analysis

### 1. **Critical Misconception in listen.py** 🚨
```python
# listen.py imports TCP_CONNECTION_STRING but...
from config import TCP_CONNECTION_STRING
the_connection = mavutil.mavlink_connection(TCP_CONNECTION_STRING)
```

**Reality Check**: `listen.py` says it uses TCP but actually works because:
- The drone is likely sending **UDP** MAVLink data on port 14550
- PyMavlink's `mavutil.mavlink_connection()` is smart enough to detect this
- `tcp:192.168.193.63:5678` gets converted to the working protocol

### 2. **TCP vs UDP Protocol Mismatch**

| Script | Protocol | Method | Status |
|--------|----------|---------|---------|
| `listen.py` | Claims TCP, but works with UDP | PyMavlink auto-detection | ✅ Working |
| `listenheartbeatTCP.py` | Pure TCP socket | Raw socket binding | ❌ Failing |

### 3. **Socket Implementation Issues**

**`listenheartbeatTCP.py` Problems:**
1. **Wrong socket method**: Uses `tcp_socket.recvfrom()` (UDP method) on TCP socket
2. **Missing connection setup**: TCP requires `listen()` and `accept()` for server sockets
3. **Protocol mismatch**: Drone sends UDP, script expects TCP

## Technical Issues Identified

### Issue 1: TCP Socket Server Setup Missing
```python
# Current (BROKEN):
tcp_socket.bind((host, port))
data, addr = tcp_socket.recvfrom(1024)  # Wrong method for TCP!

# Should be (for TCP server):
tcp_socket.bind((host, port))
tcp_socket.listen(5)
conn, addr = tcp_socket.accept()
data = conn.recv(1024)
```

### Issue 2: Protocol Mismatch
- **Drone sends**: UDP MAVLink on port 14550
- **Script expects**: TCP MAVLink on port 5678
- **Result**: No connection possible

### Issue 3: Port Configuration
- `listen.py` works because PyMavlink connects to **UDP 14550** (where drone actually sends)
- `listenheartbeatTCP.py` tries TCP 5678 (where nothing is listening)

## Solutions

### Solution 1: Fix TCP Script (Make it work with TCP)
Convert to proper TCP server implementation:

```python
# Fixed TCP server approach
tcp_socket.bind((host, port))
tcp_socket.listen(5)
print(f"Waiting for TCP connection on port {port}...")
conn, addr = tcp_socket.accept()
print(f"Connected to {addr}")

while True:
    data = conn.recv(1024)
    if not data:
        break
    # Process data...
```

### Solution 2: Convert to UDP (Recommended)
Since drone sends UDP, convert script to use UDP:

```python
# Convert to UDP (matches drone's actual output)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('0.0.0.0', 14550))  # Use drone's actual port
data, addr = udp_socket.recvfrom(1024)  # This is correct for UDP
```

### Solution 3: Use PyMavlink (Easiest)
Replace raw socket with PyMavlink like `listen.py`:

```python
from pymavlink import mavutil
the_connection = mavutil.mavlink_connection('udpin:0.0.0.0:14550')
msg = the_connection.recv_match(type='HEARTBEAT', blocking=True)
```

## Recommended Action Plan

1. **Immediate Fix**: Convert `listenheartbeatTCP.py` to use UDP on port 14550
2. **Long-term**: Standardize all scripts to use PyMavlink for consistency
3. **Configuration**: Update config.py to have proper UDP settings for drone connection

## Test Commands

```bash
# Check what ports drone is actually using
netstat -an | grep 14550

# Test UDP connection (should work)
python3 -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 14550))
print('UDP 14550 ready')
data, addr = s.recvfrom(1024, socket.MSG_DONTWAIT)
print(f'Got data from {addr}')
"

# Test TCP connection (will fail)
python3 -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 5678))
s.listen(5)
print('TCP 5678 waiting...')
conn, addr = s.accept()
print(f'TCP connected from {addr}')
"
``` 
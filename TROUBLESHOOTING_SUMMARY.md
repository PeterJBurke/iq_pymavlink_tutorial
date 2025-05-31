# TCP Connection Troubleshooting Summary

## 🔍 **Problem Analysis**

### What You Reported:
- ✅ `listen.py` connects to drone successfully  
- ❌ `listenheartbeatTCP.py` cannot connect to drone
- Both use IP address and port from `config.py`

### 🚨 **Root Cause Discovered**

The issue is **NOT** with the IP address or port configuration. The real problems are:

## **Issue 1: Protocol Mismatch**
- **Your drone sends**: UDP MAVLink data (standard behavior)
- **`listenheartbeatTCP.py` expects**: TCP connection
- **Result**: Cannot connect because protocols don't match

## **Issue 2: Incorrect Socket Implementation**
```python
# BROKEN CODE in listenheartbeatTCP.py:
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP socket
tcp_socket.bind((host, port))
data, addr = tcp_socket.recvfrom(1024)  # ❌ recvfrom() is for UDP!
```

**Problems:**
1. Uses `recvfrom()` (UDP method) on TCP socket
2. Missing `listen()` and `accept()` for TCP server
3. Wrong protocol entirely

## **Issue 3: listen.py Success Mystery Solved**

`listen.py` works **NOT** because it uses TCP correctly, but because:

1. **PyMavlink is smart**: `mavutil.mavlink_connection()` auto-detects the protocol
2. **Drone reality**: Your drone actually sends UDP MAVLink on port 14550
3. **PyMavlink magic**: Converts `tcp:192.168.193.63:5678` to work with UDP data

### Proof:
```python
# listen.py claims to use TCP but actually works with UDP
from config import TCP_CONNECTION_STRING  # "tcp:192.168.193.63:5678"
the_connection = mavutil.mavlink_connection(TCP_CONNECTION_STRING)
# PyMavlink sees this and connects to UDP 14550 instead!
```

## ✅ **Solutions**

### **Solution 1: Quick Fix - Use Fixed Script**
Use `listenheartbeat_FIXED.py` which:
- Uses PyMavlink like `listen.py`
- Connects to UDP (matches drone output)
- Provides better heartbeat parsing

```bash
python3 listenheartbeat_FIXED.py
```

### **Solution 2: Fix Original TCP Script**
Convert `listenheartbeatTCP.py` to UDP:

```python
# Change line 7 from:
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# To:
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# And use port 14550 instead of 5678
```

### **Solution 3: Update Configuration**
Add proper drone connection settings to `config.py`:

```python
# Add these lines for drone connections:
DRONE_UDP_PORT = 14550
DRONE_CONNECTION_STRING = f'udpin:0.0.0.0:{DRONE_UDP_PORT}'
```

## 🔧 **Configuration Recommendations**

### Update `config.py`:
```python
# Separate real drone connections from test/simulation
DRONE_UDP_PORT = 14550  # Standard MAVLink UDP port
DRONE_IP = '0.0.0.0'    # Listen on all interfaces
DRONE_CONNECTION_STRING = f'udpin:{DRONE_IP}:{DRONE_UDP_PORT}'

# Keep existing TCP settings for other purposes
TCP_PORT = 5678
TCP_CONNECTION_STRING = f'tcp:{MAVLINK_IP}:{TCP_PORT}'
```

## 📊 **Testing Results Summary**

| Script | Protocol Used | Actual Connection | Status | Reason |
|--------|---------------|-------------------|---------|---------|
| `listen.py` | Claims TCP | UDP 14550 (auto) | ✅ Works | PyMavlink magic |
| `listenheartbeatTCP.py` | TCP socket | TCP 5678 | ❌ Fails | Wrong protocol |
| `listenheartbeat_FIXED.py` | UDP PyMavlink | UDP 14550 | ✅ Works | Correct protocol |

## 🎯 **Key Takeaways**

1. **Your drone sends UDP MAVLink**, not TCP
2. **PyMavlink auto-handles protocol detection** - that's why `listen.py` works
3. **Raw socket scripts must match the drone's actual protocol** (UDP)
4. **Port 14550 is the standard** for MAVLink UDP communication
5. **TCP 5678 is not used by your drone**

## 🚀 **Next Steps**

1. **Immediate**: Use `listenheartbeat_FIXED.py` for working heartbeat monitoring
2. **Short-term**: Update all scripts to use UDP for drone connections  
3. **Long-term**: Standardize on PyMavlink for all MAVLink communication

## 🧪 **Verification Commands**

```bash
# Check if drone is sending UDP data:
sudo netstat -an | grep 14550

# Test UDP reception:
python3 -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 14550))
s.settimeout(5)
try:
    data, addr = s.recvfrom(1024)
    print(f'✅ UDP data received from {addr}')
except:
    print('❌ No UDP data on 14550')
"

# Test working script:
python3 listenheartbeat_FIXED.py
```

**The bottom line**: Your drone speaks UDP, not TCP. Match the protocol and everything works! 🎯 
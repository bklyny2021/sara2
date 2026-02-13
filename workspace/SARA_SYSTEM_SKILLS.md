# Sara System Information Skills

## 🌐 Network Detection Capabilities

### **IP Address Detection (Primary Method)**
```python
# Sara's embedded IP detection logic
result = subprocess.run(["hostname", "-I"], capture_output=True, text=True, timeout=5)
if result.returncode == 0:
    ips = result.stdout.strip().split()
    ipv4 = [ip for ip in ips if ":" not in ip and ip != "127.0.0.1"]
    if ipv4:
        return f"My IP address is: {ipv4[0]}"
```

### **Alternative IP Detection**
```python
# Backup method using ip addr show
result = subprocess.run(["ip", "addr", "show"], capture_output=True, text=True)
ips = re.findall(r'inet (\d+\.\d+\.\d+\.\d+)', result.stdout)
ipv4 = [ip for ip in ips if ip != "127.0.0.1"]
```

## 🧠 Knowledge Integration

### **Direct Response Pattern**
- Network queries get immediate system call response
- No need to defer to external model
- Automatic formatting of results
- Built-in error handling and timeouts

### **Keywords That Trigger System Calls**
- "ip address"
- "what is the ip"
- "my ip"
- "network status"
- "localhost ip"

## 🎯 Implementation Strategy

1. **Check keywords in message** before external model processing
2. **Execute system command** with safety timeout
3. **Filter and format results** appropriately
4. **Return direct response** without external model involvement
5. **Log interaction** in memory system

## 📚 Future Expansion

Similar pattern can be used for:
- System status queries (disk space, memory)
- Network connectivity tests
- Process monitoring
- File system operations
- System configuration checks

**Key Principle: Direct system knowledge integration = faster, more accurate responses**

---
*Updated: 2026-02-10 - Sara System Information Skills*
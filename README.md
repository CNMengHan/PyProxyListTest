# 🔍 PyProxyListTest

**A High-Performance Proxy Server Testing Tool with Multi-Protocol Support**

## 🚀 Features
- **Protocol Diversity**: Tests proxies through 4 core protocols:
  - HTTP/HTTPS 
  - SOCKS4/SOCKS4a
  - SOCKS5/SOCKS5h
- **Concurrent Testing**: 50-thread concurrent verification
- **Smart Latency Measurement**: 
  - Auto-selects fastest valid protocol variant
  - Tests against multiple targets:
    - httpbin.org (primary validation)
    - Baidu (中国站点)
    - Bing China
- **Clear Reporting**: Visual results with success/failure indicators and latency metrics

## ⚙️ Installation
```bash
pip install requests
git clone https://github.com/CNMengHan/PyProxyListTest.git
cd PyProxyListTest
```

## 🧮 Usage
```python
# Update proxies list first!
nano proxies.txt

# Run the tester
python main.py
```

**Result Legend**:
- ✅ `Protocol`: Working (with latency in ms)
- ❌ `Protocol`: Not supported

## 🛠 Technical Implementation
- **Core Libraries**:
  - `requests` for HTTP communication
  - `concurrent.futures` for thread pooling
- **Test Logic**:
  1. Sequential protocol variant testing (e.g., socks4 -> socks4a)
  2. Multiple endpoint verification
  3. Auto-fallback between protocol variants
  4. Best latency recording per protocol
- **Timeout**: 5 seconds per connection attempt

## 🌟 Key Advantages
- Protocol variant auto-detection
- China-specific site testing (Baidu/Bing CN)
- User-agent spoofing prevention
- Connection error resilience

## 🤝 Contribution
PRs welcome for:
- Improved protocol handling
- Additional test targets
- Performance optimizations

## 📜 License
MIT © 2025 CNMengHan

# Python Network & Security CLI Toolkit

A modular command-line toolkit for basic network security tasks, built in Python. Ideal for SOC analysts, ethical hackers, and learners in the networking field.

## Dependencies

```bash
pip install scapy colorama requests
```

## Usage Examples

```bash
# TCP Port scanner using socket module
python network_toolkit.py portscan --target 192.168.1.1 --ports 20-100

# Packet sniffer using Scapy
python network_toolkit.py sniffer --count 5

# Simple DNS forward lookup
python network_toolkit.py dns --target example.com

# Logs HTTP request and response headers
python network_toolkit.py httplog --target https://httpbin.org/get

# ARP scan for devices on local network (L2)
python network_toolkit.py discover --target 192.168.1.0/24
```

## Output to File

Use --output to save results:

```bash
python network_toolkit.py dns --target example.com --output results/dns_log.txt
```

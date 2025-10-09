# 🏰 Active Directory Engagement Checklist

## Recon / Enumeration
- [ ] Upgrade to PS when available
- [ ] Identify local user rights and sids → `whoami /all` /  `wmic useraccount get name,sid`
- [ ] Identify domain name + forest → `nltest /dclist:<domain>` / `systeminfo`
- [ ] Map domain trusts → BloodHound / `nltest /trusted_domains`
- [ ] Users & groups → `net user /domain`, `net group "Domain Admins" /domain`
- [ ] Logged in users on hosts → SharpHound, CrackMapExec
- [ ] List shares → `net view \\host /all` or `smbmap`

## Credential Access
- [ ] Check for local admin reuse across machines
- [ ] Search for plaintext creds → Group Policy Preferences, SYSVOL
- [ ] Dump hashes → Mimikatz, secretsdump.py
- [ ] Kerberoasting → `GetUserSPNs.py`
- [ ] AS-REP roasting if pre-auth disabled

## Lateral Movement
- [ ] SMB/WinRM with stolen creds
- [ ] Pass-the-Hash / Pass-the-Ticket
- [ ] RDP with domain creds
- [ ] PSExec/SMBexec if accessible

## Privilege Escalation
- [ ] Check misconfigured delegations (BloodHound queries)
- [ ] Exploit unconstrained delegation
- [ ] Privilege escalation via service accounts
- [ ] Check ACLs for writable GPOs, OUs, or user objects

## Post-Exploitation
- [ ] Domain persistence (Golden Ticket, Silver Ticket, Skeleton Key)
- [ ] Backdoor via GPO or scheduled tasks
- [ ] Data exfiltration targets → File shares, SQL servers, Exchange
- [ ] Clear tracks (event logs, Windows Defender alerts)

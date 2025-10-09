# Rsync

## Common Attack Paths

### Enumeration
- [ ] List available modules → `rsync <target>::`
- [ ] Attempt anonymous sync → `rsync <target>::module .`

### Attack Paths
- Anonymous modules → download sensitive files
- Misconfig → read/write to system directories
- Auth brute force if creds required

### Auxiliary Notes
- Great for pulling configs, DB dumps, and backups.
- Writable modules = potential privilege escalation.

---

## General Enumeration

*Common Commands:*

`$ sudo nmap -sV -p 873 127.0.0.1`

*Probing for Accessible Shares:*

`nc -nv 127.0.0.1 873`

*Enumerating an Open Share*

`$ rsync -av --list-only rsync://127.0.0.1/dev`
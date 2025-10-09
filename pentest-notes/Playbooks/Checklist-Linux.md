# 🐧 Linux Engagement Checklist

## Initial Access
- [ ] Check kernel + distro/version → `uname -a`, `cat /etc/*release`
- [ ] Enumerate users and groups → `id`, `cat /etc/passwd`, `getent passwd`
- [ ] Check logged in users → `who`, `w`
- [ ] Search sudo rights → `sudo -l`
- [ ] Look for cron jobs → `cat /etc/crontab`, `ls -la /etc/cron*`

## Enumeration
- [ ] List open ports/services → `ss -tulnp` / `netstat`
- [ ] Inspect processes → `ps aux`, `top`, `htop`
- [ ] Environment variables → `env`
- [ ] Check PATH manipulation possibilities
- [ ] Find setuid binaries → `find / -perm -4000 -type f 2>/dev/null`
- [ ] World-writable directories/files

## Privilege Escalation
- [ ] Check for password reuse → `.bash_history`, config files (running services)
- [ ] Weak file permissions on `/etc/shadow` or `/etc/passwd`
- [ ] Kernel exploits (if old version) → searchsploit / exploit-db
- [ ] Installed packages with known vulns → `dpkg -l` / `rpm -qa`
- [ ] Misconfigured services (NFS, Docker, etc.)
- [ ] Check for processes and sudo sessions for hijacking/caching
- [ ] Run `linpeas.sh` (even if you already have root)

## Post-Exploitation
- [ ] Dump SSH keys → `~/.ssh/`
- [ ] Grab system/network configs → `/etc/hosts`, `/etc/network/interfaces`
- [ ] Check for sensitive scripts/configs with creds
- [ ] Persistence ideas (SSH key injection, cronjob, backdoor user)

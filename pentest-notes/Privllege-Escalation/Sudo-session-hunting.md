# Process & Sudo Session Hunting

## Inspect Running Processes
Look for `sudo` or sensitive processes.
```bash
ps aux | grep sudo
```

### Check process details
```bash
# Command-line arguments
cat /proc/<PID>/cmdline | tr '\0' ' '

# Environment variables
cat /proc/<PID>/environ | tr '\0' '\n'

# Working directory & executable path
ls -l /proc/<PID>/cwd
ls -l /proc/<PID>/exe
```

---

## Inspect TTY Devices
Processes tied to terminals may be hijacked if perms are weak.

```bash
# List active TTYs
ls -l /dev/pts/

# Find which TTY a process is on
ps -eo pid,user,tty,cmd | grep sudo

# Test writing to a TTY (if perms allow)
echo "Owned!" > /dev/pts/1
```

---

## Credential Leaks
Look for keys, tokens, or passwords left behind.

```bash
# SSH keys
ls -la ~/.ssh/
cat ~/.ssh/id_rsa

# History files
cat ~/.bash_history
cat ~/.zsh_history

# Search configs
grep -i "password" ~/.bashrc ~/.profile ~/.bash_history 2>/dev/null
grep -i "token" ~/.* 2>/dev/null

# System-wide configs
grep -Ri "password" /etc/ 2>/dev/null

# Running processes with creds
ps aux | grep -E 'ssh|ftp|pass'
```

---

## Sudo Caching
Sudo keeps an auth cache (default 5 min). If active, you can escalate without a password.

```bash
# List allowed sudo commands
sudo -l

# Check cache status
sudo -v
```

- If cached → no password prompt.  
- If expired → password required.  
- Cache files: `/var/lib/sudo/` or `/run/sudo/ts/`.

---

## Key Notes
- Root-owned processes (`sudo` shells, etc.) cannot be ptraced unless you are root.  
- Same-user processes can usually be inspected via `/proc`.  
- Weak TTY perms sometimes allow injection or session hijack.  
- Cached sudo tokens are often overlooked → quick privilege escalation.

---

## Mini Checklist

**Check sudo permissions & cache**

```bash
sudo -l
sudo -v
```

**Look for sudo/root processes**

```bash
ps aux | grep sudo
```
- Inspect with `/proc/<PID>/cmdline` and `/proc/<PID>/environ`.

**Explore TTY devices**

```bash
ls -l /dev/pts/
ps -eo pid,user,tty,cmd | grep sudo
```
- Test write if perms allow:  
  `echo "ping" > /dev/pts/<ID>`

**Search for creds & tokens**

```bash
ls -la ~/.ssh/
cat ~/.bash_history
grep -i "password" ~/.* 2>/dev/null
grep -Ri "password" /etc/ 2>/dev/null
```

**Check running processes for secrets**

```bash
ps aux | grep -E 'ssh|ftp|pass|token'
```

---


# File System Search

## Common Combinations

Find file by name, send errors to /dev/null, parse lines with grep and output count

```bash
find /etc/ -name *.conf 2>/dev/null | grep systemd |wc -l
# Alternatively use "grep -c 'systemd'" instead of piping to "wc" 
```

Find users with login shells, trim the output, show only the first and last column

```bash
cat /etc/passwd | grep -v "false\|nologin" | tr ":" " " | awk '{print $1, $NF}'

# Append 'sed' to change output
sed 's/bin/sbin/g'
```

---

## Awk

Extract usernames from the `/etc/passwd` file

```bash
awk -F ':' '{print $1}' /etc/passwd

# Alternative with 'cut'
cut -d: -f1 /etc/passwd
```

Count the number of unique IP addresses and sort

```bash
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -nr
```

---

## Grep

```bash
# Recursive
grep -r 'ERROR' /var/log/

# Files containing
grep -rn /mnt/Finance/ -ie cred

# RegEx
grep -E "(my|false)" /etc/passwd
```

---

## Find

This command searches the file system for root suid, ouputs errors to null

```bash
find / -perm -4000 -type f 2>/dev/null
```

This command locates files `/path/to/dir` modified in the last 24 hours, demonstrating the find's capability to search based on criteria.

```bash
find /path/to/dir -type f -mtime -1
```

Find a given file with parameters and list by amount found

```bash
find / -type f -name *.conf -user root -size +25k -size -28k -newermt 2020-03-03 -exec ls -al {} \; 2>/dev/null | wc -l
```

---

## Open ports

Searching for open ports.

```bash
nmap -p 1-100 localhost | grep 'open' | awk '{print $1, $3}'
```

Here, grep, awk, and sort collaborate to list and organize open ports, providing valuable insights into system security.

```bash
netstat -tuln | grep 'LISTEN' | awk '{print $4}' | sort
```

---

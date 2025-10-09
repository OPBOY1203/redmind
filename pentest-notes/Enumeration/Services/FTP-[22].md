# File Transfer Protocol

## Common Attack Paths

### Enumeration
- [ ] Check for anonymous login → `ftp <target>`
- [ ] Banner grab → `nc <target> 21`
- [ ] Recursive directory listing → `ls -R`
- [ ] Nmap NSE → `nmap --script=ftp* -p21 <target>`

### Attack Paths
- Anonymous login → file leaks / upload webshells
- Weak passwords → brute force via hydra/medusa
- Cleartext creds over network → sniff with Wireshark/tcpdump
- Exploits in old vsftpd / ProFTPD versions

### Auxiliary Notes
- Try uploading test files if permissions allow.
- Watch for writable web roots (easy shell).
- Passive vs active FTP can matter in firewalled labs.

---

## General Enumeration

### Common Commands

```bash
sudo nmap -sV -p21 -sC -A 10.129.14.136

# Find NSE Scripts
find / -type f -name ftp\* 2>/dev/null | grep scripts

# Pilage all files
wget -m --no-passive ftp://anonymous:anonymous@10.129.14.136
```

## Command Reference

### FTP Command Line

| Command | Description |
|  --- |  --- |
| \-v | Suppresses verbose display of remote server responses. |
| \-n | Suppresses auto login |
| \-i | Turns off interactive prompting during multiple file transfers. |
| \-d | Enables debugging, displaying all ftp commands passed between the client and server. |
| --g | Disables filename globbing, which permits the use of wildcard chracters in local file and path names. |
| \-s:filename | Specifies a text file containing ftp commands; the commands will automatically run after ftp starts. No spaces are allowed in this parameter. Use this switch instead of redirection (>). |
| \-a | Use any local interface when binding data connection. |
| \-w:windowsize | Overrides the default transfer buffer size of 4096. |
| \-computer | Specifies the computer name or IP address of the remote computer to connect to. The computer, if specified, must be the last parameter on the line. |

### CLI Command List

| Command | Description |
|  --- |  --- |
| ! | Runs the specified command on the local computer |
| ? | Displays descriptions for ftp commands |
| append | Appends a local file to a file on the remote computer |
| ascii | Sets the file transfer type to ASCII, the default |
| bell | Toggles a bell to ring after each file transfer command is completed (default = OFF) |
| binary | Sets the file transfer type to binary |
| bye | Ends the FTP session and exits ftp |
| cd | Changes the working directory on the remote computer |
| close | Ends the FTP session and returns to the command interpreter |
| debug | Toggles debugging (default = OFF) |
| delete | Deletes a single file on a remote computer |
| dir | Displays a list of a remote directoryâ€™s files and subdirectories |
| disconnect | Disconnects from the remote computer, retaining the ftp prompt |
| get | Copies a single remote file to the local computer |
| glob | Toggles filename globbing (wildcard characters) (default = ON) |
| hash | Toggles hash sign (#) printing for each data block transferred (default = OFF) |
| help | Displays descriptions for ftp commands |

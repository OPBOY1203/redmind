# R-Services

## Common Attack Paths

### Enumeration
- [ ] Banner grab with nmap → `nmap -p512,513,514 --script=rpc* <target>`
- [ ] Check for trust files (.rhosts, hosts.equiv)

### Attack Paths
- Trusted host relationships → login without password
- Cleartext passwords → sniffable traffic
- Abuse `.rhosts` or `.netrc` for lateral movement

### Auxiliary Notes
- Rare in modern environments; often disabled.
- If present, very high-value for lateral access.

---

## General Enumeration

*Common Commands:*

`$ sudo nmap -sV -p 512,513,514 10.0.17.2`

*Login:*

```bash
rlogin 10.0.17.2 -l htb-student`

# Listing Authenticated Users Using Rwho:
rwho

# Listing Authenticated Users Using Rusers:

rusers -al 10.0.17.5
```

### Service Information

| Command | Service Daemon | Port | Transport Protocol | Description |
| --- |  --- |  --- |  --- |  --- |
| rcp | rshd | 514 | TCP | Copy a file or directory bidirectionally from the local system to the remote system (or vice versa) or from one remote system to another. It works like the cp command on Linux but provides no warning to the user for overwriting existing files on a system. |
| rsh | rshd | 514 | TCP | Opens a shell on a remote machine without a login procedure. Relies upon the trusted entries in the /etc/hosts.equiv and .rhosts files for validation. |
| rexec | rexecd | 512 | TCP | Enables a user to run shell commands on a remote machine. Requires authentication through the use of a username and password through an unencrypted network socket. Authentication is overridden by the trusted entries in the /etc/hosts.equiv and .rhosts files. |
| rlogin | rlogind | 513 | TCP | Enables a user to log in to a remote host over the network. It works similarly to telnet but can only connect to Unix-like hosts. Authentication is overridden by the trusted entries in the /etc/hosts.equiv and .rhosts files. |

*Access Control & Trusted Relationships*

The primary concern for `r-services`, and one of the primary reasons `SSH` was introduced to replace it, is the inherent issues regarding access control for these protocols. R-services rely on trusted information sent from the remote client to the host machine they are attempting to authenticate to. By default, these services utilize [Pluggable Authentication Modules (PAM)](https://debathena.mit.edu/trac/wiki/PAM) for user authentication onto a remote system; however, they also bypass this authentication through the use of the `/etc/hosts.equiv` and `.rhosts` files on the system. The `hosts.equiv` and `.rhosts` files contain a list of hosts (`IPs` or `Hostnames`) and users that are `trusted` by the local host when a connection attempt is made using `r-commands`. 
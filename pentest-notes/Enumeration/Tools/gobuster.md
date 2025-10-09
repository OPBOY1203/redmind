# gobuster Cheat Sheet

## Modes

- `dir` → directory brute-forcing  
- `dns` → DNS subdomain enumeration  
- `vhost` → virtual host enumeration  

---

## Common Options

- `-u <url>` → target URL  
- `-w <wordlist>` → wordlist to use  
- `-t <num>` → number of threads  
- `-o <file>` → save results to file  
- `-x <exts>` → add extensions (comma separated)  
- `-r` → follow redirects  
- `--wildcard` → handle wildcard DNS in `dns` mode  

---

## Directory Brute-Forcing

- Basic scan:  
  `gobuster dir -u http://10.10.10.10/ -w /usr/share/wordlists/dirb/common.txt`

- Add file extensions:  
  `gobuster dir -u http://10.10.10.10/ -w /usr/share/wordlists/dirb/common.txt -x php,txt,html`

- Save output:  
  `gobuster dir -u http://10.10.10.10/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -o results.txt`

---

## Virtual Host Enumeration

- Basic vhost scan:  
  `gobuster vhost -u http://example.com -w /usr/share/seclists/Discovery/DNS/namelist.txt`

- With custom Host header (if proxying):  
  `gobuster vhost -u http://example.com -w vhosts.txt --append-domain`

---

## DNS Enumeration

- Basic DNS scan:  
  `gobuster dns -d example.com -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt`

- With wildcard handling:  
  `gobuster dns -d example.com -w subdomains.txt --wildcard`

---

## Notes

- Thread count (`-t`) can drastically impact speed vs reliability.  
- Always test with small wordlists before scaling up.  
- Wildcard DNS may cause false positives in `dns` mode.  
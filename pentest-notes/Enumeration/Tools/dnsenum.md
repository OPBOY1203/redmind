# DNSEnum Cheat Sheet

## Basic Usage
`dnsenum <domain>`

---

## Common Options

- `--enum` → shortcut to enable several enumeration features  
- `-f <wordlist>` → brute-force subdomains with wordlist  
- `-r` → recursive brute-force (enumerate sub-subdomains)  
- `-p <num>` → set number of threads  
- `--dnsserver <ip>` → specify DNS server to use  
- `-o <file>` → output results to file  

---

## Practical Examples

- Basic enumeration:  
  `dnsenum --enum example.com`

- Subdomain brute force with SecLists:  
  `dnsenum example.com -f /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt`

- Recursive subdomain enumeration:  
  `dnsenum example.com -r`

- Specify DNS server:  
  `dnsenum example.com --dnsserver 8.8.8.8`

- Output to file:  
  `dnsenum example.com -o results.txt`

---

## Features Recap

- DNS Record Enumeration (A, AAAA, NS, MX, TXT)  
- Zone Transfer attempts on discovered NS  
- Subdomain brute-forcing with wordlists  
- Google scraping for additional subdomains  
- Reverse lookups (IP → domains)  
- WHOIS lookups for domain ownership  

---

## Notes
- Zone transfers (`AXFR`) often blocked but high-value when successful.  
- Recursive enumeration expands attack surface.  
- Use with SecLists for comprehensive brute-force results.  
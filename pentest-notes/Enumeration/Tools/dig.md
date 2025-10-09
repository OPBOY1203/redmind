# dig Cheat Sheet

## Basic Usage
`dig <domain>`

- Default lookup = A record (IPv4)

---

## Record Lookups

- IPv4:  
  `dig domain.com A`

- IPv6:  
  `dig domain.com AAAA`

- Mail servers:  
  `dig domain.com MX`

- Name servers:  
  `dig domain.com NS`

- Text records:  
  `dig domain.com TXT`

- Canonical name:  
  `dig domain.com CNAME`

- Start of authority:  
  `dig domain.com SOA`

- All records (if allowed):  
  `dig domain.com ANY`  

---

## Querying Specific Name Servers

- Query via Cloudflare:  
  `dig @1.1.1.1 domain.com`

- Query via Google DNS:  
  `dig @8.8.8.8 domain.com`

---

## Tracing & Resolution Path

- Full resolution path:  
  `dig +trace domain.com`

---

## Reverse Lookups

- Reverse IP lookup:  
  `dig -x 192.168.1.1`

---

## Output Control

- Short output:  
  `dig +short domain.com`

- Answer only:  
  `dig +noall +answer domain.com`

---

## Notes
- `ANY` queries are often blocked (RFC 8482).  
- Use `+short` for scripting and automation.  
- Combine with wordlists for scripted brute force (`for i in $(cat subs.txt); do dig +short $i.domain.com; done`).  
- Respect query limits; excessive use can trigger blocks.  
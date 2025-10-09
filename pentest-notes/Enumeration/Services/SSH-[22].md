# Secure Shell

## Common Attack Paths

### Enumeration
- [ ] Banner grab → `nc <target> 22`
- [ ] Check supported algorithms → `ssh-audit <target>`

### Attack Paths
- Weak passwords → brute force
- Weak keys → crackable (DSA/RSA < 2048-bit)
- Exploits in outdated SSH versions
- Kerberos GSSAPI auth → AD pivot

### Auxiliary Notes
- Check `.ssh/authorized_keys` for persistence.
- Privilege escalation via SSH keys found elsewhere.

---

## General Enumeration

*Common Commands:*

*SSH-Audit:*
 ```bash
git clone https://github.com/jtesta/ssh-audit.git && cd ssh-audit
./ssh-audit.py 10.129.14.132
 ```
*Change Authentication Method - brute force:*

```bash
ssh -v cry0l1t3@10.129.14.132
ssh -v cry0l1t3@10.129.14.132 -o PreferredAuthentications=password
```
# Spraying, Stuffing, and Default Credentials

## Password Spraying

This avoids account lockouts while still finding weak, org-wide passwords like `Spring2025!` or `Welcome123`.  

```shell-session
# Example: spray SMB logins with a known weak password
netexec smb 10.100.38.0/24 -u usernames.list -p 'ChangeMe123!'
```

- **When to use:** When you have a list of usernames but no passwords.  
- **Why it works:** Organizations often enforce complexity but users still pick predictable seasonal passwords.  

---

## Credential Stuffing

Stuffing means reusing **username:password pairs** stolen or leaked from another system.  
This is effective if users reuse credentials across multiple services (e.g., corporate email + VPN).  

```shell-session
# Example: stuff known creds against SSH
hydra -C user_pass.list ssh://10.100.38.23
```

- **When to use:** When you’ve already captured credentials from a dump, phishing, or another service.  
- **Why it works:** Credential reuse is one of the most common enterprise mistakes.  

---

## Default Credentials

Many applications and devices ship with **vendor default logins**.  
If admins forget to change them, attackers can gain easy access.  

```shell-session
# Install and query default credentials cheat sheet
pip3 install defaultcreds-cheat-sheet
creds search linksys
```

- **When to use:** During enumeration of new services, especially network devices or legacy applications.  
- **Why it works:** Default creds are widely published and rarely rotated on older systems.  

---
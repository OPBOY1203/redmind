# VM Snapshot & Disk Image Attacks

## Concept
Virtual machine snapshots (VirtualBox `.vdi`, VMware `.vmdk`, Hyper-V `.vhd`) are often stored unencrypted by default.  If captured, they allow full offline access to guest systems without triggering endpoint defenses.

---

## Attack Angles

### Offline Credential Extraction
- Mount snapshot/base + differencing disk:
```bash
qemu-img convert -O raw disk.vdi disk.raw
mkdir /mnt/vm
mount -o loop,ro disk.raw /mnt/vm
```

- Extract Windows:
  - `C:\Windows\System32\config\SAM` + `SYSTEM` hive
  - `NTDS.dit` for AD
- Extract Linux:
  - `/etc/shadow`
  - SSH keys, history, API tokens

Crack offline with `hashcat`, `john`, or tools like `secretsdump.py`.

------

### Snapshot Manipulation

- Inject backdoors into differencing images.
- On revert, the planted compromise activates silently.

------

### Credential / Payload Hiding

- Store creds or payloads inside snapshot diffs.
- Appears like normal VM metadata.
- Useful for stealth persistence or CTF/lab flags.

------

### Forensics & Backup Blind Spots

- VM snapshots often backed up without scrutiny.
- Attacker exfiltrates snapshots entire environment compromised without endpoint noise.

------

## Detection & Defense

- Monitor for access/copies of `.vdi`, `.vmdk`, `.vhd` files.
- Apply host-level disk encryption (BitLocker, LUKS, FileVault).
- Use VM encryption (vSphere, Hyper-V Shielded VMs).
- Treat snapshots/backups as sensitive as live hosts.

------

## Mini Checklist

1. **Identify snapshot/disk files**
    
    Look in VM directories for `.vdi`, `.vmdk`, `.vhd`.
2. **Mount or convert**
    Use `qemu-img` or native tools to mount read-only.
3. **Harvest secrets**
   
   Windows SAM, SYSTEM, NTDS.dit
   
   Linux `/etc/shadow`, SSH keys, tokens
4. **Consider manipulation**
    Explore differencing disk tampering for persistence.
5. **Think long-game**
    Snapshots = stealth attack surface outside normal monitoring.
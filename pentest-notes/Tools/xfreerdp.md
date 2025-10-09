# xfreerdp3

## Basic Connection
`xfreerdp3 +clipboard /size:1920x1080 /u:<user> /p:<pass> /v:<target>`

---

## Common Options
- `/d:<domain>` → specify domain  
- `/cert:ignore` → ignore cert warnings  
- `/dynamic-resolution` → auto-scale to window  
- `/size:<width>x<height>` → fixed resolution  
- `/f` → fullscreen  
- `/multimon` → multiple monitors  

---

## File & Drive Sharing
`xfreerdp3 /u:<user> /p:<pass> /v:<target> /drive:share,/path/to/dir`  

Example:  
`xfreerdp3 /u:<user> /p:<pass> /v:<target> /drive:loot,/home/user/loot`

---

## Clipboard & Resources
- Clipboard redirect: enabled by default  
- `/sound` → redirect sound  
- `/microphone` → redirect mic  
- `/printer` → redirect printers  

---

## Advanced Examples
- Custom resolution:  
  `xfreerdp3 /u:admin /p:password /v:10.10.10.5 /size:1920x1080`  

- Fullscreen & ignore certs:  
  `xfreerdp3 /u:admin /p:password /v:10.10.10.5 /f /cert:ignore`  

- Connect and mount local share:  
  `xfreerdp3 /u:pentest /p:Summer2025 /v:192.168.1.50 /drive:loot,/home/user/loot`  


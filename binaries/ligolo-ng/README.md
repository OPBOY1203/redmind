# Ligolo-ng v0.8.2 - Static musl build

Compiled binaries for ligolo-ng v0.8.2 to get around glibc run errors on older machines.

This was built on Kali using glibc 2.41 and tested on a Debian server with glibc 2.31.

- Linux `proxy` and `client`
- Included working Windows `client` binary to avoid compatibility issue

## Working build method

### Static binary = no libc on target needed.

```bash
sudo apt update && sudo apt install -y musl-tools build-essential golang
```

### Go - fully static

```bash
# in your Go module dir
CC=musl-gcc CGO_ENABLED=1 \
  go build -trimpath \
  -ldflags='-s -w -linkmode external -extldflags "-static"' \
  -o bin/app-musl-static

# verify
ldd bin/app-musl-static  # => "not a dynamic executable" (expected)
```

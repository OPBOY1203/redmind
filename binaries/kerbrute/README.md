# Kerbrute v1.0.3

Kerbrute is pure Go, so you can compile it **without** glibc by disabling cgo and using Go’s pure resolvers. That gives you a single static-ish binary that runs fine on systems with glibc 2.32 (and even older).

## Linux/amd64

```bash
# grab the source
git clone https://github.com/ropnop/kerbrute.git
cd kerbrute

# build a cgo-free binary with pure-Go resolvers
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
  go build -trimpath -tags "netgo,osusergo" -ldflags "-s -w" \
  -o kerbrute .

# sanity checks
ldd ./kerbrute            # should print: "not a dynamic executable"
strings ./kerbrute | grep -E 'GLIBC_|GLIBCXX' || echo "no glibc deps"
```

### If you need other targets

Swap `GOARCH`/`GOOS`:

```bash
# arm64 Linux
CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -tags "netgo,osusergo" -ldflags "-s -w" -o kerbrute-aarch64 .
# 386, Windows, etc. are the same idea with GOARCH/GOOS changed.
```

### ldd ouput

```bash
# binary from this build
ldd ./kerbrute
	not a dynamic executable

# binary built from releases
ldd kerbrute_linux_amd64                                                                   
	linux-vdso.so.1 (0x00007b16c4020000)
	libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007b16c3ff6000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007b16c3c00000)
	/lib64/ld-linux-x86-64.so.2 (0x00007b16c4022000)
```


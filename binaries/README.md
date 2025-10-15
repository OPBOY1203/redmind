# Binaries

Binaries in this section were built out of necessity while doing engagements on older systems. I've left them here, and will be dumping more as I go. Build instruction will be provided (my methods).

Newer-built glibc binaries aren’t reliably backward-compatible. However, they **are** more reliably forward-compatible.

## Compiling Methods for Older Systems

These are some methods you can use/try to build a compatible binaries.

## Find libc Version

```bash
# Show glibc on a host
getconf GNU_LIBC_VERSION; ldd --version | head -1

# Show what a binary needs
objdump -p ./bin/app-glibc217 | grep NEEDED

# Strip symbols (smaller binaries)
strip ./bin/app-* || true
```

## Shrink binaries

```bash
# Strip symbols (smaller binaries)
strip ./bin/app-* || true

# Package with brute
upx brute 'binary'

# Flags
-ldflags='-s -w
```

---

## Runs basically everywhere - musl

Static binary = no libc on target needed.

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

### C - fully static

```bash
# compile
musl-gcc -Os -s -static -o bin/app-musl-static src/app.c

# verify
ldd bin/app-musl-static  # => "not a dynamic executable"
```

------

## Must be glibc - Docker

Build against older glibc, mostly forwards compatible.

```bash
sudo apt update && sudo apt install -y docker.io || sudo apt install -y podman
```

### Go - glibc 2.17

```bash
docker run --rm -v "$PWD":/src -w /src quay.io/pypa/manylinux2014_x86_64 \
  bash -lc 'yum -y install golang && \
            CGO_ENABLED=1 go build -trimpath -ldflags="-s -w" -o bin/app-glibc217'
```

### C - glibc 2.17

```bash
docker run --rm -v "$PWD":/src -w /src quay.io/pypa/manylinux2014_x86_64 \
  bash -lc 'gcc -O2 -s -o bin/app-glibc217 src/app.c'
```

### Quick checks

```bash
# On your box (or target):
getconf GNU_LIBC_VERSION          # show host glibc
file bin/app-glibc217             # should mention GNU/Linux and dynamic linking
objdump -p bin/app-glibc217 | grep NEEDED   # show linked libs
```

------

## Static sanity test

```bash
# expect: not a dynamic executable
ldd bin/app-musl-static || true

# tiny smoke test
./bin/app-musl-static --help || true
```


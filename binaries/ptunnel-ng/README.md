# Ptunnel-ng build - glibc 2.31 + openssl 1.1

Tested on a Ubuntu server running glibc 2.32. 

## Built in a container that uses glibc 2.31 (Ubuntu 20.04 / Debian 11)

This produces a binary that will be compatible with targets using glibc 2.31 and older OpenSSL 1.1

```bash
mkdir -p ~/ptunnel_build/out
docker run --rm -it -v ~/ptunnel_build:/workdir -w /workdir ubuntu:20.04 /bin/bash -lc "\
  apt-get update && apt-get install -y build-essential autoconf automake libtool pkg-	     config git \
  libpcap-dev libssl-dev libselinux1-dev ca-certificates && \
  git clone https://github.com/utoni/ptunnel-ng.git && \
  cd ptunnel-ng && \
  ./autogen.sh && ./configure --prefix=/usr && make -j\$(nproc) && \
  cp src/ptunnel-ng /workdir/out/ && \
  echo BUILD_DONE"
```

- Uses `ubuntu:20.04` (glibc 2.31).
- Installs dev packages including `libssl-dev` that match OpenSSL 1.1
- Runs `autogen.sh` / `configure` / `make`.
- Copies the binary to `~/ptunnel_build/out/ptunnel-ng`


#!/usr/bin/env python3
# Simple xor stream recovery / reuse for the lazy

from Crypto.Util.strxor import strxor
from binascii import unhexlify
import argparse

def xor_stream_recovery(nonce_hex, enc1_hex, enc2_hex, known_plaintext_bytes):
    enc1 = bytes.fromhex(enc1_hex)
    enc2 = bytes.fromhex(enc2_hex)

    # Recover keystream
    keystream = strxor(known_plaintext_bytes, enc1)

    # Trim keystream to match length of second ciphertext
    keystream_trimmed = keystream[:len(enc2)]
    recovered = strxor(keystream_trimmed, enc2)

    return recovered

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recover plaintext from stream cipher with reused nonce.")
    parser.add_argument("--nonce", required=True, help="Nonce in hex format (unused, for clarity only)")
    parser.add_argument("--enc1", required=True, help="Hex of ciphertext from known plaintext")
    parser.add_argument("--enc2", required=True, help="Hex of target ciphertext to decrypt")
    parser.add_argument("--plaintext", required=True, help="Known plaintext (as UTF-8 string)")

    args = parser.parse_args()
    known_plaintext = args.plaintext.encode()

    result = xor_stream_recovery(args.nonce, args.enc1, args.enc2, known_plaintext)

    try:
        print("[+] Recovered Plaintext:")
        print(result.decode())
    except UnicodeDecodeError:
        print("[+] Recovered Raw Bytes:")
        print(result)

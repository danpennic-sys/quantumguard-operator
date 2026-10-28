#!/usr/bin/env python3
"""
Offline LICENSE.json issuer for QuantumGuard Operator Pack v1.

Usage:
  export QG_ISSUER_PRIVATE_KEY_HEX=<64-hex-char private key>
  # or
  python3 sign-license.py --key-file /path/to/issuer_private_key.hex \\
      --licensee "Acme Corp <security@acme.example>" \\
      --sku OEG-OPERATOR \\
      --site \\
      --notes "Operator Pack — single site" \\
      --out LICENSE.json

Never commit the private key. Run this only on an offline or highly restricted host.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone

try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
except ImportError:
    print("Requires: pip install cryptography", file=sys.stderr)
    sys.exit(1)


def load_private_key(hex_str: str | None, key_file: str | None) -> ed25519.Ed25519PrivateKey:
    if key_file:
        with open(key_file) as f:
            hex_str = f.read().strip()
    if not hex_str:
        hex_str = os.environ.get("QG_ISSUER_PRIVATE_KEY_HEX", "").strip()
    if not hex_str or len(hex_str) != 64:
        print("Need 64-char hex private key via --key-file, --key-hex, or QG_ISSUER_PRIVATE_KEY_HEX", file=sys.stderr)
        sys.exit(1)
    return ed25519.Ed25519PrivateKey.from_private_bytes(bytes.fromhex(hex_str))


def main() -> None:
    p = argparse.ArgumentParser(description="Sign a QuantumGuard Operator Pack LICENSE.json offline")
    p.add_argument("--key-file", help="Path to file containing 64-hex-char private key")
    p.add_argument("--key-hex", help="64-hex-char private key (prefer --key-file or env)")
    p.add_argument("--licensee", required=True, help='e.g. "Acme Corp <security@acme.example>"')
    p.add_argument("--sku", default="OEG-OPERATOR", choices=["OEG-OPERATOR", "OEG-SEAL", "OEG-AUDIT"])
    p.add_argument("--site", action="store_true", help="Site-wide license (default if --seats omitted)")
    p.add_argument("--seats", type=int, default=None, help="Seat count when not site-wide")
    p.add_argument("--expires", default=None, help="ISO-8601 UTC expiry or omit for perpetual")
    p.add_argument("--notes", default="Operator Pack — single site")
    p.add_argument("--issued", default=None, help="Override issued timestamp (ISO-8601 UTC)")
    p.add_argument("--out", default="LICENSE.json", help="Output path")
    args = p.parse_args()

    private_key = load_private_key(args.key_hex, args.key_file)
    public_key = private_key.public_key()
    pub_hex = public_key.public_bytes_raw().hex()

    site = args.site if args.seats is None else False
    if args.seats is not None and args.seats < 1:
        print("--seats must be positive", file=sys.stderr)
        sys.exit(1)

    issued = args.issued or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    body = {
        "product": "quantumguard-operator",
        "version": "1",
        "licensee": args.licensee,
        "site": site,
        "seats": args.seats,
        "issued": issued,
        "expires": args.expires,
        "sku": args.sku,
        "notes": args.notes,
        "issuer_public_key": pub_hex,
    }

    # Canonical: sorted keys, no whitespace
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"))
    signature = private_key.sign(canonical.encode("utf-8")).hex()

    full = dict(body)
    full["signature"] = signature

    with open(args.out, "w") as f:
        json.dump(full, f, indent=2)
        f.write("\n")

    print(f"Wrote {args.out}")
    print(f"  issuer_public_key = {pub_hex}")
    print(f"  signature         = {signature[:32]}…")
    print(f"  canonical length  = {len(canonical)} bytes")


if __name__ == "__main__":
    main()

# Issuer key (Operator Pack v1)

**Public key only.** The corresponding private key is held offline and is never committed.

| Item | Value |
|------|-------|
| Algorithm | Ed25519 (raw 32-byte public key) |
| Public key (hex) | `12e83238433a32d4111a89d951ee5a7fd2a09ff1acf8f87a8cb4352c887b6a86` |
| First used | 2026-10-28 (Operator Pack v1.0.0 bootstrap) |

## What this key signs

1. **LICENSE.json** files (see `docs/LICENSE-FORMAT.md`) — canonical JSON body, no whitespace, sorted keys.
2. **Release integrity** — detached signature of `SHA256SUMS` (`SHA256SUMS.sig`) and optional CONTRACT-v1 evidence of the same bytes (`SHA256SUMS.qg.json`).

## Verification

```bash
# Detached signature over SHA256SUMS
# (any Ed25519 tool that accepts raw 32-byte keys)
# public key = 12e83238433a32d4111a89d951ee5a7fd2a09ff1acf8f87a8cb4352c887b6a86

# LICENSE.json
# Reconstruct canonical body (drop "signature", sort keys, no whitespace)
# then verify Ed25519 signature against the public key above.
```

Structural helper (no crypto): `scripts/verify-license.sh`.

## Discipline

- Private key never enters git, CI, or networked storage in cleartext.
- License presence does **not** change QuantumGuard verdicts (PASS / FAIL / INDETERMINATE).
- Same key is used for all Operator Pack v1 licenses and release checksums.

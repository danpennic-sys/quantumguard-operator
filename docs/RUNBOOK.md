# QuantumGuard Operator Runbook

Offline / air-gapped verification procedures for Operator Pack licensees.

## Preconditions

- CONTRACT-v1 is frozen (public repo).
- Binary matches a signed release from this private repo (or build from public source if you choose).
- Evidence bundle JSON follows the public contract schema.

## Verify a single bundle (CLI)

```bash
./qg verify /path/to/evidence.json
# Expected stdout: PASS | FAIL | INDETERMINATE
# Exit codes: define consistently with public CLI (0 = PASS, non-zero otherwise as documented)
```

## Verify via HTTP (local only)

```bash
./qg-http   # listens on :8080 by default; no outbound network required for verify path
curl -s -X POST --data-binary @evidence.json http://127.0.0.1:8080/verify
```

CLI and HTTP **must** produce the same verdict for the same bytes (conformance vectors prove this).

## Air-gap intake workflow

1. Receive evidence file on removable media or approved channel.
2. Optional: compute independent SHA-256 of the file for chain-of-custody log.
3. Run `qg verify`.
4. Record verdict, operator id, and local timestamp in *your* log (QuantumGuard itself does not use wall-clock).
5. Store original evidence + verdict together for replay.

## Replay

Same evidence bytes → same verdict, always. Re-run `qg verify` on archived evidence to audit past decisions.

## What not to rely on

- Network key registries
- Wall-clock freshness inside the verifier
- PQC algorithms (not in v1)
- Multiple divergent verifier implementations

## Incident: unexpected FAIL

1. Confirm file was not truncated in transfer.
2. Re-run against public conformance vectors to confirm binary integrity.
3. Compare `payload_hash` and signature fields to the issuer’s published values if available.
4. Escalate with full evidence JSON (redact secrets in payload if needed).

## Support

Private issues on this repo or email danpennic@gmail.com with:
- QuantumGuard version / commit
- Platform
- Verdict + minimal reproduction vector (if shareable)

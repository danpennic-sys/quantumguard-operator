# QuantumGuard Operator Pack — Air-Gap Runbook

**Status:** Final for CONTRACT-v1 Operator Pack  
**Scope:** Offline / air-gapped verification only  
**Invariant:** Single deterministic verifier. No network, no wall-clock, no external trust inside verify.

This runbook is for licensees of the commercial Operator Pack. The public verifier source and CONTRACT-v1 remain free (MIT OR Apache-2.0). Operator Pack adds signed binaries, this procedure, conformance materials, and support — it does **not** change the math.

---

## 1. What the verifier does (and does not)

| Does | Does not |
|------|----------|
| Pure function: evidence bytes → `PASS` \| `FAIL` \| `INDETERMINATE` | Call network, DNS, or registries |
| Shared code path for CLI and HTTP | Use wall-clock or freshness |
| Classical Ed25519 over raw 32-byte `payload_hash` | Implement post-quantum signatures (reserved, not shipped) |
| Same input → same output, always | Distribute or revoke keys |

Exit codes (Operator Pack CLI, aligned with public `qg`):

| Verdict / condition | Exit code |
|---------------------|-----------|
| `PASS` | `0` |
| `FAIL` | `1` |
| Usage / parse / I/O error | `2` |
| `INDETERMINATE` | `3` |

---

## 2. Preconditions (before any air-gap use)

1. **Contract** — You accept CONTRACT-v1 as frozen (public repo).
2. **Binary** — Use a signed release from this private repo **or** a local build from public source at a known commit. Record the version/commit in your custody log.
3. **Integrity** — Verify release checksums (`SHA256SUMS`) offline against the published sums for that tag. Optionally verify `SHA256SUMS.sig` (issuer Ed25519) or `SHA256SUMS.qg.json` (CONTRACT-v1 evidence of the same bytes). Issuer public key is documented in `ISSUER.md`.
4. **License** — Place `LICENSE.json` next to the binary or set `QG_LICENSE_PATH`. Absence of a license does **not** change verifier verdicts; it only gates Operator Pack entitlement and support.
5. **Evidence schema** — Bundle must match CONTRACT-v1 JSON fields and encodings.

---

## 3. Binary intake (air-gap transfer)

Preferred path when the operator host has no outbound network:

1. On a connected build/admin machine: download the private Release asset for your platform + `SHA256SUMS` (+ optional `.sig` / `.qg.json`).
2. Compute checksums offline and compare to `SHA256SUMS`.
3. Copy tarball + checksums + `LICENSE.json` to removable media (or approved one-way transfer).
4. On the air-gapped host: extract, re-check checksums, place `LICENSE.json`.
5. Optional structural license check: `scripts/verify-license.sh` (requires `jq`; does **not** verify Ed25519).

```bash
# Example after extract
sha256sum -c SHA256SUMS
chmod +x qg qg-http   # names may include platform suffix; rename or symlink as needed
export QG_LICENSE_PATH=./LICENSE.json
./qg version           # if available; otherwise record binary path + SHA-256 of the binary itself
```

---

## 4. Verify a single evidence bundle (CLI)

```bash
./qg verify /path/to/evidence.json
# stdout: JSON with verdict PASS | FAIL | INDETERMINATE (and stable reason/code)
# exit: 0 | 1 | 3   (usage/I/O errors → 2)
```

Batch (shell only; still one verifier function per file):

```bash
for f in /media/evidence/*.json; do
  printf '%s\t' "$f"
  ./qg verify "$f" || true
done
```

---

## 5. Verify via local HTTP (loopback only)

HTTP is a second **interface**, not a second implementation. Bind only to loopback on air-gapped hosts.

```bash
./qg-http   # default :8080; configure bind to 127.0.0.1 only if your build supports flags
curl -s -X POST --data-binary @evidence.json http://127.0.0.1:8080/verify
```

CLI and HTTP **must** agree for the same bytes. If they disagree, treat the binary as untrusted and re-validate against public conformance vectors built from source.

---

## 6. Air-gap intake workflow (operational)

1. Receive evidence on removable media or approved channel.
2. Optional chain-of-custody: independent SHA-256 of the evidence file; record transfer id, courier, and operator id **in your log** (not inside QuantumGuard).
3. Run `./qg verify`.
4. Record: verdict, exit code, evidence SHA-256, binary SHA-256 (or release tag), operator id, **your** local timestamp.
5. Archive original evidence + verdict record together for replay.

Suggested custody line (your log, not part of the contract):

```text
evidence_sha256=... binary_tag=v1.0.0 binary_sha256=... verdict=PASS operator=... when=2026-10-27T21:00:00-05:00
```

---

## 7. Replay / audit

Same evidence bytes → same verdict, always.

```bash
./qg verify /archive/job-42/evidence.json
# Must match the historical recorded verdict if the archive is intact
```

Use this for dispute resolution and internal audit. Do not “upgrade” a past `FAIL` or `INDETERMINATE` by changing tools mid-stream; change only if the archived bytes themselves change (which is a custody event).

---

## 8. Binary self-check with public vectors

On any host that can hold the public conformance vectors (even air-gapped after one-time transfer):

```bash
# vectors/ from public quantumguard repo, transferred offline
./qg verify vectors/01_known_good.json    # expect PASS (exit 0)
./qg verify vectors/02_tampered_payload.json  # expect FAIL (exit 1)
# INDETERMINATE vectors: incomplete / unsupported alg / malformed (exit 3)
```

If golden vectors fail on a release binary, stop using that binary and contact support with tag, platform, and vector name.

---

## 9. Incident: unexpected FAIL or INDETERMINATE

1. Confirm the file was not truncated or re-encoded in transfer (re-check evidence SHA-256).
2. Re-run public conformance vectors to confirm binary integrity.
3. Confirm JSON encodings: lowercase hex for hash/sig/key, standard base64 for payload, `version`=`"1"`, `alg`=`"ed25519"`.
4. Compare `payload_hash` and `signature` to issuer-provided values if available out-of-band.
5. Escalate with: QuantumGuard version/tag, platform, verdict, minimal reproduction vector (redact secrets in `payload` if needed).

---

## 10. What not to rely on

- Network key registries or revocation inside the verifier
- Wall-clock freshness as part of the verdict
- PQC algorithms (v1 is classical Ed25519 only)
- Multiple divergent verifier implementations
- Treating Operator Pack license presence as a cryptographic trust root for evidence

---

## 11. Support

- Private issues on this repository (collaborators), or
- Email: **danpennic@gmail.com**

Include: product (`quantumguard-operator`), license version, binary tag/commit, platform, verdict, and a shareable minimal vector when possible.

**Discipline:** Claims lag the product. No post-quantum claims until a future contract ships real ML-DSA-65 and conformance vectors.

# LICENSE.json format (final for Operator Pack v1)

Machine-readable commercial license for QuantumGuard Operator Pack.

**Relationship to verification:** A missing or invalid `LICENSE.json` does **not** change public or Operator Pack verifier verdicts. It gates **entitlement and support** only. The evidence math remains CONTRACT-v1.

---

## Schema (format version "1")

```json
{
  "product": "quantumguard-operator",
  "version": "1",
  "licensee": "Acme Corp <security@acme.example>",
  "site": true,
  "seats": null,
  "issued": "2026-09-18T00:00:00Z",
  "expires": null,
  "sku": "OEG-OPERATOR",
  "notes": "Operator Pack — single site",
  "issuer_public_key": "<hex 32-byte Ed25519 public key>",
  "signature": "<hex 64-byte Ed25519 signature over canonical payload>"
}
```

### Field rules

| Field | Required | Notes |
|-------|----------|-------|
| `product` | yes | Must be exactly `quantumguard-operator` |
| `version` | yes | License **format** version; currently `"1"` |
| `licensee` | yes | Human-readable identity (org and/or email) |
| `site` | no | `true` = site-wide; if false/omitted, use `seats` |
| `seats` | no | Positive integer when not site-wide; else `null` |
| `issued` | yes | ISO-8601 UTC |
| `expires` | no | ISO-8601 UTC or `null` (perpetual for this product line / one-time SKU) |
| `sku` | no | e.g. `OEG-OPERATOR`, `OEG-SEAL`, `OEG-AUDIT` |
| `notes` | no | Free text |
| `issuer_public_key` | yes | Lowercase hex, 64 hex chars (32-byte raw Ed25519 public key) |
| `signature` | yes | Lowercase hex, 128 hex chars (64-byte Ed25519 signature) |

### Canonical payload for signature

1. Remove the `signature` field.
2. Serialize remaining fields as **canonical JSON**: object keys sorted lexicographically, no insignificant whitespace, UTF-8.
3. Sign those exact bytes with the issuer Ed25519 private key.
4. Attach `signature` as lowercase hex.

Illustrative body (not a real key):

```json
{"expires":null,"issued":"2026-09-18T00:00:00Z","issuer_public_key":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","licensee":"Acme Corp <security@acme.example>","notes":"Operator Pack — single site","product":"quantumguard-operator","seats":null,"site":true,"sku":"OEG-OPERATOR","version":"1"}
```

Same discipline as QuantumGuard evidence: deterministic and inspectable.

---

## Placement

- Default: `./LICENSE.json` next to the Operator Pack binary, or
- Environment: `QG_LICENSE_PATH=/absolute/path/to/LICENSE.json`

---

## Issuance (operator internal)

1. Collect: licensee string, site vs seats, SKU, term (one-time vs annual).
2. Build canonical JSON **without** `signature`.
3. Sign offline with the issuer private key (never commit the private key).
4. Write `LICENSE.json` with `issuer_public_key` + `signature`.
5. Deliver to customer; archive a copy offline (do not commit customer PII to a widely shared git history).

Structural helper (no crypto): `scripts/verify-license.sh`.

Full cryptographic verification of the license signature should use a small tool aligned with QuantumGuard’s Ed25519 path; the evidence verifier itself is not a license server.

---

## Example files

| Path | Purpose |
|------|---------|
| `licenses/EXAMPLE-LICENSE.json` | Placeholder signature — **not valid** |
| `licenses/LICENSE.template.json` | Blank template for issuance |

---

## SKU notes (Operator Evidence Gate)

| SKU | Intent |
|-----|--------|
| `OEG-OPERATOR` | Base Operator Pack (binaries + runbook + support) |
| `OEG-SEAL` | Evidence sealing workflow / kits that emit CONTRACT-v1 bundles |
| `OEG-AUDIT` | Conformance / audit kit for third-party verification procedures |

All SKUs still rest on the **same** frozen single verifier for verdicts.

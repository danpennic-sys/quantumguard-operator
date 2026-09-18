# LICENSE.json format

Machine-readable license for QuantumGuard Operator Pack.

## Schema (v1)

```json
{
  "product": "quantumguard-operator",
  "version": "1",
  "licensee": "Acme Corp <security@acme.example>",
  "site": true,
  "seats": null,
  "issued": "2026-09-18T00:00:00Z",
  "expires": null,
  "notes": "Operator Pack — single site",
  "issuer_public_key": "<hex 32-byte Ed25519 public key>",
  "signature": "<hex 64-byte Ed25519 signature over canonical payload>"
}
```

### Field rules

| Field | Required | Notes |
|-------|----------|-------|
| product | yes | Must be `quantumguard-operator` |
| version | yes | License format version, currently `"1"` |
| licensee | yes | Human-readable identity |
| site | no | `true` = site-wide; if false, use `seats` |
| seats | no | Integer when not site-wide |
| issued | yes | ISO-8601 UTC |
| expires | no | `null` = perpetual for this product line |
| notes | no | Free text |
| issuer_public_key | yes | Hex-encoded Ed25519 public key of issuer |
| signature | yes | Signature over **canonical** license body |

### Canonical payload for signature

Exclude `signature` itself. Serialize remaining fields as canonical JSON (sorted keys, no insignificant whitespace) then sign with Ed25519. Same spirit as QuantumGuard evidence: deterministic, inspectable.

Example (illustrative only — not a real key):

```json
{
  "expires": null,
  "issued": "2026-09-18T00:00:00Z",
  "issuer_public_key": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "licensee": "Acme Corp <security@acme.example>",
  "notes": "Operator Pack — single site",
  "product": "quantumguard-operator",
  "seats": null,
  "site": true,
  "version": "1"
}
```

## Placement

- Default path: `./LICENSE.json` next to the binary, or
- Environment: `QG_LICENSE_PATH=/path/to/LICENSE.json`

Absence of a valid license does not change public verifier behavior; it only gates Operator Pack entitlement and support.

## Example file

See `licenses/EXAMPLE-LICENSE.json` (signature is placeholder; not valid).

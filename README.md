# QuantumGuard Operator Pack

**Private licensed materials for QuantumGuard.**

Open-source verifier (v1, frozen): https://github.com/danpennic-sys/quantumguard  
This repository is the **paid Operator Pack** — access is granted after purchase.

---

## What you get

| Deliverable | Description |
|-------------|-------------|
| Signed release binaries | `qg` and `qg-http` for linux/amd64, linux/arm64, darwin/amd64, darwin/arm64 |
| Conformance kit | Golden vectors + CLI ≡ HTTP equivalence proofs |
| Operator runbook | Offline / air-gap verification procedures |
| License file | Machine-readable license for your org |
| Support window | Contract freeze guarantee + upgrade protocol notes |

**What stays free:** the QuantumGuard source, CONTRACT-v1, and public vectors remain MIT OR Apache-2.0.

**What we do not claim:** post-quantum security (PQC track is reserved, not shipped).

---

## How to buy / get access

1. Purchase via Stripe Checkout (link issued by Operator Pages / danpennic@gmail.com).
2. After payment you receive:
   - GitHub collaborator invite to this private repo, **or**
   - A signed release tarball + `LICENSE.json` emailed to you.
3. Place `LICENSE.json` next to the binary (see `docs/LICENSE-FORMAT.md`).

**Pricing (current)**  
- Operator Pack (single site): $490 one-time or $1,490 / year  
- Air-gap / site license: contact for quote  
- Compaction / lineage module: separate tier

Contact: **danpennic@gmail.com** · Operator @ operatorpagesllc.com

---

## Layout

```
quantumguard-operator/
├── README.md                 # this file
├── LICENSE.md                # commercial license terms
├── docs/
│   ├── LICENSE-FORMAT.md     # LICENSE.json schema
│   ├── RUNBOOK.md            # operator procedures
│   └── STOREFRONT.md         # how GitHub is used as storefront
├── licenses/
│   └── EXAMPLE-LICENSE.json  # sample license file (not valid)
├── releases/                 # signed binaries land here (or GitHub Releases)
└── scripts/
    └── verify-license.sh     # optional local license check helper
```

---

## Quick start (after access)

```bash
# 1. Clone or download the release for your platform
# 2. Place LICENSE.json in the working directory (or set QG_LICENSE_PATH)
# 3. Verify an evidence bundle with the same contract as public qg
./qg verify path/to/bundle.json

# HTTP
./qg-http &
curl -s -X POST --data-binary @bundle.json http://localhost:8080/verify
```

Verdicts are identical to the public verifier: `PASS` | `FAIL` | `INDETERMINATE`.

---

## Support & freeze guarantee

- CONTRACT-v1 is frozen. Breaking changes require a new major contract version.
- Operator Pack licensees get notice of any upgrade path (see public UPGRADE-v1-to-v2.md).
- Issues: open in this private repo or email danpennic@gmail.com.

**Discipline:** Marketing and claims lag the product. No PQC claims until ML-DSA-65 is implemented and tested.

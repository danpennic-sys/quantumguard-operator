# GitHub as Storefront

How QuantumGuard sells the Operator Pack using GitHub + a payment path.

## Architecture

```
Public storefront          Payment                 Fulfillment
─────────────────────      ──────────────────      ─────────────────────────────
quantumguard (public)  →   Stripe Checkout     →   Collaborator invite to
  README + MARKETING         (or Lemon/Paddle)      quantumguard-operator
  link to buy                                        OR signed tarball + LICENSE.json
```

### Public repo (quantumguard)

- Open core: source, CONTRACT-v1, vectors, CLI/HTTP.
- Marketing copy states only what is true (no PQC claims).
- README section "Operator Pack" points here and to purchase contact.

### Private repo (this repo)

- Licensed binaries, runbooks, EXAMPLE license schema, support.
- Access = proof of purchase (GitHub invite or emailed artifact).

### Payment

1. Stripe Checkout Session for Operator Pack SKU.
2. On `checkout.session.completed`:
   - Record customer email + GitHub username (collected at checkout or follow-up).
   - Issue LICENSE.json (org, seats, expires, product, signature).
   - Invite user as collaborator **or** email release tarball.
3. Optional: GitHub Releases on this private repo for versioned assets.

## License file (machine-readable)

See `docs/LICENSE-FORMAT.md` and `licenses/EXAMPLE-LICENSE.json`.

Recommended fields:

- `product`: "quantumguard-operator"
- `version`: "1"
- `licensee`: org or email
- `seats` or `site`: true
- `issued` / `expires` (ISO-8601)
- `signature`: Ed25519 over canonical payload (same discipline as QuantumGuard evidence)

Optional local check: `scripts/verify-license.sh` (does not replace contractual terms).

## GitHub Releases workflow (recommended)

1. Tag `v1.0.0` on this repo after building signed binaries.
2. Attach platform archives + SHA-256SUMS + a QuantumGuard evidence bundle of the release itself.
3. Only collaborators (licensees) can download private release assets.

## What not to do

- Do not put paid binaries in the public quantumguard repo.
- Do not claim PQC or freshness/revocation features that are not in CONTRACT-v1.
- Do not auto-merge strangers; access is post-payment only.

## Operational checklist

- [ ] Stripe product + price IDs for Operator Pack
- [ ] Checkout success page with "send GitHub username" form
- [ ] Manual or scripted collaborator invite
- [ ] LICENSE.json issuer (offline signing key)
- [ ] Public README link updated
- [ ] First paid customer documented

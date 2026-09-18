# QuantumGuard Operator Pack — End-to-End Workflow

Operational path from interest → payment → access → release → support.

---

## 1. Funnel (discovery → purchase)

```
Public quantumguard README / MARKETING
        │
        ▼
Contact: danpennic@gmail.com  (or Stripe Checkout link)
        │
        ▼
Collect: email, org name, GitHub username, site vs seats
        │
        ▼
Payment (Stripe one-time $490 or annual $1,490)
```

**Rules**
- Never promise PQC or network/clock features.
- Point buyers at public CONTRACT-v1 and conformance vectors first.

---

## 2. Fulfillment (payment → access)

| Step | Action | Owner |
|------|--------|-------|
| 2.1 | Confirm payment (Stripe dashboard or webhook) | You |
| 2.2 | Issue `LICENSE.json` (see LICENSE-FORMAT.md) signed with issuer Ed25519 key | You |
| 2.3a | **Preferred:** Invite buyer GitHub user as collaborator on `quantumguard-operator` | You |
| 2.3b | **Alt:** Email signed release tarball + LICENSE.json | You |
| 2.4 | Log: date, licensee, product, expires, GitHub login | You (private spreadsheet or Drive) |
| 2.5 | Send short onboarding email: clone private repo, place LICENSE.json, run `./qg verify` | You |

**Collaborator invite (manual)**
1. Repo → Settings → Collaborators → Add people
2. Permission: **Read** (enough for clone + Releases download)
3. Buyer accepts invite

**Do not** grant write unless they are a contractor you trust.

---

## 3. License issuance workflow

```
1. Generate canonical JSON body (no signature field)
2. Sign with offline issuer private key (Ed25519)
3. Attach issuer_public_key + signature
4. Deliver LICENSE.json to customer
5. Archive a copy under licenses/issued/YYYY-MM-DD-org.json (private only; do not commit customer data to git if repo may expand access)
```

Issuer key stays **offline**. Public key is published in each LICENSE.json and optionally in docs.

---

## 4. Release workflow (binaries)

### Build (from public quantumguard)

```bash
git clone https://github.com/danpennic-sys/quantumguard.git
cd quantumguard
git checkout <frozen-tag-or-main>
go test ./...
GOOS=linux   GOARCH=amd64 go build -trimpath -ldflags="-s -w" -o dist/qg-linux-amd64     ./cmd/qg
GOOS=linux   GOARCH=amd64 go build -trimpath -ldflags="-s -w" -o dist/qg-http-linux-amd64 ./cmd/qg-http
# repeat for linux/arm64, darwin/amd64, darwin/arm64
```

### Package

```bash
cd dist
sha256sum qg-* qg-http-* > SHA256SUMS
# optional: create QuantumGuard evidence bundle over SHA256SUMS for dogfooding
tar -czf quantumguard-operator-v1.0.0-linux-amd64.tar.gz qg-linux-amd64 qg-http-linux-amd64 SHA256SUMS
```

### Publish

1. Tag this private repo: `git tag v1.0.0 && git push origin v1.0.0`
2. GitHub → Releases → Draft from tag
3. Upload platform tarballs + SHA256SUMS
4. Release notes: commit SHA of public quantumguard used, CONTRACT-v1 freeze date, no PQC claims

Only collaborators can download private release assets.

### CI (optional)

See `.github/workflows/release.yml` — builds on tag push; you still attach/sign assets and create the GitHub Release manually or via `gh release create` with a token that has access to this private repo.

---

## 5. Customer verify path (happy path)

```bash
# After collaborator access
git clone git@github.com:danpennic-sys/quantumguard-operator.git
# Or download Release asset for their platform

cp /path/from/email/LICENSE.json .
export QG_LICENSE_PATH=./LICENSE.json   # optional

./qg verify evidence.json
# PASS | FAIL | INDETERMINATE
```

Same verdict as public `go run ./cmd/qg` — Operator Pack does not change the contract.

---

## 6. Support workflow

| Trigger | Response |
|---------|----------|
| "How do I verify offline?" | Point to docs/RUNBOOK.md |
| Unexpected FAIL | Ask for vector (redacted), platform, binary version/commit |
| Want PQC | State honestly: reserved track, not shipped; stay on v1 |
| Seat / site expansion | Issue new LICENSE.json; update log |
| Annual renewal | Stripe invoice → extend expires → re-issue LICENSE.json |

Private issues on this repo are fine for licensees.

---

## 7. Revocation / breach

1. Remove collaborator access.
2. Note breach in private log.
3. LICENSE.json does not auto-phone home; contractual termination is the control. Optional future: short-lived expires + re-issue.

---

## 8. Checklist — first live sale

- [ ] Stripe product + price live
- [ ] Issuer Ed25519 keypair generated offline; public key documented
- [ ] First LICENSE.json issued and verified structurally
- [ ] First collaborator invited (or tarball sent)
- [ ] Onboarding email sent
- [ ] Sale logged
- [ ] (Optional) v1.0.0 private Release published

---

## 9. What stays out of scope

- Automatic collaborator invite bots (do manually until volume justifies automation)
- Cryptographic license enforcement that blocks `qg` (public source must keep working; license gates *pack entitlement*, not the math)
- Claiming quantum resistance

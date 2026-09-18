# Releases

Signed Operator Pack binaries are published as **GitHub Releases** on this private repository (collaborators only).

Until the first tagged release:

1. Build from public quantumguard: `go build -o qg ./cmd/qg` and `go build -o qg-http ./cmd/qg-http`
2. Prefer official release artifacts once available (checksums + optional QuantumGuard evidence of the build).

Do not commit large binaries to git history; use Releases assets.

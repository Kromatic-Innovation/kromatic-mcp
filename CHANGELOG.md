# Changelog

All notable changes to this repository are listed here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions follow the
rules in the README's Versioning section: they cover this repository's
listing material, not the servers themselves.

## Unreleased

## 1.0.0 - 2026-11-12

### Added

- README with a quick start and one install block per server for Neumann
  (`https://neumann.kromatic.com/mcp`), Fermi
  (`https://fermi.kromatic.com/mcp`) and Krobot
  (`https://api.kromatic.com/mcp/krobot`).
- `gemini-extension.json`, which adds all three servers to Gemini CLI.
- Copies of each server's MCP Registry entry in `server.json/`, taken
  2026-11-12 (Neumann 0.2.48, Fermi 1.1.0, Krobot 2.2).
- Logos (256 and 512 px) and 400x400 Cline marketplace icons.
- `scripts/check.py` and a CI workflow that validates the manifests, and
  weekly checks the `server.json/` copies and the README's prices and
  free-tier figures against the live registry and servers.
- LICENSE (MIT, excluding the names and logos), SECURITY.md and
  CONTRIBUTING.md.

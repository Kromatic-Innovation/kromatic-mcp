# Contributing

This repository holds listing material for Kromatic's hosted MCP servers. The
server code is not here, so bugs in a server's behaviour are best reported
with that server's `send_feedback` / `feedback` tool or by email to
innovate@kromatic.com.

Welcome here:

- Issues about a wrong, broken or out-of-date install snippet, URL, price or
  `server.json` copy.
- Pull requests that fix such details or add a config block for another MCP
  client.

Before opening a pull request, run:

```sh
python3 scripts/check.py --live
```

It checks that the JSON files parse, that every MCP URL agrees across
`gemini-extension.json`, `server.json/` and the README, and that the
`server.json/` copies still match the MCP Registry. CI runs the offline
checks on every pull request and the registry comparison weekly. `--live`
needs network access; without it, run `python3 scripts/check.py`. Add a CHANGELOG entry and
bump the version in `gemini-extension.json` following the README's
Versioning section.

## Maintainers

The Kromatic team maintains this repository and reviews pull requests. The
team inbox is innovate@kromatic.com. If the repository is ever retired, it
will be archived with a note in the README, and each server's MCP Registry
entry stays the source of truth for its URL.

When a server drops or renames a field in its registry entry, update both
`DROPPED` in `scripts/check.py` and the note in `server.json/README.md`.

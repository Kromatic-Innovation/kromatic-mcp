# server.json copies

Each file here is a copy of the server's entry in the
[official MCP Registry](https://registry.modelcontextprotocol.io), taken on
2026-11-12. The registry, and the manifest each server serves itself, are the
sources of truth. These copies can fall behind them.

| Server | Registry name | Version | Published to the registry | Manifest served by the server |
| --- | --- | --- | --- | --- |
| Neumann | `io.github.Kromatic-Innovation/neumann` | 0.2.48 | 2026-11-12 | https://neumann.kromatic.com/server.json |
| Fermi | `io.github.Kromatic-Innovation/fermi` | 1.1.0 | 2026-10-28 | https://fermi.kromatic.com/server.json |
| Krobot | `io.github.Kromatic-Innovation/krobot` | 2.2 | 2026-11-06 | https://api.kromatic.com/server.json |

Source commits (in the servers' own repositories, which are private):
Neumann generates its manifest at runtime and has no committed file, so the
registry version above identifies it. Fermi's committed `server.json` was last
changed in commit `b38e404`. Krobot also generates its manifest at runtime.

One change from the registry record: `fermi.json` leaves out the
`repository` field, because it points at a private repository that would
not open for you.

To read the current entry yourself:

```sh
curl -s "https://registry.modelcontextprotocol.io/v0/servers/io.github.Kromatic-Innovation%2Fneumann/versions/latest"
```

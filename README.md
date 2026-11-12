# Kromatic MCP servers

Kromatic runs three remote MCP servers. Each one is hosted by Kromatic and
connects over Streamable HTTP, so there is nothing to install or run locally.
This repository holds only listing material: install snippets, logos and
copies of each server's `server.json`. The server code is not here.

| Server | What it does | MCP URL |
| --- | --- | --- |
| [Neumann](#neumann) | Monte Carlo ranges for uncertain plans: project cost, budget, timeline, capacity, NPV/IRR/payback. | `https://neumann.kromatic.com/mcp` |
| [Fermi](#fermi) | Calibrated probability ranges for forecasting questions, with the assumptions behind them. | `https://fermi.kromatic.com/mcp` |
| [Krobot](#krobot) | Test demand and willingness to pay before you build; decide whether to keep funding, change or stop. | `https://api.kromatic.com/mcp/krobot` |

The one-line descriptions are each server's own `server.json` description.

## Gemini CLI: all three at once

```sh
gemini extensions install https://github.com/Kromatic-Innovation/kromatic-mcp
```

This installs the [`gemini-extension.json`](gemini-extension.json) in this
repository, which adds all three servers.

## Neumann

<img src="logos/neumann-256.png" alt="Neumann logo" width="64" height="64">

Neumann runs Monte Carlo simulations of a model, so you get a realistic range
of outcomes and their odds instead of one guessed number: project cost and
budget estimates, schedules and delivery dates, capacity and staffing, revenue
and growth, and investment returns such as NPV, IRR and payback.

**Free tier, no sign-in:** 3 free runs per UTC day, each with at most 1,000
trials and 20 nodes. Signed in with a free Kromatic account, you get 10 free
runs per UTC day, each with at most 10,000 trials and 50 nodes. With an
account, a run costs 1 credit (small) or 5 (large), currently $0.50 per
credit, and a new account starts with 5 free credits.

```json
{
  "mcpServers": {
    "neumann": {
      "type": "streamableHttp",
      "url": "https://neumann.kromatic.com/mcp"
    }
  }
}
```

Claude Code: `claude mcp add --transport http neumann https://neumann.kromatic.com/mcp`

Docs: https://kromatic.com/mcp/neumann?utm_source=kromatic-mcp-repo&utm_medium=mcp-directory&utm_campaign=neumann

## Fermi

<img src="logos/fermi-256.png" alt="Fermi logo" width="64" height="64">

Fermi answers forecasting questions with calibrated estimates: how much or how
many, or whether an event will happen by a date. Each answer is a range plus a
probability distribution, with the reasoning and assumptions behind it.

**Free tier, no sign-in:** 3 free tier-1 estimates per UTC day. With an
account, tier 1, 2 and 3 estimates cost 1, 3 and 10 credits at $0.50 per
credit, and a new account starts with 3 credits.

```json
{
  "mcpServers": {
    "fermi": {
      "type": "streamableHttp",
      "url": "https://fermi.kromatic.com/mcp"
    }
  }
}
```

Claude Code: `claude mcp add --transport http fermi https://fermi.kromatic.com/mcp`

Docs: https://kromatic.com/mcp/fermi?utm_source=kromatic-mcp-repo&utm_medium=mcp-directory&utm_campaign=fermi

## Krobot

<img src="logos/krobot-256.png" alt="Krobot logo" width="64" height="64">

Krobot helps people get evidence before they commit money: test an idea
before building it, and decide as a team whether to keep funding a project,
change direction or stop. It gives you Kromatic's step-by-step methods, real
company examples and templates as text and links. It does not run experiments
for you.

**Free:** browsing, searching and reading need no sign-in. Downloading a
template and sending feedback need a free Kromatic account. No Krobot tool
charges money.

```json
{
  "mcpServers": {
    "krobot": {
      "type": "streamableHttp",
      "url": "https://api.kromatic.com/mcp/krobot"
    }
  }
}
```

Claude Code: `claude mcp add --transport http krobot https://api.kromatic.com/mcp/krobot`

Docs: https://kromatic.com/mcp/krobot?utm_source=kromatic-mcp-repo&utm_medium=mcp-directory&utm_campaign=krobot

## Notes for MCP clients

- The JSON blocks above use the Cline `cline_mcp_settings.json` shape. Other
  clients use the same URL with their own config keys (for example `httpUrl`
  in Gemini CLI, or `"type": "http"` in some clients).
- Prices and limits change. Each server reports the current ones itself:
  call its `check_account_and_credits` tool (Neumann and Fermi), or read its
  instructions when your client connects.
- Each server's registry entry is in the
  [official MCP Registry](https://registry.modelcontextprotocol.io) under
  `io.github.Kromatic-Innovation/<server>`. Copies are in
  [`server.json/`](server.json/).

## Repository contents

| Path | What it is |
| --- | --- |
| `gemini-extension.json` | Gemini CLI extension manifest that adds all three servers. |
| `server.json/<server>.json` | Copies of each server's MCP Registry entry; see [`server.json/README.md`](server.json/README.md) for where they came from. |
| `logos/<server>-256.png`, `logos/<server>-512.png` | Logos for directory listings. |
| `cline/<server>-400.png` | 400x400 icons for the Cline MCP marketplace. |

## Support

Email innovate@kromatic.com, or use each server's `send_feedback` (Neumann,
Fermi) or `feedback` (Krobot) tool.

## License

The text and configuration files are MIT licensed; see [LICENSE](LICENSE).
The Kromatic, Neumann, Fermi and Krobot names and logos are trademarks of
Kromatic and are not covered by that license.

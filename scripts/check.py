#!/usr/bin/env python3
"""Consistency checks for the kromatic-mcp listing repository.

Offline (default):
  - every JSON file parses;
  - gemini-extension.json has a name, a semver version and one httpUrl per
    server;
  - each server.json/<server>.json has a matching name and a streamable-http
    remote whose URL equals the gemini-extension.json URL;
  - the README mentions every MCP URL;
  - the CHANGELOG has an entry for the manifest's version;
  - every icon is a PNG of the documented size.

With --live, also compares each server.json/<server>.json with the MCP
Registry's latest entry (ignoring fields the README says were dropped), and
checks that every price and free-tier figure quoted in the README still
appears in the instructions each server sends when a client connects.

Exit status 0 when every check passes, 1 otherwise.
"""

from __future__ import annotations

import json
import re
import struct
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERVERS = ("neumann", "fermi", "krobot")
REGISTRY = "https://registry.modelcontextprotocol.io/v0/servers/{name}/versions/latest"
# Fields deliberately left out of a copy (see server.json/README.md).
DROPPED = {"fermi": {"repository"}}

# Each README pricing claim, paired with the wording the server itself uses
# in its MCP `initialize` instructions. Both sides are compared with
# whitespace collapsed.
PRICE_FACTS = {
    "neumann": [
        ("3 free runs per UTC day, each with at most 1,000 trials and 20 nodes",
         "3 free runs per UTC day, each with at most 1,000 trials and 20 nodes"),
        ("10 free runs per UTC day, each with at most 10,000 trials and 50 nodes",
         "10 free runs per UTC day, each with at most 10,000 trials and 50 nodes"),
        ("a run costs 1 credit (small) or 5 (large), currently $0.50 per credit",
         "a run costs 1 credit (small) or 5 (large), currently $0.50 per credit"),
        ("a new account starts with 5 free credits",
         "a new account starts with 5 free credits"),
    ],
    "fermi": [
        ("3 free tier-1 estimates per UTC day", "3 free tier-1 estimates per UTC day"),
        ("tier 1, 2 and 3 estimates cost 1, 3 and 10 credits at $0.50 per credit",
         "tier 1/2/3 costs 1/3/10 credits at $0.50 per credit"),
        ("a new account starts with 3 credits", "a new account starts with 3 credits"),
    ],
    "krobot": [
        ("browsing, searching and reading need no sign-in",
         "browsing, searching and reading need no sign-in"),
        ("No Krobot tool charges money", "no tool charges money"),
    ],
}

failures: list[str] = []


def squash(text: str) -> str:
    return re.sub(r"\s+", " ", text).lower()


def server_instructions(url: str) -> str:
    """Return the `instructions` string from an MCP initialize call."""
    body = json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                   "clientInfo": {"name": "kromatic-mcp-check", "version": "1"}},
    }).encode()
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        text = resp.read().decode("utf-8")
    for line in text.splitlines():
        if line.startswith("data:"):
            text = line[5:]
    return json.loads(text)["result"].get("instructions", "")


def fail(msg: str) -> None:
    failures.append(msg)
    print(f"FAIL {msg}")


def ok(msg: str) -> None:
    print(f"ok   {msg}")


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{path.relative_to(ROOT)} does not parse: {exc}")
        return None


def png_size(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()[:24]
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", data[16:24])


def main(argv: list[str]) -> int:
    live = "--live" in argv

    ext = load(ROOT / "gemini-extension.json")
    if ext is not None:
        if not ext.get("name"):
            fail("gemini-extension.json has no name")
        version = ext.get("version", "")
        if not re.fullmatch(r"\d+\.\d+\.\d+", version):
            fail(f"gemini-extension.json version {version!r} is not X.Y.Z")
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        if not re.search(rf"^## \[?{re.escape(version)}\]?( |$)", changelog, re.M):
            fail(f"CHANGELOG.md has no entry for {version}")
        else:
            ok(f"CHANGELOG.md has an entry for {version}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    servers = (ext or {}).get("mcpServers", {})

    for server in SERVERS:
        before = len(failures)
        url = servers.get(server, {}).get("httpUrl")
        if not url:
            fail(f"gemini-extension.json has no httpUrl for {server}")
            continue
        manifest = load(ROOT / "server.json" / f"{server}.json")
        if manifest is None:
            continue
        expected_name = manifest.get("name", "")
        if not (expected_name.startswith("io.github.") and expected_name.endswith(f"/{server}")):
            fail(f"server.json/{server}.json name is {expected_name!r}")
            continue
        remotes = [r.get("url") for r in manifest.get("remotes", [])
                   if r.get("type") == "streamable-http"]
        if url not in remotes:
            fail(f"{server}: gemini-extension.json URL {url} not in server.json remotes {remotes}")
        if url not in readme:
            fail(f"{server}: README.md does not mention {url}")
        if len(failures) == before:
            ok(f"{server}: {url} agrees across manifests and README")

        if live:
            reg_url = REGISTRY.format(name=expected_name.replace("/", "%2F"))
            try:
                with urllib.request.urlopen(reg_url, timeout=30) as resp:
                    entry = json.load(resp)["server"]
            except Exception as exc:  # network errors are reported, not hidden
                fail(f"{server}: could not read the registry entry: {exc}")
                continue
            for field in DROPPED.get(server, ()):
                entry.pop(field, None)
            if entry != manifest:
                fail(f"{server}: server.json/{server}.json differs from the registry "
                     f"(registry version {entry.get('version')}, copy {manifest.get('version')})")
            else:
                ok(f"{server}: copy matches registry version {entry.get('version')}")

            try:
                instructions = squash(server_instructions(url))
            except Exception as exc:
                fail(f"{server}: could not read its MCP instructions: {exc}")
                continue
            stale = [readme_phrase for readme_phrase, source in PRICE_FACTS[server]
                     if squash(source) not in instructions]
            missing = [readme_phrase for readme_phrase, _ in PRICE_FACTS[server]
                       if squash(readme_phrase) not in squash(readme)]
            for phrase in stale:
                fail(f"{server}: the server no longer says what README claims: {phrase!r}")
            for phrase in missing:
                fail(f"{server}: README no longer contains the checked claim {phrase!r}")
            if not stale and not missing:
                ok(f"{server}: README price and free-tier figures match the live server")

    for folder, size in (("logos", None), ("cline", (400, 400))):
        for server in SERVERS:
            names = [f"{server}-400.png"] if folder == "cline" else [f"{server}-256.png", f"{server}-512.png"]
            for name in names:
                path = ROOT / folder / name
                want = size or (int(name.rsplit("-", 1)[1][:-4]),) * 2
                got = png_size(path) if path.exists() else None
                if got != want:
                    fail(f"{folder}/{name} is {got}, expected a {want[0]}x{want[1]} PNG")
    ok("icon sizes checked")

    if failures:
        print(f"\n{len(failures)} check(s) failed")
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

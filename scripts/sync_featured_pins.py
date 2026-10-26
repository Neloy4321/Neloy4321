#!/usr/bin/env python3
"""Keep the featured card grid in sync with Neloy4321's public pinned repos.

Only the bounded Featured Engineering Work README block and assets/pinned-*.svg
are written. Existing curated project SVGs are read as design templates.
"""
from __future__ import annotations

import html
import json
import os
import re
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
OWNER = "Neloy4321"
START = "<!-- FEATURED_PINS_START -->"
END = "<!-- FEATURED_PINS_END -->"
SOURCE_CARDS = {
    "Enterprise-Multi-Branch-Network-with-High-Availability": "proj-network.svg",
    "END-to-END-ML-Project": "proj-ml.svg",
    "Enterprise-Geo-Business-Discovery-Data-Collection-Pipeline": "proj-pipeline.svg",
    "BD-AgroClim": "proj-climate.svg",
    "Bengali-fakenews-hatespeech-detection": "proj-nlp.svg",
    "Explainable-Sleep-Health": "proj-sleep.svg",
}
# Short editorial labels for repos that were not part of the original six cards.
# These labels describe the repositories; the selection/order comes only from pins.
DETAILS = {
    "CCK": (
        "CCK · Full-Stack MERN App", "FULL-STACK APPLICATION ENGINEERING",
        "React · Node.js · Express · MongoDB",
        "authentication · protected routes · responsive UI", "#7ebaf0", "application",
    ),
    "DataForge-360": (
        "DataForge 360 · Data & BI", "ENTERPRISE DATA ENGINEERING",
        "ETL · PostgreSQL · dbt · Prefect · BI",
        "data quality · orchestration · analytics", "#59d5c0", "data",
    ),
    "NetworkPulse-AI": (
        "NetworkPulse AI · Network IDS", "NETWORK SECURITY & OBSERVABILITY",
        "telemetry pipelines · ML detection · MLOps",
        "network telemetry · anomaly detection · observability", "#e8b67a", "network",
    ),
}

def pinned_repositories(token: str) -> list[dict]:
    if not token:
        raise RuntimeError("GITHUB_TOKEN is required to read GitHub pinned repositories")
    query = """
    query($login: String!) {
      user(login: $login) {
        pinnedItems(first: 6, types: REPOSITORY) {
          nodes {
            ... on Repository {
              name
              nameWithOwner
              url
              description
              isPrivate
              primaryLanguage { name }
            }
          }
        }
      }
    }
    """
    payload = json.dumps({"query": query, "variables": {"login": OWNER}}).encode("utf-8")
    request = Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "Neloy4321-pinned-card-sync",
        },
        method="POST",
    )
    with urlopen(request, timeout=30) as response:
        result = json.load(response)
    if result.get("errors"):
        raise RuntimeError("GitHub GraphQL pinnedItems query failed: " + str(result["errors"]))
    user = (result.get("data") or {}).get("user") or {}
    nodes = ((user.get("pinnedItems") or {}).get("nodes") or [])
    repos = []
    seen = set()
    for repo in nodes:
        if not repo or repo.get("isPrivate") or not repo.get("nameWithOwner"):
            continue  # Never publish private repository names in a public profile.
        slug = repo["nameWithOwner"]
        if slug in seen:
            continue
        seen.add(slug)
        repos.append(repo)
    if not repos:
        raise RuntimeError("No public pinned repositories returned; keeping existing cards")
    return repos[:6]


def shorten(value: str, length: int = 62) -> str:
    clean = " ".join((value or "").split())
    return clean if len(clean) <= length else clean[: length - 1].rstrip() + "…"


def illustration(kind: str, accent: str) -> str:
    if kind == "application":
        return f'''
<g fill="none" stroke="{accent}" stroke-width="2.2">
<rect x="54" y="50" width="276" height="116" rx="10" fill="#142535"/>
<path d="M54 77H330 M73 63h8 M91 63h8 M109 63h8"/>
<rect x="74" y="92" width="92" height="52" rx="6" fill="#173347"/>
<path d="M89 109h62 M89 120h43 M89 131h51"/>
<rect x="185" y="92" width="125" height="14" rx="4"/>
<rect x="185" y="115" width="58" height="29" rx="4"/>
<rect x="252" y="115" width="58" height="29" rx="4"/>
</g>'''
    if kind == "network":
        return f'''
<g fill="none" stroke="{accent}" stroke-width="2.2">
<circle cx="99" cy="107" r="26"/><circle cx="288" cy="67" r="19"/>
<circle cx="288" cy="148" r="19"/><path d="M125 101L269 69 M125 113L269 145"/>
<path d="M180 81l25-11 25 11v25c0 20-25 34-25 34s-25-14-25-34z" fill="#213340"/>
<path d="M195 103l8 8 16-18"/>
</g>
<circle r="4" fill="{accent}"><animateMotion path="M125 101L269 69" dur="3s" repeatCount="indefinite"/></circle>'''
    if kind == "data":
        return f'''
<g fill="none" stroke="{accent}" stroke-width="2.2">
<ellipse cx="92" cy="82" rx="36" ry="11"/><path d="M56 82v54c0 15 72 15 72 0V82 M56 109c0 15 72 15 72 0"/>
<rect x="166" y="71" width="62" height="76" rx="9" fill="#18373c"/>
<path d="M128 109H166 M228 109H268 M146 100l16 9-16 9 M248 100l16 9-16 9"/>
<rect x="268" y="70" width="74" height="78" rx="8"/>
<path d="M281 132l15-19 12 10 20-32 M281 86h47"/>
</g>
<circle r="4" fill="{accent}"><animateMotion path="M128 109H166" dur="2.7s" repeatCount="indefinite"/></circle>'''
    return f'''
<g fill="none" stroke="{accent}" stroke-width="2.2">
<rect x="58" y="46" width="274" height="124" rx="11" fill="#162b3b"/>
<path d="M58 78H332 M76 63h10 M95 63h10 M114 63h10"/>
<path d="M82 110l14 11-14 11 M107 132h44 M165 112h105 M165 129h76 M165 146h92"/>
</g>'''


def card_svg(repo: dict, index: int, templates: dict[str, str]) -> str:
    name = repo["name"]
    if name in SOURCE_CARDS:
        source = templates[SOURCE_CARDS[name]]
        source, count = re.subn(
            r'(<text x="440" y="42"[^>]*>)\d{2} / ',
            lambda match: match.group(1) + f"{index:02d} / ",
            source,
            count=1,
        )
        if count != 1:
            raise ValueError("Original showcase SVG is missing its section number: " + name)
        return source

    language = ((repo.get("primaryLanguage") or {}).get("name") or "Engineering")
    fallback_kind = (
        "application" if language in ("JavaScript", "TypeScript", "HTML") else
        "data" if language in ("Python", "SQL", "Jupyter Notebook") else "code"
    )
    title, category, subtitle, footer, accent, kind = DETAILS.get(
        name,
        (
            name.replace("-", " ").replace("_", " "),
            language.upper() + " / SOFTWARE ENGINEERING",
            shorten(repo.get("description") or f"Open-source {language} repository", 65),
            "Pinned on GitHub · explore implementation and documentation",
            "#7ebaf0" if fallback_kind == "application" else "#59d5c0",
            fallback_kind,
        ),
    )
    title = shorten(title, 52)
    category = shorten(category, 48)
    subtitle = shorten(subtitle, 64)
    footer = shorten(footer, 70)
    fontsize = 36 if len(title) <= 30 else 31 if len(title) <= 38 else 25
    esc = lambda value: html.escape(str(value), quote=True)
    art = illustration(kind, accent)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="220" viewBox="0 0 1100 220" role="img" aria-label="{esc(name)} pinned repository showcase card">
<defs><linearGradient id="bg" x1="0" x2="1"><stop stop-color="#0f1a27"/><stop offset="1" stop-color="#122132"/></linearGradient></defs>
<rect x="1" y="1" width="1098" height="218" rx="18" fill="url(#bg)" stroke="#2f4458"/>
<rect x="1" y="1" width="7" height="218" rx="3.5" fill="{accent}"/>
<rect x="28" y="24" width="360" height="172" rx="14" fill="#0d1825" stroke="#274055"/>
{art}
<path d="M415 28V192" stroke="#2a4257"/>
<text x="440" y="42" font-family="monospace" font-size="13" letter-spacing="2" fill="{accent}">{index:02d} / {esc(category)}</text>
<text x="440" y="95" font-family="Georgia,serif" font-size="{fontsize}" font-weight="700" fill="#eef4fa">{esc(title)}</text>
<text x="440" y="128" font-family="Arial,sans-serif" font-size="18" fill="#d4e1eb">{esc(subtitle)}</text>
<path d="M440 146H1042" stroke="#284254"/>
<text x="440" y="173" font-family="monospace" font-size="14" fill="#9ab0bf">{esc(footer)}</text>
<g transform="translate(880 30)">
<rect x="0" y="0" width="160" height="34" rx="17" fill="#101b28" stroke="{accent}" stroke-opacity=".65"/>
<text x="80" y="22" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" font-weight="700" fill="#eef4fa">VIEW REPOSITORY ↗</text>
</g>
</svg>'''


def pinned_block(repos: list[dict]) -> str:
    rows = [START]
    for index, repo in enumerate(repos, 1):
        url = "https://github.com/" + repo["nameWithOwner"]
        rows.append(
            f'<div align="center"><a href="{html.escape(url, quote=True)}">'
            f'<img src="assets/pinned-{index:02d}.svg" width="100%" '
            f'alt="{html.escape(repo["name"], quote=True)} pinned repository card" />'
            '</a></div>'
        )
    rows.append(END)
    return "\n".join(rows)


def apply_repos(repos: list[dict], readme: str, templates: dict[str, str]) -> tuple[str, dict[str, str]]:
    region = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if len(region.findall(readme)) != 1:
        raise ValueError("README pinned section markers must exist exactly once")
    new_readme = region.sub(lambda _: pinned_block(repos), readme)
    generated = {
        f"assets/pinned-{index:02d}.svg": card_svg(repo, index, templates)
        for index, repo in enumerate(repos, 1)
    }
    return new_readme, generated


def main() -> None:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
    repos = pinned_repositories(token)
    templates = {
        file: (ROOT / "assets" / file).read_text(encoding="utf-8")
        for file in SOURCE_CARDS.values()
    }
    readme, svg_files = apply_repos(repos, README.read_text(encoding="utf-8"), templates)
    README.write_text(readme, encoding="utf-8")
    for path, svg in svg_files.items():
        (ROOT / path).write_text(svg, encoding="utf-8")
    print("Synced GitHub public pins: " + ", ".join(r["nameWithOwner"] for r in repos))


if __name__ == "__main__":
    main()

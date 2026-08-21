#!/usr/bin/env python3
"""
Generates an animated horizontal bar chart of your top languages,
tallied live from your public repos via the GitHub REST API.
Bars grow in on load. Self-built — not skill-icons.dev / shields.io.
"""
import argparse
import os
import sys
from collections import Counter
import requests

FONT = "'JetBrains Mono','Fira Code',ui-monospace,SFMono-Regular,Consolas,monospace"
BG = "#0d1117"
GREEN = "#39d353"
DIM = "#6e7681"
WHITE = "#c9d1d9"

LANG_COLORS = {
    "Python": "#3572A5", "JavaScript": "#f1e05a", "TypeScript": "#3178c6",
    "C++": "#f34b7d", "C": "#555555", "HTML": "#e34c26", "CSS": "#563d7c",
    "Java": "#b07219", "Go": "#00ADD8", "Rust": "#dea584",
    "Dockerfile": "#384d54", "Shell": "#89e051", "Batchfile": "#C1F12E",
}
DEFAULT_COLOR = GREEN


def fetch_languages(username: str):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-readme-generator"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        repos = []
        page = 1
        while True:
            r = requests.get(
                f"https://api.github.com/users/{username}/repos?per_page=100&page={page}",
                headers=headers, timeout=10,
            )
            r.raise_for_status()
            batch = r.json()
            repos.extend(batch)
            if len(batch) < 100:
                break
            page += 1
        counts = Counter(repo["language"] for repo in repos if repo.get("language"))
        return counts.most_common(6)
    except Exception as e:
        print(f"[warn] live fetch failed, using placeholders: {e}", file=sys.stderr)
        return [("Python", 5), ("TypeScript", 3), ("JavaScript", 2)]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg(username: str, langs: list) -> str:
    width = 520
    row_h = 34
    top_pad = 50
    height = top_pad + row_h * len(langs) + 20
    max_count = max(c for _, c in langs) if langs else 1
    bar_max_w = 300

    style = f"""
    <style>
      .bg {{ fill: {BG}; }}
      text {{ font-family: {FONT}; }}
      .title {{ fill: {WHITE}; font-size: 13px; }}
      .lang {{ fill: {WHITE}; font-size: 13px; }}
      .count {{ fill: {DIM}; font-size: 12px; }}
      .frame {{
        fill: none; stroke: {GREEN}; stroke-opacity: 0.3; stroke-width: 1.5;
        animation: pulse 3.2s ease-in-out infinite;
      }}
      @keyframes pulse {{
        0%, 100% {{ stroke-opacity: 0.12; }}
        50% {{ stroke-opacity: 0.4; }}
      }}
    </style>
    """

    body = []
    for i, (lang, count) in enumerate(langs):
        y = top_pad + i * row_h
        w = max(6, (count / max_count) * bar_max_w)
        color = LANG_COLORS.get(lang, DEFAULT_COLOR)
        delay = 0.15 * i
        anim_name = f"grow{i}"
        body.append(f"""
        <style>
          @keyframes {anim_name} {{ from {{ width: 0; }} to {{ width: {w:.1f}px; }} }}
        </style>
        <text class="lang" x="16" y="{y+15}">{esc(lang)}</text>
        <rect x="130" y="{y+3}" width="{w:.1f}" height="14" rx="3" fill="{color}"
              style="animation: {anim_name} 0.8s cubic-bezier(.2,.8,.2,1) {delay:.2f}s both;"/>
        <text class="count" x="{130+bar_max_w+12}" y="{y+15}">{count}</text>
        """)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
{style}
  <rect class="bg" x="0" y="0" width="{width}" height="{height}" rx="10"/>
  <text class="title" x="16" y="28">$ git log --stat --author={esc(username)} | top languages</text>
  {"".join(body)}
  <rect class="frame" x="1" y="1" width="{width-2}" height="{height-2}" rx="10"/>
</svg>'''
    return svg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--username", default="sarthakyerane")
    ap.add_argument("--out", default="assets/lang_bars.svg")
    ap.add_argument("--offline", action="store_true")
    args = ap.parse_args()

    langs = [("Python", 5), ("TypeScript", 3), ("JavaScript", 2)] if args.offline else fetch_languages(args.username)
    svg = build_svg(args.username, langs)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        f.write(svg)
    print(f"wrote {args.out} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()

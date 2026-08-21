#!/usr/bin/env python3
"""
Generates an animated 'agent terminal session' SVG for the GitHub profile README.
Lines type themselves out character-by-character via CSS animation, with a
blinking cursor and a subtle green terminal glow. Pulls live stats from the
GitHub API (public repo count, follower count, most recently pushed repo).
"""
import argparse
import os
import sys
import requests

FONT = "'JetBrains Mono','Fira Code',ui-monospace,SFMono-Regular,Consolas,monospace"
BG = "#0d1117"
GREEN = "#39d353"
DIM = "#6e7681"
WHITE = "#c9d1d9"


def fetch_live_stats(username: str):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-readme-generator"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        r = requests.get(f"https://api.github.com/users/{username}", headers=headers, timeout=10)
        r.raise_for_status()
        user = r.json()
        r2 = requests.get(
            f"https://api.github.com/users/{username}/repos?sort=pushed&per_page=1",
            headers=headers, timeout=10,
        )
        r2.raise_for_status()
        repos = r2.json()
        latest_repo = repos[0]["name"] if repos else "unknown"
        return {
            "public_repos": user.get("public_repos", "?"),
            "followers": user.get("followers", "?"),
            "latest_repo": latest_repo,
        }
    except Exception as e:
        print(f"[warn] live fetch failed, using placeholders: {e}", file=sys.stderr)
        return {"public_repos": "?", "followers": "?", "latest_repo": "unknown"}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg(username: str, stats: dict) -> str:
    lines = [
        ("$ whoami", GREEN, True),
        (f"> {username} — GenAI engineer, RAG / agentic pipelines / MCP servers", WHITE, False),
        ("", WHITE, False),
        ("$ curl api.github.com/users/" + username, GREEN, True),
        (f"> public_repos: {stats['public_repos']}   followers: {stats['followers']}", WHITE, False),
        (f"> most recently pushed: {stats['latest_repo']}", WHITE, False),
        ("", WHITE, False),
        ("$ status --current", GREEN, True),
        ("> open to GenAI / SDE roles", WHITE, False),
        ("> 430+ DSA problems solved", WHITE, False),
    ]

    width, line_h, top_pad = 760, 26, 64
    height = top_pad + line_h * len(lines) + 30

    char_w = 9.15
    CPS = 28  # characters typed per second

    base_style = f"""
    <style>
      .term-bg {{ fill: {BG}; }}
      .titlebar {{ fill: #161b22; }}
      text {{ font-family: {FONT}; font-size: 15px; }}
      .prompt {{ fill: {GREEN}; font-weight: 600; }}
      .out {{ fill: {WHITE}; }}
      .glow {{ filter: drop-shadow(0 0 3px rgba(57,211,83,0.6)); }}

      .frame {{
        fill: none; stroke: {GREEN}; stroke-opacity: 0.35; stroke-width: 1.5;
        animation: pulse 3.2s ease-in-out infinite;
      }}
      @keyframes pulse {{
        0%, 100% {{ stroke-opacity: 0.15; }}
        50% {{ stroke-opacity: 0.5; }}
      }}

      .scan {{ animation: drift 6s linear infinite; }}
      @keyframes drift {{
        from {{ transform: translateY(0); }}
        to   {{ transform: translateY(4px); }}
      }}

      .cursor {{ fill: {GREEN}; opacity: 0; }}
      @keyframes blink {{
        0%, 49% {{ opacity: 1; }}
        50%, 100% {{ opacity: 0; }}
      }}
    </style>
    """

    scanlines = "".join(
        f'<rect x="0" y="{y}" width="{width}" height="1" fill="{GREEN}" opacity="0.025"/>'
        for y in range(0, height, 4)
    )

    per_line_style = []
    body = []
    t = 0.3
    gap = 0.18

    for i, (text, color, is_prompt) in enumerate(lines):
        y = top_pad + i * line_h
        cls = "prompt glow" if is_prompt else "out"
        safe = esc(text)
        n_chars = max(len(text), 1)
        full_w = len(text) * char_w + 16
        dur = max(0.12, len(text) / CPS)

        clip_id = f"clip{i}"
        anim_name = f"type{i}"

        per_line_style.append(
            f"@keyframes {anim_name} {{ from {{ width: 0; }} to {{ width: {full_w:.1f}px; }} }}\n"
            f".{anim_name} {{ animation: {anim_name} {dur:.2f}s steps({n_chars}, end) forwards; "
            f"animation-delay: {t:.2f}s; }}"
        )

        body.append(
            f'<clipPath id="{clip_id}"><rect class="{anim_name}" x="0" y="{y-16}" height="20" width="0"/></clipPath>'
            f'<text class="{cls}" x="28" y="{y}" clip-path="url(#{clip_id})">{safe}</text>'
        )

        if text:
            t += dur
        t += gap

    last_text = lines[-1][0]
    cursor_x = 28 + len(last_text) * char_w + 4
    cursor_y = top_pad + (len(lines) - 1) * line_h
    cursor_delay = t
    per_line_style.append(
        f".cursor {{ animation: cursor-in 0.15s ease forwards {cursor_delay:.2f}s, "
        f"blink 0.9s steps(1) infinite {cursor_delay:.2f}s; }}\n"
        f"@keyframes cursor-in {{ to {{ opacity: 1; }} }}"
    )
    body.append(f'<rect class="cursor" x="{cursor_x:.1f}" y="{cursor_y - 13}" width="9" height="16"/>')

    style = base_style + "<style>" + "\n".join(per_line_style) + "</style>"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
{style}
  <rect class="term-bg" x="0" y="0" width="{width}" height="{height}" rx="10"/>
  <g class="scan" clip-path="url(#winclip)">{scanlines}</g>
  <clipPath id="winclip"><rect x="0" y="0" width="{width}" height="{height}" rx="10"/></clipPath>
  <rect class="titlebar" x="0" y="0" width="{width}" height="34" rx="10"/>
  <rect x="0" y="20" width="{width}" height="14" fill="#161b22"/>
  <circle cx="22" cy="17" r="6" fill="#ff5f56"/>
  <circle cx="42" cy="17" r="6" fill="#ffbd2e"/>
  <circle cx="62" cy="17" r="6" fill="#27c93f"/>
  <text x="{width/2}" y="22" text-anchor="middle" fill="{DIM}" font-family="{FONT}" font-size="12">{esc(username)} — agent session</text>
  {"".join(body)}
  <rect class="frame" x="1" y="1" width="{width-2}" height="{height-2}" rx="10"/>
</svg>'''
    return svg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--username", default="sarthakyerane")
    ap.add_argument("--out", default="assets/terminal.svg")
    ap.add_argument("--offline", action="store_true")
    args = ap.parse_args()

    stats = {"public_repos": "5+", "followers": "?", "latest_repo": "Meeting-Intelligence-Agent"} \
        if args.offline else fetch_live_stats(args.username)

    svg = build_svg(args.username, stats)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        f.write(svg)
    print(f"wrote {args.out} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()

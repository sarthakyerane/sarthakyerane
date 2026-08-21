#!/usr/bin/env python3
"""
Generates an animated 'live activity log' SVG from your real public GitHub
events (pushes, PRs, etc) via the REST /events endpoint. Amber-themed to
read as a distinct system-log panel next to the green terminal header.
"""
import argparse
import os
import sys
import requests

FONT = "'JetBrains Mono','Fira Code',ui-monospace,SFMono-Regular,Consolas,monospace"
BG = "#0d1117"
AMBER = "#ffa657"
DIM = "#6e7681"
WHITE = "#c9d1d9"


def fmt_event(e):
    t = e.get("type", "")
    repo = e.get("repo", {}).get("name", "?").split("/")[-1]
    if t == "PushEvent":
        n = len(e.get("payload", {}).get("commits", []))
        return f"push  {repo}  ({n} commit{'s' if n != 1 else ''})"
    if t == "CreateEvent":
        ref_type = e.get("payload", {}).get("ref_type", "repo")
        return f"create  {ref_type}  {repo}"
    if t == "PullRequestEvent":
        action = e.get("payload", {}).get("action", "")
        return f"pr {action}  {repo}"
    if t == "IssuesEvent":
        action = e.get("payload", {}).get("action", "")
        return f"issue {action}  {repo}"
    if t == "WatchEvent":
        return f"starred  {repo}"
    if t == "ForkEvent":
        return f"forked  {repo}"
    return f"{t.replace('Event','').lower()}  {repo}"


def fetch_events(username: str, limit=6):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-readme-generator"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        r = requests.get(
            f"https://api.github.com/users/{username}/events/public?per_page=20",
            headers=headers, timeout=10,
        )
        r.raise_for_status()
        events = r.json()
        lines = []
        for e in events:
            line = fmt_event(e)
            if line not in lines:
                lines.append(line)
            if len(lines) >= limit:
                break
        return lines or ["no recent public activity"]
    except Exception as ex:
        print(f"[warn] live fetch failed, using placeholders: {ex}", file=sys.stderr)
        return ["push  Meeting-Intelligence-Agent  (3 commits)", "create  repo  Codesage"]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg(username: str, lines: list) -> str:
    width, line_h, top_pad = 620, 26, 48
    height = top_pad + line_h * len(lines) + 24

    style = f"""
    <style>
      .bg {{ fill: {BG}; }}
      text {{ font-family: {FONT}; font-size: 13.5px; }}
      .title {{ fill: {WHITE}; }}
      .amber {{ fill: {AMBER}; }}
      .dim {{ fill: {DIM}; }}
      .row {{ opacity: 0; animation: in 0.4s ease forwards; }}
      @keyframes in {{ to {{ opacity: 1; }} }}
      .dot {{ animation: blink 1.4s ease-in-out infinite; }}
      @keyframes blink {{ 0%,100% {{ opacity:.3; }} 50% {{ opacity:1; }} }}
      .frame {{
        fill: none; stroke: {AMBER}; stroke-opacity: 0.3; stroke-width: 1.5;
        animation: pulse 3.2s ease-in-out infinite;
      }}
      @keyframes pulse {{ 0%,100% {{ stroke-opacity:.12; }} 50% {{ stroke-opacity:.4; }} }}
    </style>
    """

    body = []
    for i, line in enumerate(lines):
        y = top_pad + i * line_h
        delay = 0.15 + i * 0.18
        body.append(
            f'<circle class="dot" cx="18" cy="{y-4}" r="3" fill="{AMBER}" style="animation-delay:{delay:.2f}s"/>'
            f'<text class="row amber" x="30" y="{y}" style="animation-delay:{delay:.2f}s">{esc(line)}</text>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
{style}
  <rect class="bg" x="0" y="0" width="{width}" height="{height}" rx="10"/>
  <text class="title dim" x="16" y="26">$ tail -f /var/log/{esc(username)}/activity.log</text>
  {"".join(body)}
  <rect class="frame" x="1" y="1" width="{width-2}" height="{height-2}" rx="10"/>
</svg>'''
    return svg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--username", default="sarthakyerane")
    ap.add_argument("--out", default="assets/activity.svg")
    ap.add_argument("--offline", action="store_true")
    args = ap.parse_args()

    lines = ["push  Meeting-Intelligence-Agent  (3 commits)", "create  repo  Codesage"] \
        if args.offline else fetch_events(args.username)
    svg = build_svg(args.username, lines)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        f.write(svg)
    print(f"wrote {args.out} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()

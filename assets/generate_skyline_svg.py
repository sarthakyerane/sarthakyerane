#!/usr/bin/env python3
"""
Animated isometric-style language skyline. Building height = language usage
(from your real repos via REST API). Whole skyline gently sways like a
slow-turning platform; windows twinkle. Self-built, not a stats-card service.
"""
import argparse, os, sys
from collections import Counter
import requests

BG = "#0d1117"
FONT = "'JetBrains Mono','Fira Code',ui-monospace,SFMono-Regular,Consolas,monospace"
DIM = "#6e7681"

LANG_COLORS = {
    "Python": "#3572A5", "JavaScript": "#f1c40f", "TypeScript": "#3178c6",
    "C++": "#f34b7d", "C": "#8a8a8a", "HTML": "#e34c26", "CSS": "#7952b3",
    "Java": "#b07219", "Go": "#00ADD8", "Rust": "#dea584",
    "Dockerfile": "#4d7a8c", "Shell": "#89e051",
}
DEFAULT_COLOR = "#39d353"


def shade(hex_color, factor):
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    r, g, b = (max(0, min(255, int(c * factor))) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


def fetch_languages(username: str):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-readme-generator"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        repos, page = [], 1
        while True:
            r = requests.get(f"https://api.github.com/users/{username}/repos?per_page=100&page={page}",
                              headers=headers, timeout=10)
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
        return [("Python", 6), ("TypeScript", 4), ("JavaScript", 3), ("C++", 2)]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg(username: str, langs: list) -> str:
    width, height = 720, 340
    ground_y = 270
    step_x, step_y = 90, -16
    bw, depth = 52, 16
    max_count = max(c for _, c in langs) if langs else 1
    start_x = 60

    style = f"""
    <style>
      .bg {{ fill: {BG}; }}
      text {{ font-family: {FONT}; }}
      .title {{ fill: {DIM}; font-size: 12.5px; }}
      .label {{ fill: #c9d1d9; font-size: 12px; }}
      .scene {{
        transform-box: fill-box;
        transform-origin: 50% 100%;
        animation: sway 7s ease-in-out infinite;
      }}
      @keyframes sway {{
        0%, 100% {{ transform: rotate(-2.2deg); }}
        50% {{ transform: rotate(2.2deg); }}
      }}
      .win {{ animation: twinkle 2.6s ease-in-out infinite; }}
      @keyframes twinkle {{
        0%, 100% {{ opacity: 0.15; }}
        50% {{ opacity: 0.9; }}
      }}
      .rise {{ animation: rise 0.9s cubic-bezier(.2,.8,.2,1) both; }}
      @keyframes rise {{
        from {{ transform: scaleY(0); }}
        to   {{ transform: scaleY(1); }}
      }}
    </style>
    """

    buildings = []
    labels = []
    for i, (lang, count) in enumerate(langs):
        h = 40 + (count / max_count) * 140
        color = LANG_COLORS.get(lang, DEFAULT_COLOR)
        top_c, side_c = shade(color, 1.35), shade(color, 0.55)
        bx = start_x + i * step_x
        by = ground_y + i * step_y

        front = f'<rect x="{bx}" y="{by-h:.1f}" width="{bw}" height="{h:.1f}" fill="{color}"/>'
        top = (f'<polygon points="{bx},{by-h:.1f} {bx+bw},{by-h:.1f} {bx+bw+depth},{by-h-depth:.1f} '
               f'{bx+depth},{by-h-depth:.1f}" fill="{top_c}"/>')
        side = (f'<polygon points="{bx+bw},{by-h:.1f} {bx+bw},{by:.1f} {bx+bw+depth},{by-depth:.1f} '
                f'{bx+bw+depth},{by-h-depth:.1f}" fill="{side_c}"/>')

        windows = []
        rows = max(2, int(h // 22))
        for r in range(rows):
            wy = by - 14 - r * 20
            if wy < by - h + 6:
                break
            delay = (i * 0.3 + r * 0.4) % 3
            windows.append(
                f'<rect class="win" x="{bx+10}" y="{wy:.1f}" width="8" height="8" fill="#ffe9a8" '
                f'style="animation-delay:{delay:.2f}s"/>'
                f'<rect class="win" x="{bx+bw-18}" y="{wy:.1f}" width="8" height="8" fill="#ffe9a8" '
                f'style="animation-delay:{delay+0.5:.2f}s"/>'
            )

        buildings.append(
            f'<g class="rise" style="animation-delay:{i*0.12:.2f}s; transform-box: fill-box; transform-origin:50% 100%;">'
            f'{front}{top}{side}{"".join(windows)}</g>'
        )
        labels.append(f'<text class="label" x="{bx+bw/2:.1f}" y="{by+18-i*step_y*0+18:.1f}" text-anchor="middle">{esc(lang)}</text>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
{style}
  <rect class="bg" x="0" y="0" width="{width}" height="{height}" rx="10"/>
  <text class="title" x="16" y="26">$ du -h --languages ~/{esc(username)}</text>
  <g class="scene">
    {"".join(buildings)}
  </g>
  {"".join(labels)}
</svg>'''
    return svg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--username", default="sarthakyerane")
    ap.add_argument("--out", default="assets/skyline.svg")
    ap.add_argument("--offline", action="store_true")
    args = ap.parse_args()
    langs = [("Python", 6), ("TypeScript", 4), ("JavaScript", 3), ("C++", 2)] if args.offline else fetch_languages(args.username)
    svg = build_svg(args.username, langs)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        f.write(svg)
    print(f"wrote {args.out} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()

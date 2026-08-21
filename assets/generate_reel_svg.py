#!/usr/bin/env python3
"""
Infinite auto-cycling project reel. Each project fades/slides in, holds,
fades out, then the next one plays — forever, no clicking. Pure CSS keyframe
choreography, all projects share one animation timeline so they never overlap.
"""
import argparse, os

BG = "#0d1117"
FONT = "'JetBrains Mono','Fira Code',ui-monospace,SFMono-Regular,Consolas,monospace"
GREEN = "#39d353"
WHITE = "#c9d1d9"
DIM = "#6e7681"

PROJECTS = [
    ("Meeting Intelligence Agent", "Agentic meeting memory via Claude Desktop + MCP",
     "LangGraph · FastAPI · Groq · ChromaDB · MySQL", "60% faster via 4-way parallel extraction"),
    ("Document Delta & Grounded Chat", "Format-agnostic revision diffing + cited RAG chat",
     "Gemini Vision · ChromaDB · Redis", "Numeric diffs never touch an LLM"),
    ("CodeSage", "RAG over your own codebase, hybrid with static analysis",
     "tree-sitter · Ollama · C++ analyzer", "10+ languages, deterministic bug detection"),
    ("Isometric MTO Generator", "Piping drawing to structured Material Take-Off",
     "Next.js · FastAPI · Gemini Vision", "Runs at temp 0.1, near-zero hallucination"),
    ("RIOM", "Ambient screen understanding you can query in English",
     "Tesseract · ChromaDB · Redis", "Privacy denylist built in, local-first"),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg() -> str:
    width, height = 720, 190
    n = len(PROJECTS)
    slot = 100 / n
    fade = 1.8
    total_dur = n * 4.4  # seconds

    style_blocks = []
    body = []

    for i, (name, tagline, stack, note) in enumerate(PROJECTS):
        s = slot * i
        e = slot * (i + 1)
        mid = (s + e) / 2
        stops = sorted(set([0, s, min(s + fade, e), max(e - fade, s), e, 100]))
        kf = []
        for p in stops:
            if p <= s + fade + 0.001 and p >= s - 0.001 and p < mid:
                pass
            opacity = 1 if (s + fade - 0.05) <= p <= (e - fade + 0.05) else 0
            ty = 0 if opacity == 1 else (10 if p < mid else -10)
            kf.append(f"{p:.2f}% {{ opacity:{opacity}; transform: translateY({ty}px); }}")
        anim_name = f"slot{i}"
        style_blocks.append(
            f"@keyframes {anim_name} {{ {' '.join(kf)} }}\n"
            f".{anim_name} {{ animation: {anim_name} {total_dur:.1f}s ease-in-out infinite; }}"
        )
        dot_opacity_full = f"@keyframes dot{i} {{ "
        dkf = []
        for p in stops:
            on = 1 if (s + fade - 0.05) <= p <= (e - fade + 0.05) else 0.25
            dkf.append(f"{p:.2f}% {{ opacity:{on}; }}")
        dot_opacity_full += " ".join(dkf) + " }"
        style_blocks.append(dot_opacity_full)
        style_blocks.append(f".dot{i} {{ animation: dot{i} {total_dur:.1f}s ease-in-out infinite; }}")

        body.append(f'''
        <g class="{anim_name}" style="transform-box: fill-box;">
          <text x="24" y="70" fill="{GREEN}" font-family="{FONT}" font-size="19" font-weight="700">{esc(name)}</text>
          <text x="24" y="98" fill="{WHITE}" font-family="{FONT}" font-size="14">{esc(tagline)}</text>
          <text x="24" y="122" fill="{DIM}" font-family="{FONT}" font-size="12.5">{esc(stack)}</text>
          <text x="24" y="146" fill="{GREEN}" font-family="{FONT}" font-size="12.5" opacity="0.85">↳ {esc(note)}</text>
        </g>''')

    dots = "".join(
        f'<circle class="dot{i}" cx="{24 + i*22}" cy="172" r="4" fill="{GREEN}"/>' for i in range(n)
    )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <style>
      .bg {{ fill: {BG}; }}
      .frame {{ fill:none; stroke:{GREEN}; stroke-opacity:0.3; stroke-width:1.5; animation: pulse 3.2s ease-in-out infinite; }}
      @keyframes pulse {{ 0%,100% {{ stroke-opacity:.12; }} 50% {{ stroke-opacity:.4; }} }}
      {"".join(style_blocks)}
    </style>
  <rect class="bg" x="0" y="0" width="{width}" height="{height}" rx="10"/>
  {"".join(body)}
  {dots}
  <rect class="frame" x="1" y="1" width="{width-2}" height="{height-2}" rx="10"/>
</svg>'''
    return svg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="assets/reel.svg")
    args = ap.parse_args()
    svg = build_svg()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        f.write(svg)
    print(f"wrote {args.out} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()

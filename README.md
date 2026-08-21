<!--
  HEY SARTHAK — everything's filled in now, pulled from your resume and
  real repo READMEs. Nothing left to swap out. Give it one read-through,
  then delete this comment block before you commit — it doesn't render
  on GitHub anyway, just keeps the file clean.
-->

<div align="center">

```
$ curl -s api.status/sarthakyerane

{
  "status": "operational",
  "on_call": "Sarthak Yerane — backend & applied AI",
  "region": "Bengaluru, India",
  "uptime": "no major incidents since first commit",
  "docs": "you're reading them"
}
```

</div>

<br>

### About this service

GenAI developer building production RAG systems, agentic reasoning pipelines,
and MCP servers — bridging low-level systems work (native C++ static
analysis, AST parsing) with LLM-powered architectures. If a model call can
fail, I'd rather it fail loudly and recover than fail silently and lie.

Currently open to: **internships**

<br>

## Service Status

*Live components. Status reflects what's actually shipped, not what's planned.*

| Service | Status | What it does |
|---|---|---|
| **[Meeting-Intelligence-Agent](https://github.com/sarthakyerane/Meeting-Intelligence-Agent)** | 🟢 operational | Agentic meeting analysis — cross-meeting memory, semantic search, contradiction detection across projects, exposed to Claude Desktop via MCP |
| **[Codesage](https://github.com/sarthakyerane/Codesage)** | 🟢 operational | Upload a codebase, ask questions in plain English — tree-sitter AST parsing + RAG retrieval + a hand-written C/C++ static analyzer for deterministic bug detection |
| **[Isometric-Mto-Generator](https://github.com/sarthakyerane/Isometric-Mto-Generator)** | 🟡 partial — documented limits | Piping isometric drawing in, structured Material Take-Off out, via a Gemini Vision pipeline with confidence-scored extraction |
| **[Document-delta-chat](https://github.com/sarthakyerane/Document-delta-chat)** | 🟢 operational | Format-agnostic revision diffing (PDF/DWG) + grounded RAG chat — a deterministic delta engine that only calls an LLM when string comparison genuinely can't decide, backed by a 3-tier Groq → Gemini → Ollama fallback and per-claim source citations |
| **[Omnisight-engine](https://github.com/sarthakyerane/Omnisight-engine)** *(RIOM)* | 🟢 operational | Ambient screen recall — silently captures your screen, OCR + LLM-tags every frame, then answers "what was I looking at at 3pm?" in plain English, with a privacy denylist for password managers and banking sites |
| **[Structures](https://github.com/sarthakyerane/Structures)** | 🟢 operational | DSA implementations in C++ — the load-bearing wall under everything above |

<br>

## Fallback Chain

*Every one of my LLM pipelines has a priority order when the primary fails.
So do I.*

```
PRIMARY    → deep focus, one problem at a time
FALLBACK 1 → coffee (cold, forgotten, reheated once)
FALLBACK 2 → rubber-duck the bug to whoever's in Discord
FALLBACK 3 → close laptop, walk, come back — usually resolves in O(1)
LAST RESORT → re-read my own README from three repos ago
```

<br>

<details>
<summary><strong>Known Limitations</strong> — click to expand</summary>
<br>

Borrowed this section header directly from my own Isometric-Mto-Generator
README, because it should be standard practice everywhere, not just in
repos:

- **Confidence drops on ambiguous input.** True for Gemini reading a
  hand-drawn isometric. Also true for me reading a spec with no acceptance
  criteria.
- **Async is still a work in progress.** The MTO generator runs its
  pipeline synchronously and blocks for 10–20s — noted in its own README
  as the first thing I'd fix with more time. Same policy applies to how
  I context-switch.
- **Mock mode exists for a reason.** If a required key is missing, my
  apps return a clearly-labeled mock instead of crashing. I'd rather ship
  something honest and incomplete than something that pretends.
- **Some formats just don't have clean answers.** Document-delta-chat
  supports DXF fully but documents exactly where binary DWG parsing hits
  a wall, instead of quietly returning an empty document. I'd rather say
  "here's the boundary" than pretend the coverage is total.

</details>

<br>

## Escalation Policy

*Who gets paged, in order.*

| Channel | Contact |
|---|---|
| GitHub | [@sarthakyerane](https://github.com/sarthakyerane) |
| Email | [sarthakyerane123@gmail.com](mailto:sarthakyerane123@gmail.com) |
| LinkedIn | [linkedin.com/in/sarthakyerane](https://www.linkedin.com/in/sarthakyerane/) |

<br>

<div align="center">

<sub>this service has been building continuously — see commit history for the incident log</sub>

</div>

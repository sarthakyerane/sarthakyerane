<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&duration=2500&pause=1000&color=2DD4BF&center=true&vCenter=true&width=600&lines=%24+curl+-s+api.status%2Fsarthakyerane;%7B+%22status%22%3A+%22operational%22+%7D;fetching+fallback_chain...+done;3+LLM+pipelines+%C2%B7+0+downtime" alt="Typing SVG" />

<br><br>

![Profile views](https://komarev.com/ghpvc/?username=sarthakyerane&color=2DD4BF&style=flat-square&label=profile+views)
![Status](https://img.shields.io/badge/status-operational-2DD4BF?style=flat-square)
![Region](https://img.shields.io/badge/region-Bengaluru%2C%20India-2DD4BF?style=flat-square)

</div>

<br>

### About this service

GenAI developer building production RAG systems, agentic reasoning pipelines,
and MCP servers — bridging low-level systems work (native C++ static
analysis, AST parsing) with LLM-powered architectures. If a model call can
fail, I'd rather it fail loudly and recover than fail silently and lie.

Currently open to: **internships**

<br>

<div align="center">

![Python](https://img.shields.io/badge/Python-2DD4BF?style=flat-square&logo=python&logoColor=black)
![C++](https://img.shields.io/badge/C++-2DD4BF?style=flat-square&logo=cplusplus&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-2DD4BF?style=flat-square&logo=fastapi&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-2DD4BF?style=flat-square&logo=docker&logoColor=black)
![Redis](https://img.shields.io/badge/Redis-2DD4BF?style=flat-square&logo=redis&logoColor=black)
![Groq](https://img.shields.io/badge/Groq-2DD4BF?style=flat-square)
![Gemini](https://img.shields.io/badge/Gemini-2DD4BF?style=flat-square&logo=googlegemini&logoColor=black)
![ChromaDB](https://img.shields.io/badge/ChromaDB-2DD4BF?style=flat-square)
![LangChain](https://img.shields.io/badge/LangChain-2DD4BF?style=flat-square)
![MCP](https://img.shields.io/badge/MCP-2DD4BF?style=flat-square)

</div>

<br>

## Service Status

*Live components. Status reflects what's actually shipped, not what's planned.*

| Service | Status | What it does |
|---|---|---|
| **[Meeting-Intelligence-Agent](https://github.com/sarthakyerane/Meeting-Intelligence-Agent)** | 🟢 operational | Agentic meeting analysis — cross-meeting memory, semantic search, contradiction detection, exposed to Claude Desktop via a 5-tool MCP server |
| **[Codesage](https://github.com/sarthakyerane/Codesage)** | 🟢 operational | Upload a codebase, ask questions in plain English — tree-sitter AST parsing + RAG retrieval + a hand-written C/C++ static analyzer |
| **[Isometric-Mto-Generator](https://github.com/sarthakyerane/Isometric-Mto-Generator)** | 🟡 partial — documented limits | Piping isometric drawing in, structured Material Take-Off out, via a Gemini Vision pipeline with confidence-scored extraction |
| **[Document-delta-chat](https://github.com/sarthakyerane/Document-delta-chat)** | 🟢 operational | Format-agnostic revision diffing (PDF/DWG) + grounded RAG chat, 3-tier Groq → Gemini → Ollama fallback |
| **[Omnisight-engine](https://github.com/sarthakyerane/Omnisight-engine)** *(RIOM)* | 🟢 operational | Ambient screen recall — OCR + LLM-tags every frame, semantic search over your own screen history |
| **[Structures](https://github.com/sarthakyerane/Structures)** | 🟢 operational | DSA implementations in C++ — the load-bearing wall under everything above |

<br>

## Fallback Chain

*Every one of my LLM pipelines has a priority order when the primary fails. So do I.*

<br>

<details>
<summary><strong>Known Limitations</strong> — click to expand</summary>
<br>

- **Confidence drops on ambiguous input.** True for Gemini reading a hand-drawn isometric. Also true for me reading a spec with no acceptance criteria.
- **Async is still a work in progress.** The MTO generator blocks for 10–20s synchronously — first thing I'd fix with more time. Same policy applies to how I context-switch.
- **Mock mode exists for a reason.** If a required key is missing, my apps return a clearly-labeled mock instead of crashing.
- **Some formats just don't have clean answers.** Document-delta-chat documents exactly where binary DWG parsing hits a wall instead of quietly returning an empty document.

</details>

<br>

## GitHub Stats

<div align="center">

<img src="https://github-readme-stats.vercel.app/api?username=sarthakyerane&show_icons=true&theme=github_dark&hide_border=true&bg_color=0D1117&title_color=2DD4BF&icon_color=2DD4BF&text_color=C9D1D9" width="48%" />
<img src="https://github-readme-streak-stats.herokuapp.com/?user=sarthakyerane&theme=github-dark-blue&hide_border=true&background=0D1117&ring=2DD4BF&fire=2DD4BF&currStreakLabel=2DD4BF" width="48%" />

</div>

<br>

<div align="center">

![Snake animation](https://raw.githubusercontent.com/sarthakyerane/sarthakyerane/output/github-contribution-grid-snake.svg)

</div>

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
![Snake animation](https://raw.githubusercontent.com/sarthakyerane/sarthakyerane/output/github-contribution-grid-snake.svg)

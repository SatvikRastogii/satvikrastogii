<!--
  Source of truth for the Markdown. README.md is generated from this file by
  `python src/build.py --readme` and is overwritten on every workflow run, so
  edit this file, never README.md.

  Placeholders filled by the generator:
    {{HERO}}        <picture> for whichever variant is active this week
    {{ALTERNATES}}  <details> blocks for the other two
    {{STAMP}}       generation date and the variant rotation note

  Everything else here is plain Markdown and is yours to edit. Remember that
  GitHub strips class, id and style attributes, so all styling has to live
  inside the SVGs.
-->
<div align="center">

{{HERO}}

</div>

<div align="center">

[**Portfolio**](https://satvikrastogi.vercel.app) &nbsp;·&nbsp;
[**Résumé**](https://satvikrastogi.vercel.app/satvik-rastogi-resume.pdf) &nbsp;·&nbsp;
[LinkedIn](https://www.linkedin.com/in/satvikrastogii) &nbsp;·&nbsp;
[LeetCode](https://leetcode.com/u/blackmancodes) &nbsp;·&nbsp;
[satvikrastogi777@gmail.com](mailto:satvikrastogi777@gmail.com)

</div>

---

### Selected work

**[LexGraph](https://satvikrastogi.vercel.app)** — a GraphRAG legal knowledge
navigator over Indian Supreme Court judgments. Two retrieval pipelines, flat
vector search and a knowledge graph, read the same corpus, answer the same
questions and are judged on the same metrics. Hybrid semantic router,
contradiction detection for overruled precedent, runs locally.
`Python` `GraphRAG` `NetworkX` `ChromaDB` `Llama 3.1` `RAGAS`

**[QueryForge](https://satvikrastogi.vercel.app)** — an agentic Postgres index
advisor. An LLM proposes index configurations and a real database benchmark
grades them: the actual query planner on the actual workload, not a second
model scoring the first. Propose, benchmark, archive, propose again. Read-only
allowlist, least-privilege role, hard storage budget.
`LangGraph` `MCP` `Langfuse` `Postgres`

**Wireless sensor network research** — two papers under review, six authors,
with MAIT faculty. One benchmarks classical, threshold-based and AI-driven
clustering protocols under a single simulation framework. The other is HIECF,
which pairs type-2 fuzzy logic with Q-learning for cluster head selection.

The measured results, including the metrics where these lost, are written up on
the [portfolio](https://satvikrastogi.vercel.app).

---

{{ALTERNATES}}

---

<sub>
Every image above is an animated SVG built from source in this repository —
no third-party README widgets, no badge services, no web fonts. The type is a
bitmap face in <code>src/glyphs.py</code> and a skeleton display face in
<code>src/pathfont.py</code>, both hand-authored, both rendered as geometry so
nothing depends on a font being available. The only numbers anywhere are live
counts pulled from the GitHub API by
<a href="https://github.com/SatvikRastogii/satvikrastogii/actions">a scheduled
workflow</a>. {{STAMP}}
</sub>

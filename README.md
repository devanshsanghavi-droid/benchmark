# Beyond Games: Research on LLM Benchmark Success and Failure, and a New Benchmarking Method

Work in progress. Layout:

- `research/notes/` — verified research dossiers produced by research subagents (one per topic)
- `research/refs/` — per-topic reference lists (JSON), each entry fact-checked
- `paper/` — the research paper (Markdown + BibTeX, rendered to PDF by `scripts/build_paper.py`)
- `scripts/` — build and analysis scripts

## Latest report

- [`research/reports/Business simulation benchmark design.md`](research/reports/Business%20simulation%20benchmark%20design.md): design for a business-simulation benchmark in which an AI runs a small shop or café, modelled on Andon Labs' real deployments (10 Oct 2026). It covers the world model module by module, 43 planted traps, the simulator architecture and tools, scoring, calibration and validation, and a costed build plan. It was assembled from 12 fact-checked dossiers, then put through four independent critiques and a final fact-check. Evidence is in `research/research_notes/Business sim deep dive/`, including a 402-variable master catalogue.
- [`research/reports/Novel AI benchmark and game ideas.md`](research/reports/Novel%20AI%20benchmark%20and%20game%20ideas.md): ranked shortlist of new benchmark and game ideas (1 Oct 2026), built from seven survey panels, a design-principles synthesis, 47 candidates, two rounds of red-teaming and blinded pilots. Evidence is in `research/research_notes/Novel AI benchmark and game ideas/`.

## Paper and DEBRIEF

- `paper/paper.md` → `paper/build/paper.pdf` (`python scripts/build_paper.py`): *Grade the Ripple, Not the Stone*. Why benchmarks fail, the red-teamed search, and live DEBRIEF pilots.
- `debrief/`: DEBRIEF reference implementation (generator, interpreter, mutation library, prompts, Net Fix Rate scoring), pilot driver (`python -m debrief.pilot`) and v1 analysis (`python -m debrief.analyze_v1`). Tests: `python -m pytest tests`.
- `results/pilot_v0/`, `results/pilot_v1/`: live pilot prompts, replies, coach notes, item keys and scores.

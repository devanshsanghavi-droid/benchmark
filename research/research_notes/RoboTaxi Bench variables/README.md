# RoboTaxi Bench variables: research notes (Oct 2026)

These notes are the sources for `research/reports/RoboTaxi Bench variables*.md` and `.csv`.

- **`R01`–`R12_*.md`**: 12 domain dossiers. Each one was written by a research agent. An independent fact-checker then edited it in place, adding `[corrected by fact-check: ...]` and `[uncertain: ...]` markers and a closing "Fact-check log".
- **`*_data/`**: small aggregates and analysis scripts the agents used. These include hourly demand curves computed from TLC trip records read via GitHub copies, because the TLC CloudFront host is blocked here.
- **`all_variables.json`**: the 824 verified domain variables.
- **`ALL_VARIABLES_COMPACT.md`**: one line per variable.
- **`gaps_and_merge.json`**: three output sets:
  - the three gap critics (veteran NYC driver, simulation engineer, robotaxi fleet operator);
  - 101 gap variables, fact-checked;
  - the editor's box structure, duplicate list (89), top 30, core-MVP set and still-missing list.
- **Rendering:** `python3 scripts/robotaxi_render.py collect ...` then `render ...` regenerates the reports.

**Coverage caveats.** nyc.gov, arXiv, NBER and some other hosts were unreachable, and the shared web-search budget ran out during several domains. Many regulatory figures therefore rest on search snippets and are tagged [S]. Agents tagged their own guesses [design] or [U].

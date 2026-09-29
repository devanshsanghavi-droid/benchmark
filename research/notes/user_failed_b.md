# Lead-supplied "failed" benchmarks, items 6-10: Boardwalk, grid-based game competitions, TopoBench, raw corpora to domain benchmarks, and BloomQA

Dossier prepared 2026-09-29 for the benchmark-design project. Scope: verify identity, gather adoption evidence, test the project lead's critique, and pull out design lessons for items 6-10 on the lead's list.

---

## Summary

All five arXiv IDs match the papers the lead described. There is one naming wrinkle: item 9 went up on arXiv under a different title, "Beyond Benchmarks: A Novel Framework for Domain-Specific LLM Evaluation and Knowledge Mapping", and was later renamed "From Raw Corpora to Domain Benchmarks: Automated Evaluation of LLM Domain Expertise". None of the five became a widely used leaderboard. Their failure modes differ, though, and the lead's critiques are uneven. Some are accurate, some are overstated, and one or two misread what the paper was trying to do.

| # | Paper (arXiv) | What it actually is | Main reasons it did not become a benchmark people use | Verdict on lead's critique |
|---|---|---|---|---|
| 6 | Boardwalk (2508.16447), SBGames 2025 | A **framework and feasibility study**: can LLMs write playable Python for board games from anonymized rules? 12 games, 3 LLMs | It was never built as a ranking benchmark. N is tiny. The public repo holds the API but not the evaluation outputs or evaluator. Regional venue. Google DeepMind's "Code World Models" (ICLR 2026) framed the same NL-rules-to-code capability more strongly, with verification. [corrected by fact-check: CWM (arXiv v1 6 Oct 2025) came about six weeks *after* Boardwalk (arXiv Aug 2025), so it overshadowed Boardwalk rather than pre-empting it; the genuinely earlier work is *From Code to Play* (arXiv Dec 2024)] | **Partially agree.** "Too few games to rank" is correct. "Renaming causes false results" overstates it: the authors deliberately contrasted popular and obscure games, which is the right control, and the actual risk is inflation, not falseness |
| 7 | Grid-based game competitions (2407.07796) | LLM-vs-LLM Tic-Tac-Toe, Connect-Four and Gomoku with three prompt formats. 2,310 matches, 7 LLMs plus a random player | Leaderboard frozen since mid/late 2024 (last model added Jul 2024, last commit Dec 2024). Scores are pool-relative, fragmented, and have no optimal-play reference. Pre-empted by GTBench (Feb 2024, NeurIPS 2024). Weak construct: perception/format confounds strategy | **Partially agree / mostly disagree on "max out instantly".** The games are solved, but the 2024 models did *not* saturate them: invalid moves and disqualifications were common, especially with image and illustration prompts. EMNLP 2025's TTT-Bench shows novel TTT-style games still trip up reasoning models |
| 8 | TopoBench (2603.12133), ICLR 2026 workshop | 6 Simon-Tatham-style topology puzzle families x 3 tiers, 900 instances, with a diagnostic study of failure causes | Promised code repo is **empty** six months after release. The name **collides** with an established "TopoBench" (a topological deep learning library, 256 stars). Workshop venue. 9 models, top closed model was GPT-5-mini. 50 instances per cell. No leaderboard. Crowded space (Enigmata, Reasoning Gym, PUZZLES) | **Disagree on "very simple"** (hard-tier accuracy is 0.15-0.24). **Partially agree on "nothing new"** as a benchmark. The novel part is the causal error analysis, not the task set. Calling it "dead" at about 6 months is premature |
| 9 | Raw corpora to domain benchmarks (2506.07658) | A deterministic, LLM-free pipeline: TF/TF-IDF domain keywords become cloze-style prompt-target pairs, scored by the **rank of the target token** | Needs logit access, so frontier closed-API models are effectively excluded (all reported models are open-weight: GPT-2, Llama-2/3.1, OLMo-2, Qwen-2, Mistral). The metric is unintuitive (median rank; v3 uses a 20% trimmed mean of ranks [corrected by fact-check]). No public code found. Retitled mid-life. Still under review (TMLR) | **Partially agree.** It measures domain *knowledge recall*, not expertise. But the lead mis-describes it: it is a training-time diagnostic for base models, and it was validated against an expert benchmark (r = 0.99, p < 0.001, over 6 base models; the r = 0.91 figure belongs to a Claude-generated comparison benchmark, not to this pipeline [corrected by fact-check]). As a public leaderboard it was never viable; as a diagnostic tool it is reasonable |
| 10 | BloomQA / Bloom's-taxonomy benchmark generation (2601.20253) | LLM-assisted pipeline: expert guidelines become violation scenarios, then MCQs and multi-turn dialogues at four Bloom levels. Teaching, dietetics, caregiving. About 60k+ MCQs and 15k+ dialogues (secondary source) | Generator-bias ("echo chamber") and item-validity risk. MCQ format. Niche domains with little frontier-lab pull. No official release found. The counter-intuitive headline (models better at "Analyze" than "Remember") may be an artifact of generated difficulty labels | **Partially agree.** Grounding in expert-authored guidelines is a real mitigation, and scale does help per-practice statistics. The real gap is published human validation of item quality and empirical (not assigned) difficulty calibration. Too young (8 months) to call dead |

The main cross-cutting lesson: **for these five, the lead's "the games or tasks are uninteresting" framing is secondary.** The recurring causes of non-adoption are infrastructural and methodological:

1. No maintained leaderboard, or no leaderboard at all.
2. Released artifacts that are missing or partial.
3. Metrics that exclude the frontier models people care about.
4. Small N with no uncertainty reporting.
5. Pool-relative or fragmented scores.
6. Weak or unvalidated construct links to anything decision-relevant.
7. Poor discoverability: name collisions, retitling, regional or workshop venues.
8. Being pre-empted by better-resourced work.

A new benchmark can design against every one of these.

---

## Detailed findings

### 0. Method and evidence limits

- Evidence came from WebSearch result summaries, GitHub repository pages fetched via WebFetch, GitHub's code/repository search, and raw GitHub files. The raw files include verbatim arXiv abstracts mirrored in daily-digest repositories such as `Luvata/arxive`, `CSQianDong/Awesome-arXiv-Daily-Reporter`, `2shin0/arxiv-ai-mailing` and `LIHUA919/AI-Agents-Daily-Research`.
- arXiv, OpenReview, Semantic Scholar, SBC-SOL, dergipark and author homepages were blocked for direct fetch. **Citation counts were not visible in any source for any of the five papers.** All citation-count statements below are therefore absent or qualitative.
- The session's WebSearch budget ran out partway through item 10. Some BloomQA details therefore come only from a secondary AI-generated digest (`memgrafter/research-digests`) and are flagged as medium or low confidence.
- Repository star and fork counts are as observed on 2026-09-29.

---

### 6. Boardwalk (arXiv:2508.16447)

**Identity (verified)**
- Title: *Boardwalk: Towards a Framework for Creating Board Games with LLMs*.
- Authors: Álvaro Guglielmin Becker, Gabriel Bauer de Oliveira, Lana Bertoldo Rossato, Anderson Rocha Tavares. Sources: https://arxiv.org/abs/2508.16447 and the arXiv daily mirror https://github.com/LIHUA919/AI-Agents-Daily-Research (data/2025-08-25.md). Confidence: high.
- Posted to arXiv around 2025-08-22/25 (it appears in the 2025-08-25 digest), primary category cs.LG. Confidence: high.
- Venue: SBGames 2025, the Brazilian Symposium on Computer Games and Digital Entertainment. SBC-SOL page: https://sol.sbc.org.br/index.php/sbgames/article/view/37375 (seen in search results). A secondary catalog gives DOI 10.5753/sbgames.2025.10222 (https://github.com/zsyverse/game-ai-benchmarks-papers). Confidence: high for venue, medium for DOI.
- Affiliation: most likely UFRGS (Instituto de Informática). This is inferred from the same group's follow-up arXiv:2511.05114 by Becker, Rossato and Tavares, which a search result listed as UFRGS. Not directly verified for Boardwalk itself. Confidence: medium.

**What it does** (from the verbatim abstract in the mirror)
- Three "state-of-the-art LLMs (Claude, DeepSeek and ChatGPT)" were asked to code "a selection of 12 popular and obscure games in free-form and within Boardwalk, our proposed General Game Playing API".
- "We anonymize the games and components to avoid evoking pre-trained LLM knowledge. The implementations are tested for playability and rule compliance."
- Best result: "Claude 3.7 Sonnet, yielding 55.6% of games without any errors". "While compliance with the API increases error frequency, the severity of errors is more significantly dependent on the LLM."
- The abstract ends with "We outline future steps for creating a framework to integrate this process, making the elaboration of board games more accessible". **The stated goal is a game-development tool, not a model leaderboard.**
- A secondary catalog names the models as Claude 3.7 Sonnet, DeepSeek-V3 and GPT-4o, and says the models also adapted free-form code to the API (https://github.com/zsyverse/game-ai-benchmarks-papers, research/end-to-end-generation-sources.md §19). Confidence: medium.

**Adoption evidence**
- Official repo https://github.com/LabCRAIG/boardwalk: **2 stars, 0 forks, 24 commits**, created 2025-04-22, last updated 2026-04-06 (via GitHub repo search and page fetch). It contains the `Board`/`Game` Python API only. **No LLM evaluation outputs or evaluator scripts** are present, which the secondary catalog also notes ("Partial ... complete 12-game experiment outputs and evaluator suite are not in the repository").
- Follow-up by the same group: arXiv:2511.05114, *Usando LLMs para Programar Jogos de Tabuleiro e Variações*, in Portuguese, accepted at the "I Escola Regional de Aprendizado de Máquina e Inteligência Artificial da Região Sul, 2025" (search result). It extends the work to *variants* of existing games.
- Light third-party reuse: `Cody-Jiang-Zhihong/DesignVoyager` bundles a copy of Boardwalk ("A bundled implementation of the Boardwalk framework. Based on: Becker et al. ... arXiv:2508.16447") (GitHub code search). No lab or leaderboard use found.
- Citation count: not visible.

**Competing or pre-empting work**
- Google DeepMind, *Code World Models for General Game Playing* (arXiv:2510.04542, submitted 2025-10-06; the OpenReview PDF header reads "Published as a conference paper at ICLR 2026"). The LLM translates natural-language rules *and game trajectories* into executable Python following the OpenSpiel API: transition, legal-move and termination functions, plus heuristic value and inference functions. MCTS/ISMCTS then plays with that model. This addresses the same capability as Boardwalk (NL rules to executable game code) but adds (a) automatic verification against trajectories, (b) a downstream objective (win rate), and (c) an established API and institution. Sources: https://arxiv.org/abs/2510.04542, https://openreview.net/pdf?id=1UoB7IWiku, https://github.com/google-deepmind/open_spiel. Confidence: medium-high on the ICLR 2026 status (seen only as a PDF header in a search result).
- [corrected by fact-check] Chronology: CWM's arXiv v1 is dated 6 Oct 2025, about six weeks after Boardwalk's arXiv posting (Aug 2025), and the Boardwalk repo dates from April 2025. CWM therefore *overshadowed* Boardwalk; it did not *pre-empt* it.
- The code-world-model line kept going through 2026. Search results show *When a Verified World Model Still Loses* (arXiv:2607.14169) and *World-Time Compute with Verified Code World Models* (arXiv:2609.09163). Boardwalk's line did not see comparable uptake. [corrected by fact-check: 2607.14169 is a single-author preprint by Javier Aguilar Martín (abstract mirrored in CSQianDong/Awesome-arXiv-Daily-Reporter, 17-Jul-2026), not a DeepMind follow-up; 2609.09163 is from the quome-cloud/openworld group. Both show that the *CWM framing* attracted independent follow-ups.]
- Earlier: *From Code to Play: Benchmarking Program Search for Games Using Large Language Models* (arXiv:2412.04057, Dec 2024), by Eberhardinger, Goodman, Dockhorn, Perez-Liebana, Gaina, Çakmak, Maghsudi and Lucas; an IEEE version exists per the authors' repo (ManuelEberhardinger/Benchmarking-Language-Model-Based-Program-Search-for-Games). It covers 12 TAG tabletop games in Java plus Python game tasks. [corrected by fact-check: full title and authors added]

**Assessment of the lead's critique**
- *"Only 12 games, too few to rank models":* **Agree, with a caveat.** Twelve games x 3 models x 2-3 conditions is far too small to rank models. As an illustration: if the denominator were 36 (12 games x 3 conditions; 20/36 = 55.6%, but this is my inference and unverified), the 95% binomial half-width around 55.6% would be about ±16 pp. With 24 it would be about ±20 pp. The caveat is that the paper never claimed to be a ranking benchmark. Its title says "Towards a Framework", and its abstract frames it as a feasibility study for game creation. Judging it as a failed leaderboard is partly a category error.
- *"Renaming characters/values doesn't change the underlying concepts, so results are false":* **Partially agree.** Surface anonymization (renaming pieces and games) does not hide structural isomorphism: a renamed checkers is still checkers, so pretraining can inflate success. But "false results" is too strong:
  1. The authors explicitly analyzed success "across LLMs and game popularity", which is the correct control for memorization.
  2. For a *code-generation-from-spec* task, recognizing the structure is not illegitimate as long as the model implements the specified rules. The real failure mode is the model defaulting to the canonical rules when the spec deviates.
  3. That failure mode is precisely what the follow-up on variants (2511.05114) and rule-perturbation designs test.
  
  The better critique is that anonymization is a weak contamination control, and *rule mutation* (valid variants that break memorized implementations) is the strong one.

**Additional failure causes the lead missed**
1. It is a framework paper, not a benchmark: no fixed test set, no harness, no scoring script, no leaderboard.
2. Partial artifact release: evaluation outputs and evaluator absent. Nobody can reproduce or extend the numbers.
3. Playability and rule compliance appear to have been tested with human involvement (the abstract says "tested for playability and rule compliance"; the procedure was not verifiable here). That does not scale to new models.
4. Instant staleness: three 2025 models, no update path.
5. Visibility: a regional venue (SBGames) and a 2-star repo.
6. Overshadowed by better-resourced, verifiable work (DeepMind's Code World Models, ICLR 2026). [corrected by fact-check: "pre-emption" changed to "overshadowed", since CWM appeared after Boardwalk]

**Lesson:** A spec-to-program benchmark is a good *non-game-specific* idea: executable, verifiable, contamination-resistant through mutation. It needs (i) hundreds of procedurally mutated specs, (ii) automatic differential testing against a reference implementation, and (iii) a public harness. Boardwalk had none of these.

---

### 7. Grid-based game competitions (arXiv:2407.07796)

**Identity (verified)**
- Title: *Evaluating Large Language Models with Grid-Based Game Competitions: An Extensible LLM Benchmark and Leaderboard*.
- Authors: Oguzhan Topsakal, Colby Jacob Edell, Jackson Bailey Harper. arXiv 2024-07-11 (v2 exists). Sources: https://arxiv.org/abs/2407.07796 and the verbatim abstract in https://github.com/Luvata/arxive (pages/2024-07-11-cs-ai.html). Confidence: high.
- Journal version: *Evaluating the Performance of Large Language Models (LLMs) Through Grid-Based Game Competitions: An Extensible Benchmark and Leaderboard on the Path to Artificial General Intelligence (AGI)*, **The Journal of Cognitive Systems, Vol. 9, Issue 2, February 2025** (search result for https://dergipark.org.tr/en/pub/jcs/issue/89967/1611181). Confidence: medium-high. [fact-check note: an OpenAlex-derived screening file (harishsiravuri/scholarly-knowledge-lifecycle-review) lists this title in The Journal of Cognitive Systems with year 2025; a separate paper card (Li-Battery-dc/GameSurvey_workspace) says 2024. Volume 9, issue 2 and the February date were not independently confirmed.] The repo README says the work was "submitted to a leading IEEE journal". The version I could find is in a smaller journal.
- Predecessor by the same group: Topsakal & Harper, *Benchmarking Large Language Model (LLM) Performance for Game Playing via Tic-Tac-Toe*, **Electronics 2024, 13, 1532**, DOI 10.3390/electronics13081532. It covered 980 Tic-Tac-Toe games with list and illustration prompts. Confidence: high.
- Affiliation: not verified in this session.

**What it does** (verbatim abstract)
- Tic-Tac-Toe, Connect-Four and Gomoku.
- "we simulated 2,310 matches (5 sessions for each pair among 7 LLMs and a random player) across three types of games, using three distinct prompt types: list, illustration, and image".
- Models: Claude 3.5 Sonnet, Claude 3 Sonnet, Gemini 1.5 Pro, Gemini 1.5 Flash, GPT-4 Turbo, GPT-4o, Llama3-70B.
- Metrics: "win and disqualification rates, missed opportunity analysis, and invalid move analysis".
- "We also encourage submissions of results from other LLMs."
- Reported results (secondary summaries of the journal/arXiv text; confidence medium):
  - Invalid moves were low with list prompts in Tic-Tac-Toe and Connect-Four but rose with illustration and image prompts.
  - Gomoku showed "a notable increase in invalid moves and disqualifications" across prompt types.
  - Claude 3.5 Sonnet won 94.29% as first player and 25.71% as second player in Gomoku, with no disqualifications (dergipark PDF, via search summary). [corrected by fact-check: an independent extraction (pclark425.github.io, extraction-result-9262) places the 94.29% figure in the **list-prompt** condition; the 25.71% second-player figure was not independently confirmed. The same extraction reports Claude 3.5 Sonnet at 88.57% first-player wins in Tic-Tac-Toe (list), image-prompt Tic-Tac-Toe disqualification rates of 46.67% (first) and 53.33% (second), and GPT-4 Turbo averaging 13.49 invalid moves per game in illustration-prompt Connect-Four.]

**Adoption evidence**
- Repo https://github.com/research-outcome/LLM-Game-Benchmark: **25 stars, 3 forks, 381 commits**, created 2024-05-20. It has a web leaderboard at research-outcome.github.io/LLM-Game-Benchmark/leaderboard/ (README).
- **Commit history: the last model added was "gpt-4o-mini" on Jul 19, 2024, and the last commit of any kind was a README update on Dec 14, 2024** (commits page fetched 2026-09-29). The leaderboard has no o1/o3, R1, Claude 3.7+/4, Gemini 2.x or GPT-5 entries. **The invited community submissions never materialized.**
- Tic-Tac-Toe predecessor repo: 0 stars, last updated 2024-07-30.
- Citations exist but are thin. For example, GameArena (arXiv:2412.06394) cites it: the reference list in a mirrored copy of the paper includes "Topsakal ... arXiv:2407.07796". It also shows up in curated lists such as awesome-gameagent-papers (GitHub code search). No count was visible.

**Pre-emption and competing work**
- **GTBench** (arXiv:2402.12348, Feb 2024; NeurIPS 2024 proceedings) came 5 months earlier. It has 10 game-theoretic tasks including Tic-Tac-Toe, organized by a game-theoretic taxonomy, with competition-based LLM-vs-LLM evaluation. It found that "LLMs fail in complete-information and deterministic gaming yet remain competitive in probabilistic gaming". Sources: https://arxiv.org/abs/2402.12348, NeurIPS proceedings PDF. Confidence: high. GameBench (arXiv:2406.06613, June 2024) also preceded it. [corrected by fact-check: GTBench's 10 games include **Connect-4** as well as Tic-Tac-Toe (github.com/jinhaoduan/GTBench), which strengthens the pre-emption point. Authors: Duan, Zhang, Diffenderfer, Kailkhura, Sun, Stengel-Eskin, Bansal, Chen, Xu. GameBench (Costarelli et al.) appeared at the NeurIPS 2024 Language Gamification workshop.]
- Later and similar: LLM GameLab (ECML PKDD 2025, Springer LNCS), a platform with four TTT/Connect-Four-based games and illegal-move, win/draw/loss and latency tracking. The space was, and remains, crowded.
- **TTT-Bench** (arXiv:2506.10209; EMNLP 2025 main) uses four *novel* Tic-Tac-Toe-style games. Reasoning models "score on average 41% lower on TTT-Bench compared to MATH 500 and 5% lower compared to AIME 2024". Authors: Mishra, Liu, Wu, Yu, Liu, Barsoum. Sources: https://aclanthology.org/2025.emnlp-main.140/, https://arxiv.org/abs/2506.10209. Confidence: high.

**Assessment of the lead's critique** ("solved games, models max out instantly, too easy")
- **Correct that the games are solved.** Tic-Tac-Toe and Connect-Four have known perfect-play solutions, and the free-style Gomoku variant is also solved. This is general game-theory background, not sourced in this session.
- **Not supported that "models max out instantly".** The paper's own 2024 data show substantial invalid-move and disqualification rates, especially with illustration and image prompts and in Gomoku. TTT-Bench (2025) shows that *novel* TTT-style games still separate strong reasoning models from their math-benchmark scores.
- The more accurate critique is not that the games are too easy. It is this: solved games offer a perfect reference, and the benchmark did not use it as the yardstick. Scores were LLM-vs-LLM win rates against a changing pool plus a random player. That makes them non-transitive, pool-dependent, and not comparable across time. It also mixes perception/format parsing (image prompts) with strategic skill. A solver-referenced metric, such as a move-optimality rate or regret against perfect play, would have given an absolute, stable, saturating-but-interpretable score.

**Additional failure causes the lead missed**
1. **Leaderboard abandonment.** No updates after July 2024, just as reasoning models arrived. A benchmark whose leaderboard stops is dead regardless of design quality.
2. **Fragmented metrics:** 3 games x 3 prompt types x first/second player, with win rate, disqualifications and invalid moves. There is no single headline number or rating system like Elo or Bradley-Terry.
3. **Pre-emption:** GTBench, with a stronger theoretical framing and a NeurIPS venue, came first.
4. **Construct confound:** image and illustration prompts mostly measure board parsing rather than strategy.
5. **Low incremental validity** over general reasoning benchmarks at the time.
6. **Self-hosted, academic-group maintenance** with no institutional partner.

**Lesson:** When a task has a known optimum, score against the optimum, not against other models. And budget for maintenance: a leaderboard needs an automated pipeline to add new models within days of release.

---

### 8. TopoBench (arXiv:2603.12133)

**Identity (verified)**
- Title: *TopoBench: Benchmarking LLMs on Hard Topological Reasoning*.
- Authors: Mayug Maniparambil, Nils Hoehing, Janak Kapuriya, Arjun Karuvally, Ellen Rushe, Anthony Ventresque, Noel (E.) O'Connor, Fergal Reid. Submitted 2026-03-12. Sources: https://arxiv.org/abs/2603.12133, abstract mirrors on GitHub, and the first author's site source https://github.com/mayug/mayug.github.io (_posts/2026-05-27-topobench.markdown: `venue: "ICLR Workshop"`). Confidence: high.
- Venue: Workshop on Logical Reasoning of Large Language Models at ICLR 2026 (search results). Confidence: medium-high.
- Affiliations per a search summary: Intercom Research (Maniparambil, Reid), University College Dublin, University of Galway, Salk Institute, Dublin City University, Trinity College Dublin. Confidence: medium (secondary).

**What it does**
- Primary source: the project page source, https://github.com/topobench/topobench.github.io, index.html, fetched raw.
- Six puzzle families: Flow Free, Bridges, Loopy, Galaxies, Undead, Pattern. They test connectivity, loop closure, symmetry, reflection and contiguity.
- Three tiers. **900 instances, 50 per family-tier split**, 100k max output tokens.
- Per-family verifiers, "no partial credit", pass@1.
- Explicit design choice: "without falling back on external tools or code execution".
- Results:
  - "Average accuracy across the frontier trio falls from 0.58 on easy puzzles to 0.15 on hard puzzles".
  - Abstract: "even frontier models solve fewer than one quarter of hard instances, with two families nearly unsolved".
  - Search summary of the arXiv HTML: 9 reasoning LLMs (2 closed, 7 open). Best was **GPT-5-mini-high at 0.24 on hard**; best open-weight was **DeepSeek V3.2 at 0.10**. Confidence: medium. [fact-check: "nine frontier and open-weight LLMs" is confirmed by a second digest (memgrafter/research-digests), which also says "GPT-5 Mini and DeepSeek V3.2 solve <25% of hard instances". The 2-closed/7-open split and the 0.24 and 0.10 values could not be independently confirmed; the project page contains neither number. Treat them as single-source.]
- Diagnostics:
  - 750 chain-of-thought traces (DeepSeek V3.2) annotated with an error taxonomy through an LLM-as-judge pipeline.
  - Causal interventions that inject errors into gold-solution prefixes. "Premature commitment" and "constraint forgetting" hurt; "repeated reasoning is a benign effect of search".
  - Mitigations: cell-aligned integer/JSON encodings; a structured tool interface on hard Bridges raised DeepSeek V3.2 from 40% to 46-50% (project page). [corrected by fact-check: the project page lists four conditions: baseline 40%, structured-only 46%, structured + render 42%, full suite 50%. "46-50%" omits the 42% condition.]
  - Conclusion: "the bottleneck lies in extracting constraints from spatial representations and not in reasoning over them".

**Adoption evidence**
- **The code/data repository named in the abstract, https://github.com/mayug/topobench-benchmark, is empty.** GitHub shows "This repository is empty". It has 0 stars and 0 forks, and was created and last pushed 2026-03-12. Its only issue (#1, 2026-03-13, by NielsRogge) is titled "Release TopoBench on Hugging Face" and is still open. Checked 2026-09-29. Confidence: high.
- Project-page repo topobench/topobench.github.io: 0 stars, last updated 2026-03-18.
- **Name collision:** "TopoBench" is already the name of a well-established topological deep learning benchmarking library. That library is https://github.com/geometric-intelligence/topobench, **256 stars, 113 forks, created 2023-11-30, actively pushed as of 2026-09-29**, with paper arXiv:2406.06642 (*TopoBench: A Framework for Benchmarking Topological Deep Learning*). The confusion is observable in the wild: the YGN-SAGE README and methodology docs explicitly disambiguate "the TopoBench (arXiv 2603.12133) LLM puzzle benchmark" from other "Topo*Bench" artifacts. [corrected by fact-check: the YGN-SAGE README separates its own internal "sage-topo-bench" from "the UCL TopologyBench 2024 optical-network dataset" and from "the TopoBench (arXiv 2603.12133) LLM puzzle benchmark". It does **not** mention the geometric-intelligence TDL library. So it shows the general crowding of "Topo*Bench" names, not confusion with the TDL library specifically.] Searching for "TopoBench" surfaces the TDL library first (search results).
- Light citation and interest: a 2026 GSoC proposal in foss42/apidash cites TopoBench as motivation for diagnostic failure analysis (GitHub code search). No lab adoption was seen. Citation count: not visible.

**Competing and pre-existing work (the "nothing new" question)**
- **PUZZLES** (NeurIPS 2024 Datasets & Benchmarks) is built on Simon Tatham's Portable Puzzle Collection: 40 logic puzzles with adjustable difficulty, aimed at RL. The same puzzle source as TopoBench, including Loopy and Bridges. Repo: https://github.com/ETH-DISCO/rlp. [fact-check addition: arXiv:2407.00401; authors Estermann, Lanzendörfer, Niedermayr, Wattenhofer. The repo's puzzle list includes Loopy, Bridges, Galaxies, Undead and Pattern, so five of TopoBench's six families. Flow Free is not a Tatham puzzle (background knowledge, not checked in session).]
- **Enigmata** (arXiv:2505.19914, NeurIPS 2025): 36 puzzle tasks in 7 categories, each with a generator and a rule-based verifier. Its Enigmata-Eval has 4,758 instances across Easy/Medium/Hard. [fact-check: confirmed; NeurIPS 2025 Spotlight per first author's site]
- **Reasoning Gym** (arXiv:2505.24760): 100+ procedurally generated, verifiable reasoning environments including games and puzzles. [corrected by fact-check: venue is NeurIPS 2025 Spotlight per the official repo open-thought/reasoning-gym; authors Stojanovski, Stanley, Sharratt, Jones, Adefioye, Kaddour, Köpf]
- **MindTopo** (arXiv:2609.11900, Sep 2026): a competing topology benchmark for multimodal models. It has 11,030 instances, 13 task types and 14 MLLMs; the best model reaches 54.1% against a 97.4% human ceiling. [corrected by fact-check: full-text mirrors of arXiv:2609.11900 (ZhangCurosr/zhangcursor-papers-arxiv-cl-001 and -cv-001) report that the leading model, **GPT-5.6-Sol, reaches 61.42% (task-macro average) against observed human performance of 97.87%**, with human sample-micro accuracy of 97.49%. No source for 54.1% was found; the abstract itself gives no numbers. Authors: Ge, Liu, Wang, Garnica, Lyu, Wang, Tan, Gao, Zhang, Hong, Wu, Li (Northwestern, Microsoft Research, Stanford). MindTopo cites TopoBench in its related work.] It targets the same "topological reasoning" niche with far larger N and a human baseline.

**Assessment of the lead's critique** ("very simple, nothing new, many similar benchmarks exist")
- *"Very simple":* **Disagree.** Hard-tier accuracy of about 0.15-0.24 for frontier or near-frontier models, with two families nearly unsolved, is the opposite of simple. It has real headroom.
- *"Nothing new / many similar exist":* **Partially agree.** As a *task set* it is incremental: Tatham-style grid puzzles with verifiers already exist in PUZZLES, Enigmata and Reasoning Gym. The genuinely new contribution is *diagnostic*: the error taxonomy, causal interventions on gold prefixes, and the tokenization/cell-alignment finding. That is a scientific contribution, not a leaderboard contribution.
- *"Dead":* **Premature.** At about 6.5 months old, it had not had time to fail. But the empty repo is a strong negative signal that it will never be adopted as a benchmark.

**Additional failure causes the lead missed**
1. **Artifacts never released.** The empty repo makes independent evaluation impossible, and no benchmark survives that.
2. **Name collision** with a 256-star library hurts discoverability and citation attribution.
3. **Workshop venue** means low visibility.
4. **Model coverage:** the top closed model was GPT-5-mini (a small tier), with mostly open-weight models. Headline results therefore do not speak to flagship frontier models.
5. **Small N per cell:** 50 instances per family-tier gives a 95% binomial half-width of about ±12-14 pp per cell. Per-family comparisons are noisy, though hard-tier aggregates over 300 instances are about ±4-5 pp.
6. **No-tools design** limits ecological validity. The paper's own tool experiment shows structured state access helps, and a deployed model with code execution could call a SAT/CSP solver. So the headroom partly reflects an artificial restriction.
7. **Low incremental validity:** it is unclear what product-relevant capability the score predicts beyond other spatial and puzzle benchmarks.

**Lesson:** Ship the data and harness on day one, on a stable host such as HF Datasets plus GitHub. Pick a unique name. Include flagship models. Size cells for the comparisons you intend to make. Decide deliberately whether tools are allowed, or report both conditions.

---

### 9. From raw corpora to domain benchmarks (arXiv:2506.07658)

**Identity (verified)**
- Current title: *From Raw Corpora to Domain Benchmarks: Automated Evaluation of LLM Domain Expertise*. **v1 title (2025-06-09):** *Beyond Benchmarks: A Novel Framework for Domain-Specific LLM Evaluation and Knowledge Mapping*.
- Authors: Nitin Sharma, Thomas Wolfers, Çağatay Yıldız, of the University of Tübingen and University Hospital Tübingen (search summary; medium). [corrected by fact-check: per the v3 LaTeX source mirrored in aghado01/codex-scientiae, Sharma is at University Hospital Tübingen (Psychiatry and Psychotherapy), **Wolfers at Friedrich Schiller University Jena** (Laboratory for Mental Health Mapping), and Yıldız at the University of Tübingen (Cluster of Excellence Machine Learning for Science).]
- Replacement versions appear in arXiv listings dated 2026-02-26 and 2026-03-09 (Luvata/arxive "replace" entries). A search summary says v3 was released 2026-03-05.
- Sources: https://arxiv.org/abs/2506.07658; mirrors of the v1 abstract (CSQianDong/Awesome-arXiv-Daily-Reporter, 10-Jun-2025) and the v3 abstract (Luvata/arxive, 2026-03-09). Confidence: high.
- **Venue:** the first author's own site source, https://github.com/nsharma3150/nsharma3150.github.io (_pages/about_me.md, about.md), says an extended version is "currently under review at TMLR" (submitted January 2026). One search-engine summary claimed "accepted at ACL Main Conference 2025". **That claim is not supported.** It conflicts with the June 2025 first posting and with the author's own statement, so treat it as incorrect or unverified. Confidence that it is not published at a venue as of 2026-09-29: medium.

**What it does**
- A "deterministic pipeline that transforms raw domain corpora into completion-style benchmarks without relying on other LLMs or costly human annotation".
- Extract domain keywords with TF and TF-IDF, find sentences linked to them, and build prompt-target pairs where domain-specific words are the targets. Example from a secondary summary: "...involved the use of an Experience [Target: replay]".
- Metric: **rank of the correct first target token** in the model's predicted distribution, chosen over probability because "probabilities are not well-calibrated". Multi-token targets are scored sequentially (search summary of the paper; medium-high). [fact-check: confirmed from the v3 LaTeX: "we adopt prediction rank as our primary metric". The v3 aggregate is "the 20% trimmed mean of predicted ranks, discarding the lowest and highest 20% of values", not a plain median; a v1 digest describes a median rank.]
- Corpora: arXiv (1.56M documents) and M2D2 (8.5B tokens), per the first author's site.
- Models (v1 abstract): **GPT-2 medium/XL, Llama-2/3.1, OLMo-2, Qwen-2, Mistral**, all open-weight. [fact-check: the v3 LaTeX lists base models GPT-2 XL, Llama2-7B, Mistral-7B-v0.3, Qwen2-7B, Qwen2-1.5B and Llama3.1-8B, plus their six chat/instruction-tuned variants, with OLMo-2 checkpoints for pretraining tracking. All are open-weight, so the claim holds. v3 adds a base-vs-chat comparison across four domains (CS.AI, Physics, Biology, Economics) and reports an "alignment tax": instruction tuning generally degrades domain knowledge. Claude Sonnet 4 was used only to generate a comparison benchmark.]
- Validation: "model performances on our benchmark significantly correlate with those on an expert-curated benchmark". A search snippet gives **r = 0.91-0.99, p ≤ 0.012** (medium; the number of models behind the correlation is not verified). [corrected by fact-check: the v3 LaTeX gives **r = 0.99, p < 0.001** for the pipeline against an expert benchmark derived from the textbook *Understanding Deep Learning*, with **N = 6 base models**. The r = 0.91, p = 0.012 figure is for a **Claude-generated** comparison benchmark against the same expert benchmark, not for the authors' pipeline. So "0.91-0.99" conflates the method with its LLM-generated baseline. N = 6 is also a very small basis for a correlation claim.]
- v1 claims:
  - It beats perplexity as a measure of domain knowledge.
  - "domain adaptation happens rapidly in smaller models (within 500 steps)".
  - It can be used for early stopping.
  - Mechanistic finding: early-to-mid layers do attribute extraction, and forgetting begins in middle layers.

**Adoption evidence**
- No official code repository was found in search. Search surfaced only an unrelated "daisybio/domainbenchmark" protein-domain repo.
- It is referenced in the AI Alliance's *AI Application Testing* guide (https://github.com/The-AI-Alliance/ai-application-testing, docs/references.markdown) as "an alternative approach ... without using LLMs for generating data". That is a genuine, if modest, practitioner uptake signal.
- No leaderboard; no lab usage found. Citation count: not visible.

**Assessment of the lead's critique** ("figuring out the main words in some large body of text doesn't make an adept model")
- **Partially agree on construct.** A cloze-style rank of domain terms measures *domain lexical and factual knowledge encoded in the base model*. It does not measure expertise in the sense of applying knowledge, reasoning, or producing correct advice. Knowledge is necessary but not sufficient.
- **But the critique mis-describes the method and misses its purpose.** The pipeline does not ask models to "figure out main words". It asks them to predict held-out domain terms in real context sentences. It was built as a **cheap, LLM-free, contamination-resistant probe for base models during (continual) pretraining**, and the authors validated it against an expert-curated benchmark. For that narrow job (tracking domain knowledge acquisition and forgetting during training) it is well-motivated. It is a training diagnostic, not a public capability leaderboard.

**Additional failure causes as a public benchmark**
1. **Needs logit/token-rank access.** This is my interpretation: rank-of-target needs the full or near-full next-token distribution, which major closed chat APIs do not expose. The paper's model list being entirely open-weight fits that. **A benchmark that cannot score the frontier models people care about cannot become a headline leaderboard.**
2. **Unintuitive metric:** "median rank of target token" is hard to explain to consumers and hard to compare across tokenizers. Rank depends on vocabulary and tokenization, which is a cross-model comparability issue (my inference).
3. **Old and small model roster** (GPT-2, Llama-2 era) signals "research probe" rather than "frontier benchmark". [fact-check: still true in v3, where every evaluated model is 8B parameters or smaller and open-weight, although v3 adds chat variants]
4. **No released code or dataset found**, and no fixed versioned test set: by design it regenerates from new corpora, which helps contamination but hurts leaderboard stability.
5. **Retitling mid-life** splits citations and discoverability.
6. **Not yet peer-reviewed** (under review at TMLR, per the author).
7. Single-reference targets penalize valid synonyms. The authors argue averaging keeps ranks stable (search summary), but it remains a validity threat for chat models that paraphrase.

**Lesson:** Its *good* design choices are worth copying: deterministic, LLM-free item generation from fresh corpora; contamination resistance through recency; and **explicit external validation against an expert benchmark**. Its fatal choice for public adoption was a white-box metric. A new benchmark should be black-box scorable (text in, text out) so closed frontier models can be evaluated.

---

### 10. Bloom's-taxonomy guideline benchmarks / BloomQA (arXiv:2601.20253)

**Identity (verified)**
- Title: *Automated Benchmark Generation from Domain Guidelines Informed by Bloom's Taxonomy*.
- Authors: Si Chen, Le Huy Khiem, Annalisa Szymanski, Ronald Metoyer, Ting Hua, Nitesh V. Chawla. arXiv listing 2026-01-29, cs.CL/cs.AI.
- Sources: https://arxiv.org/abs/2601.20253 and verbatim abstract mirrors (2shin0/arxiv-ai-mailing LLM/2026-01-29.md; CSQianDong/Awesome-arXiv-Daily-Reporter 29-Jan-2026). Confidence: high.
- An OpenReview submission titled "BloomQA: Automated Benchmark Generation from Domain Guidelines ..." exists (https://openreview.net/forum?id=jwJkPowRTl, seen in search results). The venue and decision could not be verified. [fact-check addition: a third-party harvest of public ICLR OpenReview data (KentoNishi/cs2760-ethics, 2026 ethics-flag CSV) lists forum jwJkPowRTl under the full title "BloomQA: Automated Benchmark Generation from Domain Guidelines **Using** Bloom's Taxonomy", with the same six authors, keywords "Bloom's Taxonomy; Food AI; Pedagogy AI", ethics flags for responsible research practice (data release) and bias, and **no decision recorded**. That suggests an ICLR 2026 submission that was not accepted, possibly withdrawn (inference, unverified).]
- Affiliation not verified in session.

**What it does** (verbatim abstract)
- "a framework for automated benchmark generation from expert-authored guidelines informed by Bloom's Taxonomy. It converts expert practices into implicit violation-based scenarios and expands them into auto-graded multiple-choice questions (MCQs) and multi-turn dialogues across four cognitive levels, enabling deterministic, reproducible, and scalable evaluation."
- Domains: "teaching, dietetics, and caregiving".
- Finding: "LLMs sometimes perform relatively better on higher-order reasoning (Analyze) but fail more frequently on lower-level items (Remember)".
- Claims "large-scale, psychometrically informed benchmarks".
- From a secondary, AI-generated digest (https://github.com/memgrafter/research-digests, ml_research_analysis_2026/2601.20253_...md); confidence medium:
  - "60,000+ MCQs and 15,000+ dialogues", "over 75,000 assessment items".
  - "LLM-assisted extraction of best practices".
  - "60-97% of practices showing significant separation between model families".
  - Fine-tuned models gained about 20% in teaching.
  - The item count matches the lead's "60k+".

**Adoption evidence**
- No official code or data repo found in GitHub code search (34 hits, all digests or feeds). No leaderboard; no lab use; citation count not visible. The paper is about 8 months old.

**Assessment of the lead's critique** ("AI-generated scenarios lead to an echo chamber; 60k+ items isn't solving scale and makes vetting harder")
- *Echo chamber:* **Partially agree.** When an LLM expands scenarios into items, generator biases can shape item content, distractors and "correct" keys. If evaluated models share training data or families with the generator, scores can reflect stylistic agreement rather than competence. That is a well-known concern with LLM-generated evaluation data (general knowledge; not sourced in this session). Two mitigations the paper does have: **grounding in expert-authored guidelines** (the practice list comes from domain experts, not the LLM) and **auto-graded MCQs** (no LLM judge at scoring time). So it is not a pure echo chamber. The residual risk sits in item generation and answer keys.
- *Scale:* **Partially disagree.** Large N is not pointless here. It enables per-practice significance testing, and the reported per-practice model separation depends on it. **Agree on vetting:** 75k generated items cannot be expert-reviewed exhaustively. Without a reported audited sample and error rate, item validity is unknown. I could not verify whether the paper reports such an audit.
- The **headline finding may be an artifact.** "Better at Analyze than Remember" is counter-intuitive. If Bloom levels and difficulty were *assigned by the generator* rather than *empirically calibrated* (for example with IRT on human responses), the inversion could reflect miscalibrated labels, not model cognition. This is my interpretation and should be tested before being cited as a finding.

**Additional failure causes**
1. MCQ format re-imports known MCQ biases, the very problem item 9's authors cite as motivation.
2. Niche practice domains (teaching, dietetics, caregiving) matter socially but have weak pull for frontier-lab leaderboards.
3. No public release found.
4. No human performance baseline visible.
5. Generated benchmarks are easy to *regenerate*, which lowers their value as a *fixed* shared yardstick unless a canonical frozen version is published.

**Lesson:** Keep the good part (expert-document grounding plus deterministic auto-grading) and fix the weak part. Use multi-family generators, exclude evaluated model families from generation, publish an expert-audited random sample with an error rate, prune items by empirical IRT statistics, and ship a frozen canonical split.

---

### Cross-cutting synthesis: why these five did not become benchmarks people use

| Failure cause | Boardwalk | Grid games | TopoBench | Raw corpora | BloomQA |
|---|---|---|---|---|---|
| Not designed as a leaderboard (framework/diagnostic) | **Yes** | No | Partly (diagnostic focus) | **Yes** (training probe) | Partly (generator framework) |
| Artifacts missing/partial | **Yes** (no evaluator/outputs) | No (open) | **Yes** (empty repo) | **Yes** (no code found) | **Yes** (none found) |
| Leaderboard not maintained / none | None | **Frozen since 2024** | None | None | None |
| Frontier closed models excluded or under-covered | Yes (3 older models) | Stale | **Yes** (GPT-5-mini top) | **Yes** (white-box metric) | Unknown |
| Small N / no uncertainty | **Yes** | Moderate | Moderate (50/cell) | Unknown | No (very large N) |
| Pool-relative or fragmented scores | No | **Yes** | No | No | No |
| Construct validity concern | Anonymization weak | Perception vs strategy confound | No-tools artificiality | Knowledge ≠ expertise | Generated labels/keys |
| Discoverability (name/venue/retitle) | Regional venue | Minor journal | **Name collision**, workshop | **Retitled**, unreviewed | Unknown venue |
| Pre-empted / outcompeted | **DeepMind CWM** (outcompeted after the fact; earlier: From Code to Play) [corrected by fact-check] | **GTBench** | Enigmata, Reasoning Gym, MindTopo | none found | none found |
| Headroom | yes | yes (in 2024) | **yes** | n/a | yes (claimed separation) |

Note that **lack of headroom was not the killer for any of these five.** The lead's "too easy" and "too simple" framing mostly does not hold. What killed or stalled them is the combination of no maintained public leaderboard, incomplete artifacts, frontier-model exclusion, and weak discoverability. Where there was a construct problem, it was specific and fixable rather than fatal.

---

## Implications for designing a new benchmark

These are for the non-game benchmark this project will propose.

1. **Ship a product, not a paper.** On day one release a frozen, versioned test split; a one-command harness (pip-installable, no heavy environment); a public leaderboard; and an automated pipeline to add new models within days of release. Grid-games died when its leaderboard froze. TopoBench's empty repo guarantees non-adoption.
2. **Black-box scorable.** Use text-in/text-out scoring only, never logits or token ranks, so closed frontier models (GPT-5-class, Claude, Gemini) can be evaluated. Item 9's white-box metric excluded exactly the models people care about.
3. **One headline number plus diagnostic sub-scores.** Report a single aggregate on an interpretable scale, plus per-skill diagnostics. Avoid grid-games' matrix of game x prompt x seat x metric.
4. **Absolute, reference-anchored scoring.** Score against a verifiable ground truth or optimum, not against a pool of other models. If pairwise comparison is used, fit a proper rating model (Bradley-Terry/Elo) with confidence intervals.
5. **Contamination resistance through mutation, not renaming.** Surface anonymization (Boardwalk) is weak. Use procedurally generated or mutated instances whose correct answer *changes* when the rules change, plus private held-out seeds and periodic refresh. Keep a canonical frozen split for comparability.
6. **Statistical power by design.** Size each reported cell for the effect sizes you care about. 50 items per cell gives about ±14 pp, too wide for model-vs-model claims. Report bootstrap CIs and consider IRT-based item selection.
7. **Explicit construct and external validation.** State what the score should predict (a real-world task outcome) and validate against an external criterion, as item 9 did with an expert benchmark. That was item 9's best practice.
8. **If items are LLM-generated:** ground them in expert or primary documents. Use multiple generator families and exclude evaluated families from generation. Grade deterministically. Publish an expert-audited random sample with a measured error rate. Calibrate difficulty *empirically* (IRT) rather than by assigned labels.
9. **Tool policy is a design decision.** Either allow tools (more realistic) or forbid them (purer construct), justify the choice, and ideally report both. TopoBench's headroom partly came from forbidding tools.
10. **Discoverability:** pick a unique, searchable name (check GitHub, HF and arXiv for collisions). Do not retitle after release. Aim for a main-track venue or a partnership with an established leaderboard host.
11. **Beat the pre-emption risk:** survey competing work (GTBench pre-empted grid-games, DeepMind's CWM overshadowed Boardwalk) and articulate the *unique* measurement the new benchmark adds (incremental validity).
12. **A promising non-game idea from this set:** "spec-to-executable" tasks (Boardwalk and CWM generalized beyond games). Examples: natural-language regulations, protocols or business rules turned into executable checkers, verified by differential testing against hidden reference implementations and rule mutations. This combines verifiability, contamination resistance and real-world relevance.

---

## Claims ledger

Confidence: H = high (primary or verbatim source), M = medium (secondary summary or single search snippet), L = low.

1. **Boardwalk identity and results.** Boardwalk (arXiv:2508.16447), by Becker, Bauer de Oliveira, Rossato and Tavares, tasked three LLMs (Claude, DeepSeek, ChatGPT) with coding 12 anonymized popular and obscure board games free-form and within the Boardwalk API. The best, Claude 3.7 Sonnet, produced 55.6% of games without errors. Sources: https://arxiv.org/abs/2508.16447; https://github.com/LIHUA919/AI-Agents-Daily-Research (data/2025-08-25.md). **H**
2. **Boardwalk venue.** Boardwalk appeared at SBGames 2025. Sources: https://sol.sbc.org.br/index.php/sbgames/article/view/37375 (search result); DOI 10.5753/sbgames.2025.10222 via https://github.com/zsyverse/game-ai-benchmarks-papers. **H** (venue) / **M** (DOI)
3. **Boardwalk repo.** The official repo (LabCRAIG/boardwalk) has 2 stars, 0 forks and 24 commits, and contains the API but no LLM evaluation outputs or evaluator (as of 2026-09-29). Sources: https://github.com/LabCRAIG/boardwalk; https://github.com/zsyverse/game-ai-benchmarks-papers. **H**
4. **Boardwalk stated goal.** Boardwalk's abstract frames the goal as creating a framework to make board-game elaboration more accessible, not as a model-ranking benchmark. Source: https://github.com/LIHUA919/AI-Agents-Daily-Research (verbatim abstract). **H**
5. **Code World Models.** Google DeepMind's *Code World Models for General Game Playing* (arXiv:2510.04542) has LLMs translate natural-language rules and trajectories into OpenSpiel-API Python world models used by MCTS. It is marked as an ICLR 2026 conference paper. Sources: https://arxiv.org/abs/2510.04542; https://openreview.net/pdf?id=1UoB7IWiku. **M-H**
6. **Grid-games setup.** Topsakal, Edell and Harper (arXiv:2407.07796) simulated 2,310 matches (5 sessions per pair among 7 LLMs and a random player) across Tic-Tac-Toe, Connect-Four and Gomoku using list, illustration and image prompts. Sources: https://arxiv.org/abs/2407.07796; https://github.com/Luvata/arxive (pages/2024-07-11-cs-ai.html). **H**
7. **Grid-games journal version.** A version appeared in The Journal of Cognitive Systems 9(2), Feb 2025. Source: https://dergipark.org.tr/en/pub/jcs/issue/89967/1611181 (search result). **M-H**
8. **Grid-games leaderboard frozen.** The repo's last model addition was gpt-4o-mini (Jul 19, 2024) and its last commit was Dec 14, 2024. It has 25 stars and 3 forks. Sources: https://github.com/research-outcome/LLM-Game-Benchmark/commits/main; https://github.com/research-outcome/LLM-Game-Benchmark. **H**
9. **Grid-games did not saturate.** In the grid-games study, invalid moves rose with illustration and image prompts and in Connect-Four and Gomoku, and Gomoku saw more disqualifications. Models did not saturate the games. Sources: https://arxiv.org/abs/2407.07796; https://dergipark.org.tr/en/download/article-file/4483558 (search summaries). **M**
10. **Grid-games Gomoku result.** Claude 3.5 Sonnet won 94.29% of Gomoku games as first player and 25.71% as second, with no disqualifications. Source: https://dergipark.org.tr/en/download/article-file/4483558 (search summary). **M** [corrected by fact-check: 94.29% is the **list-prompt** condition (independent extraction at pclark425.github.io); 25.71% is single-source and unconfirmed]
11. **GTBench pre-empted grid-games.** GTBench (arXiv:2402.12348, NeurIPS 2024) provided 10 game-theoretic tasks including Tic-Tac-Toe with LLM-vs-LLM competition, 5 months before the grid-games paper. Sources: https://arxiv.org/abs/2402.12348; https://proceedings.neurips.cc/paper_files/paper/2024/file/3191170938b6102e5c203b036b7c16dd-Paper-Conference.pdf. **H**
12. **TTT-Bench.** TTT-Bench (arXiv:2506.10209, EMNLP 2025) found reasoning models score on average 41% lower on novel TTT-style games than on MATH 500. Sources: https://aclanthology.org/2025.emnlp-main.140/; https://arxiv.org/abs/2506.10209. **H**
13. **TopoBench design.** TopoBench (arXiv:2603.12133; ICLR 2026 LLM logical reasoning workshop) has 6 puzzle families x 3 tiers, 900 instances (50 per split), pass@1, no partial credit, and no tools or code execution. Sources: https://github.com/topobench/topobench.github.io (index.html); https://arxiv.org/abs/2603.12133; https://github.com/mayug/mayug.github.io. **H**
14. **TopoBench results.** Frontier-trio mean accuracy on TopoBench is 0.58 easy, 0.38 medium and 0.15 hard. Frontier models solve fewer than a quarter of hard instances. The best model, GPT-5-mini-high, scores 0.24 on hard and the best open model, DeepSeek V3.2, scores 0.10. Sources: https://github.com/topobench/topobench.github.io; https://arxiv.org/abs/2603.12133; https://arxiv.org/html/2603.12133 (search summary). **H** (first two) / **M** (0.24 and 0.10) [fact-check: the 0.24 and 0.10 values remain single-source and unverified]
15. **TopoBench repo empty.** TopoBench's advertised code/data repo, mayug/topobench-benchmark, is empty ("This repository is empty") with 0 stars. Its only issue asks for a Hugging Face release (as of 2026-09-29). Sources: https://github.com/mayug/topobench-benchmark; https://github.com/mayug/topobench-benchmark/issues. **H**
16. **TopoBench name collision.** The name "TopoBench" collides with the topological deep learning library geometric-intelligence/topobench (256 stars, created 2023-11-30; arXiv:2406.06642). Sources: https://github.com/geometric-intelligence/topobench; https://arxiv.org/abs/2406.06642. **H**
17. **Crowded puzzle space.** Prior puzzle benchmarks include Enigmata (arXiv:2505.19914, NeurIPS 2025: 36 tasks in 7 categories, Enigmata-Eval with 4,758 instances), Reasoning Gym (arXiv:2505.24760: 100+ procedurally generated environments; NeurIPS 2025 Spotlight [corrected by fact-check]) and PUZZLES (arXiv:2407.00401; NeurIPS 2024 D&B: 40 Tatham puzzles). Sources: https://arxiv.org/pdf/2505.19914; https://neurips.cc/virtual/2025/poster/116805; https://arxiv.org/pdf/2505.24760; https://proceedings.neurips.cc/paper_files/paper/2024/file/e5d1eaadeed651ba1021c09149db4b92-Paper-Datasets_and_Benchmarks_Track.pdf. **H**
18. **MindTopo.** MindTopo (arXiv:2609.11900, Sep 2026) is a competing topology benchmark with 11,030 instances, 13 task types and 14 MLLMs. The best model scores 54.1% against a 97.4% human ceiling. Source: https://arxiv.org/abs/2609.11900. **M-H** [corrected by fact-check: the best model, GPT-5.6-Sol, scores **61.42%** (task-macro average) against **97.87%** observed human performance (human sample-micro accuracy 97.49%), per full-text mirrors in ZhangCurosr/zhangcursor-papers-arxiv-cl-001 and -cv-001, corroborated by TonyLeng1314/paper-brief. No source for 54.1% was found.]
19. **Raw-corpora method.** arXiv:2506.07658 (Sharma, Wolfers, Yıldız; v1 titled "Beyond Benchmarks: ...") builds completion benchmarks from raw corpora with TF/TF-IDF keyword targets. It scores by the rank of the target token and evaluated GPT-2 medium/XL, Llama-2/3.1, OLMo-2, Qwen-2 and Mistral. Sources: https://arxiv.org/abs/2506.07658; https://github.com/CSQianDong/Awesome-arXiv-Daily-Reporter (10-Jun-2025/NLP/README.md); https://github.com/Luvata/arxive (pages/2026-03-09-cs-cl.html). **H**
20. **Raw-corpora validation.** The benchmark correlates with an expert-curated benchmark at r = 0.91-0.99 (p ≤ 0.012). Source: https://arxiv.org/abs/2506.07658 (search summary). **M** [corrected by fact-check: the pipeline scores **r = 0.99, p < 0.001, N = 6 base models**. r = 0.91, p = 0.012 belongs to a Claude-generated comparison benchmark. Source: v3 LaTeX mirrored at https://github.com/aghado01/codex-scientiae (supellex/gauntlet/ai-eval/2506.07658v3). **H**]
21. **Raw-corpora venue status.** As of the first author's site, an extended version of arXiv:2506.07658 was under review at TMLR, having been submitted January 2026. It used arXiv (1.56M docs) and M2D2 (8.5B tokens) corpora. A search-summary claim of "ACL 2025" acceptance is unsupported. Source: https://github.com/nsharma3150/nsharma3150.github.io (_pages/about_me.md, about.md). **M-H**
22. **BloomQA method.** arXiv:2601.20253 (Chen, Khiem, Szymanski, Metoyer, Hua, Chawla) converts expert guidelines into violation-based scenarios expanded into auto-graded MCQs and multi-turn dialogues across four Bloom levels. It covers teaching, dietetics and caregiving, and reports that LLMs sometimes do better on Analyze than on Remember items. Sources: https://arxiv.org/abs/2601.20253; https://github.com/2shin0/arxiv-ai-mailing (LLM/2026-01-29.md). **H**
23. **BloomQA scale.** BloomQA generated 60,000+ MCQs and 15,000+ dialogues (75,000+ items) with LLM-assisted practice extraction. Source: https://github.com/memgrafter/research-digests (secondary AI digest). **M**
24. **No citation counts.** Citation counts for all five papers could not be observed in this session. Status: unverified.

---

## References

(All seen during this session; the URL where each was seen is in the JSON file `research/refs/user_failed_b.json`.)

1. Becker, Á. G., Bauer de Oliveira, G., Rossato, L. B., Tavares, A. R. (2025). *Boardwalk: Towards a Framework for Creating Board Games with LLMs.* SBGames 2025; arXiv:2508.16447. https://arxiv.org/abs/2508.16447
2. LabCRAIG. *boardwalk* (GitHub repository). https://github.com/LabCRAIG/boardwalk
3. Becker, Á. G., Rossato, L. B., Tavares, A. R. (2025). *Usando LLMs para Programar Jogos de Tabuleiro e Variações.* arXiv:2511.05114. https://arxiv.org/abs/2511.05114
4. Lehrach, W., Hennes, D., Lazaro-Gredilla, M., Lou, X., Wendelken, C., Li, Z., Dedieu, A., Grau-Moya, J., Lanctot, M., Iscen, A., Schultz, J., Chiam, M., Gemp, I., Zielinski, P., Singh, S., Murphy, K. P. (2025). *Code World Models for General Game Playing.* arXiv:2510.04542; ICLR 2026. https://arxiv.org/abs/2510.04542 [fact-check: full author list added from BibTeX in Eurekaleo/awesome-ai-for-games]
5. Eberhardinger, M., Goodman, J., Dockhorn, A., Perez-Liebana, D., Gaina, R. D., Çakmak, D., Maghsudi, S., Lucas, S. (2024). *From Code to Play: Benchmarking Program Search for Games Using Large Language Models.* arXiv:2412.04057 (IEEE version exists). https://arxiv.org/abs/2412.04057 [corrected by fact-check: full title and authors]
6. Topsakal, O., Edell, C. J., Harper, J. B. (2024). *Evaluating Large Language Models with Grid-Based Game Competitions: An Extensible LLM Benchmark and Leaderboard.* arXiv:2407.07796. https://arxiv.org/abs/2407.07796
7. Topsakal, O., Edell, C., Harper, J. (2025). *Evaluating the Performance of Large Language Models (LLMs) Through Grid-Based Game Competitions: An Extensible Benchmark and Leaderboard on the Path to Artificial General Intelligence (AGI).* The Journal of Cognitive Systems 9(2). https://dergipark.org.tr/en/pub/jcs/issue/89967/1611181
8. Topsakal, O., Harper, J. B. (2024). *Benchmarking Large Language Model (LLM) Performance for Game Playing via Tic-Tac-Toe.* Electronics 13, 1532. https://doi.org/10.3390/electronics13081532
9. research-outcome. *LLM-Game-Benchmark* (GitHub repository and leaderboard). https://github.com/research-outcome/LLM-Game-Benchmark
10. Duan, J., Zhang, R., Diffenderfer, J., Kailkhura, B., Sun, L., Stengel-Eskin, E., Bansal, M., Chen, T., Xu, K. (2024). *GTBench: Uncovering the Strategic Reasoning Limitations of LLMs via Game-Theoretic Evaluations.* arXiv:2402.12348; NeurIPS 2024. https://arxiv.org/abs/2402.12348
11. Costarelli, A., et al. (2024). *GameBench: Evaluating Strategic Reasoning Abilities of LLM Agents.* arXiv:2406.06613; Language Gamification Workshop, NeurIPS 2024. https://arxiv.org/abs/2406.06613
12. Mishra, P., Liu, J., Wu, J., Yu, X., Liu, Z., Barsoum, E. (2025). *TTT-Bench: A Benchmark for Evaluating Reasoning Ability with Simple and Novel Tic-Tac-Toe-style Games.* EMNLP 2025; arXiv:2506.10209. https://aclanthology.org/2025.emnlp-main.140/
13. *GameArena: Evaluating LLM Reasoning through Live Computer Games.* arXiv:2412.06394. https://arxiv.org/abs/2412.06394
14. Morillo, P., et al. (2025). *LLM GameLab: An Interactive Platform for Testing Large Language Models in Board Games.* ECML PKDD 2025, Springer LNCS. https://link.springer.com/chapter/10.1007/978-3-032-06129-4_36 [fact-check: full title and first author from morningD/lang.csconf ECML-PKDD 2025 data; DOI not independently confirmed]
15. Maniparambil, M., Hoehing, N., Kapuriya, J., Karuvally, A., Rushe, E., Ventresque, A., O'Connor, N., Reid, F. (2026). *TopoBench: Benchmarking LLMs on Hard Topological Reasoning.* ICLR 2026 Workshop on Logical Reasoning of LLMs; arXiv:2603.12133. https://arxiv.org/abs/2603.12133
16. TopoBench project page source. https://github.com/topobench/topobench.github.io (site: https://topobench.github.io/)
17. mayug. *topobench-benchmark* (empty GitHub repository). https://github.com/mayug/topobench-benchmark
18. Telyatnikov, L., Bernardez, G., Montagna, M., Vasylenko, P., Zamzmi, G., Hajij, M., Schaub, M. T., Miolane, N., Scardapane, S., Papamarkou, T. (2024). *TopoBench: A Framework for Benchmarking Topological Deep Learning.* arXiv:2406.06642; repo https://github.com/geometric-intelligence/topobench
19. Estermann, B., Lanzendörfer, L. A., Niedermayr, Y., Wattenhofer, R. (2024). *PUZZLES: A Benchmark for Neural Algorithmic Reasoning.* NeurIPS 2024 Datasets & Benchmarks; arXiv:2407.00401. https://proceedings.neurips.cc/paper_files/paper/2024/file/e5d1eaadeed651ba1021c09149db4b92-Paper-Datasets_and_Benchmarks_Track.pdf ; repo https://github.com/ETH-DISCO/rlp
20. Chen, J., He, Q., Yuan, S., Chen, A., Cai, Z., Dai, W., Yu, H., Chen, J., Li, X., Yu, Q., Zhou, H., Wang, M. (2025). *Enigmata: Scaling Logical Reasoning in Large Language Models with Synthetic Verifiable Puzzles.* arXiv:2505.19914; NeurIPS 2025 (Spotlight). https://arxiv.org/abs/2505.19914
21. Stojanovski, Z., Stanley, O., Sharratt, J., Jones, R., Adefioye, A., Kaddour, J., Köpf, A. (2025). *Reasoning Gym: Reasoning Environments for Reinforcement Learning with Verifiable Rewards.* arXiv:2505.24760; NeurIPS 2025 (Spotlight). https://arxiv.org/abs/2505.24760 [corrected by fact-check: venue added]
22. Ge, Y., Liu, A., Wang, Q., Garnica, J., Lyu, J., Wang, Z., Tan, R., Gao, J., Zhang, R., Hong, Y., Wu, J., Li, M. (2026). *MindTopo: Can Foundation Models Reason in Topological Space?* arXiv:2609.11900 (preprint). https://arxiv.org/abs/2609.11900
23. Sharma, N., Wolfers, T., Yıldız, Ç. (2025/2026). *From Raw Corpora to Domain Benchmarks: Automated Evaluation of LLM Domain Expertise* (v1: *Beyond Benchmarks: A Novel Framework for Domain-Specific LLM Evaluation and Knowledge Mapping*). arXiv:2506.07658. https://arxiv.org/abs/2506.07658
24. Sharma, N. Personal site source (status: under review at TMLR; corpora sizes). https://github.com/nsharma3150/nsharma3150.github.io
25. The AI Alliance. *AI Application Testing* guide, references page. https://github.com/The-AI-Alliance/ai-application-testing
26. Chen, S., Khiem, L. H., Szymanski, A., Metoyer, R., Hua, T., Chawla, N. V. (2026). *Automated Benchmark Generation from Domain Guidelines Informed by Bloom's Taxonomy.* arXiv:2601.20253. https://arxiv.org/abs/2601.20253
27. Chen, S., Khiem, L. H., Szymanski, A., Metoyer, R., Hua, T., Chawla, N. V. *BloomQA: Automated Benchmark Generation from Domain Guidelines Using Bloom's Taxonomy.* OpenReview submission (ICLR 2026 per a third-party harvest of ICLR data; no decision recorded). https://openreview.net/forum?id=jwJkPowRTl
28. memgrafter. *research-digests*: AI-generated digests of 2601.20253 and 2603.12133 (secondary). https://github.com/memgrafter/research-digests
29. zsyverse. *game-ai-benchmarks-papers*: catalog with artifact-availability audit (secondary). https://github.com/zsyverse/game-ai-benchmarks-papers
30. Aguilar Martín, J. (2026). *When a Verified World Model Still Loses: Play-Adequacy vs Prediction-Accuracy in LLM-Synthesized Code World Models.* arXiv:2607.14169. https://arxiv.org/abs/2607.14169 [fact-check: author added]
30b. *World-Time Compute with Verified Code World Models.* arXiv:2609.09163 (quome-cloud/openworld). https://arxiv.org/abs/2609.09163 [fact-check addition: cited in the text but missing from the reference list]
31. yannabadie. *YGN-SAGE* README (TopoBench name disambiguation). https://github.com/yannabadie/YGN-SAGE
32. foss42. *apidash* GSoC 2026 proposal citing TopoBench. https://github.com/foss42/apidash
33. Cody-Jiang-Zhihong. *DesignVoyager* (bundles Boardwalk). https://github.com/Cody-Jiang-Zhihong/DesignVoyager

---

## Verification log

Adversarial fact-check run on 2026-09-29. **Method and limits:** this session's WebSearch budget was already used up (200/200), and arXiv, OpenReview, Semantic Scholar and similar domains are blocked for fetching. Every check below was therefore done independently through GitHub code and repository search, plus WebFetch of github.com and raw.githubusercontent.com. The main sources were:

- verbatim arXiv abstract mirrors: Luvata/arxive, CSQianDong/Awesome-arXiv-Daily-Reporter, wwd29/arxiv-daily, LIHUA919/AI-Agents-Daily-Research, 2shin0/arxiv-ai-mailing;
- full-text or LaTeX mirrors: ZhangCurosr/* for MindTopo, aghado01/codex-scientiae for the 2506.07658 v3 LaTeX;
- official repos and live GitHub API metadata.

Where the only available evidence was the same secondary source the dossier had used, the verdict is "unverifiable".

| Claim | Verdict | Evidence | Sources |
|---|---|---|---|
| C1 Boardwalk identity and results | **Confirmed** | Verbatim abstract: "three state-of-the-art LLMs (Claude, DeepSeek and ChatGPT) ... 12 popular and obscure games in free-form and within Boardwalk ... We anonymize the games ... Claude 3.7 Sonnet, yielding 55.6% of games without any errors ... making the elaboration of board games more accessible." Authors match. The SBGames 2025 venue is supported by two independent third-party files: zsyverse gives DOI 10.5753/sbgames.2025.10222, and KristjanSolvi/BoardGameGenerator links sol.sbc.org.br article 37375. | https://github.com/wwd29/arxiv-daily (html/user_3/2025-08-25.html); https://github.com/zsyverse/game-ai-benchmarks-papers; https://github.com/KristjanSolvi/BoardGameGenerator |
| C2 Boardwalk repo | **Confirmed** | GitHub API: 2 stars, 0 forks, created 2025-04-22, pushed 2026-01-16, updated 2026-04-06. Commits page: 24 commits (Apr to Nov 2025), with examples such as Tic-Tac-Toe, Sudoku and Mastermind. Top level holds only `Examples/`, `README.md` and `boardwalk.py`, with no evaluation outputs or evaluator. The README does not cite the paper, but DesignVoyager's bundled copy links the paper to this repo. | https://github.com/LabCRAIG/boardwalk; https://github.com/Cody-Jiang-Zhihong/DesignVoyager |
| C3 Code World Models | **Confirmed** (framing corrected) | An LLM (Gemini 2.5 Pro) translates rules plus a few trajectories into executable Python that follows the OpenSpiel API, and MCTS/ISMCTS plans with it. It is from Google DeepMind, arXiv v1 dated 6 Oct 2025, and ICLR 2026 per several independent lists and a BibTeX entry. **Correction:** it came after Boardwalk, so "pre-empted" was changed to "overshadowed". | https://github.com/zhaoyang97/Paper-Notes (docs/ICLR2026/...); https://github.com/Eurekaleo/awesome-ai-for-games (data/paper-references.bib); https://github.com/katopz/katgpt-rs (.research/275_...) |
| C4 Grid-games setup | **Confirmed** | Verbatim abstract: "2,310 matches (5 sessions for each pair among 7 LLMs and a random player) ... list, illustration, and image". Authors match; the repo README cites arXiv:2407.07796. | https://github.com/Luvata/arxive (pages/2024-07-11-cs-ai.html); https://github.com/research-outcome/LLM-Game-Benchmark |
| C5 Grid-games leaderboard frozen | **Confirmed** | GitHub API: 25 stars, 3 forks, pushed_at 2024-12-14, 381 commits. Commit list: "Added gpt-4o-mini" on Jul 19 2024, then only README, FAQ and error-message commits to Jul 31 2024, and a README update on Dec 14 2024. | https://github.com/research-outcome/LLM-Game-Benchmark/commits/main |
| C6 Grid games not saturated; Gomoku numbers | **Corrected (minor)** | An independent extraction confirms invalid moves and disqualifications rising from list to illustration to image prompts in all three games. The 94.29% Gomoku first-player figure is the **list-prompt** condition. 25.71% (second player) was **not** independently confirmed. | https://github.com/pclark425/pclark425.github.io (html_output-2025-12-03-ad/results/extraction-result-9262.html) |
| C7 GTBench and TTT-Bench | **Confirmed** | GTBench: NeurIPS 2024, 10 games including Tic-Tac-Toe **and Connect-4**, LLM-vs-LLM, authors Duan et al.; arXiv Feb 2024, about 5 months before the grid-games paper. TTT-Bench: EMNLP 2025 main (2025.emnlp-main.140), authors match, "41% & 5% lower ... compared to MATH 500 & AIME 2024". | https://github.com/jinhaoduan/GTBench; https://github.com/esteng/esteng.github.io (_news/neurips_2024.md); https://github.com/CSQianDong/Awesome-arXiv-Daily-Reporter (13-Jun-2025); https://github.com/ZhangCurosr/zhangcursor-papers-emnlp-2025-001 |
| C8 TopoBench design and results | **Confirmed in part** | Confirmed from the project page source: six families (FlowFree, Bridges, Loopy, Galaxies, Undead, Pattern), 3 tiers, 900 instances, 50 per family-tier, pass@1, no tools or code execution, 100k max tokens, and frontier-trio 0.58 / 0.38 / 0.15. Venue per arXiv comment: "Accepted, Workshop on Logical Reasoning of Large Language Models at ICLR 2026". "Nine" models confirmed by a second digest. **Unverifiable:** GPT-5-mini-high = 0.24 on hard, DeepSeek V3.2 = 0.10, and the 2-closed/7-open split. Tool-experiment detail corrected: 40% baseline, 46% / 42% / 50% across conditions. | https://raw.githubusercontent.com/topobench/topobench.github.io/main/index.html; https://github.com/ArXCompass/ArXCompass.github.io (papers/llm/2026_03/papers_3.md); https://github.com/memgrafter/research-digests |
| C9 TopoBench repo empty; name collision | **Confirmed** | mayug/topobench-benchmark: "This repository is empty", size 0, 0 stars, created and pushed 2026-03-12, description "Code and data for topobench-benchmark". Issue #1, "Release TopoBench on Hugging Face" by NielsRogge (2026-03-13), is open with no replies. The abstract's "this http URL" target could not be read directly; the repo description, creation date and HF issue make the link near-certain. geometric-intelligence/topobench: 256 stars, 113 forks, created 2023-11-30; paper arXiv:2406.06642 by Telyatnikov et al. **Related correction:** the YGN-SAGE "disambiguation" evidence is mischaracterized (see inline). | https://github.com/mayug/topobench-benchmark; https://github.com/mayug/topobench-benchmark/issues/1; https://github.com/geometric-intelligence/topobench |
| C10 Crowded puzzle space and MindTopo | **Corrected** | PUZZLES (arXiv:2407.00401, NeurIPS 2024, 40 Tatham puzzles), Enigmata (36 tasks, 7 categories, 4,758 Enigmata-Eval instances, NeurIPS 2025 Spotlight) and Reasoning Gym (">100 tasks", **NeurIPS 2025 Spotlight**) are all confirmed. MindTopo's 11,030 instances, 13 task types and 14 MLLMs are confirmed, but the headline numbers are **wrong**: the best model, GPT-5.6-Sol, scores **61.42%** (task-macro) against **97.87%** human; human sample-micro accuracy is 97.49%. No source for 54.1% or 97.4% was found. | https://github.com/ETH-DISCO/rlp; https://github.com/BytedTsinghua-SIA/Enigmata; https://github.com/open-thought/reasoning-gym; https://github.com/ZhangCurosr/zhangcursor-papers-arxiv-cl-001 (2026-09-11/MI-NDTOPO-.../full.md); https://github.com/TonyLeng1314/paper-brief |
| C11 Raw-corpora method and validation | **Corrected** | Confirmed: v1 title "Beyond Benchmarks: ...", v3 title "From Raw Corpora to Domain Benchmarks ...", TF/TF-IDF keyword targets, prediction rank as the primary metric, and only open-weight models (v3: GPT-2 XL, Llama2-7B, Mistral-7B-v0.3, Qwen2-7B/1.5B, Llama3.1-8B plus chat variants; OLMo-2 checkpoints). **Correction:** r = 0.99 (p < 0.001, N = 6 base models) is the pipeline's correlation; r = 0.91 (p = 0.012) is a Claude-generated comparison benchmark. v3 aggregates with a 20% trimmed mean of ranks. Wolfers is at FSU Jena. | https://github.com/CSQianDong/Awesome-arXiv-Daily-Reporter (10-Jun-2025); https://github.com/Luvata/arxive (pages/2026-03-09-cs-cl.html); https://github.com/aghado01/codex-scientiae (supellex/gauntlet/ai-eval/2506.07658v3) |
| C12 Raw-corpora venue status | **Confirmed** | The author's site says "January 2026: Extended benchmarking work (preprint) submitted to TMLR" and "currently under review at TMLR", and gives the corpora as arXiv 1.56M documents and M2D2 8.5B tokens. No ACL acceptance appears anywhere on the site. The v3 arXiv metadata has no journal-ref ("36 pages, 24 figures. Third version", updated 5 Mar 2026). | https://github.com/nsharma3150/nsharma3150.github.io (_pages/about.md, about_me.md, publications.html) |
| C13 BloomQA method and finding | **Confirmed** | Verbatim abstract in four independent mirrors matches the claim, including the authors and "LLMs sometimes perform relatively better on higher-order reasoning (Analyze) but fail more frequently on lower-level items (Remember)". Addition: the OpenReview record jwJkPowRTl is an ICLR 2026 submission titled "... Using Bloom's Taxonomy" with no decision recorded. | https://github.com/2shin0/arxiv-ai-mailing (LLM/2026-01-29.md); https://github.com/Luvata/arxive (pages/2026-01-29-cs-cl.html); https://github.com/KentoNishi/cs2760-ethics |
| C14 BloomQA scale (60k+ MCQs, 15k+ dialogues) | **Unverifiable** | The only source is the AI-generated memgrafter digest, which says "60,000+ MCQs and 15,000+ dialogues", "over 75,000 assessment items" and "uses LLMs to extract best practices". No second source was found; the arXiv abstract gives no counts. Keep the "secondary, medium-low" flag and do not cite the numbers in the paper without the primary PDF. | https://github.com/memgrafter/research-digests |

**Tally:** 10 confirmed (C1, C2, C3, C4, C5, C7, C8 in part, C9, C12, C13), 3 corrected (C6, C10, C11), 0 refuted, 1 unverifiable (C14).

**Other corrections found outside the load-bearing list** (all marked inline):

1. Chronology: "pre-emption" of Boardwalk by CWM changed to "overshadowed".
2. arXiv:2607.14169 is a single-author independent preprint (Javier Aguilar Martín), not DeepMind.
3. The YGN-SAGE README does not disambiguate against the TDL TopoBench library.
4. GTBench also includes Connect-4.
5. GameBench's venue is the NeurIPS 2024 Language Gamification Workshop.
6. The TopoBench tool experiment has a 42% condition that "46-50%" left out.
7. The Grid-games journal year is 2025 in OpenAlex-derived data and 2024 in one card; volume and issue are unconfirmed.
8. "From Code to Play" now has its full title and authors.

### Reference-check summary

All 32 entries in `research/refs/user_failed_b.json` were checked; none were skipped. One entry was added for arXiv:2609.09163, which the text cites but the JSON lacked.

- **Verified: 31 of 32** (plus the added 2609.09163 entry, also verified). All arXiv IDs, titles and years match; no fabricated reference was found. Author lists were filled in where they had been "not seen": GTBench, GameBench, From Code to Play, TopoBench-TDL, PUZZLES, Enigmata, Reasoning Gym, MindTopo, 2607.14169 and LLM GameLab. Venues were corrected or added for Reasoning Gym (NeurIPS 2025 Spotlight), GameBench (NeurIPS 2024 workshop), Enigmata (Spotlight) and PUZZLES (arXiv:2407.00401 added).
- **Not fully verified: 1.** `topsakal2025jcs`: the title and journal exist per OpenAlex-derived data, but the year is inconsistent across sources (2024 vs 2025) and volume and issue are unconfirmed. Marked verified=false pending a primary check.
- **Flagged secondary:** `memgrafter2026digests` is a real repository, so it is marked verified=true, but it is an AI-generated source whose BloomQA numbers could not be corroborated. Its numbers should not be used.
- **Problematic in content (not identity):**
  - `mindtopo2026` (wrong numbers in used_for);
  - `sharma2025rawcorpora` (r-range conflation);
  - `ygnsage2026readme` (used_for mischaracterized);
  - `cwmfollowup2026playadequacy` (author missing);
  - `lehrach2025cwm` ("pre-empts" wording).

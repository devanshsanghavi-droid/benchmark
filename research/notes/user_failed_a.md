# Lead-supplied "failed" benchmarks, items 1-5 (Qi Town, Game Reasoning Arena, MastermindEval, Concept, Codenames ad-hoc concept forming)

Research subagent dossier. Date of research: 2026-09-29.

Method note: evidence comes from WebSearch result summaries (arXiv, ACL Anthology, OpenReview, LAION, news sites), direct WebFetch of GitHub pages (READMEs, commit logs, directory listings), and the GitHub repository-search API. arXiv, Hugging Face, ACL Anthology, OpenReview, Emergent Mind, Bytez, Pith and similar sites could not be fetched directly, so paper-internal numbers (for example the Qi Town Elo ranking and the Codenames win rate) come from search-result summaries. They are marked medium confidence and should be checked against the PDFs before the paper cites them. The session-wide web-search budget ran out partway through, so a few planned cross-checks are listed as open items at the end. No citation counts appeared in any search result, so this dossier makes no claim about citation counts. GitHub star, fork and commit counts are snapshots taken on 2026-09-29.

---

## Summary

- **All five papers are real, and every arXiv ID matches the paper the lead described.** Game Reasoning Arena (2508.03368) changed its name between versions: v1 was titled "Board Game Arena: A Framework and Benchmark for Assessing Large Language Models via Strategic Play".
- **Not all five are "dead", and they did not fail in the same way.**
  - **Clearly failed as benchmarks:** Qi Town (item 1) and Game Reasoning Arena (item 2). Neither has a maintained public ladder or any visible uptake. Qi Town has no public code that GitHub search could find. The last commit to Game Reasoning Arena's main branch was on 11 Sep 2025, about five weeks after release, and the repo has 9 stars. The strongest single cause, which the lead missed, is **pre-emption**. Google DeepMind and Kaggle launched **Kaggle Game Arena** on 4 Aug 2025. That is the day the Game Reasoning Arena repo was created and its LAION blog post went out, and one day before Qi Town reached arXiv. Kaggle Game Arena covers the same space (LLMs playing classic games, starting with chess, built on the same OpenSpiel engine that Game Reasoning Arena uses). It had institutional backing, chess.com media coverage and a maintained leaderboard, and it later added Poker, Werewolf and a unified cross-game leaderboard (Feb 2026).
  - **Quiet afterlife as a component rather than a leaderboard:** MastermindEval (item 3). Its multiple-choice variant has been merged into **EleutherAI's lm-evaluation-harness** as 6 tasks (added 18 Mar 2025), and the authors were still committing to the repo in Aug 2026. It never became a frontier leaderboard, but "dead" overstates it.
  - **Absorbed into a live benchmark:** Codenames ad-hoc concept forming (item 5). The Codenames game is part of **clembench**, the Potsdam dialogue-game benchmark, which has a continuously updated leaderboard and several versions. The lead is right that a competing Codenames benchmark (Stephenson et al., arXiv:2412.11373, 16 Dec 2024) came out about two months earlier. The bigger issue is saturation of the Codenames niche: 49 GitHub repos match "codenames llm".
  - **Too new to call:** Concept (item 4). It went up on arXiv on 15 Oct 2025 and was accepted to **Findings of ACL 2026**. Its headline result is a large gap: humans succeed more than 90% of the time, and no LLM exceeds 40% (reported in the abstract). A gap like that is a strength for a benchmark. Calling it "dead" less than a year after release, with a fresh top-venue acceptance, is premature. The lead's "party-game skill no product needs" critique is the weakest of the five (see below).
- **Cross-cutting lesson:** in 2025-26, game-based LLM evaluation is badly oversupplied. GitHub search finds 173 repos for "llm game benchmark" and 49 for "codenames llm". The game-style evaluations that gained traction share five traits:
  1. Institutional or sustained individual maintenance with current frontier models.
  2. One headline number.
  3. Low friction to run.
  4. Spectator or narrative value.
  5. Enough matches or items for tight confidence intervals.

  Examples are Kaggle Game Arena, lechmazur's Elimination Game (61 models including GPT-5.2 and Claude Opus 4.5) and AI Diplomacy (707 stars). The five academic papers here mostly did not have these traits. Most were one-off paper artifacts from small academic groups, published in workshops or Findings, with no plan to keep them maintained.

---

## Detailed findings

### Context: the 2025-2026 game-benchmark landscape these papers entered

- **Kaggle Game Arena (Google DeepMind and Kaggle).**
  - Announced 4 Aug 2025 as "a public AI benchmarking platform where AI models compete in strategic games", with an AI chess exhibition tournament on 5-7 Aug 2025 featuring 8 frontier LLMs, including Gemini 2.5 Pro, o3, o4-mini, Claude 4 Opus, DeepSeek R1, Kimi k2 and Grok 4 (https://siliconangle.com/2025/08/04/google-deepmind-host-ai-chess-tournament-evaluate-leading-ai-models-reasoning-skills/ ; https://www.chess.com/news/view/which-ai-model-is-the-best-at-chess-kaggle-game-arena).
  - o3 beat Grok 4 in the final (https://www.chess.com/news/view/kaggle-game-arena-chess-2025-day-3).
  - The final leaderboard used all-play-all with "over a hundred matches between every pair of models" for statistical robustness (search summary of chess.com and Kaggle coverage).
  - On 2 Feb 2026 it added Heads-Up Poker and Werewolf, with Gemini 3 models leading. It also introduced a **Unified Game Arena Leaderboard**, "a single, consolidated ranking" across games, to replace "juggling separate Elo ratings, win rates, and poker statistics" (https://gigazine.net/gsc_news/en/20260203-google-kaggle-game-arena-poker-and-werewolf/ ; https://winbuzzer.com/2026/02/04/deepmind-game-arena-poker-werewolf-gemini-3-tops-rankings-xcxwbn/). [corrected by fact-check: Poker/Werewolf activity in early Feb 2026 is loosely corroborated by an independent timeline (github.com/guzus/ai-research-arm, research/models/2026-02-03-timeline.md), but the "unified leaderboard" detail rests only on these two secondary news items, which could not be reopened. Treat it as single-source.]
  - The harness, github.com/google-deepmind/game_arena (115 stars, Apache-2.0), is built on OpenSpiel (https://github.com/google-deepmind/game_arena).
  - A technical report, "Game Arena: Strategic LLM Evaluation in Competitive Environments", went up as arXiv:2609.31473 on 25 Sep 2026 (https://arxiv.org/abs/2609.31473). (Fact-check: confirmed via arXiv mirrors on GitHub. It is 31 pages, with pilot environments Chess, Poker and Werewolf. The first author is Bovard Doerschuk-Tiberi and the last is Minmin Chen, out of about 62 authors.)
  - **Relevance:** this directly pre-empts items 1 and 2, which launched the same week.
- **Other game benchmarks in the same space.** The field was crowded before items 1-5 appeared:
  - clembench (arXiv:2305.13455; clembench2024 arXiv:2405.20859)
  - GTBench (arXiv:2402.12348)
  - Grid-based game competitions (arXiv:2407.07796; repo research-outcome/LLM-Game-Benchmark, 25 stars, Tic-Tac-Toe, Connect Four and Gomoku)
  - GameArena (live computer games, ICLR 2025, arXiv:2412.06394)
  - GAMEBoT (ACL 2025)
  - SPIN-Bench (arXiv:2503.12349)
  - KORGym (arXiv:2505.14552)
  - LMGame-Bench (arXiv:2505.15146)
  - LLM-Gomoku (arXiv:2503.21683)
  - LLM Chess (maxim-saplin/llm_chess, 133 stars, 1,430 commits, live leaderboard; arXiv:2512.01992)

  GitHub search for "llm game benchmark" returns 173 repositories (GitHub search API, 2026-09-29).
- **Community benchmarks that did gain traction**, as contrast cases:
  - AI_Diplomacy (GoodStartLabs): 707 stars, 407 commits. It has a Twitch streamer module and a 3D visualiser, and focuses on negotiation and betrayal.
  - lechmazur/elimination_game: 298 stars, TrueSkill ratings, 61 models including GPT-5.2, Claude Opus 4.5 and Gemini 3 Flash as of Jan 2026. [corrected by fact-check: the README's most recent update entry is 6 Jan 2026, with no model additions since, so maintenance has paused for about 9 months.]
  - stalkermustang/llm-bulls-and-cows-benchmark: 236 stars, created 26 Nov 2024. This is a Mastermind-type game with Wilson confidence intervals. [corrected by fact-check: this is *not* a sustained-maintenance case. Its last commit, on 1 Feb 2025, is titled "o3-mini saturated the benchmark....", and the repo has been inactive since then. It is better read as an example of fast saturation (https://github.com/stalkermustang/llm-bulls-and-cows-benchmark, commit 8a50752).]

  (GitHub pages fetched 2026-09-29.)

---

### Item 1: Qi Town, "Who is a Better Player: LLM against LLM" (arXiv:2508.04720)

**Identity (verified via search).**
- **Title:** "Who is a Better Player: LLM against LLM" (https://arxiv.org/abs/2508.04720).
- **Authors:** Yingjie Zhou and 12 co-authors: Jiezhang Cao, Farong Wen, Li Xu, Yanwei Jiang, Jun Jia, Ronghui Li, Xiaohong Liu, Yu Zhou, Xiongkuo Min, Jie Guo, Zicheng Zhang and Guangtao Zhai (search summary of arXiv and ResearchGate).
- **Affiliation:** Shanghai Jiao Tong University, per a search summary; Guangtao Zhai's group. Medium confidence.
- **Submitted:** 5 Aug 2025 (search summary).
- **Venue:** none found; arXiv preprint only, as far as could be verified.

**What it does.**
- Qi Town is described as "a virtual community" for automated round-robin tournaments between **20 LLMs from 12 organisations** (including OpenAI, Google, Anthropic and DeepSeek).
- It uses **5 games**: Gomoku, Chess, Reversi and Tic-Tac-Toe, plus a "Free-Style" mode in which two LLMs negotiate rules before playing.
- It reports three metrics:
  - **Elo**.
  - A **Performance Loop Graph (PLG)**, a directed win/loss graph that exposes intransitive cycles (A beats B, B beats C, C beats A).
  - A **Positive Sentiment Score (PSS)**, from models self-reporting a "mental state" (Desperate to Excited) after each move, framed as "mental fitness".
- The motivation is "compensating the limitation of data dependency of the mainstream Q&A based benchmark method" (https://arxiv.org/abs/2508.04720 ; https://www.emergentmind.com/papers/2508.04720 ; https://pith.science/paper/2508.04720, all via search summaries).
- **Reported results** (search summaries; medium confidence, verify against the PDF):
  - Gemini 2.0-Flash had the highest average Elo across games, "followed closely by GPT-4.1".
  - Roughly 2,850 games were played (low-medium confidence; single secondary summary). [corrected by fact-check: a second, independent AI-generated digest (memgrafter/research-digests, file 2508.04720_...md) also reports "three repetitions per game (2,850 total matches)" and "Gemini-2.0-Flash achieved highest average Elo performance". The count is arithmetically consistent: 190 pairs x 5 games x 3 repetitions = 2,850. Confidence raised to medium. The GPT-4.1 runner-up claim is still single-source.]
  - "Most LLMs remain optimistic about winning and losing, demonstrating greater adaptability to high-stress adversarial environments than humans."

**Adoption evidence.**
- GitHub repository search for "Qi Town LLM board game" and "qitown" returned **0 repositories**.
- No leaderboard, code or dataset link surfaced in any search result.
- No follow-up work citing it surfaced.
- Conclusion: no evidence of use by any lab or leaderboard.

**Assessment of the lead's critique** ("three separate scores, none comparable to other benchmarks; games simple and well known; no unique offering"): **Agree, with refinements.**
- *Three scores:* correct. The deeper problem is that the three scores measure unrelated constructs. PSS measures a model's willingness to report positive emotion when prompted. That is plausibly a prompt-following or persona artifact, not a capability; this is my interpretation, and I found no validation study for PSS. Mixing it into a benchmark dilutes the capability claim.
- *Comparability with other benchmarks:* partly misframed. Arena-style Elo is not comparable across benchmarks either. The real issue is the **absence of one headline score**. Kaggle Game Arena later had to build a unified leaderboard for exactly this reason (Feb 2026).
- *Games simple and well known:* correct and important.
  - Tic-Tac-Toe is a solved game. Two competent players always draw, which leaves no headroom at the top.
  - Chess already had a dedicated, continuously maintained LLM leaderboard (LLM Chess, 133 stars) and then Kaggle Game Arena.
  - Tic-Tac-Toe, Gomoku and Connect Four were already covered by the 2024 grid-based-games benchmark (arXiv:2407.07796, item 7 on the lead's list).
- *Pushback:* PLG is a genuinely useful scientific observation. Intransitive win cycles show that a single Elo number can mislead for matchup-dependent skills. The Free-Style negotiated-rules mode is also the one novel idea. The paper is scientifically useful as an observation, even though it failed as a benchmark.

**Additional failure causes the lead missed.**
1. **Timing and pre-emption.** It was posted one day after Google DeepMind and Kaggle launched Kaggle Game Arena, which had heavy media coverage.
2. **No public code or leaderboard found.** A benchmark that cannot be re-run cannot be adopted.
3. **Model roster aged immediately.** A top average Elo for Gemini 2.0-Flash, if confirmed, suggests the strongest reasoning models of Aug 2025 (o3, Gemini 2.5 Pro) were absent or handicapped. Frontier labs ignore a ranking that does not include frontier models.
4. **Weak construct validity for PSS**, and for "mental fitness" as a term applied to LLMs.
5. **No venue or institutional distribution channel.** It went through no harness (lm-eval, HELM, Inspect) and no hosted platform.
6. **Unclear statistical power.** With 20 models, a round-robin gives 190 pairs. About 2,850 games means roughly 15 games per pair spread across 5 games, which is too few for tight Elo intervals per game. This is my inference from the unverified game count. Compare Kaggle's more than 100 matches per pair in chess alone. [corrected by fact-check: the secondary digest states the design directly as 3 repetitions per pair per game, i.e. 3 games per pair per game type.]

**Lesson.** Classic games plus a new visualisation plus an affect metric is not a benchmark contribution in 2025. It needs a distinctive construct, released code, a maintained ladder and statistically adequate sampling.

---

### Item 2: Game Reasoning Arena (arXiv:2508.03368)

**Identity (verified).**
- **Title:** "Game Reasoning Arena: A Framework and Benchmark for Assessing Reasoning Capabilities of Large Language Models via Game Play".
- **Earlier title:** v1 was "Board Game Arena: A Framework and Benchmark for Assessing Large Language Models via Strategic Play" (https://arxiv.org/pdf/2508.03368v1 ; https://www.researchgate.net/publication/394322937).
- **Authors:** Lucia Cipolina-Kun, Marianna Nezhurina and Jenia Jitsev, from **LAION and Jülich Supercomputing Centre** (https://arxiv.org/abs/2508.03368 ; https://laion.ai/blog/reasoning_game_arena_blog_post/).
- The LAION blog post is dated 4 Aug 2025 (search summary).
- **Venue:** none found beyond arXiv.

**What it does.**
- A Python library wrapping **Google OpenSpiel** games that lets LLM agents play against random, heuristic, RL or human agents and other LLMs. [corrected by fact-check: the v1 abstract lists "random, human, reinforcement learning agents, etc."; "heuristic" does not appear there.]
- It uses LiteLLM (API), vLLM (local) and Ray (distributed execution).
- **Games** listed in the README: tic_tac_toe, connect_four, kuhn_poker, prisoners_dilemma, matrix_pd, matching_pennies, matrix_rps, hex and chess (https://github.com/SLAMPAI/game_reasoning_arena).
- The analytic emphasis is on **recording and categorising reasoning traces** rather than win rates. For example, the Llama 70B model shows richer opponent modelling than the 8B model (search summary of arXiv v3 HTML).
- The LAION blog pitches it as "the first platform to capture AI's strategic thinking in real-time". One reported finding is that "larger models show more adaptive reasoning patterns, while smaller models commit early to fixed strategies".

**Adoption evidence.**
- **GitHub:** SLAMPAI/game_reasoning_arena was created 4 Aug 2025 and has **9 stars, 4 forks** and roughly 209 commits.
- The **most recent commit on main visible on the commits page is 11 Sep 2025**. All of the last ten commits were by a single author, lcipolina, in 7-11 Sep 2025. This is strong evidence that active development stopped about five weeks after launch.
- A Hugging Face Space leaderboard exists at huggingface.co/spaces/lcipolina/game_reasoning_arena (seen in a search result; it could not be fetched). It sits on a personal account, not an organisational one.
- There is also a readthedocs site and a Discord.
- No lab or third-party leaderboard use surfaced.
- The licence is ambiguous. The repo-page fetch reported "CC BY-NC 4.0", while the raw README says MIT (unverified which applies). A non-commercial licence would deter industry use. [corrected by fact-check: the README body text says "This code is made available under a CC BY-NC 4.0 license, as found in the LICENSE file". MIT appears only in a badge, and no LICENSE file exists at the repo root (raw path returns 404). The stated licence is therefore CC BY-NC 4.0, contradicted by the badge.]

**Assessment of the lead's critique** ("heavy install for simple games; nothing unique; a framework not a ladder; academic tool not consumer-level"): **Mostly agree, with one factual correction.**
- *Heavy install:* **confirmed.** The README requires:
  - cloning the repo;
  - `conda env create -f environment.yaml`;
  - `pip install -e .`;
  - separately cloning `deepmind/open_spiel` and running its `./install.sh`;
  - creating a `.env` file with keys for Groq, Together, Fireworks and OpenAI.

  That is a lot of friction for playing Tic-Tac-Toe.
- *Not a ladder:* **partly incorrect.** There was a HF Space with a leaderboard, and the LAION blog links to "the leaderboard". But the ladder was not maintained, was not prominent, and was not refreshed with frontier models, so in practice the lead's point stands.
- *Nothing unique:* **partly unfair.** Reasoning-trace categorisation during play is a somewhat distinctive angle; interpretability is more its purpose than ranking. It is scientifically useful as a toolkit even though it failed as a benchmark.

**Additional failure causes the lead missed.**
1. **Direct pre-emption by a far better-resourced project on the same substrate.**
   - Kaggle Game Arena launched on the same day (4 Aug 2025).
   - It uses the same OpenSpiel engine.
   - It had Google DeepMind and Kaggle distribution, chess.com media and a statistically designed all-play-all ladder.
   - A three-person academic project cannot out-compete that for mindshare.
2. **Framework and benchmark identity confusion.** The paper presents itself as both a framework and a benchmark but does not commit to a canonical task set, protocol and headline score.
3. **Name churn.** It went from "Board Game Arena" to "Game Reasoning Arena". "Board Game Arena" is also the name of a popular online board-game website (my background knowledge; not verified in this session), which may have forced the rename and fragmented discoverability.
4. **Weak baselines for frontier discrimination.** Beating random or simple bots at Tic-Tac-Toe or matching pennies does not separate frontier models.
5. **Maintenance cliff.** Commits stopped around 11 Sep 2025.
6. **Possible non-commercial licence** (unverified).

**Lesson.** A harness is not a benchmark. Benchmarks become standards through a fixed protocol, a single score, low friction (hosted evaluation or `pip install` with no native builds) and sustained curation. If a well-funded incumbent is entering the same niche, differentiate on construct or do not enter.

---

### Item 3: MastermindEval (arXiv:2503.05891)

**Identity (verified).**
- **Title:** "MastermindEval: A Simple But Scalable Reasoning Benchmark".
- **Authors:** Jonas Golde, Patrick Haller, Fabio Barth and Alan Akbik, from Humboldt-Universität zu Berlin (Akbik's group; DFKI Berlin also named in one summary; medium confidence on affiliations).
- **Posted:** arXiv, 7 Mar 2025 (search summary).
- **Venue:** **ICLR 2025 Workshop on Reasoning and Planning for LLMs** (OpenReview id H4donosutm) (https://arxiv.org/abs/2503.05891 ; https://openreview.net/pdf?id=H4donosutm ; https://mlanthology.org/iclrw/2025/golde2025iclrw-mastermindeval/ ; the BibTeX in https://github.com/flairNLP/mastermind).

**What it does.** It offers three paradigms:
1. **Agentic:** the model plays Mastermind as codebreaker.
2. **Deductive:** the model is given a pre-played game state, played with Knuth's algorithm until exactly one valid code remains, and must name that code.
3. **Multiple-choice by log-likelihood:** this tests pretrained models without test-time compute.

The metric is solve rate. Difficulty scales with code length, number of colours and number of allowed guesses. More than 30,000 pre-played game states were generated (secondary summary from themoonlight.io; medium confidence). [corrected by fact-check: themoonlight.io could not be reopened and no independent source for the 30,000 figure was found. Downgraded to unverified. Knuth-algorithm pre-play *is* confirmed by the lm-evaluation-harness task README.]

Reported findings (search summaries):
- "Even easy Mastermind instances are difficult for current models".
- Performance falls as the number of statements that must be combined increases.
- o3-mini outperformed other proprietary models in every configuration (medium confidence). [corrected by fact-check: no independent confirmation found; treat as unverified. Also note that the arXiv abstract describes *two* paradigms (agentic and deductive). The third, log-likelihood multiple-choice paradigm is described in the flairNLP/mastermind README.]

**Adoption evidence.**
- **Integrated into EleutherAI lm-evaluation-harness.** The directory `lm_eval/tasks/mastermind` holds 6 tasks: mastermind_24/35/46 in easy and hard variants, where hard means distractors differ by one symbol. It was added in commit "Add MastermindEval (#2788)" on **18 Mar 2025** by the first author (https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks/mastermind). This gives the benchmark a permanent, low-friction distribution channel used in pretraining evaluations.
- **The repo is still maintained.** flairNLP/mastermind has 10 stars, 1 fork and 49 commits under an MIT licence. Recent commits:
  - 20 Mar 2026: dependency upgrade.
  - 12 May 2026: vLLM support.
  - 4 Aug 2026: "Scale dataset generation to larger settings, capture vLLM reasoning output".

  (https://github.com/flairNLP/mastermind/commits/main)
- **No public leaderboard** exists, and no frontier-lab model card citing it surfaced.
- **Competing and pre-empting work:**
  - The community "LLM Bulls and Cows benchmark" (stalkermustang) is the same game family, 4-digit code-breaking. It was created **26 Nov 2024**, about 3.5 months before MastermindEval's arXiv post, and has **236 stars**. It reports a leaderboard with Wilson confidence intervals; the snapshot fetched showed o1-mini at 60% and Claude 3.5 Sonnet at 36% over roughly 50 games each. [corrected by fact-check on three points:
    - The README table shows o1-mini at 60.0% over **25** games and Claude 3.5 Sonnet at 36.0% over 50 games.
    - flairNLP/mastermind was *created* on 15 Nov 2024, 11 days *before* the Bulls-and-Cows repo, although its public arXiv release came later (7 Mar 2025).
    - The Bulls-and-Cows repo's last commit (1 Feb 2025) is "o3-mini saturated the benchmark....". The community competitor itself went inactive through saturation before MastermindEval was even posted.]
  - TurnBench-MS (arXiv:2506.01341, Findings of EMNLP 2025) followed with a richer code-breaking game (Turing Machine).
  - Name collision: another "Mastermind" project, opendilab/Mastermind ("Empowering LLMs in Decision Games through Algorithmic Data Synthesis", ICLR 2025 SynthData Workshop spotlight, 50 stars), shares the name, which muddies discoverability.

**Assessment of the lead's critique** ("models may have memorised it; one pre-existing game; no underlying philosophy; no measurable leaderboard; not fun"): **Partly agree. Disagree on memorisation and philosophy.**
- *Memorisation:* **mostly incorrect as stated.** Instances are procedurally generated from random secret codes, so a specific instance cannot be memorised. The real vulnerabilities are different:
  - The *strategy* (Knuth's five-guess algorithm, 1977) is well known and likely in pretraining data.
  - More importantly, the task is **trivially tool-solvable**. With code length 4 and 6 colours there are only 6^4 = 1,296 codes, so a ten-line brute-force program solves any deduction instance exactly.

  Once models routinely use code execution, the benchmark measures "reasoning without tools", which is a narrow construct.
- *No philosophy:* **incorrect.** The paper states an explicit design philosophy: "simple, scalable, interpretable". It also has a clever measurement design: separating agentic play, pure deduction and likelihood-based MCQ, which isolates where reasoning fails. That is more principled than most game benchmarks.
- *No leaderboard:* **correct.**
- *Not fun for consumers:* true, but it was never aimed at consumers. It is a research diagnostic.

**Additional failure causes the lead missed.**
1. **Workshop-only venue** with a small academic team and no promotion or ladder.
2. **Pre-empted in the public eye** by a community Bulls-and-Cows leaderboard that appeared earlier and had 20 times more stars. [corrected by fact-check: this factor is weaker than stated. The MastermindEval repo predates the Bulls-and-Cows repo (15 vs 26 Nov 2024), and Bulls-and-Cows stopped on 1 Feb 2025 after o3-mini saturated it. The stronger lesson from Bulls-and-Cows is item 4 below: the game family saturates quickly under reasoning models.]
3. **Narrow construct.** It tests constraint integration over a small hypothesis space, with low incremental validity over existing logic-puzzle benchmarks.
4. **Rapid headroom erosion from reasoning models.** o3-mini led at publication. Scaling the parameters restores difficulty, but "harder Mastermind" is not a capability story labs care about. (Fact-check support: the sibling Bulls-and-Cows benchmark recorded "o3-mini saturated the benchmark" in its final commit on 1 Feb 2025. In Aug 2026 the MastermindEval authors added generation for larger boards (5x7, 6x8, 7x9; commit 03de37e), which is consistent with an attempt to restore headroom.)
5. **Tool-solvability** (above).

**Lesson.** Procedural generation with parametric difficulty is a good idea worth copying: it resists contamination and can be rescaled. Integration into a standard harness gives a benchmark a long tail of use without a leaderboard. But a task whose ground truth can be computed by a few lines of code must declare a tool-use policy, or it risks becoming a test of "refusing to write code".

---

### Item 4: Concept, "Do You Get the Hint? Benchmarking LLMs on the Board Game Concept" (arXiv:2510.13271)

**Identity (verified).**
- **Title:** "Do You Get the Hint? Benchmarking LLMs on the Board Game Concept".
- **Authors:** Ine Gevers and Walter Daelemans.
- **Posted:** arXiv, **15 Oct 2025**.
- **Venue:** **Findings of the Association for Computational Linguistics: ACL 2026** (ACL Anthology id 2026.findings-acl.1219) (https://arxiv.org/abs/2510.13271 ; https://aclanthology.org/2026.findings-acl.1219/).
- **Affiliation:** Daelemans is associated with the University of Antwerp (CLiPS), per my background knowledge; this was not verified in-session.

**What it does.**
- Uses the word-guessing board game Concept to probe **abductive reasoning**. A guesser must infer a target word or concept from another player's sequence of hints, which are placed on a board of icons in the physical game.
- **Headline result:** "easily solved by humans (with a success rate of over 90%), [it] is still very challenging for state-of-the-art LLMs (no model exceeds 40% success rate)".
- LLMs struggle to interpret other players' strategic intent and to revise initial hypotheses as information arrives sequentially.
- Performance drops further in lower-resource languages (Dutch, French and Spanish) compared with English (abstract via search summaries).
- **Data:** a Hugging Face dataset, IneG/concept, exists (seen in a search result; not fetchable).
- **Not verified:** the number of games, the models evaluated, and the source of the game logs. Planned searches for these were cut off by the search budget. [corrected by fact-check, partially filled from one AI-generated digest (memgrafter/research-digests, 2510.13271_...md; low-medium confidence):
  - Game logs were collected from the **Board Game Arena** website in English, French, Dutch and Spanish, so the data are human play logs.
  - **Seven** LLMs were tested with static and dynamic prompting, including GPT-4.1-mini, Llama-3.3-70B and GPT-OSS-120B.
  - **Caveat:** if the model roster really topped out at these models, the headline "no model exceeds 40%" may not hold for Aug-2026 frontier reasoning models. The paper should cite it as "no *evaluated* model".
  - The v1 date of 15 Oct 2025 is confirmed (ArXCompass, arXiv-API-derived). A v2 followed on 7 Jan 2026.]

**Adoption evidence.**
- GitHub search for the paper title returned no repository.
- No leaderboard was found.
- The Findings of ACL 2026 acceptance is very recent. ACL 2026 proceedings appeared about two to three months before this research date, so citation uptake would not yet be visible.

**Assessment of the lead's critique** ("party-game skill no product needs; not applicable to the real world; no depth, like Chutes and Ladders"): **Largely disagree.**
- *"Dead":* **premature.** It was released less than a year ago and has just been accepted at a top-tier venue. It has no leaderboard, but it was never framed as one.
- *"No product needs it":* **weak.** The underlying construct is:
  - inferring a communicator's intent from sparse, strategically chosen cues;
  - revising hypotheses as cues arrive.

  That is central to real deployments: interpreting under-specified user requests, clarification dialogue, multi-agent coordination, and reading hints in tutoring or search. The multilingual degradation finding is directly product-relevant.
- *"No depth / Chutes and Ladders":* **incorrect on the evidence.** Chutes and Ladders involves no decisions at all. Concept yields a human-LLM gap of more than 50 percentage points (over 90% versus under 40%). A large, human-validated gap is exactly the headroom property the lead praises elsewhere (for example in ARC-AGI).
- *Where the lead has a point:*
  - It is still one commercial game.
  - A text rendering of a visual icon board may partly test board-representation parsing rather than abduction. This is my interpretation and needs checking against the paper's rendering.
  - No leaderboard or harness integration was found.
  - Data derived from human games does not scale procedurally the way MastermindEval does.

**Additional risks and failure causes.**
1. **Single-game construct.** Results may not generalise beyond Concept's specific hint grammar.
2. **Scaling limits** if the data comes from human play logs (unverified). [corrected by fact-check: a secondary digest says the logs come from the Board Game Arena website, so this risk likely applies (low-medium confidence).]
3. **No distribution channel.** Findings papers without code, harness tasks or a leaderboard tend to be cited, not run.
4. **Crowded "word game" niche.** Prior work includes clembench's Taboo and Wordle, Codenames (items 5 and 12) and word-guessing papers such as arXiv:2310.20499 (title only seen).

**Lesson.** A human baseline plus a large gap is the most valuable design property here and should be copied. Grounding the construct (abduction, intent inference) in real tasks, rather than in the game, would have strengthened the real-world validity argument the lead found lacking.

---

### Item 5: "Ad-hoc Concept Forming in the Game Codenames as a Means for Evaluating Large Language Models" (arXiv:2502.11707)

**Identity (verified).**
- **Authors:** Sherzod Hakimov, Lara Pfennigschmidt and David Schlangen, from the University of Potsdam computational linguistics group, the clembench team.
- **Posted:** arXiv, Feb 2025; the exact day was not verified, and the ID implies mid-Feb 2025. [corrected by fact-check: v1 appears in the 17 Feb 2025 arXiv daily listing (github.com/Lcollection/Arxiv_Daily, docs/daily-papers/2025-02-17.md). v2 was listed 26 Jun 2025.]
- **Venue:** **GEM² workshop (Fourth Workshop on Generation, Evaluation and Metrics), co-located with ACL 2025** (ACL Anthology 2025.gem-1.63) (https://arxiv.org/abs/2502.11707 ; https://aclanthology.org/2025.gem-1.63/).

**What it does.**
- LLMs play both roles in Codenames, as clue-giver (spymaster) and guesser, against a *programmed mock opponent*.
- The experiments vary word properties (abstract vs. concrete, ambiguous vs. monosemic, frequency), risk (assassin), board clustering, and opponent speed.
- **Findings** (search summaries, medium confidence):
  - Of **14 models**, the best, **o3-mini, reaches a win rate of only 49%**. [corrected by fact-check: still single-source. The GitHub source of en.papernotes.org (zhaoyang97/Paper-Notes) is the same pipeline, not an independent confirmation. It reports o3-mini's figure as a *clemscore of 49.2 at a 100% played rate* and calls it a 49% win rate. It also says DeepSeek-R1 was the only model to win against the hard (fast) opponent (22.2%). Verify against the PDF before citing.]
  - Commercial models beat open-weight ones by a margin (about 5 points between o3-mini and DeepSeek-R1). [corrected by fact-check: the "about 5 points" gap is unverified. The Paper-Notes summary attributes the open-weight deficit mainly to instruction-following failures, with format errors and target hallucinations 5-10 times more frequent.]
  - Easy associations are mastered but difficult ones are not.
  - Concrete words are easier than abstract ones, and monosemic easier than ambiguous.
  - Models do better against a slow opponent than a fast one.

  (https://aclanthology.org/2025.gem-1.63.pdf ; https://en.papernotes.org/ACL2025/llm_evaluation/...)

**Adoption evidence.**
- **The game lives on inside clembench.** clp-research/clembench (5 stars, 22 forks, 287 commits) contains a `codenames/` game directory with GameMaster, players, scorer and instance generator. Its README describes experiments over word frequency, ambiguity, concreteness, assassin risk, opponent difficulty and clustered vs. random boards, matching the paper (https://github.com/clp-research/clembench/tree/main/codenames).
- The clembench **leaderboard is maintained**, with text v2.0 and v3.0 and multimodal v1.6. A secondary aggregator reports **31 models** on Clembench Text v3.0 (https://benchmarklist.com/benchmarks/clembench_text_v3/ ; secondary source, medium confidence). The leaderboard is also hosted at huggingface.co/spaces/colab-potsdam/clem-leaderboard. [corrected by fact-check: the clembench-runs CHANGELOG shows **codenames was added in clembench v2.0 (March 2025)**, alongside matchit_ascii, adventuregame, guesswhat and textmapworld (817 instances in total). The repo lists v2.0 and v3.0 run directories. clp-research/clembench was last pushed on 26 Apr 2026 and clembench-runs was last updated on 15 Apr 2026. The "31 models" figure could not be rechecked because benchmarklist.com is blocked.]
- So this paper's benchmark **did get used**, as one game inside a live multi-game ladder.

**Pre-emption and competition.**
- "Codenames as a Benchmark for Large Language Models" by Matthew Stephenson, Matthew Sidji and Benoît Ronval (arXiv:2412.11373) was **submitted 16 Dec 2024** and revised 21 Apr 2025. It evaluated GPT-4o, Gemini 1.5, Claude 3.5 Sonnet and Llama 3.1 (https://arxiv.org/abs/2412.11373).
- The gap between the two papers is about two months, which **confirms the lead's claim**.
- Hobbyist LLM-Codenames implementations predate both papers:
  - mich1803/Codenames-LLM and PierreEpron/llm-codenames were created 3 Jun 2024.
  - ilya-aby/llm-codenames, created 12 Nov 2024, has 110 stars and a live demo at llmcodenames.com; its ELO leaderboard is listed only as "future work".
- GitHub search for "codenames llm" returns **49 repositories**, and "codenames llm benchmark" returns 6 more small (1 star or fewer) benchmark repos created between Dec 2024 and Sep 2026.

**Assessment of the lead's critique** ("another Codenames benchmark came out 2 months earlier; one game models can be trained on with known strategies; doesn't measure intelligence"): **Partly agree.**
- *Pre-emption:* **correct** (Dec 2024 vs. Feb 2025). The broader truth is that the Codenames niche was saturated.
- *"Known strategies / trainable":* **weak.** Codenames boards are combinatorially sampled from word lists. There is no opening book, and the skill is semantic association under constraints, not a memorisable line of play. Training on Codenames would teach association-with-exclusion, which is a legitimate language skill.
- *"Doesn't measure intelligence":* **partially fair, for a different reason.** The core skill, embedding-like semantic association, is one LLMs are natively strong at. That makes the benchmark partly a test of distributional semantics rather than reasoning, and limits its discriminative power at the frontier. The paper's own controlled manipulations are the right response to this: they turn the game into a diagnostic of *which* lexical properties cause failure.
- *Pushback on "dead":* its design choice to build inside a maintained multi-game suite (clembench) is exactly what the other four lacked.

**Additional failure causes, as a standalone benchmark.**
1. Duplicated effort, with at least two papers and dozens of repos on the same game.
2. Workshop venue.
3. A mock opponent rather than a human baseline.
4. Language-specific (English) word lists.
5. Near-ceiling performance on easy associations.

**Lesson.** Contributing a game to an existing maintained suite gives a longer life than launching a standalone benchmark. Controlled manipulation of item properties is a strong construct-validity pattern worth reusing in non-game benchmarks.

---

### Cross-cutting synthesis: why these five did or did not stick

| Factor | Qi Town | Game Reasoning Arena | MastermindEval | Concept | Codenames (Hakimov) |
|---|---|---|---|---|---|
| Venue | arXiv only (none found) | arXiv only | ICLR'25 workshop | Findings ACL 2026 | ACL'25 GEM² workshop |
| Public code | none found | yes (9 stars) | yes (10 stars) + lm-eval harness | dataset on HF; no repo found | yes, inside clembench |
| Maintained leaderboard | no | HF Space, personal, stale | no | no | yes (clembench ladder) |
| Maintenance after paper | none visible | stopped ~11 Sep 2025 | yes, through Aug 2026 | n/a (new) | yes, via clembench |
| Pre-empted by | Kaggle Game Arena (same week); LLM Chess; grid-games benchmark | Kaggle Game Arena (same day, same OpenSpiel substrate) | Bulls-and-Cows community leaderboard (Nov 2024, 236 stars) [corrected by fact-check: weak pre-emption. The MastermindEval repo predates it, and it was itself saturated by o3-mini and inactive from 1 Feb 2025.] | crowded word-game niche | Stephenson et al. (Dec 2024); 49 GitHub repos |
| Headroom | low (solved/simple games) | low vs random bots | tunable (good) | high (humans >90% vs LLMs <40%) | moderate (best 49%) |
| Human baseline | none found | none | none | yes | no (mock opponent) |
| Tool-solvability risk | high for Tic-Tac-Toe | high for small games | very high (brute force) | low | low |
| Single headline score | no (Elo/PLG/PSS) | no | solve rate (yes) | success rate (yes) | clemscore (yes, inside clembench) |

Takeaways from the table (my interpretation, grounded in the evidence above):
1. **Distribution beats design.** The two items with an afterlife, MastermindEval via lm-eval-harness and Codenames via clembench, both plugged into an existing, maintained evaluation channel. The two clear failures, Qi Town and Game Reasoning Arena, had no channel and faced a Google-backed incumbent.
2. **Timing and incumbent risk is decisive** in hot niches. Kaggle Game Arena effectively closed "LLMs play classic board games" as a space for small academic entrants in Aug 2025.
3. **Maintenance is the hidden cost.** The community projects that gained traction (Elimination Game with 61 models through Jan 2026; LLM Chess with 1,430 commits) show that continuous re-running with frontier models is what makes a ladder matter.
4. **Construct validity matters for scientific value but not, by itself, for adoption.** Concept has the best construct and headroom story of the five but no distribution. Whether it is adopted will depend on whether someone runs it on new models.
5. **Scientific usefulness is not the same as leaderboard success.** Items 3, 4 and 5 each produced reusable findings: where deduction breaks, human-LLM abduction gaps, and which lexical properties hurt association. Judging them only as failed leaderboards is too harsh.

---

## Implications for designing a new benchmark

1. **Plan distribution before design.** Ship as a task in at least one standard harness (EleutherAI lm-evaluation-harness, and ideally a hosted or agentic harness) from day one. MastermindEval's harness integration is why it is still used.
2. **Commit to maintenance with a named owner and a budget.** Re-run new frontier models within weeks of release. A stale ladder is a dead ladder (compare Game Reasoning Arena's commit cliff with Kaggle Game Arena's expansion and Elimination Game's regular additions).
3. **Report one headline number with decomposable sub-scores, and keep non-capability measures out of the headline.** Qi Town's Elo/PLG/PSS split and Kaggle's later move to a unified leaderboard both argue for this.
4. **Near-zero friction.** Use `pip install` or an API-only harness with no native builds (Game Reasoning Arena required building OpenSpiel from source plus conda plus four API keys). Offer hosted runs if possible.
5. **Procedural generation with parametric difficulty,** as in MastermindEval, to resist contamination and permit rescaling when the benchmark saturates. But **choose tasks that are not trivially brute-forceable by a short program**, or explicitly define a tool-use policy and score both with and without tools.
6. **Human baselines and a demonstrated large human-model gap** (Concept: over 90% vs. under 40%) are the most persuasive headroom evidence. Report them with confidence intervals.
7. **Controlled item-property manipulations** (Codenames: abstract vs. concrete, ambiguous vs. monosemic, opponent speed) turn a score into a diagnostic and strengthen construct validity. Build these factors into the item generator.
8. **Statistical adequacy.** Enough items or matches per model and pair for tight intervals (Kaggle: more than 100 matches per pair; Bulls-and-Cows: Wilson intervals). Publish the intervals on the leaderboard.
9. **Check the landscape and incumbents before committing.** Search GitHub and arXiv for the construct, and expect that big-lab platforms will enter hot niches. Differentiate on construct rather than on surface (a new game or a new visualisation is not differentiation).
10. **Tie the construct to real-world referents** such as intent inference, hypothesis revision and multilingual robustness, so that the "no product needs it" objection cannot be made.
11. **Legibility and shareability drive adoption** (AI Diplomacy's visualiser and Twitch module; Kaggle chess on chess.com). For a non-game benchmark, the analogue is inspectable, shareable per-item transcripts and failure examples.
12. **Clear licensing** (permissive, unambiguous). A CC BY-NC or ambiguous licence deters industry evaluators.

---

## Claims ledger

1. arXiv:2508.04720 is "Who is a Better Player: LLM against LLM" by Yingjie Zhou and 12 co-authors (including Guangtao Zhai), submitted 5 Aug 2025. It introduces Qi Town, with 5 games (Gomoku, Chess, Reversi, Tic-Tac-Toe and Free-Style) and 20 LLMs, measured with Elo, a Performance Loop Graph and a Positive Sentiment Score. Sources: https://arxiv.org/abs/2508.04720 ; https://www.researchgate.net/publication/394304950_Who_is_a_Better_Player_LLM_against_LLM ; https://www.emergentmind.com/papers/2508.04720. **Confidence: high** for identity and design; **medium** for the exact submission date.
2. In Qi Town, Gemini 2.0-Flash had the highest average Elo, followed closely by GPT-4.1, over about 2,850 games. Source: search summaries of https://arxiv.org/abs/2508.04720 and https://bytez.com/docs/arxiv/2508.04720/paper. **Confidence: medium** for the ranking; **low-medium** for the game count. Verify in the PDF. [corrected by fact-check: Gemini-2.0-Flash at the top and the 2,850 matches (= 190 pairs x 5 games x 3 repetitions) are corroborated by a second AI-generated digest, so confidence for those is medium. The GPT-4.1 runner-up claim remains single-source and unverified.]
3. No public GitHub repository for Qi Town was found (GitHub repository search for "Qi Town LLM board game" and "qitown" returned 0 results on 2026-09-29). Source: GitHub search API. **Confidence: medium.** Absence of evidence; code could be hosted elsewhere.
4. arXiv:2508.03368 (Cipolina-Kun, Nezhurina and Jitsev; LAION and Jülich Supercomputing Centre) was titled "Board Game Arena..." in v1 and renamed "Game Reasoning Arena..." in later versions. It wraps OpenSpiel games and is compared against random, heuristic and RL agents. Sources: https://arxiv.org/abs/2508.03368 ; https://arxiv.org/pdf/2508.03368v1 ; https://laion.ai/blog/reasoning_game_arena_blog_post/. **Confidence: high.**
5. The Game Reasoning Arena repo was created 4 Aug 2025 and has 9 stars and 4 forks. Its most recent commits on main are dated 7-11 Sep 2025, and installation requires conda plus a separate OpenSpiel clone and `./install.sh`. Sources: https://github.com/SLAMPAI/game_reasoning_arena ; https://github.com/SLAMPAI/game_reasoning_arena/commits/main ; https://raw.githubusercontent.com/SLAMPAI/game_reasoning_arena/main/README.md. **Confidence: high.**
6. Kaggle Game Arena (Google DeepMind and Kaggle) launched 4 Aug 2025 with a chess exhibition on 5-7 Aug 2025, won by o3 over Grok 4. It added Poker and Werewolf plus a unified leaderboard in Feb 2026, and its harness is built on OpenSpiel. Sources: https://siliconangle.com/2025/08/04/google-deepmind-host-ai-chess-tournament-evaluate-leading-ai-models-reasoning-skills/ ; https://www.chess.com/news/view/kaggle-game-arena-chess-2025-day-3 ; https://gigazine.net/gsc_news/en/20260203-google-kaggle-game-arena-poker-and-werewolf/ ; https://github.com/google-deepmind/game_arena. **Confidence: high.**
7. Kaggle Game Arena's technical report is arXiv:2609.31473 ("Game Arena: Strategic LLM Evaluation in Competitive Environments"), submitted 25 Sep 2026, with pilot environments Chess, Poker and Werewolf. Source: https://arxiv.org/abs/2609.31473. **Confidence: medium-high.**
8. MastermindEval (Golde, Haller, Barth and Akbik; arXiv:2503.05891) appeared at the ICLR 2025 Workshop on Reasoning and Planning for LLMs. It has agentic, deductive and log-likelihood multiple-choice paradigms, and reports that even easy instances are hard for models. Sources: https://arxiv.org/abs/2503.05891 ; https://openreview.net/pdf?id=H4donosutm ; https://github.com/flairNLP/mastermind. **Confidence: high.**
9. MastermindEval was added to EleutherAI lm-evaluation-harness as 6 tasks (mastermind_24/35/46 in easy and hard variants) in commit "Add MastermindEval (#2788)" on 18 Mar 2025. The flairNLP repo received commits through 4 Aug 2026. Sources: https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks/mastermind ; https://github.com/EleutherAI/lm-evaluation-harness/commits/main/lm_eval/tasks/mastermind ; https://github.com/flairNLP/mastermind/commits/main. **Confidence: high.**
10. MastermindEval's dataset comprises more than 30,000 pre-played game states generated with Knuth's algorithm. Source: https://www.themoonlight.io/en/review/mastermindeval-a-simple-but-scalable-reasoning-benchmark (secondary). **Confidence: medium.** [corrected by fact-check: the 30,000 figure is unverified, because the source is blocked and no second source was found; confidence is now low. The Knuth-algorithm pre-play is confirmed by the lm-eval-harness README.]
11. A community Bulls-and-Cows (Mastermind-type) LLM benchmark, stalkermustang/llm-bulls-and-cows-benchmark, was created 26 Nov 2024 and has 236 stars and Wilson confidence intervals. Source: https://github.com/stalkermustang/llm-bulls-and-cows-benchmark. **Confidence: high.** [corrected by fact-check: the facts are confirmed, but the repo has been inactive since its 1 Feb 2025 commit "o3-mini saturated the benchmark....". flairNLP/mastermind was created earlier, on 15 Nov 2024.]
12. arXiv:2510.13271, "Do You Get the Hint? Benchmarking LLMs on the Board Game Concept" (Gevers and Daelemans), was posted 15 Oct 2025 and published in Findings of ACL 2026. Humans exceed 90% success, no LLM exceeds 40%, and performance drops in Dutch, French and Spanish. Sources: https://arxiv.org/abs/2510.13271 ; https://aclanthology.org/2026.findings-acl.1219/. **Confidence: high** for venue and results; **medium** for the exact date.
13. arXiv:2502.11707 (Hakimov, Pfennigschmidt and Schlangen) was published at the GEM² workshop at ACL 2025. Of 14 models, the best (o3-mini) reached a 49% win rate. Sources: https://aclanthology.org/2025.gem-1.63/ ; https://arxiv.org/abs/2502.11707 ; https://en.papernotes.org/ACL2025/llm_evaluation/ad-hoc_concept_forming_in_the_game_codenames_as_a_means_for_evaluating_large_lan/. **Confidence: high** for venue; **medium** for the numbers.
14. "Codenames as a Benchmark for Large Language Models" (Stephenson, Sidji and Ronval; arXiv:2412.11373) was submitted 16 Dec 2024, about two months before arXiv:2502.11707. Source: https://arxiv.org/abs/2412.11373. **Confidence: high.**
15. The Codenames game is part of the maintained clembench suite (a `codenames/` directory in clp-research/clembench), which has a public leaderboard with benchmark versions v2.0 and v3.0. Sources: https://github.com/clp-research/clembench ; https://github.com/clp-research/clembench/tree/main/codenames ; https://benchmarklist.com/benchmarks/clembench_text_v3/ ; https://github.com/clembench. **Confidence: high** for inclusion; **medium** for the version details.
16. GitHub repository search returns 49 repos for "codenames llm" and 173 for "llm game benchmark" (2026-09-29), indicating a saturated niche. Source: GitHub search API. **Confidence: high** for the counts at that date.
17. Community game benchmarks with sustained maintenance gained more traction than the academic items above: AI_Diplomacy (707 stars), lechmazur/elimination_game (298 stars; 61 models including GPT-5.2 and Opus 4.5) and maxim-saplin/llm_chess (133 stars, 1,430 commits). Sources: https://github.com/GoodStartLabs/AI_Diplomacy ; https://github.com/lechmazur/elimination_game ; https://github.com/maxim-saplin/llm_chess. **Confidence: high.** [corrected by fact-check: all counts are confirmed. llm_chess is clearly active, with 52 commits since 1 Jun 2026. The elimination_game README's last update entry is 6 Jan 2026. Bulls-and-Cows should not be counted in this group (see item 11).]

---

## References

(Each entry was seen in a search result or fetched page in this session. "Seen at" gives where.)

1. Zhou, Y., et al. (13 authors). "Who is a Better Player: LLM against LLM." arXiv:2508.04720, 2025. https://arxiv.org/abs/2508.04720
2. Cipolina-Kun, L., Nezhurina, M., Jitsev, J. "Game Reasoning Arena: A Framework and Benchmark for Assessing Reasoning Capabilities of Large Language Models via Game Play" (v1: "Board Game Arena: ..."). arXiv:2508.03368, 2025. https://arxiv.org/abs/2508.03368
3. SLAMPAI/game_reasoning_arena, GitHub repository. https://github.com/SLAMPAI/game_reasoning_arena
4. Cipolina-Kun, L., Nezhurina, M., Jitsev, J. "Game Reasoning Arena: Inside the Mind of AI: How LLMs Think, Strategize, and Compete in Real-Time." LAION blog, 4 Aug 2025. [corrected by fact-check: full title from the blog source, github.com/LAION-AI/laion.ai] https://laion.ai/blog/reasoning_game_arena_blog_post/
5. Game Reasoning Arena Hugging Face Space (lcipolina). https://huggingface.co/spaces/lcipolina/game_reasoning_arena (seen in search results only)
6. Golde, J., Haller, P., Barth, F., Akbik, A. "MastermindEval: A Simple But Scalable Reasoning Benchmark." ICLR 2025 Workshop on Reasoning and Planning for LLMs; arXiv:2503.05891. https://arxiv.org/abs/2503.05891 ; https://openreview.net/forum?id=H4donosutm
7. flairNLP/mastermind, GitHub repository. https://github.com/flairNLP/mastermind
8. EleutherAI lm-evaluation-harness, MastermindEval tasks. https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks/mastermind
9. Moonlight literature review of MastermindEval (secondary). https://www.themoonlight.io/en/review/mastermindeval-a-simple-but-scalable-reasoning-benchmark
10. Gevers, I., Daelemans, W. "Do You Get the Hint? Benchmarking LLMs on the Board Game Concept." Findings of ACL 2026; arXiv:2510.13271. https://aclanthology.org/2026.findings-acl.1219/
11. IneG/concept dataset (Hugging Face). https://huggingface.co/datasets/IneG/concept (seen in search results only)
12. Hakimov, S., Pfennigschmidt, L., Schlangen, D. "Ad-hoc Concept Forming in the Game Codenames as a Means for Evaluating Large Language Models." GEM² Workshop at ACL 2025; arXiv:2502.11707. https://aclanthology.org/2025.gem-1.63/
13. Stephenson, M., Sidji, M., Ronval, B. "Codenames as a Benchmark for Large Language Models." arXiv:2412.11373, 2024. https://arxiv.org/abs/2412.11373
14. clp-research/clembench, GitHub repository (includes codenames). https://github.com/clp-research/clembench
15. Chalamalasetti, K., Götze, J., Hakimov, S., Madureira, B., Sadler, P., Schlangen, D. "clembench: Using Game Play to Evaluate Chat-Optimized Language Models as Conversational Agents." EMNLP 2023 (2023.emnlp-main.689); arXiv:2305.13455. [corrected by fact-check: venue and authors added] https://arxiv.org/abs/2305.13455
16. Beyer, A., Chalamalasetti, K., Hakimov, S., Madureira, B., Sadler, P., Schlangen, D. "clembench-2024: A Challenging, Dynamic, Complementary, Multilingual Benchmark and Underlying Flexible Framework for LLMs as Multi-Action Agents." arXiv:2405.20859, 2024. [corrected by fact-check: full title and authors] https://arxiv.org/abs/2405.20859
17. Schlangen, D., Hakimov, S., Jordan, J., Sadler, P. "A Third Paradigm for LLM Evaluation: Dialogue Game-Based Evaluation using clembench." arXiv:2507.08491, 2025. [authors added by fact-check] https://arxiv.org/abs/2507.08491
18. benchmarklist.com, Clembench Text v3.0 page (secondary). https://benchmarklist.com/benchmarks/clembench_text_v3/
19. SiliconANGLE, "Google's Kaggle to host AI chess tournament ...", 4 Aug 2025. https://siliconangle.com/2025/08/04/google-deepmind-host-ai-chess-tournament-evaluate-leading-ai-models-reasoning-skills/
20. Chess.com, "OpenAI's o3 Crushes Grok 4 In Final, Wins Kaggle's AI Chess ..." https://www.chess.com/news/view/kaggle-game-arena-chess-2025-day-3
21. Gigazine, "Google adopts Werewolf and Poker in AI benchmark 'Game Arena'", 3 Feb 2026. https://gigazine.net/gsc_news/en/20260203-google-kaggle-game-arena-poker-and-werewolf/
22. WinBuzzer, "Gemini 3 Tops All Kaggle Leaderboards as Game Arena Adds Poker ...", 4 Feb 2026. https://winbuzzer.com/2026/02/04/deepmind-game-arena-poker-werewolf-gemini-3-tops-rankings-xcxwbn/
23. Doerschuk-Tiberi, B., Yan, Y., Chiu, J., et al. (Google DeepMind and Kaggle). "Game Arena: Strategic LLM Evaluation in Competitive Environments." arXiv:2609.31473, 2026. [authors added by fact-check] https://arxiv.org/abs/2609.31473
24. google-deepmind/game_arena, GitHub repository. https://github.com/google-deepmind/game_arena
25. Topsakal, O., Edell, C. J., Harper, J. B. "Evaluating Large Language Models with Grid-Based Game Competitions: An Extensible LLM Benchmark and Leaderboard." arXiv:2407.07796, 2024 [authors added by fact-check]; repo research-outcome/LLM-Game-Benchmark. https://arxiv.org/abs/2407.07796 ; https://github.com/research-outcome/LLM-Game-Benchmark
26. maxim-saplin/llm_chess, GitHub repository and leaderboard; "LLM CHESS: Benchmarking Reasoning and Instruction-Following in LLMs through Chess", arXiv:2512.01992. https://github.com/maxim-saplin/llm_chess
27. stalkermustang/llm-bulls-and-cows-benchmark, GitHub repository. https://github.com/stalkermustang/llm-bulls-and-cows-benchmark
28. Zhang, Y., Wang, M., Li, X., Ren, K., Zhu, C., Naseem, U. "TurnBench-MS: A Benchmark for Evaluating Multi-Turn, Multi-Step Reasoning in Large Language Models." Findings of EMNLP 2025; arXiv:2506.01341. https://aclanthology.org/2025.findings-emnlp.1084/
29. GoodStartLabs/AI_Diplomacy, GitHub repository. https://github.com/GoodStartLabs/AI_Diplomacy
30. lechmazur/elimination_game, GitHub repository. https://github.com/lechmazur/elimination_game
31. ilya-aby/llm-codenames, GitHub repository. https://github.com/ilya-aby/llm-codenames
32. Wang, H., Li, X., Niu, Y., Hu, S., Li, H. "MasterMind: Empowering LLMs in Decision Games through Algorithmic Data Synthesis" (ICLR 2025 SynthData Workshop; arXiv:2503.13980; games are Doudizhu and Go). [authors/ID added by fact-check] https://github.com/opendilab/Mastermind
33. Ansell, R., Toney-Wails, A. "Clueing up LLMs with Tool-Augmented Deductive Reasoning." arXiv:2609.18736, 2026. https://arxiv.org/abs/2609.18736
34. "GameArena: Evaluating LLM Reasoning through Live Computer Games." ICLR 2025; arXiv:2412.06394. https://arxiv.org/abs/2412.06394
35. "KORGym: A Dynamic Game Platform for LLM Reasoning Evaluation." arXiv:2505.14552, 2025. https://arxiv.org/abs/2505.14552
36. Lin et al. "GAMEBoT: Transparent Assessment of LLM Reasoning in Games." ACL 2025 (2025.acl-long.378). [Anthology ID confirmed by fact-check] https://aclanthology.org/2025.acl-long.378.pdf ; https://github.com/Visual-AI/GAMEBoT
37. "lmgame-Bench: How Good are LLMs at Playing Games?" arXiv:2505.15146, 2025. [title casing corrected by fact-check] https://arxiv.org/abs/2505.15146
38. "GTBench: Uncovering the Strategic Reasoning Limitations of LLMs via Game-Theoretic Evaluations." arXiv:2402.12348, 2024. https://arxiv.org/abs/2402.12348
39. "SPIN-Bench: How Well Do LLMs Plan Strategically and Reason Socially?" arXiv:2503.12349, 2025. https://arxiv.org/abs/2503.12349

### Open items (not verified because the session search budget ran out)
- Qi Town: exact Elo table, full model list, whether frontier reasoning models were included, and any code link inside the PDF.
- Concept: number of games or items, models evaluated, data source (human game logs?) and any code repository.
- Codenames ad-hoc: exact arXiv submission day and the full 14-model list.
- Citation counts for all five papers (none visible in any search result).
- Which licence applies to Game Reasoning Arena (MIT vs. CC BY-NC 4.0).

---

## Verification log

Adversarial fact-check, 2026-09-29. **Method constraint:** the session's WebSearch budget was already exhausted (200/200) when this check started, and arxiv.org, aclanthology.org, openreview.net, huggingface.co, laion.ai, chess.com, siliconangle.com, gigazine.net, benchmarklist.com, themoonlight.io, alphaxiv.org and bytez.com were all blocked. Verification therefore used independent routes:
- The GitHub API via the GitHub MCP: repository metadata, commit search and code search.
- Raw GitHub files: READMEs, CHANGELOGs, the ACL Anthology source XML (acl-org/acl-anthology) and the LAION blog source (LAION-AI/laion.ai).
- arXiv-metadata mirrors hosted on GitHub: arXiv daily digests (CSQianDong/Awesome-arXiv-Daily-Reporter, LIHUA919/AI-Agents-Daily-Research, Luvata/arxive, Lcollection/Arxiv_Daily), ArXCompass (arXiv-API dates) and MystenLabs/snowreads (raw arXiv version metadata).

AI-generated paper digests (memgrafter/research-digests, zhaoyang97/Paper-Notes) are treated as weak secondary evidence.

| ID | Verdict | Evidence | Sources |
|---|---|---|---|
| C1 | **Confirmed** | Title, the 13-author list (Zhou ... Zhai) and ID match in several arXiv digest mirrors. The abstract confirms Qi Town, "5 widely played games", "20 LLM-driven players", Elo + Performance Loop Graph + Positive Sentiment Score, and a round-robin design. v1 is dated 2025-08-05 (ArXCompass). The game list (Gomoku, Chess, Reversi, Tic-Tac-Toe, Free-Style) is corroborated by a secondary digest. "12 organizations" was **not** independently confirmed. | github.com/CSQianDong/Awesome-arXiv-Daily-Reporter (8-Aug-2025/AI/papers.jsonl); github.com/ArXCompass/ArXCompass.github.io (papers/llm/2025_08/papers_11.md); raw.githubusercontent.com/memgrafter/research-digests/main/ml_research_analysis_2025/2508.04720_who-is-a-better-player-llm-against-llm_20260210_183413.md |
| C2 | **Unverifiable (partially corroborated)** | A second, independent AI digest agrees that Gemini-2.0-Flash had the highest average Elo and that 2,850 matches were played (3 repetitions per game; 190 pairs x 5 x 3 = 2,850). The claim that GPT-4.1 "followed closely" is found in no source other than the original search summaries. The PDF could not be opened. | memgrafter digest (above) |
| C3 | **Confirmed** (minor wording fix) | The v1 title "Board Game Arena: A Framework and Benchmark for Assessing Large Language Models via Strategic Play", the authors, OpenSpiel wrapping, and comparisons with random, human and RL agents are all in the v1 abstract. The abstract does not say "heuristic". JSC funding appears in the README and the LAION blog. The later title is confirmed in the repo README. | github.com/LIHUA919/AI-Agents-Daily-Research data/2025-08-06.md; CSQianDong 6-Aug-2025; raw.githubusercontent.com/SLAMPAI/game_reasoning_arena/main/README.md; raw.githubusercontent.com/LAION-AI/laion.ai/main/blog/reasoning_game_arena_blog_post.md |
| C4 | **Confirmed** | GitHub API: created 2025-08-04T11:44Z, pushed_at 2025-09-11T20:26Z, 9 stars, 4 forks; 209 commits. The README install steps (conda env, pip -e, clone open_spiel plus ./install.sh, .env with 4 API keys) are confirmed. Extra finding: the README text states CC BY-NC 4.0, while MIT appears only in a badge. | GitHub MCP search_repositories; github.com/SLAMPAI/game_reasoning_arena |
| C5 | **Confirmed** (one sub-claim single-source) | The 3-day, 8-model AI chess exhibition kicking off Kaggle Game Arena (AINews 2025-08-05) and o3 beating Grok 4 in the final (digest of the @kaggle post, 2025-08-07) are corroborated. The harness "uses OpenSpiel" (repo README; 115 stars; created 2025-07-29). Poker and Werewolf in early Feb 2026 are corroborated by an independent timeline. The "unified leaderboard" rests only on the blocked Gigazine and WinBuzzer items. Tech report arXiv:2609.31473 (2026-09-25) is confirmed. | github.com/smol-ai/ainews-web-2025 (frozen-issues/25-08-05-gpt-oss.md); github.com/dshayan/sumbird (docs/en/news/2025-08-07); raw.githubusercontent.com/google-deepmind/game_arena/main/README.md; github.com/guzus/ai-research-arm; github.com/luohongk/Embodied-AI-Daily papers/LLM.md |
| C6 | **Confirmed** | The venue is confirmed by the BibTeX in the lm-eval task README and the flairNLP README ("Workshop on Reasoning and Planning for Large Language Models", OpenReview H4donosutm) and by the repo description ("@ ICLR 2025 Workshop on Reasoning and Planning of LLMs"). Knuth-algorithm pre-play is confirmed in the lm-eval README. The abstract mirror confirms "even easy Mastermind instances are difficult". Note that the abstract names two paradigms; the MC/log-likelihood paradigm comes from the README. | raw.githubusercontent.com/EleutherAI/lm-evaluation-harness/main/lm_eval/tasks/mastermind/README.md; raw.githubusercontent.com/flairNLP/mastermind/main/README.md; github.com/HuggingAGI/HuggingArxivLLM (2025-03-07) |
| C7 | **Confirmed** | Commit f47ddaf "Add MastermindEval (#2788)" by Jonas Golde, 2025-03-18. The 6 tasks are listed. flairNLP/mastermind commits are dated 2026-03-20, 2026-05-12 and 2026-08-04 (pushed_at 2026-08-04). | GitHub commit search (EleutherAI/lm-evaluation-harness; flairNLP/mastermind) |
| C8 | **Corrected** | Created 2024-11-26, 236 stars and Wilson intervals are confirmed. **Corrections:**<br>(a) flairNLP/mastermind was created on 2024-11-15, *before* this repo, so the pre-emption framing is weak;<br>(b) the last commit, 2025-02-01, reads "o3-mini saturated the benchmark....", so the repo has been inactive since then;<br>(c) o1-mini's 60% is over 25 games, not about 50. | GitHub MCP search_repositories and search_commits; raw.githubusercontent.com/stalkermustang/llm-bulls-and-cows-benchmark/main/README.md |
| C9 | **Confirmed** | Authors and abstract (humans >90%, no model >40%, drops in Dutch, French and Spanish) are confirmed via digests. v1 is dated 2025-10-15 (ArXCompass) and v2 2026-01-07. Findings of ACL 2026, paper id 2026.findings-acl.1219, is in an ACL 2026 metadata dump. **Caveat** (secondary, AI digest): the evaluated models reportedly include GPT-4.1-mini, Llama-3.3-70B and GPT-OSS-120B (7 in total), so "no LLM exceeds 40%" should be cited as "no evaluated LLM". | CSQianDong 16-Oct-2025/NLP; github.com/smallflyingpig/ai-conference-overview (data/classification/acl/2026-findings/batches/batch-0007.json); ArXCompass 2025_10 |
| C10 | **Venue confirmed; numbers unverifiable** | ACL Anthology source XML: 2025.gem-1.63, in "Proceedings of the Fourth Workshop on Generation, Evaluation and Metrics (GEM²)", July 2025, Vienna. The author homepage confirms "Gem-Bench workshop @ ACL'25". The claim "14 models, o3-mini 49%" appears only in Paper-Notes, which is the same source family as en.papernotes.org, so it is not independent. That source frames 49.2 as a clemscore at 100% played rate. | raw.githubusercontent.com/acl-org/acl-anthology/master/data/xml/2025.gem.xml; github.com/sherzod-hakimov/sherzod-hakimov.github.io _pages/about.md; raw.githubusercontent.com/zhaoyang97/Paper-Notes/main/docs/ACL2025/llm_evaluation/ad-hoc_concept_forming_in_the_game_codenames_as_a_means_for_evaluating_large_lan.md |
| C11 | **Confirmed** | Raw arXiv metadata gives v1 created "Mon, 16 Dec 2024 01:59:03 GMT" and authors Stephenson, Sidji and Ronval. The abstract names GPT-4o, Gemini 1.5, Claude 3.5 Sonnet and Llama 3.1. 2502.11707 v1 was listed 2025-02-17, a gap of about 2 months. | raw.githubusercontent.com/MystenLabs/snowreads/main/data/abs/2412.11373.json; github.com/Lcollection/Arxiv_Daily docs/daily-papers/2025-02-17.md |
| C12 | **Confirmed** | The codenames/ directory in clp-research/clembench (master.py, scorer.py, instancegenerator.py, ...) is confirmed; 5 stars, 22 forks, MIT, last pushed 2026-04-26. The clembench-runs CHANGELOG shows codenames added in v2.0 (Mar 2025), and the repo has v2.0 and v3.0 directories. The leaderboard URL is on HF (colab-potsdam/clem-leaderboard). | GitHub MCP; raw.githubusercontent.com/clembench/clembench-runs/main/CHANGELOG.md; github.com/clembench/clembench-runs |
| C13 | **Confirmed** (reproduced exactly) | The GitHub repository search API on 2026-09-29 returns 49 for "codenames llm", 173 for "llm game benchmark", 0 for "qitown" and 0 for "Qi Town LLM board game". | GitHub MCP search_repositories |
| C14 | **Confirmed** (with nuance) | AI_Diplomacy: 707 stars. elimination_game: 298 stars, TrueSkill, 61 models, with GPT-5.2 1st, Claude Opus 4.5 Thinking 4th and Gemini 3 Flash 5th; last update entry 6 Jan 2026. llm_chess: 133 stars, 1,430 commits, live leaderboard at maxim-saplin.github.io/llm_chess, and 52 commits since 2026-06-01. | GitHub MCP; raw.githubusercontent.com/lechmazur/elimination_game/main/README.md; github.com/maxim-saplin/llm_chess |

**Verdict counts:** 11 confirmed (C1, C3, C4, C5, C6, C7, C9, C11, C12, C13, C14), 1 corrected (C8), 0 refuted, 2 unverifiable (C2 on the GPT-4.1 runner-up claim; C10 on the 14-models/49% numbers, although its venue is confirmed).

**Other in-body corrections made (non-ledger):**
- Game Reasoning Arena licence (the README text says CC BY-NC 4.0).
- "Heuristic" agents are not in the v1 abstract.
- The Bulls-and-Cows "traction" example has been retracted.
- Elimination Game has had no model additions since Jan 2026.
- MastermindEval's 30,000-states figure and the "o3-mini best" claim are downgraded to unverified.
- The Hakimov et al. v1 date is now filled in (17 Feb 2025).
- Clembench: codenames was added in v2.0 (Mar 2025).
- Qi Town design: 3 repetitions per pair per game.
- Concept data source and model roster, with the "no evaluated model" caveat.

### Reference-check summary

- **All 39 entries were checked (none skipped).** The JSON now carries `verified` and `verify_note` for each.
- **Verified: 32.** Every academic paper reference (arXiv IDs 2508.04720, 2508.03368, 2503.05891, 2510.13271, 2502.11707, 2412.11373, 2305.13455, 2405.20859, 2507.08491, 2609.31473, 2407.07796, 2512.01992, 2506.01341, 2609.18736, 2412.06394, 2505.14552, 2505.15146, 2402.12348, 2503.12349, 2503.13980, and ACL 2025.acl-long.378) matched on title and ID. No fabricated references were found.
- **Not verified: 7.** All are secondary or web items whose domains are blocked:
  - moonlight review;
  - IneG/concept HF dataset;
  - benchmarklist.com page;
  - SiliconANGLE, chess.com, Gigazine and WinBuzzer articles. The key claims from SiliconANGLE and chess.com are corroborated independently; the Gigazine and WinBuzzer "unified leaderboard" detail is not.
- **Fields corrected in the JSON:**
  - LAION blog title (adds "in Real-Time");
  - clembench-2024 full title and 6 authors (previously "unknown");
  - authors added for 2507.08491, 2407.07796, 2609.31473 and 2305.13455;
  - 2305.13455 venue (EMNLP 2023 main);
  - Hakimov et al. venue (full GEM² proceedings name);
  - opendilab MasterMind given arXiv:2503.13980 and authors;
  - GAMEBoT given ID 2025.acl-long.378;
  - lmgame-Bench title casing;
  - LLM Chess venue (NeurIPS 2025 FoRLM workshop per README).
- **Open items still unresolved:**
  - Qi Town: "12 organizations", the full Elo table, and the GPT-4.1 runner-up claim.
  - Codenames (2502.11707): the per-model table and the o3-mini vs DeepSeek-R1 gap.
  - MastermindEval: the 30,000 states and o3-mini results.
  - Concept: the number of games.
  - Kaggle's ">100 matches per pair".
  - Affiliations for Qi Town (SJTU) and Concept (Antwerp).
  - AI_Diplomacy's commit count (407).
  - Citation counts: none were verifiable.

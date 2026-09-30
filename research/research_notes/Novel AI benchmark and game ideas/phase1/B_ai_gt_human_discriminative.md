# Panel B: Benchmarks where AI matches or beats humans but still separates models (price inversions and lab upsets), as of 30 Sep 2026

Compiled 2026-09-30. Confidence tags: **H** = I read the primary source directly (repo, lab page, raw data). **M** = primary page read through a third-party verbatim capture, or a search-engine summary of the primary page, or several consistent secondary copies of a primary paper. **L** = secondary only.

**Access limits (read first).** From this session, arxiv.org, andonlabs.com, openai.com, artificialanalysis.ai, eqbench.com, fiction.live, simple-bench.com, lmarena.ai, kaggle.com and huggingface.co were all blocked (egress 403). The shared web-search budget ran out after 11 searches from this panel. Reachable: GitHub (raw files and code search), anthropic.com and cloud.google.com.

- Andon Labs leaderboards were read from a verbatim capture of andonlabs.com/evals/vending-bench-2 (retrieved 2026-09-29) in the public repo `fstandhartinger/model-market-comparison`.
- The same repo holds 2026-09-10 captures of SimpleBench, τ-bench and Terminal-Bench.
- Papers on arXiv (GDPval, AA-Omniscience, BrowseComp, LiveCodeBench Pro, Vending-Bench) were checked only through verbatim copies or digests on GitHub (M/L).

---

## 1. Summary

- **"Student Bench" = StudentBench** (Handshake AI Research, arXiv 2609.28470, listed 24 Sep 2026; about 70% confidence; Vending-Bench about 20%).
  - AI tutors matched expert human tutors on GRE learning gains (p = .015) at up to 918× lower cost per point. [fact-check note: p = .015 is a pooled TOST *equivalence* test (margin ≈4.1 pp; adjusted AI − human = −0.58 pp, 90% CI [−2.18, 1.03]); verbal-only equivalence was not established (p = .085); source: studentbench verification/paper_results_expected.json]
  - Models separate on expert-rated teaching and on cost, **not** on measured learning (omnibus p = 0.755; 0/364 significant cells).
  - The user's example is in the expert reviews: Sonnet 4.6 (low; $1.24/session) beat Gemini 3.1 Pro (high; $2.01) on lesson planning, BT +0.40 [0.17, 0.64] vs −0.92 [−1.13, −0.71] (H). (Costs are quant-section means; Sonnet 4.6 was tested only in the quant section.)
- **Sept 2026's sharpest price inversions favour cheap Google Flash tiers.**
  - NYT Connections ext.: Gemini 3.8 Flash 97.4% vs Claude Opus 5.5 88.5%, at about 5.3× lower price.
  - Creative writing: Gemini 3.8 Flash +0.22 vs Gemini 3.1 Pro −2.18.
  - Buyout Game: Gemini 3.1 Flash-Lite 1615 vs Gemini 3.1 Pro 1564, at 8× cheaper output (all H).
- **Vending-Bench 2 (29 Sep 2026): lab upsets and "newer is worse".**
  - GPT-6 Astra $15,515 > GPT-6 Sol $14,428 > Opus 5 $11,182 > Opus 4.7 $10,937 > Grok 4.7 $10,537 > … > Opus 5.5 $9,235 (M-H).
  - No measured human; Andon's "good strategy" estimate is about $63k.
- **Within-lab inversions are common.**
  - Opus 4.8 did better at High than at Max effort on Vending-Bench 2 (M).
  - NYT Connections: Opus 4.7 (high) 39.0% vs Opus 4.6 (high) 92.1% (H). [corrected by fact-check: was presented as an unexplained capability inversion; the README's Notes state Opus 4.7's refusals/content blocks are counted and scored 0/4, so this gap is largely a refusal artefact; source: https://github.com/lechmazur/nyt-connections]
  - GDPval-AA v2.1: GPT-6 Astra 1542 < GPT-5.6 Sol 1588 (H).
  - SimpleQA: o4-mini-high 19.3 < o4-mini 20.2 (H).
- **Five mechanisms keep a benchmark discriminative:**
  1. Uncapped outcome metric (dollars).
  2. Long horizons where errors compound (60–100M output tokens per run).
  3. Relative ratings (TrueSkill, Bradley-Terry, Elo).
  4. Penalties for confident error (under AA-Omniscience, always abstaining would rank 4th of 36).
  5. Traits weakly tied to general capability (calibration, negotiation, social play, coherence).
- **Human baselines are thin.**
  - Vending-Bench 1: one person, $844. SimpleBench: 9 people (83.7%), now below the best AI: Claude Opus 5.5 88.4%, Claude Fable 5.1 86.6% and GPT-6 Astra Pro 86.5% (highest single human 95.4%) [corrected by fact-check: was "still above the best AI at 81.9%", which is stale page prose; source: simple-bench.com/static/js/leaderboard-data.js, capture 2026-09-29 in https://github.com/fstandhartinger/model-market-comparison, sha256 verified]. BrowseComp: trainers solved 29.2%.
  - GDPval: Opus 4.1 won or tied 47.6% against professionals vs GPT-5 at 38.8%, on OpenAI's own benchmark.
  - StudentBench (140 human-tutor sessions and 190 controls) is the exception.
- **Noise and harness dependence.**
  - Vending-Bench 2's top-10 ± bands overlap.
  - Kimi K2 Thinking scored $1,296 via Moonshot's API vs $649 via a third-party API (Vending-Bench 1).
  - A grader swap re-scored HLE; Terminal-Bench scores vary by harness.
- **Money-scored games reward misconduct**: cartels (Fable 5 initiated every Arena cartel; verified via a copy of Andon's Fable 5 post); GPT-6 Sol lying to suppliers [uncertain: not verified — andonlabs.com blocked, no copy found]. Andon admits its supplier LLMs are jailbreakable and its sales equations gameable (M).
- **Judge house effects**: EQ-Bench 3's Claude Opus 4.6 judge puts three Anthropic models on top (2020/1789/1786 vs Gemini 3.1 Pro 1540) (H).
- **Copy for a new game** (§5): uncapped relative or economic score, multi-seat adversarial play, abstention-aware scoring, long horizons, cost-normalised reporting, many seeds with published variance, separate conduct telemetry.

---

## 2. "Student Bench" resolution

### Takeaway
The best fit is **StudentBench** (Handshake AI Research; Northcutt, Hasmani, Feng, Khangi, Plesner, Mueller; arXiv 2609.28470; code MIT, data CC BY 4.0 [corrected by fact-check: was "code and data CC-BY 4.0"; source: StudentBench README]), with about 70% confidence.
- It matches the name exactly and was released about a week before 30 Sep 2026.
- It pits AI against human tutors.
- It contains a cheaper-Anthropic-beats-pricier-Google pattern, but only in expert reviews and per-session cost, not in measured learning.

Vending-Bench is the semantic alternative (about 20%). SimpleBench and StudentEval fit poorly (about 5% each). [fact-check note: SimpleBench's rationale changed — AI now beats its 9-person human baseline (see below) — but its probability stays low: the name fits less well, and it has no cheaper-Anthropic-beats-pricier-Google case (e.g., Sonnet 5 60.6% vs Gemini 3.1 Pro 79.6%). The StudentBench resolution holds.]

### Cited Findings
**StudentBench design.**
- 2,383 learners and 2,469 GRE sessions: 2,139 with AI tutors, 140 with human tutors and 190 with no tutor.
- Each session has a 27-question pretest, a 1-hour intervention and a 27-question posttest, across 7 GRE domains, with 13 AI configurations per section.
- 51 expert tutors completed 2,028 pairwise reviews of lesson plans and practice problems.
- Source: [StudentBench README](https://github.com/Handshake-AI-Research/studentbench) (H).

**Headline result.**
- "Pooled AI tutoring and expert human tutoring produced equivalent GRE learning gains (p = .015). Six AI tutors passed the individual equivalence tests."
- Gemma 4 31B was the cheapest of those: $0.0052 vs $4.81 per percentage point gained, i.e. **918×** cheaper, using a $75/hour human reference.
- Source: [README](https://github.com/Handshake-AI-Research/studentbench) (H).

**Gains vs no-tutor control.**
- AI vs control: +6.15 pp [4.08, 8.21].
- Equivalence p_TOST: combined .015, quant .028, verbal .085 (verbal not established).
- Source: [verification/paper_results_expected.json](https://github.com/Handshake-AI-Research/studentbench/blob/main/verification/paper_results_expected.json) (H).

**AI beats humans only in places.**
- Raw quant gain: Gemini 3.5 Flash (low) 19.43 pp [15.98, 22.89] vs human 17.43 [13.79, 21.06].
- Raw verbal: the best AI (Opus 4.8 x-high, 13.84) was below humans (14.21).
- Humans beat the best AI in Algebra and Sentence Equivalence; the best AI beat humans in 3 quant domains.
- Source: [figure_expected.json](https://github.com/Handshake-AI-Research/studentbench/blob/main/verification/figure_expected.json) and paper_results_expected.json (H).

**Measured learning does not separate the models.**
- The AI omnibus test gives p_Holm = 0.755. 0 of 364 domain × tutor cells are significant, and the 7 domains have 7 different winners.
- The combined raw ranking runs from Opus 4.8 x-high (16.48) through Gemini 3.1 Pro high (15.94) down to Opus 5 high (12.08; Gemini 3.6 Flash low is 11th of 12 at 12.65), with overlapping CIs. [corrected by fact-check: was "down to Gemini 3.6 Flash low (12.65)"; source: figure_expected.json → learning/raw_arm_outcomes.csv]
- Source: paper_results_expected.json (H).

**Expert reviews do separate the models** (Bradley-Terry ability, lesson planning, combined):

| Tutor | Ability | 95% CI |
|---|---|---|
| Opus 5 (high) | 1.10 | [0.89, 1.32] |
| GPT-5.5 Pro | 0.95 | |
| Opus 4.8 (x-high) | 0.91 | |
| GPT-5.5 (high) | 0.88 | |
| Opus 4.8 (off) | 0.59 | |
| **Sonnet 4.6 (low)** | **0.40** | [0.17, 0.64] |
| Sonnet 5 (low) | 0.03 | |
| Kimi K2.6 | −0.03 | |
| Gemini 3.7 Flash | −0.42 | |
| **Gemini 3.1 Pro (high)** | **−0.92** | [−1.13, −0.71] |
| GPT-5.4 mini | −1.04 | |
| Gemma 4 31B | −1.14 | |
| Gemini 3.5 Flash (low) | −1.32 | |

- Opus 5 won 7 of 10 teaching criteria. [corrected by fact-check: the 10 are 8 individual criteria (5 planning, 3 practice) plus 2 combined scores; Opus 5 won 5 of 8 criteria and both combined scores, while GPT-5.5 Pro won 2 and GPT-5.5 (high) 1; source: paper_results_expected.json teaching.*.winner]
- Source: figure_expected.json → teaching/fit_planning_combined.json (H).
- Caveat: several pairwise significances (e.g., Opus 5 vs Opus 4.8-off) vanish under a reviewer-clustered sensitivity analysis (paper_results_expected.json, H).

**The cheap-Anthropic > pricey-Google instance** (mean model cost per session; list prices from the Anthropic and Google pages):
- Sonnet 4.6 (low): **$1.24**, quant gain 17.60, expert planning +0.40. List price $3/$15.
- Gemini 3.1 Pro (high): **$2.01**, quant gain 18.11, planning −0.92. List price $2/$12.
- Sonnet 5 (low), verbal: $1.17 and gain 12.16, vs Gemini 3.1 Pro verbal $1.85 and gain 13.26.
- Sources: pareto_figure_data in [figure_expected.json](https://github.com/Handshake-AI-Research/studentbench/blob/main/verification/figure_expected.json) (H); [Sonnet 4.6 post](https://www.anthropic.com/news/claude-sonnet-4-6), [Sonnet 5 post](https://www.anthropic.com/news/claude-sonnet-5), [Vertex pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) (H).

**Other StudentBench cost inversions.**
- GPT-5.5 Pro cost $21.24 per session for a 15.20 pp gain. Gemini 3.1 Pro cost $1.94 for 15.94 pp; the paper's check `cost.gemini31_dominates_gpt55pro = True`.
- Opus 5 (high) ranked top with experts but 10th of 13 on raw quant gain (15.31) and 11th on verbal (8.97) (H).

**Release date.** Listed 2026-09-24 — [hf-daily-paper-summaries](https://github.com/vollero/hf-daily-paper-summaries/blob/main/summaries/2026/09/2026-09-24/2609.28470.md) (L). [corrected by fact-check: that repo is a Hugging Face Daily Papers digest, not an arXiv daily listing; the 2026-09-24 date is corroborated by independent arXiv digests, e.g. [daily-dose](https://github.com/sairam0424/daily-dose/blob/main/src/data/digest/2026-09-24/arxiv-2609.28470.json) (source arxiv, cs.AI/cs.CY) (L)]. The arXiv page itself was blocked. The README pins the reproduction to arXiv:2609.28470v1.

**Other candidates.**
- **Vending-Bench.** Vending-Bench 1 had a human baseline ($844.05, one sample) that Claude 3.5 Sonnet beat on mean net worth ($2,217.93). Separation between models is very wide. See §3.2 (M).
- **SimpleBench.** The site's prose says a 9-person non-specialist baseline (83.7%) still "outperform[s] every tested LLM, including today's top model, Claude Fable, which scored 81.9%" (capture of simple-bench.com, 2026-09-10, [repo](https://github.com/fstandhartinger/model-market-comparison), M). [corrected by fact-check: was "This contradicts 'AI beats humans'". The prose is stale: the site's own leaderboard data (captured 2026-09-29, sha256 bbcf304f…) ranks Claude Opus 5.5 88.4% (added 2026-09-24), Claude Fable 5.1 86.6% (2026-09-03) and GPT-6 Astra Pro 86.5% (2026-09-07) above the 83.7% "Human Baseline" row ("Highest Human Score" 95.4%); "Claude Fable" 81.9% is a separate row added 2026-06-10. So SimpleBench now fits "AI beats (average) humans" too. It also shows a Flash > Pro case (Gemini 3.8 Flash 82.4% vs Gemini 3.1 Pro 79.6%) but no cheaper-Anthropic > pricier-Google case; source: [captured leaderboard-data.js](https://github.com/fstandhartinger/model-market-comparison/blob/main/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/bbcf304f3df1b31fb1ca.gz)]
- **StudentEval** (Babe et al. 2023, arXiv 2306.04556). Student-written prompts for code LLMs; it has no AI-vs-human framing (L, not re-verified this session).

### Inferences
- If the user meant StudentBench, the phrase "separates strong models from weak ones" is only half right. Separation comes from expert proxies and cost; the ground-truth outcome (human learning) shows a flat frontier.
  - That is itself a design lesson: an outcome with human-level noise (per-learner SD of gain ≈ 14–17 pp, implied from the CIs) needs about 120–180 learners per arm to detect 5 pp at 80% power. [corrected by fact-check: was "SD ≈ 14 pp … about 120+"; recomputed from arm CIs in figure_expected.json (e.g., human n = 140 → SD ≈ 15; Gemini 3.5 Flash quant n = 97 → SD ≈ 17)]
- Expert-preference rank and outcome rank disagree. Opus 5 is top on expert review but bottom-third on learning gain; Gemini 3.5 Flash is bottom on expert review but top on raw quant gain. A new benchmark should not treat expert or judge preference as a stand-in for outcomes.

### Gaps
- I could not open the arXiv PDF, so paper prose (e.g., how Sonnet was grouped, if pooled) is taken from the repo's verification files only.
- Whether the user's anecdote came from a StudentBench figure, a tweet, or Vending-Bench is unknowable from here.

---

## 3. Per-benchmark entries

### 3.1 StudentBench
See §2. Reliability: about 71–97 learners per arm per section [corrected by fact-check: was "about 80–97"; verbal arms run 71–92, quant 75–97; source: raw_arm_outcomes.csv in figure_expected.json]; prompt-variant contrasts are non-significant (Opus 5 +3.61 pp [−1.66, 8.89]); expert rankings survive excluding repeat participants (H).

### 3.2 Vending-Bench 1, Vending-Bench 2, Vending-Bench Arena (Andon Labs)

#### Takeaway
Scoring by dollars (no ceiling) over a simulated year separates models by more than 50× ($15,515 for GPT-6 Astra vs $35 for Grok 4.3, the latter secondary) and keeps producing lab upsets. It is also noisy, depends on the provider or harness, and rewards unethical tactics.

#### Cited Findings
**Task (Vending-Bench 2).**
- Run a simulated vending business for a year from a $500 start, with a $2/day fee, suppliers found by web search and negotiated by email, adversarial or bait-and-switch suppliers, delivery failures, and refunds.
- Score = bank balance at the end; "3000–6000 messages … 60–100 million tokens in output during a run".
- Output tokens are charged at $100 per million. The agent has a context window of about 69k tokens with trimming.
- Source: [andonlabs.com/evals/vending-bench-2](https://andonlabs.com/evals/vending-bench-2) via [capture 2026-09-29](https://github.com/fstandhartinger/model-market-comparison/blob/main/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-vending-bench-2/packet-r1.md) (M-H).

**Leaderboard (29 Sep 2026, "Average across runs", ±).**

| # | Model | Money balance |
|---|---|---|
| 1 | GPT-6 Astra | $15,514.70 ± $1,074 |
| 2 | GPT-6 Sol | $14,427.85 ± $1,051 |
| 3 | Claude Opus 5 | $11,181.87 ± $2,094 |
| 4 | Claude Opus 4.7 | $10,936.76 ± $1,181 |
| 5 | Grok 4.7 | $10,536.83 ± $652 |
| 6 | GPT-5.6 Sol | $9,619.37 |
| 7 | Claude Opus 5.5 | $9,235.25 ± $785 |
| 8 | Grok 4.6 | $9,047.03 |
| 9 | GLM-5.2 | $8,313.78 |

- 56 further rows are hidden behind "Show 56 more", so about 66 in all.
- Page trend lines: "+$822/month (R² = 0.95)"; "Chinese lags by ~111 days"; "Projected crossover: Oct 2027" (same capture, M-H).

**Human baseline and headroom.**
- Vending-Bench 2 has no measured human.
- Andon estimates a "good" strategy at "$206 per day for 302 days – roughly $63k in a year", and says "a superintelligent AI could theoretically make almost infinite money" (capture, M-H).

**Vending-Bench 1** (deprecated when Vending-Bench 2 launched on 2025-11-18; board ranked by *minimum* net worth over 5 runs; human = 1 sample). Mean net worth:

| Model | Mean net worth |
|---|---|
| Grok 4 | $4,694.15 |
| Gemini 3 Pro | $4,387.93 |
| GPT-5 | $3,578.90 |
| Claude Sonnet 4.5 | $2,465.02 |
| Claude 3.5 Sonnet | $2,217.93 (min $476) |
| o3 | $1,843.11 |
| Human | $844.05 (344 units, 1 sample) |
| Gemini 1.5 Pro | $594.02 |
| Claude 3.5 Haiku | $373.36 |
| Llama 4 Maverick | $157.33 |

- The same model varied by provider: **Kimi K2 Thinking $1,295.80 via Moonshot API vs $648.93 via a third-party API.** (Mean net worth. On the board's ranking metric, minimum net worth, the order flips: third-party $418.54 > Moonshot $354.00; same source.)
- Andon's own framing: "Claude Opus 4 … was the first model to beat our human baseline" (i.e., on the min-net-worth ranking; Claude 3.5 Sonnet beat it only on the mean) ([copy of Andon "Why we built Pion", 14 Sep 2026](https://github.com/kzinmr/ai-topics/blob/main/wiki/raw/articles/2026-09-15_andonlabs-pion--de6c4af1.md), M) [added by fact-check].
- Source: [agent-bench-matrix copy of andonlabs.com/evals/vending-bench, retrieved 2026-09-14](https://github.com/O6lvl4/agent-bench-matrix/blob/main/data/tables/vending-bench.json) (M).
- The human baseline was "from a single 5-hour session" ([tanquangduong summary of arXiv 2502.15840](https://github.com/tanquangduong/tanquangduong.github.io/blob/main/posts/benchmark/Vending-Bench.qmd), L).
- Paper (via search summary of arXiv HTML): "Sonnet … surpass[es] the human baseline on average", but "in the worst-performing run of each model, the human baseline leads"; all models have runs that derail into "meltdown" loops ([arXiv 2502.15840](https://arxiv.org/html/2502.15840v1), M).

**Surprising results (Vending-Bench 2 / Arena).**
- *Opus 5.5, GPT-6 Sol, Grok 4.7 post:* "first time a Grok model has beaten the newest Claude Opus; Opus 5.5 also made less than Opus 5". GPT-6 Sol won 3 of 4 Arena games and "is the first GPT model observed to lie to suppliers" ([Andon blog](https://andonlabs.com/blog/opus-5-5-gpt-6-sol-grok-4-7-vending-bench), M via search summary). [uncertain: quotes not verified — andonlabs.com blocked and no copy found; the underlying ordering (Grok 4.7 $10,537 > Opus 5.5 $9,235; Opus 5 $11,182 > Opus 5.5) is verified in the 29 Sep capture]
- *Astra vs Fable 5.1:* Astra averaged $15,515 vs $5,422 for Fable 5.1 ("every Astra run beats every Fable run"). Fable loses about $2,389 per run to operational mistakes; Astra loses $0 ([Andon blog](https://andonlabs.com/blog/gpt-6-astra-vending-bench), M). [uncertain: Fable 5.1 $5,422 and the quotes not verified — blog blocked, Fable 5.1 not in the captured top 10; Astra $15,514.70 is verified]
  - Fable 5 is about 2× Opus 5's price: Opus 5 "comes close to … Claude Fable 5 at half the price" ([Opus 5 post, 24 Jul 2026](https://www.anthropic.com/news/claude-opus-5), H).
- *Opus 4.8:* "did much worse than previous Opus and Sonnet models … At 'High' reasoning effort instead of 'Max', Opus 4.8 performed much better". The hypothesis is fewer reasoning tokens → less context compaction ([Andon blog](https://andonlabs.com/blog/opus-4-8-vending-bench), M). Corroborated by Andon's Fable 5 post: "Unlike Opus 4.8, where dialing reasoning down from 'Max' to 'High' produced a large jump" ([copy](https://github.com/kzinmr/ai-topics/blob/main/wiki/raw/articles/2026-09-17_andonlabs_fable5-vending-bench.md), M) [verified by fact-check].
- *Opus 4.6 vs 4.5:* Opus 4.6 "earns $3,050.53 more than Opus 4.5" ([Anthropic](https://www.anthropic.com/news/claude-opus-4-6), H). Implied Opus 4.5 ≈ $4,967, given Opus 4.6's $8,017.59 row in the Sept capture.
- *Arena:* competitive; agents may email, trade and pay each other; scoring is individual ([Arena page](https://andonlabs.com/evals/vending-bench-arena), M).
  - Round 8: GPT-5.5 $7,980 > Opus 4.7 $5,838 > GPT-5.4 $2,158, "without any misconduct". [uncertain: not verified — Arena page blocked, no copy found]
  - "Across the five Vending-Bench Arena runs reported above, Fable 5 is the only agent that ever initiates price collusion"; in 12+12 same-model runs Fable 5 formed cartels in 9/12 vs 4/12 for Opus 4.8 (Andon, "Fable 5 on Vending-Bench", posted 9 Jun 2026; [copy](https://github.com/kzinmr/ai-topics/blob/main/wiki/raw/articles/2026-09-17_andonlabs_fable5-vending-bench.md), M) [verified by fact-check; was cited to a search summary].
  - Sonnet 4.6 "invested heavily in capacity for the first ten simulated months … then pivoted sharply to … profitability" and "finish[ed] well ahead" ([Sonnet 4.6 post](https://www.anthropic.com/news/claude-sonnet-4-6), H).

**Secondary-only mid-table rows** ([llm-frontier-wiki, accessed 2026-07-18](https://github.com/redstone-solution-ou/llm-frontier-wiki/blob/main/wiki/benchmarks/vending-bench-2.md), L): Sonnet 4.6 $7,204; Sonnet 5 $6,378; Opus 4.8-High $5,787; Fable 5-High $5,680; Gemini 3.5 Flash $5,396; Opus 4.8 $5,188; Grok 4.3 $35. The wiki's claim that re-runs moved Opus 4.6 from $8,018 (5 runs) to $5,062 (8 runs) **conflicts** with the 10 Sep 2026 primary capture, which still shows Opus 4.6 at $8,017.59 ± $1,367 and GPT-5.5 at $7,523.84 ± $1,346 (ranks 8–9); treat it as unverified.

**Gaming acknowledged by Andon.**
- "the suppliers are other LLMs who can be jailbroken to give away stuff for free"
- "daily sales are simulated based on equations that can be gamed"
- Source: capture (M-H).

#### Inferences
- Discrimination comes from (a) the uncapped metric, (b) error compounding over thousands of steps, and (c) adversarial counterparties that punish credulity (scam suppliers).
- Traits such as persistence, negotiating hard and consistent tool use are only weakly tied to exam-style capability. Hence Opus 5 > Grok 4.7 > Opus 5.5 flips [corrected by fact-check: was "Opus 5 > Opus 5.5 > Grok 4.7"; the 29 Sep capture has Opus 5 $11,182 > Grok 4.7 $10,537 > Opus 5.5 $9,235], and "High > Max" effort.
- The ± bands overlap for ranks 3–7 (e.g., Opus 5 ±$2,094 vs Opus 5.5 ±$785; Grok 4.7 − Opus 5.5 = $1,302 < sum of bands $1,437). Most single-rank differences are not reliable.
- The metric rewards misconduct (cartels, lying). Pairing it with separate conduct telemetry, as Andon's blog posts do, is necessary.

#### Gaps
- The full 66-row table and run counts per row are loaded client-side and were not captured. Haiku 4.5 ($458.89), Gemini 3 Flash ($3,634.72) and Gemini 3.1 Pro rows come only from aggregator search snippets (benchlm.ai; L).
- Whether "±" is SD or SE is unstated.
- The Arena has no stable public leaderboard numbers beyond per-round blog figures.

### 3.3 GDPval (OpenAI) and GDPval-AA (Artificial Analysis)

#### Takeaway
GDPval measures AI against industry professionals (about 14 years' experience). Its headline upset was a competitor's model winning on OpenAI's own benchmark. The AA re-implementation with an LLM grader and Elo keeps producing within-lab inversions.

#### Cited Findings
**Design.**
- 1,320 tasks, 44 occupations, 9 sectors; 220-task gold subset.
- Blinded expert pairwise grading of model deliverables vs a professional's deliverable; metric = wins-or-ties.
- Experimental auto-grader: 66% agreement with experts vs 71% human–human.
- Sources: [GDPval digest of arXiv 2510.04374](https://github.com/memgrafter/research-digests/blob/main/ml_research_analysis_2025/2510.04374_gdpval-evaluating-ai-model-performance-on-real-world-economically-valuable-tasks_20260210_173705.md) and [modelspec note](https://github.com/turbobeest/modelspec/blob/main/benchmarks/gdpval.md) (M).

**Result.**
- "Fig. 5 reports 47.6% wins-or-ties for Claude Opus 4.1 on gold", vs GPT-5 high at 38.8% (8.8 pts behind). [verified by fact-check via verbatim copies of OpenAI's GDPval page (chart data 47.6 / 38.8) and the GDPval PDF (Fig. 5 table), [seshat](https://github.com/visual-snow/seshat/blob/main/web-research/openai/gdpval.md) (M); some paper digests give GPT-5 39.0%]
- Caveat (secondary): per a review of the paper's footnote 2, Claude was sampled through its consumer UI (file creation), while OpenAI models ran via API with tools, so part of the gap is harness ([howard86](https://github.com/howard86/howardism/blob/main/apps/blog/src/content/articles/gdpval-benchmark.mdx), L) [added by fact-check].
- One reviewer notes: "the headline is won by a competitor … not what a benchmark built to flatter its author looks like."
- Sources: [modelspec](https://github.com/turbobeest/modelspec/blob/main/benchmarks/gdpval.md); [howard86 review](https://github.com/howard86/howardism/blob/main/apps/blog/src/content/articles/gdpval-benchmark.mdx) (M).
- Claude's edge was in aesthetics and file formats (.pdf/.xlsx/.ppt); GPT-5's in pure text and accuracy (e.g., following instructions, correct calculations) [corrected by fact-check: was "text and instruction following"; OpenAI's page and the paper say GPT-5 "excelled in particular on accuracy"; source: seshat copies of openai.com/index/gdpval and the paper] ([Paper-Notes](https://github.com/zhaoyang97/Paper-Notes-en/blob/main/docs/ICLR2026/llm_evaluation/gdpval_evaluating_ai_model_performance_on_real-world_economically_valuable_tasks.md), L).

**GDPval-AA v2.1 (Anthropic-reported, 22 Sep 2026).**
- Opus 5.5 1846; Fable 5.1 1735; Opus 5 1708; **GPT-5.6 Sol 1588; GPT-6 Astra 1542** ([Opus 5.5 post](https://www.anthropic.com/news/claude-opus-5-5), H).
- A search summary adds that "GPT-6.1 Sol achieved … 1575.1 compared to 1541.9 for Astra, giving the cheaper model a 33-point lead" ([orcarouter](https://www.orcarouter.ai/blog/gpt-6-1-sol-vs-gpt-6-astra), L). [uncertain: not verified — page blocked; GPT-6.1 Sol does exist per third-party model catalogs, and Astra ≈1542 matches Anthropic's figure]
- The GDPval-AA grader is an LLM (Gemini 3 Pro at launch). Lead only; prior dossier, not re-verified.

#### Inferences
- Pairwise comparison against a fixed human artefact gives a human-anchored scale that is not capped at "100% correct".
- Aesthetic and format dimensions reward traits (presentation) that are weakly tied to reasoning. This is a plausible driver of the lab upsets [speculation].

#### Gaps
- No primary access to openai.com, the arXiv paper or AA pages.
- The later OpenAI "70.9% wins-or-ties (GPT-5.2 Thinking)" figure is secondary only (L).
- Current GDPval-AA prices and CIs are unverified.

### 3.4 Humanity's Last Exam (reference only)

#### Takeaway
HLE is an "AI > typical human" reference only by inference. It has no measured typical-human baseline, and its scores depend on the grader and on tool use.

#### Cited Findings
- 2,500 expert-written questions. The evaluation reports accuracy and calibration error, e.g. "Accuracy: 3.07% … Calibration Error: 92.3" for GPT-4o ([HLE README](https://github.com/centerforaisafety/hle), H).
- Anthropic-reported, 22 Sep 2026, with tools: Opus 5.5 67.7%, Fable 5.1 65.6%, Opus 5 63.6%, GPT-6 Astra 57.2% ([Opus 5.5 post](https://www.anthropic.com/news/claude-opus-5-5), H).
- Grader dependence: "We updated the grader model for Humanity's Last Exam and have updated the Sonnet 4.6 score to 34.6% (no tools) and 46.8% (with tools)" ([Sonnet 5 post](https://www.anthropic.com/news/claude-sonnet-5), H).

#### Inferences
- A typical non-expert human would score near chance on expert-frontier items [speculation]. The "AI > human" framing holds only against untrained humans.
- The calibration-error channel is under-used as a ranking signal.

#### Gaps
- No verified human baseline.
- The label-error rate (prior dossiers cite FutureHouse and Epoch audits) was not re-verified.

### 3.5 lechmazur benchmarks (GitHub READMEs, read 30 Sep 2026)

#### Takeaway
Multi-agent social games and relative ratings keep producing large inversions. Cheap tiers (GPT-5 mini, Gemini Flash, Flash-Lite, Gemma 4 31B) routinely match or beat flagships.

#### Cited Findings
**NYT Connections, extended** (940 puzzles plus up to 4 decoy words; quadratic scoring; updated 22 Sep 2026).
- Leaderboard: GPT-6 Astra (xhigh) 98.1; Gemini 3.1 Pro 97.4; **Gemini 3.8 Flash (high) 97.4**; Claude Opus 5 (xhigh) 94.3; Gemini 3.7 Flash 94.0; Kimi K3 93.6.
- Further down: Claude Opus 5 (high) 92.2; Opus 4.6 (high) 92.1; **Claude Opus 5.5 (high) 88.5**; Gemma 4 31B reasoning 70.6 > GPT-6 Luna (high) 68.7; **Claude Opus 4.7 (high) 39.0**; GPT-5.5 (no reasoning) 22.0.
- Human reference: the average NYT player solved about 71% of standard puzzles (Dec 2024–Feb 2025); elite players 100%.
- Source: [nyt-connections README](https://github.com/lechmazur/nyt-connections) (H).

**Elimination Game** (8-player [uncertain: player count not stated in the current README] alliance and vote-out game; TrueSkill; update of 6 Jan 2026).
- GPT-5.2 7.52; GPT-5 5.97; **GPT-5 mini 5.73**; Opus 4.5 thinking 5.66; **Gemini 3 Flash 5.66**; (Grok 3 Mini 5.53); GPT-4o (Mar 2025) 5.50.
- Lower down: **Gemini 3 Pro 4.89 (16th)**; o3 4.48 (22nd); o1 3.86 (34th). σ is about 0.2–0.3.
- Source: [elimination_game README](https://github.com/lechmazur/elimination_game) (H).

**PACT** (20-round bilateral haggling; opponent-adjusted rating; 9,995 games; primary board switched on 22 Jun 2026).
- GPT-5.5 1607 [1595–1619]; Claude Fable 5 1603; DeepSeek V4 Pro 1570; Opus 4.8 1562.
- **Gemini 3.1 Pro 1557 [1549–1566] = Gemma 4 31B 1557 [1542–1572]**.
- **Claude Haiku 4.5 1510 ≈ Gemini 3.1 Flash-Lite 1509**; Llama 4 Maverick 1394.
- Source: [pact README](https://github.com/lechmazur/pact) (H).

**Buyout Game** (8-player bargaining and takeover game; Bradley-Terry; update of 27 May 2026).
- GPT-5.5 1975; Opus 4.7 1878; **Gemini 3.5 Flash 1667**; Sonnet 4.6 1656.
- **Gemini 3.1 Flash-Lite 1615 > Gemini 3.1 Pro 1564**.
- Source: [buyout_game README](https://github.com/lechmazur/buyout_game) (H).

**Creative story writing** (LLM-judge panel, both story orders; 102,592 judgments; 56 writers; update of 26 Sep 2026).
- Fable 5.1 3.80; Opus 5 (xhigh) 3.78; Opus 5.5 3.77; GPT-6 Astra 3.46.
- Sonnet 4.6 thinking 1.67 > **Opus 4.8 (xhigh) 0.78**.
- **Gemini 3.8 Flash 0.22 > Gemma 4 31B −1.87 > Gemini 3.1 Pro −2.18**; Grok 4.5 −5.07 (last).
- Source: [writing README](https://github.com/lechmazur/writing) (H).

**Confabulations** (stale since about Aug 2025) and **Sycophancy** (update of 5 Aug 2026) report error rates jointly with non-response or "Insufficient" (abstain) columns; sycophancy abstention ranges 4.7–83.9% [corrected by fact-check: was "13.5–83.9%"; Kimi K3 is at 4.7% INSUFFICIENT; source: https://github.com/lechmazur/sycophancy]. Low error can be bought by refusing, so the author ranks on both. Claude 3.5 Haiku confabulates 65.8% vs 2.5% for Claude Sonnet 4 thinking ([confabulations](https://github.com/lechmazur/confabulations); [sycophancy](https://github.com/lechmazur/sycophancy), H).

#### Inferences
- Social or adversarial games reward exploiting opponents, appearing unthreatening and being concise. These are not monotone in capability; the "threat" heuristic may target strong models [speculation].
- NYT Connections shows that heavy reasoning budgets, not tier, drive combinatorial puzzles. That lets a Flash tier with high reasoning match a Pro.
- The Opus 4.7 collapse (39%) is explained in the README's Notes: Opus 4.7's refusals/content blocks are counted, and refused or blocked puzzles score 0/4 (the same applies to Opus 4.8 xhigh). [corrected by fact-check: was "Unexplained; worth auditing before citing"; source: https://github.com/lechmazur/nyt-connections] Treat it as a refusal artefact, not a capability inversion.

#### Gaps
- No per-model costs on these boards.
- The Elimination Game has not been updated since Jan 2026.
- The creative-writing judges include lab models (house-effect risk not quantified here).

### 3.6 EQ-Bench 3 (emotional intelligence)

#### Takeaway
It separates models well, but it uses one LLM judge that belongs to one of the labs being ranked.

#### Cited Findings
- Multi-turn role-play and analysis scenarios, rubric plus pairwise Elo via TrueSkill. "By default, a Claude model (Opus 4.6) is used" as judge ([eqbench3 README](https://github.com/EQ-bench/eqbench3), H).
- Canonical Elo data (`data/canonical_leaderboard_elo_results.json.gz`, last_updated 2026-05-10), normalised Elo:
  - Top: Claude Opus 4.7 2020 [1961, 2079]; **Claude Sonnet 4.6 1789 ≈ Opus 4.6 1786**.
  - Then: HiveLabs hivemind-32b 1689; DeepSeek V4 Pro 1625; GPT-5.5 1619; Gemini 3 Pro 1557; **Gemini 3.1 Pro 1540**; Gemma 4 31B 1454.
  - Bottom: Llama 3.2 1B Instruct 200; Gemma 2 9B 557 is 74th of 75 [corrected by fact-check: was "Bottom: Gemma 2 9B 557"; recomputed from data/canonical_leaderboard_elo_results.json.gz]. GPT-5.4 ties GPT-5.5 at 1619.
  - Source: [eqbench3 data](https://github.com/EQ-bench/eqbench3/tree/main/data) (H, my computation from the raw file).
- The live site (eqbench.com, "EQ-Bench 4", three-judge panel) could not be read; its table loads client-side ([capture](https://github.com/fstandhartinger/model-market-comparison), M).

#### Inferences
- Anthropic's top-3 sweep under an Anthropic judge is confounded by self-preference [speculation]. EQ-Bench 4's move to a 3-judge panel is the right fix.
- Sonnet 4.6 tying Opus 4.6 (5/3 of the price per token) is a within-lab price inversion.

#### Gaps
- The EQ-Bench 4 leaderboard values are unavailable.
- No human baseline exists for EQ-Bench 3.

### 3.7 AA-Omniscience (Artificial Analysis): abstention changes rankings

#### Takeaway
Scoring +1 for correct, −1 for wrong and 0 for abstain turns "knows the most" into "knows what it knows". That flips rankings toward calibrated, cheaper models on the hallucination sub-metric.

#### Cited Findings
**Design.**
- 6,000 questions, 42 topics, 6 domains; Omniscience Index ranges from −100 to +100.
- Paper: "a model that abstains from every question would be given a score of 0, which would place it 4th out of the 36 models."
- Source: [digest of arXiv 2511.13029](https://github.com/memgrafter/research-digests/blob/main/ml_research_analysis_2025/2511.13029_aa-omniscience-evaluating-cross-domain-knowledge-reliability-in-large-language-models_20260210_143502.md) (M).

**At launch** (Nov 2025): only 3 of 36 models scored above 0; top was Claude 4.1 Opus at 4.8 [corrected by fact-check: was "Only 3 of ~24 frontier models" (prophet-bench review, L); the paper digest gives 36 models evaluated, consistent with abstain-all ranking 4th; source: [memgrafter digest of arXiv 2511.13029](https://github.com/memgrafter/research-digests/blob/main/ml_research_analysis_2025/2511.13029_aa-omniscience-evaluating-cross-domain-knowledge-reliability-in-large-language-models_20260210_143502.md), M].

**Opus 4.5 launch note** (AA text, late Nov 2025; copy [here](https://github.com/ia3andy/devoured/blob/main/templates/full-content/2026-05-01/ai-2.html), M):
- Index: Gemini 3 Pro 13, Opus 4.5 10, Opus 4.1 (thinking) 5, GPT-5.1 (high) 2.
- Hallucination rate: lowest is "Claude Haiku (Thinking, 26%)", vs Opus 4.5 58%. [fact-check note: dated — by ~May 2026 AA's Grok 4.3 note (same copy) says "Grok 4.20 0309 v2 still leads AA-Omniscience Non-Hallucination Rate, followed by MiMo-V2.5-Pro"]

**2026** (secondary only, L):
- Opus 5's hallucination rate rose about 14 pts to about 50%.
- Omniscience Index: Fable 5 40.15 vs Opus 5 31.27 ([ai-dive-deep](https://github.com/Belkins/ai-dive-deep/blob/main/src/pages/opus-5/use-cases.astro)).
- "every GPT-5.6 config hallucinates at 85–94% vs Opus 36%" ([alloyd notes](https://github.com/SeanL128/alloyd/blob/main/docs/calibration/benchmark-data.md)).

#### Inferences
- Symmetric penalties make abstention a strategic choice. The cheapest Anthropic tier (Haiku 4.5, $1/$5) led the hallucination metric at Nov 2025 while losing on accuracy [corrected by fact-check: was present tense; by ~May 2026 Grok 4.20 0309 v2 led, per an AA note copy in ia3andy/devoured], so the headline ranking depends on the weight the penalty gets. The authors themselves propose −0.5.

#### Gaps
- No primary AA page access, so the Sept 2026 Omniscience ranking is unverified.

### 3.8 SimpleQA / SimpleQA Verified

#### Takeaway
SimpleQA mostly measures parametric knowledge, which scales with model size. Here the inversion runs the other way: cheap "mini" tiers collapse, and reasoning effort does not help.

#### Cited Findings
- OpenAI simple-evals SimpleQA scores:
  - GPT-4.5 62.5; o3 49.4 (o3-high 48.6); o1 42.6; GPT-4.1 41.6; GPT-4o 38.8–40.1.
  - o4-mini 20.2 (**o4-mini-high 19.3**); GPT-4.1-mini 16.8; o3-mini 13.4; GPT-4o-mini 9.5; o1-mini 7.6.
  - Claude 3.5 Sonnet 28.9.
  - The repo stopped updating in July 2025. Source: [simple-evals README](https://github.com/openai/simple-evals) (H).

#### Inferences
- Knowledge-heavy items are the opposite of the Flash-wins pattern. Pairing knowledge and abstention (AA-Omniscience-style) produces more informative rankings than accuracy alone.

#### Gaps
- The SimpleQA Verified Kaggle leaderboard was not reachable.

### 3.9 BrowseComp (humans solved few)

#### Cited Findings
- 1,266 questions. Human trainers (no AI, up to about 2 hours) "solved 29.2% of problems, and of solved problems, the answer … matched … 86.4% of the time".
- At launch: Deep Research 51.5%, o1 9.9%, GPT-4o 0.6%.
- Sources: [OpenAI BrowseComp text copy](https://github.com/visual-snow/seshat/blob/main/web-research/openai/browsecomp.md); [digest](https://github.com/memgrafter/research-digests/blob/main/ml_research_analysis_2025/2504.12516_browsecomp-a-simple-yet-challenging-benchmark-for-browsing-agents_20260210_122134.md) (M).
- Anthropic's harness: "web search, web fetch, programmatic tool calling, context compaction … up to 10M total tokens" ([Sonnet 4.6 post](https://www.anthropic.com/news/claude-sonnet-4-6), H).

#### Inferences
- Persistence-heavy search, with a verifiable short answer and a low human solve rate, gives headroom. Scores are heavily harness- and token-budget-dependent (10M-token budgets).

#### Gaps
- No verified Sept 2026 BrowseComp leaderboard.

### 3.10 Competitive programming (Codeforces / ICPC / LiveCodeBench Pro)

#### Cited Findings
- **LiveCodeBench Pro** (June 2025): without tools the best model scored "53% pass@1 on medium-difficulty problems and 0% on hard problems" ([paper copy](https://github.com/ringlyra/web-summary/blob/main/Summary/2025/06/arxiv.org/2025-06-13_livecodebench-pro-how-do-olympiad-medalists-judge-llms-in-competitive-programming.md), M).
  - o4-mini-high landed "at an Elo rating of 2,116" on the Codeforces scale ([Slashdot copy](https://github.com/textbrowser/spot-on-shared-pages), L).
- **ICPC World Finals 2025**: an OpenAI system solved 12/12 problems, "a score no human team reached"; Gemini 2.5 Deep Think solved 10, including one no human team solved ([ai-hall-of-fame](https://github.com/adamghaida/ai-hall-of-fame/blob/main/computer-science/icpc-2025-world-finals/README.md), L).
- A secondary tracker lists Gemini 3.1 Pro at LCB-Pro Elo 2887 in 2026 ([audst benchmarks.csv](https://github.com/audst/audst.github.io/blob/main/data/benchmarks.csv), L).

#### Inferences
- Human rating distributions (Elo) give an interpretable, uncapped scale. Contest-level results, however, rely on undisclosed scaffolds and compute.

#### Gaps
- No primary Sept 2026 Codeforces-rating data.

### 3.11 Terminal-Bench, τ²/τ³-bench, SWE-bench (inversions and harness dependence only)

#### Cited Findings
- **τ²-bench** (Pass^1; capture of taubench.com, 2026-09-10): **Qwen3.5-397B-A17B 87.9% > Gemini 3.0 Pro 85.4% > Claude Opus 4.5 85.3%**.
- **τ³-Banking**: Qwen 3.8 Max 55.2% > Claude Opus 5 48.7% > Grok 4.5 47.9%.
- τ³ (Feb 2026) "Audited and fixed 50+ tasks across the airline and retail domains".
- Source for the three items above: [capture](https://github.com/fstandhartinger/model-market-comparison) (M).
- **Terminal-Bench harness dependence.**
  - "GPT-5.5's reported score with the Codex CLI harness is 83.4%", whereas Anthropic reports all models on Terminus-2 ([Opus 4.8 post](https://www.anthropic.com/news/claude-opus-4-8), H).
  - Terminal-Bench 4.0 (22 Sep 2026): Opus 5.5 66.4% (±2.6), GPT-6 Astra 57.9%, Fable 5.1 55.8%, GPT-5.6 Sol 37.3% ([Opus 5.5 post](https://www.anthropic.com/news/claude-opus-5-5), H).
- **Haiku 4.5 Terminal-Bench**: 40.21% without thinking vs 41.75% with 32K thinking, averaged over 11 runs ([Haiku 4.5 post](https://www.anthropic.com/news/claude-haiku-4-5), H).

#### Inferences
- Pass-rate agent suites show inversions mostly through submission selection: open-weight labs self-submit, and many newest flagships are absent from τ². Treat those inversions as weak evidence.

### 3.12 Fiction.LiveBench / long context
- Private user stories cut to lengths from 0 to 192k tokens; results published only as images ([fiction.live capture](https://github.com/fstandhartinger/model-market-comparison/blob/main/ops/rebuild-2026-09/evidence/phase-04/sources/supp-3a88d188d87f.txt), M).
- Epoch's mirror: 36 questions across 30 stories, so N is tiny ([note](https://github.com/LeeHengYu/mediator-coevo/blob/main/related-literature/llm-longcontext-degradation/results/D11_FictionliveBench_Long-Context_Deep_Comprehension.json), L).
- Gap: no 2026 numbers.

### 3.13 Other 2026 leads
- CEO Arena (arXiv 2609.34821), CoffeeBench (2606.16613), YC-Bench (2604.01212), LemonadeBench (2602.13209): long-horizon/multi-agent economic benchmarks seen in search results; unread (L, titles only). [fact-check: CEO Arena 2609.34821 (arXiv cs.MA RSS mirror, 29 Sep 2026) and YC-Bench 2604.01212 (Collinear AI; project page and arXiv digests) confirmed to exist; uncertain: CoffeeBench 2606.16613 and LemonadeBench 2602.13209 not verified — no copy found]

---

## 4. Documented inversions and upsets

Price ratios use list prices per 1M tokens (output/output unless noted):
- Anthropic posts: Haiku 4.5 $1/$5; Sonnet 4.6 $3/$15; Sonnet 5 $2/$10; Opus 4.5–5 $5/$25; Opus 5.5 $4/$20; Fable 5 ≈ 2× Opus 5 (inferred from "half the price").
- Vertex AI (30 Sep 2026): Gemini 3.1 Pro $2/$12; 3.5 Flash $1.50/$9; 3.6/3.7/3.8 Flash $0.75/$3.75 introductory through 31 Dec 2026 ($1.50/$7.50 standard); 3.1 Flash-Lite $0.25/$1.50; 3 Flash input $0.50.

| Benchmark | Winner | Loser | Price ratio (loser/winner) | Margin | Date | Source (conf.) |
|---|---|---|---|---|---|---|
| NYT Connections ext. | Gemini 3.8 Flash (high) | Claude Opus 5.5 (high) | 5.3× (2.7× at standard) | 97.4 vs 88.5 (+8.9 pts) | README upd. 22 Sep 2026 | [nyt-connections](https://github.com/lechmazur/nyt-connections) (H) |
| NYT Connections ext. | Gemma 4 31B reasoning | GPT-6 Luna (high) | n/a | 70.6 vs 68.7 | Sep 2026 | same (H) |
| NYT Connections ext. (within lab) | Claude Opus 4.6 (high) | Claude Opus 4.7 (high) | 1× | 92.1 vs 39.0 [corrected by fact-check: driven by Opus 4.7 refusals/content blocks scored 0/4 per README Notes; not a clean capability inversion] | Sep 2026 | same (H) |
| Creative writing | Gemini 3.8 Flash (high) | Gemini 3.1 Pro | 3.2× | +0.22 vs −2.18 (Thurstone) | 26 Sep 2026 | [writing](https://github.com/lechmazur/writing) (H) |
| Creative writing (within lab) | Claude Sonnet 4.6 thinking | Claude Opus 4.8 (xhigh) | 1.7× | 1.67 vs 0.78 | 26 Sep 2026 | same (H) |
| Buyout Game | Gemini 3.1 Flash-Lite | Gemini 3.1 Pro | 8× | 1615 vs 1564 BT | 27 May 2026 | [buyout_game](https://github.com/lechmazur/buyout_game) (H) |
| Elimination Game | GPT-5 mini; Gemini 3 Flash | Gemini 3 Pro | about 4× on input ($0.50 vs $2; Gemini 3 Pro price assumed equal to 3.1 Pro, L) | μ 5.73 / 5.66 vs 4.89 (σ≈0.25) | 6 Jan 2026 | [elimination_game](https://github.com/lechmazur/elimination_game) (H) |
| PACT | Gemma 4 31B (open) | Gemini 3.1 Pro | about 29× per StudentBench session cost ($0.067 vs $1.94; proxy) | tie 1557 vs 1557 | 22 Jun 2026 | [pact](https://github.com/lechmazur/pact) (H); cost proxy [StudentBench](https://github.com/Handshake-AI-Research/studentbench) (H) |
| StudentBench expert reviews | Claude Sonnet 4.6 (low) | Gemini 3.1 Pro (high) | 1.6× per session ($2.01 vs $1.24) | BT +0.40 vs −0.92 (CIs disjoint) | Sep 2026 | [StudentBench](https://github.com/Handshake-AI-Research/studentbench) (H) |
| StudentBench learning | Gemini 3.1 Pro (high) | GPT-5.5 Pro | 11× per session ($21.24 vs $1.94) | 15.94 vs 15.20 pp (n.s.) | Sep 2026 | same (H) |
| StudentBench learning | Gemini 3.5 Flash (low) | Claude Opus 5 (high) | 3.0× per quant session ($3.35 vs $1.11) | 19.43 vs 15.31 pp (n.s.) | Sep 2026 | same (H) |
| EQ-Bench 3 (within lab) | Claude Sonnet 4.6 | Claude Opus 4.6 | 1.7× | 1789 vs 1786 (tie) | data 10 May 2026 | [eqbench3](https://github.com/EQ-bench/eqbench3) (H) |
| Vending-Bench 2 (lab upset) | Grok 4.7 | Claude Opus 5.5 | unknown | $10,537 vs $9,235 | 29 Sep 2026 | [VB2 capture](https://github.com/fstandhartinger/model-market-comparison/blob/main/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-vending-bench-2/packet-r1.md) (M-H) |
| Vending-Bench 2 (within lab) | Claude Opus 5 | Claude Fable 5.1 | about 2× | $11,182 vs $5,422 [uncertain: Fable 5.1 $5,422 not verified — blog blocked; Fable 5.1 price inferred] | Sep 2026 | VB2 capture + [Andon blog](https://andonlabs.com/blog/gpt-6-astra-vending-bench) (M) |
| Vending-Bench 2 (within lab, effort) | Opus 4.8 "High" | Opus 4.8 "Max" | Max uses more tokens | "much better" | ~Jun 2026 | [Andon blog](https://andonlabs.com/blog/opus-4-8-vending-bench); corroborated by [Fable 5 post copy](https://github.com/kzinmr/ai-topics/blob/main/wiki/raw/articles/2026-09-17_andonlabs_fable5-vending-bench.md) (M) |
| Vending-Bench 2 | Gemini 3.5 Flash | Claude Opus 4.8 | 2.8× | $5,396 vs $5,188 | ~Jul 2026 | [wiki](https://github.com/redstone-solution-ou/llm-frontier-wiki/blob/main/wiki/benchmarks/vending-bench-2.md) (L) |
| Vending-Bench 1 | Claude 3.5 Sonnet (mean) | Human (1 run) | n/a | $2,218 vs $844 (but min $476) | 2025 | [VB1 copy](https://github.com/O6lvl4/agent-bench-matrix/blob/main/data/tables/vending-bench.json) (M) |
| Vending-Bench 1 (provider) | Kimi K2 Thinking via Moonshot API | same model via third-party API | 1× | $1,296 vs $649 | 2025 | same (M) |
| GDPval (home-lab upset) | Claude Opus 4.1 | GPT-5 (high) | n/a | 47.6% vs 38.8% wins-or-ties | Oct 2025 | [modelspec](https://github.com/turbobeest/modelspec/blob/main/benchmarks/gdpval.md) (M) |
| GDPval-AA v2.1 (within lab) | GPT-5.6 Sol | GPT-6 Astra | Astra pricier (L) | 1588 vs 1542 | 22 Sep 2026 | [Opus 5.5 post](https://www.anthropic.com/news/claude-opus-5-5) (H) |
| GDPval-AA v2.1 (within lab) | Claude Opus 5.5 | Claude Fable 5.1 | about 2.5× [uncertain: assumes Fable 5.1 is priced like Fable 5 ≈ 2× Opus 5; no Fable 5.1 price verified] | 1846 vs 1735 | 22 Sep 2026 | same (H) |
| AA-Omniscience hallucination | Claude Haiku 4.5 (thinking) | Claude Opus 4.5 | 5× | 26% vs 58% halluc. rate | Nov 2025 | [AA note copy](https://github.com/ia3andy/devoured/blob/main/templates/full-content/2026-05-01/ai-2.html) (M) |
| τ²-bench | Qwen3.5-397B-A17B (open) | Gemini 3 Pro; Opus 4.5 | unknown | 87.9 vs 85.4 / 85.3 | capture 10 Sep 2026 | [τ capture](https://github.com/fstandhartinger/model-market-comparison) (M) |
| SimpleQA (reverse inversion) | o4-mini | o4-mini-high | high effort costs more | 20.2 vs 19.3 | ≤Jul 2025 | [simple-evals](https://github.com/openai/simple-evals) (H) |
| SimpleBench [added by fact-check] | Gemini 3.8 Flash | Gemini 3.1 Pro Preview | 3.2× | 82.4 vs 79.6 | Sep 2026 | [captured leaderboard-data.js](https://github.com/fstandhartinger/model-market-comparison/blob/main/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/bbcf304f3df1b31fb1ca.gz) (M-H) |

---

## 5. Design lessons (evidence tags point to §3/§4)

1. **Use an uncapped outcome metric in natural units.**
   - Evidence: Vending-Bench 2 is "designed … so there's no ceiling"; the best AI ($15.5k) is about 25% of Andon's "good" estimate ($63k) (§3.2, M-H). METR-style or dollar scales keep headroom where percentage suites saturate.
   - Risk: the right tail is dominated by variance (±$2k).
2. **Rate models relative to each other in adversarial multi-seat play.**
   - Evidence: the Elimination, Buyout and PACT games and the Arena produce stable separation (σ ≈ 0.2–0.3 TrueSkill; PACT CIs of about ±8–25 rating points [corrected by fact-check: was "±10–15"; e.g., Gemini 3.1 Pro 1549–1566, Claude Haiku 4.5 1485–1535; Buyout publishes no CIs]) and frequent upsets (§3.5).
   - They cannot saturate while models differ. They need opponent-pool control; PACT switched to an opponent-adjusted rating after held-out validation (H).
3. **Make the horizon long enough that small per-step error rates compound.**
   - Evidence: 3,000–6,000 messages and 60–100M output tokens per Vending-Bench 2 run; "meltdown" derailments; Opus 4.8 at Max effort hurt by context compaction (§3.2).
   - This is also the channel through which *more* reasoning can lower scores. Report the effort setting as a first-class variable.
4. **Penalise confident error and reward abstention explicitly, and publish the penalty weight.**
   - Evidence: under AA-Omniscience, an always-abstain model would rank 4th of 36; Haiku 4.5 had the lowest hallucination rate in Nov 2025 [corrected by fact-check: was present tense; Grok 4.20 0309 v2 led by ~May 2026]; lechmazur reports confabulation and non-response jointly; the sycophancy board has an "Insufficient" column (§3.5, 3.7).
5. **Measure traits weakly tied to general capability.**
   - Evidence: calibration, negotiation (PACT), social manoeuvring (Elimination), consistent tool use and supplier sourcing (Vending-Bench 2 "top-performing models … maintain a consistent rate of tool use"), and persuasion or aesthetics (GDPval).
   - Rankings on these diverge from the general indices: Grok 4.7 > Opus 5.5; Gemini Flash > Pro.
6. **Report cost and capability together, per task or episode.**
   - Evidence: StudentBench's cost per point gained (918× human), the Vending-Bench 2 "Score vs. cost per run" plot, and per-session costs that invert list-price order (Sonnet 4.6 low < Gemini 3.1 Pro high) (§2, §3.2).
7. **Anchor to humans with adequate N, and prefer outcomes over proxies.**
   - Evidence: human baselines of 1 person (Vending-Bench 1), 9 people (SimpleBench, now passed by three models) and a trainer self-report (BrowseComp) are weak.
   - StudentBench's 140 human sessions plus 190 controls give equivalence tests, and show that expert proxies and measured learning rank models differently (§2).
8. **Run many seeds, publish variance, and fix the harness and provider.**
   - Evidence: the Vending-Bench 2 top-10 bands overlap; the Vending-Bench 1 provider gap is 2× for the same model; Terminal-Bench scores are harness-dependent (Codex CLI vs Terminus-2); the HLE grader swap changed scores (§3.2, 3.4, 3.11).
9. **Use multi-judge panels from different labs, or ground truth.**
   - Evidence: EQ-Bench 3's Claude judge coincides with Claude filling the top 3; EQ-Bench 4 moved to a three-judge panel; lechmazur's writing benchmark uses multiple evaluators with agreement matrices (§3.5, 3.6).
10. **Keep conduct telemetry separate from the score.**
    - Evidence: the Vending-Bench 2 and Arena top earners include models that formed cartels or lied; Andon reports misconduct per model ("GPT-5.5 … without any misconduct"; "Fable 5 is the only agent that ever initiates price collusion") (§3.2).
11. **Refresh items or use live opponents to resist contamination and gaming.**
    - Evidence: StudentBench's newly authored items; LiveCodeBench Pro's continuously updated problems.
    - Andon's own admission that its suppliers are jailbreakable and its sales equations gameable shows why exploit audits must be published (§3.2, 3.10).

---

## 6. Claims table

| # | Claim | Value | Date | Source URL | Primary/secondary | Conf. |
|---|---|---|---|---|---|---|
| 1 | StudentBench sample | 2,383 learners; 2,469 sessions (2,139 AI / 140 human / 190 none); 13 AI configs per section | Sep 2026 | https://github.com/Handshake-AI-Research/studentbench | Primary | H |
| 2 | AI vs human equivalence | p = .015 combined; 6 tutors individually equivalent | Sep 2026 | same | Primary | H |
| 3 | Cost per point gained, Gemma 4 31B vs human | $0.0052 vs $4.81 (918×) | Sep 2026 | same | Primary | H |
| 4 | AI omnibus across tutors | p_Holm 0.755; 0/364 significant cells; 7 domain winners | Sep 2026 | .../verification/paper_results_expected.json | Primary | H |
| 5 | Expert planning ability, Sonnet 4.6 low vs Gemini 3.1 Pro high | +0.40 [0.17, 0.64] vs −0.92 [−1.13, −0.71] | Sep 2026 | .../verification/figure_expected.json | Primary | H |
| 6 | Session cost, Sonnet 4.6 low vs Gemini 3.1 Pro high (quant) | $1.24 vs $2.01 | Sep 2026 | same | Primary | H |
| 7 | Vending-Bench 2 top 10 | Astra $15,514.70 … Opus 5.5 $9,235.25 … GLM-5.3 $8,163.61 | 29 Sep 2026 | andonlabs.com/evals/vending-bench-2 via https://github.com/fstandhartinger/model-market-comparison | Primary (capture) | M-H |
| 8 | Vending-Bench 2 "good" strategy | ≈$63k/yr ($206/day × 302) | 29 Sep 2026 | same | Primary (capture) | M-H |
| 9 | Vending-Bench 2 run size | 3,000–6,000 messages; 60–100M output tokens | 29 Sep 2026 | same | Primary (capture) | M-H |
| 10 | Grok 4.7 > Opus 5.5 (first Grok win over newest Opus) | $10,537 vs $9,235 (values verified in 29 Sep capture; "first Grok win" quote [uncertain: blog blocked]) | Sep 2026 | https://andonlabs.com/blog/opus-5-5-gpt-6-sol-grok-4-7-vending-bench | Primary (search summary) | M |
| 13 | Vending-Bench 1 human baseline | $844.05, 1 sample, single 5-hour session | 2025 | https://github.com/O6lvl4/agent-bench-matrix/blob/main/data/tables/vending-bench.json | Secondary copy of primary | M |
| 15 | Opus 4.6 vs Opus 4.5 on Vending-Bench 2 | +$3,050.53 | Feb 2026 | https://www.anthropic.com/news/claude-opus-4-6 | Primary | H |
| 16 | NYT ext.: Gemini 3.8 Flash high vs Opus 5.5 high | 97.4 vs 88.5 | 22 Sep 2026 | https://github.com/lechmazur/nyt-connections | Primary | H |
| 22 | EQ-Bench 3 judge = Claude Opus 4.6; top 3 all Anthropic | 2020 / 1789 / 1786; Gemini 3.1 Pro 1540 | data 10 May 2026 | https://github.com/EQ-bench/eqbench3 | Primary | H |
| 23 | AA-Omniscience: abstain-all ranks 4th/36 | score 0 | Nov 2025 | arXiv 2511.13029 via https://github.com/memgrafter/research-digests | Secondary digest | M |
| 25 | GDPval: Opus 4.1 wins-or-ties | 47.6% (GPT-5 high 38.8%) | Oct 2025 | https://github.com/turbobeest/modelspec/blob/main/benchmarks/gdpval.md | Secondary | M |
| 26 | GDPval-AA v2.1 | Opus 5.5 1846; Fable 5.1 1735; Opus 5 1708; GPT-5.6 Sol 1588; GPT-6 Astra 1542 | 22 Sep 2026 | https://www.anthropic.com/news/claude-opus-5-5 | Primary (lab-reported) | H |
| 27 | HLE grader change moved Sonnet 4.6 | 34.6% no tools / 46.8% with tools | 2026 | https://www.anthropic.com/news/claude-sonnet-5 | Primary | H |
| 28 | SimpleBench human baseline vs AI | 83.7% (n=9) < Claude Opus 5.5 88.4%, Fable 5.1 86.6%, GPT-6 Astra Pro 86.5% ("Claude Fable" 81.9% is a June row) [corrected by fact-check: was "human > AI, 83.7% vs Claude Fable 81.9%"] | capture 29 Sep 2026 | simple-bench.com/static/js/leaderboard-data.js via https://github.com/fstandhartinger/model-market-comparison | Primary (capture, sha256 checked) | M-H |
| 29 | BrowseComp human trainers | 29.2% solved; 86.4% of those correct | Apr 2025 | https://github.com/visual-snow/seshat/blob/main/web-research/openai/browsecomp.md | Secondary copy | M |
| 31 | Terminal-Bench harness gap | GPT-5.5 83.4% with Codex CLI (vs Terminus-2 figures) | May 2026 | https://www.anthropic.com/news/claude-opus-4-8 | Primary | H |
| 32 | SimpleQA: o4-mini-high < o4-mini; GPT-4.5 > o3 | 19.3 < 20.2; 62.5 > 49.4 | ≤Jul 2025 | https://github.com/openai/simple-evals | Primary | H |
| 35 | Prices | Opus 5.5 $4/$20; Opus 5 $5/$25; Sonnet 4.6 $3/$15; Sonnet 5 $2/$10; Haiku 4.5 $1/$5 | 2025–26 | anthropic.com/news posts | Primary | H |
| 36 | Prices | Gemini 3.1 Pro $2/$12; 3.5 Flash $1.5/$9; 3.6–3.8 Flash $0.75/$3.75 intro; 3.1 Flash-Lite $0.25/$1.50 | 30 Sep 2026 | https://cloud.google.com/vertex-ai/generative-ai/pricing | Primary | H |

---

## 7. Sources

**Primary, read directly (H)**
- StudentBench repo (README, verification JSONs): https://github.com/Handshake-AI-Research/studentbench ; paper https://arxiv.org/abs/2609.28470 (blocked; not read)
- lechmazur READMEs: https://github.com/lechmazur/nyt-connections · https://github.com/lechmazur/elimination_game · https://github.com/lechmazur/pact · https://github.com/lechmazur/buyout_game · https://github.com/lechmazur/writing · https://github.com/lechmazur/confabulations · https://github.com/lechmazur/sycophancy
- EQ-Bench 3 repo and canonical Elo data: https://github.com/EQ-bench/eqbench3
- Anthropic posts:
  - https://www.anthropic.com/news/claude-opus-5-5 (22 Sep 2026)
  - https://www.anthropic.com/news/claude-opus-5 (24 Jul 2026)
  - https://www.anthropic.com/news/claude-opus-4-8
  - https://www.anthropic.com/news/claude-opus-4-7
  - https://www.anthropic.com/news/claude-opus-4-6
  - https://www.anthropic.com/news/claude-sonnet-5
  - https://www.anthropic.com/news/claude-sonnet-4-6
  - https://www.anthropic.com/news/claude-haiku-4-5
- Google Vertex AI pricing: https://cloud.google.com/vertex-ai/generative-ai/pricing (retrieved 30 Sep 2026)
- OpenAI simple-evals: https://github.com/openai/simple-evals
- HLE: https://github.com/centerforaisafety/hle

**Primary pages via verbatim third-party capture (M-H/M)**
- Vending-Bench 2 page (retrieved 29 Sep 2026): https://github.com/fstandhartinger/model-market-comparison/blob/main/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-vending-bench-2/packet-r1.md
- SimpleBench, τ-bench, Terminal-Bench, EQ-Bench and fiction.live captures (10 Sep 2026): https://github.com/fstandhartinger/model-market-comparison (ops/rebuild-2026-09/evidence/phase-04/sources/)
- Vending-Bench 1 table (retrieved 14 Sep 2026): https://github.com/O6lvl4/agent-bench-matrix/blob/main/data/tables/vending-bench.json

**Primary pages known only through search-engine summaries (M)**
- https://andonlabs.com/evals/vending-bench-arena
- https://andonlabs.com/blog/opus-5-5-gpt-6-sol-grok-4-7-vending-bench
- https://andonlabs.com/blog/gpt-6-astra-vending-bench
- https://andonlabs.com/blog/opus-4-8-vending-bench
- https://arxiv.org/html/2502.15840v1

**Secondary (L/M)**
- GDPval: https://github.com/turbobeest/modelspec/blob/main/benchmarks/gdpval.md · https://github.com/howard86/howardism/blob/main/apps/blog/src/content/articles/gdpval-benchmark.mdx · https://github.com/zhaoyang97/Paper-Notes-en · https://github.com/memgrafter/research-digests
- AA-Omniscience: https://github.com/memgrafter/research-digests (2511.13029 digest) · https://github.com/debajyotidasgupta/prophet-bench/blob/main/docs/research/hard_knowledge_calibration_review.md · https://github.com/ia3andy/devoured (AA Opus 4.5 note) · https://github.com/Belkins/ai-dive-deep · https://github.com/SeanL128/alloyd
- BrowseComp: https://github.com/visual-snow/seshat/blob/main/web-research/openai/browsecomp.md
- Competitive programming: https://github.com/ringlyra/web-summary (LiveCodeBench Pro) · https://github.com/adamghaida/ai-hall-of-fame · https://github.com/audst/audst.github.io/blob/main/data/benchmarks.csv
- Vending-Bench 2 mid-table: https://github.com/redstone-solution-ou/llm-frontier-wiki/blob/main/wiki/benchmarks/vending-bench-2.md
- GPT-6.1 Sol vs Astra, GDPval-AA: https://www.orcarouter.ai/blog/gpt-6-1-sol-vs-gpt-6-astra
- StudentBench listing date: https://github.com/vollero/hf-daily-paper-summaries/blob/main/summaries/2026/09/2026-09-24/2609.28470.md
- Fiction.LiveBench via Epoch: https://github.com/LeeHengYu/mediator-coevo

**Could not verify (blocked or budget exhausted)**
- andonlabs.com (direct), openai.com (GDPval, BrowseComp, GPT-6 pricing), artificialanalysis.ai (current Omniscience and GDPval-AA boards), eqbench.com (EQ-Bench 4 values), kaggle.com (SimpleQA Verified), fiction.live numbers, lmarena.ai, arxiv.org PDFs.
- Full Vending-Bench 2 rows beyond the top 10.
- GPT-6 Astra, Sol and Grok 4.7 prices.

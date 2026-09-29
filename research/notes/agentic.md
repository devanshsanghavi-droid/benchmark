# Agentic, Tool-Use, and Computer-Use Benchmarks

**Evidence legend.** Each factual statement carries one tag:

- **[V]** Verified. I read it this session in a primary source: the official repo README, changelog or BibTeX, an official leaderboard data file, or the benchmark's own website source on GitHub.
- **[S]** Secondary. I read it this session, but in a third-party README or aggregator that quotes the primary source.
- **[R]** Re-analysis. My own computation this session on the benchmark's public raw data. The method is stated with the result.
- **[U]** Unverified. A widely repeated figure that I did **not** see in any source this session. It is listed only so it can be checked. Do not cite [U] items without checking.

**Method note (read first).** The session-wide WebSearch budget was already used up when this subagent started, so no web searches ran. WebFetch and curl were blocked for arxiv.org, huggingface.co, metr.org, os-world.github.io, taubench.com, andonlabs.com and openaipublic.blob.core.windows.net. The evidence therefore comes from:

1. Official GitHub repos: READMEs, CHANGELOGs, BibTeX and leaderboard tables.
2. The GitHub source repos of official benchmark websites, which hold the leaderboard data files: `os-world/os-world.github.io` (OSWorld-Verified xlsx) and `cybench/cybench.github.io` (leaderboard.csv).
3. METR's public raw run data (`METR/eval-analysis-public`). I re-fitted METR's time-horizon model on it.

Some well-known headline figures could not be re-verified this way. They are marked [U] and collected in the list of unverified items at the end of the claims ledger.

One caution came up in practice. The WebFetch summariser twice invented details that are not in the underlying file: a "human-level ~72%" line for OSWorld 2.0, and "~89% human on 233 tasks" for VisualWebArena. I then re-read every raw file directly with curl/grep, and only text confirmed that way is tagged [V].

---

## Summary

Agentic benchmarks score a model plus scaffold that takes multi-step actions in an environment: browser, OS, shell, simulated customer, or company intranet. They have become the main capability currency of 2025-2026 frontier model cards and third-party trackers. Their life cycle is much faster and messier than that of static QA benchmarks. Five patterns stand out.

1. **Launch-to-saturation is now roughly 12-24 months, even for "hard" agentic suites.**
   - OSWorld: the best model scored 12.24% against a 72.36% human baseline at launch (Apr 2024). The best verified entry reached 90.19% in Jul 2026. That was **above the human baseline by Dec 2025**, and the maintainers released OSWorld 2.0 in Jun 2026. [V]
   - Cybench: the best unguided solve rate was about 17.5% at launch (2024). Lab-reported scores reached 93-100% on 35-37-task subsets by 2026. [V]
   - MLE-bench: any-medal rate went from 17.1% (Oct 2024) to 64.4% (Feb 2026). [V]

2. **Outcome-validity bugs are endemic, and they move scores by many points.**
   - τ-bench: a do-nothing agent scored 38% (ABC audit). [V] τ³-bench shipped "75+ task fixes", covering 27 of 50 airline tasks and 26 of 114 retail tasks. [V] A 2026 grading fix (v1.0.1, 2026-07-15) moved GPT-5.5 xhigh's banking_knowledge pass^1 from 37.37 to 46.39. The non-comparability notice covers that domain only. [V] [corrected by fact-check]
   - OSWorld: 13 of 46 Chrome tasks broke because live websites changed. [V]
   - WebArena: a do-nothing agent passes 4.4% of tasks. [V]
   - The ABC checklist project page puts benchmark misrepresentation at "up to 40%" on popular benchmarks. [V] [corrected by fact-check] The citable arXiv version (arXiv:2507.02825) says instead that such issues "can lead to under- or overestimation of agents' performance by up to 100% in relative terms". Cite the paper figure, or name the project page as the source of the 40%.
   - The field's response is a wave of "-Verified" or versioned re-releases: OSWorld-Verified (Jul 2025), WebArena-Verified (Dec 2025), τ³-bench (2026), MLE-bench v2 (announced), OSWorld 2.1 (Sep 2026). [V]

3. **Harness and budget sensitivity rivals the gap between models.**
   - On OSWorld-Verified, the same model (Claude Sonnet 4.5) scores 42.88%, 58.08% and 62.88% at 15, 50 and 100 steps. o3 scores 9.1%, 17.17% and 23.0%. [V]
   - MLE-bench froze its leaderboard in Apr 2026 "while we develop an improved process for ensuring submissions are fair and comparable". [V]
   - HAL, the cross-benchmark cost-aware leaderboard, stopped updating and archived its harness. [V]
   - Labs report benchmark subsets and different graders, for example "GAIA-Text-103" with an LLM-judge template instead of the full validation set with the official scorer. [V]

4. **The benchmarks that "won" (METR time horizon, GDPval, τ²/τ³, OSWorld, Cybench) share three features:**
   - an interpretable, externally anchored unit: human task-time, expert win-rate, pass^k reliability, or a human baseline;
   - an actively maintained, versioned artefact;
   - uptake in lab model cards or government pre-deployment testing.

   Cybench's own site lists use by US and UK AISI and in Anthropic, xAI, Amazon and Meta model cards. [V]

5. **METR's time-horizon metric shows best how a unit of measurement creates a durable longitudinal narrative.**
   - It turns heterogeneous pass/fail data into "the length of human-expert task the model completes with 50% reliability". The unit stays comparable across model generations (GPT-2 in 2019 to Claude Opus 4.6 in 2026) and across task-suite versions. [V/R]
   - My re-fit of METR's public data reproduces the ~7-month doubling for 2019 to Feb 2025 (7.1 months). [R] Frontier doubling since 2024 is faster: 3.4-4.6 months depending on suite version. [R]
   - The metric's weak point is now its long-task tail. In TH1.1, **26 of the 31 tasks ≥ 8 h have *estimated*, not measured, human times**, and 12 sit at exactly 480 min. [R] The top 2026 estimate is Claude Opus 4.6 at ~12 h. [corrected by fact-check] METR's own figure caption (`reports/time-horizon-1-1/fig_params/figs.yaml`) gives "about 12 hours (95% CI: 5 hrs to 66 hrs)". The earlier "~5-51 h" came from a simplified 200-resample bootstrap. A family-task-run bootstrap (300 resamples) gave ~5-77 h, so the upper bound is unstable. Cite METR's 5-66 h. It is an extrapolation near the edge of the task distribution.

---

## Benchmark-by-benchmark

### 1. METR time-horizon measurements (HCAST + RE-Bench + SWAA → "50% time horizon")

**What it measures.** METR's method has four steps. [V]

1. Collect tasks with known human completion times.
2. Run agents on them.
3. Fit a logistic curve of P(success) against log2(human minutes), per model.
4. Report the task duration at which predicted success is 50% (p50). An 80% horizon (p80) is reported as well.

**Release and venue.** "Measuring AI Ability to Complete Long Tasks", METR, arXiv:2503.14499 (2025). The repo BibTeX lists the author as "METR". [V] [corrected by fact-check] The arXiv listing gives 25 authors: Thomas Kwa, Ben West, Joel Becker, …, Elizabeth Barnes, Lawrence Chan. Cite it as Kwa, West, et al. (2025), which METR's own figs.yaml also does. The abstract gives Claude 3.7 Sonnet a horizon of "around 50 minutes" and says doubling was "approximately every seven months since 2019, though the trend may have accelerated in 2024" (listing mirror https://raw.githubusercontent.com/Luvata/arxive/main/pages/2025-03-19-cs-ai.html). The GitHub analysis repo (`METR/eval-analysis-public`) has two reports:

- **Time Horizon 1.0**, described as "48+ models", on the original metr-task-standard framework.
- **Time Horizon 1.1**, "an updated task suite". The TH1.1 commit is dated **21 Jan 2026**, and further pipeline syncs followed through 6 Mar 2026. [V]

**Creators.** METR. Component suites:

- **HCAST** ("Human-Calibrated Autonomy Software Tasks"). The public subset is at `METR/hcast-public`, BibTeX "METR 2025". [V]
- **RE-Bench**: Wijk, Lin, Becker, Jawhar, Parikh et al. (22 authors), arXiv:2411.15114, 7 AI-R&D environments. [V] Venue: ICML 2025 (Spotlight), per the paper-copilot ICML 2025 list. [corrected by fact-check]
- **SWAA**: short software atomic actions. Source-count evidence is in the data. [R]

**Items and format** (from the public raw data, [R]):

| | TH1.0 public data | TH1.1 public data |
|---|---|---|
| Tasks | 170 | 228 |
| HCAST / SWAA / RE-Bench | 97 / 66 / 7 | 157 / 66 / 5 |
| Task families | 50 | 79 |
| Median human time | 10.0 min | 12.6 min [corrected by fact-check] |
| Maximum human time | 1,112 min | 1,800 min |
| Tasks ≥ 8 h | 14 | 31 |
| Agent runs / models | — | 23,235 runs across 20 models (median 4 runs per model-task) |

Task types are software, ML-engineering, cyber and reasoning tasks in METR's Task Standard format, run as containerised agent tasks. METR's Task Standard README says that "as of Jan 2024" METR had "~200 task families containing ~2000 tasks". [V]

**Headline results.**

- The repo states: "AI agent time horizons have been doubling approximately every 7 months." [V]
- **My re-fit** replicates METR's logistic fit. I used `sklearn` LogisticRegression with C = 1/1e-5, the `invsqrt_task_weight` diversity weights and binarised scores, exactly as in `reports/time-horizon-1-1/fig_params/figs.yaml` and `src/horizon/utils/logistic.py`. [R] The resulting p50 horizons in minutes (TH1.1, with TH1.0 in brackets):

| Model (release) | p50 TH1.1 | p50 TH1.0 | p80 TH1.1 |
|---|---|---|---|
| GPT-4 0314 (Mar 2023) | 4.0 | 6.0 | 0.9 |
| GPT-4o (May 2024) | 7.0 | 10.2 | 1.3 |
| Claude 3.5 Sonnet New (Oct 2024) | 20.5 | 30.5 | 2.6 |
| o1 (Dec 2024) | 38.8 | 41.6 | 7.1 |
| Claude 3.7 Sonnet (Feb 2025) | 60.4 | 55.3 | 12.1 |
| o3 (Apr 2025) | 119.7 | 91.4 | 30.0 |
| GPT-5 (Aug 2025) | 203.0 | 130.8 | 38.3 |
| Gemini 3 Pro (Nov 2025) | 224.3 | — | 54.1 |
| Claude Opus 4.5 (Nov 2025) | 293.0 | 246.8 | 49.4 |
| GPT-5.2 (Dec 2025) | 352.2 | — | 66.0 |
| GPT-5.3-Codex (Feb 2026) | 349.5 | — | 54.7 |
| **Claude Opus 4.6 (Feb 2026)** | **718.8** (≈12 h) | — | 69.9 |

Release dates come from METR's `data/external/release_dates.yaml`. [V] My re-fit may differ slightly from METR's published figures, because the full pipeline may apply exclusions or bootstrap medians. Cite METR's own numbers where available.

**Doubling time on the public data, fitted on the running-max (SOTA) models.** [R]

- TH1.0, 2019 (GPT-2) to Feb 2025 (Claude 3.7 Sonnet): **7.1 months**. This matches METR's headline.
- TH1.0, SOTA models from 2024 on: 4.6 months.
- TH1.1, SOTA models from 2024 on: 3.4 months.
- TH1.1, from 2025 on: 4.0 months.

**Uncertainty.** I ran a hierarchical bootstrap (task family, then task; 200 resamples). [R] The approximate 95% CIs are:

- Claude Opus 4.6: 309-3,037 min. [corrected by fact-check] METR's own reported CI is 5-66 h (≈300-3,960 min). A family→task→run bootstrap matching METR's `bootstrap.py` categories (300 resamples, this check) gave ≈300-4,624 min. Use METR's figure.
- GPT-5.2: 206-840 min.
- Claude Opus 4.5: 179-543 min.
- GPT-5: 123-414 min.

The frontier CI now extends beyond the longest task in the suite (1,800 min).

**Adoption evidence.** [V]

- The TH1.0 data covers 33 model aliases (plus human baselines), including open-weight models: DeepSeek, Qwen, Kimi K2 Thinking and gpt-oss.
- TH1.1 covers 20, through Feb 2026.
- The metric is re-used by other benchmarks. Cybench's site reports "First Solve Time by Humans", an analogous human-time unit.
- Lab model-card citations of the time horizon were **not verified** this session. [U]

**Status.** Thriving: the reference longitudinal metric. It is contested at the long-task tail.

**Why it succeeded.** [interpretation]

- (a) **The unit is human labour time.** Anyone can read it ("tasks that take an expert ~4 hours"), and it maps onto economic and safety narratives.
- (b) It aggregates heterogeneous suites (SWAA seconds-scale to RE-Bench 8-hour tasks) into one scale. That gives a **long dynamic range**: the TH1.0 data spans GPT-2 at 0.05 min to Opus 4.5 at about 4.1 h, roughly 4,600×. [R]
- (c) It **extends by adding longer tasks** instead of being replaced, as the TH1.0 → TH1.1 step shows. So the time series survives saturation of any one suite.
- (d) The data and code are public. That makes the result re-computable, as done here.

**Why it is failing or at risk.** [R + interpretation]

- (a) **Scarce, estimated long-task times.** In TH1.1, 26 of 31 tasks ≥ 8 h, and 7 of 9 tasks ≥ 12 h ([corrected by fact-check]: "≥", not ">"; only 8 tasks are strictly > 720 min), use `human_source = "estimate"`. Twelve estimates are exactly 480 min and five are exactly 600 min. [R] The 2026 frontier horizons are fitted mostly on estimated durations.
- (b) **The slope is flattening.** Claude Opus 4.6 has p80 = 70 min against p50 = 719 min, with 96% success on sub-1-h tasks but 47% on ≥ 8-h tasks. [R] The p50 therefore depends heavily on a few long tasks.
- (c) **Suite-version sensitivity.** The same model moves by up to ~55% between TH1.0 and TH1.1: GPT-5 131 → 203 min, o3 91 → 120 min. [R] Cross-version comparisons need METR's stitching (`--benchmark-results-to-stitch` in dvc.yaml). [V]
- (d) **Domain scope.** The tasks are software, ML and cyber in containerised environments. Transfer to "messier" real work is an open question (interpretation).
- (e) Human baselining is expensive. The data's `human_cost` field sums to about $22.8k across the 162 baselined TH1.1 tasks, a median implied rate of about $144/h. [R; field semantics not documented, treat as indicative]

**Sources.**
- https://raw.githubusercontent.com/METR/eval-analysis-public/main/README.md
- https://github.com/METR/eval-analysis-public/commits/main
- https://raw.githubusercontent.com/METR/eval-analysis-public/main/reports/time-horizon-1-1/data/raw/runs.jsonl
- https://raw.githubusercontent.com/METR/eval-analysis-public/main/reports/time-horizon-1-0/data/raw/runs.jsonl
- https://raw.githubusercontent.com/METR/eval-analysis-public/main/data/external/release_dates.yaml
- https://raw.githubusercontent.com/METR/eval-analysis-public/main/reports/time-horizon-1-1/fig_params/figs.yaml
- https://raw.githubusercontent.com/METR/eval-analysis-public/main/src/horizon/utils/logistic.py
- https://raw.githubusercontent.com/METR/hcast-public/main/README.md
- https://raw.githubusercontent.com/METR/ai-rd-tasks/main/README.md
- https://raw.githubusercontent.com/METR/task-standard/main/README.md

### 2. RE-Bench (METR), also a component of the time-horizon suite

- **What it measures.** Frontier AI R&D ability of agents compared with human experts, on 7 open-ended ML research-engineering environments. Examples: "Build scaffolding for Rust Codecontests", "Finetune GPT-2 for QA with RL", "Optimize an LLM Foundry finetuning script", "Restricted architecture LLM". Each environment has a starting score and an official-solution score. [V]
- **Release.** arXiv:2411.15114 (Nov 2024). Wijk, Lin, Becker, Jawhar, Parikh, Broadley, Chan, Chen, Clymer, Dhyani, Ericheva, Garcia, Goodrich, Jurkovic, Kinniment, Lajko, Nix, Sato, Saunders, Taran, West, Barnes. [V]
- **Adoption.** It was ported to Inspect (`METR/inspect-tasks-public`, "RE-Bench-Inspect") [V], and 5 RE-Bench tasks appear in TH1.1. [R]
- **Status.** Active as a component, and niche as a standalone leaderboard.
- **Headline finding** ("agents beat humans at 2-h budgets, humans win at 8 h+"): **[U]**, not in the README seen.
- **Why it succeeded.** Expert human baselines, and continuous scores rather than pass/fail.
- **Weaknesses.** Only 7 environments, and GPU-heavy.
- **Contamination guard.** Password-protected solution zips, plus a request not to publish solutions (the password is published in the README). [V]

### 3. GDPval (OpenAI)

- **What it measures.** Performance on economically valuable, real-world knowledge-work deliverables (spreadsheets, documents, slides, reports). Deliverables are graded mainly by occupational experts through blinded pairwise comparison against human-expert deliverables. [S]
- **Release.** arXiv:2510.04374 (v1 2025-10-05). The dataset is `openai/gdpval` on Hugging Face. [S: link seen in 4 independent GitHub READMEs] [corrected by fact-check] The title is "GDPval: Evaluating AI Model Performance on Real-World Economically Valuable Tasks". There are 19 authors: Patwardhan, Dias, Proehl, Kim, Wang, Watkins, Posada Fishman, Aljubeh, Thacker, Fauconnet, Kim, Chao, Miserendino, Chabot, Li, Sharman, Barr, Glaese, Tworek (cached arXiv abs page). The paper was accepted at ICLR 2026 as a poster (paper-copilot ICLR 2026 list).
- **Items.**
  - Full set: 1,320 tasks. Public "gold subset": 220 tasks. Coverage: 44 occupations in 9 sectors. [V: arXiv abstract for 220 / 44 / 9 / 14 yrs; parsed paper text for 1,320] [corrected by fact-check] (upgraded from [S])
  - Task writers average 14 years of experience. [S]
  - One third-party environment exposes a single split, "testv2 (220 tasks)". [S]
- **Frontier scores.** All [S, medium confidence]; these are third-party READMEs quoting the paper.
  - Paper (Oct 2025), Fig. 5 on the gold subset, **wins + ties**: Claude Opus 4.1 47.6%, GPT-5 high 38.8%, o3 high 34.1%, o4-mini high 27.9%, GPT-4o 12.4%. [corrected by fact-check] The previously listed 39.0 / 35.2 / 29.1 / 12.5 come from the paper's Table 2 (speed/cost analysis), not the headline figure. The paper states that "47.6% of deliverables by Claude Opus 4.1 were graded as better than (wins) or as good as (ties) the human deliverable". Source: parsed paper https://raw.githubusercontent.com/visual-snow/seshat/main/parsed/openai/2510_04374.md.
  - Later: "GPT 5.2 Thinking: 70.9% win rate vs. industry professionals" (README dated around Dec 2025). [corrected by fact-check] This is also a **wins-or-ties** figure. Third-party copies of OpenAI's GPT-5.2 launch table (found via GitHub code search, e.g. `punitarani/modelbeats` data/results/gdpval.csv) give "ties allowed, wins or ties" 70.9% and "clear wins" 49.8%. That is secondary evidence; the OpenAI page itself was not fetched.
  - ~~Whether these figures are "wins" or "wins + ties" was not verified.~~ [corrected by fact-check] Resolved: both headline figures are wins + ties.
- **Adoption evidence.** [V as README existence; S as content]
  - Artificial Analysis runs **GDPval-AA**. It uses its own agent harness ("Stirrup") and **replaces expert graders with Gemini 3 Pro pairwise grading**, aggregated by Bradley-Terry Elo anchored at GPT-5.1 (non-reasoning) = 1000, with 1,000-resample bootstrap CIs.
  - Other third-party environments and pipelines: EnvCommons/OpenReward (grader gpt-5-mini with tool access; weighted rubric), gdpval-realworks, and Claude Code experiments.
- **Status.** Thriving, and contested on grading.
- **Why it succeeded.** [interpretation]
  - The unit is economically anchored (occupations weighted by contribution to GDP; "expert win-rate").
  - Tasks are realistic, multi-modal file deliverables.
  - The metric is a relative preference rather than a brittle exact match, so it does not saturate at a hard 100%, and 50% has a natural meaning ("parity with experts").
- **Why it is failing or at risk.** [interpretation, supported by the S evidence]
  - (a) Expert pairwise grading is slow and costly. Third parties therefore swap in LLM graders, which **changes the construct**: the benchmark name stays the same while the score now measures agreement with Gemini or GPT-5-mini.
  - (b) Only the 220-task gold subset is public. Replication and contamination control conflict.
  - (c) Win-rate against a fixed human deliverable saturates once models exceed experts, and it is sensitive to the grader's taste (formatting, length).
  - (d) The tasks are single-shot deliverables, without longer-horizon interaction.
- **Sources.**
  - https://raw.githubusercontent.com/hyeonsangjeon/gdpval-realworks/main/README.md
  - https://raw.githubusercontent.com/botschen/GDPVal_Eval/main/README.md
  - https://raw.githubusercontent.com/EnvCommons/GDPVal/main/README.md
  - https://raw.githubusercontent.com/amaarora/GDPVal/main/README.md

### 4. OSWorld → OSWorld-Verified → OSWorld 2.0 (XLANG Lab / HKU)

- **What it measures.** Multimodal computer-use agents doing open-ended tasks in real VMs (Ubuntu apps: Chrome, GIMP, LibreOffice, Thunderbird, VLC, VS Code, OS, multi-app), scored by execution-based checker scripts. [V]
- **Release.**
  - Paper, environment and benchmark: 2024-04-11, arXiv:2404.07972, NeurIPS 2024 (Datasets & Benchmarks track, poster; confirmed in the paper-copilot NeurIPS 2024 list). Authors: Xie, Zhang, Chen, Li, Zhao, Cao, Hua, Cheng, Shin, Lei, Liu, Xu, Zhou, Savarese, Xiong, Zhong, Yu. [V]
  - OSWorld-Verified: 2025-07-28. [V]
  - OSWorld 2.0: 2026-06-26, arXiv:2606.29537, Yuan, Zhou, Xiong, … Xie, Yu. osworld-v2.1 followed on 2026-09-16. [V] (Added by fact-check.) The arXiv abstract describes 108 long-horizon workflows with a human median of about 1.6 h. The best agent (Claude Opus 4.8, max thinking) completes 20.6% at 500 steps, and GPT-5.5 plateaus near 13% (listing mirror 2026-06-30-cs-ai).
- **Items.** 369 tasks. 8 Google-Drive tasks may be excluded, giving 361, which "is officially permitted". [V]
- **Frontier scores.**
  - Launch: "While humans can accomplish over 72.36% of the tasks, the best model achieves only 12.24% success." [V]
  - OSWorld-Verified leaderboard xlsx, 144 entries from 2025-07-28 to 2026-08-01. [V] Running best:

| Date | Entry | Score |
|---|---|---|
| 2025-07-28 | Claude 4 Sonnet (50 steps) | 43.9% |
| 2025-07-28 | GTA1 w/ o3 | 53.1% |
| 2025-10-04 | Agent S3 w/ GPT-5 bBoN (N=10) | 69.9% |
| 2025-12-11 | Agent S3 w/ Opus 4.5 + GPT-5 bBoN (N=10, multiple rollouts) | **72.58%**, passing the 72.36% human figure |
| 2026-02-25 | HIPPO Agent w/ Opus 4.5 (first *single-rollout* entry above 72.36%; denominator 358) [corrected by fact-check] | 74.48% |
| 2026-04-20 | Holo3-35B-A3B | 82.56% |
| 2026-07-25 | Intelligence-Indeed Agent | **90.19%** (325.59/361) |

  - Best Anthropic general-model entry: "claude-fable-5[1m]", 85.96% (2026-08-01).
  - **16 entries are at or above 72.36%.** [V/R]
- **Adoption.**
  - The OSWorld-Verified acknowledgements thank Moonshot AI (Kimi), OpenAI, Anthropic, ByteDance Seed TARS, Simular and others "that provided feedback and participated in the fixes". [V]
  - Leaderboard entries come from Anthropic, OpenAI, Meta (Muse Spark 1.1), Alibaba (Qwen), Moonshot (Kimi), MiniMax, Zhipu and ByteDance. [V]
  - The repo has 3,165 GitHub stars. [V]
- **Status.** v1/Verified is **saturated**, above the human baseline. OSWorld 2.0 is **active**.
- **Why it succeeded.** [interpretation]
  - A real OS, not a simulator.
  - Execution-based checkers.
  - A human baseline.
  - Per-application breakdowns.
  - A verified leaderboard where the maintainers re-run submitted agents ("schedule a meeting with us to run your agent code on our side"). [V]
  - Cooperation with labs on fixes.
- **Why it is failing.**
  - (a) **Saturation.**
  - (b) **Live-web rot.** ABC found 13/46 Chrome tasks broken by site changes (e.g. a delta.com CSS class disappeared). Fixing them moved UI-TARS from 24/46 to 37/46 on Chrome (52% → 80%) and from 42.5% to 46% overall. [V]
  - (c) **Harness and step-budget sensitivity** (step counts are recorded in the xlsx) [V]:

| Model | 15 steps | 50 steps | 100 steps |
|---|---|---|---|
| Claude Sonnet 4.5 | 42.88% | 58.08% | 62.88% |
| o3 | 9.1% | 17.17% | 23.0% |
| OpenAI CUA | 26.0% | 31.3% | 31.4% |

  - (d) **Environment fragility.** "Proxy configuration … depends on the strength of website defenses", and Google-account OAuth is needed; "If these configurations are not properly set up … lower evaluation scores." [V]
  - (e) **Best-of-N and multi-rollout** entries (bBoN N=10) mix test-time compute with capability.
- **Mitigations in OSWorld 2.0.** [V]
  - Gated task classes on HF "to reduce benchmark leakage and help prevent evaluated agents from finding task answers, setup logic, or evaluator details online while executing a task". This is a new, agent-specific contamination vector.
  - Mocked websites and a self-hosted GitLab.
  - Release manifests that pin code, task, asset, website and VM-image versions, with "fail fast for comparable runs".
  - Three releases in three months: 2026.06.24, 2026.08.08, v2.1.
- **Sources.**
  - https://raw.githubusercontent.com/xlang-ai/OSWorld/main/README.md
  - https://raw.githubusercontent.com/os-world/os-world.github.io/main/index.html
  - https://raw.githubusercontent.com/os-world/os-world.github.io/main/static/data/osworld_verified_results.xlsx
  - https://raw.githubusercontent.com/xlang-ai/OSWorld-V2/main/README.md
  - https://raw.githubusercontent.com/xlang-ai/OSWorld-V2/main/docs/MIGRATING_v2.1_FROM_OSWORLD_V1.md
  - https://raw.githubusercontent.com/xlang-ai/OSWorld-V2/main/benchmark_releases/README.md
  - https://raw.githubusercontent.com/uiuc-kang-lab/agentic-benchmarks/main/benchmarks/osworld/README.md
  - https://github.com/xlang-ai

### 5. τ-bench → τ²-bench → τ³-bench (Sierra)

- **What it measures.** Tool-agent-user interaction. An agent with domain API tools and a policy document serves an LLM-simulated user. Success is judged by final database state plus required outputs. **pass^k** gives the probability that all k i.i.d. trials succeed, which measures reliability. [V]
- **Release.** [V]
  - τ-bench: arXiv:2406.12045 (Jun 2024). Yao, Shinn, Razavi, Narasimhan.
  - τ²-bench: "Evaluating Conversational Agents in a Dual-Control Environment", arXiv:2506.07982. Barres, Dong, Ray, Si, Narasimhan. v0.1.0 on 2025-06-12; adds the telecom dual-control domain.
  - τ³-bench, i.e. tau2-bench v1.0.0 (2026) plus v1.0.1 on 2026-07-15. Adds τ-Knowledge (banking_knowledge, arXiv:2603.04370; Shi, Zytek, Razavi, Narasimhan, Barres), τ-Voice (full-duplex audio, arXiv:2603.13686; Ray, Dhandhania, Barres, Narasimhan) and task fixes.
- **Items** (current repo, `tasks.json`). [R] Airline 50 tasks (train 30 / test 20). Retail 114 (74/40). Telecom 114 base (2,285 full). banking_knowledge 97 tasks with 698 policy documents. [V]
- **Frontier scores.**
  - τ-bench launch leaderboard, pass^1 [V]:

| Model | Retail | Airline |
|---|---|---|
| Claude 3.5 Sonnet (1022) | 0.692 | 0.460 |
| GPT-4o | 0.604 | 0.420 |

  - Retail pass^4 for Claude 3.5 Sonnet was 0.462: reliability drops sharply with k. [V]
  - τ² in lab READMEs [V]: Kimi K2 reports "Tau2 airline/retail/telecom (Avg@4)". MiniMax-M2 (Oct 2025) reports τ²-Bench 77.2, GPT-5 (thinking) 80.1*, Claude Sonnet 4.5 84.7*.
  - Banking_knowledge, re-graded under v1.0.1: GPT-5.5 xhigh 46.39 and GPT-5.4 xhigh 39.43, up from 37.37 and 30.67. [V]
- **Adoption.** The live leaderboard is at taubench.com. It is used in open-weight lab model READMEs (Kimi K2, MiniMax-M2) [V] and is part of HAL. [V]
- **Status.** τ² and τ³ are thriving. The original τ-bench repo is **deprecated**: "The tasks in this repo are not updated." [V] Grading is contested.
- **Why it succeeded.** [interpretation]
  - Realistic enterprise setting: policy compliance plus tools plus a user.
  - Cheap text-only runs.
  - A **reliability metric (pass^k)** that tracks deployment concerns better than pass@k.
  - Active maintainers who extend domains (telecom dual-control, knowledge retrieval, voice) rather than letting it die.
- **Why it is failing or contested.** [V]
  - (a) **Outcome validity.** ABC found that 38% of airline and 6% of retail tasks were intentionally unsolvable, and they pass if the DB is unchanged. A **do-nothing agent scored 38%**, and a DB-dumping spam agent scored 40%.
  - (b) **Label errors.** The τ³ fixes (based on SABER, arXiv:2512.07850) corrected 27 airline tasks, 54% of the 50. Categories: incorrect expected actions (e.g. tasks 2, 27 and 38 wrongly expected compensation), ambiguous instructions, "impossible or contradictory constraints" and "policy loophole" tasks. They also corrected 26 retail tasks and 20+ banking tasks.
  - (c) **Non-comparability across versions.** [corrected by fact-check] The exact CHANGELOG wording is "Scores produced with tau2-bench < 1.0.1 on `banking_knowledge` must not be compared against scores produced with >= 1.0.1". The notice covers the banking_knowledge domain only, not all domains. Re-grading raised scores "by up to ~9 points pass^1".
  - (d) **User-simulator noise.** The changelog adds a "hallucination reviewer for detecting user simulator deviations" and "automatic hallucination retry". Infrastructure errors are excluded from pass^k.
- **Sources.**
  - https://raw.githubusercontent.com/sierra-research/tau-bench/main/README.md
  - https://raw.githubusercontent.com/sierra-research/tau2-bench/main/README.md
  - https://raw.githubusercontent.com/sierra-research/tau2-bench/main/CHANGELOG.md
  - https://raw.githubusercontent.com/sierra-research/tau2-bench/main/data/tau2/domains/airline/tasks.json
  - https://raw.githubusercontent.com/uiuc-kang-lab/agentic-benchmarks/main/benchmarks/tau-bench/README.md
  - https://raw.githubusercontent.com/MoonshotAI/Kimi-K2/main/README.md
  - https://raw.githubusercontent.com/MiniMax-AI/MiniMax-M2/main/README.md

### 6. GAIA (General AI Assistants)

- **What it measures.** Real-world questions that are "conceptually simple for humans yet challenging for most advanced AIs". They need reasoning, multimodality, web browsing and tool use, with short exact-match answers at three difficulty levels. [S: README quoting the paper]
- **Release.** arXiv:2311.12983 (Nov 2023). [V] [corrected by fact-check] The v1 authors are Grégoire Mialon, Clémentine Fourrier, Craig Swift, Thomas Wolf, Yann LeCun and Thomas Scialom (arXiv listing mirror 2023-11-24). The ICLR 2024 version, a poster per paper-copilot, lists five of them, without Swift. The hosted leaderboard is at huggingface.co/spaces/gaia-benchmark/leaderboard (URL seen). [V]
- **Items.**
  - The UK AISI Inspect implementation says "450 questions". [V] The validation split has **165 questions** (Level 1/2/3 = 53/86/26). [V]
  - The test split "does not come with any solutions … solutions are uploaded to the online leaderboard". [V]
  - The paper's total of 466 questions, with answers retained for 300, is confirmed in the arXiv v1 abstract. [corrected by fact-check] (was [U])
- **Frontier scores.**
  - At launch: "human respondents obtain 92% vs. 15% for GPT-4 equipped with plugins" is confirmed in the arXiv v1 abstract. [corrected by fact-check] (was [U])
  - Later [V]:
    - HF Open Deep Research: "55% pass@1 on the GAIA validation set, compared to 67% for the original Deep Research" (early 2025).
    - CAMEL OWL: 69.09% (open-source framework).
    - MiroThinker v1.0 (2025-11-13): 81.9% on "GAIA-Text-103".
    - MiroThinker v1.5 (2026-01-05): 80.8% on GAIA-Val-165.
    - MiroThinker 1.7 (2026-03-11): 82.7% on GAIA-Val-165.
    - MiniMax-M2 (Oct 2025): 75.7 on "GAIA (text only)" versus GPT-5 (thinking) 76.4.
- **Adoption.** [V]
  - One of the ten benchmarks audited by ABC, with an overall ABC score of 71.3.
  - In UK AISI inspect_evals and METR's Task Standard examples.
  - Widely used by open deep-research agents (smolagents, OWL, MiroThinker) and in open-weight lab READMEs (MiniMax).
- **Status.** Near-saturated on validation and **fragmented**. It is mostly an open-source-agent benchmark now; frontier closed-lab usage was not verified.
- **Why it succeeded.** [interpretation] Short unambiguous answers make scoring cheap and exact. It was an early, general "assistant" framing, and has a hidden test set.
- **Why it is failing.** [V + interpretation]
  - (a) **Subset proliferation.** Labs report "GAIA-Text-103", a text-only subset of validation, "using the WebAgents LLM-as-a-Judge template", rather than the official scorer on the full 165 or the hidden test set. [V: MiroThinker and MiniMax READMEs] [corrected by fact-check] Only the MiroThinker README states the LLM-judge template. MiniMax-M2 states only that it uses "the 103-sample text-only GAIA validation subset following WebExplorer" and does not name its grader. MiroThinker v1.5 and 1.7 report Val-165 with the official scorer. The numbers are not comparable across reports.
  - (b) **The public validation set is the de facto benchmark.** It is exposed to contamination and tuning. ABC scores GAIA 0 on R.3 ("does not contain measures to prevent data contamination") and R.4 (no plan to update tasks). [V]
  - (c) No reference harness (ABC T.3 and R.2 = 0) and no confidence intervals (R.10 = 0). [V]
  - (d) Multimodal files are handled by pre-processing: MiroThinker uses GPT-4o to caption images and audio for a text-only model. [V] The same score therefore mixes different pipelines.
- **Sources.**
  - https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_evals/main/src/inspect_evals/gaia/README.md
  - https://raw.githubusercontent.com/AnyEvalOrg/eval-gaia/main/README.md
  - https://raw.githubusercontent.com/uiuc-kang-lab/agentic-benchmarks/main/assessments/gaia.yaml
  - https://raw.githubusercontent.com/huggingface/smolagents/main/examples/open_deep_research/README.md
  - https://raw.githubusercontent.com/camel-ai/owl/main/README.md
  - https://raw.githubusercontent.com/MiroMindAI/MiroThinker/main/README.md
  - https://raw.githubusercontent.com/MiniMax-AI/MiniMax-M2/main/README.md

### 7. WebArena → WebArena-Verified

- **What it measures.** Autonomous web agents in self-hosted, realistic sites: e-commerce, CMS admin, Reddit clone, GitLab, map and Wikipedia. It has 812 tasks with functional and programmatic evaluation. [V]
- **Release.** arXiv:2307.13854 (Jul 2023). Zhou, Xu, Zhu, Zhou, Lo, Sridhar, Cheng, Bisk, Fried, Alon, et al. [V] The WebArena-x site lists "NeurIPS 2024 · Oral". [V as displayed] [corrected by fact-check] The venue is **ICLR 2024 (poster)**, per the paper-copilot ICLR 2024 list and the VisualWebArena README BibTeX. The WebArena-x label is wrong; do not cite it.
- **Frontier scores.** At launch, human 78.24% vs GPT-4 14.41% is **[U]**. [corrected by fact-check] The arXiv v1 abstract (Jul 2023) reports the best GPT-4 agent at **10.59%**. The 14.41% / 78.24% pair presumably comes from a later version and was not seen this session. The leaderboard is a Google Sheet (link seen), and no numbers were verified.
- **Adoption.** [V]
  - The canonical harness moved to ServiceNow's AgentLab and BrowserGym (README update 12/5/2024).
  - Spin-offs: VisualWebArena, TheAgentCompany, WebArena-Infinity.
  - WebArena-Verified (ServiceNow; El hattami, Thakkar, Chapados, Pal). Presented at the NeurIPS 2025 SEA workshop, with public release scheduled for 2025-12-04 and PyPI in Jan 2026. "Every task, reference answer, and evaluator has been manually reviewed and corrected". It "removed LLM-as-a-judge evaluation and substring matching in favor of type-aware normalization". It adds offline evaluation via network-trace replay and a 258-task "Hard" subset for cost.
- **Status.** The original is **contested**. The Verified version is active.
- **Why it succeeded.** [interpretation] Self-hosted, resettable, realistic websites made it the first reproducible web-agent benchmark. It became a standard substrate for later work.
- **Why it failed.** [V]
  - ABC overall score 45.4, second-lowest of the ten audited.
  - A do-nothing agent passes **4.4%** of tasks ("These tasks use N/A as the ground truth").
  - The substring matcher ignores negation and does not penalise listing every candidate answer.
  - The LLM judge is not hardened against adversarial inputs.
  - Only relevant state is checked.
  - The Reddit clone can rate-limit.
  - There is no contamination plan.
  - Heavy self-hosting: several Docker sites. The Verified release ships images "up to 92% smaller".
- **Sources.**
  - https://raw.githubusercontent.com/web-arena-x/webarena/main/README.md
  - https://raw.githubusercontent.com/ServiceNow/webarena-verified/main/README.md
  - https://raw.githubusercontent.com/uiuc-kang-lab/agentic-benchmarks/main/assessments/webarena.yaml
  - https://raw.githubusercontent.com/uiuc-kang-lab/agentic-benchmarks/gh-pages/index.html
  - https://raw.githubusercontent.com/web-arena-x/web-arena-x.github.io/master/index.html

### 8. VisualWebArena

- **What it measures.** Multimodal web agents on visually grounded tasks. It has 910 tasks on Classifieds, Shopping, Reddit, Wikipedia and Homepage sites. [V]
- **Release.** arXiv:2401.13649 (Jan 2024), ACL 2024 (as shown on the WebArena-x site). Koh, Lo, Jang, Duvvur, Lim, Huang, Neubig, Zhou, Salakhutdinov, Fried. [V]
- **Scores.** The launch agent was GPT-4V + Set-of-Mark; its trajectories were released for all 910 tasks. [V] The human success rate is **[U]**: the summariser's "~89%" was not in the raw README.
- **Status.** Niche or stale. The last README news is dated 08/05/2024 (AMI release). [V]
- **Why it succeeded.** It was the first realistic visual web benchmark, and SoM prompting became a standard technique.
- **Why it is fading.** [interpretation] It shares WebArena's self-hosting cost. Its capability is absorbed by computer-use benchmarks (OSWorld) and live-web browsing benchmarks (BrowseComp). It has no maintained leaderboard.
- **Source.** https://raw.githubusercontent.com/web-arena-x/visualwebarena/main/README.md

### 9. BrowseComp (OpenAI) and BrowseComp-Plus

- **What it measures.** "A Simple Yet Challenging Benchmark for Browsing Agents": hard-to-find, short-answer facts that need persistent, creative web search and are easy to verify. Grading uses an LLM grader template that extracts the final answer and a confidence. [V]
- **Release.** arXiv:2504.12516 (Apr 2025; ID seen in MiroThinker README). Jason Wei, Zhiqing Sun, Spencer Papay, Scott McKinney, Jeffrey Han, Isa Fulford, Hyung Won Chung, Alex Tachard Passos, William Fedus, Mia Glaese. [V: `browsecomp_eval.py` docstring] [corrected by fact-check] On arXiv the last author is listed as "Amelia Glaese" (listing mirror 2025-04-18-cs-cl). Use the arXiv form.
- **Contamination guard.** The dataset is served as an XOR-encrypted CSV with a per-row "canary" key. [V]
- **Items.** 1,266 questions, confirmed in the arXiv abstract. [corrected by fact-check] (was [U])
- **Frontier scores.**
  - Launch: OpenAI Deep Research 51.5% (as quoted in a third-party table). [S]
  - MiniMax-M2 README (Oct 2025): GPT-5 (thinking) 54.9*, Claude Sonnet 4.5 19.6, MiniMax-M2 44. [V]
  - MiroThinker v1.5-235B: 69.8% (2026-01-05). MiroThinker-1.7: 74.0% (2026-03-11). The README headline says MiroThinker "achieves a 88.2" (proprietary H1 agent). [V as self-report]
- **Adoption.** [V] BrowseComp is one of three evals still maintained in simple-evals after Jul 2025 ("simple-evals will no longer be updated for new models or benchmark results"). It is standard in deep-research and open-weight lab READMEs (DeepSeek-V3.2-Exp, GLM-4.5, MiniMax-M2, Tongyi DeepResearch, MiroThinker). A Chinese variant, BrowseComp-ZH (arXiv:2504.19314), exists.
- **Status.** Active and approaching saturation. Reproducibility is contested.
- **Why it succeeded.** [interpretation] Asymmetric difficulty (hard to find, easy to verify) gives cheap and reliable grading. The single number is intuitive, the data is encrypted against contamination, and it arrived just as "deep research" products launched.
- **Why it is failing.**
  - (a) **The live web is non-stationary and uncontrolled.** BrowseComp-Plus (arXiv:2508.06600; Chen, Ma, Zhuang, … Chen, Lin) was created because live-web evaluation hinders "fair, transparent, and reproducible comparisons". (Fact-check: supported. The arXiv abstract says "dynamic and opaque web APIs hinder fair comparisons and reproducibility of deep research methods".) It freezes 830 queries against "a fixed, curated corpus of ~100K human-verified documents". [V]
  - (b) **Harness and budget tuning per benchmark.** MiroThinker uses a special "max300" tool-call configuration only for BrowseComp and warns that "to reproduce our reported results, you must set the correct AGENT_SET". [V]
  - (c) Answers can leak onto the web once published (interpretation).
- **Sources.**
  - https://raw.githubusercontent.com/openai/simple-evals/main/browsecomp_eval.py
  - https://raw.githubusercontent.com/openai/simple-evals/main/README.md
  - https://raw.githubusercontent.com/texttron/BrowseComp-Plus/main/README.md
  - https://raw.githubusercontent.com/MiroMindAI/MiroThinker/main/README.md
  - https://raw.githubusercontent.com/MiniMax-AI/MiniMax-M2/main/README.md

### 10. Vending-Bench and Vending-Bench 2 (Andon Labs)

- **What it measures.** Long-term coherence. An agent runs a simulated vending-machine business over very long horizons (">20M tokens" per run) and is scored by final net worth. [S]
- **Release.** "Vending-Bench: A Benchmark for Long-Term Coherence of Autonomous Agents", arXiv:2502.15840 (Feb 2025). [S: link seen in a recreation's README] [corrected by fact-check] The authors are Axel Backlund and Lukas Petersson (Andon Labs), per the arXiv listing mirror 2025-02-25-cs-ai. The abstract itself stresses "high variance in performance". Vending-Bench 2 is at andonlabs.com/evals/vending-bench-2 (URL seen; page blocked).
- **Parameters.**
  - VB2, per a third-party recreation [S, low-medium]: 365 simulated days, a $500 starting balance, a $2/day fee, output tokens billed at $100 per 1M weekly, and bankruptcy after 10 consecutive days of unpaid fees.
  - VB1, per another recreation [S]: $500 start.
- **Frontier scores.** Not verified. **[U]** A third-party README claims Grok 4 Fast is "#1 … as of November 2025" with $4,921. It looks promotional and is not usable.
- **Adoption.** [V] The concept is widely copied: ProsusAI's open-source "long-horizon agentic business simulation served over MCP, shipped as a Harbor task", plus several recreations. That is itself a sign that the original environment is **not openly released** (inference).
- **Status.** Active but closed. Niche as a leaderboard, and influential as a concept.
- **Why it succeeded.** [interpretation] It targets long-horizon coherence, a failure mode (derailment over millions of tokens) that short-task suites miss. The score is money, which needs no explanation and has no ceiling. The anecdotes are compelling.
- **Why it is failing.** [interpretation]
  - A closed environment and simulator means it cannot be reproduced.
  - It is a single run in a stochastic simulation, which gives high variance.
  - The economic model is a toy: customers and suppliers are simulated by LLMs in the recreations. So "net worth" partly measures exploitation of simulator quirks.
  - Few items: one scenario.
- **Sources.**
  - https://raw.githubusercontent.com/markattarcolgate64/open-vending-bench/main/README.md
  - https://raw.githubusercontent.com/ProsusAI/vending-bench/main/README.md
  - https://raw.githubusercontent.com/aijnek/vending_bench/main/README.md
  - https://github.com/search?q=vending-bench&type=repositories

### 11. TheAgentCompany (CMU and collaborators)

- **What it measures.** Agents acting as "digital workers" in a simulated software company (GitLab, Plane, RocketChat, OwnCloud). They browse, code, run programs and talk to simulated coworkers. Scoring is checkpoint-based: full completion plus partial credit, using deterministic and LLM evaluators. [V]
- **Release.** arXiv:2412.14161 (Dec 2024). Xu, Song, Li, Tang, Jain, Bao, Wang, Zhou, Guo, Cao, Yang, Lu, Martin, Su, Maben, Mehta, Chi, Jang, Xie, Zhou, Neubig. [V] The WebArena-x site lists it as ICML 2025. [V as displayed] [corrected by fact-check] The paper is in the **NeurIPS 2025 Datasets & Benchmarks track (poster)** per the paper-copilot NeurIPS 2025 list, and it does not appear in the ICML 2025 list.
- **Items.** 175 task images covering SDE, PM, data science, HR, finance and admin. [V]
- **Frontier scores** (leaderboard submissions repo, `evaluation/1.0.0`) [V]:

| Date | Entry | Perfect completions | Overall score |
|---|---|---|---|
| 2024-12-17 | OpenHands + Claude 3.5 Sonnet (Oct) | 42/175 (24.0%) | 34.4% |
| 2024-12-17 | OpenHands + GPT-4o | 8.57% | — |
| 2025-05-10 | Gemini 2.5 Pro | 30.29% | — |
| 2025-06-14 | OpenHands-Versa + Claude Sonnet 4 | 33.14% | 43.19% |
| 2025-10-13 | MUSE + Gemini 2.5 Flash | 41.14% | 51.78% |
| 2025-11-10 | TTE-MatrixAgent + DeepSeek-V3.2 | 42.86% | 52.40% |

  - The Claude 3.5 Sonnet launch entry averaged $6.34 per task.
- **Adoption.** [V] Research-agent papers submit to it, and MiniMax-M2 reports an "AgentCompany" column. The leaderboard has 19 submissions and **none after Nov 2025**; there are no 2026 frontier-lab entries in the repo.
- **Status.** Niche or stalling.
- **Why it succeeded.** Rich, realistic workplace simulation; partial-credit checkpoints; open trajectories and screenshots.
- **Why it is failing.** [interpretation + V]
  - Heavy setup: multiple self-hosted services and a 175-image Docker suite.
  - It is dominated by scaffold papers rather than model comparisons.
  - "Self-evolving" agents that accumulate experience across the benchmark's own tasks (MUSE) blur test-time learning with capability. [V: MUSE README]
  - Frontier labs report other suites.
- **Sources.**
  - https://raw.githubusercontent.com/TheAgentCompany/TheAgentCompany/main/README.md
  - https://raw.githubusercontent.com/TheAgentCompany/experiments/main/README.md
  - https://github.com/TheAgentCompany/experiments/tree/main/evaluation/1.0.0
  - https://raw.githubusercontent.com/TheAgentCompany/experiments/main/evaluation/1.0.0/20241217_OpenHands-0.14.2-sonnet-20241022/README.md
  - https://raw.githubusercontent.com/TheAgentCompany/experiments/main/evaluation/1.0.0/20251110_TTE-MatrixAgent-Deepseek-V3.2/README.md

### 12. Remote Labor Index (CAIS and Scale AI)

- **What it measures.** Whether AI agents can complete real, paid remote-freelance projects end-to-end. AI deliverables are compared by human evaluators against the professional human deliverable for the same brief. [V: platform README] Examples include 3D/CAD files (.dwg, .fbx, .3dm, .step), which is why an Autodesk viewer is integrated. [V]
- **Release.** The public platform repo `centerforaisafety/rli_evaluation_platform` was last updated 2025-11-03 and has 79 stars. [V] Datasets: `cais/rli-public-set` and `cais/rli-example-deliverables` on HF (URLs seen). [V]
- **Items.** The public set has **10 tasks with human deliverables**. [V] Example AI deliverables exist for Grok 4, Manus and Claude Sonnet 4.5. [V] Total project count, dollar value and headline automation rate (e.g. "best agent ~2.5%") are **[U]**.
- **Status.** Active and niche. It is new, and human evaluation limits cadence.
- **Why it matters.** [interpretation] It is the most economically literal unit: the share of real paid projects automated at client-acceptable quality. The file formats are very diverse, which resists narrow tuning.
- **Why it may fail.** [interpretation] Human qualitative evaluation is costly and slow. The public set is tiny (10), so external replication is limited. Results sit at the floor, which gives low resolution between models until capabilities catch up.
- **Source.** https://raw.githubusercontent.com/centerforaisafety/rli_evaluation_platform/main/README.md

### 13. MLE-bench (OpenAI)

- **What it measures.** ML-engineering agents on 75 Kaggle competitions, scored by medal thresholds against the historical human leaderboards. The metric is any-medal %. There are Low/Medium/High complexity splits, and the "Lite" split is the 22 Low-complexity competitions (3.3 TB → 158 GB). [V]
- **Release.** arXiv:2410.07095 (Oct 2024). Chan, Chowdhury, Jaffe, Aung, Sherburn, Mays, Starace, Liu, Maksin, Patwardhan, Weng, Mądry. [V] Venue: ICLR 2025 (Oral), per paper-copilot. Note that the arXiv abstract reports o1-preview + AIDE at 16.9% of competitions, while the README leaderboard shows 17.12 ± 0.61. [corrected by fact-check]
- **Frontier scores** (any medal %, All split). [V]
  - Launch (2024-10-08): AIDE + o1-preview 17.12 ± 0.61; AIDE + GPT-4o 8.63.
  - Latest main board: Famou-Agent 2.0 + Gemini-3-Pro 64.44 ± 1.18 (2026-02-23); AIBuildAI + Claude-Opus-4.6 63.11 (2026-03-06).
  - Non-comparable "test-set feedback" entry: Disarray ensemble 77.78.
- **Adoption.** [V] A large, fast-moving third-party leaderboard (Google CAIR, Microsoft R&D-Agent, Meta AIRA-dojo, Baidu, DeepSeek-based agents). ABC overall score 94.1, the highest of the ten audited.
- **Status.** Active, with the leaderboard **frozen**: "Update (04-24-2026): We are currently not taking any new submissions … while we develop an improved process for ensuring submissions are fair and comparable." [V]
- **Why it succeeded.** Human-referenced medal thresholds give an externally anchored, interpretable score. It requires ≥ 3 seeds with SEM, and has open grading reports.
- **Why it is failing.** [V]
  - (a) **Known task bugs deliberately left unfixed** "to avoid invalidating the leaderboard", pending a v2 in openai/frontier-evals.
  - (b) **Submission gaming or test-set feedback.** A separate table was needed for entries that used test-set feedback.
  - (c) Very expensive: 24 h per run on 36 vCPUs, 440 GB RAM and an A10 GPU, with ≥ 3 seeds.
  - (d) Kaggle leaderboards are public, so there is a contamination risk. A "familiarity" experiment is included.
- **Source.** https://raw.githubusercontent.com/openai/mle-bench/main/README.md

### 14. PaperBench (OpenAI)

- **What it measures.** End-to-end replication of 20 ICML 2024 Spotlight and Oral papers from scratch. The agent writes code, the code is executed in a reproduction container, and an LLM judge grades it against paper-specific hierarchical rubrics. [corrected by fact-check] The README makes gpt-4.1-mini the default model of the *BasicAgent solver*, and it appears as the judge model in a cheap dev-config example. The README does not name it as the default judge; it refers to an "o3-mini SimpleJudge". There is also a "Code-Dev" variant that skips execution and costs about 85% less. [V]
- **Release.** arXiv:2504.01848 (Apr 2025). The repo moved from openai/preparedness to openai/frontier-evals. [V] [corrected by fact-check] The paper is "PaperBench: Evaluating AI's Ability to Replicate AI Research" by Starace, Jaffe, Sherburn, Aung, Chan, Maksin, Dias, Mays, Kinsella, Thompson, Heidecke, Glaese and Patwardhan (README BibTeX and arXiv listing). It appeared at ICML 2025 as a poster, per paper-copilot.
- **Frontier scores.** [V] All leaderboard rows are dated 2025-04-02:
  - IterativeAgent o1-high (36 h): 26.0 ± 0.3%.
  - BasicAgent Claude 3.5 Sonnet: 21.0%.
  - Code-Dev best: 43.4%.
- **Adoption.** Lab usage was not verified this session. **[U]**
- **Status.** Niche: the public leaderboard has not been updated since Apr 2025. [V]
- **Why it succeeded.** An ambitious, research-relevant construct (AI R&D automation). Rubrics decompose credit into 8,316 individually gradable tasks (arXiv abstract). [corrected by fact-check] (was [U])
- **Why it is failing.** [interpretation + V] Very expensive (GPU reproduction, 12-36 h runs). The grade depends on an LLM judge. There are only 20 papers, and the repo needs OpenAI and HF API keys for some papers.
- **Sources.**
  - https://raw.githubusercontent.com/openai/preparedness/main/project/paperbench/README.md
  - https://raw.githubusercontent.com/openai/frontier-evals/main/README.md

### 15. Cybench (Stanford)

- **What it measures.** Offensive cybersecurity. There are 40 professional CTF tasks from 4 competitions: crypto 16, web 8, rev 6, forensics 4, misc 4, pwn 2. There are unguided and subtask-guided modes. Difficulty is indexed by **First Solve Time (FST)**, the time the first human team took to solve the task in the competition. [V]
- **Release.** arXiv:2408.08926 (Aug 2024), ICLR 2025. Zhang, Perry, Dulepet, Ji, Menders, Lin, Jones, Hussein, Liu, Jasper, Peetathawatchai, Glenn, Sivashankar, Zamoshchin, Glikbarg, Askaryar, Yang, Zhang, Alluri, Tran, Sangpisit, Oseleononmen, Boneh, Ho, Liang. [V] [corrected by fact-check] This is the 25-author ICLR 2025 BibTeX from the site; the paper was an Oral per paper-copilot. The latest arXiv version lists 27 authors (adding Yiorkadjis and Raghupathi, with some names spelled differently). State which version you cite.
- **Frontier scores** (official leaderboard.csv, unguided % solved). [V]
  - Launch: Claude 3.5 Sonnet 17.5%, GPT-4o 12.5%, o1-preview 10%. The launch hardest task solved had FST 0:11.
  - Later:
    - Claude Opus 4.5: 82% (39-task subset).
    - Claude Opus 4.6: 93% (37-task subset).
    - Claude Opus 4.7: 96% (35).
    - **Claude Mythos Preview: 100% (35-task subset)**.
    - Muse Spark (Meta): 65.4% (40).
    - Grok 4: 43% (40).
- **Adoption.** Exceptional; all [V], from the site's Impact section.
  - US and UK AISI joint pre-deployment tests of Claude 3.5 Sonnet and o1, where it was "the only open source cybersecurity benchmark".
  - UK AISI Inspect Evals.
  - Anthropic system cards from Claude 3.7 Sonnet through Opus 4.7 and Mythos Preview.
  - Amazon Nova Premier, xAI Grok 4 / 4 Fast / 4.1, Meta Muse Spark.
  - Japan and Korea AISIs; first prize in CAIS SafeBench.
- **Status.** **Saturated** at the frontier. It remains adopted for trend continuity.
- **Why it succeeded.** Fresh, professional CTFs with objective flag checks. The human-time difficulty anchor (FST) and subtask partial credit add to that. It was open-sourced with a careful ethics statement, and it fitted safety frameworks' dual-use eval needs.
- **Why it is failing.** [V]
  - (a) **Saturation** within about 20 months.
  - (b) **Subset reporting.** Labs drop 1-5 of 40 tasks (35/37/39 subsets), which limits comparability.
  - (c) **Harness leakage.** The HAL runs of o3-mini and o1-mini "likely ran on a fork of the Inspect framework that leaked the answer to a task". The scores were adjusted down by 2.5 points.
  - (d) Only 40 items, so resolution is coarse: one task is 2.5 points.
- **Sources.**
  - https://raw.githubusercontent.com/andyzorigin/cybench/main/README.md
  - https://raw.githubusercontent.com/cybench/cybench.github.io/main/index.html
  - https://raw.githubusercontent.com/cybench/cybench.github.io/main/data/leaderboard.csv

### 16. Meta-evaluation infrastructure (context for all of the above)

- **ABC: Agentic Benchmark Checklist.** "Establishing Best Practices for Rigorous Agentic Benchmarks" (project-page title). [corrected by fact-check] The arXiv paper is arXiv:2507.02825, "Establishing Best Practices for **Building** Rigorous Agentic Benchmarks" (v1 2025-07-03). It was accepted to the NeurIPS 2025 Datasets & Benchmarks track, where it is titled "…in Building Rigorous Agentic Benchmarks". Zhu, Jin, Pruksachatkun, Zhang, Liu, Cui, Kapoor, Longpre, Meng, Weiss, Barez, Gupta, Dhamala, Merizian, Giulianelli, Coppock, Ududec, Kellermann, Sekhon, Steinhardt, Schwettmann, Zaharia, Stoica, Liang, Kang. [V: project page] (Arxiv ID now captured; see above.)
  - It separates **task validity** (solvable iff the agent has the capability) from **outcome validity** (the check indicates success correctly), plus reporting.
  - Overall scores: MLE-Bench 94.1, CyBench 89.7, GAIA 71.3, τ-Bench 65.4, OSWorld 64.3, SWE-Lancer 61.3, SWE-bench-Verified 60.3, Bird-Bench 52.1, WebArena 45.4, KernelBench 44.6.
  - Claim: flaws cause "misrepresentation in performance of up to 40%". [V: project page] [corrected by fact-check] The arXiv abstract says "up to 100% in relative terms", and that applying ABC to CVE-Bench reduces overestimation by 33%.
- **HAL: Holistic Agent Leaderboard.** Stroebl, Kapoor, Narayanan, ICLR 2026. [V: README BibTeX] [corrected by fact-check] The accepted ICLR 2026 paper is "Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation", arXiv:2510.11977, by Kapoor, Stroebl, … Liang, Narayanan (31 authors; paper-copilot ICLR 2026 list and cached arXiv page). It reports 21,730 rollouts across 9 models and 9 benchmarks at about $40k. Cite that paper, not the README BibTeX. It offered cost-aware, standardised third-party evaluation across τ-bench, AssistantBench, CORE-Bench, SciCode and others, motivated by "AI Agents That Matter" (arXiv:2407.01502): "What does it mean if an agent has 1% higher accuracy … but is 10x more expensive?" [V] It is now **archived**: "HAL leaderboard results are no longer being updated … focusing our current work on agent reliability". [V]
- **Cost as an adoption barrier.** Kimi K2's README says "Some data points have been omitted due to prohibitively expensive evaluation costs." [V]

---

## Cross-cutting success factors

1. **An interpretable, externally anchored unit of measurement.** The benchmarks that support longitudinal narratives express scores in units outsiders understand:
   - METR: human expert minutes.
   - GDPval: win-rate against a 14-year-experienced professional.
   - MLE-bench: Kaggle medal thresholds.
   - Cybench: first-solve time of human CTF teams.
   - OSWorld: a 72.36% human success reference.
   - τ-bench: pass^k reliability.

   These units survive task-suite churn. METR stitched TH1.0 and TH1.1 onto one curve spanning 2019-2026. [V/R]
2. **Human calibration built into the item.** Items carry a human time or human baseline (METR, RE-Bench, Cybench FST, OSWorld), and that is what makes "superhuman" or "at parity" claims possible. [V]
3. **Long dynamic range and an extensible ceiling.** METR's log-time scale spans roughly 4,600× from GPT-2 to Claude Opus 4.5 on TH1.0. [R] GDPval win-rate and Vending-Bench net worth have no hard 100% ceiling. Pass/fail suites with 40-400 items saturate much faster (Cybench, OSWorld).
4. **Maintenance as a first-class product.**
   - Versioned releases with explicit non-comparability notices: τ³ v1.0.1, OSWorld-Verified and 2.x manifests, MLE-bench v2 plan.
   - Maintainer-run verified leaderboards: OSWorld and TheAgentCompany "verified" checkmark.
   - Public trajectories: TAC, VWA, OSWorld 2.0.

   These keep benchmarks credible after bugs surface. [V]
5. **Lab and government adoption loop.** Inclusion in UK AISI Inspect Evals, AISI pre-deployment tests and lab system cards (Cybench, GAIA, τ², BrowseComp) creates a self-reinforcing standard. [V]
6. **Cheap, deterministic scoring where possible.** Examples: BrowseComp's hard-to-find/easy-to-verify answers, exact-match GAIA answers, CTF flags, and DB-state checks in τ. WebArena-Verified explicitly *removed* LLM judges for deterministic comparison. [V]
7. **Contamination hygiene suited to agents.** Examples: encrypted datasets with canaries (BrowseComp), password-protected solutions (METR/RE-Bench), gated task code so agents cannot look answers up *during* execution (OSWorld 2.0), and encrypted trace uploads (HAL). [V]
8. **Reliability metrics.** pass^k (τ) and p80 vs p50 (METR) expose the deployment-relevant gap between "can sometimes" and "reliably does". [V]

## Cross-cutting failure factors

1. **Outcome-validity bugs.** Do-nothing and spam agents score 38-40% on τ-bench and 4.4% on WebArena. Correct solutions fail on OSWorld when the live site changes. Gold labels are wrong in 27 of 50 τ airline tasks. [V] ABC puts benchmark misrepresentation at up to 40%. [V]
2. **Live-environment rot and non-stationarity.** Live websites (OSWorld Chrome tasks, BrowseComp, GAIA's web dependence), bot defences and OAuth make scores drift over time and across networks. Successors freeze the environment: mocked websites (OSWorld 2.0), fixed corpora (BrowseComp-Plus), network-trace replay (WebArena-Verified). [V]
3. **Harness, step-budget and test-time-compute confounds.** The same model gains about 20 points from 15 to 100 steps on OSWorld-Verified. Best-of-N entries sit next to single-rollout entries. Per-benchmark agent configs are required to reproduce results (MiroThinker). Leaderboards are frozen or archived over comparability concerns (MLE-bench Apr 2026, HAL). [V]
4. **Fragmentation into subsets and private variants.** Examples: GAIA-Text-103 vs Val-165 vs hidden test, Cybench on 35/37/39 of 40 tasks, WebArena-Verified's 258-task Hard subset, GDPval gold subset vs full set. Each produces non-comparable numbers under the same name. [V]
5. **Grader drift and substitution.** LLM judges replace experts (GDPval-AA uses Gemini 3 Pro; OpenReward uses gpt-5-mini) or grade rubrics (PaperBench uses an LLM judge; the README mentions an o3-mini SimpleJudge [corrected by fact-check]). The construct changes silently. [V]
6. **Fast saturation of fixed item pools.** Pools of 40 to a few hundred tasks saturate in about 1-2 years: OSWorld passed its human baseline about 20 months after launch; Cybench reached 100% on a subset. [V/R] Without an extensible difficulty axis, the benchmark has to be replaced (OSWorld 2.0, τ³), which breaks the time series.
7. **Cost and setup burden.** Examples: MLE-bench at 24 h × 3 seeds on GPU boxes, PaperBench at 12-36 h plus GPU reproduction, TheAgentCompany and WebArena's multi-service Docker stacks, METR human baselining at about $22.8k for the TH1.1 baselined tasks. Kimi K2 omitted results due to "prohibitively expensive evaluation costs". High cost cuts the number of independent replications. [V/R]
8. **Human-reference quality at the frontier.** The measurement is only as good as its human anchor. METR's longest tasks mostly carry *estimated*, round-number times (26/31 ≥ 8 h). [R] The OSWorld human baseline (72.36%) is below today's agents, so it no longer anchors anything.
9. **Closed environments.** Vending-Bench is not openly released, and RLI's public set has 10 items. Third parties rebuild approximations, which multiplies incompatible versions. [V/S]
10. **Test-time learning on the test set.** Agents that accumulate memory across benchmark tasks (MUSE on TAC) or use test-set feedback (MLE-bench side table) measure adaptation to the benchmark rather than capability. [V]

### Design implications for our non-game benchmark (interpretation, for Phase 2)

- **Borrow METR's unit, fix its tail.** Express scores in a human-anchored, log-scaled unit such as expert minutes or dollars, with IRT or logistic fits. Invest in **measured** (not estimated) human times for the longest items, because the long tail is where frontier comparisons now happen.
- **Report reliability, not just capability.** Report pass^k or p80 next to p50.
- **Build validity into the pipeline.** Ship an **oracle solver and a do-nothing / spam-agent baseline** with every release (ABC T.9, R.13). Use deterministic, state-based checks. Freeze or mock all external resources.
- **Standardise the harness and cost budget.** Report score as a function of step/token/$ budget (a cost-performance curve) rather than one number. This absorbs the harness confound instead of hiding it.
- **Version everything.** Use manifests like OSWorld 2.x and explicit comparability rules like τ³ v1.0.1. Plan item refresh (procedural or held-out generation) so the difficulty ceiling can rise without breaking the unit.
- **Aim for about $1-10 per model per item, and fewer than a few hundred items per full run.** That keeps independent replication feasible, which HAL, MLE-bench and PaperBench show is otherwise the first thing to go.

---

## Claims ledger

1. METR's official analysis repo states: "AI agent time horizons have been doubling approximately every 7 months". The method fits a logistic P(success) against log2(human minutes) and reports the task length at 50% predicted success. — https://raw.githubusercontent.com/METR/eval-analysis-public/main/README.md — **High**
2. METR released "Time Horizon 1.1" (updated task suite) in a commit dated 21 Jan 2026. The TH1.1 public data has 228 tasks (HCAST 157, SWAA 66, RE-Bench 5) in 79 families, with 20 models from GPT-4 0314 to Claude Opus 4.6 and GPT-5.3-Codex. — https://github.com/METR/eval-analysis-public/commits/main ; https://raw.githubusercontent.com/METR/eval-analysis-public/main/reports/time-horizon-1-1/data/raw/runs.jsonl ; https://raw.githubusercontent.com/METR/eval-analysis-public/main/reports/time-horizon-1-1/params.yaml — **High** (commit date via GitHub page summary: Medium-High)
3. [R] Re-fitting METR's public TH1.0 data with METR's own settings (invsqrt weights, reg 1e-5) gives a SOTA doubling time of 7.1 months for 2019 (GPT-2) to Feb 2025 (Claude 3.7 Sonnet), and 4.6 months for 2024+. TH1.1 gives 3.4 months for 2024+. — runs.jsonl (TH1.0/TH1.1) + https://raw.githubusercontent.com/METR/eval-analysis-public/main/reports/time-horizon-1-1/fig_params/figs.yaml — **Medium-High** (own computation; verify against METR's published values)
4. [R] In TH1.1, Claude Opus 4.6 has an estimated p50 horizon of ≈719 min (~12 h), bootstrap 95% CI ≈309-3,037 min ([corrected by fact-check]: METR's own CI is 5-66 h), while p80 is ≈70 min. 26 of the 31 tasks with human time ≥ 480 min use estimated rather than baselined human times, and 12 of them are exactly 480 min. — https://raw.githubusercontent.com/METR/eval-analysis-public/main/reports/time-horizon-1-1/data/raw/runs.jsonl — **Medium-High**
5. OSWorld launched with 369 tasks. "While humans can accomplish over 72.36% of the tasks, the best model achieves only 12.24% success." — https://raw.githubusercontent.com/os-world/os-world.github.io/main/index.html ; BibTeX arXiv:2404.07972 at https://raw.githubusercontent.com/xlang-ai/OSWorld/main/README.md — **High**
6. On the official OSWorld-Verified leaderboard, the best entry passed the 72.36% human figure on 2025-12-11 (Agent S3 w/ Opus 4.5 + GPT-5 bBoN N=10, 72.58%; the first single-rollout entry above it was 74.48% on 2026-02-25 [corrected by fact-check]) and reached 90.19% on 2026-07-25 (Intelligence-Indeed Agent). OSWorld 2.0 (arXiv:2606.29537) was released 2026-06-26. — https://raw.githubusercontent.com/os-world/os-world.github.io/main/static/data/osworld_verified_results.xlsx ; https://raw.githubusercontent.com/xlang-ai/OSWorld-V2/main/README.md — **High**
7. On OSWorld-Verified the step budget strongly changes scores: Claude Sonnet 4.5 scores 42.88% / 58.08% / 62.88% at 15 / 50 / 100 steps, and o3 scores 9.1% / 17.17% / 23.0%. — osworld_verified_results.xlsx (URL above) — **High**
8. ABC audit: on τ-bench a trivial do-nothing agent scores 38%, because 38% of airline tasks are intentionally unsolvable and pass when the DB is unchanged, and a DB-dumping agent scores 40%. On WebArena a do-nothing agent passes 4.4%. On OSWorld, 13 of 46 Chrome tasks were broken by website changes. ABC states flaws cause misrepresentation "up to 40%". — https://raw.githubusercontent.com/uiuc-kang-lab/agentic-benchmarks/main/README.md ; https://raw.githubusercontent.com/uiuc-kang-lab/agentic-benchmarks/main/benchmarks/tau-bench/README.md ; https://raw.githubusercontent.com/uiuc-kang-lab/agentic-benchmarks/main/assessments/webarena.yaml ; https://raw.githubusercontent.com/uiuc-kang-lab/agentic-benchmarks/main/benchmarks/osworld/README.md ; https://raw.githubusercontent.com/uiuc-kang-lab/agentic-benchmarks/gh-pages/index.html — **High**
9. τ³-bench shipped "75+ task fixes" (27 airline tasks and 26 retail tasks; the airline domain has 50 tasks). The v1.0.1 grading fix (2026-07-15) raised banking_knowledge pass^1 by up to ~9 points (e.g. GPT-5.5 xhigh 37.37 → 46.39) and declared pre- and post-1.0.1 **banking_knowledge** results non-comparable [corrected by fact-check: the scope is banking_knowledge only]. — https://raw.githubusercontent.com/sierra-research/tau2-bench/main/CHANGELOG.md ; https://raw.githubusercontent.com/sierra-research/tau2-bench/main/README.md ; https://raw.githubusercontent.com/sierra-research/tau2-bench/main/data/tau2/domains/airline/tasks.json — **High**
10. MLE-bench (75 Kaggle competitions) went from 17.12% any-medal (AIDE + o1-preview, 2024-10-08) to 64.44% (Famou-Agent 2.0 + Gemini-3-Pro, 2026-02-23). On 2026-04-24 it stopped accepting submissions "while we develop an improved process for ensuring submissions are fair and comparable". — https://raw.githubusercontent.com/openai/mle-bench/main/README.md — **High**
11. Cybench (40 CTF tasks) had a launch best unguided solve rate of 17.5% (Claude 3.5 Sonnet). Lab-reported scores later reached 93% (Claude Opus 4.6, 37-task subset) and 100% (Claude Mythos Preview, 35-task subset). It was used by US and UK AISI in pre-deployment tests and in Anthropic, xAI, Amazon and Meta model cards. — https://raw.githubusercontent.com/cybench/cybench.github.io/main/data/leaderboard.csv ; https://raw.githubusercontent.com/cybench/cybench.github.io/main/index.html — **High** (as reported by the benchmark site)
12. TheAgentCompany (175 tasks) went from 24.0% full completion / 34.4% score (OpenHands + Claude 3.5 Sonnet, Dec 2024) to 42.86% / 52.40% (TTE-MatrixAgent + DeepSeek-V3.2, Nov 2025). There are no leaderboard submissions after Nov 2025. — https://raw.githubusercontent.com/TheAgentCompany/experiments/main/evaluation/1.0.0/20241217_OpenHands-0.14.2-sonnet-20241022/README.md ; https://raw.githubusercontent.com/TheAgentCompany/experiments/main/evaluation/1.0.0/20251110_TTE-MatrixAgent-Deepseek-V3.2/README.md ; https://github.com/TheAgentCompany/experiments/tree/main/evaluation/1.0.0 — **High**
13. GDPval (arXiv:2510.04374) covers 44 occupations in 9 sectors, with a 220-task public gold subset. Reported expert win-rates (wins + ties): Claude Opus 4.1 47.6% and GPT-5 high 38.8% (paper Fig. 5; [corrected by fact-check]: 39.0% is from the paper's Table 2), and GPT-5.2 Thinking 70.9% later (wins or ties, secondary). Artificial Analysis' GDPval-AA replaces expert graders with Gemini 3 Pro pairwise grading and Bradley-Terry Elo. — https://raw.githubusercontent.com/EnvCommons/GDPVal/main/README.md ; https://raw.githubusercontent.com/amaarora/GDPVal/main/README.md ; https://raw.githubusercontent.com/botschen/GDPVal_Eval/main/README.md ; https://raw.githubusercontent.com/hyeonsangjeon/gdpval-realworks/main/README.md — **Medium** (secondary; check the paper for the wins vs. wins+ties definition)
14. BrowseComp-Plus (arXiv:2508.06600) was created because live-web evaluation of BrowseComp hinders "fair, transparent, and reproducible comparisons". It uses 830 BrowseComp queries against a fixed ~100K-document corpus. — https://raw.githubusercontent.com/texttron/BrowseComp-Plus/main/README.md — **High**
15. Open-weight labs report GAIA on a 103-question text-only subset of the 165-question validation split, using an LLM-judge template rather than the official scorer ([corrected by fact-check]: the LLM-judge template is stated only by MiroThinker; MiniMax states only the subset). The GAIA test split has no public answers. — https://raw.githubusercontent.com/MiniMax-AI/MiniMax-M2/main/README.md ; https://raw.githubusercontent.com/MiroMindAI/MiroThinker/main/README.md ; https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_evals/main/src/inspect_evals/gaia/README.md — **High**
16. HAL (ICLR 2026 paper: Kapoor, Stroebl, … Narayanan, arXiv:2510.11977 [corrected by fact-check]) archived its harness and stopped leaderboard updates to focus on agent reliability. — https://raw.githubusercontent.com/princeton-pli/hal-harness/main/README.md — **High**

**Unverified items to check before citing (not seen this session):**

- ~~GAIA: human 92% vs GPT-4-with-plugins 15%, and 466 total questions.~~ Resolved by fact-check: confirmed in the arXiv v1 abstract.
- WebArena: human 78.24% vs GPT-4 14.41% is still unverified; the v1 abstract says 10.59%. The venue is resolved as ICLR 2024 (fact-check).
- ~~BrowseComp: 1,266 problems.~~ Resolved by fact-check: confirmed in the arXiv abstract.
- RLI: headline automation rate (~2.5%), project count and dollar value.
- Vending-Bench 2 leaderboard values are still unverified. The authors are resolved as Backlund and Petersson (fact-check).
- RE-Bench: "agents beat experts at 2 h but not at 8 h".
- ~~PaperBench: rubric leaf count.~~ Resolved by fact-check: 8,316.
- METR: model-card citations of the time-horizon metric; METR's own published p50 values for Opus 4.5/4.6.
- ~~GDPval: author list.~~ Resolved by fact-check: Patwardhan et al., 19 authors.
- ~~ABC: arXiv ID.~~ Resolved by fact-check: arXiv:2507.02825.

## References

1. Kwa, T., West, B., Becker, J., et al. (METR). *Measuring AI Ability to Complete Long Tasks.* arXiv:2503.14499, 2025. [corrected by fact-check] https://arxiv.org/abs/2503.14499 (seen via https://raw.githubusercontent.com/METR/eval-analysis-public/main/README.md)
2. METR. *eval-analysis-public* (time-horizon code and data; TH1.0, TH1.1). GitHub, 2025-2026. https://github.com/METR/eval-analysis-public
3. METR. *HCAST: Human-Calibrated Autonomy Software Tasks.* GitHub, 2025. https://github.com/METR/hcast-public
4. Wijk, H., Lin, T., Becker, J., Jawhar, S., Parikh, N., et al. *RE-Bench: Evaluating frontier AI R&D capabilities of language model agents against human experts.* ICML 2025 (Spotlight); arXiv:2411.15114, 2024. [corrected by fact-check] https://arxiv.org/abs/2411.15114
5. METR. *METR Task Standard.* GitHub. https://github.com/METR/task-standard
6. Patwardhan, T., Dias, R., Proehl, E., et al. *GDPval: Evaluating AI Model Performance on Real-World Economically Valuable Tasks.* ICLR 2026; arXiv:2510.04374, 2025. https://arxiv.org/abs/2510.04374 [corrected by fact-check]
7. Artificial Analysis. *GDPVal-AA evaluation framework* (reproduction by botschen). GitHub. https://github.com/botschen/GDPVal_Eval
8. Xie, T., Zhang, D., Chen, J., et al. *OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments.* NeurIPS 2024 Datasets & Benchmarks, arXiv:2404.07972. https://arxiv.org/abs/2404.07972
9. XLANG Lab. *OSWorld-Verified leaderboard data* (osworld_verified_results.xlsx). 2025-2026. https://github.com/os-world/os-world.github.io
10. Yuan, M., Zhou, Z., Xiong, X., et al. *OSWorld 2.0: Benchmarking Computer Use Agents on Long-Horizon Real-World Tasks.* arXiv:2606.29537, 2026. https://arxiv.org/abs/2606.29537
11. Yao, S., Shinn, N., Razavi, P., Narasimhan, K. *τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains.* arXiv:2406.12045, 2024. https://arxiv.org/abs/2406.12045
12. Barres, V., Dong, H., Ray, S., Si, X., Narasimhan, K. *τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment.* arXiv:2506.07982, 2025. https://arxiv.org/abs/2506.07982
13. Sierra Research. *tau2-bench CHANGELOG* (τ³-bench v1.0.0, v1.0.1). GitHub, 2026. https://github.com/sierra-research/tau2-bench/blob/main/CHANGELOG.md
14. Cuadron, A., Yu, P., Liu, Y., Gupta, A. *SABER: Small Actions, Big Errors — Safeguarding Mutating Steps in LLM Agents.* ICLR 2026 Workshop; arXiv:2512.07850. https://arxiv.org/abs/2512.07850
15. Shi, Q., Zytek, A., Razavi, P., Narasimhan, K., Barres, V. *τ-Knowledge: Evaluating Conversational Agents over Unstructured Knowledge.* arXiv:2603.04370, 2026.
16. Ray, S., Dhandhania, K., Barres, V., Narasimhan, K. *τ-Voice: Benchmarking Full-Duplex Voice Agents on Real-World Domains.* arXiv:2603.13686, 2026.
17. Mialon, G., Fourrier, C., Swift, C., Wolf, T., LeCun, Y., Scialom, T. *GAIA: A Benchmark for General AI Assistants.* ICLR 2024; arXiv:2311.12983, 2023. https://arxiv.org/abs/2311.12983 [corrected by fact-check]
18. UK AISI. *inspect_evals: GAIA implementation.* GitHub. https://github.com/UKGovernmentBEIS/inspect_evals/tree/main/src/inspect_evals/gaia
19. Zhou, S., Xu, F. F., Zhu, H., et al. *WebArena: A Realistic Web Environment for Building Autonomous Agents.* ICLR 2024; arXiv:2307.13854, 2023. [corrected by fact-check] https://arxiv.org/abs/2307.13854
20. El hattami, A., Thakkar, M., Chapados, N., Pal, C. *WebArena Verified: Reliable Evaluation for Web Agents.* Workshop on Scaling Environments for Agents (NeurIPS 2025). https://openreview.net/forum?id=94tlGxmqkN
21. Koh, J. Y., Lo, R., Jang, L., et al. *VisualWebArena: Evaluating Multimodal Agents on Realistic Visual Web Tasks.* ACL 2024; arXiv:2401.13649, 2024. https://arxiv.org/abs/2401.13649
22. Wei, J., Sun, Z., Papay, S., McKinney, S., Han, J., Fulford, I., Chung, H. W., Passos, A. T., Fedus, W., Glaese, A. [corrected by fact-check] *BrowseComp: A Simple Yet Challenging Benchmark for Browsing Agents.* arXiv:2504.12516, 2025. https://openai.com/index/browsecomp/
23. Chen, Z., Ma, X., Zhuang, S., et al. *BrowseComp-Plus: A More Fair and Transparent Evaluation Benchmark of Deep-Research Agent.* arXiv:2508.06600, 2025.
24. OpenAI. *simple-evals README* (deprecation notice, Jul 2025). https://github.com/openai/simple-evals
25. Backlund, A., Petersson, L. (Andon Labs). *Vending-Bench: A Benchmark for Long-Term Coherence of Autonomous Agents.* arXiv:2502.15840, 2025. [corrected by fact-check] https://arxiv.org/abs/2502.15840
26. ProsusAI. *vending-bench (open-source long-horizon business simulation).* GitHub. https://github.com/ProsusAI/vending-bench
27. Xu, F. F., Song, Y., Li, B., et al. *TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks.* NeurIPS 2025 Datasets & Benchmarks; arXiv:2412.14161, 2024. [corrected by fact-check] https://arxiv.org/abs/2412.14161
28. TheAgentCompany. *experiments (leaderboard submissions, evaluation 1.0.0).* GitHub. https://github.com/TheAgentCompany/experiments
29. Center for AI Safety. *RLI Evaluation Platform (Remote Labor Index).* GitHub, 2025. https://github.com/centerforaisafety/rli_evaluation_platform
30. Chan, J. S., Chowdhury, N., Jaffe, O., et al. *MLE-bench: Evaluating Machine Learning Agents on Machine Learning Engineering.* ICLR 2025; arXiv:2410.07095, 2024. https://github.com/openai/mle-bench
31. Starace, G., Jaffe, O., Sherburn, D., et al. *PaperBench: Evaluating AI's Ability to Replicate AI Research.* ICML 2025; arXiv:2504.01848, 2025. [corrected by fact-check] https://github.com/openai/frontier-evals/tree/main/project/paperbench
32. Zhang, A. K., Perry, N., Dulepet, R., et al. *Cybench: A Framework for Evaluating Cybersecurity Capabilities and Risks of Language Models.* ICLR 2025, arXiv:2408.08926. https://cybench.github.io
33. Cybench team. *Cybench leaderboard data* (leaderboard.csv). https://github.com/cybench/cybench.github.io
34. Zhu, Y., Jin, T., Pruksachatkun, Y., et al. *Establishing Best Practices for Building Rigorous Agentic Benchmarks* (Agentic Benchmark Checklist). NeurIPS 2025 Datasets & Benchmarks; arXiv:2507.02825, 2025. https://arxiv.org/abs/2507.02825 ; project page https://uiuc-kang-lab.github.io/agentic-benchmarks/ [corrected by fact-check]
35. Kapoor, S., Stroebl, B., Kirgis, P., et al. *Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation.* ICLR 2026; arXiv:2510.11977, 2025. Harness: https://github.com/princeton-pli/hal-harness [corrected by fact-check]
36. Kapoor, S., Stroebl, B., Siegel, Z. S., Nadgir, N., Narayanan, A. *AI Agents That Matter.* arXiv:2407.01502, 2024. [corrected by fact-check]
37. MiniMax. *MiniMax-M2 README* (benchmark table incl. τ², BrowseComp, GAIA-text, AgentCompany). GitHub, 2025. https://github.com/MiniMax-AI/MiniMax-M2
38. MiroMind. *MiroThinker README* (BrowseComp/GAIA results and harness configs). GitHub, 2025-2026. https://github.com/MiroMindAI/MiroThinker
39. Moonshot AI. *Kimi-K2 README* (Tau2 Avg@4; cost omission note). GitHub, 2025. https://github.com/MoonshotAI/Kimi-K2
40. Hugging Face. *Open Deep Research README* (GAIA validation 55% vs 67%). GitHub. https://github.com/huggingface/smolagents/tree/main/examples/open_deep_research

---

## Verification log

**Fact-checker:** adversarial fact-check subagent. **Date:** 2026-09-29.

**Method.**
- The session-wide WebSearch budget was already used up (200/200) when this check started, so **no web searches were run**. Independent verification used primary files fetched directly with curl from raw.githubusercontent.com, plus these other sources:
  - **Independent re-computation** on METR's public raw data. I downloaded `runs.jsonl` for TH1.0 and TH1.1 and wrote my own logistic fit with METR's settings (invsqrt weights, regularization 1e-5) and my own bootstrap.
  - **arXiv metadata and abstracts:**
    - The arXiv daily-listing mirror `https://raw.githubusercontent.com/Luvata/arxive/main/pages/<date>-<cat>.html`.
    - Cached arXiv abs pages in `https://raw.githubusercontent.com/stanford-cs336/lectures/main/var/files/arxiv-<md5(url)>-https_arxiv_org_abs_<id>`, which hold `citation_*` meta tags.
  - **Venue acceptance lists** from paper-copilot: `https://raw.githubusercontent.com/papercopilot/paperlists/main/{iclr/iclr2024,nips/nips2024,nips/nips2025,icml/icml2025,acl/acl2024}.json`, and the LFS files `https://media.githubusercontent.com/media/papercopilot/paperlists/main/iclr/iclr{2025,2026}.json`.
  - **GitHub code search** (GitHub MCP) to find third-party copies of documents that were blocked, such as the parsed GDPval paper in `visual-snow/seshat` and the GPT-5.2 GDPval launch table.
  - **WebFetch of github.com pages** for the METR commits page and the TheAgentCompany submissions directory.
- **Limitations.** arxiv.org, openreview.net, huggingface.co, metr.org, openai.com and os-world.github.io were not reachable directly. Where a claim rests only on the paper-copilot mirror or a third-party parsed copy, that is stated.

### Claim verdicts

| ID | Verdict | Evidence (independent of the dossier's own summary) | Sources |
|---|---|---|---|
| C1 | **Confirmed** | (1) README line "AI agent time horizons have been doubling approximately every 7 months" and the four-step method (logistic P(success) vs log2(human_minutes), threshold horizon) are verbatim in the README. (2) The commits page shows "Time Horizon 1.1 Release (#32)" on **Jan 21, 2026**, followed by syncs on Jan 30, Feb 13 and Mar 6, 2026. (3) The arXiv abstract independently says doubling has been "approximately every seven months since 2019, though the trend may have accelerated in 2024". | https://raw.githubusercontent.com/METR/eval-analysis-public/main/README.md ; https://github.com/METR/eval-analysis-public/commits/main (WebFetch) ; https://raw.githubusercontent.com/Luvata/arxive/main/pages/2025-03-19-cs-ai.html |
| C2 | **Confirmed** (as a reproducible re-analysis, not a METR-published figure) | My own implementation reproduced every number exactly. TH1.0, the paper's 11 SOTA models from 2019 to 2025-02-24: **7.10 months**. TH1.0 running-max SOTA from 2024: **4.62**. TH1.1 running-max SOTA from 2024: **3.44**. TH1.1 from 2025: **3.97**. The fit is OLS of log2(p50) on release date, using release dates from `data/external/release_dates.yaml`. Caveat: METR's own TH1.1 headline trendline is fitted on models released from 2023 on (figs.yaml `after_date: "2023-01-01"`). My recomputation of that variant is ≈4.3 months, which is my number, not METR's. METR's published trend metrics are DVC outputs that are not in git (404), so they could not be compared. | runs.jsonl (TH1.0 and TH1.1); figs.yaml; release_dates.yaml; src/horizon/utils/logistic.py |
| C3 | **Corrected** | Reproduced: Opus 4.6 p50 = 718.8 min, p80 = 69.9 min; 228 tasks; 26 of 31 tasks ≥ 480 min are `estimate`; 12 are exactly 480 min (and 5 are exactly 600). **Correction: the CI.** METR's own figs.yaml title says "Claude Opus 4.6 has a 50%-time-horizon of about 12 hours (**95% CI: 5 hrs to 66 hrs**)". The dossier's 309-3,037 min (~5-51 h) came from a simplified 200-resample bootstrap. My family→task→run bootstrap (300 resamples, mirroring METR's `bootstrap.py` categories "ftr") gave ≈300-4,624 min. The upper bound is unstable, so cite METR's 5-66 h. Minor fixes: the TH1.1 median human time is 12.6 min (not 12.8); "7 of 9 tasks > 12 h" should read "≥ 12 h". | runs.jsonl TH1.1; https://raw.githubusercontent.com/METR/eval-analysis-public/main/reports/time-horizon-1-1/fig_params/figs.yaml ; https://raw.githubusercontent.com/METR/eval-analysis-public/main/src/horizon/wrangle/bootstrap.py |
| C4 | **Confirmed** | index.html: "While humans can accomplish over 72.36% of the tasks, the best model achieves only 12.24% success". 369 tasks (361 with the 8 Google-Drive tasks excluded). README: paper released 2024-04-11. The arXiv listing (2024-04-12) confirms the title and authors. The NeurIPS 2024 (Datasets & Benchmarks, poster) venue is confirmed by paper-copilot. | https://raw.githubusercontent.com/os-world/os-world.github.io/main/index.html ; https://raw.githubusercontent.com/xlang-ai/OSWorld/main/README.md ; Luvata 2024-04-12-cs-ai ; paper-copilot nips2024 |
| C5 | **Confirmed** (with caveats added) | I parsed the xlsx myself: 144 scored entries. Running best: 72.58% on 2025-12-11 and 90.19% (325.59/361) on 2026-07-25; 16 entries are ≥ 72.36%. **Caveat 1:** the 72.58% entry is a best-of-N (bBoN, N=10) multi-rollout run. The first *single-rollout* entry above the human figure is HIPPO Agent w/ Opus 4.5 at 74.48% (266.66/358) on 2026-02-25. Denominators vary across entries (358/359/360/361/369). **Caveat 2:** the README describes the gated HF task classes for **OSWorld 2.1**, and gated assets for the 2026.08.08 release. That the 2026-06-26 2.0 release was gated from day one is not established. The arXiv listing (2026-06-30) confirms OSWorld 2.0: 108 workflows, best 20.6%. | osworld_verified_results.xlsx ; https://raw.githubusercontent.com/xlang-ai/OSWorld-V2/main/README.md ; Luvata 2026-06-30-cs-ai |
| C6 | **Confirmed** | xlsx rows. claude-sonnet-4-5-20250929: 42.88 / 58.08 / 62.88 at 15 / 50 / 100 steps. o3: 9.1 / 17.17 / 23. computer-use-preview: 26 / 31.3 / 31.4; a second 100-step row reads 29.63. | osworld_verified_results.xlsx |
| C7 | **Corrected** | The specific numbers are all verbatim in the ABC repo. τ-bench: do-nothing agent 38% ("38% of the airline partition and 6% of the retail partition" unsolvable by design); spamming agent 40%. WebArena: "A do-nothing agent can pass 4.4% of the tasks". OSWorld: "13 problems" of 46 chrome; UI-TARS 24/46 → 37/46, 42.5% → 46%. **Correction:** "up to 40%" is from the *project page*. The citable arXiv paper (arXiv:2507.02825, abstract) says issues "can lead to under- or overestimation of agents' performance by **up to 100% in relative terms**". The arXiv title is "Establishing Best Practices for *Building* Rigorous Agentic Benchmarks", and the paper is at NeurIPS 2025 Datasets & Benchmarks. The ABC findings target the original τ-bench commit `14bf0ef`, not τ²/τ³. | ABC repo README, tau-bench/README.md, assessments/webarena.yaml, osworld/README.md, gh-pages/index.html ; cached arXiv page https://raw.githubusercontent.com/stanford-cs336/lectures/main/var/files/arxiv-fbb5f80d5da213da2c4e3e7d3c3b4f0e-https_arxiv_org_abs_2507_02825 ; paper-copilot nips2025 |
| C8 | **Corrected** (scope) | README: "75+ task fixes"; CHANGELOG: "Airline task fixes (27 tasks)" and "Retail task fixes (26 tasks)". `tasks.json` has 50 airline, 114 retail and 97 banking_knowledge tasks. [1.0.1] is dated 2026-07-15: up to ~9 points pass^1, GPT-5.5 xhigh 37.37 → 46.39, GPT-5.4 xhigh 30.67 → 39.43. **Correction:** the non-comparability notice applies only to `banking_knowledge` ("Scores produced with tau2-bench < 1.0.1 on `banking_knowledge` must not be compared…"), not to all results. The earlier quote in the dossier was paraphrased inside quotation marks. [1.0.0] carries the placeholder date "2026-MM-DD". | https://raw.githubusercontent.com/sierra-research/tau2-bench/main/CHANGELOG.md ; README.md ; data/tau2/domains/*/tasks.json |
| C9 | **Confirmed** | README table: AIDE + o1-preview 17.12 ± 0.61 (2024-10-08). Main-table maximum is Famou-Agent 2.0 + Gemini-3-Pro-Preview 64.44 ± 1.18 (2026-02-23). "*Update* (04-24-2026): We are currently not taking any new submissions … fair and comparable". Known issues postponed "to avoid invalidating the leaderboard", with batched fixes planned in v2 on openai/frontier-evals. Note: the arXiv abstract gives 16.9% for the same setup. MLE-bench is ICLR 2025 (Oral). | https://raw.githubusercontent.com/openai/mle-bench/main/README.md ; cached arXiv page (2410.07095) ; paper-copilot iclr2025 |
| C10 | **Confirmed** (with caveat) | leaderboard.csv: Claude 3.5 Sonnet 17.5 unguided (40 tasks); Opus 4.6 93 (37); Mythos Preview 100 (35). The Impact section lists US and UK AISI joint pre-deployment tests ("the only open source cybersecurity benchmark"), Anthropic system cards (3.7 Sonnet → Opus 4.7 / Mythos), Amazon Nova Premier, xAI Grok 4 / 4 Fast / 4.1 and Meta Muse Spark. The arXiv abstract confirms 40 CTF tasks from 4 competitions. Caveat: lab rows are "average pass@1" on 35-39-task subsets, so they are not directly comparable to the 40-task launch numbers. | https://raw.githubusercontent.com/cybench/cybench.github.io/main/data/leaderboard.csv ; index.html ; cached arXiv page (2408.08926) |
| C11 | **Confirmed** | Launch README: "Perfect Completions: 42/175 (24.00%)", "Overall Score: 34.40%". TTE-MatrixAgent README: "75/175 (42.86%)", "52.40%". The directory listing shows 19 submissions, the latest `20251110_…`, and nothing after Nov 2025 as of 2026-09-29. The listing is WebFetch-summarised, so confidence is medium-high. | TAC experiments READMEs ; https://github.com/TheAgentCompany/experiments/tree/main/evaluation/1.0.0 |
| C12 | **Corrected** | Primary confirmation from the arXiv abstract: 44 occupations, top 9 sectors, 14 years' average experience, 220-task gold subset. The 1,320-task full set comes from the parsed paper text. **Corrections:** (a) 47.6% for Claude Opus 4.1 is **wins + ties** ("better than (wins) or as good as (ties)"). (b) In the paper's headline Fig. 5, GPT-5 high is **38.8%** (o3 high 34.1, o4-mini high 27.9, GPT-4o 12.4). The 39.0 / 35.2 / 29.1 / 12.5 values come from the paper's Table 2 (speed/cost analysis), which EnvCommons copied. (c) GPT-5.2 Thinking 70.9% is also "wins or ties"; clear wins were 49.8%. This is secondary, from copies of OpenAI's launch table. (d) The GDPval-AA description (Gemini 3 Pro pairwise, Bradley-Terry Elo anchored at GPT-5.1 = 1000) comes from a third-party reproduction repo (botschen), not from Artificial Analysis, so it stays [S]. The GDPval paper is at ICLR 2026 (poster). | cached arXiv page (2510.04374) ; https://raw.githubusercontent.com/visual-snow/seshat/main/parsed/openai/2510_04374.md ; https://raw.githubusercontent.com/punitarani/modelbeats/main/data/results/gdpval.csv (found via code search) ; EnvCommons / amaarora / botschen READMEs ; paper-copilot iclr2026 |
| C13 | **Confirmed** | README: "enable fair, transparent, and reproducible comparisons", "fixed, curated corpus of ~100K human-verified documents", "all 830 queries". The arXiv abstract independently supports the causal framing: live web APIs "hinder fair comparisons and reproducibility of deep research methods". Its ICLR 2026 submission was withdrawn, so it is an arXiv preprint. | https://raw.githubusercontent.com/texttron/BrowseComp-Plus/main/README.md ; Luvata 2025-08-12-cs-cl ; paper-copilot iclr2026 |
| C14 | **Corrected** (attribution) | The MiroThinker README says "we evaluate GAIA-Text-103 using the WebAgents LLM-as-a-Judge template, and report results on GAIA-Val-165 using the official GAIA scorer script". The MiniMax-M2 README says only "We use the 103-sample text-only GAIA validation subset following WebExplorer" and does **not** state an LLM-judge template. So the LLM-judge part is verified for MiroThinker only, and later MiroThinker versions report Val-165 with the official scorer. The Inspect README says the test split "does not come with any solutions". Val-165 = 53 / 86 / 26 by level (AnyEvalOrg). The arXiv v1 abstract confirms 466 questions, answers retained for 300, and 92% human vs 15% GPT-4 with plugins. | MiroThinker, MiniMax-M2, inspect_evals GAIA and AnyEvalOrg READMEs ; Luvata 2023-11-24-cs-ai |

**Tally.** 9 confirmed (C1, C2, C4, C5, C6, C9, C10, C11, C13). 5 corrected (C3, C7, C8, C12, C14). 0 refuted. 0 unverifiable.

### Other corrections made in the body (not among C1-C14)

- **PaperBench judge.** "LLM judge (default GPT-4.1-mini)" was wrong. gpt-4.1-mini is the BasicAgent solver default and appears in a dev-config judge example; the README mentions an o3-mini SimpleJudge. The paper has 8,316 gradable tasks.
- **WebArena.** The venue is ICLR 2024, not the "NeurIPS 2024 · Oral" shown on the WebArena-x site. The v1 abstract reports the best GPT-4 agent at 10.59%. The 14.41% / 78.24% pair is still unverified.
- **TheAgentCompany.** The venue is NeurIPS 2025 Datasets & Benchmarks, not the ICML 2025 shown on the WebArena-x site.
- **HAL.** The accepted ICLR 2026 paper is arXiv:2510.11977, by Kapoor, Stroebl, … Narayanan (31 authors). The README BibTeX's title and 3-author list do not match it.
- **ABC.** arXiv:2507.02825, with the corrected title (see C7).
- **Author names.**
  - BrowseComp's last author is "Amelia Glaese" on arXiv.
  - Vending-Bench is by Backlund and Petersson.
  - GAIA is by Mialon et al.
  - METR's paper is by Kwa, West, et al.
  - PaperBench is by Starace et al.
  - Cybench's author list differs between the ICLR BibTeX (25 authors) and the latest arXiv version (27).
- **Upgraded from [U] to verified.** BrowseComp's 1,266 questions; GAIA's 466 questions and 92% vs 15%; PaperBench's 8,316 gradable tasks; GDPval's 1,320-task full set.
- **Venues added.** RE-Bench: ICML 2025 Spotlight. MLE-bench: ICLR 2025 Oral. Cybench: ICLR 2025 Oral. PaperBench: ICML 2025. VisualWebArena: ACL 2024. GDPval: ICLR 2026. τ²-bench: desk-rejected at ICLR 2026, so arXiv only. SABER: rejected from the ICLR 2026 main track, so the workshop venue rests on the README only.
- **Still unverified.** OSWorld's star count (3,165) and RLI's star count and update date were not re-checked. They are time-varying, so do not cite them.

### Reference check summary (`refs/agentic.json`)

- **Coverage.** All **42** references were checked (0 skipped), and every entry now has `verified` and `verify_note` fields.
- **Result.** 42 are marked `verified: true` after the corrections below.
- **Problematic entries (12):** wrong or missing metadata that has now been fixed.
  - `stroebl2026hal`: wrong title, authors and ID. Replaced with arXiv:2510.11977; the README BibTeX is kept in `readme_bibtex_as_recorded`.
  - `zhu2025abc`: title and missing ID fixed (arXiv:2507.02825); NeurIPS 2025 D&B.
  - `zhou2023webarena`: venue fixed to ICLR 2024.
  - `xu2024theagentcompany`: venue fixed to NeurIPS 2025 D&B.
  - `openai2025gdpval`: title, authors and venue filled in.
  - `openai2025paperbench`: title, authors and venue filled in.
  - `gaia2023`: authors and venue filled in.
  - `metr2025horizon`: 25-author list filled in.
  - `andon2025vendingbench`: authors filled in.
  - `agentsThatMatter2024`: authors filled in.
  - `wei2025browsecomp`: author-name form changed to "Amelia Glaese".
  - `zhang2025cybench`: author-list version discrepancy noted.
- **Content issues in secondary sources.** `envcommonsGdpval2025` reports Table 2 numbers as headline win rates. `minimax2025m2` was over-cited as evidence for LLM-judge grading.
- **No fabrication found.** No reference was fabricated, and every arXiv ID in the file resolves to a paper with the stated title.

# Aggregators, Indices, and Leaderboard Infrastructure

Research dossier for the benchmark-landscape survey (Phase 1). Compiled 2026-09-29.

**How this was researched.**

- The session-wide WebSearch budget (200 calls) was used up before this subagent started, so every WebSearch call was refused.
- The following domains were also blocked by the egress proxy: artificialanalysis.ai, hai.stanford.edu, scale.com, vals.ai, huggingface.co, arxiv.org and epoch.ai. api.github.com also returned 403.
- All evidence therefore came from three GitHub channels:
  1. **Official repos (primary).** Raw README, docs and code files fetched with WebFetch from raw.githubusercontent.com:
     - stanford-crfm/helm
     - openai/simple-evals
     - LiveBench/LiveBench
     - EleutherAI/lm-evaluation-harness
     - UKGovernmentBEIS/inspect_ai and inspect_evals
     - epoch-research/eci-public and benchmark-stitching
     - huggingface/blog
     - mlresearch/v306 (the ICML 2026 PDF of Akhtar et al.)
  2. **Captured copies of primary pages (near-primary).** These are verbatim page captures stored in third-party repos, found with GitHub code search. The most important is a capture of the Artificial Analysis methodology page, including its version changelog, in `fstandhartinger/model-market-comparison`. That repo also holds captures of the Vals Index page. Others are text extractions of the AI Index 2025 and 2026 PDFs and a mirror of an Epoch AI newsletter post.
  3. **Secondary sources.** Practitioner research notes, newsletters and blogs on GitHub, found with GitHub code search.

**Evidence tags.**

| Tag | Meaning |
|---|---|
| **[V]** | Verified this session from a primary source: official repo, paper PDF, or official BibTeX/README |
| **[C]** | Seen in a captured or extracted copy of a primary page or PDF held in a third-party repo. Near-primary, but the capture's fidelity cannot be independently confirmed |
| **[S]** | Seen only in a secondary source (practitioner notes, newsletter, blog). The URL where I saw it is given |
| **[Sib]** | Taken from a sibling dossier in `research/notes/` and not re-verified by me |
| **[I]** | My interpretation |
| **[U]** | Unverified |

Citation counts could not be retrieved (Semantic Scholar and Google Scholar are blocked) and are omitted.

---

## Summary

1. **Aggregators act as the field's "consensus layer".** Their choices about which benchmarks to *include* and which to *drop* reveal what the community still finds informative. Three trends are visible across 2023–2026.

   **(a) Static knowledge and maths tests leave the indices.**
   - The HF Open LLM Leaderboard (OLL) replaced ARC, HellaSwag, MMLU, TruthfulQA, WinoGrande and GSM8K in June 2024 [S/Sib].
   - Artificial Analysis (AA) removed benchmarks from its Intelligence Index in stages [C]:
     - MATH-500 and AIME 2024 in Aug 2025;
     - MMLU-Pro, LiveCodeBench and AIME 2025 in Jan 2026;
     - IFBench in mid-2026;
     - GPQA Diamond in Sep 2026.
   - OpenAI's simple-evals labelled DROP and MGSM "saturated" and stopped updating in July 2025 [V].

   **(b) Agentic, long-horizon, economically framed tasks replace them.**
   - AA v4.3 weights "Agents" at 30% (AA-Briefcase, GDPval-AA v2, AutomationBench-AA) and "Coding" at 20% (Terminal-Bench v4.0, SciCode) [C]. Terminal-Bench sits in the Coding category, not Agents [corrected by fact-check].
   - The Vals Index weights finance, coding and legal agent tasks by each sector's share of US GDP [C].

   **(c) Evaluation moves from public academic benchmarks to aggregator-owned, often private, test sets.**
   - Examples: AA-LCR, AA-Omniscience, AA-Briefcase, GDP.pdf [C]; Vals "five private and two public benchmarks" [C]; Scale SEAL's private held-out sets [S].
2. **The first generation of open, academic aggregators has been retired or frozen.**
   - **HF OLL** was retired on **13 Mar 2025**. The stated reasons were that "as model capabilities change (hello reasoning and LM assistants), benchmarks need to follow", that the leaderboard was "slowly becoming obsolete", and that it "could encourage people to hill climb irrelevant directions" [S, quotes of HF discussion #1135 in two independent GitHub notes].
   - **Stanford HELM** entered **maintenance mode on 1 June 2026**: "no new evaluations will be added to the HELM leaderboards". The notice cites breakage from external APIs and recommends Evalchemy, Inspect Evals, Lighteval, LM Evaluation Harness and Unitxt [V].
   - **OpenAI simple-evals** stopped being updated in **July 2025** [V].
   - The *harnesses* are thriving: EleutherAI lm-evaluation-harness shipped a plugin system in 2026/09 [V], and UK AISI Inspect has 200+ pre-built evals [V].
   - The pattern [I]: **harnesses (infrastructure) outlive leaderboards (curation)**. Harnesses are cheap to maintain and serve many users. Leaderboards need continuous compute, curation, and a live defence against saturation and gaming.
3. **The second generation consists of independent, continuously re-versioned indices.**
   - **Artificial Analysis Intelligence Index.**
     - v1.0 Jan 2024 [S]; v4.3 by Sept 2026 [C].
     - Tracks 646 models [C].
     - Charts appear on lab launch pages (e.g., OpenAI's GPT-5.6 page, per [S]).
   - **Epoch AI Benchmarking Hub and Epoch Capabilities Index (ECI).**
     - The ECI is an IRT-style "Rosetta Stone" that stitches benchmarks onto one scale, anchored at Claude 3.5 Sonnet = 130 and GPT-5 = 150 [V].
   - **Vals AI** (Vals Index v2, Sep 2026) [C].
   - **Scale SEAL / "Scale Labs"** [S].
   - **LMArena ("Arena")**, a human-preference aggregator; see sibling `arenas_preference.md`.
   - These indices succeed on four things:
     - independence (they run the models themselves under identical settings);
     - speed of coverage;
     - explicit versioning with changelogs;
     - retiring saturated components.
   - They are contested over:
     - opaque reweighting (AA v4.1.1 drew bias accusations [S]);
     - dependence on LLM judges (~33% of AA weight, per [S]);
     - private sets that outsiders cannot audit;
     - funding and commercial conflicts (FrontierMath/OpenAI [S]; Meta's 49% stake in Scale [S]; Arena selling evaluation services to labs it ranks [S]).
4. **"Live" refresh alone does not keep a benchmark or aggregator informative.**
   - Akhtar et al. (ICML 2026) [V] computed an uncertainty-aware saturation index S_index:
     - LiveBench: **S_index = 0.99**. The top-5 range is only 1.09 points at ~79% accuracy, "suggesting model-level stagnation rather than task completion".
     - LiveCodeBench: 0.77.
     - Humanity's Last Exam (HLE): 0.22.
   - Private test sets (N = 4) saturate like public ones (N = 56): "Hiding test data does not appear to prevent saturation once benchmarks are widely adopted" [V].
   - LiveBench's own code lists 11 releases between 2024-06-24 and 2026-06-25, with a 5.5-month gap in 2026. The "monthly" cadence was therefore not sustained [V].
5. **Meta-reports (Stanford AI Index) are the field's "state of evaluation" reference.** They mostly re-publish self-reported numbers.
   - **AI Index 2025** [C]:
     - MMMU, GPQA and SWE-bench rose by 18.8, 48.9 and 67.3 pp within a year of introduction.
     - The HLE top score was 8.80%, FrontierMath 2%, and BigCodeBench 35.5% against a human standard of 97%.
     - The Chatbot Arena Elo-score gap between the top and 10th-ranked model shrank from 11.9% to 5.4% [corrected by fact-check].
     - Crucially, the Index "operates under the assumption that the scores reported by companies are accurate and factual".
   - **AI Index 2026** [C]:
     - "Evaluations intended to be challenging for years are saturated in months".
     - Benchmark error rates run "up to 42%", with "invalid question rates ranging from 2% on MMLU Math to 42% on GSM8K" (the AI Index's own wording).
       - [corrected by fact-check] These figures are precision@50 of the flagging method in Truong et al. (2025), i.e. the share of the 50 most-suspect *flagged* items that experts confirmed invalid (Precision@k = TP(k)/k). They are not benchmark-wide invalid rates. The same authors put GSM8K's error rate at "as high as 5%---a total of 88 questions" (SAIL blog, StanfordVL/sail-blog-new-post). Do not state that 42% of GSM8K is invalid.
     - The top 4 companies sit "within 25 Elo points".
     - Agents "still fail roughly one in three attempts on structured benchmarks".
6. **Implication for our new (non-game) benchmark [I].** To be picked up by aggregators and to survive, a benchmark should:
   - ship as a task in the standard harnesses (Inspect and lm-eval), since HELM itself points users there;
   - produce an accuracy-like score with a published standard error and enough items to keep resolution at the top (Akhtar: test-set size predicts slower saturation);
   - be regenerable, so that fresh item draws are cheap, rather than relying on a private set alone;
   - avoid LLM-judge dependence where possible;
   - be designed so that an independent third party (Epoch, AA, Vals, Scale) can run it under a fixed protocol and publish logs.

---

## Benchmark-by-benchmark

(Here "benchmark" means aggregator, index or infrastructure tool.)

### 1. Stanford HELM (Holistic Evaluation of Language Models)

- **What it measures.** A scenario × metric taxonomy.
  - The original paper measures 7 metrics (accuracy, calibration, robustness, fairness, bias, toxicity, efficiency) on 16 core scenarios "when possible (87.5% of the time)".
  - It runs 7 targeted evaluations over 26 targeted scenarios, for 42 scenarios in total [C: verbatim abstract mirrored in AkihikoWatanabe/paper_notes; also kube-dojo sources.md, which records the arXiv PDF downloaded 2026-04-28].
  - Later split into many leaderboards: HELM Capabilities, HELM Safety, VHELM (vision-language), HEIM (text-to-image), MedHELM, audio-language, and The Mighty ToRR (table reasoning) [V README].
- **Release date and venue.** arXiv:2211.09110 (Nov 2022). Published in TMLR 2023 with "Featured Certification, Expert Certification" [V official BibTeX in README].
- **Creators.** Stanford CRFM: Percy Liang, Rishi Bommasani, Tony Lee, Dimitris Tsipras, … Yifan Mai, Yuhui Zhang, Yuta Koreeda (50 authors in the BibTeX) [V].
- **Item count and format.**
  - The original evaluation covered 30 models on 42 scenarios, with all raw prompts and completions released [C abstract].
  - "Prior to HELM, models on average were evaluated on just 17.9% of the core HELM scenarios … We improve this to 96.0%" [C abstract].
  - The HELM Capabilities v1.15.0 release (dated 2025-11-24) covers 68 models [S pickai].
- **Frontier score at launch vs. latest.** Not applicable as a single number; HELM reports per-scenario means and win rates. Latest release data was nine months stale as of Aug 2026 [S pickai].
- **Adoption evidence.**
  - HELM's MMLU implementation was one of the three MMLU implementations compared by Hugging Face in June 2023. It gave LLaMA-65B 0.637, against 0.636 for the original implementation and 0.488 for the EleutherAI harness [V huggingface/blog].
  - HELM data underpins factor-analysis studies (Burnell et al. 2023: 27 HELM tasks) [Sib metascience_validity.md].
  - Several third-party benchmarks were absorbed as HELM Capabilities scenarios [Sib arenas_preference.md].
  - Use in frontier-lab model cards: **[U]** (not verified this session).
- **Status: abandoned (frozen).**
  - "HELM entered maintenance mode on June 1, 2026." No new features, "no new evaluations will be added to leaderboards", and active support for research collaborations has ended [V docs/maintenance_mode.md, README].
  - The stated risk: "many HELM scenarios and models rely on external APIs, which may change in reverse-incompatible ways" [V].
  - Recommended alternatives: Evalchemy, Inspect AI Evals, Lighteval, LLM Evaluation Harness, Unitxt [V].
- **Why it succeeded [I, backed by V].**
  - Academic credibility (TMLR certifications).
  - Standardized conditions across open, limited-access and closed models.
  - Full transparency of prompts and completions.
  - A multi-metric philosophy that made trade-offs visible.
  - It became the reference "third implementation" in reproducibility debates.
- **Why it failed or is failing [I, backed by V/S].**
  1. **Maintenance cost.** A living benchmark across many providers depends on external APIs that change or deprecate [V].
  2. **Staleness at the frontier.** Reported as nine months stale by Aug 2026 [S]; a secondary critique cites "compute intensity and staleness at the frontier" [S markusstrasser].
  3. **Fragmentation** into many sub-leaderboards, with no single headline number labs could quote [I].
  4. **Scenario difficulty.** The core scenarios (many pre-2022 datasets) saturated [I; consistent with AI Index 2026].
  5. **Funding and staffing** for an academic group. The notice mentions volunteer, best-effort maintenance [V].
- **Sources.**
  - https://raw.githubusercontent.com/stanford-crfm/helm/HEAD/README.md
  - https://raw.githubusercontent.com/stanford-crfm/helm/HEAD/docs/maintenance_mode.md
  - AkihikoWatanabe/paper_notes `agent_docs/TMLR.xml` (abstract; via GitHub code search)
  - https://raw.githubusercontent.com/huggingface/blog/main/open-llm-leaderboard-mmlu.md
  - https://raw.githubusercontent.com/niftymonkey/pickai/main/design/research/free-benchmark-sources.md
  - https://raw.githubusercontent.com/markusstrasser/agent-infra/HEAD/research/2026-06-14-benchmark-leaderboard-methodology-critique.md

### 2. Hugging Face Open LLM Leaderboard (v1 → v2 → retired)

- **What it measures.** Automated, standardized evaluation of open-weight models on Hugging Face, run on the same harness and hardware.
  - v1 tasks: ARC-Challenge, HellaSwag, MMLU, TruthfulQA, WinoGrande, GSM8K [Sib knowledge_exams.md, from the HF archived collection page].
  - DROP was added and later removed because of normalisation and stop-token scoring bugs [Sib other_dead_benchmarks.md, from the HF blog source].
  - v2 tasks: MMLU-Pro, GPQA, MuSR, MATH Level 5, IFEval, BBH [S sasilver75 notes of the HF v2 blog; S turbobeest/modelspec; confirmed by Akhtar et al.'s companion code per Sib].
- **Release date and venue.**
  - v1: 2023. The HF blog was already writing about the leaderboard on 12 June 2023 and 23 June 2023 [V huggingface/blog `_blog.yml`]. A sibling gives April 2023 [Sib].
  - v2: announced **26 June 2024** in the HF blog/Space "Performances are plateauing, let's make the leaderboard steep again" [S sasilver75/obsidian].
  - Retired **13 March 2025** [S, two independent GitHub notes quoting HF discussion #1135; commit log "Hasta la vista, leaderboard" at 2025-03-13T19:18:55Z per pickai].
- **Creators.** Hugging Face. The June 2023 blog is by the handles clefourrier, SaylorTwift, slippylolo and thomwolf [V]. The retirement post was by Clémentine Fourrier [S]. It is powered by EleutherAI lm-evaluation-harness [V harness README: "backend for Hugging Face's Open LLM Leaderboard"].
- **Item count and format.** 6 benchmarks per version, multiple-choice and generative. v2 normalised each score "between the random-choice baseline and the maximal possible score (100 points)" [S]. More than 13K models were evaluated over its life [Sib knowledge_exams.md].
- **Frontier score at launch vs. latest.** Not recorded here [U]. The v2 motivation was that v1 benchmarks "became too easy for models" [S].
- **Adoption evidence.**
  - The canonical open-model leaderboard of 2023–2025 [S].
  - Its archive became a research dataset for IRT and "tiny" benchmark work (metabench, tinyBenchmarks, Sloth, Growing Pains) [Sib metascience_validity.md].
  - It is still cited in 2025–2026 model blogs as "not active anymore" (e.g., IBM foundation-model-stack Bamba blog) [S].
- **Status: abandoned (retired, archived).**
- **Stated reasons for retirement** (quotes of Fourrier's post, seen in two independent GitHub notes) [S]:
  - "all good things come to an end: the leaderboard is officially retiring!"
  - "As model capabilities change (hello reasoning and LM assistants), benchmarks need to follow! The leaderboard is slowly becoming obsolete; we feel it could encourage people to hill climb irrelevant directions in the field. So we'd like to stop it before it happens."
  - The post also mentions "over 200 community-led leaderboards on Hugging Face" [S aledlie blog, which dates the post 13 March 2025].
- **Why it succeeded [I].**
  - Free and open submission.
  - Identical harness, prompts and hardware for everyone.
  - Reproducible.
  - A single average for ranking.
  - A strong community (voting, "maintainer's choice") [S].
- **Why it failed [I, backed by V/S/Sib].**
  1. **Saturation and contamination** of v1 tasks, the stated reasons for v2 [S].
  2. **Implementation fragility.** The June 2023 MMLU discrepancy (LLaMA-65B 0.637 vs 0.488 depending on implementation) showed "evaluations are strongly tied to their implementations–down to minute details such as prompts and tokenization" [V]. The DROP bug forced removal of a task [Sib].
  3. **Goodharting.** The maintainers themselves feared people would "hill climb irrelevant directions" [S]. A 2026 Hacker News post, "How I topped the HuggingFace open LLM leaderboard on two gaming GPUs", describes duplicating ~7 middle layers [S rasynai/MarigoldBench notes].
  4. **Scope.** Open-weight models only, so no frontier closed models [S pickai]. Static base-model tasks missed reasoning and agentic abilities [S quote].
  5. **Statistical resolution.** On v1, 11 of 40 adjacent model pairs were statistically unresolvable [Sib contamination_saturation_stats.md].
  6. **Compute cost.** Commonly cited but not verified here [U]. One secondary note asserting cost reasons also misdates the archive to June 2024, so it is treated as unreliable.
- **Sources.**
  - https://raw.githubusercontent.com/huggingface/blog/main/open-llm-leaderboard-mmlu.md
  - huggingface/blog `_blog.yml` (code search)
  - https://raw.githubusercontent.com/sasilver75/obsidian/HEAD/Open%20LLM%20Leaderboard%20V2.md
  - https://raw.githubusercontent.com/niftymonkey/pickai/main/design/research/free-benchmark-sources.md
  - https://raw.githubusercontent.com/niftymonkey/pickai/main/design/research/benchmark-adoption.md
  - aledlie/aledlie.github.io `_posts/2026-08-11-stale-marquee-claims.md` (code search)
  - foundation-model-stack/bamba `blog/bamba31T.md` (code search)
  - https://raw.githubusercontent.com/EleutherAI/lm-evaluation-harness/main/README.md

### 3. LiveBench

- **What it measures.** General LLM ability across 6 categories: Reasoning, Math, Coding, Language, Data Analysis, Instruction Following. It has "18 diverse tasks".
  - Questions have "verifiable, objective ground-truth answers … without the use of an LLM judge" [V README; V changelog 2024-06-12].
  - An agentic-coding category was added 2025-05-30, using SWE-Agent, later Mini-SWE-Agent with a 250-step limit (2025-10-03) [V changelog].
- **Release date and venue.**
  - Initial launch 2024-06-12 [V changelog]. arXiv:2406.19314.
  - ICLR 2025 Spotlight [V README].
  - Title in the official BibTeX: "LiveBench: A Challenging, Contamination-Free LLM Benchmark". Akhtar et al. cite it as "…Contamination-Limited…" [V both].
- **Creators.** Colin White, Samuel Dooley, Manley Roberts, Arka Pal, Benjamin Feuer, Siddhartha Jain, Ravid Shwartz-Ziv, Neel Jain, Khalid Saifullah, Sreemanti Dey, Shubh-Agrawal, Sandeep Singh Sandha, Siddartha Venkat Naidu, Chinmay Hegde, Yann LeCun, Tom Goldstein, Willie Neiswanger, Micah Goldblum [V BibTeX].
- **Item count and format.**
  - About 1,000 questions after 2024-07-26 ("brought the total number of questions to 1000") [V changelog]. Akhtar et al. use n = 1000 [V].
  - Question sources are "recently-released datasets, arXiv papers, news articles, and IMDb movie synopses" [V README].
- **Release cadence (claimed vs. actual).**
  - The README says "LiveBench releases new questions monthly" [V].
  - The code's `LIVE_BENCH_RELEASES` lists 2024-06-24, 2024-07-26, 2024-08-31, 2024-11-25, 2025-04-02, 2025-04-25, 2025-05-30, 2025-11-25, 2025-12-23, 2026-01-08 and 2026-06-25 [V `livebench/common.py`]. That is 11 releases in ~24 months, including gaps of ~4, ~6 and ~5.5 months.
  - Fact-check addition: changelog.md's newest entry is 2026-01-08, and there is no changelog entry for the 2026-06-25 release listed in code. Separately, the Inspect Evals LiveBench README states "The dataset completely refreshes every 6 months and the authors delay publicly releasing the questions from the most-recent update". The original arXiv abstract promised questions "added and updated on a monthly basis" [V/C].
- **Frontier score at launch vs. latest.**
  - Launch (June 2024): the original arXiv abstract states "LiveBench is difficult, with top models achieving below 65% accuracy" [C: abstract reproduced in aishwaryanr/awesome-generative-ai-guide] [corrected by fact-check].
  - Latest: top models at ~79%, with the top-5 range compressed to 1.09 points (Akhtar et al., ICML 2026, from leaderboard data) [V].
  - A June 2026 Reddit comment observed "Claude 4.8, Gemini 3.1, GPT-5.4, and GPT-5.5 all within 4 total points out of ~80" [S pickai].
- **Adoption evidence.**
  - ICLR spotlight [V]. Widely listed by aggregators and practitioners (ModelHub uses LiveBench as a "backbone, contamination-resistant" source [S]).
  - The repo has 1,299 stars and was pushed 2026-08-29 [S pickai].
  - Akhtar et al. included it among 60 widely used benchmarks [V].
- **Status: active but saturated/contested.**
- **Why it succeeded [I].**
  - Objective auto-scoring with no judge bias.
  - Contamination-limiting by design.
  - Broad categories packaged as one number.
  - Free and open.
  - High-profile authors and venue.
- **Why it is failing [V/S/I].**
  1. **Score compression.** S_index 0.99 at ~79% accuracy is "model-level stagnation rather than task completion" [V Akhtar]. The benchmark no longer separates the frontier even though it is not near 100%. Likely causes [I]: small per-task n and noisy items near the ceiling of what is solvable.
  2. **Cadence slippage.** Refresh depends on a small team [V release list; I].
  3. **Reputation.** Practitioner comments: "Livebench is a notoriously sloppy benchmark… artificial analysis is a better bench"; "livebench was good, but now it's a joke" [S pickai, Reddit quotes; low evidentiary weight].
  4. **Public release after each round** lets older questions leak into training data [I].
  5. **Fragile data access.** The leaderboard is a single-page app whose CSV snapshots rotate; there is a domain migration [S pickai].
- **Sources.**
  - https://raw.githubusercontent.com/LiveBench/LiveBench/main/README.md
  - https://raw.githubusercontent.com/LiveBench/LiveBench/main/changelog.md
  - LiveBench/LiveBench `livebench/common.py` (code search)
  - Akhtar et al. PDF: https://raw.githubusercontent.com/mlresearch/v306/main/assets/akhtar26a/akhtar26a.pdf
  - https://raw.githubusercontent.com/niftymonkey/pickai/main/design/research/benchmark-adoption.md
  - https://raw.githubusercontent.com/DDamianZR/ModelHub/HEAD/SOURCES.md

### 4. Epoch AI Benchmarking Hub

- **What it measures.** A database of benchmark results. Epoch runs some evaluations itself and collates others from external benchmark maintainers.
  - The mirrored Epoch newsletter says: "Third-party organizations, such as Epoch AI, independently run and collate benchmark results on a page like the benchmarking hub" [C].
  - Epoch-run benchmarks include GPQA Diamond, MATH Level 5, OTIS Mock AIME, FrontierMath (Tiers 1–3 and Tier 4) and SWE-bench Verified [S htihle provenance audit; S AINews May 2025].
  - External additions (~May 2025): Aider Polyglot, WeirdML, Balrog and Factorio Learning Environment, then VPCT, Fiction-liveBench, GeoBench and SimpleBench [S AINews 2025-05-07 and 2025-05-30].
- **Release date.** Launch date **[U]**. An Epoch SWE-bench Docker-image registry repo was created 2024-10-28 [V repo metadata]. The Hub was operating by at least May 2025 [S].
- **Creators.** Epoch AI.
- **Item count and format.**
  - The data ships as `epoch.ai/data/benchmark_data.zip` under CC-BY-4.0, with about 76–80 CSVs [S pickai; S ModelHub].
  - Rows include standard errors and public eval logs [S ModelHub]. Evaluations appear to use UK AISI Inspect [S htihle: "Epoch AI (Inspect)"; V that the org has Inspect-related repos].
- **Frontier scores.** Benchmark-specific. See the per-benchmark sibling dossiers (math.md, knowledge_exams.md, coding.md).
- **Adoption evidence.**
  - Other aggregators and indices build on it (ECI; Mozilla's State of Open Source AI report uses ECI [S]).
  - Practitioners describe it as "the more defensible one" relative to AA [S pickai].
  - Epoch results are frequently quoted in model-launch discourse, e.g., its DeepSeek-R1-0528 GPQA Diamond 76% (±2%) [S AINews].
- **Status: thriving (niche-to-mainstream).**
- **Why it succeeded [S/I].**
  - Independent runs with confidence intervals.
  - Clear policy: no scores reported until errors are resolved, "except in pathological cases" [C].
  - Open licence and bulk data.
  - Public logs.
  - Willingness to correct errors after outside replication. A statistician found that "24/144 of the sets contain LLMs with different release dates", and "Epoch have confirmed this is a mistake… and they will correct it" [S pickai].
- **Why it could fail [S/I].**
  1. **Funding conflicts.** FrontierMath was funded by OpenAI. The htihle audit says only, conditionally, that contamination biases such as OpenAI's FrontierMath access "would inflate closed-side scores"; it does not claim this has been shown. That audit is itself LLM-generated ("Independent Opus 4.7 web-research audit") [S htihle; S arvindcr4 "Funder / commissioner: OpenAI"] [corrected by fact-check]. Sibling dossiers discuss the o3 FrontierMath 25% vs ~10% discrepancy [Sib].
  2. **Cost limits coverage.** Only a subset of models and benchmarks is run internally [I].
  3. **Adoption gap versus AA** in developer tooling [S pickai: ECI reference repo has few stars].
- **Sources.**
  - https://raw.githubusercontent.com/shakir-fattani/ai-updates/HEAD/epochai.substack.com/why-benchmarking-is-hard/content.md
  - https://raw.githubusercontent.com/htihle/open_closed_gap/HEAD/provenance_audit/APPENDIX.md
  - https://raw.githubusercontent.com/DDamianZR/ModelHub/HEAD/SOURCES.md
  - https://raw.githubusercontent.com/niftymonkey/pickai/main/design/research/benchmark-adoption.md
  - smol-ai/ainews-web-2025 frozen issues 25-05-07 and 25-05-30 (code search)
  - GitHub org listing for epoch-research (search_repositories)

### 5. Epoch Capabilities Index (ECI)

- **What it measures.** A single latent "capability" score per model. It fits "performance = sigmoid(discriminability * (capability − difficulty))" across benchmarks, which is an IRT/2PL-style model [V eci-public README].
  - Every benchmark gets a difficulty and a slope; every model gets a capability with bootstrap CIs [V].
  - The scale is anchored at **Claude 3.5 Sonnet = 130 and GPT-5 = 150**. Anchor models are "pinned by definition" [V].
  - This 130/150 anchoring is the published ECI product's convention (eci-public README). The Rosetta Stone paper resolves identifiability by fixing one benchmark (e.g. WinoGrande, α = 1, D = 0) [S memgrafter digest]. Cite the anchors to the ECI documentation, not the paper [corrected by fact-check].
- **Release date and venue.** Paper: "A Rosetta Stone for AI Benchmarks", arXiv:2512.00193 (2025) [V eci-public README].
  - Precursor code repo `epoch-research/benchmark-stitching` created 2025-07-01 [V metadata; README describes forecasting, acceleration detection and optimisation-effect analyses].
  - `eci-public` created 2026-02-01 [V metadata].
- **Creators.** Anson Ho, Jean-Stanislas Denain, David Atanasov, Samuel Albanie, Rohin Shah [V].
- **Item count and format.**
  - About 37 benchmarks and 867 rows in `epoch_capabilities_index.csv` (Aug 2026) [S pickai]. Another secondary note says "40+ benchmarks, min 4 evals/model" [S Dylancouzon, citing epoch.ai/benchmarks/eci]. Treat the count as ~37–40+ [S].
  - "+5 ECI ≈ a doubling of the METR time horizon" [S Dylancouzon; U].
- **Latest known scores.** Per Mozilla's "The state of open source AI" (v1.0.1, July 2026): GPT-5.6 Sol 162 vs. Kimi K3 156, a 6-point open–closed gap with overlapping CIs [S dgirard/fiches-veille summary].
- **Adoption evidence.** Used in Mozilla's report [S], by independent Bayesian re-implementations (linkofrivia/ECI_Bayesian: K = 4 multidimensional Beta-MIRT over 88–96 benchmarks) [S], and by forecasting analyses [S].
- **Status: active / niche** (methodologically influential, modest direct uptake).
- **Why it matters for us [I].** ECI is the clearest answer to the user's critique that game-benchmark scores are "none comparable to other benchmarks": a new benchmark can be linked to ECI via shared models. This also sets the bar for *discriminant* validity. A new benchmark that just re-measures the ECI factor adds little [Sib metascience_validity.md].
- **Weaknesses [S/Sib/I].**
  1. Unidimensionality is assumed, not tested [Sib metascience_validity.md]. ECI_Bayesian decomposes capability into four axes [S].
  2. Correctness depends on how benchmarks and model versions are pooled; the replication-found aggregation error is noted above [S].
  3. Benchmarks with thin model panels cannot be identified. ECI_Bayesian drops MindCube because its "5-taker panel cannot identify a loading row" [S].
- **Sources.**
  - https://raw.githubusercontent.com/epoch-research/eci-public/main/README.md
  - https://raw.githubusercontent.com/epoch-research/benchmark-stitching/main/README.md
  - https://raw.githubusercontent.com/linkofrivia/ECI_Bayesian/HEAD/README.md
  - dgirard/fiches-veille `fiches/2026-07/mozilla-state-of-open-source-ai-2026-07.md` (code search)
  - Dylancouzon/AIE-talk `research/H-lag-chart.md` (code search)

### 6. Artificial Analysis (AA) Intelligence Index

- **What it measures.** A weighted composite of independently re-run evaluations. As of the captured methodology page (Sept 2026), **v4.3** uses 10 evaluations in four categories [C]:
  - **Agents 30%:** AA-Briefcase, GDPval-AA v2, AutomationBench-AA
  - **Coding 20%:** Terminal-Bench v4.0, SciCode
  - **General 30%:** AA-Omniscience, GDP.pdf, AA-LCR v1.1
  - **Scientific Reasoning 20%:** HLE, CritPt
  - AA also publishes speed, latency, price, "cost per Intelligence Index task", and Coding and Agentic sub-indices [C; S].
- **Methodology principles** [C]:
  - "Standardized: All models are evaluated under identical conditions…"
  - "Zero-Shot Instruction Prompted"
  - "Transparent: We disclose our methodology, including prompt templates…"
  - "a 95% confidence interval for Artificial Analysis Intelligence Index of less than ±1%" (from experiments with >10 repeats)
  - Temperature 0 for non-reasoning models and 0.6 for reasoning models; pass@1.
- **Version history** (captured AA changelog [C], cross-checked against the MaxiZm/actualanalysis audit [S], which is self-described as written by a "Gemini Agent", i.e. AI-generated and not an independent human audit [corrected by fact-check]; a second independent capture of the AA page (dingkwang/agent-eval-course, Aug 2026, v4.1.1 with GPQA Diamond still included) is consistent):

| Version | Dates | Change |
|---|---|---|
| v1.0 | ~Jan 2024 | First version [S hollobit/SOTA] |
| v2.0 | 11 Feb 2025 – 4 Aug 2025 | [C] |
| v2.1 | Aug 2025 | "Added IFBench / Added AIME 2025 / Removed MATH-500 / Removed AIME 2024" [C] |
| v2.2 | Aug–Sep 2025 | Added AA-LCR [S] |
| v3.0 | 2 Sep – Dec 2025 | Added Terminal-Bench Hard and τ²-Bench Telecom; "Included MMLU-Pro and LiveCodeBench in Intelligence Index" [C] |
| v4.0 | Jan 2026 | Added GDPval-AA, AA-Omniscience and CritPt; "Removed MMLU-Pro, LiveCodeBench, AIME 2025 from Intelligence Index"; "New category-based weighting structure: Agents (25%), Coding (25%), General (25%), Scientific Reasoning (25%)" [C] |
| v4.0.1–v4.0.4 | Jan – Jun 2026 | Terminal-Bench Hard trimmed to 44 tasks (broken dependencies); GDPval-AA re-anchored; grader-model swaps due to deprecations [C/S] |
| v4.1 | Jun – Aug 2026 | GDPval-AA v2 (panel of three frontier LLM judges; Elo re-baselined to human experts = 1000); Terminal-Bench Hard → Terminal-Bench v2.1; τ²-Bench Telecom → τ³-Banking; "Removed IFBench from the Intelligence Index (we continue to run it…)"; weights "Agents (34%), Coding (24%), Scientific Reasoning (24%), General (18%)" [C; added by fact-check] |
| v4.1.1 | Aug – Sep 2026 | Pinned τ³-Banking to upstream; graders for HLE, AA-LCR and AA-Omniscience upgraded to GPT-5.6 Luna [C] |
| v4.2 | Sep 2026 | "Added GDP.pdf (10%)…"; "Removed GPQA Diamond from the Intelligence Index"; AA-LCR → v1.1; added AA-Briefcase (15%) [C] |
| v4.3 | current at capture (late Sep 2026) | 10 evals, 30/20/30/20 weights [C] |

- **Creators.** Artificial Analysis, an independent company. Its about page lists angel backers (Nat Friedman, Daniel Gross, Andrew Ng, others) [S pickai]. Whether labs pay for evaluations is not disclosed [S].
- **Item count.** 646 models on the index page at capture [C]; "500+ models" [S].
- **Frontier score at launch vs. latest.** Scores are not comparable across versions [I; the changelog says minor bumps "may include changes to contributing evaluations, … weightings, anchors" (S pickai quoting AA API docs)]. Reported points:
  - v4.0: GLM-5 was the first open model to reach 50 [S].
  - v4.1 (July 2026): best closed model 61 (Claude Opus 5), best open 57 (Kimi K3) [S Mozilla report via dgirard].
  - v4.1.1 (Aug 2026): Opus 5 63, Fable 5 62, Kimi K3 60, DeepSeek V4 Pro 0813 53 [S wmpeng/codingplan].
- **Adoption evidence.**
  - OpenAI's GPT-5.6 launch page reportedly shows two AA Intelligence Index v4.1 charts [S wmpeng].
  - OpenRouter exposes AA indices for 165 of 396 models [S pickai].
  - Mozilla's 2026 report uses it as its headline capability measure [S].
  - Developer tools select models from it; e.g., BasedHardware/omi refreshes daily from AA [S pickai].
  - It is widely cited in open-model launch coverage (GLM-5, DeepSeek V4, Kimi K3) [S multiple].
- **Status: thriving (the de facto public composite in 2026), but contested.**
- **Why it succeeded [I, backed by C/S].**
  - It runs every model itself under identical zero-shot settings.
  - It covers new releases within days.
  - It combines intelligence with price and speed, which is what buyers need.
  - It publishes a changelog and CIs.
  - It **aggressively retires saturated components**: MATH-500, AIME 2024, AIME 2025, MMLU-Pro, LiveCodeBench, IFBench and GPQA Diamond were all removed between Aug 2025 and Sep 2026 [C].
  - It keeps the index hard by adding agentic, economically framed tasks.
- **Why it is contested [S/I].**
  1. **Frequent reweighting.** It invites accusations: "An open source mode (Qwen 3.8 max) was number 1 on the agentic index, then they just so happen to launch 'v4.1.1'… Highly likely to be paid off imo" [S Reddit via pickai; unsubstantiated allegation].
  2. **LLM-judge dependence.** "~33% of weight flows through LLM judges" [S markusstrasser]. GDPval-AA v2 uses "a panel of three frontier LLM judges" [C]. The graders are themselves frontier models, e.g., GPT-5.6 Luna [C], so the index is not judge-neutral [I].
  3. **Aggregator-owned evals.** AA-LCR, AA-Omniscience, AA-Briefcase, AutomationBench-AA and GDPval-AA reduce external reproducibility [I]. One meta-analysis notes the index "mixes proprietary evals … with public ones" and that "items do not rotate on a schedule" [S indexable-inc].
  4. **Restrictive data licence.** Attribution is required; redistribution is restricted [S pickai; S fstandhartinger ops notes].
  5. **Version churn** makes longitudinal comparison hard [I].
- **Sources.**
  - Captured AA methodology page: https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/HEAD/ops/rebuild-2026-09/evidence/phase-04/sources/aa-1ea3e75f96c3.txt (and code-search fragments of the same file)
  - https://raw.githubusercontent.com/MaxiZm/actualanalysis/HEAD/docs/audits/coverage-expansion-2026-09-06/artificial-analysis.md
  - https://raw.githubusercontent.com/niftymonkey/pickai/main/design/research/benchmark-adoption.md
  - https://raw.githubusercontent.com/markusstrasser/agent-infra/HEAD/research/2026-06-14-benchmark-leaderboard-methodology-critique.md
  - wmpeng/codingplan and dgirard/fiches-veille notes (code search)
  - hollobit/SOTA HISTORY.md (code search)
  - indexable-inc/index-bak `benchmark-meta-analysis.svx` (code search)

### 7. Scale AI SEAL leaderboards (now "Scale Labs")

- **What it measures.** Expert-built frontier, agentic and safety evaluations, many on **private held-out datasets**.
  - Boards include Humanity's Last Exam (run with CAIS) [S htihle], SWE-Bench Pro (public and commercial subsets; arXiv:2509.16941) [S razzant/ouroboros], MCP Atlas [S fstandhartinger capture URLs] and SEAL Tool Use [S linkofrivia].
  - Also SEAL Showdown, a demographically verified human-preference arena (Sept 2025) [Sib arenas_preference.md].
- **Release date.** SEAL Leaderboards were introduced ~late May 2024 "with private datasets and paid annotators for fairer, higher quality expert evaluations of frontier models" [S AINews 2024-05-30, citing r/LocalLLaMA].
- **Creators.** Scale AI (Safety, Evaluations and Alignment Lab).
- **Item count and format.**
  - 233 score rows across 39 categories as of Aug 2026 [S pickai]; "20+ benchmarks, 100+ models" [S ModelHub].
  - The SWE-Bench Pro public set has 731 instances from copyleft repos [S linkofrivia].
  - Rebranded as "Scale Labs" (labs.scale.com) [S pickai].
- **Frontier scores.** Benchmark-specific; see sibling dossiers.
- **Adoption evidence.**
  - HLE's official board [S].
  - SWE-Bench Pro became a standard agentic-coding metric [Sib coding.md].
  - Practitioner aggregators cite "Scale SEAL SWE-bench Pro" [S].
- **Status: active.**
- **Why it succeeded [S/I].**
  - Private held-out sets give the "highest" anti-contamination value of any source [S ModelHub].
  - Expert construction.
  - Frontier difficulty.
  - Scale's annotation network makes such data possible.
- **Why it is contested or at risk [S/I].**
  1. **Neutrality.** Scale is a data vendor to labs. Meta took a 49% stake in 2025, and one analysis argues the "neutrality" promise "broke … irreversibly" [S guzus; the stake figure is not verified from primary sources here].
  2. **Opacity.** Private sets cannot be audited by outsiders, and rows are often agent+model scaffolds rather than models [S pickai]. There is no API or data export, and the licence is unclear [S].
  3. **Private sets do not prevent saturation** once widely adopted [V Akhtar et al.].
- **Sources.**
  - smol-ai/ainews-web-2025 `24-05-30-ainews-contextual-position-encoding-cope.md` (code search)
  - https://raw.githubusercontent.com/htihle/open_closed_gap/HEAD/provenance_audit/APPENDIX.md
  - https://raw.githubusercontent.com/DDamianZR/ModelHub/HEAD/SOURCES.md
  - https://raw.githubusercontent.com/niftymonkey/pickai/main/design/research/free-benchmark-sources.md
  - razzant/ouroboros `devtools/benchmarks/swe_bench_pro/METHODOLOGY.md` (code search)
  - linkofrivia/ECI_Bayesian `data/curated/benchmark_access.csv` (code search)
  - guzus/ai-research-arm (code search)

### 8. Vals AI (Vals Index)

- **What it measures.** Independently run evaluations of "economically valuable and real-world tasks" [S fstandhartinger change-request list]. There are 40+ benchmarks (GPQA, MMLU-Pro, MMMU, SWE-bench, LiveCodeBench, plus domain sets), with accuracy, latency, cost per test and token counts reported per model [S pickai].
- **Vals Index v2** (page captured 2026-09-18; "Updated 9/15/2026, Version 2") [C]:
  - Described as "A single measure of AI's potential economic impact — agentic model performance across finance, coding, and legal tasks, weighted by each sector's share of U.S. GDP."
  - Components:
    - Finance (~8.0% GDP): Finance Agent v2, Excel Modeling Benchmark
    - Coding (~5.6%): Terminal-Bench 2.1, Vibe Code Bench, Code Migration
    - Legal (~1.2%): Legal Research Bench, HLAB
  - It aggregates "five private and two public benchmarks".
  - Accuracy is published with a standard error per model, and Finance Agent v2 averages three runs per model. [corrected by fact-check] Both statements come from the capturing repo's registry notes, not the captured page text; that repo's own verifier flagged them as absent from the excerpt. Independent partial support: maxim-saplin/llm_chess lists an upstream `stderr` for the Vals Index score (earlier version). Treat as [S], not [C].
- **Release date and creators.** Vals AI. Founding and launch dates **[U]**.
- **Latest scores** (Sep 2026) [C]: Claude Fable 5.1 68.83%, Claude Opus 5 67.21%, GPT-6 Astra 66.61%.
- **Adoption evidence.** It is listed alongside AA, Epoch, Scale Labs and LiveBench as a flagship independent evaluator in practitioner tooling [S fstandhartinger]. Model identifiers use provider/model form, giving the best exact-match rate against models.dev [S pickai].
- **Status: active (enterprise niche, growing).**
- **Why it succeeded [I].**
  - Domain realism (legal, finance, tax).
  - Private sets.
  - Economic weighting that speaks to buyers.
  - Standard errors.
- **Risks [S/I].**
  - "no license or terms statement exists anywhere on the site" [S pickai].
  - Private sets cannot be audited.
  - GDP weights are a normative choice.
  - Small public profile compared with AA.
- **Sources.**
  - https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/HEAD/data/raw/benchmarks/daily-evidence/2026-09-18T12-58-20-378Z/gauntlet/protocol-vals-index-finance-agent-2/packet-r1.md
  - https://raw.githubusercontent.com/niftymonkey/pickai/main/design/research/free-benchmark-sources.md

### 9. LMArena ("Arena") as an aggregator

The full treatment is in sibling `arenas_preference.md`. Aggregator-relevant points seen this session:

- **Scale and business.** It has a CC-BY-4.0 public leaderboard-history dataset (`lmarena-ai/leaderboard-dataset`) with 2,251,197 rows, released April 2026 [S pickai]. It raised $150M at a $1.7B valuation in Jan 2026, and "Its paying customers include AI companies whose models appear on the leaderboard" [S pickai].
- **The Leaderboard Illusion** (arXiv:2504.20879) [S, quoted in pickai and markusstrasser]:
  - "27 private LLM variants tested by Meta in the lead-up to the Llama-4 release".
  - Google and OpenAI received "an estimated 19.2% and 20.4% of all data on the arena", against 29.7% for 83 open-weight models combined.
  - Additional Arena data can yield "relative performance gains of up to 112%".
- **AI Index 2026** notes that "Arena leaderboard standing may partly reflect adaptation to the platform rather than general capability", and that the top 4 companies cluster within 25 Elo [C].
- **Status: thriving but contested.** Among developers it has the weakest reputation of the candidate data sources [S pickai], yet it is still "a bit harder to fake" than public static benchmarks [S Reddit quote].
- **Sources.**
  - https://raw.githubusercontent.com/niftymonkey/pickai/main/design/research/benchmark-adoption.md
  - https://raw.githubusercontent.com/markusstrasser/agent-infra/HEAD/research/2026-06-14-benchmark-leaderboard-methodology-critique.md
  - https://raw.githubusercontent.com/malafronte/ai-tools-lab/HEAD/anydoc/output/batch-2026-09-01/02-structured-pdf.md

### 10. Stanford AI Index (2025 and 2026 reports): the meta-aggregator

- **What it is.** An annual report by Stanford HAI. Chapter 2 (Technical Performance) compiles benchmark state-of-the-art values and calibrates the best model against human baselines [C].
- **Sourcing methodology (2025)** [C]: "the Index sources benchmark scores from leaderboards, public repositories such as Papers With Code and RankedAGI, as well as company papers, blog posts, and product releases. The Index operates under the assumption that the scores reported by companies are accurate and factual." Scores were current as of mid-February 2025.
- **2025 findings on benchmarks** [C: HAI page capture and parsed chapter PDF]:
  - "In 2023, researchers introduced new benchmarks—MMMU, GPQA, and SWE-bench… scores rose by 18.8, 48.9, and 67.3 percentage points".
  - "The saturation of traditional AI benchmarks like MMLU, GSM8K, and HumanEval… has pushed researchers to explore additional evaluation methods". Examples: HLE ("the top system scores just 8.80%"), FrontierMath ("AI systems solve only 2% of problems") and BigCodeBench ("35.5% success rate—well below the human standard of 97%").
  - Frontier convergence: the top vs. 10th-model gap fell from 11.9% to 5.4%, and the top two were separated by 0.7%.
  - The open–closed gap narrowed from 8.04% (Jan 2024) to 1.70% (Feb 2025).
  - "Complex reasoning remains a problem" (PlanBench).
- **2026 findings on benchmarks** [C: chapter-highlight extraction; S secondary summaries]:
  - "Evaluations intended to be challenging for years are saturated in months, compressing the window in which benchmarks remain useful for tracking progress."
  - "The benchmarks used to measure AI progress face growing reliability and gaming concerns, with error rates up to 42% on widely used evaluations."
    - Invalid-question rates (precision@50): MMLU Math and OpenBookQA 2%, MMLU Cli/Med 6%, AIR-Bench 9%, MedQA 23%, ThaiExam 26%, MMLU 5Sub 31%, GSM8K 42% [C sermakarevich chunks].
      - [corrected by fact-check] Precision@50 (Truong et al. 2025, "Fantastic Bugs and Where to Find Them in AI Benchmarks", NeurIPS 2025, arXiv:2511.16842) is the fraction of the top-50 *flagged* items confirmed invalid. It measures the flagging method's hit rate, not the share of each benchmark that is invalid. GSM8K's estimated error rate is ~5% (88 questions) per the same authors.
    - Responses mentioned: Truong et al. (2025), a statistical item-flagging framework with "up to 84% precision", and Cheng et al. (2025), a "certificate-grade", community-governed framework with secure environments, continuously refreshed items and delayed result disclosure [C].
  - "Top model performance is converging, with 4 companies now clustered within 25 Elo points" [C].
  - "AI agents … still fail roughly one in three attempts on structured benchmarks" [C].
  - Frontier systems reached or exceeded human baselines on MMLU, MMMU, GPQA Diamond, AIME, ImageNet and SuperGLUE [C sermakarevich].
  - HLE: "Frontier models gained 30 percentage points in a single year on Humanity's Last Exam" [C: verbatim in AI Index 2026 highlight extractions, malafronte/ai-tools-lab and mineru-lab; upgraded by fact-check].
  - SWE-bench Verified went from ~60% to ~100% of the AI Index human-baseline-normalised score in one year [S FractalK; exact framing U].
  - Jagged intelligence: IMO gold, yet analog clocks are read correctly only 50.6% of the time vs 90.1% for humans (ClockBench) [C].
  - The Foundation Model Transparency Index fell from 58 to 40 [S markusstrasser; U].
- **Adoption.** The report is ubiquitous in press and secondary literature (dozens of GitHub notes found) [S].
- **Status: thriving (meta-report).**
- **Limitation [I].** Because it largely re-publishes developer-reported scores, it inherits their prompting, scaffolding and selection biases. It is a narrative authority, not an independent measurement.
- **Sources.**
  - https://raw.githubusercontent.com/petroslamb/autonomy-tax-enterprise-agents/HEAD/sources/raw/031_stanford_ai_index_2025_rjina.md
  - https://raw.githubusercontent.com/weaviate-tutorials/workshop-pdf-driven-rag/HEAD/data/parsed/hai_ai_index_report_2025_chapter_2-parsed-text.md
  - https://raw.githubusercontent.com/malafronte/ai-tools-lab/HEAD/anydoc/output/batch-2026-09-01/02-structured-pdf.md
  - sermakarevich/chunker `output/ai_report_2026_pdf/content/*` (code search)
  - https://raw.githubusercontent.com/markusstrasser/agent-infra/HEAD/research/2026-06-14-benchmark-leaderboard-methodology-critique.md
  - FractalK/ai-auto-wiki (code search)

### 11. EleutherAI LM Evaluation Harness (lm-eval)

- **What it is.** "a unified framework to test generative language models on a large number of different evaluation tasks", supporting "over 60 academic benchmarks with hundreds of subtasks and variants" [V README].
- **Release and venue.** Development began in 2020 [U]. The citable release is a Zenodo software record, v0.4.3 (July 2024), DOI 10.5281/zenodo.12608602. Authors: Gao, Tow, Abbasi, Biderman, Black, DiPofi, Foster, Golding, Hsu, Le Noac'h, Li, McDonell, Muennighoff, Ociepa, Phang, Reynolds, Schoelkopf, Skowron, Sutawika, Tang, Thite, Wang, Wang, Zou [V BibTeX].
  - The companion paper is "Lessons from the Trenches on Reproducible Evaluation of Language Models" (Biderman, Schoelkopf, Sutawika, Gao, Tow et al.; arXiv:2405.14782, May 2024) [S kzinmr; S emphasis10].
- **Adoption evidence.**
  - Verbatim README sentence [corrected by fact-check]: "The Language Model Evaluation Harness is the backend for 🤗 Hugging Face's popular Open LLM Leaderboard, has been used in hundreds of papers, and is used internally by dozens of organizations including NVIDIA, Cohere, BigScience, BigCode, Nous Research, and Mosaic ML." [V README]
  - New benchmarks ship as lm-eval tasks, e.g., MastermindEval, added 18 Mar 2025 [Sib user_failed_a.md].
- **Recent activity** [V README news]:
  - 2025/02: SGLang integration.
  - 2025/07: `think_end_token` for stripping reasoning traces.
  - 2025/12: CLI refactor; base package no longer depends on torch/transformers.
  - 2026/09: plugin system.
- **Status: thriving (infrastructure).**
- **Why it succeeded [I].**
  - Neutral, open-source and extensible.
  - Versioned tasks.
  - Became the de facto implementation for base-model evaluation.
  - Low marginal cost.
- **Limits [V/S].**
  - Its default implementation choices can shift scores dramatically: MMLU on LLaMA-65B scored 0.488 in the (January 2023) EleutherAI harness vs 0.636 in the original implementation and 0.637 in HELM [V] [corrected by fact-check].
  - Mistral-7B scored 47.1% in cloze format vs 51.5% in MMLU-style format [S kzinmr summary of arXiv:2405.14782]. This makes "cross-paper comparisons 'nonsensical'" [S].
  - It was historically oriented to log-likelihood evaluation of base models rather than agentic tasks [I].
- **Sources.**
  - https://raw.githubusercontent.com/EleutherAI/lm-evaluation-harness/main/README.md
  - https://raw.githubusercontent.com/kzinmr/ai-topics/HEAD/wiki/raw/papers/2024-05-23_2405.14782_lessons-from-the-trenches.md
  - https://raw.githubusercontent.com/huggingface/blog/main/open-llm-leaderboard-mmlu.md

### 12. UK AISI Inspect and Inspect Evals

- **What it is.** "a framework for large language model evaluations" from the UK AI Security Institute. It supports prompt engineering, tool use, multi-turn dialogue, model-graded evaluations and extensions, with "Over 200 pre-built evaluations" [V inspect_ai README]. It was open-sourced in May 2024 [S quantified-uncertainty/longterm-wiki; S hummbl].
- **Inspect Evals** is "A library of evaluations built using Inspect AI". It "is maintained by Generality Labs, a London-based nonprofit", and was "founded in 2024 with contributions from the UK AI Security Institute, Arcadia Impact, and the Vector Institute" [V inspect_evals README]. Examples include CyBench, SciKnowEval and GDM capabilities evals [V]. Harbor-framework evals such as Terminal-Bench 2.0 and SWE-Bench Pro are run through the separate Inspect Harbor package (meridianlabs-ai/inspect_harbor), which the README points to; they are not part of Inspect Evals itself [V] [corrected by fact-check].
- **Adoption evidence.**
  - HELM's maintenance notice recommends "Inspect AI Evals" [V].
  - Epoch runs its evaluations via Inspect [S htihle].
  - METR ported RE-Bench to Inspect, and the GAIA/Cybench/τ² implementations are used in lab and government pre-deployment testing [Sib agentic.md].
- **Status: thriving (infrastructure, especially agentic and safety evaluation).**
- **Why it succeeded [I].**
  - Government backing with open source (Apache-2.0 [S]).
  - Designed for agentic, sandboxed, tool-using evaluation from the outset.
  - A shared, logged format that makes third-party runs auditable.
- **Risk [Sib].** Harness forks can leak answers. In HAL runs of o3-mini/o1-mini, "a fork of the Inspect framework … leaked the answer to a task" [Sib agentic.md].
- **Sources.**
  - https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_ai/main/README.md
  - https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_evals/main/README.md
  - quantified-uncertainty/longterm-wiki (code search)

### 13. OpenAI simple-evals

- **What it is.** Lightweight reference implementations and a published results table for MMLU, MATH, GPQA, DROP, MGSM, HumanEval, SimpleQA, BrowseComp and HealthBench [V README].
- **Philosophy.** Zero-shot chain-of-thought, because "this prompting technique is a better reflection of the models' performance in realistic usage" than few-shot or role-play prompts [V].
- **Status: abandoned for results.** "July 2025: `simple-evals` will no longer be updated for new models or benchmark results." The repo keeps hosting reference implementations for HealthBench, BrowseComp and SimpleQA [V].
- **Saturation statement.** For MGSM and DROP: "We believe these evals are saturated for our newer models, but are reporting them for completeness" [V].
- **Last frontier row.** o3-high: MMLU 93.3, GPQA 83.4, MATH 98.1, HumanEval 88.4, MGSM 92.0, DROP 89.8, SimpleQA 48.6 [V].
- **Why it matters [I].** A lab-run "aggregator" is a transparency gesture, not a neutral index. Once the lab's own frontier saturated the classic set, maintaining it had no value to the lab, so only the lab's *new* benchmarks were kept alive.
- **Source.** https://raw.githubusercontent.com/openai/simple-evals/main/README.md

### 14. Other infrastructure and aggregators noted (not researched in depth)

- **Lighteval (Hugging Face), Evalchemy, Unitxt.** Named by HELM as recommended alternatives [V].
- **OpenCompass** (rank.opencompass.org.cn) and **Kaggle Benchmarks.** Listed as aggregators in a Sept 2026 practitioner source list [S fstandhartinger].
- **Princeton HAL (Holistic Agent Leaderboard).** See sibling `agentic.md` [Sib].
- **OpenRouter.** Exposes AA indices in its model API and publishes usage rankings [S pickai]. Usage share is a revealed-preference signal distinct from benchmark scores [I].

---

## What makes an aggregator trusted (synthesis)

Evidence from practitioner source audits (pickai, ModelHub, htihle provenance audit, markusstrasser critique) and from the aggregators' own policies [V/C/S] suggests seven trust properties. The interpretation is mine [I].

1. **The scorer is independent of the scored.**
   - Epoch, AA, Vals and Scale run models themselves. The AI Index and some leaderboards rely on self-reports [C: AI Index "operates under the assumption that the scores reported by companies are accurate"].
   - htihle's audit rates Epoch-run GPQA, MATH L5 and OTIS "✅ single evaluator, fixed harness". It rates GSM8K, MMLU and MMLU-Pro "❌ self-reported / mixed shot counts" [S].
   - One secondary critique puts it this way: "A score's trustworthiness is bounded by the discloser's transparency" [S markusstrasser].
2. **Fixed, disclosed protocol with uncertainty.**
   - Identical prompts, temperatures and scaffolds; published CIs or standard errors: AA "<±1%" [C]; Vals SE per model [C]; Epoch stderr and logs [S].
   - Why it matters: scaffold choice alone moves SWE-bench Verified "up to an 11% difference for GPT-5 and up to a 15% difference for Kimi K2 Thinking". Epoch names scaffolds (agentic evals) and API providers (model access) as "the two most impactful components"; on the provider side, "The selection of an appropriate provider has the biggest impact on model performance" [C Epoch newsletter mirror] [corrected by fact-check].
3. **Versioning and changelogs** that explain removals (AA [C]; LiveBench [V]). Unannounced or unexplained reweighting destroys trust (AA v4.1.1 accusation [S]).
4. **Contamination and saturation management.** Private or rotating items (SEAL, Vals, LiveBench), and prompt retirement of saturated components (AA, OLL v2, simple-evals). But private sets alone do not prevent saturation [V Akhtar].
5. **Open data and licence.** Epoch is CC-BY [S]; LMArena's history dataset is CC-BY-4.0 [S]. AA, Scale and Vals restrict or omit licences, which limits downstream reuse and auditing [S].
6. **Accountability to replication.** Epoch accepted and corrected an externally found aggregation error [S]. This was described as "the strongest trust signal in the survey" [S pickai].
7. **Funding and commercial neutrality.** Trust is damaged by FrontierMath–OpenAI funding [S], Meta's stake in Scale [S], and Arena selling services to ranked labs [S].

## What the indices reveal about which benchmarks are still informative (synthesis)

**Revealed-preference evidence from aggregator composition changes** [C/V/S]:

| Benchmark | Dropped or declared saturated by | When |
|---|---|---|
| ARC, HellaSwag, MMLU, TruthfulQA, WinoGrande, GSM8K | HF OLL v2 | Jun 2024 [S/Sib] |
| DROP, MGSM | OpenAI simple-evals ("saturated") | by Jul 2025 [V] |
| MATH-500, AIME 2024 | AA v2.1 | Aug 2025 [C] |
| MMLU-Pro, LiveCodeBench, AIME 2025 | AA v4.0 | Jan 2026 [C] |
| IFBench, τ²-Bench Telecom, Terminal-Bench Hard | AA v4.1 (replaced or removed) | Jun 2026 [C] |
| GPQA Diamond | AA v4.2 | Sep 2026 [C] |
| MMLU, MMMU, GPQA Diamond, AIME, SWE-bench Verified | AI Index 2026 (at or above human baseline / saturated) | Apr 2026 [C/S] |
| LiveBench | Akhtar et al. (S_index 0.99) | ICML 2026 [V] |

**Still-informative benchmarks as of Sep 2026** (in AA v4.3, the Vals Index or Epoch; low saturation per Akhtar) [C/V/S]:

- **HLE** (S_index 0.22 [V]; in AA [C]).
- **CritPt** (frontier physics) [C].
- **SciCode** [C].
- **Terminal-Bench (v2.1 → v4.0)** [C].
- **GDPval-AA v2** [C].
- **AA-LCR**, **AA-Omniscience** [C].
- **FrontierMath** (Epoch) [S].
- **SWE-Bench Pro** (Scale) [S].
- **Vals Finance Agent / Legal Research / Excel Modeling** [C].
- **METR time horizons** [S htihle].
- **ARC-AGI-2** (unsaturated per Akhtar; ARC-AGI flagged by htihle for API-exposure leakage risk) [V/S].

**Interpretation [I].** The informative frontier has moved on three axes:

- **(i) From recall to action.** Agentic, multi-step, tool-using work with verifiable end states.
- **(ii) From generic academic items to economically framed professional tasks.** GDP-weighted in Vals; GDPval, GDP.pdf and AA-Briefcase in AA.
- **(iii) From public static sets to aggregator-controlled, versioned, often private sets.** These are graded by LLM panels where outputs are open-ended.

Component half-lives inside AA are now months:

- MMLU-Pro was (re-)included in Sep 2025 and removed in Jan 2026.
- AIME 2025 was added in Aug 2025 and removed in Jan 2026.

A new benchmark should therefore be designed for **renewal**, not permanence.

---

## Cross-cutting success factors

1. **Independent execution under a fixed, disclosed protocol.** Examples: AA, Epoch, Vals, Scale, and HELM in its day. [C/V/S]
2. **Fast coverage of new frontier releases.** AA covers releases within days and lists 646 models [C]. The OLL's exclusion of closed models capped its relevance [S].
3. **Versioning and willingness to retire saturated parts.** AA's changelog [C] and OLL v2 [S] kept each product relevant beyond the life of individual benchmarks.
4. **Buyer-relevant framing.** A single headline number plus cost and speed (AA), or economic weighting (Vals), is what makes launch pages and procurement cite a source [C/S].
5. **Harness integration and low-friction reuse.** lm-eval and Inspect outlived HELM and the OLL, and HELM's own notice sends users there [V]. Benchmarks that ship as harness tasks get picked up [Sib].
6. **Transparency with uncertainty.** CIs or SEs, logs and prompts (AA, Vals, Epoch [C/S]); raw completions (HELM [C]).
7. **Openness of data under a clear licence.** This enables secondary research (OLL archive → metabench and tinyBenchmarks [Sib]; Epoch CC-BY → ECI_Bayesian [S]).
8. **Institutional backing and neutrality.** Government-backed (UK AISI Inspect), non-profit or academic (EleutherAI, Epoch), or independent company (AA) [V/S].

## Cross-cutting failure factors

1. **Saturation of included benchmarks.** It is faster than the curation cycle: "saturated in months" [C AI Index 2026]. Every aggregator has had to swap components (OLL v1 → v2; AA five removal rounds in 14 months) [S/C].
2. **Score compression at the top without ceiling.** LiveBench shows S_index 0.99 at ~79% [V]. Aggregators that average many small tests lose resolution [I].
3. **Maintenance cost and dependence on external APIs.** Examples: HELM maintenance mode [V]; the OLL [S]; LiveBench cadence slips [V].
4. **Goodhart and hill-climbing.** The OLL retired to avoid it [S]; layer-duplication "hacks" topped it [S]; Arena private variant testing [S].
5. **Implementation and scaffold sensitivity.** MMLU 0.637 vs 0.488 [V]; scaffolds move SWE-bench Verified by up to 11–15 points [C]; provider variance [C]. These undermine comparability across aggregators.
6. **Reliance on self-reported numbers.** The AI Index [C], and most per-benchmark leaderboards [S htihle].
7. **Item errors.** The AI Index 2026 headline says "error rates up to 42%" [C]. The underlying figures are precision@50 of a flagging method, not benchmark-wide invalid rates; GSM8K's estimated error rate is ~5% (Truong et al. 2025) [corrected by fact-check]. The DROP scoring bug is another example [Sib].
8. **Conflicts of interest and opacity.** Examples: funding (FrontierMath) [S]; ownership (Scale/Meta) [S]; selling services to ranked labs (Arena) [S]; undisclosed reweighting or judge choices (AA) [S]; private sets nobody can audit [I].
9. **LLM-judge dependence.** Grader models change on deprecation (AA upgraded the HLE, AA-LCR and AA-Omniscience graders to GPT-5.6 Luna in v4.1.1 [C]; the claim of "four" grader swaps in 2026 was not verified by fact-check), and judges add bias [S].
10. **Licence and data-access fragility.** Missing ToS (Vals), restrictive redistribution (AA), SPA-embedded data (LiveBench, Scale) [S]. These block third-party auditing and aggregation.
11. **Lab-run aggregators end when the lab's interest ends.** simple-evals was frozen in July 2025 [V].

## Implications for the new benchmark (feeds Phase 2) [I]

- Ship as **Inspect and lm-eval tasks** with a fixed reference protocol and logs, so Epoch, AA, Vals and similar evaluators can run it independently.
- Use an **item generator or renewal process** (fresh draws per evaluation window). Report per-window SE, and aim for n large enough that top-model gaps exceed SE∆ (the Akhtar S_index logic).
- Prefer **programmatic verification** over LLM judges. If judges are unavoidable, pin and version them and publish judge-agreement statistics.
- Include **anchor items and shared models** so scores can be linked to the ECI scale, and report **discriminant validity against ECI**.
- Publish **data under CC-BY**, a changelog, and a component-retirement policy from day one.
- Declare funding and conflicts. Keep the maintaining body neutral.

---

## Claims ledger

1. HELM (Liang et al.) was published in TMLR 2023 with "Featured Certification, Expert Certification"; the official BibTeX lists 50 authors.
   - Source: https://raw.githubusercontent.com/stanford-crfm/helm/HEAD/README.md
   - Confidence: **High**
2. The HELM abstract reports:
   - 7 metrics on 16 core scenarios (87.5% of the time);
   - 26 targeted scenarios;
   - 30 models on 42 scenarios;
   - coverage improved from 17.9% to 96.0%.
   - Sources: AkihikoWatanabe/paper_notes `agent_docs/TMLR.xml` (code search); kube-dojo `docs/research/ai-history/chapters/ch-66-benchmark-wars/sources.md` (code search)
   - Confidence: **High** (two independent mirrors of the abstract)
3. HELM entered maintenance mode on 1 June 2026. No new evaluations will be added to its leaderboards. It recommends Evalchemy, Inspect AI Evals, Lighteval, LM Evaluation Harness and Unitxt.
   - Sources: https://raw.githubusercontent.com/stanford-crfm/helm/HEAD/docs/maintenance_mode.md ; https://raw.githubusercontent.com/stanford-crfm/helm/HEAD/README.md
   - Confidence: **High**
4. Hugging Face's 23 June 2023 blog found LLaMA-65B MMLU = 0.637 (HELM), 0.636 (original) and 0.488 (EleutherAI harness), and concluded that "Evaluations are strongly tied to their implementations".
   - Sources: https://raw.githubusercontent.com/huggingface/blog/main/open-llm-leaderboard-mmlu.md ; huggingface/blog `_blog.yml`
   - Confidence: **High**
5. Open LLM Leaderboard v2 (26 June 2024) switched to MMLU-Pro, GPQA, MuSR, MATH Level 5, IFEval and BBH. The reasons given were saturation, contamination and errors. Scores are normalised between the random baseline and 100.
   - Sources: https://raw.githubusercontent.com/sasilver75/obsidian/HEAD/Open%20LLM%20Leaderboard%20V2.md ; turbobeest/modelspec `benchmarks/musr.md` (code search)
   - Confidence: **Medium-High** (secondary summaries of the HF blog)
6. The Open LLM Leaderboard was retired on 13 March 2025 (HF discussion #1135). The stated reasons: model capabilities changed (reasoning, LM assistants), the leaderboard was "slowly becoming obsolete", and it "could encourage people to hill climb irrelevant directions".
   - Sources: https://raw.githubusercontent.com/niftymonkey/pickai/main/design/research/free-benchmark-sources.md ; https://raw.githubusercontent.com/niftymonkey/pickai/main/design/research/benchmark-adoption.md ; aledlie/aledlie.github.io `_posts/2026-08-11-stale-marquee-claims.md`
   - Confidence: **Medium-High** (consistent quotes in independent secondary sources; primary page blocked)
7. More than 13K models were evaluated on the OLL over its life.
   - Source: sibling `knowledge_exams.md` (HF collection page)
   - Confidence: **Medium** (not re-verified)
8. lm-evaluation-harness supports "over 60 academic benchmarks with hundreds of subtasks and variants". It is the backend of the HF Open LLM Leaderboard and is used internally by NVIDIA, Cohere, BigScience, BigCode, Nous Research and Mosaic ML. Its Zenodo citation is v0.4.3 (July 2024), DOI 10.5281/zenodo.12608602.
   - Source: https://raw.githubusercontent.com/EleutherAI/lm-evaluation-harness/main/README.md
   - Confidence: **High**
9. "Lessons from the Trenches on Reproducible Evaluation of Language Models" (Biderman et al., arXiv:2405.14782, May 2024) reports Mistral-7B at 47.1% (cloze) vs 51.5% (MMLU-style).
   - Sources: https://raw.githubusercontent.com/kzinmr/ai-topics/HEAD/wiki/raw/papers/2024-05-23_2405.14782_lessons-from-the-trenches.md ; emphasis10/AI-paper-digest (code search)
   - Confidence: **Medium** (secondary summary)
10. Inspect is a UK AI Security Institute framework with "over 200 pre-built evaluations". Inspect Evals is maintained by Generality Labs (London nonprofit) and was founded in 2024 with UK AISI, Arcadia Impact and the Vector Institute.
    - Sources: https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_ai/main/README.md ; https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_evals/main/README.md
    - Confidence: **High**
11. Inspect was open-sourced in May 2024.
    - Source: quantified-uncertainty/longterm-wiki `content/docs/knowledge-base/responses/scalable-eval-approaches.mdx` (code search)
    - Confidence: **Medium**
12. OpenAI simple-evals: "July 2025: simple-evals will no longer be updated for new models or benchmark results". MGSM and DROP are described as "saturated for our newer models". o3-high row: MMLU 93.3, GPQA 83.4, MATH 98.1, HumanEval 88.4, MGSM 92.0, DROP 89.8, SimpleQA 48.6.
    - Source: https://raw.githubusercontent.com/openai/simple-evals/main/README.md
    - Confidence: **High**
13. LiveBench:
    - ICLR 2025 Spotlight; 18 tasks in 6 categories; objective ground truth with no LLM judge;
    - README claims "new questions monthly";
    - launched 2024-06-12, and reached 1,000 questions after 2024-07-26.
    - Sources: https://raw.githubusercontent.com/LiveBench/LiveBench/main/README.md ; https://raw.githubusercontent.com/LiveBench/LiveBench/main/changelog.md
    - Confidence: **High**
14. LiveBench's code lists 11 releases: 2024-06-24, 2024-07-26, 2024-08-31, 2024-11-25, 2025-04-02, 2025-04-25, 2025-05-30, 2025-11-25, 2025-12-23, 2026-01-08 and 2026-06-25.
    - Source: LiveBench/LiveBench `livebench/common.py` (GitHub code search)
    - Confidence: **High**
15. Akhtar et al. (ICML 2026, PMLR 306):
    - 29 of 60 benchmarks show high or very high saturation (S_index ≥ 0.7), 14 of them very high;
    - LiveBench S_index 0.9888 (top range 1.09, SE∆ 0.1028, ~79%);
    - LiveCodeBench 0.7691;
    - HLE 0.2198;
    - public (56) vs private (4) benchmarks show no significant difference: "Hiding test data does not appear to prevent saturation once benchmarks are widely adopted".
    - Source: https://raw.githubusercontent.com/mlresearch/v306/main/assets/akhtar26a/akhtar26a.pdf
    - Confidence: **High**
16. Akhtar et al. note that the leaderboards they rely on "may exist for a benchmark, often differing in evaluation setups" and that "Many leaderboards are not regularly updated and may omit newly released models".
    - Source: same PDF
    - Confidence: **High**
17. ECI fits "performance = sigmoid(discriminability * (capability − difficulty))", anchored at Claude 3.5 Sonnet = 130 and GPT-5 = 150. The paper is "A Rosetta Stone for AI Benchmarks" (Ho, Denain, Atanasov, Albanie, Shah; arXiv:2512.00193).
    - Source: https://raw.githubusercontent.com/epoch-research/eci-public/main/README.md
    - Confidence: **High**
18. ECI covers ~37 benchmarks and 867 rows (Aug 2026 data).
    - Sources: https://raw.githubusercontent.com/niftymonkey/pickai/main/design/research/benchmark-adoption.md ; Dylancouzon/AIE-talk (code search, says "40+")
    - Confidence: **Low-Medium**
19. Epoch's newsletter found that switching scaffolds changes SWE-bench Verified by "up to an 11% difference for GPT-5 and up to a 15% difference for Kimi K2 Thinking". GPQA Diamond averages across settings (gpt-oss, high reasoning; 198 questions) ranged from 74% to 80%, but "these differences were not statistically significant". Scaffolds and API providers are named as the two most impactful components; "The selection of an appropriate provider has the biggest impact on model performance" [corrected by fact-check]. The post is by Florian Brand and Jean-Stanislas Denain (per secondary), published 23–24 Dec 2025.
    - Source: https://raw.githubusercontent.com/shakir-fattani/ai-updates/HEAD/epochai.substack.com/why-benchmarking-is-hard/content.md
    - Confidence: **Medium-High** (mirror)
20. AA Intelligence Index changelog:
    - v2.1 (Aug 2025) removed MATH-500 and AIME 2024;
    - v4.0 (Jan 2026) removed MMLU-Pro, LiveCodeBench and AIME 2025, added GDPval-AA, AA-Omniscience and CritPt, and set 4 categories at 25%;
    - v4.1 (Jun–Aug 2026) removed IFBench and replaced Terminal-Bench Hard and τ²-Bench Telecom;
    - v4.2 (Sep 2026) removed GPQA Diamond;
    - v4.3 has 10 evals weighted Agents 30 / Coding 20 / General 30 / Science 20.
    - Sources: https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/HEAD/ops/rebuild-2026-09/evidence/phase-04/sources/aa-1ea3e75f96c3.txt ; https://raw.githubusercontent.com/MaxiZm/actualanalysis/HEAD/docs/audits/coverage-expansion-2026-09-06/artificial-analysis.md
    - Confidence: **Medium-High** (captured primary page, verbatim via code-search fragments, plus a second independent capture; the MaxiZm "audit" is AI-generated) [corrected by fact-check]
21. AA states a 95% CI for the Intelligence Index of less than ±1%, evaluates zero-shot under identical conditions, and lists 646 models.
    - Source: same capture, plus `aa-e3caaea65cc5.txt` (code search)
    - Confidence: **Medium-High**
22. About 33% of AA Intelligence Index weight flows through LLM judges.
    - Source: https://raw.githubusercontent.com/markusstrasser/agent-infra/HEAD/research/2026-06-14-benchmark-leaderboard-methodology-critique.md
    - Confidence: **Low-Medium** (secondary; depends on version)
23. Vals Index v2 (updated 15 Sep 2026) weights finance, coding and legal agentic tasks by US-GDP share. It aggregates "five private and two public benchmarks" and publishes an SE per model. Top scores: Claude Fable 5.1 68.83%, Claude Opus 5 67.21%, GPT-6 Astra 66.61%.
    - Source: https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/HEAD/data/raw/benchmarks/daily-evidence/2026-09-18T12-58-20-378Z/gauntlet/protocol-vals-index-finance-agent-2/packet-r1.md
    - Confidence: **Medium** (captured page)
24. Scale introduced SEAL Leaderboards around late May 2024, "with private datasets and paid annotators".
    - Source: smol-ai/ainews-web-2025 `buttondown-emails/24-05-30-ainews-contextual-position-encoding-cope.md` (code search)
    - Confidence: **Medium** (newsletter)
25. Meta took a 49% stake in Scale AI, which critics argue compromised its neutrality.
    - Source: guzus/ai-research-arm `research/generative/2026-06-22T061332--frontier-ai-data-supply-chain.ara.md` (code search)
    - Confidence: **Low-Medium** (secondary analysis)
26. AI Index 2025:
    - MMMU, GPQA and SWE-bench rose 18.8, 48.9 and 67.3 pp in one year;
    - HLE top score 8.80%, FrontierMath 2%, BigCodeBench 35.5% vs a human 97%;
    - top vs 10th model gap fell from 11.9% to 5.4%;
    - the Index assumes company-reported scores are "accurate and factual".
    - Sources: https://raw.githubusercontent.com/petroslamb/autonomy-tax-enterprise-agents/HEAD/sources/raw/031_stanford_ai_index_2025_rjina.md ; https://raw.githubusercontent.com/weaviate-tutorials/workshop-pdf-driven-rag/HEAD/data/parsed/hai_ai_index_report_2025_chapter_2-parsed-text.md
    - Confidence: **Medium-High** (captured page and parsed PDF)
27. AI Index 2026:
    - "Evaluations intended to be challenging for years are saturated in months";
    - "error rates up to 42% on widely used evaluations", with "invalid question rates ranging from 2% on MMLU Math to 42% on GSM8K" (AI Index wording). These are precision@50 values of a flagging method, not benchmark-wide invalid rates [corrected by fact-check];
    - "4 companies now clustered within 25 Elo points";
    - agents "still fail roughly one in three attempts".
    - Sources: https://raw.githubusercontent.com/malafronte/ai-tools-lab/HEAD/anydoc/output/batch-2026-09-01/02-structured-pdf.md ; sermakarevich/chunker `output/ai_report_2026_pdf/content/L1/ai-index-2026-performance-benchmarking.md` (code search); tanioklyce-dev/robot_research (code search)
    - Confidence: **Medium** (PDF extractions in third-party repos)
28. AI Index 2026 reports HLE +30 pp in one year.
    - Sources: kzinmr/ai-topics `wiki/raw/articles/2026-04-14_stanford-ai-index-report-2026-technical-performance.md` (code search); markusstrasser critique; verbatim "Frontier models gained 30 percentage points in a single year on Humanity's Last Exam" in malafronte/ai-tools-lab and malafronte/mineru-lab PDF extractions
    - Confidence: **Medium-High** (upgraded by fact-check)
29. Leaderboard Illusion: Meta privately tested 27 variants before Llama 4; Google received 19.2% and OpenAI 20.4% of Arena data.
    - Sources: https://raw.githubusercontent.com/niftymonkey/pickai/main/design/research/benchmark-adoption.md ; markusstrasser critique; rasynai/MarigoldBench (code search)
    - Confidence: **Medium** (secondary quotes; primary in sibling `arenas_preference.md`)
30. The htihle provenance audit rates Epoch-run GPQA Diamond, MATH L5 and OTIS Mock AIME as independent (single evaluator, fixed harness). It rates GSM8K, MMLU and MMLU-Pro leaderboard numbers as largely self-reported, and flags FrontierMath's OpenAI funding.
    - Source: https://raw.githubusercontent.com/htihle/open_closed_gap/HEAD/provenance_audit/APPENDIX.md
    - Confidence: **Low-Medium** (secondary; the per-benchmark audit files are self-described as "Independent Opus 4.7 web-research audit, 2026-05-26", i.e. LLM-generated) [corrected by fact-check]
31. An external replication found an ECI aggregation error ("24/144 of the sets contain LLMs with different release dates"), which Epoch acknowledged.
    - Source: https://raw.githubusercontent.com/niftymonkey/pickai/main/design/research/benchmark-adoption.md
    - Confidence: **Low-Medium**
32. HELM Capabilities release v1.15.0 is dated 2025-11-24 (68 models) and was described as nine months stale in Aug 2026.
    - Source: https://raw.githubusercontent.com/niftymonkey/pickai/main/design/research/free-benchmark-sources.md
    - Confidence: **Medium**

---

## References

The machine-readable version is `research/refs/aggregators_indices.json`. "Seen at" gives where I actually saw each item this session.

1. Liang, P., Bommasani, R., Lee, T., et al. (2023). *Holistic Evaluation of Language Models.* TMLR (Featured and Expert Certification). arXiv:2211.09110. https://openreview.net/forum?id=iO4LZibEqW
   - Seen at: stanford-crfm/helm README; abstract mirror in AkihikoWatanabe/paper_notes.
2. Stanford CRFM (2026). *HELM Maintenance Mode Policy.* https://crfm-helm.readthedocs.io/en/latest/maintenance_mode/
   - Seen at: https://raw.githubusercontent.com/stanford-crfm/helm/HEAD/docs/maintenance_mode.md
3. clefourrier, SaylorTwift, slippylolo, thomwolf (HF handles as listed in the post) (2023-06-23). *What's going on with the Open LLM Leaderboard?* Hugging Face blog. https://huggingface.co/blog/open-llm-leaderboard-mmlu
   - Seen at: huggingface/blog raw.
   - Note: the real-name mapping of the handles is **[U]**, except that "clefourrier" is commonly Clémentine Fourrier.
4. Hugging Face (2024-06-26). *Open-LLM performances are plateauing, let's make the leaderboard steep again* (Open LLM Leaderboard v2). https://huggingface.co/spaces/open-llm-leaderboard/blog. The exact title (with the "Open-LLM" prefix) comes from the captured Space HTML [corrected by fact-check].
   - Seen at: sasilver75/obsidian notes (secondary).
5. Fourrier, C. (2025-03-13). *It's been a wild ride, folks :) (end of the Open LLM Leaderboard)*, HF discussion #1135. https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard/discussions/1135
   - Seen at: niftymonkey/pickai notes; aledlie blog (secondary quotes).
6. White, C., Dooley, S., Roberts, M., Pal, A., Feuer, B., Jain, S., Shwartz-Ziv, R., Jain, N., Saifullah, K., Dey, S., Shubh-Agrawal, Sandha, S. S., Naidu, S. V., Hegde, C., LeCun, Y., Goldstein, T., Neiswanger, W., Goldblum, M. (2025). *LiveBench: A Challenging, Contamination-Free LLM Benchmark.* ICLR 2025 (Spotlight). arXiv:2406.19314.
   - Seen at: LiveBench README.
7. LiveBench team. *LiveBench repository: changelog.md and livebench/common.py.* https://github.com/LiveBench/LiveBench
   - Seen at: raw changelog; code search.
8. Akhtar, M., Reuel, A., Soni, P., et al. (2026). *When AI Benchmarks Plateau: A Systematic Study of Benchmark Saturation.* ICML 2026, PMLR 306.
   - Seen at: https://raw.githubusercontent.com/mlresearch/v306/main/assets/akhtar26a/akhtar26a.pdf
   - arXiv:2602.16763, corroborated by fact-check (duanyytop/agents-radar HN digests, Aug 2026, link this exact title to arxiv.org/abs/2602.16763).
9. Ho, A., Denain, J.-S., Atanasov, D., Albanie, S., Shah, R. (2025). *A Rosetta Stone for AI Benchmarks.* arXiv:2512.00193.
   - Seen at: epoch-research/eci-public README.
10. Epoch AI (2026). *eci-public: Epoch Capabilities Index* (GitHub). https://github.com/epoch-research/eci-public
11. Epoch AI (2025). *benchmark-stitching* (GitHub). https://github.com/epoch-research/benchmark-stitching
12. Brand, F., Denain, J.-S. (Epoch AI) (23–24 Dec 2025). *Why benchmarking is hard.* Gradient Updates newsletter. https://epoch.ai/gradient-updates/why-benchmarking-is-hard. The date comes from the mirror's meta.yaml (substack publish-date 2025-12-24) and kzinmr ("Dec 23, 2025"); the authors are per kzinmr (secondary) [corrected by fact-check].
    - Seen at: mirror in shakir-fattani/ai-updates.
13. Epoch AI. *AI Benchmarking Hub.* https://epoch.ai/benchmarks
    - Seen at: references in the Epoch newsletter mirror and AINews.
14. Artificial Analysis (2026). *Intelligence Benchmarking methodology* (Intelligence Index v4.3 and changelog). https://artificialanalysis.ai/methodology/intelligence-benchmarking
    - Seen at: capture in fstandhartinger/model-market-comparison.
15. MaxiZm/actualanalysis (2026-09-06). *Artificial Analysis coverage/version audit* (GitHub; secondary; the file names a "Gemini Agent" as auditor, so it is AI-generated) [corrected by fact-check].
16. Vals AI (2026-09-15). *Vals Index (Version 2).* https://www.vals.ai/benchmarks/vals_index
    - Seen at: capture in fstandhartinger/model-market-comparison.
17. Scale AI (2024). *SEAL Leaderboards* (now Scale Labs). https://scale.com/leaderboard
    - Seen at: AINews 2024-05-30 (secondary); pickai; ModelHub.
18. Deng, X., Da, J., Pan, E., He, Y. Y., Ide, C., Garg, K., Lauffer, N., et al. (2025). *SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?* arXiv:2509.16941 (Scale AI; published 2025-09-21) [corrected by fact-check].
    - Seen at: razzant/ouroboros METHODOLOGY.md.
19. Singh, S., et al. (2025). *The Leaderboard Illusion.* arXiv:2504.20879 (NeurIPS 2025 D&B per secondary source).
    - Seen at: pickai; markusstrasser; turbobeest (secondary).
20. Stanford HAI (2025). *The 2025 AI Index Report.* https://hai.stanford.edu/ai-index/2025-ai-index-report
    - Seen at: petroslamb capture; weaviate-tutorials parsed chapter 2.
21. Stanford HAI (2026). *The 2026 AI Index Report.* https://hai.stanford.edu/ai-index/2026-ai-index-report
    - Seen at: malafronte PDF extraction; sermakarevich chunks; shawkatdidar brief.
22. Gao, L., Tow, J., Abbasi, B., Biderman, S., et al. (2024). *The Language Model Evaluation Harness* (v0.4.3). Zenodo. doi:10.5281/zenodo.12608602
    - Seen at: lm-eval README.
23. Biderman, S., Schoelkopf, H., Sutawika, L., Gao, L., Tow, J., et al. (2024). *Lessons from the Trenches on Reproducible Evaluation of Language Models.* arXiv:2405.14782.
    - Seen at: kzinmr/ai-topics; emphasis10/AI-paper-digest (secondary).
24. UK AI Security Institute (2024). *Inspect* (inspect_ai). https://github.com/UKGovernmentBEIS/inspect_ai
25. Generality Labs, UK AISI, Arcadia Impact, Vector Institute (2024–). *Inspect Evals.* https://github.com/UKGovernmentBEIS/inspect_evals
26. OpenAI (2024–2025). *simple-evals.* https://github.com/openai/simple-evals
27. niftymonkey/pickai (2026). *free-benchmark-sources.md* and *benchmark-adoption.md* (practitioner research notes; secondary).
28. Ihle, H. T. (htihle) (2026). *open_closed_gap: provenance audit appendix* (GitHub; secondary, LLM-generated web-research audit in Ihle's repo) [corrected by fact-check].
29. DDamianZR/ModelHub (2026). *SOURCES.md* (practitioner source assessment; secondary).
30. markusstrasser/agent-infra (2026-06-14). *Benchmark & leaderboard methodology critique* (secondary).
31. aledlie (2026-08-11). *Stale marquee claims* (blog post; secondary).
32. smol-ai AINews (2024-05-30; 2025-05-07; 2025-05-30). Newsletter archive issues (secondary).
33. Mozilla (2026-07). *The State of Open Source AI* v1.0.1. https://stateofopensource.ai
    - Seen at: dgirard/fiches-veille summary (secondary).
    - Fact-check: the report's existence is confirmed (V1.0 July 2026, CTO letter by Raffi Krikorian; a later v1.1 exists). The AA and ECI figures quoted from it were NOT verified against the report.
34. linkofrivia (2026). *ECI_Bayesian* (GitHub; secondary re-analysis).
35. sasilver75 (2024). *Open LLM Leaderboard V2* (Obsidian notes; secondary).

---

## Verification log

Adversarial fact-check run on 2026-09-29 by a separate agent.

**Method and constraints.** The session-wide WebSearch budget was already exhausted (every WebSearch call returned "used its web search budget (200 of 200)"). A broad curl probe of blocked domains was also denied. Independent checking therefore used three channels:

1. **Re-fetching primary files** from raw.githubusercontent.com with WebFetch.
2. **Local text extraction** of the Akhtar et al. PMLR PDF, using pypdf.
3. **GitHub code search**, which returns *verbatim* text fragments, to find independent mirrors, captures and citations.

**Warning for downstream agents.** WebFetch's summariser produced a *fabricated* AA changelog when asked to summarise the long capture `aa-1ea3e75f96c3.txt`. It also miscounted the HELM authors as 48; the true count is 50. Numbers in this log were taken only from verbatim fragments, the verbatim BibTeX, or the extracted PDF text.

### Claim verdicts

| ID | Verdict | Evidence (independent where possible) |
|---|---|---|
| C1 HELM maintenance mode | **Confirmed** | Re-fetched `docs/maintenance_mode.md` and README: "HELM entered maintenance mode on June 1, 2026"; "no new evaluations will be added to the HELM leaderboards"; the maintainers can no longer actively support research collaborations; external APIs "may change in reverse-incompatible ways". Recommended: Evalchemy, Inspect AI Evals, Lighteval, "LLM Evaluation Harness" (sic), Unitxt. |
| C2 HELM design numbers | **Confirmed** | The official BibTeX author field counts exactly 50 names; TMLR 2023 with "Featured Certification, Expert Certification". TMLR 2023 is independently listed in the Akhtar et al. bibliography. Abstract numbers (7 metrics; 16 core scenarios, 87.5%; 7 targeted evaluations on 26 targeted scenarios; 30 models on all 42 scenarios; 17.9% → 96.0%) appear verbatim in the skothr/llm-research abstract excerpt and in thorbenlouw notes (arXiv 2211.09110v2). |
| C3 OLL retirement and v2 | **Confirmed (secondary level; primary HF pages blocked)** | Date 13 Mar 2025 and discussion #1135 corroborated by ≥5 independent repos (tatdt622989 blog, sbluemin/fleet-harness, aledlie, gperdrizet, SalvatMigliaccio). The "hill climb irrelevant directions" quote also appears in scottblydotcom/hermia and rasynai/MarigoldBench. The v2 task list, the June 2024 launch and the saturation/contamination/errors rationale are corroborated independently (scottblydotcom, AutoTrustAI survey, sasilver75). The exact v2 blog title is "Open-LLM performances are plateauing, let's make the leaderboard steep again" (captured Space HTML). |
| C4 MMLU implementation gap | **Confirmed** | Raw blog: original 0.636, HELM 0.637, "EleutherAI Harness (January 2023)" 0.488; "Evaluations are strongly tied to their implementations"; `_blog.yml` date "June 23, 2023". The dossier body elsewhere mislabelled 0.637 as the "original" value; fixed inline. |
| C5 simple-evals freeze | **Confirmed** | Re-fetched README: "July 2025: `simple-evals` will no longer be updated for new models or benchmark results"; MGSM/DROP "saturated for our newer models"; it continues to host HealthBench, BrowseComp and SimpleQA; o3-high row values match. |
| C6 LiveBench cadence | **Confirmed** | README: "releasing new questions monthly", "18 diverse tasks across 6 categories", no LLM judge, ICLR 2025 Spotlight. `common.py` `LIVE_BENCH_RELEASES` has exactly the 11 dates listed, none between 2026-01-08 and 2026-06-25. Added: changelog stops at 2026-01-08; Inspect Evals README says it "completely refreshes every 6 months". |
| C7 Akhtar et al. saturation | **Confirmed** | Extracted PDF text: "Of the 60 benchmarks analyzed, 29 exhibit high or very high saturation (Sindex≥0.7), out of which 14 fall into the very high category". Table 7: LiveBench n = 1000, range 1.09, SE∆ 0.1028, S_index 0.9888 (~79%); LiveCodeBench 0.7691; HLE 0.2198. Top-k default k = 5. "Public (N=56) and private (N=4) … Hiding test data does not appear to prevent saturation once benchmarks are widely adopted". PMLR 306, ICML 2026 Seoul. arXiv:2602.16763 is independently corroborated. |
| C8 ECI | **Confirmed, with a nuance** | eci-public README: "performance = sigmoid(discriminability * (capability - difficulty))"; anchors Claude 3.5 Sonnet = 130 and GPT-5 = 150. Paper authors and arXiv:2512.00193 are independently confirmed (memgrafter digest; arXiv daily listing for 2025-12-02). Nuance: the 130/150 anchors are the ECI product's convention, while the paper's identifiability anchor is a fixed benchmark. |
| C9 AA changelog | **Confirmed (captured copy)** | Verbatim code-search fragments of the capture: v2.1 (5–6 Aug 2025) "Removed MATH-500 / Removed AIME 2024"; v4.0 "January 2026 … Removed MMLU-Pro, LiveCodeBench, AIME 2025 … Agents (25%), Coding (25%), General (25%), Scientific Reasoning (25%)"; v4.1 "June 2026—August 2026 … Removed IFBench"; v4.2 "September 2026 … Removed GPQA Diamond"; v4.3 "incorporates 10 evaluations"; weights 10/15/5/10/10/5/10+5/10/10/10, which sums to 30/20/30/20; "95% confidence interval … of less than ±1%". A second, independent capture (dingkwang, Aug 2026: v4.1.1, 9 evals incl. GPQA, 34/24/24/18) is consistent. |
| C10 Epoch "Why benchmarking is hard" | **Corrected** | The quotes are right ("up to an 11% difference for GPT-5 and up to a 15% difference for Kimi K2 Thinking"; 74–80%, not significant). Corrections: (a) the GPQA range is for **gpt-oss** (198 questions); (b) Epoch names **scaffolds and API providers as "the two most impactful components"**, and the provider is said to have "the biggest impact on model performance" on the model-access side, so "API providers were the largest source of variance" overstates it; (c) Epoch writes "%" where secondary sources say "points". Date is 23–24 Dec 2025; authors are Florian Brand and Jean-Stanislas Denain (per secondary). Several independent repos cite the same 11/15 figures. |
| C11 AI Index 2025 | **Confirmed** | Verbatim across ≥5 independent PDF extractions: "scores rose by 18.8, 48.9, and 67.3 percentage points" (SWE-bench 4.4% → 71.7%); HLE 8.80%; FrontierMath 2%; BigCodeBench 35.5% vs human 97%; "operates under the assumption that the scores reported by companies are accurate and factual". Clarified inline that the 11.9% → 5.4% gap is the Chatbot Arena Elo gap between the top and 10th model. |
| C12 AI Index 2026 | **Corrected (interpretation)** | All four quotes are verbatim in several independent OCR/PDF extractions, including "A review found invalid question rates ranging from 2% on MMLU Math to 42% on GSM8K". However, the underlying source (Truong et al. 2025, *Fantastic Bugs…*, NeurIPS 2025, arXiv:2511.16842) reports **precision@50** = TP(50)/50 among *flagged* items, not benchmark-wide invalid rates; the same authors estimate GSM8K's error rate at ~5% (88 questions). The dossier must not present "42% of GSM8K is invalid" as fact. Also confirmed: "Frontier models gained 30 percentage points in a single year on Humanity's Last Exam", and the March 2026 Arena Elos Anthropic 1,503 / xAI 1,495 / Google 1,494 / OpenAI 1,481. |
| C13 Harness infrastructure | **Confirmed** | lm-eval README: "Over 60 standard academic benchmarks … hundreds of subtasks and variants"; the BibTeX is Zenodo v0.4.3, month 07, 2024, doi 10.5281/zenodo.12608602. The verbatim usage sentence is "…is the backend for 🤗 Hugging Face's popular Open LLM Leaderboard, has been used in hundreds of papers, and is used internally by dozens of organizations including NVIDIA, Cohere, BigScience, BigCode, Nous Research, and Mosaic ML"; the dossier's paraphrased quote was fixed inline. Inspect: "over 200 pre-built evaluations"; Inspect Evals is "maintained by Generality Labs, a London-based nonprofit". Harbor evals (Terminal-Bench 2.0, SWE-Bench Pro) run via the separate Inspect Harbor package; fixed inline. |
| C14 Vals Index v2 | **Corrected (provenance)** | Verbatim in captures: "Updated 9/15/2026, Version 2"; "A single measure of AI's potential economic impact…weighted by each sector's share of U.S. GDP"; "aggregates five private and two public benchmarks" (7 components listed). But the "standard error per model" and "three runs" details come from the capturing repo's registry notes, which its own verifier flagged as **absent from the captured page** ("missing_evidence"). Independent partial support comes from maxim-saplin/llm_chess, which lists an upstream `stderr` of the index score for an earlier version. Downgraded to [S]. All captures come from a single repo (fstandhartinger), and no independent capture of the v2 text was found. |

**Counts.** 11 confirmed, 3 corrected, 0 refuted, 0 unverifiable.

### Other corrections made inline (outside C1–C14)

- **htihle provenance audit.** Described as a "secondary expert audit". Its per-benchmark files are self-labelled "Independent Opus 4.7 web-research audit, 2026-05-26", so it is LLM-generated; confidence downgraded. On FrontierMath it states only that OpenAI access "would inflate closed-side scores" (conditional), not that it does.
- **MaxiZm "independent audit" of AA.** Self-described as written by a "Gemini Agent", i.e. AI-generated.
- **AA Agents weight.** The summary implied Terminal-Bench counts toward "Agents"; it is in Coding (20%).
- **AA grader swaps.** "AA swapped graders four times in 2026" was not verified; only the v4.1.1 grader upgrade was confirmed.
- **LiveBench launch score.** Filled in: the arXiv abstract reports top models below 65% at launch.
- **HLE +30 pp.** Upgraded to Medium-High, since it is verbatim in the AI Index 2026 highlights.
- **Reference metadata.** Fixed or filled: OLL v2 blog title; Akhtar arXiv ID; Epoch newsletter date and authors; SWE-Bench Pro title and authors; Mozilla report URL and existence.

### Reference-check summary

- **Checked:** 34 of 34 JSON entries; none skipped.
- **Existence:** all 34 marked `verified: true`, confirmed at primary level where a primary was reachable, otherwise via independent secondary copies.
- **Problematic entries (9):**
  - **Wrong or missing metadata** (fixed in JSON): `hf2024ollv2` (title), `akhtar2026plateau` (ID, now arXiv:2602.16763), `epochWhyBenchHard` (year, authors, venue, URL), `swebenchpro2025` (title, authors).
  - **Mischaracterised or over-claimed:**
    - `ihle2026provenance`: LLM-generated audit.
    - `maxizm2026aaaudit`: AI-generated.
    - `vals2026index`: SE claim not in the capture.
    - `hai2026aiindex`: precision@50 misread as an invalid-item rate.
    - `mozilla2026openai`: quoted scores unverified against the report.
- **Not re-verified:** the Leaderboard Illusion numbers (27 variants; 19.2%/20.4%; 112%), because code search was rate-limited. They are deferred to the sibling `arenas_preference.md`.
- **Misattribution found in the wild:** at least one secondary repo attributes "A Rosetta Stone for AI Benchmarks" to "Sevilla et al."; the correct authors are Ho, Denain, Atanasov, Albanie and Shah.

### Key sources used by the fact-check

- **Primary files** (raw.githubusercontent.com):
  - stanford-crfm/helm `README.md` and `docs/maintenance_mode.md`
  - openai/simple-evals `README.md`
  - LiveBench/LiveBench `README.md`, `changelog.md` and `livebench/common.py`
  - epoch-research/eci-public and benchmark-stitching READMEs
  - EleutherAI/lm-evaluation-harness `README.md`
  - UKGovernmentBEIS/inspect_ai and inspect_evals READMEs
  - huggingface/blog `open-llm-leaderboard-mmlu.md` and `_blog.yml`
  - mlresearch/v306 `akhtar26a.pdf` (text extracted locally)
- **Captures and extractions:**
  - fstandhartinger/model-market-comparison: AA and Vals captures (code-search fragments)
  - dingkwang/agent-eval-course `docs/aa-intelligence-benchmarking-methodology.md`
  - malafronte/ai-tools-lab and malafronte/mineru-lab: AI Index 2026 extractions
  - weaviate-tutorials, Panteve, aichaoukdour and Juanesillo: AI Index 2025 extractions
  - shakir-fattani/ai-updates Epoch mirror (`content.md`, `meta.yaml`)
- **Independent corroboration:**
  - memgrafter/research-digests (2512.00193, 2406.19314)
  - duanyytop/agents-radar (2602.16763)
  - ATOM00blue/machine-learning-library (2509.16941)
  - StanfordVL/sail-blog-new-post (Truong et al., precision@k definition)
  - aims-foundations/fantastic-bugs (NeurIPS 2025 BibTeX)
  - htihle/htihle.github.io and htihle/open_closed_gap `provenance_audit/weirdml.md`
  - maxim-saplin/llm_chess (Vals stderr)
  - sasilver75/obsidian (SEAL launch 29 May 2024)
  - kzinmr/ai-topics (Epoch post authors and date)

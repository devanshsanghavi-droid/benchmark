# Other low-adoption and abandoned benchmarks, and how concentrated benchmark usage is

Research dossier, compiled 2026-09-29. It covers:

- game-based LLM benchmarks and whether any of them achieved lasting adoption;
- non-game benchmarks and leaderboards that were retired, frozen or abandoned;
- the empirical meta-literature on benchmark usage concentration, saturation and failure.

Siblings cover related ground. The user's 10 named benchmarks are in `user_failed_a.md` and `user_failed_b.md`. Exam-style benchmarks, including MMLU, GPQA and HLE in depth, are in `knowledge_exams.md`. This dossier cross-references them rather than repeating them.

**Evidence-gathering note (read this first).** The shared WebSearch budget for this session was already used up (200/200) before this subagent started, and direct fetches were blocked for arxiv.org, nature.com, neurips.cc, kaggle.com, crossref and europepmc. All evidence below therefore comes from sources I could actually reach:

1. **Official GitHub repositories:** READMEs, BibTeX blocks, commit pages, archive banners and docs, fetched through raw.githubusercontent.com and WebFetch on github.com.
2. **The PMLR proceedings repository**, `mlresearch/v306`. I downloaded the full ICML 2026 PDF of Akhtar et al. from it and extracted the text.
3. **GitHub code search**, which surfaces verbatim arXiv abstracts, author lists and BibTeX held in arXiv-digest repos, paper-notes repos and thesis bibliographies.
4. **Cached copies of primary documents that live in GitHub repos:** a Google blog post (Feb 2026), the text of the Gemini 2.5 technical report, and a transcript of an Anthropic video.

Each item below gives the URL where I saw it. Where only a secondary summary was reachable, I label it **[secondary]**. Tags used throughout:

- **[V]** verified in this session;
- **[S]** secondary source only;
- **[I]** my interpretation;
- **[U]** unverified background knowledge, excluded from the claims ledger.

---

## Summary

- **No game-based LLM benchmark has entered the mainstream reporting canon.**
  - *Verified basis.* Akhtar et al. (ICML 2026) drew candidates from three sources: 61 model-developer reports (Jan 2022 to Nov 2025, mentioning 190 benchmarks, where a ≥5-report "sustained usage" filter applied), highly cited benchmark papers found via Semantic Scholar, and hypothesis-driven additions from Google Scholar searches. After filtering (text-only, clear protocol, leaderboard available) and refinement, 60 remained, and none of the 60 is a game benchmark [V]. The 60 are therefore not all "sustained-use" benchmarks in the developer-report sense [corrected by fact-check].
  - *Caveat.* The text-only and leaderboard filters could also have removed game benchmarks, so this is not proof that games never appear in reports [I].
  - *What is still alive, and how:*
    - **Kaggle Game Arena** (Google DeepMind and Kaggle, launched 4 Aug 2025 with the blog post "Rethinking how we measure AI intelligence" [corrected by fact-check]) has institutional backing, added poker and Werewolf in Feb 2026, and put out a technical report on 25 Sep 2026 [V].
    - **Community-maintained ladders:** clembench and LLM Chess [V].
    - **Training-environment afterlives:** TextArena pivoted to RL self-play and a NeurIPS 2025 competition [V].
  - *Dormant or archived academic game benchmarks:*
    - GTBench: last commit Sep 2024; its promised public-submission leaderboard is still "Will be ready soon" [V].
    - GameBench: last commit Jun 2024 [V].
    - SmartPlay: last commit Apr 2024; repo archived 1 Jul 2026 [V].
    - lmgame-Bench: no commits since Sep 2025 [V].
    - MC-Bench (Minecraft): no updates since Sep 2025 [V].
- **"Claude/Gemini plays Pokémon" are showcases, not benchmarks.**
  - In an Anthropic video, a speaker who by turn order appears to be the engineer behind Claude Plays Pokémon says "I don't think anybody's making their buying decision for a model on which model plays Pokemon the best. So this is really for our own understanding" [V, transcript; the transcripts carry no speaker labels, so attribution is inferred — corrected by fact-check].
  - The Gemini 2.5 technical report says the Gemini run was set up by an independent developer. Its harness was modified mid-run "as difficulties arose". Run 1 (Gemini 2.5 Pro Exp 03-25) took 813 hours and run 2 (Gemini 2.5 Pro Preview 05-06, fixed harness) took 406.5 hours [V]. Both the harness and the model checkpoint changed between runs [corrected by fact-check]. Harnesses differ across labs and even across runs, so scores are not comparable [I].
- **Mainstream infrastructure also dies.**
  - The Hugging Face Open LLM Leaderboard went v1 → v2 (June 2024) → retired (13 Mar 2025) [S; primary in `knowledge_exams.md`; date independently corroborated by a CSET report footnote citing HF discussion #1135, "March 13, 2025" — fact-check]. Its DROP task was pulled earlier (blog of 1 Dec 2023) because of normalisation and stop-token scoring bugs [V].
  - Stanford's HELM entered **maintenance mode on 1 June 2026**: "no new evaluations will be added to the HELM leaderboards" [V].
  - The BIG-bench repo (more than 200 tasks) was **archived on 17 Apr 2026** [V]. Usage had already shifted to small subsets: BIG-bench Lite (24 tasks, by the organisers) and BIG-Bench Hard (23 tasks, by Suzgun et al.) [V]. Akhtar et al. excluded BIG-Bench for lacking up-to-date leaderboard data [V].
- **Meta-literature: the base rate.** The usual fate of a benchmark is under-use or quick saturation, not lasting adoption.
  - **Koch et al. 2021 (NeurIPS D&B best-paper award) [V]:**
    - dataset use is increasingly concentrated on fewer datasets within task communities;
    - most papers within most tasks use datasets built for other tasks, "even though most tasks have created more datasets than they have imported";
    - dominant datasets come from a handful of elite institutions: over 50% of usages trace to 12 institutions, per Ruder's summary [S].
  - **Ott et al. 2022 (Nature Communications; 3,765 benchmarks) [V]:** "many benchmarks fail to find widespread utilization", and "a large fraction … quickly trended towards near-saturation". They conclude that future benchmarks should emphasise "versatility, breadth and real-world utility".
  - **Dehghani et al. 2021 [V]:** model rankings can flip with the choice of benchmark tasks (the "benchmark lottery").
  - **Akhtar et al. 2026 [V]:** 29 of 60 widely used LLM benchmarks are highly saturated. Age and small test sets predict saturation. Expert-curated benchmarks saturate less at comparable ages, but the authors flag this comparison as age-confounded [corrected by fact-check]. Private test sets do not help.
- **No study I could reach gives a single "fraction of new benchmarks ever reused" figure for LLMs.**
  - A rough funnel [I]: about 445 LLM benchmark papers at six top venues 2018–2024 (Bean et al. 2025) versus 190 benchmarks ever cited in 61 frontier-developer reports 2022–2025. Akhtar et al. do not report how many of the 190 passed their ≥5-report filter; their final 60 also include highly cited and hypothesis-driven additions [corrected by fact-check]. So "a few tens" is the right order of magnitude for sustained multi-report use, not a measured 60.
  - So most new benchmarks are never adopted by model developers, and only a few tens recur. Treat this as an order-of-magnitude reading, not a measured rate.
- **Main predictors of benchmark failure (synthesis):**
  - no distribution channel (harness or hosted leaderboard);
  - no maintainer or refresh plan;
  - saturation and age;
  - small test sets;
  - label or scoring errors;
  - contamination;
  - heavy installs;
  - no single comparable headline score;
  - weak link to decisions users actually make;
  - being pre-empted by a better-resourced incumbent in the same niche.

---

## Detailed findings

### 1. The empirical meta-literature on benchmark usage and failure

#### 1.1 Koch, Denton, Hanna and Foster (2021): "Reduced, Reused and Recycled: The Life of a Dataset in Machine Learning Research"

- **Venue.** NeurIPS 2021 Datasets and Benchmarks Track (Round 2), arXiv:2112.01716.
  - The arXiv digest comment reads "35th Conference on Neural Information Processing Systems (NeurIPS 2021)" [V] (https://raw.githubusercontent.com/TTXS123OK/CVPapers/HEAD/cs.CV/2021/12/20211203.md).
  - It won the Datasets and Benchmarks best-paper award [V, multiple GitHub listings, e.g. https://github.com/brunomaga/brunomaga.github.io/blob/master/publications.md ("Winner of the 'Datasets and Benchmarks Best Paper Award' at NeurIPS 2021"). A list of NeurIPS awards in the Preet37/SAGE repo shows the same].
- **Data.** Usage data for 2015–2020 [V, abstract]. The abstract does not name Papers With Code; that source is stated only in secondary notes (e.g., dadadadawjb/honors: "use PaperWithCode's papers and datasets") [corrected by fact-check].
- **Findings, from the abstract [V]:**
  - "increasing concentration on fewer and fewer datasets within task communities";
  - "significant adoption of datasets from other tasks";
  - "concentration across the field on datasets that have been introduced by researchers situated within a small number of elite institutions".
- **Base-rate sentence, from the paper body as quoted by a blog [S, medium-high].** "the majority of papers within most tasks use datasets that were originally created for other tasks, instead of ones explicitly created for their own task — even though most tasks have created more datasets than they have imported" (https://raw.githubusercontent.com/wvrossem/woutervanrossem.github.io/HEAD/content/post/2021/12/2021-12-06T1948.md).
  - This is the most direct pre-LLM evidence that **most newly created task-specific datasets are under-used** [I].
- **Concentration number [S].** Sebastian Ruder's "ML and NLP Research Highlights of 2021" captions Koch et al.'s figure: "Over 50% of dataset usages can be attributed to 12 institutions. The concentration of dataset usage on institutions and specific datasets as measured by the Gini coefficient has increased in recent years" (GitHub code search hit in `sebastianruder/sebastianruder`, `ml-highlights-2021/index.html`).

#### 1.2 Ott, Barbosa-Silva, Blagec, Brauner and Samwald (2022): "Mapping global dynamics of benchmark creation and saturation in artificial intelligence"

- **Venue.** Nature Communications 13, Article 6793 (2022), DOI 10.1038/s41467-022-34591-0, arXiv:2203.04592 [V] (arXiv digest: https://raw.githubusercontent.com/TTXS123OK/CVPapers/HEAD/cs.CV/2022/03/20220309.md; BibTeX with DOI, PMID 36357391 and PMCID PMC9649641 in https://github.com/EliasSchlie/thesis/blob/main/references.bib).
- **Data.** 3,765 benchmarks covering all of computer vision and NLP. The data was curated in the Intelligence Task Ontology (ITO), built from Papers With Code [V abstract; the ITO repo README links the analysis notebooks: https://raw.githubusercontent.com/OpenBioLink/ITO/HEAD/notebooks/README.md].
- **Findings, from the abstract [V]:**
  - "a large fraction of benchmarks quickly trended towards near-saturation";
  - "**many benchmarks fail to find widespread utilization**";
  - "benchmark performance gains for different AI tasks were prone to unforeseen bursts";
  - "We analyze attributes associated with benchmark popularity, and conclude that future benchmarks should emphasize **versatility, breadth and real-world utility**."
- **Version note [fact-check].** arXiv v1 (Mar 2022) listed Barbosa-Silva first, covered 1,688 benchmarks and ended with a different conclusion ("large-scale community collaboration … real-world utility and impact"). The 3,765-benchmark abstract and the "versatility, breadth and real-world utility" sentence belong to the Nature Communications version (Ott first author). Cite the journal version.
- **Limitation of this dossier.** I could not reach the full text, so I report no per-benchmark percentages from Ott et al. Any specific share of "never-reused" benchmarks attributed to this paper would need checking against the Nature Communications text [U].

#### 1.3 Dehghani et al. (2021): "The Benchmark Lottery"

- **Paper.** arXiv:2107.07002 (14 Jul 2021). Authors: Mostafa Dehghani, Yi Tay, Alexey A. Gritsenko, Zhe Zhao, Neil Houlsby, Fernando Diaz, Donald Metzler, Oriol Vinyals [V] (https://raw.githubusercontent.com/TTXS123OK/CVPapers/HEAD/cs.CV/2021/07/20210714.md).
- **Abstract [V]:**
  - "many factors, other than fundamental algorithmic superiority, may lead to a method being perceived as superior";
  - "the relative performance of algorithms may be altered significantly simply by choosing different benchmark tasks";
  - "every benchmark makes a statement about what it perceives to be important … this might lead to biased progress."
- **Venue.** One secondary source calls it NeurIPS; I could not confirm the venue, so cite it as the arXiv preprint. [Fact-check: it was submitted to the NeurIPS 2021 Datasets and Benchmarks track (OpenReview 5Str2l1vmr-) but is absent from the accepted D&B 2021 list checked; keep "arXiv preprint".]
- **Relevance.** Inertia and path-dependence decide which benchmarks survive, not only quality. The "Deprecating Benchmarks" paper (§1.6) cites this "Benchmark Lottery" dynamic when it explains why ImageNet-style incumbents persist [S].

#### 1.4 Liao, Taori, Raji and Schmidt (2021): "Are We Learning Yet? A Meta Review of Evaluation Failures Across Machine Learning"

- **Venue.** NeurIPS 2021 Datasets and Benchmarks Track (https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/757b505cfd34c64c85ca5b5690ee5293-Abstract-round2.html). I saw the title, authors and venue in a NeurIPS 2021 paper listing (Doragd/Algorithm-Practice-in-Industry, `nips2021.md`) [V for bibliographic facts only; I did not read the abstract here].
- Cited only as the canonical cross-field taxonomy of evaluation failures.

#### 1.5 Label-error and contamination literature (why benchmarks get "killed")

- **Northcutt, Athalye and Mueller (2021): "Pervasive Label Errors in Test Sets Destabilize Machine Learning Benchmarks"** (arXiv:2103.14749). Abstract [V]:
  - "an average of at least 3.3% errors across the 10 datasets";
  - "label errors comprise at least 6% of the ImageNet validation set";
  - with corrected labels, "ResNet-18 outperforms ResNet-50 if the prevalence of originally mislabeled test examples increases by just 6%".
  - Sources: https://github.com/mavenlin/ai_research_trends (post for 2021-03-26) and the companion repo https://github.com/cleanlab/label-errors.
- **Gema et al.: "Are We Done with MMLU?"** (arXiv:2406.04127). Abstract [V]:
  - "57% of the analysed questions in the Virology subset contain errors";
  - they built MMLU-Redux, 3,000 re-annotated questions across 30 subjects (https://github.com/aishwaryanr/awesome-generative-ai-guide/blob/main/research_updates/2024_papers/june_list.md; repo https://github.com/aryopg/mmlu-redux). [corrected by fact-check: that is the arXiv v1 (June 2024) figure; the later/NAACL version reports 5,700 re-annotated questions across all 57 subjects (Luvata/arxive 2025-01-13 replacement listing; AkihikoWatanabe/paper_notes NAACL.xml). Cite the figure that matches the version.]
  - Overall rate of about 6.49% of MMLU questions containing errors (later version's abstract) [V, fact-check]. Venue NAACL 2025 (Long Papers), ACL Anthology 2025.naacl-long.262 [V, fact-check; DeepSeek-R1 reference list copy and AI-Paper-Trends NAACL 2025 atlas].
- **Zhang et al.: "A Careful Examination of Large Language Model Performance on Grade School Arithmetic" (GSM1k)** (arXiv:2405.00332).
  - The arXiv v1 abstract reports "accuracy drops of up to 13%" versus GSM8K, with "several families of models (e.g., Phi and Mistral) showing evidence of systematic overfitting" [V] (https://github.com/lyy1994/awesome-data-contamination README).
  - The NeurIPS 2024 version's abstract says "up to 8%" [V] (https://github.com/fzyzcjy/ai_math_paper_list, `render/neurips_2024.md`).
  - **The headline number changed between versions. Cite the one that matches the version you reference.**

#### 1.6 2024–2026 meta-studies

**BetterBench (Reuel, Hardy, Smith, Lamparth, Hardy and Kochenderfer; NeurIPS 2024 Datasets and Benchmarks; arXiv:2411.12990)** [S, detailed secondary deep-read: https://raw.githubusercontent.com/rasynai/MarigoldBench/HEAD/analysis/literature/deep/betterbench.md]

- **Framework.** 46 criteria across a benchmark lifecycle: design, implementation, documentation, maintenance and retirement. Retirement was not scored.
- **Sample.** 24 benchmarks: 16 foundation-model and 8 non-FM.
- **Stage scores.** Implementation was the weakest stage (mean 6.2/15), then maintenance (9.6).
- **Specific gaps:**
  - 17 of 24 lack an easy replication script;
  - 14 of 24 neither ran multiple evaluations nor reported significance or uncertainty;
  - MMLU scored 5.5 and GPQA 11.0, yet labs report both without distinguishing their quality.
- **Correlation.** Design and usability scores correlate (r = 0.693, p < 0.001).

**"Measuring What Matters: Construct Validity in Large Language Model Benchmarks" (Bean et al., NeurIPS 2025 Datasets and Benchmarks Track [track added by fact-check; DBLP-derived BibTeX in se-uhd/llm-guidelines-website]; arXiv:2511.04703)**

- Authors: Andrew M. Bean and 41 co-authors (Oxford-led). "With a team of 29 expert reviewers, we conduct a systematic review of 445 LLM benchmarks from leading conferences in natural language processing and machine learning" [V] (https://github.com/sailfish009/paper, `2025.11.04.txt`; author list in `CSQianDong/Awesome-arXiv-Daily-Reporter`, `10-Nov-2025`).
- Paper-notes summary [S] (https://raw.githubusercontent.com/zhaoyang97/Paper-Notes/HEAD/docs/NeurIPS2025/recommender/measuring_what_matters_construct_validity_in_large_language_model_benchmarks.md):
  - the 445 came from 46,114 papers at ICML, ICLR and NeurIPS (2018–2024) and ACL, NAACL and EMNLP (2020–2024), via 2,189 keyword candidates;
  - only about 16% of benchmarks use statistical tests to compare models;
  - about 27% use convenience sampling;
  - 8 recommendations.

**"Deprecating Benchmarks: Criteria and Framework" (San Joaquin, Gipiškis, Staufer and Gil; arXiv:2507.06434)**

- Authors from arXiv digest [V] (`CSQianDong/Awesome-arXiv-Daily-Reporter`, `10-Jul-2025`).
- Paper-notes summary [S] (https://raw.githubusercontent.com/zhaoyang97/Paper-Notes/HEAD/docs/ICML2025/recommender/deprecating_benchmarks_criteria_and_framework.md):
  - 7 deprecation criteria: saturation, contamination, statistical bias, high label-error rate, task obsolescence, invalidated assumptions, and semantic drift;
  - a three-phase deprecation process: assess, report, notify;
  - an EU AI Office implementation example.
- The venue is listed as ICML 2025; the track is unverified. [corrected by fact-check: the arXiv comment reads "Accepted to the ICML 2025 Technical AI Governance Workshop". It is a workshop paper, not an ICML main-conference paper.]

**"When AI Benchmarks Plateau: A Systematic Study of Benchmark Saturation" (Akhtar, Reuel, Soni … Biderman, Talat, Ghosh, Solaiman; 37 authors)**

- **Venue.** Proceedings of the 43rd ICML (2026), PMLR vol. 306, pp. 1602–1629; arXiv:2602.16763 [V] (PMLR post: https://raw.githubusercontent.com/mlresearch/v306/HEAD/_posts/2026-09-29-akhtar26a.md; PDF: https://raw.githubusercontent.com/mlresearch/v306/main/assets/akhtar26a/akhtar26a.pdf; code: https://github.com/evaleval/benchmark-saturation). All findings below are from the PMLR PDF [V].
- **Sampling frame.** The 61 official model-developer reports (model cards and technical reports) cover Jan 2022 to Nov 2025 and come from OpenAI, Anthropic, Google, Meta, Alibaba and others. Together they mention **190 benchmarks used in at least one report**. Benchmarks drawn from developer reports had to appear in **at least five distinct reports** ("sustained usage"), be text-only, and have up-to-date leaderboard data. BIG-Bench was excluded for lacking leaderboard data. The final set is **60 benchmarks**. [corrected by fact-check: §3.1 of the PMLR PDF names a second candidate source, "highly-cited benchmark papers" collected via the Semantic Scholar API, and a third step, "hypothesis-driven refinement" that added benchmarks (e.g., multilingual, templated, open-ended) found through Google Scholar searches. The ≥5-report filter applies only to the developer-report candidates, so the 60 are not all sustained-use benchmarks.]
- **Saturation measure.** The S_index is uncertainty-aware: it compares the top-5 score range with the standard error, using an effective test size n^0.5.
- **Findings:**
  - **29 of 60 show high or very high saturation (S_index ≥ 0.7); 14 are very high (≥ 0.9).**
  - Saturation rises with age.
  - Larger test sets mean less saturation.
  - Public (N = 56) and private (N = 4) test sets show similar saturation. "Hiding test data does not appear to prevent saturation once benchmarks are widely adopted."
  - Expert-curated benchmarks saturate less at comparable ages; ARC-AGI and BBH remain unsaturated. [fact-check: the authors class this curation comparison (H3) as age-confounded ("curation categories differ significantly in age (p = 0.0017)") and conclude only that expert-driven design "may improve robustness … though age remains a cofounding factor". Curation is not among the regression's robust predictors.]
  - After controlling for age, adoption proxies are not significant: citations ρ = 0.22, p = 0.12; report frequency ρ = 0.05, p = 0.73.
  - A Bayesian regression gives R² = 0.884 ± 0.012, with age and test-set size the most consistent predictors.
  - Even "live" benchmarks saturate: LiveBench has S_index 0.99 at about 79% accuracy; LiveCodeBench has 0.77.
  - **Version note.** A secondary summary of an earlier arXiv version gives public/private as 52/8. The ICML version says 56/4. Cite the ICML version.
- **Game benchmarks.** None of the 60 is a game benchmark (Table 3 checked) [V]. See the text-only caveat in the Summary.

#### 1.7 What the base rate looks like (synthesis) [I]

No accessible source reports "X% of LLM benchmarks are never reused". The evidence triangulates as follows:

1. **Creation vastly exceeds adoption.**
   - About 445 LLM benchmark papers were accepted at six top venues alone through 2024 (Bean et al.), before counting arXiv-only releases.
   - Frontier-developer reports over nearly four years mention 190 benchmarks, and many of those are pre-LLM classics (GLUE, SQuAD, BoolQ, PIQA, and so on) (Akhtar et al.).
   - Only a few tens were in sustained, multi-report use: the ≥5-report criterion fed a final set of 60 after other filters. That set also includes hypothesis-driven additions and highly cited benchmarks found via Semantic Scholar [second source added by fact-check], so the exact number passing the usage filter alone is not reported.
2. **Pre-LLM field-wide data points the same way.** Many benchmarks "fail to find widespread utilization" (Ott et al., 3,765 benchmarks). Most tasks create more datasets than they import, yet most papers use imported ones (Koch et al.).
3. **Adoption is not safety.** Of the benchmarks that are adopted, about half end up saturated (Akhtar et al.). Mainstream suites also get frozen or retired: the Open LLM Leaderboard, HELM and BIG-bench (§3).
4. **Working estimate.** A reasonable prior is that a newly released LLM benchmark is more likely than not never to appear in a frontier model report. Among those that do, a sizeable fraction saturate within a few years. Treat this as a qualitative prior; quantifying it properly would need a citation- or report-tracking study (a possible contribution for the paper).

---

### 2. Game-based LLM benchmarks: adoption audit

Repository metrics come from WebFetch of github.com pages on 2026-09-29 and are exact as displayed [V]. Stars are a weak proxy for adoption, so read them together with maintenance signals.

| Benchmark | Paper / venue | What it is | Maintenance signal (as of 2026-09-29) | Leaderboard | Status |
|---|---|---|---|---|---|
| **GTBench** | arXiv:2402.12348; NeurIPS 2024 (per co-author's site) | 10 OpenSpiel games (Tic-Tac-Toe, Connect-4, Kuhn poker, Liar's Dice, Nim, negotiation, iterated prisoner's dilemma…) | 74 stars, 12 forks, 21 commits. Last commit **6 Sep 2024**. README: "Upload to GTBench HF Leaderboard — Will be ready soon"; "Customized LLM Agent — Will be ready soon" | HF Space (static) | **Dormant.** Submission path never shipped |
| **GameBench** | arXiv:2406.06613; Language Gamification NeurIPS 2024 Workshop | Multi-game strategic-reasoning suite, 9 authors | 21 stars, 3 forks. Last commit **27 Jun 2024** | Vercel website | **Dormant** |
| **SmartPlay** | arXiv:2310.01557; ICLR 2024 (Microsoft) | 6 games (RPS, bandit, Hanoi, Messenger, Crafter, MineDojo) | 145 stars. Last commit **11 Apr 2024**. **Archived 1 Jul 2026.** Needs a MineDojo install | none | **Dead / archived** |
| **clembench** | arXiv:2305.13455, EMNLP 2023; clembench-2024 arXiv:2405.20859 | Dialogue games (Taboo, Wordle, Codenames, …) run with the clemcore framework | Commits through **15 Apr 2026** ("added benchmarking files for v3.0"). 5 stars on the games repo | Maintained (v2.0/v3.0) | **Alive, niche** |
| **BALROG** | arXiv:2411.13543; ICLR 2025 | Long-horizon agentic games (NetHack, Crafter, BabyAI, …) for LLMs and VLMs | 272 stars. Commits through **9 Apr 2026** (API integrations) | balrogai.com | **Alive, moderate** |
| **TextArena** | arXiv:2504.11442 | 100+ text games (current README; the arXiv abstract says "57+ unique environments" [fact-check]) | 429 stars, 99 forks, 1,174 commits. Updates: SPIRAL self-play RL (Jul 2025), UnstableBaselines RL library, **MindGames NeurIPS 2025 competition**, 192-language support (14 Aug 2026) | textarena.ai | **Alive, mainly as an RL training environment** |
| **lmgame-Bench** | arXiv:2505.15146 | Sokoban, Tetris, 2048, Candy Crush, Mario, Ace Attorney, Pokémon Red | 983 stars, 104 forks. Last commit **12 Sep 2025** | HF Space | **Stalling** |
| **LLM Chess** | arXiv:2512.01992 (Kolasani, Saplin, Crispino et al. [authors corrected by fact-check]); NeurIPS FoRLM 2025 workshop | Multi-turn chess vs random player or Komodo Dragon engine; Elo plus instruction-following durability | 133 stars, 1,430 commits. README: 2025 reasoning models "saturated random-based evaluations, prompting the addition of Dragon" | Live GitHub Pages leaderboard | **Alive, community** |
| **Kaggle Game Arena** | Tech report arXiv:2609.31473 (25 Sep 2026) | Google DeepMind and Kaggle platform. Chess (2025), then poker and Werewolf (Feb 2026) | Harness repo `google-deepmind/game_arena`: 115 stars, 4 commits. Built on OpenSpiel | kaggle.com/game-arena | **Alive, institutionally backed** |
| **MC-Bench** (Minecraft) | website mcbench.ai (no paper seen) | Pairwise human votes on LLM-generated Minecraft builds | GitHub org `mc-bench`: backend last updated **30 Sep 2025**, frontend Apr 2025, orchestrator Dec 2024 | Web arena | **Apparently stalled** |

Sources, in table order:

- https://github.com/jinhaoduan/GTBench and its `/commits/main` page. The README was fetched via raw.githubusercontent.com. NeurIPS 2024: https://github.com/esteng/esteng.github.io `_news/neurips_2024.md`.
- https://github.com/Joshuaclymer/GameBench and `/commits/main`. Venue and authors: `selfimproving-agent/Awesome-Self-Improving-Agents` `Paper/references.bib`.
- https://github.com/microsoft/SmartPlay and `/commits/main`.
- https://github.com/clp-research/clembench and `/commits/main`. Venue: `selfimproving-agent/Awesome-Self-Improving-Agents` README.
- https://github.com/balrog-ai/BALROG and `/commits/main`. ICLR 2025: `Peiyang-Song/Awesome-LLM-Reasoning-Failures` README.
- https://github.com/LeonGuertler/TextArena.
- https://github.com/lmgame-org/GamingAgent and `/commits/main`.
- https://github.com/maxim-saplin/llm_chess.
- https://github.com/google-deepmind/game_arena. Tech-report abstract: `luohongk/Embodied-AI-Daily` `papers/LLM.md`.
- https://github.com/mc-bench.

**Kaggle Game Arena, in more detail.**

- **Launch.**
  - Google's launch post (blog.google/technology/ai/kaggle-game-arena/) framed Game Arena as a response to static benchmarks "reaching near-perfect scores". It promised an "all-play-all ranking system" and an "inaugural chess exhibition" with eight leading models [S] (summary in `franperezlopez/news`, `index_2025_49.html`). [fact-check: the post is titled "Rethinking how we measure AI intelligence" and dated Aug 04, 2025 in copies of Google's blog listing (mebjas.github.io roundups), HN item 44787777 and TLDR AI of 5 Aug 2025.]
  - An RSS entry dated **6 Aug 2025** reports the exhibition tournament under way [V] (`rumca-js/RSS-Link-Database-2025`). A secondary compilation dates the launch to **4 Aug 2025** [S] (`shehryarsaroya/agent-eve`). [fact-check: 4 Aug 2025 is now corroborated as above; the 3-day, 8-model exhibition started 5 Aug 2025.]
- **Feb 2026 expansion.** Google's 2 Feb 2026 post, "Game Arena: Poker and Werewolf, and Gemini 3 tops chess", by Oran Kelly of Google DeepMind [V, cached copy of blog.google in `youzhenxing/info_hub`] [corrected by fact-check: that string is the page's HTML title; the displayed headline, used by HN and newsletter listings, is "Advancing AI benchmarking with Game Arena". Byline: Oran Kelly, Product Manager, Google DeepMind]:
  - adds Werewolf ("our first team-based game played entirely through natural language") and poker;
  - reports "**Gemini 3 Pro and Gemini 3 Flash currently have the top Elo ratings**" on chess.
- **Operator's own models on top [I].** The platform operator's own models lead its headline leaderboard. That need not mean bias, but it is a perception risk for any lab-run benchmark. Independent governance is a design lesson.
- **Technical report.** Its abstract claims Game Arena "enables models to play head-to-head matchups … where the gameplay strength naturally increases as models evolve, **preventing performance saturation**" [V].
  - Note [I]: Akhtar et al. show that "live" static benchmarks can still saturate at the top. Arena-style relative ratings sidestep ceiling effects but create other problems: rating comparability over time, and harness sensitivity (see the harness's majority-voting and "rethinking" samplers and LLM-based move parsing in the repo README [V]).

**"Claude Plays Pokémon" and "Gemini Plays Pokémon".**

- **Anthropic.**
  - The Anthropic video "Lessons on AI agents from Claude Plays Pokemon" (transcript copy: https://github.com/Unson-LLC/anthropic-youtube) says the project began informally with Claude 3.5 Sonnet in June 2024. The team "included Claude Plays Pokemon as part of our Claude 3.7 Sonnet launch … the benchmark with all the lines of how far each model's got through the different gyms." The engineer adds: "I don't think anybody's making their buying decision for a model on which model plays Pokemon the best. So this is really for our own understanding" [V]. [corrected by fact-check: the video (youtube.com/watch?v=CXhYDOvgpuU, published 24 Apr 2025 per a second transcript mirror, ai-native-engineer/anthropic-mirror) is a conversation between David (Applied AI, the project's engineer) and Alex (Claude Relations, host). The "3.7 Sonnet launch" sentence is the host's question, not the engineer's statement. The "buying decision" line follows the alternating turn order of the engineer, but neither transcript labels speakers, so treat the attribution as probable, not certain.]
  - A third-party agent-infrastructure catalogue lists it as a "Closed agent harness (Anthropic-internal); not reproducible by third parties; benchmark protocol informal — no standardized scoring" [S] (`MrPeppersDev/agent-infrastructure-landscape`).
- **Google (Gemini 2.5 technical report, text copy in `ShiwenZhang00/AI_Model_Evaluation_on_L4`) [V]:**
  - "On March 28, 2025, an independent developer not affiliated with Google, Joel Zhang, set up a Twitch stream";
  - "over the course of the run, modifications were made to the setup as difficulties arose";
  - "on May 2, 2025, Gemini 2.5 Pro completed the game after 813 hours";
  - a second, fully autonomous run with "the finalized fixed agentic harness" completed in "406.5 hours (nearly exactly half the time of the first run)";
  - [fact-check] the report names different checkpoints: run 1 used "Gemini 2.5 Pro Exp 03-25" and run 2 (begun 22 May 2025) used "Gemini 2.5 Pro Preview 05-06". The two runs therefore differ in model version as well as harness;
  - the harness feeds "a subset of RAM information" overlaid on a screenshot, with summary resets every 100 turns and a goals system.
- **Interpretation [I].** These were compelling public demonstrations of long-horizon agency, and both appeared in frontier-lab launch materials. They fail as benchmarks because:
  - there is one game;
  - the harness differs by lab and changes within a run;
  - there are one or two runs, so no variance estimate;
  - the operators are different parties;
  - there is no fixed scoring protocol;
  - the task has no direct link to product decisions (per the Anthropic engineer's own quote).
  - ~~The same *halving of completion time from a harness change alone* shows how scaffold-dependent game scores are.~~ [corrected by fact-check: the halving cannot be attributed to the harness alone, because the model checkpoint also changed (Exp 03-25 → Preview 05-06). It shows that uncontrolled changes in scaffold and model version can halve the headline number, which is still an argument against such runs as benchmarks.]

**Minecraft-based evaluations.**

- **Voyager** (arXiv:2305.16291; Wang, Xie, Jiang, Mandlekar, Xiao, Zhu, Fan, Anandkumar; README: https://github.com/MineDojo/Voyager) is an agent method, not a benchmark [V].
- **Mindcraft/MineCollab** (arXiv:2504.17950; White, Nottingham et al.; README: https://github.com/kolbytn/mindcraft, now github.com/mindcraft-bots/mindcraft [fact-check]) bundles a multi-agent task suite [V].
  - Its README warns: "We are currently not very responsive to github issues", and "Do not connect this bot to public servers with coding enabled" [V]. Minecraft evaluations need licensed game clients, servers and Node/Java toolchains [V, README requirements]. [I] That is a heavy-install barrier of the kind the user identified for Game Reasoning Arena.
- **MC-Bench**: see the table above.

**Did any game benchmark achieve lasting adoption?**

1. **Not as a mainstream reported metric.** None appears among Akhtar et al.'s 60 benchmarks in sustained use [V, with the text-only caveat]. The closest to lasting status is **Kaggle Game Arena**, which is under 14 months old and backed by Google DeepMind and Kaggle [V]. Its long-term independence and uptake by other labs are not yet established [I].
2. **Survival correlates with a maintainer and a platform, not with game choice [I]:**
   - clembench (a university group with versioned releases);
   - LLM Chess (a single dedicated maintainer, 1,430 commits, adaptive opponent strength);
   - BALROG (API-integration commits into 2026);
   - Game Arena (an institution).
   - Dormancy tracks the end of the paper cycle: GTBench, GameBench and SmartPlay all went quiet within months of publication.
3. **The most durable "use" of game environments is as RL training environments, not evaluation [V/I].** Evidence: TextArena's SPIRAL, UnstableBaselines and MindGames competition, and clembench's "playpen" training use case (README).

---

### 3. Non-game failures, retirements and freezes

#### 3.1 Hugging Face Open LLM Leaderboard

- **Versions.** v1 used ARC, HellaSwag, MMLU, TruthfulQA, WinoGrande and GSM8K. v2 (from June 2024) used IFEval, MuSR, GPQA, MATH, BBH and MMLU-Pro [primary evidence in `knowledge_exams.md`]. The v2 task list is also confirmed by the Akhtar et al. companion code, which analyses "HuggingFace Open LLM v2 (BBH, GPQA, MMLU-PRO, MUSR, IFEval, MATH)" [V] (https://github.com/evaleval/benchmark-saturation).
- **Retirement [S here; primary in `knowledge_exams.md`].**
  - "retired 2025-03-13; HF's successor is infrastructure (Community Evals, Feb 2026 — leaderboards attached to benchmark datasets, verified badges) not a ranking" (`gmale/aint`, `experiments/005-model-market-survey.md`).
  - "this leaderboard has been retired" (https://github.com/fboulnois/llm-leaderboard-csv README).
- **DROP removal (a scoring-bug failure) [V]** (https://raw.githubusercontent.com/huggingface/blog/main/open-llm-leaderboard-drop.md; authors: clefourrier, cabreraalex, stellaathena, SaylorTwift, thomwolf):
  - After DROP was added, "the overwhelming majority of models scor[ed] less than 10 out of 100 on their f1-score".
  - Causes: number normalisation failed when a number was followed by non-space whitespace, and "." served as the stop token.
  - "**We have therefore taken the decision to remove DROP from the Open LLM Leaderboard until a new version arises.**"
  - A full leaderboard update "took 8 years of GPU time". [fact-check: exact wording is "the full update took 8 years of GPU time, and a lot of it was taken by DROP"; "the full update" is the re-run of all models when Winogrande, GSM8K and DROP were added. The post is dated 1 Dec 2023 in huggingface/blog `_blog.yml`.]
- **Lesson [I].** Even the most-used open leaderboard was killed by saturation, cost and obsolescence. Its harness bugs silently corrupted a benchmark for months.

#### 3.2 HELM (Stanford CRFM)

- **Maintenance mode.** "HELM entered maintenance mode on June 1, 2026 … no new features will be added to HELM, and **no new evaluations will be added to the HELM leaderboards**." The maintainers point users to Evalchemy, Inspect AI Evals, Lighteval, the LM Evaluation Harness and Unitxt [V] (https://raw.githubusercontent.com/stanford-crfm/helm/HEAD/docs/maintenance_mode.md; README note).
- **Before the freeze.** HELM had fragmented into many leaderboards: Capabilities, Safety, VHELM, HEIM, MedHELM, audio and others [V, README].
- **Model cards.** I could not verify, in this session, how often HELM scores appeared in frontier model cards [U]. So "limited uptake in model cards" remains unverified here. The verified signal is the 2026 freeze.
- **Lesson [I].** A holistic, many-metric design can be the right science and still lose the attention economy to single-number benchmarks and leaner harnesses.

#### 3.3 BIG-bench

- **Size.** "More than 200 tasks" from a collaborative call. The BIG-bench Lite leaderboard covers 24 tasks. The paper is in TMLR 2023 (arXiv:2206.04615). The README still says the paper "is currently under review" [V] (https://raw.githubusercontent.com/google/BIG-bench/HEAD/README.md). ~~[I] The README was never updated after acceptance, a small sign of neglect.~~ [corrected by fact-check: the README's citation section does cite the published TMLR 2023 version; only the "under review" sentence is stale.]
- **Archived.** "This repository was archived by the owner on Apr 17, 2026" (3.2k stars, 5,893 commits) [V] (https://github.com/google/BIG-bench).
- **The distillate is what survived.**
  - BBH kept **23** tasks, those "for which prior language model evaluations did not outperform the average human-rater". Before BBH, "the best model in the BIG-Bench paper [was already] outperforming average reported human-rater results on 65% of the BIG-Bench tasks" [V] (https://raw.githubusercontent.com/suzgunmirac/BIG-Bench-Hard/HEAD/README.md; Findings of ACL 2023, arXiv:2210.09261).
  - BBH is among Akhtar et al.'s 60 sustained-use benchmarks and remains unsaturated [V]. Full BIG-Bench was **excluded** from that study for lacking up-to-date leaderboard data [V].
- **Lesson [I].** Crowdsourcing hundreds of tasks produced breadth but not a ladder people climb. Adoption went to a small, hard, cheap-to-run subset with one number. This mirrors Koch et al.'s within-community concentration at the level of individual tasks.

#### 3.4 Benchmarks damaged by label errors, scoring bugs or contamination (summary)

- **Label errors.** At least 3.3% on average across 10 classic test sets, and at least 6% of ImageNet validation, enough to flip model rankings (Northcutt et al.) [V]. Errors in 57% of analysed MMLU Virology questions (Gema et al.) [V].
- **Scoring bugs.** DROP on the Open LLM Leaderboard (above) [V].
- **Contamination.** GSM8K vs GSM1k gaps of up to 13% (arXiv v1) or 8% (NeurIPS version) for some model families [V].
- **Hygiene is not enough.** Private test sets do not prevent saturation once a benchmark is widely adopted (Akhtar et al.) [V]. Hygiene protects validity, not longevity [I; consistent with `knowledge_exams.md`].

---

### 4. Predictors of benchmark failure and success (synthesis)

"Evidence" gives the strongest source. Items marked [I] are my synthesis across cases.

| Factor | Direction | Evidence |
|---|---|---|
| Age and cumulative exposure | Older benchmarks are more saturated | Akhtar et al. 2026 [V] |
| Test-set size and measurement resolution | Small sets saturate (lose discrimination) sooner | Akhtar et al. 2026 [V]; BetterBench: "a 1% improvement can be reliably detected" [S] |
| Expert curation vs crowdsourcing | Expert-curated sets resist saturation better (age-confounded per the authors [fact-check]) | Akhtar et al. 2026 [V] |
| Private test set | No protective effect on saturation | Akhtar et al. 2026 [V] |
| Versatility, breadth, real-world utility | Associated with popularity | Ott et al. 2022 [V, abstract] |
| Institutional origin | Dominant datasets come from few elite institutions | Koch et al. 2021 [V]; >50% of usages from 12 institutions [S] |
| Distribution channel (harness integration, hosted leaderboard, frontier model-card inclusion) | Needed for adoption | Case evidence: Game Arena and Open LLM Leaderboard (while alive) vs GTBench's never-shipped submission path [V/I]; sibling `user_failed_a.md` finds the same (MastermindEval via lm-eval, Codenames via clembench) |
| Named maintainer and refresh cadence | Survival | clembench, LLM Chess, BALROG, TextArena alive vs GTBench, GameBench, SmartPlay dormant [V/I]; BetterBench: maintenance is the second-weakest lifecycle stage [S] |
| Reproducibility and ease of running | Adoption and credibility | BetterBench: 17/24 lack a replication script [S]; heavy installs (SmartPlay needs MineDojo; Minecraft servers) [V] |
| Single comparable headline score | Adoption | Game Arena's later unified leaderboard (sibling evidence); BBH/BBL distillation [V/I] |
| Label and scoring quality | Errors trigger removal or replacement | DROP removal; MMLU-Redux; Northcutt et al. [V] |
| Statistical rigour | Usually missing | Bean et al.: about 16% use statistical tests [S]; BetterBench: 14/24 no significance or uncertainty [S] |
| Relevance to real decisions | Showcases without decision relevance stay demos | Anthropic Pokémon quote [V]; Ott et al. "real-world utility" [V] |
| Timing and incumbency | Pre-emption kills niche entrants | Sibling `user_failed_a.md` (Game Arena launched the same week as Qi Town and Game Reasoning Arena) |
| Construct validity | Weak definitions are common | Bean et al. 2025 (445 benchmarks) [V/S] |

---

## Implications for designing a new benchmark

These are written for a non-game LLM benchmark and follow from the evidence above.

1. **Assume failure is the default.** Design explicitly against the usual causes of death: no distribution, no maintainer, saturation and validity defects. Put a "longevity plan" section in the paper [I; base-rate evidence §1.7].
2. **Build the distribution channel in from day one.**
   - Ship a task for widely used harnesses (EleutherAI LM Evaluation Harness, Inspect, Lighteval) and a hosted, maintained leaderboard. HELM's own freeze notice points users to these harnesses [V].
   - Make it cheap and API-only, with no game engines, emulators or servers to install [V/I].
3. **Report one headline number plus diagnostics.**
   - One number helps adoption; the 23-task BBH outlived the full 200-task BIG-bench [V/I]. BBH is among Akhtar et al.'s 60; full BIG-bench was excluded.
   - Keep per-skill breakdowns so it is not a "lottery" (Dehghani et al.) [V].
4. **Design for resolution and against saturation.**
   - Use a large effective test size or a renewable item generator.
   - Report uncertainty and confidence intervals.
   - Publish the Akhtar et al. S_index (top-k range vs SE) on the leaderboard and pre-commit to refresh or deprecation triggers. Only about 16% of benchmarks use statistical tests (Bean et al.) [S].
   - Note that "live" refresh alone did not stop LiveBench from reaching very high saturation [V].
5. **Prefer expert-validated items and renewable generation over crowdsourced static pools.** Expert curation is associated with resistance to saturation, though Akhtar et al. flag the comparison as age-confounded [corrected by fact-check]. A private test set by itself does not help (Akhtar et al.) [V].
6. **Budget for label and scoring audits before release.** Publish a measured error rate. MMLU- and ImageNet-scale error rates (roughly 3–7%) are enough to reorder models, and a single normalisation bug killed DROP on the Open LLM Leaderboard [V].
7. **Tie the construct to decisions users actually make.**
   - Ott et al.'s popularity correlates are "versatility, breadth and real-world utility" [V].
   - The Pokémon lesson: if nobody would choose a model based on the score, it stays a demo [V].
8. **Plan a maintenance budget and governance.**
   - Name an owner, a versioning scheme and deprecation criteria (San Joaquin et al.: saturation, contamination, label errors, task obsolescence, …) [S].
   - Avoid a lab-run leaderboard where the operator's own model tops the board without independent oversight (Game Arena, Feb 2026) [V/I].
9. **Make the score robust to scaffolding.** Fix and publish the harness; version it; report harness-variance ablations. The two Gemini Pokémon runs differed by 2x, with both the harness and the model checkpoint changed, so the effect cannot be attributed to either alone [corrected by fact-check] [V/I].
10. **Watch for timing and incumbents.** Check whether a large institution is about to occupy the niche. If so, differentiate or partner (sibling finding).

---

## Claims ledger

Confidence reflects source type and how directly I observed the claim.

1. **Koch et al. (2021)** found "increasing concentration on fewer and fewer datasets within task communities" and "concentration across the field on datasets that have been introduced by researchers situated within a small number of elite institutions", using 2015–2020 Papers With Code data. NeurIPS 2021 Datasets and Benchmarks Track; arXiv:2112.01716.
   - Sources: https://raw.githubusercontent.com/TTXS123OK/CVPapers/HEAD/cs.CV/2021/12/20211203.md ; https://github.com/mavenlin/ai_research_trends (2021-12-03 post).
   - **Confidence: high.**
2. **Koch et al.** state that "the majority of papers within most tasks use datasets that were originally created for other tasks … even though most tasks have created more datasets than they have imported". Per Ruder's summary of their figure, over 50% of dataset usages are attributable to 12 institutions.
   - Sources: https://raw.githubusercontent.com/wvrossem/woutervanrossem.github.io/HEAD/content/post/2021/12/2021-12-06T1948.md ; GitHub `sebastianruder/sebastianruder` `ml-highlights-2021/index.html`.
   - **Confidence: medium** (secondary quotes of the paper).
3. **Ott et al. (2022, Nature Communications 13:6793; DOI 10.1038/s41467-022-34591-0)** curated 3,765 CV and NLP benchmarks. They found a large fraction trended quickly toward near-saturation, "many benchmarks fail to find widespread utilization", and future benchmarks should emphasise "versatility, breadth and real-world utility".
   - Sources: https://raw.githubusercontent.com/TTXS123OK/CVPapers/HEAD/cs.CV/2022/03/20220309.md ; https://github.com/EliasSchlie/thesis/blob/main/references.bib.
   - **Confidence: high.**
4. **Dehghani et al. (2021, arXiv:2107.07002)** show that the relative performance of algorithms "may be altered significantly simply by choosing different benchmark tasks".
   - Source: https://raw.githubusercontent.com/TTXS123OK/CVPapers/HEAD/cs.CV/2021/07/20210714.md.
   - **Confidence: high.**
5. **Akhtar et al. (ICML 2026, PMLR 306:1602–1629)** reviewed 61 model-developer reports (Jan 2022 to Nov 2025) mentioning 190 benchmarks. They required at least 5 reports for "sustained usage" among developer-report candidates, added highly cited benchmarks (Semantic Scholar) and hypothesis-driven additions, and analysed 60 benchmarks [corrected by fact-check]. Findings:
   - 29/60 have high or very high saturation, and 14 are very high;
   - saturation rises with age and falls with test-set size;
   - public (56) and private (4) test sets do not differ;
   - expert curation is associated with resilience (age-confounded, per the authors) [corrected by fact-check].
   - Sources: https://raw.githubusercontent.com/mlresearch/v306/main/assets/akhtar26a/akhtar26a.pdf ; https://raw.githubusercontent.com/mlresearch/v306/HEAD/_posts/2026-09-29-akhtar26a.md ; https://github.com/evaleval/benchmark-saturation.
   - **Confidence: high.**
6. **No game-based benchmark is among the 60 benchmarks** in Akhtar et al.'s analysed set (Table 3; not purely a sustained-use set [corrected by fact-check]). Their text-only and leaderboard filters may also have excluded game benchmarks.
   - Source: https://raw.githubusercontent.com/mlresearch/v306/main/assets/akhtar26a/akhtar26a.pdf.
   - **Confidence: high** for the fact; **medium** for its meaning as an adoption signal.
7. **HELM maintenance mode.** HELM entered maintenance mode on 1 June 2026, after which "no new evaluations will be added to the HELM leaderboards".
   - Source: https://raw.githubusercontent.com/stanford-crfm/helm/HEAD/docs/maintenance_mode.md.
   - **Confidence: high.**
8. **BIG-bench.** The repo (more than 200 tasks) was archived on 17 Apr 2026. BBH retained 23 tasks where prior models had not beaten average human raters, and the best BIG-bench-paper model already beat average human raters on 65% of tasks.
   - Sources: https://github.com/google/BIG-bench ; https://raw.githubusercontent.com/suzgunmirac/BIG-Bench-Hard/HEAD/README.md.
   - **Confidence: high.**
9. **Open LLM Leaderboard, DROP.** Hugging Face removed DROP from the Open LLM Leaderboard after normalisation and stop-token bugs left most models scoring below 10 F1, and noted that a full update took "8 years of GPU time". The leaderboard itself was retired, dated 13 Mar 2025 by secondary sources.
   - Sources: https://raw.githubusercontent.com/huggingface/blog/main/open-llm-leaderboard-drop.md ; https://github.com/fboulnois/llm-leaderboard-csv ; https://github.com/gmale/aint.
   - **Confidence: high** for DROP; **medium** for the retirement date in this dossier (primary in `knowledge_exams.md`).
10. **Academic game benchmarks went dormant soon after publication:**
    - GTBench: last commit 6 Sep 2024; leaderboard upload "Will be ready soon".
    - GameBench: last commit 27 Jun 2024.
    - SmartPlay: last commit 11 Apr 2024; archived 1 Jul 2026.
    - lmgame-Bench: last commit 12 Sep 2025.
    - Sources: https://github.com/jinhaoduan/GTBench/commits/main ; https://github.com/Joshuaclymer/GameBench/commits/main ; https://github.com/microsoft/SmartPlay/commits/main ; https://github.com/lmgame-org/GamingAgent/commits/main.
    - **Confidence: high** (as of 2026-09-29).
11. **Kaggle Game Arena.**
    - Launched in 2025 with chess (exhibition under way by 6 Aug 2025).
    - Added Werewolf and poker on 2 Feb 2026, when Gemini 3 Pro and Gemini 3 Flash topped the chess Elo leaderboard.
    - Published a technical report (arXiv:2609.31473, 25 Sep 2026) claiming the arena format prevents performance saturation.
    - Sources: cached Google blog in https://github.com/youzhenxing/info_hub (`output/community/content_cache/20260203/12f40143f5b25b5f.txt`) ; https://github.com/luohongk/Embodied-AI-Daily (`papers/LLM.md`) ; https://github.com/rumca-js/RSS-Link-Database-2025 ; https://github.com/google-deepmind/game_arena.
    - **Confidence: high** for Feb 2026 and the report; **medium** for the exact launch day.
12. **Gemini Plays Pokémon.**
    - Set up by an independent developer (28 Mar 2025).
    - Its harness was modified during run 1, which completed on 2 May 2025 after 813 hours.
    - Run 2, with a fixed harness, took 406.5 hours.
    - Source: the Gemini 2.5 technical report text in https://github.com/ShiwenZhang00/AI_Model_Evaluation_on_L4 (`Documents/gemini_v2_5_report.txt`).
    - **Confidence: high** (verbatim copy of the report; not fetched from the arXiv or Google host).
13. **Claude Plays Pokémon.** In the Anthropic video, the host notes it featured in the Claude 3.7 Sonnet launch as progress lines; the engineer behind it (by turn order; transcripts are unlabeled) says nobody makes buying decisions on it: "this is really for our own understanding" [corrected by fact-check: the launch remark is the host's, not the engineer's].
    - Source: https://github.com/Unson-LLC/anthropic-youtube (transcript `049-Lessons on AI agents from Claude Plays Pokemon.md`).
    - **Confidence: medium-high** (transcript copy of an official video).
14. **Construct validity and statistical rigour are commonly missing:**
    - Bean et al. (NeurIPS 2025, arXiv:2511.04703) reviewed 445 LLM benchmarks with 29 expert reviewers; about 16% use statistical tests [secondary].
    - BetterBench (NeurIPS 2024 D&B) found 17/24 benchmarks lack a replication script and 14/24 report no significance or uncertainty [secondary].
    - Sources: https://github.com/sailfish009/paper (`2025.11.04.txt`) ; https://raw.githubusercontent.com/zhaoyang97/Paper-Notes/HEAD/docs/NeurIPS2025/recommender/measuring_what_matters_construct_validity_in_large_language_model_benchmarks.md ; https://raw.githubusercontent.com/rasynai/MarigoldBench/HEAD/analysis/literature/deep/betterbench.md.
    - **Confidence: high** for 445/29; **medium** for the percentages.
15. **Label errors and contamination:**
    - Northcutt et al.: an average of at least 3.3% label errors across 10 benchmark test sets, and at least 6% of ImageNet validation.
    - MMLU: 57% of analysed Virology questions contain errors.
    - GSM1k: accuracy drops of up to 13% (arXiv v1) or 8% (NeurIPS 2024 version) versus GSM8K.
    - Sources: https://github.com/mavenlin/ai_research_trends (2021-03-26) ; https://github.com/aishwaryanr/awesome-generative-ai-guide (`june_list.md`) ; https://github.com/lyy1994/awesome-data-contamination ; https://github.com/fzyzcjy/ai_math_paper_list.
    - **Confidence: high.**

---

## References

"Seen at" gives the URL where I observed each item in this session.

1. Koch, B., Denton, E., Hanna, A., Foster, J. G. *Reduced, Reused and Recycled: The Life of a Dataset in Machine Learning Research.* NeurIPS 2021 Datasets and Benchmarks Track. arXiv:2112.01716. https://arxiv.org/abs/2112.01716. Seen at: https://raw.githubusercontent.com/TTXS123OK/CVPapers/HEAD/cs.CV/2021/12/20211203.md
2. Ott, S., Barbosa-Silva, A., Blagec, K., Brauner, J., Samwald, M. *Mapping global dynamics of benchmark creation and saturation in artificial intelligence.* Nature Communications 13, 6793 (2022). DOI 10.1038/s41467-022-34591-0. arXiv:2203.04592. Seen at: https://raw.githubusercontent.com/TTXS123OK/CVPapers/HEAD/cs.CV/2022/03/20220309.md
3. Dehghani, M., Tay, Y., Gritsenko, A. A., Zhao, Z., Houlsby, N., Diaz, F., Metzler, D., Vinyals, O. *The Benchmark Lottery.* arXiv:2107.07002 (2021). Seen at: https://raw.githubusercontent.com/TTXS123OK/CVPapers/HEAD/cs.CV/2021/07/20210714.md
4. Liao, T., Taori, R., Raji, I. D., Schmidt, L. *Are We Learning Yet? A Meta Review of Evaluation Failures Across Machine Learning.* NeurIPS 2021 Datasets and Benchmarks. https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/757b505cfd34c64c85ca5b5690ee5293-Abstract-round2.html. Seen at: GitHub `Doragd/Algorithm-Practice-in-Industry` (`nips2021.md`)
5. Ruder, S. *ML and NLP Research Highlights of 2021* (blog, 2022). Figure caption summarising Koch et al. Seen at: GitHub `sebastianruder/sebastianruder` (`ml-highlights-2021/index.html`)
6. Northcutt, C. G., Athalye, A., Mueller, J. *Pervasive Label Errors in Test Sets Destabilize Machine Learning Benchmarks.* NeurIPS 2021. arXiv:2103.14749. Seen at: https://github.com/mavenlin/ai_research_trends ; https://github.com/cleanlab/label-errors
7. Gema, A. P., Leang, J. O. J., Hong, G., Devoto, A., Mancino, A. C. M., Saxena, R., He, X., Zhao, Y., Du, X., Ghasemi Madani, M. R., Barale, C., McHardy, R., Harris, J., Kaddour, J., van Krieken, E., Minervini, P. *Are We Done with MMLU?* NAACL 2025 (Long Papers), ACL Anthology 2025.naacl-long.262; arXiv:2406.04127 [authors and venue verified by fact-check]. Seen at: https://github.com/aishwaryanr/awesome-generative-ai-guide ; https://github.com/aryopg/mmlu-redux
8. Zhang, H., Da, J., Lee, D., et al. *A Careful Examination of Large Language Model Performance on Grade School Arithmetic.* NeurIPS 2024. arXiv:2405.00332. Seen at: https://github.com/lyy1994/awesome-data-contamination ; https://github.com/fzyzcjy/ai_math_paper_list
9. Reuel, A., Hardy, A., Smith, C., Lamparth, M., Hardy, M., Kochenderfer, M. J. *BetterBench: Assessing AI Benchmarks, Uncovering Issues, and Establishing Best Practices.* NeurIPS 2024 Datasets and Benchmarks. arXiv:2411.12990. Seen at: https://raw.githubusercontent.com/rasynai/MarigoldBench/HEAD/analysis/literature/deep/betterbench.md
10. Bean, A. M., Kearns, R. O., Romanou, A., et al. (42 authors). *Measuring What Matters: Construct Validity in Large Language Model Benchmarks.* NeurIPS 2025 Datasets and Benchmarks Track [track verified by fact-check]. arXiv:2511.04703. Seen at: https://github.com/sailfish009/paper (`2025.11.04.txt`) ; https://github.com/CSQianDong/Awesome-arXiv-Daily-Reporter
11. San Joaquin, A., Gipiškis, R., Staufer, L., Gil, A. *Deprecating Benchmarks: Criteria and Framework.* arXiv:2507.06434 (2025). ICML 2025 Workshop on Technical AI Governance [corrected by fact-check: workshop paper, per the arXiv comment]. Seen at: https://github.com/CSQianDong/Awesome-arXiv-Daily-Reporter (`10-Jul-2025`) ; https://raw.githubusercontent.com/zhaoyang97/Paper-Notes/HEAD/docs/ICML2025/recommender/deprecating_benchmarks_criteria_and_framework.md
12. Akhtar, M., Reuel, A., Soni, P., et al. (37 authors). *When AI Benchmarks Plateau: A Systematic Study of Benchmark Saturation.* ICML 2026, PMLR 306:1602–1629. arXiv:2602.16763. Seen at: https://raw.githubusercontent.com/mlresearch/v306/main/assets/akhtar26a/akhtar26a.pdf ; https://github.com/evaleval/benchmark-saturation
13. Hugging Face (clefourrier, cabreraalex, stellaathena, SaylorTwift, thomwolf). *Open LLM Leaderboard: DROP deep dive.* Blog, 1 Dec 2023 [date verified by fact-check from huggingface/blog `_blog.yml`]. https://huggingface.co/blog/open-llm-leaderboard-drop. Seen at: https://raw.githubusercontent.com/huggingface/blog/main/open-llm-leaderboard-drop.md
14. Open LLM Leaderboard retirement: Fourrier, C. *It's been a wild ride, folks :) (end of the Open LLM Leaderboard)*, HF Space discussion #1135, 13 Mar 2025 (title and date via a CSET report footnote and niftymonkey/pickai notes; primary page not fetched) [fact-check]. Secondary reports seen at: https://github.com/fboulnois/llm-leaderboard-csv ; https://github.com/gmale/aint (primary HF source in `knowledge_exams.md`)
15. Stanford CRFM. *HELM Maintenance Mode Policy* (2026). https://crfm-helm.readthedocs.io/en/latest/maintenance_mode/. Seen at: https://raw.githubusercontent.com/stanford-crfm/helm/HEAD/docs/maintenance_mode.md
16. Liang, P., Bommasani, R., Lee, T., et al. *Holistic Evaluation of Language Models.* TMLR 2023. https://openreview.net/forum?id=iO4LZibEqW. Seen at: https://raw.githubusercontent.com/stanford-crfm/helm/HEAD/README.md
17. Srivastava, A., et al. (BIG-bench authors). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models.* TMLR 2023. arXiv:2206.04615. Seen at: https://raw.githubusercontent.com/google/BIG-bench/HEAD/README.md ; https://github.com/google/BIG-bench
18. Suzgun, M., et al. *Challenging BIG-Bench Tasks and Whether Chain-of-Thought Can Solve Them.* Findings of ACL 2023. arXiv:2210.09261. Seen at: https://raw.githubusercontent.com/suzgunmirac/BIG-Bench-Hard/HEAD/README.md
19. Duan, J., Zhang, R., Diffenderfer, J., Kailkhura, B., Sun, L., Stengel-Eskin, E., Bansal, M., Chen, T., Xu, K. *GTBench: Uncovering the Strategic Reasoning Limitations of LLMs via Game-Theoretic Evaluations.* NeurIPS 2024. arXiv:2402.12348. Seen at: https://github.com/jinhaoduan/GTBench
20. Costarelli, A., Allen, M., Hauksson, R., Sodunke, G., Hariharan, S., Cheng, C., Li, W., Clymer, J., Yadav, A. *GameBench: Evaluating Strategic Reasoning Abilities of LLM Agents.* Language Gamification NeurIPS 2024 Workshop. arXiv:2406.06613. Seen at: https://github.com/Joshuaclymer/GameBench ; `selfimproving-agent/Awesome-Self-Improving-Agents` (`references.bib`)
21. Chalamalasetti, K., Götze, J., Hakimov, S., Madureira, B., Sadler, P., Schlangen, D. *clembench: Using Game Play to Evaluate Chat-Optimized Language Models as Conversational Agents.* EMNLP 2023. arXiv:2305.13455. Seen at: `IAAR-Shanghai/SurveyX` references ; https://github.com/clp-research/clembench
22. Beyer, A., Chalamalasetti, K., Hakimov, S., Madureira, B., Sadler, P., Schlangen, D. *clembench-2024: A Challenging, Dynamic, Complementary, Multilingual Benchmark and Underlying Flexible Framework for LLMs as Multi-Action Agents.* arXiv:2405.20859 [authors added by fact-check from arXiv listing mirrors]. Seen at: `selfimproving-agent/Awesome-Self-Improving-Agents` README
23. Wu, Y., Tang, X., Mitchell, T., Li, Y. *SmartPlay: A Benchmark for LLMs as Intelligent Agents.* ICLR 2024. arXiv:2310.01557. Seen at: https://github.com/microsoft/SmartPlay
24. Paglieri, D., Cupiał, B., Coward, S., Piterbarg, U., Wołczyk, M., Khan, A., Pignatelli, E., Kuciński, Ł., Pinto, L., Fergus, R., Foerster, J. N., Parker-Holder, J., Rocktäschel, T. *BALROG: Benchmarking Agentic LLM and VLM Reasoning On Games.* ICLR 2025. arXiv:2411.13543. Seen at: https://github.com/balrog-ai/BALROG
25. Guertler, L., Cheng, B., Yu, S., Liu, B., Choshen, L., Tan, C. *TextArena.* arXiv:2504.11442 (2025). Seen at: https://github.com/LeonGuertler/TextArena
26. Hu, L., Huo, M., Zhang, Y., Yu, H., Xing, E. P., Stoica, I., Rosing, T., Jin, H., Zhang, H. *lmgame-Bench: How Good are LLMs at Playing Games?* arXiv:2505.15146 (2025). Seen at: https://github.com/lmgame-org/GamingAgent
27. Kolasani, S., Saplin, M., Crispino, N., Montgomery, K., Davis, J. Q., Zaharia, M., Wang, C., Wang, C. *LLM CHESS: Benchmarking Reasoning and Instruction-Following in LLMs through Chess.* Workshop on Foundations of Reasoning in Language Models (FoRLM @ NeurIPS 2025). arXiv:2512.01992 [corrected by fact-check: first author is Sai Kolasani, not Maxim Saplin; source: co-author Nicholas Crispino's site]. Seen at: https://github.com/maxim-saplin/llm_chess
28. Doerschuk-Tiberi, B., Yan, Y., Chiu, J., et al. (62 authors, Kaggle and Google DeepMind, incl. O. Kelly, M. Lanctot, M. Risdal, O. Firat, M. Chen). *Game Arena: Strategic LLM Evaluation in Competitive Environments.* Technical report, arXiv:2609.31473 (25 Sep 2026; 31 pages) [authors added by fact-check from arXiv mailing mirrors]. Seen at: https://github.com/luohongk/Embodied-AI-Daily (`papers/LLM.md`)
29. Kelly, O. (Google DeepMind). *Advancing AI benchmarking with Game Arena* (page title: "Game Arena: Poker and Werewolf, and Gemini 3 tops chess") [headline corrected by fact-check]. Google blog, 2 Feb 2026. https://blog.google/innovation-and-ai/models-and-research/google-deepmind/kaggle-game-arena-updates/. Seen at: cached copy in https://github.com/youzhenxing/info_hub
30. Google. *Rethinking how we measure AI intelligence* (Kaggle Game Arena launch post), Google blog, 4 Aug 2025 [title and date added by fact-check]. https://blog.google/technology/ai/kaggle-game-arena/. Seen at: summary in https://github.com/franperezlopez/news (`index_2025_49.html`)
31. Google DeepMind. *game_arena* harness repository. https://github.com/google-deepmind/game_arena. Seen at: the same URL
32. Anthropic. *Lessons on AI agents from Claude Plays Pokemon* (YouTube video, 24 Apr 2025, https://www.youtube.com/watch?v=CXhYDOvgpuU [URL and date added by fact-check]; transcript). Seen at: https://github.com/Unson-LLC/anthropic-youtube
33. Gemini Team, Google (Comanici, G., et al.). *Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and Next Generation Agentic Capabilities.* Technical report, 2025, arXiv:2507.06261 [ID added by fact-check] (§4.1 and §8.2, Gemini Plays Pokémon). Seen at: https://github.com/ShiwenZhang00/AI_Model_Evaluation_on_L4 (`Documents/gemini_v2_5_report.txt`)
34. MC-Bench (Minecraft AI Benchmark). https://mcbench.ai ; GitHub org https://github.com/mc-bench. Seen at: https://github.com/mc-bench
35. White, I., Nottingham, K., Maniar, A., Robinson, M., Lillemark, H., Maheshwari, M., Qin, L., Ammanabrolu, P. *Collaborating Action by Action: A Multi-agent LLM Framework for Embodied Reasoning* (Mindcraft/MineCollab). arXiv:2504.17950 (2025). Seen at: https://github.com/kolbytn/mindcraft
36. Wang, G., Xie, Y., Jiang, Y., Mandlekar, A., Xiao, C., Zhu, Y., Fan, L., Anandkumar, A. *Voyager: An Open-Ended Embodied Agent with Large Language Models.* arXiv:2305.16291 (2023). Seen at: https://github.com/MineDojo/Voyager

---

## Verification log

Adversarial fact-check completed 2026-09-29. **Method.** WebSearch was unavailable: the session-wide budget of 200/200 was already spent before this check started. Every claim was therefore re-checked through independent routes:

- GitHub code search across all public repositories, looking for verbatim abstracts, BibTeX, arXiv mailing mirrors and paper lists that were *different* from the ones the dossier cited;
- WebFetch of github.com pages (commit logs, archive banners, READMEs);
- curl of raw.githubusercontent.com files;
- an independent re-extraction of the Akhtar et al. PMLR PDF text with pypdf.

Verdicts: **confirmed**, **corrected** (the claim needed a material fix), **refuted**, or **unverifiable**.

| ID | Verdict | Evidence (independent of the dossier's cited source where possible) |
|---|---|---|
| C1 | **confirmed** | The abstract text ("increasing concentration on fewer and fewer datasets within task communities … small number of elite institutions", 2015–2020) appears verbatim in mavenlin/ai_research_trends, truas/research_notes, brunomaga publications and DeepSurvey-Bench `a2REF.jsonl`. The NeurIPS 2021 D&B round-2 proceedings entry is in Doragd/Algorithm-Practice-in-Industry `nips2021.md`. The best-paper award appears in SarahRastegar/Best-Papers-Top-Venues and FeiSun/PaperReading. **Note:** "Papers With Code" is not in the abstract; that detail comes from secondary notes (dadadadawjb/honors). Fixed inline. |
| C2 | **confirmed** (medium) | The body sentence ("the majority of papers within most tasks use datasets that were originally created for other tasks … even though most tasks have created more datasets than they have imported") is quoted identically in two independent notes: wvrossem blog and truas/research_notes. Ruder's caption ("Over 50% of dataset usages can be attributed to 12 institutions … Gini coefficient has increased") appears in sebastianruder/sebastianruder and in a second copy (ShinAsakawa.github.io translation). Both are secondary quotes of the paper; the full paper was not read. |
| C3 | **confirmed** | Nature Communications 13:6793, the DOI, 3,765 benchmarks, "many benchmarks fail to find widespread utilization" and "versatility, breadth and real-world utility" appear in TTXS123OK (arXiv v4 journal-ref), EliasSchlie/thesis (PMID/PMCID), DeepSurvey-Bench and two 2026 papers' reference lists. **Version caveat:** arXiv v1 had 1,688 benchmarks, a different conclusion and Barbosa-Silva as first author (mavenlin/ai_research_trends 2022-03-09). Added inline. |
| C4 | **confirmed** | The abstract sentence appears verbatim in mavenlin, TatsuyaShirakawa/daily-arxiv-gatsby and the NeurIPS D&B 2021 OpenReview crawl (id 5Str2l1vmr-). It is absent from the accepted D&B 2021 list, so it stays an arXiv preprint. |
| C5 | **corrected** | Numbers confirmed by independent re-extraction of the PMLR PDF: 61 documents; 190 benchmarks; the ≥5-report rule; 60 benchmarks; 29 high or very high and 14 very high; 56 public vs 4 private; citations ρ = 0.22 (p = 0.12); report frequency ρ = 0.05 (p = 0.73); R²_Bayes = 0.884 ± 0.012; LiveBench S = 0.99 at about 79%; LiveCodeBench S = 0.77; default α = 0.5. The PMLR post confirms the title, all 37 authors, pp. 1602–1629 and the 43rd ICML. arXiv:2602.16763 confirmed via agents-radar HN digests. **Correction 1:** the 60 are *not* a pure "sustained-use" set. §3.1 adds (a) highly cited benchmarks found via the Semantic Scholar API and (b) hypothesis-driven additions from Google Scholar searches; the ≥5-report filter applies only to the developer-report candidates. **Correction 2:** the finding that "expert curation predicts resilience" is overstated. The authors call the curation comparison age-confounded (curation groups differ in age, p = 0.0017) and conclude only that it "may improve robustness"; curation is not among the regression's robust predictors (age and test-set size are). |
| C6 | **confirmed** (fact) | Table 3 re-read: none of the 60 is game-based. Framing corrected to "analysed set" per C5. The text-only and leaderboard filters are stated in §3.1, so the dossier's caveat stands. |
| C7 | **confirmed** | `docs/maintenance_mode.md` re-fetched, and the README banner was found independently via code search: "HELM entered maintenance mode on June 1, 2026 … no new evaluations will be added to the HELM leaderboards". The alternatives list (Evalchemy, Inspect AI Evals, Lighteval, LLM Evaluation Harness, Unitxt) is confirmed. |
| C8 | **confirmed** | Archive banner re-fetched: "archived by the owner on Apr 17, 2026" (3.2k stars, 5,893 commits, "more than 200" tasks, BBL = 24 tasks). The BBH abstract (23 tasks; 65%) appears verbatim in 17k+ code hits (e.g., the lm-evaluation-harness leaderboard README). **Side correction:** the dossier's remark that the README "was never updated after acceptance" is wrong, because the README's citation block cites TMLR 2023. Fixed inline. |
| C9 | **confirmed** | The HF blog markdown was re-fetched with curl and quotes match. The `_blog.yml` date is **1 Dec 2023**. "8 years of GPU time" refers to "the full update" when Winogrande, GSM8K and DROP were added ("a lot of it was taken by DROP"). The retirement date of 13 Mar 2025 is independently corroborated by a CSET report footnote citing HF discussion #1135 (copy in Juanesillo/codefest-ad-astra-2026) and by niftymonkey/pickai. |
| C10 | **confirmed** | Commit pages re-fetched: GTBench, latest 6 Sep 2024, README still says "Will be ready soon" twice; GameBench, 27 Jun 2024; SmartPlay, 11 Apr 2024 and archived 1 Jul 2026; lmgame-Bench (GamingAgent main), 12 Sep 2025. Also re-checked: clembench, 15 Apr 2026; BALROG, 9 Apr 2026; mc-bench org, newest update Sep 30, 2025. |
| C11 | **confirmed** | The Feb 2026 facts appear in the info_hub cache and in foragents/pppp606/HN archives dated 2026-02-02. The tech report arXiv:2609.31473v1 was found in four independent daily-arXiv mirrors (published_at 2026-09-25T16:20:55Z; 31 pages; 62 authors, first Bovard Doerschuk-Tiberi), with abstract "preventing performance saturation". **Reference fixes (not claim errors):** the Feb 2026 post's headline is "Advancing AI benchmarking with Game Arena"; the launch post is "Rethinking how we measure AI intelligence", 4 Aug 2025. |
| C12 | **confirmed** (claim), interpretation corrected | The passage (Joel Zhang; 28 Mar 2025; "modifications were made to the setup as difficulties arose"; 2 May 2025; 813 h; 406.5 h) appears verbatim in three further independent text copies (cfn0324/Pokemon-AI, ktolnos/presentations, visual-snow/seshat parse of arXiv 2507.06261). **Correction to the dossier's interpretation:** run 1 used *Gemini 2.5 Pro Exp 03-25* and run 2 used *Gemini 2.5 Pro Preview 05-06*. The halving therefore cannot be attributed to the harness "alone". Fixed in §2 and Implication 9. |
| C13 | **corrected** | Two independent transcript copies (Unson-LLC; ai-native-engineer/anthropic-mirror, video CXhYDOvgpuU, 24 Apr 2025) confirm both quotes. However, "So we included Claude Plays Pokemon as part of our Claude 3.7 Sonnet launch … the benchmark with all the lines" is said by the **host** (Alex, Claude Relations), not by the engineer (David, Applied AI). The "buying decision" line fits the engineer's turn in the alternation, but the transcripts have no speaker labels. Confidence lowered to medium; fixed inline. |
| C14 | **confirmed** (with version caveat) | Northcutt abstract verbatim (mavenlin; Semantic Scholar CSV); NeurIPS 2021 D&B per the official cleanlab/label-errors BibTeX. MMLU "57% … Virology" appears in both versions of the Gema et al. abstract; NAACL 2025 verified (2025.naacl-long.262). **Caveat:** "3,000 questions / 30 subjects" is arXiv v1; the later version reports 5,700 / 57 subjects and 6.49%. GSM1k: "up to 13%" (v1; Luvata/arxive and HuggingAGI mirrors) vs "up to 8%" (NeurIPS 2024; fzyzcjy list) confirmed. |

**Totals:** 12 confirmed (C12 with an interpretation fix), 2 corrected (C5, C13), 0 refuted, 0 unverifiable.

### Other corrections made in this pass

These fall outside C1–C14.

- **San Joaquin et al.** is an ICML 2025 *Technical AI Governance Workshop* paper, not a main-conference paper. Source: the arXiv comment.
- **LLM Chess:** the first author is **Sai Kolasani**, not Maxim Saplin. The full author list is taken from co-author N. Crispino's site.
- **Bean et al.:** the track is NeurIPS 2025 **Datasets and Benchmarks**.
- **TextArena:** the arXiv abstract says 57+ environments; the current README says 100+.
- **Dehghani et al.:** it was submitted to NeurIPS 2021 D&B but is not in the accepted list checked, so keep "arXiv preprint".
- **Mindcraft** repo moved to mindcraft-bots/mindcraft.
- **lmgame-Bench** has an OpenReview entry that appears in an ICLR 2026 atlas. Acceptance is unverified, so the venue stays arXiv.

### Reference-check summary

All **35 of 35** original entries in `refs/other_dead_benchmarks.json` were checked; none were skipped. One missing entry was added: clembench-2024, which the dossier cites (ref 22) but the JSON lacked. That gives 36 entries, all now `verified: true`, each with a `verify_note`.

No fabricated references were found. Problems fixed:

1. `saplin2025llmchess`: wrong first author and incomplete authors. Corrected to Kolasani et al.
2. `sanjoaquin2025deprecating`: venue implied ICML main conference. Corrected to the ICML 2025 TAIG workshop.
3. `kelly2026gamearena`: title was the SEO page title. The headline is "Advancing AI benchmarking with Game Arena".
4. `google2025gamearena`: placeholder title. Corrected to "Rethinking how we measure AI intelligence", 4 Aug 2025.
5. `anthropic2025pokemon`: the URL pointed to a different page (anthropic.com/news) rather than the transcribed video. Corrected to the YouTube URL.

Entries completed with verified details:

- `gema2024mmlu`: NAACL 2025, full authors, ACL Anthology URL.
- `hf2023drop`: date 1 Dec 2023.
- `openllm2025retired`: primary title, HF discussion URL and 13 Mar 2025 date.
- `gamearena2026report`: author list.
- `gemini2025report`: arXiv:2507.06261.
- `suzgun2023bbh`: full authors.
- `northcutt2021pervasive`: D&B track.
- `bean2025measuring`: D&B track.

**Residual single-source items (still secondary):**

- BetterBench stage scores (6.2/15; 9.6; MMLU 5.5; GPQA 11.0; r = 0.693);
- Bean et al.'s 46,114 / 2,189 funnel figures;
- the Akhtar arXiv-version 52/8 public/private split;
- the "Deprecating Benchmarks cites the Benchmark Lottery" remark.

Treat these as [S] until the primary PDFs are read.

# Brief B: The evaluation ecosystem (arenas, ARC-AGI, aggregators, lab adoption)

Evidence brief for Phase 2 (designing a new non-game benchmark). Compiled 2026-09-29 from four fact-checked dossiers: `notes/arenas_preference.md`, `notes/arc_agi.md`, `notes/aggregators_indices.md` and `notes/model_cards_adoption.md`. Where a dossier carries "[corrected by fact-check]" or a verification-log verdict, the corrected version is used here.

**Citation conventions.**
- `[key]` is a citation key from `research/refs/*.json`. Keys come from `arenas_preference.json`, `arc_agi.json`, `aggregators_indices.json` or `model_cards_adoption.json`.
- `[D:MCA]` marks a count derived in `model_cards_adoption.md` §A. That section builds a release × benchmark matrix from the headline tables of 34 releases by 7 developers (Dec 2024 to Sep 2026), cited there as `anthropic2025claude37` … `minimax2025m2`. The fact-check re-ran the counts and added 7 omitted releases: `anthropic2026fable51`, `anthropic2026sonnet55`, `google2025gemini3flashcard`, `google2026gemini31flashlitecard`, `google2026gemini35flashlitecard`, `openai2025gpt52codex` and `openai2026gpt54mininano`. Counts are exact for the stated sample and should be cited as sample-specific.
- `(S)` marks a claim resting on secondary sources only. `(I)` marks this brief's interpretation.

---

## Headline findings

1. **Adoption is decided by the ecosystem layer, not by the paper.**
   - The strongest measured predictor of lab uptake is a *trusted third-party leaderboard that runs or verifies frontier models*, so that competitors' numbers are citable.
     - Gemini 3 Pro's evaluation document sources non-Gemini numbers from "ARC Prize Verified", Scale's HLE leaderboard, Artificial Analysis, matharena.ai, andonlabs.com and Kaggle [google2025gemini3eval].
     - Sonnet 5.5 cites "Official AA-Briefcase v1.1 and GDPval-AA v2.1 scores from Artificial Analysis" [anthropic2026sonnet55].
   - GDPval went from 1/14 frontier-lab headline tables in 2025 to 12/13 in 2026 after Artificial Analysis turned it into GDPval-AA [D:MCA; anthropic2026opus55].
   - Academic citations do not predict adoption.
     - Across 39 benchmarks, citation counts correlate *negatively* with 2025–26 headline adoption (ρ = −0.34, exploratory, confounded by age) [D:MCA; evaleval2026saturationdata].
     - Appearing in technical reports is unrelated to saturation (ρ = 0.05, p = 0.73) [akhtar2026plateau].
2. **Everything saturates. Brands survive by versioning.**
   - ARC-AGI-2 went from single digits at launch (Mar 2025) to 95.0% at $1.12/task (Sep 2026) [kamradt2025arcagi2launch; alloevil2026tracker; latere2026field].
   - ARC-AGI-3 went from under 1% (Mar 2026) to 99.9% under a provider harness (Sep 2026) [latere2026field; kamradt2026astra].
   - None of the 8 benchmark families in Claude 3.7 Sonnet's table (Feb 2025) appears in any Anthropic headline table from Opus 4.8 (May 2026) onward [anthropic2025claude37; anthropic2026opus48; anthropic2026opus5; anthropic2026opus55].
   - Every family with long 2026 headline presence is a versioned brand (Terminal-Bench, OSWorld, ARC-AGI, GDPval-AA, Finance Agent). Humanity's Last Exam (HLE) is the only unversioned exception [D:MCA].
3. **Lab headline tables are concentrated, fast-churning and product-aligned.**
   - 34 releases name 110 benchmark families. 48 (44%) appear exactly once, and only 11 appear in at least a third of releases [D:MCA]. In the 41-release expansion: 112 families, 40% single-release, 9 families at ≥1/3.
   - The agentic share of frontier headline rows rose 23% → 35% → 61% → 76% from 2025H1 to 2026H2. The expanded sample gives 23/36/56/77%, and a stricter classification gives 23/33/54/74% [D:MCA].
4. **Games are absent from lab headline tables. The lead's diagnosis holds here.**
   - Zero conventional game benchmarks appear in 34 headline tables [D:MCA].
   - Pokémon appears only as a demo [anthropic2025claude4; gemini2025gemini25; anthropic2026sonnet55].
   - Google did not put its own Kaggle Game Arena in the Gemini 3, 3.1 or 3.5 tables [D:MCA].
   - The only game-like rows are ARC-AGI-3 and Vending-Bench 2. ARC-AGI-3 rode an established, philosophy-driven brand (I).
5. **The arena recipe distributes; it does not validate.**
   - Chatbot Arena grew from ~240K votes (ICML 2024) to "3M+" by April 2025 [chiang2024chatbotarena; lmarena2025twoyear].
   - It raised $150M at a $1.7B valuation in January 2026 [techcrunch2026seriesa] (S).
   - Its scores reward length and tone [li2024stylecontrol; chen2025sentimentcontrol], can be gamed by private variants [singh2025leaderboardillusion], and can be moved by hundreds of rigged votes [min2025voterigging].
   - Arena Elo is announced at launches but is a row in 0/34 headline tables [D:MCA].
6. **ARC-AGI's durability comes from theory plus institution, not format.**
   - A written construct (skill-acquisition efficiency) [chollet2019measure] is paired with human calibration, tiered data, exact scoring, a cost axis, a nonprofit steward with a testing policy, prize money tied to open-sourcing, and annual versioning [arcprize2026policy; chollet2026arcprize2025].
   - ConceptARC uses the same format with tighter concept control but has none of the institutions, and it stayed a research instrument [moskvichev2023conceptarc] (I).
   - Philosophy did not prevent saturation. ARC's 2025 claim that "Log-linear scaling is insufficient to beat ARC-AGI-2" [chollet2026arcprize2025] was overtaken within about a year [measured2026].
7. **First-generation academic aggregators died; harnesses and independent indices thrive.**
   - The HF Open LLM Leaderboard retired on 13 Mar 2025 so as not to "encourage people to hill climb irrelevant directions" [fourrier2025ollretire] (S).
   - HELM entered maintenance mode on 1 June 2026 [crfm2026helmmaint].
   - OpenAI froze simple-evals in July 2025 [openai2025simpleevals]. The harnesses underneath (lm-eval, Inspect) keep growing [gao2024harness; aisi2024inspect].
   - Artificial Analysis (AA) removed seven benchmarks from its index between Aug 2025 and Sep 2026 [aa2026method].
8. **Freshness and privacy slow saturation but do not stop it.**
   - Private test sets (N = 4) saturate like public ones (N = 56) [akhtar2026plateau].
   - "Live" LiveBench has S_index 0.99, with a top-5 spread of 1.09 points at ~79% [akhtar2026plateau].
   - ARC reports "knowledge overfitting" through IID public/private splits [chollet2026arcprize2025].
9. **Comparability is now threatened more by harness, judge and price than by items:** a 36-point ARC-AGI-3 harness gap for one model at equal effort [kamradt2026astra]; up to 11–15% scaffold effects on SWE-bench Verified [epochWhyBenchHard]; a 79.0 vs 49.1 judge swing on Arena-Hard v2 [arenahardauto2025repo]; one o3 run priced at $200 or $26 per task [kamradt2025arcagi2launch; chollet2024o3blog]. Details in F7.

---

## Success factors (with evidence)

**S1. A citable, independent leaderboard that runs every frontier model.** *Strength: strong.*
- Labs source competitor columns from third-party boards: ARC Prize Verified, the Scale HLE leaderboard, Artificial Analysis, Zapier's AutomationBench leaderboard [google2025gemini3eval; anthropic2026opus55; anthropic2026sonnet55].
- GDPval went 1/14 → 12/13 once it had an AA runner [D:MCA].
- Counter-case: FrontierMath is hosted by Epoch but appears in 4/34 releases, all of them OpenAI's [D:MCA]. A third-party host is not enough when the sponsor relationship is single-lab (I).

**S2. Alignment with what labs are selling.** *Strength: strong.*
- The agentic share of headline rows went 23% → 76% [D:MCA].
- SWE-bench Pro went 1/14 → 9/11 frontier tables (2025 → 2026H1) [D:MCA].
- Terminal-Bench was in Anthropic's table on day one (Claude Opus 4, 43.2%) [anthropic2025claude4] and in 11/11 frontier releases in 2026H1 [D:MCA].

**S3. Versioned brand continuity.** *Strength: strong.*
- Terminal-Bench 1.0 → 2.0 → 2.1 → 4.0; OSWorld → Verified → 2.0 → 2.1; ARC-AGI-1 → 2 → 3; GDPval → GDPval-AA → v2 → v2.1 [D:MCA].
- A new version of an already adopted brand reaches headline tables within weeks. Terminal-Bench 2.0 was released 7 Nov 2025 and appeared in Opus 4.5 on 24 Nov 2025 [D:MCA; anthropic2025opus45].
- ARC describes its versioning as "a real world refinement loop" [chollet2026arcprize2025].

**S4. A headroom window at adoption.** *Strength: moderate-strong.*
- ARC-AGI-2 was adopted about 8 months after launch, when scores reached 31–38% [google2025gemini3eval; anthropic2025opus45].
- ARC-AGI-3 was adopted when Opus 5 reached 30.2%, against 1.5% for its predecessor [anthropic2026opus5].
- Benchmarks are dropped at ceiling: AIME at 100% [openai2025gpt52], and none of the verified 2026 frontier tables reports AIME [D:MCA].

**S5. An explicit construct theory with stated limits.** *Strength: moderate. It works for durability and culture, not against saturation.*
- Chollet defines intelligence as skill-acquisition efficiency. He argues that unlimited priors or data let experimenters "'buy' arbitrary levels of skills" [chollet2019measure].
- He lists his own weaknesses up front, e.g. "Test validity is not established" [chollet2019measure].
- The theory told ARC how to evolve: a cost axis in Dec 2024 [chollet2024o3blog], human calibration in 2025 [kamradt2025arcagi2launch], and human-relative action efficiency in 2026 [arcprize2026docs].
- The lead's "underlying philosophy" credit is well supported for ARC; for Design Arena the evidence is secondary only [designarena2025] (S).

**S6. Human calibration of items.** *Strength: moderate.*
- ARC-AGI-2 tested over 400 members of the public. Every task was solved by ≥2 people in ≤2 attempts, at a human cost of $17/task [kamradt2025arcagi2launch].
- ARC-AGI-3 tested 458 participants, and every environment was beaten by ≥2 of them [kamradt2026humandata].
- Four frontier labs reported ARC-AGI in 2025 model cards [chollet2026arcprize2025].

**S7. Freshness by construction.** *Strength: moderate. It is necessary but not sufficient.*
- About 75% of daily Arena prompts are new, and fewer than 1% appear in popular benchmarks (355,575 battles) [dunlap2025freshness].
- Arena's policy gives contamination as the explicit design reason [lmarena2024policy].

**S8. A two-sided incentive loop, for volume.** *Strength: strong for engagement, weak for lab headline adoption.*
- Users get free, anonymous access to frontier and pre-release models [lmarena2025twoyear].
- Labs get pre-release testing (300+ tests by April 2025) and a share of vote data [lmarena2025twoyear].
- The 2025 rebuild aimed to be "more fun to use" [lmarena2025company].
- Arenas where laypeople can judge outputs in seconds (Text, WebDev, Design) grew fastest. Arenas needing expert checking (Search citations, Copilot correctness) grew more slowly [vichare2025webdevarena; miroyan2026searcharena; chi2025copilotarena] (I).

**S9. Openness and auditability.**
- Arena released code, 1.5M prompts and vote data [lmarena2025twoyear], and from 1 July 2025 promises 100% of leaderboard votes and model identities [lmarena2024policy].
- ARC publishes outputs, replays and verified-only boards [chollet2024o3blog; arcprize2026community].
- Epoch publishes CC-BY data with standard errors, and accepted an externally found aggregation error [pickai2026notes] (S).
- Open data is what made independent audits possible, e.g. the Leaderboard Illusion [singh2025leaderboardillusion] (I).

**S10. Harness integration and low running cost.**
- HELM's maintenance notice sends users to Inspect, lm-eval, Lighteval, Evalchemy and Unitxt [crfm2026helmmaint].
- lm-eval is "the backend for 🤗 Hugging Face's popular Open LLM Leaderboard" [gao2024harness]. Inspect ships "over 200 pre-built evaluations" [aisi2024inspect].
- Expensive suites get skipped. Kimi K2 omitted data points "due to prohibitively expensive evaluation costs" [moonshot2025kimik2].

**S11. Stewardship with a written testing policy.**
- ARC runs a single $10k-capped run per model and publishes within 30 days with no sponsor embargoes. It tests only commercial APIs with more than $10M/month gross revenue, and has an academic panel (Gureckis, Mitchell, Misra) [arcprize2026policy].
- AA publishes a changelog and a 95% CI of less than ±1% [aa2026method].

---

## Failure factors (with evidence)

**F1. Ceiling saturation, in months.**
- AI Index 2026: "Evaluations intended to be challenging for years are saturated in months" [hai2026aiindex].
- MMMU, GPQA and SWE-bench rose 18.8, 48.9 and 67.3 points within a year of introduction [hai2025aiindex].
- Headline lifetimes of static benchmarks are about 7–30 months [D:MCA].
- Time to human parity fell from ~15–20 years (MNIST) to ~1 year (GLUE) [kiela2021dynabench].

**F2. Too few items to separate the frontier.**
- Test-set size is one of the two most consistent predictors of saturation [akhtar2026plateau].
- MT-Bench (80 questions) had 22.6% separability, against 87.4% for Arena-Hard [li2024arenahardblog].
- Terminal-Bench 2.0 (n = 82) was flagged as very highly saturated (S = 0.97) one month after release [evaleval2026saturationdata].

**F3. Style over substance in preference signals.**
- Length is the dominant style factor (0.249 vs ≤0.031 for markdown) [li2024stylecontrol].
- Positive tone raises win rates [chen2025sentimentcontrol].
- Assertiveness skews how annotators perceive factuality [hosking2024humanfeedback].
- LLM-judge preferences do not track safety or knowledge measures [feuer2025styleoutweighs].
- Search Arena users reward citation count, yet "humans do not always check citations" [miroyan2026searcharena].

**F4. Gaming through selective disclosure and manipulation.**
- Meta privately tested 27 variants before Llama 4 [singh2025leaderboardillusion]. The public Maverick ranked 32nd, while the preference-tuned variant ranked #2 [techcrunch2025vanillamaverick; verge2025maverick] (S).
- Hundreds of rigged votes can move ranks [min2025voterigging].
- Model identity can be inferred with >95% accuracy [huang2025adversarialleaderboards].
- A P2L router reached #1 on Arena, i.e. a composed system rather than a better base model [frick2025p2l].

**F5. Judge dependence and exploitable automatic proxies.**
- Changing the judge swings Gemini-2.5 from 79.0 to 49.1 [arenahardauto2025repo]. LLM judges favour their own generations [panickssery2024selfpreference].
- A constant "null model" reaches an 86.5% LC win rate on AlpacaEval 2.0 [zheng2025cheating].
- About 33% of the AA index weight flows through LLM judges [strasser2026critique] (S, L-M).

**F6. Contamination through distribution, not items.**
- IID public and private splits let models learn ARC as a domain (I). Gemini 3 Deep Think used ARC colour mappings without being prompted [chollet2026arcprize2025]. This is a single-excerpt diagnosis that ARC "cannot precisely quantify".
- About 10,000 score reports were made against a 100-task private set [chollet2024arcprize].
- OpenAI retired SWE-bench Verified. Of 138 audited problems, 59.4% had material flaws, and frontier models could reproduce "the gold patch, or verbatim problem statement specifics for certain tasks" [openai2026swebvretire].

**F7. Harness, scaffold, implementation and price non-comparability.**
- ARC-AGI-3 differs by 36 pp across harnesses at the same effort [kamradt2026astra; arcprize2026arcagi3benchmarking].
- The same MMLU setup gives 0.637 (HELM) vs 0.488 (EleutherAI harness) [hf2023ollmmlu].
- SWE-bench Verified: OpenAI reported on a 477-task subset, Anthropic on all 500 [openai2025o3; openai2025gpt5; D:MCA].
- Cost-per-task is a pricing artefact unless the price table is pinned [chollet2024o3blog].

**F8. Maintenance cost and dependence on a small team.**
- HELM: external APIs "may change in reverse-incompatible ways" [crfm2026helmmaint].
- LiveBench promised monthly releases but shipped 11 in ~24 months [livebench2026repo].
- The AlpacaEval and WildBench boards stalled at mid-2024 models [li2023alpacaeval; lin2025wildbench].

**F9. Fragmentation into incomparable scores.** HELM split into many sub-leaderboards with no single number labs could quote [liang2023helm; crfm2026helmmaint] (I). This is the aggregator-scale analogue of the lead's "three incomparable scores" critique of Qi Town.

**F10. Relative ratings that drift.**
- Bradley-Terry scores are anchored to the current pool, so a 1500 in 2026 cannot be compared with a 1217 in 2023 [lmsys2023btupdate] (I).
- 205 of 243 public Arena models were silently deprecated [singh2025leaderboardillusion] (S body figure).
- AA's minor version bumps may change evaluations, weightings and anchors [pickai2026notes] (S).

**F11. Conflicts of interest and capture risk.**
- Arena sells evaluation services to labs it ranks [techcrunch2026seriesa] (S).
- ARC's donors include AI labs; independence rests on written recusal rules [arcprize2026policy].
- FrontierMath's OpenAI funding is flagged in an LLM-generated audit [ihle2026provenance] (L).

**F12. Pre-emption by better-resourced near-duplicates.**
- WildBench (ICLR 2025 spotlight) ended up absorbed into HELM rather than running its own board. It was crowded out by Arena-Hard, which carried the Arena brand [lin2025wildbench; li2025arenahard] (I).
- Google DeepMind/Kaggle's Game Arena was announced on 4 Aug 2025, the same week as two of the lead's game benchmarks [siliconangle2025kaggle; `notes/user_failed_a.md`].
- Aggregators now own their evaluations (AA-LCR, AA-Omniscience, AA-Briefcase), which narrows the space for independents [aa2026method] (I).

**F13. Self-reports presented as consensus.** The AI Index "operates under the assumption that the scores reported by companies are accurate and factual" [hai2025aiindex].

---

## Quantitative facts worth citing

| Fact | Number | Date | Source key | Confidence |
|---|---|---|---|---|
| Chatbot Arena votes in its ICML paper | >240K | 2024 | chiang2024chatbotarena | H |
| Arena scale | "3M+" votes, 400+ models, 300+ pre-release tests, 1.5M prompts released | Apr 2025 | lmarena2025twoyear | H ("3M+" is in the title only) |
| Daily fresh Arena prompts; overlap with benchmarks | ~75%; <1% (355,575 battles) | May–Dec 2024 data | dunlap2025freshness | H |
| Arena Series A | $150M at $1.7B post-money; >$30M annualised consumption revenue | Jan 2026 | techcrunch2026seriesa | M (S) |
| Length coefficient in style control | 0.249 vs ≤0.031 for markdown features | Aug 2024 | li2024stylecontrol | H |
| Private variants tested by Meta pre-Llama-4 | 27 | Apr 2025 | singh2025leaderboardillusion | H (abstract) |
| Arena data share | Google 19.2%, OpenAI 20.4%; 83 open-weight models 29.7% combined | Apr 2025 | singh2025leaderboardillusion | H (estimate) |
| Public Llama-4-Maverick rank | 32nd (experimental variant #2) | Apr 2025 | techcrunch2025vanillamaverick | M |
| Votes needed to shift Arena rank | "hundreds" (omnipresent rigging); ~1,000 (offline simulation) | 2025 | min2025voterigging; huang2025adversarialleaderboards | H |
| Surge AI audit of Arena votes | disagreed with 52% of 500 (39% strongly) | ~Jan 2026 | surge2026lmarena | M (vendor COI) |
| Separability with 95% CIs | MT-Bench 22.6% vs Arena-Hard v0.1 87.4% | Apr 2024 | li2024arenahardblog | H |
| Null-model win rate, AlpacaEval 2.0 LC | 86.5% | 2024–25 | zheng2025cheating | H |
| Judge swing, Arena-Hard v2 | Gemini-2.5 79.0 (Gemini judge) vs 49.1 (GPT-4.1 judge) | Apr 2025 | arenahardauto2025repo | H |
| WebDev Arena deduplication | 103,096 → 61,473 votes; #1 score 1362.94 → 1311.40 | Mar 2025 | vichare2025webdevarena | H |
| Copilot Arena position bias | 82% of accepted completions were the top one | Nov 2024 | chi2024copilotarenablog | H |
| ARC-AGI-1 brute-forceability | 49% of private set solved by the 2020 entries' ensemble; deep learning ≤1% | 2020 (reported 2024) | chollet2024arcprize | H |
| ARC private-set probing | ~10,000 score reports vs 100 tasks | by 2024 | chollet2024arcprize | H |
| ARC Prize participation | 2024: 1,430 teams / 17,789 entries; 2025: 1,455 / 15,154; papers 47 → 90 | 2024–25 | chollet2024arcprize; chollet2026arcprize2025 | H |
| o3-preview on ARC-AGI-1 semi-private | 75.7% ($2,680, 6 samples) vs 87.5% ($456,000, 1,024 samples, ~172× compute) | Dec 2024 | chollet2024o3blog | H |
| Same o3 configuration, cost per task | $200 (o1-pro pricing) vs $26 (o3-pro pricing) | Mar / Dec 2025 | kamradt2025arcagi2launch; chollet2024o3blog | H |
| ARC-AGI-2 human calibration | >400 people; ≥2 solvers per task; $17/task; individual average 60% (launch table) or 66% (README) | Mar 2025 | kamradt2025arcagi2launch; arcprize2025arcagi2repo | H |
| Individual human average, ARC-AGI-1 eval (H-ARC) | 64.2% (1,729 people, 3 attempts) vs panel 98% | 2024 | legris2024harc; broadbent2025pareto | H |
| Labs reporting ARC-AGI in 2025 model cards | 4 (Anthropic, Google DeepMind, OpenAI, xAI) | 2025 | chollet2026arcprize2025 | H (ARC's own statement) |
| ARC-AGI-2 Kaggle (open, compute-capped) vs frontier API | 24.03% at $0.20/task vs 54% (end 2025) → 95.0% at $1.12/task | 2025 → Sep 2026 | chollet2026arcprize2025; alloevil2026tracker | H / M-H |
| First crossing of ARC-AGI-2's 85% line | GPT-5.5 at 85%, ~13 months after launch | Apr 2026 | measured2026 | M |
| ARC-AGI-3 harness gap (GPT-6 Astra) | 62.7% standard vs 98.6% provider adapter (both max effort); 99.9% (high) | Sep 2026 | kamradt2026astra | H (translation) |
| ARC-AGI-3 human study | 458 participants (one digest says 486) | Apr 2026 | kamradt2026humandata | H |
| Headline-table concentration | 110 families in 34 releases; 48 (44%) single-release; 11 in ≥1/3 | Dec 2024–Sep 2026 | D:MCA | H for this sample |
| 2025 staples in frontier-3 tables | AIME 13/14 → 0/13; MMMU 11/14 → 0/13; GPQA 14/14 → 6/13; SWE-bench Verified 13/14 → 4/13 | 2025 → 2026 | D:MCA | H (sample); expanded 14/16 → 0/18, 11/16 → 0/18, 15/16 → 8/18, 14/16 → 4/18 |
| Agentic share of frontier headline rows | 23 → 35 → 61 → 76% (expanded 23/36/56/77) | 2025H1 → 2026H2 | D:MCA | M |
| Anthropic consecutive-table retention | 0.75–1.00 (2025) → 0.33–0.42 (mid/late 2026) | 2025–26 | D:MCA | H |
| GDPval / GDPval-AA uptake | 1/14 → 12/13 frontier tables | 2025 → 2026 | D:MCA | H |
| Conventional game benchmarks in headline tables | 0/34 | 2025–26 | D:MCA | H |
| Arena Elo as a headline-table row | 0/34 | 2025–26 | D:MCA | H |
| Citations vs lab adoption | Spearman ρ = −0.34 (p ≈ 0.03, n = 39) | 2026 | D:MCA; evaleval2026saturationdata | L-M |
| Benchmarks with high saturation | 29 of 60; report frequency vs saturation ρ = 0.05 (p = 0.73) | ICML 2026 | akhtar2026plateau | H |
| LiveBench score compression | S_index 0.99; top-5 range 1.09 pts at ~79% | 2026 | akhtar2026plateau | H |
| LiveBench actual release cadence | 11 releases in ~24 months (claimed monthly) | Jun 2024–Jun 2026 | livebench2026repo | H |
| SWE-bench Verified audit | 59.4% of 138 audited hard problems flawed; SOTA 74.9 → 80.9% in 6 months | Feb 2026 | openai2026swebvretire | M-H (mirror) |
| Scaffold effect on SWE-bench Verified | up to 11% (GPT-5) and 15% (Kimi K2 Thinking) | Dec 2025 | epochWhyBenchHard | M-H |
| MMLU implementation gap (LLaMA-65B) | 0.637 HELM / 0.636 original / 0.488 EleutherAI harness | Jun 2023 | hf2023ollmmlu | H |
| AA Intelligence Index | 646 models; 95% CI < ±1%; v4.3 weights Agents 30 / Coding 20 / General 30 / Science 20 | Sep 2026 | aa2026method | M-H (capture) |
| AI Index frontier convergence | top vs 10th model gap 11.9% → 5.4%; 4 companies within 25 Elo | 2025; 2026 | hai2025aiindex; hai2026aiindex | M-H / M |
| Time to human parity (Dynabench Fig. 1) | ~15–20 years (MNIST, Switchboard) → ~1 year (GLUE, SQuAD 2.0) | 2021 | kiela2021dynabench | M (figure reading) |

---

## Case vignettes

**V1. The chatbot that topped the arena was not the one that shipped (April 2025).**
- Meta launched Llama 4 claiming Maverick beat GPT-4o on LMArena, where it ranked #2 [verge2025maverick] (S).
- The entry was "Llama-4-Maverick-03-26-Experimental", "optimized for conversationality". LMArena said Meta's "interpretation of our policy did not match what we expect from model providers" [verge2025maverick] (S).
- The public release ranked 32nd [techcrunch2025vanillamaverick] (S).
- Weeks later, the Leaderboard Illusion counted 27 private Meta variants tested before release [singh2025leaderboardillusion].
- LMArena's own sentiment control singled out the experimental variant as one that falls once tone is controlled [chen2025sentimentcontrol].
- LMArena disputed the magnitude of the effect (~+11 Elo) [lmarena2025response], then added "provisional" labels, a retirement list and full vote-data release [lmarena2024policy].
- Lesson: the scored artifact must be the shipped artifact.

**V2. A constant string outscores GPT-4o (2024–25).**
- AlpacaEval's length-controlled version raised correlation with Arena to 0.98 [dubois2024lcalpacaeval].
- A "null model" that returns one adversarially crafted constant response now sits on the official AlpacaEval 2.0 board at an 86.5% LC win rate, far above gpt-4o-2024-05-13 at 57.5 [zheng2025cheating; li2023alpacaeval].
- Lesson: validation against human rankings at launch does not protect an LLM-judged benchmark from adversarial optimisation.

**V3. $456,000 for 11.8 points: how ARC got a cost axis (Dec 2024).**
- OpenAI's o3-preview scored 75.7% on ARC-AGI-1's semi-private set with 6 samples, and 87.5% with 1,024 samples at about 172× the compute ($456,000 total) [chollet2024o3blog].
- It had been trained on 75% of the public training set [chollet2024o3blog].
- ARC's response: "efficiency (e.g., compute cost) is now a required metric" [chollet2024o3blog].
- The same run was later listed at $200/task and at $26/task, depending on which price schedule was assumed [kamradt2025arcagi2launch; chollet2024o3blog].
- Lesson: efficiency must be reported in pinned prices *and* raw tokens.

**V4. One model, two harnesses, 36 points (September 2026).**
- ARC-AGI-3 launched in March 2026 with frontier AI below 1% [latere2026field].
- Six months later, GPT-6 Astra scored 62.7% under ARC's standard harness and 98.6% under a provider-designed harness at the same max effort; its best run reached 99.9% [kamradt2026astra].
- Astra "built its own tools for each game" [kamradt2026astra].
- ARC now reports both harnesses and says they "answer different evaluation questions" [arcprize2026policy].
- ARC's own caveat is that ARC-AGI-3 is "deterministic and closed" and does not represent real-world complexity [kamradt2026astra].
- Nineteen days after the Astra result, Anthropic's Opus 5.5 table and system card contain no ARC-AGI row [anthropic2026opus55; anthropic2026opus55card] (M). This is consistent with labs dropping benchmarks at ceiling (I).

**V5. The leaderboard that retired itself (March 2025).**
- Hugging Face's Open LLM Leaderboard was the canonical open-model ladder, powered by lm-eval [gao2024harness].
- In June 2023 it discovered that LLaMA-65B's MMLU score was 0.637 or 0.488 depending on the implementation [hf2023ollmmlu].
- It replaced all six v1 tasks in June 2024 [hf2024ollv2].
- In March 2025 it retired, because it "could encourage people to hill climb irrelevant directions" [fourrier2025ollretire] (S).
- HELM followed into maintenance mode in June 2026 [crfm2026helmmaint]. The harnesses underneath both lived on [gao2024harness; aisi2024inspect].
- Lesson: infrastructure outlives curation.

**V6. From lab benchmark to universal line item via a third party (2025–26).**
- OpenAI's GDPval used blinded expert grading and appeared in only one frontier table in 2025, OpenAI's own GPT-5.2 [D:MCA; openai2025gpt52].
- Artificial Analysis rebuilt it as GDPval-AA, an automated LLM-judge Elo leaderboard [aa2026method].
- By 2026 it was in 12 of 13 frontier-lab headline tables [D:MCA]. Anthropic reported that "Artificial Analysis ran GDPval-AA … on a pre-release deployment" [anthropic2026sonnet55].
- Contrast: FrontierMath, Epoch-hosted but tied to one sponsor, appears in OpenAI tables only [D:MCA].

**V7. The retirement letter (February 2026).**
- OpenAI co-built SWE-bench Verified in 2024. By 2026 it "became a standard metric reported in frontier model releases" [openai2026swebvretire].
- On 23 Feb 2026 OpenAI stopped reporting it. It found that 59.4% of 138 audited hard problems had material flaws, and that frontier models could reproduce gold patches or verbatim problem details [openai2026swebvretire].
- SOTA had moved from 74.9% to 80.9% in six months [openai2026swebvretire].
- SWE-bench Pro rose from 1/14 frontier tables to 9/11 (2026H1). OpenAI itself had adopted it before the letter [D:MCA; openai2025gpt52].
- Lesson: public-provenance items plus RL-era training shorten benchmark lifetimes. Retirement is now lab-driven.

---

## Tensions and disagreements in the evidence

1. **Consumer fun vs lab adoption.**
   - The arena loop's "fun" drives huge volume [lmarena2025twoyear; lmarena2025company].
   - Yet Arena Elo is a row in 0/34 lab headline tables [D:MCA].
   - Kaggle Game Arena, arguably the most spectator-friendly format, is absent from Google's own tables [D:MCA].
   - The lead's "not fun for consumers" diagnosis explains arena engagement, not lab reporting. The adoption predictors are third-party runners, product alignment and headroom [D:MCA].
2. **Philosophy vs durability.**
   - ARC's theory made it a cultural reference and let it evolve [chollet2019measure; chollet2026arcprize2025].
   - But ARC-AGI-2 was saturated about 18 months after launch [alloevil2026tracker]. The theory's efficiency claim failed once cost fell below the $17/task human reference [kamradt2025arcagi2launch] (I).
   - Same-format ConceptARC, without institutions, stayed niche [moskvichev2023conceptarc] (I).
   - Philosophy looks necessary for identity but not sufficient for adoption.
3. **Private sets.**
   - SEAL, Vals and ARC use private or semi-private tiers as anti-contamination measures [scale2024seal; vals2026index; arcprize2026policy].
   - Akhtar et al. find no saturation difference (private N = 4, public N = 56) [akhtar2026plateau]. The private sample is tiny.
4. **Small n: cheap vs unresolvable.**
   - Small sets were adopted *because* they were cheap: GPQA with 198 items, SWE-bench Verified with 500 [D:MCA] (I).
   - Test-set size predicts saturation [akhtar2026plateau], and MT-Bench's 80 items could not separate models [li2024arenahardblog].
5. **Human baselines are not one number.**
   - ARC's "human panel" (≥2 solvers; 98% on ARC-AGI-1 semi-private [broadbent2025pareto]) vs individual averages: 64.2% on ARC-AGI-1 eval with 3 attempts [legris2024harc], 60% or 66% on ARC-AGI-2 [kamradt2025arcagi2launch; arcprize2025arcagi2repo].
   - Crowd raters disagree with expert auditors on 52% of Arena votes [surge2026lmarena] (vendor COI).
   - The ARC-AGI-3 baseline was redefined three weeks after launch [arcprize2026docs].
6. **Leaderboard Illusion vs LMArena.**
   - "29.7% share of data for 83 open models" and "40.9% of battles involving an open model" measure different quantities [singh2025leaderboardillusion; lmarena2025response].
   - The 112% gain is on Arena-Hard (static, LLM-judged), not human Arena [lmarena2025response].
   - Neither side refutes the other.
7. **Figures that disagree across sources.**
   - Arena's "50 million votes" (all modalities, since May 2025) is a company claim that is not comparable with other counts (https://raw.githubusercontent.com/Amal-David/docingest/main/server/storage/docs/lmarena.ai/documentation_2026-01-18T14:34:01.052Z.md) (S).
   - Other discrepancies in the evidence: ARC-AGI-2's training set is given as 400 or 1,000 tasks [chollet2026arcprize2025; arcprize2025arcagi2repo]; GPT-5.6 Sol's ARC-AGI-1 score as 97.5 or 96.5 depending on the card [anthropic2026opus5card; anthropic2026fable51card]; the ARC-AGI-3 participant count as 458 or 486 [kamradt2026humandata].
8. **Independence vs funding.**
   - ARC's refusal of sponsor embargoes coexists with lab donors [arcprize2026policy].
   - Arena's "neutral, open" promise [lmarena2025company] coexists with selling evaluations to ranked labs [techcrunch2026seriesa] (S).
   - AA reweighting drew an unsubstantiated "paid off" allegation [pickai2026notes] (S).
9. **Echo chambers in the meta-evidence itself.**
   - Two "independent audits" cited in the aggregator literature are LLM-generated [ihle2026provenance; maxizm2026aaaudit].
   - The AI Index 2026's "error rates up to 42%" is precision@50 of a flagging method, not a benchmark-wide invalid rate [hai2026aiindex].
   - A summarising tool fabricated an AA changelog during this project's own research (`notes/aggregators_indices.md`, Verification log).
   - Human-authored items are also flawed (59.4% of audited SWE-bench Verified problems [openai2026swebvretire]). "Human vs AI-generated" is therefore less decisive than "audited vs unaudited" (I).
10. **Framework vs ladder.**
    - The lead is right that frameworks do not become ladders: HELM fragmented and froze [crfm2026helmmaint].
    - But frameworks survive as *harness infrastructure* [gao2024harness; aisi2024inspect]. A benchmark shipped as a harness task keeps a quiet afterlife: MastermindEval was merged into lm-eval as 6 tasks [lmevalMastermind].

---

## Implications for a new non-game benchmark

Each item below is interpretation (I), traced to the evidence above.

1. **State the construct theory and known flaws on day one** (S5). Borrow ARC's candour ("Test validity is not established") [chollet2019measure]. Show *discriminant* validity against the Epoch Capabilities Index (ECI), a single latent capability scale anchored at Claude 3.5 Sonnet = 130 and GPT-5 = 150 [epoch2026ecipublic; ho2025rosetta]. Include anchor models so scores link to the ECI and are not "incomparable".
2. **Score verifiable outcomes, not raw preference** (F3, F5). Use exact or executable checks. If preference is used, collect it only among verified-correct outputs and model style covariates, as Arena's style control does [li2024stylecontrol]. If LLM judges are unavoidable, pin, version and rotate them across model families, and publish judge-sensitivity [arenahardauto2025repo].
3. **Size for resolution** (F2). Choose n so that top-model gaps exceed their standard error, following the Akhtar S_index logic [akhtar2026plateau]. Publish SEs or CIs with a single headline number plus category slices [aa2026method; lmsys2023btupdate].
4. **Build renewal into the generator, avoiding IID public/private splits** (F6). Draw fresh items per window. Keep public dev items structurally distinct from held-out items [chollet2026arcprize2025]. Pre-announce a version cadence of about 4–6 months under one stable name [D:MCA]. Ship v1 at about 10–40% frontier accuracy to open a headroom window [D:MCA].
5. **Tier the data, but do not rely on privacy alone.** Use public / semi-private (zero data retention) / private tiers with an agreement-gap alarm [arcprize2026policy], and assume saturation anyway [akhtar2026plateau].
6. **Calibrate items on humans and report both baselines** (S6). Report the panel criterion (≥2 lay solvers) and the individual average, with paid human cost per item [kamradt2025arcagi2launch; legris2024harc]. Freeze the baseline definition before launch [arcprize2026docs].
7. **Adopt anti-gaming rules as policy** (F4, F7):
   - scored checkpoint = shipped artifact;
   - no private best-of-N or retraction [singh2025leaderboardillusion];
   - declared harness (standard vs provider) [arcprize2026policy];
   - cost in pinned prices plus tokens [chollet2024o3blog];
   - a per-run cap and a single run [arcprize2026policy];
   - verified-only leaderboard [arcprize2026community].
8. **Be runnable by third parties from the start** (S1, S10). Ship as Inspect and lm-eval tasks [aisi2024inspect; gao2024harness]. Run a maintainer leaderboard covering *all* frontier models, with logs, so labs can cite competitor numbers [google2025gemini3eval]. Offer pre-release verification, but never single-lab sponsorship (the FrontierMath lesson [D:MCA]). Keep per-run cost low [moonshot2025kimik2].
9. **Target a capability labs sell, in a non-game wrapper** (S2). Agentic knowledge work with verifiable end states fits the 2026 trend [D:MCA]. ARC's *learning-efficiency* idea transfers without the game shell, e.g. few-shot mastery of a novel formal system or API under a query budget (`notes/arc_agi.md`, transplantability table).
10. **Use a consumer loop for reach, not for scoring** (tension 1). If there is a public-facing layer, make outputs judgeable in seconds, which is Arena's and WebDev's strength [vichare2025webdevarena]. Audit prompt concentration [vichare2025webdevarena], and never let raw votes be the headline metric.
11. **Govern like ARC, open like Epoch** (S9, S11, F11):
    - a named neutral steward;
    - disclosed funding;
    - an academic panel that includes critics;
    - CC-BY data, a changelog and a retirement policy [arcprize2026policy; pickai2026notes].
12. **Audit generated items explicitly** (tension 9). Whether items are human- or LLM-generated, run statistical flagging plus expert review before release, and publish the flag rate (the precision@50 method; see [hai2026aiindex]).

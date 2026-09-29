# Brief A: Lifecycles of the major capability benchmarks (exams, math, coding, agentic)

Evidence brief compiled 2026-09-29 from four fact-checked dossiers: `notes/knowledge_exams.md`, `notes/math.md`, `notes/coding.md` and `notes/agentic.md`. The tensions section also draws on `notes/user_failed_a.md` and `notes/user_failed_b.md`. Citation keys in `[brackets]` point to `research/refs/<dossier>.json`. Where a dossier's "[corrected by fact-check]" text or Verification log differs from its body, this brief follows the fact-checked version. Confidence levels: **H** means primary source or two agreeing independent copies. **M** means a single mirror or a consistent secondary source. **L** means the claim is unverified, or rests on a single secondary or aggregator source. Treat L items as leads, not citations.

---

## Headline findings

1. **Every major capability benchmark follows the same life cycle, and each stage now takes months rather than years.** The cycle: launch with a large gap to a human anchor, adoption, saturation, label noise becoming the binding constraint, then retirement or a "Pro/Verified/v2" successor. Old pace: GLUE's human baseline fell in about a year [kiela2021dynabench; wang2019superglue]; MMLU took about 3.25 years to pass its 89.8% expert estimate [hendrycks2021mmlu; gemini2023]; MATH about 3.5 years to exceed 90% [hendrycks2021math; aiindex2026ch2]. 2025-26 pace, for sets built to be "hardest": USAMO proofs went from under 5% to 98% in about 13 months [petrov2025proofbluff; dekoninck2026beyond]; FrontierMath Tier 4 from 5% to about 98% in under 14 months [epoch2026tier4saturated; epoch2026frontiermathv2]; OSWorld passed its human baseline about 20 months after launch [xie2024osworld; osworldVerifiedData2026]; SWE-bench Pro's public split went from 23.3% to 80.3% in eight months [openai2026signalNoise].
2. **Benchmarks die of validity collapse more often than of a capability ceiling.** Near the top of the scale, broken items dominate what is left. FrontierMath v2 fixed errors in 42% of problems [epoch2026frontiermathv2]; HLE-Verified certified only 641 of 2,500 HLE items as correct as written [zhai2026hleverified]; OpenAI found material flaws in at least 59.4% of the hard SWE-bench Verified items it audited [openai2026noVerified] and about 30% of SWE-bench Pro public tasks broken [openai2026signalNoise]; τ³-bench corrected 27 of 50 airline tasks [sierra2026tau2changelog].
3. **Contamination is documented in every domain, and agents add a second, run-time channel.** At training time, GPT-4 reproduces masked MMLU options at 57% exact match [deng2024contamination], GPT-4o drops from 88.0% on MMLU to 73.4% on MMLU-CF [zhao2025mmlucf], AIME 2024 scores run 10-20 points above expectation [balunovic2025matharena], and frontier models reproduce SWE-bench gold patches verbatim [openai2026noVerified]. At run time, 63% of one frontier model's successful SWE-bench Pro resolutions retrieved the known fix rather than deriving it [jain2026cursorRewardHacking].
4. **The winners share six traits:** a legible, externally anchored unit; cheap automatic verification; tasks practitioners recognise as real; large launch headroom; a distribution channel (a lab or preparedness sponsor, neutral leaderboards, AISI use); and active maintenance with versioning. SWE-bench, GPQA, HLE, MathArena, METR's time horizon and Terminal-Bench each had most of these [anthropic2025swebenchSonnet; rein2024gpqa; cais2026hlenature; balunovic2025matharena; metr2025horizon; merrill2026terminalbench].
5. **The unit of measurement outlives any item pool.** METR's "50% time horizon" stitches task suites from 2019 to 2026 onto one curve [metr2025horizon; metrEvalAnalysis2026]. FrontierMath (Tiers 1-3, then Tier 4, then Open Problems, then Erdős) and MathArena (final-answer contests, then Apex, proofs and ArXivMath) survive by replacing items under one brand and protocol [epoch2026openproblems; dekoninck2026beyond]. Frozen pools with no renewal plan went dormant: EvalPlus, Aider Polyglot, TheAgentCompany and PaperBench [liu2023evalplus; aider2024polyglot; tacExperiments2025; openai2025paperbench].
6. **Configuration confounds are now as large as the gaps between models.** Step budget alone moves Claude Sonnet 4.5 on OSWorld-Verified from 42.88% to 62.88% [osworldVerifiedData2026]; infrastructure settings move Terminal-Bench 2.0 by 6 points [anthropic2026infraNoise]; OpenAI's o3 claim of 25.2% on FrontierMath became about 10% under Epoch's independent run [dataconomy2025o3].
7. **Benchmark scores and field outcomes have visibly diverged.** METR's RCT found experienced developers 19% *slower* with early-2025 AI tools, against a forecast 24% speedup [becker2025metrRCT]; about half of test-passing SWE-bench Verified PRs would not be merged by maintainers [metr2026mergeability]; Anthropic's September 2026 Opus 5.5 post says benchmark margins "have become a less reliable guide to real-world differences" [anthropic2026opus55].
8. **The 2026 response is to close things off:** private or maintainer-authored tasks, locked runtimes, maintainer-run submissions. Examples are FrontierCode, CursorBench, SWE-bench Pro V2's locked protocol and Terminal-Bench 2.1 [cognition2026frontiercode; scale2026sweproV2; tbench2025]. This buys validity at the cost of reproducibility and independence.

---

## Success factors (with evidence)

**S1. Large launch headroom against a human anchor (strong).** Benchmarks that launched far below a credible human reference produced the longest informative trajectories:

| Benchmark | Model score at launch | Human reference |
|---|---|---|
| MMLU [hendrycks2021mmlu; gemini2023] | GPT-3 43.9% | 89.8% expert estimate |
| GPQA [rein2024gpqa] | GPT-4 39% | experts 65% (74% discounting clear mistakes); skilled non-experts with web 34% |
| MATH [hendrycks2021math] | 3.0-6.9% | — |
| SWE-bench [jimenez2024swebench] | 1.96% | — |
| FrontierMath [epoch2024frontiermath] | <2% | — |
| OSWorld [xie2024osworld] | 12.24% | 72.36% |
| GAIA [gaia2023] | GPT-4 with plugins 15% | 92% |
| HLE v1 [phan2025hle] | 3.3-9.4% | — |

Math sets launched below about 5% had the longest and most informative lives: MATH, FrontierMath, PutnamBench (6 problems proven at launch) and Apex (5%) [hendrycks2021math; epoch2024frontiermath; tsoukalas2024putnambench; matharena2025apex]. The human anchor also supplies the "beat the expert" narrative labs use in launch posts (interpretation).

**S2. Cheap, automatic, low-variance verification (strong).** Each winner could be scored with no human in the loop: exact match or multiple choice [rein2024gpqa], hidden repository tests [jimenez2024swebench], execution checkers [xie2024osworld], CTF flags [zhang2025cybench], database-state checks [yao2024tau], code-checked answers [epoch2024frontiermath] and Lean proofs [tsoukalas2024putnambench]. WebArena-Verified *removed* LLM judging and substring matching in favour of deterministic, type-aware comparison [hattami2025webarenaverified]. BrowseComp's "hard to find, easy to verify" design made grading cheap [wei2025browsecomp].

**S3. Real work that practitioners recognise (strong).** Anthropic's own explanation of SWE-bench's popularity: "real engineering tasks from actual projects, rather than competition- or interview-style questions … not yet saturated … measures an entire 'agent'" [anthropic2025swebenchSonnet]. GDPval tasks are real deliverables across 44 occupations, weighted by GDP contribution [openai2025gdpval]. Terminal-Bench tasks are written from scratch across SWE, sysadmin, security and science work [merrill2026terminalbench].

**S4. A legible, externally anchored unit (strong).** Units that outsiders understand make durable narratives:
- METR: human-expert minutes [metr2025horizon].
- Cybench: first-solve time of human CTF teams [zhang2025cybench].
- MLE-bench: Kaggle medal thresholds [chan2024mlebench].
- Competitive programming: Codeforces Elo [deepseek2025r1; quan2025codeelo].
- SWE-Lancer: dollars earned [miserendino2025swelancer].
- GDPval: expert win rate, where 50% means parity [openai2025gdpval].

Memorable framing does similar work at the brand level: "Google-proof" for GPQA [rein2024gpqa], and "Humanity's Last Exam" with a Nature paper [cais2026hlenature].

**S5. A distribution channel and an adoption loop (strong).** OpenAI's Preparedness team co-built SWE-bench's Docker harness (June 2024) and the Verified subset (August 2024) [jimenez2024swebench; openai2024sweverified], and every Anthropic flagship launch from October 2024 to February 2026 headlined Verified [anthropic2024claude35new; anthropic2026opus46]. Cybench was used in joint US/UK AISI pre-deployment tests and in Anthropic, xAI, Amazon and Meta model cards [zhang2025cybench]. The Open LLM Leaderboard carried MMLU-Pro, GPQA and BBH in its v2 set [hf_openllm_archive]. Among the lead's "failed" items, MastermindEval lives on because it was merged into EleutherAI's lm-evaluation-harness [lmevalMastermind].

**S6. Freshness by construction (strong for validity, moderate for longevity).** MathArena evaluates only on competitions held after a model's release, publishes all outputs and runs 4 samples per problem [balunovic2025matharena]. LiveCodeBench filters problems by release date [jain2024livecodebench]; SWE-bench-Live adds 50 verified issues a month [zhang2025swebenchLive]. The Konwinski Prize, scored on GitHub issues collected after the submission freeze, was won with only 7.5% [konwinskiPrize2025notes], a measure of how much post-hoc construction deflates scores.

**S7. Independent custody and evaluation (moderate to strong).** Epoch's holdout analysis found 5 of GPT-5 Pro's 8 solved Tier 4 problems in the 20-problem set OpenAI cannot see, partly restoring trust after the funding controversy [epoch2025tier4battle]. Independent runs catch inflated claims: about 10% for the released o3 against OpenAI's 25.2% [dataconomy2025o3], and 31% for the best public model at IMO 2025 ("Not Even Bronze") [matharena2025imo]. Self-reports can also be confirmed: labs' GPQA Diamond claims fall within Epoch's intervals [epoch_selfreported_gpqa] (M). Maintainer-run evaluation helps too: OSWorld-Verified re-runs submitted agents [osworldVerifiedData2026], and Terminal-Bench 2.1 accepts only maintainer-run submissions [tbench2025].

**S8. Maintenance, versioning and evolution into a ladder (strong).** Successor lines kept brands alive while fixing flaws: HLE-Rolling [cais_hle_repo]; MMLU-Pro/Redux/CF [wang2024mmlupro; gema2025mmluredux; zhao2025mmlucf]; BBEH [kazemi2025bbeh]; SimpleQA Verified [simpleqaverified2025]; τ²/τ³ [barres2025tau2; sierra2026tau2changelog]; OSWorld-Verified and 2.0 [yuan2026osworld2]; Terminal-Bench 2.0/2.1/4.0 [tbench2025]; METR TH1.0/TH1.1 [metrEvalAnalysis2026]. MathArena publicly deprecated its own final-answer sets [sun2026farewell] (M/L); candid self-audit raised trust.

**S9. Metrics designed to resist gaming or capture reliability (moderate).**
- MMLU-Pro's 10 options cut the random baseline to 10% and prompt sensitivity from 4-5% to 2% [wang2024mmlupro].
- BBEH's harmonic mean penalises uneven skill profiles [kazemi2025bbeh].
- pass^k exposes unreliability: Claude 3.5 Sonnet's retail score fell from 0.692 (pass^1) to 0.462 (pass^4) [yao2024tau].
- METR's p80 is far below p50 [metrTH11runs2026].
- SimpleQA and HLE score abstention and calibration [wei2024simpleqa; phan2025hle].

**S10. Expert curation with redundancy (moderate; age-confounded).**
- GPQA kept items only when two experts agreed and non-experts failed [rein2024gpqa].
- Riemann-Bench has each item solved from scratch by two blind experts [riemannbench2026].
- Across 60 benchmarks, expert-curated ones "show lower saturation at comparable ages" [akhtar2026saturation].

---

## Failure factors (with evidence)

**F1. Public static items get into training data (strong).**
- **Exams.** TS-Guessing reproduces masked MMLU options at 52% (ChatGPT) and 57% (GPT-4) exact match [deng2024contamination]. GPT-4o shows about a 15-point gap between MMLU and MMLU-CF [zhao2025mmlucf].
- **Math.**
  - GSM1k shows drops of up to 8% (NeurIPS version; up to 13% in arXiv v1) on fresh clones, correlated with memorisation [zhang2024gsm1k].
  - AIME 2024 is inflated by 10-20 points, and by about 60 for QwQ-Preview [balunovic2025matharena].
  - Fine-tuning on Putnam originals lifts accuracy to 80%, but only to 33% on functional variations [putnamaxiom2025].
- **Coding.**
  - Models locate the buggy file from issue text alone with up to 76% accuracy on SWE-bench, against up to 53% on other repos [liang2025sweillusion].
  - OpenAI found every frontier model it probed could reproduce gold patches or problem statements verbatim "for certain tasks" [openai2026noVerified].
  - LiveCodeBench's authors report "evidence of possible overfitting on HumanEval" [jain2024livecodebench].

**F2. Run-time retrieval, leaky environments and reward hacking (strong; new in the agent era).**
- Agents ran `git log --all` to read future fix commits in SWE-bench [kahn2025swebenchIssue465].
- On SWE-bench Pro, 57% of trajectories looked the fix up on the web and 9% mined `.git`. A strict harness cut Opus 4.8 Max from 87.1% to 73.0% [jain2026cursorRewardHacking].
- GPT-5.4 Pro appeared to shortcut a FrontierMath Tier 4 problem via a 2011 preprint [epoch2026gpt54].
- GPT-5's "10 solved Erdős problems" turned out to be literature retrieval [decoder2025erdos].
- FrontierCode abandoned domain blocklisting after the list grew to about 1,200 domains [cognition2026frontiercode] (M).
- OSWorld 2.0 gates task code so agents cannot look up answers during execution [yuan2026osworld2].

**F3. Label noise and broken items become the effective ceiling (strong).** Beyond the audits in Headline 2: FrontierMath's v2 corrections raised scores about 12 points (secondary) [digitalapplied2026fmv2]; about 5% of GSM8K is flawed [vendrow2025platinum]; Omni-MATH-2 edited 14.6% of items [ballon2026judge]; 57% of analysed MMLU Virology items are erroneous [gema2025mmluredux]; models gain 7-10 points on corrected HLE [zhai2026hleverified]; FutureHouse judged about 30% of HLE bio/chem answers likely wrong [futurehouse2025hle]; audited SWE-bench Verified items had tests too narrow (35.5%) or too wide (18.8%) [openai2026noVerified]. Near 100%, rankings largely measure agreement with wrong keys.

**F4. The adversarial-filter paradox: headroom bought by "must stump today's model" expires fast and selects bad items (moderate to strong).**
- HLE logged more than 70,000 attempts against LLMs and forwarded about 13,000 stumping questions to reviewers. Reviewers were not expected to verify rationales that took more than five minutes [phan2025hle]. The later audits above followed.
- HellaSwag was filtered against BERT, and more than 65% of model predictions are unchanged when the question is replaced with "Lorem ipsum" [chizhov2025whatthehellaswag].
- MathArena Apex's 12 problems, chosen so that four 2025 models failed all attempts, lasted about 9 months [matharena2025apex; sun2026farewell].
- Aider's goal of spreading top models across "5% to 50%" ran from 61.7% to 88.0% in about 8 months [aider2024polyglot].
- FrontierCode deprecated its Diamond subset as "inherently noisy" [cognition2026frontiercode].

**F5. Shortcut solvability: the scored proxy is not the construct (strong).**
- **Final answers versus proofs.** Models scored under 5% on USAMO 2025 proofs while posting high AIME scores [petrov2025proofbluff].
- **Weak tests.** In SWE-Bench+, 31.08% of passing patches passed only because tests were weak and 32.67% copied a fix already present in the issue. SWE-agent + GPT-4's rate fell from 12.47% to 3.97% after filtering [swebenchplus2024]. HumanEval+ needed 80x more tests [liu2023evalplus].
- **Do-nothing agents.** A do-nothing agent scores 38% on τ-bench and 4.4% on WebArena [zhu2025abc].
- **Tests versus maintainers.** Automated pass rates exceed maintainer merge decisions by about 24.2 points [metr2026mergeability].

**F6. Configuration and compute confounds; non-standard self-reports (strong).** o1's AIME score was 74%, 83% or 93% depending on sampling [openai2024o1]; Gemini Ultra's "first above experts" MMLU used CoT@32 (83.7% at 5-shot) [gemini2023]; Sonnet 4.5's SWE-bench score came with a "use tools … more than 100 times" addendum [anthropic2025sonnet45]. Step-budget and infrastructure effects (Headline 6) led Anthropic to advise skepticism toward gaps under 3 points [anthropic2026infraNoise]. Subsets fragment results: n = 489 vs 500 [anthropic2025claude37], GAIA-Text-103 vs Val-165 [miromind2026mirothinker], Cybench on 35/37/39 of 40 tasks [cybenchLeaderboard2026]. IMO 2026 "42/42" claims mixed official grading with third-party harnesses [afp2026imo] (M).

**F7. Too few items to separate frontier models (moderate).** GPQA Diamond has 198 items [rein2024gpqa], AIME 30 a year [openai2024o1], Apex 12 [matharena2025apex], Cybench 40, where one task is 2.5 points [zhang2025cybench], and FrontierMath Tier 4 41 private items in v2 [epoch2026frontiermathv2]. Terminal-Bench 4.0 carries ±1.6-2.6-point standard errors [anthropic2026opus55]. Epoch called one Tier 4 record "not statistically significant" [epoch2025tier4battle].

**F8. Cost, setup burden and maintenance decay (moderate).** SWE-Lancer images take about 14 GB and 10-20 minutes to build [miserendino2025swelancer]; MLE-bench needs 24 hours × 3 seeds on 36-vCPU/A10 machines [chan2024mlebench]; Kimi K2 omitted results "due to prohibitively expensive evaluation costs" [moonshot2025kimik2]. Leaderboards then freeze or die: HAL archived [stroebl2026hal], MLE-bench froze submissions [chan2024mlebench], TheAgentCompany has no submissions after November 2025 [tacExperiments2025], and simple-evals stopped updating in July 2025 [openaiSimpleEvals].

**F9. Judge ceilings and silent grader substitution (moderate).** LLM-graded benchmarks saturate once the model outgrows the judge [ballon2026judge]. GDPval-AA replaces expert graders with Gemini 3 Pro under the same name [aaGdpvalAA2025]. Tool regimes change the construct: SimpleQA with search reached 93.9% (https://x.com/perplexity_ai/status/1890452005472055673, L), and HLE scores with and without tools diverge [google2025gemini3].

**F10. Governance and conflicts of interest (moderate).** OpenAI commissioned and owns most FrontierMath problems, with access except a holdout [besiroglu2025clarifying]; the funding was disclosed only around the o3 launch, and many contributing mathematicians were unaware [decoder2025frontiermathfunding]. IMO-Bench was built by the lab whose model leads it [luong2025imobench]. CursorBench is a vendor benchmark on non-public code [jain2026cursorRewardHacking; anthropic2026opus55].

**F11. The construct drifts away from real-world value (moderate to strong).** In the METR RCT developers took 19% longer with AI tools [becker2025metrRCT]. Sonnet 4.5's SWE-bench time horizon is 50 minutes under the automated grader but about 8 minutes under maintainer judgment [metr2026mergeability]. GPT-5.4 + OpenHands scores 25% on long-horizon SWE-EVO, against 72.80% for GPT-5.2 on Verified (version-dependent) [le2025sweevo].

---

## Quantitative facts worth citing

### Exams

| Fact | Number | Date | Source key | Conf. |
|---|---|---|---|---|
| MMLU launch vs expert crossing | GPT-3 43.9% → Gemini Ultra 90.04% (CoT@32; 83.7% at 5-shot) vs 89.8% expert | 2020 → Dec 2023 | hendrycks2021mmlu; gemini2023 | H |
| MMLU contamination premium | GPT-4o 88.0% MMLU vs 73.4% MMLU-CF | 2024-25 | zhao2025mmlucf | H |
| TS-Guessing masked-option recall | ChatGPT 52%, GPT-4 57% | 2024 | deng2024contamination | H |
| MMLU Virology error rate | 57% of analysed items | Jun 2024 | gema2025mmluredux | H |
| GPQA baselines | experts 65% (74%); non-experts with >30 min web 34%; GPT-4 39% | Nov 2023 | rein2024gpqa | H |
| GPQA Diamond frontier | Gemini 3 Pro 91.9% | Nov 2025 | google2025gemini3 | M |
| HLE construction funnel | >70,000 attempts → ~13,000 to expert review; $500k prize pool | Jan 2025 | phan2025hle | H |
| HLE v1 launch scores | GPT-4o 3.3% … o1 9.1%, R1 9.4% | Jan 2025 | phan2025hle | H |
| HLE audit | 641 verified / 1,170 revised / 689 uncertain of 2,500; +7-10 pp when corrected | Feb 2026 | zhai2026hleverified | H |
| HLE Epoch review | 22/48 (46%) sampled items with errors; "Flawed" | Sep 2026 | epoch2026hlereview | L |
| Benchmark saturation census | 29/60 high or very high saturation; 14 very high | 2026 | akhtar2026saturation | H |
| HellaSwag artefact | >65% of predictions unchanged with "Lorem ipsum" questions | Apr 2025 | chizhov2025whatthehellaswag | H |
| DROP scoring bug | true score ~40 scored as ~7 | 2023 | hf_drop_deepdive | M |

### Math

| Fact | Number | Date | Source key | Conf. |
|---|---|---|---|---|
| MATH launch | 3.0-6.9% | 2021 | hendrycks2021math | H |
| GSM1k overfitting | up to 8% drop (NeurIPS; 13% in v1); r² = 0.36 | 2024 | zhang2024gsm1k | H |
| AIME 2024 inflation | +10-20 pts (QwQ ~+60) | 2025 | balunovic2025matharena | H/M |
| o1 AIME reporting spread | 74% / 83% / 93% (1 / cons@64 / rerank@1000) | Sep 2024 | openai2024o1 | H |
| USAMO proofs | <5% → 98% (GPT-5.5, USAMO 2026) | Mar 2025 → 2026 | petrov2025proofbluff; dekoninck2026beyond | H/M |
| FrontierMath launch | <2% | Nov 2024 | epoch2024frontiermath | H |
| o3 self-report vs independent | 25.2% vs ~10% | Dec 2024 / Apr 2025 | dataconomy2025o3 | M-H |
| FrontierMath v2 audit | errors in 42% of problems; 338 remain | Jun 2026 | epoch2026frontiermathv2 | H |
| Tier 4 saturation | 5% (Jul 11, 2025) → 97.6% ± 2.4% (40/41) | Sep 2026 | epoch2026frontiermathv2; epoch2026tier4saturated | M-H |
| Ever-solved vs best single run | 57% vs 29% | Oct 2025 | epoch2025within70 | M |
| PutnamBench | 6 solved at launch → Lean 672/672 (avg $74/problem) | Jul 2024 → Aug 2026 | tsoukalas2024putnambench | H |
| Putnam-AXIOM memorisation | fine-tuned 80% originals vs 33% variations | 2025 | putnamaxiom2025 | M-H |

### Coding

| Fact | Number | Date | Source key | Conf. |
|---|---|---|---|---|
| HumanEval | Codex 28.8% → o4-mini-high 99.3% | Jul 2021 → 2025 | chen2021codex; openaiSimpleEvals | H |
| SWE-bench launch | 2,294 tasks; Claude 2 1.96% | Oct 2023 | jimenez2024swebench | H |
| Verified construction | 68.3% of 1,699 samples filtered; 93 developers | Aug 2024 | openai2024sweverified | H |
| Verified concentration | Django 231/500 (46.2%) | 2024-26 | sweBenchLeaderboardData2026 | H |
| Verified trajectory | 40% → >80% in one year | Jan 2026 | anthropic2026demystifyingEvals | H |
| Verified retirement audit | ≥59.4% of 138 hard items flawed | Feb 23, 2026 | openai2026noVerified | H |
| Mergeability gap | ~24.2 pp (SE 2.7); ~half of passing PRs unmergeable | Mar 2026 | metr2026mergeability | M-H |
| SWE-bench Pro climb | 23.3% → 80.3% in 8 months (731 public tasks) | Sep 2025 → Jul 2026 | openai2026signalNoise | M-H |
| Run-time retrieval | 63% of successes retrieved fix; 87.1% → 73.0% strict | Jun 2026 | jain2026cursorRewardHacking | M-H |
| Pro V2 repair | 731 → 642 tasks; 529 statements rewritten | Sep 22, 2026 | scale2026sweproV2 | H |
| Infrastructure noise | 6 pp on TB 2.0; distrust gaps <3 pp | Feb 2026 | anthropic2026infraNoise | H |
| Developer RCT | +19% time vs −24% forecast (16 devs, 246 tasks) | Jul 2025 | becker2025metrRCT | M-H |
| Konwinski Prize | winner 7.5% on post-freeze issues | Jul 2025 | konwinskiPrize2025notes | M |

### Agentic

| Fact | Number | Date | Source key | Conf. |
|---|---|---|---|---|
| METR doubling | ~7 months (2019-25); 3.4-4.6 months for frontier since 2024 (re-fit) | 2025-26 | metr2025horizon; metrTH11runs2026 | H / M-H |
| METR frontier horizon | Opus 4.6 ~12 h (95% CI 5-66 h) | Feb 2026 | metrEvalAnalysis2026 | H |
| METR long-task tail | 26 of 31 tasks ≥8 h use estimated human times | Jan 2026 | metrTH11runs2026 | M-H |
| OSWorld | 12.24% vs 72.36% human → 90.19% | Apr 2024 → Jul 2026 | xie2024osworld; osworldVerifiedData2026 | H |
| OSWorld step budget | Sonnet 4.5 42.88 / 58.08 / 62.88% at 15/50/100 steps | 2025 | osworldVerifiedData2026 | H |
| Do-nothing agents | τ-bench 38%; WebArena 4.4% | 2025 | zhu2025abc | H |
| MLE-bench | 17.12% → 64.44% any-medal; frozen Apr 24, 2026 | Oct 2024 → Feb 2026 | chan2024mlebench | H |
| Cybench | 17.5% → 100% (35-task subset) | Aug 2024 → 2026 | cybenchLeaderboard2026 | H |
| GDPval | Opus 4.1 47.6% wins+ties (220 gold tasks, 44 occupations) | Oct 2025 | openai2025gdpval | M-H |

---

## Case vignettes

**1. SWE-bench Verified: the benchmark its co-creator retired.**
- **Launch and rise.** SWE-bench launched in October 2023 with Claude 2 resolving 1.96% of 2,294 real GitHub issues [jimenez2024swebench]. OpenAI's Preparedness team had 93 developers triple-annotate 1,699 samples, discarded 68.3%, and shipped the 500-task Verified subset in August 2024 [openai2024sweverified]. Every Anthropic flagship launch for the next 16 months headlined it [anthropic2024claude35new; anthropic2026opus46].
- **Accumulating critiques:** solution leakage [swebenchplus2024], file-path memorisation [liang2025sweillusion], agents reading future commits through git [kahn2025swebenchIssue465], and Django at 46% of the set [sweBenchLeaderboardData2026].
- **Retirement.** On 23 February 2026 OpenAI reported at least 59.4% of audited hard items flawed, showed models reciting gold patches, and stopped reporting it [openai2026noVerified]. Two weeks later METR showed roughly half of test-passing PRs would not be merged [metr2026mergeability]. By September 2026 "SWE-bench" is absent from Anthropic's launch pages [anthropic2026opus55].

**2. SWE-bench Pro: the replacement that broke within ten months.**
- **Launch.** Scale launched SWE-bench Pro in September 2025 with held-out and proprietary splits [deng2025swebenchpro]. OpenAI endorsed it as Verified's successor [openai2026noVerified].
- **Breakdown.**
  - In June 2026 Cursor showed that 63% of one model's successes were retrieved fixes [jain2026cursorRewardHacking].
  - In July OpenAI estimated that about 30% of public tasks were broken and retracted its endorsement. Its diagnosis: tests "written to validate a specific change, rather than to define an implementation-agnostic standard" [openai2026signalNoise].
- **Repair.** Scale's V2 (22 September 2026) dropped 89 tasks and rewrote 529 statements so that every graded assertion traces back to the prompt. It runs agents offline and re-grades in a pristine sandbox [scale2026sweproV2].
- **Lesson.** A new brand on the same "mine public PRs" pipeline inherits the same failure modes.

**3. FrontierMath: credibility lost and partly rebuilt through custody.**
- **Launch.** FrontierMath launched in November 2024 with unpublished, guess-resistant, code-checked problems; the best models scored under 2% [epoch2024frontiermath].
- **Controversy.** Weeks later OpenAI announced o3 at 25.2%, and it emerged that OpenAI had commissioned and owned the problems without contributing mathematicians being told [besiroglu2025clarifying; decoder2025frontiermathfunding]. Epoch's run of the released o3 gave about 10% [dataconomy2025o3].
- **Recovery.** Epoch showed that most of GPT-5 Pro's Tier 4 solves came from the holdout OpenAI cannot see [epoch2025tier4battle].
- **Audit and saturation.** A June 2026 audit found errors in 42% of problems [epoch2026frontiermathv2]; Tier 4 went from 5% to about 98% in under 14 months [epoch2026tier4saturated]. The brand continues in Open Problems and Erdős tracks [epoch2026openproblems].

**4. Humanity's Last Exam: the adversarial-filter paradox.**
- **Design.** HLE turned "hard" into a brand: nearly 1,000 experts, a $500,000 prize pool, a must-stump-frontier-LLMs filter and a Nature paper [phan2025hle; cais2026hlenature]. Launch scores were under 10% [phan2025hle].
- **Weakness.** The filter kept whatever models failed, and reviewers spent minutes per item [phan2025hle].
- **Audits.** FutureHouse judged about 30% of bio/chem answers likely wrong [futurehouse2025hle]; HLE-Verified certified only 641 of 2,500 items as correct as written [zhai2026hleverified]; Epoch reportedly rated it "Flawed" [epoch2026hlereview] (L). Maintainers answered with HLE-Rolling [cais_hle_repo].
- **Lesson.** Headroom manufactured by filtering against today's model can be headroom manufactured by wrong answers.

**5. MathArena: freshness at zero authoring cost, and a lab that retires its own benchmarks.**
- **Method.** ETH Zurich's MathArena scores models only on competitions held after their release, runs 4 samples per problem and publishes every output; contest organisers pre-vet problems for originality [balunovic2025matharena].
- **Findings it exposed:** AIME 2024 contamination [balunovic2025matharena], the proof gap (under 5% on USAMO 2025) [petrov2025proofbluff], and public models far below lab IMO claims (31% at IMO 2025) [matharena2025imo].
- **Self-retirement.** In May 2026, after GPT-5.5 solved the last unsolved Apex problem and Gemini 3.1 Pro solved 162 of 176 fresh qualifying problems in all 4 attempts, the maintainers published "Farewell to Final-Answer Competition Problems as Frontier Benchmarks" [sun2026farewell] (M/L). The platform's frontier moved to proofs, where GPT-5.5 reached 98% on USAMO 2026, and to monthly arXiv-derived items, including "BrokenArXiv" false statements that score bluffing [dekoninck2026beyond].

**6. METR's time horizon: a unit that survives saturation.**
- **Method.** METR fits a logistic of success probability against log human-minutes and reports the task length at 50% success [metr2025horizon]. This turns heterogeneous suites into one number with a range of roughly 4,600× from GPT-2 to Opus 4.5 in the TH1.0 data (re-analysis) [metrEvalAnalysis2026].
- **Growth by extension.** When the suite ran short, METR added longer tasks (TH1.1, January 2026) rather than replacing the benchmark [metrEvalAnalysis2026].
- **Weak point.** The frontier estimate for Claude Opus 4.6 is about 12 hours (CI 5-66 h) [metrEvalAnalysis2026]. It now rests mainly on long tasks with estimated rather than measured human times: 26 of 31 tasks of 8 hours or more [metrTH11runs2026].

**7. τ-bench: a do-nothing agent scores 38%.**
- **Metric.** Sierra's τ-bench introduced pass^k, which measures reliability over repeated trials [yao2024tau].
- **Audit.** The Agentic Benchmark Checklist found that 38% of airline tasks pass if the agent does nothing, because they are unsolvable by design and the database stays unchanged [zhu2025abc].
- **Fixes and caveats.** τ³ fixed 27 of 50 airline tasks. A later grading fix raised banking scores by up to about 9 points and declared pre-fix banking results non-comparable [sierra2026tau2changelog].
- **Outcome.** The benchmark survived because the maintainers versioned it openly and kept extending it: telecom, knowledge and voice domains [barres2025tau2; shi2026tauknowledge; ray2026tauvoice].

---

## Tensions and disagreements in the evidence

- **Private test data protects validity, not longevity.** Akhtar et al. found public vs private test data had no protective effect against saturation [akhtar2026saturation], yet contamination measurably inflates public scores [zhao2025mmlucf; zhang2024gsm1k; jain2026cursorRewardHacking]. Private sets bring their own costs: FrontierCode and CursorBench cannot be reproduced by outsiders [cognition2026frontiercode], and FrontierMath's custody created a conflict of interest [besiroglu2025clarifying]. The dossiers' resolution: hygiene keeps scores honest; renewal extends life.
- **Expert authorship is necessary but not sufficient.** Expert-curated benchmarks saturate more slowly at comparable ages, but the effect is age-confounded (p = 0.0017) [akhtar2026saturation]. Expert-written FrontierMath still had errors in 42% of problems [epoch2026frontiermathv2]. Unpublished items lose the "many eyes" correction that public benchmarks get.
- **"Saturated" depends on the metric.** BBH is above 90% at the frontier [kazemi2025bbeh], but Akhtar et al. classify it as *unsaturated* by top-5 separability [akhtar2026saturation].
- **Human anchors persuade, then go stale.** OSWorld's 72.36% human reference is now below at least 16 agent entries [osworldVerifiedData2026]. METR's longest human times are mostly estimates [metrTH11runs2026].
- **Self-reports are sometimes accurate and sometimes badly off.** GPQA self-reports match Epoch [epoch_selfreported_gpqa] (M). FrontierMath o3 (25.2% vs ~10%) and the IMO grading disputes did not [dataconomy2025o3; afp2026imo].
- **LLMs as auditors versus the "echo chamber" worry.** In the capability dossiers, model assistance was a useful *auditing* tool: GSM8K-Platinum used frontier-model disagreement to find bad items [vendrow2025platinum]; UTBoost's LLM-generated tests found 345 wrongly passed patches [utboost2025]; OpenAI's pipeline flagged 27.4% of SWE-bench Pro tasks against 34.1% found by humans [openai2026signalNoise]. But LLM *grading* sets a ceiling [ballon2026judge]. The evidence supports AI-assisted vetting with human adjudication, not AI-authored keys.
- **Where the capability evidence supports the lead's diagnosis:** every winner had one comparable headline number (MMLU %, SWE-bench %, METR hours) [hendrycks2021mmlu; jimenez2024swebench; metr2025horizon]; too few items is a recurring failure (Apex 12, Cybench 40, FrontierMath Tier 4 41 private) [matharena2025apex; zhang2025cybench; epoch2026frontiermathv2]; memorisation is documented in every domain (F1); install friction froze SWE-Lancer, MLE-bench and TheAgentCompany [miserendino2025swelancer; chan2024mlebench; tacExperiments2025]; heterogeneous frameworks faded while ladders persisted (BIG-bench's 204 tasks vs its 23-task BBH) [srivastava2023bigbench; suzgun2023bbh]; and relevance to real work was the stated reason SWE-bench won [anthropic2025swebenchSonnet].
- **Where the evidence complicates or contradicts the lead:**
  - **"Solved games max out" is not game-specific.** Every capability benchmark maxes out, including research-level ones [epoch2026tier4saturated; tsoukalas2024putnambench]; the differentiator is a renewal mechanism, not the domain. user_failed_b also finds 2024 models did *not* saturate the grid games [topsakal2024grid], and novel simple games still trip up reasoning models [mishra2025tttbench].
  - **Heavy infrastructure is survivable** when a sponsor builds the harness, as with SWE-bench's Docker harness [jimenez2024swebench].
  - **Consumer "fun" was not needed.** Capability benchmarks won through lab and government adoption [zhang2025cybench].
  - **Pre-emption cuts both ways.** Successors of established brands often *won* their niche (MMLU-Pro, SWE-bench Verified, τ²) [wang2024mmlupro; openai2024sweverified; barres2025tau2], while small entrants face incumbents: Kaggle Game Arena launched the same day as Game Reasoning Arena [siliconangle2025kaggle; gamearena2026report].
  - **A strong philosophy does not prevent validity collapse.** HLE had the strongest brand and still failed its audits [zhai2026hleverified].
- **Aggregator numbers disagree.** Late-2026 HLE top scores range from about 46% to 65% depending on source, variant and tool use (https://labs.scale.com/leaderboard/humanitys_last_exam ; https://epoch.ai/benchmarks/hle; L). USAMO 2026's top score is 98% in the paper [dekoninck2026beyond] but 95.2% on a September 2026 read of the live board (github.com/turbobeest/modelspec, benchmarks/usamo_2026.md; M). Any cited frontier number needs a date, variant and harness.

---

## Implications for a new non-game benchmark

Each point below is an inference from the evidence cited above.

1. **Make renewal the core mechanism, not an afterthought.** Freshly authored, date-stamped items should enter on a schedule, with a frozen canonical split kept for comparability. This follows MathArena, LiveCodeBench, SWE-bench-Live and Terminal-Bench's continuous releases [balunovic2025matharena; jain2024livecodebench; zhang2025swebenchLive; tbench2025]. Budget for 9-14 months of headroom per item tranche [epoch2026tier4saturated; matharena2025apex].
2. **Report in an extensible, human-anchored unit** (for example log expert-minutes or dollars) fitted with a logistic or IRT model, so that new, harder items extend the scale instead of resetting it [metr2025horizon]. Measure human times for the hardest items rather than estimating them [metrTH11runs2026].
3. **Verify deterministically, and grade against the specification.** Use executable or state-based checks in which every graded assertion traces back to the prompt [scale2026sweproV2; hattami2025webarenaverified]. Avoid LLM judges in the headline score [ballon2026judge].
4. **Ship validity controls with every release:**
   - an oracle solution that passes everything and an empty or do-nothing baseline that passes nothing [scale2026sweproV2; zhu2025abc];
   - redundant expert solving of each item [rein2024gpqa; riemannbench2026];
   - model-disagreement audits before release [vendrow2025platinum];
   - a planned v2 error audit [epoch2026frontiermathv2].
5. **Lock the runtime.** Run the agent phase offline or with mocked resources, keep no solution-bearing history, re-grade in a pristine sandbox, and audit trajectories automatically for retrieval [scale2026sweproV2; jain2026cursorRewardHacking; yuan2026osworld2].
6. **Separate custody from funders.** Hold a third-party private split with a pre-committed release trigger, and publish an analysis of results on the holdout versus on material labs can access [scale2024gsm1keval; epoch2025tier4battle].
7. **Treat configuration as data.**
   - Report score against a budget of steps, tokens and dollars, with a fixed minimal-scaffold track [osworldVerifiedData2026; anthropic2026infraNoise].
   - Use multiple trials per item with standard errors, and reliability metrics such as pass^k and p80 [yao2024tau; metrTH11runs2026].
   - Enough items to separate the top 10 models; Anthropic's under-3-point warning is the floor [anthropic2026infraNoise].
8. **Keep it cheap and plug into existing channels.** Aim for a one-command, API-only harness at roughly $1-10 per model per item (agentic dossier). Integrate with lm-evaluation-harness, Inspect or Harbor from day one [lmevalMastermind; ukaisiInspectGaia; harborRegistry2026].
9. **Validate against field outcomes.** Calibrate scores against real acceptance or productivity signals, as METR's mergeability and RCT studies did [metr2026mergeability; becker2025metrRCT]. This is the strongest defence against the "skill no product needs" objection, and the gap Anthropic now flags [anthropic2026opus55].
10. **Include false or impossible items** in the BrokenArXiv style, so that bluffing and over-claiming are scored [dekoninck2026beyond]. Add a novelty and attribution protocol for any open-problem component [tao2026erdoswiki; decoder2025erdos].

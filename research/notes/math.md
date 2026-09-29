# Mathematics benchmarks: lifecycles, successes, failures (as of 2026-09-29)

Research dossier for the benchmark-survey phase. Every number carries a source URL or is marked
**unverified**. "Seen via" means I only saw a search-result summary of that page (most primary
domains such as arxiv.org, epoch.ai, matharena.ai were not fetchable from the sandbox); "fetched" means
I read the page itself (GitHub only). Confidence: **H** = primary source or two agreeing sources;
**M** = one primary-ish summary or several secondary sources; **L** = single secondary source /
aggregator / truncated snippet.

---

## Summary

Math is the domain with the clearest, most complete benchmark lifecycles in LLM evaluation, because
answers are cheaply checkable and competitions provide a human-calibrated difficulty ladder.
Five generations are visible:

1. **Static public datasets (2021-2023): GSM8K, MATH, MATH-500.** Launched with very low scores
   (MATH: 3.0-6.9% for the LLMs of 2021), saturated within about 3-4 years (o1 reported 94.8% on OpenAI's MATH eval, which for o1 and later models is the MATH-500 subset per OpenAI's simple-evals README [corrected by fact-check]; DeepSeek-R1 97.3%
   on MATH-500). They were then retired from frontier reporting. Contamination and label noise
   drove the retirement as much as capability did. Scale AI's GSM1k showed drops of up to 13% (arXiv v1 abstract, May 2024) or up to 8% (NeurIPS 2024 version) [corrected by fact-check] for
   some model families (Mistral, Phi), and the size of each drop correlated with memorization of GSM8K. GSM8K-Platinum
   found that about 5% of GSM8K items were flawed, so the benchmark's practical ceiling sits below 100%.
2. **Recycled competition sets (2024-2025): AIME 2024/2025, HMMT, Omni-MATH, PutnamBench.**
   These were hard at launch and matched to human percentiles. But they are public, so contamination
   arrived quickly: MathArena estimated AIME 2024 scores were inflated by 10-20 points, and about 60 points for
   QwQ-Preview. Final-answer formats also reward pattern-matching over rigor.
3. **Live / temporally held-out evaluation (2025-): MathArena.** MathArena evaluates models on competitions
   held after each model's release, publishes all outputs, runs 4 samples per problem, and adds human-graded proof
   competitions (USAMO, IMO, Putnam). Its "Proof or Bluff" USAMO 2025 study (most models below 5%) exposed the gap
   between final-answer scores and proof ability. About 13 months later GPT-5.5 scored 98% on USAMO
   2026. In May 2026 MathArena itself published "Farewell to Final-Answer Competition Problems as
   Frontier Benchmarks".
4. **Expert-authored private benchmarks (Nov 2024-): FrontierMath.** FrontierMath has unpublished problems,
   answers that resist guessing, automatic verification, and a private holdout. It launched with frontier models below 2%. It is the most
   credible "hard" math benchmark, and also the most instructive failure case on governance:
   - OpenAI funded it and owns most of the problems. OpenAI's access to them was disclosed only after the o3 announcement (Dec 2024).
   - OpenAI's reported o3 score of 25.2% (aggressive test-time compute) compares with Epoch's later independent figure of about 10%.
   - The June 2026 v2 audit found errors in about 42% of problems. Correcting them raised scores by about 12 points; GPT-5.5 (xhigh) went from about 35% (v1, secondary) to 72.5% on Tier 4 v2 (Epoch benchmark page) [corrected by fact-check].
   - Tier 4 rose from a 5% top score at launch (Jul 2025) to 98% (GPT-6 Astra, Sep 2026). Epoch announced on Sep 10, 2026 that every Tier 4 problem had been solved at least once (secondary report quoting Epoch) [corrected by fact-check].
5. **Research-level, open-ended and formal (2026-):** First Proof (unpublished research lemmas with
   encrypted answers), FrontierMath Open Problems and FrontierMath Erdős, Formal Conjectures (1,029 open Lean
   conjectures), Riemann-Bench (25 private problems, all models below 10%), and MathArena ArXivMath/BrokenArXiv
   (monthly, drawn from new arXiv papers). The competition ceiling is gone: at IMO 2026 two systems
   (Huawei Celia, Xiaohongshu dots-note-3.0) reportedly received officially graded 42/42 scores. The other 42/42 results were not lab self-reports under official grading: Claude Fable 5, GPT-5.6 Sol and Kimi K3 were scored 42/42 by a third-party harness (Deedy Das) using Claude-based graders, and AxiomProver self-published Lean proofs [corrected by fact-check].

**Core lesson.** In math, benchmark credibility has come from four things:
- (a) **freshness**: problems created after the model's training cutoff;
- (b) **custody**: a held-out set controlled by a party other than the model developer;
- (c) **verifiability**: automatic answer checking or formal proof, plus expert grading of proofs;
- (d) **transparency about evaluation conditions**: compute, number of samples, and who graded.

Benchmark failure came from:
- public static items, which lead to contamination;
- label noise, which creates fake ceilings and hides true scores;
- final-answer-only formats, which reward guessing and shortcuts;
- small item counts, which make scores high-variance;
- undisclosed funder access;
- lab self-reported results under non-standard compute.

Saturation is also speeding up. Early benchmarks took years to saturate. The 2025 "hardest" ones (USAMO proofs, MathArena Apex, FrontierMath Tier 4) took about 9-14 months.

---

## Benchmark-by-benchmark

### 1. GSM8K (Grade School Math 8K)
- **Measures:** multi-step grade-school arithmetic word problems; final numeric answer.
- **Release / venue:** Oct 2021, arXiv:2110.14168 ("Training Verifiers to Solve Math Word Problems"). (H)
- **Creators:** OpenAI: Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, John Schulman [corrected by fact-check] (BibTeX in github.com/OpenLMLab/LEval citation.bib and github.com/Strivin0311/llms-learning) (H; seen via search summary of arxiv.org/pdf/2110.14168)
- **Items / format:** about 8.5K human-written problems (train plus 1,319-item test; fact-check: consistent with GSM8K-Platinum's 1,209 items = 1,319 - 110 removed, per the sglang benchmark README that runs `--num-questions 1209 --platinum` [corrected by fact-check]). Natural language in, number out.
- **Launch vs latest:** Launch baseline numbers were not verified this session. By 2025, "current frontier models achieving ~95% accuracy" and "recent frontier LLMs have excluded evaluations on GSM8K following concerns that it has reached saturation" (Vendrow et al., GSM8K-Platinum). (M)
- **Adoption:** For years it was a near-universal model-card metric. It is in EleutherAI lm-evaluation-harness (github.com/EleutherAI/lm-evaluation-harness task README seen in results). High citation count (exact count **unverified**).
- **Status:** **saturated + contaminated**; retired from frontier reporting; survives as a small-model/regression check.
- **Why it succeeded:** Cheap exact-match grading, clear human meaning ("grade school"), a large training split that made it a training target, and it arrived just as chain-of-thought prompting made it tractable.
- **Why it failed:**
  - It is fully public, and memorization was shown (GSM1k).
  - About 5% of items were flawed ("mislabeled or ambiguous"), so "progress ... often stalls before models actually achieve reliable performance" (GSM8K-Platinum).
  - It is too easy for reasoning models.
  - Surface-form fragility (GSM-Symbolic) showed that scores did not measure robust reasoning.
- **Sources:** https://arxiv.org/pdf/2110.14168 ; https://gradientscience.org/gsm8k-platinum/ ; https://arxiv.org/abs/2502.03461

### 2. GSM1k (Scale AI overfitting study)
- **Measures:** Whether GSM8K scores reflect memorization. It uses 1,000 new problems matched to GSM8K on human solve rate, number of steps, and answer magnitude.
- **Release / venue:** May 2024, arXiv:2405.00332; NeurIPS 2024 Datasets & Benchmarks Track. (H)
- **Creators:** Scale AI: Hugh Zhang, Jeff Da, Dean Lee, Vaughn Robinson, Catherine Wu, Will Song, Tiffany Zhao, Pranav Raja, Dylan Slack, Qin Lyu, Sean Hendryx, Russell Kaplan, Michele Lunati, Summer Yue [corrected by fact-check] (github.com/lyy1994/awesome-data-contamination).
- **Items / format:** 1,000 human-annotated problems, written "solely with human annotators, without assistance from any LLM". **Only 50 examples are released.** Scale commits to releasing the full set "when 3 open source models of different lineages reach 95+% accuracy on GSM1k" (fetched github.com/scaleapi/gsm1k_eval). (H)
- **Key results:**
  - The NeurIPS 2024 / latest abstract reports "accuracy drops of up to 8%, with several families of models showing evidence of systematic overfitting across almost all model sizes" (mirror: github.com/fzyzcjy/ai_math_paper_list render/neurips_2024.md). Mistral and Phi are named explicitly only in the v1 abstract. (H) [corrected by fact-check]
  - The **arXiv v1 abstract (May 1, 2024)**, not a NeurIPS version, says "accuracy drops of up to 13%, with several families of models (e.g., Phi and Mistral) showing evidence of systematic overfitting" and reports Spearman r^2 = 0.32 (mirrors: github.com/lyy1994/awesome-data-contamination; HuggingAGI/HuggingArxiv). The 13% -> 8% and 0.32 -> 0.36 changes are between arXiv v1 and the NeurIPS 2024 version; cite the figure matching the version. (H) [corrected by fact-check]
  - There is a positive relationship (Spearman r² = 0.36 in the NeurIPS version; 0.32 in v1 [corrected by fact-check]) between a model's probability of generating GSM8K examples and its GSM8K-to-GSM1k gap. (H)
  - Frontier models (GPT-4, Gemini, Claude) showed minimal overfitting. (H)
- **Status:** **niche / diagnostic.** It is a methodological landmark rather than a leaderboard. The private test set was never widely adopted, partly by design.
- **Why it succeeded:** It is the canonical demonstration of the "fresh-clone" method. It combines a held-out release policy with a pre-committed release trigger, and it gives causal-style evidence (memorization probability vs gap).
- **Why it failed as a benchmark:** It tests an already-easy skill, it is private, and it has no maintained leaderboard. Its value was the finding, not ongoing tracking.
- **Sources:** https://arxiv.org/pdf/2405.00332 ; https://scale.com/research/llm-performance-grade-school-arithmetic ; https://github.com/scaleapi/gsm1k_eval ; https://papers.nips.cc/paper_files/paper/2024/file/53384f2090c6a5cac952c598fd67992f-Paper-Datasets_and_Benchmarks_Track.pdf

### 3. GSM-Symbolic / GSM-NoOp (Apple): robustness perturbation of GSM8K
- **Measures:** Variance under template instantiation (changed names and numbers, added clauses) and under irrelevant "no-op" clauses.
- **Release / venue:** Oct 2024, arXiv:2410.05229; ICLR 2025. (H)
- **Creators:** Iman Mirzadeh, Keivan Alizadeh, Hooman Shahrokhi, Oncel Tuzel, Samy Bengio, Mehrdad Farajtabar (Apple). (H)
- **Findings:**
  - All models drop on GSM-Symbolic compared with GSM8K.
  - Models are more sensitive to changed numbers than to changed names.
  - Degradation and variance grow with the number of clauses.
  - GSM-NoOp causes drops of "up to 65%". (H, via ICLR paper summary)
  - A 2026 LessWrong post ("Revisiting GSM-Symbolic: do 2026 frontier models still fail") suggests frontier models now "seem to reason okay". (L; title seen only)
- **Status:** **niche / diagnostic** (templates are released at github.com/apple/ml-gsm-symbolic).
- **Lesson:** Perturbation-based variants expose memorization. But once published they become static themselves, and they measure robustness on easy items rather than frontier capability.
- **Sources:** https://arxiv.org/pdf/2410.05229 ; https://machinelearning.apple.com/research/gsm-symbolic ; https://www.lesswrong.com/posts/Ze4C99Dasj74YKCFh/revisiting-gsm-symbolic-do-2026-frontier-models-still-fail

### 4. GSM8K-Platinum (MIT Madry Lab): label-noise repair
- **Measures:** The same skill as GSM8K on a relabeled test set where "100% performance is attainable".
- **Release / venue:** Feb 2025, arXiv:2502.03461 ("Do Large Language Model Benchmarks Test Reliability?"); part of 15 "platinum benchmarks". (H)
- **Creators:** Joshua Vendrow, Edward Vendrow, Sara Beery, Aleksander Madry (fetched BibTeX, github.com/MadryLab/platinum-benchmarks). (H)
- **Method / result:** They inspected every question where any frontier LLM disagreed with the stated answer: 219 flagged; 110 removed, 99 verified, 10 relabeled. (H, via gradientscience summary) "Frontier language models still make mistakes on surprisingly simple tasks." (fetched)
- **Status:** **niche / active** as a reliability check.
- **Lesson:** "Saturation" at about 95% partly hid label noise. Benchmarks need an error-audit pipeline, and model disagreement is a cheap signal for finding bad items.
- **Sources:** https://gradientscience.org/gsm8k-platinum/ ; https://arxiv.org/abs/2502.03461 ; https://github.com/MadryLab/platinum-benchmarks

### 5. MATH (Hendrycks et al.)
- **Measures:** Competition mathematics (AMC 10/12, AIME and similar) across 7 subjects and 5 difficulty levels; final answer in a box, with full step-by-step solutions.
- **Release / venue:** Mar 2021, arXiv:2103.03874; NeurIPS 2021 Datasets & Benchmarks. (H)
- **Creators:** Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, Jacob Steinhardt (fetched BibTeX, github.com/hendrycks/math). (H)
- **Items / format:** 12,500 problems (7,500 train / 5,000 test; the split is **unverified** this session), plus the AMPS pretraining corpus.
- **Launch vs latest:**
  - At launch, LLM accuracy was 3.0-6.9%. The authors extrapolated that about 10^35 parameters would be needed for 40%, implying that scaling alone would not solve MATH. (M, via summaries citing the paper)
  - The Stanford AI Index 2026 describes it as "roughly 7% accuracy" at introduction, with "frontier models now exceed 90%, rendering the benchmark effectively saturated". (M)
  - o1 reported 94.8% (Sep 2024; cited in the Omni-MATH abstract as "OpenAI o1 achieves 94.8% on MATH dataset"). Caveat: OpenAI's simple-evals README states that "for newer models (anything on or after o1) we evaluate on MATH-500", so this is most likely a MATH-500 figure; simple-evals later lists the released o1 at 96.4. (M-H) [corrected by fact-check]
- **Adoption:** Ubiquitous in model cards 2022-2024. Basis of MATH-500 and PRM800K. High citations (exact count **unverified**).
- **Status:** **saturated** (and presumed contaminated because it is fully public with solutions).
- **Why it succeeded:** Graded difficulty levels, broad subject coverage, answers that check automatically, and truly low launch scores (about 5%), which gave it a long useful life of about 3.5 years. Its low launch scores were also wrong about the future in an informative way: the "10^35 parameters" extrapolation failed because of new methods (chain of thought, RL on reasoning).
- **Why it failed:** Public training split and solutions; the scale of contamination is unknown; answer-format parsing issues; ceiling effects.
- **Sources:** https://github.com/hendrycks/math/ ; https://arxiv.org/pdf/2103.03874 ; https://hai.stanford.edu/assets/files/ai_index_report_2026_chapter_2_technical.pdf ; https://arxiv.org/abs/2410.07985

### 6. MATH-500
- **Measures:** The same as MATH, on a 500-problem uniformly random held-out subset of the MATH test set.
- **Release:** May 2023, from OpenAI's "Let's Verify Step by Step" (Lightman et al., arXiv:2305.20050). OpenAI put 4.5K MATH test problems into the PRM800K training data and "evaluate[d] our models only on the remaining 500 held-out problems" (fetched github.com/openai/prm800k). (H) It was later redistributed as HuggingFaceH4/MATH-500.
- **Launch vs latest:** Their best PRM solved 78.2% (2023). (H) DeepSeek-R1 reported 97.3% (Jan 2025, arXiv:2501.12948). (H) Artificial Analysis still hosts a MATH-500 leaderboard (URL seen). (M)
- **Status:** **saturated** (above 97% by early 2025).
- **Lesson:** An in-house "held-out" subset of a public benchmark is only held out from the creator's own training. Everyone else's data pipelines still see the public MATH test problems.
- **Sources:** https://github.com/openai/prm800k ; https://cdn.openai.com/improving-mathematical-reasoning-with-process-supervision/Lets_Verify_Step_by_Step.pdf ; https://huggingface.co/datasets/HuggingFaceH4/MATH-500 ; https://arxiv.org/pdf/2501.12948

### 7. AIME 2024 / 2025 / 2026 (as used by labs)
- **Measures:** American Invitational Mathematics Examination: 15 problems per paper, integer answers 0-999. Two papers per year give 30 problems.
- **Adoption:** Became the headline reasoning metric in the "reasoning model" era.
  - OpenAI o1 (Sep 12, 2024): "74% (11.1/15) with a single sample, 83% (12.5/15) with consensus among 64 samples, and 93% (13.9/15) when re-ranking 1000 samples". (H, openai.com)
  - DeepSeek-R1: 79.8% pass@1 on AIME 2024. (H)
- **Contamination:**
  - The MathArena paper finds AIME 2024 "significantly contaminated". Most models score 10-20 points above the human-percentile-aligned expectation derived from their AIME 2025 score, and QwQ-Preview-32B is about 60 points above. (H, via arXiv:2505.23281 summary)
  - Even the "fresh" AIME 2025 was compromised: an identical problem to AIME 2025 I Q1 was found on Quora, and near-identical ones for Q3 and Q5 on math.stackexchange (Papailiopoulos, Feb 2025). (M)
  - One summary states "8 out of the 30 problems in AIME 2025 were identified as having close analogs in online sources". Fact-check: an independent 2026 survey (github.com/suncityldp/zx-bench, docs/LLM数学推理评测综述-2026.md) attributes this to the MathArena paper itself (8 AIME 2025 problems with near-versions online found via deep-research search, vs 1 for HMMT 2025). (M; still secondary) [corrected by fact-check]
- **Latest:** AIME 2026 is near ceiling. An aggregator (benchlm.ai) reports top models "clustered within 2.1 points" at about 95-99%. (L; aggregator) The Stanford AI Index 2026 describes AIME as transitioning "into an entry standard for model capability rather than ... a frontier evaluation set". (M)
- **Status:** **saturated / contaminated** as a frontier discriminator. Each new year's contest is still used as a "live" check, and MathArena hosts AIME 2026 (fetched README).
- **Why it succeeded:** Human anchoring (USAMO qualification cutoffs, percentiles), prestige, a fresh edition every year, and integer answers that are trivially graded.
- **Why it failed:**
  - Only 30 items a year, so scores are high-variance and one problem is worth 3.3 points.
  - Answers can be guessed or brute-forced.
  - Near-duplicates exist online even for new editions.
  - Labs report pass@1, consensus@64 and re-ranked@1000 interchangeably.
  - It saturated within about 18 months of o1.
- **Sources:** https://openai.com/index/learning-to-reason-with-llms/ ; https://arxiv.org/html/2505.23281v2 ; https://x.com/DimitrisPapail/status/1888325914603516214 ; https://www.emergentmind.com/topics/aime-2024-and-aime-2025-benchmarks ; https://hai.stanford.edu/assets/files/ai_index_report_2026_chapter_2_technical.pdf ; https://benchlm.ai/benchmarks/aime2026

### 8. HMMT (Harvard-MIT Mathematics Tournament) February 2025 / 2026
- **Measures:** A final-answer high-school competition (30 problems as used by MathArena), harder than AIME in combinatorics.
- **Results:**
  - At the MathArena HMMT Feb 2025 release, "only o3-mini crossing the 50% mark" (Mislav Balunović, X). (M)
  - Later, o4-mini (high) reached 82.5% and o3 (high) 77.5%. Combinatorics was consistently the weakest domain. (M; intuitionlabs summary of MathArena data)
  - For HMMT Feb 2026, aggregators show top scores of about 95-97% (e.g., "Qwen3.7 Max 97.1%"). (L; llm-stats/benchlm aggregators, **unverified** against MathArena)
- **Status:** **saturated** at the frontier by 2026 (per aggregators); still used for mid-size and open models.
- **Lesson:** Moving to harder fresh competitions buys roughly one year of headroom.
- **Sources:** https://x.com/mbalunovic/status/1891180987507245499 ; https://intuitionlabs.ai/articles/hmmt25-ai-benchmark-explained ; https://huggingface.co/datasets/MathArena/hmmt_feb_2026 ; https://llm-stats.com/benchmarks/hmmt-feb-26

### 9. MathArena (ETH Zurich SRI Lab / INSAIT): live, uncontaminated competition evaluation
- **Measures:** Model performance on math competitions held after the model's release. It started with final-answer contests (AIME, HMMT, BRUMO, SMT and others) and expanded to proof contests (USAMO, IMO, IMC, Putnam, Miklós Schweitzer), visual math (Kangaroo), Project Euler, the Apex sets, ArXivMath, BrokenArXiv and ArXivLean (fetched github.com/eth-sri/matharena). (H)
- **Release / venue:** Launched with AIME 2025 (Feb 2025). Paper arXiv:2505.23281 (May 2025), "MathArena: Evaluating LLMs on Uncontaminated Math Competitions", NeurIPS 2025 Datasets and Benchmarks track (ETH SRI publication page, github.com/eth-sri/eth-sri.github.io _publications/balunovic2025matharena.md) [corrected by fact-check]. The v1 abstract reported 30 models, 5 competitions and 149 problems, and "On USAMO 2025, even top models score below 25%". Follow-up: "Beyond Benchmarks: MathArena as an Evaluation Platform for Mathematics with LLMs", arXiv:2605.00674 (submitted May 1, 2026), ICML 2026 (venue not independently confirmed by fact-check). (H for paper; M for venue)
- **Creators:**
  - 2025 paper: Mislav Balunović, Jasper Dekoninck, Ivo Petrov, Nikola Jovanović, Martin Vechev. (H)
  - 2026 paper: Jasper Dekoninck, Nikola Jovanović, Tim Gehrunger, Kári Rögnvaldsson, Ivo Petrov, Chenhao Sun, Martin Vechev. (H; fetched BibTeX)
- **Items / format:** 162 problems across 7 competitions and more than 50 models at the time of the 2025 paper. By default it runs 4 samples per problem and reports mean accuracy with variance. Proof competitions are human-graded (and semi-automatic by 2026). All outputs are public. (H)
- **Key results:**
  - 2025 paper: "On IMO 2025, top models achieve slightly less than 40%." (H)
  - 2026 paper: "GPT-5.5 reaches 98% on the 2026 USA Math Olympiad and 74% on research-level questions." (H)
  - The model page shows GPT-5.5 (xhigh) at 98.21% on USAMO 2026 (not independently re-read; a Sep 2026 third-party read of the live USAMO 2026 board, github.com/turbobeest/modelspec benchmarks/usamo_2026.md, listed the top model at 95.2%, so live-board numbers can differ from the paper's 98% [corrected by fact-check]). For USAMO 2026 the automated and human graders "assign the same score for almost all solutions". (M)
- **Adoption:** Widely cited by the press (e.g., Scientific American used MathArena's IMO 2025 numbers). Hugging Face datasets are published per competition (e.g., MathArena/aime_2026, MathArena/hmmt_feb_2026). Paper accepted at ICML 2026. Lab model cards cite AIME/HMMT 2025 results, often via MathArena's framing (M).
- **Status:** **thriving** as a platform. Its final-answer sub-benchmarks are **saturated** by the maintainers' own admission.
- **Why it succeeded:**
  - It guarantees freshness by construction (temporal holdout).
  - Problems are "pre-vetted by competition organizers for originality" at zero authoring cost.
  - Human percentiles are built in.
  - It is transparent: public outputs, multiple runs, cost reporting.
  - It adds proof grading.
  - The maintainers are willing to retire their own benchmarks and publish negative findings, e.g. "Not Even Bronze" and "Farewell to Final-Answer Competition Problems". The self-retirement blog (May 12, 2026, Sun, Dekoninck, Vechev) reports three things. (M-H, via search summary of matharena.ai/no_final_answer)
    - GPT-5.5 solved the last unsolved Apex problem (IMO 2025 P6).
    - Apex Shortlist exceeds 90%.
    - On 176 fresh qualifying problems, Gemini 3.1 Pro solved 162 in all 4 attempts and each of the other 14 at least once. They concluded that final-answer competition problems "are no longer reliable for hard frontier-model benchmarks".
- **Why it is under pressure:**
  - It depends on the supply of human competitions, which is roughly 100-200 new problems a year and bounded in difficulty by the high-school and undergraduate ceiling.
  - Small per-competition item counts make scores noisy.
  - Online near-duplicates exist even for new contests (AIME 2025).
  - Proof grading is costly, and it increasingly relies on LLM judges.
- **Sources:** https://arxiv.org/abs/2505.23281 ; https://arxiv.org/abs/2605.00674 ; https://icml.cc/virtual/2026/82577 ; https://github.com/eth-sri/matharena ; https://matharena.ai/no_final_answer/ ; https://matharena.ai/models/openai_gpt_55 ; https://matharena.ai/usamo/

### 10. MathArena Apex (and Apex Shortlist)
- **Measures:** The hardest final-answer problems of 2025. There are 12 problems, each selected so that GPT-5, Grok 4, Gemini 2.5 Pro and GLM 4.5 all fail on all 4 attempts. Hundreds of 2025 problems were screened. (M-H)
- **Release:** Aug 2025 (Nikola Jovanović, X). At launch "the best model scoring only 5%"; another capture of the Apex page quotes "By design, the best model scores only 5.2%" (github.com/RishiJain905/LocalModelResearch) [corrected by fact-check]. Canonical citation: Dekoninck, Jovanović, Petrov, Vechev, "MathArena Apex: Unconquered Final-Answer Problems" (2025), as cited in the DeepSeek-V4.1 report reference list. MathArena's tables list Apex at 12 problems and Apex Shortlist at 47; by Sep 2026 MathArena marked Apex, Apex Shortlist, HMMT and AIME 2026 as Deprecated (github.com/fstandhartinger/model-market-comparison data/SCRAPING.md). (M)
- **Latest:** GPT-5.5 solved the last unsolved problem (IMO 2025 P6), and Apex Shortlist is at 90% or more (May 2026). (M)
- **Status:** **saturated** in about 9 months.
- **Lesson:** Adversarial filtering against current models, the way Apex was built, creates headroom that is quickly consumed. A set of 12 items is too small for fine-grained ranking.
- **Sources:** https://matharena.ai/apex/ ; https://x.com/ni_jovanovic/status/1957431094665736205 ; https://matharena.ai/no_final_answer/

### 11. USAMO 2025 proof evaluation ("Proof or Bluff")
- **Measures:** Full natural-language proofs for the 6 USAMO 2025 problems, graded by human expert judges with rubrics.
- **Release:** Mar 2025, arXiv:2503.21934; later at the AI4Math@ICML 2025 workshop. Authors: Ivo Petrov, Jasper Dekoninck, Lyuben Baltadzhiev, Maria Drencheva, Kristian Minchev, Mislav Balunović, Nikola Jovanović, Martin Vechev (ETH Zurich and INSAIT; ETH SRI publication page) [corrected by fact-check]. (H)
- **Result:** "All tested models struggled significantly, achieving less than 5% on average" (early version). A later summary says "none exceeding a score of 30%, and most achieving only trivial scores below 5%", which likely reflects later-added models. Fact-check: secondary summaries of the later version give Gemini-2.5-Pro about 25% (10.1/42), with all other models below 5% (github.com/Proteusiq/unthinking) [corrected by fact-check]. The authors found the following failure modes (H):
  - flawed logic;
  - unjustified assumptions;
  - lack of creativity;
  - self-assessment bias, where models claim success.
- **One year later:** GPT-5.5 (xhigh) scored 98.21% on USAMO 2026 (MathArena). (M-H)
- **Status of proof-olympiad evaluation:** **saturated at the frontier by 2026.**
- **Lesson:** Final-answer benchmarks (AIME) over-stated reasoning ability in early 2025, and proof-grading exposed the gap. The gap then closed within about 13 months, so format changes buy headroom but not permanence.
- **Sources:** https://arxiv.org/abs/2503.21934 ; https://files.sri.inf.ethz.ch/matharena/usamo_report.pdf ; https://www.sri.inf.ethz.ch/publications/petrov2025usamo ; https://matharena.ai/models/openai_gpt_55

### 12. IMO 2025 and IMO 2026 (competition-as-benchmark; lab claims)
- **IMO 2025 (July 2025):**
  - MathArena's independent evaluation of public models ("Not Even Bronze"): best was Gemini 2.5 Pro at 31% (13 points), below the 19/42 bronze cutoff. MathArena used best-of-32 selection. (M-H) Per Scientific American, Gemini 2.5 Pro, Grok 4, o3 high, o4-mini high and DeepSeek R1 "all failed to produce a single completely correct solution". (M)
  - Google DeepMind's advanced Gemini Deep Think was **officially graded and certified by IMO coordinators at 35/42**, the gold standard. It worked end-to-end in natural language within 4.5 hours. (H, deepmind.google blog)
  - OpenAI's experimental reasoning model got 35/42 as **graded by three former IMO medalists**, not via official IMO grading. It was announced before the closing ceremony, reportedly against an embargo request. Fact-check: the embargo point is contested; one careful secondary account notes there was no official IMO condemnation and that two versions of the requested release timing circulate (github.com/oratis/Markup) [corrected by fact-check]. (M; multiple secondary sources, e.g., LessWrong and Hacker News threads, theneuron)
  - IMO president Gregor Dolinar said the IMO "cannot validate the methods used by the AI models, including the amount of compute used or whether there was any human involvement". Fact-check: the primary IMO statement (imo2025.au news page, Jul 19, 2025, as transcribed in github.com/oratis/Markup) reads "the IMO cannot validate the methods, including the amount of compute used or whether there was any human involvement, or whether the results can be reproduced"; quote the primary wording [corrected by fact-check]. Terence Tao stressed that capability claims depend on testing methodology and floated separate AI Olympiads. (M, Scientific American)
  - A third-party paper (arXiv:2507.15855) claimed Gemini 2.5 Pro could reach gold with an agentic verification-and-refinement pipeline. MathArena criticized its methodology. (M)
- **IMO 2026 (Shanghai, July 15-16, 2026):**
  - Huawei's "Celia" and Xiaohongshu/RedNote's "dots-note-3.0" achieved **42/42 under the IMO's official judging process**, "the first time any large language model had achieved a perfect score" under official judging. (M, AFP via France24 and Taipei Times)
  - AFP also reports that models from OpenAI, Anthropic, Axiom Math and Moonshot ("Kimi K3") scored 42/42. Fact-check: these are not official or lab-graded results. Claude Fable 5, GPT-5.6 Sol (xhigh) and Kimi K3 were scored 42/42 by Deedy Das's (Menlo Ventures) self-administered harness with Claude-based grading agents, which its operator calls "strong but not authoritative"; AxiomProver's 42/42 is self-published Lean proofs, not officially IMO-verified. The Huawei and Xiaohongshu "official" gradings rest on company announcements and press reports; one source notes that the IMO's own news page carries no statement on AI grading in 2026. NVIDIA Nemotron 3 Ultra reportedly scored 30/42 (github.com/adamghaida/ai-hall-of-fame mathematics/imo-2026-perfect-score; github.com/HarperZ9/flywheel records/2026-07-25) [corrected by fact-check]. (M)
  - AxiomProver's repo reports 42/42 with Lean-verified proofs (457-4,229 lines of Lean 4 per problem; about 1,496 minutes of total solve time) (fetched github.com/AxiomMath/IMO2026). The repo does not state official grading. (H for repo content)
  - For comparison, only 7 of 666 human contestants scored 42/42. (M)
- **Status:** **saturated** (the maximum score has been reached, including under official conditions).
- **Why it "succeeded" as a benchmark:** It is the most legible milestone for the public, it involves official third-party grading, and the problems are fresh.
- **Why it failed as a benchmark:**
  - It has 6 problems a year.
  - There was no standard for compute, number of attempts, or human involvement.
  - Official and self-graded results were mixed in press coverage.
  - Announcement timing was a PR contest.
  - It saturated within one year of the first gold.
- **Sources:** https://deepmind.google/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/ ; https://matharena.ai/imo/ ; https://www.scientificamerican.com/article/mathematicians-question-ai-performance-at-international-math-olympiad/ ; https://www.lesswrong.com/posts/RcBqeJ8GHM2LygQK3/openai-claims-imo-gold-medal ; https://www.france24.com/en/live-news/20260723-ai-catches-up-with-humans-to-score-100-at-top-maths-contest ; https://www.taipeitimes.com/News/world/archives/2026/07/24/2003861308 ; https://github.com/AxiomMath/IMO2026 ; https://arxiv.org/pdf/2507.15855

### 13. IMO-Bench (Google DeepMind): IMO-AnswerBench / ProofBench / GradingBench / LeanProofBench
- **Measures:** IMO-level short answers, proofs graded with detailed guidelines for auto-grading, proof-grading ability, and Lean proofs.
- **Release / venue:** Nov 2025, arXiv:2511.01846, "Towards Robust Mathematical Reasoning", EMNLP 2025 (main). (H)
- **Creators:** Thang Luong, Dawsen Hwang, Hoang H. Nguyen, Golnaz Ghiasi, Yuri Chervonyi, Insuk Seo, Junsu Kim, Garrett Bingham, Jonathan Lee, Swaroop Mishra, Alex Zhai, Clara Huiyi Hu, Henryk Michalewski, Jimin Kim, Jeonghyun Ahn, Junhwi Bae, Xingyou Song, Trieu H. Trinh, Quoc V. Le, Junehyuk Jung (fetched BibTeX, github.com/google-deepmind/superhuman). (H)
- **Items:** IMO-ProofBench has 60 problems (30 Basic, 30 Advanced). (M) Other counts are **unverified**.
- **Results:** Gemini Deep Think scored 80.0% on IMO-AnswerBench and 65.7% on advanced IMO-ProofBench, "surpassing the best non-Gemini models by large margins of 6.9% and 42.4%". (M)
- **Maintenance:** v2 releases fixed "problems that had ambiguous problem statements or incorrect answers", a ProofBench typo, and "incorrect formalizations" in LeanProofBench (fetched). (H)
- **Status:** **active**.
- **Caveat (interpretation):** The benchmark was built by the lab whose model leads it and "played a crucial role" in that lab's IMO effort. That is a structural conflict of interest similar in kind to FrontierMath/OpenAI, though disclosed.
- **Sources:** https://aclanthology.org/2025.emnlp-main.1794/ ; https://github.com/google-deepmind/superhuman/tree/main/imobench/ ; https://www.alphaxiv.org/abs/2511.01846

### 14. FrontierMath (Epoch AI): Tiers 1-3, Tier 4, Open Problems, Erdős
- **Measures:** Research-grade mathematics problems with definite, automatically verifiable answers (numbers or mathematical objects checked by code). They are designed to be "guess-proof" and to require hours or days of work from experts.
- **Release / venue:** arXiv:2411.04872, submitted Nov 7, 2024 (latest version Dec 23, 2025). "Developed by Epoch AI with over 60 mathematicians". (H) Authors (v7): Elliot Glazer, Ege Erdil, Tamay Besiroglu, Diego Chicharro, Evan Chen, Alex Gunning, Caroline Falkman Olsson, Jean-Stanislas Denain, Anson Ho, Emily de Oliveira Santos, et al. (about 40 listed; mirror github.com/tiendungchs/PersonalWiki) [corrected by fact-check].
- **Items / format:**
  - v1: 300 core problems (Tiers 1-3; roughly 25% olympiad level, 50% graduate level, 25% research level (M)).
  - Tier 4: 50 problems, completed June 2025. Written mainly by professors and postdocs, each doing a several-week project; 2 are public and 48 private. (M-H, epoch.ai pages via search)
  - v2 (June 12, 2026): 338 problems, split into 295 (Tiers 1-3) and 43 (Tier 4). (M-H)
- **Launch score:** "Current state-of-the-art AI models solve under 2% of problems" (Nov 2024). (H)
- **Trajectory:**

  | Date | Result | Source / confidence |
  |---|---|---|
  | Dec 20, 2024 | OpenAI announced o3 at 25.2%, under "aggressive test-time compute settings" | M-H |
  | Apr 2025 | Epoch's independent evaluation of the released o3 found about 10% | M; dataconomy, the-decoder |
  | Jul 2025 | Tier 4 launched with a top score of 5% | M; Epoch X post via secondary summaries |
  | Oct 2025 | GPT-5 Pro set a Tier 4 record at 13%, "edging out Gemini 2.5 Deep Think by a single problem (not statistically significant)" | M-H; Epoch substack |
  | Oct 2025 analysis | Best single run on Tiers 1-3 was 29%, but 57% of problems had been solved by some model on some run ("pass@the-kitchen-sink"). GPT-5 pass@32 grew sub-logarithmically and capped below 50%. | M-H; Epoch Gradient Update |
  | Jan 2026 | GPT-5.2 Pro scored 31% on Tier 4. As of Jan 2026, 17 of 48 private Tier 4 problems had been solved by some model. | L-M; truncated X title and epoch.ai summary |
  | Mar 5, 2026 | GPT-5.4 Pro scored 50% on Tiers 1-3 and 38% on Tier 4. One newly solved Tier 4 problem appeared to be shortcut via a 2011 preprint it found. 42% (20/48) of Tier 4 had been solved at least once. It solved none of FrontierMath: Open Problems. | M-H; Epoch substack summary |
  | Jun 12, 2026 | **v2 audit** (details below) | M-H; epoch.ai + secondary |
  | Sep 2026 | GPT-6 Astra (released Sep 3, 2026) scored about 98% (97.6% ± 2.4%) on Tier 4 (v2); Epoch page captured Sep 24, 2026 lists 64 models tested, next best Claude Fable 5 (max) 90.2%. Scores are on the private set (43 minus 2 public = 41 problems, so 97.6% is 40/41, not "42 of 43" as some press says) [corrected by fact-check]. "Every FrontierMath Tier 4 problem has now been solved" at least once. Epoch considers Tier 4 saturated: "When Tier 4 was launched on July 11th, 2025, the top score was 5% ... less than 14 months later, the top score is 98%." | M; Epoch X post seen via search plus epoch.ai model page; wording from secondary summary |
  | Sep 2026 | Tiers 1-3 v2: an aggregator lists GPT-5.6 Sol at 89% | L; benchlm.ai aggregator, **unverified** against Epoch |

  Details of the June 12, 2026 v2 audit (42%, 338 = 295 + 43, 123/12 corrected and 5/7 removed are confirmed verbatim on the Epoch Tier 4 v2 page and changelog captured Sep 24, 2026 [corrected by fact-check]; the "~12 points higher" figure is secondary only):
  - It addressed errors in **42% of problems**: 123 corrected in Tiers 1-3 and 12 in Tier 4; 5 removed from Tiers 1-3 and 7 from Tier 4.
  - Most errors were "simple calculation mistakes ... off-by-one errors and flipped signs".
  - Models "scored around 12 percentage points higher on the corrected set", and rankings were similar.
  - GPT-5.5-xhigh's Tier 4 score reportedly rose from 35% to 73% (M; digitalapplied/Digg summaries). Fact-check: the Epoch Tier 4 v2 page (captured Sep 24, 2026, github.com/Develata/AI-Barking docs/0924/sources/usage/epoch-tier4.txt) lists GPT-5.5 (xhigh) at 72.5%; the ~35% v1 figure is secondary only [corrected by fact-check].
- **Human baseline:** In an MIT competition with 8 teams of 4-5 strong undergraduates or experts, given 4.5 hours and internet access on 23 questions, o4-mini-medium scored 22%, against 19% for the average team and 35% for all teams combined. Epoch: the informative human baseline is "somewhere between 30-50%". (M-H; Epoch Gradient Update by Anson Ho)
- **Funding / access controversy:**
  - OpenAI commissioned the 300 core problems and the 50 Tier 4 problems. OpenAI "retains ownership ... and has access to the problems and solutions, with the exception of a holdout set". (H; epoch.ai/latest/openai-and-frontiermath, seen via search)
  - The funding was disclosed only in a late arXiv version, around the o3 announcement. Fact-check: per Epoch's "Clarifying the creation and use of the FrontierMath benchmark" (Jan 23, 2025), the contract barred disclosure until around the o3 launch; the partnership was announced then, but the ownership and data-access terms were explained only in January 2025, after community criticism. "Only after" overstates the timing: say "at or around the o3 announcement (Dec 20, 2024), with access terms disclosed only in Jan 2025" [corrected by fact-check]. Earlier versions omitted it, and many of the 60+ contributing mathematicians were reportedly unaware. Tamay Besiroglu said Epoch "made a mistake" in not being more transparent. (M-H; the-decoder, LessWrong, Yahoo/TechCrunch syndication)
  - A **verbal** agreement prohibits OpenAI from training on the materials. (M)
  - For Tier 4, OpenAI has 28 of 48 problems and solutions, and Epoch holds out 20. Of GPT-5 Pro's 8 solved problems, 5 were in the held-out set (Oct 2025). That is evidence against a large access advantage at that point (M-H; Epoch substack). This is the kind of analysis that partly restored credibility.
- **Descendants:**
  - **FrontierMath: Open Problems** (Jan 2026 pilot): unsolved research problems with computationally verifiable solutions, expanded to 50 problems by Jul 31, 2026. On Aug 12, 2026, "Hadamard matrix of order 668" was marked solved by AI, credited to "a team of three humans and Claude" (reported by an Anthropic researcher). (M; epoch.ai pages via search)
  - **FrontierMath Erdős**: 68 Erdős problems formalized in Lean, about 10% of the unsolved problems at the time (Aug 2026). (M) Fact-check (secondary, the-vault-ai 2026-09-11): launched Sep 1, 2026; problems selected by Thomas Bloom and open as of August 2026; GPT-6 Astra solved 2 of 68 (3%) in the official run [corrected by fact-check].
- **Status:**
  - Tier 4: **saturated** (Sep 2026).
  - Tiers 1-3: **active but near ceiling** (aggregator, L).
  - Credibility: **contested but largely maintained**, thanks to the holdout analysis and independent re-evaluation.
  - Successor tracks: **active/thriving**.
- **Why it succeeded:**
  - Unpublished expert-authored problems.
  - Answers that resist guessing and are checked automatically, so no LLM judge is needed.
  - Very low launch score (<2%), which gave about 2 years of useful signal for Tiers 1-3.
  - Tiering that matches human expertise levels.
  - An independent evaluator runs the models (Epoch, not labs).
  - A private holdout.
  - Public, candid analysis: pass@N ceilings, human baselines, and error audits.
- **Why it failed or is failing:**
  - (1) **Funder conflict of interest and undisclosed access** damaged trust at the moment of its biggest headline.
  - (2) **Lab-reported scores under non-standard compute** (25.2% vs about 10%) muddied comparisons.
  - (3) **Label errors in 42% of problems** meant v1 scores understated capability by about 12 points and by up to about 38 points for individual models. Expert-authored does not mean correct: unpublished problems lose the "many eyes" error-correction of public benchmarks.
  - (4) **Small N** for Tier 4 (48, later 43) makes scores noisy.
  - (5) **Literature-retrieval shortcuts** (the 2011 preprint) blur "reasoning" and "search".
  - (6) Saturation within about 14 months for Tier 4, despite being designed as research-level.
- **Sources:** https://arxiv.org/abs/2411.04872 ; https://epoch.ai/latest/openai-and-frontiermath ; https://the-decoder.com/openai-quietly-funded-independent-math-benchmark-before-setting-record-with-o3/ ; https://www.lesswrong.com/posts/8ZgLYwBmB3vLavjKE/some-lessons-from-the-openai-frontiermath-debacle ; https://dataconomy.com/2025/04/21/openais-o3-claimed-25-percent-independent-test-says-try-10/ ; https://epochai.substack.com/p/frontiermath-tier-4-battle-royale ; https://epochai.substack.com/p/gpt-54-set-a-new-record-on-frontiermath ; https://epoch.ai/gradient-updates/less-than-70-percent-of-frontiermath-is-within-reach-for-todays-models ; https://epoch.ai/gradient-updates/is-ai-already-superhuman-on-frontiermath ; https://epoch.ai/benchmarks/frontiermath-tier-4-v2 ; https://x.com/EpochAIResearch/status/2065488154086568445 ; https://www.digitalapplied.com/blog/epoch-frontiermath-v2-error-corrected-ai-benchmark-analysis ; https://x.com/EpochAIResearch/status/2098103831502708864 ; https://epoch.ai/models/gpt-6-astra ; https://epoch.ai/frontiermath/open-problems ; https://epoch.ai/latest/announcing-frontiermath-erdos

### 15. PutnamBench (formal theorem proving)
- **Measures:** Formal proofs of Putnam competition theorems in Lean 4, Isabelle and Coq, checked by proof assistants.
- **Release / venue:** Jul 2024, arXiv:2407.11214; NeurIPS 2024 Datasets & Benchmarks. (H)
- **Creators:** George Tsoukalas, Jasper Lee, John Jennings, Jimmy Xin, Michelle Ding, Michael Jennings, Amitayush Thakur, Swarat Chaudhuri (UT Austin Trishul lab; fetched BibTeX). (H)
- **Items:** 1,724 formalizations (672 Lean 4, 640 Isabelle, 412 Coq) in the **current** repo (fetched README; problems from 1962-2025). This is not the launch size: the NeurIPS 2024 / arXiv v2 abstract reports 1,692 formalizations of 640 theorems (v1: 1,697). [corrected by fact-check] (H)
- **Launch:** "Only 6 problems were successfully proven" across all methods. (H)
- **Latest:** Confirmed from the official leaderboard data (raw.githubusercontent.com/trishullab/PutnamBench/main/docs/results.json): Hilbert 462 (avg pass@1840, Oct 2025); Seed-Prover 1.5 581 (10 H20-days per problem, Dec 27, 2025); Aleph Prover (Logical Intelligence) 668/672 (Jan 11, 2026; avg $68, limit $1,400 per problem); and **Aleph Prover 672/672, "problems: all" (Aug 26, 2026; avg $74, max $1,468 per problem)**. The leaderboard page now headlines "Lean — all 672 solved (cheapest first)". [corrected by fact-check] (H)
- **Status:** **saturated** on Lean (672/672, Aug 2026). The leaderboard now ranks by cost. [corrected by fact-check]
- **Why it succeeded:** Verification is perfect (proof checker), so there is no judge or label noise at the proof level. It is multi-language. Low launch score. It has a public leaderboard.
- **Why it is failing:**
  - The Putnam problems and informal solutions are public, so contamination is possible at the idea level.
  - Formalizations can be mis-stated, and the formal statement has to be trusted.
  - Compute budgets vary enormously (pass@1840, GPU-days per problem), so leaderboard numbers are hard to compare without a cost axis.
- **Sources:** https://arxiv.org/pdf/2407.11214 ; https://github.com/trishullab/PutnamBench ; https://arxiv.org/pdf/2512.17260 ; https://arxiv.org/html/2602.24273v2

### 16. Putnam 2025 live (AxiomProver) and Putnam-AXIOM (variations)
- **Putnam 2025 (Dec 6, 2025):** AxiomProver (Axiom Math) produced Lean 4.21.0 proofs for all 12 problems, verified with SafeVerify. **8 were solved within the competition window and 4 (A5, A6, B4, B6) afterwards** (fetched github.com/AxiomMath/putnam2025). The README does not state whether humans formalized the problem statements. (H) MathArena also evaluated Putnam 2025 (fetched README). (H) A secondary claim that 12/12 is "only the sixth perfect score in 98 years" is (L).
- **Putnam-AXIOM** (arXiv:2508.08292; ICML 2025 poster; an earlier version appeared at a NeurIPS 2024 workshop per the URL seen):
  - 522 Putnam problems plus 100 programmatic "functional variations". (M-H)
  - o1-preview scores 41.9% on the originals but loses 19.6 points (a 46.8% relative drop) on the variations.
  - Fine-tuning on the originals raised original accuracy to 80% but variation accuracy only to 33%, clear evidence of memorization. (M-H)
- **Lesson:** Formal verification removes grading ambiguity. Functional variations are a cheap contamination probe, and the evidence cuts both ways: memorization is real, and it can be distinguished from reasoning.
- **Sources:** https://github.com/AxiomMath/putnam2025 ; https://matharena.ai/putnam/ ; https://arxiv.org/abs/2508.08292 ; https://icml.cc/virtual/2025/poster/44232

### 17. Omni-MATH (and Omni-MATH-2)
- **Measures:** Olympiad-level final-answer problems across more than 33 sub-domains and more than 10 difficulty levels.
- **Release / venue:** Oct 10, 2024, arXiv:2410.07985; ICLR 2025. (H)
- **Creators:** Bofei Gao, Feifan Song, Zhe Yang, Zefan Cai, Yibo Miao, Qingxiu Dong, Lei Li, Chenghao Ma, Liang Chen, Runxin Xu, Zhengyang Tang, Benyou Wang et al. (Peking University and others; the affiliation is **unverified**). (H for names seen)
- **Items:** 4,428 problems. Omni-MATH-Rule is a subset of 2,821 problems that can be graded by exact match; the rest need an LLM judge (the paper provides an "Omni-Judge"; its details are **unverified** this session). (H/M)
- **Launch vs latest:** o1-mini 60.54% and o1-preview 52.55% at launch. (H) One secondary summary says the state of the art later reached "around 85%". (L)
- **Audit (2026):** Ballon, Algaba, Verbeken, Ginis, "Benchmarks Saturate When The Model Gets Smarter Than The Judge" (arXiv:2601.19532; Jan 27, 2026). They produced **Omni-MATH-2**: 647 problems edited (14.6%), 247 tagged non-standard (5.6%) because of missing images, proof or estimation requests, duplicates or missing answers. Omni-MATH-2-Filtered has 4,181 problems. Their argument is that saturation can come from a judge that is weaker than the model, not from a capability ceiling (fetched github README). (H)
- **Status:** **saturating / noisy**; niche.
- **Lesson:** Scraped competition corpora carry label noise of about 15%. When an LLM judge is used, the judge sets the ceiling.
- **Sources:** https://arxiv.org/abs/2410.07985 ; https://omni-math.github.io/ ; https://arxiv.org/abs/2601.19532 ; https://github.com/MartheBallon/Benchmarks-saturate-when-the-model-gets-smarter-than-the-judge

### 18. 2026 research-level math benchmarks
- **First Proof** (arXiv:2602.05192; Feb 5, 2026; revised Mar 16, 2026):
  - Authors: Mohammed Abouzaid, Andrew J. Blumberg, Martin Hairer, Joe Kileel, Tamara G. Kolda, Paul D. Nelson, Daniel Spielman, Nikhil Srivastava, Rachel Ward, Shmuel Weinberger, Lauren Williams. (H)
  - Format: 10 research lemmas "which have arisen naturally in the research process of the authors", never posted online, with answers **encrypted** for a short time. Entrants had one week. (H)
  - Results: OpenAI had about 5 proofs that appeared correct, and Google DeepMind's Aletheia about 6 (experts not unanimous on one). Some correct answers were "copied so closely from published works without citing them that they would have been rejected for plagiarism". (M-H; Scientific American)
  - Second batch: the best model got "six or seven of the 10 questions basically right" ("C-"). Fact-check (secondary): the batch-2 report (arXiv:2606.18119; testing May 28-Jun 1, 2026) says 7 of 10 problems received at least one passing grade from at least one system (github.com/tobiasosborne/ai-agents-seminar) [corrected by fact-check]. The project is framed as "a response to AI companies' growing fixation on using advanced math as a benchmark ... regardless of whether those metrics reflect the problems professional mathematicians actually care about". (M-H; Scientific American)
  - Status: **active, high-credibility, low-throughput** (10 problems per round, expert grading).
- **Riemann-Bench** (arXiv:2604.06802; Apr 8, 2026; ICLR 2026 workshop "Logical Reasoning of LLMs" (workshop venue not re-verified); Surge AI: authors Suhaas Garre, Erik Knutsen, Sushant Mehta, Edwin Chen; Surge blog post dated Mar 24, 2026 [corrected by fact-check]):
  - 25 private problems by "Ivy League mathematics professors, graduate students, and PhD-holding IMO medalists".
  - Each problem gets double-blind verification by two experts who solve it from scratch, and has a unique closed-form answer with programmatic verification.
  - "All frontier models currently score below 10%." (M-H)
  - Status: **new**. N=25 is very small, and it is commercially produced (interpretation).
- **Formal Conjectures** (Google DeepMind plus community; arXiv:2605.13171, May 13, 2026; authors Moritz Firsching, Paul Lezeau, Salvatore Mercuri, Miklós Z. Horváth, Yaël Dillies, Calle Sönne, Eric Wieser, Fred Zhang, Thomas Hubert, Blaise Agüera y Arcas, Pushmeet Kohli [corrected by fact-check]; GitHub Apache-2.0 / CC-BY-4.0):
  - 2,615 Lean 4 statements, including 1,029 open conjectures (a "zero-contamination testbed") and 836 solved problems for autoformalization.
  - It has "already enabled new mathematical discoveries". (M-H)
  - Versioned tags track mathlib releases (fetched). (H)
- **MathArena ArXivMath / BrokenArXiv / ArXivLean** (2026):
  - ArXivMath has monthly final-answer research problems extracted from the previous month's arXiv papers.
  - BrokenArXiv has "plausible but false" statements perturbed from new papers. A model fails if it "proves" the false statement, so the benchmark directly measures bluffing.
  - ArXivLean is the formal-proof counterpart. (M-H)
  - GPT-5.5 scored 74% on research-level questions (Beyond Benchmarks). (H)
- **Seen only as titles (not characterized, do not cite for content without verification):**
  - SOOHAK: "A Mathematician-Curated Benchmark" (arXiv:2605.09063)
  - "Benchmarks in Leipzig" (arXiv:2606.05818)
  - "The Ramanujan Challenge For AI" (arXiv:2607.09721)
  - "OEIS Open" (arXiv:2608.11941)
  - "Automated Conjecture Resolution with Formal Verification" (arXiv:2604.03789)

### 19. Cautionary episode: GPT-5 and the Erdős problems (Oct 2025)
- OpenAI's Kevin Weil tweeted that GPT-5 "found solutions to 10 (!) previously unsolved Erdős problems". Thomas Bloom (erdosproblems.com) called this "a dramatic misinterpretation": "open" on his site meant he didn't know of a solution. GPT-5 had found existing literature. The tweet was deleted, and Demis Hassabis criticized the communication. (M-H; the-decoder, Slashdot)
- Terence Tao's community wiki on AI contributions to Erdős problems separates primary contributions (AI standalone, AI alongside literature, and so on) from secondary ones (literature search, formalization, rewriting, computation). It states explicitly: **"This page is not a benchmark"**, warning of selection bias and incomplete literature review (fetched). (H)
- **Lesson:** Open-problem "benchmarks" need a verified-novelty protocol and a contribution taxonomy. Otherwise, literature retrieval is scored as discovery.
- **Sources:** https://the-decoder.com/leading-openai-researcher-announced-a-gpt-5-math-breakthrough-that-never-happened/ ; https://science.slashdot.org/story/25/10/20/1827201/openais-embarrassing-math ; https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems

### Saturation timeline (headline evidence)

| Benchmark | Launch top score (date) | Latest frontier (date) | Time to ~saturation | Conf. |
|---|---|---|---|---|
| MATH | 3.0-6.9% (2021) | 94.8% o1 (Sep 2024; likely MATH-500 [corrected by fact-check]); ">90%" (AI Index 2026) | ~3.5 yr | M |
| MATH-500 | 78.2% PRM (2023) | 97.3% DeepSeek-R1 (Jan 2025) | ~1.7 yr | H |
| GSM8K | (unverified) | ~95% (2025) | ~3-4 yr | M |
| USAMO proofs | <5% avg (Mar 2025) | 98.21% GPT-5.5 on USAMO 2026 (~May 2026) | ~13-14 mo | M-H |
| IMO | 31% best public model (Jul 2025); 35/42 lab systems | 42/42 officially graded (Jul 2026) | ~12 mo | M |
| MathArena Apex (12) | 5% (Aug 2025) | last problem solved by GPT-5.5 (by May 2026) | ~9 mo | M |
| FrontierMath T1-3 | <2% (Nov 2024) | 50% GPT-5.4 Pro (Mar 2026); ~89% v2 per aggregator (Sep 2026) | ~2 yr (approaching) | M / L |
| FrontierMath T4 | 5% (Jul 2025) | ~98% GPT-6 Astra, declared saturated (Sep 2026) | ~14 mo | M |
| PutnamBench | 6/640 (Jul 2024) | 581 Seed-Prover 1.5 (Dec 2025); 668/672 Aleph (Jan 2026); 672/672 Aleph (Aug 26, 2026) [corrected by fact-check] | ~2 yr | H |
| Riemann-Bench | <10% (Apr 2026) | n/a | open | M |

---

## Cross-cutting success factors

1. **Temporal holdout (freshness by construction).** Evaluating on problems created after model release (MathArena, First Proof, ArXivMath monthly) is the only contamination defence that needs no trust in any party. It turned AIME and HMMT from contaminated into usable for about one year each.
2. **Custodial holdout with pre-committed release rules.** GSM1k (50 of 1,000 released; full release when 3 open models of different lineages reach 95%+) and FrontierMath's Epoch-held subsets (the 50-problem holdout, 20/48 of Tier 4). The explicit holdout-versus-access analysis (5 of GPT-5 Pro's 8 Tier 4 solves were in the holdout) restored credibility after the funding scandal.
3. **Expert-authored, unpublished, guess-resistant items with automatic verification.** FrontierMath's design of large, non-guessable answers checked by code avoids both LLM-judge ceilings and easy guessing. The same holds for Riemann-Bench, where two experts independently re-solve each problem.
4. **Machine-checkable proofs.** PutnamBench, Formal Conjectures and AxiomProver's Lean outputs remove grading ambiguity and scale to open problems.
5. **Large launch headroom.** Benchmarks launched below about 5% (MATH, FrontierMath, PutnamBench, Apex) had the longest and most informative trajectories.
6. **Human anchoring.** Competition percentiles and medals (AIME/USAMO cutoffs, IMO medals, the FrontierMath MIT team baseline) make scores legible to the public and to labs, which drives adoption.
7. **An independent evaluator running the models.** Epoch and MathArena both run models themselves, report multiple runs and variance, and publish outputs. They caught the o3 25% vs about 10% discrepancy and the IMO "Not Even Bronze" gap.
8. **Maintainers who retire or repair their own benchmarks.** Examples are MathArena's "Farewell to Final-Answer..." post, FrontierMath v2, IMO-Bench v2 and GSM8K-Platinum. Candid self-audit increases trust.
9. **Evolving from benchmark to platform or ladder.** FrontierMath went from Tiers 1-3 to Tier 4 to Open Problems and Erdős. MathArena went from final-answer contests to Apex, proofs, ArXivMath, BrokenArXiv and Lean. Both keep one brand and protocol while replacing items as they saturate.
10. **Measuring rigor, not just answers.** Proof grading (USAMO/IMO) and false-statement detection (BrokenArXiv) exposed failure modes that final answers hid ("bluffing" and self-assessment bias).

## Cross-cutting failure factors

1. **Public static test sets become contaminated.** Evidence: GSM1k gaps (up to 8-13%, r² = 0.36 with memorization), AIME 2024 inflated by 10-20 points (60 for QwQ), Putnam-AXIOM variations (−46.8% relative for o1-preview; fine-tuning gives 80% on originals vs 33% on variations), and online near-duplicates for AIME 2025.
2. **Label noise creates fake ceilings and hides true scores.** GSM8K had about 5% flawed items. Omni-MATH had 14.6% of items edited. FrontierMath had errors in **42%** of problems, which depressed scores by about 12 points (35% vs 73% for one model on Tier 4). IMO-Bench also needed v2 fixes. Expert authorship without redundant solving is not enough.
3. **The judge ceiling.** When grading needs an LLM judge (Omni-MATH non-rule subset, proof grading), the benchmark saturates once the model outgrows the judge (Ballon et al., 2026).
4. **The final-answer format rewards shortcuts.** It allows guessing, numeric pattern-matching, brute force, and literature lookup (the 2011 preprint on FrontierMath). It misses rigor: models scored below 5% on USAMO proofs while scoring highly on AIME.
5. **Small N gives high variance.** AIME has 30 items a year, IMO 6, Apex 12, FrontierMath Tier 4 48 private in v1 and 41 private in v2 [corrected by fact-check], Riemann-Bench 25, First Proof 10. Rankings among top models are often within noise ("not statistically significant", Epoch).
6. **Funder conflicts of interest and undisclosed access.** OpenAI funded and owns FrontierMath and has access to most of it. The funding was disclosed late, contributing mathematicians were not told, and the no-training safeguard is a verbal agreement. Lab-built benchmarks topped by the same lab's model (IMO-Bench) are a milder version of the same problem.
7. **Non-standardized evaluation conditions in lab self-reports.** Examples: o3 at 25.2% with aggressive compute vs about 10% for the released model; pass@1 vs cons@64 vs re-rank@1000 on AIME; best-of-n at IMO; self-graded vs officially graded IMO results; announcements before embargoes lift.
8. **Accelerating saturation.** The useful life of benchmarks has fallen from about 3-4 years (MATH, GSM8K) to about 9-14 months (USAMO proofs, Apex, FrontierMath Tier 4), even for benchmarks explicitly designed as "research-level". Any new benchmark needs a renewal mechanism, not just difficulty.
9. **Confusing discovery with retrieval.** The Erdős episode, the GPT-5.4 Pro shortcut via a 2011 preprint, and plagiarism-like First Proof answers show that "solved" needs a novelty and attribution protocol.
10. **Low throughput of high-credibility formats.** Expert proof grading and research-lemma challenges (First Proof, IMO official grading) are credible but produce about 10 data points per round and cannot support continuous leaderboards.

## Implications for designing a new (non-game) benchmark (interpretation, for Phase 2)
- Build in **renewal**: continuous generation of fresh items tied to a date, with the item source external to labs.
- Build in **custody**: a third-party-held private split, a pre-committed release policy, and a published analysis of access versus holdout.
- **Verify labels redundantly**: at least two independent expert solves, plus model-disagreement audits before release. Budget for a v2 audit.
- Prefer **machine-checkable outputs** (executable checks, formal proofs, or verifiable objects) over LLM judges. If a judge is used, report judge-vs-human agreement and cap claims at the judge's ability.
- **Standardize and report compute**: tokens, samples, tools, wall-clock time, and cost as first-class axes (pass@k curves, as in "pass@the-kitchen-sink").
- Include **"broken" or false items** (BrokenArXiv style) so that bluffing is scored.
- Use a **large enough N**, with confidence intervals, to rank the top 10 models.
- Require a **novelty/attribution protocol** for any open-problem component.

---

## Claims ledger

1. GSM1k (1,000 new human-written GSM8K-style problems) found accuracy drops of up to 8% (NeurIPS 2024 abstract; up to 13% with r² = 0.32 in the arXiv v1 abstract [corrected by fact-check]) for some models, with Mistral and Phi showing systematic overfitting across almost all sizes. Spearman r² = 0.36 between a model's probability of generating GSM8K examples and its GSM8K-GSM1k gap; frontier models showed minimal overfitting. Sources: https://arxiv.org/pdf/2405.00332 ; https://scale.com/research/llm-performance-grade-school-arithmetic. **Confidence: H** (the 13% figure is from arXiv v1, not a NeurIPS summary [corrected by fact-check]).
2. Scale AI released only 50 GSM1k examples and committed to a full release when 3 open-source models of different lineages reach 95%+. Source: https://github.com/scaleapi/gsm1k_eval (fetched). **H**
3. GSM8K-Platinum inspected 219 questions flagged by frontier-model disagreement: 110 removed, 99 verified, 10 relabeled. About 5% of GSM8K questions had problems. Sources: https://gradientscience.org/gsm8k-platinum/ ; https://arxiv.org/abs/2502.03461. **H/M**
4. GSM-NoOp (irrelevant clauses) caused performance drops of up to 65% across state-of-the-art models (ICLR 2025). Source: https://arxiv.org/pdf/2410.05229. **H**
5. MATH (12,500 problems, NeurIPS 2021) launched with LLM accuracy of 3.0-6.9%, and frontier models now exceed 90% (AI Index 2026). Sources: https://arxiv.org/pdf/2103.03874 ; https://hai.stanford.edu/assets/files/ai_index_report_2026_chapter_2_technical.pdf. **M**
6. MATH-500 is a 500-problem uniformly random held-out subset created by OpenAI because 4.5K MATH test problems were used in PRM800K training. Sources: https://github.com/openai/prm800k (fetched). **H**. DeepSeek-R1 reported 97.3% on MATH-500 and 79.8% on AIME 2024: https://arxiv.org/pdf/2501.12948. **H**
7. OpenAI o1 (Sep 2024) reported AIME 2024 scores of 74% (single sample), 83% (consensus of 64) and 93% (re-rank of 1,000). Source: https://openai.com/index/learning-to-reason-with-llms/. **H**
8. The MathArena paper found AIME 2024 significantly contaminated. Most models score 10-20 points above human-percentile-aligned expectations, and QwQ-Preview-32B about 60 points above. Source: https://arxiv.org/html/2505.23281v2. **H/M**
9. Problems identical or near-identical to AIME 2025 I problems 1, 3 and 5 existed online (Quora, math.stackexchange) before the contest. Sources: https://x.com/DimitrisPapail/status/1888325914603516214 ; https://arxiv.org/html/2505.23281v2. **M**
10. At the time of the 2025 paper, MathArena covered 162 problems from 7 competitions and more than 50 models; top models scored slightly under 40% on IMO 2025. Source: https://arxiv.org/abs/2505.23281. **H**
11. On USAMO 2025 proofs, models averaged below 5% ("Proof or Bluff"). Source: https://arxiv.org/abs/2503.21934. **H**
12. GPT-5.5 reaches 98% on USAMO 2026 and 74% on research-level questions (MathArena "Beyond Benchmarks", ICML 2026). Sources: https://arxiv.org/abs/2605.00674 ; https://matharena.ai/models/openai_gpt_55. **H/M**
13. MathArena Apex (12 hardest 2025 final-answer problems) launched with a best score of 5%. By May 2026 GPT-5.5 had solved its last unsolved problem, and Apex Shortlist exceeded 90%. On 176 fresh problems Gemini 3.1 Pro solved 162 in all 4 attempts. MathArena declared final-answer competition problems no longer reliable for frontier benchmarking. Sources: https://matharena.ai/apex/ ; https://matharena.ai/no_final_answer/. **M**
14. At IMO 2025, MathArena's best public model (Gemini 2.5 Pro) scored 31% (13/42), below bronze. Google DeepMind's Gemini Deep Think was officially certified by IMO coordinators at 35/42. OpenAI's 35/42 was graded by three former medalists, not officially. Sources: https://matharena.ai/imo/ ; https://deepmind.google/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/ ; https://www.lesswrong.com/posts/RcBqeJ8GHM2LygQK3/openai-claims-imo-gold-medal. **H (DeepMind) / M (OpenAI grading)**
15. The IMO president said the IMO "cannot validate the methods used by the AI models, including the amount of compute used or whether there was any human involvement". Source: https://www.scientificamerican.com/article/mathematicians-question-ai-performance-at-international-math-olympiad/. **M-H**
16. At IMO 2026, Huawei's Celia and Xiaohongshu's dots-note-3.0 scored 42/42 under official IMO judging, a first (per company announcements and press; not confirmed on an IMO page). Other 42/42 results (Claude Fable 5, GPT-5.6 Sol, Kimi K3) came from a third-party harness with Claude-based graders, and AxiomProver's from self-published Lean proofs [corrected by fact-check]. 7 of 666 humans scored perfectly. Sources: https://www.france24.com/en/live-news/20260723-ai-catches-up-with-humans-to-score-100-at-top-maths-contest ; https://github.com/AxiomMath/IMO2026. **M**
17. FrontierMath (arXiv:2411.04872, Nov 2024; Epoch AI with 60+ mathematicians) launched with state-of-the-art models solving under 2%, using unpublished problems and automated verification. Source: https://arxiv.org/abs/2411.04872. **H**
18. OpenAI commissioned the 300 core FrontierMath problems (and the 50 Tier 4 problems), owns them, and has access to problems and solutions except for a holdout. The partnership was disclosed only around o3's Dec 20, 2024 announcement (the contract barred earlier disclosure), and the ownership and access terms only on Jan 23, 2025 [corrected by fact-check]. Epoch acknowledged a transparency mistake. Sources: https://epoch.ai/latest/openai-and-frontiermath ; https://the-decoder.com/openai-quietly-funded-independent-math-benchmark-before-setting-record-with-o3/ ; https://www.lesswrong.com/posts/8ZgLYwBmB3vLavjKE/some-lessons-from-the-openai-frontiermath-debacle. **H/M**
19. OpenAI claimed 25.2% for o3 on FrontierMath (Dec 2024, aggressive test-time compute), while Epoch's April 2025 independent test of the released o3 found about 10%. Sources: https://dataconomy.com/2025/04/21/openais-o3-claimed-25-percent-independent-test-says-try-10/ ; https://the-decoder.com/openai-quietly-funded-independent-math-benchmark-before-setting-record-with-o3/. **M-H**
20. On FrontierMath Tier 4, OpenAI has access to 28 of 48 problems and Epoch holds out 20. GPT-5 Pro set a 13% record (Oct 2025), and 5 of its 8 ever-solved problems were in the holdout. Source: https://epochai.substack.com/p/frontiermath-tier-4-battle-royale. **M-H**
21. FrontierMath v2 (June 12, 2026) addressed errors in 42% of problems (123 corrected and 5 removed in Tiers 1-3; 12 corrected and 7 removed in Tier 4), leaving 338 problems (295 + 43). Models scored about 12 points higher on the corrected set. Sources: https://epoch.ai/benchmarks/frontiermath-tier-4-v2 ; https://x.com/EpochAIResearch/status/2065488154086568445 ; https://www.digitalapplied.com/blog/epoch-frontiermath-v2-error-corrected-ai-benchmark-analysis. **M**
22. FrontierMath Tier 4 went from a 5% top score at launch (July 11, 2025) to 98% (GPT-6 Astra, Sep 2026). Every Tier 4 problem has been solved at least once, and Epoch considers it saturated. Sources: https://x.com/EpochAIResearch/status/2098103831502708864 ; https://epoch.ai/models/gpt-6-astra ; https://www.kucoin.com/news/flash/gpt-6-astra-solves-final-frontiermath-tier-4-problem. **M** (primary is an X post seen only via search; wording from a secondary source)
23. In an Epoch human-baseline competition (8 teams, 4.5 hours, 23 questions), o4-mini-medium scored 22%, against 19% for the average team and 35% for all teams combined. Source: https://epoch.ai/gradient-updates/is-ai-already-superhuman-on-frontiermath. **M-H**
24. Epoch: best single FrontierMath run 29%, 57% of problems ever solved by any model/run, and GPT-5 pass@32 capped below 50%. Source: https://epoch.ai/gradient-updates/less-than-70-percent-of-frontiermath-is-within-reach-for-todays-models. **M-H**
25. GPT-5.4 Pro scored 50% on FrontierMath Tiers 1-3 and 38% on Tier 4 (Mar 2026). One new solve appeared to use a 2011 preprint as a shortcut, and it solved no FrontierMath Open Problems. Source: https://epochai.substack.com/p/gpt-54-set-a-new-record-on-frontiermath. **M-H**
26. PutnamBench (NeurIPS 2024) now has 1,724 formalizations (672 Lean 4, 640 Isabelle, 412 Coq); at NeurIPS 2024 it had 1,692 formalizations of 640 theorems [corrected by fact-check]. Only 6 problems were proven at launch (paper §4.2, confirmed). Lean was fully solved (672/672, Aleph Prover) on Aug 26, 2026 [corrected by fact-check]. Sources: https://github.com/trishullab/PutnamBench ; https://arxiv.org/pdf/2407.11214. **H**
27. AxiomProver produced Lean proofs for all 12 Putnam 2025 problems, 8 within the competition window and 4 afterwards. Source: https://github.com/AxiomMath/putnam2025. **H**
28. Putnam-AXIOM: o1-preview scores 41.9% on originals and drops 19.6 points (46.8% relative) on functional variations. Fine-tuning gives 80% on originals vs 33% on variations. Source: https://arxiv.org/abs/2508.08292. **M-H**
29. Omni-MATH (4,428 problems; ICLR 2025) launch scores were o1-mini 60.54% and o1-preview 52.55%. Omni-MATH-2 edited 647 problems (14.6%) and tagged 247 (5.6%) as non-standard. Sources: https://arxiv.org/abs/2410.07985 ; https://github.com/MartheBallon/Benchmarks-saturate-when-the-model-gets-smarter-than-the-judge. **H**
30. First Proof (Feb 5, 2026; 11 mathematicians including Hairer and Spielman) posed 10 unpublished research lemmas with encrypted answers. OpenAI had about 5 apparently correct and DeepMind's Aletheia about 6. Some answers were plagiarism-like. Sources: https://arxiv.org/abs/2602.05192 ; https://www.scientificamerican.com/article/first-proof-is-ais-toughest-math-test-yet-the-results-are-mixed/. **H/M**
31. Riemann-Bench: 25 private problems, double-blind expert verification, all frontier models below 10% (Apr 2026). Source: https://arxiv.org/abs/2604.06802. **M-H**
32. Formal Conjectures: 2,615 Lean 4 statements, including 1,029 open conjectures and 836 solved problems. Source: https://arxiv.org/html/2605.13171v1. **M-H**
33. In Oct 2025 an OpenAI executive's claim that GPT-5 solved 10 open Erdős problems was retracted. The "solutions" were existing literature. Source: https://the-decoder.com/leading-openai-researcher-announced-a-gpt-5-math-breakthrough-that-never-happened/. **M-H**
34. IMO-Bench (EMNLP 2025, Google DeepMind): Gemini Deep Think scored 80.0% on AnswerBench and 65.7% on advanced ProofBench. v2 corrected ambiguous or incorrect items. Sources: https://aclanthology.org/2025.emnlp-main.1794/ ; https://github.com/google-deepmind/superhuman/tree/main/imobench/. **M/H**

---

## References

(Canonical URL; "seen at" where different. F = fetched, S = seen in search result summary.)

1. Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H., Kaiser, L., Plappert, M., Tworek, J., Hilton, J., Nakano, R., Hesse, C., Schulman, J. (2021) [corrected by fact-check]. Training Verifiers to Solve Math Word Problems. arXiv:2110.14168. https://arxiv.org/abs/2110.14168 (S)
2. Zhang, H., Da, J., Lee, D., Robinson, V., Wu, C., Song, W., Zhao, T., Raja, P., Slack, D., Lyu, Q., Hendryx, S., Kaplan, R., Lunati, M., Yue, S. (2024) [corrected by fact-check]. A Careful Examination of Large Language Model Performance on Grade School Arithmetic. NeurIPS 2024 Datasets & Benchmarks. arXiv:2405.00332. https://arxiv.org/abs/2405.00332 (S)
3. Scale AI (2024). gsm1k_eval repository. https://github.com/scaleapi/gsm1k_eval (F)
4. Mirzadeh, I., Alizadeh, K., Shahrokhi, H., Tuzel, O., Bengio, S., Farajtabar, M. (2025). GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning in Large Language Models. ICLR 2025. arXiv:2410.05229. (S)
5. Vendrow, J., Vendrow, E., Beery, S., Madry, A. (2025). Do Large Language Model Benchmarks Test Reliability? arXiv:2502.03461. (F BibTeX); GSM8K-Platinum blog https://gradientscience.org/gsm8k-platinum/ (S)
6. Hendrycks, D., Burns, C., Kadavath, S., Arora, A., Basart, S., Tang, E., Song, D., Steinhardt, J. (2021). Measuring Mathematical Problem Solving With the MATH Dataset. NeurIPS 2021. arXiv:2103.03874. (F BibTeX)
7. Lightman, H., Kosaraju, V., Burda, Y., Edwards, H., Baker, B., Lee, T., Leike, J., Schulman, J., Sutskever, I., Cobbe, K. (2023). Let's Verify Step by Step. arXiv:2305.20050; ICLR 2024 [corrected by fact-check]. (F BibTeX, github.com/openai/prm800k)
8. OpenAI (2024). Learning to reason with LLMs. https://openai.com/index/learning-to-reason-with-llms/ (S)
9. DeepSeek-AI (2025). DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning. arXiv:2501.12948. (S)
10. Balunović, M., Dekoninck, J., Petrov, I., Jovanović, N., Vechev, M. (2025). MathArena: Evaluating LLMs on Uncontaminated Math Competitions. NeurIPS 2025 Datasets and Benchmarks [corrected by fact-check]. arXiv:2505.23281. (S)
11. Dekoninck, J., Jovanović, N., Gehrunger, T., Rögnvaldsson, K., Petrov, I., Sun, C., Vechev, M. (2026). Beyond Benchmarks: MathArena as an Evaluation Platform for Mathematics with LLMs. ICML 2026. arXiv:2605.00674. (F BibTeX via github.com/eth-sri/matharena)
12. Petrov, I., Dekoninck, J., Baltadzhiev, L., Drencheva, M., Minchev, K., Balunović, M., Jovanović, N., Vechev, M. (2025). Proof or Bluff? Evaluating LLMs on 2025 USA Math Olympiad. arXiv:2503.21934; AI4Math@ICML 2025 workshop [corrected by fact-check]. (S)
13. MathArena (2025). Not Even Bronze: Evaluating LLMs on 2025 International Math Olympiad. https://matharena.ai/imo/ (S)
14. Dekoninck, J., Jovanović, N., Petrov, I., Vechev, M. (2025). MathArena Apex: Unconquered Final-Answer Problems. https://matharena.ai/apex/ [corrected by fact-check] (S)
15. Sun, C., Dekoninck, J., Vechev, M. (2026). Farewell to Final-Answer Competition Problems as Frontier Benchmarks. MathArena blog, May 12, 2026. https://matharena.ai/no_final_answer/ (S)
16. Papailiopoulos, D. (2025). AIME I 2025: A Cautionary Tale About Math Benchmarks and Data Contamination. X post. https://x.com/DimitrisPapail/status/1888325914603516214 (S)
17. Glazer, E., Erdil, E., Besiroglu, T., Chicharro, D., Chen, E., Gunning, A., Falkman Olsson, C., Denain, J.-S., Ho, A., de Oliveira Santos, E., et al. (2024). FrontierMath: A Benchmark for Evaluating Advanced Mathematical Reasoning in AI. arXiv:2411.04872 [corrected by fact-check]. (S)
18. Besiroglu, T. / Epoch AI (2025). Clarifying the creation and use of the FrontierMath benchmark. https://epoch.ai/latest/openai-and-frontiermath (S)
19. The Decoder (2025). OpenAI quietly funded independent math benchmark before setting record with o3. (S)
20. LessWrong (2025). Some lessons from the OpenAI-FrontierMath debacle. (S)
21. Dataconomy (2025). OpenAI's o3 claimed 25%, independent test says "try 10". (S)
22. Epoch AI (2025). FrontierMath Tier 4: Battle Royale. https://epochai.substack.com/p/frontiermath-tier-4-battle-royale (S)
23. Epoch AI (2025). Less than 70% of FrontierMath is within reach for today's models. (S)
24. Ho, A. / Epoch AI (2025). Is AI already superhuman on FrontierMath? (S)
25. Epoch AI (2026). GPT-5.4 set a new record on FrontierMath. (S)
26. Epoch AI (2026). FrontierMath Tier 4 (v2) benchmark page / v2 announcement. https://epoch.ai/benchmarks/frontiermath-tier-4-v2 ; https://x.com/EpochAIResearch/status/2065488154086568445 (S)
27. Epoch AI (2026). "Every FrontierMath Tier 4 problem has now been solved" (X). https://x.com/EpochAIResearch/status/2098103831502708864 (S)
28. Epoch AI (2026). FrontierMath: Open Problems. https://epoch.ai/frontiermath/open-problems (S)
29. Luong, T., et al. (2025). Towards Robust Mathematical Reasoning (IMO-Bench). EMNLP 2025. arXiv:2511.01846. (F BibTeX)
30. Google DeepMind (2025). Advanced version of Gemini with Deep Think officially achieves gold-medal standard at the IMO. (S)
31. Scientific American (2025). Mathematicians Question AI Performance at International Math Olympiad. (S)
32. AFP / France24 (2026). AI catches up with humans to score 100% at top maths contest. (S)
33. Axiom Math (2026). IMO2026 repository. https://github.com/AxiomMath/IMO2026 (F)
34. Axiom Math (2025). Putnam2025 repository. https://github.com/AxiomMath/putnam2025 (F)
35. Tsoukalas, G., Lee, J., Jennings, J., Xin, J., Ding, M., Jennings, M., Thakur, A., Chaudhuri, S. (2024). PutnamBench. NeurIPS 2024 D&B. arXiv:2407.11214. (F BibTeX)
36. Gulati, A., Miranda, B., Chen, E., Xia, E., Fronsdal, K., Dumont, B., Obbad, E., Koyejo, S. (2025). Putnam-AXIOM: A Functional and Static Benchmark. ICML 2025 (venue not re-verified). arXiv:2508.08292 [corrected by fact-check]. (S)
37. Gao, B., Song, F., Yang, Z., Cai, Z., Miao, Y., Dong, Q., Li, L., Ma, C., Chen, L., Xu, R., Tang, Z., Wang, B., et al. (2025). Omni-MATH. ICLR 2025. arXiv:2410.07985. (S)
38. Ballon, M., Algaba, A., Verbeken, B., Ginis, V. (2026). Benchmarks Saturate When The Model Gets Smarter Than The Judge. arXiv:2601.19532. (F README/BibTeX)
39. Abouzaid, M., Blumberg, A. J., Hairer, M., Kileel, J., Kolda, T. G., Nelson, P. D., Spielman, D., Srivastava, N., Ward, R., Weinberger, S., Williams, L. (2026). First Proof. arXiv:2602.05192. (S)
40. Scientific American (2026). First Proof is AI's toughest math test yet. The results are mixed; and AI scores a 'C–' on its hardest math test yet. (S)
41. Garre, S., Knutsen, E., Mehta, S., Chen, E. (2026). Riemann-Bench: A Benchmark for Moonshot Mathematics. arXiv:2604.06802 [corrected by fact-check]. (S)
42. Firsching, M., Lezeau, P., Mercuri, S., Horváth, M. Z., Dillies, Y., Sönne, C., Wieser, E., Zhang, F., Hubert, T., Agüera y Arcas, B., Kohli, P. (2026) [corrected by fact-check]. Formal Conjectures: An Open and Evolving Benchmark for Verified Discovery in Mathematics. arXiv:2605.13171. https://github.com/google-deepmind/formal-conjectures (F)
43. The Decoder (2025). Leading OpenAI researcher announced a GPT-5 math breakthrough that never happened. (S)
44. Tao, T., et al. AI contributions to Erdős problems (GitHub wiki). https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems (F)
45. Stanford HAI (2026). AI Index Report 2026, Chapter 2: Technical Performance. (S)

---

## Verification log

Adversarial fact-check pass (2026-09-29). **Method and limits:** The session's WebSearch budget was already exhausted when this pass started (every query returned "web search budget used"). Direct fetches of arxiv.org, epoch.ai, matharena.ai, scale.com, gradientscience.org, papers.nips.cc, france24.com, the-decoder.com and trishullab.github.io were egress-blocked. All evidence below therefore comes from GitHub: official repos (fetched), raw files in those repos, and GitHub code search over third-party mirrors (arXiv-digest repos, paper-note repos, page snapshots). Mirrors of an abstract or page are labelled "mirror". Third-party commentary is labelled "secondary". Nothing below relies on the original dossier's own search summaries.

### Claim verdicts

| ID | Verdict | Evidence (independent of the dossier's sources) | Sources |
|---|---|---|---|
| C1 GSM1k | **corrected** | "Up to 13%", Phi/Mistral named, and r² = 0.32 are all from the **arXiv v1 abstract (May 1, 2024)**. The NeurIPS 2024 abstract says "up to 8%", r² = 0.36, and "several families of models" (no names). The dossier wrongly called 13% a "NeurIPS-version summary". Confirmed: 50 of 1,000 items released, with release when 3 open models of different lineages reach 95%; frontier models show minimal overfitting; full author list. | mirror v1: github.com/lyy1994/awesome-data-contamination README; github.com/HuggingAGI/HuggingArxiv (2024-05-01); github.com/jeff-da/jeff-da.github.io gsm1k.html (co-author page). Mirror NeurIPS: github.com/fzyzcjy/ai_math_paper_list render/neurips_2024.md. Fetched: github.com/scaleapi/gsm1k_eval |
| C2 GSM8K-Platinum | **confirmed (M, indirect)** | The released GSM8K-Platinum has 1,209 questions = 1,319 GSM8K test − 110 removed, which matches the 110-removed figure. 219 = 110 + 99 + 10 is internally consistent. The gradientscience post itself could not be re-read. Paper authors and ID are confirmed from the BibTeX. | github.com/MadryLab/platinum-benchmarks (fetched BibTeX); sglang benchmark/gsm8k/README.md (`--num-questions 1209 --platinum`), e.g. github.com/rednote-machine-learning/RedKnot |
| C3 MATH launch / o1 / R1 | **corrected (minor)** | Confirmed: MATH 3.0–6.9% at launch (HF evaluate metric card: "accuracies ranging from 3.0% to 6.9%"), NeurIPS BibTeX, and the Omni-MATH abstract "OpenAI o1 achieves 94.8% on MATH dataset". Correction: OpenAI's simple-evals README says models "on or after o1" are evaluated on **MATH-500**, so o1's 94.8% is very likely a MATH-500 figure, and simple-evals later lists released o1 at 96.4. DeepSeek-R1's MATH-500 97.3 and AIME 2024 79.8 are confirmed in the official README. | github.com/microsoft/wina lm_eval/metrics/competition_math/README.md; github.com/hendrycks/math; raw.githubusercontent.com/openai/simple-evals/main/README.md (footnote 6); github.com/HuggingAGI/HuggingArxiv (Omni-MATH abstract); raw.githubusercontent.com/deepseek-ai/DeepSeek-R1/main/README.md |
| C4 AIME 2024 contamination | **confirmed (M)** | The primary abstract says "we find strong signs of contamination in AIME 2024". Three independent secondary readers of §4.1 report most models 10–20 points above the human-percentile expectation and QwQ-Preview-32B about 60 points above. Venue is NeurIPS 2025 D&B. | github.com/eth-sri/eth-sri.github.io _publications/balunovic2025matharena.md; github.com/suncityldp/zx-bench docs/LLM数学推理评测综述-2026.md; github.com/AlexSabaka/mathbot MATHBOT_PROBLEMS_PROPOSAL_v2.md; github.com/g-leech/argmin-gravitas 2025-11-09 post |
| C5 USAMO 2025 → 2026 | **confirmed (with caveats)** | The Proof-or-Bluff v1 abstract says "achieving less than 5% on average". The later version gives Gemini-2.5-Pro about 25% (10.1/42), and the MathArena v1 abstract says "even top models score below 25%". The Beyond Benchmarks abstract says "GPT-5.5, now reaches 98% on the 2026 USA Math Olympiad and 74% on research-level questions". The 98.21% model-page value was not re-read, and a Sep 2026 third-party read of the live board showed a top of 95.2%. | github.com/eth-sri/eth-sri.github.io _publications/petrov2025usamo.md; github.com/Proteusiq/unthinking; github.com/lhnows/alignai docs/Arxiv/2026-05-04.md and github.com/wwd29/arxiv-daily (abstract mirrors); github.com/turbobeest/modelspec benchmarks/usamo_2026.md |
| C6 Apex / "Farewell" | **unverifiable (partially corroborated)** | Corroborated: launch Aug 2025; best model about 5% ("By design, the best model scores only 5.2%", secondary capture); 12 problems (Shortlist 47); MathArena later marked Apex, Shortlist and the final-answer competitions **Deprecated** (Sep 2026 table scrape). **Not found:** the May 2026 "Farewell" post, GPT-5.5 solving the last Apex problem, and the 162/176 Gemini 3.1 Pro figure. | github.com/RishiJain905/LocalModelResearch; github.com/alopatenko/LLMEvaluation; github.com/fstandhartinger/model-market-comparison data/SCRAPING.md and CHANGELOG.md; DeepSeek-V4.1 report reference list (github.com/bojieli/ai-infra-book) |
| C7 FrontierMath launch | **confirmed (H)** | Abstract: "Current state-of-the-art AI models solve under 2% of problems"; "new, unpublished problems and automated verification". The paper body says "over 60 mathematicians". First author is Elliot Glazer. | mirrors: github.com/ATOM00blue/machine-learning-library corpus/papers/2411.04872.md; github.com/tiendungchs/PersonalWiki (arXiv v7 clipping) |
| C8 OpenAI funding / access | **corrected (timing)** | Confirmed from Epoch's "Clarifying the creation and use of the FrontierMath benchmark" (2025-01-23), as quoted by several repos: OpenAI commissioned the 300 problems, owns them, and has access except for a holdout; Epoch cannot share them without OpenAI's written permission; many writers were not told; communication "should have been more ... transparent". Correction: the contract barred disclosure "until around the time o3 launched", so the partnership was disclosed **around** (not strictly after) the Dec 20, 2024 announcement. The ownership and access terms came only in Jan 2025. The Epoch benchmark page (Sep 2026) states: "FrontierMath was developed with funding from OpenAI, who has exclusive access to a subset of the benchmark." | github.com/akira82-ai/100-questions-of-ai-agent; github.com/yoheinakajima/evaluator-bench (bench/seed_v0.py, outreach/epoch.md); github.com/yashdave003/evaluation-ecosystem-explorer; Epoch page snapshot github.com/Develata/AI-Barking docs/0924/sources/usage/epoch-tier4.txt |
| C9 o3 25.2% vs ~10% | **confirmed (M)** | The Dataconomy article exists (Apr 21, 2025; title "OpenAI's o3 claimed 25%, independent test says 'try 10'"). Two independent wikis record "Epoch's April 2025 independent run of released o3 scored ~10%" against the 25.2% Dec 2024 claim. | github.com/Neurabuzz/neurabuzz archive 2025-04-22; github.com/quantified-uncertainty/longterm-wiki reasoning.mdx; github.com/yashdave003/evaluation-ecosystem-explorer |
| C10 FrontierMath v2 | **confirmed (H for counts; M for "+12 pp")** | Epoch page, captured Sep 24, 2026: "On 2026-06-12 ... addressing errors in 42% of problems ... 338 problems ... 295 ... 43". Changelog: "corrected 123 problems in Tiers 1-3 and 12 problems in Tier 4 ... removed 5 ... and 7". The "~12 pp higher" figure appears only in secondary sources. GPT-5.5 (xhigh) is 72.5% on Tier 4 v2. | github.com/Develata/AI-Barking docs/0924/sources/usage/epoch-tier4.txt; github.com/treehouse-ladder/wikipilot; github.com/benchflow-ai/awesome-evals notes/articles/benchmark-label-errors.md; github.com/prajwalgajakesari/the-vault-ai (2026-06-17) |
| C11 Tier 4 saturation | **confirmed (M-H)** | Epoch page: GPT-6 Astra 97.6% ± 2.4% on the private set (41 problems, so 40/41), 64 models tested. A secondary report quotes Epoch (Sep 10, 2026): "Every FrontierMath Tier 4 problem has now been solved by AI, with GPT-6 Astra solving the last problem standing", with launch on July 11, 2025 at 5%. OpenAI has access to 28 of 48 private Tier 4 problems and Epoch holds out 20 (careful secondary). Import AI #420 confirms Tier 4 = 50 problems (Jul 2025). "Epoch considers it saturated" is secondary wording. | github.com/Develata/AI-Barking epoch-tier4.txt; github.com/prajwalgajakesari/the-vault-ai editions/2026/09/11; github.com/htihle/open_closed_gap open_chinese_vs_closed/CATEGORIES.md; github.com/bedwards/hex-index (Import AI 420) |
| C12 IMO 2025 | **confirmed (M-H)** | "Not Even Bronze: Evaluating LLMs on 2025 International Math Olympiad" was posted at matharena.ai/imo/ on 2025-07-19, and a capture quotes "Gemini 2.5 Pro: 31% — well below bronze medal threshold (19/42)". DeepMind's result was officially certified at 35/42. OpenAI's 35/42 was graded by former medalists. The IMO statement's primary wording (imo2025.au, 2025-07-19) differs slightly from the dossier's SciAm-sourced quote (fixed inline). The embargo claim is contested. | github.com/kherrick/hacker-news archives/2025-07-19; github.com/RishiJain905/LocalModelResearch; github.com/walkinglabs/self-improving-agent-notebook; github.com/oratis/Markup; DeepMind blog URL linked from github.com/google-deepmind/superhuman README |
| C13 IMO 2026 | **corrected** | Confirmed: Huawei Celia and Xiaohongshu dots-note-3.0 at 42/42 described as officially graded; 7 of 666 humans at 42/42; gold cutoff 29; AxiomProver 42/42 with Lean (521/1224/4229/520/457/771 lines; 24+360+869+39+65+139 = 1,496 min). **Correction:** the OpenAI/Anthropic/Moonshot 42/42 figures were **not lab self-reports**. They came from Deedy Das's third-party harness with Claude-based graders, labelled "strong but not authoritative". Axiom's result is self-published and not officially verified. The official gradings rest on company announcements and press, and one source says the IMO's own site has no statement. | github.com/adamghaida/ai-hall-of-fame mathematics/imo-2026-perfect-score (CONTEXT.md, PROMPT.md); github.com/HarperZ9/flywheel project-docs/records/2026-07-25; github.com/tobiasosborne/ai-agents-seminar; raw.githubusercontent.com/AxiomMath/IMO2026/main/README.md (fetched) |
| C14 PutnamBench / Putnam 2025 | **corrected** | Confirmed: "a total of 6 problems in PutnamBench are successfully proven" (paper §4.2, arXiv v2 text). Axiom solved 12/12 Putnam 2025, 8 within the window (A5, A6, B4, B6 after), in Lean 4.21.0 with SafeVerify. **Correction:** 1,724 formalizations (672/640/412) is the **current** repo size. The NeurIPS/v2 paper had 1,692 formalizations of 640 theorems. **Update:** the official leaderboard data shows Aleph Prover at 668/672 (Jan 11, 2026) and **672/672 (Aug 26, 2026)**, so Lean is fully saturated. | raw.githubusercontent.com/trishullab/PutnamBench/main/README.md and main/docs/results.json; paper text mirror raw.githubusercontent.com/epfl-lara/LeanFlow/.../paper/sources/tsoukalas2024_putnambench.txt; github.com/leejasper851/leejasper851.github.io; raw.githubusercontent.com/AxiomMath/putnam2025/main/README.md |

**Tally:** 8 confirmed (C2, C4, C5, C7, C9, C10, C11, C12), 5 corrected (C1, C3, C8, C13, C14), 0 refuted, 1 unverifiable (C6).

### Other corrections made inline
- The GSM8K and GSM1k author lists are complete. GSM8K's 1,319-item test is now indirectly corroborated.
- MathArena paper venue: NeurIPS 2025 D&B. Proof or Bluff: full authors, AI4Math@ICML 2025.
- FrontierMath author list added. Erdős launch date given as Sep 1, 2026 (secondary). First Proof batch 2 report arXiv:2606.18119 (secondary).
- Riemann-Bench authors: Garre, Knutsen, Mehta, Chen (Surge AI). Formal Conjectures authors added.
- The Apex canonical title is "MathArena Apex: Unconquered Final-Answer Problems". The Apex and final-answer boards are Deprecated.
- The AIME 2025 "8 of 30 near-duplicates" figure is attributed to the MathArena paper itself (secondary).

### Reference check summary (refs/math.json)
- **Checked:** all 50 entries (0 skipped).
- **verified = true:** 37. Existence and metadata were confirmed through an official repo, a BibTeX, an arXiv-listing mirror, or a URL recorded by an independent repo.
- **verified = false:** 13. These could not be independently located this pass: madrylab GSM8K-Platinum blog, the MathArena "Farewell" post, the Papailiopoulos X post, Epoch "Tier 4 Battle Royale", "Less than 70% ...", the Digital Applied article, the Epoch X status 2098103831502708864, the three Scientific American articles (2025 IMO; 2026 First Proof "results are mixed"; 2026 "C-"), the LessWrong "OpenAI Claims IMO Gold Medal" post, the AFP/France24 article, and the AI Index 2026 chapter. Their content is often corroborated elsewhere (see verify_note), but the specific URL/title was not seen.
- **Metadata fixed:**
  - Seed-Prover 1.5 title was truncated. The full title is "...via Learning from Experience".
  - GSM8K author list was reordered and completed ("et al." had hidden 5 middle authors).
  - Filled previously "[not verified]" author lists: GSM1k, Proof or Bluff, FrontierMath, Putnam-AXIOM, Riemann-Bench, Formal Conjectures.
  - Venues: MathArena → NeurIPS 2025 D&B; Let's Verify → ICLR 2024; Proof or Bluff → AI4Math@ICML 2025.
  - Apex title/authors.
- **No fabricated references found.** Every arXiv ID checked (2110.14168, 2405.00332, 2410.05229, 2502.03461, 2103.03874, 2305.20050, 2501.12948, 2505.23281, 2605.00674, 2503.21934, 2411.04872, 2511.01846, 2407.11214, 2512.17260, 2508.08292, 2410.07985, 2601.19532, 2602.05192, 2604.06802, 2605.13171) matches the stated title.

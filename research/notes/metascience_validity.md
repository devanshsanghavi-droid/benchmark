# Measurement validity, psychometrics, and the structure of LLM capabilities

*Research dossier for the benchmark-design project. Compiled 2026-09-29.*

**How this dossier was sourced.** The session's WebSearch budget was already used up (200 of 200 calls) when this subagent started. arXiv, OpenReview, ACL Anthology, NeurIPS proceedings and github.io were blocked for direct fetch. Evidence therefore comes from GitHub, which was reachable:

- **Official repositories:** BetterBench paper text, ObsScaling, tinyBenchmarks, metabench, Safetywashing, ECI, Fluid Benchmarking and Signal-and-Noise.
- **Full-text mirrors of papers:** Ruan et al., Burnell et al., Train-before-Test, Sloth, Owen, ADeLe/General Scales, and the Desai et al. 2026 COLM PDF.
- **arXiv-digest mirrors that reproduce abstracts verbatim.**
- **Bibliography files** used to confirm bibliographic details of classical psychometrics papers.

Every claim below states its source. **[H]/[M]/[L]** give high, medium or low confidence. "Primary" means I read the paper text or the authors' official repository or website. "Secondary" means a third-party summary, and it is flagged.

---

## Summary

1. **Construct validity is the weakest link in LLM benchmarking, and this has been measured, not merely argued.**
   - Bean et al. (NeurIPS 2025 D&B) had 29 expert reviewers review 445 LLM benchmark papers. They found recurring problems in phenomenon definition, task design and scoring that "undermine the validity of the resulting claims", and they issue eight recommendations.
   - BetterBench (Reuel et al., NeurIPS 2024 D&B) scored 24 benchmarks against 46 best practices. 14 of 24 reported no uncertainty or statistical significance, and 17 of 24 shipped no easy-to-run replication scripts.
   - These audits sit on a 2020–2022 critique literature: Ethayarajh & Jurafsky 2020; Raji et al. 2021; Bowman & Dahl 2021; Liao et al. 2021; Hutchinson et al. 2022.

2. **Classical psychometrics already supplies the needed vocabulary.** It has been ported into LLM evaluation mainly since 2023.
   - Cronbach & Meehl (1955): construct validity and the nomological network.
   - Campbell & Fiske (1959): convergent and discriminant validity, and method variance through the multitrait-multimethod (MTMM) matrix.
   - Sechrest (1963) and Hunsley & Meyer (2003): incremental validity.
   - Messick (1989, 1995), Kane (2013) and the AERA/APA/NCME *Standards* (2014): the unified, argument-based view of validity.
   - Desai et al. (COLM 2026) is a large-scale application of convergent and discriminant validity to LLM benchmarks (56 benchmarks, 53 models). [corrected by fact-check: the earlier wording "the first" is not claimed by the paper and is unverified; Safetywashing (2024) had already run a discriminant-style "capabilities correlation" analysis]

3. **LLM capabilities are strongly low-dimensional.** Across studies there is a positive manifold and a dominant first factor:
   - Burnell et al. 2023: 3 factors explain 82% of variance.
   - Ilić 2023: 1 factor explains 85%, as cited by Ruan et al.
   - Ruan et al. 2024: PC1 explains about 80% and the top-3 PCs about 97%.
   - Zhang et al. 2025: PC1 explains 70% under direct evaluation and 86–93% after train-before-test.

   Desai et al. find that benchmarks labelled "reasoning" and "knowledge" are **not discriminable** from each other. Several "safety" benchmarks correlate more with capability benchmarks than with each other. Shared **score format** predicts benchmark similarity more strongly than shared concept. Safetywashing (Ren et al., NeurIPS 2024 Datasets and Benchmarks Track [corrected by fact-check: track added]) makes the same point for safety: many safety benchmarks track upstream capability and training compute.

4. **The dominant factor is not the whole story, and its interpretation is contested.**
   - Several analyses keep 3 or more factors (Burnell; Sloth; PC-2 "reasoning" and PC-3 "programming" in Ruan).
   - Kearns (2026) argues that plain latent-factor models extract a factor that largely proxies model scale.
   - Zhou et al. (ADeLe; arXiv 2025, published in *Nature* 2026 [corrected by fact-check: journal publication added]) argue that population-based factor solutions shift as the model population changes. They propose non-populational, rubric-based demand scales instead.

5. **Item response theory (IRT) is now standard infrastructure.**
   - tinyBenchmarks (ICML 2024): 100 items estimate MMLU within about 2 points.
   - metabench (ICLR 2025): under 3% of Open LLM Leaderboard items, reconstruction error under 1%.
   - Fluid Benchmarking (COLM 2025): IRT raises validity and adaptive item selection lowers variance.
   - Growing Pains (2026): fixed-parameter calibration for linking new datasets.
   - Epoch Capabilities Index: a one-dimensional IRT "Rosetta Stone" that stitches benchmarks onto one scale.

**Bottom line for the key question.** In a typical model-by-benchmark matrix, 70–85% of variance is one general factor. So a new benchmark's headline correlation with other benchmarks says almost nothing about whether it adds information. The question is how much **reliable variance remains after partialling out general capability** (and scale), and whether that residual predicts something external.

A new benchmark should therefore ship a **validity argument** with five parts:
- (i) reliability with uncertainty;
- (ii) convergent evidence, meaning agreement with alternative operationalizations of the same construct, ideally with a different format;
- (iii) discriminant evidence against a general-capability index and against same-format benchmarks;
- (iv) incremental validity: ΔR² over the general factor for predicting an external criterion, on held-out and newer models;
- (v) stability of these results across model populations and over time.

---

## Detailed findings

### 1. Classical validity theory (the foundations a paper should cite)

| Concept | Canonical source (bibliographic details verified in this session) | What it contributes to benchmark design |
|---|---|---|
| Construct validity; nomological network | Cronbach & Meehl (1955), *Psychological Bulletin* 52(4):281–302, doi:10.1037/h0040957 [H: bib seen in elliottower/scib-construct-validity; also cited by BetterBench] | A benchmark score is meaningful only within a network of predicted relations with other variables. Validity is established by testing those predictions. |
| Convergent and discriminant validity; method variance | Campbell & Fiske (1959), "Convergent and discriminant validation by the multitrait-multimethod matrix", *Psychological Bulletin* 56(2):81–105, doi:10.1037/h0046016 [H] | Different methods measuring the same trait should agree. The same method measuring different traits should agree *less*. For LLMs, "method" includes task format, score format and judge type (Desai et al. 2026 find method effects dominate). |
| Incremental validity | Sechrest (1963), "Incremental validity: A recommendation", *Educational and Psychological Measurement* 23(1):153–158, doi:10.1177/001316446302300113 [H: citation seen]. Hunsley & Meyer (2003), "The incremental validity of psychological testing and assessment: Conceptual, methodological, and statistical issues", *Psychological Assessment* 15(4):446–455, doi:10.1037/1040-3590.15.4.446 [H: citation seen] | A new test earns its place only if it improves prediction beyond what cheaper, existing measures provide. The standard method is hierarchical regression (ΔR²). *Summary of content is from background knowledge, not re-read this session.* |
| Unified validity; consequential aspect | Messick (1989), "Validity", in *Educational Measurement* (3rd ed.), pp. 13–103; Messick (1989), "Meaning and values in test validation", *Educational Researcher* 18(2):5–11; Messick (1995), "Validity of psychological assessment…", *American Psychologist* 50(9):741–749, doi:10.1037/0003-066X.50.9.741 [H: citations seen] | Validity belongs to the *interpretations and uses* of scores, not to the test itself. It includes the social consequences of score use (relevant to Goodhart effects and leaderboard gaming). A bibliography annotation summarises Messick 1995 as "content, construct, consequential validity" [seen in harvard-edge/cs249r_book bib]. The usual six-aspect breakdown is background knowledge and is **not verified here**. |
| Argument-based validation | Kane (2013), "Validating the interpretations and uses of test scores", *Journal of Educational Measurement* 50(1):1–73, doi:10.1111/jedm.12000 [H: citation seen] | Write an explicit interpretation/use argument (scoring → generalization → extrapolation → decision) and test its weakest inference. |
| Professional standard | AERA, APA & NCME (2014), *Standards for Educational and Psychological Testing* [H: citation seen] | The accepted reference for what validity, reliability and fairness evidence a test must document. |
| Measurement validity outside psychology | Adcock & Collier (2001), "Measurement validity: A shared standard for qualitative and quantitative research", *American Political Science Review* 95(3):529–546 [H: seen in the Desai et al. bibliography] | Separates the background concept, the systematized concept, indicators and scores. This maps onto "phenomenon → task → metric → claim" (Bean et al.). |
| Measurement modelling in ML | Jacobs & Wallach (2021), "Measurement and Fairness", FAccT '21, pp. 375–385, doi:10.1145/3442188.3445901 [H: citation seen] | Imports construct validity and reliability into ML fairness. Precursor to Wallach et al. 2025. |

### 2. The 2020–2022 critique literature (why benchmarks fail as measurements)

- **Ethayarajh & Jurafsky (2020), "Utility is in the Eye of the User: A Critique of NLP Leaderboards", EMNLP 2020, doi:10.18653/v1/2020.emnlp-main.393, arXiv:2009.13888.**
  - Argument, via microeconomic theory: leaderboards are poor proxies for practitioners' utility because they ignore costs that users bear (model size, energy, latency).
  - Recommendation: report statistics of practical concern.
  - Source: abstract notes at makrai/notes; DOI at the acl-org/ethics-reading-list. [H]
  - *Implication:* a benchmark's "construct" should include the user's cost function where relevant.
- **Raji, Bender, Paullada, Denton & Hanna (2021), "AI and the Everything in the Whole Wide World Benchmark", NeurIPS 2021 Datasets & Benchmarks Track, arXiv:2111.15366.** An earlier version appeared as a NeurIPS 2020 ML-Retrospectives workshop post. [corrected by fact-check: the author order above is the arXiv order. The NeurIPS D&B proceedings version is cited as Raji, Denton, Bender, Hanna & Paullada (BetterBench ref [67]; Desai et al. bibliography). Use that order when citing the NeurIPS version.]
  - Critiques treating narrow benchmarks as measures of "general" capability.
  - BetterBench adopts its definition of a benchmark: "a particular combination of a dataset or sets of datasets [...], and a metric, conceptualized as representing one or more specific tasks or sets of abilities, picked up by a community of researchers as a shared framework for the comparison of methods" (quoted in BetterBench §1). [H]
  - Desai et al. cite it for the point that the concepts benchmarks claim to measure are "often underspecified". [H]
- **Bowman & Dahl (2021), "What Will it Take to Fix Benchmarking in Natural Language Understanding?", NAACL 2021, arXiv:2104.02145.**
  - Evaluation for many NLU tasks "is broken". Unreliable and biased systems score highly on IID benchmarks.
  - Adversarial out-of-distribution test sets "only obscure the abilities that we want to measure".
  - Proposes four criteria that most benchmarks fail. The fix requires progress in "the design of benchmark datasets, the reliability with which they are annotated, their size, and the ways they handle social bias" (abstract via makrai/notes). [H]
  - The four criteria are usually summarised as validity, reliable annotation, statistical power and disincentivising biased models. *That summary is from background knowledge.* [M]
- **Liao, Taori, Raji & Schmidt (2021), "Are We Learning Yet? A Meta Review of Evaluation Failures Across Machine Learning", NeurIPS 2021 D&B (Round 2).**
  - A taxonomy of evaluation failures across ML subfields, covering both **internal and external validity** issues. The description is from the *fairmlbook* (Barocas, Hardt & Narayanan) bibliographic notes. [H for existence; M for content, secondary]
- **Hutchinson, Rostamzadeh, Greer, Heller & Prabhakaran (2022), "Evaluation Gaps in Machine Learning Practice", FAccT 2022, doi:10.1145/3531146.3533233, arXiv:2205.05256.**
  - Verbatim abstract (DBLP/OpenAlex record): evaluations "frequently focus on only a narrow range of decontextualized predictive behaviours".
  - An empirical study of CV and NLP papers shows "a general focus on a handful of evaluation methods".
  - The discipline implicitly commits to "consequentialism, abstractability from context, the quantifiability of impacts, the limited role of model inputs in evaluation, and the equivalence of different failure modes". [H]
- Related items seen only as bibliography entries, cited by Desai et al.: Blodgett et al. (2021), "Stereotyping Norwegian Salmon…", ACL-IJCNLP 2021, pp. 1004–1015; Subramonian et al. (2023), "It takes two to tango…", Findings of ACL 2023, pp. 3234–3279. [H for existence]

### 3. LLM-era validity audits (2024–2026)

#### 3.1 BetterBench (Reuel, Hardy, Smith, Lamparth, Hardy & Kochenderfer; NeurIPS 2024 D&B; arXiv:2411.12990)

Primary source: the full paper text mirrored at Lumysia/agi-benchmark-framework.

- Assessment framework of **46 best practices** across a **five-stage lifecycle**: design, implementation, documentation, maintenance, retirement. **24 AI benchmarks** were evaluated. [H] [fact-check note: retirement is part of the lifecycle model but is excluded from scoring, so scores cover four stages (BetterBench appendix). The 24 are 16 foundation-model and 8 non-foundation-model benchmarks.]
- "14 out of 24 benchmarks did not perform multiple evaluations of the same model or report statistical significance or uncertainty of results." [H]
- "17 out of 24 benchmarks do not provide easy-to-run scripts to replicate the results… and 4 out of 24 only provide scripts to replicate part of the results." Implementation-stage scores were the lowest. [H]
- MMLU scored lowest (weighted average **5.5**) and GPQA scored "significantly higher" (**11.0**). Model cards for GPT-4, Claude-3 and Gemini report both without acknowledging the quality gap. [H]
- A GitHub build-status badge was used by only 3 of 24 benchmarks. [H]
- Construct validity is listed as an **open challenge** that BetterBench explicitly does *not* score. It "would presumably require in-depth analysis by domain experts". [H]
- *Implication:* BetterBench is a necessary-but-not-sufficient hygiene checklist. It does not establish validity.

#### 3.2 Measuring What Matters (Bean et al.; NeurIPS 2025 D&B; arXiv:2511.04703; OpenReview mdA5lVvNcU)

- **Primary (abstract):**
  - "With a team of 29 expert reviewers, we conduct a systematic review of 445 LLM benchmarks from leading conferences in natural language processing and machine learning."
  - The reviewers find "patterns related to the measured phenomena, tasks, and scoring metrics which undermine the validity of the resulting claims".
  - They give "eight key recommendations". [H]
  - Venue confirmed by the Desai et al. bibliography: "Thirty-ninth Annual Conference on Neural Information Processing Systems Datasets and Benchmarks Track, 2025". [H]
- **Secondary (AI-generated paper note, zhaoyang97/Paper-Notes-en; not checked against the PDF):**
  - Corpus: 46,114 papers were filtered to 2,189 candidates and then 445.
  - Codebook of 21 items covering face, content, predictive, ecological, convergent and discriminant validity. Double-review Brennan–Prediger κ = 0.524.
  - Recommendations: (1) define the phenomenon; (2) measure only the phenomenon, controlling format and instruction confounds; (3) representative sampling rather than convenience sampling; (4) caution when reusing datasets; (5) guard against contamination; (6) use statistical tests to compare models; (7) do error analysis; (8) justify construct validity.
  - Reported prevalences: definition contested in 47.8% of papers; convenience sampling in 27%; exact-match scoring in 81.3%; statistical tests in **16%**; construct validity discussed in 53.4%; LLM-generated items in 31.2%.
  - **Confidence [M/L]:** re-verify every percentage against the paper before citing. The note is internally inconsistent in one place (43.3% vs 40.7% for manually constructed tasks).
  - [fact-check note] The **16%** statistical-testing figure is independently repeated by two further secondary sources: an LLM-written digest quoting §4 as "16.0% of reviewed benchmarks conducted any statistical testing" (memgrafter/research-digests), and a Hacker News digest ("Only 16% of studies used statistical methods when comparing models"; Planeshifter/hackernews-ai-digest). Upgrade 16% to [M]. It is still not checked against the PDF. The other percentages stay [M/L].

#### 3.3 What AI Benchmarks Actually Measure (Desai, Truong, Wallach, Chouldechova, Cooper, Garcia-Gathright, Ho, Jacobs, Koyejo, Pangakis & Wang; COLM 2026 [listed as Oral on A. F. Cooper's site]; arXiv:2609.08812)

Primary source: the PDF from afedercooper.github.io, obtained via raw.githubusercontent.com. This is the most directly relevant paper for the "incremental and discriminant validity" question.

- **Method.** Adapts convergent and discriminant validity (Campbell & Fiske 1959; Adcock & Collier 2001; Messick 1989) to **56 capability and safety benchmarks** and **53 models**.
  - Benchmarks with similar purported concepts get a shared "assigned concept".
  - Spearman correlations of model rankings are compared within and between concepts.
  - Item-level IRT models compare one shared latent trait against concept-specific traits (ΔAUC).
  - Eight benchmarks were excluded (four saturated, four format-sensitive), leaving 48. [H]
- **Capability concepts are not discriminable.** "Correlations between model rankings on benchmarks with different assigned capability concepts (e.g., reasoning versus knowledge) are often as high as correlations between model scores on benchmarks with the same assigned concept … with the exception of summarization." At item level, knowledge and reasoning are "predicted as well by a single shared latent trait". ΔAUC between reasoning and knowledge = 0.011 [0.010, 0.011]. [H]
- **Safety concepts converge weakly.** Refusal, safety-detection and bias benchmarks show "wide interquartile ranges and correlations that frequently approach or fall below zero". Ethics, bias, privacy and unsafe-behaviour benchmarks correlate more with capability benchmarks than with each other, consistent with Ren et al. 2024. [H]
- **Method variance dominates.**
  - Benchmarks "primarily cluster by score format rather than assigned concept".
  - In regression on pairwise correlation, format outweighs concept (β_format = 0.275, p < 0.0001; β_concept = 0.138, p = 0.003).
  - With LLM-judge vs. other formats coded as binary, the concept effect vanishes (β_concept = −0.058, p = 0.998; β_format = 0.526). [H]
  - [fact-check note] β_format = 0.275 / β_concept = 0.138 come from the model with format coded at three levels (multiple-choice, exact-match free response, LLM-judge free response). The abstract frames the format effect cautiously ("In some cases, benchmarks that share benchmark design elements … correlate more strongly … than benchmarks with the same assigned concept"). The heading "method variance dominates" is our paraphrase and is stronger than the authors' framing.
- **Mislabelled benchmarks.**
  - BBQ-accuracy (labelled *bias*) correlates more with *reasoning* benchmarks (relabeling statistic 0.15, 95% CI [0.07, 0.23]).
  - DecodingTrust-Fair correlates more with *knowledge* (0.14 [0.05, 0.24]).
  - OR-Bench (over-refusal) does behave distinctly: refusal and over-refusal are strongly inversely correlated, ΔAUC between them = 0.062. [H]
- **Caution in the paper itself.** Low correlation among safety benchmarks is *not* treated as evidence of poor construction, because safety concepts "may be inherently multi-dimensional". The approach assesses convergence but does not explain causes. [H]

#### 3.4 Safetywashing (Ren, Basart, Khoja, Gatti, Phan, Yin, Mazeika, Pan, Mukobi, Kim, Fitz & Hendrycks; NeurIPS 2024 Datasets and Benchmarks Track [corrected by fact-check: track added, per the proceedings PDF filename "…-Paper-Datasets_and_Benchmarks_Track.pdf"], *Advances in NeurIPS* 37:68559–68594; arXiv:2407.21792)

- **Abstract (primary via arXiv mirror):** "many safety benchmarks highly correlate with both upstream model capabilities and training compute, potentially enabling 'safetywashing'—where capability improvements are misrepresented as safety advancements". The authors call for safety goals "empirically separable from generic capabilities advancements". [H]
- **Method (official project website source):**
  1. Build a models × benchmarks score matrix.
  2. Take the **first principal component of the capability benchmarks** as a "capabilities score".
  3. Compute each safety benchmark's **Spearman correlation** with that score, called the "capabilities correlation". [H]
- *Implication:* this is the simplest operational **discriminant-validity-against-g** test in the literature. Any new benchmark claiming to measure something other than "being a better model" should report its capabilities correlation.

#### 3.5 Other position and theory papers

- **Wallach et al. (2025), "Position: Evaluating Generative AI Systems is a Social Science Measurement Challenge", ICML 2025 (PMLR v267), arXiv:2411.10939.** Title, venue and ID seen. The Desai et al. authors build directly on it. [H for bibliographic details]
- **Kearns (2026), "Quantifying construct validity in large language model evaluations", arXiv:2602.15532.** This is a thesis; the abstract was read in an arXiv-feed mirror.
  - "Latent factor models ignore scaling laws, and as a result, the capabilities they extract often proxy model size. Scaling laws ignore measurement error, and as a result, the capabilities they extract are both uninterpretable and overfit to the observed benchmarks."
  - The proposed "structured capabilities model" lets scale inform capabilities, which in turn inform scores up to measurement error. It "outperform[s] latent factor models on parsimonious fit indices, and exhibit[s] better out-of-distribution benchmark prediction than scaling laws" on Open LLM Leaderboard data. [H for abstract]
  - A secondary AI-generated digest adds that the dominant EFA factor explains about 72% of variance and correlates with log-parameters (R² ≈ 0.47). [L; verify]
- **Alaa et al. (2025), "Medical large language model benchmarks should prioritize construct validity", arXiv:2503.10694.** Seen in the Desai et al. bibliography. [H for existence]
- **Liu, Blodgett, Cheung, Liao, Olteanu & Xiao (2024), "ECBD: Evidence-Centered Benchmark Design for NLP", ACL 2024, pp. 16349–16365, arXiv:2406.08723.** Seen in the BetterBench and ADeLe bibliographies. It ports evidence-centered design from educational assessment. [H for existence; content from background knowledge]
- **Burnell et al. (2023), "Rethink reporting of evaluation results in AI", *Science* 380(6641):136–138.** Seen in the Desai bibliography. [H for existence]
- **Psychometrics-for-AI positions:**
  - Wang, Jiang, Hernández-Orallo, Stillwell, Sun, Luo & Xie (2023), "Evaluating General-Purpose AI with Psychometrics", arXiv:2310.16379. The abstract argues that task-collection benchmarks cannot predict performance on new tasks, focus on aggregates, and raise "questions about what is being measured". It proposes placing psychometrics "at the core of evaluating general-purpose AI". [H]
  - Zhuang et al., "From Static Benchmarks to Adaptive Testing: Psychometrics in AI Evaluation", arXiv:2306.10512. It argues for computerized adaptive testing with item parameter estimation. [H] It appeared at **ICML 2025** (position track, PMLR v267, "zhuang25e") as "Position: AI Evaluation Should Learn from How We Test Humans". [corrected by fact-check: upgraded from [M] to [H] via a PMLR-derived ICML 2025 listing (zhihengli-casia/AI-Paper-Trends). The ICML author list appears to differ from the arXiv list ("Yan Zhuang, Qi Liu, Zachary Pardos, Patrick C. Kyllonen, Jiyun Zu, Zhenya Huang, et al."), so check PMLR before citing the ICML version.]
  - Ye, Jin, Xie, Zhang & Song (2025), "Large Language Model Psychometrics: A Systematic Review of Evaluation, Validation, and Enhancement", arXiv:2505.08245. Seen via its companion paper list, ValueByte-AI/Awesome-LLM-Psychometrics, which mostly covers personality, values and morality constructs rather than capability measurement. [H for existence]
  - Hernández-Orallo (2017), *The Measure of All Minds: Evaluating Natural and Artificial Intelligence*, Cambridge University Press, and Hernández-Orallo (2017), "Evaluation in artificial intelligence: from task-oriented to ability-oriented measurement", *Artificial Intelligence Review* 48:397–447. Both seen in the ADeLe bibliography. [H for existence]

### 4. Item response theory in NLP and LLM evaluation

**Lineage (bibliographic details verified):**
- Lalor, Wu & Yu (2016), "Building an evaluation scale using item response theory", EMNLP 2016, pp. 648–657.
- Martínez-Plumed, Prudêncio, Martínez-Usó & Hernández-Orallo (2019), "Item response theory in AI: Analysing machine learning classifiers at the instance level", *Artificial Intelligence* 271:18–42, doi:10.1016/j.artint.2018.09.004.
- Vania et al. (2021), "Comparing test sets with item response theory", ACL-IJCNLP 2021, pp. 1141–1158.
- Rodriguez, Barrow, Hoyle, Lalor, Jia & Boyd-Graber (2021), "Evaluation Examples are not Equally Informative: How Should That Change NLP Leaderboards?", ACL 2021, pp. 4486–4503.
- Lalor, Rodriguez, Sedoc & Hernández-Orallo (2024), "Item response theory for natural language processing", EACL 2024 tutorial, pp. 9–13.

[H for all bibliographic facts]

**LLM-era results:**

| Work | Key verified facts | Source / confidence |
|---|---|---|
| **tinyBenchmarks** (Maia Polo, Weber, Choshen, Sun, Xu & Yurochkin; ICML 2024; arXiv:2402.14992) | **100 examples per tiny dataset** for Open LLM Leaderboard tasks (TruthfulQA, GSM8K, Winogrande, ARC, HellaSwag, MMLU) and AlpacaEval 2.0. MMLU estimation error (mean across LLMs) is IRT 0.024, p-IRT 0.016, gp-IRT 0.016. These are on a 0–1 accuracy scale, i.e. about 1.6–2.4 points. | Official README [H]; ICML venue from DBLP-style bib in borgr/publications [H]; ICML 2024 = PMLR v235 (mlresearch/v235) [fact-check] |
| **metabench** (Kipnis, Voudouris, Schulze Buschoff & Schulz; ICLR 2025; arXiv:2407.12844) [fact-check note: the arXiv title differs from the ICLR title: "metabench – a sparse benchmark to measure general ability in large language models" (ADeLe ref [89])] | Distils Open LLM Leaderboard 1 to "<3% of its original size". Item selection uses IRT on "over 5000 LLMs". The six benchmark scores are reconstructed with "<0.9% mean absolute error" and the leaderboard score with "<0.5%". Sloth summarises a factor analysis in which "the main factor (carrying 80% of the data variability) is highly correlated with the 'grand' (average) score". | Official README [H]; Sloth full text [H] |
| **Fluid Benchmarking** (Hofmann, Heineman, Magnusson, Lo, Dodge, Sap, Koh, Wang, Hajishirzi & Smith; COLM 2025; arXiv:2509.11106) | Fits an item response model to existing LM results and selects items adaptively (CAT-style). On efficiency, validity, variance and saturation it beats random sampling and IRT baselines, "e.g., higher validity and less variance on MMLU with fifty times fewer items". "Item response theory … increases validity, while dynamic item selection reduces variance." | Official repo BibTeX [H]; abstract via paper-notes mirror [H] |
| **Signal and Noise** (Heineman, Hofmann, Magnusson, Gu, Smith, Hajishirzi, Lo & Dodge; NeurIPS 2025 [corrected by fact-check: venue added]; arXiv:2508.13144) | Defines *signal* (a benchmark's ability to separate models) and *noise* (sensitivity to random variability during training) and studies their ratio. The NeurIPS abstract reports 30 benchmarks and 465 open-weight models from 60M to 32B parameters. | Official README [H]; NeurIPS 2025 listing and abstract via davidheineman/conference-papers and zhihengli-casia/AI-Paper-Trends [H] |
| **Growing Pains** (Habba, Itzhak, Yehudai, Perlitz, Bandel, Shmueli-Scheuer, Choshen & Stanovsky [corrected by fact-check: full author list from an arXiv digest]; arXiv:2604.12843, April 2026; code at eliyahabba/growing-pains) | Multidimensional IRT with **fixed-parameter calibration** (anchor items held fixed) so a growing suite stays comparable. With 100 anchors per dataset, MAE is about 2–3 pp on more than 400 models (Open LLM Leaderboard 395 models; MMLU 428). | arXiv ID from digest [H]; numbers from a structured sidecar in the author-affiliated repo borgr/paper-geo [M] |
| **Epoch Capabilities Index / "A Rosetta Stone for AI Benchmarks"** (Ho, Denain, Atanasov, Albanie & Shah; arXiv:2512.00193) | Fits "performance = sigmoid(discriminability × (capability − difficulty))" across benchmarks, giving one capability score per model and a difficulty and slope per benchmark. The scale is anchored at Claude 3.5 Sonnet = 130 and GPT-5 = 150, with bootstrap CIs. **Unidimensionality is assumed, not tested.** [fact-check note: this last sentence is the dossier author's interpretation from the README only. The paper text was not read, so whether it tests dimensionality is unverified. Soften to "the README model is one-dimensional" unless checked.] | Official epoch-research/eci-public README [H] |
| **Quantifying variance** (Madaan et al. 2024, arXiv:2406.10229) | Seen only as a bibliographic entry (Llama 3 report bibliography and an arXiv listing). Content not verified. | [H for existence] |

**ADeLe / General Scales (Zhou, Pacchiardi, Martínez-Plumed, Collins, … , Hernández-Orallo; 26 authors in the arXiv v2 order given in the refs JSON; arXiv:2503.06378; published in *Nature* 2026, doi:10.1038/s41586-026-10303-2)** is a non-IRT alternative. Primary source: full text. [corrected by fact-check: author order taken from an arXiv listing (CSQianDong digest) and the adgomant BibTeX. The *Nature* publication comes from the first author's own repo (lexzhou/ADeLe-practical-session). Vol. 652, pp. 58–67 comes from two third-party bibs [M]. One third-party extract lists different co-authors for the *Nature* version, and the practical-session repo mentions 19 rubrics, so the numbers below are from arXiv v2 (18 rubrics). Check nature.com before citing *Nature*-specific details.]
- It uses **18 rubrics** that assign each item a demand level on general scales. They are applied to **16,108 instances** from **63 tasks in 20 benchmarks** (289,944 annotations), with **15 LLMs**.
- It critiques factor analysis and IRT directly: these populational techniques "lead to different results for AI system 'populations', whenever a new set of LLMs are added". It cites the change between Burnell et al. and Ilić & Gignac. Its own abilities are "non-populational" and absolute.
- Finding: "many benchmarks lack either specificity or sensitivity: they do not have a minimum number of instances of all demands for the dimensions their designers claimed they measure, and they include non-zero demands on other dimensions".
- Instance-level success prediction from demand profiles beats black-box baselines, especially out of distribution. The best reported AUROC is 0.88 (GPT-4o).
- Inter-rater agreement for the GPT-4o rubric annotation averages 0.86.
- [H for all of the above]

### 5. The structure of LLM capabilities (g-like factor vs. multiple abilities)

All rows are primary unless noted.

| Study | Data | Structural finding |
|---|---|---|
| **Burnell, Hao, Conway & Hernández-Orallo (2023)**, arXiv:2306.10062 | 29 LLMs × 27 HELM tasks | Positive manifold with mean inter-task **r = 0.56**. Frequentist EFA gives **three factors** explaining **33%, 31% and 17%** of variance (**82% cumulative**), interpreted as comprehension, language modelling and reasoning. Model size correlates positively with all three, most strongly with comprehension. Instruction tuning correlates negatively with the language-modelling factor and positively with reasoning. Authors: "we suggest that benchmarks could be streamlined by focusing on tasks that tap into each broad model ability." [H]. *Note:* an LLM-written secondary summary attached the wrong factor labels to the percentages. [corrected by fact-check: labels re-checked in the paper text. F1 = comprehension (33%), F2 = language modelling (31%), F3 = reasoning (17%) ("broadly interpreted as capturing comprehension, language modelling, and reasoning, respectively"; Table 2). The authors also report poor EFA fit given the small sample (CFI = 0.70, TLI = 0.61, RMSEA = 0.26), which should be cited alongside the 82%.] |
| **Ilić (2023)**, arXiv:2310.11616; **Ilić & Gignac (2024)**, *Intelligence* 106:101858 | Open LLM Leaderboard and GLUE | Ruan et al. report that Ilić "found that a single factor explains 85% of the performance on the Open LLM Leaderboard and GLUE leaderboard". [H that Ruan says this; M for the number itself] [fact-check note: Ruan's ref [40] is the 2023 arXiv paper "Unveiling the general intelligence factor in language models: A psychometric approach" (Ilić alone). The 2024 *Intelligence* article with Gignac has a different title. Attribute the 85% only to the 2023 arXiv paper, and do not treat the two as the same work without checking.] |
| **Owen (2024)**, "How predictable is language model benchmark performance?", arXiv:2401.04757 (Epoch) | 11 architectures, five orders of magnitude of compute | Extrapolating BIG-Bench Hard average across one order of magnitude of compute gives mean absolute error of about **6 pp**. For individual BIG-Bench tasks it is about **18 pp**. "Aggregated benchmarks, averaging over many individual tasks, are much more predictable." [H] |
| **Ruan, Maddison & Hashimoto (2024)**, "Observational Scaling Laws and the Predictability of Language Model Performance", NeurIPS 2024, arXiv:2405.10938 | About 100 public models (v3 abstract; v1 said about 80) on MMLU, ARC-C, HellaSwag, Winogrande, TruthfulQA, GSM8K, XWinograd and HumanEval. [corrected by fact-check: the PCA behind the 80%/97% figures uses **77 pretrained base models from 21 families** (v3 §3); ~100 is the paper-wide count. The "v1 said about 80" remark was not re-checked.] | "The top 3 PCs explaining ∼97% of the variance … the first PC alone explains nearly 80% of the variation". PC-1 is "general capability", PC-2 "reasoning" (math and code) and PC-3 "programming". Instruction-tuned appendix: top-3 PCs explain about 98.6%. PC measures scale log-linearly with training FLOPs within families. Agentic performance of models such as GPT-4 "can be precisely predicted from simpler non-agentic benchmarks". [H] |
| **Sloth** (Maia Polo, Somerstep, Choshen, Sun & Yurochkin; NeurIPS 2025; arXiv:2412.06540) | 12 benchmarks from Open LLM Leaderboard v1/v2 | Performance is driven by "low-dimensional latent skills, such as reasoning and instruction following". Family-specific efficiencies convert compute to skills. [H]. A secondary summary gives three weakly correlated skills (reasoning–knowledge r = 0.12). [M; read off figures, not re-verified] |
| **Zhang, Dominguez-Olmedo & Hardt (2025)**, "Train-before-Test Harmonizes Language Model Rankings", arXiv:2507.05195 | 61 models × 24 benchmarks | Under direct evaluation, cross-benchmark ranking agreement is average **Kendall τ = 0.52**. After identical benchmark-specific fine-tuning ("train-before-test") it rises to **0.76**, improving 274 of 276 pairs. PC1 variance goes from **70% to 86%**, and to **93%** within a family, making the matrix "essentially rank one". [H] |
| **Desai et al. (2026)**, COLM 2026 | 56 benchmarks × 53 models | Reasoning and knowledge are not discriminable. Several safety concepts load on capability. Format outweighs concept (see §3.3). [H] |
| **Kearns (2026)** | Open LLM Leaderboard | Plain latent factors proxy model size, so scale should be modelled explicitly (see §3.5). [H for abstract] |
| **Zhou et al. (2025)** | 15 LLMs, 20 benchmarks | Factor solutions are population-dependent. Knowledge abilities track model size. Reasoning, learning and abstraction, and social abilities are boosted in chain-of-thought and inference-heavy models. [H] |

**2025–2026 multi-factor results, secondary and not independently verified.** These come from an LLM-written literature table in elasticity-ai/stylized-facts, dated 2026-09. Treat all as **[L]** until checked.
- Maimon et al. 2025, "From Benchmarks to Skills: Low-Rank Factors…": 60 LLMs × 44 benchmarks, eight factors.
- Habba et al. 2026: 3–8 interpretable dimensions.
- Hou et al. 2026, "CogArena": 55 open-weight models × 13 cognitive paradigms; a common axis explains about half the variance.
- Haznitrama et al. 2026: a general factor across 156 models.
- The same table's "Gaps" section observes three things, all interpretive: almost all factor analyses use open-weight models and Open-LLM-Leaderboard-style short-answer tasks; agentic and long-horizon benchmarks are absent from the score matrices; and no study has tested whether a first factor extracted on one model population predicts a benchmark introduced later.

**Synthesis.**

1. There is robust evidence of a strong general factor. 70–85% of variance falls on the first component in most reported matrices, rising above 90% once task-specific preparation is equalised.
2. There is consistent evidence of a few secondary dimensions: reasoning or math/code, knowledge, instruction-following, and comprehension or language modelling.
3. Evidence is growing that measured "dimensions" partly reflect **method** (score format, LLM-judge use) and **scale**, not the intended construct.
4. The number and identity of factors are **unstable across model populations** (Zhou et al.). Any benchmark's validity evidence is therefore population-relative and must be re-established as frontier models change.

### 6. How much incremental information does a new benchmark add?

This section is my synthesis. Formulas are standard psychometrics. The numbers are illustrative calculations, not literature results.

- **Low-dimensionality means a high correlation with other benchmarks is the default, not a finding.** If PC1 explains about 80% of variance across existing benchmarks (Ruan et al.), then a new reliable benchmark that measures "being a stronger model" will correlate about 0.85–0.9 with the general index. It will add almost nothing. Bowman & Dahl, Burnell et al. and metabench/tinyBenchmarks all point the same way: a large fraction of existing items and benchmarks are redundant.
- **Decompose the variance of a new benchmark X across models.** Var(X) = g-loading² (shared with general capability) + reliable specific variance (s²) + error variance (1 − reliability).
  - The incremental information is s² = reliability − h², where h² is the communality with existing factors.
  - A benchmark can have low correlation with g simply because it is *noisy*. A low "capabilities correlation" alone is therefore **not** evidence of distinctiveness. Desai et al. make this caution for safety benchmarks, and Heineman et al. frame the same issue as signal-to-noise.
  - Reliability must be estimated first: split-half on items, re-runs across seeds or temperatures, IRT test information, and bootstrap CIs over items.
- **Report the disattenuated correlation with the general index**, r_Xg / √(rel_X · rel_g). If it is near 1, the benchmark is redundant however "novel" its tasks look. This is a standard correction; the 1.0 threshold is a rule of thumb, not from a cited LLM paper.
- **Incremental validity (Sechrest 1963; Hunsley & Meyer 2003) needs an external criterion.** Examples: success on real user tasks, expert-rated outputs in a deployment setting, or a held-out behavioural outcome. Then test ΔR² in a hierarchical regression: criterion ~ general index (ECI or PC1) [+ log-compute] + new benchmark.
  - Without a criterion, one can only show *discriminant* validity, not *utility*.
  - Ruan et al.'s pre-registered forecasts on later models show how to make such tests prospective.
- **Control scale explicitly.** Kearns (2026) argues, in a thesis that has not been peer reviewed, that latent factors absorb scale. [corrected by fact-check: earlier wording "shows" overstated the evidential status] Use a structured model (log-compute → capabilities → scores), or at least partial out log-compute, so the "specific" component is not just a size proxy.
- **Statistical power is the binding constraint because the unit of analysis is the model.** With n models, the standard error of a Fisher-z-transformed correlation is about 1/√(n − 3): about 0.19 for n = 30, 0.15 for n = 50, and 0.10 for n = 100. Typical studies use 29 (Burnell), 53 (Desai), 61 (Zhang) or about 100 (Ruan) models. So a new benchmark's partial correlation with g needs about 50–100 diverse models, or item-level IRT pooling, for a tight interval.
- **Method-variance controls (MTMM).** Desai et al. show that format (for example LLM-judge vs. exact-match) predicts correlation more than concept does. A new benchmark should demonstrate convergent validity with at least one **different-format** measure of the same construct. It should also show lower correlation with **same-format** benchmarks of *different* constructs.

---

## Implications for designing a new benchmark

These points are interpretive and derived from the evidence above. They are written as design requirements for the project's non-game benchmark.

1. **Write a validity argument up front** (Kane 2013; Messick; Bean et al. recommendations 1 and 8). Define the construct, its sub-components, what it is *not*, and the predicted nomological network: which existing benchmarks it should and should not correlate with, and which external outcomes it should predict. Pre-register these predictions.
2. **Target a construct that is plausibly off the general factor.** A new benchmark earns its place if it measures variance that PC1 or ECI misses. Evidence suggests candidates where ranking reversals already exist:
   - calibration and know-what-you-don't-know (ADeLe's metacognition dimension);
   - cost and utility-aware behaviour (Ethayarajh & Jurafsky);
   - over-refusal vs. refusal trade-offs, which Desai et al. found strongly inversely correlated and distinct.

   Avoid constructs that the literature shows collapse onto g: generic "reasoning" vs. "knowledge" distinctions (Desai et al.), and multiple-choice bias QA that tracks reasoning (BBQ-accuracy).
3. **Ship five pieces of validity evidence with the benchmark.**
   - (a) **Reliability.** Item-level results, multiple seeds, bootstrap CIs, and a signal-to-noise ratio (Heineman et al.). Answers BetterBench's 14/24 finding and Bean et al.'s finding that only 16% (secondary figure) of papers use statistical tests.
   - (b) **Convergent evidence** with at least one alternative operationalization in a *different* format.
   - (c) **Discriminant evidence.** Report the capabilities correlation (Safetywashing method), the disattenuated correlation with ECI or PC1, and correlations with same-format benchmarks of other constructs (MTMM).
   - (d) **Incremental validity.** ΔR² over the general index (and log-compute) for an external criterion, on held-out and *newer* models.
   - (e) **Population stability.** Bootstrap over model subsets and time-split by release date, addressing the population-dependence critique of Zhou et al.
4. **Use IRT from day one, and link to a common scale.**
   - Calibrate item difficulty and discrimination empirically rather than by author-assigned labels. This addresses the Bloom's-taxonomy failure the user flagged, where generator-assigned difficulty levels were never validated.
   - Include **anchor items** linked to existing scales (ECI-style sigmoid; Growing Pains fixed-parameter calibration). Scores are then comparable across versions and to other benchmarks. This answers the user's Qi Town critique ("3 separate scores, none comparable").
   - Report two numbers: the model's position on the general scale, and its **residual (construct-specific) score with a CI**.
5. **Make the item bank generative, and refresh it with linked calibration.** This counters saturation and contamination (the MastermindEval memorization critique) without breaking comparability. IRT anchors allow new items to be calibrated onto the old scale (Growing Pains; Fluid Benchmarking). Adaptive item selection cuts cost; tinyBenchmarks and metabench show 100 items or under 3% of the bank can suffice for a unidimensional score.
6. **Control method variance deliberately.** Vary format, and measure each construct with at least two score formats such as programmatic verification and human rating. Avoid relying solely on an LLM judge, because Desai et al. found LLM-judge format is the strongest predictor of benchmark similarity. Also treat items that LLMs themselves generate with caution (the Bloom's-benchmark "echo chamber" concern).
7. **Enough items per reported cell and enough models.** Size the item bank for the smallest effect you intend to rank. BetterBench and Bowman & Dahl both stress statistical power; this addresses the Boardwalk critique ("only 12 games, too few to rank models"). Evaluate at least about 50 diverse models, spanning families and scales, so that partial correlations with g are estimable.
8. **Instance-level demand annotation.** Annotate items with demand levels (ADeLe-style rubrics) to show **sensitivity** (the benchmark covers the claimed demand range) and **specificity** (low demands on extraneous dimensions). Many existing benchmarks fail both (Zhou et al.).
9. **Consequential validity and maintenance.** Plan for Goodhart effects and retirement (BetterBench lifecycle; Messick's consequential aspect). Publish replication scripts (BetterBench 17/24 finding), versioning, and a contamination policy.

---

## Claims ledger

| # | Claim | Source URL(s) | Confidence |
|---|---|---|---|
| 1 | Bean et al. (NeurIPS 2025 D&B, arXiv:2511.04703) had 29 expert reviewers systematically review 445 LLM benchmarks and give eight key recommendations. | https://github.com/CSQianDong/Awesome-arXiv-Daily-Reporter/blob/main/10-Nov-2025/AI/README.md ; venue: https://github.com/afedercooper/afedercooper.github.io/blob/main/paper/desai2026validity.pdf | High |
| 2 | Per a secondary summary, only 16% of the 445 reviewed papers used statistical tests to compare models, and 47.8% had contested phenomenon definitions. | https://github.com/zhaoyang97/Paper-Notes-en/blob/main/docs/NeurIPS2025/recommender/measuring_what_matters_construct_validity_in_large_language_model_benchmarks.md | Medium-low (secondary; verify in PDF) |
| 3 | BetterBench (NeurIPS 2024 D&B, arXiv:2411.12990) defines 46 best practices across a five-stage lifecycle and assesses 24 benchmarks. 14/24 report no uncertainty or significance; 17/24 lack easy replication scripts; MMLU scored 5.5 vs GPQA 11.0. | https://github.com/Lumysia/agi-benchmark-framework/blob/main/papers/BetterBench_Criteria.txt | High |
| 4 | Ruan, Maddison & Hashimoto (NeurIPS 2024): the top-3 PCs of standard benchmark scores explain about 97% of variance and PC1 alone nearly 80%. PC measures scale log-linearly with training compute within families. | https://github.com/elasticity-ai/stylized-facts/blob/main/references/text/ruan2024observational.txt ; https://github.com/ryoungj/ObsScaling | High |
| 5 | Burnell et al. (2023): across 29 LLMs and 27 HELM tasks, mean inter-task r = 0.56. Three factors explain 33%, 31% and 17% (82% cumulative) of variance. | https://github.com/elasticity-ai/stylized-facts/blob/main/references/text/burnell2023reveal.txt | High |
| 6 | Ruan et al. report that Ilić (2023) found a single factor explaining 85% of performance on the Open LLM Leaderboard and GLUE. | https://github.com/elasticity-ai/stylized-facts/blob/main/references/text/ruan2024observational.txt | Medium (second-hand number) |
| 7 | Zhang, Dominguez-Olmedo & Hardt (2025): across 61 models and 24 benchmarks, mean cross-benchmark Kendall τ is 0.52 under direct evaluation and 0.76 under train-before-test. PC1 variance rises from 70% to 86% (93% within a family). | https://github.com/elasticity-ai/stylized-facts/blob/main/references/text/zhang2025trainbeforetest.txt | High |
| 8 | Desai et al. (COLM 2026): across 56 benchmarks and 53 models, reasoning and knowledge benchmarks are not discriminable. Several safety benchmarks correlate more with capability benchmarks than with each other. Score format predicts benchmark similarity more than concept (β_format 0.275 vs β_concept 0.138). | https://github.com/afedercooper/afedercooper.github.io/blob/main/paper/desai2026validity.pdf | High |
| 9 | Safetywashing (NeurIPS 2024 Datasets and Benchmarks Track [corrected by fact-check]): many safety benchmarks highly correlate with upstream capabilities and training compute. The method is the Spearman correlation between a safety benchmark and PC1 of capability benchmarks. | https://github.com/centerforaisafety/safetywashing ; https://github.com/justinphan3110cais/safetywashing_website ; https://github.com/Luvata/arxive/blob/main/pages/2024-08-01-cs-lg.html | High |
| 10 | tinyBenchmarks (ICML 2024) uses 100 examples per benchmark; mean MMLU estimation error is 0.024 (IRT) and 0.016 (gp-IRT). | https://github.com/felipemaiapolo/tinyBenchmarks ; https://github.com/borgr/publications/blob/main/orig.bib | High |
| 11 | metabench (ICLR 2025) distils the Open LLM Leaderboard to under 3% of its size using IRT on over 5000 LLMs. It reconstructs benchmark scores with under 0.9% MAE and the leaderboard score with under 0.5% MAE. | https://github.com/adkipnis/metabench | High |
| 12 | Fluid Benchmarking (COLM 2025): IRT raises validity and adaptive item selection lowers variance; better validity and lower variance on MMLU with 50× fewer items. | https://github.com/allenai/fluid-benchmarking ; https://github.com/AkihikoWatanabe/paper_notes/blob/main/agent_docs/COLM.xml | High |
| 13 | Zhou et al. (ADeLe, arXiv:2503.06378; *Nature* 2026, doi:10.1038/s41586-026-10303-2 [corrected by fact-check]): 18 rubrics (arXiv v2), 16,108 instances from 63 tasks and 20 benchmarks, 15 LLMs. Population-based factor analysis and IRT give different results as new LLMs are added. Many benchmarks lack sensitivity or specificity for their claimed constructs. | https://github.com/elasticity-ai/stylized-facts/blob/main/references/text/zhou2025generalscales.txt | High |
| 14 | Kearns (2026, arXiv:2602.15532): latent factor models extract capabilities that "often proxy model size". A structured-capabilities model fits better and predicts held-out benchmarks better than scaling laws. | https://github.com/Barca0412/Introduction-to-Quantitative-Finance/blob/main/data/papers/2026-02-18.json | High (abstract only) |
| 15 | The Epoch Capabilities Index fits performance = sigmoid(discriminability × (capability − difficulty)), a one-dimensional IRT model anchored at Claude 3.5 Sonnet = 130 and GPT-5 = 150. | https://github.com/epoch-research/eci-public | High |
| 16 | Owen (2024): extrapolating BIG-Bench Hard average across one order of magnitude of compute gives about 6 pp mean absolute error, vs about 18 pp for individual tasks. | https://github.com/elasticity-ai/stylized-facts/blob/main/references/text/owen2024predictable.txt | High |
| 17 | Hutchinson et al. (FAccT 2022) find that ML evaluations focus on a narrow range of decontextualized predictive behaviours and a handful of evaluation methods. | https://github.com/djroytburg/mind_the_gap/blob/main/data/final_dataset/fat_2022.jsonl | High |
| 18 | Bowman & Dahl (NAACL 2021) argue that NLU evaluation is broken, that adversarial OOD test sets obscure the abilities being measured, and that fixes require better dataset design, annotation reliability, size and handling of social bias. | https://github.com/makrai/notes/blob/master/bowman-21-benchmark-naacl.md | High (abstract notes) |
| 19 | Growing Pains (Habba et al., 8 authors, arXiv:2604.12843): with 100 anchor items per dataset, fixed-parameter calibration predicts full-benchmark accuracy within about 2–3 pp MAE on more than 400 models. | https://github.com/borgr/paper-geo/blob/main/data/sidecars/growing-pains-extensible-and-efficient-llm-benchmarking-via.md ; https://github.com/duanyytop/agents-radar/blob/main/digests/2026-04-16/ai-arxiv-en.md | Medium |
| 20 | Classical sources for convergent/discriminant validity (Campbell & Fiske 1959, Psych. Bull. 56(2):81–105) and incremental validity (Sechrest 1963, EPM 23(1):153–158; Hunsley & Meyer 2003, Psych. Assess. 15(4):446–455). | https://github.com/elliottower/scib-construct-validity/blob/main/docs/paper_d_v11.bib ; https://github.com/forrtproject/forrtproject.github.io/blob/main/content/glossary/references/index.md | High (bibliographic) |

---

## References

*"Seen at" gives where the item was observed in this session. Each item is marked verified-primary, verified-bibliographic or secondary.*

**Classical measurement theory**
1. Cronbach, L. J., & Meehl, P. E. (1955). Construct validity in psychological tests. *Psychological Bulletin*, 52(4), 281–302. doi:10.1037/h0040957. Seen at elliottower/scib-construct-validity bib and in the BetterBench bibliography. [bibliographic]
2. Campbell, D. T., & Fiske, D. W. (1959). Convergent and discriminant validation by the multitrait-multimethod matrix. *Psychological Bulletin*, 56(2), 81–105. doi:10.1037/h0046016. Seen at the same bib and in the Desai et al. bibliography. [bibliographic]
3. Sechrest, L. (1963). Incremental validity: A recommendation. *Educational and Psychological Measurement*, 23(1), 153–158. doi:10.1177/001316446302300113. Seen at the FORRT glossary references. [bibliographic]
4. Messick, S. (1989). Validity. In R. L. Linn (Ed.), *Educational Measurement* (3rd ed., pp. 13–103). American Council on Education/Macmillan. Seen at 7th-ave-labs/work-validity-eval references.bib. [bibliographic]
5. Messick, S. (1989). Meaning and values in test validation: The science and ethics of assessment. *Educational Researcher*, 18(2), 5–11. Seen in the Desai et al. bibliography. [bibliographic]
6. Messick, S. (1995). Validity of psychological assessment: Validation of inferences from persons' responses and performances as scientific inquiry into score meaning. *American Psychologist*, 50(9), 741–749. doi:10.1037/0003-066X.50.9.741. Seen at harvard-edge/cs249r_book references.bib. [bibliographic]
7. Adcock, R., & Collier, D. (2001). Measurement validity: A shared standard for qualitative and quantitative research. *American Political Science Review*, 95(3), 529–546. Seen in the Desai et al. bibliography. [bibliographic]
8. Hunsley, J., & Meyer, G. J. (2003). The incremental validity of psychological testing and assessment: Conceptual, methodological, and statistical issues. *Psychological Assessment*, 15(4), 446–455. doi:10.1037/1040-3590.15.4.446. Seen at the FORRT glossary references. [bibliographic]
9. Kane, M. T. (2013). Validating the interpretations and uses of test scores. *Journal of Educational Measurement*, 50(1), 1–73. doi:10.1111/jedm.12000. Seen at 7th-ave-labs/work-validity-eval references.bib. [bibliographic]
10. American Educational Research Association, American Psychological Association, & National Council on Measurement in Education (2014). *Standards for Educational and Psychological Testing*. AERA. Seen at harvard-edge/cs249r_book references.bib. [bibliographic]
11. Hernández-Orallo, J. (2017). *The Measure of All Minds: Evaluating Natural and Artificial Intelligence*. Cambridge University Press. Seen in the ADeLe bibliography. [bibliographic]
12. Hernández-Orallo, J. (2017). Evaluation in artificial intelligence: from task-oriented to ability-oriented measurement. *Artificial Intelligence Review*, 48, 397–447. Seen in the ADeLe bibliography. [bibliographic]
13. Jacobs, A. Z., & Wallach, H. (2021). Measurement and Fairness. *FAccT '21*, 375–385. doi:10.1145/3442188.3445901. Seen at 7th-ave-labs/work-validity-eval references.bib. [bibliographic]

**Benchmark critique and meta-science**

14. Ethayarajh, K., & Jurafsky, D. (2020). Utility is in the Eye of the User: A Critique of NLP Leaderboards. *EMNLP 2020*. doi:10.18653/v1/2020.emnlp-main.393; arXiv:2009.13888. Seen at makrai/notes, acl-org/ethics-reading-list and roomylee/nlp-papers-with-arxiv. [secondary abstract notes + bibliographic]
15. Raji, I. D., Denton, E., Bender, E. M., Hanna, A., & Paullada, A. (2021). AI and the Everything in the Whole Wide World Benchmark. *NeurIPS 2021 Datasets and Benchmarks Track* (Round 2; OpenReview j6NxpQbREA1). arXiv:2111.15366, whose arXiv author order is Raji, Bender, Paullada, Denton, Hanna. [corrected by fact-check: proceedings author order] Seen at mavenlin/ai_research_trends, the BetterBench text and adewale/skill-eval-harness. [bibliographic; definition quoted via BetterBench]
16. Bowman, S. R., & Dahl, G. E. (2021). What Will it Take to Fix Benchmarking in Natural Language Understanding? *NAACL 2021*. arXiv:2104.02145. Seen at makrai/notes and the ADeLe bibliography. [abstract notes]
17. Liao, T., Taori, R., Raji, I. D., & Schmidt, L. (2021). Are We Learning Yet? A Meta Review of Evaluation Failures Across Machine Learning. *NeurIPS 2021 Datasets and Benchmarks Track (Round 2)*. OpenReview mPducS1MsEK. Seen at Doragd/Algorithm-Practice-in-Industry NeurIPS-2021 list and fairmlbook datasets chapter. [bibliographic + secondary description]
18. Hutchinson, B., Rostamzadeh, N., Greer, C., Heller, K., & Prabhakaran, V. (2022). Evaluation Gaps in Machine Learning Practice. *FAccT 2022*, 1859–1876 [pages added by fact-check]. doi:10.1145/3531146.3533233; arXiv:2205.05256. Seen at djroytburg/mind_the_gap (DBLP/OpenAlex record with abstract). [primary abstract]
19. Blodgett, S. L., Lopez, G., Olteanu, A., Sim, R., & Wallach, H. (2021). Stereotyping Norwegian Salmon: An Inventory of Pitfalls in Fairness Benchmark Datasets. *ACL-IJCNLP 2021*, 1004–1015. Seen in the Desai et al. bibliography. [bibliographic]
20. Reuel, A., Hardy, A., Smith, C., Lamparth, M., Hardy, M., & Kochenderfer, M. J. (2024). BetterBench: Assessing AI Benchmarks, Uncovering Issues, and Establishing Best Practices. *NeurIPS 2024 Datasets and Benchmarks Track*. arXiv:2411.12990. Seen at the Lumysia/agi-benchmark-framework full text. [primary]
21. Ren, R., Basart, S., Khoja, A., Gatti, A., Phan, L., Yin, X., Mazeika, M., Pan, A., Mukobi, G., Kim, R. H., Fitz, S., & Hendrycks, D. (2024). Safetywashing: Do AI Safety Benchmarks Actually Measure Safety Progress? *NeurIPS 2024 Datasets and Benchmarks Track* (37:68559–68594) [corrected by fact-check: track]. arXiv:2407.21792. Seen at centerforaisafety/safetywashing and the project website source. [primary]
22. Liu, Y. L., Blodgett, S. L., Cheung, J. C. K., Liao, Q. V., Olteanu, A., & Xiao, Z. (2024). ECBD: Evidence-Centered Benchmark Design for NLP. *ACL 2024*, 16349–16365. arXiv:2406.08723. Seen in the BetterBench and ADeLe bibliographies. [bibliographic]
23. Wallach, H., Desai, M., Cooper, A. F., Wang, A., Atalla, C., Barocas, S., et al. (2025). Position: Evaluating Generative AI Systems is a Social Science Measurement Challenge. *ICML 2025* (PMLR 267). arXiv:2411.10939. Seen at VectorInstitute/aspis, zhihengli-casia/AI-Paper-Trends and the Desai bibliography. [bibliographic]
24. Bean, A. M., Kearns, R. O., Romanou, A., et al. (2025). Measuring what Matters: Construct Validity in Large Language Model Benchmarks. *NeurIPS 2025 Datasets and Benchmarks Track*. arXiv:2511.04703; OpenReview mdA5lVvNcU. Seen at the arXiv daily digest (abstract, full author list), am-bean/benchmark_review and the Desai bibliography. [primary abstract; stats secondary]
25. Alaa, A., Hartvigsen, T., Golchini, N., Dutta, S., Dean, F., Raji, I. D., & Zack, T. (2025). Medical large language model benchmarks should prioritize construct validity. arXiv:2503.10694. Seen in the Desai bibliography. [bibliographic]
26. Kearns, R. O. (2026). Quantifying construct validity in large language model evaluations. arXiv:2602.15532 (thesis). Seen in an arXiv feed mirror (Barca0412/…/2026-02-18.json). [primary abstract]
27. Desai, M., Truong, S. T., Wallach, H., Chouldechova, A., Cooper, A. F., Garcia-Gathright, J., Ho, D. E., Jacobs, A. Z., Koyejo, S., Pangakis, N., & Wang, A. (2026). What AI Benchmarks Actually Measure: Adapting Convergent and Discriminant Validity to Interrogate Fifty-Six AI Benchmarks. *COLM 2026*. arXiv:2609.08812. Seen at afedercooper/afedercooper.github.io PDF. [primary]

**Psychometrics for AI and IRT**

28. Lalor, J. P., Wu, H., & Yu, H. (2016). Building an Evaluation Scale using Item Response Theory. *EMNLP 2016*, 648–657. Seen at the pbotter42 irt-contamination bib and the ADeLe bibliography. [bibliographic]
29. Martínez-Plumed, F., Prudêncio, R. B. C., Martínez-Usó, A., & Hernández-Orallo, J. (2019). Item response theory in AI: Analysing machine learning classifiers at the instance level. *Artificial Intelligence*, 271, 18–42. doi:10.1016/j.artint.2018.09.004. [bibliographic]
30. Vania, C., Htut, P. M., Huang, W., Mungra, D., Pang, R. Y., Phang, J., Liu, H., Cho, K., & Bowman, S. R. (2021). Comparing Test Sets with Item Response Theory. *ACL-IJCNLP 2021*, 1141–1158. [bibliographic]
31. Rodriguez, P., Barrow, J., Hoyle, A. M., Lalor, J. P., Jia, R., & Boyd-Graber, J. (2021). Evaluation Examples are not Equally Informative: How Should That Change NLP Leaderboards? *ACL 2021*, 4486–4503. [bibliographic]
32. Lalor, J. P., Rodriguez, P., Sedoc, J., & Hernández-Orallo, J. (2024). Item response theory for natural language processing. *EACL 2024 Tutorial Abstracts*, 9–13. [bibliographic]
33. Maia Polo, F., Weber, L., Choshen, L., Sun, Y., Xu, G., & Yurochkin, M. (2024). tinyBenchmarks: evaluating LLMs with fewer examples. *ICML 2024*. arXiv:2402.14992. Seen at felipemaiapolo/tinyBenchmarks and borgr/publications bib. [primary]
34. Kipnis, A., Voudouris, K., Schulze Buschoff, L. M., & Schulz, E. (2025). metabench – A Sparse Benchmark of Reasoning and Knowledge in Large Language Models. *ICLR 2025*. arXiv:2407.12844. Seen at adkipnis/metabench. [primary]
35. Wang, X., Jiang, L., Hernández-Orallo, J., Stillwell, D., Sun, L., Luo, F., & Xie, X. (2023). Evaluating General-Purpose AI with Psychometrics. arXiv:2310.16379. Seen at qhduan/cn-chat-arxiv (abstract) and the ADeLe bibliography. [primary abstract]
36. Zhuang, Y., Liu, Q., Ning, Y., Huang, W., Pardos, Z. A., Kyllonen, P. C., Zu, J., Mao, Q., Lv, R., Huang, Z., Zhao, G., Zhang, Z., Wang, S., & Chen, E. (2023/2025). From Static Benchmarks to Adaptive Testing: Psychometrics in AI Evaluation. arXiv:2306.10512. It appeared as "Position: AI Evaluation Should Learn from How We Test Humans", ICML 2025 (PMLR 267). [corrected by fact-check: confirmed, not "reportedly"; the ICML author list may differ] Seen at Luvata/arxive (abstract) and zhaoyang97/Paper-Notes. [primary abstract; venue secondary]
37. Ye, H., Jin, J., Xie, Y., Zhang, X., & Song, G. (2025). Large Language Model Psychometrics: A Systematic Review of Evaluation, Validation, and Enhancement. arXiv:2505.08245. Seen at ValueByte-AI/Awesome-LLM-Psychometrics. [bibliographic]
38. Hofmann, V., Heineman, D., Magnusson, I., Lo, K., Dodge, J., Sap, M., Koh, P. W., Wang, C., Hajishirzi, H., & Smith, N. A. (2025). Fluid Language Model Benchmarking. *COLM 2025*. arXiv:2509.11106. Seen at allenai/fluid-benchmarking. [primary]
39. Heineman, D., Hofmann, V., Magnusson, I., Gu, Y., Smith, N. A., Hajishirzi, H., Lo, K., & Dodge, J. (2025). Signal and Noise: A Framework for Reducing Uncertainty in Language Model Evaluation. *NeurIPS 2025* [corrected by fact-check: venue]. arXiv:2508.13144. Seen at allenai/signal-and-noise. [primary README]
40. Madaan, L., Singh, A. K., Schaeffer, R., Poulton, A., Koyejo, S., Stenetorp, P., Narang, S., & Hupkes, D. (2024). Quantifying Variance in Evaluation Benchmarks. arXiv:2406.10229. Seen at the Llama 3 report bibliography mirror and isLinXu/paper-list. [bibliographic]
41. Habba, E., Itzhak, I., Yehudai, A., Perlitz, Y., Bandel, E., Shmueli-Scheuer, M., Choshen, L., & Stanovsky, G. (2026) [authors completed by fact-check]. Growing Pains: Extensible and Efficient LLM Benchmarking Via Fixed Parameter Calibration. arXiv:2604.12843. Seen at duanyytop/agents-radar and borgr/paper-geo. [secondary structured notes]
42. Ho, A., Denain, J.-S., Atanasov, D., Albanie, S., & Shah, R. (2025). A Rosetta Stone for AI Benchmarks. arXiv:2512.00193. Epoch Capabilities Index code: github.com/epoch-research/eci-public. [primary README]
43. Zhou, L., Pacchiardi, L., Martínez-Plumed, F., Collins, K. M., Moros-Daval, Y., Zhang, S., Zhao, Q., Huang, Y., Sun, L., Prunty, J. E., Li, Z., Sánchez-García, P., Chen, K. J., Casares, P. A. M., Zu, J., Burden, J., Mehrbakhsh, B., Stillwell, D., Cebrian, M., Wang, J., Henderson, P., Wu, S. T., Kyllonen, P. C., Cheke, L., Xie, X., & Hernández-Orallo, J. (2025). General Scales Unlock AI Evaluation with Explanatory and Predictive Power. arXiv:2503.06378. Published in *Nature* (2026), doi:10.1038/s41586-026-10303-2. Seen at elasticity-ai/stylized-facts full text. [primary] [corrected by fact-check: arXiv author order and *Nature* publication added. The *Nature* author list and volume/pages (652:58–67, third-party) still need checking on nature.com.]

**Structure of capabilities**

44. Burnell, R., Hao, H., Conway, A. R. A., & Hernández-Orallo, J. (2023). Revealing the structure of language model capabilities. arXiv:2306.10062. Seen as full text. [primary]
45. Burnell, R., Schellaert, W., Burden, J., Ullman, T. D., Martínez-Plumed, F., Tenenbaum, J. B., et al. (2023). Rethink reporting of evaluation results in AI. *Science*, 380(6641), 136–138. Seen in the Desai bibliography. [bibliographic]
46. Ilić, D. (2023). Unveiling the general intelligence factor in language models: A psychometric approach. arXiv:2310.11616; Ilić, D., & Gignac, G. E. (2024). Evidence of interrelated cognitive-like capabilities in large language models: Indications of artificial general intelligence or achievement? *Intelligence*, 106, 101858. Seen in the Ruan and ADeLe bibliographies. [bibliographic] [fact-check note: these are two separate works. The refs JSON previously merged them under one key; it now has separate entries (ilic2023unveiling, ilic2024positive).]
47. Owen, D. (2024). How predictable is language model benchmark performance? arXiv:2401.04757. Seen as full text. [primary]
48. Ruan, Y., Maddison, C. J., & Hashimoto, T. (2024). Observational Scaling Laws and the Predictability of Language Model Performance. *NeurIPS 2024*. arXiv:2405.10938. Seen as full text and at ryoungj/ObsScaling. [primary]
49. Maia Polo, F., Somerstep, S., Choshen, L., Sun, Y., & Yurochkin, M. (2025). Sloth: scaling laws for LLM skills to predict multi-benchmark performance across families. *NeurIPS 2025*. arXiv:2412.06540. Seen as full text. [primary]
50. Zhang, G., Dominguez-Olmedo, R., & Hardt, M. (2025). Train-before-Test Harmonizes Language Model Rankings. arXiv:2507.05195. Seen as full text. [primary]
51. Perlitz, Y., Gera, A., Arviv, O., Yehudai, A., Bandel, E., Shnarch, E., Shmueli-Scheuer, M., & Choshen, L. [authors added by fact-check from arXiv listing mirrors] (2024). Benchmark Agreement Testing Done Right: A Guide for LLM Benchmark Evaluation. arXiv:2407.13696. Seen at The-AI-Alliance/trust-safety-evals, which links the paper and the IBM/benchbench repo. [bibliographic, title and ID only]
52. elasticity-ai/stylized-facts (2026). "The latent factor of LLM intelligence" (LLM-written literature summary, book chapter source). Seen at github.com/elasticity-ai/stylized-facts/blob/main/book/latent-factor-of-llm-intelligence.llm.qmd. [secondary; used only to locate primary sources and for flagged [L] items]

---

## Verification log

*Adversarial fact-check, 2026-09-29.* WebSearch was already exhausted for the session (200/200), and arXiv, Crossref, OpenAlex and DBLP were blocked (HTTP 403). Independent checks therefore used two routes:

- **GitHub code search**, across arXiv RSS/digest mirrors, author homepages, official repos and third-party BibTeX files.
- **Full texts re-read directly:** the paper-text mirrors (Ruan, Burnell, Zhang, Owen, Zhou/ADeLe, Sloth, BetterBench) and the Desai et al. PDF, which I extracted with pypdf myself.

Where I only re-read the source the original agent cited, I say so and give at least one additional independent source where one exists.

### Claim verdicts

| ID | Verdict | Evidence (what was checked) | Sources |
|---|---|---|---|
| C1 | **Confirmed** | Abstract ("29 expert reviewers … 445 LLM benchmarks … eight key recommendations") appears verbatim in ≥6 independent arXiv digests. The 42-author BibTeX was seen. The arXiv comment reads "39th NeurIPS 2025 Track on Datasets and Benchmarks". | github.com/microsoft/BC-Bench/blob/main/paper/bcbench.bib ; github.com/sailfish009/paper/blob/main/2025.11.04.txt ; github.com/advanced-cs/arXiv_daily (daily_papers/20251110_Mon/text.md) ; github.com/cemde/cemde.github.io (_publications/2025-measuring-what-matters.md) |
| C2 | **Confirmed** | Paper text: 46 practices; 24 benchmarks (16 FM + 8 non-FM); "14 out of 24 … did not perform multiple evaluations … or report statistical significance or uncertainty"; "17 out of 24 … do not provide easy-to-run scripts"; 4/24 partial; build status 3/24; MMLU weighted average 5.5 vs GPQA 11.0. The same quotes appear in an independent literature extraction. Nuance: retirement is excluded from scoring. | github.com/Lumysia/agi-benchmark-framework/blob/main/papers/BetterBench_Criteria.txt ; github.com/rasynai/MarigoldBench (analysis/literature/deep/betterbench.md) ; github.com/Luvata/arxive (pages/2024-11-21-cs-ai.html, abstract) |
| C3 | **Confirmed** | v3 text: "top 3 PCs explaining ∼97% of the variance … the first PC alone explains nearly 80%". PC-1 is linear in log-training FLOPs within families (R² > 0.9). Paper footer says NeurIPS 2024. Nuance: the PCA uses 77 base models from 21 families. | github.com/elasticity-ai/stylized-facts/blob/main/references/text/ruan2024observational.txt ; github.com/deep-diver/neurips2024 (spotlight On5WIN7xyD figure note) ; github.com/yibingwei-1/scaling-law-survey (SURVEY.en.md) |
| C4 | **Confirmed** | Text: 29 LLMs, HELM tasks (27 used), mean r = 0.56 (Med = 0.6); Table 2 gives 0.33 / 0.31 / 0.17, cumulative 0.82. Factor order is comprehension, language modelling, reasoning. EFA fit is poor (CFI 0.70). Abstract confirmed separately. | github.com/elasticity-ai/stylized-facts/blob/main/references/text/burnell2023reveal.txt ; github.com/qhduan/cn-chat-arxiv (papers/23/06/2306.10062.json) |
| C5 | **Confirmed** | Text: 61 models (six families) × 24 benchmarks; average Kendall τ 0.52 → 0.76; 274/276 pairs improve; PC1 70% → 86%, and 93% "only considering Qwen models". | github.com/elasticity-ai/stylized-facts/blob/main/references/text/zhang2025trainbeforetest.txt |
| C6 | **Confirmed** (with framing nuance) | PDF header "Published as a conference paper at COLM 2026". The paper reports 56 benchmarks and 53 models, with 48 analysed after excluding 4 saturated and 4 format-sensitive benchmarks. Reported values: β_format = 0.275 (p < 0.0001) and β_concept = 0.138 (p = 0.003); the binary LLM-judge coding gives β_concept = −0.058. Ethics, bias, privacy and unsafe-behaviour benchmarks correlate more with capability benchmarks than with each other. The authors' own framing of the format effect is "in some cases". Venue, authors and ID are confirmed by the first author's site and BibTeX. | afedercooper.github.io/paper/desai2026validity.pdf (via raw.githubusercontent.com) ; github.com/madesai22/meera-desai (bibs/desai-benchmarks-colm.txt, index.html) ; github.com/madesai22/what-ai-benchmarks-actually-measure |
| C7 | **Corrected** (venue precision) | The abstract finding ("highly correlate with both upstream model capabilities and training compute") and the three-step method (PC1 of capability benchmarks → Spearman "capabilities correlation") are confirmed. Venue correction: **NeurIPS 2024 Datasets and Benchmarks Track** (proceedings PDF filename). | github.com/centerforaisafety/safetywashing (README, analysis.py) ; github.com/justinphan3110cais/safetywashing_website (src/components/body/index.jsx) ; github.com/kevincoakley/the-shift-toward-open (paper_lists/excluded_papers/NeurIPS_2024.csv) ; github.com/Luvata/arxive (pages/2024-12-30-cs-cl.html) |
| C8 | **Confirmed** | The README table gives these MMLU errors: IRT 0.024 (0.017), p-IRT 0.016, gp-IRT 0.016. It also describes 100 examples per tiny dataset. The ICML 2024 venue is confirmed as PMLR v235. | github.com/felipemaiapolo/tinyBenchmarks (README.md) ; github.com/mlresearch/v235 (_posts/2024-07-08-maia-polo24a.md) ; github.com/borgr/paper-geo (tasks/arxiv_jref.md) |
| C9 | **Confirmed** | README: "<3% of its original size", "over 5000 LLMs", "<0.9% mean absolute error", "<0.5%". The README BibTeX gives ICLR 2025. The arXiv title differs from the ICLR title. | github.com/adkipnis/metabench (README.md) |
| C10 | **Confirmed** | The abstract appears verbatim in an independent arXiv mirror, including "higher validity and less variance on MMLU with fifty times fewer items" and "item response theory … increases validity, while dynamic item selection reduces variance". The official BibTeX says "Second Conference on Language Modeling" (COLM 2025). | github.com/t41372/DayDayArXiv (daydayarxiv_frontend/public/data/2025-09-14/cs.AI.json) ; github.com/allenai/fluid-benchmarking (README.md) ; github.com/AkihikoWatanabe/paper_notes (agent_docs/COLM.xml) |
| C11 | **Corrected** (publication status and author order; the numbers are confirmed) | arXiv v2 text reports 18 rubrics; 16,108 instances; 63 tasks from 20 benchmarks; 289,944 annotations; 15 LLMs; best AUROC 0.88 (GPT-4o); rWG averaging 0.86. The "populational … lead to different results … whenever a new set of LLMs are added" quote and the "lack either specificity or sensitivity" quote are verbatim. **Update:** the paper is now published in *Nature* 2026 (doi:10.1038/s41586-026-10303-2), according to the first author's repo. The author order was fixed from an arXiv listing. | github.com/elasticity-ai/stylized-facts/blob/main/references/text/zhou2025generalscales.txt ; github.com/lexzhou/ADeLe-practical-session (README.md) ; github.com/CSQianDong/Awesome-arXiv-Daily-Reporter (11-Mar-2025/NLP/README.md) ; github.com/latere-ai/ai-as-an-infrastructure (refs/the-capability-horizon.bib, vol/pages [M]) |
| C12 | **Confirmed** (abstract level only) | The abstract is identical in three independent arXiv mirrors. It says latent-factor capabilities "often proxy model size", and structured capabilities "outperform latent factor models on parsimonious fit indices, and exhibit better out-of-distribution benchmark prediction than scaling laws" on OpenLLM Leaderboard data. The work is a thesis and not peer-reviewed. | github.com/Barca0412/Introduction-to-Quantitative-Finance (data/papers/2026-02-18.json) ; github.com/CSQianDong/Awesome-arXiv-Daily-Reporter (18-Feb-2026/AI/README.md) ; github.com/sailfish009/paper (2026.02.18.txt) |
| C13 | **Confirmed** | The official README gives `performance = sigmoid(discriminability * (capability - difficulty))` and anchors "(Claude 3.5 Sonnet = 130, GPT-5 = 150)" with bootstrap CIs. Authors and title are confirmed by the README BibTeX and an arXiv listing (2025-12-02). The dossier's "unidimensionality … not tested" is interpretation and is unverified. | github.com/epoch-research/eci-public (README.md) ; github.com/epoch-research/benchmark-stitching ; github.com/sailfish009/paper (2025.12.02.txt) |
| C14 | **Confirmed** | Owen abstract: "extrapolating BIG-Bench Hard performance across one order of magnitude in compute, we observe average absolute errors of 6 percentage points (pp) … individual BIG-Bench tasks … 18pp". The body gives other horizons: 3.9 pp across a doubling for BBH, and 17 pp at 0.67 OOM for single tasks. An LLM-written secondary table conflates these, but the dossier's figures are correct. | github.com/elasticity-ai/stylized-facts/blob/main/references/text/owen2024predictable.txt (abstract, lines 10–16) |

**Totals:** 12 confirmed, 2 corrected (C7, C11), 0 refuted, 0 unverifiable.

### Other corrections made in this dossier (outside C1–C14)

1. "Desai et al. is **the first** large-scale application …" was softened to "a large-scale application". The paper makes no priority claim, and Safetywashing predates it.
2. Raji et al. (2021) has a different author order in the NeurIPS D&B proceedings (Raji, Denton, Bender, Hanna, Paullada) than on arXiv.
3. Signal and Noise (Heineman et al.) is a **NeurIPS 2025** paper, not just arXiv.
4. Zhuang et al.'s ICML 2025 position-paper version is confirmed (it was [M] before). Its ICML author list may differ from the arXiv list.
5. Growing Pains: full 8-author list added. benchbench (Perlitz et al.) authors added.
6. Ilić (2023, arXiv:2310.11616) and Ilić & Gignac (2024, *Intelligence*) were conflated in one JSON entry; they are now split. Ruan's 85% figure belongs to the 2023 arXiv paper.
7. Burnell factor labels are now attached from the paper text (comprehension 33%, LM 31%, reasoning 17%), with a note on poor EFA fit.
8. Ruan's PCA is on 77 base models (21 families), not ~100.
9. "Kearns (2026) shows" was softened to "argues (thesis, not peer-reviewed)".
10. Bean et al.'s 16% statistical-testing figure is now corroborated by two further independent secondary sources ([M]). It is still not checked against the PDF.
11. Hutchinson et al. pages (1859–1876) were added. metabench's arXiv title differs from its ICLR title.

### Reference check summary (refs/metascience_validity.json)

- **Entries:** 49 original. All 49 were checked; none skipped. Four entries that the dossier cited but the JSON lacked were added: ilic2023unveiling, messick1989meaning, blodgett2021salmon and subramonian2023tango. Each was seen in the Ruan or Desai bibliographies.
- **Verified:** 53/53 (`verified: true`). No fabricated reference was found: every title, author list, year and ID resolved to a real work.
- **Problems found and fixed:**
  - One conflated entry (Ilić).
  - Two venues missing their precision or peer-reviewed version (Safetywashing D&B track; Signal and Noise NeurIPS 2025).
  - One publication-status update (ADeLe → *Nature* 2026).
  - Two incomplete author lists (Growing Pains; benchbench).
  - One author-order ambiguity (Raji et al.).
  - One title variant (metabench).
  - One upgraded venue (Zhuang ICML 2025).
- **Residual caveats:**
  - Some DOIs and page ranges were carried from the original agent's sources and not re-seen independently. Each such case is noted in `verify_note`: Cronbach DOI, Campbell & Fiske end page, Vania pages, Ethayarajh and Hutchinson arXiv IDs, Jacobs & Wallach exact pages.
  - The ADeLe *Nature* volume and pages are from third-party bibs only [M].

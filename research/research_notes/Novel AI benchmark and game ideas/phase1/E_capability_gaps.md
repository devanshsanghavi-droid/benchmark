# Panel E: Capability gaps. Human advantages over frontier AI, inter-model divergence, and under-measured abilities (as of 30 Sep 2026)

**Scope and method.** Evidence is current to 30 Sep 2026. Access was restricted: arxiv.org, metr.org, epoch.ai, arcprize.org, openreview.net, huggingface.co and simple-bench.com all returned EGRESS_BLOCKED. Primary pages I read directly are GitHub READMEs and data (via raw.githubusercontent.com) and anthropic.com. For papers on blocked hosts I saw the primary URL plus a search-engine summary of it, not the full text.

**Web budget.** About 39 searches. Five fetch attempts, all blocked.

**Lead files.** The in-repo dossiers dated 2026-09-29 were used as leads only. Nothing in this note is cited to them.

**Confidence labels.**
- **H**: I read the primary source this session (paper repo, official page, raw data).
- **M**: I saw the primary URL, but only through a search-engine summary; or I saw one consistent secondary source.
- **L**: aggregator only, or unclear provenance.
- **[C]**: a number I computed this session from primary public data.
- **[speculation]**: marks my own conjecture.

---

## Summary

1. **The robust human advantages are perceptual and interactive, not verbal-abstract.**
   - Core vision (BabyVision, Jan 2026): the best model scores 49.7% against 94.1% for adults.
   - Intuitive physics (IntPhys 2, Jun 2025): models are near chance (≤57.5%) against 96.4% for humans. [corrected by fact-check: was "≤55.6%"; the best model overall is V-JEPA 2 at 57.51%, and Gemini 2.5 Flash's 55.63% is only the best MLLM; source: arXiv 2506.09849 results table, via search excerpts]
   - Mental spatial transformation: GPT-5 was still short in Aug 2025.
   - Reward-free world-model learning (AutumnBench, Oct 2025): 517 humans beat o3, Gemini 2.5 Pro and Claude 4 Sonnet.
   - The physics and exploration results predate 2026 models.
2. **Static few-shot abstraction is no longer a human moat on accuracy.**
   - ARC-AGI-2 rose from 54.2% verified (GPT-5.2 Pro, Dec 2025) to 95.0% verified (GPT-6 Astra, Sep 2026, per ARC Prize as reported secondhand). [corrected by fact-check: was "to 95%+ with harnesses"; Imbue's 95.1% harness result is on the *public* eval set, which is not comparable with verified semi-private scores; sources: ARC Prize X post / arcprize.org/results/openai-gpt-6-astra (via search), imbue.com (via search)]
   - o3 matches humans (73%) on text ConceptARC.
   - The gaps that remain: about 27% of o3's correct answers use unintended or wrong rules (about 8% for humans), and accuracy drops sharply on visual inputs. [corrected by fact-check: was "about 28%"; the paper's abstract says "around 27%"; source: arXiv 2510.02125, via search excerpts]
3. **Interactive skill acquisition is fragile as a human advantage.**
   - ARC-AGI-3 launched on 25 Mar 2026 with every frontier model below 1% against 100% for humans.
   - By 3 Sep 2026, GPT-6 Astra scored 62.7% on the standard harness (max effort) and 99.9% on a state-preserving harness (high effort). At matched max effort the two harnesses give 62.7% vs 98.6%. [clarified by fact-check; source: translation of arcprize.org/blog/astra]
   - Under the state-preserving (Provider Adapter) harness, it used fewer actions than the median human on 96.0% of levels.
4. **Classic "reasoning vs reciting" deficits shrink with reasoning models, and the evidence is stale.** This covers counterfactual tasks, embers of autoregression, GSM-NoOp, MATH-P-Hard and Mystery Blocksworld.
   - The newest models tested are o1, o1-mini, R1 and Gemini-2.0-thinking (≤ early 2025).
   - GSM-NoOp: −17.5% for o1-preview against up to −65.7% for the worst model.
   - Mystery Blocksworld: 52.8% for o1-preview and 43.3% for R1.
   - ToM perturbation fragility is GPT-3.5-era; a 2026 paper finds reasoning models robust.
5. **Long-horizon reliability is a robust structural gap.**
   - In METR's public data [C], the 80% horizon is 4–10× shorter than the 50% horizon for every model; for Opus 4.6 it is 12.0 h against 70 min. (Re-run by fact-check with METR's own pipeline settings; reproduced. METR first announced 14.5 h for Opus 4.6 on 20 Feb 2026 and corrected it to 11 h 59 min about 3 Mar 2026.)
   - Mythos Preview: p50 ≥ 16 h and p80 about 3.1 h.
   - METR's suite is running out of long tasks.
6. **Learning from new context or from experience is weak in 2026 frontier models.**
   - CL-bench: the best model reaches 23.7% and the average is 17.2%.
   - Continual Learning Bench: agents don't reuse knowledge across episodes, and memory systems don't beat naive in-context learning.
   - Neither benchmark has a human baseline.
7. **Metacognition and abstention are robust deficits and diverge strongly by lab.**
   - Reasoning fine-tuning cuts abstention by about 24%.
   - AA-Omniscience hallucination rates: 88% for Gemini 3 Pro against 48% for Claude 4.5 Sonnet.
   - Claude refused up to 70% of hallucination-eval items in the Anthropic–OpenAI pilot.
8. **The general factor dominates but is not total.**
   - PC1 explains about 79% of variance on a 96-configuration complete-case grid (12 benchmarks) drawn from 421 AA model configurations [H data]. [corrected by fact-check: was "across 421 AA model configurations"; the PCA and factor analysis ran on the n = 96 complete-case grid; source: repo PHASE2_REPORT.md and notebook] Epoch finds cross-domain r = 0.68 against within-domain r = 0.79. On Epoch's broader 39-benchmark set, PC1 captures only about half the variance.
   - A second axis separates **agentic** strength from **math and vision** (Epoch's "Claudiness", Nov 2025). [corrected by fact-check: was "A replicated second axis … (Epoch's 'Claudiness'; the Aug 2026 AA factor analysis)". The AA-data study finds an agentic-vs-academic split only when 3 factors are forced. Its own parallel analysis retains 1 factor, and its battery has no vision or math benchmarks. So it is at most partial support, not a replication. Source: louisyzhu/frontier-ai-economic-validity PHASE2_REPORT.md]
9. **Vision is the largest lab reordering found.** BabyVision scores: Gemini 3 Pro 49.7, GPT-5.2 34.4, Claude 4.5 Opus 14.2. (Verified. These are Jan 2026 models; no re-test of the Sep 2026 frontier was found.)
10. **The general factor is partly a release-date trend** (R² ≈ 0.48–0.51). Its share fell from 92% to 64% on one small battery when reasoning models arrived.
11. **Headline margins no longer track real-world differences.**
    - Anthropic's Opus 5.5 post (22 Sep 2026) says so.
    - Vendor grids reorder Opus 5.5 and GPT-6 Astra by benchmark.
    - METR's RCT found a 19% slowdown with early-2025 tools, and its 2026 follow-up was confounded by selection.
12. **Best under-measured targets, each with a documented deficit and cheap procedural generation:**
    - (i) calibrated abstention;
    - (ii) cross-episode learning on generated latent rule systems;
    - (iii) exploration efficiency;
    - (iv) procedurally generated core vision and intuitive physics;
    - (v) p80/p95 long-chain execution.

---

## Q1. Which human advantages are robust, and which are fragile?

### Takeaway
Human advantages that survive 2025–26 reasoning models are in non-verbal perception (vision, intuitive physics, mental spatial transformation), in efficient active exploration and world-model learning, and in reliability over long task chains. Text-based abstraction, analogy, ToM vignettes and perturbed math have mostly been closed or shrunk by test-time compute. Evidence on several classic deficits is stale: it was last measured on o1 or R1-era models.

### Human-advantage map

Status definitions:
- **Robust**: a large gap persists in the most recent models tested.
- **Fragile**: the gap shrank sharply with reasoning or test-time compute, or was closed by at least one model or harness.
- **Closed**: the frontier is at or above the human baseline.
- **Stale**: no model newer than early 2025 has been tested.

| Ability | Key evidence | Latest models tested (date) | Status | Conf. |
|---|---|---|---|---|
| Core visual perception (discrimination, tracking, spatial perception, visual patterns) | BabyVision, 388 items: adults 94.1%, best model 49.7%. Most models are below 3-year-olds; Gemini 3 Pro Preview trails 6-year-olds by about 20 points | Gemini 3 Pro Preview, GPT-5.2, Claude 4.5 Opus (Jan 2026; ICML 2026) | **Robust** | H (README); M (child comparison) |
| Intuitive physics (possible vs impossible video) | IntPhys 2: humans 96.44% (92.44% on held-out); best model V-JEPA 2 57.51%; best MLLM Gemini 2.5 Flash 55.63%; chance is 50% [corrected by fact-check: was "best model 55.63% (Gemini 2.5 Flash)"; source: arXiv 2506.09849 results table, via search excerpts] | Gemini 2.5 Flash, V-JEPA 2 and other video models (Jun 2025) | **Robust but stale for 2026** | M |
| Spatial reasoning (mental transformation) | GPT-5 is human-level on metric measurement and spatial relations, short on mental reconstruction and deformation/assembly. Spatial4D-Bench: humans about 17 points above GPT-5 | GPT-5 (Aug 2025); Spatial4D (Jan 2026) | **Robust for transformation subskills; closed for measurement and relations** | M |
| World-model learning via reward-free exploration | AutumnBench/WorldTest (43 environments, 129 tasks, 517 humans): humans beat o3, Gemini 2.5 Pro and Claude 4 Sonnet. More compute helps in only some environments | o3, Gemini 2.5 Pro, Claude 4 Sonnet (Oct 2025) | **Robust in 2025; untested on 2026 models** | M |
| Interactive skill acquisition, novel games (ARC-AGI-3) | Launch: all frontier <1% (best 0.37%, Gemini 3.1 Pro). Humans solve 100% of environments, but that is a panel figure: each environment was solved by at least 2 participants. Mid-2026: best 7.78% (GPT-5.6 Sol), then Claude Opus 5 at 30.16%. 3 Sep 2026: GPT-6 Astra 62.7% standard (max effort) / 99.9% Provider Adapter (high effort); 98.6% Provider Adapter at max effort. Under the Provider Adapter, fewer actions than the median human on 96.0% of levels [clarified by fact-check; sources: translation of arcprize.org/blog/astra; Opus 5 system card as cited in sibling dossier F] | GPT-6 Astra (Sep 2026) | **Fragile / closing (harness-dependent)** | M |
| Active causal learning (blicket-style interventions) | Some SOTA LLMs near human hypothesis-inference accuracy but explore less efficiently; same conjunctive-disjunctive gap | Unspecified "state-of-the-art" LLMs (CogSci 2026) | **Accuracy fragile; exploration efficiency robust** | M/L |
| Static few-shot abstraction (ARC-AGI-1/2) | ARC-AGI-2: GPT-5.2 Pro 54.2% verified (Dec 2025). Imbue harness took Gemini 3.1 Pro from 88.1% to 95.1% (Feb 2026) on the *public* eval set [corrected by fact-check: the public-eval status was not stated; source: imbue.com post, via search excerpts]. 97.9% claimed on the public eval. GPT-6 Astra 95.0% verified (Sep 2026; secondary, via ARC Prize X post) | Gemini 3.1 Pro + harness (Feb 2026); others 2026 | **Closed on accuracy** (efficiency and priors not separately established) | M |
| Concept abstraction with the right rule, across modalities (ConceptARC) | o3 (medium) matches or beats human accuracy (73%) in text, but about 27% of its correct grids use "correct-unintended" or incorrect rules, against about 8% for humans [corrected by fact-check: was "about 28%"; source: arXiv 2510.02125 abstract, via search]. Visual-modality accuracy drops sharply | o3 (Oct 2025) | **Accuracy closed (text); rule fidelity and visual abstraction robust** | M |
| Analogy with counterfactual alphabets | Humans 75.3% vs GPT-4 45.2% zero-shot (136 humans). Webb et al. rebut: GPT-4 with code execution solves the counterfactual variants | GPT-4 (2024) | **Stale** (no reasoning-model test found) | M/L |
| Counterfactual task variants ("reasoning or reciting") | Consistent degradation on counterfactual variants across 11 task families | GPT-4, Claude, PaLM (2023) | **Stale** | M |
| Embers of autoregression (sensitivity to output probability) | o1 improves greatly, especially on rare task variants, but "still displays the same qualitative trends" | o1 (Oct 2024) | **Fragile / stale** | M |
| Perturbation robustness in math | GSM-NoOp: drops up to −65.7%; o1-preview −17.5%, o1-mini −29.1%. MATH-P-Hard: o1-mini −16.49%, Gemini-2.0-flash-thinking −12.9%; about 40% of o1-mini's errors blindly reuse the original technique | o1-mini, Gemini 2.0 Flash Thinking (early 2025) | **Fragile / stale** | M |
| Planning in obfuscated domains | Mystery Blocksworld: o1-preview 52.8%, R1 43.3% (non-reasoning LLMs ≈0%). Randomized Mystery: 37.3% and 25.8% | DeepSeek R1 (Jan 2025) | **Fragile / stale** | H |
| Planning at scale ("Illusion of Thinking") | Accuracy collapses past a complexity threshold. Rebuttal: many failures are output-token limits or unsolvable instances. Replication: failures are partly cognitive (about 8 disks in Tower of Hanoi) | Mid-2025 LRMs (e.g. Claude 3.7 Thinking, R1; list not re-verified) | **Contested; stale** | M |
| Theory of mind under trivial alterations | Ullman (2023): GPT-3.5 fails trivial alterations. 2026: reasoning models are "consistently" more robust to prompt and task perturbations; the authors attribute this to general robustness, not a new ToM capability. [uncertain: a Feb 2026 study (arXiv 2602.22072) still finds failures on some perturbation classes and finds that CoT hurts some; its model list was not checked, so "largely closed" may overstate] | Reasoning models (Aug 2026 preprint; accepted at Discovery Science 2026) | **Largely closed (text vignettes)** | M/L |
| Implicit world models | Orbit-trained transformers predict trajectories but recover a "nonsensical" force law | Mostly purpose-trained transformers (ICML 2025) | **Robust for sequence models; untested for frontier agents** | M |
| Everyday trick and common-sense questions (SimpleBench) | Human baseline 83.7% (n = 9). Claude Opus 5.5 is reported at 88.4% (22 Sep 2026) [uncertain: not verified — aggregator only; simple-bench.com blocked; the last official figure found (Jun 2026, via sibling dossier A) was Claude Fable 5 at 81.9%, just below humans] | Claude Opus 5.5 (Sep 2026) | **Closed or at parity within noise** (per aggregators) | L/M |
| Long-horizon reliability | p80 is 4–10× shorter than p50 [C; reproduced by fact-check]. Public frontier p80 was about 1.5 h in Feb–Mar 2026; Mythos Preview p50 ≥ 16 h and p80 about 3.1 h | Opus 4.6, GPT-5.3-Codex (public data); Mythos Preview (Mar–May 2026) | **Robust gap in reliability (not in reach)** | H (data) / M |
| Learning from new context and from experience | CL-bench: average 17.2%, best 23.7%. Continual Learning Bench: no reuse across episodes; memory systems do not help | GPT-5.1 and 9 other frontier models (Feb 2026); frontier agents (Jun 2026) | **Robust deficit (no human baseline)** | M (scores); H (design) |
| Metacognition, calibration and abstention | Reasoning fine-tuning cuts abstention about 24% (measured on reasoning-vs-base pairs such as DeepSeek R1-Distill-Llama-70B and s1); scale "almost no effect"; 48 LLMs (newest o1-preview) overconfident on clinical questions; AA-Omniscience hallucination 48–88% for the Nov 2025–Jan 2026 models (the 36% low end is an aggregator figure for Opus 4.8 [uncertain: not verified]) | 20 LLMs incl. R1-distills (Jun 2025); Gemini 3 and Claude 4.5–4.8 (Nov 2025–2026) | **Robust deficit; human comparison ambiguous** | H/M |
| Few-shot concept learning and compositional generalization (Lake 2017; Lake & Baroni 2023) | Not re-verified this session | — | **Unknown for 2025–26** | — |

### Cited Findings

Numbers already given in the map above are not repeated here. Each bullet names the source for the corresponding map row.

**Perception and physics**
- BabyVision uses child comparison groups aged 3, 6, 10 and 12, plus adults. The four domains are fine-grained discrimination, visual tracking, spatial perception and visual pattern recognition. Deficits are "consistent … across all four domains" — [README](https://raw.githubusercontent.com/UniPat-AI/BabyVision/main/README.md) (H); [arXiv 2601.06521](https://arxiv.org/abs/2601.06521) (M).
- IntPhys 2 uses photorealistic Unreal scenes with moving cameras. MLLMs are sensitive to prompt phrasing and use long video poorly — [arXiv 2506.09849](https://arxiv.org/abs/2506.09849) (M).
- Spatial reasoning sources: [Cai et al., arXiv 2508.13142](https://arxiv.org/pdf/2508.13142); [Spatial4D-Bench, arXiv 2601.00092](https://arxiv.org/pdf/2601.00092) (M).

**Exploration and interactive learning**
- AutumnBench task families are masked-frame prediction, planning and change-of-dynamics prediction. The authors attribute the human edge to "strategic experimental design, better uncertainty quantification, and flexible belief updating" — [Warrier et al., arXiv 2510.19788](https://arxiv.org/abs/2510.19788) (M).
- ARC-AGI-3 launch results — [ARC Prize](https://arcprize.org/blog/arc-agi-3-launch); [arXiv 2603.24621](https://arxiv.org/abs/2603.24621) (M).
- The two ARC-AGI-3 harnesses differ as follows (secondary sources agree on 62.7 and 99.9):
  - The standard harness carries forward only the notes the model chooses to keep.
  - The Provider Adapter harness "preserves opaque reasoning state between requests and uses compaction".
  - Source: [ARC Prize, Astra post](https://arcprize.org/blog/astra) (M).
- Blicket study: active exploration improves adults' conjunctive inference. LLMs "approach human-level performance on hypothesis inference accuracy" but "exhibit less efficient exploration strategies" — [arXiv 2606.06464](https://arxiv.org/abs/2606.06464) (M).
- LM agents show a disjunctive bias like adults' — search summary of related work, e.g. [arXiv 2604.20039](https://arxiv.org/abs/2604.20039) (L; attribution uncertain).

**Abstraction and analogy**
- ARC-AGI-2 scores:
  - GPT-5.2 Pro 54.2% at the start of 2026 — [Metaculus](https://www.metaculus.com/questions/41131/top-arc-agi-2-score-in-2026/) (L/M).
  - Imbue harness result — [Imbue](https://imbue.com/blog/2026-02-27-arc-agi-2-evolution) (M).
  - Confluence Lab's 97.9% is on the public set, which is not comparable to semi-private results (L).
- ConceptARC text, visual and rule-quality results — [Beger, …, Mitchell, arXiv 2510.02125](https://arxiv.org/abs/2510.02125) (M).
- Counterfactual analogies: human CI [73.4, 77.3]; GPT-3 48.8% and GPT-3.5 35.0% — [Lewis & Mitchell, CogSci](https://escholarship.org/uc/item/58d9s666) (M/L).
- Webb et al.'s rebuttal — [arXiv 2404.13070](https://arxiv.org/abs/2404.13070) (M).

**Reasoning versus reciting**
- GSM-Symbolic and GSM-NoOp results — [Mirzadeh et al., ICLR 2025](https://arxiv.org/abs/2410.05229) (M). The template design (50 instances per template; P1 and P2 variants) is confirmed in the [repo](https://raw.githubusercontent.com/apple/ml-gsm-symbolic/main/README.md) (H).
- MATH-Perturb uses 279 perturbed level-5 MATH problems — [Huang et al., ICML 2025](https://proceedings.mlr.press/v267/huang25k.html) (M).
- Embers of autoregression:
  - The o1 follow-up tests shift ciphers, Pig Latin, article swapping and reversal — [McCoy et al., arXiv 2410.01792](https://arxiv.org/abs/2410.01792) (M).
  - The original study — [PNAS 2024 PDF](https://cocosci.princeton.edu/papers/mccoy2024embers.pdf).
- "Reasoning or Reciting" task families: arithmetic, programming execution and generation, syntax, spatial, drawing, music chords and melodies, chess, SET and logic — [repo](https://raw.githubusercontent.com/ZhaofengWu/counterfactual-evaluation/master/README.md) (H); [arXiv 2307.02477](https://arxiv.org/abs/2307.02477).
- PlanBench: non-reasoning models score ≈0% on Mystery Blocksworld (Claude 3.5 Sonnet 0%, GPT-4o 0%). On Blocksworld Hard (PDDL), R1 scores 53.6% and o1-preview 23.65% — [README](https://raw.githubusercontent.com/karthikv792/LLMs-Planning/main/README.md) (H).
- "Illusion of Thinking" debate — [original, arXiv 2506.06941](https://arxiv.org/abs/2506.06941); [Lawsen rebuttal, arXiv 2506.09250](https://arxiv.org/abs/2506.09250); [replication, arXiv 2507.01231](https://arxiv.org/abs/2507.01231) (M).
- Theory of mind — [arXiv 2608.04646](https://arxiv.org/html/2608.04646) (M/L).
- World models — [Vafa et al., ICML 2025](https://proceedings.mlr.press/v267/vafa25a.html) (M).

**Long horizons, learning, metacognition**
- METR sources:
  - Frontier risk report — [METR, 19 May 2026](https://metr.org/blog/2026-05-19-frontier-risk-report/) (M).
  - Mythos result — [METR on X](https://x.com/METR_Evals/status/2052896621760004602) (M).
  - p80 values — [time-horizons page](https://metr.org/time-horizons/) (M).
- [C] Refit of METR's TH1.1 public runs: 24,008 lines covering 20 models, using METR's weighted logistic on log2 human-minutes with invsqrt task weights.

| Model | p50 (min) | p80 (min) |
|---|---|---|
| Opus 4.6 | 718.9 | 69.9 |
| GPT-5.3-Codex | 349.5 | 54.7 |
| GPT-5.2 | 352.2 | 66.0 |
| Opus 4.5 | 293.0 | 49.4 |
| Gemini 3 Pro | 224.3 | 54.1 |
| GPT-5 | 203.0 | 38.3 |

  - The p50/p80 ratio spans 4.0–10.3 across all 20 models.
  - Opus 4.6 has the flattest slope of the 20 (−0.41 per log2 minute, against −0.47 to −0.69 for the rest).
  - The Opus 4.6 values match METR's published ~12 h and ~70 min.
  - Data: [runs.jsonl](https://raw.githubusercontent.com/METR/eval-analysis-public/main/reports/time-horizon-1-1/data/raw/runs.jsonl) (H).
- Self-conditioning on own errors is "not mitigated by scaling model size"; RL-trained thinking models do not self-condition — [Sinha et al., arXiv 2509.09677](https://arxiv.org/abs/2509.09677) (M).
- CL-bench:
  - Design: 1,899 tasks, about 63 rubrics and about 20 expert-hours per context, GPT-5.1 judge — [README](https://raw.githubusercontent.com/Tencent-Hunyuan/CL-bench/main/README.md) (H).
  - Scores — [arXiv 2602.03587](https://arxiv.org/abs/2602.03587) (M).
- Continual Learning Bench (UC Berkeley and Snorkel; six domains, each with a latent structure learnable across episodes): "naive ICL outperforms systems dedicated to memory management" — [arXiv 2606.05661](https://arxiv.org/abs/2606.05661) (M); [README](https://raw.githubusercontent.com/pgasawa/continual-learning-bench/main/README.md) (H).
- AbstentionBench (20 datasets, 6 scenarios, 20 LLMs):
  - "Reasoning fine-tuning hurts abstention"; scale has "almost no effect" — [README](https://raw.githubusercontent.com/facebookresearch/AbstentionBench/main/README.md) (H).
  - −24% on average — [arXiv 2506.09038](https://arxiv.org/abs/2506.09038) (M).
- Clinical calibration: 48 LLMs on 300 gastroenterology questions. Even o1-preview, GPT-4o and Claude 3.5 Sonnet are substantially overconfident — [Nature Portfolio s44355-026-00053-3](https://www.nature.com/articles/s44355-026-00053-3) (M).
- SimpleBench:
  - Human baseline 83.7% (n = 9) — [explainer](https://itdoeswhatnow.com/benchmarks/simplebench/) (M).
  - Opus 5.5 at 88.4% and Fable 5.1 at 86.6% — [benchmarklist](https://benchmarklist.com/benchmarks/simplebench/) (L; the official site was blocked).

### Inferences
- The pattern fits **"verbal-symbolic gaps close; embodied-perceptual and exploration-efficiency gaps persist."**
  - Every text-only deficit with a 2025–26 test (ConceptARC-text, ToM perturbations, SimpleBench, ARC-AGI-2) has closed or nearly closed.
  - The perception, physics and spatial-transformation gaps remain large in the newest models tested.
- **Efficiency is more robust than accuracy.**
  - ARC-AGI-3 accuracy closed within about 6 months, and even action-efficiency is claimed for Astra.
  - The blicket and AutumnBench results show gaps in *how many experiments* are needed even where accuracy converges.
  - [speculation] Exploration efficiency measured as information gain per action, not success, may be the more durable human advantage.
- **Harness sensitivity is part of the construct.** The same model scores 62.7% or 99.9% on ARC-AGI-3 depending on memory handling. So any "learning" benchmark measures a model-plus-memory system unless state carry-over is fixed by protocol.
- **Right answer, wrong rule** (about 28% on ConceptARC for o3) is under-measured: accuracy-only scoring hides it.
- Several famous deficits are **stale**: Wu et al., Lewis & Mitchell, embers, GSM-NoOp, Mystery Blocksworld and "Illusion of Thinking" have no published 2026-frontier re-test that I found. [speculation] Given the ARC and SimpleBench trajectories, most have probably shrunk further. A benchmark built on them should re-baseline first.

### Gaps
- No 2026-model results found for IntPhys 2, AutumnBench, Mystery Blocksworld, GSM-NoOp, Wu-style counterfactuals, Lewis–Mitchell analogies or embers-style probability sensitivity.
- No human baselines exist for CL-bench or Continual Learning Bench, so "learning from experience" cannot yet be stated as a human-versus-AI gap. It is a documented deficit against the task ceiling.
- Few-shot concept learning and compositional generalization (Lake et al. 2017; Lake & Baroni 2023) were not re-verified this session, and no 2025–26 frontier result was found.
- The ARC-AGI-3 human-efficiency comparison (96% of levels) was seen only via summary. It was unclear which harness it applies to.
- The SimpleBench "closed" verdict rests on aggregators, and the human baseline is n = 9.

---

## Q2. Where do frontier models differ most from each other?

### Takeaway
About 75–80% of benchmark variance is one general factor, and part of it is a release-date trend. The reliable residual concentrates on:
- an **agentic vs academic/vision/math axis** (Epoch's "Claudiness", replicated in Aug 2026 Artificial Analysis data);
- **vision and perception**: a 3.5× spread on BabyVision among frontier labs;
- **hallucination and abstention policy**, which differs by lab and even inversely with accuracy.

Output diversity is where models are most *alike*: the "Artificial Hivemind" effect.

### Model-divergence map

| Ability | Evidence of spread or reordering beyond general capability | Conf. |
|---|---|---|
| **General factor (baseline)** | AA data (421 configurations × 12 benchmarks, Aug 2026): PC1 79.4%; factor 1 74.5% of common variance; mean inter-benchmark Spearman 0.79; parallel analysis retains 1 factor. Epoch: cross-domain r 0.68 vs within-domain 0.79. Krakauer: PC1 fell from 92% to 64% on a 4-benchmark battery once reasoning models arrived | H (data); M |
| **Agentic vs academic/math/vision** | Epoch's PC2 ("Claudiness") is "good at agentic tasks but bad at vision and math"; Claude models score highest. In the AA-data 3-factor oblique solution, F1 is agentic/economic and F2 is academic/IF/long-context (see Cited Findings) | M; H (data) |
| **Vision / core perception** | BabyVision: Gemini 3 Pro 49.7 vs GPT-5.2 34.4 vs Claude 4.5 Opus 14.2 among models of broadly similar general capability. This is the largest lab reordering found | H |
| **Hallucination and abstention** | AA-Omniscience hallucination rate: Gemini 3 Pro Preview 88%, Gemini 3 Flash 85%, Claude Opus 4.5 58%, Claude 4.5 Sonnet 48%. The highest-accuracy models (GPT-5, Gemini 2.5 Pro) do not lead the index. Anthropic–OpenAI pilot: Claude refuses up to 70%; o3 gives more than twice as many correct answers but hallucinates more | M |
| **Coding–reasoning coupling** | 34 models from 10 labs: capabilities co-vary (r = +0.72), but per-lab coupling slopes differ 5× (Google 1.15 vs DeepSeek 0.23). HLE and instruction-following keep their spread as SWE-bench saturates | M (built on 2 benchmarks only) |
| **Frontier head-to-head reordering (Sep 2026)** | Vendor grid in the Opus 5.5 post: the Opus 5.5 vs GPT-6 Astra lead flips from one benchmark to the next (see Cited Findings) | H (vendor-reported) |
| **Output diversity / creativity** | Artificial Hivemind: strong intra- and inter-model homogeneity across more than 70 models. In 79% of cases a model's own responses to one prompt have average pairwise similarity above 0.8. This is low divergence, a shared weakness | M |
| **Economic / knowledge-work tasks** | No distinct factor. They add incremental prediction under linear learners (the advantage reverses under tree learners) | M; H (data) |
| **Sycophancy, persuasion** | No quantitative cross-lab comparison found this session | — |

### Cited Findings
- Epoch's second principal component:
  - It is "good at agentic tasks but bad at vision and math", and Claude models score highest on it.
  - It is defined by positive weights on The Agent Company, OSUniverse, OSWorld and the Factorio Learning Environment.
  - PC1 captures about half the variance of Epoch's 39-benchmark dataset.
  - Source: [Epoch, "Benchmark Scores = General Capability + Claudiness"](https://epoch.ai/gradient-updates/benchmark-scores-general-capability-claudiness) (M; Nov 2025).
- Benchmark scores are "nearly as correlated across domains (0.68) as within them (0.79)" — [Epoch data insight](https://epoch.ai/data-insights/benchmark-correlations) (M; date not verified, c. early 2026).
- Zhu, "One Capability or Many?" (arXiv 2608.29420, Aug 2026): 421 model configurations, 12 benchmarks (4 economic). "A single factor explains 74.5% of common variance and tracks model release date (R² = 0.505)." Economic benchmarks form no distinct factor but "add incremental predictive information" — [arXiv 2608.29420](https://arxiv.org/abs/2608.29420) (M).
  - The repository's result file gives PC1 share 0.794, factor-1 communal share 0.745, parallel-analysis k = 1, dominant-factor date R² = 0.477 (the abstract says 0.505, perhaps a different specification), and mean off-diagonal Spearman 0.79 — [task1_structure_results.json](https://raw.githubusercontent.com/louisyzhu/frontier-ai-economic-validity/main/data/processed/task1_structure_results.json) (H).
  - Three-factor oblique loadings (raw) — [loadings_raw.csv](https://raw.githubusercontent.com/louisyzhu/frontier-ai-economic-validity/main/data/processed/loadings_raw.csv) (H):

| Factor | Benchmark loadings |
|---|---|
| F1 (agentic / economic) | Terminal-Bench v2.1 1.05, GDPval 0.87, Terminal-Bench Hard 0.81, τ²-Bench 0.71, τ³-Banking 0.57, AA-Omniscience 0.56 |
| F2 (academic / IF / long context) | GPQA 0.97, IFBench 0.90, AA-LCR 0.73, SciCode 0.69 |
| F3 (frontier physics research) | CritPt 0.95 |

- Krakauer, "The Rise and Fall of G in AGI" (Apr 2026): 39 models from 2019–2025 on 14 benchmarks.
  - PC1 explains 90% on a 5-benchmark core battery, falling to 77% by 2024.
  - On a 4-benchmark battery it peaks at 92% in 2023–24 and falls to 64% with reasoning models, "coincident with a rotation in the G-factor".
  - Source: [arXiv 2604.09911](https://arxiv.org/abs/2604.09911) (M).
- Maimon et al. (TACL 2026): 60 LLMs × 44 benchmarks give an "intrinsically low-rank" structure with eight skills. Some skills, such as "Precision & Fidelity" and "Ethical Judgment", are defined by a few highly discriminative tasks — [ACL Anthology](https://aclanthology.org/2026.tacl-1.75/); [arXiv 2507.20208](https://arxiv.org/abs/2507.20208) (M).
- Earlier structure studies, not re-read this session (M): Burnell et al. 2023 found 3 factors on HELM ([arXiv 2306.10062](https://arxiv.org/abs/2306.10062)). Ruan et al. 2024 found PC1 ≈ 80% ([arXiv 2405.10938](https://arxiv.org/abs/2405.10938)).
- "Growing Pains" (May 2026): 34 models, 10 labs. Capabilities cooperate (r = +0.72), with lab-specific trajectories: "DeepSeek reversed from reasoning-rich to coding-first; Google maintains consistent reasoning emphasis; Anthropic oscillates". Coupling slopes vary 5× — [arXiv 2605.18840](https://arxiv.org/abs/2605.18840) (M).
- AA-Omniscience:
  - 6,000 questions, 42 topics, 6 domains. Hallucination rate is incorrect / (incorrect + abstentions); the Omniscience Index gives +1 correct, −1 incorrect, 0 abstain — [arXiv 2511.13029](https://arxiv.org/abs/2511.13029); [AA page](https://artificialanalysis.ai/evaluations/omniscience) (M).
  - Hallucination rates: Gemini 3 Pro Preview (high) 88%, Gemini 3 Flash (reasoning) 85%, Claude 4.5 Sonnet (thinking) 48%, Claude Opus 4.5 (thinking) 58% (M).
  - Claude Opus 4.8: 35.9% hallucination, 46.6% accuracy, index 27 — [suprmind aggregator](https://suprmind.ai/hub/ai-hallucination-rates-and-benchmarks/) (L).
- Anthropic–OpenAI pilot cross-evaluation (Aug 2025):
  - Claude Opus 4 and Sonnet 4 had refusal rates "as much as 70%" on hallucination evals.
  - o3 gave "more than twice as many fully correct responses" but hallucinated more.
  - Source: [OpenAI](https://openai.com/index/openai-anthropic-safety-evaluation/) (M).
- Anthropic, "Introducing Claude Opus 5.5" (22 Sep 2026). Vendor-reported; GPT-6 Astra figures "as reported by OpenAI" — [Anthropic](https://www.anthropic.com/news/claude-opus-5-5) (H):

| Benchmark | Opus 5.5 | Fable 5.1 | Opus 5 | GPT-6 Astra | GPT-5.6 Sol |
|---|---|---|---|---|---|
| Terminal-Bench 4.0 | 66.4 | 55.8 | 52.3 | 57.9 | 37.3 |
| GDPval-AA v2.1 | 1846 | 1735 | 1708 | 1542 | 1588 |
| AutomationBench | 40.0 | 31.4 | 26.9 | 41.4 | 28.8 |
| HLE (with tools) | 67.7 | 65.6 | 63.6 | 57.2 | — |
| Terminal-Bench-Science 0.1 | 58.7 | 52.6 | 29.0 | 64.6 | 22.4 |

- Artificial Hivemind (NeurIPS 2025 D&B, Best Paper award): Infinity-Chat has 26K open-ended queries. More than 70 models show "pronounced intra- and inter-model homogenization" — [NeurIPS proceedings](https://proceedings.neurips.cc/paper_files/paper/2025/hash/754d5a526a5ee5a47220664a0eb92751-Abstract-Datasets_and_Benchmarks_Track.html); [NeurIPS blog](https://blog.neurips.cc/2025/11/26/announcing-the-neurips-2025-best-paper-awards/) (M).

### Inferences
- **Most reliable reordering axes:**
  - (1) perception and vision;
  - (2) agentic vs academic;
  - (3) epistemic policy (answer vs abstain).
  All three reflect post-training emphasis by lab. That is reliable variance, but arguably not a "cognitive" construct. It also lowers the effective N in any psychometric study, because models cluster by family.
- **Accuracy and hallucination are dissociable.** The most knowledgeable models do not lead abstention-aware indices, so a benchmark that scores abstention separately gets a lab-reordering axis for free. [speculation] This axis may shrink if labs converge on abstention training after the 2025 "why models hallucinate" discourse.
- **Release date as a confound.** Because the g-factor tracks release date (R² about 0.5), residual "abilities" should be estimated net of date and compute, not just net of the first factor.
- The **Opus 5.5 vs GPT-6 Astra grid** shows that at the Sep 2026 frontier, ranking depends on which agentic benchmark is chosen, even though the grid is vendor-reported. A benchmark that resolves these reorderings with independent, reliability-controlled runs would carry information.

### Gaps
- Sycophancy, persuasion, creativity quality and instruction-following: I found no primary cross-lab quantitative comparison with 2026 models this session (one search returned only marketing pages).
- Could not read Epoch's Claudiness post or the ECI paper in full. PC2's variance share and stability are unknown.
- In-repo leads claim that forecasting (ForecastBench) and calibration error (as opposed to Brier score) are nearly uncorrelated with general capability among frontier models. I did not verify this against primary sources, so it is not reported as a finding.
- Whether the "agentic" axis is a stable ability or a transient post-training emphasis (see the Growing Pains lab oscillation) is unresolved.

---

## Q3. Which abilities are under-measured by headline benchmarks, and what says they matter?

### Takeaway
Headline grids in Sep 2026 cover agentic coding, knowledge work, HLE, computer use and chart reading. They do **not** report:
- calibrated abstention;
- cross-episode learning;
- exploration efficiency;
- core perception or intuitive physics;
- high-reliability (p80+) execution;
- rule fidelity (right answer for the right reason).

Each of these has documented deficits, and several have lab spread. Most can be generated procedurally, which resists contamination.

### Ranked list

The ranking weighs A, B and C jointly:
- **A**: strength of evidence of a deficit or spread;
- **B**: how well novel instances can be generated;
- **C**: whether the ability is absent from headline grids. The Opus 5.5 launch grid has no row for any of these.

| Rank | Ability | Evidence strength | Why it matters (evidence) | Testability with novel generated instances |
|---|---|---|---|---|
| 1 | **Calibrated abstention** | Strong: −24% from reasoning fine-tuning; AA-Omniscience spread 36–88%; 48 LLMs overconfident | Hallucination in deployment; labs differ by policy | **High**: unanswerable, underspecified or stale-premise variants of solvable items, scored with an abstention-aware rule |
| 2 | **Learning from experience across episodes** | Strong deficit (CL-bench best 23.7%; no reuse across episodes); no human baseline | On-the-job improvement; ARC-AGI-3 harness gap (62.7 vs 99.9) shows state carry-over is decisive | **High**: generated latent rule systems shared across episodes; score the learning-curve slope |
| 3 | **Exploration and experimentation efficiency** | Moderate–strong: AutumnBench humans > 2025 models; blicket LLMs less efficient; ARC-AGI-3 accuracy closed in 6 months | Science and agents; human edge attributed to experiment design | **High**: generated grid worlds and causal machines; information gain per action vs Bayesian-optimal and human baselines |
| 4 | **Core visual perception and intuitive physics** | Strong human gap (49.7 vs 94.1; physics near chance) and 3.5× lab spread | Computer use, embodied agents, charts | **High**: procedural images and videos; possible-vs-impossible pairs |
| 5 | **High-reliability long-chain execution (p80/p95)** | Strong: p80 4–10× below p50 [C]; self-conditioning | Deployment needs reliability; METR suite saturating | **High**: long synthetic state-tracking chains with exact checks; report pass^k and p80 |
| 6 | **Rule fidelity (right answer for the right reason)** | Moderate. About 28% of o3's correct ConceptARC answers use unintended or incorrect rules | Accuracy overstates generalization | **Medium–high.** Generate items where the intended and shortcut rules diverge on held-out probes |
| 7 | **Robustness to counterfactual and irrelevant perturbation** | Moderate but stale (≤ early 2025) | Detects memorization; o1-mini errors ~40% misapplied originals | **High.** Template-based (GSM-Symbolic style); best as a *control* condition, not a headline |
| 8 | **Output diversity / novelty** | Moderate (Hivemind, 70+ models) | Homogenization across labs; creative and brainstorming use | **Medium.** Generated open prompts, but diversity scoring needs embeddings or judges |
| 9 | **Implicit world-model coherence** | Moderate for small sequence models, thin for frontier agents | Predictive success without the right model generalizes poorly | **High.** Synthetic automata or physics; Vafa-style inductive-bias probes |
| 10 | **Mental spatial transformation** | Moderate (GPT-5 short on reconstruction, deformation and assembly) | Engineering and design; embodied work | **High.** Procedural 3D shapes, folding and assembly |
| — | ToM under perturbation; everyday trick questions | Weak or closed by 2026 | — | Low priority |

### Cited Findings
- Opus 5.5 headline grid rows (22 Sep 2026) are all agentic, knowledge-work, HLE, computer-use or chart items. None covers abstention, calibration, learning or perception without tools — [Anthropic](https://www.anthropic.com/news/claude-opus-5-5) (H).
- Supporting evidence for ranks 1–10: see Q1 and Q2 Cited Findings. Key sources are [AbstentionBench](https://raw.githubusercontent.com/facebookresearch/AbstentionBench/main/README.md), [CL-bench](https://arxiv.org/abs/2602.03587), [Continual Learning Bench](https://arxiv.org/abs/2606.05661), [AutumnBench](https://arxiv.org/abs/2510.19788), [BabyVision](https://raw.githubusercontent.com/UniPat-AI/BabyVision/main/README.md), [IntPhys 2](https://arxiv.org/abs/2506.09849), [METR runs](https://raw.githubusercontent.com/METR/eval-analysis-public/main/reports/time-horizon-1-1/data/raw/runs.jsonl), [ConceptARC multimodal](https://arxiv.org/abs/2510.02125) and [Artificial Hivemind](https://proceedings.neurips.cc/paper_files/paper/2025/hash/754d5a526a5ee5a47220664a0eb92751-Abstract-Datasets_and_Benchmarks_Track.html).
- CL-bench costs about 20 expert-hours per context and relies on an LLM judge (GPT-5.1) — [README](https://raw.githubusercontent.com/Tencent-Hunyuan/CL-bench/main/README.md) (H). Hand-authored learning benchmarks are expensive, which argues for procedural generation.
- METR notes that measurement becomes unstable once only a few tasks exceed the horizon: 5 of 228 are ≥ 16 h — [METR via OfficeChai](https://officechai.com/ai/claude-mythos-shows-50-time-horizon-of-16-hours-on-metr-benchmark/); [METR limitations note](https://metr.org/notes/2026-01-22-time-horizon-limitations/) (M).

### Inferences
- **Two design requirements follow.**
  - Candidates 1–5 must show **discriminant validity against the general factor and release date**. [speculation] A task framed as "skill acquisition" can still be mostly g-loaded, and whether ARC is has not been checked here.
  - The measure should be an **efficiency or reliability statistic** (slope, information per action, p80, abstention-aware score), not raw accuracy, which saturates fastest.
- [speculation] Abstention (rank 1) and perception (rank 4) are the most likely to *reorder* labs. Learning (rank 2) and exploration (rank 3) are the most likely to *separate humans from AI* in the near term, but ARC-AGI-3 shows they can close within months once harnesses carry state.

### Gaps
- No study I found reports the g-loading of abstention, exploration efficiency, or cross-episode learning slope against ECI or PC1 with 2026 models. Their "off-g" status is untested.
- "What evidence says they matter" is thin for perception in real deployments beyond vendor chart benchmarks. I found no field study linking BabyVision-type skills to agent outcomes.

---

## Q4. Critiques of current evaluation that point to measurable gaps

### Takeaway
Four lines of evidence show that headline scores miss real-world differences:
- The jagged frontier: similar-looking tasks fall on opposite sides of AI competence.
- Field RCTs diverge from benchmarks.
- Vendors themselves now concede that benchmark margins are unreliable.
- Harness and metric choices swing scores by tens of points.

Each suggests a measurable target: calibrated self-knowledge of the frontier, reliability, and protocol-fixed state handling.

### Cited Findings
- Jagged frontier (BCG field experiment, *Organization Science*):
  - For 18 tasks inside the frontier, AI users completed 12.2% more tasks, 25.1% faster, with higher quality.
  - For a task chosen to lie outside it, AI users were 19% (reported as percentage points in the working paper) less likely to be correct.
  - Source: [Dell'Acqua et al.](https://pubsonline.informs.org/doi/full/10.1287/orsc.2025.21838) (M).
- METR RCT (Jul 2025): 16 experienced developers, 246 tasks. With early-2025 AI tools they took 19% longer, contrary to the speedups that experts and the developers themselves predicted — [METR](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) (M).
- METR follow-up (24 Feb 2026):
  - METR judges the new data unreliable because of a "significant increase in developers choosing not to participate because they do not wish to work without AI".
  - Reported "speedup" estimates: −18% (CI −38% to +9%) for returning developers and −4% (CI −15% to +9%) for new recruits.
  - METR nevertheless believes developers are likely more sped up in early 2026.
  - Source: [METR](https://metr.org/blog/2026-02-24-uplift-update/) (M). The sign convention was not verified in the full text; read these as reported.
- Anthropic (22 Sep 2026): "at these levels of capability we've found that benchmark margins have become a less reliable guide to real-world differences". It adds that in its own use the gap between Opus 5.5 and Fable 5.1 "is narrower than these scores suggest" — [Anthropic](https://www.anthropic.com/news/claude-opus-5-5) (H).
- The ARC-AGI-3 harness effect (62.7% vs 99.9% for the same model) comes entirely from memory handling — [ARC Prize](https://arcprize.org/blog/astra) (M).
- "Illusion of Thinking" and its rebuttals show that output-token caps and unsolvable instances can masquerade as reasoning failure — [arXiv 2506.09250](https://arxiv.org/abs/2506.09250); [arXiv 2507.01231](https://arxiv.org/abs/2507.01231) (M).
- Economic benchmarks do not form a distinct latent capability, and the leading factor is "substantially a time trend" — [Zhu 2026](https://arxiv.org/abs/2608.29420) (M).
- Construct validity: a review of 445 LLM benchmarks by 29 experts found patterns that "undermine the validity of the resulting claims" — [Bean et al., arXiv 2511.04703](https://arxiv.org/abs/2511.04703) (M; not re-read this session).

### Inferences
- The jagged-frontier result implies a measurable ability that is *not* on any leaderboard: **the model's knowledge of its own frontier.** That means predicting in advance which tasks it will fail and abstaining or deferring. This links Q4 back to abstention and metacognition (Q3 rank 1).
- Harness sensitivity means any learning or agentic benchmark must **fix the state-carry protocol** (none, notes-only, full state) and report each, or it measures harness engineering.
- [speculation] The RCT selection problem (developers refusing no-AI conditions) suggests that field validation will increasingly need within-task ablations, such as AI-off segments, instead of between-subject designs.

### Gaps
- METR's 2026 follow-up design changes and any newer RCT results (after Feb 2026) were not found.
- There is no quantitative mapping from any benchmark to real-world productivity for 2026 models, apart from vendor statements.

---

## Claims table

| # | Claim | Value | Date | Source URL | Primary/secondary | Conf. |
|---|---|---|---|---|---|---|
| 1 | BabyVision adult human accuracy | 94.1% | Jan 2026 | https://raw.githubusercontent.com/UniPat-AI/BabyVision/main/README.md | Primary | H |
| 2 | BabyVision best model / spread | Gemini3-Pro-Preview 49.7; GPT-5.2 34.4; Claude-4.5-Opus 14.2 | Jan 2026 | same | Primary | H |
| 3 | Gemini 3 Pro vs 6-year-olds | ~20 points behind | Jan 2026 | https://arxiv.org/abs/2601.06521 | Primary (summary) | M |
| 4 | IntPhys 2 humans vs best model | 96.44% vs 55.63% (chance 50%) | Jun 2025 | https://arxiv.org/abs/2506.09849 | Primary (summary) | M |
| 5 | Spatial4D-Bench human lead over GPT-5 | ~17 points (human 78.02) | Jan 2026 | https://arxiv.org/pdf/2601.00092 | Primary (summary) | M |
| 6 | AutumnBench: humans beat o3, Gemini 2.5 Pro, Claude | 517 humans; 43 envs; 129 tasks | Oct 2025 | https://arxiv.org/abs/2510.19788 | Primary (summary) | M |
| 7 | ARC-AGI-3 at launch | All frontier <1% (best 0.37%); humans 100% of envs | 25 Mar 2026 | https://arcprize.org/blog/arc-agi-3-launch | Primary (summary) + secondary | M |
| 8 | GPT-6 Astra on ARC-AGI-3 | 62.7% standard; 99.9% provider harness; fewer actions than median human on 96% of levels | 3 Sep 2026 | https://arcprize.org/blog/astra | Primary (summary) + secondary | M |
| 9 | ARC-AGI-2 harness SOTA | Gemini 3.1 Pro 88.1% → 95.1% (Imbue) | 27 Feb 2026 | https://imbue.com/blog/2026-02-27-arc-agi-2-evolution | Primary (summary) | M |
| 10 | ConceptARC: o3 text accuracy vs humans; wrong-rule share | ≥73% (human 73%); ~28% of correct grids use unintended or incorrect rules | Oct 2025 | https://arxiv.org/abs/2510.02125 | Primary (summary) | M |
| 11 | Counterfactual analogies, humans vs GPT-4 | 75.3% vs 45.2% | 2024 | https://escholarship.org/uc/item/58d9s666 | Secondary summary | M/L |
| 12 | GSM-NoOp drops | up to −65.7%; o1-preview −17.5%; o1-mini −29.1% | Oct 2024 / ICLR 2025 | https://arxiv.org/abs/2410.05229 | Primary (summary) | M |
| 13 | MATH-P-Hard drops | o1-mini −16.49%; Gemini-2.0-FT −12.9% | Feb 2025 / ICML 2025 | https://proceedings.mlr.press/v267/huang25k.html | Primary (summary) | M |
| 14 | Mystery Blocksworld (latest on leaderboard) | R1 43.3%; o1-preview 52.8%; Randomized 25.8% / 37.3% | Jan 2025 | https://raw.githubusercontent.com/karthikv792/LLMs-Planning/main/README.md | Primary | H |
| 15 | o1 still probability-sensitive | Qualitative | Oct 2024 | https://arxiv.org/abs/2410.01792 | Primary (summary) | M |
| 16 | Reasoning models more robust on ToM perturbations | Qualitative | Aug 2026 | https://arxiv.org/html/2608.04646 | Primary (summary) | M/L |
| 17 | Orbital transformer recovers nonsensical force law | Qualitative | ICML 2025 | https://proceedings.mlr.press/v267/vafa25a.html | Primary (summary) | M |
| 18 | METR public frontier p80 | ~1.5 h (50 min to 2 h 40 min) | Feb–Mar 2026 | https://metr.org/blog/2026-05-19-frontier-risk-report/ | Primary (summary) | M |
| 19 | Mythos Preview p50 | ≥16 h (CI 8.5–55 h); 5 of 228 tasks ≥16 h | Mar 2026 | https://x.com/METR_Evals/status/2052896621760004602 | Primary (summary) | M |
| 20 | Mythos p80; Opus 4.6 p80 | 3 h 06 min; ~70 min | 9 May 2026 | https://metr.org/time-horizons/ | Primary (summary) | M |
| 21 | p50/p80 ratio across 20 models | 4.0–10.3×; Opus 4.6 719 vs 70 min | TH1.1 data (to Feb 2026) | https://raw.githubusercontent.com/METR/eval-analysis-public/main/reports/time-horizon-1-1/data/raw/runs.jsonl | Primary data [C] | H |
| 22 | Self-conditioning not fixed by scale; thinking fixes it | Qualitative | Sep 2025 | https://arxiv.org/abs/2509.09677 | Primary (summary) | M |
| 23 | CL-bench frontier average / best | 17.2% / 23.7% (GPT-5.1) | Feb 2026 | https://arxiv.org/abs/2602.03587 | Primary (summary) | M |
| 24 | Continual Learning Bench: memory systems don't beat naive ICL | Qualitative | Jun 2026 | https://arxiv.org/abs/2606.05661 | Primary (summary) | M |
| 25 | Reasoning fine-tuning reduces abstention | −24% average; scale "almost no effect" | Jun 2025 | https://raw.githubusercontent.com/facebookresearch/AbstentionBench/main/README.md ; https://arxiv.org/abs/2506.09038 | Primary | H (direction) / M (24%) |
| 26 | 48 LLMs overconfident on clinical questions | All poorly calibrated | 2026 | https://www.nature.com/articles/s44355-026-00053-3 | Primary (summary) | M |
| 27 | AA-Omniscience hallucination rates | Gemini 3 Pro 88%; Claude 4.5 Sonnet 48%; Opus 4.5 58% | Nov 2025–2026 | https://arxiv.org/abs/2511.13029 | Primary (summary) | M |
| 28 | Claude refusals vs o3 hallucinations | Claude up to 70% refusals; o3 >2× correct answers, more hallucination | Aug 2025 | https://openai.com/index/openai-anthropic-safety-evaluation/ | Primary (summary) | M |
| 29 | SimpleBench human baseline; top model | 83.7% (n = 9); Opus 5.5 88.4% | Sep 2026 | https://benchmarklist.com/benchmarks/simplebench/ | Secondary | L |
| 30 | Epoch cross- vs within-domain correlation | 0.68 vs 0.79 | c. 2026 | https://epoch.ai/data-insights/benchmark-correlations | Primary (summary) | M |
| 31 | Epoch PC2 "Claudiness" | Agentic + / vision and math − | Nov 2025 | https://epoch.ai/gradient-updates/benchmark-scores-general-capability-claudiness | Primary (summary) | M |
| 32 | AA-data general factor | PC1 79.4%; factor 1 74.5%; date R² 0.48–0.51; mean ρ 0.79 | Aug 2026 | https://raw.githubusercontent.com/louisyzhu/frontier-ai-economic-validity/main/data/processed/task1_structure_results.json | Primary data | H |
| 33 | AA-data agentic vs academic factors | TB v2.1 1.05, GDPval 0.87 (F1); GPQA 0.97, IFBench 0.90 (F2) | Aug 2026 | https://raw.githubusercontent.com/louisyzhu/frontier-ai-economic-validity/main/data/processed/loadings_raw.csv | Primary data | H |
| 34 | g-factor share falls with reasoning models | 92% → 64% (4-benchmark battery) | Apr 2026 | https://arxiv.org/abs/2604.09911 | Primary (summary) | M |
| 35 | Lab coupling slopes differ | 5× (Google 1.15 vs DeepSeek 0.23) | May 2026 | https://arxiv.org/abs/2605.18840 | Primary (summary) | M |
| 36 | Artificial Hivemind | >70 models homogeneous; 79% of cases intra-model similarity >0.8 | NeurIPS 2025 | https://proceedings.neurips.cc/paper_files/paper/2025/hash/754d5a526a5ee5a47220664a0eb92751-Abstract-Datasets_and_Benchmarks_Track.html | Primary (summary) | M |
| 37 | Opus 5.5 vs GPT-6 Astra reordering | TB 4.0 66.4 vs 57.9; TB-Science 58.7 vs 64.6; GDPval-AA 1846 vs 1542 | 22 Sep 2026 | https://www.anthropic.com/news/claude-opus-5-5 | Primary (vendor) | H |
| 38 | "Benchmark margins … less reliable guide" | Quote | 22 Sep 2026 | https://www.anthropic.com/news/claude-opus-5-5 | Primary | H |
| 39 | METR RCT | +19% completion time; 16 devs; 246 tasks | Jul 2025 | https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ | Primary (summary) | M |
| 40 | METR 2026 follow-up unreliable (selection) | −18% [−38, +9]; −4% [−15, +9] ("speedup" as reported) | 24 Feb 2026 | https://metr.org/blog/2026-02-24-uplift-update/ | Primary (summary) | M |
| 41 | Jagged frontier field experiment | +12.2% tasks, 25.1% faster inside; −19 points outside | Org. Sci. 2026 | https://pubsonline.informs.org/doi/full/10.1287/orsc.2025.21838 | Primary (summary) | M |
| 42 | Active blicket: LLMs explore less efficiently | Qualitative | CogSci 2026 | https://arxiv.org/abs/2606.06464 | Primary (summary) | M |

---

## Sources

**H: read directly this session**

- BabyVision README — https://raw.githubusercontent.com/UniPat-AI/BabyVision/main/README.md
- PlanBench README — https://raw.githubusercontent.com/karthikv792/LLMs-Planning/main/README.md
- AbstentionBench README — https://raw.githubusercontent.com/facebookresearch/AbstentionBench/main/README.md
- CL-bench README — https://raw.githubusercontent.com/Tencent-Hunyuan/CL-bench/main/README.md
- Continual Learning Bench README — https://raw.githubusercontent.com/pgasawa/continual-learning-bench/main/README.md
- GSM-Symbolic README — https://raw.githubusercontent.com/apple/ml-gsm-symbolic/main/README.md
- Wu et al. README — https://raw.githubusercontent.com/ZhaofengWu/counterfactual-evaluation/master/README.md
- METR TH1.1 run data — https://raw.githubusercontent.com/METR/eval-analysis-public/main/reports/time-horizon-1-1/data/raw/runs.jsonl
- Zhu 2026 repository and data — https://raw.githubusercontent.com/louisyzhu/frontier-ai-economic-validity/main/README.md
- Anthropic, "Introducing Claude Opus 5.5" — https://www.anthropic.com/news/claude-opus-5-5

**M: primary URL, content seen via search summary**

- Perception and physics:
  - https://arxiv.org/abs/2601.06521
  - https://arxiv.org/abs/2506.09849
  - https://arxiv.org/pdf/2508.13142
  - https://arxiv.org/pdf/2601.00092
- Exploration and interactive learning:
  - https://arxiv.org/abs/2510.19788
  - https://arcprize.org/blog/arc-agi-3-launch
  - https://arxiv.org/abs/2603.24621
  - https://arcprize.org/blog/astra
  - https://imbue.com/blog/2026-02-27-arc-agi-2-evolution
  - https://arxiv.org/abs/2606.06464
- Abstraction, analogy and ToM:
  - https://arxiv.org/abs/2510.02125
  - https://arxiv.org/abs/2404.13070
  - https://escholarship.org/uc/item/58d9s666
  - https://arxiv.org/html/2608.04646
- Perturbation, planning and world models:
  - https://arxiv.org/abs/2410.05229
  - https://proceedings.mlr.press/v267/huang25k.html
  - https://arxiv.org/abs/2410.01792
  - https://cocosci.princeton.edu/papers/mccoy2024embers.pdf
  - https://arxiv.org/abs/2506.06941
  - https://arxiv.org/abs/2506.09250
  - https://arxiv.org/abs/2507.01231
  - https://proceedings.mlr.press/v267/vafa25a.html
- Long horizons and learning:
  - https://metr.org/blog/2026-05-19-frontier-risk-report/
  - https://metr.org/time-horizons/
  - https://metr.org/notes/2026-01-22-time-horizon-limitations/
  - https://x.com/METR_Evals/status/2052896621760004602
  - https://arxiv.org/abs/2509.09677
  - https://arxiv.org/abs/2602.03587
  - https://arxiv.org/abs/2606.05661
- Abstention and calibration:
  - https://arxiv.org/abs/2506.09038
  - https://www.nature.com/articles/s44355-026-00053-3
  - https://arxiv.org/abs/2511.13029
  - https://openai.com/index/openai-anthropic-safety-evaluation/
- Capability structure:
  - https://epoch.ai/gradient-updates/benchmark-scores-general-capability-claudiness
  - https://epoch.ai/data-insights/benchmark-correlations
  - https://arxiv.org/abs/2512.00193
  - https://arxiv.org/abs/2608.29420
  - https://arxiv.org/abs/2604.09911
  - https://aclanthology.org/2026.tacl-1.75/
  - https://arxiv.org/abs/2605.18840
  - https://proceedings.neurips.cc/paper_files/paper/2025/hash/754d5a526a5ee5a47220664a0eb92751-Abstract-Datasets_and_Benchmarks_Track.html
- Field evidence:
  - https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
  - https://metr.org/blog/2026-02-24-uplift-update/
  - https://pubsonline.informs.org/doi/full/10.1287/orsc.2025.21838
- Cited but not re-read:
  - https://arxiv.org/abs/2306.10062
  - https://arxiv.org/abs/2405.10938
  - https://arxiv.org/abs/2511.04703
  - https://arxiv.org/abs/2307.02477

**L: aggregators and secondary coverage**

- https://benchmarklist.com/benchmarks/simplebench/
- https://itdoeswhatnow.com/benchmarks/simplebench/
- https://www.datalearner.com/en/leaderboards
- https://suprmind.ai/hub/ai-hallucination-rates-and-benchmarks/
- https://officechai.com/ai/arc-agi-3/
- https://thenewstack.io/astra-arc-agi-benchmark/
- https://officechai.com/ai/claude-mythos-shows-50-time-horizon-of-16-hours-on-metr-benchmark/
- https://www.metaculus.com/questions/41131/top-arc-agi-2-score-in-2026/

**Not verifiable this session**

- Full texts on arxiv.org, metr.org, epoch.ai, arcprize.org, openreview.net, huggingface.co and simple-bench.com (all egress-blocked).
- 2026-model re-tests of GSM-NoOp, Mystery Blocksworld, IntPhys 2, AutumnBench, Lewis–Mitchell and Wu et al. (none found).
- Cross-lab sycophancy and persuasion rates (none found).

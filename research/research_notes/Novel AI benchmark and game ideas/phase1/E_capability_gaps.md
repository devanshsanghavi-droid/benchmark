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

1. **The robust human advantages as of Sep 2026 are perceptual and interactive, not verbal-abstract.**
   - Core visual perception (BabyVision, Jan 2026): the best model scores 49.7% against 94.1% for adults. Only the best model beats 3-year-olds, and it still trails 6-year-olds by about 20 points.
   - Intuitive physics from video (IntPhys 2, Jun 2025): models are near chance (≤55.6%) against 96.4% for humans.
   - Mental spatial transformation: GPT-5 was still short of humans on mental reconstruction, deformation and assembly (Aug 2025).
   - Reward-free world-model learning through exploration (AutumnBench, Oct 2025): 517 humans beat o3, Gemini 2.5 Pro and Claude.
   - Caveat: the physics and exploration results predate 2026 models.
2. **Static "few-shot abstraction" is no longer a human moat on accuracy.**
   - ARC-AGI-2 went from 54.2% (GPT-5.2 Pro, start of 2026) to 95–98% with harnesses and program search by early/mid 2026.
   - On ConceptARC's text format, o3 matches the human 73%.
   - Two gaps remain: about 28% of o3's correct answers rest on unintended or wrong rules, and accuracy drops sharply when the same tasks are shown visually.
3. **Interactive skill acquisition is closing fast, and its measured size depends on the harness.**
   - ARC-AGI-3 launched on 25 Mar 2026 with every frontier model below 1% and humans solving 100% of environments.
   - By 3 Sep 2026 GPT-6 Astra scored 62.7% on the standard harness and 99.9% on a provider harness that keeps its reasoning state between calls.
   - It reportedly used fewer actions than the median human on 96% of levels.
   - This is "fragile, not robust".
4. **Classic "reasoning or reciting" deficits shrink with reasoning models, but no 2026 data exist.** This covers counterfactual variants, embers of autoregression, GSM-NoOp distractors, MATH-P-Hard and Mystery Blocksworld.
   - Every quantified result is from o1, o1-mini, R1 or Gemini-2.0-thinking (late 2024 to early 2025).
   - GSM-NoOp: drops of −17.5% (o1-preview) against up to −65.7% for the worst model.
   - Mystery Blocksworld: 52.8% (o1-preview) and 43.3% (R1). Randomized Mystery: 37.3% and 25.8%.
   - Treat these as older-model evidence.
5. **Theory-of-mind perturbation fragility (Ullman 2023) is largely a GPT-3.5-era finding.** A 2026 paper reports that reasoning models are consistently more robust to ToM perturbations.
6. **Long-horizon reliability is a robust, structural gap.**
   - My refit of METR's public TH1.1 data [C] gives an 80%-success horizon 4–10× shorter than the 50% horizon for every model.
   - Claude Opus 4.6 has the widest gap: p50 ≈ 12.0 h against p80 ≈ 70 min.
   - Claude Mythos Preview: p50 ≥ 16 h (CI 8.5–55 h) and p80 about 3 h 06 min.
   - METR's suite is running out of long tasks: only 5 of 228 are ≥ 16 h.
7. **Learning from experience and from novel context is weak, and this has been measured in 2026 frontier models.**
   - CL-bench (Feb 2026): ten frontier models average 17.2%; the best, GPT-5.1, reaches 23.7%.
   - Continual Learning Bench (Jun 2026): agents overfit to recent observations and fail to reuse knowledge across episodes, and memory systems do not beat naive in-context learning.
   - No human baselines exist for either benchmark.
8. **Metacognition and abstention show the largest, most lab-specific divergence.**
   - Reasoning fine-tuning cuts abstention by about 24% (AbstentionBench, 2025).
   - AA-Omniscience hallucination rates: 88% for Gemini 3 Pro against 48% for Claude 4.5 Sonnet.
   - In the Anthropic–OpenAI pilot, Claude refused up to 70% of hallucination-eval items, while o3 answered more and hallucinated more.
9. **The general factor dominates but is not total.**
   - PC1 explains about 79% of variance across 421 Artificial Analysis model configurations [H data]. Epoch finds cross-domain r = 0.68 against within-domain r = 0.79.
   - A replicated second axis separates **agentic** strength from **math and vision**. Epoch calls it "Claudiness", and the Aug 2026 AA-data factor analysis separates Terminal-Bench, GDPval and τ² from GPQA, IFBench and AA-LCR.
   - Vision shows the largest reordering. On BabyVision the spread is 3.5×: Gemini 3 Pro 49.7%, GPT-5.2 34.4%, Claude 4.5 Opus 14.2%.
10. **The general factor is partly a release-date trend.** It tracks release date with R² ≈ 0.48–0.51. Its dominance fell (92% → 64% on one small battery) when reasoning models arrived.
11. **Headline benchmark margins no longer predict real-world differences.**
    - Anthropic's Opus 5.5 launch post (22 Sep 2026) says as much.
    - Vendor grids reorder frontier models by benchmark. Opus 5.5 leads Terminal-Bench 4.0 (66.4 vs 57.9) and GDPval-AA (1846 vs 1542), while GPT-6 Astra leads Terminal-Bench-Science (64.6 vs 58.7).
    - METR's RCT found a 19% slowdown with early-2025 tools. Its 2026 follow-up was confounded by developers refusing to work without AI.
12. **The best under-measured targets combine a documented deficit, measured lab spread, and cheap procedural generation.** In order:
    - (i) calibrated abstention on generated unanswerable or underspecified variants;
    - (ii) cross-episode learning on procedurally generated latent rule systems;
    - (iii) exploration efficiency (actions and experiments per bit learned) in novel interactive worlds;
    - (iv) procedurally generated core-vision and intuitive-physics items;
    - (v) high-reliability (p80/p95) long-chain execution.

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
| Intuitive physics (possible vs impossible video) | IntPhys 2: humans 96.44% (92.44% on held-out); best model 55.63% (Gemini 2.5 Flash); chance is 50% | Gemini 2.5 Flash and video models (Jun 2025) | **Robust but stale for 2026** | M |
| Spatial reasoning (mental transformation) | GPT-5 reaches human level on metric measurement and spatial relations. Big shortfalls remain on mental reconstruction, deformation and assembly, and comprehensive reasoning. Spatial4D-Bench: humans 78.02, about 17 points above GPT-5 | GPT-5 (Aug 2025); Spatial4D (Jan 2026) | **Robust for transformation subskills; closed for measurement and relations** | M |
| World-model learning via reward-free exploration | AutumnBench/WorldTest (43 environments, 129 tasks, 517 humans): humans beat o3, Gemini 2.5 Pro and Claude. More compute helps in only some environments | o3, Gemini 2.5 Pro, Claude (Oct 2025) | **Robust in 2025; untested on 2026 models** | M |
| Interactive skill acquisition, novel games (ARC-AGI-3) | Launch: all frontier models <1% (best 0.37%, Gemini 3.1 Pro); humans solve 100% of environments. 3 Sep 2026: GPT-6 Astra 62.7% on the standard harness, 99.9% on the provider harness, and fewer actions than the median human on 96% of levels | GPT-6 Astra (Sep 2026) | **Fragile / closing (harness-dependent)** | M |
| Active causal learning (blicket-style interventions) | Some SOTA LLMs approach human accuracy at hypothesis inference, but they explore less efficiently. They show the same conjunctive-vs-disjunctive gap; LM agents have a disjunctive bias like adults, not children | Unspecified "state-of-the-art" LLMs (CogSci 2026) | **Accuracy fragile; exploration efficiency robust** | M/L |
| Static few-shot abstraction (ARC-AGI-1/2) | ARC-AGI-2: GPT-5.2 Pro 54.2% at the start of 2026. Imbue's evolution harness took Gemini 3.1 Pro from 88.1% to 95.1% (Feb 2026). Confluence Lab reports 97.9% on the public eval at $11.77/task | Gemini 3.1 Pro + harness (Feb 2026); others 2026 | **Closed on accuracy** (efficiency and priors not separately established) | M |
| Concept abstraction with the right rule, across modalities (ConceptARC) | o3 (medium) matches or beats human accuracy (73%) in text, but about 28% of its correct grids use "correct-unintended" or incorrect rules. Visual-modality accuracy drops sharply | o3 (Oct 2025) | **Accuracy closed (text); rule fidelity and visual abstraction robust** | M |
| Analogy with counterfactual alphabets | Humans 75.3% vs GPT-4 45.2% zero-shot (136 humans). Webb et al. rebut: GPT-4 with code execution solves the counterfactual variants | GPT-4 (2024) | **Stale** (no reasoning-model test found) | M/L |
| Counterfactual task variants ("reasoning or reciting") | Consistent degradation on counterfactual variants across 11 task families | GPT-4, Claude, PaLM (2023) | **Stale** | M |
| Embers of autoregression (sensitivity to output probability) | o1 improves greatly, especially on rare task variants, but "still displays the same qualitative trends" | o1 (Oct 2024) | **Fragile / stale** | M |
| Perturbation robustness in math | GSM-NoOp: drops up to −65.7%; o1-preview −17.5%, o1-mini −29.1%. MATH-P-Hard: o1-mini −16.49%, Gemini-2.0-flash-thinking −12.9%; about 40% of o1-mini's errors blindly reuse the original technique | o1-mini, Gemini 2.0 Flash Thinking (early 2025) | **Fragile / stale** | M |
| Planning in obfuscated domains | Mystery Blocksworld: o1-preview 52.8%, R1 43.3% (non-reasoning LLMs ≈0%). Randomized Mystery: 37.3% and 25.8% | DeepSeek R1 (Jan 2025) | **Fragile / stale** | H |
| Planning at scale ("Illusion of Thinking") | Accuracy collapses past a complexity threshold. Rebuttal: many failures are output-token limits or unsolvable instances. Replication: failures are partly cognitive (about 8 disks in Tower of Hanoi) | Claude 3.7 Thinking, o3-mini, R1 era (Jun–Jul 2025) | **Contested; stale** | M |
| Theory of mind under trivial alterations | Ullman (2023): GPT-3.5 fails trivial alterations. 2026: reasoning models are "consistently" more robust to prompt and task perturbations | Reasoning models (Aug 2026 preprint) | **Largely closed (text vignettes)** | M/L |
| Implicit world models | Transformers trained on orbits predict trajectories well but recover a "nonsensical" force law; they excel at the training task without an inductive bias toward the true model | Mostly purpose-trained transformers (ICML 2025) | **Robust for sequence models; untested for frontier agents** | M |
| Everyday trick and common-sense questions (SimpleBench) | Human baseline 83.7% (n = 9). Claude Opus 5.5 is reported at 88.4% (22 Sep 2026) | Claude Opus 5.5 (Sep 2026) | **Closed** (per aggregators) | L/M |
| Long-horizon reliability | p80 is 4–10× shorter than p50 [C]. Public frontier p80 was about 1.5 h in Feb–Mar 2026; Mythos Preview p50 ≥ 16 h and p80 about 3.1 h | Opus 4.6, GPT-5.3-Codex (public data); Mythos Preview (Mar–May 2026) | **Robust gap in reliability (not in reach)** | H (data) / M |
| Learning from new context and from experience | CL-bench: average 17.2%, best 23.7%, context ignored in 55–66% of failures. Continual Learning Bench: no reuse across episodes; memory systems do not help | GPT-5.1 and 9 other frontier models (Feb 2026); frontier agents (Jun 2026) | **Robust deficit (no human baseline)** | M (scores); H (design) |
| Metacognition, calibration and abstention | Reasoning fine-tuning cuts abstention by about 24%, and scale has "almost no effect". 48 LLMs all overconfident on clinical questions. AA-Omniscience hallucination rates of 36–88% | 20 LLMs incl. R1-distills (Jun 2025); Gemini 3 and Claude 4.5–4.8 (Nov 2025–2026) | **Robust deficit; human comparison ambiguous** | H/M |
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
- The ECI fits many benchmarks with a single dimension (a sigmoid IRT with a capability per model and a difficulty and slope per benchmark) — [Ho et al., "A Rosetta Stone for AI Benchmarks", arXiv 2512.00193](https://arxiv.org/abs/2512.00193) (M).
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
- Earlier structure studies:
  - Burnell et al. (2023): 3 factors (comprehension, language modelling, reasoning) on HELM — [arXiv 2306.10062](https://arxiv.org/abs/2306.10062) (M; not re-read this session).
  - Ruan et al. (NeurIPS 2024): PC1 nearly 80%, top-3 PCs about 97% — [arXiv 2405.10938](https://arxiv.org/abs/2405.10938) (M; not re-read this session).
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
- BabyVision per-lab spread (see Q1) — [README](https://raw.githubusercontent.com/UniPat-AI/BabyVision/main/README.md) (H).

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
| 1 | **Calibrated abstention / knowing when one does not know** | Strong. AbstentionBench: −24% from reasoning fine-tuning, scale has no effect. AA-Omniscience spread 36–88%. Clinical overconfidence across 48 LLMs | Hallucination is a major deployment failure, and labs differ by policy (Claude refuses up to 70%) | **High.** Generate unanswerable, underspecified or stale-premise variants of solvable items, and score with an abstention-aware proper rule |
| 2 | **Learning from experience across episodes** | Strong for the deficit (CL-bench best 23.7%; Continual Learning Bench shows no reuse, and memory systems do not help). No human baseline | Real work needs improvement on the job. Harness effects on ARC-AGI-3 (62.7 vs 99.9) show state carry-over is decisive | **High.** Procedurally generated latent rule systems or environments shared across episodes; measure the learning-curve slope, not final accuracy |
| 3 | **Exploration and experimentation efficiency** | Moderate to strong. AutumnBench: humans beat 2025 models. Blicket: LLMs explore less efficiently. ARC-AGI-3 was closed in accuracy within 6 months | Scientific and agentic settings; humans' advantage is attributed to experiment design and belief updating | **High.** Generated grid worlds and causal machines; score information gain per action against a Bayesian-optimal and a human baseline |
| 4 | **Core visual perception and intuitive physics** | Strong human gap (BabyVision 49.7 vs 94.1; IntPhys 2 near chance) and a 3.5× lab spread | Computer use, embodied agents, and chart and diagram work (vendors now report "Chartography" with tools) | **High.** Synthetic images and videos from procedural generators; possible-vs-impossible pairs |
| 5 | **High-reliability long-chain execution (p80/p95)** | Strong. p80 is 4–10× below p50 [C]; self-conditioning on own errors | Deployment needs reliability, not 50% success; METR's suite is saturating (5 of 228 tasks ≥ 16 h) | **High.** Long synthetic execution chains (key–value updates, state tracking) with exact verification; report pass^k and p80 |
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
  - Candidates 1–5 must show **discriminant validity against the general factor and release date**. For example, the ARC family turned out to be g-loaded despite its skill-acquisition framing (an in-repo lead, not verified here).
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

**Primary sources read directly this session (H)**
- BabyVision README — https://raw.githubusercontent.com/UniPat-AI/BabyVision/main/README.md
- PlanBench / LLMs-Planning README — https://raw.githubusercontent.com/karthikv792/LLMs-Planning/main/README.md
- AbstentionBench README — https://raw.githubusercontent.com/facebookresearch/AbstentionBench/main/README.md
- CL-bench README — https://raw.githubusercontent.com/Tencent-Hunyuan/CL-bench/main/README.md
- Continual Learning Bench README — https://raw.githubusercontent.com/pgasawa/continual-learning-bench/main/README.md
- GSM-Symbolic README — https://raw.githubusercontent.com/apple/ml-gsm-symbolic/main/README.md
- Wu et al., counterfactual-evaluation README — https://raw.githubusercontent.com/ZhaofengWu/counterfactual-evaluation/master/README.md
- METR eval-analysis-public README and TH1.1 runs — https://raw.githubusercontent.com/METR/eval-analysis-public/main/README.md ; https://raw.githubusercontent.com/METR/eval-analysis-public/main/reports/time-horizon-1-1/data/raw/runs.jsonl
- Zhu, economic-validity repo (README, task1_structure_results.json, loadings_raw.csv, loadings_residualised.csv, benchmark_taxonomy.csv) — https://raw.githubusercontent.com/louisyzhu/frontier-ai-economic-validity/main/README.md
- Anthropic, "Introducing Claude Opus 5.5" (22 Sep 2026) — https://www.anthropic.com/news/claude-opus-5-5

**Primary sources seen via URL plus search summary (M)**
- Perception and physics:
  - BabyVision paper — https://arxiv.org/abs/2601.06521 ; https://icml.cc/virtual/2026/poster/63195
  - IntPhys 2 — https://arxiv.org/abs/2506.09849
  - Cai et al., GPT-5 spatial intelligence — https://arxiv.org/pdf/2508.13142
  - Spatial4D-Bench — https://arxiv.org/pdf/2601.00092
- Exploration and interactive learning:
  - AutumnBench / WorldTest — https://arxiv.org/abs/2510.19788
  - ARC-AGI-3 — https://arcprize.org/blog/arc-agi-3-launch ; https://arxiv.org/abs/2603.24621 ; https://arcprize.org/blog/astra ; https://arcprize.org/results/openai-gpt-6-astra
  - Imbue ARC-AGI-2 — https://imbue.com/blog/2026-02-27-arc-agi-2-evolution
  - Human Adults and LLMs as Scientists — https://arxiv.org/abs/2606.06464
- Abstraction, analogy and ToM:
  - ConceptARC multimodal — https://arxiv.org/abs/2510.02125
  - Webb et al. counterfactual analogies — https://arxiv.org/abs/2404.13070
  - Lewis & Mitchell (CogSci) — https://escholarship.org/uc/item/58d9s666
  - ToM in reasoning models — https://arxiv.org/html/2608.04646
- Perturbation, planning and world models:
  - GSM-Symbolic — https://arxiv.org/abs/2410.05229
  - MATH-Perturb — https://proceedings.mlr.press/v267/huang25k.html
  - Embers o1 — https://arxiv.org/abs/2410.01792 ; Embers PNAS — https://cocosci.princeton.edu/papers/mccoy2024embers.pdf
  - Illusion of Thinking — https://arxiv.org/abs/2506.06941 ; rebuttal https://arxiv.org/abs/2506.09250 ; replication https://arxiv.org/abs/2507.01231
  - Vafa et al. 2025 — https://proceedings.mlr.press/v267/vafa25a.html
- Long horizons and learning:
  - METR frontier risk report — https://metr.org/blog/2026-05-19-frontier-risk-report/
  - METR time horizons — https://metr.org/time-horizons/
  - METR limitations note — https://metr.org/notes/2026-01-22-time-horizon-limitations/
  - METR Mythos post — https://x.com/METR_Evals/status/2052896621760004602
  - Sinha et al., long-horizon execution — https://arxiv.org/abs/2509.09677
  - CL-bench — https://arxiv.org/abs/2602.03587
  - Continual Learning Bench — https://arxiv.org/abs/2606.05661
- Abstention and calibration:
  - AbstentionBench — https://arxiv.org/abs/2506.09038
  - LLM clinical confidence — https://www.nature.com/articles/s44355-026-00053-3
  - AA-Omniscience — https://arxiv.org/abs/2511.13029 ; https://artificialanalysis.ai/evaluations/omniscience
  - Anthropic–OpenAI pilot — https://openai.com/index/openai-anthropic-safety-evaluation/
- Capability structure and divergence:
  - Epoch Claudiness — https://epoch.ai/gradient-updates/benchmark-scores-general-capability-claudiness
  - Epoch benchmark correlations — https://epoch.ai/data-insights/benchmark-correlations
  - ECI / Rosetta Stone — https://arxiv.org/abs/2512.00193
  - Zhu 2026 — https://arxiv.org/abs/2608.29420
  - Krakauer 2026 — https://arxiv.org/abs/2604.09911
  - Maimon et al. — https://aclanthology.org/2026.tacl-1.75/
  - Growing Pains — https://arxiv.org/abs/2605.18840
  - Artificial Hivemind — https://proceedings.neurips.cc/paper_files/paper/2025/hash/754d5a526a5ee5a47220664a0eb92751-Abstract-Datasets_and_Benchmarks_Track.html
- Field evidence:
  - METR RCT — https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ ; update https://metr.org/blog/2026-02-24-uplift-update/
  - Dell'Acqua et al. — https://pubsonline.informs.org/doi/full/10.1287/orsc.2025.21838

**Cited but not re-read this session (bibliographic; M)**
- Burnell et al. 2023 — https://arxiv.org/abs/2306.10062
- Ruan et al. 2024 — https://arxiv.org/abs/2405.10938
- Bean et al. 2025 — https://arxiv.org/abs/2511.04703
- Wu et al. — https://arxiv.org/abs/2307.02477

**Secondary / aggregator (L)**
- SimpleBench aggregators — https://benchmarklist.com/benchmarks/simplebench/ ; https://www.datalearner.com/en/leaderboards ; https://itdoeswhatnow.com/benchmarks/simplebench/
- AA-Omniscience aggregator — https://suprmind.ai/hub/ai-hallucination-rates-and-benchmarks/
- ARC-AGI-3 coverage — https://officechai.com/ai/arc-agi-3/ ; https://thenewstack.io/astra-arc-agi-benchmark/
- Mythos coverage — https://officechai.com/ai/claude-mythos-shows-50-time-horizon-of-16-hours-on-metr-benchmark/
- ARC-AGI-2 forecasting question — https://www.metaculus.com/questions/41131/top-arc-agi-2-score-in-2026/

**Could not verify (blocked or not found)**
- Full texts on arxiv.org, metr.org, epoch.ai, arcprize.org, openreview.net and huggingface.co (egress blocked).
- simple-bench.com (blocked).
- Any 2026-model re-test of GSM-NoOp, Mystery Blocksworld, IntPhys 2, AutumnBench, Lewis–Mitchell or Wu et al. (not found).
- Cross-lab sycophancy or persuasion rates (not found).

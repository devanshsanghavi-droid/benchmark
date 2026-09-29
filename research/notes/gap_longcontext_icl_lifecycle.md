# Gap dossier: lifecycle of synthetic and natural long-context and in-context-learning benchmarks (2023–2026)

Compiled 2026-09-29 by the gap-filling research subagent. Refs: `research/refs/gap_longcontext_icl_lifecycle.json`.

**What this covers.** NIAH, RULER, NoLiMa, HELMET, LongBench / LongBench v2, LOFT, Michelangelo (Latent List, MRCR, IDK), OpenAI-MRCR (v1, v2), Graphwalks, Google DeepMind MRCR v2, BrowseComp Long Context, Fiction.LiveBench, Artificial Analysis AA-LCR and BABILong. On the ICL side: many-shot ICL, LongICLBench, ManyICLBench, MIR-Bench, LMAct, HELMET-ICL, CL-bench and MTOB-as-long-context. It adds third-party runners (Context Arena, AA, Epoch, HELM, lm-eval-harness, NeMo, Prime Intellect) and the Chroma "Context Rot" report.

**How this was researched.**
- WebSearch had budget left, and 5 searches were used.
- WebFetch reached github.com (HTML), which was used for commit histories. It could not reach openai.com, arxiv.org, huggingface.co, fiction.live, contextarena.ai, longbench2.github.io, princeton-nlp.github.io or cdn.sanity.io.
- `raw.githubusercontent.com`, `storage.googleapis.com` (Gemini reports and model cards, and the public `mrcr_v2` bucket) and `anthropic.com` were read directly with curl.
- The model-card tables and the HELMET correlation figure were read from rendered images.
- OpenAI launch pages were read from the `visual-snow/seshat` markdown mirror, the same mirror `model_cards_adoption.md` used.
- The Michelangelo and Many-Shot ICL papers were read in full from parsed copies in the same repo (`parsed/deepmind/2409_12640.md`, `2404_11018.md`).

**Labels.**
- **H**: primary source (official repo, report PDF, model card or launch page, or a faithful mirror of one), or two independent agreeing copies.
- **M**: a single mirror, a secondary summary, a WebFetch model summary, or a search-engine summary.
- **L**: one weak or unverified source.
- **[D]**: a number I derived by arithmetic from cited numbers.
- **[I]**: my interpretation.
- **U**: not verified.

Keys in [brackets] resolve in the refs JSON. Existing survey keys are reused where the work is already in the survey.

---

## Summary

1. **NIAH saturated in about three months, then left headline tables.**
   - Kamradt's needle test started with two runs: GPT-4-128K (8 Nov 2023) and Claude 2.1 (21 Nov 2023). Both showed clear failures: GPT-4 at ≥73K tokens and 10–50% depth, Claude 2.1 across most long cells [kamradt2023niah] (H).
   - By Feb–Mar 2024 the Gemini 1.5 and Claude 3 launches reported >99.7% to 1M and >99% respectively [gemini2024gemini15; anthropic2024claude3] (H).
   - The test was a single needle with a lexically matching question, out-of-place in a Paul Graham haystack. The original runs were graded by GPT-4 (H).
   - It was prompt-fragile: Claude 2.1 went from 27% to 98% with a one-line prompt edit [anthropic2023claude21prompting] (H).
   - It was also detectable: Claude 3 Opus flagged the needle as "artificially inserted" (H).
   - In 2025–26 NIAH appears only as figures (DeepSeek-V3, GPT-4.1), never as a table row in the 34-release matrix (H).

2. **Removing lexical overlap moves "effective context" by one to two orders of magnitude.**
   - NoLiMa's needles share minimal wording with the question. At 32K, 10 of 12 models fall below 50% of their short-context score, and GPT-4o drops from 99.3 to 69.7 [modarressi2025nolima] (H).
   - The same models look very different on RULER [D, from both READMEs]:

     | Model | RULER effective length | NoLiMa effective length |
     |---|---|---|
     | Gemini 1.5 Pro | >128K | 2K |
     | Llama 3.1 70B | 64K | 2K |
     | Command R+ | 32K | <1K |

   - Llama 4 Scout claims 10M tokens. Its NoLiMa effective length is 1K (H).
   - This is the long-context analogue of the MTOB example-copying confound [aycock2024grammarbook]. A surface match between query and material inflates apparent "use of context".
   - The *rank order*, however, survived in a small overlap (Spearman 0.89 between RULER-32K and NoLiMa-32K, N = 6, [D]). The shortcut mostly compressed headroom rather than scrambling ranks.

3. **Lab-owned synthetic generators persisted because they were re-parameterised, not because they resisted saturation.** Each lab's fixed configurations saturated fast:

   | Benchmark and setting | From | To | Interval |
   |---|---|---|---|
   | OpenAI-MRCR, 2-needle at 128K | 57.2% (GPT-4.1, Apr 2025) | 95.2% (GPT-5, Aug 2025) | 4 months |
   | Graphwalks BFS, <128K | 61.7% | 94.0% (GPT-5.2, Dec 2025) | 8 months |
   | Google MRCR v2, ≤128K | 58.0% (Gemini 2.5 Pro, Jun 2025) | 94.8% (GPT-5.5, measured by Google, May 2026) | 11 months |

   - The owners kept the brand alive by turning the knobs: 2 → 8 needles, a style dimension added to the keys, and bins extended to 1M (OpenAI) and 8M (Google's released data).
   - Scores at 1M remain low: Gemini 3.5 Flash 26.6%, GPT-5.5 74.0% on OpenAI's 512K–1M bin (H).
   - Both families stayed essentially single-lab in headline tables: Graphwalks is OpenAI-only and Google's MRCR v2 is Google-only. The public data nevertheless spread widely through harnesses (HELM, lm-eval-harness, NeMo, evalscope, openbench, Prime Intellect) (H).

4. **Synthetic recall predicts natural long-document tasks only moderately, and predicts ICL worst.**
   - HELMET's category correlation matrix gives Recall (JSON KV plus RULER MK/MV) vs RAG 0.87, Re-rank 0.86, Summ 0.87, LongQA 0.84 and Cite 0.74. Recall vs ICL is only 0.63, and ICL vs other categories is 0.36–0.59 [yen2025helmet] (H for the values; N is not printed on the figure).
   - HELMET's headline is that NIAH is "not a good predictor"; no synthetic task averaged Spearman >0.8 with real tasks (M; N≈35 per a secondary summary).
   - Michelangelo's three tasks correlate at only 0.64 (MRCR–Latent List), 0.043 (MRCR–IDK) and −0.25 (Latent List–IDK) across 10 models [vodrahalli2024michelangelo] (M-H).
   - Two creator-run synthetic tasks from the same lab rank models differently. On the GPT-4.1 page, MRCR vs Graphwalks gives Spearman 0.23 (N = 8, [D]): o1 scores 22.1 on MRCR but 62.0 on Graphwalks.

5. **Context length did not become a METR-style legible unit.**
   - Claimed windows plateaued at about 1M from Feb 2024 (Gemini 1.5) to 2026 (GPT-4.1, Opus 4.6 beta, Gemini 3.5 Flash) (H).
   - "Effective length" is task-relative (the NoLiMa vs RULER gaps above), and it is not anchored to humans.
   - Labs converged instead on per-bin curves and "context rot" language, with an AUC summary from Context Arena (L-M). There is no trend line comparable to METR's ~7-month doubling [kwa2025metr].

6. **The two survey claims hold, with scope conditions.**
   - *[akhtar2026plateau] (templated benchmarks saturate no slower).* This holds at the level of fixed configurations in this family. But Akhtar's 60 benchmarks contain **zero** procedurally generated long-context benchmarks, and "templated" is defined as surface literal diversity. The null result therefore does not test knob-bearing generators, which is the case that persisted (H).
   - *[stojanovski2025reasoninggym] (public generators become curricula).* This is confirmed directly:
     - BABILong ships a 5k-per-task training split [kuratov2024babilong] (H).
     - Fine-tuning on synthetic key-value retrieval transfers to real multi-document QA (+10.5 on 20-document MDQA) [xiong2024artificialneedles] (M-H).
     - Prime Intellect packaged Graphwalks, MRCR v2, Oolong, CL-bench and LongBench-Pro as RL-ready tasksets in Jun–Aug 2026 [primeintellect2026longcontext] (H).
     - Google says it "hill-climbed" on LOFT and MRCR-V2 [gemini2025gemini25] (H).
   - No evidence was found of a frontier lab *training on* OpenAI-MRCR or Graphwalks data (U).

7. **ICL benchmarks repeatedly collapsed into retrieval or copying.**
   - Many-shot classification ICL (LongICLBench and HELMET-ICL style) is "essentially retrieving similar exemplars": the Sample Learning Ratio is ≫1 [zou2025manyiclbench] (M).
   - Many-shot ICL performance peaks and then declines with more shots, and is order-sensitive [agarwal2024manyshot; yan2025mirbench] (H/M).
   - The closest 2026 analogue to the proposed design is CL-bench: expert-built fictional or modified knowledge. Frontier models average 17.2% there, the best (GPT-5.1) 23.7%, and context is ignored in 55–66% of failures. But it is LLM-judge-graded against rubrics and costs about 20 expert-hours per context [dou2026clbench] (M-H).

8. **Design consequence** [I]: the field's converged shortcut controls give a ready-made checklist (§Implications):
   - in-distribution near-duplicate distractors;
   - minimal literal overlap;
   - random or abstract labels;
   - a short-context or no-context baseline;
   - separate complexity and length knobs;
   - a published chance or noise floor;
   - an explicit tool policy;
   - a similar-exemplar ablation.

   Adoption evidence says a lab-legible headline also needs a public generator, a third-party runner, and a re-parameterisation path under one name.

---

## Findings

### F0. Lifecycle table (details and sources in F1–F17)

**Column key.**
- **Gen:** SP = synthetic procedural; NT = natural text; SP+NT = synthetic insertion into natural filler.
- **Grader:** Ex = exact, string or set metric; J = LLM judge.
- **Adoption:** headline-table releases from `model_cards_adoption.md`, plus additions found here.
- Confidence labels are in the detailed sections.

| Benchmark (creator, date) | Gen | Grader | Headroom at launch | Saturation / top | Shortcuts found | Generator as training data | Versions / successor | Adoption (tables; third party) | Last commit |
|---|---|---|---|---|---|---|---|---|---|
| NIAH (Kamradt, Nov 2023) | SP+NT | J (GPT-4) → Ex (v2) | GPT-4 fails ≥73K | >99% by Feb–Mar 2024 | Lexical overlap; OOD needle; 27→98% prompt artifact; needle detected | Used as fine-tuning baseline; KV-retrieval FT transfers | v2 2026 (uuid_chain) | 0 table rows; figures only | 8 Jun 2026 |
| RULER (NVIDIA, Apr 2024) | SP (+NT QA) | Ex | Top ≈96 avg; open models collapse at 64–128K | Frontier ≈96 by Aug 2024 | VT = multi-needle; CWE/FWE by frequency; leaked QA; easy defaults | Not verified (U) | RULER v2 (Oct 2025) | 0 frontier; open-weight tech reports; HELMET Recall | 22 Jul 2026 |
| NoLiMa (Adobe/LMU, Feb 2025) | SP+NT | Ex | GPT-4o 69.7 at 32K | Not saturated (o3 58.5 Hard @32K) | Designed control for literal match | — | NoLiMa-Hard | 0 tables | 17 Jul 2025 |
| HELMET (Princeton/Intel, Oct 2024) | mixed | Ex + J (summ) | Open ≪ closed | Not reported | Random-int ICL labels as control | — | LongProc | 0 tables; academic | 19 Sep 2026 |
| LongBench v1 (THUDM, Aug 2023) | NT (+3 SP) | Ex/F1/ROUGE | — | — | Parametric leakage (100-LongBench) | — | v2 | — | — |
| LongBench v2 (THUDM, Dec 2024) | NT | Ex (MCQ, 25% floor) | Best 50.1 / o1-prev 57.7 vs human 53.7 | ≈65 by Jun 2025 | Baseline knowledge not separated | — | LongBench-Pro | D1, X1 | 15 Jan 2025 |
| LOFT (GDM, Jun 2024) | NT corpora | Ex | — | Hard ≤128K 87.0 (Jun 2025) | Public corpora (leakage) | Hill-climbed by owner | — | G1 only | 13 Jun 2025 |
| Michelangelo (GDM, Sep 2024) | SP (LSQ) | Ex/approx | All drop before 32K | MRCR spun out; LL/IDK dropped | Designed against short-circuiting | "Not intended for training" | MRCR-V2 | Only MRCR used | (eval_hub 2026) |
| OpenAI-MRCR (OpenAI, Apr 2025) | SP | Ex (SequenceMatcher + hash) | 57.2 (2-needle 128K) | 95.2 by Aug 2025 → v2 8-needle; 1M still 74.0 | Tools trivialise; ~5% wrong GT (fixed v2) | Prime taskset | MRCR v2 (Dec 2025) | O2, O6, O8, O9, X1 (+GPT-5 dev, 5.4 mini); many harnesses; Context Arena | HF (U) |
| Graphwalks (OpenAI, Apr 2025) | SP | Ex (set F1) | 61.7 (BFS <128K) | 94.0 by Dec 2025 → 256K–1M bins | REPL-solvable; ambiguous depth prompt; self-including answers | Prime taskset | bins re-cut; metric → F1 | O2, O6, O8, O9 only (+GPT-5 dev, 5.4 mini); lm-eval, NeMo | HF (U) |
| GDM MRCR v2 (Google, Jun 2025) | SP | Ex | 58.0 ≤128K / 16.4 1M | ≤128K 94.8 (GPT-5.5); 1M flat ≈26 | Floors 15–51%; tools | Hill-climbed; generator public 2026 | "GDM-MRCR v2" | All 5 Google releases; HELM; Context Arena | eval_hub 19 Feb 2026 |
| BrowseComp LC (OpenAI, Aug 2025) | NT (search results) | Ex | 80–90 at 128K | Saturated at launch | Non-discriminating at 128K | — | — | O6 (+GPT-5 dev); dropped | HF (U) |
| Fiction.LiveBench (fiction.live, 2025) | NT | unclear | — | o3 100 at 120K | Tiny N (36 questions) | — | dated editions | 0 tables; Epoch mirror | n/a |
| AA-LCR (Artificial Analysis, 2025) | NT | J | GPT-5 76 (Oct 2025) | Unsaturated | 16 keys wrong; grader swaps | — | v1.1 (Sep 2026) | X2; AA Index 5% | n/a |
| BABILong (AIRI et al., Jun 2024) | SP+NT | Ex | GPT-4 degrades beyond 10% of window | U | Leaked bAbI base | **Ships training split** | — | 0 tables | 1 Jun 2026 |
| Many-shot ICL (GDM, Apr 2024) | NT tasks | Ex | Gains +few→many | n/a (method) | Order sensitivity; peaks then declines | — | → LOFT/HELMET ICL | 0 | n/a |
| LongICLBench (TIGER-Lab, Apr 2024) | NT classif. | Ex | Declines with #labels | U | ≈ similar-sample retrieval (SLR) | — | ManyICLBench | 0 | 20 Feb 2025 |
| MIR-Bench (Yan et al., Feb 2025) | SP (functions) | Ex | o1 79.65 avg | Declines ≥1K shots | Generators public | Curriculum-ready | — | 0 | U |
| LMAct (GDM, Dec 2024) | SP (envs) | Ex (reward) | Rarely expert | U | Demos often don't help | — | — | 0 | archived Jul 2026 |
| CL-bench (Tencent/Fudan, Feb 2026) | NT expert-authored novel | J (rubrics) | Best 23.7 | Unsaturated | Context ignored 55–66% | Prime taskset | CL-bench Life | 0 | 9 May 2026 |

### F1. Needle-in-a-Haystack (NIAH): viral, saturated, discredited as a measure, but still alive as a tool

**Creator and date.**
- Greg Kamradt. The first public runs were GPT-4-128K on 8 Nov 2023 and Claude 2.1 on 21 Nov 2023 (README "Original story & historical results") [kamradt2023niah] (H).

**Generation method.**
- Synthetic insertion of one fact into natural filler (Paul Graham essays) at a grid of context lengths × depths.
- The GPT-4 run used 15 depths × 15 lengths (1K–128K), plus "2x tests … for larger contexts". The Claude 2.1 run used 35 × 35, with sigmoid-spaced depths (H, from the original figures in the repo).
- The canonical needle was "The best thing to do in San Francisco is eat a sandwich and sit in Dolores Park on a sunny day." The question was "What is the most fun thing to do in San Francisco?" (quoted by Anthropic) [anthropic2023claude21prompting] (H).
- The question and needle share "San Francisco" and "thing to do": a literal-overlap design [I].

**Grader.**
- The original runs were LLM-judged: the Claude 2.1 figure says "The output was evaluated (with GPT-4) for accuracy" (H).
- The v2 rewrite (May 2026) uses exact-match and hop-count scorers (H, README).

**Headroom at launch.**
- GPT-4-128K "started to degrade at large context lengths when the fact was placed between 10%-50% document depth". Failing cells begin at 73K–82K (H, figure).
- Claude 2.1's accuracy "progressively decreased as context lengths increased" (H, figure).

**Saturation.** Frontier saturation came within about 3–4 months:
- Gemini 1.5 Pro reported "near-perfect 'needle' recall (>99.7%) up to 1M tokens" and 99.2% at 10M (Feb 2024 version; report PDF updated May 2024). It reported 100% up to 530K, against Claude 2.1's 98% at 200K [gemini2024gemini15] (H).
- Claude 3 (4 Mar 2024): Opus reached "near-perfect recall, surpassing 99% accuracy" with "one of 30 random needle/question pairs per prompt" on "a diverse crowdsourced corpus" [anthropic2024claude3] (H).
- RULER (Apr 2024): "Despite achieving nearly perfect performance on the vanilla needle-in-a-haystack (NIAH) test, most models exhibit large degradation" on RULER [hsieh2024ruler] (H).
- HELMET: "most LCLMs achieve perfect NIAH scores" [yen2025helmet] (M-H, project-page capture).
- GPT-4.1 (14 Apr 2025): its "internal needle in a haystack eval" retrieves the needle "at all positions … up to 1M" [openai2025gpt41] (H, mirror).

**Artifacts and critiques, with numbers.**
- *Prompt artifact.*
  - Claude 2.1 declined to answer from an out-of-place sentence. The Anthropic fix, "a simple prompt adjustment improving accuracy from 27% to 98%", is a 71-point swing from prompt wording alone (Dec 6, 2023) [anthropic2023claude21prompting] (H).
  - Gemini 1.5 likewise warned that "future versions of 'needle(s)-in-a-haystack' style tests should account for prompt robustness" (H).
- *Detectability and evaluation awareness.* Claude 3 Opus "identified the limitations of the evaluation itself by recognizing that the 'needle' sentence appeared to be artificially inserted" [anthropic2024claude3] (H).
- *Lexical matching.*
  - NoLiMa: in NIAH-style benchmarks "models can exploit existing literal matches between the needle and haystack" [modarressi2025nolima] (H). See F3.
  - Chroma's "Context Rot" report (14 Jul 2025, 18 models) found that lower needle–question semantic similarity makes degradation with length steeper. It also found models do *better* on shuffled than on coherent haystacks [hong2025contextrot] (M, two secondary copies).
- *Out-of-distribution haystacks.* Michelangelo: inserting "dramatically out-of-distribution context … such as Paul Graham essays … makes the problem significantly easier", because the relevant information is "a priori identifiable" [vodrahalli2024michelangelo] (M-H, parsed copy).
- *Resolution.* A single needle/question pair swept over 225 cells gives many correlated trials of one item. Claude 3's 30-pair variant was the first public fix [I from H facts].

**Launch-material use.**
- Gemini 1.5 made NIAH its Figure 1, across text, video and audio (H).
- Claude 3 used it in text (H).
- DeepSeek-V3 (Dec 2024) showed a NIAH figure, "performs well across all context window lengths up to 128K" [deepseek2024v3] (H).
- GPT-4.1 showed a figure (H).
- NIAH is **not a row in any of the 34 headline tables** (Dec 2024–Sep 2026) in `model_cards_adoption.md` (H, derived from that dossier's lists).

**Generators as training data.**
- NIAH-style data was used as a fine-tuning baseline, and synthetic key-value retrieval fine-tuning "significantly improves" retrieval on real tasks: GPT-3.5 Turbo gained +10.5 on 20-document MDQA at position 10 [xiong2024artificialneedles] (M-H, two digests).

**Versions and maintenance.**
- A v2.0.0 rewrite was merged on 30 May 2026. It adds a `uuid_chain` multi-hop task that "does not reveal the chain structure" and exact recipe reconstruction. The last commit was 8 Jun 2026 (M, WebFetch of commits page; H for the README content).
- About 2.4k GitHub stars (M).

### F2. RULER: configurable synthetic tasks and "effective context length"

**Creator and date.** Hsieh, Sun, Kriman, Acharya, Rekesh, Jia, Zhang, Ginsburg (NVIDIA), arXiv:2404.06654, April 2024 [hsieh2024ruler] (H, README BibTeX).

**Method.**
- 13 synthetic tasks in 4 categories (H):
  - retrieval: NIAH variants with multi-key, multi-value and distractor needles;
  - multi-hop tracing: variable tracking;
  - aggregation: common- and frequent-word extraction;
  - QA: SQuAD or HotpotQA with filler.
- Every task has configurable complexity knobs, e.g. `num_needle_k`, `num_hops` and `alpha` (H).
- Grader: exact or recall-based (H).

**Unit.**
- "Effective length" is the longest length at which a model exceeds a fixed threshold: Llama-2-7B's score at 4K (85.6%).
- Under that threshold, "only half of them can effectively handle sequence length of 32K", and "almost all models fall below the threshold before reaching the claimed context lengths" (H).

**Headroom at launch and saturation.**
- The top commercial model already averaged about 96: Gemini-1.5-Pro 95.8 average and 94.4 at 128K; Jamba-1.5-large 96.0 average and 95.1 at 128K (Jamba results are author-reported, Aug 2024) (H for values).
- Open models collapsed at 64–128K, e.g. Mistral-Large-2407 23.7 at 128K and DBRX 0.0 (H).
- RULER was therefore saturated for the frontier almost immediately. It discriminated among open-weight models [I].

**Self-declared limitation.** The 13 configurations were chosen because "most models can achieve good (some almost perfect) performance at short context size"; harder configurations were "not stress test[ed]"; RULER "cannot replace the more preferred realistic tasks" (H).

**Shortcuts found by others.** Michelangelo, Appendix D [vodrahalli2024michelangelo] (M-H):
- In default Variable Tracking "every variable which has been introduced in the context actually indeed has the value 3". The task "reduce[s] to a multi-needle retrieval task", hence "exceedingly high performance".
- CWE/FWE can be solved by frequency without "fine-grained counting".
- The QA tasks use "likely leaked questions from SQuAD and HotpotQA".
- Paul Graham filler is out-of-distribution.

**Adoption.**
- Open-weight tech reports supplied scores the README relays "reported by authors": Jamba 1.5, Qwen2.5-1M, Qwen3, EXAONE 4.0 (H).
- RULER is not in any frontier-3 headline table (H, matrix).
- It is embedded in HELMET's Recall category (RULER MK-2, MK-3, MV, plus JSON KV at 128K; `configs/recall.yaml`) (H).

**Versions and maintenance.**
- RULER v2 was added on 9 Oct 2025 through NVIDIA NeMo-Skills (`rulerv2-ns` branch). The last commit was 22 Jul 2026 (M for dates, WebFetch; H for branch READMEs).

### F3. NoLiMa: the lexical-overlap control, and the MTOB parallel

**Creator and date.** Modarressi, Deilamsalehy, Dernoncourt, Bui, Rossi, Yoon, Schütze (Adobe Research / LMU), arXiv:2502.05167, ICML 2025 [modarressi2025nolima] (H, README BibTeX).

**Method.**
- A curated needle set in which "questions and needles have minimal lexical overlap, requiring models to infer latent associations", placed in filtered, shuffled haystacks.
- The base score is accuracy at 250–1K tokens. Effective length is the longest context keeping ≥85% of the base score (H).

**Size of drops (README table)** (H):

| Model | Base score | Score at 32K | Effective length |
|---|---|---|---|
| GPT-4.1 | 97.0 | 79.8 | 16K |
| GPT-4o | 99.3 | 69.7 | 8K |
| Llama 3.3 70B | 97.3 | 42.7 | 2K |
| Gemini 1.5 Pro | 92.6 | 48.2 | 2K |
| Claude 3.5 Sonnet | 87.6 | 29.8 | 4K |
| Llama 4 Scout (10M claimed) | 81.7 | 21.6 | 1K |
| Gemma 3 4B | 73.6 | 0.9 | <1K |

- NoLiMa-Hard (10 hardest pairs, 32K): o3 100.0 → 58.5; Gemini 2.5 Pro 99.1 → 58.6; o4-mini 99.6 → 11.7 (H).
- Restoring literal matches "recovers near-baseline accuracy even at 32K". Literal-match *distractors* "severely impair" accuracy (M, search-engine summaries of the paper).

**Comparison with RULER on the same models.** Six-model overlap: Llama 3.1 70B and 8B, Gemini 1.5 Pro, Jamba 1.5 Mini, Command R+ and Mistral Large 2407. "Command R+" is version-ambiguous. All figures are [D]; the ranks hold with low power:

| Comparison | Spearman | Pearson | p (Spearman) |
|---|---|---|---|
| RULER 32K vs NoLiMa 32K | 0.89 | 0.77 | 0.02 |
| RULER 128K vs NoLiMa 32K | 0.71 | 0.55 | 0.11 |

- The *level* differs enormously: RULER-32K spans 87–96 while NoLiMa-32K spans 7–48.
- [I] Removing lexical overlap mainly restores **headroom and scale**. In this small sample it does not reorder models.

**MTOB parallel** [I]:
- MTOB's apparent "learning from a grammar" came "almost all" from copying the book's parallel examples [aycock2024grammarbook] (H via survey).
- NIAH's apparent "use of 1M context" came largely from literal matching.
- In both cases the fix is a paired control that removes the surface route: NoLiMa's non-literal needles, and Aycock's explanation-vs-examples ablation.
- The size of the effect is comparable in kind. GPT-4o's effective length falls from "passes NIAH at 128K" to 8K. MTOB-style gains collapse without the parallel sentences.

**Maintenance.** The last commit was 17 Jul 2025, adding o3 and o4-mini results (M). The benchmark is not in any lab headline table (H, matrix).

### F4. HELMET: synthetic vs downstream correlations, and ICL as the odd one out

**Creator and date.** Yen, Gao, Hou, Ding, Fleischer, Izsak, Wasserblat, Chen (Princeton and Intel), arXiv:2410.02694, ICLR 2025 [yen2025helmet] (H).

**Method.**
- Seven application-centric categories up to 128K: Recall, RAG, Re-rank, Cite, LongQA, Summ, ICL (H).
- Recall = RULER MK-2, MK-3, MV and JSON KV (synthetic) (H, config).
- ICL = 5 many-shot classification sets at thousands of shots: TREC coarse (6,600 shots), TREC fine, BANKING77, CLINIC150, NLU (H, config).
- By default the ICL labels are **mapped to random integers** ("we map the labels to a random integer"), so the model cannot use label semantics and must learn the mapping in context (H, `data.py`).
- Summarisation uses model-based evaluation, i.e. an LLM judge (H, README).

**Findings.** The project page (final version) says "Through a comprehensive study of 59 LCLMs, we find that":
1. "synthetic tasks like NIAH are not good predictors of downstream performance";
2. "the diverse categories in HELMET exhibit distinct trends and low correlation with each other";
3. "while most LCLMs achieve perfect NIAH scores, open-source models significantly lag behind closed ones when the task requires full-context reasoning" (M-H: page capture in a third-party repo, consistent with the search summary).

**Correlations (Spearman; README figure `task_correlation.png`)** (H for values; N not printed on the figure):

| Pair | ρ |
|---|---|
| Recall–RAG | 0.87 |
| Recall–Summ | 0.87 |
| Recall–Re-rank | 0.86 |
| Recall–LongQA | 0.84 |
| Recall–Cite | 0.74 |
| **Recall–ICL** | **0.63** |
| RAG–LongQA (highest pair) | 0.93 |
| ICL–RAG | 0.59 |
| ICL–LongQA | 0.58 |
| ICL–Re-rank | 0.47 |
| ICL–Summ | 0.39 |
| ICL–Cite | 0.36 |

- Per the arXiv v1 summary, synthetic-vs-real Spearman was computed over **35 instruction-tuned models**. "None of the synthetic tasks achieves an average correlation higher than 0.8", original NIAH is "≤0.8" with all real categories, and RULER MK and JSON KV correlate best (M, search summary).
- [I] Two readings follow:
  - Harder synthetic recall is a *reasonable but imperfect* proxy for natural long-document tasks (ρ ≈ 0.74–0.87).
  - Many-shot ICL, with abstract labels, is the most distinct long-context capability. That supports a learning-from-context construct being off the recall factor. It also warns that its reliability must be established first (brief D, T5).

**Maintenance and successor.**
- The last commit was 19 Sep 2026 (M).
- LongProc (arXiv:2501.05414), a benchmark of long procedural *generation*, is hosted in the same repo (H).
- HELMET is not in any lab headline table (H, matrix).

### F5. LongBench (v1) and LongBench v2: natural text, fixed length, MCQ

**LongBench v1.**
- Bai et al. (THUDM/Zhipu), arXiv:2308.14508, ACL 2024 [bai2024longbench] (H).
- 21 tasks in 6 categories, 4,750 test items, with average lengths mostly 5K–15K. It includes 3 synthetic tasks (passage count, passage retrieval EN/ZH) and a length-uniform LongBench-E (H).

**LongBench v2.**
- Bai et al., arXiv:2412.15204, released 20 Dec 2024 [bai2024longbench2] (H).
- 503 four-option MCQs over 8K–2M words, collected from "nearly 100 highly educated individuals". Human experts with search tools scored 53.7% under a 15-minute limit (H).
- At launch the best direct answer was 50.1%, and o1-preview reached 57.7%, "surpassing the human baseline by 4%" (H).
- **Grader:** exact MCQ letter, with a 25% chance floor [I].
- **Later scores:**
  - DeepSeek-V3 48.7 (Dec 2024) [deepseek2024v3] (H).
  - MiniMax-M1-40k 61.5 (Jun 2025) [minimax2025m1] (H).
  - 65.0 for the column I read as Gemini 2.5 Pro in the same table (M; column identity inferred from the table order).
  - The human baseline was passed at launch and headroom above it is modest [I].
- **Shortcut critique.** "100-LongBench" (arXiv:2505.19293; ACL Findings 2025) argues that de facto benchmarks, LongBench included, do not separate long-context ability from baseline and parametric knowledge. It proposes a length-controllable variant and a "LongScore", which shifts rankings [yang2025longbench100] (M, search summary).
- **Adoption.**
  - LongBench v2 appears in 2 headline tables, DeepSeek-V3 (D1) and MiniMax-M1 (X1), and DeepSeek dropped it for R1 (H, matrix).
  - A successor, LongBench-Pro (arXiv:2601.02872), exists as a Prime Intellect taskset (M; authorship not verified).
- **Maintenance.** The last commit was 15 Jan 2025 (M). The leaderboard site was unreachable (U).

### F6. LOFT (Google DeepMind): natural corpora in context, used once, then hill-climbed

**Creator and date.** Lee, Chen, Dai, Dua, Sachan, Boratko, Luan, Arnold, Perot, Dalmia, Hu, Lin, Pasupat, Amini, Cole, Riedel, Naim, Chang, Guu, "Can Long-Context Language Models Subsume Retrieval, RAG, SQL, and More?", arXiv:2406.13121, June 2024 [lee2024loft] (H, README BibTeX).

**Method.**
- 6 categories (retrieval, RAG, SQL, many-shot ICL, multimodal and others), 35 datasets, 4 modalities, and 32K/128K/1M splits.
- "Corpus-in-Context" prompting over public corpora (BEIR, etc.) (H).
- Grader: exact metrics such as recall@1 and EM (H).

**Use in Gemini 2.5 (Jun 2025)** [gemini2025gemini25] (H):
- LOFT hard-retrieval subset, 300 queries.
- Gemini 2.5 Pro scored 87.0% at ≤128K and 69.8% at 1M. o3-high scored 77.0%, o4-mini 60.5%, Claude 4 Sonnet 81.6% and Grok 3 Beta 73.1% at ≤128K.
- Google states: "When hill-climbing, we targeted challenging retrieval tasks (like LOFT …), long-context reasoning tasks (like MRCR-V2 …)". A lab optimising its model development against its own synthetic or semi-synthetic benchmarks is a documented Goodhart pathway [I].

**Leakage.** The corpora are public datasets, so parametric-knowledge leakage is uncontrolled [I]. Michelangelo notes that LOFT's SPIDER SQL task does test multi-hop reasoning (M-H).

**Adoption and maintenance.** LOFT appears once in the matrix (G1) and in no later Gemini table (H). The last commit was 13 Jun 2025 (M).

### F7. Michelangelo: latent-structure queries, and why only MRCR survived

**Creator and date.** Vodrahalli, Ontañón, Tripuraneni, Xu, Jain, Shivanna, Hui, Dikkala, Kazemi, Fatemi, Anil, Dyer, Shakeri, Vij, Mehta, Ramasesh, Le, Chi, Lu, Firat, Lazaridou, Lespiau, Attaluri, Olszewska (Google DeepMind / Google Research), arXiv:2409.12640, Sep 2024 [vodrahalli2024michelangelo] (M-H: full parsed copy; the ID is confirmed by the eval_hub README and the HELM code).

**Method: the Latent Structure Queries (LSQ) framework.**
- Build a latent structure. Mix *relevant* updates, whose count sets complexity, with *irrelevant* updates or filler, whose amount sets length, "decompos[ing] the difficulty … into two orthogonal components".
- The filler is "guaranteed to not impact the final answer", which ensures "no leakage from pretraining data" and "no short cuts".
- Three tasks:
  - **Latent List:** Python list operations, then a view query.
  - **MRCR:** multi-round coreference over near-duplicate writing requests. It was first introduced in the Gemini 1.5 report, scored by `difflib.SequenceMatcher` ratio, with 2,000 instances there [gemini2024gemini15] (H).
  - **IDK:** the answer is absent.
- The authors say the tasks are "not intended to be used for training prior to evaluation". The code task is "not intended to be run on a model which has access to a code editor" (M-H).

**Findings.**
- "All models experience significant fall off in performance before 32K" (M-H).
- Families specialise: "Gemini models perform the best on MRCR, GPT models outperform others on Latent List, and Claude-3.5 Sonnet performs the best on IDK" (M-H).
- Cross-task Spearman across **10 models**: MRCR–Latent List 0.64, MRCR–IDK 0.043, Latent List–IDK −0.25 (M-H; heatmap values from the parsed description).
- Perplexity-vs-length curves are "anti-correlated" with long-reasoning error, so perplexity "may not be a proxy" (M-H).

**Lifecycle.**
- Only **MRCR** reached headline tables: Google MRCR-V2 in G1–G4 and Gemini 3.5 Flash-Lite, and OpenAI's derivative. Latent List and IDK appear in no matrix table (H).
- The paper itself notes that "MRCR worked out of the box with no tweaks" for post-trained models, whereas "Latent List and IDK both required additional post-processing … due to variations in model output styles" (M-H).
- [I] The task that survived was the one with the cheapest, most robust scoring, and it was the most "retrieval-like" of the three. The most latent-structure-heavy task (Latent List) did not survive, although GPT-4o led it.

### F8. OpenAI-MRCR and Graphwalks (released with GPT-4.1, 14 Apr 2025)

**Release.**
- GPT-4.1's page open-sourced both [openai2025gpt41] (H, mirror): OpenAI-MRCR at `huggingface.co/datasets/openai/mrcr` [openai2025mrcr] and Graphwalks at `…/openai/graphwalks` [openai2025graphwalks].
- MRCR is described as "inspired by the MRCR eval first introduced by Gemini (arXiv:2409.12640v2)" (H, HELM scenario docstring quoting the dataset card).

**OpenAI-MRCR generation.**
- "Multi-turn synthetic conversations" in which the user asks for writing on a topic ("write a poem about tapirs"). "Two, four, or eight identical requests" are inserted, and the model must "retrieve the response corresponding to a specific instance (e.g., 'give me the third poem about tapirs')".
- Distractors are near-misses: "a short story about tapirs rather than a poem, or a poem about frogs" (H).
- Dataset: 2,400 samples. Prompts average about 944K characters (15K–5.2M). Bins run 4K–8K up to 512K–1M (M, evalscope card).
- [D] 3 needle counts × 8 bins × 100 = 2,400, consistent with 100 items per cell (M).
- Scoring: the model "must prepend an alphanumeric hash". If the hash is missing the score is 0; otherwise the score is the `SequenceMatcher` ratio (H, HELM metric docstring adapted from the dataset README).
- More than 180 code files on GitHub reference its `random_string_to_prepend` field. These include HELM, NVIDIA NeMo-Skills, evalscope, openbench and AISBench (H, code search count).

**Graphwalks generation.**
- "Fills the context window with a directed graph composed of hexadecimal hashes, and then asks the model to perform a breadth-first search (BFS) starting from a random node … return all nodes at a certain depth". A second variant asks for "parents".
- It is "designed to require reasoning across multiple positions in the context and cannot be solved sequentially" (H).
- Fields: `prompt`, `answer_nodes`, `prompt_chars`, `problem_type`. Scoring is node-set F1 or exact set match. There are 1,150 tasks (H for fields and scoring, from lm-eval-harness, openbench and Prime code; M for the count).

**Headroom at launch** (GPT-4.1 page) (H):
- MRCR 2-needle at 128K: GPT-4.1 57.2, o1-high 22.1, o3-mini-high 18.7, GPT-4.5 38.5. At 1M: GPT-4.1 46.3.
- Graphwalks BFS <128K: GPT-4.1 61.7, o1 62.0, GPT-4.5 72.3. At >128K: GPT-4.1 19.0.

**Trajectory and re-parameterisation:**

| Release | Date | Reported | Confidence |
|---|---|---|---|
| GPT-5 developer page | Aug 2025 | MRCR 2-needle 128K **95.2**, 256K 86.8; Graphwalks BFS <128K 78.3 [openai2025gpt5dev] | M-H, two independent copies |
| GPT-5.2 | 11 Dec 2025 | "OpenAI MRCRv2", 8 needles, "fixes ~5% of tasks that had incorrect ground truth": 4K–8K 98.2, 128K–256K 77.0; "first model … near 100% on the 4-needle MRCR variant (out to 256k)"; Graphwalks BFS <128K **94.0**, parents 89.0 [openai2025gpt52] | H |
| GPT-5.4 | 5 Mar 2026 | New 256K–1M bins: Graphwalks BFS 21.4, MRCR v2 512K–1M 36.6 [openai2026gpt54] | H |
| GPT-5.5 | 23 Apr 2026 | MRCR v2 512K–1M **74.0**; Graphwalks BFS "1mil f1" 45.4 (GPT-5.4 at 9.4 on this bin); columns for Claude Opus 4.7, e.g. Graphwalks BFS 256K 76.9 vs GPT-5.5 73.7 [openai2026gpt55] | H |

**Measurement defects found downstream.**
- NVIDIA's Graphwalks port preserves "two upstream-prompt corrections". The BFS prompt "is rewritten to disambiguate 'depth N' — without this rewrite, models often return nodes at intermediate depths". The "parents prompt sometimes includes the target node inside its own answer set" [nvidia2026nemogw] (H, code comment).
- Metric and bin definitions drift across releases: "accuracy" vs "f1"; "<128K" vs "0K–128K" vs "256k"/"1mil". GPT-5.4's own two pages disagree slightly (BFS 0–128K 93.0 vs 93.1) (H) [I: this complicates cross-release comparison].
- Tool-solvability: Prime Intellect's taskset has the agent "parse [the graph] from a REPL instead of spending tokens" [primeintellect2026longcontext] (H). A code tool turns Graphwalks into a trivial BFS [I].

**Adoption.**
- Headline rows: OpenAI-MRCR in O2, O6, O8, O9 and MiniMax-M1 (X1); Graphwalks in O2, O6, O8, O9 only [model_cards_adoption.md] (H).
- **Addition from this dossier:** both also appear on the GPT-5 developer page (Aug 2025) and the GPT-5.4 mini/nano page (17 Mar 2026) [openai2026gpt54mininano], which the matrix did not count (H/M-H).
- Anthropic cites "the 8-needle 1M variant of MRCR v2" in prose for Opus 4.6: 76% vs Sonnet 4.5 at 18.5% [anthropic2026opus46] (H). Which lab's MRCR v2 is meant is not stated (U).
- Third-party runners:
  - Context Arena (Dillon Uzar, from 24 Apr 2025) ran OpenAI-MRCR, later GDM-MRCR v2, across 77 model configurations by Jun 2026 [contextarena2025] (L-M, secondary).
  - HELM, NeMo, lm-eval-harness and openbench implement both (H).

### F9. Google DeepMind MRCR v2 (MRCR-V2, later "GDM-MRCR v2")

**Definition.**
- "A significantly harder instance of the MRCR family". It increases "the nesting of the dictionary size to depth 3 rather than 2 by including a style parameter (… 'write a poem about penguins in an archaic style')".
- The reported setting is 8-needle: "≤128K" cumulative plus "1M pointwise" [gemini2025gemini25] (H).

**Availability timeline.**
- The Gemini 3 Pro evaluation note (Nov 2025) says MRCR v2 was "not publicly available yet" [google2025gemini3eval] (H).
- The public bucket `storage.googleapis.com/mrcr_v2` holds 36 CSVs named `mrcr_v2p1_{2,4,8}needle_in_(…)` with bins up to (4,194,304, 8,388,608) tokens. The objects are last-modified 9 Jul 2025 (H, bucket listing).
- The code and README entered `google-deepmind/eval_hub` on 19 Feb 2026 [gdm2026mrcrv2] (M for the date, WebFetch of commit history; H for the README). The release includes generator code and distribution tests: "we also support generating your own versions of MRCR".

**Noise floors (from the README)** (H):
- A model that "reproduces any of the assistant responses uniformly at random" scores about 1%.
- A model that "reproduces one of the **relevant** … responses" scores about 51% (2-needle), 27% (4-needle) and 15% (8-needle).

**Tool caveat (from the README).** "If the model is given access to code tools, the task becomes considerably simpler. Any report of MRCR should explicitly state whether or not tools were provided" (H).

**Trajectory.** Google-run, from Gemini reports and model cards (H):

| Model | ≤128K | 1M |
|---|---|---|
| Gemini 1.5 Pro | 26.2 | 12.1 |
| Gemini 2.5 Pro (Jun 2025) | 58.0 | 16.4 |
| Gemini 3 Pro (Nov 2025) | 77.0 | 26.3 |
| Gemini 3.1 Pro (Feb 2026) | 84.9 | 26.3 |
| Gemini 3.5 Flash (May 2026) | 77.3 | 26.6 |
| Gemini 3.5 Flash-Lite (Jul 2026, labelled "GDM-MRCR v2") | 72.2 | 21.3 |

- Competitors as measured by Google:

  | Model | ≤128K | Source card |
  |---|---|---|
  | o3-high | 57.1 | Gemini 2.5 report |
  | Claude 4 Opus ("no thinking and API refusals") | 16.1 | Gemini 2.5 report |
  | Claude Sonnet 4.5 | 47.1 | Gemini 3 Pro card |
  | GPT-5.1 | 61.6 | Gemini 3 Pro card |
  | Sonnet 4.6 | 84.9 | Gemini 3.1 Pro card |
  | Opus 4.6 | 84.0 | Gemini 3.1 Pro card |
  | GPT-5.2 | 83.8 | Gemini 3.1 Pro card |
  | Opus 4.7 | 59.3 | Gemini 3.5 Flash card |
  | **GPT-5.5** | **94.8** | Gemini 3.5 Flash card |

  Competitors show "not supported" at 1M.
- [I] The ≤128K setting is near saturation; the 1M pointwise setting has been flat at about 26% for Google models for three releases, 11 points above the 8-needle relevant-needle floor.

**Adoption.** All 5 Google releases examined (G1–G4 plus 3.5 Flash-Lite), and no non-Google headline table (H). Third-party: Context Arena, HELM (`deepmind_mrcr_v2_scenario.py`) and Prime Intellect (H/M).

### F10. BrowseComp Long Context (OpenAI): saturated at launch, dropped after two releases

- **Release.** Open-sourced with GPT-5 (Aug 2025): "the model receives a user query, a long list of related search results, and must answer based on the search results". Answers are derived from BrowseComp [openai2025browsecomplc; wei2025browsecomp] (M-H: two independent copies of the GPT-5 developer page; the dataset path is `openai/BrowseCompLongContext`).
- **Scores at launch (128K):** GPT-5 90.0, GPT-5 mini 89.4, GPT-4.1 nano **89.4**, GPT-4.1 85.9, o4-mini 80.0. The range is 80–90, SD 3.8 [D]. At 256K the spread widens: 19.1 (GPT-4.1 nano) to 88.8 (M-H).
- **GPT-5.2 (Dec 2025):** 92.0 and 89.8 vs GPT-5.1's 90.0 and 89.5 (H). It is absent from the GPT-5.4 and GPT-5.5 tables (H).
- **Correlations on the GPT-5 page** (N = 8): Spearman with MRCR 0.29 and with Graphwalks 0.23 [D].
- [I] This is a natural-text, retrieval-dominated set that was already non-discriminating at its headline setting. It died quickly even though the owner ran it.

### F11. Fiction.LiveBench (fiction.live): natural narrative comprehension, third-party mirrored

- **Creator.** The fiction.live platform (individual author not named); launched early 2025 with dated editions (Feb, Mar and Apr 2025) [fictionlive2025] (M).
- **Method.** "36 questions over 30 long stories". Shortened versions of each story are made "from near-shortest to the original", tested at 0–120K and later 192K. The questions test theory of mind, chronology and implicit information (M, Epoch description via two secondary pages).
- **Grader.** Not documented ("Exact grading method (LLM-judge vs human) … not documented in reachable sources") (M, independent provenance audit).
- **Scores.** At 120K, o3 (medium) scored 100.0 and GPT-5 96.9; 43 models were listed on Epoch (L-M, secondary).
- **Adoption.** Epoch mirrors it ("We source the data directly from the Fiction.liveBench leaderboard") [epochHub; ainews2025epoch] (M). It appears in no lab headline table (H).
- [I] It is small (36 questions), its grading is unclear, and it is near ceiling at 120K for top reasoning models. It fails the resolution criteria in brief D (S3) even though it is natural and hard to shortcut.

### F12. Artificial Analysis AA-LCR: third-party, natural, judge-graded, maintained by patching

- **Creator and date.** Artificial Analysis. Added to the Intelligence Index around Aug–Sep 2025 (v2.2) [aa2026method; aa2025lcr] (M-H, AA methodology capture).
- **Method.** "100 hard text-based questions spanning 7 categories of documents". About 100K tokens (cl100k) of input per question, "~3M total unique input tokens spanning ~230 documents" (H-capture).
- **Grader.** An "Equality Checker LLM", pass@1 (H-capture). The grader model changed from Qwen3 235B A22B 2507 (non-reasoning) to GPT-5.6 Luna (medium) in v4.1.1.
- **v1.1 (Sep 2026).** "Adds a system prompt to clarify grading instructions, corrects 16 answer keys … Scores are not directly comparable with v1.0" (H-capture). That is **16% of items** re-keyed a year after launch [D].
- **Scores (AA numbers relayed in MiniMax-M2's README, Oct 2025):** GPT-5 (thinking) 76, DeepSeek-V3.2 69, Claude Sonnet 4.5 66, Gemini 2.5 Pro 66, MiniMax-M2 61, Kimi K2 0905 52 [minimax2025m2] (M).
- **Adoption.**
  - 5% weight in AA Intelligence Index v4.3 (H-capture).
  - One lab headline table, X2 (MiniMax-M2) (H, matrix).
  - At least 328 GitHub code hits, including Harbor adapters that "correct 2 known errors in the original dataset" (M).
  - AA also runs a medical variant, MLCR-AA (H-capture).

### F13. BABILong: generative reasoning-in-a-haystack, with an official training split

- **Creator and date.** Kuratov, Bulatov, Anokhin, Rodkin, Sorokin, Sorokin, Burtsev (AIRI, DeepPavlov, LIMS). Preprint Jun 2024; NeurIPS 2024 D&B [kuratov2024babilong] (H).
- **Method.** 20 bAbI tasks, with facts "hidden" among PG19 book sentences, at lengths 0–10M. Exact-answer scoring (H).
- **Headroom.** "Even models that claim to support 128K tokens, such as GPT-4 … experience degradation beyond 10% of their input capacity. RAG methods do not help, while fine-tuning of small scale models … shows that the tasks are solvable" (H).
- **Training data.** The repo ships "Training data … with 5000 samples per task and length" and a "Train your long-context model" notebook (H).
- **Critique.** Michelangelo says BABILong "may all suffer" from short-circuiting, because bAbI "is heavily leaked (as it is a famous evaluation from almost a decade ago)" and has known biases (Kaushik & Lipton 2018) (M-H).
- **Maintenance and adoption.** Leaderboard updates ran through Apr 2025. The last commit (1 Jun 2026) added Gemini 3 Flash results (M). It appears in no lab headline table (H).

### F14. ICL-specific benchmarks

**Many-shot ICL** (Agarwal, Singh, Zhang, Bohnet, Rosias, Chan, Zhang, Anand, Abbas, Nova, Co-Reyes, Chu, Behbahani, Faust, Larochelle, Google DeepMind; arXiv:2404.11018; NeurIPS 2024 per the paper's contribution statement) [agarwal2024manyshot] (H, parsed copy).
- Findings:
  - "significant performance gains" from few- to many-shot;
  - "Reinforced ICL" (model-generated rationales) and "Unsupervised ICL" work;
  - many-shot ICL is "effective at overriding pretraining biases" (flipped or abstract labels eventually approach default-label performance);
  - it "can learn high-dimensional functions with numerical inputs";
  - "next-token prediction loss" is not a good indicator of ICL performance.
- Caveats reported:
  - Performance "improves … up to a point, and then declines" (MATH peaks at about 125 shots; GPQA degrades at 250).
  - Repeating 25 examples to 1,000 shots "significantly lags" distinct examples.
  - Accuracy varies strongly across ten random orderings of the same 50 MATH examples, and "an ordering that excels in one subarea may perform poorly in another" (H for the qualitative claims; the figure's per-split values were not transcribed).
- Not a benchmark with a leaderboard. Its tasks fed LOFT, HELMET and LongBench-style ICL categories [I].

**LongICLBench** (Li, Zhang, Do, Yue, Chen; arXiv:2404.02060; TMLR 2025 per README) [li2024longiclbench] (H).
- 6 extreme-label classification sets (28–174 classes) at 2K–50K tokens; 13 models.
- Findings are qualitative: decline with task complexity; difficulty with 174 classes; "sensitive to the position of the instances in the demonstrations" (H).
- The last commit was 20 Feb 2025 (M).

**ManyICLBench / "On Many-Shot In-Context Learning for Long-Context Evaluation"** (Zou, Khalifa, Wang; arXiv:2411.07130; ACL 2025) [zou2025manyiclbench] (M, notes plus index).
- The Sample Learning Ratio drops the 10% most- vs least-similar exemplars. Classification ICL shows SLR ≫1: "similar-sample learning", i.e. retrieval.
- Math and summarisation show SLR ≈1: "all-sample learning". On these, models degrade from about 16K, against about 64K on SSL tasks (M).
- [I] This is the ICL counterpart of the MTOB copying confound.

**MIR-Bench** (Yan et al.; arXiv:2502.09933; NeurIPS 2025 per notes) [yan2025mirbench] (H README / M venue).
- Many-shot *inductive* reasoning over program-generated input→output functions. Ground-truth code and data generators were published (Feb 2025). Exact-match scoring; 21 models.
- Top MIR-Core average: o1-1217 79.65. Performance peaks around 32–256 shots and falls by 2,048 shots, e.g. DeepSeek-R1 from 75.5 to 38.8 (H).
- [I] This is the nearest existing *procedurally generated learn-a-function-from-examples* benchmark. It publishes its generators, which makes it curriculum-ready.

**LMAct** (Ruoss, Pardo, Chan, Li, Mnih, Genewein, Google DeepMind; arXiv:2412.01441; ICML 2025) [ruoss2025lmact] (H).
- 0 to 512 expert episodes in context (up to 1M tokens) across tic-tac-toe, chess, Atari, grid worlds, crosswords and a cheetah.
- "Models rarely manage to fully reach expert performance, and often, presenting more demonstrations has little effect" (H).
- Repository archived (read-only) by 24 Jul 2026 (M).

**CL-bench and CL-bench Life** (Dou et al. with Yao, Tencent Hunyuan and Fudan; arXiv:2602.03587, Feb 2026; Life arXiv:2604.27043, Apr 2026) [dou2026clbench] (H README).
- 500 expert-built contexts, 1,899 tasks and 31,607 rubrics, with "avg. 20 hours expert effort per context".
- Four categories: domain knowledge, rule systems, procedures, empirical discovery.
- Contexts are built by "fictional creation, modification of existing knowledge, or incorporation of niche and emerging specialized knowledge" (M, search summary).
- **Grader:** GPT-5.1 as judge, all-or-nothing over rubrics (H).
- **Results:** "ten frontier models average 17.2%; GPT-5.1 best at 23.7%". "Context ignored" occurs in 55–66% of outputs, and format errors in 33–46%. GPT-5.1 falls from about 30% at 0–4K tokens to about 16% at 32K+ (M-H, two independent secondary pages).
- **Maintenance:** last commit 9 May 2026 (M). Also packaged as a Prime Intellect taskset (H).

**MTOB as a "long-context" headline.** Llama 4's model card files MTOB under "Long Context" [meta2025llama4card] (H):

| Model | Half book (en→kgv / kgv→en chrF) | Full book (en→kgv / kgv→en chrF) |
|---|---|---|
| Llama 4 Scout | 42.2 / 36.6 | 39.7 / 36.3 |
| Llama 4 Maverick | 54.0 / 46.4 | 50.8 / 46.7 |

This is the only headline-table use of an in-context *learning* benchmark in the matrix (MTOB in M1).

### F15. Third-party runners and harnesses

| Runner | What it runs | Evidence |
|---|---|---|
| Artificial Analysis | AA-LCR (own; 5% of index), MLCR-AA | H-capture |
| Epoch AI Hub | Fiction.LiveBench (mirrored, not run) | M |
| Vals AI | No long-context benchmark found | U |
| Context Arena | OpenAI-MRCR → GDM-MRCR v2, 77 configurations; AUC@128K and AUC@1M. GPT-5.5 (medium) 87.5 → 50.9; Opus 4.6 (high) 76.8 → 46.9; Opus 4.7 AUC@1M ≈7.6 | L-M |
| HELM (Stanford CRFM) | OpenAI-MRCR, DeepMind MRCR v2 | H, code |
| EleutherAI lm-eval-harness | Graphwalks 128K and 1M | H |
| NVIDIA NeMo-Skills / NeMo Gym | MRCR, Graphwalks, RULER v2 | H |
| Prime Intellect prime-envs | Graphwalks, MRCR v2, Oolong (synth, real, pairs), CL-bench, LongBench-Pro, LongCoT, verbatim-copy, patterned-NIAH, all as agent-in-sandbox RL tasksets (Jun–Aug 2026) | H |

- [I] Cross-lab inconsistency is visible. Opus 4.7 scores 59.3 (Google MRCR v2 ≤128K, Google-run), 59.2 at 128–256K and 32.2 at 512K–1M (OpenAI MRCR v2, OpenAI-run), and about 7.6 AUC@1M (Context Arena). Opus 4.6 scores 76% on "8-needle 1M" (Anthropic-run).
- On the same Google benchmark, measured by Google, Opus 4.6 → Opus 4.7 falls from 84.0 (Gemini 3.1 Pro card) to 59.3 (Gemini 3.5 Flash card). Over the same pair of cards, HLE (no tools) rises from 40.0 to 46.9 (H for values).
- OpenAI's GPT-5.5 table also puts Opus 4.7 far below GPT-5.5 at 512K–1M (32.2 vs 74.0). Anthropic reported 76% for Opus 4.6 at 8-needle 1M. The direction is consistent, but the harnesses differ (L-M).
- [I] Long-context retrieval can move against general capability. This is a discriminant datum any "learning from material" construct should expect to reproduce.

### F16. Did synthetic generators become training data? (evidence for [stojanovski2025reasoninggym])

| Evidence | Direction | Confidence |
|---|---|---|
| BABILong ships a 5k-per-task-and-length training split and a training notebook | Confirms | H |
| Synthetic numerical key-value retrieval fine-tuning (GPT-3.5 Turbo, Mistral 7B) transfers to real tasks (+10.5 MDQA-20 at position 10); "synthetic data was more effective than directly finetuning on the target dataset" | Confirms (generators as curricula work) | M-H |
| Prime Intellect converts Graphwalks, MRCR v2, Oolong, CL-bench and LongBench-Pro into verifiers tasksets (initial versions 24 Jun 2026) for its environment hub | Confirms (packaged as RL environments) | H |
| GDM releases MRCR generator code with distribution tests | Enables | H |
| Gemini 2.5 "hill-climb[ed]" on LOFT and MRCR-V2 | Confirms that labs optimise against their own synthetic evaluations | H |
| Michelangelo authors: "not intended to be used for training prior to evaluation" | Intent against | M-H |
| Direct evidence that a frontier lab trained on OpenAI-MRCR or Graphwalks data | None found | U |

### F17. Saturation vs [akhtar2026plateau]

- **Scope.** Akhtar's Table 3 lists 60 benchmarks. None is NIAH, RULER, MRCR, Graphwalks, LongBench, LOFT, BABILong or HELMET; the only long-document one is QuALITY. "Templated" is defined as "Whether prompts use templated structures (e.g., 'What is the capital of ___?') vs. natural variation". The authors note "fully synthetic benchmarks currently exhibit low saturation but are also relatively recent" (H).
- **Within this family** (fixed configurations):

  | Configuration | Time to saturation (≥90% or non-discriminating) | Confidence |
  |---|---|---|
  | NIAH | about 3 months | H |
  | RULER default suite (frontier) | ≤4 months | H/M |
  | BrowseComp LC 128K | 0 months | M-H |
  | OpenAI-MRCR 2-needle 128K | 4 months | M-H |
  | Graphwalks <128K | 8 months | H |
  | GDM MRCR v2 ≤128K | ~11 months | H |
  | LOFT hard ≤128K | 87% at 12 months | H |

  Natural sets saturated too:

  | Natural set | What happened | Confidence |
  |---|---|---|
  | LongBench v2 | Passed the 15-minute human baseline at launch | H |
  | Fiction.LiveBench 120K | 100% for o3 within months | L-M |

- **Families with knobs:** MRCR and Graphwalks remained informative after 12–17 months by adding needles, bins and style depth. The 1M settings are still ≤75% (H).
- **Verdict** [I]:
  - The claim is **confirmed for configurations**: procedural generation per se did not slow saturation.
  - It is **not tested for families**, and here the evidence points the other way. The generator's *difficulty knob* let the name survive, as `model_cards_adoption.md` predicted ("ship with a difficulty knob and a version roadmap under one stable name").

### F18. Answers to the four questions

**Q1. Which synthetic in-context benchmarks stayed informative and adopted, and which saturated or were discredited? What separates them?**

*Stayed informative and in headline tables into 2026:*
- OpenAI-MRCR (v1 → v2), Graphwalks and GDM MRCR v2 (H).
- AA-LCR, a natural set run inside a third-party index (H).
- RULER stayed in open-weight tech reports through 2025 but never entered frontier tables (H).

*Saturated, faded or discredited:*
- NIAH: saturated in about 3 months, lexically shortcuttable, prompt-fragile.
- BrowseComp LC: non-discriminating at launch, dropped after 2 releases.
- LOFT: one release.
- Michelangelo's Latent List and IDK: never adopted.
- BABILong: leaked base.
- LongICLBench-style classification ICL: collapses to retrieval.
- NoLiMa and HELMET remain academic diagnostics without table uptake.

*What distinguishes the survivors* [I, from H facts]:
1. **Latent-structure inference vs retrieval is not the discriminator.**
   - MRCR is ordinal retrieval plus verbatim copying.
   - Latent List, the most latent-structure-heavy task, did not survive.
   - Graphwalks survived as algorithmic multi-hop, but it is REPL-trivial with tools.
2. **Distractor design is a discriminator.**
   - MRCR's distractors are in-distribution near-duplicates (same topic, different format; same format, different topic; later, a style axis). Lexical matching cannot locate the needle.
   - NIAH's needle was out of place and lexically matched to the question.
3. **The difficulty knob is the strongest discriminator.** Every survivor was re-parameterised upward when its headline setting saturated:
   - needles 2 → 8;
   - bins 128K → 256K–1M (OpenAI) and up to 8M (GDM data);
   - key depth 2 → 3 (style).
   - Fixed-setting sets (BrowseComp LC, LOFT hard, NIAH) died.
4. **Creator-run evaluation matters for *headline* persistence.**
   - Graphwalks appears only in OpenAI tables and GDM MRCR v2 only in Google tables, including Google measuring GPT-5.5 on it.
   - These are the labs selling 1M-token windows. The benchmarks measure the product claim, and the owners "hill-climb" on them [gemini2025gemini25].
   - Cross-lab spread happened through public data and harnesses, not tables.
5. **Cheap, judge-free scoring that "worked out of the box"** (MRCR vs Latent List and IDK).

**Q2. How well do synthetic in-context scores predict natural long-document performance and general capability?**

| Evidence | Correlation | N | Confidence |
|---|---|---|---|
| HELMET, synthetic Recall vs natural categories (RAG, Re-rank, LongQA, Summ, Cite) | 0.74–0.87 | N not printed; 59 models in study | H values |
| HELMET, synthetic Recall vs many-shot ICL | 0.63 | same | H |
| HELMET, ICL vs natural categories | 0.36–0.59 | same | H |
| HELMET, original NIAH vs real tasks | ≤0.8 each; no synthetic task averages >0.8 | ≈35 instruction-tuned models | M |
| Michelangelo, cross-task (synthetic vs synthetic) | 0.64 / 0.043 / −0.25 | 10 | M-H |
| RULER-32K vs NoLiMa-32K | 0.89 (Spearman), 0.77 (Pearson) | 6 | [D] |
| OpenAI-MRCR vs Graphwalks (GPT-4.1 page) | 0.23 | 8 | [D] |
| OpenAI-MRCR vs Graphwalks (GPT-5 page) | 0.61 | 8 | [D] |
| BrowseComp LC vs MRCR and Graphwalks | 0.29 / 0.23 | 8 | [D] |

- *General capability:* no published correlation between an MRCR-family score and a general index was found (U).
- The discriminant datum: Opus 4.6 → 4.7 fell 84.0 → 59.3 on GDM MRCR v2 while HLE rose 40.0 → 46.9, both Google-measured (H).
- Reasoning models (o1, o3-mini) scored 18–22 on MRCR but 51–62 on Graphwalks (H).
- [I] Synthetic recall is a moderate proxy for natural long-document QA and RAG, a weak proxy for ICL, and not a proxy for general capability.

**Q3. Did "context length" work as a legible unit, as METR's human-minutes did?** Only partly, and not as a trend unit [I, from H facts]:
- **What worked.**
  - It worked as *marketing* (1M, 2M and 10M windows) and as the x-axis of every lab chart: per-bin MRCR and Graphwalks rows, "context rot".
  - RULER's and NoLiMa's "effective length" gave a single number.
- **Why it failed as a trend unit.**
  1. Claimed windows plateaued around 1M from Feb 2024 (Gemini 1.5) to 2026 (GPT-4.1 1M; Opus and Sonnet 4.6 1M beta; Gemini 3.5 Flash 1M) (H). There is no doubling trend to report.
  2. Effective length is task-relative. For the same six models it differs between RULER and NoLiMa by 16× (Mistral Large 2407: 32K vs 2K) to more than 128× (Jamba 1.5 Mini: >128K vs <1K). Gemini 1.5 Pro goes from >128K to 2K, and Llama 4 Scout's claimed 10M becomes 1K (H values; ratios [D]).
  3. It has no human anchor. METR fits P(success) against log2 of *human* minutes [kwa2025metr]; nothing comparable exists for tokens.
  4. Scores at a given length depend on needle count, style depth and tool access. GDM itself says tool and no-tool results are "not meaningful" to compare.
- Third parties converged on area-under-curve summaries (Context Arena AUC@128K and AUC@1M) (L-M) rather than a single effective length.

**Q4. Which shortcut controls did the field converge on, and which should a "learn a novel system from provided material" benchmark adopt?**

*Converged on*, meaning at least two independent groups use each:

| Control | Where it is used |
|---|---|
| In-distribution near-duplicate distractors | MRCR v1 and v2; Michelangelo; NoLiMa distractor variants; Context Rot |
| Multiple needles with ordinal or relational disambiguation | MRCR; RULER MK and MV; Gemini 1.5's 100-needle test |
| Minimal literal overlap between query and evidence | NoLiMa; Context Rot similarity bands |
| Short-context baseline normalisation | NoLiMa base score; 100-LongBench LongScore; Michelangelo complexity–length decomposition |
| Abstract or random labels | HELMET ICL; many-shot flipped labels |
| Answer-certifying prefix hash and exact string scoring | MRCR |
| Published noise and chance floors | GDM MRCR; Michelangelo App. B |

*Not converged:*
- tool policy (GDM asks for disclosure; Prime runs REPL agents);
- judge vs exact grading for natural sets (AA-LCR, CL-bench and HELMET-summ use judges);
- position sweeps (NIAH depth heatmaps faded).

*Adopt for the proposed benchmark:* see §Implications 1–8. The additions specific to "learning" are:
- the example-vs-explanation factorial [aycock2024grammarbook];
- the similar-exemplar ablation [zou2025manyiclbench];
- composition items;
- a closed-book floor.

---

## Implications for designing a new benchmark

These apply to a procedurally generated "learn a novel system from provided material" benchmark. All are [I], grounded in the findings above.

1. **Build the lexical-overlap control in, not after.**
   - Generate query items whose surface strings do not appear in the material (NoLiMa). Pair each with a "literal" twin in which the relevant rule or example shares tokens with the query.
   - Report the literal − non-literal gap as a first-class number.
   - NoLiMa's own base-to-32K drops are 30–83 points (GPT-4o 99.3→69.7; Command R+ 90.9→7.4). On the six models shared with RULER, RULER-32K minus NoLiMa-32K is 48–85 points, and effective length shrinks 16× to more than 128× ([D]; the tasks differ, so this is not a clean paired gap).

2. **Control example-copying three ways** (Aycock plus ManyICLBench):
   - (a) Factorial material conditions: rules-only, examples-only, both.
   - (b) An SLR-style ablation: remove the k% of worked examples most similar to each test item and report the drop.
   - (c) Composition items whose answer requires combining ≥2 rules never co-occurring in any example.
   - Without (b) and (c), a "learning" score may be similar-exemplar retrieval, as it was for many-shot classification.

3. **Kill parametric priors with abstract symbols and a no-material baseline.**
   - Use random identifiers for the novel system's tokens and labels (HELMET's random-integer labels; many-shot label-flip).
   - Always run a closed-book condition.
   - The target is a closed-book score at chance. Report it as the floor.

4. **Separate complexity from length, and give both knobs a versioning plan.**
   - Borrow Michelangelo's decomposition: the number of *relevant* rules or updates sets complexity, and irrelevant but in-distribution material sets length.
   - Pre-declare the harder settings, which RULER did not.
   - MRCR and Graphwalks survived only because their owners could re-parameterise (2→8 needles, 128K→1M/8M bins) under one name. Build that path, e.g. system size and rule depth tiers, into v1.

5. **Use in-distribution, near-duplicate distractors.** The persistent benchmarks (MRCR) use distractors that differ from the target by one attribute (format, topic, style). The discredited one (NIAH) used an out-of-place sentence that models could spot or refuse. For a novel system, include near-miss rules and decoy examples that differ in one feature.

6. **Publish the noise floor and chance model.** GDM's MRCR README gives random-relevant floors of 51%, 27% and 15%. LongBench v2 has a 25% MCQ floor. Report scores as above-floor and prefer answer spaces with a floor near 0: exact program outputs or derivations rather than MCQ.

7. **Fix and disclose the tool policy.**
   - "If the model is given access to code tools, the task becomes considerably simpler" (GDM). Graphwalks is a REPL one-liner.
   - Either (a) run sealed and tool-free, or (b) run a tool track separately, with items designed so that executing supplied code does not reveal answers. An example is learning a system from its *specification* when no interpreter is supplied.
   - Label every score with the tool condition.

8. **Exact verifiers, plus generator unit tests.**
   - Judge-graded siblings accumulated errors and churn:
     - AA-LCR re-keyed 16/100 items and swapped graders;
     - CL-bench depends on GPT-5.1 as judge;
     - NIAH v1 was GPT-4-judged.
   - Exact-graded synthetic sets still shipped defects: OpenAI MRCR had about 5% wrong ground truth; Graphwalks had ambiguous "depth" prompts and self-including answer sets.
   - Ship distribution tests (as GDM does) and an oracle solver that must score 100% on every generated item.

9. **Validity plan with targets taken from this family.**
   - Run a HELMET-style correlation study against natural "learn from documentation" tasks, e.g. CL-bench and CodeUpdateArena-like APIs. Use N ≥ 30 models.
   - Expected ranges: harder synthetic recall correlates 0.74–0.87 with natural long-document categories; ICL correlates only 0.36–0.63 with them. A learning construct should sit nearer the ICL end (distinct), but must first show reliability (brief D, T5).
   - Include a discriminant check against pure long-context recall (MRCR or NoLiMa) and against general capability. Opus 4.6 → 4.7 shows these can move in opposite directions.

10. **Anchor the headline to human learners, not to tokens.**
    - Context length failed as a legible trend unit: windows plateaued at about 1M, effective length is task-relative, and nothing like METR's human-minute doubling emerged.
    - Report per-tier curves plus one scalar tied to a human-legible quantity. Examples: "fraction of a novel system mastered from N pages", or human-learner parity as in MTOB's human baseline.

11. **Plan for curriculum capture.**
    - Public generators *will* become RL tasksets. Prime Intellect packaged six long-context evaluations within months, and BABILong ships a training split.
    - Keep live-window seeds and some structural families private. Rotate families, not just seeds.
    - Run a deliberate "train on the public generator" stress test and report transfer to the private families. Report the gap as a contamination index.

12. **Adoption path.**
    - Creator-run synthetic benchmarks stayed single-lab in headline tables, but public data and a harness PR reached HELM, lm-eval-harness, NeMo, evalscope, openbench and Prime within months.
    - To get beyond single-lab use:
      - (a) release a public dev generator plus harness adapters at launch;
      - (b) secure a third-party runner (AA, Epoch or a Context-Arena-style site);
      - (c) keep per-item cost prefix-cache-friendly, as GDM designed MRCR v2.

---

## Claims ledger

| # | Claim | Source URL(s) | Confidence |
|---|---|---|---|
| 1 | NIAH's original runs were GPT-4-128K (8 Nov 2023; 15×15 grid 1K–128K; degradation at large lengths, 10–50% depth) and Claude 2.1 (21 Nov 2023; 35×35; evaluated "with GPT-4"). | https://raw.githubusercontent.com/gkamradt/LLMTest_NeedleInAHaystack/main/README.md ; …/img/GPT_4_testing.png ; …/img/Claude_2_1_testing.png | H |
| 2 | A prompt adjustment moved Claude 2.1 NIAH accuracy from 27% to 98% (6 Dec 2023). | https://claude.com/blog/claude-2-1-prompting (redirect from anthropic.com/news/claude-2-1-prompting) | H |
| 3 | Gemini 1.5 Pro: >99.7% needle recall to 1M, 99.2% at 10M; 100 needles ≈70% at 128K, >60% to 1M; MRCR introduced and scored by SequenceMatcher over 2,000 instances. | https://storage.googleapis.com/deepmind-media/gemini/gemini_v1_5_report.pdf | H |
| 4 | Claude 3 Opus >99% NIAH with 30 needle/question pairs; recognised the needle as artificially inserted (4 Mar 2024). | https://www.anthropic.com/news/claude-3-family | H |
| 5 | NIAH is not a row in any of 34 headline tables, Dec 2024–Sep 2026; it appears as figures in DeepSeek-V3 and GPT-4.1 materials. | research/notes/model_cards_adoption.md §A.2 ; https://raw.githubusercontent.com/deepseek-ai/DeepSeek-V3/main/README.md ; https://raw.githubusercontent.com/visual-snow/seshat/main/web-research/openai/gpt-4-1.md | H |
| 6 | RULER: 13 tasks, 4 categories; effective length = threshold of Llama-2-7B at 4K (85.6%); "only half" handle 32K; Gemini-1.5-Pro 95.8 average and 94.4 at 128K; harder configurations not stress-tested. | https://raw.githubusercontent.com/NVIDIA/RULER/main/README.md | H |
| 7 | RULER v2 added 9 Oct 2025; last commit 22 Jul 2026. | https://github.com/NVIDIA/RULER/commits/main ; https://raw.githubusercontent.com/NVIDIA/RULER/rulerv2-ns/README.md | M |
| 8 | Michelangelo: RULER VT reduces to multi-needle retrieval (every variable = 3); CWE/FWE solvable by frequency; Paul Graham filler is OOD; BABILong short-circuits via leaked bAbI. | https://raw.githubusercontent.com/visual-snow/seshat/main/parsed/deepmind/2409_12640.md | M-H |
| 9 | NoLiMa: at 32K, 10 of 12 models fall below 50% of base; GPT-4o 99.3→69.7; effective lengths GPT-4o 8K, Gemini 1.5 Pro 2K, Llama 4 Scout 1K; NoLiMa-Hard o3 100→58.5 at 32K. | https://raw.githubusercontent.com/adobe-research/NoLiMa/main/README.md | H |
| 10 | Restoring literal matches recovers near-baseline NoLiMa accuracy at 32K; literal-match distractors impair accuracy. | WebSearch summaries of arXiv:2502.05167 (ResearchGate, alphaXiv listings) | M |
| 11 | Six-model overlap: Spearman(RULER-32K, NoLiMa-32K) = 0.89 (p = 0.02); RULER-128K 0.71. | Derived from claims 6 and 9 | M [D] (N = 6) |
| 12 | HELMET category Spearman: Recall vs RAG 0.87, Summ 0.87, Re-rank 0.86, LongQA 0.84, Cite 0.74, ICL 0.63; ICL vs others 0.36–0.59. | https://raw.githubusercontent.com/princeton-nlp/HELMET/main/assets/task_correlation.png | H (values); N unstated |
| 13 | HELMET (59 LCLMs): NIAH not a good predictor of downstream; categories weakly correlated; most models perfect on NIAH. | https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/main/ops/rebuild-2026-09/evidence/phase-04/sources/supp-970ee183b830.txt ; WebSearch summary of arXiv:2410.02694v1 | M-H |
| 14 | HELMET: no synthetic task averages Spearman >0.8 with real tasks (35 instruction-tuned models). | WebSearch summary of arXiv:2410.02694 | M |
| 15 | HELMET ICL maps labels to random integers by default; Recall = RULER MK-2, MK-3, MV plus JSON KV. | https://raw.githubusercontent.com/princeton-nlp/HELMET/main/data.py ; …/configs/recall.yaml ; …/configs/icl.yaml | H |
| 16 | LongBench v2: 503 MCQ; human experts 53.7% (15 min); best direct 50.1%; o1-preview 57.7% (Dec 2024). | https://raw.githubusercontent.com/THUDM/LongBench/main/README.md | H |
| 17 | Gemini 2.5 "hill-climb[ed]" on LOFT and MRCR-V2; LOFT hard ≤128K 87.0 / 1M 69.8; MRCR-V2 ≤128K 58.0 / 1M 16.4; MRCR-V2 adds a style parameter (depth-3 keys) and uses 8 needles. | https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf | H |
| 18 | Michelangelo cross-task Spearman over 10 models: MRCR–LL 0.64, MRCR–IDK 0.043, LL–IDK −0.25; MRCR "worked out of the box", LL and IDK needed post-processing; tasks not intended for training. | https://raw.githubusercontent.com/visual-snow/seshat/main/parsed/deepmind/2409_12640.md | M-H |
| 19 | OpenAI-MRCR (2/4/8 identical requests, near-miss distractors) and Graphwalks (hex-hash graph, BFS or parents; "cannot be solved sequentially") released with GPT-4.1 on 14 Apr 2025; GPT-4.1 57.2 (MRCR 2-needle 128K), 61.7 (Graphwalks BFS <128K); o1 22.1 / 62.0. | https://raw.githubusercontent.com/visual-snow/seshat/main/web-research/openai/gpt-4-1.md | H (mirror) |
| 20 | OpenAI-MRCR scoring: hash prefix required, else 0; SequenceMatcher ratio; 2,400 samples, bins 4K–1M. | https://raw.githubusercontent.com/stanford-crfm/helm/main/src/helm/benchmark/metrics/openai_mrcr_metrics.py ; https://raw.githubusercontent.com/modelscope/evalscope/main/docs/en/benchmarks/openai_mrcr.md | H (scoring) / M (counts) |
| 21 | GPT-5 developer page (Aug 2025): MRCR 2-needle 128K 95.2; Graphwalks BFS <128K 78.3; BrowseComp LC 128K 90.0 with GPT-4.1 nano 89.4. | https://raw.githubusercontent.com/syhya/syhya.github.io/main/content/en/posts/2025-08-24-gpt5/index.md ; https://raw.githubusercontent.com/Java-Edge/Java-Interview-Tutorial/main/docs/md/AI/llm/GPT-5.md | M-H |
| 22 | GPT-5.2 introduced OpenAI MRCRv2 (8-needle; fixes ~5% wrong ground truth); 4K–8K 98.2, 128K–256K 77.0; Graphwalks BFS <128K 94.0. | https://raw.githubusercontent.com/visual-snow/seshat/main/web-research/openai/introducing-gpt-5-2.md | H (mirror) |
| 23 | GPT-5.5: MRCR v2 512K–1M 74.0 (GPT-5.4 36.6); Graphwalks BFS 1M F1 45.4; reports Claude Opus 4.7 on OpenAI's evals (Graphwalks BFS 256K 76.9). | https://raw.githubusercontent.com/visual-snow/seshat/main/web-research/openai/introducing-gpt-5-5.md ; …/introducing-gpt-5-4.md | H (mirror) |
| 24 | NVIDIA's Graphwalks port corrects an ambiguous "depth N" BFS prompt and parents answer sets that include the target. | https://raw.githubusercontent.com/NVIDIA-NeMo/Gym/main/benchmarks/graphwalks/prepare.py | H |
| 25 | GDM MRCR v2 was "not publicly available yet" in Nov 2025; public bucket files dated 9 Jul 2025 with bins to 8M; eval_hub release commit 19 Feb 2026. | https://storage.googleapis.com/deepmind-media/gemini/gemini_3_pro_model_evaluation.pdf ; https://storage.googleapis.com/mrcr_v2 ; https://github.com/google-deepmind/eval_hub/commits/master/eval_hub/mrcr_v2 | H / H / M |
| 26 | GDM MRCR v2 noise floors ≈1% (any response) and ≈51%, 27%, 15% (random relevant response, 2/4/8 needles); code tools make it "considerably simpler". | https://raw.githubusercontent.com/google-deepmind/eval_hub/master/eval_hub/mrcr_v2/README.md | H |
| 27 | Google MRCR v2 (8-needle), Google-run: 3 Pro 77.0/26.3; 3.1 Pro 84.9/26.3; 3.5 Flash 77.3/26.6; 3.5 Flash-Lite 72.2/21.3; GPT-5.5 94.8 (≤128K); Opus 4.6 84.0; Opus 4.7 59.3. | https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-Pro-Model-Card.pdf ; …/Gemini-3-1-Pro-Model-Card.pdf ; …/Gemini-3-5-Flash-Model-Card.pdf ; …/Gemini-3-5-Flash-Lite-Model-Card.pdf | H |
| 28 | Anthropic reports Opus 4.6 at 76% on the 8-needle 1M variant of MRCR v2 vs Sonnet 4.5 at 18.5% (5 Feb 2026). | https://www.anthropic.com/news/claude-opus-4-6 | H |
| 29 | Spearman(MRCR 2-needle 128K, Graphwalks BFS <128K) = 0.23 across 8 OpenAI models on the GPT-4.1 page; 0.61 on the GPT-5 page; BrowseComp LC vs MRCR 0.29. | Derived from claims 19 and 21 | M [D] (N = 8) |
| 30 | AA-LCR: 100 questions, ~100K tokens, 7 document categories, LLM equality checker; v1.1 corrected 16 answer keys; grader swapped (Qwen3 235B → GPT-5.6 Luna); 5% of AA Index v4.3. | https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/main/ops/rebuild-2026-09/evidence/phase-04/sources/aa-1ea3e75f96c3.txt | M-H (capture) |
| 31 | AA-LCR Oct 2025: GPT-5 (thinking) 76, DeepSeek-V3.2 69, Sonnet 4.5 66, Gemini 2.5 Pro 66. | https://raw.githubusercontent.com/MiniMax-AI/MiniMax-M2/main/README.md | M |
| 32 | Fiction.LiveBench: 36 questions over 30 stories; Epoch mirrors it; o3 100% at 120K. | https://raw.githubusercontent.com/htihle/open_closed_gap/main/provenance_audit/fictionlivebench.md ; https://raw.githubusercontent.com/LeeHengYu/mediator-coevo/main/related-literature/llm-longcontext-degradation/results/D11_FictionliveBench_Long-Context_Deep_Comprehension.json | L-M |
| 33 | BABILong ships a 5k-sample-per-task training split; GPT-4 degrades beyond 10% of 128K; small fine-tuned models solve the tasks. | https://raw.githubusercontent.com/booydar/babilong/main/README.md | H |
| 34 | Fine-tuning on synthetic key-value retrieval gives +10.5 on 20-document MDQA (GPT-3.5 Turbo) and beats fine-tuning on MDQA itself. | https://raw.githubusercontent.com/memgrafter/research-digests/main/ml_research_analysis_2024/2406.19292_from-artificial-needles-to-real-haystacks-improving-retrieval-capabilities-in-llms-by-finetuning-on-synthetic-data_20260212_113049.md ; HuggingAGI/HuggingArxiv digest | M-H |
| 35 | Prime Intellect packages Graphwalks, MRCR v2, Oolong, CL-bench and LongBench-Pro as sandboxed agent tasksets (initial 24 Jun 2026); the Graphwalks agent parses the graph "from a REPL". | https://raw.githubusercontent.com/PrimeIntellect-ai/prime-envs/main/environments/long_context/README.md ; …/graphwalks/graphwalks/taskset.py ; …/mrcr_v2/README.md | H |
| 36 | Many-shot ICL: gains from few- to many-shot; overrides pretraining biases; NLL is not predictive; performance can decline with more shots (MATH peak ~125); order-sensitive. | https://raw.githubusercontent.com/visual-snow/seshat/main/parsed/deepmind/2404_11018.md | H (parsed) / M (figure values) |
| 37 | ManyICLBench: classification ICL has SLR ≫1 (similar-sample retrieval); math and summarisation SLR ≈1 and degrade from ~16K. | https://raw.githubusercontent.com/zhaoyang97/Paper-Notes-en/main/docs/ACL2025/llm_efficiency/on_many-shot_in-context_learning_for_long-context_evaluation.md | M |
| 38 | MIR-Bench: generated functions with published generators; o1 MIR-Core average 79.65; performance falls at 1K–2K shots (DeepSeek-R1 75.5 → 38.8). | https://raw.githubusercontent.com/KaiYan289/MIR-Bench/main/README.md | H |
| 39 | LMAct: up to 512 demonstrations or 1M tokens; models rarely reach expert level; more demonstrations often have little effect. | https://raw.githubusercontent.com/google-deepmind/lm_act/master/README.md | H |
| 40 | CL-bench: 500 contexts, 1,899 tasks, 31,607 rubrics, GPT-5.1 judge; frontier average 17.2%, best 23.7%; context ignored 55–66%. | https://raw.githubusercontent.com/Tencent-Hunyuan/CL-bench/main/README.md ; https://raw.githubusercontent.com/harbor-framework/harbor/main/adapters/clbench/README.md ; memgrafter digest 2602.03587 | H (design) / M-H (scores) |
| 41 | Llama 4 files MTOB under "Long Context" (Maverick half-book 54.0/46.4 chrF). | https://raw.githubusercontent.com/meta-llama/llama-models/main/models/llama4/MODEL_CARD.md | H |
| 42 | Akhtar et al.'s 60-benchmark sample contains no synthetic long-context benchmark; "templated" means surface prompt templating; templated vs non-templated p = 0.10. | https://raw.githubusercontent.com/mlresearch/v306/main/assets/akhtar26a/akhtar26a.pdf (Table 3, App. D) | H |
| 43 | Context Arena (from 24 Apr 2025) runs MRCR across 77 configurations; GPT-5.5 AUC@128K 87.5 → AUC@1M 50.9. | https://raw.githubusercontent.com/LeeHengYu/mediator-coevo/main/related-literature/llm-longcontext-degradation/results/D12_Context_Arena.json ; https://raw.githubusercontent.com/smol-ai/ainews-web-2025/main/src/content/frozen-issues/25-05-01-not-much.md | L-M |
| 44 | Chroma "Context Rot" (14 Jul 2025, 18 models): lower needle–question similarity steepens degradation; shuffled haystacks are easier. | https://raw.githubusercontent.com/BobYeger/state-of-agents/main/sources/Context%20Rot.md ; https://raw.githubusercontent.com/momo-personal-assistant/momo-research/main/Context%20Rot.md | M |
| 45 | Last commits: NIAH 8 Jun 2026 (v2 rewrite 30 May 2026); HELMET 19 Sep 2026; LongBench 15 Jan 2025; LOFT 13 Jun 2025; NoLiMa 17 Jul 2025; BABILong 1 Jun 2026; LongICLBench 20 Feb 2025; CL-bench 9 May 2026; LMAct archived by 24 Jul 2026. | github.com/<repo>/commits pages via WebFetch | M |

---

## References

Keys resolve in `research/refs/gap_longcontext_icl_lifecycle.json`. Keys marked † are reused from other survey JSON files.

1. [kamradt2023niah] Kamradt, G. Needle In A Haystack: Pressure Testing LLMs (GitHub repo; v2 2026). https://github.com/gkamradt/LLMTest_NeedleInAHaystack
2. [anthropic2023claude21prompting] Anthropic. Long context prompting for Claude 2.1. 6 Dec 2023. https://claude.com/blog/claude-2-1-prompting
3. [anthropic2024claude3] Anthropic. Introducing the next generation of Claude. 4 Mar 2024. https://www.anthropic.com/news/claude-3-family
4. [gemini2024gemini15]† Gemini Team, Google. Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context. 2024. https://storage.googleapis.com/deepmind-media/gemini/gemini_v1_5_report.pdf
5. [hsieh2024ruler] Hsieh, C.-P., Sun, S., Kriman, S., Acharya, S., Rekesh, D., Jia, F., Zhang, Y., Ginsburg, B. RULER: What's the Real Context Size of Your Long-Context Language Models? arXiv:2404.06654, 2024. https://github.com/NVIDIA/RULER
6. [modarressi2025nolima] Modarressi, A., Deilamsalehy, H., Dernoncourt, F., Bui, T., Rossi, R. A., Yoon, S., Schütze, H. NoLiMa: Long-Context Evaluation Beyond Literal Matching. ICML 2025; arXiv:2502.05167. https://github.com/adobe-research/NoLiMa
7. [yen2025helmet] Yen, H., Gao, T., Hou, M., Ding, K., Fleischer, D., Izsak, P., Wasserblat, M., Chen, D. HELMET: How to Evaluate Long-Context Language Models Effectively and Thoroughly. ICLR 2025; arXiv:2410.02694. https://github.com/princeton-nlp/HELMET
8. [bai2024longbench] Bai, Y., et al. LongBench: A Bilingual, Multitask Benchmark for Long Context Understanding. ACL 2024; arXiv:2308.14508. https://github.com/THUDM/LongBench
9. [bai2024longbench2] Bai, Y., Tu, S., Zhang, J., et al. LongBench v2: Towards Deeper Understanding and Reasoning on Realistic Long-context Multitasks. arXiv:2412.15204, 2024. https://github.com/THUDM/LongBench
10. [yang2025longbench100] Yang, W., Jin, H., Zhong, S., Jiang, S., Wang, Q., Chaudhary, V., Han, X. 100-LongBench: Are de facto Long-Context Benchmarks Literally Evaluating Long-Context Ability? arXiv:2505.19293; ACL Findings 2025.
11. [lee2024loft] Lee, J., Chen, A., Dai, Z., et al. Can Long-Context Language Models Subsume Retrieval, RAG, SQL, and More? (LOFT). arXiv:2406.13121, 2024. https://github.com/google-deepmind/loft
12. [vodrahalli2024michelangelo]† Vodrahalli, K., et al. Michelangelo: Long Context Evaluations Beyond Haystacks via Latent Structure Queries. arXiv:2409.12640, 2024.
13. [openai2025gpt41]† OpenAI. Introducing GPT-4.1 in the API. 14 Apr 2025. https://openai.com/index/gpt-4-1 (mirror: visual-snow/seshat)
14. [openai2025mrcr] OpenAI. OpenAI-MRCR dataset (openai/mrcr). 2025. https://huggingface.co/datasets/openai/mrcr
15. [openai2025graphwalks] OpenAI. Graphwalks dataset (openai/graphwalks). 2025. https://huggingface.co/datasets/openai/graphwalks
16. [openai2025gpt5dev] OpenAI. Introducing GPT-5 for developers (long-context results; BrowseComp Long Context release). Aug 2025. Seen via two copies.
17. [openai2025browsecomplc] OpenAI. BrowseComp Long Context dataset (openai/BrowseCompLongContext). 2025.
18. [wei2025browsecomp]† Wei, J., et al. BrowseComp: A Simple Yet Challenging Benchmark for Browsing Agents. 2025.
19. [openai2025gpt5]† OpenAI. Introducing GPT-5. 7 Aug 2025.
20. [openai2025gpt52]† OpenAI. Introducing GPT-5.2. 11 Dec 2025.
21. [openai2026gpt54]† OpenAI. Introducing GPT-5.4. 5 Mar 2026.
22. [openai2026gpt54mininano]† OpenAI. Introducing GPT-5.4 mini and nano. 17 Mar 2026.
23. [openai2026gpt55]† OpenAI. Introducing GPT-5.5. 23 Apr 2026.
24. [gemini2025gemini25]† Gemini Team. Gemini 2.5 technical report. 2025. https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf
25. [google2025gemini3eval]† Google DeepMind. Model Evaluation – Gemini 3 Pro. Nov 2025.
26. [google2025gemini3card]† Google DeepMind. Gemini 3 Pro Model Card. Nov 2025.
27. [google2026gemini31card]† Google DeepMind. Gemini 3.1 Pro Model Card. Feb 2026.
28. [google2026gemini35flashcard]† Google DeepMind. Gemini 3.5 Flash Model Card. 2026.
29. [google2026gemini35flashlitecard]† Google DeepMind. Gemini 3.5 Flash-Lite Model Card. 2026.
30. [gdm2026mrcrv2] Google DeepMind. MRCR V2 (eval_hub release; data bucket mrcr_v2). 2026. https://github.com/google-deepmind/eval_hub/tree/master/eval_hub/mrcr_v2
31. [anthropic2026opus46]† Anthropic. Introducing Claude Opus 4.6. 5 Feb 2026.
32. [anthropic2026opus47]† Anthropic. Introducing Claude Opus 4.7. 16 Apr 2026.
33. [aa2026method]† Artificial Analysis. Intelligence Benchmarking methodology (Index v4.3 and changelog). 2026.
34. [aa2025lcr] Artificial Analysis. AA-LCR: Artificial Analysis Long Context Reasoning (dataset ArtificialAnalysis/AA-LCR; v1.1 2026).
35. [fictionlive2025] fiction.live. Fiction.LiveBench (long-context deep comprehension leaderboard). 2025–.
36. [epochHub]† Epoch AI. Benchmarking Hub. https://epoch.ai/benchmarks
37. [ainews2025epoch]† AINews issues 2025-05-07 and 2025-05-30.
38. [contextarena2025] Uzar, D. Context Arena (MRCR leaderboard). 2025–. https://contextarena.ai
39. [hong2025contextrot] Hong, K., Troynikov, A., Huber, J. Context Rot: How Increasing Input Tokens Impacts LLM Performance. Chroma technical report, 14 Jul 2025.
40. [kuratov2024babilong]† Kuratov, Y., Bulatov, A., Anokhin, P., Rodkin, I., Sorokin, D., Sorokin, A., Burtsev, M. BABILong. NeurIPS 2024 D&B; arXiv:2406.10149.
41. [xiong2024artificialneedles] Xiong, Z., Papageorgiou, V., Lee, K., Papailiopoulos, D. From Artificial Needles to Real Haystacks: Improving Retrieval Capabilities in LLMs by Finetuning on Synthetic Data. arXiv:2406.19292, 2024; ICLR 2025 (per paper lists).
42. [agarwal2024manyshot] Agarwal, R., Singh, A., Zhang, L. M., et al. Many-Shot In-Context Learning. arXiv:2404.11018; NeurIPS 2024.
43. [li2024longiclbench] Li, T., Zhang, G., Do, Q. D., Yue, X., Chen, W. Long-context LLMs Struggle with Long In-context Learning (LongICLBench). arXiv:2404.02060; TMLR 2025.
44. [zou2025manyiclbench] Zou, K., Khalifa, M., Wang, L. On Many-Shot In-Context Learning for Long-Context Evaluation (ManyICLBench). arXiv:2411.07130; ACL 2025.
45. [yan2025mirbench] Yan, K., Ling, Z., Liu, K., Yang, Y., Fan, T.-H., Shen, L., Du, Z., Chen, J. MIR-Bench. arXiv:2502.09933, 2025.
46. [ruoss2025lmact] Ruoss, A., Pardo, F., Chan, H., Li, B., Mnih, V., Genewein, T. LMAct: A Benchmark for In-Context Imitation Learning with Long Multimodal Demonstrations. ICML 2025; arXiv:2412.01441.
47. [dou2026clbench] Dou, S., Zhang, M., Yin, Z., et al. (incl. Yao, S.). CL-bench: A Benchmark for Context Learning. arXiv:2602.03587, 2026; CL-bench Life arXiv:2604.27043.
48. [meta2025llama4card]† Meta. Llama 4 Model Card. 2025.
49. [deepseek2024v3]† DeepSeek-AI. DeepSeek-V3 README. Dec 2024.
50. [minimax2025m1]† MiniMax. MiniMax-M1 README. Jun 2025.
51. [minimax2025m2]† MiniMax. MiniMax-M2 README. Oct 2025.
52. [nvidia2026nemogw] NVIDIA. NeMo Gym / NeMo-Skills Graphwalks benchmark preparation code. 2026.
53. [primeintellect2026longcontext] Prime Intellect. prime-envs long-context tasksets. 2026.
54. [stanfordhelm2025mrcr] Stanford CRFM. HELM OpenAI-MRCR and DeepMind MRCR v2 scenarios.
55. [akhtar2026plateau]† Akhtar, M., et al. When AI Benchmarks Plateau: A Systematic Study of Benchmark Saturation. arXiv:2602.16763; PMLR v306.
56. [stojanovski2025reasoninggym]† Stojanovski, Z., et al. Reasoning Gym. arXiv:2505.24760.
57. [aycock2024grammarbook]† Aycock, S., Stap, D., Wu, D., Monz, C., Sima'an, K. Can LLMs Really Learn to Translate a Low-Resource Language from One Grammar Book? arXiv:2409.19151; ICLR 2025.
58. [tanzer2023mtob]† Tanzer, G., et al. MTOB. arXiv:2309.16575; ICLR 2024.
59. [kwa2025metr]† Kwa, T., West, B., et al. (METR). Measuring AI Ability to Complete Long Tasks. arXiv:2503.14499.

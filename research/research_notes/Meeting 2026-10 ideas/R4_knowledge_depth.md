# R4: "Depth of knowledge" test, research brief

Compiled on 7 Oct 2026. The idea is to ask models deep, open-ended questions closed-book (for example "What caused the rise and fall of Rome?") and compare depth and accuracy.

**Source tags.** [P] means a primary source: the official repo or paper text. [S] means a secondary source: a search summary, aggregator or digest. [I] means our own inference.

**Access limits.** arxiv.org, aclanthology.org, artificialanalysis.ai and kaggle.com were blocked from this session, so primary facts come from the official GitHub repos.

---

## 1. Existing benchmarks

| Benchmark | What it is | Key facts (dated) |
|---|---|---|
| **SimpleQA** (OpenAI, Oct 2024) | 4,326 adversarial short fact questions. Each answer is graded correct, incorrect or not attempted. | simple-evals (frozen Jul 2025): GPT-4o 38.8–40.1, o3 49.4, **GPT-4.5 62.5**, o4-mini 20.2, gpt-4.1-nano 7.6 [P]. |
| **SimpleQA Verified** (DeepMind, Sep 2025) | 1,000 de-noised prompts, scored by F1. | Launch: Gemini 2.5 Pro 55.6. Gemini 3 Pro 72.1 (Nov 2025) [S]. |
| **FACTS Parametric** (DeepMind/Kaggle, Dec 2025) | Closed-book factoid questions, private held-out set. | Gemini 3 Pro 76.4 at launch. 2026 snapshots put the top at about 78–79, but aggregators disagree [S]. |
| **FActScore** (EMNLP 2023) | Biographies split into atomic facts, each checked against Wikipedia. | ChatGPT 58% with human graders; the estimator has under 2% error [S]. README, score / facts per answer: GPT-4 73.1 / 60.8, Alpaca-7B 39.7 / 17.4 [P]. |
| **LongFact + SAFE** (DeepMind, 2024) | 2,280 prompts on 38 topics. SAFE verifies claims via search. **F1@K** adds recall. | SAFE agrees with humans 72% of the time and wins 76% of disagreements. About $0.20–0.40 per response, versus $4 human [P]. |
| **VeriScore** (EMNLP Findings 2024) | Extracts only *verifiable* claims. | 16 models on 8 tasks; GPT-4o best [S]. Open extractor and verifier models available [P]. |
| **HalluLens** (Meta, 2025) | Dynamically generated, so it cannot leak. Tasks: PreciseWikiQA, LongWiki, **NonExistentRefusal** (fake entities). | Reports hallucination-when-answering separately from refusal [P]. |
| **WildHallucinations** (2024) | 7,919 entities from real WildChat queries; 15 LLMs. | Half the entities lack a Wikipedia page, and models **hallucinate more on those**. Retrieval helps only slightly [S]. |
| **AA-Omniscience** (Nov 2025) | 6,000 questions, 42 topics. Index = 100·(correct − incorrect)/N, so abstaining scores 0. Hallucination rate = incorrect / (incorrect + abstained). | Launch top was Claude 4.1 Opus at **4.8**; only 3 of 36 models were above 0, and abstaining on everything would have ranked 4th. GPT-5 (high): 39% accuracy, 81% hallucination rate [S]. Sep 2026: Claude Fable 5.1 43.5, Fable 5 43.3 (about 65% accuracy, 64% hallucination rate) [S]. |
| **HLE** (*Nature* 2026) | 2,500 expert closed-ended questions, about 9% humanities, with calibration error reported. | Under 10% (Jan 2025), rising to about 45–65% in late 2026 depending on source [S]. Only 641 items survived full verification (HLE-Verified) [S]. |
| **MMLU-Pro** (NeurIPS 2024) | Over 12,000 questions, 10 options each, including History. | GPT-4o 72.55 at launch [P]. The top is now about 90, so it is saturated [S]. |
| **HiST-LLM** (NeurIPS 2024) | Seshat databank: 36,000 data points on over 600 polities, 4-choice. | Balanced accuracy 33.6% (Llama-3.1-8B) to **46% (GPT-4-Turbo)**, against 25% chance. Weakest on Sub-Saharan Africa and Oceania [S]. Data in repo [P]. |
| **HistBench** (2025) | 414 historian-written questions in 29 languages. | GPT-4o 18.6%, the HistAgent system 27.5% [S]. |
| **ProHist-Bench** (ACL 2026) | 400 expert questions on China's imperial examinations, **10,891 rubric items**. | Across 18 LLMs, state-of-the-art models "struggle" [S]. |
| **FactRBench** (EMNLP 2025) | Long-form precision **and recall** against reference fact sets. | High precision does not imply high recall [S]. |

**Gap [I].** Nobody owns long-form humanities answers scored for depth (recall) and calibration, stratified by how obscure the topic is.

---

## 2. Grading cheaply and objectively

1. **Atomic claims, then verification (precision).** This is the FActScore, SAFE and VeriScore approach. It costs about $0.20–0.40 per answer with search [P], and less against a fixed reference pack of expert excerpts. On its own it rewards short, safe answers.
2. **Expert key-point ("nugget") coverage (recall, which is the real "depth").** Experts write 8–15 required points per prompt, and a judge marks which are covered. In TREC 2024 RAG, automatic nugget scores correlated strongly with manual ones at the run level [S].
3. **Expert rubrics.**
   - HealthBench used 262 physicians, 48,562 weighted criteria and a model grader validated against physicians [S].
   - ProHist-Bench averages about 27 rubric items per question.
   - Rubrics are costly to write but cheap to grade with.
4. **Pairwise preference is the weakest option.**
   - Raters preferred answers *with factual errors* over short ones (Wu & Aji) [S].
   - Length control raised AlpacaEval's correlation with Chatbot Arena from 0.93 to 0.98 [P].
   - Arena's style control re-ranked models [P].
   - LLM judges self-prefer [S].
   - If used at all: secondary only, with length capped.
5. **Penalise hallucination, reward abstention.**
   - Kalai et al. (OpenAI, Sep 2025) argue that binary grading *causes* hallucination. They propose stating the rule "answer only if >t confident; errors cost t/(1−t)" [S].
   - Pick t (for example 0.75, so an error costs 3), state it and publish it.
   - Remember that under AA's symmetric ±1 penalty, abstaining on everything ranks 4th.

---

## 3. Separation, saturation, size, contamination

- **Closed-book recall still separates models and is not saturated.**
  - The same OpenAI models span **7.6–62.5 on SimpleQA but only 80–93 on MMLU** [P].
  - On AA-Omniscience (Sep 2026), the best models are about 65% accurate but still give a wrong answer instead of abstaining on about 60% of their misses [S].
  - Multiple-choice knowledge (MMLU-Pro, about 90%) is saturated.
- **Raw recall is largely a proxy for model size.**
  - SimpleQA within families: gpt-4.1 41.6, mini 16.8, nano 7.6. o3 49.4 against o4-mini 20.2. The largest model, GPT-4.5, is top [P].
  - Reasoning effort does not help: o4-mini-high scores 19.3 against o4-mini's 20.2 [P].
  - Models store about 2 bits of knowledge per parameter (Allen-Zhu & Li, ICLR 2025) [S].
  - AA: accuracy tracks size, but **hallucination rate does not**, and small models such as Nemotron Nano 9B score well on the index [S].
  - So the signal that is not just size is **calibration and abstention** [I].
- **The long tail is where models separate.**
  - Accuracy scales with the number of relevant pretraining documents (Kandpal et al., ICML 2023) [S].
  - Scaling mostly helps popular facts (PopQA) [S].
  - Hallucinations rise for entities without a Wikipedia page and for under-documented regions [S].
- **Rome and the US presidents are poor items [I].**
  - **Head topics:** they are saturated in pretraining, so every frontier model writes a fluent overview, and what remains is a contest of length and style.
  - **No ground truth:** "Causes of the fall" is contested; Demandt catalogued 210 proposed causes [S].
  - **Knowledge cutoff:** "The US presidents" mainly tests where each model's training data ends (for example, whether it covers 2025 onwards).
  - **Contaminated grader:** the LLM grader shares the same textbook knowledge.

---

## 4. What would make it novel and useful

1. **An obscurity curve.** Stratify topics head/torso/tail by Wikipedia pageviews or presence. Plot precision, recall and abstention against obscurity: where does each model start making things up, and does it hedge there? Nobody publishes this as a long-form curve [I].
2. **Plausible fake controls** (HalluLens-style), for example a fictional dynasty or treaty, to measure false acceptance.
3. **Depth defined as nugget recall, not length.** For interpretive prompts, score coverage of the historiographical positions.
4. **Consistency** across samples, paraphrases and languages, as a reference-free signal (SelfCheckGPT; semantic entropy, *Nature* 2024) [S].
5. **Calibration** via per-claim confidence tags, scored with Brier.
6. **A human-expert anchor:** graduate students answer closed-book under the same length cap.
7. **Refreshable items** generated from Seshat or Wikidata to reduce contamination. Report results size- and cost-normalised.

Caveat [I]: every component exists somewhere. The novelty is in combining them and focusing on long-form humanities answers.

---

## 5. Synthesis

### Talking points

1. **Plain closed-book recall is already well covered.** SimpleQA, FACTS and AA-Omniscience rank it. A depth test must add long-form recall, obscurity and calibration.
2. **Famous topics make poor items.** They are contaminated, have no ground truth and become a style contest. Keep a few as controls only.
3. **Raw depth is mostly model size.** "Knows what it doesn't know" (abstention, hedging, consistency) is the size-independent signal.
4. **Grade with claims and nuggets, not preferences.** Pairwise judging measures length and markdown.
5. **Publish the penalty.** State t, then report accuracy, hallucination rate and attempt rate separately.
6. **Tail topics separate models.** That means regional, non-English, pre-modern history and entities without a Wikipedia page.
7. **Validate the judge.** Have experts blind-grade about 10% of items, and use a judge from a different model family (or an ensemble).

### Minimal design (about 2–3 person-weeks)

- **Items.** 120 prompts in three tiers of 40:
  - Head control: for example Rome.
  - Torso: for example Songhai or the Haitian Revolution.
  - Tail: Seshat polities or local histories without an English Wikipedia page.
  - Add 15 fake-entity prompts.
  - Each real prompt gets 8–15 expert-vetted nuggets and a reference pack.
- **Protocol.**
  - Closed-book, 500-word cap, fixed temperature.
  - 3 samples plus 1 paraphrase per prompt.
  - The prompt states: "hedge or abstain if unsure; errors cost 3".
- **Scores.**
  - **Depth** = nugget recall.
  - **Precision** = supported ÷ verifiable claims, with VeriScore-style extraction checked against the reference pack.
  - **Hallucination rate** = contradicted claims.
  - **Calibration** = Brier score.
  - **Consistency** = contradiction rate across samples.
  - **Headline** = recall − 3 × contradicted share, plotted against obscurity tier.
- **Validation.** Two historians blind-grade 10% of answers; expert-written answers serve as a human baseline on 15 prompts.
- **Cost [I].** About 3,800 answers (8 models × 120 × 4). At $0.05–0.40 each, grading costs about $200–1,500.

---

### Sources

- **Primary (GitHub):**
  - openai/simple-evals
  - shmsw25/FActScore
  - google-deepmind/long-form-factuality
  - Yixiao-Song/VeriScore
  - facebookresearch/HalluLens
  - TIGER-AI-Lab/MMLU-Pro
  - centerforaisafety/hle
  - seshat-db/HiST-LLM
  - tatsu-lab/alpaca_eval
  - lm-sys/lm-sys.github.io (style-control post, Aug 2024)
- **Secondary [S]:**
  - arXiv: 2511.13029 (AA-Omniscience, via memgrafter digest), 2411.04368 (SimpleQA), 2509.07968 (SimpleQA Verified), 2512.10791 (FACTS), 2407.17468 (WildHallucinations), 2505.20246 (HistBench), 2411.09607 (AutoNuggetizer), 2505.08775 (HealthBench), 2509.04664 (Kalai et al.), 2602.13964 (HLE-Verified).
  - ACL Anthology: 2026.acl-long.1378 (ProHist-Bench), 2025.emnlp-main.905 (FactRBench), 2025.coling-main.21 (Wu & Aji).
  - Conference and journal papers: Kandpal et al. (ICML 2023), PopQA (ACL 2023), Allen-Zhu & Li (ICLR 2025), semantic entropy (*Nature* 2024).
  - Leaderboard snapshot: benchlm.ai (Sep 2026).
  - Demandt's list: courses.washington.edu/rome250.

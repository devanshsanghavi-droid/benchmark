# Knowledge and Reasoning Exam Benchmarks: Lifecycles, Successes and Failures

Research dossier, compiled 2026-09-29. Scope: static, closed-ended knowledge and reasoning "exam" benchmarks for LLMs (MMLU family, GPQA, Humanity's Last Exam, SimpleQA, the BIG-Bench family, HellaSwag, AI2 ARC, TruthfulQA, WinoGrande, DROP, GLUE/SuperGLUE).

Evidence conventions:
- **[V]** is a verified fact, seen in a primary source (paper, official repo, lab blog or model card) or in a search-result summary of one. The URL is given.
- **[S]** comes from a secondary source only (aggregator, news or blog). Treat it with care.
- **[I]** is my interpretation or synthesis, not a sourced fact.
- **[U]** is unverified: from memory or from an inconsistent source. Do not cite it without re-checking.

Tooling caveat: WebFetch was blocked for arxiv.org, epoch.ai, lastexam.ai, futurehouse.org and most news sites. Most paper numbers therefore come from search-result summaries of the primary page, cross-checked against a second query or a GitHub README where possible. Leaderboard numbers after about mid-2026 came only from aggregators and were **inconsistent across sites**. They are flagged low confidence.

---

## Summary

Static exam benchmarks follow a predictable lifecycle. A benchmark launches with a large headroom gap. It is adopted because it is cheap, automatically scorable, and gives one headline number. It is then saturated, typically in 1 to 4 years in the LLM era. Near the ceiling, its label noise becomes the binding constraint. Finally it drops out of frontier model cards, sometimes replaced by a "Pro", "Redux", "Verified", "Extra Hard" or "Diamond" successor.

- **Saturation speed has collapsed.** GLUE's human baseline (87.1) was passed in about a year: GLUE was released in 2018, and MT-DNN scored 87.6 in June 2019. SuperGLUE's human baseline (89.8) was passed by DeBERTa (89.9) around the turn of 2020/21, less than two years after release. MMLU (2020) went from 43.9% for GPT-3 to 90.0% for Gemini Ultra, above the 89.8% expert estimate, by December 2023. That 90.04% used CoT@32 prompting; the same model scored 83.7% under standard 5-shot [corrected by fact-check: Gemini 1.0 report PDF]. GPQA Diamond went from 39% for a GPT-4 baseline in November 2023 to 78.3% for o1 in September 2024, above PhD experts at 69.7% [fact-check: unverified; re-check o1 vs o1-preview], and to 94.3% for Gemini 3.1 Pro in February 2026 [fact-check: unverified; the model-card table is an image]. A 2026 ICML study of 60 benchmarks found that about half are saturated.
- **Label noise sets the effective ceiling and eventually kills benchmarks.** MMLU is about 6.5% erroneous overall [fact-check: unverified; not in the MMLU-Redux v1 abstract], with 57% of the Virology subset erroneous (MMLU-Redux; confirmed). HellaSwag has up to 40% ungrammatical prompts and more than 21% of items with multiple valid answers. The multiple-choice format of TruthfulQA could be gamed to 79.6% without seeing the question. Humanity's Last Exam (HLE), the flagship "unsaturated" benchmark of 2025-26, has faced three independent audits:
  - FutureHouse found 29 ± 3.7% of text-only bio/chem answers contradicted by the literature. [fact-check: the post exists (Andrew White, "About 30% of ...", July 2025); the exact 29 ± 3.7% is unverified]
  - HLE-Verified could fully validate only 641 to 668 of 2,500 items. [fact-check: confirmed]
  - Epoch AI's September 2026 Benchmark Review found accuracy-altering errors in 22/48 (46%) sampled items and rated HLE **"Flawed"**. [fact-check: unverified; no reachable source]
- **Contamination is demonstrated, not hypothetical.** GPT-4 guessed masked (wrong) MMLU answer options at a 57% exact-match rate [corrected by fact-check: TS-Guessing masks a wrong option]. GPT-4o drops from 88.0% on MMLU to 73.4% on the decontaminated MMLU-CF.
- **What gave staying power:**
  - Expert authorship with an adversarial filter against current models (GPQA, HLE).
  - A "Google-proof" or closed-book design that stays hard even with a search engine (GPQA non-experts reached 34% with 30+ minutes of web access).
  - Memorable framing ("Humanity's Last Exam", "PhD-level").
  - Canary strings and gated distribution.
  - Continued maintenance. HLE now ships HLE-Rolling and HLE-Diamond, and the MMLU family spawned MMLU-Pro, MMLU-Redux and MMLU-CF.
  - Being run by trusted third parties (Scale, Epoch, Artificial Analysis) so self-reports can be checked.
- **What killed the others:**
  - Crowdsourced construction, which saturates faster than expert-curated work according to the 2026 saturation study.
  - Answer-choice artefacts that let models score without reasoning (HellaSwag, TruthfulQA-MC, ARC-Challenge scoring setups).
  - Label noise that makes the last 5 to 10 points meaningless.
  - Scoring bugs (DROP on the Hugging Face Open LLM Leaderboard).
  - The shift to reasoning models and agents with tools, which made small, closed, short-answer tests either trivial (SimpleQA with search: 93.9%) or irrelevant.

As of late 2026, frontier labs' headline tables still carry GPQA Diamond, HLE and multilingual MMLU (MMMLU), and sometimes SimpleQA Verified. Original MMLU, HellaSwag, ARC, WinoGrande, TruthfulQA, DROP, BBH and (Super)GLUE are legacy or appendix items at best. Hugging Face's Open LLM Leaderboard dropped the v1 set (ARC, HellaSwag, MMLU, TruthfulQA, WinoGrande, GSM8K) in June 2024, and the whole leaderboard was retired in March 2025. OpenAI stopped updating `simple-evals` in July 2025 and had already labelled DROP (and MGSM) saturated.

---

## Benchmark-by-benchmark

### 1. MMLU (Measuring Massive Multitask Language Understanding)

- **What it measures:** broad academic and professional knowledge. It has 57 subjects across STEM, humanities, social sciences and professional fields (law, medicine), in 4-option multiple choice. [V]
- **Release / venue / creators:**
  - Released on arXiv:2009.03300 (September 2020) and published at ICLR 2021. [V]
  - Authors: Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, Jacob Steinhardt. [V]
  - Sources: https://arxiv.org/abs/2009.03300 , https://iclr.cc/virtual/2021/poster/2962
- **Items / format:** the test split is about 14k questions [U: count not re-verified this session] in 4-way multiple choice. The random baseline is 25% (from the repo leaderboard). [V]
- **Launch vs. frontier:**
  - Launch: GPT-3 175B few-shot scored 43.9% [V]. The repo leaderboard's top listed entry is Chinchilla 70B at 67.5% (https://github.com/hendrycks/test). [V]
  - GPT-4 scored 86.4% in March 2023 (https://cdn.openai.com/papers/gpt-4.pdf). [V]
  - Gemini Ultra scored 90.0% in December 2023, the "first model to outperform human experts (89.8%)" (https://arxiv.org/pdf/2312.11805). [V] The exact figure is 90.04% with CoT@32 (uncertainty-routed chain of thought, 32 samples). Under standard 5-shot, Gemini Ultra scored 83.7%, below GPT-4's reported 86.4%. The "first above experts" headline is therefore prompting-dependent. [corrected by fact-check: https://storage.googleapis.com/deepmind-media/gemini/gemini_1_report.pdf]
  - o3-high scored 93.3% in OpenAI's simple-evals table (2025) (https://github.com/openai/simple-evals). [V]
- **Time to saturation:** about 3.25 years to pass the expert estimate (September 2020 to December 2023) [I]. Scores have plateaued at about 92-93% since. That plateau is consistent with the ~6.5% error ceiling. [I, supported by MMLU-Redux]
- **Label errors:** MMLU-Redux estimates that 6.49% of MMLU questions contain errors, and that 57% of analysed Virology questions are erroneous. Correcting labels reorders models: Llama 3.1 405B moves from 16th to 1st on Virology (https://aclanthology.org/2025.naacl-long.262/ ; https://arxiv.org/abs/2406.04127). [fact-check: 57% Virology and "significant discrepancies with the model performance metrics that were originally reported" are confirmed in the v1 abstract. The 6.49% figure and the Llama 3.1 405B 16th→1st example were NOT found in any reachable source and are unverified. Llama 3.1 post-dates v1 (June 2024), so they must come from a later version.]
- **Contamination:**
  - TS-Guessing: with one wrong option masked, ChatGPT reproduced the missing MMLU option at a 52% exact-match rate, and GPT-4 at 57% (Deng et al., NAACL 2024, https://aclanthology.org/2024.naacl-long.482/). [V] [corrected by fact-check: the abstract specifies "masking a wrong answer in a multiple-choice question"]
  - GPT-4o scores 88.0% (5-shot) on MMLU but 73.4% (5-shot) and 71.9% (0-shot) on the decontaminated MMLU-CF (https://github.com/microsoft/MMLU-CF). [V]
- **Adoption:**
  - It was the de facto headline number in 2021-2024 model cards: GPT-4, Gemini 1.0 and the Open LLM Leaderboard v1 (2023-24). [V]
  - In 2025-26, frontier labs report **MMMLU (multilingual MMLU)** rather than MMLU:
    - Gemini 3.1 Pro: MMMLU 92.6% (https://deepmind.google/models/model-cards/gemini-3-1-pro/). [V via search summary]
    - Claude Opus 4.5 system card includes MMMLU 91.8% (https://www.anthropic.com/claude-opus-4-5-system-card). [corrected by fact-check: downgraded to U. 91.8% is exactly Gemini 3 Pro's MMMLU in Google's November 2025 launch table (Willison transcription), so this is a possible mix-up. The Opus 4.5 value could not be checked because the PDF host is blocked. Do not cite.]
  - Secondary sources say GPT-5.1, Gemini 3 Pro and Claude Opus 4.5 no longer report original MMLU (https://www.understandingai.org/p/why-its-getting-harder-to-measure ; https://digitortoise.com/mmlu-benchmark/). [S]
- **Status:** **saturated / contaminated.** It is kept as a legacy "floor check" [S: Surge AI], and it lives on via MMMLU and its successors.
- **Why it succeeded:** [I]
  - Breadth (57 subjects) produced one memorable number that loosely tracked "general knowledge".
  - It was trivially cheap to run, with log-prob or letter scoring.
  - It launched with huge headroom (GPT-3 at 44% against a ~90% expert estimate), so it tracked about 3 years of scaling progress.
  - Its human-expert anchor (89.8%) gave a narrative finish line.
- **Why it failed:** [I]
  - Its questions were scraped from publicly available practice exams, which made contamination likely. The TS-Guessing and MMLU-CF evidence supports this.
  - Crowd- and web-sourced answer keys with about 6.5% errors cap the meaningful range.
  - The 4-option format rewards elimination heuristics and is prompt-sensitive: 4-5% variation, per MMLU-Pro.

### 1a. MMLU-Pro

- **What it measures:** a harder, more reasoning-heavy MMLU. It has 14 domains, and options were expanded from 4 to 10. [V]
- **Release / venue / creators:** arXiv:2406.01574 (June 2024), NeurIPS 2024. Authors: Yubo Wang, Xueguang Ma, Ge Zhang, Yuansheng Ni, Abhranil Chandra, … Wenhu Chen (TIGER-AI-Lab) (https://github.com/TIGER-AI-Lab/MMLU-Pro ; https://neurips.cc/virtual/2024/poster/97435). [V]
- **Items / format:**
  - More than 12,000 curated questions with 10 options. Trivial and noisy MMLU items were removed, and there were two rounds of expert review. [V]
  - Accuracy drops 16-33% relative to MMLU.
  - Prompt sensitivity falls from 4-5% to 2%. [V, repo README]
- **Launch vs. frontier:** at launch (mid-2024) the repo leaderboard showed Claude-3.5-Sonnet 76.12%, GPT-4o 72.55% and Gemini-1.5-Pro 69.03%. [V] Latest: about 90%, with Gemini 3 Pro at about 90.1% and Claude Opus 4.5 (reasoning) at about 89.5% (https://intuitionlabs.ai/articles/mmlu-pro-ai-benchmark-explained ; https://artificialanalysis.ai/evaluations/mmlu-pro). [S]
- **Time to saturation:** about 1.5 years to reach about 90% (mid-2024 to late 2025). [S/I]
- **Label errors:** none quantified in sources seen this session. The inherited MMLU items were filtered. [I]
- **Adoption:**
  - It was one of 6 tasks on the Open LLM Leaderboard v2 (June 2024 to its March 2025 retirement) (https://huggingface.co/collections/OpenEvals/archived-open-llm-leaderboard-2023-2024). [V]
  - It is widely reported by open-weight labs such as DeepSeek and Qwen, and tracked by Artificial Analysis and Kaggle. [S]
- **Status:** **active, approaching saturation.**
- **Why it succeeded:** [I] It was a drop-in replacement with the same brand and format. Ten options cut the guess rate to 10% and reduce elimination tricks. It was adopted by a major neutral leaderboard at launch.
- **Why it is failing:** [I] It is still a public, static multiple-choice test on the same knowledge distribution, and reasoning models closed the gap in about 18 months.

### 1b. MMLU-Redux (label-error audit)

- **What it is:** an expert re-annotation of MMLU using an error taxonomy. [V]
- **Release / venue / creators:** "Are We Done with MMLU?", arXiv:2406.04127 (June 2024), NAACL 2025. First author Aryo Pradipta Gema, with colleagues at Edinburgh and elsewhere (https://aclanthology.org/2025.naacl-long.262/). [V]
- **Items:**
  - The paper describes 5,700 re-annotated questions across all 57 subjects. [V, search summary of paper]
  - The GitHub repo describes 30 subjects × 100 questions = 3,000 (https://github.com/aryopg/mmlu-redux). [V]
  - These look like two versions: MMLU-Redux 2.0 (5,700) and the original (3,000). [I, medium] [fact-check: the v1 arXiv abstract (June 2024) confirms "3,000 manually re-annotated questions across 30 MMLU subjects". The 5,700 / 57-subject version is unverified. Venue confirmed as NAACL 2025 (Vol. 1), pp. 5069–5096, with 16 authors from Gema to Minervini.]
- **Key findings:** 6.49% of MMLU is erroneous; 57% of analysed Virology items are erroneous; model rankings change on corrected subsets. [V]
- **Adoption:** reported in the DeepSeek-V3 and Qwen3 technical reports (DeepSeek-V3 scores 89.1) (https://arxiv.org/pdf/2412.19437 ; https://arxiv.org/pdf/2505.09388). [V via search summary]
- **Status:** **niche / active.** It is used as a cleaner MMLU by open-model labs.
- **Why it matters:** it is the canonical evidence that exam-benchmark ceilings are set by label noise, not model capability. [I]

### 1c. MMLU-CF (contamination-free MMLU)

- **What it is:** Microsoft, arXiv:2412.15194, ACL 2025 (main). Authors: Qihao Zhao, Yangyu Huang, Tengchao Lv, Lei Cui, … Furu Wei (https://github.com/microsoft/MMLU-CF). [V]
- **Items:** a 10,000-question open validation set and a 10,000-question **closed** test set, built with decontamination rules. [V]
- **Result:** GPT-4o scores 73.4% (5-shot) and 71.9% (0-shot), against 88.0% on MMLU. [V]
- **Status:** **niche.**
- **Lesson:** a closed test set combined with rewritten items exposes the contamination premium. [I]

### 2. GPQA and GPQA-Diamond

- **What it measures:** graduate-level, "Google-proof" multiple-choice questions in biology, physics and chemistry. [V]
- **Release / venue / creators:** arXiv:2311.12022 (November 2023), COLM 2024. Authors: David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe Pang, Julien Dirani, Julian Michael, Samuel R. Bowman (https://github.com/idavidrein/gpqa ; https://arxiv.org/abs/2311.12022). [V]
- **Items / format:** 448 questions in the main set. Diamond is a 198-question subset, kept only where both expert validators answered correctly and most non-experts answered incorrectly. [V]
- **Human baselines:**
  - Experts (holding or pursuing a PhD in the domain) score 65%, or 74% after discounting mistakes the experts later acknowledged.
  - Skilled non-experts score 34%, despite more than 30 minutes on average with unrestricted web access.
  - The GPT-4 baseline was 39%. [V] [fact-check: all four numbers confirmed verbatim from the abstract reproduced in the EleutherAI lm-evaluation-harness gpqa README. Akhtar et al. list the paper-time Diamond state of the art as 38.8 (GPT-4). The Diamond size of 198 was not re-fetched.]
- **Launch vs. frontier:**
  - Launch (November 2023): GPT-4 at 39%. [V]
  - o1 scored 78.3% on Diamond, against PhD experts at 69.7%, in September 2024 (https://openai.com/index/learning-to-reason-with-llms/). [fact-check: downgraded to U. openai.com is blocked and no mirror was found. Before citing, re-check which model (o1 or o1-preview) and which metric (pass@1 or consensus) the 78.3% refers to.]
  - GPT-5 pro scored 88.4% without tools in August 2025 (https://openai.com/index/introducing-gpt-5/). [V via search summary]
  - Gemini 3 Pro scored 91.9% in November 2025 (https://blog.google/products/gemini/gemini-3/). [V] [fact-check: confirmed via Simon Willison's transcription of Google's launch table, https://simonwillison.net/2025/Nov/18/gemini-3/, read from his GitHub blog backup. The same table gives GPT-5.1 88.1% and Claude Sonnet 4.5 83.4%.]
  - Gemini 3.1 Pro scored 94.3% in February 2026 (https://deepmind.google/models/model-cards/gemini-3-1-pro/). [fact-check: downgraded to U. The model card PDF exists ("Published: February 2026"), but its results table is an image and the number could not be read.]
  - Aggregators list about 93-94% for several models in mid/late 2026 (https://benchlm.ai/blog/posts/gpqa-diamond-science-benchmark). [S]
- **Time to saturation:** about 10 months to beat experts (November 2023 to September 2024), and about 2.3 years to reach about 94% [I]. That is effectively at the noise ceiling (see below).
- **Label errors:** Epoch AI's "GPQA Diamond: What's left?" (written when state of the art was about 83%) examined the items models consistently fail. It concluded that about 90-95% of Diamond questions are likely valid as written (https://epoch.ai/gradient-updates/gpqa-diamond-whats-left). [V via search summary] [fact-check: unverified. epoch.ai is blocked and no mirror was found; treat the noise-ceiling estimate as U until re-checked.] Implication: the ceiling is roughly 90-95%, and it is now reached. [I]
- **Contamination defences:** a canary string (`gpqa:4b24:...`), a **password-protected** data zip, and a request not to post examples online (https://github.com/idavidrein/gpqa). [V]
- **Adoption:**
  - It is in the headline tables of OpenAI, Google DeepMind and Anthropic model cards (GPT-5, Gemini 3/3.1, Claude Opus 4.5), on the Open LLM Leaderboard v2, and in the Epoch AI Benchmarking Hub. [V]
  - Epoch found that labs **accurately** self-report GPQA Diamond: self-reports fall within Epoch's confidence intervals (https://epoch.ai/data-insights/self-reported-gpqa). [V via search summary]
- **Status:** **saturated at the frontier** in 2026, though it still separates mid-tier models in the 60-90% range [S]. It is still reported.
- **Why it succeeded:** [I]
  - Expert-written questions, with a two-expert agreement filter plus a non-expert failure filter, give both validity and difficulty.
  - The "Google-proof" framing and the 34%-with-web non-expert baseline were uniquely persuasive.
  - It is small, so it is cheap to run.
  - Gated distribution kept it cleaner than MMLU.
  - It arrived just before reasoning models, so it became the default yardstick of the "o1 moment".
- **Why it is failing:** [I]
  - Only 198 Diamond items, so the standard error is about ±3 points at 80%. Differences between frontier models are within noise.
  - The multiple-choice format with 4 options is exploitable by elimination.
  - It is now above the estimated validity ceiling.

### 3. Humanity's Last Exam (HLE)

- **What it measures:** frontier expert-level, closed-ended academic questions. The question mix is about 41% maths, 11% biology and medicine, 10% CS/AI, 9% physics, 9% humanities and social science, 7% chemistry, 4% engineering and 9% other. About 14% of questions are multimodal. Formats are multiple choice or exact short answer, and calibration error is reported alongside accuracy (https://en.wikipedia.org/wiki/Humanity's_Last_Exam). [S: Wikipedia summary; V for the 2,500 and multimodal facts from the Nature abstract] [fact-check: the v1 paper (January 2025, 3,000 questions) states that 10% of questions require an image and 80% are exact-match. The 14% figure (current version) is unverified.]
- **Release / venue / creators:**
  - arXiv:2501.14249, submitted 24 January 2025 (https://arxiv.org/abs/2501.14249). [V]
  - Published in **Nature 649, 1139–1146 (2026)** as "A benchmark of expert-level academic questions to assess AI capabilities", DOI 10.1038/s41586-025-09962-4 (https://raw.githubusercontent.com/centerforaisafety/hle/main/citation.txt ; https://www.nature.com/articles/s41586-025-09962-4). [V]
  - The authors are the Center for AI Safety (CAIS), Scale AI and the HLE Contributors Consortium. Long Phan is listed first. [V]
  - Secondary sources place Nature publication in January 2026. [S]
- **Items / format:**
  - 2,500 public questions. Secondary sources report it launched with 3,000 and was cut to 2,500 after revisions. [V for 2,500; S for 3,000] [corrected by fact-check: 3,000 at launch is now V, from the v1 full text mirrored at https://raw.githubusercontent.com/averkij/top_papers/main/assets/json/2501.14249.json. The HLE README's example output shows an intermediate 2,700-question version ("n = 2700"). So the sequence was 3,000 → 2,700 → 2,500.]
  - A private held-out set also exists. [S]
  - Canary string `hle:3r2s:...` (https://github.com/centerforaisafety/hle). [V]
- **Construction:**
  - There were nearly 1,000 expert contributors from more than 500 institutions in about 50 countries. [S → V, v1 paper]
  - Questions had to stump frontier LLMs before going to expert review. More than 70,000 attempts were logged against the LLMs, and about 13,000 questions that stumped them were forwarded to expert human review. [corrected by fact-check: the dossier previously said "about 70,000 submissions passed that LLM filter", which is wrong. Per the v1 paper, 70,000+ were attempts and about 13,000 passed. Exact-match questions had to stump all test models, and multiple-choice questions all but one.]
  - Reviewers "were not expected to verify the full accuracy of each provided solution rationale if it would take more than five minutes", with an estimated 3-5 minutes per review. [V, v1 paper; added by fact-check]
  - A $500,000 prize pool paid $5,000 for each of the top 50 questions and $500 for each of the next 500 (https://scale.com/blog/humanitys-last-exam ; https://safe.ai/blog/humanitys-last-exam ; https://intuitionlabs.ai/articles/humanitys-last-exam-ai-benchmark). [S, consistent across 2-3 sources]
- **Launch vs. frontier:**
  - Launch (January 2025), in the current paper version: GPT-4o 2.7%, Claude 3.5 Sonnet 4.1%, o1 8.0% (calibration error 83%), DeepSeek-R1 8.5% (calibration error 73%). [fact-check: downgraded to U; not independently confirmed. The HLE README example shows gpt-4o-2024-11-20 at 3.07% ± 0.65% on the 2,700-question version.]
  - In the January 2025 v1: GPT-4o 3.3%, Grok 2 3.8%, Claude 3.5 Sonnet 4.3%, Gemini 1.5 Pro 5.0%, Gemini 2.0 Flash Thinking 6.2%, o1 9.1% and DeepSeek-R1 9.4%, on the full set except R1, which is text-only because it is not multimodal. RMS calibration errors ranged from 81.8% to 93.9%. v1 text-only results: GPT-4o 2.9%, o1 8.9%, DeepSeek-R1 9.4%. [corrected by fact-check: the dossier previously labelled GPT-4o 3.3% as "text-only", but that is the full-set figure. Source: v1 full text, https://raw.githubusercontent.com/averkij/top_papers/main/assets/json/2501.14249.json]
  - Perplexity Deep Research scored 21.1% with search in February 2025. [S]
  - Grok 4 Heavy scored 44.4% **with tools** in July 2025 (https://techcrunch.com/2025/07/09/elon-musks-xai-launches-grok-4-alongside-a-300-monthly-subscription/ ; https://www.scientificamerican.com/article/elon-musks-new-grok-4-takes-on-humanitys-last-exam-as-the-ai-race-heats-up/). [V via search summary]
  - GPT-5 pro scored 42% with tools in August 2025 (https://techcrunch.com/2025/08/07/openais-gpt-5-is-here/). [S]
  - Gemini 3 Pro scored **37.5% without tools** in November 2025 (https://blog.google/products/gemini/gemini-3/). [V] [fact-check: confirmed via Willison's transcription of Google's table. The same table gives 45.8% with search and code execution, GPT-5.1 26.5% and Claude Sonnet 4.5 13.7% (no tools).]
  - Gemini 3.1 Pro scored **44.4% without tools** in February 2026 (https://deepmind.google/models/model-cards/gemini-3-1-pro/). [fact-check: downgraded to U; the model-card results table is an image and could not be read.]
  - Late September 2026 figures from aggregators are **inconsistent**. They range from about 46-55% (Scale Labs public snapshot) to 59-65% (Epoch hub and other aggregators, e.g., "61.4%" for the top model on the Epoch hub). Figures vary with tools on or off, the HLE variant, and the grader (https://labs.scale.com/leaderboard/humanitys_last_exam ; https://epoch.ai/benchmarks/hle ; https://benchlm.ai/benchmarks/scale-humanitys-last-exam). [S, low confidence]
- **Time course:** about 8% to about 44% no-tools in 13 months [I from V points], an unusually fast climb for a benchmark branded "last".
- **Published critiques / label errors:**
  1. **FutureHouse (July 2025).** 29 ± 3.7% (95% CI) of text-only chemistry and biology answers had directly conflicting evidence in peer-reviewed literature. FutureHouse noted that reviewers spent only minutes per question and that full accuracy checks were not required. It released "HLE Bio/Chem Gold". The HLE team's own follow-up found about 18% of a Bio/Chem subset problematic (https://www.futurehouse.org/research/hle-exam ; https://the-decoder.com/nearly-29-percent-of-humanitys-last-exam-questions-are-wrong-or-misleading/). [V via two search summaries] [corrected by fact-check: HLE-Verified's reference list cites this as "Andrew White. About 30% of humanity's last exam chemistry/biology answers are likely wrong", July 2025, at https://www.futurehouse.org/research-announcements/hle-exam. That confirms the author, title, date and a headline of about 30%. The exact 29 ± 3.7% CI and the ~18% follow-up remain unverified because the primary page is blocked.]
  2. **HLE-Verified (arXiv:2602.13964, February 2026; Weiqi Zhai, Zhihai Wang et al.; 35 authors from Alibaba Group and the Qwen Team).** This was a two-stage expert-plus-model audit of all 2,500 items (https://arxiv.org/abs/2602.13964 ; https://github.com/SKYLENAGE-AI/HLE-Verified). [V; fact-check confirmed from the mirrored full text and the repo README]
     - The paper abstract reports 641 items verified correct and 1,170 revised and certified.
     - The repo reports Gold 668, Revision 1,143 and Uncertain 689. The difference is probably between versions [I].
     - Models gain 7-10 pp on the corrected set, and 30-40 pp on the originally erroneous items.
  3. **Epoch AI Benchmark Reviews (launched 17 September 2026).** Epoch audited a random stratified sample of 48 HLE questions (6 per category). 22 (46%) had substantial accuracy-altering errors, and 12 were impossible to answer as written. Verdict: **"Flawed"**. Across the programme, 9 of the first 15 reviewed benchmarks were rated Flawed, 4 Verified and 2 with insufficient information. "Flawed" most commonly means more than 20% of tasks have accuracy-impacting errors (https://epoch.ai/benchmarks/hle/review ; https://runtimewire.com/article/epoch-ai-benchmark-reviews-nine-flawed ; https://www.theneuron.ai/news/epoch-ai-benchmark-reviews-nine-flawed/). [V via search summaries of the Epoch page; date corroborated by the Epoch X post ID decoding to 2026-09-17] [fact-check: could NOT be independently confirmed. epoch.ai, runtimewire.com, theneuron.ai and x.com are all blocked, and no mirror was found. Treat every number in this item as U until the primary page is re-read.]
- **Maintainer response:**
  - **HLE-Rolling** is a continually updated fork that cleans items and swaps easy items for harder held-out ones. It is described as a "migration path" once models hit the noise ceiling. The repo changelog shows batches of edits dated 20 February 2026 and 27 July 2026 (https://github.com/centerforaisafety/hle/blob/main/hle-rolling-changes.txt ; https://huggingface.co/datasets/cais/hle-rolling). [V] [corrected by fact-check: from the fetched changelog, the counts are 20 February 2026: 166 re-added, 27 removed, 8 updated; 27 July 2026: 79 added, 6 removed.]
  - **HLE-Diamond** is a refined 1,000-question subset (500 reasoning and 500 knowledge, closed-book) released after "a year of review". It was announced by CAIS and Scale; the X post ID decodes to 23 September 2026 (https://lastexam.ai/blog/hle-diamond ; https://huggingface.co/datasets/cais/hle-diamond). [V for existence and size via search summary; model scores quoted there are S/low] [fact-check: not independently confirmed. lastexam.ai, huggingface.co and x.com are blocked, and the HLE GitHub README does not mention Diamond.]
- **Adoption:**
  - It is in the headline tables of Google (Gemini 3/3.1), OpenAI (GPT-5) and xAI (Grok 4) launches. [V]
  - Independent leaderboards include Scale Labs, Epoch, and Artificial Analysis. [V]
  - It was published in Nature. [V]
  - Prediction markets exist on its scores (e.g., "Highest score on HLE before 31 December 2026") (https://www.octagonai.co/markets/science-and-technology/ai/highest-score-on-humanity-s-last-exam-before-dec-31-2026/). [S]
- **Status:** **thriving but contested.** It is the most visible knowledge exam of 2025-26. It is climbing fast, and it is now officially "Flawed" per Epoch, with about 20-46% of items suspect depending on the audit. [fact-check: the Epoch verdict is unverified. The best-confirmed audit is HLE-Verified: only 641 of 2,500 (25.6%) verified correct as-is, 1,170 needed revision and 689 were indeterminate.]
- **Why it succeeded:** [I]
  1. Unforgettable framing ("Humanity's Last Exam").
  2. Launch-day headroom: frontier models were under 10%, and calibration error was reported alongside.
  3. Adversarial construction against the current frontier, so it was hard by design.
  4. Massive expert crowdsourcing with cash prizes, which gave breadth plus PR.
  5. Institutional backing (CAIS plus Scale) and a Nature paper.
  6. Private held-out questions plus a canary string.
  7. Active maintenance (Rolling, Diamond).
- **Why it is failing:** [I]
  1. The adversarial filter ("must stump the model") selects for items that are wrong, ambiguous or under-specified, as well as for items that are hard. Hard-but-wrong items survive because the model "failed" them. This is the likely root cause of the 20-46% error rates.
  2. Reviewers spent minutes per item, and there was no full solution verification.
  3. Exact-answer, closed-ended items conflate retrieval of obscure facts with reasoning.
  4. Tool-use (search) variants make it a different benchmark. Scores with and without tools diverge, and aggregators mix them.
  5. The public 2,500 items invite contamination.

### 4. SimpleQA (and SimpleQA Verified)

- **What it measures:** short-form, parametric factuality: single-answer, fact-seeking questions. It also measures hallucination through "not attempted" versus "incorrect". [V]
- **Release / venue / creators:** "Measuring short-form factuality in large language models", Jason Wei et al. (OpenAI), arXiv:2411.04368, blog "Introducing SimpleQA" (October/November 2024) (https://openai.com/index/introducing-simpleqa/ ; https://cdn.openai.com/papers/simpleqa.pdf). [V]
- **Items / format:**
  - 4,326 questions. Each answer was verified by two independent annotators.
  - Questions were **adversarially collected against GPT-4**: each tripped up at least one model during creation.
  - Grading is by a prompted ChatGPT grader. [V]
- **Estimated error rate:** about 3%. Of the disagreements OpenAI inspected, 2.8% were grader or human errors and 2.8% were genuine question issues. [fact-check: downgraded to U; not found in any reachable source.] The 4,326 count and "adversarially collected against GPT-4 responses" are confirmed (SimpleQA Verified, Table 2; SimpleQA abstract in the arXiv listing mirror).
- **Launch vs. frontier:**
  - Launch: GPT-4o 38.2%, o1-preview 42.7%. [fact-check: downgraded to U. OpenAI's simple-evals README instead lists SimpleQA o1-preview 42.4 and gpt-4o 39.0, 40.1 and 38.8 for the 2024-05-13, 08-06 and 11-20 snapshots. Cite simple-evals, or re-check the paper table and name the snapshot.]
  - GPT-4.5 scored 62.5%, with a 37.1% hallucination rate, in February 2025 (https://openai.com/index/introducing-gpt-4-5/). [V] [fact-check: 62.5 confirmed in the simple-evals README. 37.1% is corroborated by Willison (27 February 2025), who adds GPT-4o 61.8%, o3-mini 80.3% and o1 44% hallucination.]
  - o3-high scored 48.6% (https://github.com/openai/simple-evals). [V]
  - With retrieval, Perplexity Deep Research scored **93.9%** in February 2025 (https://x.com/perplexity_ai/status/1890452005472055673). [S] The task is essentially solved once a search tool is allowed. [I]
  - A Manifold market on ">90% before 2026" resolved NO for the closed-book setting. [S]
- **SimpleQA Verified:**
  - Google DeepMind and Google Research, arXiv:2509.07968 (September 2025). [V] Authors: Lukas Haas, Gal Yona, Giovanni D'Antonio, Sasha Goldshtein, Dipanjan Das. [added by fact-check from the mirrored full text]
  - 1,000 prompts. It fixes noisy or incorrect labels, topical bias and redundancy.
  - Gemini 2.5 Pro F1 55.6, GPT-5 52.3, Claude Opus 4 28.3. [V]
  - Gemini 3 Pro scored 72.1% in November 2025. [V via search summary of the Google blog and model card] [fact-check: confirmed via the Willison transcription. The same table gives GPT-5.1 34.9% and Claude Sonnet 4.5 29.3%.]
  - Kaggle leaderboard: https://www.kaggle.com/benchmarks/deepmind/simpleqa-verified
- **Adoption:** OpenAI system cards (GPT-4.5, o-series hallucination evaluations) and Google Gemini 3 model cards use SimpleQA Verified. Epoch's September 2026 Benchmark Reviews reportedly rated SimpleQA **"Verified"** (https://www.theneuron.ai/news/epoch-ai-benchmark-reviews-nine-flawed/). [S, medium]
- **Status:** **active.** As a closed-book hallucination and calibration metric it is not saturated. It is trivial with tools.
- **Why it succeeded:** [I]
  - Low label noise (about 3%), thanks to the single-answer design.
  - Measures abstention as well as accuracy, which matters for product hallucination.
  - Cheap to grade.
  - Came from a lab with distribution.
- **Why it is weakening:** [I]
  - It is adversarial only against GPT-4-era models.
  - It measures long-tail trivia rather than useful knowledge.
  - Search-enabled agents trivialise it.
  - The original set had enough noise and topical skew that Google rebuilt it.

### 5. BIG-bench, BIG-Bench Hard (BBH), BIG-Bench Extra Hard (BBEH)

**BIG-bench ("Beyond the Imitation Game")**

- **Release / venue / creators:** arXiv:2206.04615 (June 2022), TMLR 2023. 204 tasks from 450 authors at 132 institutions, led by Google (https://arxiv.org/abs/2206.04615). [V]
- **Items:** 204 tasks, spanning linguistics, maths, commonsense, biology, physics, social bias, code and more. BIG-bench Lite is a 24-task subset (https://github.com/google/BIG-bench). [V]
- **Contribution to practice:** it introduced the **canary string** convention to keep tasks out of training corpora. GPQA and HLE later reused it. [V]
- **Status:** **abandoned** as a headline benchmark. The GitHub repo was archived (read-only) on 17 April 2026, per the repo page (https://github.com/google/BIG-bench). [V via fetch, medium]
- **Why it faded:** [I]
  - It was too heterogeneous, with too many small tasks and variable quality, to give one number.
  - Running it was expensive.
  - Its lasting legacy is its hard subset (BBH) and the canary convention.

**BIG-Bench Hard (BBH)**

- **Release / venue / creators:** arXiv:2210.09261 (October 2022), Findings of ACL 2023. Mirac Suzgun, Nathan Scales, Nathanael Schärli, Sebastian Gehrmann, Yi Tay, Hyung Won Chung, Aakanksha Chowdhery, Quoc Le, Ed Chi, Denny Zhou, Jason Wei (https://aclanthology.org/2023.findings-acl.824/). [V]
- **Items:** 23 BIG-bench tasks on which prior models had not beaten the average human rater. [V]
- **Launch vs. frontier:** with chain-of-thought, PaLM beat the average human rater on 10 of 23 tasks, and Codex on 17 of 23. [V] By early 2025, state-of-the-art models scored above 90% (per the BBEH paper) (https://arxiv.org/abs/2502.19187). [V]
- **Adoption:** it was one of 6 tasks on the Open LLM Leaderboard v2. [V]
- **Status:** **saturated.** [corrected by fact-check: add nuance. Akhtar et al. (ICML 2026) say that "several of these benchmarks (e.g., ARC-AGI, BIG-Bench Hard) remain unsaturated despite prolonged exposure" by their top-5 separability index, which uses leaderboard data dominated by open-weight models. BBEH's "over 90%" refers to frontier state of the art. "Saturated" therefore holds for absolute accuracy at the frontier, not for model separability.]
- **Why:** [I] It was defined as "hard for 2022 models", and chain-of-thought plus scale removed the difficulty within about 2 years.

**BIG-Bench Extra Hard (BBEH)**

- **Release / venue / creators:** arXiv:2502.19187 (February 2025), ACL 2025. Mehran Kazemi, Bahare Fatemi, Hritik Bansal, John Palowitch, Chrysovalantis Anastasiou, Sanket Vaibhav Mehta et al. (Google DeepMind) (https://github.com/google-deepmind/bbeh ; https://aclanthology.org/2025.acl-long.1285/). [V] [fact-check: title, authors, 4,520 / 460 examples, 9.8% / 44.8% and BBH "over 90%" confirmed. The ACL 2025 venue is not confirmed: the repo BibTeX says arXiv preprint 2025.]
- **Items:** a one-to-one harder replacement for each of the 23 BBH tasks: 4,520 examples, with a 460-example mini version. It uses the **harmonic mean** as its headline metric, to penalise uneven skill profiles. [V]
- **Launch scores (harmonic mean / micro average):**
  - o3-mini (high): 44.8 / 54.2
  - DeepSeek R1: 6.8 / 34.9
  - Gemini 2.0 Flash: 9.8 / 23.9
  - GPT-4o: 6.0 / 22.3
  - Random: 2.4 / 8.4
  - Source: https://github.com/google-deepmind/bbeh/blob/main/leaderboard.md [V]
- **Latest:** aggregators list a top of about 64-67% in mid-2026 (https://pricepertoken.com/leaderboards/benchmark/bbeh). [S, low confidence; metric unclear]
- **Status:** **active / niche**, used mainly by Google.
- **Design lesson:** [I] a harmonic-mean aggregate resists saturation from strength in a few tasks.

### 6. HellaSwag

- **What it measures:** commonsense sentence completion. Choose the most plausible continuation of an ActivityNet or WikiHow context. [V]
- **Release / venue / creators:** arXiv:1905.07830, ACL 2019. Rowan Zellers, Ari Holtzman, Yonatan Bisk, Ali Farhadi, Yejin Choi (UW/AI2). [V]
- **Items / format:** about 70k problems in 4-way multiple choice, built by adversarial filtering against BERT. [V]
- **Launch vs. frontier:** humans score 95.6%. BERT-Large, the strongest model at launch, scored 47.3% [V]. GPT-4 scored 95.3% (10-shot) in March 2023 (https://cdn.openai.com/papers/gpt-4.pdf). [V] [fact-check: the abstract (lm-eval-harness hellaswag README) gives humans ">95%" and state of the art "<48%", consistent with 95.6 / 47.3. GPT-4 95.3% 10-shot is corroborated as "(reported)" in the Gemini 1.0 report. That report also shows HellaSwag contamination sensitivity: roughly 100 extra fine-tuning steps on web extracts raised Gemini Ultra to 96.0% (1-shot).]
- **Time to saturation:** about 4 years to human parity (2019 to 2023). [I]
- **Label errors / validity:**
  - "What the HellaSwag? On the Validity of Common-Sense Reasoning Benchmarks" (Chizhov et al., arXiv:2504.07825, April 2025) (https://arxiv.org/abs/2504.07825) found: [V]
    - up to 40% of prompts are ungrammatical, rising to 95.7% for the ActivityNet subset; [fact-check: unverified; not in the abstract]
    - more than 21% of items have multiple equally valid answers; [fact-check: unverified; not in the abstract]
    - more than 65% of model predictions are unchanged when the question is replaced by "Lorem ipsum" (or when models see only the answer texts); [fact-check: confirmed in the abstract. The authors are Pavel Chizhov, Mattia Nee, Pierre-Carl Langlais and Ivan P. Yamshchikov.]
    - the proposed GoldenSwag subset keeps 1,525 items (15.2%).
  - Surge AI reports that 36% of rows contain errors (https://surgehq.ai/blog/hellaswag-or-hellabad-36-of-this-popular-llm-benchmark-contains-errors). [S, vendor blog]
- **Adoption:** a staple of 2023 model cards (GPT-4, Llama, Falcon) and the Open LLM Leaderboard v1. It was removed in v2 (June 2024). [V]
- **Status:** **saturated / contested** (construct validity).
- **Why it succeeded:** [I] Cheap log-likelihood scoring, a large human–model gap at launch, and a catchy name.
- **Why it failed:** [I]
  - Adversarial filtering against one weak model (BERT) made items "hard" through artefacts, not through commonsense.
  - The noisy source data (ActivityNet captions) produced ungrammatical and ambiguous items.
  - Answer-only cues mean models can score without reading the context.

### 7. AI2 Reasoning Challenge (ARC; not ARC-AGI)

- **What it measures:** grade-school science multiple choice, split into an Easy set and a Challenge set. The Challenge set contains questions that both a retrieval solver and a PMI solver got wrong. [V]
- **Release / creators:** "Think you have Solved Question Answering? Try ARC, the AI2 Reasoning Challenge", Peter Clark et al., arXiv:1803.05457 (2018) (https://arxiv.org/abs/1803.05457). [V]
- **Items:** 7,787 questions, plus a 14M-sentence science corpus. [V] [fact-check: 7,787 confirmed, split into a Challenge Set of 2,590 and an Easy Set of 5,197. Authors: Clark, Cowhey, Etzioni, Khot, Sabharwal, Schoenick, Tafjord. Source: lm-evaluation-harness arc README.]
- **Launch vs. frontier:** GPT-4 scored 96.3% on ARC-Challenge (25-shot) in March 2023 (https://cdn.openai.com/papers/gpt-4.pdf). [V] 2018 launch baselines were near random on Challenge. [U]
- **Validity:** "ARC 'Challenge' Is Not That Challenging" (Findings of ACL 2025; https://aclanthology.org/2025.findings-acl.144.pdf) shows the following. [V via search summary; author names not verified this session]
  - Scores differ by **up to 35 points** depending on whether the model sees all options together or scores each option separately.
  - The chosen setup changes model rankings.
  - Much of the benchmark's perceived difficulty was an artefact of the evaluation protocol.
- **Adoption:** a staple of 2023 model cards and the Open LLM Leaderboard v1; removed in v2. [V]
- **Status:** **saturated / abandoned** for frontier models.
- **Lesson:** [I] Difficulty defined relative to 2018 information-retrieval solvers, not humans or experts, evaporates as soon as LMs arrive.

### 8. TruthfulQA

- **What it measures:** avoidance of "imitative falsehoods", i.e. common misconceptions humans repeat. [V]
- **Release / venue / creators:** arXiv:2109.07958, ACL 2022 (pp. 3214–3252). Stephanie Lin, Jacob Hilton, Owain Evans (https://aclanthology.org/2022.acl-long.229/). [V]
- **Items:** 817 questions in 38 categories (health, law, finance, politics…). It offers a generation format (judged by a fine-tuned GPT-judge) and multiple choice (MC1/MC2). [V]
- **Launch vs. frontier:** at launch the best model was about 58% truthful and humans about 94% [corrected by fact-check: upgraded to V. The abstract in the sylinrl/TruthfulQA README reads "The best model was truthful on 58% of questions, while human performance was 94%".] The repo baseline table lists UnifiedQA 3B at 53.86% "true" (https://github.com/sylinrl/TruthfulQA). [V]
- **Validity / gaming:**
  - Turner et al. (January 2025, Alignment Forum) show a simple decision tree reaches **79.6%** on multiple-choice TruthfulQA **without seeing the question**, using "odd-one-out" heuristics (https://www.alignmentforum.org/posts/57k6xNcWtAtsSTcor/gaming-truthfulqa-simple-heuristics-exposed-dataset). [V via search summary] [fact-check: unverified. alignmentforum.org is blocked and the TruthfulQA README does not mention it; confirm the authors and the 79.6% before citing.]
  - The authors responded with a new binary-choice multiple-choice setting in January 2025 (https://github.com/sylinrl/TruthfulQA ; https://www.alignmentforum.org/posts/Bunfwz6JsNd44kgLT/new-improved-multiple-choice-truthfulqa). [V]
  - The repo notes that some answers have become outdated: for example, models that can browse now answer "yes" truthfully to questions asking whether they can browse. [V]
- **Adoption:** in GPT-4 (2023) and many 2023 open-model cards, and on the Open LLM Leaderboard v1; removed in v2. [V] It is rarely reported by frontier labs in 2025-26. [I, S]
- **Status:** **abandoned / contested.**
- **Why it succeeded:** [I] It named a real failure mode (models repeating human misconceptions), which gave inverse-scaling results a story. It was small and cheap.
- **Why it failed:**
  - The multiple-choice format is exploitable. [V]
  - Its answers are time-dependent (world and model facts change). [V]
  - It is small and public, so it is easy to train on. [I]
  - Assistant post-training (RLHF) targets misconception-avoidance directly. [I]

### 9. WinoGrande

- **What it measures:** pronoun and commonsense resolution in Winograd-schema style, as binary fill-in-the-blank. [V]
- **Release / venue / creators:** arXiv:1907.10641, AAAI 2020. Keisuke Sakaguchi, Ronan Le Bras, Chandra Bhagavatula, Yejin Choi (https://aaai.org/papers/08732-winogrande-an-adversarial-winograd-schema-challenge-at-scale/). [V]
- **Items:** about 44k problems. Crowdsourced, then debiased with the AFLITE algorithm. Test labels are hidden, with an AI2 leaderboard (https://github.com/allenai/winogrande). [V]
- **Launch vs. frontier:** GPT-4 scored 87.5% (5-shot) in March 2023. [V] The human baseline is about 94% [U]. RoBERTa-era scores were about 79% [U].
- **Adoption:** in 2023 model cards and the Open LLM Leaderboard v1; removed in v2. [V]
- **Status:** **saturated / abandoned.**
- **Why:** [I] Binary choice gives a 50% floor and a compressed range. AFLITE's debiasing targeted surface biases detectable by 2019 models, not by LLMs. It was crowdsourced.

### 10. DROP (Discrete Reasoning Over Paragraphs)

- **What it measures:** reading comprehension requiring discrete operations (counting, sorting, arithmetic) over Wikipedia paragraphs, scored by F1 or exact match. [V]
- **Release / venue / creators:** NAACL 2019, Dheeru Dua et al. (https://aclanthology.org/N19-1246/). [V]
- **Items:** about 96k crowdsourced, adversarially created questions. [V]
- **Launch vs. frontier:** GPT-4 scored 80.9 F1 (3-shot) in March 2023, the one benchmark where GPT-4 did not beat fine-tuned state of the art. [V] o3-high scored 89.8 (https://github.com/openai/simple-evals). [V] OpenAI's simple-evals README states that DROP (and MGSM) are "saturated for our newer models". [V]
- **Scoring problems:** Hugging Face's "Open LLM Leaderboard: DROP deep dive" found that:
  - number normalisation failed on non-space whitespace;
  - floating-point answers were never matched;
  - using "." as a stop token truncated long answers.
  
  As a result, models with a true score of about 40 were scored at about 7. DROP was removed from the leaderboard (https://huggingface.co/blog/open-llm-leaderboard-drop). [V]
- **Status:** **saturated / abandoned.**
- **Why it failed:** [I] F1 string-matching over free-form answers is brittle across output styles, and crowdsourced adversarial questions were beaten by scale.

### 11. GLUE and SuperGLUE (the classic saturation story)

- **GLUE:**
  - Released in 2018. The human baseline is 87.1.
  - Microsoft's MT-DNN scored 87.6 on 8 June 2019, and the state of the art was 88.4 by July 2019. That is about 1 year after release (https://syncedreview.com/2019/06/18/microsoft-mt-dnn-surpasses-human-baselines-on-glue-benchmark-score/ ; https://arxiv.org/pdf/1905.00537). [V]
  - GLUE was released in April 2018 [S/U].
- **SuperGLUE:**
  - Wang et al., arXiv:1905.00537 (May 2019), a "stickier" successor. The human baseline is 89.8. [V]
  - BERT scored 69.0. RoBERTa scored 84.6 less than 3 months later. T5 scored 88.9. [V]
  - Microsoft's DeBERTa (1.5B) scored **89.9**, above the human baseline, on 29 December 2020 / January 2021 (https://www.microsoft.com/en-us/research/blog/microsoft-deberta-surpasses-human-performance-on-the-superglue-benchmark/). [V] [fact-check: the blog was fetched, published 6 January 2021. It gives single-model 89.9 vs. 89.8 macro-average and an ensemble of 90.3.]
- **Framing:** Kiela et al. (Dynabench, NAACL 2021) argue that surpassing human estimates used to take decades and now takes a few years. GLUE saturated within a year, and SuperGLUE had models at the top of its leaderboard (https://aclanthology.org/2021.naacl-main.324/). [V]
- **Status:** **abandoned** (historic).
- **Why it matters:** [I] It is the template for every later "harder successor" cycle: GLUE → SuperGLUE, MMLU → MMLU-Pro, BBH → BBEH, GPQA → HLE, HLE → HLE-Diamond. Each successor buys about 1-3 years.

---

## Cross-cutting success factors

Each factor has evidence and my synthesis.

1. **Expert authorship plus an agreement filter.** GPQA required two expert validators to agree and non-experts to fail. The 2026 ICML saturation study found **expert-curated benchmarks resist saturation better than crowdsourced ones** (Akhtar et al., arXiv:2602.16763). [V]
2. **Built-in, quantified headroom with a human anchor.** MMLU (44% model vs. about 90% expert), GPQA (39% model vs. 65-74% expert and 34% non-expert with web) and HLE (under 10% at launch) all launched far from the ceiling, with a crisp "beat the expert" narrative. [V/I]
3. **"Google-proof" or closed-book validity claims.** The non-expert-with-web control is GPQA's most distinctive design feature. It makes the benchmark about expertise, not retrieval. [V/I]
4. **Framing and branding.** "Humanity's Last Exam", "PhD-level", "Google-proof" and "Diamond" help labs use a benchmark in launch posts, which drives adoption. HLE plus Nature plus prediction markets is the extreme case. [I]
5. **Cheap, automatic, low-variance scoring.** Every successful exam here is multiple-choice or exact-match, and runs in minutes. [I]
6. **Contamination hygiene.** Canary strings (BIG-bench, GPQA, HLE), password-protected archives (GPQA), private held-out sets (HLE, MMLU-CF) and hidden test labels (WinoGrande, HellaSwag). [V] Caveat: the saturation study found that **public vs. private test data showed no protective effect against saturation** [V]. Hygiene protects validity, not longevity. [I]
7. **Maintenance and versioning.** Successor lines keep a brand alive while fixing flaws: MMLU → Pro/Redux/CF/MMMLU; SimpleQA → SimpleQA Verified; HLE → HLE-Rolling/HLE-Diamond; BBH → BBEH; TruthfulQA → binary multiple choice. [V]
8. **Neutral third-party re-evaluation.** Scale Labs, Epoch AI, Artificial Analysis, and the (retired) HF Open LLM Leaderboard. Epoch found that labs report GPQA Diamond accurately. Independent replication makes self-reported numbers credible and keeps a benchmark in circulation. [V/I]
9. **Metric design that resists gaming.** 10 options (MMLU-Pro) instead of 4, the harmonic mean across tasks (BBEH), calibration error (HLE), and abstention-aware scoring (SimpleQA). [V]

## Cross-cutting failure factors

1. **Saturation, faster every generation.** GLUE took about 1 year, SuperGLUE under 2, HellaSwag about 4, MMLU about 3, GPQA-Diamond under 1 to beat experts, and HLE went from under 10% to about 45% without tools in 13 months. About half of the 60 benchmarks studied are saturated (29 of 60 highly saturated or worse, 14 extreme) (arXiv:2602.16763). [V]
2. **Label noise becomes the ceiling.** MMLU 6.49%; MMLU Virology 57%; HellaSwag up to 40% ungrammatical and more than 21% with multiple valid answers; SimpleQA about 3%; GPQA-Diamond about 5-10%; HLE bio/chem 29 ± 3.7% (FutureHouse) or about 18% (HLE team); HLE overall 46% of a 48-item sample (Epoch). [fact-check: confirmed are MMLU Virology 57%, HellaSwag >65% Lorem-ipsum invariance, and HLE-Verified's 641 gold / 1,170 revised / 689 uncertain of 2,500. Unverified are MMLU 6.49%, SimpleQA ~3%, GPQA 5-10%, FutureHouse's exact 29 ± 3.7%, HLE-team 18% and Epoch 46%.] Once models are within about 10 points of 100%, rankings mostly measure agreement with wrong keys. [V/I]
3. **The adversarial-filter paradox.** Filtering for items that current models fail over-selects mislabeled or ambiguous items (HLE) or artefact-laden items (HellaSwag, filtered against BERT). The filter's model also defines "hard" only relative to one generation. [I, supported by the HLE audits and HellaSwag validity work]
4. **Format artefacts and shortcut solvability.** Answer-only cues (HellaSwag: 65% of predictions unchanged with Lorem-ipsum questions), odd-one-out heuristics (TruthfulQA-MC: 79.6% without the question), and scoring-protocol sensitivity (ARC-Challenge: up to 35 points). [V]
5. **Contamination.** Public test items from web sources (MMLU from practice exams) are memorised: TS-Guessing 57% for GPT-4, and a GPT-4o gap of about 15 points between MMLU and MMLU-CF. [V]
6. **Brittle scoring pipelines.** DROP's F1 normalisation bugs and the HLE and SimpleQA reliance on LLM graders introduce harness-dependent variance. Different harnesses then yield incompatible leaderboard numbers (as in the inconsistent September 2026 HLE figures across aggregators). [V/I]
7. **Small item counts.** GPQA-Diamond's 198 items and TruthfulQA's 817 give wide confidence intervals. Differences between frontier models become statistically meaningless before the benchmark "saturates". [I]
8. **Tool-use regime shift.** Closed-book knowledge tests become ill-defined once models browse. SimpleQA with search scores 93.9%, and HLE with and without tools gives different numbers. Leaderboards mix regimes. [V/I]
9. **Stale facts.** Time-sensitive answers rot, as in the TruthfulQA browsing questions. [V]
10. **Construct drift.** Benchmarks named for "commonsense" or "reasoning" (HellaSwag, ARC, WinoGrande) were shown to measure artefacts and protocol. Their construct validity collapsed before saturation did. [V/I]
11. **Ecosystem retirements.** HF Open LLM Leaderboard v1 → v2 in June 2024, then retired in March 2025 after evaluating more than 13K models, because it was "becoming obsolete" with reasoning models and assistants. OpenAI simple-evals stopped updating in July 2025. BIG-bench's repo was archived in April 2026. [V]

---

## Claims ledger

Each claim is numbered and given a confidence. Sources are the URLs where the claim was seen.

1. MMLU (Hendrycks et al., ICLR 2021) covers 57 subjects. GPT-3 175B few-shot scored 43.9% at launch. [high] https://arxiv.org/abs/2009.03300 ; https://iclr.cc/virtual/2021/poster/2962
2. GPT-4 (March 2023) reported MMLU 86.4%, HellaSwag 95.3%, ARC-Challenge 96.3%, WinoGrande 87.5% and DROP F1 80.9. [high] https://cdn.openai.com/papers/gpt-4.pdf ; https://arxiv.org/abs/2303.08774
3. Gemini Ultra (December 2023) scored 90.0% on MMLU, described as the first model to exceed the 89.8% human-expert estimate. [high] https://arxiv.org/pdf/2312.11805 [corrected by fact-check: 90.04% was with CoT@32; the model scored 83.7% under 5-shot. Confirmed from the report PDF, https://storage.googleapis.com/deepmind-media/gemini/gemini_1_report.pdf]
4. MMLU-Redux (Gema et al., NAACL 2025) estimates that 6.49% of MMLU questions contain errors, and that 57% of analysed Virology questions contain errors. [fact-check: 57% and NAACL 2025 confirmed; the 6.49% figure is unverified → medium] https://aclanthology.org/2025.naacl-long.262/ ; https://arxiv.org/abs/2406.04127
5. ChatGPT and GPT-4 reproduced masked MMLU answer options at 52% and 57% exact-match rates (TS-Guessing, NAACL 2024). [high] https://aclanthology.org/2024.naacl-long.482/ ; https://arxiv.org/abs/2311.09783
6. GPT-4o scores 88.0% (5-shot) on MMLU but 73.4% (5-shot) on the contamination-free MMLU-CF (ACL 2025). [high] https://github.com/microsoft/MMLU-CF ; https://arxiv.org/abs/2412.15194
7. MMLU-Pro has more than 12,000 questions with 10 options across 14 domains. It lowers accuracy by 16-33% versus MMLU and cuts prompt sensitivity from 4-5% to 2% (NeurIPS 2024). [high] https://github.com/TIGER-AI-Lab/MMLU-Pro ; https://arxiv.org/abs/2406.01574
8. The top MMLU-Pro scores reached about 90% by late 2025 or 2026 (Gemini 3 Pro about 90.1%). [medium-low; secondary aggregators] https://intuitionlabs.ai/articles/mmlu-pro-ai-benchmark-explained ; https://artificialanalysis.ai/evaluations/mmlu-pro
9. GPQA (Rein et al., COLM 2024) has 448 questions. Experts score 65% (74% discounting clear mistakes). Skilled non-experts score 34% despite more than 30 minutes of web access. The best GPT-4 baseline scored 39%. Diamond has 198 questions. [high] https://arxiv.org/abs/2311.12022 ; https://github.com/idavidrein/gpqa
10. o1 scored 78.3% on GPQA Diamond against 69.7% for PhD experts (OpenAI, September 2024). [fact-check: unverified; openai.com blocked → low until re-checked (o1 vs o1-preview?)] https://openai.com/index/learning-to-reason-with-llms/
11. Gemini 3 Pro scored 91.9% on GPQA Diamond and 37.5% on HLE without tools (November 2025). Gemini 3.1 Pro scored 94.3% on GPQA Diamond, 44.4% on HLE without tools and 92.6% on MMMLU (February 2026). [fact-check: the Gemini 3 Pro figures are confirmed via the Willison transcription of Google's table. The Gemini 3.1 Pro figures are unverified, because the model-card table is an image → medium] https://blog.google/products/gemini/gemini-3/ ; https://deepmind.google/models/model-cards/gemini-3-1-pro/
12. Epoch AI estimates that about 90-95% of GPQA Diamond questions are valid as written. [fact-check: unverified; epoch.ai blocked → low] https://epoch.ai/gradient-updates/gpqa-diamond-whats-left
13. Epoch AI found that AI developers' self-reported GPQA Diamond scores fall within Epoch's own confidence intervals. [medium] https://epoch.ai/data-insights/self-reported-gpqa
14. HLE was posted as arXiv:2501.14249 on 24 January 2025. It was published as "A benchmark of expert-level academic questions to assess AI capabilities", Nature 649, 1139–1146 (2026), DOI 10.1038/s41586-025-09962-4. [high] https://raw.githubusercontent.com/centerforaisafety/hle/main/citation.txt ; https://www.nature.com/articles/s41586-025-09962-4 ; https://arxiv.org/abs/2501.14249
15. HLE has 2,500 multimodal questions (multiple choice or short answer), designed to be unambiguous and not quickly answerable by internet retrieval. [high] https://www.nature.com/articles/s41586-025-09962-4 ; https://github.com/centerforaisafety/hle
16. HLE launch-era accuracies (current paper version) were GPT-4o 2.7%, Claude 3.5 Sonnet 4.1%, o1 8.0% and DeepSeek-R1 8.5%. [fact-check: unverified. The v1 values (3,000 questions) are confirmed: GPT-4o 3.3, Claude 3.5 Sonnet 4.3, o1 9.1, R1 9.4 → medium] https://arxiv.org/abs/2501.14249 ; https://en.wikipedia.org/wiki/Humanity's_Last_Exam
17. HLE had a $500,000 prize pool: $5,000 for each of the top 50 questions and $500 for each of the next 500. [corrected by fact-check: upgraded to high; confirmed in the v1 paper text] https://scale.com/blog/humanitys-last-exam ; https://intuitionlabs.ai/articles/humanitys-last-exam-ai-benchmark
18. FutureHouse (July 2025) found that 29 ± 3.7% (95% CI) of HLE text-only chemistry and biology answers conflict with peer-reviewed literature. An HLE-team follow-up found about 18% of a Bio/Chem subset problematic. [fact-check: the post (Andrew White, "About 30% ...", July 2025) is confirmed via the HLE-Verified reference list. The CI and the 18% figure are unverified → medium] https://www.futurehouse.org/research-announcements/hle-exam [URL corrected by fact-check] ; https://the-decoder.com/nearly-29-percent-of-humanitys-last-exam-questions-are-wrong-or-misleading/
19. HLE-Verified (arXiv:2602.13964) verified 641 items as correct and revised 1,170. Models gain 7-10 pp on average, and 30-40 pp on originally erroneous items. The repo's final split is Gold 668, Revision 1,143 and Uncertain 689. [fact-check: all numbers confirmed from the mirrored full text and the repo README → high] https://arxiv.org/abs/2602.13964 ; https://github.com/SKYLENAGE-AI/HLE-Verified
20. Epoch AI Benchmark Reviews (launched 17 September 2026) found substantial accuracy-altering errors in 22 of 48 sampled HLE questions (46%), 12 of them impossible as written, and rated HLE "Flawed". Nine of the first 15 benchmarks reviewed were rated Flawed. [fact-check: unverified; every source blocked, no mirror → low until re-checked] https://epoch.ai/benchmarks/hle/review ; https://runtimewire.com/article/epoch-ai-benchmark-reviews-nine-flawed
21. CAIS maintains HLE-Rolling, a continually updated fork, and released HLE-Diamond, a 1,000-question subset (500 reasoning and 500 knowledge). [fact-check: the HLE-Rolling changelog is confirmed (2026-02-20: 166 re-add / 27 remove / 8 update; 2026-07-27: 79 add / 6 remove). HLE-Diamond is unverified → medium-low] https://huggingface.co/datasets/cais/hle-rolling ; https://github.com/centerforaisafety/hle/blob/main/hle-rolling-changes.txt ; https://lastexam.ai/blog/hle-diamond
22. Grok 4 Heavy scored 44.4% on HLE with tools (July 2025). [fact-check: unverified; techcrunch.com blocked → medium] https://techcrunch.com/2025/07/09/elon-musks-xai-launches-grok-4-alongside-a-300-monthly-subscription/
23. SimpleQA has 4,326 questions and an estimated inherent error rate of about 3%. At launch GPT-4o scored 38.2% and o1-preview 42.7%. [fact-check: 4,326 confirmed. The ~3% and 38.2 / 42.7 figures are unverified; simple-evals lists o1-preview 42.4 and gpt-4o 38.8-40.1 by snapshot → medium] https://openai.com/index/introducing-simpleqa/ ; https://arxiv.org/abs/2411.04368
24. GPT-4.5 scored 62.5% on SimpleQA with a 37.1% hallucination rate (February 2025). [high] https://openai.com/index/introducing-gpt-4-5/
25. Perplexity Deep Research reported 93.9% on SimpleQA with search (February 2025). [medium; secondary] https://x.com/perplexity_ai/status/1890452005472055673
26. SimpleQA Verified (arXiv:2509.07968) has 1,000 prompts. Gemini 2.5 Pro scored F1 55.6, GPT-5 52.3 and Claude Opus 4 28.3. [high] https://arxiv.org/abs/2509.07968 ; https://www.kaggle.com/benchmarks/deepmind/simpleqa-verified
27. BIG-bench (TMLR 2023) has 204 tasks from 450 authors at 132 institutions. [high] https://arxiv.org/abs/2206.04615
28. BBH (Findings of ACL 2023) has 23 tasks. With chain-of-thought, PaLM beat average human raters on 10 of 23 and Codex on 17 of 23. By early 2025 state-of-the-art models exceeded 90%. [high] [fact-check: ">90%" confirmed in the BBEH text. Note that Akhtar et al. (ICML 2026) classify BBH as unsaturated by top-5 separability.] https://aclanthology.org/2023.findings-acl.824/ ; https://arxiv.org/abs/2502.19187
29. BBEH (ACL 2025) replaces each of the 23 BBH tasks. At launch the best harmonic-mean score was o3-mini (high) at 44.8, and the best general-purpose model was Gemini 2.0 Flash at 9.8. [high] https://github.com/google-deepmind/bbeh/blob/main/leaderboard.md
30. HellaSwag (ACL 2019): humans 95.6%, BERT-Large 47.3%. [high] https://arxiv.org/abs/1905.07830
31. "What the HellaSwag?" (arXiv:2504.07825) found up to 40% ungrammatical prompts and more than 21% of items with multiple valid answers. More than 65% of predictions were unchanged with "Lorem ipsum" in place of the question. [fact-check: >65% confirmed in the abstract. The 40% and 21% figures are unverified → medium] https://arxiv.org/abs/2504.07825
32. A decision tree can reach 79.6% on multiple-choice TruthfulQA without seeing the question. The authors released a binary multiple-choice variant in January 2025. [fact-check: the January 2025 binary variant is confirmed in the TruthfulQA README. The 79.6% decision-tree result is unverified → medium] https://www.alignmentforum.org/posts/57k6xNcWtAtsSTcor/gaming-truthfulqa-simple-heuristics-exposed-dataset ; https://github.com/sylinrl/TruthfulQA
33. On ARC-Challenge, scores differ by up to 35 points depending on the evaluation setup (Findings of ACL 2025). [fact-check: unverified; aclanthology.org blocked → medium] https://aclanthology.org/2025.findings-acl.144.pdf
34. HF's Open LLM Leaderboard removed DROP after finding normalisation and stop-token bugs that deflated scores (true about 40 scored about 7). [high] https://huggingface.co/blog/open-llm-leaderboard-drop
35. OpenAI's simple-evals stopped updating in July 2025 and describes DROP and MGSM as saturated. o3-high scores MMLU 93.3, GPQA 83.4, DROP 89.8 and SimpleQA 48.6. [high] https://github.com/openai/simple-evals
36. GLUE's human baseline of 87.1 was passed by MT-DNN (87.6) in June 2019. SuperGLUE's human baseline of 89.8 was passed by DeBERTa (89.9) around January 2021. [high] https://syncedreview.com/2019/06/18/microsoft-mt-dnn-surpasses-human-baselines-on-glue-benchmark-score/ ; https://www.microsoft.com/en-us/research/blog/microsoft-deberta-surpasses-human-performance-on-the-superglue-benchmark/
37. The Open LLM Leaderboard v1 (April 2023 to June 2024) used ARC-c, HellaSwag, MMLU, TruthfulQA, WinoGrande and GSM8K. v2 (from June 2024) used IFEval, MuSR, GPQA, MATH, BBH and MMLU-Pro. The leaderboard was retired in March 2025 after evaluating more than 13K models. [high] https://huggingface.co/collections/OpenEvals/archived-open-llm-leaderboard-2023-2024 ; https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard/discussions/1135
38. Akhtar et al. (ICML 2026, arXiv:2602.16763) studied 60 benchmarks and found nearly half saturated. Expert-curated benchmarks resist saturation better than crowdsourced ones, and public vs. private test data had no protective effect. [high] [fact-check: confirmed from the PMLR 306 PDF (29/60 high or very high; 14 very high). Nuance: curation categories are age-confounded (p = 0.0017). The paper says "Expert-curated benchmarks show lower saturation at comparable ages".] https://arxiv.org/abs/2602.16763 ; https://github.com/evaleval/benchmark-saturation
39. Late-2026 top HLE scores are between about 46% and 65%, depending on the source, the variant and whether tools are allowed. [low; inconsistent aggregators] https://labs.scale.com/leaderboard/humanitys_last_exam ; https://benchlm.ai/benchmarks/scale-humanitys-last-exam ; https://epoch.ai/benchmarks/hle

---

## References

These were seen during this session. Titles, venues and IDs are as seen. See `research/refs/knowledge_exams.json` for structured entries.

1. Hendrycks, D., Burns, C., Basart, S., Zou, A., Mazeika, M., Song, D., Steinhardt, J. *Measuring Massive Multitask Language Understanding.* ICLR 2021. arXiv:2009.03300. https://arxiv.org/abs/2009.03300
2. Gema, A. P., et al. *Are We Done with MMLU?* NAACL 2025. arXiv:2406.04127. https://aclanthology.org/2025.naacl-long.262/
3. Wang, Y., Ma, X., Zhang, G., et al. *MMLU-Pro: A More Robust and Challenging Multi-Task Language Understanding Benchmark.* NeurIPS 2024. arXiv:2406.01574. https://arxiv.org/abs/2406.01574
4. Zhao, Q., Huang, Y., Lv, T., Cui, L., et al. *MMLU-CF: A Contamination-free Multi-task Language Understanding Benchmark.* ACL 2025. arXiv:2412.15194. https://arxiv.org/abs/2412.15194
5. Deng, C., et al. *Investigating Data Contamination in Modern Benchmarks for Large Language Models.* NAACL 2024. arXiv:2311.09783. https://aclanthology.org/2024.naacl-long.482/
6. Rein, D., Hou, B. L., Stickland, A. C., Petty, J., Pang, R. Y., Dirani, J., Michael, J., Bowman, S. R. *GPQA: A Graduate-Level Google-Proof Q&A Benchmark.* COLM 2024. arXiv:2311.12022. https://arxiv.org/abs/2311.12022
7. Epoch AI. *GPQA Diamond: What's left?* Gradient Updates (date not verified). https://epoch.ai/gradient-updates/gpqa-diamond-whats-left
8. Epoch AI. *AI developers accurately report GPQA Diamond scores for recent models.* Data insight (date not verified). https://epoch.ai/data-insights/self-reported-gpqa
9. OpenAI. *Learning to Reason with LLMs.* Blog, September 2024. https://openai.com/index/learning-to-reason-with-llms/
10. Phan, L., et al. (CAIS & Scale AI). *Humanity's Last Exam.* arXiv:2501.14249, 2025. https://arxiv.org/abs/2501.14249
11. Center for AI Safety, Scale AI & HLE Contributors Consortium. *A benchmark of expert-level academic questions to assess AI capabilities.* Nature 649, 1139–1146 (2026). DOI:10.1038/s41586-025-09962-4. https://www.nature.com/articles/s41586-025-09962-4
12. White, A. (FutureHouse). *About 30% of Humanity's Last Exam chemistry/biology answers are likely wrong.* Research announcement, July 2025. https://www.futurehouse.org/research-announcements/hle-exam [corrected by fact-check: author and URL taken from the HLE-Verified reference list]
13. Zhai, W., Wang, Z., et al. *HLE-Verified: A Systematic Verification and Structured Revision of Humanity's Last Exam.* arXiv:2602.13964, 2026. https://arxiv.org/abs/2602.13964
14. Epoch AI. *Benchmark Review: Humanity's Last Exam.* September 2026. https://epoch.ai/benchmarks/hle/review
15. CAIS. *Humanity's Last Exam* GitHub repository, including the HLE-Rolling changelog. https://github.com/centerforaisafety/hle
16. CAIS / Scale AI. *Introducing HLE-Diamond.* Blog, around September 2026 (from the X post ID). https://lastexam.ai/blog/hle-diamond
17. Wei, J., et al. *Measuring short-form factuality in large language models* (SimpleQA). arXiv:2411.04368, 2024. https://openai.com/index/introducing-simpleqa/
18. Google DeepMind & Google Research. *SimpleQA Verified: A Reliable Factuality Benchmark to Measure Parametric Knowledge.* arXiv:2509.07968, 2025. https://arxiv.org/abs/2509.07968
19. OpenAI. *simple-evals* GitHub repository (deprecated July 2025). https://github.com/openai/simple-evals
20. OpenAI. *Introducing GPT-4.5.* Blog, February 2025. https://openai.com/index/introducing-gpt-4-5/
21. Srivastava, A., et al. (BIG-bench authors). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models.* TMLR 2023. arXiv:2206.04615. https://arxiv.org/abs/2206.04615
22. Suzgun, M., Scales, N., Schärli, N., Gehrmann, S., Tay, Y., Chung, H. W., Chowdhery, A., Le, Q., Chi, E., Zhou, D., Wei, J. *Challenging BIG-Bench Tasks and Whether Chain-of-Thought Can Solve Them.* Findings of ACL 2023. arXiv:2210.09261. https://aclanthology.org/2023.findings-acl.824/
23. Kazemi, M., Fatemi, B., Bansal, H., Palowitch, J., Anastasiou, C., Mehta, S. V., et al. *BIG-Bench Extra Hard.* ACL 2025. arXiv:2502.19187. https://aclanthology.org/2025.acl-long.1285/
24. Zellers, R., Holtzman, A., Bisk, Y., Farhadi, A., Choi, Y. *HellaSwag: Can a Machine Really Finish Your Sentence?* ACL 2019. arXiv:1905.07830. https://arxiv.org/abs/1905.07830
25. Chizhov, P., et al. *What the HellaSwag? On the Validity of Common-Sense Reasoning Benchmarks.* arXiv:2504.07825, 2025. https://arxiv.org/abs/2504.07825
26. Surge AI. *HellaSwag or HellaBad? 36% of this popular LLM benchmark contains errors.* Blog (date not verified). https://surgehq.ai/blog/hellaswag-or-hellabad-36-of-this-popular-llm-benchmark-contains-errors
27. Lin, S., Hilton, J., Evans, O. *TruthfulQA: Measuring How Models Mimic Human Falsehoods.* ACL 2022. arXiv:2109.07958. https://aclanthology.org/2022.acl-long.229/
28. Turner, A., et al. *Gaming TruthfulQA: Simple Heuristics Exposed Dataset Weaknesses.* Alignment Forum, January 2025. https://www.alignmentforum.org/posts/57k6xNcWtAtsSTcor/gaming-truthfulqa-simple-heuristics-exposed-dataset
29. TruthfulQA authors. *New, improved multiple-choice TruthfulQA.* Alignment Forum / LessWrong, January 2025. https://www.alignmentforum.org/posts/Bunfwz6JsNd44kgLT/new-improved-multiple-choice-truthfulqa
30. Sakaguchi, K., Le Bras, R., Bhagavatula, C., Choi, Y. *WinoGrande: An Adversarial Winograd Schema Challenge at Scale.* AAAI 2020. arXiv:1907.10641. https://aaai.org/papers/08732-winogrande-an-adversarial-winograd-schema-challenge-at-scale/
31. Clark, P., et al. *Think you have Solved Question Answering? Try ARC, the AI2 Reasoning Challenge.* arXiv:1803.05457, 2018. https://arxiv.org/abs/1803.05457
32. (Authors not verified.) *ARC 'Challenge' Is Not That Challenging.* Findings of ACL 2025. https://aclanthology.org/2025.findings-acl.144.pdf
33. Dua, D., et al. *DROP: A Reading Comprehension Benchmark Requiring Discrete Reasoning Over Paragraphs.* NAACL 2019. https://aclanthology.org/N19-1246/
34. Hugging Face. *Open LLM Leaderboard: DROP deep dive.* Blog. https://huggingface.co/blog/open-llm-leaderboard-drop
35. OpenAI. *GPT-4 Technical Report.* arXiv:2303.08774, 2023. https://arxiv.org/abs/2303.08774
36. Gemini Team, Google. *Gemini: A Family of Highly Capable Multimodal Models.* arXiv:2312.11805, 2023. https://arxiv.org/abs/2312.11805
37. Wang, A., et al. *SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems.* arXiv:1905.00537, 2019. https://arxiv.org/abs/1905.00537
38. Microsoft Research. *Microsoft DeBERTa surpasses human performance on the SuperGLUE benchmark.* Blog, January 2021. https://www.microsoft.com/en-us/research/blog/microsoft-deberta-surpasses-human-performance-on-the-superglue-benchmark/
39. Synced. *Microsoft MT-DNN Surpasses Human Baselines on GLUE Benchmark Score.* June 2019. https://syncedreview.com/2019/06/18/microsoft-mt-dnn-surpasses-human-baselines-on-glue-benchmark-score/
40. Kiela, D., et al. *Dynabench: Rethinking Benchmarking in NLP.* NAACL 2021. arXiv:2104.14337. https://aclanthology.org/2021.naacl-main.324/
41. Akhtar, M., Reuel, A., Soni, P., et al. *When AI Benchmarks Plateau: A Systematic Study of Benchmark Saturation.* ICML 2026. arXiv:2602.16763. https://arxiv.org/abs/2602.16763
42. Hugging Face. *Open LLM Leaderboard retirement ("It's been a wild ride, folks").* March 2025. https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard/discussions/1135
43. Google. *Gemini 3* launch blog. November 2025. https://blog.google/products/gemini/gemini-3/
44. Google DeepMind. *Gemini 3.1 Pro Model Card.* February 2026. https://deepmind.google/models/model-cards/gemini-3-1-pro/
45. OpenAI. *Introducing GPT-5.* August 2025. https://openai.com/index/introducing-gpt-5/
46. TechCrunch. *Elon Musk's xAI launches Grok 4 alongside a $300 monthly subscription.* 9 July 2025. https://techcrunch.com/2025/07/09/elon-musks-xai-launches-grok-4-alongside-a-300-monthly-subscription/
47. Anthropic. *System Card: Claude Opus 4.5.* November 2025. https://www.anthropic.com/claude-opus-4-5-system-card [fact-check: existence confirmed via redirect; the MMMLU 91.8% attribution is unverified and a possible mix-up with Gemini 3 Pro]

---

## Verification log

Adversarial fact-check performed 2026-09-29 by an independent sub-agent.

**Method and limits.** The session-wide WebSearch budget (200 calls) was already exhausted when this check started, so **no WebSearch was used**. The egress proxy blocked arxiv.org, export.arxiv.org, nature.com, openai.com, cdn.openai.com, blog.google, deepmind.google, epoch.ai, futurehouse.org, lastexam.ai, huggingface.co, aclanthology.org, alignmentforum.org, crossref, openalex, dblp and all news sites.

Evidence therefore comes only from reachable primary or near-primary sources:

- **Full-text or PDF mirrors:**
  - Akhtar et al. ICML 2026 PDF (PMLR 306), https://raw.githubusercontent.com/mlresearch/v306/main/assets/akhtar26a/akhtar26a.pdf
  - Full-text JSONs in `averkij/top_papers` for HLE v1 (2501.14249), HLE-Verified (2602.13964), SimpleQA Verified (2509.07968) and BBEH (2502.19187)
  - Gemini 1.0 report and Gemini 3 / 3.1 Pro model-card PDFs on storage.googleapis.com
- **Verbatim abstracts:**
  - arXiv daily-listing mirror `Luvata/arxive`, for MMLU-Redux v1, MMLU-Pro, SimpleQA and "What the HellaSwag?"
  - EleutherAI `lm-evaluation-harness` task READMEs, for GPQA, HellaSwag, ARC, WinoGrande, DROP and TruthfulQA
  - `lyy1994/awesome-data-contamination`, for Deng et al. and MMLU-CF
- **Official repo READMEs:**
  - hendrycks/test, TIGER-AI-Lab/MMLU-Pro, microsoft/MMLU-CF, idavidrein/gpqa
  - centerforaisafety/hle, including citation.txt and hle-rolling-changes.txt
  - SKYLENAGE-AI/HLE-Verified, openai/simple-evals, google-deepmind/bbeh, sylinrl/TruthfulQA, evaleval/benchmark-saturation
- **Reference lists** inside the fetched papers, used for venue, page and author checks.
- **Official pages:** the Microsoft Research DeBERTa blog (microsoft.com was reachable).
- **Transcription of a lab table:** Simon Willison's transcription of Google's Gemini 3 launch table, read from his GitHub blog backup (`simonw/simonwillisonblog-backup`, entry 2025-11-18). This is secondary but verbatim.

Verdict rule: a claim is **confirmed** when every load-bearing number was seen in an independent source this session, **corrected** when a component was wrong, **refuted** when it is false, and **unverifiable** when nothing contradicts it but at least one load-bearing number could not be confirmed.

### Claim verdicts

| ID | Verdict | Evidence (this session) | Sources |
|---|---|---|---|
| C1 MMLU-Redux 6.49% / Virology 57% / rankings change | **Unverifiable** (partly confirmed) | v1 abstract: "57% of the analysed questions in the Virology subset contain errors"; "significant discrepancies with the model performance metrics that were originally reported"; v1 = 3,000 questions / 30 subjects. NAACL 2025 (Vol. 1) pp. 5069–5096 and the 16-author list confirmed via the Akhtar et al. and HLE-Verified reference lists. **6.49% not found anywhere reachable.** The Llama-3.1-405B 16th→1st example is also unverified. | Luvata/arxive `pages/2024-06-07-cs-ai.html`; mlresearch/v306 akhtar26a.pdf |
| C2 MMLU GPT-3 43.9%; Gemini Ultra 90.0% > 89.8% | **Confirmed** (with nuance) | hendrycks/test README: GPT-3 175B few-shot 43.9, ICLR 2021. Gemini report: "achieving an accuracy of 90.04% … Human expert performance is gauged at 89.8% … Gemini Ultra is the first model t[o outperform]". Nuance added inline: this used **CoT@32**; 5-shot was 83.7% (GPT-4 reported 86.4%). | raw.githubusercontent.com/hendrycks/test/master/README.md; storage.googleapis.com/deepmind-media/gemini/gemini_1_report.pdf |
| C3 TS-Guessing 52%/57%; GPT-4o 88.0 vs 73.4 MMLU-CF | **Confirmed** | Deng et al. abstract: "ChatGPT and GPT-4 demonstrated an exact match rate of 52% and 57%". The method masks a *wrong* option (dossier wording fixed). MMLU-CF README and abstract: GPT-4o 73.4% 5-shot / 71.9% 0-shot (test), 88.0 MMLU; ACL 2025. NAACL 2024 venue for Deng et al. confirmed via the Akhtar reference list. | lyy1994/awesome-data-contamination README; github.com/microsoft/MMLU-CF |
| C4 MMLU-Pro >12k, 10 options, 14 domains, −16–33%, 4-5%→2% | **Confirmed** | arXiv abstract (listing mirror) plus README: "drop in accuracy by 16% to 33%", "4-5% in MMLU to just 2%" (24 prompt styles), >12,000 questions, 14 domains, NeurIPS 2024. | Luvata/arxive `2024-06-04-cs-cl.html`; github.com/TIGER-AI-Lab/MMLU-Pro |
| C5 GPQA 448; Diamond 198; experts 65/74%; non-experts 34% (>30 min web); GPT-4 39% | **Confirmed** (Diamond size not re-fetched) | Abstract reproduced verbatim in lm-evaluation-harness gpqa README confirms 448, 65% (74%), 34%, ">30 minutes … unrestricted access to the web" and 39%. BibTeX confirms COLM 2024 and the authors. Akhtar et al. Table 6 lists paper-time Diamond SOTA as 38.8 (GPT-4). The 198-item Diamond size was not re-seen. | raw.githubusercontent.com/EleutherAI/lm-evaluation-harness/main/lm_eval/tasks/gpqa/README.md; github.com/idavidrein/gpqa |
| C6 o1 78.3 vs 69.7; Gemini 3 Pro 91.9; Gemini 3.1 Pro 94.3; Epoch 90-95% valid | **Unverifiable** (partly confirmed) | Gemini 3 Pro GPQA Diamond 91.9% confirmed via Willison's transcription of Google's table. **o1 78.3/69.7, Gemini 3.1 Pro 94.3 and Epoch's 90-95% could not be checked.** openai.com and epoch.ai are blocked, and the 3.1 Pro model-card table is an image. The o1 figure should be re-checked for o1 vs o1-preview and pass@1 vs consensus. | simonwillison.net/2025/Nov/18/gemini-3/ via GitHub backup; Gemini-3-1-Pro-Model-Card.pdf |
| C7 HLE arXiv:2501.14249 / Nature 649, 1139-1146 (2026) / DOI | **Confirmed** | citation.txt gives Nature 649, 1139–1146 (2026), DOI 10.1038/s41586-025-09962-4, arXiv 2501.14249, authors CAIS, Scale AI and HLE Contributors Consortium. The README gives 2,500 questions. HLE-Verified cites "Center for AI Safety et al., 2026". The v1 full text confirms the arXiv version (Long Phan first author). | raw.githubusercontent.com/centerforaisafety/hle/main/citation.txt; top_papers 2501.14249.json |
| C8 HLE launch (current version) GPT-4o 2.7 / Sonnet 4.1 / o1 8.0 / R1 8.5; Gemini 3 Pro 37.5; 3.1 Pro 44.4 | **Unverifiable** (partly confirmed) | Gemini 3 Pro 37.5% no tools confirmed (also 45.8% with search + code). Current-version launch numbers and Gemini 3.1 Pro 44.4% **not confirmed**. v1 (3,000 questions) Table 1 confirmed: GPT-4o 3.3, Grok 2 3.8, Claude 3.5 Sonnet 4.3, Gemini 1.5 Pro 5.0, Gemini 2.0 Flash Thinking 6.2, o1 9.1, R1 9.4 (text-only). The dossier's "v1 text-only GPT-4o 3.3%" was corrected: that is the full-set figure, and text-only is 2.9%. | top_papers 2501.14249.json; Willison backup; hle README (gpt-4o-2024-11-20 3.07% on n = 2,700) |
| C9 FutureHouse 29 ± 3.7%; HLE team ~18% | **Unverifiable** (partly confirmed) | The post is confirmed via the HLE-Verified reference list: "Andrew White. About 30% of humanity's last exam chemistry/biology answers are likely wrong", futurehouse.org/**research-announcements**/hle-exam, July 2025. The URL was corrected. The CI and the 18% follow-up are unverified. | top_papers 2602.13964.json |
| C10 Epoch Benchmark Reviews: HLE 22/48 (46%), 12 impossible, "Flawed"; 9/15 Flawed; launched 17 Sep 2026 | **Unverifiable** | No reachable source. epoch.ai, runtimewire.com, theneuron.ai and x.com are blocked, Epoch's GitHub org has no reviews repo, and the Willison backup (to 2026-09-28) never mentions it. **Highest-risk claim in the dossier: re-check before citing.** | — |
| C11 HLE-Verified 641-668 verified; ~1,150 revised; +7-10 pp | **Confirmed** | Paper abstract: 641 verified, 1,170 revised-and-certified, 689 uncertain; "average absolute accuracy gain of 7--10 percentage points"; "30--40 percentage points" on erroneous items. Repo: Gold 668 / Revision 1,143 / Uncertain 689. 35 authors, Alibaba Group and Qwen Team. | top_papers 2602.13964.json; github.com/SKYLENAGE-AI/HLE-Verified |
| C12 SimpleQA 4,326, ~3% error, GPT-4o 38.2, o1-preview 42.7; SimpleQA Verified 1,000 | **Unverifiable** (partly confirmed) | Confirmed: 4,326 (SimpleQA Verified, Table 2); "adversarially collected against GPT-4 responses" (abstract); SimpleQA Verified has 1,000 prompts and fixes "noisy and incorrect labels, topical biases, and question redundancy"; F1 55.6 / 52.3 / 28.3; Gemini 3 Pro 72.1%. **~3% and 38.2/42.7 not found.** simple-evals lists o1-preview 42.4 and gpt-4o 38.8–40.1 by snapshot. | Luvata/arxive `2024-11-08-cs-cl.html`; top_papers 2509.07968.json; openai/simple-evals README; Willison backup |
| C13 HellaSwag: 40% ungrammatical, >21% multi-valid, >65% Lorem-ipsum; humans 95.6 / BERT-L 47.3; GPT-4 95.3 | **Unverifiable** (partly confirmed) | Confirmed: >65% Lorem-ipsum invariance ("What the HellaSwag?" abstract; authors Chizhov, Nee, Langlais, Yamshchikov); HellaSwag abstract gives humans ">95%" and SOTA "<48%"; GPT-4 95.3% 10-shot "(reported)" in the Gemini report. **40% and 21% are not in the abstract and are unverified.** | Luvata/arxive `2025-04-11-cs-cl.html`; lm-eval hellaswag README; gemini_1_report.pdf |
| C14 Akhtar et al. ICML 2026: 60 benchmarks, 14 properties, ~half saturated, expert > crowdsourced, private data no effect | **Confirmed** (with nuance) | PMLR 306 PDF abstract: "60 language model benchmarks using 14 properties … nearly half … exhibit saturation … resilience to saturation is impacted by expert-curation, not by public test data". 29/60 high or very high, 14 very high; 37 authors; ICML 2026, Seoul. Nuance: curation categories are age-confounded, and the paper says "Expert-curated benchmarks show lower saturation at comparable ages". It also names BIG-Bench Hard as *unsaturated*. | raw.githubusercontent.com/mlresearch/v306/main/assets/akhtar26a/akhtar26a.pdf |

**Totals:**

| Verdict | Count | Claims |
|---|---|---|
| Confirmed | 7 | C2, C3, C4, C5, C7, C11, C14 |
| Corrected (claim level) | 0 | — |
| Refuted | 0 | — |
| Unverifiable (all but C10 partly confirmed) | 7 | C1, C6, C8, C9, C10, C12, C13 |

Several claims had sub-parts that were corrected in the dossier text, or that needed nuance (see below). None of the 14 claims was refuted.

### Corrections made in the dossier text (marked inline "[corrected by fact-check]")

1. **HLE construction:** the dossier said "About 70,000 submissions passed that LLM filter", which is wrong. Per the v1 paper, more than 70,000 *attempts* were logged, and about 13,000 questions that stumped the LLMs were forwarded to expert review.
2. **HLE v1 scores:** GPT-4o 3.3% is the v1 *full-set* figure, not text-only; v1 text-only is 2.9% (o1 9.1% full / 8.9% text-only; R1 9.4%). HLE went 3,000 → 2,700 → 2,500 questions, and launch at 3,000 is now [V].
3. **Gemini Ultra MMLU 90.0%:** achieved with CoT@32; 83.7% at 5-shot. The "first above experts" framing is prompting-dependent.
4. **TS-Guessing:** the masked option is a *wrong* answer option.
5. **FutureHouse critique:** author (Andrew White), title and URL corrected to `https://www.futurehouse.org/research-announcements/hle-exam`, per the HLE-Verified reference list.
6. **Claude Opus 4.5 MMMLU 91.8%:** downgraded to U. The figure equals Gemini 3 Pro's MMMLU in Google's November 2025 table (possible mix-up).
7. **HLE-Rolling:** counts filled in from the changelog (2026-02-20: 166 re-add, 27 remove, 8 update; 2026-07-27: 79 add, 6 remove).
8. **BBH status:** nuance added. Akhtar et al. classify BBH as unsaturated by top-5 separability, although frontier accuracy is above 90%.
9. **TruthfulQA launch numbers** (best 58%, humans 94%): upgraded from U to V.
10. **SimpleQA launch numbers** (38.2 / 42.7) and ~3% error: downgraded to U. simple-evals gives o1-preview 42.4 and GPT-4o 38.8–40.1 by snapshot.
11. **Downgraded to U** (not refuted), each flagged inline: o1 78.3 vs 69.7; Gemini 3.1 Pro 94.3 / 44.4; the Epoch GPQA 90-95% estimate; the Epoch Benchmark Reviews numbers; HLE-Diamond; MMLU 6.49%; HellaSwag 40% / 21%; Turner et al. 79.6%; the ARC "up to 35 points" result; Grok 4 Heavy 44.4%.

### Reference check summary

All **48** entries in `research/refs/knowledge_exams.json` were checked; none were skipped. **32 are verified: true** and **16 are verified: false** (could not be confirmed this session; none were found to be fabricated).

Fixes applied in the JSON:

- **Full author lists** added or corrected for MMLU-Redux (16 authors), MMLU-Pro (17), Deng et al. (5), SimpleQA (8), SimpleQA Verified (Haas, Yona, D'Antonio, Goldshtein, Das; the dossier had "author list not verified"), "What the HellaSwag?" (4), ARC (7), DROP (6) and SuperGLUE (8).
- **HLE-Verified:** authors noted as 35 people from Alibaba Group and the Qwen Team.
- **Venues:** NAACL 2025 pp. 5069–5096 (MMLU-Redux), NAACL 2024 (Deng et al.), NeurIPS 2024 Datasets and Benchmarks (MMLU-Pro), ICML 2026 / PMLR 306 (Akhtar et al.).
- **DROP:** arXiv:1903.00161 added.
- **FutureHouse:** URL and author corrected.

Verified: false entries:

- epoch_gpqa_whatsleft, epoch_selfreported_gpqa, epoch2026hlereview
- openai2024o1, openai2025gpt45 (numbers corroborated secondarily), openai2025gpt5
- cais2026hlediamond
- surge_hellabad
- turner2025gamingtruthfulqa, arcnotchallenging2025
- hf_drop_deepdive, hf2025openllm_retire, hf_openllm_archive
- google2025gemini3 (numbers corroborated via transcription)
- synced2019mtdnn, techcrunch2025grok4

Unconfirmed details within verified entries:

- The BBEH "ACL 2025" venue (the repo BibTeX says arXiv 2025).
- The Gemini report's arXiv ID 2312.11805 (the title is confirmed).

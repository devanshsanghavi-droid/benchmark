# ARC-AGI as a case study: a benchmark built on an explicit theory of intelligence

Research dossier, compiled 2026-09-29. It covers:

- Chollet's 2019 framework;
- ARC-AGI-1, ARC-AGI-2 and ARC-AGI-3, together with the ARC Prize competitions around them;
- the efficiency (cost and action) axis, human calibration, dataset tiers and Kaggle compute limits;
- the main critiques;
- which of ARC's design principles can be carried over to a **non-game** benchmark.

Siblings cover related ground. `metascience_validity.md` covers general validity theory, and `other_dead_benchmarks.md` covers game benchmarks that failed to gain adoption. This file cross-references them only where needed.

**Evidence-gathering note (read this first).**

- The shared WebSearch budget for this session was already used up (200/200) before this subagent started.
- arcprize.org, arxiv.org and substack.com were blocked by the egress proxy. I tested this directly: `arcprize.org:443` returned `CONNECT 403` and `aiguide.substack.com` returned `EGRESS_BLOCKED`.

All evidence below therefore comes from sources I could reach:

1. **Official ARC Prize GitHub repositories.** These are `fchollet/ARC-AGI`, `arcprize/ARC-AGI-2`, `arcprize/docs` (the Mintlify source of docs.arcprize.org), `arcprize/arc-agi-benchmarking`, `arcprize/ARC-AGI-3-Agents`, `arcprize/ARC-AGI-3-Kaggle-Starter`, `arcprize/ARC-AGI-Community-Leaderboard` and `arcprize/hierarchical-reasoning-model-analysis`. I read them through raw.githubusercontent.com. They are primary sources.
2. **Verbatim third-party caches of primary documents,** found through GitHub code search:
   - the full text of the *ARC Prize 2024* and *ARC Prize 2025* technical reports, extracted from arXiv PDFs;
   - cached HTML of the arcprize.org o3 blog post (with its 2025 pricing updates) and a cached copy of the ARC-AGI-2 launch post;
   - an evidence packet captured **today (2026-09-29 05:49 UTC)** by a third-party benchmark-tracking repo. It holds the full text of arcprize.org/policy, arcprize.org/leaderboard, arcprize.org/arc-agi/1, arcprize.org/arc-agi/2 and the 14 Apr 2026 ARC-AGI-3 human-dataset blog post. It also holds machine summaries of the official leaderboard JSON files (`v1.json`, `v2.json`, `v3.json`);
   - a mirror of the Claude Opus 5 and Claude Fable 5.1 system cards;
   - a full Chinese translation of the ARC Prize "GPT-6 Astra on ARC-AGI-3" blog post (3 Sep 2026).
3. **Secondary sources:** newsletters (Interconnects), benchmark trackers (Epoch-derived data), and paper digests.

Tags used throughout:

- **[P]**: primary source read directly (an official repo or docs).
- **[P-c]**: primary text read through a verbatim third-party cache or mirror.
- **[P-t]**: primary text read through a translation.
- **[S]**: secondary source only.
- **[I]**: my interpretation.
- **[U]**: unverified background knowledge. [U] items are kept out of the claims ledger.

**Scope flag (the project avoids games).** ARC-AGI-1 and ARC-AGI-2 are static input→output puzzles, not games. **ARC-AGI-3 is explicitly game-like**:

- ARC's own docs call its environments "interactive game environments" and "hand crafted environments" with "levels" [P].
- The Claude Opus 5 system card calls them "novel, turn-based game environments" [P-c].

ARC-AGI-3 is covered here because it is the current flagship. Its *format* is therefore **not** a template for our non-game method (see "Transplantability" below).

---

## Summary

- **ARC is the clearest example of a benchmark whose durability comes from a stated theory rather than from a task list.**
  - Chollet (2019) defines intelligence as *skill-acquisition efficiency*. He argues that skill alone is a bad proxy, because "unlimited priors or unlimited training data allow experimenters to 'buy' arbitrary levels of skills" [P-c].
  - ARC puts this into practice through three constraints [P-c]:
    1. **novel tasks** with a unique logic for each task ("developer-aware generalization");
    2. **explicit, minimal priors** (Core Knowledge);
    3. **fair human–AI comparison.**
  - Every later ARC design decision can be traced to this theory [I]:
    - the cost axis (2024);
    - the "easy for humans" human-panel calibration (2025);
    - "action efficiency" relative to humans (2026).
- **Timeline.** Every step below is verified [P or P-c] unless tagged otherwise.
  - **ARC-AGI-1 (Nov 2019).** Pure deep learning scored ≤1% in the first Kaggle contest (2020). The top single entry reached 20%, but an ensemble of all 2020 entries reached 49%. The best score was still only 33% in early 2024.
  - **ARC Prize 2024 (launched 11 Jun 2024).** The Grand Prize was $600K. 1,430 teams submitted 17,789 entries. The best private-set score rose to 55.5% (MindsAI, not open-sourced); the best open-source winner scored 53.5% (the ARChitects).
  - **o3-preview (Dec 2024).** OpenAI's o3-preview scored **75.7%** on the semi-private set within the $10k budget and **87.5%** at about 172× compute. It had been trained on 75% of the public training set.
  - **ARC-AGI-2 (24 Mar 2025).** Every task was solved by at least 2 humans in at most 2 attempts. At launch, pure LLMs scored 0% and reasoning systems scored in single digits.
  - **ARC Prize 2025.** 1,455 teams submitted 15,154 entries; the top Kaggle score was 24.03% at $0.20/task.
  - **ARC-AGI-3 (25 Mar 2026).** An interactive format; at launch, frontier AI scored below 1%.
- **How fast each version fell (2025–2026).** After the o3 moment, each version was overtaken quickly:
  - **ARC-AGI-1** is saturated. Claude Opus 5 and GPT-5.6 Sol score 97.5%, against a human panel at 98% [P-c].
  - **ARC-AGI-2** reached **95.0% (GPT-6 Astra, Sep 2026, $1.12/task)** on the semi-private set, above the 85% prize threshold, within about 18 months [S, corroborated by the official `v2.json` maximum of 95 captured today].
  - **ARC-AGI-3** went from under 1% (Mar 2026) to **62.7% under ARC's standard harness (max effort) and 99.9% under a provider-designed harness (high effort)** (GPT-6 Astra, 3 Sep 2026) [P-t]. At the same (max) effort the pair is 62.7% vs 98.6% [corrected by fact-check].
- **What made ARC durable and culturally influential** [I, grounded in the evidence below]:
  1. a falsifiable philosophy ("easy for humans, hard for AI");
  2. human calibration of every item;
  3. a tiered private-data regime run by a neutral **steward** (a nonprofit with a testing policy and an academic panel);
  4. exact-match automatic scoring;
  5. mandatory efficiency reporting;
  6. prize money tied to open-sourcing;
  7. a willingness to **version the benchmark roughly every year** once it is beaten.
  - ARC's own 2025 report states the last point directly: "the most valuable and effective benchmarks are created by teams fundamentally committed to driving progress … a year-over-year commitment" [P-c].
- **Lab adoption.** Four frontier labs reported ARC-AGI in 2025 model cards: Anthropic, Google DeepMind, OpenAI and xAI [P-c]. Anthropic's July 2026 Claude Opus 5 system card has a dedicated ARC-AGI section with ARC-Prize-verified scores [P-c].
  - *Added by fact-check.* The mirrored **Claude Opus 5.5** system card (dated 22 Sep 2026 per a secondary source) has **no ARC-AGI row or section** in its capability summary table or in §§8.1–8.17 [P-c mirror; Medium confidence, because mirror completeness is not verified]. [I] This is a possible early sign that labs drop a benchmark from headline tables once it saturates.
- **Main failure modes.** All are documented by ARC itself [P-c/P-t]:
  - a small private set (100 tasks) probed by about 10,000 score reports;
  - 49% of ARC-AGI-1 was brute-forceable;
  - difficulty was inconsistent across splits;
  - accuracy can be "bought" with compute;
  - "knowledge overfitting": frontier models learned ARC's colour encoding, so the benchmark was contaminated without any memorised items;
  - large harness sensitivity on ARC-AGI-3 for the same model: 62.7% → 99.9% best-vs-best (37 points, but across different effort settings), or 62.7% → 98.6% at the same max effort (36 points) [corrected by fact-check];
  - rapid saturation once the format became a lab target.
- **External critiques add validity questions** [P-c/S]:
  - Accuracy overestimates abstraction in text form: models pass using surface "shortcuts" (Beger, Mitchell et al. 2025).
  - Representation choices matter a great deal: a vision transformer trained from scratch reaches 60.4% on ARC-1 (VARC).
  - The individual human average is far below the "human panel" figure: 64.2% on ARC-AGI-1 eval (H-ARC) and about 60–66% on ARC-AGI-2 [P/P-c].

---

## Benchmark-by-benchmark

### 0. Foundation: Chollet (2019), "On the Measure of Intelligence"

- **What it argues** [P-c, verbatim abstract via caches]:
  - The field benchmarks intelligence by "comparing the skill exhibited by AIs and humans at specific tasks, such as board games and video games". Skill is "heavily modulated by prior knowledge and experience".
  - The paper "articulate[s] a new formal definition of intelligence based on Algorithmic Information Theory, describing intelligence as skill-acquisition efficiency and highlighting the concepts of scope, generalization difficulty, priors, and experience".
  - It proposes "a set of guidelines for what a general AI benchmark should look like".
  - It presents ARC, "built upon an explicit set of priors designed to be as close as possible to innate human priors". It argues that ARC "enables fair general intelligence comparisons between AI systems and humans".
  - *Note for our project:* the paper's opening critique is aimed squarely at game-based benchmarking. This is the intellectual root of the user's intuition that games are a weak basis for benchmarks [I].
- **Release.** arXiv:1911.01547 [cs.AI], v1 dated 5 Nov 2019, v2 dated 25 Nov 2019 [P-c]. The `fchollet/ARC-AGI` repo was created on 2019-11-05 [P].
- **Original ARC design, as stated in the paper** [P-c]:
  - 400 training tasks and 600 evaluation tasks, 1,000 in total.
  - About 3.3 demonstrations per task on average, and usually 1 test input.
  - 10 symbols (colours); grids from 1×1 to 30×30.
  - The test-taker must construct the output grid from scratch, including its size.
  - Success is binary and exact.
  - The benchmark aims at "developer-aware generalization … by only featuring novel tasks in the evaluation set".
  - ARC "does not involve language, pictures of real-world objects, or real-world common sense".
- **Self-declared weaknesses** (§III.2) [P-c]:
  - "Generalization is not quantified."
  - "Test validity is not established."
  - "Dataset size and diversity may be limited."
  - "Core Knowledge priors may not be well understood and may not be well captured in ARC."
  - Stating limits this candidly up front is itself a trust-building design choice [I].
- **Primary sources:**
  - https://arxiv.org/abs/1911.01547, text seen via https://raw.githubusercontent.com/commotum/4D/6dd4d04fd21a681d337e4342beb6ef51e0476a07/Notes/Vision/pdfs-3/2019_MOI.md
  - abstract quoted in https://raw.githubusercontent.com/Interconnects-AI/homebase/b2c74a0cb0765f2c65abe8cbc8ba48d5ff877d7a/public/2024/2024-12-20-openaiso3thegrandfinaleofaiin2024.md

### 1. ARC-AGI-1: the original Abstraction and Reasoning Corpus (2019–2024)

- **What it measures.** Few-shot induction of a novel grid transformation from about 3 demonstration pairs. It uses only Core Knowledge priors: "objectness, basic topology, elementary integer arithmetic" [P-c, 2024 report].
- **Release date and venue.**
  - Released Nov 2019 alongside arXiv:1911.01547, with the GitHub repo `fchollet/ARC-AGI` [P].
  - Later renamed from "ARC" to "ARC-AGI" "to avoid name collisions with other AI benchmarks" [P-c].
- **Creators.** François Chollet, then at Google [P-c]. Since 2024 it has been stewarded by the ARC Prize Foundation, co-founded by Chollet and Mike Knoop in April 2024 and led by president Greg Kamradt [P-c, policy page captured 2026-09-29].
- **Item count and format.** Now 1,000 tasks [P-c]:
  - public training: 400, easy;
  - public evaluation: 400, hard;
  - semi-private: 100, "introduced in mid-2024 … hand selected … when testing closed source models";
  - private: 100, used as the final leaderboard in 2020, 2022, 2023 and 2024.
  - Tasks are JSON; grids are integers 0–9 up to 30×30.
  - The original README allowed 3 trials per test input [P]. ARC Prize scoring uses **2 attempts** (pass@2) [P-c].
- **Frontier score at launch vs latest.**
  - *At launch and in the pre-LLM era* [P-c]:
    - No deep-learning entry exceeded 1% in the 2020 Kaggle contest.
    - GPT-3 scored 0% by direct prompting.
    - The 2020 Kaggle winner, icecuber, reached 20% using brute-force DSL search.
    - The best score was 33% by early 2024, and 55.5% by Nov 2024 (ARC Prize 2024).
  - *Pass@1 prompting baselines, end of 2024, semi-private* [P-c]: o1-preview 18%, Claude 3.5 Sonnet 14%, GPT-4o 5%, Gemini 1.5 4.5%.
  - *o3-preview, 20 Dec 2024* [P-c]:
    - 75.7% semi-private at 6 samples, and 87.5% at 1,024 samples (about 172× compute);
    - on the public eval, 82.8% and 91.5% respectively.
  - *Released o3, Apr 2025* [P-c, leaderboard snapshot mirrored Dec 2025]: 60.8% (high, $0.50/task).
  - *Dec 2025* [P-c snapshot]: GPT-5.2 Pro (X-High) 90.5% at $11.65/task; GPT-5.2 (X-High) 86.2% at $0.96/task.
  - *Jul–Sep 2026*:
    - 97.5% for Claude Opus 5 (max) and GPT-5.6 Sol (xhigh) (Opus 5 system card, Table 8.1.A) [P-c]. *Fact-check note:* the Claude Fable 5.1 card's Table 8.1.A lists GPT-5.6 Sol at **96.5%** on ARC-AGI-1, with no effort label. Competitor figures therefore differ across cards by effort setting [corrected by fact-check];
    - 97.5% for Claude Fable 5.1 [P-c];
    - 98.5% for GPT-6 Astra (xhigh) and Claude Fable 5 (xhigh) [S, Epoch-derived tracker]. The Fable 5 figure is also in the Fable 5.1 card's Table 8.1.A [P-c, added by fact-check].
  - *Human reference points:*
    - 2025 human panel: 98% on the semi-private set [P-c snapshot];
    - the original private tasks were tested by 2 people who scored 97% and 98% [P-c];
    - the H-ARC individual average on the public eval is 64.2% [S/P-c].
- **Adoption evidence.**
  - Four ARC competitions: Kaggle 2020 ($20K), ARCathon 2022 ($100K), ARCathon 2023 ($100K) and ARC Prize 2024 [P-c].
  - ARC Prize 2024 [P-c]:
    - Prizes were a $600K Grand Prize at 85%, $50K progress prizes and $75K paper prizes. The Grand Prize was not claimed.
    - The Kaggle leaderboard ran on a P100 GPU for up to 12 h with no internet, about $10 of compute per entry.
    - A separate ARC-AGI-Pub leaderboard allowed up to $10,000 of API spend on the semi-private set, about 1,000× more compute.
    - ARC reported that "at least seven distinct efforts" by companies with more than $1M in funding were working on the benchmark.
  - OpenAI chose ARC-AGI-1 as the headline benchmark in the o3 livestream; ARC co-presented with Sam Altman and Mark Chen [P-c].
  - The `fchollet/ARC-AGI` repo had 4,839 stars and 727 forks on 2026-09-29 [P].
- **Status.** **Saturated.** The frontier (about 97.5–98.5%) is at the human-panel level (98%). ~~ARC itself describes ARC-AGI-1 as "solved"~~ The captured arc-agi/1 page (2026-09-29) frames ARC-AGI-1 historically ("endured five years of global competitions, a 50,000x scale-up of base LLMs") and points to ARC-AGI-2 as "the next iteration". I found no ARC text calling it "solved"; that label is my interpretation [corrected by fact-check]. The leaderboard is still updated: 20 model rows changed in `v1.json` today [P-c].
- **Why it succeeded** [I, with the evidence above]:
  1. It resisted the 2020–2024 LLM scale-up. ARC says it survived "a 50,000x scale-up of base LLM pretraining" [P-c]. That made it the single cleanest counter-example to "scale is all you need", which is a strong cultural hook.
  2. It **detected a real regime change**: test-time adaptation and reasoning models in late 2024. It did so before most knowledge benchmarks registered one [P-c].
  3. It is cheap to run and exact-match scored, and its format is human-playable and easy to show on social media.
  4. A prize and a steward arrived exactly when the benchmark became relevant (2024).
- **Why it failed or is failing** [P-c unless tagged]:
  1. **Small private set, reused for years.** About 10,000 private-set scores had been reported to participants by 2024: "a significant risk of overfitting, since each score has the potential to extract a tiny but non-zero amount of information about the content of the hidden tasks."
  2. **Brute-force susceptibility.** "49% of the private evaluation set was solved by at least one team" in 2020, all using brute-force program search, so "a large fraction … does not carry a useful signal towards AGI."
  3. **Inconsistent difficulty across splits.** "The different evaluation datasets are not drawn from a consistent human difficulty distribution." The public eval is easier than the semi-private set, which is why the ±10 pp agreement rule exists.
  4. **Compute purchasability.** o3 needed about 172× compute for +11.8 pp. This forced ARC to make cost reporting mandatory.
  5. **The "tuned" confound.** "OpenAI shared they trained the o3 we tested on 75% of the Public Training set." Also, the released o3 "is not the same as the one we tested".
- **Key sources:**
  - 2024 report text: https://raw.githubusercontent.com/UNIR-TUC/arc-agi/48d931918edd904b99ef546a98adc97e19ccf528/src/SuperCompressARC/Docs/2024/2412.04604v2_arc_prize_2024.md
  - o3 blog cache: https://raw.githubusercontent.com/ndbroadbent/arc_agi_pareto_frontiers/90d0c6822f82b8ef95423f2a37c74cdb45e7b40f/sources/o3_announcement.html
  - repo: https://raw.githubusercontent.com/fchollet/ARC-AGI/master/README.md
  - arc-agi/1 page capture: https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-1/packet-r1.md

#### 1a. The o3-preview result (Dec 2024) and its compute cost: the "efficiency axis" moment

The testing report was published by Chollet on 20 Dec 2024. The table below is as it appears in the cached page, which already includes pricing updates made on 24 Mar 2025 and 10 Dec 2025 [P-c].

| Set | Tasks | Config | Score | Total cost | Samples | Tokens | Cost/task | Time/task |
|---|---|---|---|---|---|---|---|---|
| Semi-Private | 100 | High-efficiency | 75.7% | $2,680 | 6 | 33.5M | $26 | 1.3 min |
| Semi-Private | 100 | Low-efficiency | 87.5% | $456,000 | 1,024 | 5.7B | $4,560 | 13.8 min |
| Public | 400 | High-efficiency | 82.8% | $66,772 | 6 | 111M | $167 | n/a |
| Public | 400 | Low-efficiency | 91.5% | $760,000 | 1,024 | 9.5B | $1,900 | n/a |

- **Cost notes.**
  - The notes say the costs were re-based twice: first to o1-pro pricing (3/24/2025), then to "o3-pro pricing of $80/M/Tokens" (12/10/2025) [P-c].
  - The ARC-AGI-2 launch post (Mar 2025) listed o3-preview-low at **$200/task** [P-c]. The Dec 2025 leaderboard snapshot also lists $200/task [P-c mirror].
  - So the *same run* has been reported at $200/task and at $26/task depending on the assumed price schedule [I]. **Cost-per-task depends on the pricing assumed, not only on the system**, and any cost axis we adopt must pin the price table and its date.
- **Policy change.**
  - ARC's stated rule after this result: "Due to variable inference budget, efficiency (e.g., compute cost) is now a required metric when reporting performance" [P-c].
  - The high-efficiency 75.7% fit within the ARC-AGI-Pub budget rule of under $10k and took first place. The 87.5% run did not [P-c].
- **How ARC framed the result** [P-c]:
  - ARC called it "a genuine breakthrough", but "not an acid test for AGI": "o3 still fails on some very easy tasks."
  - It predicted that ARC-AGI-2 would cut o3's score to "under 30% even at high compute (while a smart human would still be able to score over 95% with no training)".
  - It also stated: "You'll know AGI is here when the exercise of creating tasks that are easy for regular humans but hard for AI becomes simply impossible."
- **Openness.** ARC published o3's outputs, prompt and results for community analysis [P-c].
- **Secondary commentary.** Interconnects [S] relays Mike Knoop's progression on ARC-AGI-1 from X: GPT-2 0%, GPT-3 0%, GPT-4 2%, GPT-4o 5%, o1-preview 21%, o1 high 32%, o1 Pro about 50%, o3 tuned-low 76%, tuned-high 87%. It notes that the prize was "not claimed because it was above a cost threshold and not open-sourced".

### 2. ARC-AGI-2 (released 24 Mar 2025)

- **What it measures.** The same input→output grid format, with tasks chosen to be "even harder for AI (in particular, AI reasoning systems), while maintaining the same relative ease for humans" [P-c]. The three targeted weaknesses are **symbolic interpretation**, **compositional reasoning** and **contextual rule application** [P-c, arc-agi/2 page captured today].
- **Release date and venue.**
  - Launched 24 Mar 2025 in the blog post "ARC-AGI-2 + ARC Prize 2025 is Live!" by Greg Kamradt [P-c]. The repo changelog confirms: "2025-03-24 1,360 ARC-AGI-2 released" [P].
  - Paper: "ARC-AGI-2: A New Challenge for Frontier AI Reasoning Systems", arXiv:2505.11831, 17 May 2025 [P-c abstract].
- **Creators.** François Chollet, Mike Knoop, Gregory Kamradt, Bryan Landers and Henry Pinkard, per the paper's arXiv metadata and BibTeX [P-c/S].
- **Item count and format** [P; P-c]:
  - 1,000 public training tasks (ARC-AGI-1 tasks plus new ones), 120 public eval, 120 semi-private and 120 private.
  - Discrepancy: the 2025 technical report's text lists "Public training tasks (400, imported from ARC-AGI-1)". The repo and launch post both say 1,000. I treat 1,000 as correct and flag the discrepancy.
  - Eval sets are "calibrated": IID, with scores comparable across sets to within an expected "<1pp", assuming no overfitting [P-c].
  - Pass@2. This is justified because "certain tasks have explicit ambiguity and require two guesses to disambiguate" [P-c].
  - Changelog versus v1 [P-c]:
    - 120 tasks per eval set, up from 100;
    - all tasks solved by the 2020 Kaggle entries were removed ("susceptible to brute force search");
    - controlled human testing was added;
    - new task types were designed.
  - Minor documentation drift: the README says both "2 trials" and "3 trials" for each test input [P].
- **Human calibration** [P-c; P]:
  - "Over 400 members of the general public" were tested in San Diego in early 2025.
  - "Every task … solved by at least 2 humans in 2 attempts or less." The 2025 report says each task was attempted by 2–10 humans.
  - The average individual scores well below the panel:
    - launch table: 60% average on ARC-AGI-2, versus 64.2% on ARC-AGI-1;
    - README: "Average human performance on these tasks in our test sample was 66%."
  - Human cost was reported as **$17/task**: a "$115–150 show-up fee, plus a $5/task solve incentive". ARC notes that "only 70% of registrations actually showed up" and believes "the true limit … is likely in the $2–5/task range".
- **Frontier score at launch vs latest.**
  - *Launch, 24 Mar 2025, pass@2, semi-private* [P-c]:

    | System | Score | Cost/task |
    |---|---|---|
    | o3-preview-low | about 4% (estimate) | $200 |
    | o1-pro | about 1% | $200 |
    | ARChitects (2024 winner) | 3% | $0.25 |
    | o3-mini-high | 0.0% | n/a |
    | r1 | 0.3% | n/a |
    | GPT-4.5 | 0.0% | n/a |
    | Human panel | 100% | $17 |

  - *Paper Table 1, as of 14 May 2025* [S tracker]: o3 (medium) 3.0%.
  - *Released o3 (high)* [P-c snapshot]: 6.5%.
  - *Late 2025* [P-c snapshot, plus the 2025 report]:
    - GPT-5.2 Pro (High): 54.2%, $15.72/task.
    - GPT-5.2 (X-High): 52.9%, $1.90/task.
    - Gemini 3 Pro with the Poetiq refinement harness: 54% at $31/task, up from a 31% baseline at $0.81/task.
    - Claude Opus 4.5 (64k): 37.6%.
    - The top Kaggle (open-source, compute-limited) score was NVARC at **24.03%** on the private set, at $0.20/task.
  - *2026*:
    - Gemini 3 Deep Think (2/26): 84.6% at $13.62/task (Feb 2026) [S tracker].
    - Claude Opus 4.7: 75.83% [P-c, Opus 5 card].
    - Claude Opus 5 (max): **90.42%** [P-c]. GPT-5.6 Sol: **92.5%** [P-c, Opus 5 card Table 8.1.A]. *Fact-check note:* the card lists Sol's 92.5 as a competitor figure "drawn from the respective developers' published system cards or benchmark leaderboards", with no effort label. The "(max)" label, $1.44/task and ARC-verified status come from the alloevil tracker, which cites the official leaderboard [S] [corrected by fact-check]. Claude Fable 5.1: **90%** [P-c].
    - **GPT-6 Astra (max): 95.0% at $1.12/task (ARC Prize leaderboard, Sep 2026)** [S, from three trackers: alloevil, latere-ai and measured (95, no cost)]. This is consistent with the official `v2.json` captured today, whose highest served score is 95 [P-c summary]; the summary does not say which row holds it. ~~One tracker lists 94.6 as the "independent" value [S].~~ Not reproduced by fact-check: no source fetched in this check lists 94.6 for Astra on ARC-AGI-2. Treat it as unverified [corrected by fact-check].
- **Adoption evidence.**
  - ARC Prize 2025 ran 26 Mar–3 Nov 2025 [P-c]:
    - Prizes: $700K Grand Prize at ≥85% within Kaggle efficiency limits; $125K guaranteed progress prizes; $175K to be announced.
    - Kaggle compute was "~$50 worth of compute per submission", described as "2x compute vs. 2024 (L4x4s)".
    - Solutions had to be open-sourced before receiving private-set scores.
    - 1,455 teams submitted 15,154 entries, and 90 papers were submitted, up from 47.
    - The Top Score winners were NVARC (24.03%), the ARChitects (16.53%), MindsAI (12.64%), Lonnie (6.67%) and G. Barbadillo (6.53%).
    - The top paper award went to TRM (7M parameters; 45% on ARC-AGI-1 and 8% on ARC-AGI-2).
  - "Four frontier AI labs (Anthropic, Google DeepMind, OpenAI, and xAI) reported ARC-AGI performance in public model cards in 2025, establishing ARC-AGI as an industry standard benchmark" [P-c].
  - The 2026 Anthropic system cards (Opus 5, Fable 5.1) report ARC-Prize-*verified* ARC-AGI-1/2/3 scores [P-c].
- **Status.** **Saturated on the verified semi-private set (95% > 85% target) in about 18 months.** The 85% line itself was first reached by GPT-5.5 (xhigh), at 85% on 2026-04-23, about 13 months after launch [S, measured tracker; added by fact-check]. The Kaggle Grand Prize track (open-source, compute-capped) was unclaimed as of the latest report I could read (the 2025 report, Jan 2026). ARC committed to "continue operating the ARC-AGI-2 Grand Prize competition in 2026", and an "ARC-AGI-2 Competition" link is live on arcprize.org today [P-c]. I could not find a 2026 ARC-AGI-2 Kaggle result [U].
- **Why it succeeded:**
  - It kept the familiar format ("ensuring continuity for researchers") [P-c].
  - It fixed v1's measured flaws: larger and calibrated eval sets, removal of brute-forceable tasks, and IID splits [P-c].
  - It made cost a first-class axis on the leaderboard [P-c].
  - It worked with labs to verify scores [P-c].
  - [I] It became the de facto "reasoning" line item in model cards.
- **Why it failed or is failing:**
  1. **Knowledge overfitting** [P-c, 2025 report]. ARC wrote: "even well-designed benchmarks resistant to direct memorization can now be 'overfit' if the public training and private test sets are too similar (e.g., independent and identically distributed) … We assert that this phenomenon is now occurring with ARC-AGI-1 and ARC-AGI-2." The evidence was that Gemini 3 Deep Think used "correct ARC color mappings in its reasoning" although the harness "does not mention ARC-AGI tasks or color formats". *Fact-check nuance:* ARC adds "accidentally or intentionally, although we cannot determine which". The evidence is a single quoted reasoning excerpt, and ARC says it "cannot precisely quantify the magnitude of this effect". Treat it as an anecdotal, self-reported diagnosis rather than a measured contamination rate [added by fact-check]. [I] The IID calibration that makes splits comparable also makes the private set learnable from the public distribution. This is a structural tension.
  2. **The efficiency claim did not hold.** In 2025, ARC wrote that "Log-linear scaling is insufficient to beat ARC-AGI-2" [P-c]. Yet frontier models reached 95% at $1.12/task, below the $17/task human panel [S], within about 18 months. [I] Once cost falls below the human baseline, the efficiency axis no longer separates AI from humans on this format.
  3. **Two worlds.** The Kaggle open-source track (24% in 2025) and the verified frontier API track (54% by end 2025, 95% by Sep 2026) diverged widely [P-c/S]. [I] The prize measures something different from what labs report.
- **Key sources:**
  - repo readme and changelog: https://raw.githubusercontent.com/arcprize/ARC-AGI-2/main/readme.md and https://raw.githubusercontent.com/arcprize/ARC-AGI-2/main/changelog.md
  - launch cache: https://raw.githubusercontent.com/steel-dev/leaderboard/33aaee5bf46a492e0ff9a84eb7643f8d0def66d6/docs/research/arc-agi-2/paper.md
  - 2025 report text: https://raw.githubusercontent.com/UNIR-TUC/arc-agi/48d931918edd904b99ef546a98adc97e19ccf528/src/SuperCompressARC/Docs/2025/2601.10904v1_arc_prize_2025.md
  - abstract: https://raw.githubusercontent.com/ATOM00blue/machine-learning-library/5e1e934ba4d745962b9012aabb5b62c9bd663895/corpus/papers/2505.11831.md
  - today's capture: https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-2/packet-r1.md
  - tracker: https://raw.githubusercontent.com/alloevil/llm-benchmarks-tracker/8e239c46ead8a4b063cc7d6ada272b53ad99633c/data/results/arc-agi-2.json

### 3. ARC-AGI-3 (launched 25 Mar 2026): interactive, and explicitly **game-like**

- **What it measures.** "Agentic intelligence." Agents act in turn-based 2D grid environments (64×64 frames, 16 colours per a secondary digest) with "no instructions, no rules, and no stated goals" [P-c Opus 5 card; S].
  - ARC tests four components [P-t]: **exploration, modeling, goal-setting, planning and execution**.
  - The docs frame the targets as "Exploration; Percept → Plan → Action; Memory; Goal Acquisition; Alignment" [P].
  - ARC's definition behind the design is [P-t]: "AGI = a system that can acquire any skill humans can acquire, with human-level efficiency."
- **Release date and venue.**
  - Full launch 25 Mar 2026 [S, several independent secondary sources; ARC's Kaggle comp start date matches].
  - Paper: "ARC-AGI-3: A New Challenge for Frontier Agentic Intelligence", arXiv:2603.24621 [S; title from three independent listings]. The author list was not verified; one BibTeX lists "ARC Prize Foundation".
  - A preview ran from July 2025. The Agents SDK was first released 2025-07-18 [P], and environment lp85 was "included as an ARC-AGI-3 preview environment in July 2025" [P-c].
  - The open-source toolkit and engine were released 29 Jan 2026 [P].
- **Creators.** The ARC Prize Foundation.
- **Item count and format** [P-c]:
  - 135 environments ("games"), each with multiple levels.
  - 25 are public demo environments. The rest are split into semi-private (55) and fully private (55) sets [S tracker].
  - Actions are discrete (ACTION1–7; ACTION6 takes x,y coordinates). Only environment-affecting actions count; "tool calls, reasoning steps, retries" do not [P].
- **Human calibration** [P-c, "Measuring Human Performance on ARC-AGI-3", 14 Apr 2026]:
  - **458 participants** from the general public in a San Francisco testing centre. *Fact-check note:* one LLM-assisted secondary digest of the arXiv paper (2603.24621 v1; nick-lang/VNR) reports **486** participants. This is unresolved: it may be a digest error or a counting difference. Cite 458 to the blog post, not to the paper [added by fact-check].
  - 90-minute sessions, with "~$130 base plus $5 for each environment" solved. The Astra post says "$115 per 90-minute session" plus $5 per game, about $12.78 per attempted game [P-t]. These figures disagree slightly.
  - "First-run" conditions, with no mention of ARC or AI. Humans get "the same 'system prompt'" and affordances as AI.
  - Environments too hard for people were excluded or revised. "Every environment is beaten by at least two independent participants", from a panel of about 10 per environment.
  - The public-demo human dataset (342 replays across 25 environments; 145 solves) is open-sourced.
  - Solvability per environment varies: r11l was solved by 10 of 10 players, tr87 by 6 of 12.
- **Scoring: Relative Human Action Efficiency (RHAE)** [P, docs]:
  - Per level: `(human_baseline_actions / ai_actions)^2`, capped at 1.15. The current docs define the baseline as the **"upper median human"** per level; with an even number of finishers, the upper of the two middle entries is used [P, methodology.mdx; precision added by fact-check].
  - Levels are weighted by level index, so a game's maximum score is limited by the levels completed.
  - The total is the mean over games.
  - A per-level cutoff of 5× the human action count is reported in the paper digest [S].
  - **The scoring changed three weeks after launch** (14 Apr 2026) [P]: the baseline moved from the "2nd best human" to the "median human", and the per-level cap rose from 1.0× to 1.15×. The stated reasons were a "luck factor" in some levels and "first place doesn't always get 100%". The net effect was about +0.5 pp for humans and AI [P-c].
- **Frontier score at launch vs latest.**
  - *Launch, Mar 2026.* All frontier models scored **below 1%** [S].
    - "Frontier AI 0.51%" is cited to ARC's launch post by two independent secondary sources.
    - The per-model figures differ across sources because of the scoring revision: Gemini 3.1 Pro 0.37%, GPT-5.4 0.26%, Opus 4.6 0.25% in one source; 0.50/0.40/0.20% in another.
  - *May 2026* [S]: GPT-5.5 0.43% and Claude Opus 4.7 0.18%, on the standard harness.
  - *July 2026* [P-c, Claude Opus 5 system card §8.14.2]:
    - **Claude Opus 5 (high): 30.16%** ARC-Prize-verified, "roughly four times the best previously reported score".
    - GPT-5.6 Sol (max): 7.78%. Claude Opus 4.8 (high): 1.52%.
  - *OpenAI harness experiment, July 2026* [S]: OpenAI re-ran Sol with "retained reasoning and compaction", raising its *public-set* score from 13.3% to 38.3%.
  - *3 Sep 2026* [P-t, ARC Prize "OpenAI's GPT-6 Astra on ARC-AGI-3", Greg Kamradt], GPT-6 Astra on the semi-private set:

    | Effort | Standard harness | Provider Adapter harness |
    |---|---|---|
    | max | 62.7%, $26,098 | 98.6%, $17,332 |
    | xhigh | 59.3%, $37,317 | 98.4%, $18,147 |
    | high | 54.8%, $40,705 | **99.9%, $18,817** |
    | medium | 38.6%, $48,090 | 98.4%, $19,285 |
    | low | 17.5%, $38,166 | 98.0%, $21,298 |
    | none | 35.2%, $49,791 | 96.7%, $23,457 |

    - Astra (max, Provider Adapter) used fewer actions than the median human on **96.0% of levels**, and 51.7% fewer actions on average.
    - The official `v3.json` captured today has a maximum served score of 99.946 [P-c summary]. This matches the 99.9% figure.
- **Adoption evidence.**
  - ARC Prize 2026 is a Kaggle code competition, "ARC Prize 2026 – ARC-AGI-3". Internet is disabled; accelerators are T4×2 (default), P100 or an ARC-AGI-3-exclusive RTX 6000 [P, docs and starter repo].
  - Per a secondary wiki [S]:
    - Prizes total $850K, including a $700K bonus unlocked only by a 100% score.
    - Deadline 2 Nov 2026; winners announced 4 Dec 2026.
    - About 1,556 teams as of July 2026.
  - "Nearly one million scorecards have been submitted on public environments" [P-c].
  - Anthropic's Opus 5 system card reports ARC-AGI-3 as a headline result [P-c].
- **Status.** **Active but already saturating under provider harnesses, six months after launch.** Comparability is **contested** because of harness dependence. ARC now reports both harnesses and labels each result [P-c policy].
- **Why it succeeded (so far):**
  - It measures *learning efficiency* directly, comparing human and AI action counts "for the first time" [P-c].
  - It is the most thorough human study in the series [P-c].
  - It came with open replays and datasets [P-c].
  - It had verified results from the first day [P-c].
- **Why it failed or is failing:**
  1. **Harness sensitivity.** The same model scored 62.7% (Standard, max effort) or 99.9% (Provider Adapter, high effort), depending on whether the harness keeps opaque reasoning state between calls [P-t]. At the same max effort the figures are 62.7% vs 98.6%. ARC's own framing is that the "best observed score rose from 62.7% to 99.9%" [corrected by fact-check]. The harness distinction is independently documented in the official `arcprize/arc-agi-3-benchmarking` README [P, added by fact-check]. ARC's policy now says the two harnesses "answer different evaluation questions" [P-c].
  2. **Closed, deterministic worlds.** ARC itself says ARC-AGI-3's "scope and format are tightly bounded, environment mechanics and goals are deterministic and closed. It does not represent real-world complexity and openness" [P-t].
  3. **Scoring non-stationarity.** The human baseline changed three weeks after launch [P].
  4. **Game-likeness.** This makes it out of scope as a template for our project [I].
  5. **Game-specific tooling.** Astra "built its own tools for each game" (maze_solver.py, combat_solver.py) in the PRO-LONG harness [P-t]. [I] Tool access turns a test of learning efficiency into a programming task.
- **Key sources:**
  - docs: https://raw.githubusercontent.com/arcprize/docs/main/methodology.mdx and https://raw.githubusercontent.com/arcprize/docs/main/changelog.mdx
  - human dataset post capture: https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-3/packet-r1.md
  - Astra translation: https://raw.githubusercontent.com/lihenair/techtranslate/821908553b702d9de6565d186fdd2e8661303f6f/archive/2026-09-05/ai/OpenAIs-GPT-6-Astra-on-ARC-AGI-3.md
  - Opus 5 card mirror: https://raw.githubusercontent.com/malob/ai-system-cards/282a67c3c79617b23a1a23ed0869239b6e28d139/cards/anthropic/claude-opus-5/sections/08b-capabilities-2.md

### 4. Cross-version mechanisms (deep dive)

**4a. Data tiers: public vs semi-private vs private** [P-c, arcprize.org/policy captured 2026-09-29].

- **Public tasks** are fully open. **Semi-private** tasks are "used for frontier model testing on the Verified Leaderboard". Because they are sent to external APIs, ARC acknowledges "the possibility of limited leakage over time".
- The semi-private defences are:
  1. zero-data-retention agreements with providers;
  2. "release of successive ARC-AGI benchmark versions on a roughly annual basis, which shifts the frontier signal onto fresh tasks";
  3. monitoring the public-vs-semi-private gap.
- **Private tasks** have access "extremely restricted to a small number of trusted parties" and are used for the Kaggle competition.
- **Agreement rules.** Verified scores must show "good agreement" between public and semi-private results:
  - ARC-AGI-1: ±10 pp, with public easier;
  - ARC-AGI-2: ±3 pp, calibrated;
  - ARC-AGI-3: ±15 pp, with public *harder*.
- **Who gets tested.** Verification is limited to "public, high-usage, commercially available model APIs", and commercial APIs "must have >$10M USD gross revenue/mo … to ensure sufficient commercial generalization pressure against benchmark overfitting".
- **Budget.** Runs are capped at $10,000 each, with a single run and no averaging. Cost is computed at retail prices.
- **Publication timing.** Results are published "no later than 30 days after public release", and "Sponsors cannot impose additional embargoes."
- **Governance.**
  - The steward is a nonprofit with donors publicly disclosed and conflict-of-interest recusal.
  - An **independent academic panel** reviews the methodology: Todd Gureckis (NYU), **Melanie Mitchell** (Santa Fe Institute) and Vishal Misra (Columbia). The panel "does not review every individual test result." *Fact-check correction:* the earlier label "a prominent ARC critic" was interpretation, not sourced. Accurately, Mitchell's group has published critical analyses of AI abstraction on ARC-style tasks (ConceptARC 2023; Beger et al. 2025), and Gureckis co-authored H-ARC [corrected by fact-check].
  - *Added by fact-check:* the policy states that the Foundation "is a nonprofit funded by donations from individuals, foundations, and **AI labs**". It also says that sponsor status does not affect verification, scoring, publication timing or data access [P-c]. [I] This matters for the "lab partnership without capture" claim below. Independence rests on stated policy, not on the absence of lab funding.
- **Two leaderboards.** The **Community Leaderboard** shows methods, not scores. Self-reported scores are "untrustworthy by design", and "only ARC Prize Verified scores" are displayed [P, community leaderboard README]. A verification fund reimburses up to $2,500 per verified reproduction [P-c].

**4b. The cost and efficiency axis** [P-c]:

- The 2024 report predicted that "it is thus no longer possible to assign a score to an approach, but only to the combination of an approach plus a compute budget".
- It estimated that 85% could be reached by Greenblatt-style sampling at about 10^8 programs per task, a "multi-million dollar compute budget".
- **Dec 2024:** efficiency became mandatory.
- **Mar 2025:** "all ARC-AGI reporting will come along with an efficiency metric. We are starting with cost." The leaderboard became a score-versus-cost scatter that shows only systems under $10,000 per run.
- **2026:** ARC-AGI-3 adds *action* efficiency against humans.
- **Critiques of the cost axis:**
  - Cost is a pricing artefact: the o3-preview figures were re-priced twice [P-c].
  - A third-party analysis argues that point-in-time cost-per-task snapshots hide very fast frontier cost declines [S, ndbroadbent].

**4c. Kaggle compute limits (open-source prize track):**

| Year | Compute | Budget or constraint | Source |
|---|---|---|---|
| 2024 | 1× P100 | ≤12 h, no internet, about $10 of compute per entry | [P-c] |
| 2025 | L4×4 ("2× compute vs. 2024") | about $50 per submission | [P-c] |
| 2026 (ARC-AGI-3) | T4×2 default, P100, or RTX 6000 | internet disabled; runtime ≤9 h [S] | [P] |

- Verification of non-Kaggle submissions requires a one-click Kaggle notebook that runs in under 12 h and costs at most $10,000 at runtime [P-c].

**4d. Program search, test-time training and refinement loops** [P-c]:

- **2024 approach families:** DSL brute force, LLM-generated Python programs, LLM-guided DSL search, LLM debugging, test-time training (TTT) and induction+transduction ensembles.
  - "Deep learning-guided program synthesis does not currently decisively beat DSL-based brute-force program search – both score in the 40% range today with comparable compute budgets."
- **2025: the "refinement loop"** became the dominant technique: evolutionary program synthesis (Berman; Pang), zero-pretraining networks (TRM at 7M parameters; CompressARC at 76K parameters) and application-layer harnesses (Poetiq).
  - Frontier reasoning shows the same pattern: Gemini 3 Pro used 96 reasoning tokens on one task, while Gemini 3 Deep Think used 138,000.
- **HRM replication (ARC Prize, Aug 2025)** [P repo; S findings]:
  - ARC verified HRM at 32% on ARC-AGI-1 semi-private and 2% on ARC-AGI-2.
  - "The hierarchical architecture had minimal performance impact when compared to a similarly sized transformer."
  - The outer refinement loop drove performance.
  - A `puzzle_id` embedding makes the method transductive.
  - [I] This is ARC acting as an *auditor* of claimed breakthroughs, which builds trust.

### 5. Derivative and supporting instruments (for contrast)

- **ConceptARC** (Moskvichev, Odouard and Mitchell, 2023; arXiv:2305.07141) [P repo README; S]:
  - 16 concept groups × 10 tasks, in ARC format, designed to test systematic understanding of each concept.
  - Status: **niche but active in research**. Examples are the 2025 multimodal study by Beger, Mitchell et al., and ARC's own HRM analysis, which trained on ConceptARC data [P].
  - [I] It uses the same format with more rigorous concept control, but it has no prize, no steward, no leaderboard and no versioning, and it stayed a research instrument. This supports the view that *institutional* design, not the task format, drove ARC-AGI's adoption.
- **H-ARC** (LeGris, Vong, Lake and Gureckis, 2024; arXiv:2409.01374) [S/P-c]:
  - 1,729 humans attempted all 800 public ARC-AGI-1 tasks.
  - Average accuracy was 76.2% on training tasks and 64.2% on evaluation tasks.
  - 790 of the 800 tasks were solved by at least one person within 3 attempts.
  - *Fact-check additions (verbatim abstract):* the estimated ranges are 73.3–77.2% (training) and 55.9–68.9% (evaluation). Participants were crowd-workers recruited online, and H-ARC allowed **3 attempts**, whereas ARC Prize scores pass@2. The 64.2% is therefore not strictly comparable with pass@2 AI scores, even though ARC's own ARC-AGI-2 launch table uses 64.2% as the ARC-AGI-1 "Human panel (average)" [P-c].
  - [I] This shows that ARC's "easy for humans" is a **panel-level** property (someone solves it), not an individual-level one. ARC-AGI-2 kept this panel definition: at least 2 solvers. Our method should state explicitly which kind of human baseline it uses.

### 6. Critiques (consolidated)

| Critique | Evidence | Tag |
|---|---|---|
| Accuracy overstates abstraction (shortcuts) | Beger, Mitchell et al. (arXiv:2510.02125): "the best models' rules are often based on surface-level 'shortcuts' and capture intended abstractions far less often than humans … using accuracy alone … may overestimate abstract-reasoning capabilities in textual modalities and underestimate it in visual modalities" | [P-c abstract] |
| Perception and format confound | VARC (arXiv:2511.14761): treating ARC as image-to-image translation, a ViT trained from scratch reaches 60.4% on ARC-1, "competitive with those of leading LLMs". Text serialisation of grids is a design choice that shapes results [I]. *Fact-check caveats:* the abstract does not name the ARC-1 split. The official repo shows both single-model and ensemble variants, and whether 60.4% is the ensemble figure was not verified. Do not compare it directly with verified semi-private scores [added by fact-check]. | [P-c abstract] |
| Brute force / compute purchasability | 49% of ARC-AGI-1 solvable by 2020 brute-force search; o3 used 172× compute for +11.8 pp | [P-c] |
| Private-set probing | About 10,000 scores reported against 100 private tasks | [P-c] |
| Contamination without memorisation ("knowledge overfitting") | Gemini 3 Deep Think used ARC colour mappings unprompted; ARC "cannot precisely quantify the magnitude of this effect" | [P-c] |
| Training on the public set ("tuned") | o3-preview was trained on 75% of the public training set | [P-c] |
| Does it measure intelligence? | Chollet's own list: "Test validity is not established"; "Generalization is not quantified". ARC Prize: "not an acid test for AGI". Mitchell's Dec 2024 essay "Did OpenAI Just Solve Abstract Reasoning?" exists; I saw it only as a citation, and its content is **not verified here**. | [P-c]; essay [S citation only] |
| Human baseline definitions | Panel (≥2 solvers) vs individual average (60–66% on ARC-AGI-2; 64.2% on ARC-AGI-1 eval). ARC-AGI-3 baseline changed from 2nd-best to median. | [P/P-c] |
| Harness and scaffold dependence | 62.7% (Standard, max effort) vs 99.9% (Provider Adapter, high effort) for the same model on ARC-AGI-3; 62.7% vs 98.6% at the same max effort [corrected by fact-check] | [P-t] |
| Rapid saturation despite "hard for AI" design | ARC-AGI-2 went from single digits to 95% in about 18 months; ARC-AGI-3 went from under 1% to 99.9% (provider harness) in about 6 months | [S/P-t] |
| Narrowness | Grid puzzles; ARC-AGI-3 is closed and deterministic and "does not represent real-world complexity" | [P-c/P-t] |

---

## Cross-cutting success factors

These are drawn from the ARC case. Each carries a pointer to its evidence; the synthesis is mine [I].

1. **An explicit theory of the construct, written before the tasks.** Skill-acquisition efficiency, controlling for priors and experience [P-c]. This gave ARC three things:
   - a narrative ("scale alone doesn't do it");
   - a principled answer to "what counts as cheating" (training on the test; buying skill with priors or compute);
   - the ability to *evolve* the benchmark while keeping its identity.
2. **"Easy for humans, hard for AI" as the selection rule, with measured human calibration.** Every eval item has at least 2 independent human solvers (v2, v3). There are large lay-public studies: over 400 people for v2 and 458 for v3. Human cost is reported per task [P-c]. This makes the "gap" interpretable and gives a natural stopping criterion: AGI is here when no such tasks can be found.
3. **Each item tests a novel rule** ("every task … follows a different logic"), and the training set teaches only priors [P-c]. This resists the item-level memorisation that killed knowledge benchmarks.
4. **Tiered data with an explicit threat model.** Public train, public eval, semi-private (API-exposed, zero data retention) and private (competition only). Agreement thresholds between tiers act as an overfitting alarm [P-c].
5. **Cheap, exact, automatic scoring.** Exact grid match with pass@2 and no LLM judge [P-c]. Results are reproducible and free of grader drift.
6. **An efficiency axis on the leaderboard.** Cost per task alongside accuracy since Dec 2024/Mar 2025, a $10k cap, retail pricing, and a human cost reference [P-c]. This framing was adopted by labs and the press.
7. **A neutral, accountable steward.** A nonprofit with a public testing policy, publication-timing rules, conflict-of-interest recusal, an independent academic panel (including a critic), a split between the verified and community leaderboards, published model outputs and replays, and independent replication of hyped results (HRM) [P-c; P].
8. **Incentives that create a research community.**
   - Prize money tied to open-sourcing: MindsAI's top 2024 score was ineligible because it was not open-sourced.
   - Paper awards; submissions rose from 47 to 90 papers.
   - A Kaggle track with compute caps, so individuals can compete.
   - Community SDKs and replays.

   [P-c] This attracted startups (at least 7 with more than $1M in funding) and all major labs.
9. **Planned obsolescence: roughly annual versioning.** ARC-AGI-1 (2019) → ARC-AGI-2 (2025) → ARC-AGI-3 (2026). The format was preserved where possible (v2 kept v1's format), and design choices were driven by a failure analysis of the previous version [P-c]. ARC calls this "a real world refinement loop … iteratively improving benchmarks in response to AI progress" [P-c].
10. **Lab partnership without capture.** ARC co-presented o3's result, verifies lab models before release, and is cited in model cards [P-c]. At the same time it refuses sponsor embargoes and privileged data access [P-c]. *Fact-check caveat:* the Foundation's donors include AI labs (policy page) [P-c], so "without capture" rests on written policy and recusal rules, not on financial independence.
11. **Shareable, human-playable artefacts.** Every task can be played in a browser (arcprize.org/play; the ARC-AGI-3 environments). Failure examples such as "o3 fails this easy task" go viral [P-c; I].

### Transplantability to a NON-GAME benchmark (the question the project asked)

| ARC design principle | Transplantable? | Notes for our method [I] |
|---|---|---|
| Written construct theory (efficiency of acquiring new skill given priors and experience) | **Yes, core** | Define the construct first. "Learning efficiency on novel, non-game problems" fits well: for example, few-shot adaptation to a new formal system, invented API, notation or procedure. |
| Human-calibrated items (≥2 lay solvers; report the individual average too) | **Yes** | Report both the panel criterion and individual averages (H-ARC lesson). Pay and record human cost per item. |
| Novel rule per item, with training that exposes only priors | **Yes** | Generate items whose governing rule is new at test time, but avoid IID public/private splits. The 2025 "knowledge overfitting" shows that IID calibration lets models learn the distribution. |
| Tiered data (public / semi-private / private), with an agreement-gap alarm | **Yes** | Adopt it with zero-data-retention terms, and track the public-vs-held-out gap. Rotate held-out items on a schedule. |
| Exact, automatic scoring (no LLM judge) | **Yes** | Use executable or verifiable answers wherever possible. |
| Efficiency axis (cost per task, with pinned price tables) | **Yes, with a fix** | Freeze the price schedule and date. Also report token or compute counts, because dollars get re-priced (o3: $200 → $26 per task). |
| Interaction or learning efficiency against humans (RHAE-style) | **Partially** | The *idea* transfers (measure how many queries or examples are needed to learn, relative to humans). The *game* implementation does not. Use non-game interactive probes, such as asking questions of a simulated system or an oracle under a query budget. |
| Harness declaration (standard vs provider) | **Yes, mandatory** | Report results per declared harness, as ARC now does. |
| Neutral steward, testing policy, academic panel, verified vs community boards | **Yes** | This is institutional rather than technical. It is essential for adoption and cheap to write down. |
| Prize tied to open-sourcing | **Optional** | It needs funding. A lighter version is paper awards or a verified-reproduction fund. |
| Roughly annual versioning with public failure analysis | **Yes** | Build in versioning and a "known flaws" section from day one. |
| Grid/visual format; Core Knowledge priors | **No** (format-specific) | Our items can be textual or symbolic; keep the "minimal, stated priors" principle. |
| Interactive game environments (ARC-AGI-3) | **No** (out of scope by design) | Keep the construct (exploration, hypothesis revision, efficient action) and drop the game wrapper. |

---

## Cross-cutting failure factors

1. **Small, long-lived private sets leak through feedback.** About 10,000 score reports against 100 tasks [P-c]. *Mitigation ARC adopted:* 120-task calibrated sets, a separate semi-private set for intermediate scoring, and annual turnover [P-c].
2. **Items solvable by brute force carry no signal.** 49% of ARC-AGI-1 [P-c]. *Mitigation:* remove tasks solved by naive search before release (the v2 changelog) [P-c].
3. **Scores can be bought with compute.** o3 used 172× compute for +11.8 pp [P-c]. *Mitigation:* mandatory cost reporting and a $10k cap [P-c]. The fix is imperfect because prices change [P-c; I].
4. **Contamination without memorisation.** IID public and private sets plus heavy public training give "knowledge overfitting" [P-c]. [I] A benchmark whose held-out set is drawn from the same generator as its public set will eventually be learned as a *domain*.
5. **Scaffold and harness dependence breaks comparability.** A 36-point swing for the same model at the same max effort (62.7% vs 98.6%), or 37 points best-vs-best across effort settings [P-t] [corrected by fact-check].
6. **Metric instability.** The ARC-AGI-3 baseline was redefined three weeks after launch [P]. Cost figures were re-priced [P-c]. Documentation drifted (2 vs 3 trials; 400 vs 1,000 training tasks) [P; P-c].
7. **Validity gaps admitted by the creator.** "Test validity is not established" (2019) [P-c]. External work finds shortcut solutions and modality effects [P-c]. [I] High accuracy on an ARC-style task does not by itself show the intended abstraction.
8. **Fast saturation once the benchmark becomes a lab target.** v2: about 18 months to 95%. v3: about 6 months to 99.9% under the provider harness [S/P-t]. The more successful and adopted the benchmark, the faster it saturates [I]. Plan for succession.
9. **Divergence between the prize track and the frontier track.** 2025 Kaggle: 24%; verified API frontier: 54% [P-c]. [I] Prize constraints (open-source, $50 of compute) measure a different quantity from lab-reported scores. This is confusing for readers of either number.
10. **Narrow, closed task worlds.** ARC concedes that ARC-AGI-3 "does not represent real-world complexity and openness" [P-t]. This echoes the user's "not applicable to real work" criticism of game benchmarks. ARC survived that criticism through philosophy and stewardship, not through real-world relevance [I].

---

## Claims ledger

Confidence is High, Medium or Low. Unless stated otherwise, all URLs were accessed on 2026-09-29.

1. **Chollet's 2019 paper defines intelligence as skill-acquisition efficiency** "highlighting the concepts of scope, generalization difficulty, priors, and experience". It argues that unlimited priors or training data let experimenters "buy" skill (arXiv:1911.01547).
   - Sources: https://raw.githubusercontent.com/Interconnects-AI/homebase/b2c74a0cb0765f2c65abe8cbc8ba48d5ff877d7a/public/2024/2024-12-20-openaiso3thegrandfinaleofaiin2024.md ; https://raw.githubusercontent.com/commotum/4D/6dd4d04fd21a681d337e4342beb6ef51e0476a07/Notes/Vision/pdfs-3/2019_MOI.md ; https://github.com/y-arjun-y/arjunyadav/blob/66bf0ee0a0036f6cd9d1d42b11c46649afb87691/pages-md/ai-safety.md
   - Confidence: **High.**
2. **The original ARC had 400 training and 600 evaluation tasks with 10 colours and grids of 1×1 to 30×30.** Chollet listed its weaknesses, including "Test validity is not established" and "Generalization is not quantified".
   - Source: https://raw.githubusercontent.com/commotum/4D/6dd4d04fd21a681d337e4342beb6ef51e0476a07/Notes/Vision/pdfs-3/2019_MOI.md (verbatim paper quotes in a notes repo)
   - Confidence: **Medium-High.**
3. **ARC-AGI-1 is split into 400 public training, 400 public eval, 100 semi-private and 100 private tasks.** Scoring uses 2 attempts per test input. The private set was the final leaderboard in 2020, 2022, 2023 and 2024.
   - Sources: 2024 report text https://raw.githubusercontent.com/UNIR-TUC/arc-agi/48d931918edd904b99ef546a98adc97e19ccf528/src/SuperCompressARC/Docs/2024/2412.04604v2_arc_prize_2024.md ; arc-agi/1 capture https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-1/packet-r1.md
   - Confidence: **High.**
4. **In the 2020 Kaggle contest no deep-learning entry exceeded 1%, and GPT-3 scored 0%.** The top entry scored 20% (icecuber, brute-force search). An ensemble of all 2020 entries solved 49% of the private set. The best score was 33% by early 2024.
   - Source: 2024 report text (URL in claim 3).
   - Confidence: **High.**
5. **ARC Prize 2024 ran 11 Jun–10 Nov 2024.** Prizes were a $600K Grand Prize at 85%, $50K progress and $75K paper. 1,430 teams submitted 17,789 entries. MindsAI scored 55.5% (not open-sourced, so ineligible), and the ARChitects won with 53.5%. Kaggle ran on a P100 for ≤12 h with no internet (about $10 of compute), while ARC-AGI-Pub allowed $10,000 of API spend.
   - Source: 2024 report text (URL in claim 3); also https://raw.githubusercontent.com/ndbroadbent/arc_agi_pareto_frontiers/90d0c6822f82b8ef95423f2a37c74cdb45e7b40f/sources/arc_technical_report.html (seen in search)
   - Confidence: **High.**
6. **About 10,000 private-set scores had been reported to participants by 2024, creating a leakage risk.** Anecdotally, ARC-AGI-1's evaluation splits differed in human difficulty.
   - Source: 2024 report text (URL in claim 3).
   - Confidence: **High.**
7. **o3-preview (tested by ARC, 20 Dec 2024) scored 75.7% on the 100-task semi-private set** with 6 samples within the $10k public-leaderboard limit, and 87.5% with 1,024 samples (about 172× compute). The public eval scores were 82.8% and 91.5%. The model "trained … on 75% of the Public Training set". The low-efficiency semi-private run used 5.7B tokens.
   - Source: https://raw.githubusercontent.com/ndbroadbent/arc_agi_pareto_frontiers/90d0c6822f82b8ef95423f2a37c74cdb45e7b40f/sources/o3_announcement.html (cached arcprize.org/blog/oai-o3-pub-breakthrough); corroborated by https://raw.githubusercontent.com/Interconnects-AI/homebase/b2c74a0cb0765f2c65abe8cbc8ba48d5ff877d7a/public/2024/2024-12-20-openaiso3thegrandfinaleofaiin2024.md
   - Confidence: **High.**
8. **o3-preview cost figures were re-based twice** (3/24/2025 and 12/10/2025), to $26/task for the 75.7% run in the current page. The ARC-AGI-2 launch post and the Dec 2025 leaderboard data listed the same configuration at $200/task.
   - Sources: o3 cache (URL in claim 7); https://raw.githubusercontent.com/steel-dev/leaderboard/33aaee5bf46a492e0ff9a84eb7643f8d0def66d6/docs/research/arc-agi-2/paper.md ; https://raw.githubusercontent.com/ndbroadbent/arc_agi_pareto_frontiers/90d0c6822f82b8ef95423f2a37c74cdb45e7b40f/data/evaluations.json
   - Confidence: **High.**
9. **After o3, ARC made efficiency mandatory.** It wrote "Due to variable inference budget, efficiency (e.g., compute cost) is now a required metric", and later "all ARC-AGI reporting will come along with an efficiency metric. We are starting with cost".
   - Sources: o3 cache; ARC-AGI-2 launch cache (URLs in claims 7 and 8).
   - Confidence: **High.**
10. **ARC-AGI-2 was released on 24 Mar 2025** with 1,000 training, 120 public eval, 120 semi-private and 120 private tasks. Brute-forceable tasks were removed. Over 400 humans were tested, and every task was solved by at least 2 humans in ≤2 attempts. At launch, pure LLMs scored 0% and reasoning systems scored in single digits (o3-low about 4%, estimated).
    - Sources: https://raw.githubusercontent.com/arcprize/ARC-AGI-2/main/readme.md ; https://raw.githubusercontent.com/arcprize/ARC-AGI-2/main/changelog.md ; launch cache (URL in claim 8)
    - Confidence: **High.**
11. **The average individual human scores far below the ARC-AGI-2 human panel.** The launch table gives a human panel average of 60%, and the README says "Average human performance … 66%". The reported human cost is $17/task.
    - Sources: launch cache (URL in claim 8); https://raw.githubusercontent.com/arcprize/ARC-AGI-2/main/readme.md
    - Confidence: **High.**
12. **H-ARC tested 1,729 humans on all 800 public ARC-AGI-1 tasks.** They averaged 76.2% on training and 64.2% on evaluation tasks, and 790 of 800 tasks were solved by at least one person within 3 attempts.
    - Sources: https://github.com/geometor/arcprize/blob/10e87b6e4b2f8df6019f0cdd3fd90a53b19f0961/docsrc/refs/papers/h-arc-a-robust-estimate-of-human-performance-on-the-abstraction-and-reasoning-corpus-benchmark/summary.rst ; https://github.com/connorsmith256/nn-knowhow/blob/839d6a884548c540911710d68279c143211c3d69/research-log.md ; https://github.com/mysh212/CHSH-nhspc114-PRI/blob/6fbcb34604ddd032a324d3f263f2bccbd2bf7a77/Problems/H-ARC.md (abstract translation)
    - Confidence: **Medium-High.**
13. **ARC Prize 2025 ran 26 Mar–3 Nov 2025.** 1,455 teams submitted 15,154 entries, and the top private-set score was 24% (NVARC 24.03%) at $0.20/task. Paper submissions rose from 47 to 90. The top paper award went to TRM (7M parameters; 45% on ARC-AGI-1, 8% on ARC-AGI-2).
    - Sources: https://raw.githubusercontent.com/UNIR-TUC/arc-agi/48d931918edd904b99ef546a98adc97e19ccf528/src/SuperCompressARC/Docs/2025/2601.10904v1_arc_prize_2025.md ; https://raw.githubusercontent.com/ATOM00blue/machine-learning-library/5e1e934ba4d745962b9012aabb5b62c9bd663895/corpus/papers/2601.10904.md
    - Confidence: **High.**
14. **Four frontier labs (Anthropic, Google DeepMind, OpenAI, xAI) reported ARC-AGI in public model cards in 2025.** ARC describes this as "establishing ARC-AGI as an industry standard benchmark for AI reasoning".
    - Source: 2025 report abstract and text (URLs in claim 13).
    - Confidence: **High** (this is ARC's own statement).
15. **ARC asserts "knowledge overfitting" on ARC-AGI-1/2.** Because the public and private sets are IID, models trained on public data can overfit. The evidence is that Gemini 3 Deep Think used correct ARC colour mappings without being prompted.
    - Source: 2025 report text (URL in claim 13).
    - Confidence: **High.**
16. **The Poetiq refinement harness on Gemini 3 Pro raised ARC-AGI-2 from 31% ($0.81/task) to 54% ($31/task),** as verified by ARC.
    - Sources: 2025 report text (URL in claim 13); https://raw.githubusercontent.com/ndbroadbent/arc_agi_pareto_frontiers/90d0c6822f82b8ef95423f2a37c74cdb45e7b40f/data/evaluations.json
    - Confidence: **High.**
17. **ARC-AGI-2 frontier verified scores in 2026:** Claude Opus 5 (max) 90.42%; GPT-5.6 Sol 92.5% (listed in the Opus 5 card's Table 8.1.A as a competitor figure without an effort label; the "(max)", $1.44/task and verified status come from the alloevil tracker [S]) [corrected by fact-check]; Claude Fable 5.1 90%; Claude Opus 4.7 75.83%.
    - Source: https://raw.githubusercontent.com/malob/ai-system-cards/282a67c3c79617b23a1a23ed0869239b6e28d139/cards/anthropic/claude-opus-5/sections/08b-capabilities-2.md ; https://github.com/malob/ai-system-cards/blob/282a67c3c79617b23a1a23ed0869239b6e28d139/cards/anthropic/claude-fable-5-1/sections/08-capabilities.md
    - Confidence: **High** (lab system card quoting ARC-verified numbers, read via a mirror).
18. **GPT-6 Astra (max) scored 95.0% on ARC-AGI-2 semi-private at $1.12/task (Sep 2026).** This is the highest verified score, above the 85% Grand Prize threshold.
    - Sources: https://raw.githubusercontent.com/alloevil/llm-benchmarks-tracker/8e239c46ead8a4b063cc7d6ada272b53ad99633c/data/results/arc-agi-2.json ; https://github.com/latere-ai/ai-as-an-infrastructure/blob/bf1a025f002170a3a6b28a1168ca64dea4ab5442/en/field/2026-09.qmd ; official v2.json maximum of 95 in the capture at https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-2/packet-r1.md
    - Confidence: **Medium-High** (three secondary trackers, plus an official data-scale summary whose maximum is 95). The earlier "one tracker lists 94.6" was not reproduced by fact-check [corrected by fact-check].
19. **ARC-AGI-3 is interactive and game-like:** 135 environments, 25 public. Its human study tested 458 participants in 90-minute first-run sessions, and every environment was beaten by at least 2 participants.
    - Source: capture of arcprize.org/blog/arc-agi-3-human-dataset (14 Apr 2026) at https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-3/packet-r1.md ; docs https://raw.githubusercontent.com/arcprize/docs/main/games.mdx
    - Confidence: **High.**
20. **ARC-AGI-3 scoring (RHAE)** is `(human/AI actions)^2` per level, capped at 1.15, weighted by level index and averaged over games. On 14 Apr 2026 the baseline changed from 2nd-best to median human, and the cap from 1.0 to 1.15.
    - Sources: https://raw.githubusercontent.com/arcprize/docs/main/methodology.mdx ; https://raw.githubusercontent.com/arcprize/docs/main/changelog.mdx
    - Confidence: **High.**
21. **At the ARC-AGI-3 launch (25 Mar 2026), frontier AI scored below 1%.** A 0.51% best figure is cited to ARC's launch post.
    - Sources: https://github.com/latere-ai/ai-as-an-infrastructure/blob/bf1a025f002170a3a6b28a1168ca64dea4ab5442/en/field/2026-09.qmd ; https://raw.githubusercontent.com/memgrafter/research-digests/491d1e597ee1384396057fbe72e2bdec9f11c2c6/ml_research_analysis_2026/2603.24621_arc-agi-3-a-new-challenge-for-frontier-agentic-intelligence_20260331_185732.md ; https://raw.githubusercontent.com/kristiRule/claude-learning/50b19e9c6a6b071c5af981ce71ca272d20cfad1a/demos/research-pipeline/ai-agi-overview/knowledge/arc_agi_chollet.md
    - Confidence: **Medium** for "<1%" (secondary but consistent), **Low-Medium** for the exact 0.51%.
22. **Claude Opus 5 (high) scored 30.16% on ARC-AGI-3 semi-private (ARC-verified), in July 2026.** GPT-5.6 Sol (max) scored 7.78% and Claude Opus 4.8 1.52%.
    - Source: Opus 5 card mirror (URL in claim 17).
    - Confidence: **High.**
23. **GPT-6 Astra on ARC-AGI-3 semi-private (3 Sep 2026):** Standard harness (max) 62.7% at $26,098; Provider Adapter harness (high) 99.9% at $18,817, and (max) 98.6% at $17,332. Headline comparisons must state that 62.7% → 99.9% changes both harness and effort [fact-check note]. Astra (max, Provider Adapter) used fewer actions than the median human on 96.0% of levels.
    - Sources: https://raw.githubusercontent.com/lihenair/techtranslate/821908553b702d9de6565d186fdd2e8661303f6f/archive/2026-09-05/ai/OpenAIs-GPT-6-Astra-on-ARC-AGI-3.md (translation of arcprize.org/blog/astra) ; https://raw.githubusercontent.com/Belkins/ai-dive-deep/ecac08d8d3ffe24d6301579938d9d4e64bd101ff/src/content/chapters/49-gpt-6-astra.mdx ; official v3.json maximum 99.946 in the ARC-AGI-3 capture (URL in claim 19)
    - Confidence: **High.**
24. **ARC states that ARC-AGI-3 is "tightly bounded … deterministic and closed"** and does not represent real-world complexity. It does not claim that Astra is AGI.
    - Source: Astra translation (URL in claim 23).
    - Confidence: **Medium-High** (read in translation).
25. **ARC's testing policy (captured 2026-09-29):**
    - semi-private sets carry acknowledged leakage risk, mitigated by zero data retention and roughly annual new versions;
    - public/semi-private agreement bands are ±10, ±3 and ±15 pp for v1, v2 and v3;
    - commercial APIs are tested only if gross revenue exceeds $10M/month;
    - runs are capped at $10,000 with a single run;
    - results are published ≤30 days after release, with no sponsor embargoes;
    - an academic panel of Gureckis, Mitchell and Misra reviews the policy.
    - Source: capture at https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-2/packet-r1.md
    - Confidence: **High.**
26. **ARC's Community Leaderboard treats self-reported scores as "untrustworthy by design"** and displays only ARC Prize Verified scores.
    - Source: https://raw.githubusercontent.com/arcprize/ARC-AGI-Community-Leaderboard/main/README.md
    - Confidence: **High.**
27. **ARC Prize's HRM analysis verified 32% (ARC-AGI-1 semi-private) and 2% (ARC-AGI-2).** It found that the hierarchical architecture added little over a matched transformer, and that the outer refinement loop drove performance.
    - Sources: https://raw.githubusercontent.com/arcprize/hierarchical-reasoning-model-analysis/main/README.md (existence and method) ; https://github.com/UOR-Foundation/uor-r4/blob/7cc595495cda7ed9965228bd07fab63f1a67c2b2/docs/integration/review-2026-09-16/05-literature-brief.md (findings) ; HRM rows in https://raw.githubusercontent.com/ndbroadbent/arc_agi_pareto_frontiers/90d0c6822f82b8ef95423f2a37c74cdb45e7b40f/data/evaluations.json
    - Confidence: **Medium-High.**
28. **Beger, Mitchell et al. (arXiv:2510.02125)** find that accuracy on ConceptARC overestimates abstraction in textual modalities, because models use surface shortcuts, and underestimates it in visual modalities.
    - Source: https://github.com/Luvata/arxive/blob/1620fc6bcd136848375a9c12a057db05dfb0d287/pages/2025-10-06-cs-cl.html (verbatim abstract)
    - Confidence: **High.**
29. **VARC (arXiv:2511.14761)** is a ViT trained from scratch that treats ARC as image-to-image translation with test-time training. It reaches 60.4% on ARC-1.
    - Source: https://raw.githubusercontent.com/Yasouimo/NetPlagStream/2ef20657d2270987392a0421ce743c2a8ac675bb/data/corpus_initial/2511.14761v1.txt
    - Confidence: **High.**
30. **ARC Prize 2025 Kaggle rules:** about $50 of compute per submission (L4×4, "2× compute vs. 2024"), no internet APIs, and open-sourcing required before private scores are released. Prizes were a $700K Grand Prize at 85%, $125K guaranteed and $175K to be announced.
    - Source: launch cache (URL in claim 8).
    - Confidence: **High.**
31. **The ARC Prize 2026 ARC-AGI-3 Kaggle competition** runs with internet disabled on T4×2, P100 or RTX 6000 accelerators.
    - Sources: https://raw.githubusercontent.com/arcprize/docs/main/arc-prize-2026.mdx ; https://raw.githubusercontent.com/arcprize/ARC-AGI-3-Kaggle-Starter/main/README.md
    - Confidence: **High.**
    - The $850K total, the $700K bonus at 100%, the 2 Nov 2026 deadline and about 1,556 teams come from https://raw.githubusercontent.com/tiendungchs/PersonalWiki/3d53ba4956d8299648d7348ba566dba324eff201/wiki/entities/arc-agi.md. Confidence: **Low-Medium** (secondary only).
32. **ARC-AGI-1 frontier in mid/late 2026 is about 97.5–98.5%,** against a human panel at 98%: Claude Opus 5 and GPT-5.6 Sol 97.5% (system card); GPT-6 Astra 98.5% (Epoch-derived tracker).
    - Sources: Opus 5 card mirror (URL in claim 17) ; https://raw.githubusercontent.com/rishikeshn-eng/measured/2e30d67d10d6db8b508c8fad39ce136b370a78f4/index.html ; human panel in the evaluations.json snapshot (URL in claim 27)
    - Confidence: **High** for 97.5%; **Medium** for 98.5%.

---

## References

A machine-readable list is in `research/refs/arc_agi.json`. For each entry below, "Seen at" is where I actually read it.

1. Chollet, F. (2019). *On the Measure of Intelligence.* arXiv:1911.01547.
   - Seen at: commotum/4D notes (verbatim quotes); Interconnects cache; y-arjun-y page (abstract).
2. Chollet, F. (2019). *The Abstraction and Reasoning Corpus (ARC-AGI-1)*, GitHub `fchollet/ARC-AGI`.
   - Seen at: raw README; GitHub repo metadata.
3. ARC Prize Foundation (2025). *ARC-AGI-2 repository* (readme and changelog), GitHub `arcprize/ARC-AGI-2`.
4. Chollet, F., Knoop, M., Kamradt, G., Landers, B. (2024/2025). *ARC Prize 2024: Technical Report.* arXiv:2412.04604 (v2 dated 9 Jan 2025).
   - Seen at: UNIR-TUC/arc-agi full-text extraction.
5. Chollet, F., Knoop, M., Kamradt, G., Landers, B., Pinkard, H. (2025). *ARC-AGI-2: A New Challenge for Frontier AI Reasoning Systems.* arXiv:2505.11831.
   - Seen at: ATOM00blue abstract; LHTB BibTeX.
6. Chollet, F., Knoop, M., Kamradt, G., Landers, B. (2026). *ARC Prize 2025: Technical Report.* arXiv:2601.10904.
   - Seen at: UNIR-TUC full text; ATOM00blue abstract.
7. ARC Prize Foundation (2026). *ARC-AGI-3: A New Challenge for Frontier Agentic Intelligence.* arXiv:2603.24621. Author list not verified.
   - Seen at: memgrafter digest; Eurekaleo BibTeX; alloevil tracker.
8. Chollet, F. (20 Dec 2024). *OpenAI o3 Breakthrough High Score on ARC-AGI-Pub.* ARC Prize blog.
   - Seen at: cached HTML in ndbroadbent/arc_agi_pareto_frontiers.
9. Kamradt, G. (24 Mar 2025). *ARC-AGI-2 + ARC Prize 2025 is Live!* ARC Prize blog.
   - Seen at: cached text in steel-dev/leaderboard.
10. Kamradt, G. (14 Apr 2026). *Measuring Human Performance on ARC-AGI-3.* ARC Prize blog.
    - Seen at: capture in fstandhartinger/model-market-comparison.
11. Kamradt, G. (3 Sep 2026). *OpenAI's GPT-6 Astra on ARC-AGI-3.* ARC Prize blog.
    - Seen at: Chinese translation in lihenair/techtranslate.
12. ARC Prize Foundation (2026). *ARC Prize Verified Testing Policy*, arcprize.org/policy.
    - Seen at: capture of 2026-09-29.
13. ARC Prize Foundation (2026). *ARC-AGI-1 / ARC-AGI-2 pages and Leaderboard*, arcprize.org.
    - Seen at: capture of 2026-09-29.
14. ARC Prize Foundation (2026). *ARC-AGI-3 documentation* (methodology, changelog, games, ARC Prize 2026), GitHub `arcprize/docs`.
15. ARC Prize Foundation. *arc-agi-benchmarking*, *ARC-AGI-3-Agents*, *ARC-AGI-3-Kaggle-Starter*, *ARC-AGI-Community-Leaderboard* and *hierarchical-reasoning-model-analysis* READMEs (GitHub).
16. LeGris, S., Vong, W. K., Lake, B. M., Gureckis, T. M. (2024). *H-ARC: A Robust Estimate of Human Performance on the Abstraction and Reasoning Corpus Benchmark.* arXiv:2409.01374.
17. Moskvichev, A., Odouard, V. V., Mitchell, M. (2023). *The ConceptARC Benchmark: Evaluating Understanding and Generalization in the ARC Domain.* arXiv:2305.07141.
    - Seen at: victorvikram/ConceptARC README.
18. Beger, C., Yi, R., Fu, S., Moskvichev, A., Tsai, S. W., Rajamanickam, S., Mitchell, M. (2025). *Do AI Models Perform Human-like Abstract Reasoning Across Modalities?* arXiv:2510.02125. A later version adds Kaleda Denton.
19. Hu, K., Cy, A., Qiu, L., Ding, X. D., Wang, R., Zhu, Y. E., Andreas, J., He, K. (2025). *ARC Is a Vision Problem!* arXiv:2511.14761.
20. Jolicoeur-Martineau, A. (2025). *Less is More: Recursive Reasoning with Tiny Networks.* arXiv:2510.04871.
    - Seen at: 2025 report reference list.
21. Wang, G. et al. (2025). *Hierarchical Reasoning Model.* arXiv:2506.21734.
    - Seen at: 2025 report reference list; arcprize HRM-analysis README.
22. Li, W.-D. et al. (2024). *Combining Induction and Transduction for Abstract Reasoning.* arXiv:2411.02272.
    - Seen at: 2024 report reference list.
23. Akyürek, E., Damani, M., Qiu, L., Guo, H., Kim, Y., Andreas, J. (2024). *The Surprising Effectiveness of Test-Time Training for Abstract Reasoning.* arXiv:2411.07279. [author list completed by fact-check]
    - Seen at: open-thought/arc-agi-2 research list; the full author list is from ARC Prize 2024 report ref 1.
24. Spelke, E. S., Kinzler, K. D. (2007). *Core knowledge.* Developmental Science, pp. 89–96.
    - Seen at: 2024 report reference list.
25. Anthropic (2026). *Claude Opus 5 System Card*, §8.14 ARC-AGI.
    - Seen at: malob/ai-system-cards mirror. Canonical PDF (link seen in the Fable 5.1 card): https://www-cdn.anthropic.com/b514064af1408018e64b1ad24e7d5e75850b4ffd/Claude%20Opus%205%20System%20Card.pdf [added by fact-check].
26. Anthropic (2026). *Claude Fable 5.1 System Card*, ARC-AGI section.
    - Seen at: malob/ai-system-cards mirror.
27. Lambert, N. (20 Dec 2024). *OpenAI's o3: The grand finale of AI in 2024.* Interconnects.
    - Seen at: Interconnects-AI/homebase.
28. ndbroadbent (GitHub handle) (2025). *ARC-AGI Leaderboard Analysis* (Pareto frontiers; mirrored leaderboard data), GitHub.
29. Measured: the AI evaluation landscape (2026). Frontier curves derived from the Epoch AI Benchmarking Hub. GitHub `rishikeshn-eng/measured`. [Secondary]
30. alloevil (2026). *llm-benchmarks-tracker*: ARC-AGI-2 and ARC-AGI-3 entries. GitHub. [Secondary]
31. latere-ai (2026). *AI as an Infrastructure*, field notes for Sep 2026. GitHub. [Secondary]
32. Mitchell, M. (2024). *Did OpenAI Just Solve Abstract Reasoning?* AI: A Guide for Thinking Humans (Substack).
    - **Seen only as a citation** in an ICML 2025 position-paper text; content not read.
33. Anthropic (2026). *Claude Opus 5.5 System Card*, §8 Capabilities. [added by fact-check]
    - Seen at: malob/ai-system-cards mirror (`claude-opus-5-5/sections/08a-capabilities-1.md`, `08b-capabilities-2.md`). It contains no ARC-AGI row or section.
34. ARC Prize Foundation (2026). *arc-agi-3-benchmarking* README: Standard and Provider Adapter harnesses. GitHub `arcprize/arc-agi-3-benchmarking`. [added by fact-check]

---

## Verification log

This log was added by the adversarial fact-checker on 2026-09-29.

**Method and constraints.**
- The shared WebSearch budget was already exhausted (200/200) when this check started, so **no WebSearch queries could be run**.
- Instead, every load-bearing claim was re-checked in two ways:
  1. I downloaded the cited primary-text caches myself (raw.githubusercontent.com via curl) and grepped them for the exact wording and numbers, rather than relying on the dossier's summaries.
  2. I used GitHub code search and direct fetches to find **independent second copies** of the same primary texts, such as other full-text extractions of the ARC Prize reports, arXiv daily listings, official arcprize repos, a second translation of the Astra post, and other system-card sections.
- arxiv.org, arcprize.org and the GitHub REST API (repo metadata) were unreachable.
- Verdicts are confirmed / corrected / refuted / unverifiable.

### Claim verdicts

**C1. Chollet 2019 definition, "buy" skill, "Test validity is not established".**
- **Verdict: CONFIRMED** (High).
- The abstract wording ("skill-acquisition efficiency and highlighting the concepts of scope, generalization difficulty, priors, and experience"; "unlimited priors or unlimited training data allow experimenters to 'buy' arbitrary levels of skills") appears verbatim in three independent repos (commotum/4D notes, Interconnects homebase, y-arjun-y notebook).
- The §III.2 weaknesses list, including "Test validity is not established", and the title-page line "arXiv:1911.01547v2 [cs.AI] 25 Nov 2019" appear in the commotum notes.
- The ARC Prize 2024 report (ref 7) cites the same arXiv ID.
- Sources:
  - https://raw.githubusercontent.com/commotum/4D/6dd4d04fd21a681d337e4342beb6ef51e0476a07/Notes/Vision/pdfs-3/2019_MOI.md
  - https://raw.githubusercontent.com/y-arjun-y/arjunyadav/66bf0ee0a0036f6cd9d1d42b11c46649afb87691/pages-md/ai-safety.md
  - https://raw.githubusercontent.com/Interconnects-AI/homebase/b2c74a0cb0765f2c65abe8cbc8ba48d5ff877d7a/public/2024/2024-12-20-openaiso3thegrandfinaleofaiin2024.md

**C2. About 10,000 private-set scores; 49% solved by at least one 2020 entry; no deep-learning entry above 1%.**
- **Verdict: CONFIRMED** (High).
- Verbatim in two independent full-text copies of arXiv:2412.04604v2: "on the order of 10,000 private evaluation set scores have been reported"; "49% of the private evaluation set was solved by at least one team (all of which were using some variation of brute-force program search)"; "no deep-learning based approach scored above 1%".
- The same report says the 49% was achievable "by ensembling all 2020 competition entries". The best single Kaggle brute-force submission reached 40% (alijs).
- Sources:
  - the UNIR-TUC copy (URL in the claim)
  - https://raw.githubusercontent.com/atimics/crlplrimes/HEAD/paper/sources/text/chollet2024arcprize.txt

**C3. ARC Prize 2024 facts.**
- **Verdict: CONFIRMED** (High).
- Both copies confirm every item: 11 Jun–10 Nov 2024; $600,000 Grand Prize at 85%; 1,430 teams and 17,789 entries; state of the art 33% → 55.5% (MindsAI, did not open-source, ineligible); ARChitects 1st at 53.5%; single P100, under 12 h, no internet; "$10 of compute per entry" vs up to $10,000 in API credits (about 1,000× more compute).
- Sources: as for C2.

**C4. o3-preview 75.7% / 87.5%, 172×, trained on 75% of public training, efficiency mandatory, $26 vs $200 per task.**
- **Verdict: CONFIRMED** (High).
- The cached arcprize.org post (byline "By François Chollet, Published 20 Dec 2024") contains all figures.
  - Semi-private: 75.7% at $2,680 total, 6 samples, 33.5M tokens, $26/task. The low-efficiency run scored 87.5% with 1,024 samples, 5.7B tokens and $4,560/task.
  - Quotes: "trained the o3 we tested on 75% of the Public Training set"; "efficiency (e.g., compute cost) is now a required metric".
  - Re-pricing notes are dated 3/24/2025 (o1-pro pricing) and 12/10/2025 (o3-pro pricing, $80/M tokens).
- The arithmetic is internally consistent: 33.5M × $80/M = $2,680, about $26.8/task. The $200/task figure in the ARC-AGI-2 launch table (24 Mar 2025, "based on … o1-pro pricing") and in the Dec-2025 leaderboard mirror (`costPerTask: 200`) matches the o1-pro re-basing.
- *Caveat:* the original Dec-2024 table survives only as an image in the Interconnects post, which says "o3 high-compute costs not available". **The original pre-re-basing cost figure could not be recovered.**
- Sources:
  - https://raw.githubusercontent.com/ndbroadbent/arc_agi_pareto_frontiers/90d0c6822f82b8ef95423f2a37c74cdb45e7b40f/sources/o3_announcement.html
  - https://raw.githubusercontent.com/steel-dev/leaderboard/33aaee5bf46a492e0ff9a84eb7643f8d0def66d6/docs/research/arc-agi-2/paper.md
  - https://raw.githubusercontent.com/ndbroadbent/arc_agi_pareto_frontiers/90d0c6822f82b8ef95423f2a37c74cdb45e7b40f/data/evaluations.json
  - Interconnects (URL in C1)

**C5. ARC-AGI-2 launch facts.**
- **Verdict: CONFIRMED** (High).
- Launch post: "By Greg Kamradt Published 24 Mar 2025". Changelog: "2025-03-24 1,360 ARC-AGI-2 released" (1,000 / 120 / 120 / 120).
- Also confirmed in the launch post:
  - brute-force tasks removed ("all solved tasks from the original 2020 Kaggle contest");
  - "over 400 humans";
  - "at least 2 humans in 2 attempts or less";
  - "Pure LLMs score 0%"; "we estimate that o3-preview-low would score ~4%";
  - human panel average 60% at $17/task;
  - README: "Average human performance … 66%".
- The dossier's flagged discrepancy is real: the 2025 technical report lists "Public training tasks (400, imported from ARC-AGI-1)". The 2025 report adds that each task was attempted by 2–10 humans.
- Sources:
  - launch cache (C4)
  - https://raw.githubusercontent.com/arcprize/ARC-AGI-2/main/readme.md
  - https://raw.githubusercontent.com/arcprize/ARC-AGI-2/main/changelog.md
  - https://raw.githubusercontent.com/tiendungchs/PersonalWiki/HEAD/raw/ARC%20Prize%202025%20Technical%20Report.md

**C6. ARC Prize 2025 figures and the "industry standard" quote.**
- **Verdict: CONFIRMED** (High).
- Verbatim in three independent full-text copies of arXiv:2601.10904 and in the arXiv daily listing of 2026-01-19, which carries the same four authors.
- Figures: 1,455 teams and 15,154 entries; "24% at a compute cost of $0.20 per task"; NVARC 24.03%; "90 papers submitted, up from 47"; four labs listed; "establishing ARC-AGI as an industry standard benchmark for AI reasoning".
- Sources:
  - https://raw.githubusercontent.com/UNIR-TUC/arc-agi/48d931918edd904b99ef546a98adc97e19ccf528/src/SuperCompressARC/Docs/2025/2601.10904v1_arc_prize_2025.md
  - https://raw.githubusercontent.com/visual-snow/seshat/HEAD/parsed/deepmind/2601_10904.md
  - https://raw.githubusercontent.com/2shin0/arxiv-ai-mailing/HEAD/ALL/2026-01-19.md

**C7. "Knowledge overfitting" and the Gemini 3 Deep Think colour-mapping evidence.**
- **Verdict: CONFIRMED** (High), with nuance added inline.
- §4.1 of the 2025 report, verbatim in three copies, reads: "We assert that this phenomenon is now occurring with ARC-AGI-1 and ARC-AGI-2 – accidentally or intentionally, although we cannot determine which." The evidence is one quoted Gemini 3 Deep Think excerpt; the harness "does not mention ARC-AGI tasks or color formats". ARC "cannot precisely quantify the magnitude of this effect".
- This is an anecdotal diagnosis (n = 1 excerpt), not a measured rate.
- Sources: as for C6.

**C8. ARC-AGI-2 frontier of 95.0% (GPT-6 Astra, $1.12/task); Opus 5 90.42% and GPT-5.6 Sol 92.5% in the Opus 5 card.**
- **Verdict: CORRECTED** (minor, attribution).
- The 95.0% at $1.12/task is corroborated by:
  - alloevil (official-leaderboard source, dated 2026-09-02, accessed 2026-09-04; also notes OpenAI's launch table shows 95.0%);
  - latere-ai (USD 1.12);
  - measured (95, 2026-09-03);
  - the official v2.json capture maximum of 95.
  - All are secondary except the scale summary, which does not identify the row. Confidence: Medium-High.
- Opus 5 at 90.42% is explicitly ARC-verified in the Opus 5 card (§8.14.1).
- **Correction:** the card's 92.5 for GPT-5.6 Sol appears only in Table 8.1.A as a competitor figure "drawn from the respective developers' published system cards or benchmark leaderboards", without an effort label. The "(max)" label and the ARC-verified $1.44/task come from the alloevil tracker [S].
- The dossier's "one tracker lists 94.6" was **not reproduced**.
- Added: the measured tracker shows GPT-5.5 (xhigh) at 85% on 2026-04-23, the first time the 85% line was reached (about 13 months after launch).
- Sources:
  - https://raw.githubusercontent.com/malob/ai-system-cards/282a67c3c79617b23a1a23ed0869239b6e28d139/cards/anthropic/claude-opus-5/sections/08a-capabilities-1.md
  - the 08b section (URL in C10)
  - alloevil and latere (URLs in the claim)
  - https://raw.githubusercontent.com/rishikeshn-eng/measured/2e30d67d10d6db8b508c8fad39ce136b370a78f4/index.html

**C9. ARC-AGI-3 format, human study and RHAE.**
- **Verdict: CONFIRMED** (High), with two notes.
- The capture of arcprize.org/blog/arc-agi-3-human-dataset ("Greg Kamradt, Published 14 Apr 2026") confirms:
  - "458 participants"; "135 abstract reasoning environments"; 25 public demo environments;
  - 90-minute sessions under "first-run" conditions;
  - "Every environment is beaten by at least two independent participants";
  - the baseline change from 2nd-best to median, and the cap from 100% to 115% (+0.5 pp).
- docs/changelog.mdx (14 Apr 2026) and methodology.mdx confirm `(human/AI)^2`, the 1.15 cap and level-index weighting.
- *Notes:*
  1. The docs now specify the **"upper median"** human.
  2. One LLM-assisted digest of the arXiv paper (v1) says **486** participants and describes the original rule as `min(1,(h/a)^2)` against the second-best human. The participant count is unresolved; cite 458 to the blog post.
- Sources:
  - packet (URL in the claim)
  - https://raw.githubusercontent.com/arcprize/docs/main/methodology.mdx
  - https://raw.githubusercontent.com/arcprize/docs/main/changelog.mdx
  - https://raw.githubusercontent.com/nick-lang/VNR/HEAD/lit/2026-arc-agi-3-report.md

**C10. ARC-AGI-3 progression: under 1% at launch; Opus 5 30.16% vs Sol 7.78%; Astra 62.7% vs 99.9%.**
- **Verdict: CORRECTED** (effort-level mismatch).
- Under 1% at launch:
  - confirmed in the paper digests VNR, graphkasten (submitted 2026-03-24), SihoonSung and memgrafter (Gemini 3.1 Pro 0.37%, GPT-5.4 0.26%, Opus 4.6 0.25%);
  - latere-ai cites ARC's launch post for 0.51% on 25 Mar.
- Opus 5 card §8.14.2 verbatim: "verified score of 30.16%, set at high effort … GPT-5.6 Sol reached 7.78% at max effort". Its July 2026 date is secondary (measured: 2026-07-24).
- **Correction:** 62.7% ($26,098) is **max** effort under the Standard harness, while 99.9% ($18,817) is **high** effort under the Provider Adapter. At the same max effort the Provider Adapter scored 98.6% ($17,332), about 36 pp, not 37.
- The three sources agree on the per-effort table: the Chinese translation of the ARC post, a second translation of a TheNewStack article, and the Belkins chapter. The Belkins chapter itself notes that "the headline 62.7-to-99.9 comparison changes two variables".
- Sources:
  - https://raw.githubusercontent.com/lihenair/techtranslate/821908553b702d9de6565d186fdd2e8661303f6f/archive/2026-09-05/ai/OpenAIs-GPT-6-Astra-on-ARC-AGI-3.md
  - https://raw.githubusercontent.com/rocksun/mwblog/HEAD/ai/openai-astra-harness-arc-agi-3/openai-astra-harness-arc-agi-3.md
  - https://raw.githubusercontent.com/Belkins/ai-dive-deep/ecac08d8d3ffe24d6301579938d9d4e64bd101ff/src/content/chapters/49-gpt-6-astra.mdx
  - https://raw.githubusercontent.com/malob/ai-system-cards/282a67c3c79617b23a1a23ed0869239b6e28d139/cards/anthropic/claude-opus-5/sections/08b-capabilities-2.md

**C11. Testing policy points.**
- **Verdict: CONFIRMED** (High for content; single-capture provenance).
- All items are verbatim in the sha256-stamped capture of arcprize.org/policy (retrieved 2026-09-29T05:49:46Z):
  - "acknowledge the possibility of limited leakage over time";
  - zero data retention plus "successive ARC-AGI benchmark versions on a roughly annual basis";
  - ±10 / ±3 / ±15 pp agreement bands;
  - ">$10M USD gross revenue/mo";
  - "$10,000 USD per run … A single run is used";
  - "no later than 30 days after public release, or 30 days after evaluation completion if already public, whichever is earlier. Sponsors cannot impose additional embargoes";
  - the panel of Gureckis (NYU), Mitchell (Santa Fe Institute) and Misra (Columbia), which "does not review every individual test result".
- GitHub code search found this text **only** in the same tracker repo (fstandhartinger, including 2026-09-28 packets), so there is no independent copy.
- The harness split is independently confirmed by the official arcprize/arc-agi-3-benchmarking README.
- Added: donors include AI labs.
- Sources:
  - packet (URL in the claim)
  - https://raw.githubusercontent.com/arcprize/arc-agi-3-benchmarking/main/README.md

**C12. Beger, Mitchell et al. (arXiv:2510.02125).**
- **Verdict: CONFIRMED** (High).
- The verbatim abstract and seven authors appear in the 2025-10-06 arXiv cs.CL listing (marked "replace-cross", i.e. a revised version) under the link abs/2510.02125.
- Source: https://raw.githubusercontent.com/Luvata/arxive/1620fc6bcd136848375a9c12a057db05dfb0d287/pages/2025-10-06-cs-cl.html

**C13. VARC 60.4% on ARC-1; representation matters.**
- **Verdict: CONFIRMED** (High for the abstract; the second sentence is interpretation [I]).
- The verbatim abstract (v1, 2025-11-18) confirms image-to-image translation, a vanilla ViT trained from scratch on ARC data, test-time training and "60.4% accuracy on the ARC-1 benchmark".
- The eight authors are confirmed by the official BibTeX in lillian039/VARC.
- The split, and single-model vs ensemble, are not verified.
- It is listed as a CVPR 2026 poster in a secondary list.
- Sources:
  - https://raw.githubusercontent.com/Yasouimo/NetPlagStream/2ef20657d2270987392a0421ce743c2a8ac675bb/data/corpus_initial/2511.14761v1.txt
  - https://raw.githubusercontent.com/lillian039/VARC/HEAD/README.md
  - https://raw.githubusercontent.com/SkalskiP/top-cvpr-2026-papers/HEAD/README.md

**C14. H-ARC.**
- **Verdict: CONFIRMED** (upgrade from Medium to High).
- Verbatim abstract, with arXiv:2409.01374, four authors and a publication date of 2024-09-02: "1729 humans on the full set of 400 training and 400 evaluation tasks … 76.2% … 64.2% … 790 out of the 800 tasks were solvable by at least one person in three attempts".
- It is also ARC Prize 2024 report ref 18. The ARC-AGI-2 launch table uses 64.2% as the ARC-AGI-1 average.
- Caveat added inline: 3 attempts vs pass@2.
- Source: https://raw.githubusercontent.com/geometor/arcprize/10e87b6e4b2f8df6019f0cdd3fd90a53b19f0961/docsrc/refs/papers/h-arc-a-robust-estimate-of-human-performance-on-the-abstraction-and-reasoning-corpus-benchmark/index.rst

**Tally:** 12 confirmed, 2 corrected (C8, C10), 0 refuted, 0 unverifiable.

### Other corrections made in the dossier body (outside C1–C14)

- "ARC itself describes ARC-AGI-1 as 'solved'" was **not supported** by the captured arc-agi/1 page and has been rewritten.
- "Melanie Mitchell (… a prominent ARC critic)" was unsourced interpretation and has been rewritten.
- The Fable 5.1 card lists GPT-5.6 Sol at 96.5% on ARC-AGI-1 (no effort label), whereas the Opus 5 card lists 97.5 (xhigh). This is noted inline.
- "37-point swing" is qualified in three places.
- New finding: the mirrored **Claude Opus 5.5 system card (Sep 2026) contains no ARC-AGI section or row**. Medium confidence, because mirror completeness is not verified.
- New context: the ARC Prize Foundation's donors include AI labs.
- The Akyürek et al. author list has been completed.

### Reference-check summary (`research/refs/arc_agi.json`)

- **Coverage.** 36 original entries were checked, 36 of 36 (none skipped), and 2 were added (the Opus 5.5 card and the arc-agi-3-benchmarking README), for a total of 38.
- **Verified: 38 of 38 exist with the stated title, authors, year and ID/URL,** subject to the notes below. **No fabricated or garbled reference was found.**
- **Fixes applied:**
  - `akyurek2024ttt`: authors completed (Akyürek, Damani, Qiu, Guo, Kim, Andreas) from ARC Prize 2024 ref 1.
  - `spelke2007core`: the `url` pointed to the ARC report cache, not the paper; set to null. Volume, issue and DOI were not seen.
  - `anthropic2026opus5card`: `url` replaced with the CDN PDF link seen in the Fable 5.1 card.
  - `hu2025varc`: venue annotated (CVPR 2026 per a secondary list).
- **Residual weak points, flagged in `verify_note`:**
  - The ARC-AGI-3 paper's individual authors are unverified; only "ARC Prize Foundation" was seen.
  - The HRM blog title is unverified.
  - The later co-author (Denton) on Beger et al. is unverified.
  - The Mitchell Substack post is verified as a citation only; its content was not read.
  - The policy page has a single third-party capture.
  - The canonical URLs for the Fable 5.1 and Opus 5.5 cards are not verified.
  - The stars/forks of `fchollet/ARC-AGI` are unverified (API 403).

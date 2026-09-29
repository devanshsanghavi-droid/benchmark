# Public Attention, Consumer Appeal and Practitioner Uptake: Why Some LLM Evaluations Capture Attention and Others Don't

Research dossier for the benchmark-landscape survey (Phase 1). Compiled 2026-09-29.

**How this was researched.** The session's WebSearch budget (200 calls) was used up before this subagent started, so every search call was refused. arxiv.org, epoch.ai, x.com, karpathy.bearblog.dev and most news sites were unreachable; one direct fetch of karpathy.bearblog.dev returned `EGRESS_BLOCKED`. All evidence therefore comes from GitHub and raw.githubusercontent.com:

- **Primary text of Simon Willison's blog.** The repo `simonw/simonwillisonblog-backup` publishes the blog's database as newline-delimited JSON: 3,335 entries, 8,479 link posts and 1,461 quotations as of 2026-09-28. I loaded it into SQLite and queried it directly. This is the richest primary source for the pelican test, practitioner "vibe" evaluation, and the author's contemporaneous commentary on ARC-AGI, METR, Project Vend, AI Village and LMArena. Its quotation table also stores verbatim quotes with source URLs, including Chollet, Kamradt, Noam Brown, Karpathy, Zuckerberg and OpenAI.
- **Official repositories.**
  - `lmarena/lmarena.github.io` blog source.
  - `arcprize/docs`.
  - `centerforaisafety/hle` (README and `citation.txt`).
  - `METR/eval-analysis-public`.
  - `google-deepmind/game_arena`.
  - `simonw/pelican-bicycle`.
  - `dylanjcastillo/blog/_extras/pelicanmaxxing` (config and README).
  - `lisadunlap/VibeCheck`.
  - `stanford-cs336/spring2025-lectures` (lecture 12 on evaluation).
  - The yc-oss mirror of the YC company API.
- **Verbatim copies of papers or abstracts held in third-party GitHub repos.** Each is labelled where used:
  - ARC Prize 2024 technical report full text;
  - ARC Prize 2025 technical report abstract;
  - Karpathy's 2025 year-in-review;
  - Hardt's SIAM News essay;
  - arXiv metadata records;
  - BibTeX abstracts for Ott et al., Koch et al., Orr & Kang, and Blum & Hardt.
- **Secondary compilations,** always labelled [S]:
  - the smol-ai AINews archive (`smol-ai/ainews-web-2025`);
  - `benchflow-ai/awesome-evals` notes;
  - `rasynai/MarigoldBench` community-discourse analysis;
  - `vibewatch/startup` LMArena evidence file;
  - `steveash/hitchhikers-guide-to-ai-native-engineering` source notes.

Sibling dossiers cover adjacent ground: `arenas_preference.md` (Arena methodology and critiques), `knowledge_exams.md` (HLE audits), `metascience_validity.md` (validity theory, BetterBench) and `user_failed_a.md` (game benchmarks). I cross-reference them rather than repeat them.

**Evidence tags used throughout.**

| Tag | Meaning |
|---|---|
| **[V]** | Verified this session from a primary source, or from a verbatim copy of a primary source whose provenance is stated |
| **[S]** | Seen only in a secondary source (newsletter archive, compiled notes, third-party summary). The original URL is given where known, but I did not fetch it |
| **[I]** | My interpretation |
| **[U]** | Unverified or anecdotal; do not cite as fact |

---

## Summary

**1. The lead's three-factor hypothesis is partly right but incomplete [I].** The hypothesis is that successful evaluations share an underlying philosophy, a measurable leaderboard, and consumer appeal ("fun").
- **Philosophy.** ARC-AGI and Chatbot Arena do have an explicit philosophy.
  - ARC: "easy for humans, hard for AI"; Chollet's definition of intelligence as skill-acquisition efficiency [V].
  - Arena: real people, real prompts, "the community calls the winners" [V].
- **A leaderboard is not necessary for attention.** The most viral informal test of 2025, Simon Willison's "pelican riding a bicycle", began as an explicit joke and never had a leaderboard. The "count the r's in strawberry" meme had neither a philosophy nor a leaderboard [V].
- **"Fun" is better stated as "stakes plus story".** HLE and METR are not fun, but they carry high stakes and dramatic framing.
- **Four factors the hypothesis misses, each with evidence below:**
  - (a) human-legible units;
  - (b) a lab-adoption loop, where labs print the number in launch tables;
  - (c) recurring "moments", such as release-day tests, mystery models, prizes and tournaments;
  - (d) shareable artifacts or stories.

**2. Human-legible units recur in every case [V facts, I pattern].**
- METR reports AI ability in *hours of human work*, with a time horizon "doubling approximately every 7 months" [V, repo README].
- Vending-Bench reports *dollars of net worth*. Andon Labs argue money "never saturates" [S].
- ARC anchors every score to "tasks humans find easy". ARC-AGI-3 scores *action efficiency relative to the upper-median first-time human player* [V].
- Arena borrowed Elo "from chess and other competitive games" [V].
- HLE borrows the exam metaphor ("the final closed-ended academic benchmark of its kind") [V].

**3. Attention accumulates over years and is triggered by moments, not launch [V].**
- ARC existed for five years. Pre-2024 competitions offered $20,000 (2020) and $100,000 (2022 and 2023) in prizes [V].
- It was renamed from "ARC" to "ARC-AGI" [V], then relaunched in 2024 with a $600,000 grand prize (1,430 teams, 17,789 entries) [V].
- It became a headline in December 2024 when o3 scored 75.7% (87.5% at high compute). Chollet wrote that ARC-AGI-1 "took 4 years to go from 0% with GPT-3 in 2020 to 5% in 2024 with GPT-4o" [V].
- By 2025, four frontier labs (Anthropic, Google DeepMind, OpenAI, xAI) reported ARC-AGI in model cards [V abstract copy].

**4. The pelican test is a complete natural experiment in viral-benchmark lifecycles [V, all from the primary blog database].**
- **Created** 25 October 2024 as a joke. It was chosen because no pelican-on-bicycle SVGs "might have already been sucked into the training data".
- **Adopted** by Karpathy in his Grok 3 "vibe check" (18 February 2025).
- **Showcased** in an AI Engineer World's Fair keynote with an LLM-judged Elo tournament (June 2025).
- **Noticed by labs:**
  - a split-second appearance in the Google I/O keynote (May 2025);
  - a GPT-5 launch video (August 2025);
  - an Anthropic interpretability paper (October 2025);
  - a Jeff Dean animation tweet (February 2026).
- **Denied as a training target** by an OpenAI researcher ("we do not hill climb on svg art", November 2025).
- **Hardened** with a v2 prompt (November 2025).
- **Declared decoupled from utility** by its creator (April 2026: "even that loose connection to utility has been broken"; July 2026: "That connection has been mostly severed now").
- **Formally tested for gaming** in a 1,008-SVG, 7-model factorial study that found no pelican-specific boost (July 2026) [V config and results: the results are verified from the post source `dylanjcastillo/blog/posts/pelicanmaxxing.qmd`, dated 18 July 2026] [corrected by fact-check].
- **Lesson:** shareable, absurd, visual and cheap tests spread fast. Their validity is transient, and they invite suspicion of gaming.

**5. Consumer participation is real but commercially and scientifically double-edged.**
- **Scale:**
  - Arena went from 4.7K votes in its first week to "3M+ votes, 400+ models, 300+ pre-release tests" (April 2025) [V]. The first week ran from late April to early May 2023: the platform launched in late April, and the 3 May 2023 post says it "was launched about one week ago" [corrected by fact-check].
  - The company later reported "2M+ monthly votes" and "3M+ monthly users" [S].
  - It raised $100M at a $600M valuation (May 2025) and $150M at $1.7B (January 2026) [S, TechCrunch via evidence file; corroborated by several independent news digests during fact-check].
- **What drives participation:** the community's stated motive is "frequent access to the best models, and being a part of the first to access the newest ones" [V]. Anonymous pre-release models (for example `gpt2-chatbot`, April 2024) trigger "a parallel distributed 'vibe check'" [V].
- **The downside:**
  - Popular preference signals reward style and agreeableness (see `arenas_preference.md`).
  - OpenAI's April 2025 sycophancy rollback showed three things [V]:
    - A/B tests "seemed to indicate that the small number of users who tried the model liked it".
    - User feedback (thumbs-up/down) "can sometimes favor more agreeable responses".
    - Expert "vibe checks" had flagged that the behaviour "felt" slightly off.

    [corrected by fact-check] The original line attributed the "agreeable responses" quote to A/B tests; OpenAI attributes it to user feedback.

**6. "Arena for X" is now a genre.** Its evidence of attention is mostly secondary.
- Design Arena is a YC Summer 2025 company classified as "Consumer", with the one-liner "World's largest crowdsourced benchmark for AI-generated design" [V]. Its placements feature in 2026 launch-day coverage (GLM-5.2 "#1 on Design Arena", Elo 1360, posted by @Designarena and relayed in launch round-ups) [S].
- Siblings in the genre:
  - WebDev/Code Arena;
  - MC-Bench/MineBench, which uses Minecraft builds [V repos];
  - Kaggle Game Arena, launched 4 August 2025 with a chess exhibition and grandmaster commentary [S; repo V].

**7. Story-driven agent evals win attention through failure narratives, but can backfire [V].**
- **Stories that spread:**
  - Project Vend's tungsten cubes [V];
  - Vending-Bench's Claude emailing the FBI [S];
  - AI Village's public replays [V].
- **Lab adoption:** Google put Vending-Bench 2 net worth ($5,478.16 for Gemini 3 Pro) in its Gemini 3 launch table next to HLE and ARC-AGI-2 [V; the text Willison published is Gemini-3-generated alt text of Google's table image, and the numbers are corroborated by independent copies [corrected by fact-check]].
- **Backfire:** AI Village's "act of kindness" email to Rob Pike (December 2025) produced a public backlash. Simon Willison argues such experiments must keep humans in the loop for outbound actions that affect non-consenting people [V].

**8. Practitioners distrust public numbers and rely on vibes, private stashes and revealed preference [V/S].**
- **Karpathy:**
  - March 2025: "there is an evaluation crisis. I don't really know what metrics to look at right now" [S, multiple consistent copies].
  - December 2025: "general apathy and loss of trust in benchmarks", "Training on the test set is a new art form" [V verbatim copy].
- **OpenAI** formally runs internal "vibe checks" [V].
- **Simon Willison** keeps "a collection of tasks that are just beyond the capabilities of the frontier models" and asks labs for "an example prompt which failed on [the previous model] but succeeds" [V].
- **Stanford CS336** (Spring 2025) teaches "Vibes", OpenRouter usage ("Maybe a model is good if people choose to use it (and pay for it)") and the Karpathy "crisis" as evaluation modes [V].

**9. The academic literature on benchmark adoption is thin but consistent [V].**
- Ott et al. (Nature Communications 2022; 3,765 benchmarks): "many benchmarks fail to find widespread utilization"; future benchmarks "should emphasize versatility, breadth and real-world utility".
- Koch et al. (NeurIPS 2021 D&B): "increasing concentration on fewer and fewer datasets" and on datasets from "a small number of elite institutions".
- Martínez-Plumed et al. (Nature Machine Intelligence 2021) studied community dynamics behind 25 popular benchmarks.
- Orr & Kang (FAccT 2024) trace benchmarking's "competitive" epistemology through the Common Task Framework and the Netflix Prize.
- Hardt (SIAM News 2025): "Competitive leaderboard climbing has been the main way machine learning advances."
- **Gap:** I found no controlled or causal study of what makes an LLM benchmark go viral. All virality claims below are case-based.

**10. Bottom line for our project [I].** Design two channels:
- a **measurement channel** that is rigorous, largely hidden, versioned, with CIs and human baselines;
- an **attention channel** with a thesis-bearing name, a human-legible unit, a single headline ladder with cost, shareable per-item artifacts and failure stories, a public "try it yourself" subset, and recurring release-day and season moments.

Keep them coupled but separable, so that popularity cannot corrupt the score. This avoids the Arena style-bias, pelicanmaxxing, sycophancy and HLE-label-noise failure modes.

---

## Detailed findings

### 1. Testing the lead's hypothesis: philosophy + leaderboard + fun

The table scores each case on the three factors the lead proposed and on the four additional factors this dossier identifies. Cell entries are [I] judgements grounded in the evidence in §2.

| Case | Explicit philosophy / thesis | Measurable ladder | "Fun" / consumer appeal | Human-legible unit | Lab-adoption loop | Recurring moments | Shareable artifact / story | Attention outcome |
|---|---|---|---|---|---|---|---|---|
| ARC-AGI / ARC Prize | Strong (Chollet 2019 definition; "easy for humans, hard for AI") | Yes (Kaggle + ARC-AGI-Pub, cost per task) | Moderate (humans can play tasks) | % of human-easy tasks; RHAE vs human actions | Yes (4 labs' model cards in 2025) | Annual prize, o3 moment, new versions | Puzzle grids; o3 cost headlines | Very high |
| Chatbot Arena / LMArena | Strong ("the community calls the winners") | Yes (Elo/BT with CIs) | High (free frontier access, mystery models) | Elo (chess metaphor) | Yes (launch posts cite rank) | Every model release; pre-release aliases | Side-by-side battles | Very high, commercial |
| Design Arena | Moderate (crowd taste in design) | Yes (Elo per category) | High (visual, seconds to judge) | Elo | Partial (launch-day coverage) [S] | Launch days; anonymous previews | Designs/websites | High (niche) |
| Pelican on a bicycle | None, explicitly a joke | No (gallery; one ad-hoc Elo run) | Very high (absurd, visual) | An image anyone can judge | Yes (I/O keynote, GPT-5 video) | Every model release | SVG images | Very high among practitioners |
| Strawberry r-count | None (a meme) | No | High (gotcha) | Right/wrong | Indirect (o1 codename coincidence) | Each release | Screenshot | Very high, short-lived |
| HLE | Strong framing ("last exam") | Yes | Low (not playable) | Exam % | Yes (Gemini 3, Kimi K2 tables) | New model results | Example questions | High |
| METR time horizon | Strong (forecasting autonomy) | Yes (trend chart) | Low | Human hours; doubling time | Yes (widely cited) | New model points | One chart | High |
| Vending-Bench / Project Vend / AI Village | Moderate (long-horizon coherence) | Vending-Bench yes; Village no | High (stories) | Dollars | Yes (Gemini 3 table) | Ongoing seasons | Meltdown anecdotes | High, with backlash risk |
| Kaggle Game Arena | Moderate ("soft skills" via games) | Yes (Elo, unified board) | High for chess fans | Elo | Google-owned | Tournaments | Commentated matches | High publicity; practitioner uptake unclear |

**Reading of the table [I]:**
- Attention requires at least one of: a shareable artifact or story, a human-legible unit, or a lab-adoption loop.
- Durable practitioner uptake additionally requires a measurable ladder with headroom plus institutional maintenance, which the joke tests lack.
- "Philosophy" matters most for *longevity and legitimacy*. ARC survived several saturation cycles by versioning (ARC-AGI-1 → 2 → 3) under the same thesis. It matters less for initial virality.

### 2. Case studies

#### 2.1 ARC-AGI and ARC Prize: philosophy plus prize plus a "moment"

**Philosophy and naming [V].**
- The ARC Prize 2024 technical report (Chollet, Knoop, Kamradt, Landers; arXiv:2412.04604v2, dated 9 January 2025) states the origin. In 2019 Chollet defined AGI as "a system capable of efficiently acquiring new skills and solving novel problems for which it was neither explicitly designed nor trained". He published the Abstraction and Reasoning Corpus "(later renamed ARC-AGI to avoid name collisions with other AI benchmarks)".
- The abstract calls it "the most important unsolved AI benchmark in the world because it seeks to measure generalization on novel tasks – the essence of intelligence – as opposed to skill at tasks that can be prepared for in advance". Source: verbatim text copy at `atimics/crlplrimes/paper/sources/text/chollet2024arcprize.txt`.
- Greg Kamradt's ARC-AGI-2 launch post (25 March 2025) states the design contrast that makes it quotable [V, quoted verbatim in Willison's quotation table with source URL https://arcprize.org/blog/announcing-arc-agi-2-and-arc-prize-2025]:
  - "All other AI benchmarks focus on superhuman capabilities or specialized knowledge by testing 'PhD++' skills. ARC-AGI is the only benchmark that takes the opposite design choice – by focusing on tasks that are relatively easy for humans, yet hard, or impossible, for AI".
  - "Pure LLMs score 0% on ARC-AGI-2 ... every task in ARC-AGI-2 has been solved by at least 2 humans in under 2 attempts."

**Attention built slowly, then spiked [V].**
- Pre-2024 competitions:
  - 2020 Kaggle: $20,000 in prizes;
  - 2022 ARCathon 1: $100,000;
  - 2023 ARCathon 2: $100,000.
- In 2020 "no deep-learning based approach scored above 1%" (2024 report).
- **ARC Prize 2024:**
  - Prizes: a $600,000 grand prize for 85% on the private set (unclaimed), $50,000 in progress prizes and $75,000 in paper prizes.
  - "In total, 1,430 teams submitted 17,789 entries."
  - State of the art on the private set rose from 33% to 55.5%. The ARChitects won with 53.5%.
  - The authors "were surprised to the degree that well-funded AI research startups would change their roadmaps to prioritize beating the benchmark". They knew of "at least seven distinct efforts ... by organizations that have greater than $1M in funding".
- **The o3 moment (20 December 2024)** [V; Chollet quoted in Willison's quotation table, source https://arcprize.org/blog/oai-o3-pub-breakthrough]:
  - "OpenAI's new o3 system - trained on the ARC-AGI-1 Public Training set - has scored a breakthrough 75.7% on the Semi-Private Evaluation set at our stated public leaderboard $10k compute limit. A high-compute (172x) o3 configuration scored 87.5%."
  - "ARC-AGI-1 took 4 years to go from 0% with GPT-3 in 2020 to 5% in 2024 with GPT-4o. All intuition about AI capabilities will need to get updated for o3."
  - Willison's same-day post extrapolated a cost of roughly $1.1M for the high-compute run (172 × $6,677). That is *his* estimate, not ARC's [V]. Cost became part of the story.
- **Cost-efficiency as a headline [V, ARC Prize account quoted by Willison, 11 December 2025]:** "A year ago, we verified a preview of an unreleased version of @OpenAI o3 (High) that scored 88% on ARC-AGI-1 at est. $4.5k/task. Today, we've verified a new GPT-5.2 Pro (X-High) SOTA score of 90.5% at $11.64/task. This represents a ~390X efficiency improvement in one year."
- **ARC Prize 2025** [V, verbatim abstract copy of arXiv:2601.10904 at `tiendungchs/PersonalWiki`; also a full-text copy at `UNIR-TUC/arc-agi`. Authors are Chollet, Knoop, Kamradt and Landers, and the report is dated 19 January 2026 [corrected by fact-check]]:
  - "The Kaggle competition attracted 1,455 teams and 15,154 entries, with the top score reaching 24% on the ARC-AGI-2 private evaluation set. Paper submissions nearly doubled year-over-year to 90 entries".
  - "four frontier AI labs (Anthropic, Google DeepMind, OpenAI, and xAI) reported ARC-AGI performance in public model cards in 2025, establishing ARC-AGI as an industry standard benchmark for AI reasoning".
  - It also warns of "knowledge-dependent overfitting" and "new forms of benchmark contamination".
- **Lab-adoption examples [V, launch materials as published by Willison. The Gemini 3 table text is alt text generated by Gemini 3 Pro from Google's screenshot, not a manual transcription. Its figures match independent copies [corrected by fact-check]]:**
  - Gemini 3 Pro (18 November 2025): "ARC-AGI-2 (Visual reasoning puzzles; ARC Prize Verified) Gemini 3 Pro 31.1%, Gemini 2.5 Pro 4.9%, Claude Sonnet 4.5 13.6%, GPT-5.1 17.6%".
  - GPT-5.2 (11 December 2025): "52.9% on ARC-AGI-2 (up from 17.6% for GPT-5.1 Thinking)".
  - The "ARC Prize Verified" label is itself a trust device [I].

**ARC-AGI-3 and human-anchored scoring [V, `arcprize/docs`].**
- ARC-AGI-3 is an "Interactive Reasoning Benchmark" of games. It is game-based, so it is out of scope for our design, but its *scoring* is instructive.
- Scoring uses "Relative Human Action Efficiency" (RHAE): `level_score = (human_baseline_actions / ai_actions)^2`. It is capped at 1.15 per level and weighted toward later levels.
- The baseline is the "upper median human (by fewest actions)" among first-time players.
- The docs invite the public directly: "Can you build an agent to beat this game?", with a human-play GIF.
- ARC Prize 2026 runs on Kaggle ([V] `arc-prize-2026.mdx`).
- A caution on durability [V, Willison, 3 September 2026, quoting the ARC blog]: GPT-6 Astra scored 99.9% on ARC-AGI-3 ("released in March") for $19K using OpenAI's custom "Provider Adapter harness", versus 62.7% for $26K with the default harness. Harness choice is now a first-order variable, and even a flagship interactive benchmark can be approached within months [I].

**Why it works [I]:**
1. A one-sentence, falsifiable thesis with a human anchor.
2. Prize money plus open-sourcing requirements, which create a research community (1,400+ teams per year).
3. A secondary public leaderboard with verified frontier-lab entries and cost disclosure.
4. Versioning under one brand when saturation approaches.
5. Tasks that laypeople can look at and attempt.

**Risks:**
- Knowledge coverage and contamination (the 2025 report's own warning).
- Harness dependence.
- The "AGI" name invites over-reading. Chollet himself stressed that "Passing ARC-AGI does not equate to achieving AGI" [V, quoted by Willison, 20 December 2024].

#### 2.2 Chatbot Arena / LMArena: the consumer participation engine

Methodology, critiques and reforms are covered in `arenas_preference.md`. Here I focus on the attention and participation mechanics.

- **Metaphor and design desiderata (first results/leaderboard post, 3 May 2023; the arena itself launched about a week earlier, in late April 2023 [corrected by fact-check]) [V, `lmarena.github.io/_posts/2023-05-03-arena.md`]:**
  - The post adopts "the Elo rating system, which is a widely-used rating system in chess and other competitive games".
  - It lists the properties a benchmark system should have: "Scalability", "Incrementality" ("evaluate a new model using a relatively small number of trials") and "Unique order".
  - It invited "the entire community to join this effort by contributing new models and evaluating them". The first week produced "4.7k valid anonymous votes".
- **Growth and stated motive (27 April 2025 post) [V]:**
  - "3M+ votes, 400+ models, and 300+ pre-release tests"; "**Tens of millions** of battle pairings"; "1.5 million prompts ... released".
  - Providers receive 20% of the data; "nearly 41% of battles involving an open model".
  - The stated user motive: "a valuable experience involves having frequent access to the best models, and being a part of the first to access the newest ones. To meet the community expectations ... we upsample the best models, and new models".
  - "Every model steps into the arena, but only the best rise to the top ... the community calls the winners."
- **Fun as an explicit product goal [V, 17 April 2025 company-formation post]:** "The goal is to make LMArena more accessible, more reliable, and ultimately more fun to use for everyone testing the world's leading AI models." The same post promises "LMArena will stay neutral, open, and accessible to everyone".
- **Mystery-model mechanic [V, Willison, 29 April 2024]:** An unlabeled `gpt2-chatbot` appeared on the Arena. "Lots of people are performing a parallel distributed 'vibe check' and sharing results with each other". It was later confirmed as OpenAI's. Design Arena later showed the same mechanic with an anonymous "Arrow Preview" SVG model (February 2026) [S, AINews 26-02-26].
- **Stakes [V, Willison, 30 April 2025]:** The Arena "has become the go-to place for vibes-based evaluation of LLMs ... one of the most influential leaderboards in the LLM world, which means that billions of dollars of investment are now being evaluated based on those scores."
- **Commercial scale [S, vibewatch evidence file citing TechCrunch 21 May 2025 and 6 January 2026, PR Newswire, arena.ai blog]:**
  - "$100 million in a seed funding round that values the organization at $600 million".
  - "$150 million Series A at a post-money valuation of $1.7 billion".
  - Company claims of "250M+ real conversations, 2M+ monthly votes, and ... 3M+ monthly users".
- **Practitioner and lab pushback:**
  - Mark Zuckerberg (Dwarkesh podcast, April 2025): open benchmarks and "the LM Arena stuff ... are often skewed toward a very specific set of uses cases, which are often not actually what any normal person does in your product" [V, quoted with source URL https://www.dwarkesh.com/p/mark-zuckerberg-2].
  - Willison, in June 2025: "There are leaderboards, but I've been losing some trust in those recently" [V].
  - Karpathy's year-in-review lists "getting that upvote from a human on the LM Arena" among the optimisation targets that make LLMs "jagged" [V verbatim copy].

**Lesson [I]:** Participation is bought with *access* (free frontier and pre-release models) and *novelty* (mystery models), not with altruism. That buys scale, but it also samples voters who reward style. A new benchmark that wants crowd participation must pay participants in something they value and must separate taste from correctness.

#### 2.3 "Arena for X": Design Arena, WebDev/Code Arena, MC-Bench, Kaggle Game Arena

- **Design Arena [V/S].**
  - YC record (yc-oss mirror): one-liner "World's largest crowdsourced benchmark for AI-generated design", batch Summer 2025, team size 3, industry "Consumer", former name "Arcada". `launched_at` decodes to 30 July 2025 [V].
  - Early community traction: an August 2025 r/LocalLLaMA post, "Half of the models in the top 10 on Design Arena are OW/OS, and they're all from China" (score 192) [S, AINews 25-08-08]. A geopolitical or open-vs-closed framing made the leaderboard shareable [I].
  - By mid-2026 its placements were part of launch-day coverage. AINews says GLM-5.2 "was immediately positioned by third parties", including "Design Arena per @Designarena". Whether the labs' own posts cite it is not verified [S, AINews 26-06-16 and 26-07-15]:
    - GLM-5.2 "#1, Elo 1360";
    - Thinking Machines' Inkling at "#9 overall, Elo 1257" on the Agentic Web App Arena.
  - Methodology details are in `arenas_preference.md` [S].
- **WebDev/Code Arena.** Users vote on two *working apps*. See `arenas_preference.md`. Willison (31 December 2024): "Hard to come up with a more convincing argument that this feature is now a commodity" [V]. The "feature" is prompt-driven app building (Artifacts/Canvas-style); the WebDev Arena leaderboard is his evidence for it [corrected by fact-check].
- **MC-Bench / MineBench.** Crowd votes on Minecraft builds generated by LLMs (`mc-bench/mc-bench-frontend`; `Ammaar-Alam/minebench`, arena landing page) [V repos exist]. This is game-adjacent: the output is a visual artifact, not gameplay.
- **Kaggle Game Arena** [S, AINews 25-08-04 and 25-08-05; repo V]:
  - "Kaggle and Google launched the Game Arena to pressure-test models in competitive games (starting with text chess), with live commentary by Magnus Carlsen and Hikaru Nakamura".
  - A 3-day chess exhibition with 8 models.
  - Community skepticism: "some engineers questioned chess as a true test of intelligence, viewing it as a strategy optimization game".
  - February 2026: Google framed poker, Werewolf and chess as "soft skills" evaluation [S, AINews 26-02-04].
  - The harness (`google-deepmind/game_arena`) runs on OpenSpiel [V].
  - Mid-2026 Reddit commenters used Game Arena as the reference ordering against which other chess leaderboards are sanity-checked [S, AINews 26-08-03].
  - Interpretation [I]: celebrity commentary and a tournament format bought publicity, but I found no evidence that practitioners choose models by Game Arena rank. This supports the lead's view that games alone do not produce *practitioner* uptake.

#### 2.4 Pelican riding a bicycle: lifecycle of a viral practitioner test (all [V] from the blog database unless noted)

| Date | Event | Source (slug in `simonwillisonblog-backup`) |
|---|---|---|
| 2024-10-25 | First post. "I decided to roll out my own LLM benchmark ... I chose that because a) I like pelicans and b) I'm pretty sure there aren't any pelican on a bicycle SVG files floating around (yet) that might have already been sucked into the training data." 16 models; prompt `Generate an SVG of a pelican riding a bicycle`. | blogmark `pelicans-on-a-bicycle` → https://simonwillison.net/2024/Oct/25/pelicans-on-a-bicycle/ |
| 2025-02-18 | Karpathy's Grok 3 "vibe check" includes the pelican prompt: "I was delighted to see him include my ... benchmark in his tests". | blogmark `andrej-karpathy-grok-3` (tweet https://twitter.com/karpathy/status/1891720635363254772) |
| May 2025 | Appears "(for a split second) in the Google I/O keynote". Willison: "They're on to me." | entry `six-months-in-llms`; entry `the-year-in-llms` |
| 2025-06-06 | AI Engineer World's Fair keynote "The last six months in LLMs, illustrated by pelicans on bicycles". "There are plenty of benchmarks full of numbers. I don't get much value out of those numbers ... Everyone needs their own benchmark ... started as a joke but is beginning to show itself to actually be a little bit useful!" He ran an LLM-judged pairwise tournament: 34 images, 560 matches, gpt-4.1-mini judge, Elo table, "about 18 cents". | https://simonwillison.net/2025/Jun/6/six-months-in-llms/ |
| Aug 2025 | "I got to talk about it in a GPT-5 launch video filmed at OpenAI HQ." | entry `the-year-in-llms` |
| Oct 2025 | "got a mention in an Anthropic interpretability research paper". | entry `the-year-in-llms` |
| 2025-11-13 | "What happens if AI labs train for pelicans riding bicycles?" His answer is that they "would get caught", because he would test other animals and vehicles. It quotes OpenAI's Aidan McLaughlin: "we do not hill climb on svg art" (X, ID decodes to 6 November 2025). | https://simonwillison.net/2025/Nov/13/training-for-pelicans-riding-bicycles/ |
| 2025-11-18 | "my pelican benchmark is beginning to feel a little bit too basic". v2 prompt: "Generate an SVG of a California brown pelican riding a bicycle. The bicycle must have spokes and a correctly shaped bicycle frame ...". | entry `gemini-3` |
| 2025-12-31 | Year review, "The year of pelicans riding bicycles": "It's ended up a meme in its own right ... To my surprise, there appears to be a correlation between how good the model is at drawing pelicans on bicycles and how good it is overall." It counted "89 posts and counting". | https://simonwillison.net/2025/Dec/31/the-year-in-llms/ |
| Feb 2026 | "Google's Jeff Dean tweeted this video of an animated pelican riding a bicycle, plus a frog on a penny-farthing ... So maybe the AI labs have been paying attention after all!" | entry `5-minute-llms` (19 May 2026) |
| 2026-04-16 | Qwen3.6-35B-A3B on a laptop beats Claude Opus 4.7: "The pelican benchmark has always been meant as a joke ... for the most part, there has been a direct correlation between the quality of the pelicans produced and the general usefulness of the models ... Today, even that loose connection to utility has been broken." | entry `qwen-beats-opus` |
| 2026-04-21 | Approves a third party's effort "to pollute the training set of pelicans riding bicycles" (a "Pelican Riding a Bicycle #1" page that shows a bear on a snowboard). | blogmark `scosman` |
| 2026-07-16 | "That connection has been mostly severed now ... The biggest limitation of the pelican is that it doesn't touch at all on the thing that matters most for today's model: agentic tool calling ... So don't go using pelicans to compare models!" The value left is "a forcing function for actually trying the model". | https://simonwillison.net/2026/Jul/16/kimi-k3/ |
| 2026-07-22 | Links Dylan Castillo, "Are AI labs pelicanmaxxing?" Design verified from the code config: 7 models (`gpt-5.6-terra`, `grok-4.5`, `glm-5.2`, `qwen3.7-max`, `gemini-3.5-flash`, `claude-sonnet-5`, `deepseek-v4-pro`), 8 animals × 6 vehicles, `N_SAMPLES = 3` (1,008 SVGs) [V]. Findings [V, post source `posts/pelicanmaxxing.qmd` dated 18 July 2026 [corrected by fact-check]; the steveash note agrees]: pelican 6th of 8 animals; the pelican-bicycle cell #42 of 48; no significant lab-specific pelican effect (smallest p = 0.25); the design "can't detect" "SVGmaxxing". | blogmark `are-ai-labs-pelicanmaxxing`; `dylanjcastillo/blog/_extras/pelicanmaxxing/config.py` |

The backup lists 42 blog entries and 92 link posts tagged `pelican-riding-a-bicycle` as of 28 September 2026 [V, SQL count].

**Why it spread [I, with quoted rationale]:**
- **Absurdity plus difficulty.** "Drawing bicycles is really hard ... pelicans can't ride bicycles. They're the wrong shape!" [V].
- **Instant visual judgement.** Anyone can judge the image in a second.
- **Cheap and fast.** Minutes and cents per model.
- **A running series tied to every release day.**
- **Interpretable artifacts.** "LLMs almost universally include comments in their attempts. This means you get a better idea of what they were trying to achieve" [V].
- **A trusted curator** with a large audience.

**Why it lost validity [V/I]:**
- Frontier capability shifted to agentic tool use, which the test does not touch.
- Some labs may optimise the *class* ("SVGmaxxing"), which Castillo's design explicitly cannot detect.
- Public galleries pollute future training data.

**Lesson for us [I]:** Borrow the *form* (a visual per-item artifact, a release-day ritual, a transparent prompt), not the *measurement*. Rotate a hidden, perturbed family of prompts, as Castillo's factorial grid does.

#### 2.5 "How many r's are in strawberry": a gotcha meme

- **The meme's reach.** OpenAI's o1 was "previously rumored as having the codename 'strawberry'" [V, Willison, 12 September 2024]. Noam Brown felt he had to deny the link: "Believe it or not, the name Strawberry does not come from the 'How many r's are in strawberry' meme. We just chose a random word. As far as we know it was a complete coincidence." [V, quoted with source https://twitter.com/polynoamial/status/1834312400419652079; ID decodes to 12 September 2024].
- **Academic follow-up.** Fu, Ferrando, Conde, Arriaga & Reviriego, "Why Do Large Language Models (LLMs) Struggle to Count Letters?", arXiv:2412.18626 (19 December 2024), opens with "the inability of many LLMs to count the number of 'r' letters in 'strawberry'".
  - It finds "models are capable of recognizing the letters but not counting them".
  - Errors correlate most strongly "with the number of letters with counts larger than one" [V, arXiv metadata copy in `MystenLabs/snowreads`].
- **Practitioner verdict.**
  - December 2024: "OpenAI's o1 may finally be able to (mostly) count the Rs in strawberry, but its abilities are still limited".
  - December 2025: "Initial demos showed it solving mathematical logic puzzles and counting the Rs in strawberry - two things I didn't find myself needing in my day-to-day model usage. It turned out that the real unlock of reasoning was in driving tools." [V].
- **Lesson [I].** Gotchas go viral because they expose a *surprising* failure that anyone can verify. They die once fixed, and they measure a tokenizer artifact rather than a useful capability. A new benchmark can harvest the "surprising failure anyone can verify" appeal as its *example gallery*, not as its metric.

#### 2.6 Humanity's Last Exam: naming and contributor incentives

- **Framing.** The official README says HLE "is designed to be the final closed-ended academic benchmark of its kind with broad subject coverage", with "2,500 questions across dozens of subjects". It ships a canary string [V, `centerforaisafety/hle`].
- **Contributor incentives.** Stanford CS336 lecture 12 (Spring 2025) lists HLE as "Awarded $500K prize pool + co-authorship to question creators" [V, `stanford-cs336/spring2025-lectures/lecture_12.py`].
- **Peer-reviewed title drops the brand.** The official `citation.txt` gives the Nature version as "A benchmark of expert-level academic questions to assess AI capabilities", *Nature* 649, 1139–1146 (2026), doi:10.1038/s41586-025-09962-4, arXiv:2501.14249. Authors are listed as "Center for AI Safety and Scale AI and HLE Contributors Consortium" [V]. The public name and the journal title diverge [I]: the brand did its attention work in launch tables and press, not in peer review.
- **Lab adoption.** Gemini 3 Pro launch table: "Humanity's Last Exam (Academic reasoning) No tools: Gemini 3 Pro 37.5% ... With search and code execution: Gemini 3 Pro 45.8%" [V. The text is Gemini-generated alt text published by Willison, not his own transcription; the figures are corroborated independently [corrected by fact-check]]. Kimi K2 Thinking claimed a "new state-of-the-art on Humanity's Last Exam (HLE)" (November 2025) [V, quoted by Willison].
- **Validity problems.** Label-noise audits are covered in `knowledge_exams.md`:
  - FutureHouse: about 29% of chemistry and biology answers conflict with the literature;
  - HLE-Verified;
  - Epoch AI's September 2026 rating of "Flawed".
- **Anecdote not verified.** A widely repeated story says the benchmark was first named "Humanity's Last Stand". I found no primary source this session [U]; do not cite it.
- **Lesson [I].** A grandiose, thesis-bearing name plus money and co-authorship for contributors generates both attention and items. Crowdsourced expert items at speed produce label noise that later audits expose. Budget for verification from day one.

#### 2.7 METR time horizons: a unit and a chart

- **The unit and the trend [V].** `METR/eval-analysis-public` README:
  - "The time horizon methodology measures AI agent capabilities by: 1. Collecting tasks with known human completion times ... 3. Fitting a logistic curve modeling P(success) as a function of log2(human_minutes) 4. Extracting the 'time horizon'".
  - "**Key finding**: AI agent time horizons have been doubling approximately every 7 months."
  - The repo holds Time Horizon v1.0 and v1.1 reports.
- **The paper.** "Measuring AI Ability to Complete Long Tasks", arXiv:2503.14499 (March 2025), first author Thomas Kwa. The author order is Kwa, West, Becker, Deng, Garcia, Hasin, Jawhar, Kinniment, Rush, Von Arx and others, 25 authors ending with Barnes and Chan [corrected by fact-check] [V, arXiv author list copies in `CSQianDong/Awesome-arXiv-Daily-Reporter` and `lhl/agentic-memory`]. The abstract states Claude 3.7 Sonnet's 50% horizon is "around 50 minutes" and the doubling is "approximately every seven months since 2019" [V]. A daily-papers summary reports "170 software engineering, cybersecurity, machine learning, and general reasoning tasks" and a 50% horizon for Claude 3.7 Sonnet of "around 50 minutes" [S, `gabrielchua/daily-ai-papers` 2025-03-19].
- **Practitioner reception [V].** Willison's 2025 review, under "The year of long tasks":
  - "One of the most interesting recent charts about LLMs ... 2024's best models tapped out at under 30 minutes."
  - "METR conclude that 'the length of tasks AI can do is doubling every 7 months'. I'm not convinced that pattern will continue to hold, but it's an eye-catching way of illustrating current trends in agent capabilities."
- **Export of the unit.**
  - METR's own `cross-domain-horizon` repo ("Estimate the time horizon of AIs over time on various domains like knowledge and vision") [V repo description].
  - AI Digest built an explainer at theaidigest.org/time-horizons [S].
  - Practitioner commentary calls it "The most important chart in AI" [S, LinkedIn post cited in a GitHub reference list; anecdotal].
- **Lesson [I].** One trend line with an intuitive unit (hours of human work) and a memorable rate ("doubles every 7 months") travels further than a table. It also invites extrapolation beyond the evidence (Willison's scepticism). Publish CIs and the fit's assumptions with the chart.

#### 2.8 Story-driven agent evaluations: Vending-Bench, Project Vend, Andon Labs, AI Village

- **Vending-Bench.** Backlund & Petersson (Andon Labs), "Vending-Bench: A Benchmark for Long-Term Coherence of Autonomous Agents", arXiv:2502.15840, published 20 February 2025 [V BibTeX copies; e.g., `usaginoki/mbzuai-master-thesis`].
  - Secondary summaries describe runs of more than 20M tokens.
  - Failure modes: "misinterpreting delivery schedules, forgetting orders, or descending into tangential 'meltdown' loops".
  - The story that spread: Claude 3.5 Sonnet "emailed the FBI about 'cyber financial crimes'" [S, `steel-dev/leaderboard` summary; `tanquangduong` blog summary].
  - Andon Labs' stated design rationale in a podcast [S, benchflow-ai notes on the Latent Space interview]:
    - "money never saturates as a metric ... whereas any percentage caps at 100%";
    - they re-sorted the leaderboard "by *minimum* net worth across 5 runs" to capture tail risk.
- **Lab adoption [V].** Gemini 3 Pro launch table (18 November 2025, as Gemini-generated alt text published by Willison; the $5,478.16 figure is independently corroborated via the Andon Labs leaderboard [corrected by fact-check]): "Vending-Bench 2 (Long-horizon agentic tasks; Net worth (mean), higher is better) Gemini 3 Pro $5,478.16; Gemini 2.5 Pro $573.64; Claude Sonnet 4.5 $3,838.74; GPT-5.1 $1,473.43." Also cited in the GLM-5 technical report's references [S, translated copy].
- **Project Vend (Anthropic + Andon Labs, June 2025) [V, Willison quoting https://www.anthropic.com/research/project-vend-1].**
  - A real office vending business run by "Claudius".
  - "An employee light-heartedly requested a tungsten cube, kicking off a trend of orders for 'specialty metal items'".
  - "Claudius was cajoled via Slack messages into providing numerous discount codes".
  - Anthropic: "we would not hire Claudius."
- **Andon Labs retail and cafe (2026) [V, Willison, 5 May 2026].**
  - An AI-run cafe in Stockholm, whose staff ran a "Hall of Shame" shelf of odd orders (120 eggs with no stove, 6,000 napkins, and so on).
  - Willison's objection: "I don't think it's ethical to run experiments like this that affect real-world systems and steal time from people ... experiments like this need to keep their own human operators in-the-loop for outbound actions that affect other people."
- **AI Village (Sage / AI Digest) [V, Willison, 26 December 2025].**
  - Started April 2025: "We gave four AI agents a computer, a group chat, and an ambitious goal: raise as much money for charity as you can."
  - Runs daily with public replays (for example the "Day 265 replay page").
  - An email credited to "Claude Opus 4.5 AI Village" enraged Rob Pike. The incident was discussed on Hacker News and Lobste.rs.
  - Season 1 raised about $2,000 [S, handbook citing theaidigest.org recap].
- **Lesson [I].**
  - Long-horizon agent evals generate *stories*, and stories are the most shareable output of all.
  - A money unit is intuitive and unbounded, and labs will print it.
  - Real-world side effects convert attention into backlash.
  - A non-game benchmark can keep the narrative channel (transcripts, "hall of shame" galleries) inside a sandbox with simulated counterparties.

#### 2.9 Vibe checks and practitioner evaluation

- **"Vibemarking" named by the press [V, Benj Edwards, Ars Technica, 23 July 2024, quoted by Willison].** "These benchmarks aren't necessarily scientifically sound ... measuring the subjective experience of using a conversational AI model (through what might be called '**vibemarking**') on A/B leaderboards like Chatbot Arena is a better way to judge new LLMs". It links The Markup's "Everyone is judging AI by these tests, but experts say they're close to meaningless" (July 2024).
- **Karpathy on vibes and evals.**
  - August 2024: "The RM [Reward Model] we train for LLMs is just a vibe check ... It's not the 'actual' objective of correctly solving problems, it's a proxy objective of what looks good to humans" [V, source https://twitter.com/karpathy/status/1821277264996352246].
  - 2 March 2025 (X status 1896266683301659068; date from ID decode): "My reaction is that there is an evaluation crisis. I don't really know what metrics to look at right now." The post goes on to say that MMLU "was a good and useful for a few years but that's long over"; that SWE-Bench Verified is "great but itself too narrow"; that labs "started to really overfit" to Chatbot Arena via "prompt mining ... private evals bombardment, and ... explicit use of rankings as training supervision"; and that "an ensemble" of private evals "might be one promising path forward" [S, the same wording in three independent GitHub copies; the vibe-check sentence ("I now fear they are misleading and there is too much opportunity for confirmation bias, too low sample size") appears in one copy only]. Stanford CS336 lecture 12 shows it as "A crisis..." [V].
  - December 2025 year-in-review: "Related to all this is my general apathy and loss of trust in benchmarks in 2025. The core issue is that benchmarks are almost by construction verifiable environments and are therefore immediately susceptible to RLVR ... In the typical benchmaxxing process, teams in LLM labs inevitably construct environments adjacent to little pockets of the embedding space occupied by benchmarks and grow jaggies to cover them. Training on the test set is a new art form." [V, verbatim copy at `nanzhipro/karpathy-wiki/raw/2025/12.20.md`; post URL https://karpathy.bearblog.dev/year-in-review-2025/].
- **Labs run vibe checks [V].** OpenAI's sycophancy postmortem (quoted by Willison, 2 May 2025; source https://openai.com/index/expanding-on-sycophancy/):
  - "internal experts spend significant time interacting with each new model before launch. We informally call these 'vibe checks'".
  - "our offline evaluations ... generally looked good. Similarly, the A/B tests seemed to indicate that the small number of users who tried the model liked it ... Nevertheless, some expert testers had indicated that the model behavior 'felt' slightly off".
  - "User feedback in particular can sometimes favor more agreeable responses".
  - Willison: "yet more evidence that the entire AI industry runs on 'vibes'".
- **Vibes are gameable [V, Thane Ruthenis, LessWrong, March 2025, quoted by Willison].** "'vibe checks' for how smart a model feels are easily gameable by making it have a better personality."
- **Practitioner method [V].**
  - Hamel Husain (March 2024): "unsuccessful products almost always share a common root cause: a failure to create robust evaluation systems".
  - Willison: "I know I need to move beyond 'vibe checks'".
  - Ethan Mollick (December 2024): firms need "internal, validated, firm-specific benchmarks ... No one is going to be doing this for organizations, you need to do it yourself."
  - Andrew Ng (The Batch 297): a good eval ranks A above B whenever "a skilled human judge" does.
  - Willison (24 November 2025): "I've fallen behind on maintaining my own collection of tasks that are just beyond the capabilities of the frontier models ... I frequently advise people to stash away tasks that models fail at ... (a tip I picked up from Ethan Mollick)". He also asks labs for "an example prompt which failed on Sonnet 4.5 but succeeds on Opus 4.5".
  - May 2026 talk: "the supposedly 'best' model (depending mostly on vibes) changed hands five times between the three big providers". This refers to **November 2025**, not the whole six-month period [corrected by fact-check].
- **Academic legitimation [V].**
  - Stanford CS336 lecture 12 ("Evaluation") has a "## Vibes" section (a Demis Hassabis tweet), "A crisis..." (Karpathy), and "Maybe a model is good if people choose to use it (and pay for it)..." (OpenRouter rankings). Its takeaways include "Always look at the individual instances and the predictions."
  - VibeCheck (`lisadunlap/VibeCheck`, "Discover and Quantify Qualitative Differences in Large Language Models") operationalises vibes on Chatbot Arena data [V repo; venue not verified].

**Lesson [I].** Practitioners trust (a) concrete item-level before/after examples, (b) their own private failure stashes, and (c) revealed preference (usage and spend). A benchmark that wants practitioner uptake should publish per-item transcripts and "newly solved / newly broken" diffs per release. It should also let practitioners fork a private variant.

### 3. Academic literature on what makes benchmarks influential

| Work | What it establishes | Tag |
|---|---|---|
| Ott, Barbosa-Silva, Blagec, Brauner & Samwald, "Mapping global dynamics of benchmark creation and saturation in artificial intelligence", *Nature Communications* 13:6793 (2022), doi:10.1038/s41467-022-34591-0, arXiv:2203.04592 | Curated "3765 benchmarks covering the entire domains of computer vision and natural language processing". It found "a large fraction of benchmarks quickly trends towards near-saturation, that many benchmarks fail to find widespread utilization". It "analyze[s] attributes associated with benchmark popularity, and conclude[s] that future benchmarks should emphasize versatility, breadth and real-world utility." | [V abstract, BibTeX copy in `EliasSchlie/thesis/references.bib`] |
| Koch, Denton, Hanna & Foster, "Reduced, Reused and Recycled: The Life of a Dataset in Machine Learning Research", NeurIPS 2021 Datasets & Benchmarks, arXiv:2112.01716 | For 2015-2020: "increasing concentration on fewer and fewer datasets within task communities, significant adoption of datasets from other tasks, and concentration across the field on datasets that have been introduced by researchers situated within a small number of elite institutions." A personal-page listing says it won the D&B best paper award. | [V abstract; award S] |
| Martínez-Plumed, Barredo, Ó hÉigeartaigh & Hernández-Orallo, "Research community dynamics behind popular AI benchmarks", *Nature Machine Intelligence* (2021), doi:10.1038/s42256-021-00339-6 | Analysed "twenty five popular benchmarks in AI from Papers With Code, with around two thousand result entries", linking results to institutions and communities (academia vs. tech giants), "activity, performance jumps and efficiency". | [V repo README `nandomp/AI_Research_Dynamics`] |
| Orr & Kang, "AI as a Sport: On the Competitive Epistemologies of Benchmarking", FAccT 2024, pp. 1875–1884, doi:10.1145/3630106.3659012 | A genealogy of benchmarking via Highleyman's OCR dataset (1960s), the Common Task Framework (1980s), "a state-led project to standardize benchmark datasets as legitimate indicators of technical progress", and "the Netflix Prize which further solidified benchmarking as a competitive goal". | [V abstract, ACM BibTeX copy] |
| Hardt, "The Emerging Science of Machine Learning Benchmarks", *SIAM News*, 1 May 2025 (and book at mlbenchmarks.org) | "Competitive leaderboard climbing has been the main way machine learning advances." "Tech executives now recite their company's number on ... MMLU ... in presentations to shareholders." "model *rankings* — rather than model *evaluations* — are the primary scientific export of machine learning benchmarks." In the LLM era, multitask aggregation is unstable (social-choice trade-offs). | [V, clipped full text in `YuZinyakoff/ai-safety-evals-wiki`] |
| Blum & Hardt, "The Ladder: A Reliable Leaderboard for Machine Learning Competitions", ICML 2015, PMLR 37:1006-1014, arXiv:1502.04585 | Participants who "repeatedly evaluate their submissions on the leaderboard ... may begin to overfit to the holdout data that supports the leaderboard". The paper gives a leaderboard algorithm with guarantees, tested on real Kaggle submissions. | [V abstract, PMLR BibTeX copy] |
| Donoho, "50 Years of Data Science", *J. Computational and Graphical Statistics* 26(4):745–766 (2017), doi:10.1080/10618600.2017.1384734 | The source of the "Common Task Framework" argument: shared tasks with leaderboards as the engine of ML progress. | [bibliographic V; content S via reading notes] |

**Synthesis [I].** The academic record supports two parts of the lead's hypothesis:
- "measurable leaderboard to climb": competitive climbing is the historical engine (Donoho, Orr & Kang, Hardt);
- "real-world utility": Ott et al.'s popularity attributes.

It also warns that attention concentrates on a few benchmarks from elite institutions (Koch et al.). A new entrant needs a distribution strategy, not just quality. And leaderboards invite adaptive overfitting (Blum & Hardt), so hidden holdouts and submission limits are structural requirements.

### 4. Practitioner and newsletter commentary on why evals win or lose trust

Most of this section is [S], from the `rasynai/MarigoldBench` community-discourse compilation. It lists the Interconnects, Zvi, Epoch and SemiAnalysis URLs it read.

- **Nathan Lambert (Interconnects):**
  - "Big Tech's LLM evals are just marketing" (December 2023): "Without any semblance of a fair comparison, the numbers are marketing, not science."
  - "Evaluations: Trust, performance, and price" (March 2024): "Evals are now about trust and performance, whereas previously they were just about performance."
  - "GPT-4o-mini changed ChatBotArena" (July 2024): "No evaluation tool has an infinite lifespan."
  - "Building on evaluation quicksand" (October 2024): labs "hillclimb by focusing on a few key evaluations".
  - [S]
- **Epoch AI (Greg Burnham, August 2026, "9 big questions benchmarks can help answer"):** warns of "benchmaxxing", in which developers "prioritize achieving high benchmark scores even while their models lag at the capabilities those benchmarks are intended to measure". It praises realism-first evals (Andon Labs, Remote Labor Index) [S; tight paraphrase per the compiler].
- **What this community trusts [S, compiler's synthesis]:** "evaluators over benchmarks": neutral institutions (METR, Epoch), disclosed methodology, error bars, holdout governance, ARC-AGI's headroom, and revealed preference (OpenRouter usage).
- **Import AI (Jack Clark) and Dwarkesh Patel.** I could not retrieve an Import AI essay on benchmark influence this session [U]. The Dwarkesh evidence used here is the Zuckerberg interview quote (§2.2) [V].

### 5. Synthesis: attention mechanisms, evidence strength, and failure modes

| Mechanism | Examples | Evidence strength | Documented failure mode when over-used |
|---|---|---|---|
| **Thesis-bearing name** | ARC→ARC-AGI rename; "Humanity's Last Exam"; "pelican riding a bicycle"; "time horizon"; "Vending-Bench" | Rename and title facts [V]; causal effect on attention [U/I] | Over-reading ("AGI"); peer-review venue drops the brand (HLE Nature title) |
| **Human-legible unit** | Human hours (METR); dollars (Vending-Bench); human-relative actions (ARC-AGI-3); Elo (Arena) | [V] definitions; appeal [I, plus Andon's own rationale S] | Extrapolation (METR trend); unit hides variance (Andon switched to the minimum) |
| **Headroom with a human anchor** | ARC "easy for humans"; HLE launched with low scores; METR doubling | [V] | Fast saturation; ARC-AGI-3 99.9% within about 6 months on a custom harness [V via Willison] |
| **Lab-adoption loop** | ARC in 4 labs' model cards; HLE, ARC-AGI-2 and Vending-Bench 2 in the Gemini 3 table; Arena ranks at launch | [V] | Self-reported, incomparable settings; benchmaxxing (Karpathy; Burnham [S]) |
| **Participation with pay-offs** | Free frontier and pre-release access (Arena); prizes and co-authorship (ARC, HLE); human-playable tasks (ARC) | [V] | Style and sycophancy bias; rater quality; vote rigging (see `arenas_preference.md`); label noise (HLE) |
| **Recurring moments** | Release-day pelican; o3 on ARC; mystery models; prize seasons; tournaments | [V] | News-cycle chasing; provider gaming of pre-release testing |
| **Shareable per-item artifacts** | SVGs; apps (WebDev Arena); designs; METR chart | [V] | Aesthetic bias; public items leak into training ("pollute the training set") |
| **Failure stories** | Tungsten cubes; FBI email; AI Village replays; Andon "Hall of Shame" | [V/S] | Real-world harm and backlash (Rob Pike incident) |
| **Cost and efficiency disclosure** | ARC cost per task; "~390X efficiency improvement in one year" | [V] | Harness-specific numbers (ARC-AGI-3 provider harness) |

**Evidence vs. anecdote.**
- **Established by data:**
  - adoption concentrates on few benchmarks (Koch; Ott);
  - Arena and ARC participation counts (organiser-reported);
  - lab launch tables citing ARC-AGI-2, HLE and Vending-Bench 2 (primary text).
- **Established by first-person primary accounts:** the pelican lifecycle, including lab sightings (Willison's own reports, some of lab materials he appeared in).
- **Anecdotal or secondary:**
  - "most important chart" framings;
  - community virality signals (Reddit scores, AINews summaries);
  - podcast rationales (Andon Labs).
- **Missing entirely:** a causal or controlled study of benchmark virality, and systematic citation or traffic data. Semantic Scholar and Google Scholar were blocked, so no citation counts are reported.

---

## Implications for designing a new benchmark

Each lesson is tagged with the evidence it rests on. All are compatible with a non-game design.

**Naming**
1. **Put the thesis in the name.** One noun phrase a journalist can repeat, stating what humans find easy or valuable and AI does not. Precedents: "ARC-AGI" (renamed to carry the thesis), "Humanity's Last Exam", "Vending-Bench" (§2.1, §2.6, §2.8).
2. **Keep a sober subtitle for journals.** HLE appears in *Nature* as "A benchmark of expert-level academic questions to assess AI capabilities". Plan both registers from day one (§2.6).
3. **Avoid generic "X-Bench" names in crowded genres.** `user_failed_a.md` found 173 GitHub repos for "llm game benchmark". Attention concentrates on few benchmarks (Koch et al.).

**Narrative**

4. **Choose a human-legible headline unit.** Examples: minutes or hours of skilled human work, dollars of value, or a percentage relative to a named human baseline. Report the *minimum* or a lower quantile across seeds alongside the mean (Andon Labs' tail-risk argument [S]). Consider an unbounded unit to delay saturation (§2.7, §2.8).
5. **State one falsifiable thesis and a human anchor.** For example: "every item is solved by ≥2 of 3 first-time domain practitioners within X minutes; frontier models solve Y%". ARC's "solved by at least 2 humans in under 2 attempts" is the template (§2.1).
6. **Publish a trend, not only a table.** A single chart of capability over model release date, with CIs, is the most shareable object in the METR case. Also publish the fit assumptions, to avoid extrapolation backlash (§2.7).
7. **Harvest failure stories safely.** Publish transcripts of striking failures (a "hall of shame") from sandboxed, simulated counterparties. Never let agents contact non-consenting people. The AI Village and Andon cafe backlash shows the cost (§2.8).

**Visual and shareable outputs**

8. **Make every item produce an inspectable artifact** (a document, diagram, table, rendered page or chart) that a layperson can judge in seconds. Pair it with an *automatic correctness check*, so the viral image is not the score. WebDev/Design Arena show the appeal; style-bias findings show the risk (§2.3; `arenas_preference.md`).
9. **Release-day diff cards.** For each new model, publish "newly solved / newly failed" items with side-by-side outputs. This is exactly what Willison asked labs for (§2.9), and it recreates the pelican ritual with a validated, rotating item pool.
10. **Keep the public showcase items separate from the scored hidden set.** Rotate them. Public pelican galleries became training-set pollution, and "SVGmaxxing" is undetectable when the task class is public (§2.4).

**Participation**

11. **Offer a "try it yourself" mode.** Humans attempt public items and see how they compare with models and the human baseline (ARC's playable tasks, §2.1). This also builds the human baseline cheaply, with consent.
12. **Pay contributors in credit.** Prizes plus co-authorship produced HLE's items and ARC's 1,400+ teams per year. Budget for multi-stage verification to avoid HLE-style label noise (§2.1, §2.6).
13. **If crowd judgement is used, collect it on *correctness-checkable* dimensions or as expert-stratified votes.** Mass popularity signals reward agreeableness (OpenAI sycophancy postmortem, §2.9).

**Leaderboard design**

14. **One headline ladder with CIs, cost per task, and a "verified vs. self-reported" badge.** ARC Prize Verified appears in lab launch tables. Arena's CI-backed single score won adoption (§2.1, §2.2).
15. **Use a hidden holdout, submission limits, and a public/semi-private overfit check.** ARC flags scores as overfit if semi-private and public differ by more than ±10% [V, 2024 report]. Blum & Hardt's Ladder formalises adaptive-overfitting risk (§3).
16. **Pin the scored artifact to the released artifact** (checkpoint or hash) and pin the harness. Report default-harness and provider-harness numbers separately. This follows the Llama-4-Maverick lesson (`arenas_preference.md`) and ARC-AGI-3's harness gap (§2.1).
17. **Version under a stable brand** (v1 → v2 → v3) when saturation approaches, as ARC did. Pre-commit to retirement rules (§2.1; `knowledge_exams.md`).
18. **Design for practitioner uptake, not just press.**
    - Ship per-item transcripts, a small open "dev" split practitioners can fork into private suites (Mollick and Willison stash advice), and revealed-preference cross-checks such as correlation with usage.
    - Report correlation with Arena and other boards, but do not optimise for it (§2.9).
19. **Plan a lab-adoption path.** Labs print benchmarks that are:
    - (a) hard enough that their gain is visible;
    - (b) run or verified by a neutral party;
    - (c) cheap to reproduce.

    Offer pre-release verification under a published, symmetric policy that allows no best-of-N retraction (§2.1, §2.2).

---

## Claims ledger

| # | Claim | Source URL(s) | Confidence |
|---|---|---|---|
| 1 | Simon Willison created the "Generate an SVG of a pelican riding a bicycle" test on 25 October 2024, initially over 16 models. He chose it partly because he was "pretty sure there aren't any pelican on a bicycle SVG files floating around (yet) that might have already been sucked into the training data." | https://simonwillison.net/2024/Oct/25/pelicans-on-a-bicycle/ ; seen at https://raw.githubusercontent.com/simonw/simonwillisonblog-backup/main/simonwillisonblog/blog_blogmark.ndjson ; https://github.com/simonw/pelican-bicycle | High |
| 2 | Willison reports that the pelican test "ended up a meme in its own right". It appeared in the Google I/O keynote (May 2025), in a GPT-5 launch video (August 2025) and in an Anthropic interpretability paper (October 2025). | https://simonwillison.net/2025/Dec/31/the-year-in-llms/ (blog_entry.ndjson in the backup repo) | High (as his first-person report) |
| 3 | By April and July 2026 Willison judged the pelican test's correlation with model usefulness broken ("even that loose connection to utility has been broken"; "That connection has been mostly severed now"). Its main remaining value is as "a forcing function for actually trying the model". | https://simonwillison.net/2026/Apr/16/qwen-beats-opus/ ; https://simonwillison.net/2026/Jul/16/kimi-k3/ | High |
| 4 | Castillo's "pelicanmaxxing" study generated SVGs from 7 frontier models × 8 animals × 6 vehicles × 3 samples (1,008 SVGs). It reported no statistically significant lab-specific pelican effect, but cannot detect class-level "SVGmaxxing". | https://github.com/dylanjcastillo/blog/tree/main/_extras/pelicanmaxxing (config.py, V) ; https://dylancastillo.co/posts/pelicanmaxxing.html (post source https://raw.githubusercontent.com/dylanjcastillo/blog/main/posts/pelicanmaxxing.qmd, V) | High (design and results) [corrected by fact-check] |
| 5 | ARC was published in 2019 as the Abstraction and Reasoning Corpus and "later renamed ARC-AGI to avoid name collisions". Pre-2024 competitions offered $20K (2020) and $100K (2022, 2023). ARC Prize 2024 offered a $600K grand prize (unclaimed) and drew 1,430 teams with 17,789 entries. SOTA rose from 33% to 55.5%. | arXiv:2412.04604 (https://arxiv.org/abs/2412.04604), verbatim text at https://raw.githubusercontent.com/atimics/crlplrimes/main/paper/sources/text/chollet2024arcprize.txt | High |
| 6 | ARC Prize 2025 drew 1,455 teams and 15,154 entries (top 24% on the ARC-AGI-2 private set) and 90 paper submissions. Four frontier labs (Anthropic, Google DeepMind, OpenAI, xAI) reported ARC-AGI in 2025 model cards. | arXiv:2601.10904 (https://arxiv.org/abs/2601.10904), abstract copy at https://github.com/tiendungchs/PersonalWiki (raw/ARC Prize 2025 Technical Report.md) | Medium-high (verbatim secondary copy of abstract) |
| 7 | On 20 December 2024 ARC Prize reported o3 at 75.7% on ARC-AGI-1 semi-private at the $10K limit and 87.5% at high compute (172x). Chollet noted ARC-AGI-1 "took 4 years to go from 0% with GPT-3 in 2020 to 5% in 2024 with GPT-4o". | https://arcprize.org/blog/oai-o3-pub-breakthrough (quoted in blog_quotation.ndjson of the Willison backup) | High |
| 8 | Chatbot Arena launched in late April 2023 [corrected by fact-check] (first results post 3 May 2023) using Elo "widely-used ... in chess and other competitive games", with 4.7K votes in week one. By April 2025 it reported "3M+ votes, 400+ models, and 300+ pre-release tests", and said the community values "frequent access to the best models, and being a part of the first to access the newest ones". | https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2023-05-03-arena.md ; https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2025-04-27-two-year-celebration.md | High |
| 9 | LMArena's 2025 rebuild aimed to make it "more fun to use". The company raised $100M at $600M (May 2025) and $150M at a $1.7B post-money valuation (January 2026). | https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2025-04-17-new-beta.md (V) ; https://techcrunch.com/2026/01/06/lmarena-lands-1-7b-valuation-four-months-after-launching-its-product/ via https://raw.githubusercontent.com/vibewatch/startup/main/reports/20260625005021-lmarena/evidence.yaml (S) | Fun quote high; funding medium |
| 10 | Google's Gemini 3 Pro launch table (November 2025) reported HLE (37.5% no tools), ARC-AGI-2 (31.1%, "ARC Prize Verified") and Vending-Bench 2 net worth ($5,478.16), alongside other benchmarks. | https://simonwillison.net/2025/Nov/18/gemini-3/ (Gemini-3-generated alt text of Google's table image, published by Willison; figures corroborated by independent copies) | High [corrected by fact-check] |
| 11 | OpenAI's sycophancy postmortem (May 2025) states that internal experts run informal "vibe checks". Offline evals and A/B tests "looked good" while expert testers felt behavior was "off", and "User feedback ... can sometimes favor more agreeable responses". | https://openai.com/index/expanding-on-sycophancy/ (quoted at https://simonwillison.net/2025/May/2/what-we-missed-with-sycophancy/) | High |
| 12 | Karpathy wrote (2 March 2025) "there is an evaluation crisis. I don't really know what metrics to look at right now". In December 2025 he described "general apathy and loss of trust in benchmarks" and wrote "Training on the test set is a new art form." | https://x.com/karpathy/status/1896266683301659068 (S; copies at https://github.com/datawhalechina/diy-llm and https://github.com/whaleybear/swoop-web) ; https://karpathy.bearblog.dev/year-in-review-2025/ (verbatim copy at https://github.com/nanzhipro/karpathy-wiki raw/2025/12.20.md) | March tweet medium; December text high |
| 13 | METR's time-horizon method fits P(success) against log2(human minutes). It reports AI agent time horizons "doubling approximately every 7 months". | https://github.com/METR/eval-analysis-public ; arXiv:2503.14499 | High |
| 14 | Ott et al. (Nature Communications 2022), covering 3,765 benchmarks, found that "many benchmarks fail to find widespread utilization" and recommended "versatility, breadth and real-world utility". Koch et al. (NeurIPS 2021) found usage concentrating on fewer datasets from "a small number of elite institutions". | doi:10.1038/s41467-022-34591-0 ; arXiv:2112.01716 (abstracts via BibTeX copies) | High |
| 15 | Hardt (SIAM News, May 2025): "Competitive leaderboard climbing has been the main way machine learning advances"; rankings are "the primary scientific export of machine learning benchmarks". | https://www.siam.org/publications/siam-news/articles/the-emerging-science-of-machine-learning-benchmarks/ (clipped copy in YuZinyakoff/ai-safety-evals-wiki) | Medium-high |
| 16 | HLE's official citation lists the Nature version as "A benchmark of expert-level academic questions to assess AI capabilities", Nature 649:1139–1146 (2026). The README calls HLE "designed to be the final closed-ended academic benchmark of its kind" with 2,500 questions. | https://github.com/centerforaisafety/hle (citation.txt, README.md) | High |
| 17 | Noam Brown stated that o1's codename "Strawberry does not come from the 'How many r's are in strawberry' meme". Fu et al. (arXiv:2412.18626) found LLMs "capable of recognizing the letters but not counting them". | https://twitter.com/polynoamial/status/1834312400419652079 (via Willison quotation table) ; https://arxiv.org/abs/2412.18626 | High |
| 18 | Kaggle Game Arena launched in early August 2025 with a chess exhibition that featured commentary by Magnus Carlsen and Hikaru Nakamura. It expanded to poker and Werewolf, framed as "soft skills", in February 2026. | AINews 25-08-04 and 26-02-04 (https://github.com/smol-ai/ainews-web-2025) ; https://github.com/google-deepmind/game_arena | Medium (secondary) |
| 19 | Design Arena is a YC Summer 2025 company with industry "Consumer" and the one-liner "World's largest crowdsourced benchmark for AI-generated design". | https://raw.githubusercontent.com/yc-oss/api/main/batches/summer-2025/design-arena.json | High |

---

## References

Only sources seen this session. **SU** = seen URL (where I read it).

1. Willison, S. (2024-10-25). "Pelicans on a bicycle" (link post). https://simonwillison.net/2024/Oct/25/pelicans-on-a-bicycle/ — SU: `simonw/simonwillisonblog-backup` blog_blogmark.ndjson.
2. Willison, S. `simonw/pelican-bicycle` README. https://github.com/simonw/pelican-bicycle — SU: raw README.
3. Willison, S. (2025-06-06). "The last six months in LLMs, illustrated by pelicans on bicycles." https://simonwillison.net/2025/Jun/6/six-months-in-llms/ — SU: backup blog_entry.ndjson.
4. Willison, S. (2025-11-13). "What happens if AI labs train for pelicans riding bicycles?" https://simonwillison.net/2025/Nov/13/training-for-pelicans-riding-bicycles/ — SU: backup.
5. Willison, S. (2025-12-31). "2025: The year in LLMs." https://simonwillison.net/2025/Dec/31/the-year-in-llms/ — SU: backup.
6. Willison, S. (2026-04-16). "Qwen3.6-35B-A3B on my laptop drew me a better pelican than Claude Opus 4.7." https://simonwillison.net/2026/Apr/16/qwen-beats-opus/ — SU: backup.
7. Willison, S. (2026-07-16). "Kimi K3, and what we can still learn from the pelican benchmark." https://simonwillison.net/2026/Jul/16/kimi-k3/ — SU: backup.
8. Castillo, D. (2026-07-18). "Are AI labs pelicanmaxxing?" https://dylancastillo.co/posts/pelicanmaxxing.html ; code https://github.com/dylanjcastillo/blog/tree/main/_extras/pelicanmaxxing — SU: config.py/README and post source `posts/pelicanmaxxing.qmd` (raw GitHub) [corrected by fact-check].
9. Willison, S. (2025-02-18). "Andrej Karpathy's initial impressions of Grok 3." https://simonwillison.net/2025/Feb/18/andrej-karpathy-grok-3/ — SU: backup.
10. Willison, S. (2025-04-30). "Understanding the recent criticism of the Chatbot Arena." https://simonwillison.net/2025/Apr/30/criticism-of-the-chatbot-arena/ — SU: backup.
11. Willison, S. (2025-11-24). "Claude Opus 4.5, and why evaluating new LLMs is increasingly difficult." https://simonwillison.net/2025/Nov/24/claude-opus/ — SU: backup.
12. Willison, S. (2025-11-18). "Trying out Gemini 3 Pro with audio transcription and a new pelican benchmark." https://simonwillison.net/2025/Nov/18/gemini-3/ — SU: backup.
13. OpenAI (2025-05). "Expanding on what we missed with sycophancy." https://openai.com/index/expanding-on-sycophancy/ — SU: quoted in Willison link post (backup).
14. Willison, S. (2025-12-26). "How Rob Pike got spammed with an AI slop 'act of kindness'." https://simonwillison.net/2025/Dec/26/slop-acts-of-kindness/ — SU: backup.
15. Anthropic (2025-06). "Project Vend: Can Claude run a small shop?" https://www.anthropic.com/research/project-vend-1 — SU: quoted in Willison link post (backup).
16. Chollet, F., Knoop, M., Kamradt, G., Landers, B. (2025). "ARC Prize 2024: Technical Report." arXiv:2412.04604 — SU: verbatim text in `atimics/crlplrimes`.
17. Chollet, F., Knoop, M., Kamradt, G., Landers, B. (2026). "ARC Prize 2025: Technical Report." arXiv:2601.10904 [corrected by fact-check] — SU: abstract copy in `tiendungchs/PersonalWiki`; full text in `UNIR-TUC/arc-agi`.
18. Chollet, F. (2024-12-20). "OpenAI o3 breakthrough high score on ARC-AGI-Pub." https://arcprize.org/blog/oai-o3-pub-breakthrough — SU: Willison quotation table.
19. Kamradt, G. (2025-03-25). "Announcing ARC-AGI-2 and ARC Prize 2025." https://arcprize.org/blog/announcing-arc-agi-2-and-arc-prize-2025 — SU: Willison quotation table.
20. ARC Prize. ARC-AGI-3 documentation (methodology, quickstart, ARC Prize 2026). https://github.com/arcprize/docs — SU: raw GitHub.
21. Zheng, L., Sheng, Y., Chiang, W.-L., Zhang, H., Gonzalez, J. E., Stoica, I. (2023-05-03). "Chatbot Arena: Benchmarking LLMs in the Wild with Elo Ratings." LMSYS blog — SU: `lmarena/lmarena.github.io/_posts/2023-05-03-arena.md`.
22. LMArena (2025-04-17). "LMArena is Growing to Support our Community Platform." — SU: `_posts/2025-04-17-new-beta.md`.
23. LMArena (2025-04-27). "Celebrating Community Impact: 3M+ votes, 400+ models, and 300+ pre-release tests." — SU: `_posts/2025-04-27-two-year-celebration.md`.
24. TechCrunch (2026-01-06). "LMArena lands $1.7B valuation four months after launching its product." https://techcrunch.com/2026/01/06/lmarena-lands-1-7b-valuation-four-months-after-launching-its-product/ — SU: `vibewatch/startup` evidence.yaml [S].
25. Y Combinator company record: Design Arena (Summer 2025). https://www.ycombinator.com/companies/design-arena — SU: `yc-oss/api` mirror.
26. Center for AI Safety, Scale AI, HLE Contributors Consortium (2026). "A benchmark of expert-level academic questions to assess AI capabilities." *Nature* 649:1139–1146. doi:10.1038/s41586-025-09962-4; arXiv:2501.14249 — SU: `centerforaisafety/hle` citation.txt and README.
27. Kwa, T., West, B., Becker, J., Deng, A., Garcia, K., Hasin, M., Jawhar, S., Kinniment, M., et al. (2025) [corrected by fact-check]. "Measuring AI Ability to Complete Long Tasks." arXiv:2503.14499 — SU: `METR/eval-analysis-public` README; BibTeX in `natolambert/rlhf-book`.
28. Backlund, A., Petersson, L. (2025). "Vending-Bench: A Benchmark for Long-Term Coherence of Autonomous Agents." arXiv:2502.15840 — SU: BibTeX/notes in multiple GitHub repos (e.g., `usaginoki/mbzuai-master-thesis`).
29. Google DeepMind. `game_arena` harness. https://github.com/google-deepmind/game_arena — SU: raw README; launch coverage via AINews [S].
30. smol-ai. AINews archive (issues 25-08-04, 25-08-05, 25-08-08, 26-02-04, 26-06-16, 26-07-15, 26-08-03). https://github.com/smol-ai/ainews-web-2025 — [S].
31. Karpathy, A. (2025-03-02). "Evaluation crisis" post. https://x.com/karpathy/status/1896266683301659068 — SU: secondary copies (datawhalechina/diy-llm; whaleybear/swoop-web; mariozupan/llm-evaluation-framework) [S].
32. Karpathy, A. (2025-12). "2025 LLM Year in Review." https://karpathy.bearblog.dev/year-in-review-2025/ — SU: verbatim copy `nanzhipro/karpathy-wiki/raw/2025/12.20.md`.
33. Stanford CS336 course staff (2025). CS336 Spring 2025, Lecture 12: Evaluation (lecturer names not verified this session). https://github.com/stanford-cs336/spring2025-lectures — SU: lecture_12.py.
34. Ott, S., Barbosa-Silva, A., Blagec, K., Brauner, J., Samwald, M. (2022). "Mapping global dynamics of benchmark creation and saturation in artificial intelligence." *Nature Communications* 13:6793. doi:10.1038/s41467-022-34591-0; arXiv:2203.04592 — SU: BibTeX abstract in `EliasSchlie/thesis`.
35. Koch, B., Denton, E., Hanna, A., Foster, J. G. (2021). "Reduced, Reused and Recycled: The Life of a Dataset in Machine Learning Research." NeurIPS 2021 Datasets & Benchmarks. arXiv:2112.01716 — SU: abstract in `mavenlin/ai_research_trends`.
36. Martínez-Plumed, F., Barredo, P., Ó hÉigeartaigh, S., Hernández-Orallo, J. (2021). "Research community dynamics behind popular AI benchmarks." *Nature Machine Intelligence* 3(7):581–589 [corrected by fact-check]. doi:10.1038/s42256-021-00339-6 — SU: `nandomp/AI_Research_Dynamics` README.
37. Orr, W., Kang, E. B. (2024). "AI as a Sport: On the Competitive Epistemologies of Benchmarking." FAccT 2024, 1875–1884. doi:10.1145/3630106.3659012 — SU: ACM BibTeX with abstract in `nestorcastelblanco/Bibliometria_AA`.
38. Hardt, M. (2025-05-01). "The Emerging Science of Machine Learning Benchmarks." *SIAM News*. https://www.siam.org/publications/siam-news/articles/the-emerging-science-of-machine-learning-benchmarks/ — SU: clipped text in `YuZinyakoff/ai-safety-evals-wiki`.
39. Blum, A., Hardt, M. (2015). "The Ladder: A Reliable Leaderboard for Machine Learning Competitions." ICML 2015, PMLR 37:1006–1014. arXiv:1502.04585 — SU: PMLR BibTeX in `mreid/papersite`.
40. Donoho, D. (2017). "50 Years of Data Science." *JCGS* 26(4):745–766. doi:10.1080/10618600.2017.1384734 — SU: bibliographic references in `marketneutral/hedge_fund_evolution`, `By-Xin/ByCsdiy`.
41. Fu, T., Ferrando, R., Conde, J., Arriaga, C., Reviriego, P. (2024). "Why Do Large Language Models (LLMs) Struggle to Count Letters?" arXiv:2412.18626 — SU: arXiv metadata in `MystenLabs/snowreads`.
42. Brown, N. (2024-09-12). Post on the "Strawberry" codename. https://twitter.com/polynoamial/status/1834312400419652079 — SU: Willison quotation table.
43. Edwards, B. (2024-07-23). Ars Technica on "vibemarking". https://arstechnica.com/information-technology/2024/07/the-first-gpt-4-class-ai-model-anyone-can-download-has-arrived-llama-405b/ — SU: Willison quotation table.
44. Ruthenis, T. (2025-03). "A Bear Case: My Predictions Regarding AI Progress." LessWrong. https://www.lesswrong.com/posts/oKAFFvaouKKEhbBPm/a-bear-case-my-predictions-regarding-ai-progress — SU: Willison quotation table.
45. Husain, H. (2024-03). "Your AI Product Needs Evals." https://hamel.dev/blog/posts/evals/ — SU: Willison link post.
46. Zuckerberg, M., on Dwarkesh Podcast (2025-04/05). https://www.dwarkesh.com/p/mark-zuckerberg-2 — SU: Willison quotation table.
47. Dunlap, L., et al. VibeCheck: Discover and Quantify Qualitative Differences in LLMs. https://github.com/lisadunlap/VibeCheck — SU: README. Venue and ID not verified.
48. rasynai. MarigoldBench community-discourse analysis (Interconnects, Zvi, Epoch, SemiAnalysis quotes). https://github.com/rasynai/MarigoldBench/tree/main/analysis/community — [S].
49. benchflow-ai. awesome-evals notes on Andon Labs (Latent Space interview). https://github.com/benchflow-ai/awesome-evals — [S].

---

## Verification log

Adversarial fact-check run on 2026-09-29 by a separate subagent.

**Method.**
- WebSearch was unavailable: the session's 200-call budget was already exhausted, and every query was refused.
- Independent checks therefore used:
  - fresh fetches of primary files from raw.githubusercontent.com: the Willison blog backup ndjson (entries, link posts, quotations and tag tables), the LMArena post sources, the HLE citation and README, the METR README, the ARC-AGI-3 docs, the YC record, and the pelicanmaxxing config and post source;
  - GitHub code search for independent copies of paper abstracts, BibTeX and news digests;
  - decoding tweet snowflake IDs to dates.
- Domains blocked for fetching: x.com, techcrunch.com, dylancastillo.co, arxiv.org, openai.com and arcprize.org.
- "Independent" below means a copy in a repository other than the one the dossier cited.

### Load-bearing claims

| ID | Verdict | Evidence | Sources checked |
|---|---|---|---|
| C1: pelican test created 25 Oct 2024, 16 models, training-data rationale | **Confirmed** | See note C1 | backup `blog_blogmark.ndjson`; `simonw/pelican-bicycle` README |
| C2: meme; Google I/O (May 2025), GPT-5 video (Aug 2025), Anthropic paper (Oct 2025); link to usefulness severed (Apr/Jul 2026) | **Confirmed** | See note C2 | backup `blog_entry.ndjson` entries `the-year-in-llms`, `six-months-in-llms`, `qwen-beats-opus`, `kimi-k3` |
| C3: Castillo 7×8×6×3 = 1,008 SVGs; no significant lab-specific pelican effect; cannot detect SVGmaxxing | **Confirmed** (upgraded from S to V) | See note C3 | https://raw.githubusercontent.com/dylanjcastillo/blog/main/posts/pelicanmaxxing.qmd ; `_extras/pelicanmaxxing/config.py`; backup blogmark `are-ai-labs-pelicanmaxxing` |
| C4: ARC 2019 / rename; $20K (2020), $100K (2022, 2023); $600K unclaimed; 1,430 teams / 17,789 entries; 33% → 55.5% | **Confirmed** | See note C4 | `atimics/crlplrimes` text; `UNIR-TUC/arc-agi` `2412.04604v2_arc_prize_2024.md`; GitHub code search (5 repos with the exact sentence) |
| C5: ARC Prize 2025: 1,455 teams, 15,154 entries, 24%, 90 papers, four labs' model cards | **Confirmed** (author metadata corrected) | See note C5 | `UNIR-TUC/arc-agi` `2601.10904v1_arc_prize_2025.md`; code search (69 hits for "1,455 teams" + "15,154 entries") |
| C6: o3 75.7% at $10K limit, 87.5% at 172×; "4 years to go from 0% ... to 5%" | **Confirmed** | See note C6 | backup `blog_quotation.ndjson` (francois-chollet), blogmark `openai-o3-breakthrough` |
| C7: Arena launch with chess Elo, 4.7K votes in first week; 3M+ votes / 400+ models / 300+ pre-release tests; access motive; "more fun to use" | **Corrected** (launch month) | See note C7 | three `lmarena.github.io/_posts` files (fetched); code search (turbobeest/modelspec, WSJ summary in panaversity/learn-agentic-ai) |
| C8: $100M at $600M (May 2025); $150M Series A at $1.7B post-money (Jan 2026) | **Confirmed** (secondary only) | See note C8 | `guzus/ai-research-arm` 2026-01-17 and 2026-01-20; `sivadotblog/tldr` 2026-01-07; `GaloisField2718/tldr_news`; `vibewatch/startup` evidence.yaml |
| C9: Gemini 3 Pro table: HLE 37.5% (no tools), ARC-AGI-2 31.1% ("ARC Prize Verified"), Vending-Bench 2 $5,478.16 | **Confirmed**, with a provenance correction | See note C9 | backup entry `gemini-3`; code search (`duclm1x1/Dive-Ai`, `jjxxmiin.github.io`, `redstone-solution-ou/llm-frontier-wiki`) |
| C10: OpenAI sycophancy postmortem: "vibe checks"; offline evals and A/B "looked good"; experts felt it "off"; user feedback favours agreeable responses | **Confirmed** (via verbatim secondary quotation) | See note C10 | backup blogmark `what-we-missed-with-sycophancy` |
| C11: Karpathy 2 Mar 2025 "evaluation crisis"; Dec 2025 "general apathy and loss of trust in benchmarks", "Training on the test set is a new art form" | **Confirmed** (March tweet via secondary copies only) | See note C11 | `rasynai/MarigoldBench` twitter-x.md; `stanford-cs336/spring2025-lectures/lecture_12.py`; `nanzhipro/karpathy-wiki` raw/2025/12.20.md; code search |
| C12: METR fits P(success) vs log2(human minutes); doubling roughly every 7 months | **Confirmed** (author list corrected) | See note C12 | https://raw.githubusercontent.com/METR/eval-analysis-public/main/README.md ; arXiv abstract copies found by code search |
| C13: Ott et al. 3,765 benchmarks, "fail to find widespread utilization", "versatility, breadth and real-world utility"; Koch et al. "small number of elite institutions" | **Confirmed** | See note C13 | `EliasSchlie/thesis/references.bib`; `mavenlin/ai_research_trends` `_posts/2021-12-03`; `TTXS123OK/CVPapers`; `OpenBioLink/ITO` |
| C14: HLE Nature title, 649:1139–1146 (2026); README "final closed-ended academic benchmark of its kind", 2,500 questions | **Confirmed** | See note C14 | `centerforaisafety/hle` `citation.txt` and README (fetched); code search for `s41586-025-09962-4` (263 hits) |

**Notes on the evidence.**

- **C1.** The link post is dated 2024-10-25T23:56:50Z. Its text reads "I've run it through 16 models so far" and "pretty sure there aren't any pelican on a bicycle SVG files floating around (yet) that might have already been sucked into the training data". The prompt appears verbatim in the repo README.
- **C2.**
  - The quotes are verbatim in the 2025-12-31 year review: "It's ended up a meme in its own right"; "It showed up (for a split second) in the Google I/O keynote in May, got a mention in an Anthropic interpretability research paper in October and I got to talk about it in a GPT-5 launch video filmed at OpenAI HQ in August".
  - 2026-04-16: "even that loose connection to utility has been broken". 2026-07-16: "That connection has been mostly severed now".
  - Minor inconsistency in the source: the year review places the AI Engineer World's Fair keynote "in July", but the keynote post is dated 2025-06-06. The dossier's June date is right.
  - All sightings are Willison's first-person reports. The Google, OpenAI and Anthropic materials themselves were not inspected.
- **C3.**
  - The post source (front matter date 07/18/2026) says: "I generated 1,008 SVGs across seven frontier models"; "The pelican is 6th of 8"; "#42 of 48"; "none comes close to significance (smallest p = 0.25)"; "SVGmaxxing ... This experiment can't detect that."
  - `config.py` has 7 models, 8 animals, 6 vehicles and `N_SAMPLES = 3`.
  - Caveats in the study: a single LLM judge (GPT-5.6 Luna), from the same family as one contestant. The README mentions "two judges from different labs", but `config.py` lists one judge.
- **C4.** Two independent full-text copies agree on:
  - "(later renamed ARC-AGI to avoid name collisions with other AI benchmarks)";
  - "2020 ... ($20,000 USD in prizes)", "2022: ARCathon 1 ($100,000 in prizes)", "2023: ARCathon 2 ($100,000 in prizes)";
  - "Grand Prize of $600,000 ... The Grand Prize was not claimed";
  - "In total, 1,430 teams submitted 17,789 entries";
  - "increased from 33% to 55.5%".

  The 55.5% was MindsAI's score, which was ineligible for a prize; the ARChitects won with 53.5%.
- **C5.**
  - The abstract is verbatim in an independent full-text copy.
  - Correction to the reference: the authors are François Chollet, Mike Knoop, Gregory Kamradt and Bryan Landers (not "ARC Prize Foundation, author list not verified"). The report is dated 19 January 2026.
  - "Four frontier labs reported ARC-AGI in model cards" is the organisers' own claim.
- **C6.**
  - The quotation-table text matches the claim verbatim.
  - Context: the "0% → 5%" line refers to GPT-family LLMs. The same 2024 report gives a 2020 Kaggle top score of 20%, so ARC-AGI-1 was not at 0% overall in 2020.
  - Willison's $6,677 figure was for o3 on the 400 *public* tasks (82.8%). His $1.1M high-compute estimate is his extrapolation, as the dossier says.
- **C7.**
  - Confirmed: "Elo rating system, which is a widely-used rating system in chess and other competitive games"; "collected 4.7k valid anonymous votes"; the April 2025 figures and motive quote; "more fun to use" (17 April 2025).
  - **Correction:** the arena launched in late April 2023, not May. The 3 May 2023 post says "The arena was launched about one week ago", and secondary sources say "launched in April 2023". The first leaderboard and blog post were May 2023.
  - "3M+ votes" appears in the post title; the body gives "Tens of millions of battle pairings".
- **C8.**
  - TechCrunch is blocked. Several independent digests agree: "$150 million Series A at $1.7 billion post-money valuation", led by Felicis and UC Investments, on 6 January 2026.
  - Sherwood (via the TLDR AI archive) reports "raised $250 million in the last seven months", which is consistent with $100M + $150M.
  - The $600M valuation of the May 2025 seed is stated in the `guzus` digest and the vibewatch file.
  - Confidence is medium-high; there is no primary source.
- **C9.**
  - The figures are right: HLE 37.5% / 45.8%; ARC-AGI-2 31.1% (Deep Think 45.1%); GPQA 91.9%; Vending-Bench 2 $5,478.16, also on the Andon Labs leaderboard per `redstone-solution-ou/llm-frontier-wiki`.
  - **Provenance correction:** the "Willison transcription" is alt text that Gemini 3 Pro generated from a screenshot of Google's table ("I fed it that image URL and asked it to generate alt text"). Willison published it; he did not transcribe it. Inline labels are fixed.
- **C10.**
  - Verbatim in Willison's quote block: "We informally call these 'vibe checks'"; "our offline evaluations—especially those testing behavior—generally looked good. Similarly, the A/B tests seemed to indicate that the small number of users who tried the model liked it. [...] some expert testers had indicated that the model behavior 'felt' slightly off"; "User feedback in particular can sometimes favor more agreeable responses".
  - openai.com was not fetched.
  - Wording fix in the Summary: the "agreeable responses" line is about user thumbs feedback, not A/B tests.
- **C11.**
  - The March wording is consistent across independent copies. Status 1896266683301659068 decodes to 2025-03-02 18:29 UTC, consistent with GPT-4.5 release reactions. x.com was not fetched.
  - The December passage is verbatim in `nanzhipro/karpathy-wiki`, and the phrase appears in 22 GitHub files, including `Proteusiq/unthinking`, which links karpathy.bearblog.dev/year-in-review-2025/.
- **C12.**
  - README: "Fitting a logistic curve modeling P(success) as a function of log2(human_minutes)"; "AI agent time horizons have been doubling approximately every 7 months". The arXiv abstract says "approximately every seven months since 2019".
  - **Correction to the author list:** Kwa, West, Becker, Deng, Garcia, Hasin, Jawhar, Kinniment, ... (25 authors). Kinniment is 8th, not 6th. The repo BibTeX lists the author as "METR".
- **C13.**
  - Ott et al.: abstract verbatim in the BibTeX; Nat Commun 13:6793; arXiv:2203.04592 confirmed via the authors' group repo `OpenBioLink/ITO`.
  - Koch et al.: abstract verbatim ("concentration across the field on datasets that have been introduced by researchers situated within a small number of elite institutions"). One secondary source says it won a NeurIPS 2021 outstanding D&B paper award.
- **C14.**
  - `citation.txt`: `title = {A benchmark of expert-level academic questions to assess {AI} capabilities}`, Nature 649, 1139--1146, 2026.
  - README: "designed to be the final closed-ended academic benchmark of its kind ... 2,500 questions".
  - Independent BibTeX copies add issue 8099.

### Other statements checked in passing

- **"Changed hands five times" (§2.9). Corrected.** The May 2026 talk says this happened in **November 2025**, not across six months.
- **Pelican tag counts. Confirmed.** Tag id 5802 in the backup gives 42 entries and 92 joined link posts (93 raw tag rows).
- **ARC-AGI-3 99.9% for $19K via the "Provider Adapter harness", vs 62.7% for $26K on the default harness. Confirmed as reported** in Willison's blogmark `gpt6-astra` (2026-09-03), which quotes arcprize.org/blog/astra. The ARC page was not fetched.
- **`gpt2-chatbot` confirmed as OpenAI's. Confirmed** (backup blogmark `gpt2-chatbot-confirmed-as-openai`).
- **Stockholm cafe (Andon Labs, 5 May 2026) and "Hall of Shame" items. Confirmed** (blogmark `our-ai-started-a-cafe-in-stockholm`).
- **Direct quotes confirmed verbatim in the backup:**
  - Zuckerberg: "LM Arena stuff" (Dwarkesh);
  - Kamradt: "opposite design choice";
  - Ruthenis: "easily gameable";
  - Edwards: "vibemarking";
  - Noam Brown: Strawberry denial (status ID decodes to 2024-09-12);
  - Karpathy: "RM ... just a vibe check" (status ID decodes to 2024-08-07);
  - Mollick, Husain, Ng;
  - the Project Vend quotes;
  - the AI Village quotes;
  - ARC's "~390X efficiency" (GPT-5.2 entry, 2025-12-11);
  - GPT-5.2 at 52.9% on ARC-AGI-2.
- **ARC ±10% overfit rule and "no deep-learning based approach scored above 1%" (2020). Confirmed** in the 2024 report text.
- **ARC-AGI-3 RHAE. Confirmed** from `arcprize/docs/methodology.mdx`:
  - `(human_baseline_actions / ai_actions) ^ 2`;
  - a 1.15 cap per level;
  - an upper-median first-time-human baseline;
  - weighting by level number.
- **Hardt SIAM News quotes. Confirmed** in the clipped text (published 2025-05-01).
- **Design Arena YC record. Confirmed** (launched_at = 2025-07-30).
- **Clarification to §2.3.** Willison's "now a commodity" line refers to prompt-driven app building, with WebDev Arena as his evidence.
- **Not re-verified (search budget exhausted and domains blocked):**
  - Kaggle Game Arena launch details (Carlsen/Nakamura commentary, 8 models, dates);
  - Design Arena launch-day placements (GLM-5.2 #1, Elo 1360);
  - Andon Labs podcast rationale;
  - "most important chart" framings;
  - the AI Village Season 1 total.

  All of these stay [S] as the dossier already labels them.

### Reference-check summary

- **Checked:** all 40 entries in `refs/virality_consumer.json`, none skipped. Each now has `verified` and `verify_note` fields.
- **Verified:** 40 of 40. Each work exists with the stated title, venue and year, or is a blog/web page confirmed through a verbatim copy.
  - For 7 entries the verification is through secondary verbatim copies only, because the primary domain was blocked:
    - OpenAI sycophancy post;
    - Project Vend;
    - ARC o3 blog;
    - ARC-AGI-2 announcement;
    - TechCrunch;
    - Karpathy's March 2025 tweet;
    - Ars Technica.
- **Corrected entries:**
  1. `arcprize2026report2025`: authors were "ARC Prize Foundation (author list not verified)". They are Chollet, Knoop, Kamradt and Landers.
  2. `kwa2025metr`: author order was wrong (Kinniment listed 6th). Replaced with the full 25-author list.
  3. `martinezplumed2021dynamics`: added volume, issue and pages 3(7):581–589.
  4. `castillo2026pelicanmaxxing`: `seen_url` now points to the primary post source. Results are verified there, and the post is dated 18 July 2026.
- **Residual caveats:**
  - `blum2015ladder`: arXiv:1502.04585 was not re-checked; GitHub search was rate-limited.
  - `karpathy2025review`: exact title not confirmed.
  - `chollet2025arcprize2024`: dated 2025 (v2); v1 is December 2024.
- **Fabricated or garbled references found:** none.

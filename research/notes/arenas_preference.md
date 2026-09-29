# Arena and Human/LLM-Preference Benchmarks (Chatbot Arena/LMArena/Arena, WebDev/Code, Copilot, Search, Design Arena, MT-Bench, AlpacaEval, Arena-Hard, WildBench)

Research dossier for the benchmark-landscape survey (Phase 1). Compiled 2026-09-29.

**How this was researched.** The session's WebSearch budget was exhausted before this subagent started, so every search call was refused. arxiv.org, huggingface.co, openreview.net, news sites and the Hacker News API were also unreachable. All evidence therefore came from GitHub:

- Raw files fetched with `curl` from raw.githubusercontent.com:
  - the full source of the LMArena blog (`lmarena/lmarena.github.io/_posts/*.md`), which is the primary text of the official blog posts;
  - official benchmark READMEs (FastChat, llm_judge, arena-hard-auto, alpaca_eval, WildBench, copilot-arena, search-arena, arena-rank, p2l, Cheating-LLM-Benchmarks, Rigging-ChatbotArena, sos-bench, human-feedback-paper);
  - PMLR proceedings records (`mlresearch/v235`, `mlresearch/v267`), which carry verbatim abstracts, authors and pages;
  - a cached arXiv API record of arXiv:2504.20879;
  - the AlpacaEval 2 leaderboard CSV;
  - DeepSeek-V3 and DeepSeek-R1 READMEs.
- GitHub code search, which surfaced cached news items and third-party evidence files. Those are labelled secondary.

**Evidence tags used throughout:**

| Tag | Meaning |
|---|---|
| **[V]** | Verified this session from a primary source (paper record, official repo or official blog source) |
| **[S]** | Seen only in a secondary source (news cache, newsletter, third-party compiled evidence file, awesome-list). The original URL is given, but I did not fetch it |
| **[I]** | My interpretation |
| **[U]** | Unverified |

Citation counts could not be retrieved (Semantic Scholar and Google Scholar are blocked) and are omitted.

---

## Summary

1. **Chatbot Arena won the most important adoption race among LLM evaluations of 2023-2026.** It was later renamed LMArena and then "Arena" (arena.ai), rebranded in January 2026 [S].
   - It launched in May 2023 as a Berkeley/LMSYS research demo [V].
   - It spun out as a company in April 2025 [V].
   - It raised a $100M seed at a $600M valuation (May 2025) [S], then a $150M Series A at a $1.7B post-money valuation (January 2026) [S].
   - By January 2026 its annualized "consumption run rate" from a paid evaluation product exceeded $30M [S].
   - Vote volume grew from ~240K votes (ICML 2024 paper) [V] to "3M+" (April 2025) [V]. The company later claimed "50 million votes" (January 2026) [S]. That figure conflicts with another secondary count of ~5.4M (March 2026) [S], so treat platform-wide totals as company claims. [corrected by fact-check] The Series A blog text (scraped copy, Amal-David/docingest, 2026-01-18) says the 50 million votes came "in a matter of months" after the May 2025 seed and were cast "across text, vision, web dev, search, video and image modalities". The two figures therefore probably measure different scopes (all modalities since May 2025 vs. a text-only count) and are not directly comparable [I].
   - Frontier labs routinely announce Arena ranks at launch, including Meta (Llama 4), Google (Gemini 3 at 1501, November 2025) and many 2026 releases [S].
2. **Why it succeeded [I, backed by V/S evidence below]:**
   - open-ended, real user prompts;
   - no fixed test set to leak, with ~75% of each day's prompts "fresh" [V];
   - a single comparable number (a Bradley-Terry "Arena Score" with CIs) [V];
   - continuous refresh as new models are added within days;
   - a consumer incentive loop: free, anonymous access to frontier models, with voting as the price of admission [V];
   - openness: code, 1.5M+ prompts and vote data released [V];
   - vendor buy-in through pre-release anonymous testing [V];
   - a spin-off ladder of domain arenas (Vision, WebDev/Code, Search, Copilot, Agent, image/video).
3. **Its failure modes are now well documented:**
   - **Style bias.** Length is the dominant style factor, and positive sentiment also raises scores [V]. [corrected by fact-check] The earlier text said emoji also raise scores. In the sentiment-control post, the emoji-count coefficient is slightly *negative* (-0.0039 in the full model, -0.0048 in the ablation), so emoji use did not raise scores.
   - **Human-rater limits.** Surge AI disagreed with 52% of 500 audited votes [S]. Assertiveness skews perceived factuality [V].
   - **Gaming by providers.**
     - Meta shipped an Arena-optimised "Llama-4-Maverick-03-26-Experimental". It ranked #2, while the public release ranked 32nd [S].
     - Best-of-N private testing: 27 private Meta variants before Llama 4 [V abstract].
   - **Data-access asymmetry.** Google and OpenAI each received about 20% of all arena data, versus 29.7% for 83 open-weight models combined [V abstract].
   - **Vote rigging.** Hundreds of votes can move ranks [V]. Model identity can be de-anonymised with >95% accuracy [V].
   - **Silent deprecations, and arena-data overfitting that does not transfer** [S].
   - **Conflict of interest** once the platform sells evaluation services to the labs it ranks [S].
   - LMArena contested several of these numbers [V]. It also adopted reforms: pre-release variants disclosed as allowed, "provisional" labels, a public retirement list, and release of 100% of leaderboard vote data from 1 July 2025 [V].
4. **LLM-judge proxies of the arena, and why most had short lives.** MT-Bench, AlpacaEval (2.0 LC), Arena-Hard-Auto and WildBench were built to approximate Arena cheaply.
   - Each achieved high correlation with Arena rankings at launch:
     - AlpacaEval LC: Spearman 0.98 [V];
     - Arena-Hard: 89.1% agreement / 98.6% correlation [V];
     - WildBench: Pearson 0.98 [S].
   - Each then failed on one or more of:
     - saturation: MT-Bench separability fell to 22.6% [V]; DeepSeek-R1 reported AlpacaEval-LC 87.6 and Arena-Hard 92.3 [V];
     - gaming: a constant "null model" reached an 86.5% LC win rate on AlpacaEval 2.0 [V]; 9B fine-tunes top the AlpacaEval board [V];
     - judge bias: on Arena-Hard v2, Gemini-2.5 scores 79.0 with a Gemini judge but 49.1 with a GPT-4.1 judge [V];
     - staleness: the AlpacaEval and WildBench leaderboards stopped adding frontier models around mid-2024 [V].
5. **Design Arena (designarena.ai)** is the most successful non-LMArena arena. It is a YC Summer-2025 startup ("World's largest crowdsourced benchmark for AI-generated design") [S] with a tournament-style multi-model Bradley-Terry protocol and per-category boards [S]. By mid-2026 labs cited it in release notes (Thinking Machines "Inkling" at 1257 on Agentic Web Dev; GLM-5.2 "#1 on Design Arena") [S].
6. **Bottom line for our project [I].** The arena recipe works as a distribution and engagement machine. It is not a validity guarantee. A new non-game benchmark should keep:
   - fresh, real prompts;
   - one comparable rating with CIs;
   - a consumer-facing loop;
   - open data.

   It should also design out the arena's failure modes:
   - separate substance from style, with verifiable, checkable outcomes instead of raw "which do you like";
   - a pre-registered submission policy: no private best-of-N, and scored artifact = shipped artifact;
   - rater quality control or expert strata;
   - anti-rigging defences;
   - an independent governance and funding model.

---

## Benchmark-by-benchmark

### 1. Chatbot Arena → LMArena → Arena (arena.ai)

**What it measures.** Crowdsourced pairwise human preference between two anonymous LLM responses to a prompt the user writes. Votes are A, B, tie or both-bad. Ratings come from a Bradley-Terry (BT) logistic regression, bootstrapped for 95% CIs and reweighted for non-uniform sampling. [V]

**Release, venue, creators**
- Launched May 2023. The first leaderboard post (3 May 2023) covered battles from 24 April to 1 May 2023. [V]
- Authors of the launch post: L. Zheng, Y. Sheng, W.-L. Chiang, H. Zhang, J. E. Gonzalez, I. Stoica (UC Berkeley / LMSYS). [V]
- Technical paper: "Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference", Chiang, Zheng, Sheng, Angelopoulos, Li, Li, Zhu, Zhang, Jordan, Gonzalez, Stoica. ICML 2024, PMLR 235:8359-8388, arXiv:2403.04132. [V]

**Item count and format.** There is no fixed item set. The platform streams live user prompts.
- The paper reported "over 240K votes". [V]
- Policy page (March 2024): "over 800,000 votes", "more than 90 LLMs". [V]
- FastChat README: "over 1.5M human votes". [V, undated]
- Vote-rigging paper: ~1.7M historical votes. [V]
- April 2025 blog: "3M+ votes, 400+ models, and 300+ pre-release tests", "Tens of millions" of battle pairings served, 1.5M prompts released. [V]
- September 2025 company product post: "250M+ real conversations, 2M+ monthly votes, 3M+ monthly users". [S]
- January 2026 Series A blog: "the community has contributed 50 million votes". [S] This conflicts with Grokipedia's "5,430,034 votes" as of 5 March 2026. [S, low reliability] [corrected by fact-check] The full sentence reads: "Since announcing our $100M Seed round last year in May ... In a matter of months, the community has contributed: 50 million votes across text, vision, web dev, search, video and image modalities". The 50M is therefore a post-May-2025, all-modality count (seen via a scraped copy of the blog: Amal-David/docingest `lmarena.ai/documentation_2026-01-18`).

**Method evolution [V]**
- Online Elo was replaced by BT MLE with bootstrap CIs in December 2023. The post explains that online Elo had "considerable variability".
- Vote counts in the December 2023 update: 130,000+.
- The score was renamed "Arena Score" ("which we formerly called the Elo score").
- Category leaderboards were added, including Hard Prompts (May 2024).
- Style control (29 August 2024) adds length and markdown features to the BT regression.
- Sentiment control (22 April 2025) adds emoji count and sentiment.
- Prompt-to-Leaderboard (arXiv:2502.14855; published at ICML 2025, PMLR 267:17672-17689 [corrected by fact-check]) gives per-prompt leaderboards.
- Arena-Rank, the open-source ranking package (`pip install arena-rank`), powers the leaderboard.

**Frontier score at launch vs. latest.** BT scores are relative and anchored, so values are not comparable across years [I].
- Launch leaderboard (24 April-1 May 2023): vicuna-13b #1 at 1169 Elo. GPT-4 had not yet been added. [V]
- December 2023: GPT-4-Turbo 1217. [V]
- 18 November 2025: Gemini 3 Pro debuted at #1 in Text with 1501, and #1 in WebDev with 1487. [S; AINews citing @arena]
- February 2026: Gemini-3.1-Pro tied #1 in Text at 1500. [S]
- 5 March 2026: claude-opus-4-6 at 1504. [S, Grokipedia]
- July 2026: Claude Opus 5 Max #1 in "Text Arena with factuality on". [S] This suggests a 2026 factuality toggle; details not verified [U].

**Adoption evidence**
- The paper abstract calls it "one of the most referenced LLM leaderboards, widely cited by leading LLM developers and companies". [V]
- Launch announcements cite Arena rank:
  - Meta's Llama 4 announcement claimed it bested GPT-4o on LMArena [S];
  - Google's Gemini 3 launch cited #1 across Arena leaderboards [S];
  - Kimi, GLM, DeepSeek, Gemini 3.5 Flash and others in 2026 [S].
- Commercial scale:
  - $100M seed at $600M (TechCrunch, 21 May 2025) [S];
  - $150M Series A at a $1.7B post-money valuation, led by Felicis and UC Investments (TechCrunch and PR Newswire, 6 January 2026) [S]. [corrected by fact-check: now independently corroborated] A Latent Space episode dated 2026-01-06 gives "$150m at a $1.7B valuation, with $30M annualized consumption revenue". The Series A blog text lists participation from Andreessen Horowitz, The House Fund, LDVP, Kleiner Perkins, Lightspeed Venture Partners and Laude Ventures;
  - more than $30M annualized consumption run rate by December 2025, less than four months after launching its "AI Evaluations" product (September 2025) [S].
- Competitors copied the format, which is itself adoption evidence [I]: Scale AI's SEAL Showdown (launched about 22 September 2025, with demographically verified raters from its Outlier platform) [S], and Artificial Analysis's image and video arenas [S].

**Status: thriving (commercially), contested (scientifically).**

**Why it succeeded**
1. **No static test set to contaminate.** LMArena's own analysis of 355,575 battles (May-December 2024) found that about 75% of each day's prompts are "significantly different from any prompt on a previous day", and that fewer than 1% of user prompts appear in popular benchmarks. [V] The policy FAQ gives contamination as the explicit reason for the design. [V]
2. **Real-world, open-ended distribution** rather than multiple choice. [V]
3. **One comparable number with CIs**, plus category slices. [V]
4. **Consumer incentive loop.** Users get free, anonymous side-by-side access to frontier and pre-release models. The team reports the community's main ask is "frequent access to the best models, and being a part of the first to access the newest ones". [V] The 2025 rebuild explicitly aimed to be "more fun to use". [V]
5. **Vendor incentive loop.**
   - Anonymous pre-release testing (300+ by April 2025). [V]
   - Rating shared privately, plus up to 20% of the model's votes. [V]
   - This gives labs a reason to submit early and to publicise results. [I]
6. **Openness.** FastChat code, datasets (Chatbot Arena Conversations 33k, LMSYS-Chat-1M, arena-human-preference-140k) and published methodology papers. [V]
7. **Continuous extension into new modalities and verticals** (Vision, WebDev/Code, Search, Copilot, RepoChat, Agent, Text-to-Image, Video, Document). This keeps the brand relevant as chat saturates. [V/S]

**Why it is failing or contested**
1. **Style over substance.**
   - Style control found that length is the dominant style factor (normalized coefficient 0.249 when controlling for both length and markdown, vs. 0.019-0.031 for markdown). [corrected by fact-check] The 0.019-0.031 range holds only in the control-both model. When markdown alone is controlled, the list coefficient is 0.111 (header 0.044, bold 0.056). Controlling reshuffled ranks: GPT-4o-mini and Grok-2-mini fell, and Claude 3.5 Sonnet rose to tie #1 on Hard Prompts. [V]
   - Sentiment control found positive and very-positive tone raise win rates. Models "known for strong stylistic and emotional appeal - like Grok-3 and Llama-4-Maverick-Experimental - drop in rank" under control. [V]
2. **Rater quality.**
   - Surge AI's audit of 500 Arena votes disagreed with 52% (39% "strongly"), for example crowd votes for a hallucinated Wizard of Oz quote and a mathematically impossible cake-pan substitution. Their summary: "confidence beats accuracy and formatting beats facts." [S; Surge AI is a paid-labeling vendor, a possible conflict of interest]
   - Hosking et al. (ICLR 2024) showed that the assertiveness of outputs skews annotators' perceived factuality errors, so preference scores under-represent factuality. [V]
3. **Provider gaming via private variants (see §1a, §1b).** [V/S]
4. **Vote rigging.**
   - Min et al. (ICML 2025): an "omnipresent" rigging strategy exploiting BT coupling can improve a target model's rank "by rigging only hundreds of new votes". It was simulated on ~1.7M historical votes. [V]
   - Huang et al. (ICML 2025, oral): an attacker can identify which model produced a reply with >95% accuracy and shift the leaderboard for roughly a thousand votes. Defences added: Cloudflare, reCAPTCHA, login, rate limits. [V] [corrected by fact-check] The thousand-vote cost was "verified in a simulated, offline version of Chatbot Arena", not demonstrated on the live leaderboard. Some defences (Cloudflare, malicious-user detection, rate limiting) predated the collaboration; reCAPTCHA and login were being added.
5. **New position and affiliation biases in 2026 formats.** The May 2026 leaderboard changelog for "Battles in Direct" reported "a position bias favoring Model A" and "an advantage given to models that share an organization with the prior turns of context". [S]
6. **Routers and systems, not models.** In January 2025 an LMArena-trained P2L router "achieved the #1 spot in the Chatbot Arena leaderboard". [V] This illustrates that the top slot can be won by composition rather than by a better base model [I].
7. **Governance and conflict of interest.** Arena now sells evaluation services to OpenAI, Google and xAI, which it also ranks. Press has framed it as "the leaderboard 'you can't game,' funded by the companies it ranks". [S]
8. **Narrow task coverage.** Community critiques call it a "one-shot vibe check" that does not capture multi-turn, long-context or agentic ability. [S] Agent Arena (June 2026) moved away from pairwise votes to "causal tracing" of real agent sessions. [S]

**Sources**
- https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2023-05-03-arena.md
- https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2023-12-07-leaderboard-elo-update.md
- https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2024-03-01-policy.md
- https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2024-08-29-style-control.md
- https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2025-04-22-sentiment-control.md
- https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2025-03-5-freshness.md
- https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2025-04-17-new-beta.md
- https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2025-04-27-two-year-celebration.md
- https://raw.githubusercontent.com/mlresearch/v235/gh-pages/_posts/2024-07-08-chiang24b.md
- https://raw.githubusercontent.com/lm-sys/FastChat/main/README.md
- https://raw.githubusercontent.com/lmarena/arena-rank/main/README.md
- https://raw.githubusercontent.com/lmarena/p2l/main/README.md
- https://raw.githubusercontent.com/mlresearch/v267/gh-pages/_posts/2025-10-06-min25a.md
- https://raw.githubusercontent.com/mlresearch/v267/gh-pages/_posts/2025-10-06-huang25z.md
- Secondary:
  - https://github.com/vibewatch/startup (`reports/20260625005021-lmarena/evidence.yaml`), which cites TechCrunch, PR Newswire, arena.ai/blog/series-a, arena.ai/blog/ai-evaluations, arena.ai/blog/leaderboard-changelog and arena.ai/blog/agent-arena-methodology;
  - https://github.com/smol-ai/ainews-web-2025 (issues 25-11-18, 26-01-28, 26-02-19, 26-07-16, 26-07-27);
  - https://github.com/Planeshifter/hackernews-ai-digest (`data/digest_2026-01-07.md`);
  - https://github.com/GaloisField2718/tldr_news (SEAL Showdown).

#### 1a. "The Leaderboard Illusion" (Singh et al., 2025): the central critique

**Bibliographic details [V]**
- Authors: Shivalika Singh, Yiyang Nan, Alex Wang, Daniel D'Souza, Sayash Kapoor, Ahmet Üstün, Sanmi Koyejo, Yuntian Deng, Shayne Longpre, Noah Smith, Beyza Ermis, Marzieh Fadaee, Sara Hooker.
- arXiv:2504.20879, first posted 29 April 2025, 68 pages.
- NeurIPS 2025 poster 121845. [corrected by fact-check] It was in the Datasets & Benchmarks track, as a poster (OpenReview 4Ae8edNqm0), per the papercopilot/paperlists `nips2025.json` record.

**Abstract claims [V, verbatim from the cached arXiv API record]**
- "undisclosed private testing practices benefit a handful of providers who are able to test multiple variants before public release and retract scores if desired."
- "we identify 27 private LLM variants tested by Meta in the lead-up to the Llama-4 release."
- "Providers like Google and OpenAI have received an estimated 19.2% and 20.4% of all data on the arena, respectively. In contrast, a combined 83 open-weight models have only received an estimated 29.7%."
- "even limited additional data can result in relative performance gains of up to 112% on the arena distribution."
- The NeurIPS-listed abstract rewords this as "112% on ArenaHard, a test set from the arena distribution". It also anonymises Meta as "one provider testing 27 private variants before making one model public at the second position" and Google/OpenAI as "the top two providers". [V]

**Further findings, per a third-party reading of v2 [S, benchflow-ai/awesome-evals notes]** [fact-check: the ~2M battles, 243 models and 42 providers (January 2024-April 2025) figures are corroborated by an independent summary (gabrielchua/daily-ai-papers, 30 April 2025). The "out of 243 public models, 205 have been silently deprecated" quote is corroborated by microprediction/winning. The remaining body numbers are still single-source.]
- Scope: ~2M battles, 243 models and 42 providers, January 2024 to April 2025.
- 205 of 243 public models were silently deprecated, vs. 47 officially listed; 64% of silent removals were open-weight or open-source.
- 7.3% of December 2024 prompts reappear verbatim in January 2025.
- Raising the arena-data share of an SFT mix from 0% to 70% lifted the ArenaHard win rate from 23.5% to 49.9%, while MMLU slipped from 66.5% to 64.4-65.9%. The gains do not generalise.
- The paper makes five reform recommendations:
  1. prohibit score retraction;
  2. cap private variants;
  3. use stratified, auditable deprecation;
  4. make sampling fair;
  5. publish quarterly transparency reports.

**LMArena's rebuttal (9 May 2025) [V]**
- Official stats show open models at 40.9% of battles, not the 8.8% the writeup counted. [fact-check note, I] The 40.9% counts battles *involving* at least one open model (the 27 April post says "nearly 41% of battles involving an open model"). The paper's 29.7% is an estimated *share of all data* for 83 open-weight models. The two are different quantities, and neither refutes the other.
- The "+100 points" figure came from a Gaussian simulation "unrelated to Chatbot Arena". LMArena estimates the real effect at about +11 Elo after 50 tests and 3,000 votes, "diminishes to zero as fresh evaluation data accumulates".
- Scores of the same checkpoint (1069 ± 27 vs. 1054) overlap within CIs.
- Cohere itself had 9 pre-release tests since January 2025, "2-3x more" than xAI or OpenAI.
- The 112% gain was on Arena-Hard, "a static benchmark with 500 data points that uses an LLM judge", not on human Arena.

**Policy changes after the dispute [V, current policy page]**
- Explicit statement that "Model providers are all allowed to test multiple variants of their models pre-release".
- Results are marked "provisional" until 2,000 fresh post-release votes if more than 10 variants were tested in parallel.
- A public list of retired models from 15 June 2025.
- "as of July 1, 2025, we will share 100% of the arena vote data used for the public leaderboard". [fact-check note] The policy qualifies this as "(model identities and votes)". Prompts and responses are shared only in part, and only with user consent.
- Sampling rules: weight 5 until 3,000 votes; top-10 models get weight 3; retirement rules are published.

**Press quote [S; TechCrunch, 30 April 2025; fact-check: seen only in one secondary compilation (vibewatch), not independently confirmed, so treat as unverified]:** Sara Hooker: "Only a handful of [companies] were told that this private testing was available ... This is gamification."

#### 1b. The Llama-4-Maverick experimental-variant controversy (April 2025)

- **Meta's launch claims.** Meta launched Llama 4 (Scout and Maverick) around 5-6 April 2025, claiming Maverick beat GPT-4o on LMArena. It took #2 behind Gemini 2.5 Pro. [S; Slashdot/The Verge, 8 April 2025]
- **The variant.** Meta's own materials disclosed that the Arena entry was an "experimental chat version" "optimized for conversationality", labelled "Llama-4-Maverick-03-26-Experimental". [S; Wikipedia copy; TechCrunch]
- **LMArena's statement:** "Meta's interpretation of our policy did not match what we expect from model providers. Meta should have made it clearer that 'Llama-4-Maverick-03-26-Experimental' was a customized model to optimize for human preference." [S; The Verge via Wikipedia copy and vibewatch evidence file]
- **The release model.** LMArena then scored the public release, "Llama-4-Maverick-17B-128E-Instruct". As of 11 April 2025 it ranked 32nd, below months-old models such as GPT-4o, Claude 3.5 Sonnet and Gemini 1.5 Pro. [S; TechCrunch cached text; Slashdot 13 April 2025] [fact-check: the 32nd rank is confirmed by the Slashdot RSS cache of 13 April 2025, which quotes TechCrunch and Neowin. That cache names Claude 3.5 Sonnet and Gemini-1.5-Pro-002 as ranking higher; the GPT-4o comparison was not seen in the caches read.]
- **Advertised score.** Meta advertised an Elo of about 1417 for the experimental variant. [S, multiple secondary]
- **Meta's response.** A Meta spokesperson said the company experiments with "all types of custom variants". [S]
- **Style/sentiment evidence.** LMArena's own sentiment-control analysis later singled out "Llama-4-Maverick-Experimental" as a model that drops in rank once style, sentiment and emoji are controlled. [V]
- **Lesson [I].** The scored artifact must be the shipped artifact, identified by checkpoint or hash. Otherwise a preference leaderboard rewards preference-tuned demo variants.

### 2. WebDev Arena → Code Arena (LMArena)

**What it measures.** A user submits an app prompt, two models each build a working web app, the user interacts with both and votes. Ratings use BT. [V]

**Release and creators.** Launched December 2024. Blog post dated 10 March 2025 by Aryan Vichare, Anastasios Angelopoulos, Wei-Lin Chiang, Kelly Tang and Luca Manolache. No peer-reviewed paper found [U]. [V]

**Item count and format**
- There is no fixed set.
- By March 2025: "over 80,000 community votes". [V]
- Duplicate sample prompts were heavily over-represented. The top suggested prompts ("Clone of VS Code / Cursor" 4,189; WhatsApp clone 3,385; chess 3,154) dominated. [V]
- Deduplication reduced votes from 103,096 to 61,473, and scores shifted by 9-52 points (Claude 3.7 Sonnet 1362.94 → 1311.40). [V]

**Scores**
- March 2025: Claude 3.7 Sonnet #1 (1362.94; 76% average win rate). [V]
- June 2025: Gemini-2.5-Pro-Preview-06-05 at 1443 overtook Claude Opus 4 at 1412. [S]
- November 2025: Gemini 3 Pro at 1487. [S]
- By 2026 it had become "Code Arena" with WebDev and Frontend boards. Kimi K3 reached #1 on Frontend Code Arena at 1679 in July 2026, with a 76% pairwise win rate. [S]

**Adoption.** Cited in lab launch materials (Gemini 3, Kimi K3, GLM-5.2, Gemini 3.5 Flash). [S] **Status: thriving.**

**Why it succeeded [I]**
- Outputs are *interactive artifacts* that ordinary users can judge by trying them.
- The task is realistic and open-ended.
- It is fun (apps and games).
- The skill is commercially relevant (front-end coding).

**Why it is failing or contested**
- Prompt concentration on UI-suggested examples. [V]
- Aesthetic and first-impression bias, with no functional testing. [I] Reddit commenters questioned "what it actually measures" [S].
- Leadership is volatile and swings with launch timing [S/I].

**Sources**
- https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2025-03-06-webdev-arena.md
- AINews issues 25-06-05, 25-11-18, 26-07-16 (https://github.com/smol-ai/ainews-web-2025).

### 3. Copilot Arena (CMU + Berkeley / LMArena)

**What it measures.** In-the-wild code-completion and inline-edit preference inside VS Code. The free extension shows two completions or two diffs, and the user accepts one. [V]

**Release, venue, creators.** Extension launched October 2024. First leaderboard blog 12 November 2024. Paper "Copilot Arena: A Platform for Code LLM Evaluation in the Wild", Chi, Chen, Angelopoulos, Chiang, Mittal, Jain, Zhang, Stoica, Donahue, Talwalkar. ICML 2025, PMLR 267:10354-10382, arXiv:2502.09328. [V]

**Scale**
- November 2024: 2.5K downloads, 100K+ completions, 10K+ battles, 9 models. [V]
- Paper: "over 4.5 million suggestions from 10 models and ... over 11k pairwise judgements". [V]

**Key findings [V]**
- **Position bias:** "82% of accepted completions were the top completion". The effect differs by model: as the bottom completion, Sonnet-3.5 was accepted 23.4% of the time vs. 12.8% for Gemini Flash.
- Rankings "differ from those of existing evaluations".
- Preference is consistent across languages but varies by task category.

**Status: niche / active.** The repo was still being updated in September 2026 [V, repo metadata], but no current public leaderboard was verified [U].

**Why it succeeded [I].** Evaluation piggybacks on real work, and users get a free tool. Implicit signals (acceptance) replace explicit votes.

**Why it is failing [I].**
- Low vote volume relative to the text arena.
- Strong UI position bias.
- It competes with free first-party copilots, and required disabling other completion providers [V, README].

**Sources**
- https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2024-11-12-copilot-arena.md
- https://raw.githubusercontent.com/lmarena/copilot-arena/main/README.md
- https://raw.githubusercontent.com/mlresearch/v267/gh-pages/_posts/2025-10-06-chi25a.md

### 4. Search Arena (LMArena)

**What it measures.** Pairwise preference over search-augmented LLM systems (Perplexity Sonar, Gemini Grounding, OpenAI web-search) on real, often current-events queries. [V]

**Release, venue, creators**
- Launched 18 March 2025; blog 14 April 2025. [V]
- Paper "Search Arena: Analyzing Search-Augmented LLMs", Miroyan, Wu, King, Li, Pan, Hu, Chiang, Angelopoulos, Darrell, Norouzi, Gonzalez. arXiv:2506.05334. The README says ICLR 2026. Its BibTeX says "Thirteenth International Conference on Learning Representations" with year 2026, which is internally inconsistent; ICLR 2026 is the fourteenth. [V] [corrected by fact-check] ICLR 2026 is confirmed as the venue (poster; OpenReview MMGRlDnhtI, per papercopilot `iclr2026.json`). The official BibTeX there reads "The Fourteenth International Conference on Learning Representations", so "Thirteenth" is a typo in the repo README.

**Item count.** At launch, 11k+ votes were filtered to 7k battles (search-arena-v1-7k). The full public dataset has about 24k (`search_arena_24k.jsonl`). [V]

**Scores.** April 2025: Gemini-2.5-Pro-Grounding and Perplexity-Sonar-Reasoning-Pro at the top. [V] Latest standings: [U].

**Key findings [V]**
- Users prefer longer responses, more citations, and citations to community/blog sources over Wikipedia.
- "models do not always cite retrieved sources accurately and humans do not always check citations!"

**Status: niche.** The README points to legacy.lmarena.ai with "new UI integration is coming soon" [V].

**Why it succeeded.** It filled an evaluation gap for a fast-growing product category, and the data release produced an ICLR paper.

**Why it is failing.** It inherits the length bias and adds *citation-count* bias, meaning surface proxies for credibility. Humans do not verify the citations. [V/I]

**Sources**
- https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2025-04-14-search-arena.md
- https://raw.githubusercontent.com/lmarena/search-arena/main/README.md

### 5. Design Arena (designarena.ai)

**What it measures.** Crowdsourced preference over AI-generated visual and front-end design. A prompt goes to several models, outputs are shown anonymously, and a human picks winners in a mini-tournament until a 1-4 ranking exists. Each pairwise choice is a vote.

- Ratings: BT "iterated to convergence, normalized, then 400 × log10(strength)", with a minimum vote threshold and hidden identities.
- Separate boards for websites, UI components, mobile apps, slides, games, 3D, SVGs, data visualisations, logos, video and text-to-speech, plus an overall frontend board.
- An "Agentic Web Dev" track evaluates web apps built by coding agents.

Source for the method is secondary: AgentsORG/design-engineering notes summarising notes.designarena.ai/methodology. [S]

**Release and creators**
- YC Summer 2025 company "Design Arena", one-liner "World's largest crowdsourced benchmark for AI-generated design", team size 3, San Francisco. [S; yc-oss mirror of the YC API] [fact-check: re-read and confirmed. The same record lists the former name "Arcada" and a YC launch timestamp of 2025-07-30. Independent third-party repos (Geno-Claw/ai-ui-benchmark, bra1nDump/skillpack, deepakorani/chemistry-arena) also describe it as "Arcada Labs, YC S25", with a 4-model anonymous tournament and Bradley-Terry scoring. All of this is secondary.]
- A founder "Show HN" on 12 July 2025 (HN item 44542578) and an August 2025 follow-up are recorded by a third-party catalogue. [S] The HN API itself was blocked.
- No peer-reviewed paper found. [U]

**Adoption evidence [S]**
- Z.ai's GLM-5.2 launch (June 2026) claimed "#1 on Design Arena", citing @Designarena.
- Thinking Machines' "Inkling" announcement (15 July 2026) reported Design Arena Agentic Web Dev at 1257.
- Third-party tools route design tasks to "designarena.ai's current top-ranked model" (K1ta141k/mcp-bench-router) and combine DesignArena with Artificial Analysis for price-quality comparisons.

**Status: thriving (niche domain).**

**Why it succeeded [I]**
- The user explicitly credits DesignArena, together with ARC-AGI and Arena, for having an "underlying philosophy" and a "measurable leaderboard".
- Design outputs are visually judgeable by laypeople in seconds, so the task is fun to vote on.
- Multi-way tournaments extract more pairwise comparisons per prompt than 2-way votes.
- Per-category boards give domain-specific ladders.
- It launched while the main LMArena was busy commercialising.

**Why it is failing or at risk [I]**
- Pure aesthetic preference, with no functional or accessibility checks. This is the same style-over-substance risk as the main Arena.
- A startup-run leaderboard carries the same incentive and conflict-of-interest questions.
- Methodology is documented only on its own site.

**Sources**
- https://raw.githubusercontent.com/yc-oss/api/main/batches/summer-2025/design-arena.json
- https://raw.githubusercontent.com/AgentsORG/design-engineering/main/skills/design-engineering/references/meta/design-benchmarks.md
- https://raw.githubusercontent.com/Claire1217/benchmark-radar/main/data/library_source_reviews.json
- AINews 26-06-16 (GLM-5.2)

### 6. MT-Bench

**What it measures.** Multi-turn chat quality. There are 80 two-turn questions (160 turns), 10 per category across 8 categories: Writing, Roleplay, Extraction, Reasoning, Math, Coding, STEM and Humanities. GPT-4 grades each answer on a 1-10 scale. [V]

**Release, venue, creators.** June 2023 (blog "Chatbot Arena Leaderboard Updates (Week 8): Introducing MT-Bench and Vicuna-33B", 22 June 2023). Paper "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena", Zheng, Chiang, Sheng, Zhuang, Wu, Zhuang, Lin, Li, Li, Xing, Zhang, Gonzalez, Stoica. NeurIPS 2023 Datasets & Benchmarks track, arXiv:2306.05685. [V]

**Headline finding.** Strong LLM judges "can align impressively well with both controlled and crowdsourced human preferences, achieving over 80% agreement ... comparable to the agreement between two different human judges". The paper also catalogues position, verbosity and self-enhancement biases. [V]

**Scores**
- At launch: GPT-4 8.99/10. [V]
- By April 2024: only 22.6% separability with 95% CIs, and 26.1% agreement-with-CI with Chatbot Arena, across 20 top models. Arena-Hard-Auto v0.1 had 87.4% / 89.1% on the same measures. [V] [fact-check note] MT-Bench's plain Spearman correlation with Arena on the same models was still 91.3%, so the low figure comes from the CI-aware metric. The blog prose also calls 22.6% an "agreement" figure in one place, contradicting its own table. Figures here follow Table 1.
- Later frontier MT-Bench scores: [U].

**Adoption.** Huge in 2023-24: the MT-Bench column on the Arena leaderboard, and open-model papers. It is still bundled in eval harnesses (e.g., mlfoundations/evalchemy includes MTBench) [V, code search].

**Status: saturated / abandoned as a frontier metric.**

**Why it succeeded.** It was cheap, fast, multi-turn, came with a validated judge methodology, and was bundled with the Arena brand. [I]

**Why it failed [V/I].**
- 80 questions is too few to separate close models.
- A 10-point scale with a ceiling.
- The questions are public and static (contaminable).
- The GPT-4 judge has known biases.
- It was superseded by its own authors' Arena-Hard.

**Sources**
- https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2023-06-22-leaderboard-week8.md
- https://raw.githubusercontent.com/lm-sys/FastChat/main/fastchat/llm_judge/README.md
- https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2024-04-19-arena-hard.md
- https://raw.githubusercontent.com/CSHaitao/Awesome-LLMs-as-Judges/main/README.md

### 7. AlpacaEval, AlpacaEval 2.0 and Length-Controlled AlpacaEval

**What it measures.** Instruction-following quality as the win rate against a reference model, judged by an LLM (GPT-4 Turbo "weighted_alpaca_eval_gpt4_turbo" in 2.0). The set has 805 instructions drawn from self-instruct, OASST, Vicuna, Koala and HH-RLHF. The judge is validated on 20K human annotations. [V]

**Release, venue, creators [V]**
- AlpacaEval: Li, Zhang, Dubois, Taori, Gulrajani, Guestrin, Liang, Hashimoto, GitHub, May 2023. It is built on AlpacaFarm (Dubois et al., arXiv:2305.14387; NeurIPS 2023 spotlight [corrected by fact-check]).
- Length-Controlled AlpacaEval: Dubois, Galambosi, Liang, Hashimoto, arXiv:2404.04475, COLM 2024. COLM venue per Percy Liang's publication database. [corrected by fact-check] The COLM 2024 version (OpenReview CybBmzWBX0, poster) is titled "Length-Controlled AlpacaEval: A Simple *Debiasing* of Automatic Evaluators" and lists three authors: Dubois, Liang, Hashimoto (no Galambosi). The arXiv version is "A Simple Way to Debias Automatic Evaluators" with four authors. Cite the version that matches the venue.

**Length control [V]**
- LC fits a GLM to predict what the preference would be "if the model's output had the same length as the baseline".
- It raised Spearman correlation with Chatbot Arena from 0.93 to 0.98. [fact-check note] The COLM abstract and one README passage give the baseline as 0.94 (0.94→0.98); two other README passages say 0.93.
- It cut "relative length gameability" from ~21% to ~6%.
- Raw 2.0 was easy to game: prompting the baseline to "give as much detail as possible" moved its win rate from 50% to 64%, and "be as concise as possible" moved it to 23%.
- Cost: <$10 and <3 minutes per model.

**Scores**
- AlpacaEval 2.0 baseline: gpt4_1106_preview = 50%. [V]
- Frontier LC win rates in the official CSV: gpt-4o-2024-05-13 57.5, gpt-4-turbo-2024-04-09 55.0, claude-3-5-sonnet-20240620 52.4. [V]
- The CSV contains no 2025-26 frontier models. [V, 223 entries inspected]
- Lab-reported (not on the board): DeepSeek-V3 70.0 (December 2024) and DeepSeek-R1 87.6 (January 2025). [V, DeepSeek READMEs]

**Gaming evidence [V]**
- The official CSV lists a community "NullModel" at an **86.5% LC win rate** (76.9% raw). It returns a constant, adversarially crafted response, from "Cheating Automatic LLM Benchmarks: Null Models Achieve High Win Rates" (Xiaosen Zheng, Tianyu Pang, Chao Du, Qian Liu, Jing Jiang, Min Lin; ICLR 2025, oral per repo; arXiv:2410.07137). [fact-check: the ICLR 2025 oral is confirmed by the papercopilot `iclr2025.json` record. The same abstract also reports an 83.0 score on Arena-Hard-Auto and 9.55 on MT-Bench for the null model.]
- The top non-null entries are 9B Gemma-2 fine-tunes and mixture-of-agents stacks (e.g., SelfMoA_gemma-2-9b-it-WPO-HB at 78.5, average length 3,261 tokens). They outrank GPT-4o and Claude 3.5 Sonnet.

**Documented limitations (README) [V].** Annotators prefer longer outputs and lists: 0.68/0.69 for the GPT-4 annotator and 0.64/0.61 for humans. They also prefer outputs from models similar to themselves. There is no safety evaluation. The README says "should not be used as replacement for human evaluation in important settings".

**Adoption.** A standard metric in 2024 preference-optimisation papers (DPO/SimPO/WPO entries on the board) [V]. It appears in DeepSeek V3/R1 model cards [V].

**Status: saturated / gamed / leaderboard stale.**

**Why it succeeded [I].** It was the cheapest human-preference proxy (<$10), showed high correlation with Arena, and was easy to run with pip.

**Why it failed.**
- A fixed, public, small (805) instruction set that is easy and unrepresentative (the README admits this).
- A single judge and a single baseline.
- Exploitability by length, style and adversarial strings.
- The ceiling was reached by 2025.

**Sources**
- https://raw.githubusercontent.com/tatsu-lab/alpaca_eval/main/README.md
- https://raw.githubusercontent.com/tatsu-lab/alpaca_eval/main/src/alpaca_eval/leaderboards/data_AlpacaEval_2/weighted_alpaca_eval_gpt4_turbo_leaderboard.csv
- https://raw.githubusercontent.com/sail-sg/Cheating-LLM-Benchmarks/main/README.md
- https://raw.githubusercontent.com/deepseek-ai/DeepSeek-R1/main/README.md
- https://raw.githubusercontent.com/deepseek-ai/DeepSeek-V3/main/README.md

### 8. Arena-Hard-Auto (v0.1 → v2.0) and BenchBuilder

**What it measures.** Pairwise LLM-judge win rate against a baseline on hard prompts mined from Chatbot Arena by the BenchBuilder pipeline. BenchBuilder uses BERTopic clusters, scores clusters on "7 key criteria", and keeps 250 clusters with mean score ≥ 6/7. Each prompt is judged twice with positions swapped, and results are aggregated with BT and bootstrapped CIs. [V]

**Release, venue, creators [V]**
- Blog 19 April 2024 (Tianle Li, Wei-Lin Chiang, Evan Frick, Lisa Dunlap, Banghua Zhu, Joseph E. Gonzalez, Ion Stoica).
- Paper "From Crowdsourced Data to High-quality Benchmarks: Arena-Hard and BenchBuilder Pipeline" (adds Tianhao Wu). ICML 2025, PMLR 267:34209-34231, arXiv:2406.11939.

**Items**
- v0.1: 500 prompts, GPT-4-Turbo judge, GPT-4-0314 baseline. [V]
- v2.0 (23 April 2025): "500 fresh, challenging real-world user queries ... and 250 creative writing queries". Judges are GPT-4.1 and Gemini-2.5; style control has been supported since 14 October 2024. [V]

**Validation claims [V]**
- Blog: 89.1% agreement-with-CI and 87.4% separability (vs. MT-Bench 26.1% / 22.6% and AlpacaEval-LC 81.2% / 83.2%), at $25.
- Paper: "3x higher separation ... compared to MT-Bench and ... 98.6% correlation with human preference rankings, all at a cost of $20".

**Scores and saturation [V]**
- The v0.1 style-controlled leaderboard (file dated 11/14, presumably 2024) is topped at 88.7 by a Nemotron-Super-49B "Feedback-Edit-ITS" system. [corrected by fact-check] The file header "(Updated: 11/14)" cannot be taken as November 2024. The file lists "Llama-3.3-Nemotron-Super-49B-v1-Feedback-Edit-ITS", and to my (unverified) background knowledge Llama-3.3-Nemotron-Super-49B-v1 was released in 2025. The update date is therefore unknown. The same system scores 93.4 on the non-style-controlled v0.1 board in that file.
- DeepSeek-R1 reports ArenaHard (GPT-4-1106 judge) 92.3, with o1-mini at 92.0 (January 2025).
- v2.0 (April 2025, Gemini-2.5 judge): o3 85.9, o4-mini-high 79.1, gemini-2.5 79.0.

**Judge dependence / self-preference [V]**
- On v2.0 hard prompts, gemini-2.5 scores **79.0 under the Gemini-2.5 judge but 49.1 under the GPT-4.1 judge**. gpt-4.1 scores 50.0 vs. 58.3 in the reverse direction. The 2024 blog already found the Claude-3-Opus judge inflated Claude-family scores.
- This is consistent with self-preference bias (Panickssery et al., NeurIPS 2024, arXiv:2404.13076) [V venue via author page; fact-check: confirmed as a NeurIPS 2024 *oral* per papercopilot `nips2024.json`].

**Adoption.** DeepSeek V3/R1 model cards [V]. It became the de facto open-model chat metric in 2024-25 [I]. The Leaderboard Illusion used ArenaHard as its test of arena-data overfitting [V].

**Status: active but contested.** The README news stops at April 2025 [V]. v0.1 is saturated.

**Why it succeeded [I].** Real-user hard prompts, CI-based separability as an explicit design goal, cheap automation, and a validated link to Arena.

**Why it is failing.**
- Judge self-preference and style bias.
- A fixed public set, trainable via Arena data (the 23.5→49.9 example [S]).
- Refresh depends on the Arena team's cadence.

**Sources**
- https://raw.githubusercontent.com/lmarena/arena-hard-auto/main/README.md
- https://raw.githubusercontent.com/lmarena/arena-hard-auto/main/misc/past_leaderboards.md
- https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2024-04-19-arena-hard.md
- https://raw.githubusercontent.com/mlresearch/v267/gh-pages/_posts/2025-10-06-li25h.md

### 9. WildBench (AI2)

**What it measures.** Performance on 1,024 challenging tasks selected from real user-chatbot logs (WildChat, over 1M conversations filtered). Each task has a checklist of 5-10 questions generated by GPT-4-Turbo and Claude-3-Opus. There are two metrics: WB-Reward (pairwise against three baselines, with a length penalty that converts "slightly better/worse" to tie when the winner is much longer) and WB-Score (individual scoring). WB-Elo merges the two. [V README; S benchmark card]

**Release, venue, creators [V]**
- Bill Yuchen Lin, Yuntian Deng, Khyathi Chandu, Faeze Brahman, Abhilasha Ravichander, Valentina Pyatkin, Nouha Dziri, Ronan Le Bras, Yejin Choi.
- arXiv:2406.04770 (June 2024). ICLR 2025 (spotlight) per the Sci-Reasoning ICLR-2025 list; OpenReview id MKEHCx25xp. [corrected by fact-check] The spotlight is confirmed by papercopilot `iclr2025.json`. That ICLR/OpenReview record lists **8 authors, without Faeze Brahman**. The arXiv BibTeX in the WildBench README lists 9 authors, including Brahman. Use the author list that matches the version cited.

**Validation.** Pearson correlation with Chatbot Arena Elo (Hard-English, up to 20 May 2024): 0.98 for WB-Reward and 0.95 for WB-Score. [S benchmark card; the README states WB Reward-Mix has the highest correlation [V]] [corrected by fact-check: upgraded to V] The ICLR 2025 abstract states that "WB-Reward achieves a Pearson correlation of 0.98 with top-ranking models" and that "WB-Score reaches 0.95, surpassing both ArenaHard's 0.91 and AlpacaEval2.0's 0.89".

**Scores.** No verified frontier numbers [U]. The README's model-add list stops at mid-2024 models (e.g., claude-3-5-sonnet-20240620) [V].

**Adoption.** Included in Stanford HELM's capabilities scenarios [S, HELM v1.15.0 core_scenarios reference in the eval card]. An EEE card lists OLMo 2 32B at 0.734 [S].

**Status: niche / absorbed.** It lives on inside HELM rather than as its own leaderboard.

**Why it succeeded.** Real-user tasks, instance-specific checklists (more interpretable than a bare preference), and an explicit length penalty.

**Why it failed [I].**
- The "dynamically updated" ambition (per the card) was not sustained.
- Dependence on GPT-4-class judges.
- Crowded by Arena-Hard, which has the Arena brand.
- The standalone leaderboard went quiet.

**Sources**
- https://raw.githubusercontent.com/allenai/WildBench/main/README.md
- https://raw.githubusercontent.com/evaleval/eval-cards/main/metadata/benchmark_card_WildBench.json
- https://github.com/AmberLJC/Sci-Reasoning (`prior_work_extraction/results/organized/ICLR_2025/MKEHCx25xp.md`)

### 10. Other items in this family (brief)

- **Prompt-to-Leaderboard (P2L).** Frick, Chen, Tennyson, Li, Chiang, Angelopoulos, Stoica, arXiv:2502.14855. [corrected by fact-check] It was published at ICML 2025 as "Prompt-to-Leaderboard: Prompt-Adaptive LLM Evaluations" (PMLR 267:17672-17689). An LLM outputs prompt-specific BT coefficients. The P2L router took #1 on Chatbot Arena in January 2025. [V]
- **Arena-Rank.** LMArena's open-sourced ranking package (BT with CIs). The example leaderboard uses the public `arena-human-preference-140k` dataset. [V]
- **SEAL Showdown (Scale AI, about September 2025).** A preference leaderboard with verified rater demographics (country, education, profession, language, age) from Scale's Outlier platform. It was pitched as a fix for LMArena's unrepresentative crowd. [S]
- **Agent Arena (Arena, June 2026).** "Rather than pairwise votes, rankings are calculated using a methodology we call causal tracing". [S] This is a notable 2026 retreat from pure pairwise preference for agentic tasks [I].
- **Cross-reference.** Game-based arenas (Kaggle Game Arena, TextArena, MC-Bench) are covered in the sibling dossiers `other_dead_benchmarks.md` and `user_failed_a.md`.

---

## Cross-cutting success factors

1. **Freshness by construction beats contamination.**
   - Live prompts (Arena), post-hoc mined prompts (Arena-Hard v2) and real-log mining (WildBench) all cite contamination resistance as their raison d'être. [V]
   - Arena measured ~75% daily prompt freshness and <1% overlap with public benchmarks. [V]
   - Caveat: the same mechanism lets heavy data holders anticipate the prompt distribution. This is the Leaderboard Illusion's 7.3% cross-month duplication. [S]
2. **One headline number with uncertainty.**
   - BT scores with bootstrap CIs, plus category slices, give press, labs and users a single rank to cite.
   - Arena-Hard made "separability with confidence" a design metric. [V]
   - Compare the user's critique of Qi Town's three incomparable scores.
3. **A two-sided incentive loop.**
   - Consumers get free, anonymous access to frontier and pre-release models, and "fun". [V]
   - Labs get pre-release signal, 20% of their vote data, and a marketing number. [V]
   - This loop, not methodological purity, drove scale (3M+ votes by April 2025 [V]; company claims of 50M by January 2026 [S]). [I]
4. **Judgeability by laypeople.**
   - The most successful arenas (Text, WebDev/Code, Design, Image/Video) ask for judgements a non-expert can make in seconds.
   - Arenas needing expert verification (Search citations, Copilot code correctness) grew more slowly. [V/I]
5. **Open data and methods.** FastChat, Arena-Rank, datasets (33k, 1M, 140k, 24k), notebooks and papers. These allowed third-party audits (Leaderboard Illusion, vote rigging) and bought legitimacy. [V]
6. **Brand ladder and continuous extension.**
   - One brand, many arenas: Vision, WebDev → Code, Search, Copilot, Agent, image and video.
   - Automated derivatives (Arena-Hard) replace saturated items without losing the brand.
   - This mirrors the MathArena/FrontierMath pattern noted in the sibling `math.md`. [V/I]
7. **Institutional and financial backing.** A third-party compilation lists an a16z open-source AI grant announcement (December 2023) among LMArena's funding sources [S; the grant to LMSYS itself was not verified]. That was followed by the spin-out and VC money, which gave long-lived maintenance. Academic one-offs (WildBench, MT-Bench, AlpacaEval leaderboards) stalled when authors moved on. [V/I]
8. **Cheap automatic proxies as a complement.**
   - The LLM-judge proxies won adoption in *model development loops* because they cost $10-25 per model and ran in minutes. [V]
   - They correlated at 0.93-0.98 with Arena at launch. [V]

## Cross-cutting failure factors

1. **Style is not substance.**
   - Human voters and LLM judges both reward length, markdown, lists, positive sentiment and confident tone. [V: style and sentiment control; AlpacaEval README; Hosking et al.; S: Surge audit]
   - Post-hoc regression controls help, but only for the features you think to measure. The Surge critique argues low-quality inputs cannot be "patched". [S]
2. **Preference ≠ correctness.**
   - Preference scores under-represent factuality. [V, Hosking et al.]
   - Search Arena users reward citation count while not checking the citations. [V]
   - LLM judges' preferences do not track safety or world-knowledge measures (SOS-Bench, Feuer et al., ICLR 2025). [S] [fact-check: upgraded to V. The ICLR 2025 abstract, via papercopilot, states "LLM-judge preferences do not correlate with concrete measures of safety, world knowledge, and instruction following".]
   - Real-world echo: OpenAI's 25 April 2025 GPT-4o update became sycophantic after an added thumbs-up/down reward signal and was rolled back by 28 April. [S] This shows that optimising for immediate user approval is itself a failure mode.
3. **Gaming by selective disclosure.**
   - Private best-of-N testing and retraction, and preference-tuned demo variants (Llama-4-Maverick-Experimental), mean the scored artifact is not the shipped one. [V/S]
   - Remedies adopted: explicit policy, "provisional" labels, retirement list, 100% vote-data release. [V]
4. **Adversarial manipulation of open voting.**
   - Hundreds to about a thousand votes can move ranks. [V]
   - De-anonymisation reaches >95% accuracy. [V]
   - New position and affiliation biases appeared in the 2026 formats. [S]
5. **Judge dependence and self-preference (LLM-judge proxies).**
   - Rank reversals when the judge model changes (Gemini 79.0 vs. 49.1). [V]
   - Position bias (Wang et al., ACL 2024) and self-recognition-linked self-preference (Panickssery et al., NeurIPS 2024). [S venue listings; fact-check: both venues confirmed via papercopilot `acl2024.json` / `nips2024.json` (Panickssery is an oral)]
6. **Adversarial and null-response exploits of static judge benchmarks.** A constant response reaches an 86.5% LC win rate on AlpacaEval 2.0. [V]
7. **Saturation and staleness of fixed sets.**
   - MT-Bench separability 22.6%. [V]
   - AlpacaEval-LC 87.6 and Arena-Hard 92.3 by January 2025. [V]
   - AlpacaEval and WildBench leaderboards frozen at mid-2024 models. [V]
8. **Unrepresentative, unaccountable crowds.**
   - Self-selected, anonymous, unpaid voters. Demographics are unknown to LMArena, and SEAL Showdown's pitch is exactly demographic verification [S].
   - UI-suggested prompts dominate some arenas (WebDev: 40% duplicate votes removed). [V]
   - Selection effects in which models get sampled: proprietary models are upsampled [V policy; V abstract].
9. **Relative ratings drift and are not comparable over time.**
   - BT scores are anchored to the current pool. Deprecations and a shifting prompt mix break comparability. [S Leaderboard Illusion; I]
   - A 1500 in 2026 is not "better" than a 1217 in 2023 in any absolute sense. [I]
10. **Commercial conflict of interest.** Selling evaluations to ranked labs (from September 2025) and VC funding raise neutrality questions that the platform must manage. [S]
11. **Narrow task type.** Single-turn, first-impression judgements. Critics call Arena a "one-shot vibe check", and Arena's own Agent Arena moved to causal tracing. [S]

## Implications for the new (non-game) benchmark [interpretation]

- **Keep:**
  - real, fresh prompts;
  - a single rating with CIs (BT or IRT) plus category slices;
  - a consumer-facing participation loop;
  - open data and code;
  - a named maintainer with sustainable funding.
- **Fix:**
  - Score *verifiable outcomes* (executable checks, rubric items with ground truth, reference-anchored facts), not raw "which do you like". Where preference is essential, collect it *after* verification (e.g., only among correct answers) and model style covariates in the rating.
  - Adopt the Leaderboard Illusion reforms by design:
    - pre-registration of submissions;
    - no private variants or retraction;
    - the scored checkpoint equals the shipped artifact;
    - public sampling and deprecation logs.
  - Stratify raters (verified expert panels plus crowd), with gold-question QC.
  - Use multiple judges with cross-family rotation and report judge-sensitivity.
  - Add anti-rigging defences (login, rate limits, anomaly detection).
  - Anchor ratings with fixed reference models so scores are comparable over time.

---

## Claims ledger

Confidence levels: H = high (primary source fetched), M = medium (secondary source or minor ambiguity), L = low.

1. **Chatbot Arena paper.** Chiang et al., ICML 2024, PMLR 235:8359-8388; arXiv:2403.04132. The abstract reports "over 240K votes" and calls Arena "one of the most referenced LLM leaderboards". H.
   - https://raw.githubusercontent.com/mlresearch/v235/gh-pages/_posts/2024-07-08-chiang24b.md
2. **Launch and method change.** Arena launched with a leaderboard on 3 May 2023 covering 24 April-1 May 2023 battles (vicuna-13b #1 at 1169). It moved from online Elo to Bradley-Terry MLE with bootstrap CIs in December 2023, at 130,000+ votes. H.
   - https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2023-05-03-arena.md
   - https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2023-12-07-leaderboard-elo-update.md
3. **Scale in April 2025.** LMArena reported "3M+ votes, 400+ models, and 300+ pre-release tests", 1.5M prompts released, and 20% of data shared back with model providers. H.
   - https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2025-04-27-two-year-celebration.md
4. **Company formation.** LMArena announced on 17 April 2025 that it was starting a company, promising to stay "neutral, open". H.
   - https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2025-04-17-new-beta.md
5. **Funding.** LMArena raised a $100M seed at a $600M valuation (reported 21 May 2025). It raised a $150M Series A at a $1.7B post-money valuation, led by Felicis and UC Investments (6 January 2026), with an annualized consumption run rate above $30M in December 2025. M (secondary compilation of TechCrunch and PR Newswire; not fetched directly).
   - https://techcrunch.com/2025/05/21/lm-arena-the-organization-behind-popular-ai-leaderboards-lands-100m/
   - https://techcrunch.com/2026/01/06/lmarena-lands-1-7b-valuation-four-months-after-launching-its-product/
   - https://www.prnewswire.com/news-releases/lmarena-raises-150-million-to-build-the-worlds-most-trusted-ai-evaluation-platform-302653012.html
   - Seen at https://github.com/vibewatch/startup/blob/main/reports/20260625005021-lmarena/evidence.yaml
6. **Rebrand.** The product rebranded from LMArena to "Arena" (arena.ai) in January 2026. M (multiple secondary sources).
   - https://github.com/smol-ai/ainews-web-2025/blob/main/src/content/issues/26-01-28-not-much.md
   - https://github.com/diegosouzapw/OmniRoute (code comment)
   - https://raw.githubusercontent.com/lmarena/arena-rank/main/README.md (links to arena.ai)
7. **Style control.** Style control (29 August 2024) adds length and markdown features to the BT regression. Length is the dominant style factor (coefficient 0.249 vs. ≤0.031 for markdown), and controlling for it reshuffles rankings. H.
   - https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2024-08-29-style-control.md
8. **Sentiment control.** Sentiment control (22 April 2025) finds positive and very-positive tone increase win probability. Emoji count has a small negative coefficient [corrected by fact-check]. Grok-3 and Llama-4-Maverick-Experimental drop in rank under control, and Claude-3.7 rises. H.
   - https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2025-04-22-sentiment-control.md
9. **Prompt freshness.** About 75% of daily Arena prompts are fresh (not similar to any prior-day prompt), and fewer than 1% appear in popular benchmarks (355,575 battles, May-December 2024). H.
   - https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2025-03-5-freshness.md
10. **Leaderboard Illusion core claims.** Singh et al. (arXiv:2504.20879; NeurIPS 2025 Datasets & Benchmarks poster [track added by fact-check]) report 27 private Meta variants pre-Llama-4. Google and OpenAI received an estimated 19.2% and 20.4% of arena data, vs. 29.7% for 83 open-weight models combined. Arena data gives up to 112% relative gains on ArenaHard. H (abstract text); M for body-level numbers.
    - https://raw.githubusercontent.com/stanford-cs336/spring2025-lectures/main/var/files/arxiv-5669e33cedb3be4470c98e99224a076f-http_export_arxiv_org_api_query_id_list_2504_20879
    - https://raw.githubusercontent.com/davidheineman/conference-papers/main/2025-neurips/session_3.md
11. **LMArena rebuttal.** LMArena disputed the Leaderboard Illusion: open models were 40.9% of battles, the pre-release boost is about +11 Elo after 50 tests and 3,000 votes, and the 112% figure concerns Arena-Hard, not human Arena. It committed to "provisional" labels and a retirement list. The policy now promises release of 100% of leaderboard vote data from 1 July 2025. H.
    - https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2025-05-09-our-response.md
    - https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2024-03-01-policy.md
12. **Llama-4 Maverick.** Meta's LMArena #2 entry was "Llama-4-Maverick-03-26-Experimental", "optimized for conversationality". LMArena said Meta's interpretation "did not match what we expect from model providers". The unmodified release model ranked 32nd (11 April 2025). M (secondary: The Verge, TechCrunch and Slashdot caches).
    - https://www.theverge.com/meta/645012/meta-llama-4-maverick-benchmarks-gaming
    - https://techcrunch.com/2025/04/11/metas-vanilla-maverick-ai-model-ranks-below-rivals-on-a-popular-chat-benchmark/
    - Seen via https://github.com/rumca-js/RSS-Link-Database-2025 and https://github.com/textbrowser/spot-on-shared-pages
13. **Vote rigging.** Omnipresent rigging can improve a model's Arena rank with "only hundreds of new votes" (Min et al., ICML 2025, arXiv:2501.17858). An attacker can de-anonymise responses with >95% accuracy and shift rankings with about a thousand votes (Huang et al., ICML 2025). H.
    - https://raw.githubusercontent.com/mlresearch/v267/gh-pages/_posts/2025-10-06-min25a.md
    - https://raw.githubusercontent.com/mlresearch/v267/gh-pages/_posts/2025-10-06-huang25z.md
14. **MT-Bench.** MT-Bench has 80 multi-turn questions in 8 categories, graded 1-10 by GPT-4, with GPT-4 at 8.99 in June 2023. Its separability with 95% CIs across 20 top models was only 22.6% by April 2024, vs. 87.4% for Arena-Hard-Auto v0.1 (89.1% agreement with Arena). H.
    - https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2023-06-22-leaderboard-week8.md
    - https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2024-04-19-arena-hard.md
15. **Length control.** Length-controlled AlpacaEval (COLM 2024; arXiv:2404.04475; the COLM version is titled "...A Simple Debiasing of Automatic Evaluators", by Dubois, Liang and Hashimoto [corrected by fact-check]) raised Spearman correlation with Chatbot Arena from 0.93 to 0.98 and cut length gameability from ~21% to ~6%. Prompting for verbosity or concision moves the baseline from 50% to 64% or 23%. H.
    - https://raw.githubusercontent.com/tatsu-lab/alpaca_eval/main/README.md
    - https://github.com/percyliang/refdb (venue)
16. **Null model.** A constant "null model" appears on the official AlpacaEval 2.0 leaderboard with an 86.45% LC win rate (Zheng et al., ICLR 2025, arXiv:2410.07137). H.
    - https://raw.githubusercontent.com/tatsu-lab/alpaca_eval/main/src/alpaca_eval/leaderboards/data_AlpacaEval_2/weighted_alpaca_eval_gpt4_turbo_leaderboard.csv
    - https://raw.githubusercontent.com/sail-sg/Cheating-LLM-Benchmarks/main/README.md
17. **Saturation in lab reports.** DeepSeek-R1 (January 2025) reports AlpacaEval 2.0 LC 87.6 and ArenaHard (GPT-4-1106 judge) 92.3, with o1-mini at 92.0. H.
    - https://raw.githubusercontent.com/deepseek-ai/DeepSeek-R1/main/README.md
18. **Arena-Hard v2.0 judge sensitivity.** Arena-Hard v2.0 (April 2025) uses 500 hard and 250 creative-writing prompts with GPT-4.1 or Gemini-2.5 judges. Gemini-2.5 scores 79.0 under the Gemini judge vs. 49.1 under the GPT-4.1 judge. H.
    - https://raw.githubusercontent.com/lmarena/arena-hard-auto/main/README.md
19. **Arena-Hard paper.** The Arena-Hard/BenchBuilder paper (ICML 2025, arXiv:2406.11939) claims 98.6% correlation with human preference rankings and 3x the separation of MT-Bench at a cost of $20. H.
    - https://raw.githubusercontent.com/mlresearch/v267/gh-pages/_posts/2025-10-06-li25h.md
20. **WebDev Arena.** WebDev Arena launched December 2024 and had 80,000+ votes by March 2025. Deduplicating repeated sample prompts cut votes from 103,096 to 61,473; Claude 3.7 Sonnet was #1 at 1362.94. H.
    - https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2025-03-06-webdev-arena.md
21. **Copilot Arena.** Copilot Arena (ICML 2025) served 4.5M+ suggestions from 10 models and collected 11k+ pairwise judgements. 82% of accepted completions were the top-positioned one. H.
    - https://raw.githubusercontent.com/mlresearch/v267/gh-pages/_posts/2025-10-06-chi25a.md
    - https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2024-11-12-copilot-arena.md
22. **Search Arena.** Launched 18 March 2025 with 7k filtered votes and a 24k public dataset. Users prefer longer, more-cited responses, but citations are not always accurate and humans do not check them. Paper arXiv:2506.05334, ICLR 2026 per README. H.
    - https://raw.githubusercontent.com/lmarena/search-arena/main/README.md
    - https://raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2025-04-14-search-arena.md
23. **Design Arena.** Design Arena is a YC Summer-2025 company describing itself as the "World's largest crowdsourced benchmark for AI-generated design". It uses anonymous multi-model tournaments aggregated by Bradley-Terry. M (secondary).
    - https://raw.githubusercontent.com/yc-oss/api/main/batches/summer-2025/design-arena.json
    - https://raw.githubusercontent.com/AgentsORG/design-engineering/main/skills/design-engineering/references/meta/design-benchmarks.md
24. **Surge AI audit.** Surge AI audited 500 LMArena votes and disagreed with 52% (39% strongly). M (secondary HN digest; the author has a commercial interest).
    - https://surgehq.ai/blog/lmarena-is-a-plague-on-ai (seen via https://raw.githubusercontent.com/Planeshifter/hackernews-ai-digest/main/data/digest_2026-01-07.md)
25. **Assertiveness bias.** Hosking et al. (ICLR 2024) find output assertiveness skews human-perceived factuality errors. H.
    - https://raw.githubusercontent.com/cohere-ai/human-feedback-paper/main/README.md
    - https://github.com/tomhosking/tomhosking (venue)
26. **P2L router.** The P2L router reached #1 on the Chatbot Arena leaderboard in January 2025. H (authors' own README).
    - https://raw.githubusercontent.com/lmarena/p2l/main/README.md
27. **WildBench.** 1,024 real-user tasks with checklists. WB-Reward Pearson 0.98 with Arena Elo (hard). ICLR 2025 spotlight. M (card and list are secondary; the README is primary for task format). [corrected by fact-check] Now H: the ICLR 2025 abstract and spotlight status were confirmed via papercopilot. Note that the ICLR author list omits Faeze Brahman.
    - https://raw.githubusercontent.com/allenai/WildBench/main/README.md
    - https://raw.githubusercontent.com/evaleval/eval-cards/main/metadata/benchmark_card_WildBench.json

---

## References

Primary sources were fetched as raw files this session. Secondary sources are those seen only via a cache or compilation, with the seen-at URL given.

1. Chiang, W.-L., Zheng, L., Sheng, Y., Angelopoulos, A. N., Li, T., Li, D., Zhu, B., Zhang, H., Jordan, M., Gonzalez, J. E., Stoica, I. (2024). *Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference.* ICML 2024, PMLR 235:8359-8388. arXiv:2403.04132. https://arxiv.org/abs/2403.04132. Seen at: https://raw.githubusercontent.com/mlresearch/v235/gh-pages/_posts/2024-07-08-chiang24b.md
2. Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E. P., Zhang, H., Gonzalez, J. E., Stoica, I. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.* NeurIPS 2023 Datasets & Benchmarks. arXiv:2306.05685. Seen at: FastChat README; CSHaitao/Awesome-LLMs-as-Judges.
3. Zheng, L., Sheng, Y., Chiang, W.-L., Zhang, H., Gonzalez, J. E., Stoica, I. (2023). *Chatbot Arena: Benchmarking LLMs in the Wild with Elo Ratings.* LMSYS blog, 3 May 2023. https://lmsys.org/blog/2023-05-03-arena/ (source: lmarena/lmarena.github.io `_posts/2023-05-03-arena.md`)
4. Zheng, L., Chiang, W.-L., Sheng, Y., Zhang, H. (2023). *Chatbot Arena Leaderboard Updates (Week 8): Introducing MT-Bench and Vicuna-33B.* LMSYS blog, 22 June 2023. Source: `_posts/2023-06-22-leaderboard-week8.md` [authors added by fact-check]
5. Chiang, W.-L., Li, T., Gonzalez, J. E., Stoica, I. (2023). *Chatbot Arena - New models & Elo system update.* LMSYS blog, 7 December 2023. Source: `_posts/2023-12-07-leaderboard-elo-update.md` [authors added by fact-check]
6. LMArena (2024, updated 2025). *Chatbot Arena Policy.* Blog, 1 March 2024 (current text includes 2025 updates). Source: `_posts/2024-03-01-policy.md`
7. Li, T., Chiang, W.-L., Angelopoulos, A. (2024). *Does Style Matter? Disentangling style and substance in Chatbot Arena.* Blog, 29 August 2024. Source: `_posts/2024-08-29-style-control.md`
8. Chen, C., Chiang, W.-L., Li, T., Angelopoulos, A. (2025). *Does Sentiment Matter Too? Introducing Sentiment Control.* Blog, 22 April 2025. Source: `_posts/2025-04-22-sentiment-control.md`
9. Dunlap, L., Lu, E., Gonzalez, J. E., Angelopoulos, A. N., Chiang, W.-L., Stoica, I. (2025). *How Many User Prompts are New?* Blog, 18 April 2025. Source: `_posts/2025-03-5-freshness.md`
10. LMArena Team (2025). *LMArena is Growing to Support our Community Platform.* Blog, 17 April 2025. Source: `_posts/2025-04-17-new-beta.md`
11. LMArena Team (2025). *Celebrating Community Impact: 3M+ votes, 400+ models, and 300+ pre-release tests.* Blog, 27 April 2025. Source: `_posts/2025-04-27-two-year-celebration.md`
12. LMArena Team (2025). *Our Response to "The Leaderboard Illusion" Writeup.* Blog, 9 May 2025. Source: `_posts/2025-05-09-our-response.md`
13. Singh, S., Nan, Y., Wang, A., D'Souza, D., Kapoor, S., Üstün, A., Koyejo, S., Deng, Y., Longpre, S., Smith, N., Ermis, B., Fadaee, M., Hooker, S. (2025). *The Leaderboard Illusion.* arXiv:2504.20879; NeurIPS 2025 Datasets & Benchmarks Track (poster) [track corrected by fact-check]. Seen at: cached arXiv API record in stanford-cs336/spring2025-lectures; davidheineman/conference-papers.
14. Li, T., Chiang, W.-L., Frick, E., Dunlap, L., Wu, T., Zhu, B., Gonzalez, J. E., Stoica, I. (2025). *From Crowdsourced Data to High-quality Benchmarks: Arena-Hard and BenchBuilder Pipeline.* ICML 2025, PMLR 267:34209-34231. arXiv:2406.11939. Seen at: mlresearch/v267 `li25h`; arena-hard-auto README.
15. Li, T., Chiang, W.-L., Frick, E., Dunlap, L., Zhu, B., Gonzalez, J. E., Stoica, I. (2024). *From Live Data to High-Quality Benchmarks: The Arena-Hard Pipeline.* Blog, 19 April 2024. Source: `_posts/2024-04-19-arena-hard.md`
16. lmarena/arena-hard-auto (2023-2025). GitHub repository (Arena-Hard v2.0, 23 April 2025). https://github.com/lmarena/arena-hard-auto
17. Li, X., Zhang, T., Dubois, Y., Taori, R., Gulrajani, I., Guestrin, C., Liang, P., Hashimoto, T. B. (2023). *AlpacaEval: An Automatic Evaluator of Instruction-following Models.* GitHub. https://github.com/tatsu-lab/alpaca_eval
18. Dubois, Y., Galambosi, B., Liang, P., Hashimoto, T. B. (2024). *Length-Controlled AlpacaEval: A Simple Way to Debias Automatic Evaluators.* arXiv:2404.04475. Seen at: alpaca_eval README; percyliang/refdb. [corrected by fact-check] The COLM 2024 version is Dubois, Y., Liang, P., Hashimoto, T. *Length-Controlled AlpacaEval: A Simple Debiasing of Automatic Evaluators.* First Conference on Language Modeling (COLM 2024), OpenReview CybBmzWBX0.
19. Dubois, Y., Li, X., Taori, R., Zhang, T., Gulrajani, I., Ba, J., Guestrin, C., Liang, P., Hashimoto, T. B. (2023). *AlpacaFarm: A Simulation Framework for Methods that Learn from Human Feedback.* NeurIPS 2023 (spotlight) [venue added by fact-check]. arXiv:2305.14387. Seen at: alpaca_eval README BibTeX.
20. Zheng, X., Pang, T., Du, C., Liu, Q., Jiang, J., Lin, M. (2025). *Cheating Automatic LLM Benchmarks: Null Models Achieve High Win Rates.* ICLR 2025. arXiv:2410.07137. Seen at: sail-sg/Cheating-LLM-Benchmarks; AmberLJC/Sci-Reasoning.
21. Lin, B. Y., Deng, Y., Chandu, K., Brahman, F., Ravichander, A., Pyatkin, V., Dziri, N., Le Bras, R., Choi, Y. (2025). *WildBench: Benchmarking LLMs with Challenging Tasks from Real Users in the Wild.* ICLR 2025 (spotlight). arXiv:2406.04770. [fact-check: the ICLR/OpenReview author list has 8 authors and omits Brahman, F.; the arXiv version has 9.] Seen at: allenai/WildBench README; AmberLJC/Sci-Reasoning.
22. Chi, W., Chen, V., Angelopoulos, A. N., Chiang, W.-L., Mittal, A., Jain, N., Zhang, T., Stoica, I., Donahue, C., Talwalkar, A. (2025). *Copilot Arena: A Platform for Code LLM Evaluation in the Wild.* ICML 2025, PMLR 267:10354-10382. arXiv:2502.09328. Seen at: mlresearch/v267 `chi25a`; copilot-arena README.
23. Chi, W., Chen, V., et al. (2024). *Copilot Arena: Initial Leaderboard, Insights, and a New Prompting Method for Code Completions.* Blog, 12 November 2024. Source: `_posts/2024-11-12-copilot-arena.md`
24. Vichare, A., Angelopoulos, A. N., Chiang, W.-L., Tang, K., Manolache, L. (2025). *WebDev Arena: A Live LLM Leaderboard for Web App Development.* Blog, 10 March 2025. Source: `_posts/2025-03-06-webdev-arena.md`
25. Miroyan, M., Wu, T.-H., King, L., Li, T., Pan, J., Hu, X., Chiang, W.-L., Angelopoulos, A. N., Darrell, T., Norouzi, N., Gonzalez, J. E. (2026). *Search Arena: Analyzing Search-Augmented LLMs.* ICLR 2026 (per README). arXiv:2506.05334. Seen at: lmarena/search-arena README.
26. Miroyan, M., Wu, T.-H., et al. (2025). *Introducing the Search Arena: Evaluating Search-Enabled AI.* Blog, 14 April 2025. Source: `_posts/2025-04-14-search-arena.md`
27. Frick, E., Chen, C., Tennyson, J., Li, T., Chiang, W.-L., Angelopoulos, A. N., Stoica, I. (2025). *Prompt-to-Leaderboard: Prompt-Adaptive LLM Evaluations.* ICML 2025, PMLR 267:17672-17689. arXiv:2502.14855 (arXiv title: "Prompt-to-Leaderboard"). Seen at: lmarena/p2l README; mlresearch/v267 `frick25a`. [venue and title corrected by fact-check]
28. lmarena/arena-rank (2025-2026). *Arena-Rank: The ranking methodology powering the Arena leaderboard.* GitHub. https://github.com/lmarena/arena-rank
29. Min, R., Pang, T., Du, C., Liu, Q., Cheng, M., Lin, M. (2025). *Improving Your Model Ranking on Chatbot Arena by Vote Rigging.* ICML 2025, PMLR 267:44252-44271. arXiv:2501.17858. Seen at: mlresearch/v267 `min25a`; sail-sg/Rigging-ChatbotArena.
30. Huang, Y., Nasr, M., Angelopoulos, A. N., Carlini, N., Chiang, W.-L., Choquette-Choo, C. A., Ippolito, D., Jagielski, M., Lee, K., Liu, K., Stoica, I., Tramèr, F., Zhang, C. (2025). *Exploring and Mitigating Adversarial Manipulation of Voting-Based Leaderboards.* ICML 2025 (oral), PMLR 267:25654-25671. arXiv:2501.07493 (confirmed by independent arXiv listings) [fact-check]. Seen at: mlresearch/v267 `huang25z`.
31. Hosking, T., Blunsom, P., Bartolo, M. (2024). *Human Feedback is not Gold Standard.* ICLR 2024. arXiv:2309.16349. Seen at: cohere-ai/human-feedback-paper; tomhosking/tomhosking.
32. Feuer, B., Goldblum, M., Datta, T., Nambiar, S., Besaleli, R., Dooley, S., Cembalest, M., Dickerson, J. P. (2025) [full author list added by fact-check]. *Style Outweighs Substance: Failure Modes of LLM Judges in Alignment Benchmarking.* ICLR 2025. arXiv:2409.15268. Seen at: penfever/sos-bench README; zhihengli-casia/AI-Paper-Trends.
33. Panickssery, A., Bowman, S. R., Feng, S. (2024). *LLM Evaluators Recognize and Favor Their Own Generations.* NeurIPS 2024 (oral). arXiv:2404.13076. Seen at: ihsgnef.github.io publications; CSHaitao/Awesome-LLMs-as-Judges.
34. Wang, P., Li, L., Chen, L., Cai, Z., Zhu, D., Lin, B., Cao, Y., Kong, L., Liu, Q., Liu, T., Sui, Z. (2024). *Large Language Models are not Fair Evaluators.* ACL 2024 (long). arXiv:2305.17926. Seen at: haizelabs/verdict docs. [full author list added by fact-check, from the papercopilot `acl2024.json` record]
35. DeepSeek-AI (2025). *DeepSeek-R1* (GitHub README with evaluation table). https://github.com/deepseek-ai/DeepSeek-R1
36. DeepSeek-AI (2024). *DeepSeek-V3* (GitHub README with open-ended evaluation table). https://github.com/deepseek-ai/DeepSeek-V3
37. The Verge (2025). *Meta got caught gaming AI benchmarks.* 7-8 April 2025. https://www.theverge.com/meta/645012/meta-llama-4-maverick-benchmarks-gaming. Secondary: seen via Slashdot RSS cache (rumca-js/RSS-Link-Database-2025) and vibewatch/startup evidence file.
38. TechCrunch (2025). *Meta's vanilla Maverick AI model ranks below rivals on a popular chat benchmark.* 11 April 2025. https://techcrunch.com/2025/04/11/metas-vanilla-maverick-ai-model-ranks-below-rivals-on-a-popular-chat-benchmark/. Secondary: cached text in Saryal-Saeed/Ideation-; Slashdot cache.
39. TechCrunch (2025). *Study accuses LM Arena of helping top AI labs game its benchmark.* 30 April 2025. https://techcrunch.com/2025/04/30/study-accuses-lm-arena-of-helping-top-ai-labs-game-its-benchmark/. Secondary: vibewatch/startup. [fact-check: UNVERIFIED. Seen only in this one compilation; do not cite without checking.]
40. TechCrunch (2025). *LM Arena, the organization behind popular AI leaderboards, lands $100M.* 21 May 2025. And TechCrunch (2026). *LMArena lands $1.7B valuation four months after launching its product.* 6 January 2026. Secondary: vibewatch/startup evidence file.
41. Surge AI (date unverified; discussed on HN January 2026). *LMArena is a cancer on AI.* https://surgehq.ai/blog/lmarena-is-a-plague-on-ai. Secondary: Planeshifter/hackernews-ai-digest.
42. Design Arena (2025-2026). designarena.ai (YC S25). https://www.designarena.ai/. Secondary: yc-oss/api; AgentsORG/design-engineering; Claire1217/benchmark-radar.
43. OpenAI (2025). *Sycophancy in GPT-4o: what happened and what we're doing about it* (29 April 2025) and *Expanding on what we missed with sycophancy* (2 May 2025). https://openai.com/index/sycophancy-in-gpt-4o/. Secondary: MohamedAbdallah-14/unslop research notes.
44. Scale AI (2025). *SEAL Showdown.* About 22 September 2025. https://scale.com/blog/showdown. Secondary: GaloisField2718/tldr_news (TLDR AI 23 September 2025).

---

## Verification log

Adversarial fact-check run on 2026-09-29. This session's WebSearch budget was already exhausted, as it was for the original agent. Every search call returned "web search budget used (200 of 200)". Because of that, independent checking relied on three routes:

1. **Primary files re-fetched myself** from raw.githubusercontent.com: the LMArena blog sources, the PMLR v235/v267 records, and the READMEs and CSVs.
2. **Independent conference paper lists.** papercopilot/paperlists records for ICML 2024/2025, NeurIPS 2023/2024/2025, ICLR 2024/2025/2026, COLM 2024 and ACL 2024. These give title, authors, track and oral/poster status from OpenReview.
3. **GitHub code search** for independent third-party mirrors: arXiv listing mirrors, news RSS caches and podcast transcripts.

All scratch copies are in the session scratchpad (`fc_arenas/`).

| ID | Verdict | Evidence and notes | Sources |
|---|---|---|---|
| C1 | **Confirmed** | The PMLR record gives ICML 2024 (41st ICML), pages 8359-8388, 11 authors, and an abstract containing "over 240K votes" and "one of the most referenced LLM leaderboards, widely cited by leading LLM developers and companies". Papercopilot lists it as an ICML 2024 poster. arXiv:2403.04132 has the same title and abstract (qhduan/cn-chat-arxiv mirror; FastChat BibTeX). | raw.githubusercontent.com/mlresearch/v235/gh-pages/_posts/2024-07-08-chiang24b.md; raw.githubusercontent.com/papercopilot/paperlists/main/icml/icml2024.json; github.com/qhduan/cn-chat-arxiv (papers/24/03/2403.04132.json); github.com/lm-sys/FastChat (fastchat/serve/monitor/monitor.py) |
| C2 | **Confirmed** (with nuance) | The 27 April 2025 post gives 400+ public models, 300+ pre-release tests, 1.5M prompts released, 20% of data shared back with providers, and "Tens of millions" of pairings. "3M+ votes" appears only in the post title. The 17 April 2025 post says "We are starting a company to support LMArena!" | raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2025-04-27-two-year-celebration.md; .../2025-04-17-new-beta.md |
| C3 | **Confirmed** (medium; secondary but now multi-source) | **Series A:** A Latent Space episode dated 2026-01-06 gives "$150m at a $1.7B valuation, with $30M annualized consumption revenue ... after their September eval product". A scraped copy of the Series A blog names Felicis and UC Investments as leads (plus a16z, The House Fund, LDVP, Kleiner Perkins, Lightspeed, Laude). The same text says "$100M Seed round last year in May". **Seed valuation:** $600M appears in a third-party digest (prabhic/selector-almanac) and in the vibewatch compilation; the TechCrunch pages themselves were not fetched. **Rebrand:** AINews for 28 Jan 2026 reports "LMArena rebranded to Arena (arena.ai)" and cites the blog "lmarena-is-now-arena". The arena-rank README links arena.ai. | raw.githubusercontent.com/Memories-ai-labs/ai-founder-kb/main/raw-transcripts/latent-space/state-of-evals-lmarenas-17b-vision.txt; raw.githubusercontent.com/Amal-David/docingest/main/server/storage/docs/lmarena.ai/documentation_2026-01-18T14:34:01.052Z.md; raw.githubusercontent.com/smol-ai/ainews-web-2025/main/src/content/issues/26-01-28-not-much.md; raw.githubusercontent.com/vibewatch/startup/main/reports/20260625005021-lmarena/evidence.yaml |
| C4 | **Confirmed** (with one side correction) | **Style control:** the table (control both) gives length 0.249, list 0.031, header 0.024, bold 0.019. Ranks reshuffle: GPT-4o-mini and Grok-2-mini drop; Claude 3.5 Sonnet ties #1 on Hard Prompts. **Sentiment control:** positive coefficients for positive (0.0146) and very positive (0.0285) tone. Grok-3 and Llama-4-Maverick-Experimental drop; Claude-3.7 rises. **Correction elsewhere in the dossier:** emoji count has a *negative* coefficient (-0.0039 / -0.0048), so the Summary's "emoji also raise scores" was wrong and has been fixed. | raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2024-08-29-style-control.md; .../2025-04-22-sentiment-control.md |
| C5 | **Confirmed** | The blog (dated 2025-04-18) reports 355,575 battles from May to December 2024. "Roughly 75% of the prompts collected each day are significantly different from any prompt on a previous day" (similarity threshold 0.7), and "Less than 1% of user prompts appear in popular benchmarks". | raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2025-03-5-freshness.md |
| C6 | **Confirmed** (venue refined) | The arXiv API record (v1, 29 Apr 2025) contains 27 Meta variants, 19.2% / 20.4%, 83 open-weight models at 29.7%, and "112% on the arena distribution". The NeurIPS abstract words it as "112% on ArenaHard". Papercopilot places it in the **NeurIPS 2025 Datasets & Benchmarks track, poster**. The 112% is ArenaHard win rate 23.5% to 49.9% (relative +112.3%) per a third-party summary [S]. | raw.githubusercontent.com/stanford-cs336/spring2025-lectures/main/var/files/arxiv-...2504_20879; raw.githubusercontent.com/davidheineman/conference-papers/main/2025-neurips/session_3.md; raw.githubusercontent.com/papercopilot/paperlists/main/nips/nips2025.json; github.com/gabrielchua/daily-ai-papers (archive/2025/04/30.md) |
| C7 | **Confirmed** (with nuance) | The 9 May 2025 post contains all of the following: "Open Models at 40.9%"; "around +11 Elo after 50 tests and 3000 votes"; the 112% gain on "'Arena-Hard,' a static benchmark with 500 data points that uses an LLM judge"; provisional labels (after 10+ parallel pre-release tests, until 2,000 fresh votes); and marking of retired models. The policy page says "as of July 1, 2025, we will share 100% of the arena vote data used for the public leaderboard (model identities and votes)" and "As of June 15, 2025" for the retirement list. **Nuance [I]:** 40.9% is the share of battles *involving* an open model. That is not the same metric as the paper's 29.7% data share. | raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2025-05-09-our-response.md; .../2024-03-01-policy.md; .../2025-04-27-two-year-celebration.md |
| C8 | **Confirmed** (medium; secondary, multiple independent caches) | The Slashdot RSS cache (8 Apr 2025) has the headline "Meta Got Caught Gaming AI Benchmarks", #2 behind Gemini 2.5 Pro, "experimental chat version ... optimized for conversationality", and the LMArena quote. The Slashdot cache of 13 Apr 2025 (quoting TechCrunch, "Friday") reports that the unmodified Llama-4-Maverick-17B-128E-Instruct "ranked 32nd". The Wikipedia text copy has the full LMArena quote with 'Llama-4-Maverick-03-26-Experimental'. The GPT-4o-ranks-higher detail was not seen in the caches read. | github.com/rumca-js/RSS-Link-Database-2025 (2025/04/2025-04-08 and 2025-04-13 Slashdot entries); raw.githubusercontent.com/cyrilvincent/rag/main/data/wiki/Llama_(language_model).txt |
| C9 | **Confirmed** (with nuance) | **Min et al.** (PMLR v267 min25a, pp. 44252-44271): omnipresent rigging, ~1.7M historical votes, "only hundreds of new votes"; ICML 2025 poster. **Huang et al.** (PMLR v267 huang25z, pp. 25654-25671): >95% model identification, "roughly a thousand votes (verified in a simulated, offline version of Chatbot Arena)"; ICML 2025 **oral**. arXiv:2501.07493 was confirmed by independent listings. | raw.githubusercontent.com/mlresearch/v267/gh-pages/_posts/2025-10-06-min25a.md; .../2025-10-06-huang25z.md; papercopilot icml2025.json; github.com/isLinXu/paper-list (docs/LLM/2025-01.md); github.com/sail-sg/Rigging-ChatbotArena README |
| C10 | **Confirmed** (with nuance) | **Week-8 blog:** "80 high-quality, multi-turn questions", 8 categories, GPT-4 at 8.99. The llm_judge README says "score on a scale of 10". **Arena-Hard blog, Table 1:** MT-Bench agreement with CI 26.1%, separability 22.6%; Arena-Hard-Auto v0.1 89.1% / 87.4%; 20 top models (13 Apr 2024). **Nuance:** MT-Bench's Spearman correlation was still 91.3%, and the blog prose mislabels 22.6% as "agreement" in one sentence. | raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2023-06-22-leaderboard-week8.md; .../2024-04-19-arena-hard.md; raw.githubusercontent.com/lm-sys/FastChat/main/fastchat/llm_judge/README.md |
| C11 | **Confirmed** (with reference correction) | **README:** "increases the correlation with ChatBot Arena from 0.93 to 0.98"; relative length gameability "~21% ... ~6%". **CSV:** NullModel LC 86.4578, raw 76.92. **ICLR 2025 oral** confirmed (papercopilot). **Corrections:** the COLM 2024 paper is titled "...A Simple Debiasing of Automatic Evaluators", with authors Dubois, Liang and Hashimoto only. Its abstract says 0.94→0.98, which differs from the 0.93 in the README. | raw.githubusercontent.com/tatsu-lab/alpaca_eval/main/README.md; .../weighted_alpaca_eval_gpt4_turbo_leaderboard.csv; raw.githubusercontent.com/papercopilot/paperlists/main/colm/colm2024.json; media.githubusercontent.com/media/papercopilot/paperlists/main/iclr/iclr2025.json |
| C12 | **Confirmed** | **DeepSeek-R1 README:** "AlpacaEval2.0 (LC-winrate) 87.6"; "ArenaHard (GPT-4-1106) 92.3" (o1-mini 92.0). **Arena-Hard README** (v2.0 news dated Apr 23 2025, hard prompts with style control): gemini-2.5 scores 79.0 under the Gemini-2.5 judge and 49.1 under the GPT-4.1 judge; gpt-4.1 scores 50.0 vs. 58.3. | raw.githubusercontent.com/deepseek-ai/DeepSeek-R1/main/README.md; raw.githubusercontent.com/lmarena/arena-hard-auto/main/README.md |
| C13 | **Confirmed** | **WebDev blog** (front-matter date 2025-03-10): "Since our launch ... in Dec 2024, we have collected over 80,000 community votes"; "reducing the votes from 103096 to 61473". **Copilot blog:** "82% of accepted completions were the top completion". **PMLR chi25a:** "over 4.5 million suggestions from 10 models and ... over 11k pairwise judgements". | raw.githubusercontent.com/lmarena/lmarena.github.io/main/_posts/2025-03-06-webdev-arena.md; .../2024-11-12-copilot-arena.md; raw.githubusercontent.com/mlresearch/v267/gh-pages/_posts/2025-10-06-chi25a.md |
| C14 | **Confirmed** (medium; secondary only) | **YC record (yc-oss mirror):** batch "Summer 2025", one-liner verbatim, team size 3, former name "Arcada". **Method:** the AgentsORG notes describe multi-model tournaments to a 1-4 ranking, aggregated by BT with "400 × log10(strength)". Independent repos (Geno-Claw/ai-ui-benchmark, bra1nDump/skillpack, deepakorani/chemistry-arena) corroborate YC S25, Arcada Labs, 4-model tournaments and Bradley-Terry. designarena.ai and its methodology page are unreachable, so the "per-category boards" detail rests on the AgentsORG notes. | raw.githubusercontent.com/yc-oss/api/main/batches/summer-2025/design-arena.json; raw.githubusercontent.com/AgentsORG/design-engineering/main/skills/design-engineering/references/meta/design-benchmarks.md; github.com/Geno-Claw/ai-ui-benchmark (docs/RESEARCH.md); github.com/bra1nDump/skillpack (competition.md) |

**Other corrections made inline** (each marked "[corrected by fact-check]"):

- **Emoji effect.** Emoji do not raise scores; the coefficient is negative.
- **"50 million votes".** The figure is all-modality and counted since May 2025, so it is not comparable to a text-only total.
- **P2L venue.** Published at ICML 2025 (PMLR 267:17672-17689), with a different title.
- **Leaderboard Illusion track.** NeurIPS 2025 Datasets & Benchmarks.
- **Search Arena BibTeX.** "Thirteenth" is a repo typo; the official BibTeX reads Fourteenth ICLR.
- **LC-AlpacaEval.** The COLM version has a different title and author list.
- **AlpacaFarm venue.** NeurIPS 2023 spotlight.
- **WildBench.** The ICLR author list omits Faeze Brahman; the 0.98/0.95 correlations are now upgraded to [V].
- **SOS-Bench claim.** Upgraded to [V].
- **Arena-Hard "11/14" leaderboard date.** Unreliable.
- **Style-control range.** The markdown coefficient range applies only to the control-both model.
- **Huang et al.** The attack cost was verified offline, in simulation.
- **Vote-data release.** Means model identities and votes, not prompts.
- **Sara Hooker/TechCrunch quote.** Unverified.

**Claims I could not independently confirm (left as [S] or [U]):**

- **Arena scores reported only in newsletters:** Gemini 3 Pro 1501/1487 (Nov 2025), Gemini-3.1-Pro 1500, claude-opus-4-6 1504, Claude Opus 5 "factuality on", Kimi K3 1679.
- **Arena's 2026 product and changelog items:** the May 2026 changelog position/affiliation biases, Agent Arena "causal tracing" (June 2026), and the September 2025 "250M+ conversations / 2M+ monthly votes / 3M+ monthly users" figures. These are seen only in the vibewatch compilation.
- **Grokipedia's 5,430,034-vote count.**
- **Design Arena's adoption claims:** GLM-5.2 "#1" and Inkling 1257. The Inkling figure was also recorded in Claire1217/benchmark-radar, which is secondary.
- **Leaderboard Illusion body numbers other than 243/205/~2M/42:** 64% open among silent removals, 7.3% prompt reuse, and MMLU 66.5→64.4.
- **Sycophancy rollback timing:** "by 28 April" (secondary).
- **Surge AI audit:** the blog's publication date is unknown.

**Reference check summary.**

- **Coverage:** 44 of 44 references checked, none skipped. Of these, 43 are marked `verified: true` and 1 `verified: false`: techcrunch2025study, seen only in the vibewatch compilation.
- **No fabricated references were found.** Every arXiv ID, PMLR page range and conference venue that was checked exists and matches its title.
- **Metadata corrections written to the JSON:**
  - frick2025p2l: title and venue changed to ICML 2025, PMLR 267:17672-17689;
  - dubois2024lcalpacaeval: COLM title and author discrepancy noted in the venue field;
  - dubois2023alpacafarm: venue set to NeurIPS 2023;
  - singh2025leaderboardillusion: D&B track added;
  - huang2025adversarialleaderboards, panickssery2024selfpreference and zheng2025cheating: oral status added;
  - miroyan2026searcharena: poster status added;
  - feuer2025styleoutweighs and wang2024notfair: full author lists added;
  - lmsys2023mtbenchblog and lmsys2023btupdate: authors added;
  - lin2025wildbench: author-list caveat added.
- **References that rest on secondary sources only**, with verify_note saying so: the Verge, TechCrunch, OpenAI sycophancy and SEAL Showdown items.

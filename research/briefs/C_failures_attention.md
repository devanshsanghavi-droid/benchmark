# Brief C: Why benchmarks fail, and what earns attention

Evidence brief compiled 2026-09-29 from four fact-checked dossiers: `notes/user_failed_a.md`, `notes/user_failed_b.md`, `notes/other_dead_benchmarks.md` and `notes/virality_consumer.md`. Keys in [brackets] point to `research/refs/<dossier>.json`; where a work has keys in several files (GTBench: [duan2024gtbench] = [gtbench2024]), one is used. The LLM Chess key [saplin2025llmchess] keeps its name although the first author is Kolasani. Fact-checked text overrides dossier bodies. Facts without a refs key carry a URL or, for GitHub search counts, a dossier ledger pointer.

Confidence ratings:

- **H:** a primary source, or two agreeing independent copies.
- **M:** a single mirror, or a consistent secondary source.
- **L:** a single AI-generated digest, or unverified.

Star and commit counts are snapshots from 2026-09-29. No paper in these dossiers had an observable citation count.

---

## Headline findings

1. **Most benchmarks fail, and being adopted does not keep one alive.**
   - Ott et al. curated 3,765 computer-vision and NLP benchmarks and found that "many benchmarks fail to find widespread utilization" [ott2022mapping].
   - Koch et al. found usage concentrating on fewer datasets, drawn from "a small number of elite institutions" [koch2021reduced]. A secondary summary puts more than 50% of usages at 12 institutions [ruder2022highlights].
   - For LLMs: about 445 benchmark papers appeared at six top venues in 2018-2024 [bean2025measuring]. Over roughly the same era, 61 frontier-developer reports (Jan 2022 to Nov 2025) mention only 190 benchmarks between them [akhtar2026plateau], and only a few tens recur across reports. That last figure is an order-of-magnitude reading; nobody has measured a reuse rate.
   - Adoption is no protection: 29 of Akhtar et al.'s 60 widely used benchmarks are highly saturated [akhtar2026plateau], and the Open LLM Leaderboard (13 Mar 2025), BIG-bench (17 Apr 2026) and HELM (1 Jun 2026) were retired, archived or frozen [openllm2025retired; srivastava2023bigbench; helm2026maintenance].

2. **None of the lead's ten became a leaderboard people use, but they failed in different ways.** "Boring game" is rarely the cause that mattered.
   - *Clear failures*, with no ladder and no uptake: Qi Town [zhou2025qitown] and Game Reasoning Arena [graRepo2025].
   - *Survived as components*: MastermindEval, as six lm-evaluation-harness tasks [lmevalMastermind], and Hakimov et al.'s Codenames, as one game in the maintained clembench ladder [clembenchRepo].
   - *Too young to call*: Concept, just accepted at Findings of ACL 2026 [gevers2026concept]; TopoBench [maniparambil2026topobench]; BloomQA [chen2026bloomqa].
   - For items 6-10, lack of headroom killed none of them. What stalled them was missing artifacts, frozen or absent leaderboards, frontier-model exclusion and poor discoverability.

3. **Distribution matters more than design.**
   - Both survivors plugged into channels that someone else already maintained.
   - The standalone academic game benchmarks went quiet when the paper cycle ended:
     - GTBench: last commit 6 Sep 2024, and its submission leaderboard still reads "Will be ready soon" [duan2024gtbench].
     - GameBench: last commit 27 Jun 2024 [costarelli2024gamebench].
     - SmartPlay: archived 1 Jul 2026 [wu2024smartplay].
     - Grid-games: last model added 19 Jul 2024 [researchoutcome2024llmgamebenchmark].

4. **In a crowded niche, an incumbent's arrival decides the outcome.**
   - Kaggle Game Arena launched on 4 Aug 2025 [google2025gamearena]. That is the day the Game Reasoning Arena repo was created [graRepo2025] and one day before Qi Town reached arXiv [zhou2025qitown]. It is built on the same OpenSpiel engine as Game Reasoning Arena [deepmind2025gamearenarepo].
   - GitHub search returns 173 repos for "llm game benchmark" and 49 for "codenames llm" (GitHub search API, 2026-09-29; `user_failed_a` ledger 16).

5. **No game benchmark has entered the mainstream reporting canon.**
   - None of Akhtar et al.'s 60 benchmarks is game-based [akhtar2026plateau], although their text-only and leaderboard filters may have screened some out.
   - Labs' own game showcases are explicitly not decision-relevant. From Anthropic's Claude Plays Pokémon video, probably spoken by the project engineer: "I don't think anybody's making their buying decision for a model on which model plays Pokemon the best" [anthropic2025pokemon].

6. **Attention and adoption are separate outcomes with separate drivers.**
   - Attention came from shareable artifacts, human-legible units, recurring "moments" and appearances in lab launch tables. It did not require a leaderboard. The pelican test began as a joke with no ladder and still reached a Google I/O keynote and a GPT-5 launch video [willison2024pelicans; willison2025yearinllms].
   - Lasting use by practitioners also required a measurable ladder with headroom, plus someone to maintain it.

7. **The lead's three-part hypothesis (philosophy, leaderboard, fun) is half right.**
   - Philosophy predicts longevity and legitimacy more than initial virality. ARC kept one thesis through three versions (ARC-AGI-1, 2 and 3) [chollet2025arcprize2024; arcprize2026docs].
   - "Fun" is better restated as "stakes plus story". HLE and METR's time horizon are not fun, yet both are highly visible [cais2026hle; kwa2025metr].
   - The hypothesis misses four factors: human-legible units, a lab-adoption loop, recurring moments and shareable artifacts.

8. **Viral tests lose validity over time.**
   - The pelican test was created on 25 Oct 2024. By 16 Jul 2026 its creator wrote of its link to model quality: "That connection has been mostly severed now" [willison2024pelicans; willison2026kimik3].
   - About six months after ARC-AGI-3's release, a model scored 99.9% on it with a custom harness, against 62.7% with the default harness (https://arcprize.org/blog/astra, as quoted by Willison).
   - Practitioners describe "general apathy and loss of trust in benchmarks" [karpathy2025review].

9. **The evidence rejects some of the lead's critiques and supports others.**
   - *Rejected:* memorisation as MastermindEval's main threat (instances are procedurally generated; the real problem is that a short program solves them) [golde2025mastermindeval]; Concept as "Chutes and Ladders" (the human-model gap exceeds 50 points) [gevers2026concept]; grid-game models "maxing out instantly" [topsakal2024grid]; TopoBench as "very simple" (hard-tier accuracy 0.15) [topobench2026projectpage].
   - *Supported:* install friction, fragmented scores, pre-emption, too-small N (Boardwalk) and generator echo-chamber risk.

---

## Success factors (with evidence)

**S1. A distribution channel built in from day one (strong).**
- MastermindEval was merged into EleutherAI lm-evaluation-harness as 6 tasks on 18 Mar 2025 [lmevalMastermind]. Its repo had 10 stars and was still receiving commits in Aug 2026 [mastermindRepo].
- Codenames entered clembench v2.0 in Mar 2025, inside a maintained ladder that shipped v2.0 and v3.0 [clembenchRepo; chalamalasetti2023clembench].
- When HELM froze, its maintainers pointed users to harnesses: Evalchemy, Inspect, Lighteval, LM Evaluation Harness and Unitxt [helm2026maintenance].
- Even a training-time probe picked up practitioner uptake through a guide: the AI Alliance's AI Application Testing guide cites it [aialliance2025apptesting].

**S2. A named maintainer and a refresh cadence (strong).** Survival tracks maintenance, not choice of game:
- LLM Chess has 1,430 commits, 52 of them since 1 Jun 2026. It added the Komodo Dragon engine after reasoning models "saturated random-based evaluations" [saplin2025llmchess; llmChessRepo].
- clembench has commits through 15 Apr 2026 [chalamalasetti2023clembench].
- BALROG has commits through 9 Apr 2026 [paglieri2025balrog].
- Kaggle Game Arena added poker and Werewolf on 2 Feb 2026 [kelly2026gamearena].
- The Elimination Game reached 61 models, including GPT-5.2 and Claude Opus 4.5, then paused after 6 Jan 2026 [eliminationGameRepo].

BetterBench scores maintenance as the second-weakest lifecycle stage (mean 9.6; secondary) [reuel2024betterbench].

**S3. One headline number with uncertainty, plus diagnostics (moderate to strong).**
- Kaggle reportedly replaced "juggling separate Elo ratings, win rates, and poker statistics" with a unified leaderboard. This rests on a single source [gigazine2026gamearena; winbuzzer2026gamearena].
- The 23-task BIG-Bench Hard outlived the 200-plus-task BIG-bench [suzgun2023bbh; srivastava2023bigbench]. BBH is in Akhtar et al.'s set and remains unsaturated [akhtar2026plateau].
- Hardt: "model *rankings* — rather than model *evaluations* — are the primary scientific export" of benchmarks [hardt2025siam].
- Arena adopted Elo explicitly for "Scalability", "Incrementality" and "Unique order" [zheng2023arenablog].

**S4. A large gap to a human anchor (strong for legitimacy).**
- Concept: humans succeed more than 90% of the time, and no evaluated LLM exceeds 40% [gevers2026concept].
- ARC-AGI-2: "every task ... has been solved by at least 2 humans in under 2 attempts", while "Pure LLMs score 0%" [kamradt2025arcagi2].
- MindTopo: the best model, GPT-5.6-Sol, scores 61.42% against 97.87% for humans [mindtopo2026].
- ARC-AGI-3 scores AI actions against the "upper median" first-time human [arcprize2026docs].

**S5. A unit ordinary people can read (moderate; case-based).**
- METR expresses ability in hours of human work, "doubling approximately every 7 months" [kwa2025metr].
- Vending-Bench uses dollars of net worth [backlund2025vending].
- Arena borrowed Elo "from chess and other competitive games" [zheng2023arenablog].
- HLE borrows the exam metaphor: "the final closed-ended academic benchmark of its kind" [cais2026hle].

**S6. Lab launch tables and neutral verification (strong, for attention).**
- Four frontier labs (Anthropic, Google DeepMind, OpenAI and xAI) reported ARC-AGI in 2025 model cards, per the organisers [arcprize2026report2025].
- Google's Gemini 3 Pro launch table printed HLE (37.5% without tools), ARC-AGI-2 (31.1%, labelled "ARC Prize Verified") and Vending-Bench 2 ($5,478.16) side by side [willison2025gemini3].
- The "Verified" label is itself a trust device.

**S7. Paying participants, plus recurring moments (moderate).**
- *Prizes and co-authorship:*
  - ARC Prize 2024 drew 1,430 teams and 17,789 entries [chollet2025arcprize2024].
  - HLE offered a $500K prize pool plus co-authorship to question writers [cs336lecture12].
- *Access:* Arena users say they value "frequent access to the best models, and being a part of the first to access the newest ones" [lmarena2025twoyear].
- *Moments:* ARC ran for about five years before o3's 75.7% (20 Dec 2024) made it a headline [chollet2024o3arc].

**S8. Artifacts people share and failure stories (moderate; drives attention only).**
- Anyone can judge a pelican SVG in a second [willison2025sixmonths].
- Project Vend's tungsten-cube orders and "we would not hire Claudius" spread widely [anthropic2025projectvend].
- AI Diplomacy (707 stars) ships a Twitch streamer module and a 3D visualiser [aiDiplomacyRepo].
- Kaggle's chess launch had commentary from Magnus Carlsen and Hikaru Nakamura (secondary; https://github.com/smol-ai/ainews-web-2025).

**S9. Renewable, parametric, controlled item generation (moderate).**
- MastermindEval scales difficulty through code length, colours and guesses, and added larger boards in Aug 2026 [golde2025mastermindeval; mastermindRepo].
- Hakimov et al. manipulate concreteness, ambiguity, frequency and opponent speed, which turns a score into a diagnostic [hakimov2025codenames].
- TTT-Bench's *novel* games leave reasoning models on average 41% below their MATH 500 scores [mishra2025tttbench].

**S10. A thesis-bearing name, versioned under a stable brand (moderate).** ARC was "later renamed ARC-AGI to avoid name collisions with other AI benchmarks" [chollet2025arcprize2024]. HLE's brand carried launch tables, while *Nature* published it under a sober title [cais2026hle]. Ott et al.'s correlates of popularity are "versatility, breadth and real-world utility" [ott2022mapping].

---

## Failure factors (with evidence)

**F1. Maintenance stops or the leaderboard is abandoned (strong).**
- Game Reasoning Arena: repo created 4 Aug 2025, last commit on main 11 Sep 2025, 9 stars [graRepo2025].
- Grid-games: invited "submissions of results from other LLMs", but none arrived. Its last model was gpt-4o-mini (19 Jul 2024), so it has no o1/o3, R1 or GPT-5 entries [researchoutcome2024llmgamebenchmark].
- Stars do not prevent stalling: lmgame-Bench has 983 stars and no commits since 12 Sep 2025 [hu2025lmgame]. MC-Bench's newest update is 30 Sep 2025 [mcbench].

**F2. Missing or partial artifacts (strong).**
- TopoBench's advertised repo is empty ("This repository is empty"). Its only issue, "Release TopoBench on Hugging Face", has been open since 13 Mar 2026 [mayug2026topobenchrepo].
- Boardwalk's repo holds the API but no evaluator or outputs [labcraig2025boardwalkrepo].
- GitHub search found no public code for Qi Town [zhou2025qitown].
- BetterBench: 17 of 24 benchmarks lack an easy replication script (secondary) [reuel2024betterbench].

**F3. Pre-emption, incumbency and a crowded niche (strong in hot niches).**
- Kaggle Game Arena against Game Reasoning Arena and Qi Town (same week, same engine) [google2025gamearena; graRepo2025].
- GTBench came out in Feb 2024, five months before the grid-games paper, and already included Tic-Tac-Toe and Connect-4 [gtbench2024].
- Stephenson et al.'s Codenames benchmark was submitted on 16 Dec 2024, about two months before Hakimov et al. [stephenson2024codenames; hakimov2025codenames].
- PUZZLES already contains five of TopoBench's six puzzle families. Enigmata and Reasoning Gym also precede it [puzzles2024; enigmata2025; reasoninggym2025].
- Code World Models appeared about six weeks after Boardwalk and *overshadowed* it; it did not pre-empt it [lehrach2025cwm].
- Counter-case: MastermindEval's "pre-emption" is weak. Its repo (15 Nov 2024) predates Bulls-and-Cows (26 Nov 2024) [mastermindRepo; bullsCowsRepo].

**F4. No single comparable score, or scores that depend on the model pool (moderate).**
- Qi Town reports three unrelated measures: Elo, a Performance Loop Graph and a "Positive Sentiment Score" [zhou2025qitown].
- Grid-games splits results by 3 games, 3 prompt types and 2 seats, and reports wins, disqualifications and invalid moves as win rates within a changing pool [topsakal2024grid].
- HELM had fragmented into many leaderboards before it froze [helm2026maintenance].

**F5. Friction, and metrics that need model internals (moderate).**
- Game Reasoning Arena requires a conda environment, a separate OpenSpiel clone plus `./install.sh`, and keys for four providers [graRepo2025].
- SmartPlay needs MineDojo [wu2024smartplay], and Mindcraft needs licensed Minecraft clients [white2025mindcraft].
- The raw-corpora benchmark scores by token rank, which needs logits. Every model it evaluates is open-weight [sharma2025rawcorpora].

**F6. Frontier models excluded, or a roster that is instantly stale (moderate).**
- Qi Town's top model was Gemini 2.0 Flash (M) [zhou2025qitown].
- TopoBench's top closed model was GPT-5-mini [maniparambil2026topobench].
- The raw-corpora benchmark evaluates only models of 8B parameters or fewer [sharma2025rawcorpora].
- Boardwalk tested three 2025 models [becker2025boardwalk].
- Concept tested 7 models, including GPT-4.1-mini (L). It should be cited as "no *evaluated* model" [gevers2026concept].

**F7. Small N and no uncertainty (moderate).**
- Akhtar et al. find that small test sets saturate sooner [akhtar2026plateau].
- About 16% of 445 benchmarks use statistical tests (secondary) [bean2025measuring], and 14 of 24 report no uncertainty [reuel2024betterbench].
- TopoBench's 50 items per cell give roughly ±12-14 pp.
- Boardwalk's roughly 36 trials give about ±16 pp around 55.6%. This is an illustrative calculation [becker2025boardwalk].

**F8. Construct problems (moderate).**
- *Tool-solvability:* Mastermind with 4 positions and 6 colours has 6^4 = 1,296 codes, so brute force solves it [golde2025mastermindeval].
- *Perception confounded with strategy:* with image prompts, Tic-Tac-Toe disqualification rates reached 46.67% and 53.33% [topsakal2024grid].
- *Knowledge is not expertise:* this is the construct gap in the raw-corpora benchmark [sharma2025rawcorpora].
- *Assigned Bloom labels:* these may explain BloomQA's "Analyze > Remember" inversion [chen2026bloomqa].
- *A self-reported "mental state" metric:* Qi Town's Positive Sentiment Score [zhou2025qitown].

**F9. Hard to find: name collisions, retitling, venue and licence (weak to moderate).**
- TopoBench collides with a 256-star topological deep learning library of the same name [topobenchTDL2024].
- MastermindEval collides with opendilab's MasterMind [opendilabMastermind].
- Game Reasoning Arena was "Board Game Arena" in v1 [cipolinakun2025gra]; the raw-corpora paper was "Beyond Benchmarks" in v1 [sharma2025rawcorpora].
- Game Reasoning Arena's README states CC BY-NC 4.0, while its badge says MIT [graRepo2025].

**F10. Fast saturation, including in game formats and "live" benchmarks (strong).**
- Bulls-and-Cows' final commit (1 Feb 2025) reads "o3-mini saturated the benchmark...." [bullsCowsRepo].
- LiveBench has S_index 0.99 at about 79% accuracy [akhtar2026plateau].
- Private test sets showed similar saturation to public ones (4 private vs 56 public) [akhtar2026plateau].

**F11. Label and scoring errors (strong where present).**
- A normalisation and stop-token bug left most models under 10 F1 on DROP, and Hugging Face removed it [hf2023drop].
- Northcutt et al. found at least 3.3% label errors across 10 test sets [northcutt2021pervasive].
- 57% of the MMLU Virology questions analysed contain errors [gema2024mmlu].

**F12. No link to decisions users actually make (moderate).**
- Nobody buys a model because it plays Pokémon well [anthropic2025pokemon].
- Zuckerberg: Arena-style benchmarks are "often not actually what any normal person does in your product" (https://www.dwarkesh.com/p/mark-zuckerberg-2).
- Community members questioned chess "as a true test of intelligence" (secondary; https://github.com/smol-ai/ainews-web-2025), which supports the lead's "skills no product needs" critique for games generally.

**F13. Gaming, and loss of trust in popular signals (moderate).**
- Karpathy: "Training on the test set is a new art form" [karpathy2025review].
- A leaderboard invites adaptive overfitting to its holdout [blum2015ladder].
- In OpenAI's sycophancy incident, thumbs-up/down feedback "can sometimes favor more agreeable responses" [openai2025sycophancy].
- A benchmark run by one lab raises the question of whether its operator's own models are favoured. On Game Arena, Gemini 3 held the top chess Elo [kelly2026gamearena].

---

## Quantitative facts worth citing

| Fact | Number | Date | Source key | Conf. |
|---|---|---|---|---|
| Benchmarks curated; many "fail to find widespread utilization" | 3,765 (journal version; arXiv v1 had 1,688) | 2022 | ott2022mapping | H |
| Dataset usage concentrated at elite institutions | >50% of usages from 12 institutions | 2021 | koch2021reduced; ruder2022highlights | M |
| LLM benchmark papers at six top venues | ~445 (29 expert reviewers) | 2018-2024 | bean2025measuring | H |
| Benchmarks using statistical tests | ~16% | 2025 | bean2025measuring | M |
| Developer reports vs benchmarks mentioned | 61 reports; 190 benchmarks | Jan 2022-Nov 2025 | akhtar2026plateau | H |
| Widely used benchmarks highly saturated | 29 of 60 (14 very high) | 2026 | akhtar2026plateau | H |
| Adoption proxies vs saturation (age-controlled) | citations ρ = 0.22 (p = 0.12); report frequency ρ = 0.05 (p = 0.73) | 2026 | akhtar2026plateau | H |
| "Live" benchmark saturation | LiveBench S = 0.99 at ~79%; LiveCodeBench 0.77 | 2026 | akhtar2026plateau | H |
| BetterBench gaps | 17/24 no replication script; 14/24 no uncertainty | 2024 | reuel2024betterbench | M |
| Label errors in classic test sets | ≥3.3% average (10 sets); ≥6% ImageNet validation | 2021 | northcutt2021pervasive | H |
| MMLU Virology error rate | 57% of analysed items | 2024-25 | gema2024mmlu | H |
| DROP scoring failure | most models <10 F1; full update took "8 years of GPU time" | 1 Dec 2023 | hf2023drop | H |
| BIG-bench vs its distillate | >200 tasks archived; BBH keeps 23 | 17 Apr 2026 | srivastava2023bigbench; suzgun2023bbh | H |
| HELM freeze | no new evaluations after | 1 Jun 2026 | helm2026maintenance | H |
| Kaggle Game Arena launch vs GRA repo creation | same day | 4 Aug 2025 | google2025gamearena; graRepo2025 | H |
| Game Reasoning Arena repo | 9 stars; last main commit 11 Sep 2025 | 2026-09-29 | graRepo2025 | H |
| Qi Town design | 20 LLMs, 5 games, 2,850 matches (190 pairs × 5 × 3) | Aug 2025 | zhou2025qitown | M |
| MastermindEval in lm-eval harness | 6 tasks | 18 Mar 2025 | lmevalMastermind | H |
| Bulls-and-Cows saturation | "o3-mini saturated the benchmark" (236 stars) | 1 Feb 2025 | bullsCowsRepo | H |
| Concept human-LLM gap | humans >90%; no evaluated LLM >40% | Oct 2025 | gevers2026concept | H |
| Codenames best model (single source) | o3-mini ~49% (clemscore 49.2) of 14 models | 2025 | hakimov2025codenames | L |
| Codenames and game repo crowding | 49 "codenames llm"; 173 "llm game benchmark" | 2026-09-29 | GitHub search API (user_failed_a ledger 16) | H |
| Grid-games leaderboard freeze | 2,310 matches; last model 19 Jul 2024; 25 stars | 2024 | topsakal2024grid; researchoutcome2024llmgamebenchmark | H |
| TTT-Bench novel-game drop | −41% vs MATH 500; −5% vs AIME 2024 | 2025 | mishra2025tttbench | H |
| Boardwalk result | Claude 3.7 Sonnet 55.6% error-free, 12 games, 3 LLMs; repo 2 stars | 2025 | becker2025boardwalk; labcraig2025boardwalkrepo | H |
| TopoBench difficulty | frontier trio 0.58 / 0.38 / 0.15 (easy/medium/hard); 900 items, 50 per cell | Mar 2026 | topobench2026projectpage | H |
| TopoBench name-collision library | 256 stars, 113 forks | 2026-09-29 | topobenchTDL2024 | H |
| MindTopo human-model gap | 61.42% vs 97.87% human | Sep 2026 | mindtopo2026 | H |
| Raw-corpora validation | r = 0.99, p < 0.001, N = 6 base models | 2026 (v3) | sharma2025rawcorpora | H |
| Academic game benchmark dormancy | GTBench 6 Sep 2024; GameBench 27 Jun 2024; SmartPlay archived 1 Jul 2026 | 2024-26 | duan2024gtbench; costarelli2024gamebench; wu2024smartplay | H |
| Stars ≠ survival | lmgame-Bench 983 stars, last commit 12 Sep 2025; clembench games repo 5 stars, alive | 2026-09-29 | hu2025lmgame; clembenchRepo | H |
| Community ladders that lasted | LLM Chess 1,430 commits; AI Diplomacy 707 stars; Elimination Game 61 models | 2026 | saplin2025llmchess; aiDiplomacyRepo; eliminationGameRepo | H |
| Gemini Plays Pokémon runs | 813 h (Exp 03-25, harness modified) vs 406.5 h (Preview 05-06) | 2025 | gemini2025report | H |
| ARC prize history | $20K (2020); $100K (2022, 2023); $600K grand prize unclaimed (2024) | 2020-24 | chollet2025arcprize2024 | H |
| ARC Prize participation | 1,430 teams / 17,789 entries (2024); 1,455 / 15,154 (2025) | 2024-25 | chollet2025arcprize2024; arcprize2026report2025 | H |
| o3 on ARC-AGI-1 | 75.7% ($10K limit); 87.5% (172× compute) | 20 Dec 2024 | chollet2024o3arc | H |
| Labs reporting ARC-AGI in model cards | 4 (Anthropic, GDM, OpenAI, xAI) | 2025 | arcprize2026report2025 | M |
| ARC-AGI-3 harness effect | 99.9% ($19K, provider harness) vs 62.7% ($26K, default) | Sep 2026 | https://arcprize.org/blog/astra (via Willison) | M |
| Arena growth | 4.7K votes in week one → 3M+ votes, 400+ models, 300+ pre-release tests | 2023 → Apr 2025 | zheng2023arenablog; lmarena2025twoyear | H |
| LMArena funding | $100M at $600M; $150M at $1.7B | May 2025; Jan 2026 | techcrunch2026lmarena | M |
| Gemini 3 Pro launch table | HLE 37.5% (no tools); ARC-AGI-2 31.1%; Vending-Bench 2 $5,478.16 | 18 Nov 2025 | willison2025gemini3 | H |
| METR headline | time horizon doubles ~every 7 months; Claude 3.7 Sonnet ~50 min | Mar 2025 | kwa2025metr | H |
| HLE incentives | $500K prize pool + co-authorship; 2,500 questions | 2025 | cs336lecture12; cais2026hle | H |
| Pelican keynote tournament | 34 images, 560 matches, ~18 cents | 6 Jun 2025 | willison2025sixmonths | H |
| Pelicanmaxxing test | 1,008 SVGs, 7 models; smallest p = 0.25 | 18 Jul 2026 | castillo2026pelicanmaxxing | H |

---

## Case vignettes

**1. Same week, same engine: Game Reasoning Arena and Kaggle Game Arena.**
- On 4 Aug 2025, LAION and Jülich published a blog post and created the repo for "Board Game Arena", later renamed Game Reasoning Arena [laion2025grablog; graRepo2025].
- The same day, Google DeepMind and Kaggle launched Game Arena on the same OpenSpiel substrate [google2025gamearena; deepmind2025gamearenarepo]. Its chess exhibition drew chess.com coverage and grandmaster commentary [chesscom2025kaggleday3].
- Game Reasoning Arena asked users for conda, an OpenSpiel build and four API keys. Its README text states a non-commercial licence. Commits stopped on 11 Sep 2025 at 9 stars [graRepo2025].
- Game Arena added poker and Werewolf in Feb 2026 and published a technical report with about 62 authors in Sep 2026 [kelly2026gamearena; gamearena2026report].
- Qi Town reached arXiv the next day. It had no code that GitHub search could find [zhou2025qitown].

**2. Surviving by joining a harness: MastermindEval.**
- MastermindEval was a workshop paper with no leaderboard [golde2025mastermindeval].
- Eleven days after the arXiv release, its first author merged six tasks into lm-evaluation-harness [lmevalMastermind]. The authors were still committing in Aug 2026, adding larger boards [mastermindRepo].
- Its community sibling, the Bulls-and-Cows leaderboard, had 236 stars and Wilson intervals. Its last commit is titled "o3-mini saturated the benchmark...." [bullsCowsRepo].
- The lesson: harness integration gives a benchmark a long afterlife, while a popular game ladder can saturate in ten weeks.

**3. The empty repository: TopoBench.**
- TopoBench had real headroom: the three frontier models averaged 0.15 on hard puzzles [topobench2026projectpage]. It also ran a thoughtful causal error analysis [maniparambil2026topobench].
- Six months on, the code-and-data repo named in its abstract is still empty, and a request to publish it on Hugging Face has gone unanswered [mayug2026topobenchrepo].
- Searching the name surfaces a 256-star topological deep learning library first [topobenchTDL2024].
- Meanwhile MindTopo arrived with 11,030 instances and a human baseline [mindtopo2026].

**4. The leaderboard that stopped: grid-based game competitions.**
- The authors ran 2,310 matches and invited the community to submit more models [topsakal2024grid].
- None came. The last model added was gpt-4o-mini on 19 Jul 2024, just as reasoning models arrived [researchoutcome2024llmgamebenchmark].
- GTBench had already covered Tic-Tac-Toe and Connect-4 at NeurIPS [gtbench2024].
- The games were not saturated. Invalid moves and disqualifications were common with image prompts [topsakal2024grid]. What the benchmark lacked was a maintainer and a solver-referenced score.

**5. The pelican: from joke to keynote to "severed".**
- Simon Willison created the pelican test on 25 Oct 2024 because no such SVGs "might have already been sucked into the training data" [willison2024pelicans].
- It reached Karpathy's Grok 3 vibe check [willison2025grok3karpathy], the Google I/O keynote, a GPT-5 launch video and an Anthropic paper [willison2025yearinllms].
- An OpenAI researcher said "we do not hill climb on svg art" [willison2025trainpelicans].
- By Jul 2026 its creator said the link to utility was "mostly severed" [willison2026kimik3]. A 1,008-SVG factorial study found no pelican-specific boost, but could not detect class-level "SVGmaxxing" [castillo2026pelicanmaxxing].
- The test spread with no leaderboard at all.

**6. Five quiet years, then one moment: ARC.**
- ARC ran prize competitions from 2020, with $20K and then $100K purses [chollet2025arcprize2024].
- It was renamed ARC-AGI and relaunched with a $600K grand prize, drawing 1,430 teams [chollet2025arcprize2024].
- It became a headline when o3 scored 75.7% on 20 Dec 2024. Chollet noted GPT-family models had taken four years to go from 0% to 5% [chollet2024o3arc].
- By 2025, four labs printed ARC-AGI in their model cards [arcprize2026report2025].
- Its durability now depends on the harness. On ARC-AGI-3, one model scored 99.9% with a custom harness against 62.7% with the default (https://arcprize.org/blog/astra).

**7. A showcase is not a benchmark: Pokémon.**
- An independent developer ran Gemini Plays Pokémon and modified the harness "as difficulties arose". The first run took 813 hours; a second run, with a fixed harness *and* a newer checkpoint, took 406.5 hours [gemini2025report].
- The Anthropic engineer behind Claude Plays Pokémon (probable attribution) said nobody picks a model on this basis: "this is really for our own understanding" [anthropic2025pokemon].

**8. Flagship infrastructure dies too.** HELM stopped adding evaluations on 1 Jun 2026 [helm2026maintenance]. BIG-bench's 200-plus crowdsourced tasks were archived while its 23-task hard subset survived [srivastava2023bigbench; suzgun2023bbh]. A normalisation bug scored most models under 10 F1 on DROP until Hugging Face pulled it [hf2023drop]; the Open LLM Leaderboard itself was retired in Mar 2025 [openllm2025retired].

---

## Tensions and disagreements in the evidence

1. **The lead's "uninteresting games" diagnosis versus infrastructural causes.** For items 6-10 the dossier concludes that "lack of headroom was not the killer for any of these five" (see TopoBench at 0.15 and grid-game disqualifications) [topobench2026projectpage; topsakal2024grid]. The lead is still right in a narrower sense: we found no evidence that practitioners choose models by game rank, even for Kaggle Game Arena (secondary), and a lab engineer disowned game results as a basis for buying decisions [anthropic2025pokemon].

2. **Is a leaderboard necessary?**
   - *No, for attention:* the pelican and strawberry tests had none [willison2024pelicans; fu2024countletters].
   - *No, for survival:* MastermindEval survives without one through the harness [lmevalMastermind].
   - *Yes, for lab adoption and climbing:* Hardt calls rankings the main export [hardt2025siam], and Orr & Kang trace benchmarking's competitive epistemology [orr2024sport].

3. **Popularity does not protect against saturation.**
   - Controlling for age, citations and report frequency do not predict saturation [akhtar2026plateau].
   - Game Arena's report claims its format prevents saturation [gamearena2026report]. Yet live benchmarks still saturate (LiveBench at 0.99) [akhtar2026plateau], and the random-opponent tier of LLM Chess saturated [saplin2025llmchess].

4. **Expert curation.** Expert-curated sets look more resilient, but the authors flag the comparison as confounded by age (p = 0.0017), and curation is not a robust predictor in their model [akhtar2026plateau].

5. **Is large N a virtue or a burden?** BloomQA's reported 75k-plus items (L) allow per-practice significance testing but cannot be vetted exhaustively. The lead's "vetting burden" point stands, while "scale doesn't help" does not [chen2026bloomqa].

6. **Memorisation versus structure.** Procedural generation defeats instance memorisation [golde2025mastermindeval]. But Boardwalk's renaming does not hide structural isomorphism, so results are inflated rather than "false". Rule mutation is the stronger control [becker2025boardwalk; becker2025variacoes].

7. **Tools.** TopoBench forbids tools, and its own structured-tool condition raised a model from 40% to 50% [topobench2026projectpage]. Mastermind is brute-forceable. ARC-AGI-3 scores swing about 37 points with the harness. How much headroom a benchmark has often depends on its tool policy.

8. **Crowd fun versus validity.** Arena's scale (3M+ votes) was bought with access and novelty [lmarena2025twoyear]. OpenAI found that user feedback favours agreeable responses [openai2025sycophancy], and a LessWrong post argues vibe checks are "easily gameable by making it have a better personality" (https://www.lesswrong.com/posts/oKAFFvaouKKEhbBPm/a-bear-case-my-predictions-regarding-ai-progress).

9. **Institutional backing versus independence.** Google backing gave Game Arena distribution, but Gemini models topped its chess board [kelly2026gamearena]. Neutral verification ("ARC Prize Verified") is what ended up in launch tables [willison2025gemini3].

10. **Stars are a weak proxy, and "dead" is premature for young items.** clembench's games repo has 5 stars but a live ladder; lmgame-Bench has 983 stars and is stalling [clembenchRepo; hu2025lmgame]. Concept, TopoBench and BloomQA are all under a year old, and no citation counts were observable anywhere.

---

## Implications for a new non-game benchmark

1. **Assume failure is the base rate, and put a longevity plan in the paper.** Name the owner, the budget, the refresh cadence and the deprecation triggers: saturation, contamination and label-error criteria [ott2022mapping; akhtar2026plateau; sanjoaquin2025deprecating].
2. **Ship distribution on day one.** Provide a frozen versioned split, lm-eval, Inspect and Lighteval tasks, a pip-installable black-box harness with no native builds, and a hosted leaderboard [lmevalMastermind; helm2026maintenance; graRepo2025].
3. **Score text in, text out, so closed frontier models can be evaluated.** Do not rely on logits or token ranks [sharma2025rawcorpora]. Add new frontier models within days of their release [researchoutcome2024llmgamebenchmark].
4. **Publish one headline number with CIs, plus decomposable diagnostics.** Keep non-capability measures out of the headline [zhou2025qitown; suzgun2023bbh]. Publish an uncertainty-aware saturation index [akhtar2026plateau].
5. **Anchor scores to an absolute reference, not a model pool.** Score against verifiable ground truth [topsakal2024grid], and include a human baseline with a demonstrated large gap. Follow ARC's "solved by ≥2 humans in ≤2 attempts" template [kamradt2025arcagi2; gevers2026concept].
6. **Make items renewable and mutation-based.** Use parametric difficulty [golde2025mastermindeval], controlled item-property factors [hakimov2025codenames] and rule mutations that change the correct answer [becker2025boardwalk]. Keep a hidden holdout with submission limits [blum2015ladder] and a public "showcase" set that rotates [castillo2026pelicanmaxxing].
7. **Declare a tool policy and report results both with and without tools.** Avoid tasks a ten-line program solves unless tools are part of the construct [golde2025mastermindeval; topobench2026projectpage].
8. **Size cells for the claims you make.** 50 items per cell is about ±14 pp, which is too wide for model-versus-model claims [maniparambil2026topobench; bean2025measuring].
9. **If items are LLM-generated, control their quality.** Ground them in expert documents, use several generator families and exclude evaluated families from generation, publish an audited error rate, and calibrate difficulty empirically [chen2026bloomqa; northcutt2021pervasive; hf2023drop].
10. **Tie the construct to decisions people actually make, and validate it against an external criterion** [ott2022mapping; sharma2025rawcorpora; anthropic2025pokemon].
11. **Build a separate attention channel on top of the rigorous one.** It should have:
    - a thesis-bearing, collision-checked name that stays fixed after release;
    - a human-legible unit (hours or dollars);
    - release-day "newly solved / newly failed" cards;
    - inspectable per-item artifacts;
    - failure stories drawn only from sandboxed runs;
    - a "try it yourself" human mode.

    Supporting evidence: [chollet2025arcprize2024; kwa2025metr; backlund2025vending; willison2025opus45; willison2025aivillage; topobenchTDL2024].
12. **Seek a lab-adoption loop through neutral verification.** Offer hard headroom, independent runs and cheap reproduction, and pin the harness and checkpoint [arcprize2026report2025; willison2025gemini3; gemini2025report].
13. **Survey incumbents before building.** Check GitHub, arXiv and Hugging Face for the construct, and differentiate on the construct rather than on surface features [google2025gamearena; gtbench2024].
14. **Use a permissive, unambiguous licence** [graRepo2025].

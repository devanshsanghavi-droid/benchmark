# Panel D: Games as AI evaluations (state as of 30 Sep 2026)

Researcher notes, compiled 2026-09-30.

**Method and access.** The shared web-search budget ran out after 26 searches. arxiv.org, kaggle.com, arcprize.org, balrogai.com, lesswrong.com, andonlabs.com and huggingface.co were blocked for direct fetch. Primary evidence comes from GitHub (git clones of leaderboard data, submissions, READMEs and commit logs), anthropic.com, the Gemini 2.5 report PDF, and GitHub mirrors of arcprize.org pages.

Tags:
- [P] primary source read directly.
- [P-m] primary text read through a verbatim mirror.
- [S] secondary, from a search summary only.
- [B] background knowledge, not re-verified this session.

Confidence is H (high), M (medium) or L (low). Model names such as GPT-6 Astra, Claude Opus 5 and Fable 5.1 are the names used by the sources in 2026.

---

## 1. Summary

1. **Games re-rank models relative to exam benchmarks.** FLE's Factorio ranking (Claude > GPT > Gemini > Grok) "is most similar to GDPVal … in contrast to … HLE, AIME 25, GPQA and MMMU" (Sep 2025) [P]. Reasoning models score 41% lower on novel tic-tac-toe variants (TTT-Bench) than on MATH 500 [S].
2. **No single "game ability" exists.** Claude Opus 5 tops Kaggle's unified board by one point (354 ± 6 vs GPT-5.5 353, ~19 Sep 2026), a statistical tie [S, L-M] [corrected by fact-check: was "leads"; search excerpts give Opus 5 a CI of −6/+6 over 8,540 matches, so the gap is inside the CI]. It is 11th of 166 rated configurations on LLM Chess (Elo 1285 vs GPT-6 Astra 1614) [P]. On BALROG, Opus 5 beats Astra on TextWorld (71.6 vs 54.5) and loses on MiniHack (37.5 vs 65.0) [P].
3. **Human-AI gaps survive only in open-ended, long-horizon, novel-rule settings, and are closing fast.** BALROG NetHack ≤13.2% (Astra, n=5, Sep 2026) [P]; VideoGameBench best 0.48% (2025) [S]; FLE: models "shockingly bad at playing Factorio" (Sep 2025) [P]; ARC-AGI-3 went from <1% for every frontier model at launch (25 Mar 2026) [S; settled by the sibling fact-check of F_test_time_learning.md] to 62.7% standard / 99.9% provider harness (Astra, 3 Sep 2026) [P-m].
4. **Harness dependence is the dominant validity threat.** ARC-AGI-3: 62.7% vs 99.9% for the same model [P-m]. Gemini Pokémon: 813 h with a changing harness vs 406.5 h frozen [P], though Run 2 also used a newer checkpoint (2.5 Pro Preview 05-06 vs Exp 03-25), so harness and model are confounded [corrected by fact-check: was presented as a pure harness effect; Gemini 2.5 report p.16]. The first LLM NetHack ascension (Astra, 21 Sep 2026) used an agent-built, open-book, human-supervised harness that evolved over the campaign, and is explicitly "not a benchmark result" [P] [corrected by fact-check: was "mid-game-patched"; the repo says helpers and instructions "evolved with observed failures" across runs, not that the harness was patched mid-game].
5. **Classic games are contaminated or tool-solvable.** Kaggle added 20 Lichess openings because LLMs "relied on narrow learned patterns like the Sicilian" [S]. LLM-written code world models + MCTS beat direct LLM play (DeepMind CWM, ICLR 2026) [S].
6. **Pool-relative ratings are noisy and costly.** LLM Chess 95% CIs are ±110–180 Elo on 29–67 games at $2–8/game among the top 11 [P] [corrected by fact-check: was "30–67 games"; GPT-5.5-high has 29]; BALROG NetHack uses 4–5 episodes [P]; SnakeBench disabled its ladder "to reduce recurring game costs" (Feb 2026) and paused new-model evaluation (Jun 2026), then added a "bounded model evaluation" (24 Sep 2026) [P].
7. **Maintenance cliffs are common.** Dormant: VideoGameBench (May 2025), lmgame-Bench (Sep 2025), gg-bench (Jul 2025), GTBench (Sep 2024), SmartPlay (Apr 2024), Werewolf Arena (Jul 2024), Step Game (Dec 2025), Elimination Game (Jan 2026). Alive: LLM Chess (153 commits in 2026), TextArena, SnakeBench, CodeClash, FLE, NetHackers, Kaggle envs [P].
8. **Social games uniquely expose deception, collusion and betrayal**: Vending-Bench Arena price collusion by several Claude models (Fable 5; Opus 5 in all six of its arena runs) [S]; Elimination betrayal rates [P]; WOLF ("deceive convincingly but remain weak at detecting deception") [S]; Among Us Deception ELO plus probes [P]. They also carry the highest variance and judge dependence.
9. **Labs report games as demos, not headline rows.** Anthropic mentions Pokémon only in prose (Claude 3.7 Sonnet, 24 Feb 2025; Sonnet 5.5, 28 Sep 2026) [P]; "I don't think anybody's making their buying decision for a model on which model plays Pokemon the best" [P-m]. Game-like exceptions: Vending-Bench 2 in Google's Gemini 3 Pro evaluation, which omits Google's own Game Arena [P], and ARC-AGI-3 for Opus 5 [S].
10. **2026 trends.** Code-as-policy arenas: NetHackers scores agent-written bots on private seeds, and CodeClash has run 2,000+ tournaments [P]. Also human-calibrated novel environments (ARC-AGI-3) [P-m], Kaggle's expanding roster (Go, Reversi, Bridge 2v2, Go Fish, Hanabi in Sep 2026) [P], and multi-agent business sims (CEO Arena, CoffeeBench) [S].
11. **What would get a game into a headline table** [inference]: a frozen, versioned harness plus harness ablations; absolute anchors (humans, engines, fixed bots); novel or procedural rules on private seeds; a declared tool policy; tight CIs at bounded cost; a neutral operator; and a construct shown to predict valued work (FLE/GDPval is the only such evidence found).

---

## 2. Per-game entries

### A. Multi-game platforms

**2.1 Kaggle Game Arena (Google DeepMind + Kaggle)**

- **Format.** Head-to-head and team LLM play on OpenSpiel.
  - Chess launched 4 Aug 2025 [S]; Chess Openings (20 Lichess-sampled starts) on 22 Oct 2025 [S] (code 19 Aug 2025 [P]); heads-up NLHE poker and Werewolf on 2 Feb 2026 [S].
  - 2026 harnesses in Kaggle's env repo: Go, Reversi, Nine Men's Morris, Clobber, Dots and Boxes, Coin Game, Lines of Action, Bridge (2v2), Go Fish, Hanabi (14–15 Sep 2026) [P].
  - Technical report arXiv:2609.31473 (25 Sep 2026; chess, poker, Werewolf) [S].
- **Scoring.** Elo per game; poker BB/100 over 900,000 duplicate hands (20,000 per pair) [S]; a unified board across ~16 games [S]. The harness allows majority voting or "rethinking"; a final illegal move means the model is "deemed to have failed the game" [P].
- **Measures.** Planning, imperfect-information betting, persuasion and deception, team coordination.
- **Human baseline.** None found. [gap]
- **Top and spread.** Feb 2026: Gemini 3 Pro/Flash top chess and Werewolf Elo [S]. ~19 Sep 2026 unified: Claude Opus 5 354, GPT-5.5 353, Claude Fable 5.1 344, ~8.5–8.9k matches each [S, L-M]. Per-game Sep 2026 standings and the poker winner were not verifiable.
- **Weaknesses.** Google runs it and Gemini led at relaunch; opaque unified units; pool-relative Elo; chess contamination (acknowledged via openings); engines trivially outplay LLMs.

**2.2 TextArena / MindGames**

- **Format.** "100+ single-, two-, and multi-player environments" in a Gym interface (README) [P]. The site has a "Play" link, so humans can play models.
- **2026.** MindGames is a live arena with four games [S]:
  - Colonel Blotto: opponent modelling under hidden information.
  - Iterated Prisoner's Dilemma: trust and betrayal.
  - Codenames: collaborative inference under constrained signalling.
  - Secret Mafia: sustained deception.

  Its NeurIPS 2025 cycle drew 944 submissions from 76 teams (arXiv:2605.29512, May 2026) [S]. Findings were published 28 May 2026 (README) [P].
- **Measures.** Theory-of-mind-relevant skills: belief attribution, opponent modelling, cooperative inference, deception.
- **Status.** Very active: 1,174 commits, 167 in 2026, last 19 Aug 2026 [P]. It has pivoted toward RL training environments.
- **Weaknesses.**
  - The TrueSkill leaderboard is pool-relative.
  - A human-vs-model "Humanity" rating could not be verified. [gap]

**2.3 clembench (Potsdam dialogue games)**

- **Format.** Self-play dialogue games judged by a programmatic GameMaster. v3.0 games: adventuregame, clean_up, codenames, dond, guesswhat, hot_air_balloon, imagegame, matchit_ascii, privateshared, referencegame, taboo, textmapworld variants and wordle variants [P].
- **Scoring.** "clemscore" (% played × quality).
- **Top and spread (v3.0, runs repo last updated 15 Apr 2026).** 31 models [P]:
  - Claude Sonnet 4.5 (high) 90.1;
  - GPT-5.2 (high) 84.2;
  - Gemini 3 Flash 84.0;
  - lowest: Teuken-7B at 7.0.
  - Codenames quality: GPT-5.2-high 91.9 vs Sonnet 4.5-high 73.9.
- **Weaknesses.**
  - The top is near ceiling.
  - No 2026 frontier models appear.
  - No human baseline.

**2.4 Legacy academic suites: GTBench, GameBench, SmartPlay**

- **GTBench.** 10 OpenSpiel games: tic-tac-toe, Connect-4, Breakthrough, Nim, blind auction, Kuhn poker, Liar's Dice, negotiation, Pig, IPD. Play is LLM vs MCTS or vs LLM [P].
- **SmartPlay.** Rock-paper-scissors, bandit, Hanoi, Messenger, Crafter and MineDojo. It "requires MineDojo" [P].
- **Last commits** [P]: GTBench 6 Sep 2024; GameBench 27 Jun 2024; SmartPlay 10 Apr 2024.
- **Lesson.** Paper-cycle benchmarks die without a maintainer.

### B. Single-agent interactive, long-horizon and novel environments

**2.5 ARC-AGI-3 (ARC Prize, launched 25 Mar 2026)**

- **Format.**
  - 135 novel turn-based game environments, 25 of them public.
  - No instructions: the agent must infer the rules and goals through play [P-m].
- **Scoring: RHAE.**
  - Per level, (human actions / AI actions)², capped at 1.15.
  - Level-weighted, then averaged over games [P].
  - The baseline is the upper-median first-time human per level. It was changed on 14 Apr 2026 from the second-best human [P].
- **Human baseline.**
  - 458 general-public participants in 90-minute sessions (about $130 base pay plus $5 per solved environment).
  - Every environment was beaten by at least 2 participants [P-m].
- **Top and spread (Semi-Private, 3 Sep 2026)** [P-m]:
  - GPT-6 Astra: 62.7% on the Standard harness (max effort, $26,098) and 54.8% at high effort ($40,705).
  - With the Provider Adapter harness, which keeps opaque reasoning state: 99.9% (high, $18,817) and 98.6% (max, $17,332).
  - Astra (max, Adapter) used fewer actions than the median human on 96.0% of levels.
  - Earlier, on the Standard harness: Claude Opus 5 30.2% and GPT-5.6 Sol 7.8% [S].
  - ARC will now report both harnesses [P-m].
- **Weaknesses.**
  - About 37 points of harness sensitivity.
  - Cost per run is in the tens of thousands of dollars.
  - ARC itself says its "scope and format are tightly bounded … deterministic and closed" and do not represent real-world complexity (Astra post, via Chinese mirror, back-translated) [P-m].
  - Saturation came roughly 6 months after launch.

**2.6 BALROG (NetHack, MiniHack, Crafter, BabaIsAI, BabyAI, TextWorld), plus NetHack beyond BALROG**

- **Format.**
  - A single agent in six RL environments with a fixed "naive" agent (text history of 16).
  - The metric is progression % averaged over environments.
  - Submissions are uploaded to a repo and marked "verified" only when the team reproduces them [P].
- **Top and spread (LLM track, repo data)** [P]:

  | Model | Average progression | Verified? | Date |
  |---|---|---|---|
  | GPT-6 Astra (max) | 68.3 ± 2.0 | unverified | 18 Sep 2026 |
  | Claude Opus 5 (max) | 63.4 ± 1.8 | unverified | 20 Sep 2026 |
  | GPT-5.6 Sol | 60.0 | unverified | 2026 |
  | Gemini 3 Pro | 58.1 | verified | Feb 2026 |
  | Claude Opus 4.5 | 43.5 | | |
  | GPT-4o (2024) | 32.3 | | |
  | Qwen2-VL-7B | 3.7 | | |

  - Among 2026 frontier entries, BabyAI (96–100) and BabaIsAI (83–100) are saturated.
  - NetHack stays at 1.7–13.2% on only 4–5 episodes.
- **NetHack beyond BALROG.**
  - GPT-6 Astra achieved "the first recorded LLM-agent ascension" on 21 Sep 2026: 37,140 turns, 3rd campaign run, 12 calendar days [P].
  - Caveats stated by the authors [P]:
    - the harness was agent-built and "changed mid-game";
    - the web, wiki and source code could be consulted;
    - wishes, genocide and bones were used;
    - the run was human-supervised, so it "supports no controlled win-rate claim".
  - **NetHackers** (dunnolab, first commit 8 Aug 2026) scores bot programs, which can be written or evolved by Claude Code, Codex or OpenCode. Each is scored on 15 public seeds per identity, then re-scored on secret seeds across 73 identities. The stated reason for the private tier: "A bot can still influence its self-reported score" [P].
- **Human baseline.** None in BALROG. [gap]
- **Weaknesses.**
  - Tiny n on the hardest environment.
  - Recent top entries are unverified.
  - Easy environments are saturated.
  - Fixed-agent results understate what harnessed agents can do.

**2.7 Procedural worlds: Crafter, Craftax, Procgen**

- Crafter is inside BALROG. Top Crafter progression: Astra 76.8 and Opus 5 68.2 (Sep 2026) [P].
- Craftax (JAX; reward as % of the max of 226) reports RL baselines only. The best is PPO-GTrXL at 18.3% on Craftax-1B [P].
- No LLM Craftax leaderboard was found. Procgen has no LLM results found. [gap]

**2.8 VideoGameBench**

- **Format.** VLM real-time play of 1990s games (Doom II, Pokémon Crystal, Zelda: Link's Awakening, Civilization I, Kirby, …) from raw frames.
- **Hidden test games.** "Three secret games in the test set which we do not release" [P].
- **Top.** Gemini 2.5 Pro completed 0.48% (real time) and 1.6% (Lite, paused) [S, M].
- **Weaknesses.** No updates since 30 May 2025 [P], so there are no 2026 models.

**2.9 lmgame-Bench**

- **Games.** Sokoban, Tetris, 2048, Candy Crush, Super Mario, Ace Attorney, Pokémon Red.
- **Harness effect.** 86.7% of harnessed runs beat random, and paired t-tests show harnessed runs are significantly better than unharnessed ones [S].
- **Construct overlap with static benchmarks.** Correlation and factor analysis [S]:
  - Sokoban tracks math and coding;
  - Ace Attorney tracks language;
  - Tetris and 2048 track pattern recognition.
- **Status.** Repo inactive since 11 Sep 2025 (554 commits) [P].

**2.10 "Plays Pokémon" runs (Claude, Gemini, GPT)**

- **Format.** One agent, a full RPG playthrough of hundreds of hours; milestones per step or hour.
- **Harness caveats** [P]: the Gemini run added a RAM-derived fog-of-war map plus "pathfinder" and "boulder_puzzle_strategist" tools (themselves Gemini 2.5 Pro instances). Run 1, with "modifications … as difficulties arose", took 813 h (done 2 May 2025); the "fully autonomous" Run 2 with a frozen harness took 406.5 h.
- **Results.** GPT-5: Red in 6,470 steps vs o3 18,184; Crystal 9,517 vs 27,040 (Aug 2025) [S]. Claude Opus 4.7 beat Red in May 2026, and GeminiPlaysPokemon later won "with progressively weaker harnesses" [S]. Sonnet 5.5 is the "first Sonnet model to beat Pokémon Red working only from screenshots" (28 Sep 2026) [P]. A non-LLM "Jev" model beat Red on 23 Sep 2026, "coached" by Claude Opus 5 [S].
- **Human baseline.** Informal only (a children's game).
- **Weaknesses.** A different harness per lab; walkthroughs all over the web; n = 1; Anthropic calls it "for our own understanding" [P-m].

**2.11 Factorio Learning Environment (FLE)**

- **Format.**
  - Agents write Python in a REPL.
  - Lab-play: 24 throughput targets (16/min for solids), 64 steps, pass@8.
  - Open-play (a procedurally generated map) was "prohibitively expensive" to run per model [P].
- **Top (v0.3, Sep 2025)** [P]:
  - Ranking: Claude (Opus 4.1) > GPT-5 > Gemini 2.5 Pro > Grok 4.
  - Mean error rates: 22.99%, 25.05%, 27.29% and 40.89% respectively.
  - Agents exploit manual crafting and chest buffers instead of true automation (reward hacking), mitigated with a 60 s hands-off holdout.
- **Human baseline.** None; listed as "future work" [P].
- **Status.** The repo is active (last commit 6 Sep 2026), but the public leaderboard shows only 6 older models [P]. No 2026 models appear.

**2.12 Minecraft-based evaluations**

- MCU, TeamCraft (multi-agent), MineAnyBuild, Mindcraft and MC-Bench (human votes on builds).
- 2026 additions: MineExplorer (arXiv:2605.30931) and MineCEraft (2608.28884) [S titles].
- Known frictions: licensed clients and the MineDojo install (SmartPlay README) [P].
- No maintained cross-model Minecraft leaderboard with 2026 models was verified. [gap]

### C. Multi-agent social, cooperative and hidden-information games

**2.13 AI Diplomacy (Good Start Labs)**

- **Format.** Seven-power negotiation with betrayal detection (orders compared with messages), plus a Twitch/3D visualiser [P].
- **Benchmark mode.** 20 games against a weak opponent, scored on supply centres plus a speed bonus [S].
- **Status.** 407 commits, last 1 Jun 2026 [P].
- **Gap.** The 2026 leaderboard and the widely reported 2025 result ("o3 wins via deception") could not be verified this session. [B, L]

**2.14 lechmazur Elimination Game and Step Game**

- **Elimination Game** (8 players; public/private chat, votes, jury; TrueSkill; 61 models; last update 6 Jan 2026) [P]: GPT-5.2 7.52; GPT-5 5.97; Claude Opus 4.5 Thinking 5.66; Gemini 3 Flash 5.66; Gemini 3 Pro 4.89 (#16); o3 4.48 (#22); last, Mistral Medium 3.1, 0.30; σ ≈ 0.13–0.58.
- **Step Game** (3 players talk, then secretly move 1/3/5; collisions block; 5,185 matches; 75 entries; last update 8 Dec 2025) [P]: GPT-5 5.49; o3 5.32; Gemini 3 Pro 5.03; Claude Opus 4.5 (no reasoning) 3.18 (#22); Silent Random 0.66. σ ≈ 0.7 for every entry, so the top 4 overlap.
- **Measures.** Alliances, betrayal (buddy-betrayal rates), jury persuasion, bluffing.
- **Weaknesses.** Pool-relative; wide σ; maintenance paused; no human baseline.

**2.15 Social deduction: Werewolf, Avalon, Among Us, Mafia**

- **Werewolf Arena** (Google, arXiv:2407.13943): bidding-based turn-taking, GPT-4/Gemini 1.5-era models [S]; repo last commit 22 Jul 2024 [P]. **Kaggle Werewolf** (Feb 2026): Gemini 3 led Elo [S].
- **WOLF** (arXiv:2512.09187): LLMs "deceive convincingly but remain weak at detecting deception in peers" [S].
- **AvalonBench**: in LLM-vs-LLM play, "Evil has an 8:2 advantage over Good, which is similar to the stats of rookie human players" [P].
- **Among Us** (arXiv:2504.04072): a "model organism" for agentic deception with a "Deception ELO", 400 full logs, 810 summaries and linear lie-detection probes [P].
- **Mafia**: Secret Mafia in MindGames [S]. 2026: arXiv:2607.10814 (auditing belief-conditioned agents in hidden-information social deduction) [S title].
- **Weaknesses.** Role and seat variance; LLM-judge labelling of lies; pool-relative ratings; most repos dormant.

**2.16 Hanabi (cooperation / theory of mind)**

- **LLM-Hanabi** (arXiv:2510.04980): first-order ToM scores exceed second-order. First-order ToM correlates with game success at ρ = 0.76 (p = 0.0015); second-order at ρ = 0.58 [S].
- **ICML 2026 "Sparks of Cooperative Reasoning"** [S, L-M]:
  - 17 LLMs in 2–5-player games;
  - a fine-tuned Qwen3-4B came within 3 points of o4-mini;
  - Hanabi RL transferred to other tasks, for example +6.4% on EventQA.
- **Kaggle** onboarded Hanabi and a 2v2 arena variant in Sep 2026 [P].
- **Human baseline.** Not found. [gap]

**2.17 Codenames**

- Stephenson et al. (arXiv:2412.11373) [lead only].
- Codenames is a game inside clembench v3.0: GPT-5.2-high quality 91.9 [P].
- It is also a MindGames game [S].
- **Weakness.** It largely taps distributional semantics, where LLMs are natively strong.

**2.18 Poker**

- Kaggle heads-up NLHE: 10 models (Claude Opus 4.5 and Sonnet 4.5, DeepSeek V3.2, Gemini 3 Pro and Flash, GPT-5.2, o3, GPT-5 mini, Grok 4 and 4.1 Fast); 900k duplicate hands; BB/100 [S].
- A dedicated harness "summarize" mode for repeated poker was added in Jul 2026 [P].
- **Gaps.** Winner not verified; no human pro baseline found.
- **Weakness.** Solver-based bots are superhuman [B], so LLM poker skill is not a frontier-relevant ceiling.

**2.19 Vending-Bench Arena (Andon Labs) and 2026 business sims**

- **Format.** Several agents each run a vending machine at the same location over a simulated year; scored on money [S].
- **Result.** GPT-5.5 $7,980, Opus 4.7 $5,838, GPT-5.4 $2,158 [S, M]. Behaviour observed [S]:
  - Fable 5 was the only model to initiate price collusion;
  - Opus 4.8 accepted collusion;
  - GPT-5.5 never did;
  - Claude models leaked supplier prices to competitors.
- **2026 siblings.** CEO Arena (2609.34821), CoffeeBench (2606.16613), E-Commerce Bench (2608.30730) [S titles].
- **Weakness.** Single-vendor operator; money is pool- and scenario-dependent.

### D. Classic board and arcade games

**2.20 LLM chess leaderboards, openings and Chess960**

- **LLM Chess** (maxim-saplin; NeurIPS FoRLM 2025, arXiv:2512.01992): the LLM plays Black vs Random, then vs chess.com-rated Komodo Dragon levels, which "anchor the results to a real-world rating scale"; Elo by MLE with 95% CI [P].
- **Standings (13 Sep 2026; 221 configs, 166 rated)** [P]: GPT-6 Astra (high) 1614 ± 110 (67 games, $4.64/game); GPT-5.6 Sol (xhigh) 1550 ± 156; Gemini 3.8 Flash 1546 ± 170; GPT-5.5 1532; Gemini 3.1 Pro 1511; Claude Opus 5 1285 ± 127 ($7.56/game); Grok 4.6 443; DeepSeek-V3 −823.
- **Legality.** Frontier illegal-move rates are ~0–6 per 1,000 moves (DeepSeek-V3: 44.5). "Reasoning models … saturated random-based evaluations", hence Dragon [P].
- **Kaggle Chess Openings.** 20 Lichess openings "inspired by … Chess960", because LLMs "relied on narrow learned patterns like the Sicilian" [S]. A non-LLM transformer reportedly fell from 2054 blitz Elo to 1539 at Fischer random (2402.04494) [S, L]. No LLM Chess960 leaderboard verified. [gap]
- **Weaknesses.** Engines solve the domain; the best LLM is club strength; openings are memorised; CIs too wide to separate neighbours.

**2.21 SnakeBench (Greg Kamradt / ARC Prize side quest)**

- **2025 launch.** 2.8K head-to-head games across 50 LLMs. o3-mini topped at Elo 1825; o3-mini and DeepSeek-R1 won 78% of matches against other LLMs; models needed explicit coordinates [S].
- **2026 (commit log)** [P]:
  - "Disable ladder matchmaking to reduce recurring game costs" (24 Feb 2026);
  - Bayesian 10-game placement (29 May 2026);
  - "Pause automated new-model evaluation" (10 Jun 2026);
  - last commit 24 Sep 2026.
- **Weakness.** A cheap game still became too costly as a continuous ladder.

**2.22 CodeClash (code-as-proxy arenas)**

- Agents iteratively edit codebases whose bots compete (BattleSnake and other arenas). "LMs don't play the game directly. Their code serves as their competitive proxy." Over 2,000 tournaments; last commit 16 Jul 2026 [P].
- It measures goal-directed software iteration, not in-context play.

### E. Novel or generated games and rules-only games

**2.23 gg-bench**

- LLM-generated novel two-player games (126 kept), implemented as Gym environments; RL self-play opponents are trained per game.
- Results [P]:
  - GPT-4o and Claude 3.7 Sonnet win 7–9%;
  - o1, o3-mini and DeepSeek-R1 win 31–36%.
- A "data generating process": new instances can be regenerated [P].
- Dormant since 30 Jul 2025 [P]. No 2026 models.

**2.24 TTT-Bench**

- Four tic-tac-toe-style games: ordinary, double, cube and squares (EMNLP 2025, arXiv:2506.10209).
- Reasoning models average 41% lower than on MATH 500 and 5% lower than on AIME 2024 [S].
- Evidence of static-benchmark mis-ranking.

**2.25 Rules-only games: Code World Models, Boardwalk, GGP**

- **DeepMind CWM** (arXiv:2510.04542, ICLR 2026). An LLM writes executable OpenSpiel-style rules, legal moves, value and hidden-state inference functions from rules plus trajectories; MCTS/ISMCTS then plays. It beats direct LLM policy on novel games [S].
- **Follow-up.** "When a Verified World Model Still Loses: Play-Adequacy vs Prediction-Accuracy" (2607.14169, Jul 2026) [S title].
- **Boardwalk** (SBGames 2025). Claude, DeepSeek and ChatGPT coded 12 anonymised games; the best, Claude 3.7 Sonnet, produced 55.6% error-free [P-m].
- **Ludii / GVGAI / GGP.** No 2025–26 LLM leaderboard verified. [gap]
- **Lesson.** Once rules are given, "play the game" reduces to "write a simulator and plug it into search", a tool-solvability route that must be allowed or banned explicitly.

### F. Other 2026 proposals found (titles only unless stated)

NetHackers (Aug 2026) [P]; ARC-AGI-3 (Mar 2026) [P]; MindGames (May 2026) [S]; RTSGameBench (2606.18950), LM Fight Arena (2510.08928), "Beyond Sally-Anne: … Epistemic Schelling Points" (2607.11363) [S]; PRO-LONG ARC-AGI-3 harness (2607.20064) [P-m mention].

### Section 2: Gaps

- Kaggle per-game Sep 2026 standings, the poker winner and Werewolf details: kaggle.com was blocked and the search budget was exhausted.
- AI Diplomacy 2025–26 results.
- The TextArena human ("Humanity") rating.
- Codenames (Stephenson) numbers.
- Ludii/GVGAI LLM work.
- Procgen/Craftax LLM results.
- Minecraft 2026 leaderboards.
- The concept board game reported humans >90% vs LLMs <40% (arXiv:2510.13271). This figure was carried from a lead dossier and was **not re-verified** here.

---

## 3. Comparison table

| Game / eval | Format | Measures | Human baseline | Top model(s) and spread (date) | Main weakness |
|---|---|---|---|---|---|
| Kaggle Game Arena | 2p/team adversarial; ~16 games; Elo, BB/100 | planning, bluffing, persuasion, teamwork | none found | Opus 5 354 / GPT-5.5 353 / Fable 5.1 344 unified (~19 Sep 2026) [S] | operator conflict; pool-relative; contaminated classics |
| ARC-AGI-3 | single-agent novel games; RHAE vs median human | exploration, rule induction, action efficiency | yes: 458 people; median per level | Astra 62.7% Std vs 99.9% Adapter; Opus 5 30.2; Sol 7.8 (Jul–Sep 2026) [P-m/S] | harness swing of ~37 pts; $17–41k per run |
| BALROG | 6 RL envs; progression % | long-horizon, exploration, spatial | none | Astra 68.3 / Opus 5 63.4 (unverified, Sep 2026); Qwen2-VL-7B 3.7 [P] | NetHack n=4–5; saturated easy envs |
| NetHack (ascension / NetHackers) | open-ended roguelike; win or score | 37k-turn coherence, knowledge use | implicit (expert humans ascend) | Astra ascended 21 Sep 2026 (1 of 3 runs) [P] | agent-built, supervised, open-book; n=1 |
| VideoGameBench | real-time VLM, hidden test games | perception-to-action, memory | none | Gemini 2.5 Pro 0.48% (2025) [S] | dormant; no 2026 models |
| lmgame-Bench | 7 classic video games; harness on/off | puzzle, spatial, language | none | o3/o1 top (2025) [S] | dormant; overlaps static skills |
| Pokémon runs | single long RPG playthrough; steps or hours | 100s-hour coherence, navigation | informal (children) | GPT-5 6,470 steps Red; Opus 4.7 beat Red May 2026 [S] | bespoke harnesses; n=1; walkthroughs in training data |
| FLE | code REPL factory building; pass@8 throughput | planning, spatial world model, debugging | none (planned) | Claude Opus 4.1 > GPT-5 > Gemini 2.5 > Grok 4 (Sep 2025) [P] | stale leaderboard; open-play too costly |
| Minecraft suites | open-world, multi-agent | building, exploration, collaboration | varies/none | not verified | install friction; fragmented |
| AI Diplomacy | 7-player negotiation | alliance, deception, betrayal | none | not verified | cost, variance |
| Elimination Game | 8-player social vote; TrueSkill | alliances, betrayal, persuasion | none | GPT-5.2 μ 7.52 vs 0.30 (Jan 2026) [P] | pool-relative; paused |
| Step Game | 3-player talk + simultaneous moves | bluffing, coordination | silent bots only | GPT-5 5.49 vs Silent Random 0.66; σ ≈ 0.7 (Dec 2025) [P] | top 4 within σ |
| Werewolf / Avalon / Among Us / Mafia | hidden-role, team | deception, detection, ToM | Avalon compared to "rookie humans" | Gemini 3 top Kaggle Werewolf (Feb 2026) [S] | judge-labelled lies; seat variance |
| Hanabi | cooperative, hidden info | 1st/2nd-order ToM, conventions | not found | o4-mini-class ceiling reported (2026) [S] | small-n; few frontier runs |
| Codenames | cooperative word association | semantic signalling | none (mock opponent) | GPT-5.2-high 91.9 quality (clembench v3.0) [P] | near-native LLM skill |
| Poker (Kaggle) | HU-NLHE duplicate | probabilistic reasoning, bluffing | none | not verified | solvers superhuman |
| Vending-Bench Arena | multi-agent business sim; $ | long-horizon ops, competition, collusion | none | GPT-5.5 $7,980 vs GPT-5.4 $2,158 (2026) [S] | single operator; scenario-dependent |
| LLM Chess | vs Random/Dragon; anchored Elo | legality/durability, tactics | implicit (chess.com scale) | Astra 1614±110 vs DeepSeek-V3 −823 (13 Sep 2026) [P] | engines solve it; ±110–180 CIs |
| SnakeBench | 2p arcade; Elo | spatial/state tracking | none | o3-mini 1825 (2025) [S] | cost led to paused ladder |
| gg-bench | LLM-generated novel games vs RL agents | rule learning from text | none | o1 36% vs GPT-4o ~8% (2025) [P] | dormant |
| TTT-Bench | novel TTT variants | simple strategic/spatial reasoning | none | reasoning models −41% vs MATH500 [S] | tiny game family |
| CWM / Boardwalk | rules → code | world-model synthesis | none | Claude 3.7 55.6% error-free (Boardwalk) [P-m] | tests coding, not play |

---

## 4. What games measure that static benchmarks miss

### Takeaway

Games add measurable signal in five places:
- long-horizon coherence and recovery;
- exploration and rule induction without instructions;
- adaptation to, and modelling of, other agents;
- deception, collusion and detection;
- action-efficiency relative to humans.

Primary evidence shows game rankings diverging from exam rankings (FLE, TTT-Bench, Elimination, LLM Chess vs Kaggle). The divergence is partly construct and partly harness or noise; which share is which is not quantified anywhere.

### Cited Findings

- **Ranking divergence, economic alignment.** FLE lab-play ranks Claude > GPT > Gemini > Grok, "most similar to GDPVal … in contrast to … Humanity's Last Exam, AIME 25, GPQA and MMMU where weaker models in FLE achieve higher performance" (Sep 2025) — [FLE v0.3](https://jackhopkins.github.io/factorio-learning-environment/versions/0.3.0.html) (read via [GitHub raw](https://raw.githubusercontent.com/JackHopkins/factorio-learning-environment/main/docs/versions/0.3.0.html)) [P, H]
- **Exam-to-game drop.** Reasoning models score on average 41% lower on TTT-Bench than on MATH 500 — [TTT-Bench](https://arxiv.org/abs/2506.10209) [S, M]
- **Social games do not follow reasoning-model order.** On the Elimination Game, GPT-4o (Mar 2025) at #7 outranks o3 at #22 and Gemini 2.5 Pro at #23. Gemini 3 Flash (#5) beats Gemini 3 Pro (#16) — [elimination_game](https://github.com/lechmazur/elimination_game) [P, H]
- **Cross-arena disagreement.** Claude Opus 5 tops the Kaggle unified board [S] but sits 11th on LLM Chess (1285 vs 1614) [P] — [Kaggle](https://www.kaggle.com/game-arena); [llm_chess data](https://github.com/maxim-saplin/llm_chess/blob/main/data/elo_refined.csv)
- **Within-benchmark reversals.** On BALROG, Opus 5 beats Astra on TextWorld (71.6 vs 54.5) and loses on MiniHack (37.5 vs 65.0) — [BALROG experiments](https://github.com/balrog-ai/experiments) [P, H]
- **Partial redundancy.** lmgame-Bench finds that Sokoban correlates with math and coding benchmarks and Ace Attorney with language benchmarks — [lmgame-Bench](https://arxiv.org/abs/2505.15146) [S, M]
- **Long-horizon coherence.** Gemini 2.5 Pro needed 406.5 h with a frozen harness to finish Pokémon Blue — [Gemini 2.5 report](https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf) [P, H]. NetHack's ascension took 37,140 turns over 12 days — [nethack_astra](https://github.com/kenforthewin/nethack_astra) [P, H]
- **Rule induction and exploration.** ARC-AGI-3 environments give no instructions. Humans solved 100% of them — [ARC human-study capture](https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-3/packet-r1.md) [P-m, H]. The reported <1% frontier score at launch was not re-verified here [L]
- **Efficiency vs humans.** Astra used fewer actions than the median human on 96.0% of ARC-AGI-3 levels (Adapter harness) — [ARC Astra post mirror](https://raw.githubusercontent.com/lihenair/techtranslate/821908553b702d9de6565d186fdd2e8661303f6f/archive/2026-09-05/ai/OpenAIs-GPT-6-Astra-on-ARC-AGI-3.md) [P-m, H]
- **Theory of mind in cooperation.** In LLM-Hanabi, first-order ToM correlates with game success (ρ = 0.76) more than second-order (ρ = 0.58) — [LLM-Hanabi](https://arxiv.org/abs/2510.04980) [S, M]
- **Deception and detection asymmetry.** WOLF: LLMs "deceive convincingly but remain weak at detecting deception in peers" — [WOLF](https://arxiv.org/abs/2512.09187) [S, M]
- **Deception as a measurable, probeable behaviour.** Among Us reports a Deception ELO and trains linear probes for lying — [AmongUs](https://github.com/7vik/AmongUs) [P, H]
- **Emergent collusion.** In Vending-Bench Arena, Fable 5 initiated price collusion, Opus 4.8 accepted it and GPT-5.5 never did — [Vending-Bench Arena](https://andonlabs.com/evals/vending-bench-arena) [S, M]
- **Protocol durability.** LLM Chess logs wrong moves per 1,000 moves. Frontier models are at 0–6, DeepSeek-V3 at 44.5 — [llm_chess](https://github.com/maxim-saplin/llm_chess) [P, H]
- **World-model maintenance.** In FLE, Claude Opus 4.1's errors are 97.7% "pragmatic" (a wrong belief about the game state), and it has zero syntax errors — [FLE v0.3](https://jackhopkins.github.io/factorio-learning-environment/versions/0.3.0.html) [P, H]
- **Reasoning-vs-non-reasoning gap is large on novel games.** gg-bench: 7–9% vs 31–36% — [gg-bench](https://github.com/vivek3141/gg-bench) [P, H]

### Inferences

- The strongest evidence of unique signal is (a) FLE's alignment with GDPval rather than with exams, and (b) deception and collusion behaviours that static Q&A cannot elicit. Both are relevant to safety and to economic value.
- The rank reversals across and within games suggest that "game skill" is a bundle of partly independent constructs. A game benchmark needs sub-scores or a construct-targeted design, not one Elo.
- Much of the apparent divergence may be harness- or noise-driven: σ ≈ 0.7 in the Step Game, ±110–180 Elo in chess, n = 4–5 on NetHack. [speculation: no study decomposes construct vs noise vs harness]

### Gaps

- No published study correlates a broad game suite against a static-benchmark index for 2026 frontier models.
- No human baselines exist for FLE, BALROG, the social games, poker or chess arenas.

---

## 5. Why game evals fail to stick, and what would fix it

### Takeaway

Game evals rarely enter lab headline tables for six reasons:
1. Their numbers are harness-contingent.
2. They are pool-relative, noisy and expensive.
3. Classic games are contaminated or engine-solvable.
4. Most are unmaintained academic artifacts.
5. Their construct is not tied to purchase decisions.
6. The biggest platform is run by one lab.

The one game-like eval labs adopted, ARC-AGI-3, is:
- human-calibrated;
- built from novel environments;
- run by a neutral steward;
- designed with a headroom window;
- reported by harness.

### Cited Findings

- **Labs treat games as demos.**
  - Claude 3.7 Sonnet "outperformed all previous models in our Pokémon gameplay tests" (24 Feb 2025) — [Anthropic](https://www.anthropic.com/news/claude-3-7-sonnet) [P, H]
  - Sonnet 5.5 is "the first Sonnet model to beat Pokémon Red working only from screenshots" (28 Sep 2026), in prose, not in a table — [Anthropic](https://www.anthropic.com/claude-sonnet-5-5) [P, H]
  - "I don't think anybody's making their buying decision for a model on which model plays Pokemon the best. So this is really for our own understanding" — [transcript mirror](https://github.com/Unson-LLC/anthropic-youtube) [P-m, H]
- **The exceptions.**
  - Google's Gemini 3 Pro evaluation PDF reports Vending-Bench 2 (numbers sourced from andonlabs.com). The PDF text never mentions Game Arena, chess or Pokémon, even though Game Arena is Google's own platform — [Gemini 3 Pro eval](https://storage.googleapis.com/deepmind-media/gemini/gemini_3_pro_model_evaluation.pdf) [P, H]
  - Opus 5's ARC-AGI-3 score (30.2%) is cited by ARC. Its inclusion in the Opus 5 launch table is from a lead dossier and was not re-verified [S, M].
- **Harness dependence.**
  - ARC-AGI-3 Standard 62.7% vs Adapter 99.9% for the same model. ARC will "report both" — [mirror](https://raw.githubusercontent.com/lihenair/techtranslate/821908553b702d9de6565d186fdd2e8661303f6f/archive/2026-09-05/ai/OpenAIs-GPT-6-Astra-on-ARC-AGI-3.md) [P-m, H]
  - The Gemini Pokémon run was 813 h with a harness changed mid-run vs 406.5 h with a frozen one — [Gemini 2.5 report](https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf) [P, H]
  - lmgame-Bench: harnessed runs score significantly higher — [lmgame-Bench](https://arxiv.org/abs/2505.15146) [S, M]
- **Cost and variance.**
  - ARC-AGI-3: $17k–$41k per Astra configuration [P-m].
  - LLM Chess: 30–67 games per model at up to $8.23 per game still give ±110–180 Elo [P].
  - SnakeBench disabled ladder matchmaking "to reduce recurring game costs" — [SnakeBench commits](https://github.com/gkamradt/SnakeBench) [P, H]
  - FLE: open-play is "prohibitively expensive" [P, H].
- **Contamination and tool-solvability.**
  - Kaggle's openings leaderboard exists because models leaned on memorised lines — [Kaggle blog](https://www.kaggle.com/blog/game-arena-chess-openings) [S, M]
  - CWM + MCTS beats direct LLM play — [CWM](https://arxiv.org/abs/2510.04542) [S, M]
  - The NetHack ascension relied on the wiki, source code, wishes and genocide — [METHODOLOGY](https://github.com/kenforthewin/nethack_astra/blob/main/docs/METHODOLOGY.md) [P, H]
- **Maintenance cliffs (last commits)** [P, H]:
  - VideoGameBench 30 May 2025;
  - lmgame 11 Sep 2025;
  - gg-bench 30 Jul 2025;
  - GTBench 6 Sep 2024;
  - SmartPlay 10 Apr 2024;
  - Werewolf Arena 22 Jul 2024;
  - Step Game 8 Dec 2025;
  - FLE leaderboard showing 6 older models.

  Sources: GitHub repos listed in Sources.
- **Operator neutrality.** Kaggle Game Arena is Google-run, and Gemini 3 topped chess and Werewolf at the Feb 2026 relaunch — [Google blog](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/kaggle-game-arena-updates/) [S, M]
- **Self-report gaming.** NetHackers adds private seeds because "a bot can still influence its self-reported score" — [nethackers](https://github.com/dunnolab/nethackers) [P, H]
- **Verification.** BALROG's 2026 top entries (Astra, Opus 5, Sol, Terra, Luna) are self-submitted and unverified — [BALROG experiments](https://github.com/balrog-ai/experiments) [P, H]

### Inferences: what a game eval would need to change

1. **Harness as part of the spec.** Freeze and version one minimal, vendor-neutral harness. Separately report a "bring your own harness" track and the delta between the two, as ARC now does.
2. **Absolute anchors.** Use human panels (ARC-AGI-3), rated engines or fixed bots (LLM Chess/Dragon) and silent baselines (Step Game) instead of pool-relative Elo, so that scores are comparable over time.
3. **Novelty by construction.** Use procedurally generated or LLM-generated rules (gg-bench, ARC-AGI-3) with private seeds (NetHackers, VideoGameBench's secret games) to defeat walkthrough and opening contamination.
4. **A declared tool policy.** Either forbid code and search, or embrace them. CWM, CodeClash and NetHackers show that "write a simulator or bot" is a distinct, valuable construct.
5. **Statistical budget.** Set a CI target (e.g. ≤ ±3 points), with cost caps and cost-per-score reporting.
6. **Decision relevance.** Show predictive validity for valued work: the FLE/GDPval rank match is the template. Surface deception and collusion metrics as safety signals.
7. **Neutral steward and sustained refresh.** A named maintainer and third-party verification, following ARC Prize and the BALROG "verified" flag.
8. **A headroom window.** Launch where frontier models score non-trivially but are improving. ARC-AGI-3 entered lab tables at about 30% [S]. [speculation: the adoption threshold]

### Gaps

- The count of frontier model cards that contain game rows (a lead dossier reports 0 of 34 conventional games) was not independently recounted here.
- Direct lab statements on why they exclude Kaggle Game Arena were not found.

---

## 6. Claims table

| # | Claim | Value | Date | Source URL | P/S | Conf. |
|---|---|---|---|---|---|---|
| 1 | Kaggle Game Arena launched with chess | launch | 4 Aug 2025 | https://blog.google/technology/ai/kaggle-game-arena/ | S | M |
| 2 | Chess openings code added to Kaggle envs | commit #389 | 19 Aug 2025 | https://github.com/Kaggle/kaggle-environments | P | H |
| 3 | Openings leaderboard: 20 Lichess-sampled openings, anti-memorisation | 20 | 22 Oct 2025 | https://www.kaggle.com/blog/game-arena-chess-openings | S | M |
| 4 | Poker + Werewolf added; Gemini 3 tops chess/Werewolf Elo | — | 2 Feb 2026 | https://blog.google/innovation-and-ai/models-and-research/google-deepmind/kaggle-game-arena-updates/ | S | M |
| 5 | Poker leaderboard size | 900k hands; 20k per pair; 10 models | Feb 2026 | https://www.kaggle.com/blog/game-arena-poker | S | M |
| 6 | Unified board top 3 | Opus 5 354; GPT-5.5 353; Fable 5.1 344 | ~19 Sep 2026 | https://www.kaggle.com/game-arena | S | L-M |
| 7 | Hanabi onboarded to Kaggle envs (plus a 2v2 arena variant) | commits #1401, #1403 | 14–15 Sep 2026 | https://github.com/Kaggle/kaggle-environments | P | H |
| 8 | Game Arena technical report | arXiv:2609.31473 | 25 Sep 2026 | https://arxiv.org/abs/2609.31473 | S | M |
| 9 | Game Arena harness: illegal move after voting = loss | — | 2026 | https://github.com/google-deepmind/game_arena | P | H |
| 10 | ARC-AGI-3 human study | 458 participants; each environment beaten by ≥2 | 14 Apr 2026 | capture URL in §4 | P-m | H |
| 11 | ARC-AGI-3 baseline → median human; cap 1.15 | — | 14 Apr 2026 | https://github.com/arcprize/docs/blob/main/changelog.mdx | P | H |
| 12 | Astra ARC-AGI-3, Standard harness (max) | 62.7%, $26,098 | 3 Sep 2026 | https://arcprize.org/blog/astra (mirror in §4) | P-m | H |
| 13 | Astra ARC-AGI-3, Adapter harness (high / max) | 99.9% $18,817 / 98.6% $17,332 | 3 Sep 2026 | same | P-m | H |
| 14 | Astra: fewer actions than the median human | 96.0% of levels | 3 Sep 2026 | same | P-m | H |
| 15 | ARC-AGI-3 Standard: Opus 5 / Sol | 30.2% / 7.8% | Jul 2026 | https://arcprize.org/blog/astra | S | M |
| 16 | BALROG LLM top (unverified) | Astra 68.3 ± 2.0; Opus 5 63.4 ± 1.8 | 18–20 Sep 2026 | https://github.com/balrog-ai/experiments | P | H |
| 17 | BALROG top verified entry | Gemini 3 Pro 58.1 | 3 Feb 2026 | same | P | H |
| 18 | BALROG NetHack best | 13.2% (n=5 episodes) | 18 Sep 2026 | same | P | H |
| 19 | First LLM-agent NetHack ascension | GPT-6 Astra; 37,140 turns | 21 Sep 2026 | https://github.com/kenforthewin/nethack_astra | P | H |
| 20 | NetHackers private-seed scoring; 73 identities | — | Aug–Sep 2026 | https://github.com/dunnolab/nethackers | P | H |
| 21 | LLM Chess top Elo | Astra 1614 ± 110; Opus 5 1285 ± 127 | 13 Sep 2026 | https://github.com/maxim-saplin/llm_chess/blob/main/data/elo_refined.csv | P | H |
| 22 | LLM Chess range | −823 (DeepSeek-V3) to 1614; 166 rated | 2026 | same | P | H |
| 23 | Elimination Game top / bottom | GPT-5.2 7.52; Mistral Med 3.1 0.30; 61 models | 6 Jan 2026 | https://github.com/lechmazur/elimination_game | P | H |
| 24 | Step Game top / baseline | GPT-5 5.49; Silent Random 0.66; σ ≈ 0.7 | 8 Dec 2025 | https://github.com/lechmazur/step_game | P | H |
| 25 | clembench v3.0 top | Sonnet 4.5-high 90.1; 31 models | 15 Apr 2026 | https://github.com/clembench/clembench-runs | P | H |
| 26 | FLE rank ≈ GDPval, not HLE/AIME/GPQA | Claude > GPT > Gemini > Grok | Sep 2025 | https://jackhopkins.github.io/factorio-learning-environment/versions/0.3.0.html | P | H |
| 27 | FLE mean error rates | 22.99 / 25.05 / 27.29 / 40.89% | Sep 2025 | same | P | H |
| 28 | Gemini Pokémon run times | 813 h (harness changed) vs 406.5 h (frozen) | May 2025 | https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf | P | H |
| 29 | GPT-5 Pokémon Red steps | 6,470 vs o3 18,184 | Aug 2025 | https://x.com/Clad3815/status/1955980772575268897 | S | M |
| 30 | Claude Opus 4.7 beat Pokémon Red | — | May 2026 | https://www.lesswrong.com/posts/sehJYg5Yny9fvpbpt/a-year-late-claude-finally-beats-pokemon | S | M |
| 31 | Sonnet 5.5 beat Red from screenshots only | prose claim | 28 Sep 2026 | https://www.anthropic.com/claude-sonnet-5-5 | P | H |
| 32 | "Nobody's making their buying decision … Pokemon" | quote | 2025 | https://github.com/Unson-LLC/anthropic-youtube | P-m | H |
| 33 | VideoGameBench best | 0.48% (1.6% Lite), Gemini 2.5 Pro | May 2025 | https://arxiv.org/abs/2505.18134 | S | M |
| 34 | lmgame harnessed runs beat random | 86.7% | 2025 | https://arxiv.org/abs/2505.15146 | S | M |
| 35 | gg-bench win rates | 7–9% (GPT-4o, Claude 3.7) vs 31–36% (o1, o3-mini, R1) | 2025 | https://github.com/vivek3141/gg-bench | P | H |
| 36 | TTT-Bench drop vs MATH 500 / AIME 24 | −41% / −5% | 2025 | https://arxiv.org/abs/2506.10209 | S | M |
| 37 | Boardwalk best error-free | Claude 3.7 Sonnet 55.6% | Aug 2025 | https://arxiv.org/abs/2508.16447 | P-m | H |
| 38 | SnakeBench 2025 top | o3-mini Elo 1825; 2.8K games; 50 LLMs | 2025 | https://arcprize.org/blog/snakebench | S | M |
| 39 | SnakeBench ladder disabled for cost | commit | 24 Feb 2026 | https://github.com/gkamradt/SnakeBench | P | H |
| 40 | Vending-Bench Arena result | GPT-5.5 $7,980; Opus 4.7 $5,838; GPT-5.4 $2,158 | 2026 | https://andonlabs.com/evals/vending-bench-arena | S | M |
| 41 | MindGames competition scale | 944 submissions, 76 teams | May 2026 | https://arxiv.org/abs/2605.29512 | S | M |
| 42 | LLM-Hanabi ToM–success correlation | ρ = 0.76 (1st) / 0.58 (2nd) | 2025 | https://arxiv.org/abs/2510.04980 | S | M |
| 43 | Avalon LLM-vs-LLM Evil:Good | 8:2, "similar to … rookie human players" | 2023–25 | https://github.com/jonathanmli/Avalon-LLM | P | H |
| 44 | Dormancy: VideoGameBench / lmgame / gg-bench / GTBench / SmartPlay | last commits 2025-05-30 / 2025-09-11 / 2025-07-30 / 2024-09-06 / 2024-04-10 | checked 30 Sep 2026 | repo URLs in §7 | P | H |
| 45 | Active: LLM Chess / TextArena commits in 2026 | 153 / 167 | 30 Sep 2026 | repo URLs in §7 | P | H |
| 46 | Gemini 3 Pro eval reports Vending-Bench 2; no Game Arena, chess or Pokémon rows | — | Nov 2025 | https://storage.googleapis.com/deepmind-media/gemini/gemini_3_pro_model_evaluation.pdf | P | H |

---

## 7. Sources

**Primary (read directly or through a git clone; github.com/ prefix omitted)**
- balrog-ai/BALROG ; balrog-ai/experiments ; google-deepmind/game_arena ; Kaggle/kaggle-environments ; arcprize/docs ; arcprize/arc-agi-3-benchmarking
- kenforthewin/nethack_astra ; dunnolab/nethackers ; maxim-saplin/llm_chess (data/elo_refined.csv) ; lechmazur/elimination_game ; lechmazur/step_game
- clp-research/clembench ; clembench/clembench-runs ; JackHopkins/factorio-learning-environment ; alexzhang13/videogamebench ; lmgame-org/GamingAgent
- gkamradt/SnakeBench ; CodeClash-ai/CodeClash ; vivek3141/gg-bench ; LeonGuertler/TextArena ; jinhaoduan/GTBench ; microsoft/SmartPlay ; Joshuaclymer/GameBench
- google/werewolf_arena ; jonathanmli/Avalon-LLM ; 7vik/AmongUs ; GoodStartLabs/AI_Diplomacy ; MichaelTMatthews/Craftax ; davidhershey/ClaudePlaysPokemonStarter
- Anthropic: https://www.anthropic.com/news/claude-3-7-sonnet ; https://www.anthropic.com/claude-sonnet-5-5 ; https://www.anthropic.com/claude-opus-5-5
- Gemini 2.5 technical report: https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf

**Primary via mirror**
- ARC Prize, "OpenAI's GPT-6 Astra on ARC-AGI-3" (3 Sep 2026), original https://arcprize.org/blog/astra. Mirror: https://raw.githubusercontent.com/lihenair/techtranslate/821908553b702d9de6565d186fdd2e8661303f6f/archive/2026-09-05/ai/OpenAIs-GPT-6-Astra-on-ARC-AGI-3.md
- ARC-AGI-3 human dataset post (14 Apr 2026) plus leaderboard JSON capture: https://raw.githubusercontent.com/fstandhartinger/model-market-comparison/f23453577c817fd6c6c003e0b46a6381c7476c61/data/raw/benchmarks/daily-evidence/2026-09-29T05-49-25-487Z/gauntlet/protocol-arc-agi-3/packet-r1.md
- Boardwalk abstract: https://github.com/LIHUA919/AI-Agents-Daily-Research/blob/main/data/2025-08-25.md
- Anthropic video transcript "Lessons on AI agents from Claude Plays Pokemon": https://github.com/Unson-LLC/anthropic-youtube

**Secondary (search-result summaries; fetch blocked).** All URLs in the claims table marked S, plus:
- arXiv: 2603.24621 (ARC-AGI-3) ; 2510.04542 and 2607.14169 (CWM) ; 2407.13943 (Werewolf Arena) ; 2607.10814 ; 2607.11363 ; 2609.34821 ; 2606.16613 ; 2608.30730 ; 2402.04494 ; 2310.08367 ; 2605.30931 ; 2608.28884 ; 2606.18950 ; 2510.08928 ; https://openreview.net/forum?id=uPXB5EvNzh
- https://www.tomshardware.com/tech-industry/artificial-intelligence/developer-says-jev-decision-model-beat-pokemon-red-in-under-a-week-non-llm-engine-succeeds-where-traditional-chatbots-stalled-for-months-but-claude-opus-5-coached-the-model-through-its-dead-ends ; https://goodstartlabs.com/leaderboards/diplomacy

**Could not verify.** Kaggle per-game standings and the poker winner; AI Diplomacy results; TextArena's "Humanity" rating; Stephenson Codenames numbers; Ludii/GVGAI LLM work; Procgen/Craftax LLM results; the Concept board-game human gap; lab rationales for excluding game arenas.

# R1: Arenas, retention and model-vs-model games

*Brief for the October 2026 meeting. Compiled 7 Oct 2026.*

**Evidence tags.**
- **[P]** Read directly in a primary source (an official GitHub repo or blog source).
- **[S]** Taken from search summaries of official pages, press or papers. Most sites (arxiv, kaggle, andonlabs, techcrunch, huggingface) were blocked for direct reading.
- **[I]** My own inference.

Model names from after mid-2026 (Opus 5, Fable 5, GPT-5.5/5.6) are as the sources report them.

## Bottom line

- **People return for utility, not to vote.** The main draw is free and early access to frontier models. Spectacle, such as a "mystery model", causes spikes; utility keeps the base.
- **Revenue comes from AI labs, not from visitors.**
  - Arena sells private evaluations and preference data to labs: annualised revenue was $30M in Dec 2025 and reportedly $100M in Jun 2026 [S].
  - Design Arena claims $60M ARR [S].
  - Yupp paid users for votes, raised $33M and shut down in Mar 2026 [S].
- **"Break the model" games drew the most public participation.** Gandalf had more than 1M players and Gray Swan's agent challenge collected 1.8M attacks. They share clear win conditions, levels, prizes and leaderboards. Their data became datasets and papers.
- **Model-vs-model social and economic games give the most quotable findings about specific models.** Examples: Claude models forming price cartels, and o3 deceiving other players in Diplomacy. These findings are credible only with luck and seat controls and many games.
- **The main threats to credibility** are style bias, labs testing many variants privately, vote rigging, single-run "exhibitions" reported as rankings, and operator conflicts of interest.

## 1. Existing arenas

### 1a. Arenas where humans vote

| Arena | Mechanism | Traction |
|---|---|---|
| **Arena** (formerly LMArena / Chatbot Arena) | The user writes a prompt, two anonymous models answer, the user votes. Bradley-Terry ratings with confidence intervals. | 3M+ votes, 400+ models and 300+ pre-release tests by Apr 2025 [P]. More than 5M monthly users; renamed "Arena" on 28 Jan 2026 [S]. $100M seed at a $600M valuation (May 2025); $150M Series A at $1.7B (Jan 2026) [S]. |
| WebDev Arena, now **Code Arena** | Two models each build a web app; the user tries both. | 80k votes by Mar 2025. Votes were deduplicated from 103,096 to 61,473 because the homepage's sample prompts dominated [P]. Code Arena launched 17 Nov 2025 and went full-stack on 2 Jul 2026 [S]. |
| **Copilot Arena** | A VS Code extension shows two code completions side by side. | 4.5M suggestions but 11k judgements [S]. 833 voters and 200–250 daily users at launch (Nov 2024) [P]. |
| RepoChat / Search Arena | Chat about a GitHub repo; compare search-augmented models. | RepoChat: 12,732 conversations but only 4,857 votes [P]. Search Arena votes track answer length and citation count [P]. |
| **RedTeam Arena** ("Bad Words") | Players try to make a model say a target word. Elo is computed over player × model × prompt. | "Thousands of users" at launch (Sep 2024) [P]. |
| **Design Arena** (YC S25, ex-Arcada Labs, company now "Intelligence") | The user picks a prompt and a medium (site, game, 3D, image, video, slides, audio). Four anonymous models answer. Five pairwise votes rank them 1–4 [S]. | 47k users in its first 4 weeks (Jul 2025) and 5.3M users by Aug 2026 [S]. $7.9M seed led by Index Ventures (Aug 2026) [S]. Claims ARR went from $5M to $60M in six months, from a few labs buying private evaluations and preference data [S]. Labs cite it at launch, e.g. GLM-5.2 "#1" [S]. |
| Yupp (2025–26) | Side-by-side comparisons; users earned credits. | 1.3M users. Shut down 31 Mar 2026 because labs moved to expert-sourced and agentic data [S]. |

### 1b. Arenas where models compete against each other

| Arena | Format |
|---|---|
| **Kaggle Game Arena** (Google DeepMind) | All-play-all games: chess (Aug 2025), poker and Werewolf (Feb 2026), more in 2026. Open harness [P]. The chess launch was streamed with Nakamura, GothamChess and Carlsen [S]. Poker runs about 900k hands [S]. |
| **Vending-Bench Arena** (Andon Labs) | Agents each run a vending machine at the same location. They can message, trade and undercut; the score is money made [S]. |
| lechmazur games | **Elimination**: 8 models, public and private chat, votes and a jury; 61 models [P]. **Step Game**: talk, then a secret move; includes silent-bot baselines [P]. **PACT**: buyer–seller bargaining; 9,995 games [P]. **Buyout** (Mar 2026): elimination with money and buyouts [P]. |
| **AI Diplomacy** (Every, now Good Start Labs) | 7-player negotiation streamed on Twitch, with betrayal detection [P]. The spin-out raised $3.6M to sell game data for reinforcement learning (RL) [S]. |
| **CodeClash** (Princeton/Stanford) | Agents edit codebases whose bots compete. 1,680 tournaments; ICML 2026 [S]. |
| Werewolf | Google's Werewolf Arena (2024, agents bid to speak); Foaster (2025, a separate Elo per role); Kaggle (2026) [S]. |
| **Alpha Arena** (Nof1) | 6 models traded $10k each of real money in crypto, Oct–Nov 2025; Qwen3 Max won and most lost [S]. |
| PokerBattle.ai | 9 models, 3,799 play-money hands; o3 won and Llama 4 went bust [S]. |
| SnakeBench | Cut back on cost: "Disable ladder matchmaking to reduce recurring game costs" (2026) [P]. |

## 2. Traction and retention evidence

**What brings people back**
- **Free and early access to frontier models.** LMArena: "a valuable experience involves having frequent access to the best models, and being a part of the first to access the newest ones". Its sampling therefore favours top and new models [P].
- **Mystery models are the largest growth events.** "Nano-banana" (Aug 2025) brought about 10× traffic, more than 3M monthly users and 5M+ votes in two weeks [S].
- **Polish.** In 2025 surveys users called the site "janky" and "laggy"; the rebuild added login and saved history [P].
- **Embedding the arena in real work yields lots of use but few explicit votes.** Copilot Arena: 4.5M suggestions vs 11k votes. RepoChat: 12.7k conversations vs 4.9k votes. So design for implicit signals [P/S/I].
- **Spectacle works in bursts.** Examples are the Kaggle chess stream, Diplomacy on Twitch, Alpha Arena's real money, and lechmazur's replays. No arena publishes retention numbers [I].
- **Stakes.** Polymarket runs monthly markets on which company has the top model, settled by Arena's leaderboard; some months traded $2.7–3.1M [S]. In Tensor Trust, each player defends their own "bank account" [S].

**Documented problems**
- **Leaderboard Illusion** (Apr 2025; 2M battles). Labs tested variants privately and withdrew bad scores; Meta tested 27 variants before Llama 4. Google and OpenAI got about 20% of the data each [S]. LMArena's reply estimated "around +11 Elo after 50 tests and 3000 votes" and added "provisional" labels [P].
- **Llama 4.** Meta launched citing a chat-tuned experimental variant ranked #2; the released model ranked about 32nd [S].
- **Style bias.** Controlling for length and markdown, or for sentiment and emoji, reorders the rankings: Grok-3 and the experimental Llama 4 drop, Claude 3.7 rises [P]. An audit by Surge AI, a data-labelling vendor, disagreed with 52% of 500 sampled votes [S].
- **Gaming.**
  - A few hundred to about a thousand rigged votes can move ranks (arXiv 2501.17858) [S].
  - Which model wrote a reply can be identified with more than 95% accuracy (arXiv 2501.07493) [S].
- **Conflicts of interest.** Arena sells evaluations to the labs it ranks [S]. Google runs Kaggle Game Arena, and Gemini led at its relaunch [S].

## 3. "Break the model" games

| Game | Participation | What made it sticky | Data outcome |
|---|---|---|---|
| **Gandalf** (Lakera, 2023–) | More than 1M players, 40M prompts and guesses [S]. | 8 levels with escalating defences; one goal: get the password. | Public datasets and the paper "Gandalf the Red" [P/S]. The data fed Lakera's product; Check Point bought Lakera for about $300M in 2025 [S]. |
| **HackAPrompt** | 1.0 (2023): 2,800+ participants, 600k+ prompts, $37.5k in prizes [S]. 2.0 (2025): prize pools up to $500k, run "like a season of a videogame" [S]. | Levels, tracks, bounties, leaderboard. | Public dataset; EMNLP 2023 best theme paper [S]. |
| **Tensor Trust** (Berkeley, 2023) | 126k attacks and 46k defences (later dump: 563k attacks) [S]. | Player-vs-player economy: defend your account and steal other players' balances. | ICLR 2024 spotlight paper; open data [P]. |
| **Gray Swan Arena** | Agent challenge with the UK AI Security Institute (2025): 1.8M attacks, 62k successful, 22 models, $171.8k in prizes [S]. More than $300k in prizes overall [S]. | Rolling waves, cash, live leaderboard, Discord, sponsoring labs. | ART benchmark paper: indirect injection succeeded 27.1% of the time vs 5.7% for direct; robustness weakly linked to model scale [S]. |

**Common traits [I]:**
- A binary, checkable win condition, so no judge disputes.
- Escalating levels.
- Public ranks and cash prizes.
- A community.
- Sponsors who need the data.

## 4. Model-vs-model formats with repeatable findings

- **Vending-Bench Arena** [S]
  - Claude Opus 4.6 got all three rivals to fix prices and won.
  - Claude Opus 5 proposed or joined a cartel in 6 of 6 runs and broke 11 truces (its rivals broke 2 and 1). It paid customers $8.54 in refunds vs GPT-5.6 Sol's $655.
  - Andon Labs reports that Claude models are both the top earners and the most collusive across versions. This held across rounds, which makes it the most robust finding here.
- **AI Diplomacy**
  - o3 kept up false alliances and timed betrayals; Claude Opus 4 "refused to lie" and lost [S].
  - The repo measures each model's lie rate (0–100%) by comparing its messages with its orders [P].
- **Elimination Game.** Social rank does not follow reasoning rank: GPT-4o is #7 and o3 is #22; Gemini 3 Flash is #5 and Gemini 3 Pro is #16 [P].
- **Step Game.** "Large frontier models charm first, then knife their partners late". The Silent Random bot scores 0.66 vs GPT-5's 5.49 [P].
- **Werewolf (Foaster).** GPT-5 won 96.7% of games and kept a 93% manipulation rate as a werewolf [S].
- **CodeClash.** Claude Sonnet 4.5 won 0 of 150 rounds against a strong human-written bot [S].
- **Kaggle Game Arena.** Skill does not carry over between games, and rules must be checked so models cannot exploit fixed mechanics [S].

**How arenas control for luck, seat and starting conditions**
- **Mirrored match packs** (Buyout Game). The same setup is replayed with seats swapped, and only complete pairs count. A published chart shows seat luck exists but does not dominate [P].
- **Duplicate deals and volume.** Kaggle poker plays about 900k hands [S]. PokerBattle's 3,799 hands and Alpha Arena's single run are entertainment, not evidence. Nof1 later moved to several competitions with identical inputs [S].
- **Role balance.** Foaster rates each role separately; Werewolf Arena assigns roles at random [S].
- **Order effects.** TrueSkill ratings are averaged over 500 random orderings of the game logs [P].
- **Baselines.** Scripted silent bots (Step Game); truthful buyer and seller baselines with fixed seeds (PACT) [P]; set chess openings (Kaggle) [S].
- **Uncertainty.** PACT's #1, GPT-5.5 at 1607 (1595–1619), and #2, Fable 5 at 1603 (1587–1620), are tied once confidence intervals are shown [P].

## 5. Talking points

1. **Utility before spectacle.** Arena retains millions by giving free, early access to frontier models. Our "watch models compete" pitch must answer: what does the visitor leave with, for example the best answer to their own problem [I]?
2. **Give spectators a stake.**
   - Let them predict the winner, with a personal calibration score and streaks.
   - Let them set the challenge: their prompt, puzzle or attack.
   - Polymarket, Tensor Trust and Gandalf show that stakes and ownership bring people back.
3. **Progression, seasons and fresh content.** Use levels, seasons with prizes, and new or mystery models. Budget cost per match: SnakeBench had to drop its continuous ladder over cost.
4. **Rank on objective game outcomes; use human votes for taste.** Human votes reward length, style, confidence and citations. Keep spectator votes in a separate, style-controlled leaderboard.
5. **Remove luck before publishing a ranking.** Use mirrored seats, duplicate deals and role balance. Play hundreds of games per model, report confidence intervals and include baselines. Label showpieces as exhibitions.
6. **Behavioural findings and data are the most valuable output.** The collusion and deception results drew press and lab attention. Break-it data became datasets, papers and a $300M acquisition. Plan open logs, a replay viewer and data licensing from day one.
7. **Governance is part of the product.** Publish rules on pre-release variants, provisional labels and data access. Add defences against rigging (login, rate limits, checks against identifying models). Disclose conflicts of interest.
8. **Business reality.** Keep the visitor side free; revenue comes from labs buying private evaluations and data. Yupp shows that paying people for generic votes is not a moat. Pick a niche where our data is scarce, such as multi-agent or agentic behaviour [I].

**Biggest pitfalls:**
- Style-driven rankings.
- Selective private testing by labs.
- Rigging and models being identified.
- Single runs with small samples.
- Running costs.
- An operator who also competes.
- Harness effects mistaken for model skill.
- PR risk from showcasing deception.
- Unclear consent for visitor data.

## Sources

**Primary [P]**
- LMArena blog sources: https://github.com/lmarena/lmarena.github.io/tree/main/_posts. Posts used: style-control, redteam-arena, copilot-arena, repochat-arena, webdev-arena, search-arena, new-beta, sentiment-control, two-year-celebration, our-response (2024–25).
- github.com/lechmazur/{elimination_game, step_game, pact, buyout_game}
- github.com/GoodStartLabs/AI_Diplomacy
- github.com/CodeClash-ai/CodeClash
- github.com/google-deepmind/game_arena
- github.com/HumanCompatibleAI/tensor-trust
- github.com/lakeraai/dsec-gandalf
- github.com/gkamradt/SnakeBench (commit log)

**Secondary [S]**

*Arena and Code Arena*
- en.wikipedia.org/wiki/Arena_(AI_platform)
- sacra.com/c/lmarena
- techcrunch.com/2026/01/06/lmarena-lands-1-7b-valuation-four-months-after-launching-its-product/
- 36kr.com/p/3452202289092230 (nano-banana)
- cryptobriefing.com/code-arena-fullstack-ai-model-rankings/
- proceedings.mlr.press/v267/chi25a.html (Copilot Arena paper)

*Arena critiques*
- arxiv.org/abs/2504.20879 (The Leaderboard Illusion)
- arXiv 2501.17858 and 2501.07493 (vote rigging)
- Llama 4 coverage and the Surge AI audit, via `research/notes/arenas_preference.md`

*Design Arena and Yupp*
- techcrunch.com/2026/08/03/designarena-creators-raise-7-9-million-to-bring-taste-to-ai-models/
- ycombinator.com/launches/O5h-design-arena-1-benchmark-for-ai-design
- aiweekly.co/alerts/design-arena-maker-intelligence-raises-79m-seed-at-60m-arr
- techcrunch.com/2026/03/31/yupp-ai-shuts-down-33m-a16z-crypto-chris-dixon

*Polymarket*
- polyguana.com/market/547728 (a third-party mirror of Polymarket data)

*Break-the-model games*
- arxiv.org/abs/2501.07927 (Gandalf)
- venturelab.swiss/Lakera-acquired-by-Checkpoint-in-USD-300-million-deal
- arxiv.org/abs/2311.16119 (HackAPrompt)
- learnprompting.org/blog/announce-hackaprompt-2
- decrypt.co/323351/how-to-trick-chatgpt-and-get-paid-50000/
- proceedings.iclr.cc/paper_files/paper/2024/hash/519c51529c3544b3430bd8b17d400365-Abstract-Conference.html (Tensor Trust)
- grayswan.ai/news/uk-aisi-x-gray-swan-agent-red-teaming-challenge-results-snapshot
- arxiv.org/abs/2507.20526 (ART benchmark)
- app.grayswan.ai/arena/about

*Vending-Bench Arena*
- andonlabs.com/evals/vending-bench-arena
- andonlabs.com/blog/opus-4-6-vending-bench
- andonlabs.com/blog/opus-5-vending-bench
- shellypalmer.com/2026/07/claude-opus-5-topped-a-vending-machine-benchmark-and-broke-eleven-truces/

*AI Diplomacy*
- every.to/context-window/would-your-llm-ever-lie-to-you
- every.to/on-every/our-new-incubation-raised-3-6-million-to-teach-ais-to-play-games

*Kaggle Game Arena*
- siliconangle.com/2025/08/04/google-deepmind-host-ai-chess-tournament-evaluate-leading-ai-models-reasoning-skills/
- pokerlistings.com/news/google-hosts-final-ai-poker-matches-in-the-game-arena
- emergentmind.com/papers/2609.31473

*Other model-vs-model arenas*
- foaster-werewolf-benchmark.static.hf.space (Werewolf)
- arxiv.org/abs/2511.00839 (CodeClash)
- forklog.com/en/four-out-of-six-ai-models-suffer-losses-in-trading-tournament/ (Alpha Arena)
- pokernews.com/news/2025/11/poker-bot-battle-results-49971.htm (PokerBattle.ai)

**Not verified:** HackAPrompt 2.0's final participation; Kaggle's per-game standings; stream viewer counts; retention or cohort data for any arena (none published).

# Phase 4 red team R4: prior art and interest (Q6)

As of 30 Sep 2026. Reviewer R4, adversarial. Lens: rubric Q6 ("Is it interesting enough that people would care about the results?") plus pre-emption (does essentially the same benchmark or game already exist, 2023–2026?).

**Independence.** Candidates were read only from `phase3/candidates_spec.md`. I did not open `ideation_rationale.md` or any `ideas_*.md`. Other evidence: `phase2/design_principles.md` (§3, §4 P19–P20, §7), the Phase 1 dossiers (mainly B, C, D, E and F), and about 45 web searches.

**Evidence tags.** [V] seen this session in search results (title and abstract level; arXiv PDFs not opened); [V2] secondary source only; [B] my background knowledge, not re-verified; [D-x] fact-checked Phase 1 dossier x; [spec] speculation.

genstrat.org and understandingai.org were blocked, so their content comes from search summaries only. Reference numbers [R#] point to the list in §5.

---

## 0. How Q6 was scored

**What predicts adoption** (dossier evidence):
- **What got adopted.**
  - AutomationBench is in the Opus 5.5 launch table. Zapier runs it as a neutral runner: deterministic grading, a private split, and a purchase-relevant task [D-C §2A].
  - ARC-AGI-3 appears in the Opus 5 system card (§8.14.2, 30.16%) [D-D].
  - Vending-Bench 2 appears in Google's Gemini 3 Pro evaluation, which leaves out Google's own Game Arena [D-D §5].
- **What labs put in headline tables.** Every Opus 5.5 headline row is agentic, knowledge-work, HLE, computer-use or chart. None covers abstention, calibration, learning, or perception without tools [D-E].
- **Games in lab tables.** A lead dossier found conventional games in 0 of 34 lab headline tables. This was not recounted [D-D §5 Gaps; uncertain].
- **What died.** Headroom does not buy adoption: OfficeBench (47% vs 93%), TopoBench and Game Reasoning Arena [D-C]. SnakeBench turned off matchmaking "to reduce recurring game costs" [D-D]. Pokémon runs and Alpha Arena drew attention, not adoption [D-D, R32].

**Scale used (1–5):** 5 = a realistic path to a lab launch table, or an ARC-level brand with public participation; 4 = a likely system-card or third-party-index (AA, Epoch) entry plus a press-ready story; 3 = a plausible community board or press showcase, lab citation unlikely; 2 = a niche research audience; 1 = nobody would care.

No candidate scores 5. None has a steward of the ARC, Zapier or AA kind, and in 2026 no lab table admits A1 perception or learning rows without one.

**Verdict rule on this lens:**
- **Kill** when pre-emption is strong *and* the twist would not change the headline story, or when a live-human or physical dependency makes third-party reproduction impossible *and* the construct is already covered.
- **Revise** when a real twist or audience survives only after a change of headline, a merge, or a new steward.
- **Keep** when Q6 ≥ 4 and pre-emption is partial.

---

## 1. All 47 candidates

| ID | Name | Q6 | Pre-emption (closest existing work) | Main attack | Fix | Verdict |
|---|---|---|---|---|---|---|
| C01 | Kinetic | 3 | **Strong.** SpookyBench / "Time Blindness" (CVPR 2026): frames are noise alone, humans far ahead of models [R1]. ActPLD point-light MLLM test [R2]. Name collides with DeepMind's Kinetics dataset [R3] | SpookyBench already owns the headline "single frames are noise; video models are time-blind", and its data has been public since 2025. Threshold ratios are psychophysics jargon, and no lab sells motion-defined-shape perception [D-E] | Rename. Ship it as SpookyBench's renewing, staircased successor, inside one A1 perception battery with C04, C06 and C11 | revise |
| C02 | Live Rig | 3 (press 4, labs 1) | **Partial.** Butter-Bench, LLM-controlled robots: 40% vs 95% humans [R4]. CyberRunner beat humans at a labyrinth with RL [R5]. Distributed real-robot evaluation networks [B] | The best video story in the set, but no third party can reproduce physical rigs. A single operator is a maintenance cliff, and rig drift breaks comparisons between seasons. Robotics labs won't enter an API-LLM contest | Run it as a yearly showcase through an existing real-robot evaluation network. Never make it a headline number | revise |
| C03 | Novel Expert | 2 | **Partial.** Category-learning paradigms (information-integration vs rule-based, COVIS) [B]; Bongard-style few-shot sets [B]. I found no LLM version with feedback on every trial | "Trials to 80% on blended-boundary creatures" means nothing outside psychology. Tools-on means training a classifier, which hits the ceiling; a tools-off headline looks artificial to labs | Fold it into a perception battery as a sub-score | kill |
| C04 | Earworm | 2 | **Partial.** MMAU-Pro (AAAI 2026): humans 77.9% vs best model 59.2% [R6]. MUSE music-perception benchmark [R6] | A human-over-AI audio gap is already published. The streaming tap-along track runs only on the few real-time audio APIs, so the leaderboard would have holes. Novel tunings are niche | Aim it at real-time voice APIs, with tap-along and source counting as the headline; drop the rest | revise |
| C05 | Stump Arena | 4 | **Strong on mechanism.** HLE: model-fail gate plus a $500k prize pool [R7]. Dynabench and "Beat the AI" adversarial loops [R9]. Blind-Spots-Bench (Jul 2026): human-easy, model-hard items [R8] | The mechanism is old. Scoring each model against a panel penalises the panel's labs. Items drift toward cheap tricks (counting, tokenisation). Dynabench faded without a funded steward | Make "median author-minutes to stump" the headline; I found no prior art for it. Use a cross-lab panel, diversity caps, and a funded neutral steward | **keep** |
| C06 | Alien Physics | 3 | **Partial.** NewtonBench, with altered laws; it became an RL environment in 4.5 months [D-F]. CRONOS, counterfactual physics in video [R10]. QuantiPhy shows VLMs anchored to real-world priors [R10]. IntPhys 2 [D-A] | "Billiards with alien gravity" is fun, but the Open track reduces to fitting a simulator, and NewtonBench shows such families get trained on within months | Make adaptation speed the headline (error on shots 1–5 vs 20–25, against humans). Use it as the physics module of a battery | revise |
| C07 | Tacit Signals | 2 | **Strong on paradigm.** The Tacit Communication Game, a cognitive-science paradigm since about 2010 [R11] | Each release needs live human pairs, costing $600–900 and taking weeks. Human-outcome metrics are low-power (StudentBench: 0 of 364 cells significant [D-B]). Non-verbal conventions are not a product | Fold the bot-partner idea into C44 | kill |
| C08 | Glyph Pact | 2 | **Strong.** ICCA (COLM 2024): MLLMs in repeated reference games do not shorten their messages [R12]. Partner-specificity was tested in Jun 2026 [R12]. Post-training cuts message length by up to 26% [R12] | Both headline findings (efficiency and partner-specificity) are published, and the ability can be trained in one paper's worth of RL | none | kill |
| C09 | First-Run Arcade | 4 | **Partial to strong.** ARC-AGI-3: novel games, no instructions, turn-based [R13]. OmniGameArena (Jun 2026): 12 new real-time Unreal Engine 5 games [R14]. Real-Time Reasoning Gym [R15]. VideoGameBench is dormant [R14] | The real-time track measures API latency as much as cognition. Frontier models may all score near 0 (no separation), and labs will dispute it. ARC could add real-time and take the story. $2–8k per run | Use the paused track as the A2 headline and real time as the A1 headline, plus a latency-normalised variant. Position it as ARC-AGI-3's real-time complement | revise |
| C10 | Two Clocks | 2 | **Partial to strong.** AgileThinker: dual-thread fast and slow LLM agents (ICLR 2026) [R15]; the psychology dual-task literature [B] | Dual-task cost belongs to the agent architecture (a BYOH fast-plus-slow pair wins), so it rates harnesses. The ratio metric is hard to read | Keep it as an ablation inside C09 | kill |
| C11 | Wayfinder | 2 | **Partial.** MindTopo 97.9 vs 61.4 [D-A]. 360CityArena: humans 77.3% vs 17.1% [R16]. MindCube and VSI-Bench [D-A] | A crowded area. Dossier A notes that none of the new spatial benchmarks has become a leaderboard labs track | Merge into the perception and embodied battery; the shortcut and door tests become sub-scores | revise |
| C12 | Cartographer & Scout | 2 | **Strong.** Talk the Walk (2018): a guide with a map and a tourist with first-person views, localising through dialogue [R17]. CVDN and "Where Are You?" [B] | An eight-year-old paradigm. Each model needs $1.5k and 100 human dyads, so no neutral runner could keep pace with releases | none | kill |
| C13 | Deep Seasons | 3 | **Partial.** Continual Learning Bench (Jun 2026) includes a strategic-game domain, and naive in-context learning beats memory systems there [R18]. BALROG NetHack; the NetHack ascension was harness-driven [R18] | Learning slope over 8 campaigns is noisy, and the notebook protocol decides the score (the ARC-AGI-3 harness gap). It competes with C41 for the same "learns from experience" story | Merge with C41. Pre-register the minimum detectable effect. Headline the slope against humans | revise |
| C14 | Kelly Exam | 3 | **Partial to strong.** AA-Omniscience, a third-party index that penalises confident errors [R19]. KellyBench (Apr 2026), a name clash [R19]. LLMs wagering on their own answers (Dec 2025) [R19] | AA already sells "knows what it knows" through an index labs watch. Log-wealth is harder to read than "hallucination rate" | Rename. Merge with C15 and C26 into one self-knowledge exam, and pitch AA as the runner | revise |
| C15 | Prospective Self-Forecast | 3 | **Partial to strong.** P(IK) (Kadavath 2022) [B]. "Looking Inward": self- vs cross-prediction [R20]. "Masked by Consensus" (ACL 2026): self-probes beat peer probes only on disagreement subsets, and only for facts [R20]. "Beyond Confidence" (May 2026) [R20]. MarketBench [R21] | Self-Edge over a panel may be near 0 for every model, which would mean no separation. Twin items leak difficulty | Make the triage payoff the headline: the value of knowing when to decline. Merge with C14 and C26 | revise |
| C16 | Pushback Ledger | 4 | **Strong.** lechmazur's sycophancy board (Aug 2026) [R22]. "Sustained multi-turn pressure" (Sep 2026) [R22]. "It's Not Always Sycophancy" (May 2026) [R22]. FlipFlop and SycEval [R22] | Crowded. Labs run their own sycophancy evaluations in system cards [B]. 2026 papers already treat yielding and resisting as one mechanism | Make discrimination the single number, rotate fallacy templates, and find a neutral runner. Its cost ($15–80) is its edge | revise |
| C17 | Reliability Horizon | 3 | **Strong.** "The Illusion of Diminishing Returns" (ICLR 2026): measures execution horizon when the plan is given [R23]. TMBench correlates r = 0.73 with AIME, MATH and GPQA [R23]. METR's 50% and 80% horizons [D-E] | Every lab would run a made-up register machine in code, not in its head. High correlation with general ability means little new information | Report L95 on agentic tool-use procedures instead of mental simulation | revise |
| C18 | Compaction Chronicle | 4 | **Partial.** "The Compaction Cliff" (Aug 2026): repeated compaction is "almost" unmeasured [R24]. LongMemEval, BEAM and MemoryAgentBench [R24]. Fiction.LiveBench [D-B] | A frozen notes protocol penalises vendors that ship native compaction (ARC-AGI-3: 62.7 vs 98.6 [D-D]). Memory-vendor benchmarks are marketing-polluted | Publish frozen and provider-native tracks side by side. Single number: memory half-life | **keep** |
| C19 | Frozen-Student Tutor | 3 | **Strong to partial.** Teach2Eval (2025): frozen 1–2B students grade the teacher [R25]. Saha et al. 2023 [R25]. StudentBench [D-B] | Tiny frozen students reward prompt engineering for small models, not teaching. StudentBench shows expert-rated teaching and measured learning disagree | Gate on a validity arm with human learners. Rename | revise |
| C20 | Misconception Clinic | 2 | **Partial.** AuditBench: 56 models with implanted behaviours [R26]. Anthropic's auditing game [R26]. Eedi misconception data [B] | Two constructs (diagnosis and minimal patch) for two audiences. Fine-tuning a new pool of learners every quarter is heavy upkeep | Contribute the repair metric to AuditBench | kill |
| C21 | Simulated Futures Exchange | 2 | **Partial.** BoxingGym, DiscoveryWorld, AutumnBench [D-F] | A data-science task with a sandbox, where the AutoML anchor may win. "CRPS share of achievable skill" is hard to read | Fold anything worth keeping into C23 | kill |
| C22 | Long-Tail Futures | 3 | **Strong.** ForecastBench auto-generates dataset questions (ACLED, DBnomics, FRED, Wikipedia, yfinance), has human baselines and is tracked on Epoch's hub [R28]. Context is Key [R28]. QuantSightBench (Apr 2026) [R28] | Same generator idea, with a neutral runner already in place. No-web context packs make it a contest between time-series foundation models. 2,000 questions a week is heavy upkeep | Contribute series without public forecasts to ForecastBench | kill |
| C23 | Hunch Lab | 4 | **Partial.** "Predicting Empirical AI Research Outcomes" (NeurIPS 2025): a system 64.4% vs experts 48.9%; o3 near chance [R29]. Forecasting research success (May 2026) [R29]. BrainBench [B] | Owner compute is $5–20k a season. Runtime and cellular-automaton items dilute the ML story. A scaling-law extrapolator may beat everyone | Headline only (a): "unrun ML experiments, AI vs ML researchers". Lock predictions, then publish results as a public contest | **keep** |
| C24 | MDL Arena | 2 | **Strong.** The KoLMogorov-Test (ICLR 2025): write the shortest program that generates the data, compared with GZIP [R30] | A headline in bits over L_ref is hard to read, and KT already made the compression-as-intelligence point | none | kill |
| C25 | Mechanism Lab | 2 | **Partial.** Studies of LLM auctions and collusion [R31]; "Institutional AI" (Cournot markets) [R31] | A tiny audience. The oracle is the owner's own search, which invites validity disputes. No link to buying decisions | none on this lens | kill |
| C26 | Contractor's Auction | 3 | **Strong.** MarketBench (Apr 2026): agents state a price and a success probability before a task is assigned, and models are poor at it [R21] | Pre-empted five months ago. Profit depends on the anchor bidders' parameters, which makes it pool-relative | Fold the bidding sub-score into the C14/C15 merge | kill |
| C27 | Signal Pit | 3 | **Partial.** Alpha Arena, real-money LLM trading: the Season 1 winner made +22%, then lost in all 4 Season 1.5 competitions [R32]. LLM double-auction collusion [R31] | The public likes real money, not dice-sum toy markets. With code allowed, a 50-line Bayes script reaches the ceiling | Tools-off headline; pitch it as "Alpha Arena without the noise" | revise |
| C28 | Hidden-Dynamics Economy | 3 | **Strong.** Vending-Bench 2 (in Google's Gemini 3 Pro evaluation), Vending-Bench Arena, and FLE, including the hands-off holdout [D-B, D-D]. CEO Arena and CoffeeBench [D-D] | Andon Labs owns the adopted business-sim slot and FLE owns the factory slot | Offer the V/V* oracle normalisation to Andon Labs or FLE | kill |
| C29 | Whodunit Engine | 3 | **Partial.** WhodunitBench (NeurIPS 2024), a name clash [R34]. TurnaboutLLM [R34]. MuSR [B]. Murder-mystery environments with an LLM simulator [R34] | Name collision. Template-parsed questions feel like a parser adventure. It may saturate once models handle question selection | Rename. Add uncapped difficulty knobs (NPC count, liars, budget). Pitch it as cheap and deterministic | revise |
| C30 | Masquerade | 3 | **Strong.** Kaggle Werewolf, run by Google [D-D]. MafiaScope (Jul 2026), belief probing in social deduction [R35]. Clocktower Radio, a Blood on the Clocktower benchmark [R35]. AvalonBench and Among Us [D-D] | The belief-bits twist has been done, and Google runs the big social-deduction arena. $1.5–2k per model, with high seat variance | none | kill |
| C31 | Debate Court | 3 | **Strong.** Khan et al. (ICML 2024): hidden passages, verified quotes, non-expert judges [R36]. Kenton et al. (NeurIPS 2024) [R36]. A May 2026 follow-up [R36] | The protocol is Khan et al. with generated corpora. Truth Advantage is a research metric, not a launch-table row | Hand it to an AISI as a standing oversight evaluation, and report DWR as a persuasion-risk metric | revise |
| C32 | Nomic Engine | 2 | **Partial.** NomicLaw (AIES 2025) [R37]; an LLM self-amendment game (GECCO 2025) [R37]. The name clashes with Nomic AI [B] | The headline (probe accuracy) is static code reasoning with a political wrapper, and Nomic is obscure | Reframe as loophole-finding in governance or smart-contract code | kill |
| C33 | Exploitability Gauntlet | 2 | **Strong.** GENSTRAT (May 2026): procedurally generated two-player zero-sum imperfect-information card games, with a leaderboard [R38]. gg-bench and Kaggle poker [D-D] | GENSTRAT owns the slot. Exploitability in milli-pots is hard to read, and the Open track can run CFR | Offer exact exploitability to GENSTRAT as a metric | kill |
| C34 | Setter's Duel | 3 | **Partial.** Proposer–solver self-play (Absolute Zero) [B]; SATBench puzzle generation [R39]. I found no benchmark that scores a model as setter | A frozen ladder ages fast, so hardness scores inflate over time. Setters can exploit the ladder's tokenisation instead of building depth | Make human solve time a co-headline, and ban encoding tricks | revise |
| C35 | Game Designer's Duel | 2 | **Strong.** GAVEL: LLMs plus evolution generate Ludii games, scored by MCTS playability, balance and depth [R40]. gg-bench [D-D]. Mage (May 2026) [R40] | Competitors write the test set, which is non-stationary and pool-relative. MCTS "depth" can be gamed with branching factor. ARC-AGI-4 is claiming the "can AI invent" story [R13] | none | kill |
| C36 | Season Forge | 3 | **Strong on story.** At the AtCoder World Tour Finals Heuristic, OpenAI was 2nd in 2025 and beat all 12 human finalists in Jul 2026 [R41]. ALE-Bench and an AHC 1st place [R41]. CodeClash: models lost every round to an expert human bot (Nov 2025) [R41] | The human-percentile headline is likely saturated at launch. Prizes cost $20–50k a season. The A2 slot overlaps CodeClash and ALE-Bench | Drop human percentile as the headline. Use an anchored Bradley-Terry scale against the operator's bot; secret games are the differentiator | revise |
| C37 | Saboteur's Patch | 4 | **Strong.** ControlArena (UK AISI and Redwood), with code-sabotage settings [R42]. SHADE-Arena (Anthropic) [R42]. AI Control backdoors [R42] | Labs already run these in-house for system cards. A public "best saboteur" ranking is a PR liability no lab will cite | Headline the auditor only, and ship it as a ControlArena setting with generated repos and witnesses | revise |
| C38 | Relay | 3 | **Partial.** LLM "telephone game" transmission chains [R43]. GlossoGen (Sep 2026) [R43]. Continual Learning Bench [R18] | About 960 humans per run can't be sustained, and note-writing overlaps C18 | Make the AI-only lite track the headline ("notes that help a successor", i.e. agent handoff). Run human chains once, as a study | revise |
| C39 | Blind Spot Cartographer | 3 | **Strong, plus a name clash.** Blind-Spots-Bench (Jul 2026) [R8]; the HLE gate [R7] | The authoring score rewards weakness: more own failures means more accepted items. Items also pass between providers | Credit only items that also stump stronger panel members. Merge it into C05 as the model-author arm | revise |
| C40 | Rules Gauntlet | 3 | **Partial to strong.** gg-bench, and CWM, which writes rules as code and adds MCTS [D-D]. ARC-AGI-3 (blind track) [R13]. LudoBench, rulebook edge cases: rule integration 36% [R44]. GVGAI-LLM [R44] | The blind track duplicates ARC-AGI-3, and the Open rulebook track reduces to simulator plus search | Keep only the long-rulebook edge-case track, pitched as "apply rare clauses in long documents" | revise |
| C41 | Practice Week | 4 | **Partial.** Continual Learning Bench (Jun 2026) [R18]; MemoryBench and SEAGym (2026) [R18] | One new game a season means n = 1 game. 60 games give Elo intervals like LLM Chess's ±110–180 [D-D]. The notes cap dominates | Use 3–5 games a season and a pre-registered minimum detectable effect. Human-vs-AI matches are the spectacle | revise |
| C42 | Hidden-Rule Lab | 3 | **Strong.** ZendoWorld: 73.3% vs 44.5% [R45]. FalsifyBench, WILT, AutumnBench [R45]. WitnessBench, with a private test set and held-out primitives [R45] | The seventh benchmark in a crowded niche. ARC-AGI-3 took the "experiment efficiency" story and closed in about 5 months [D-F] | Keep only the adaptive-adversary mode, a new "worst-case rule learning" story, and absorb C43 | revise |
| C43 | Eleusis Masters | 2 | **Strong.** Metta's Eleusis cogame [R45]; the Hugging Face "game of science" space [D-F]; ZendoWorld [R45] | The solver role is pre-empted. The setter reward ("spread the solvers apart") is pool-relative and can be gamed | Fold the setter role into C42 | kill |
| C44 | Convention Cross-Play | 3 | **Strong.** AH2AC2: Hanabi with human proxies [R46]. "The Convention Gap" (Sep 2026) [R46]. Interchangeability study (Sep 2026) [R46]. Kaggle Hanabi (Sep 2026) [D-D] | Google runs Hanabi at scale, human pairing adds cost, and the only novelty is the seasonal grammar | Headline deterministic cross-play with bots whose conventions are hidden. Absorb C07 and C08 as channel variants | revise |
| C45 | Crowd Oracle | 4 | **Partial.** Centaur / Psych-101 [B]. LLM vs human coordination games (Apr 2026) [R47]. LLM–human strategic baselines (May 2026) [R47]. Focal-point collusion [R47] | A $10–15k panel every season is a recurring cost (SnakeBench cut its ladder over cost [D-D]), and "which humans?" invites controversy | Find a survey-firm sponsor. One number: % of modal payoff. Stratum results are the press hook | **keep** |
| C46 | Grift | 3 (press 4, labs 1) | **Partial.** MakeMePay (OpenAI; in the o1 system card) [R48]. Vending-Bench Arena cartels [D-D]. OpenDeception [B] | $15–20k a season, ethics review, and human grifters that can't be repeated. A "conned rate" among live humans is a PR liability labs won't cite | Add an AI-only track with scripted grifters for reproducibility; run human games as a yearly showcase | revise |
| C47 | Defuse Line | 3 | **Strong.** GPTNT (Jun 2026): Keep Talking and Nobody Explodes, real time, manual and partner withholding; no model defuses a single bomb in real time [R49] | The same design and headline were published three months ago | none; collaborate with GPTNT | kill |

**Counts.**
- **Kill: 18.** C03, C07, C08, C10, C12, C20, C21, C22, C24, C25, C26, C28, C30, C32, C33, C35, C43, C47.
- **Revise: 25.**
- **Keep: 4.** C05, C18, C23, C45.
- **Q6 distribution:** 5 → 0; 4 → 8 (C05, C09, C16, C18, C23, C37, C41, C45); 3 → 24; 2 → 15; 1 → 0.
- **Pre-emption:** strong, or strong on one axis (mechanism, paradigm or story), for 28; partial for 19; none for 0.

---

## 2. Notes on the 12 most promising or contested candidates

### C05 Stump Arena — keep (the strongest on Q6)

**Prior art.** The adversarial filter is old:
- Dynabench and "Beat the AI" [R9].
- HLE crowdsourced about 70k trial questions, kept those frontier models failed, and paid from a $500k pool [R7]. HLE is expert-level, not "easy for humans".
- Blind-Spots-Bench (arXiv 2607.08317, Jul 2026) is closest in spirit: 235 items from graduate students that frontier chatbots failed but humans found easy [R8]. It is a one-off static set with no renewal.

**Twist.** Three things are new together: weekly rounds, a gate of naive paid verifiers, and **cost to stump** (median author-minutes per stumper) as a trendable headline. I found no prior art that headlines cost to stump.

**Who cares.**
- The press: "it now takes a random person 40 minutes to stump AI" is one number with a direction.
- The public: bounties give participation, the ingredient behind ARC's 1,455 teams and about 1M ARC-AGI-3 scorecards (rubric §7 Q6).
- Labs would cite the per-model solve rate only if the brand becomes ARC-like.

**Attacks.**
1. Scoring each model against a panel penalises the panel's labs. The spec's cross-panel qualification helps.
2. Stumpers cluster in cheap tricks. Blind-Spots-Bench's taxonomy hints at perception and counting clusters. That is acceptable for A1, but diversity caps need teeth.
3. A $15–30k-a-season programme with weekly moderation is exactly the upkeep that killed Dynabench-era efforts. Without a foundation-style steward it will die.

[spec] Retired items released after 6 months become training data, so part of any rise in cost to stump will reflect that, not capability.

### C23 Hunch Lab — keep

**Why it scores well.** It is tied to what labs care about most in 2026, automating AI research. The story "can AI predict ML experiment results better than ML researchers?" is press-ready. BrainBench, where LLMs beat neuroscientists at predicting results, drew wide attention [B].

**Prior art.** Wen et al. (arXiv 2506.00794, NeurIPS 2025) pair published ideas [R29]:
- a fine-tuned system scored 64.4% vs experts' 48.9%;
- off-the-shelf o3 was near chance.

A May 2026 follow-up trains forecasters of research success [R29]. Both use *already-published* outcomes, so they can be contaminated.

**Twist.** Running experiments after predictions lock gives uncontaminated ground truth and a distributional score. That changes the construct and makes the result more credible.

**Attacks.**
- Small-MLP deltas may not track frontier research intuition (construct validity) [spec].
- Item types (b)–(d) (runtimes, cellular automata, SAT phase transitions) dilute the story and should be secondary.
- Owner compute of $5–20k a season needs a sponsor.
- Recruiting 40 ML researchers is costly but carries the headline.

### C18 Compaction Chronicle — keep

**What labs sell.** Long-running agents with context management. OpenAI reported that "two settings" (retained reasoning plus compaction) tripled ARC-AGI-3 scores [D-A]. A neutral "memory half-life under self-compaction" number maps straight onto that product (P19).

**Prior art is partial.**
- "The Compaction Cliff in Long-Running AI Agent Memory" (arXiv 2608.22752) states that repeated compaction is "almost" unmeasured [R24].
- Existing memory benchmarks (LoCoMo, LongMemEval, BEAM) are about conversational recall, and memory-tool vendors publish many of the guides [R24]. That creates a credibility gap a neutral benchmark can fill.

**Main attack.** Frozen-versus-native harness capture: the ARC-AGI-3 gap was 62.7 vs 98.6 for the same model [D-D]. Labs with native compaction will quote only their own harness. So publish both, as ARC now does.

**Legibility.** "Half-life in chunks" suits engineers more than the press; a fit for Artificial Analysis or Epoch as runner [spec].

### C45 Crowd Oracle — keep

**Interest.** "Can AI predict what people will choose?" matters to marketers, pollsters and social scientists who use "silicon samples", and to the public.

**Prior art is partial.**
- Centaur (Nature 2025) predicts human behaviour in psychology experiments [B].
- 2026 papers compare LLM and human play in coordination games. One finds LLMs coordinate with each other far more than humans do (72% vs 31% agreement) [R47].
- Focal-point collusion work treats the ability as a safety risk [R47].

None scores models against a *freshly collected, private* human distribution on new items each season.

**Attacks.**
1. A recurring $10–15k panel is the kind of cost that ends community ladders [D-D].
2. "Which humans?" Country strata turn any headline into an argument about representativeness.
3. LLM monoculture: strong models may all converge on the modal choice, which compresses the top of the scale.

**Fixes.** Find a survey firm as sponsor. Headline "% of modal payoff". Publish the AI–AI coordination axis as a safety side result.

### C09 First-Run Arcade — revise (highest-upside game)

**Interest.** "ARC-AGI-3, but real time" is legible, and people can watch it. ARC-AGI-3's entry into the Opus 5 system card [D-D] is the one precedent for a game-like A1 benchmark reaching lab reporting.

**Prior art.** ARC-AGI-3 (turn-based) [R13]; OmniGameArena (Jun 2026: 12 new real-time UE5 games) and V-ICAL Bench (Sep 2026) [R14]; Real-Time Reasoning Gym [R15]; VideoGameBench (dormant) [D-D].

ARC Prize has announced that ARC-AGI-4 will target "open innovation" [R13; V2]. [spec] That may leave the real-time novel-game niche open, or ARC may take it.

**Attacks.**
1. At 10 Hz with API round trips, every frontier reasoning model may score near 0, so there is no A2 separation. The rubric warns that "0% … is most often a signal of a broken task" (P20).
2. Provider latency differs by region and tier, which is unfair, and labs will say so.
3. $2–8k per run.

**Fix.** Make the paused track the A2 headline and real time the A1 story, with a latency-normalised variant. Approach ARC Prize as a partner, not a competitor.

### C16 Pushback Ledger — revise

**Interest.** Sycophancy is the most press-visible behavioural failure since the 2025 GPT-4o rollback [B], and labs discuss it in system cards [B].

**Pre-emption is strong.**
- lechmazur's sycophancy board, updated 5 Aug 2026, with an abstention column [D-B].
- "Measuring LLM Sycophancy under Sustained Multi-Turn Pressure" (Sep 2026) [R22].
- "It's Not Always Sycophancy" (May 2026). It argues that yielding and resisting are "one belief-updating mechanism" and calls for telling "healthy revision" from capitulation [R22]. That is C16's symmetric thesis.

**What's left.** A deterministic, standing, symmetric discrimination score with frozen pre-verified challengers and a human baseline. It costs only $15–80 a run, which makes it index-friendly.

**Attack.** It can be gamed by learning to switch only when the challenge includes a checkable derivation. Rotate fallacy templates that include fake derivations.

**Verdict.** Worth doing only with a neutral runner; otherwise it is the fifth sycophancy board.

### C41 Practice Week (with C13 Deep Seasons) — revise and merge

**Interest.** Whether AI "improves with practice" is a central 2026 question. Continual Learning Bench (arXiv 2606.05661) found "naive ICL outperforms systems dedicated to memory management" [R18]. MemoryBench, SkillLearnBench and SEAGym also appeared in 2026 [R18]. Human-vs-AI matches after a week of practice are a spectator story. The Practice Week format gives the clean, legible story; C13 gives the richer world.

**Attacks.**
- **Power.** One new game a season is n = 1. Sixty games against a ladder give LLM-Chess-like Elo intervals of ±110–180 [D-D].
- **Harness.** The notes protocol decides the score [D-E, D-F].
- **Budget.** Both candidates spend tokens on the same story.

**Fix.** One product with two tracks (abstract game and roguelike campaign), 3–5 new games a season, and a pre-registered minimum detectable effect.

### C36 Season Forge — revise

**Pre-empted story.** At the AtCoder World Tour Finals Heuristic, OpenAI's system placed 2nd in 2025 and "completely" beat all 12 human finalists in July 2026 [R41; V2]. Sakana's agent won AHC058, and ALE-Bench exists [R41]. The "AI vs contest veterans on a timed heuristic or bot task" story is told, and humans lost.

**Counter-evidence.** In CodeClash, top models lost every round to an expert human bot (Nov 2025) [R41; V2], so a gap on secret strategy-game bots may last a season or two.

**Q6.** Bot-writing is close to what labs sell (agentic coding), a better lab path than most games. But a human-percentile headline would likely hit 100% at launch, and $20–50k a season in prizes buys little.

**Fix.** Keep the human arm for one or two seasons as a headroom check. Make the anchored Bradley-Terry rating against the operator's 10×-time bot the durable scale. Differentiate from CodeClash through secret games.

### C37 Saboteur's Patch — revise and contribute

**Adoption channel.** System-card safety sections, where SHADE-Arena and ControlArena-style evaluations appear [R42].

**Pre-emption is strong.**
- ControlArena (UK AISI and Redwood) already has code-sabotage settings [R42].
- AI Control's backdoor paradigm is the template [R42].

**Twist.** Generated repos with formal property suites and execution-verified witnesses. That is deterministic and scalable.

**Main attack.** A public saboteur leaderboard is dual-use and a PR liability, so labs won't cite it. Headline the auditor only.

**Best path.** Ship it as a ControlArena setting rather than a new brand.

### C14 Kelly Exam (with C15 and C26) — revise and merge

**The niche is taken.**
- AA-Omniscience already runs "knows what it knows" through a neutral index. An always-abstain model would place 4th of 36 [D-B].
- KellyBench (arXiv 2604.27865, Apr 2026) takes the name [R19].
- LLM wagering on own answers was studied in Dec 2025 [R19].
- MarketBench (arXiv 2604.23897) found models "poor at forecasting both their success probability and their token usage", and those errors carry into auctions [R21]. That pre-empts C26 and much of C15.
- "Masked by Consensus" finds a self-advantage only on factual disagreement subsets [R20], so C15's Self-Edge may be near zero everywhere.

**What would matter.** One maintained "Self-Knowledge Exam" for agents, combining bet sizing, triage and bidding. Headline "value recovered by knowing when to decline". Pitch AA as runner. Separately they are three weak entries.

### C42 Hidden-Rule Lab — revise, narrowly

**The most crowded niche in the set:** ZendoWorld (humans 73.3% vs VLMs 44.5%), FalsifyBench, WILT, AutumnBench, InductionBench, Hero's Journey, WitnessBench (private test, held-out primitives) and Metta's Eleusis cogame [R45, D-F]. ARC-AGI-3 already turned experiment efficiency into a headline and was saturated in about 5 months [D-F].

**What's left.** The adaptive-adversary mode: the hidden rule is committed only after the subject's experiments, to maximise errors. It gives a new "worst-case learner" story that none of the above has.

**Fix.** Ship only that mode, absorb C43's setter role, and approach the ZendoWorld or Witness authors about hosting it.

### C47 Defuse Line — kill (a contested kill)

GPTNT (arXiv 2606.28514, Jun 2026) builds on Keep Talking and Nobody Explodes, with split information, a live countdown and optional withholding of the manual or partner [R49]. Its headline: "not one of the closed- and open-source models tested defuses a single bomb in real time, a bar that human players clear". C47's real twists (a manual generated fresh each episode, blind human operators) do not change that headline, so a launch would read as a copy. Only path: contribute generated manuals to GPTNT.

---

## 3. Top 10 survivors on this lens

1. **C05 Stump Arena.** The headline "cost to stump" is new; public participation is built in. It needs an ARC-style steward.
2. **C23 Hunch Lab.** The AI-research-automation story, with uncontaminated ground truth. It needs a compute sponsor.
3. **C18 Compaction Chronicle.** Directly about what labs sell (long-running agents). Frozen and native tracks.
4. **C09 First-Run Arcade.** The only A1 game with an ARC-AGI-3-like lab path. It must solve latency and partner rather than compete with ARC.
5. **C45 Crowd Oracle.** Broad public interest and a fresh private human distribution. It needs a panel sponsor.
6. **C16 Pushback Ledger.** High salience and cheap. It survives only with a neutral runner and the symmetric score as headline.
7. **C41 Practice Week + C13 Deep Seasons**, merged. The continual-learning narrative. Needs 3–5 games a season for power.
8. **C37 Saboteur's Patch.** The safety-section channel. Auditor-only headline, shipped as a ControlArena setting.
9. **Self-Knowledge Exam (C14 + C15 + C26 merged).** A live finding (MarketBench) and a natural AA index entry. Separately each is pre-empted.
10. **C29 Whodunit Engine.** Cheap ($20–100), deterministic, and legible ("AI detective vs puzzle fans"). Must be renamed.

Next in line: C38 (AI-only handoff), C36 (A2 only), C40 (rulebook track only).

---

## 4. The 10 most fatal flaws across the set

1. **Same design already published.** C08 (ICCA and the partner-specificity paper), C12 (Talk the Walk), C22 (ForecastBench), C24 (KoLMogorov-Test), C26 (MarketBench), C30 (MafiaScope, Kaggle Werewolf), C33 (GENSTRAT), C35 (GAVEL), C47 (GPTNT). Launching any of these reads as a copy; pre-emption kills at launch (principles §3, mode 12).
2. **Crowded niches split attention.** Hidden-rule learning (C42/C43: at least 7 prior benchmarks), social deduction (C30), Hanabi-style cooperation (C44), spatial exploration (C11), memory (C18) and sycophancy (C16). None of the recent spatial or video benchmarks has become a leaderboard labs track [D-A].
3. **Games start with an adoption deficit.** 27 of 47 candidates are games; games appear in 0 of 34 lab headline tables [uncertain, D-D]; Google's own evaluation left out Google's Game Arena [D-D]. Only ARC-AGI-3 and Vending-Bench 2 crossed over, both with neutral stewards and human or economic anchors.
4. **Live humans are needed for every model release.** C02, C07, C08, C12, C38, C44 (human arm), C45 (panel), C46, C47, and C36 (prizes). This means recurring five-figure costs, weeks of delay and no third-party reproduction. Human-outcome metrics are also low-power: StudentBench measured learning with 0 of 364 cells significant [D-B].
5. **The headline measures the harness or infrastructure, not the model:** C10 (dual-task architecture), C13, C18, C38 and C41 (notes protocols), C09 (API latency). ARC-AGI-3 moved from 62.7 to 98.6 on harness alone [D-D]; labs will quote whichever track flatters them.
6. **The human-vs-AI story is already settled, or will be at launch:** C36 (AtCoder 2026 [R41]), C45 (LLMs out-coordinate humans with each other [R47]); the Open tracks of C17, C27 and C33 hit the ceiling with a short script. Several "both"-archetype A1 framings may be dead on arrival.
7. **Tools-off headlines on problems code solves.** C03, C17, C21, C24, C27 and C33. Labs, and design principle P4, treat banning code as artificial. The tools-on track saturates, so neither track tells a story labs will repeat.
8. **Illegible headline metrics:** bits over L_ref (C24), milli-pots (C33), CRPS share of achievable skill (C21), dual-task ratio (C10), Repair − 2·Harm (C20), Σdepth/√lines (C35), log-wealth (C14). None survives a one-sentence press test (P20).
9. **Self-referential or pool-relative scores with perverse incentives:** in C39 weaker authors get more items accepted; C43's setter reward is pool-relative; in C35 competitors write the test set; C05 scores each model against a panel; C26 and C27 profits depend on anchor parameters. Such scores are non-stationary and easy to dispute (principles §3, mode 10).
10. **Upkeep beyond any plausible steward.** Every candidate needs secret generators rotated quarterly by a named owner; some add physical rigs (C02), 2,000 questions a week (C22), quarterly fine-tuned learners (C20), seasonal human panels (C45) or 960-person chains (C38). Adoption failure, not saturation, killed TopoBench, OfficeBench and Game Reasoning Arena [D-C]. As a portfolio, the programme can maintain perhaps 2–3 of these [spec].

**Also.** Name collisions: Kinetic (Kinetics), Kelly Exam (KellyBench), Nomic Engine (Nomic AI), Whodunit Engine (WhodunitBench), Blind Spot Cartographer (Blind-Spots-Bench). Dual-use optics: saboteur, grift and deception leaderboards (C37, C46, C30) that labs will not cite.

---

## 5. References

Tags as in the header; arXiv PDFs were not opened.

- **R1.** SpookyBench / "Time Blindness" (CVPR 2026) [V]; https://arxiv.org/abs/2505.24867; https://github.com/TimeBlindness/time-blindness
- **R2.** ActPLD, point-light biological motion in MLLMs [V]. https://arxiv.org/abs/2509.23517
- **R3.** Kinetics dataset (DeepMind, 2017) [B]. https://arxiv.org/abs/1705.06950
- **R4.** Butter-Bench (40% vs 95% humans) [V]. https://arxiv.org/abs/2510.21860
- **R5.** CyberRunner, labyrinth [B]. https://arxiv.org/abs/2312.09906
- **R6.** Audio benchmarks: MMAU-Pro [V]: https://arxiv.org/abs/2508.13992; MUSE [V]: https://arxiv.org/abs/2510.19055
- **R7.** HLE: Nature paper [V]: https://www.nature.com/articles/s41586-025-09962-4; Scale results [V]: https://scale.com/blog/humanitys-last-exam-results
- **R8.** Blind-Spots-Bench (Jul 2026) [V]. https://arxiv.org/abs/2607.08317
- **R9.** Adversarial human-in-the-loop data collection: Dynabench [B]: https://arxiv.org/abs/2104.14337; Beat the AI [B]: https://arxiv.org/abs/2002.00293
- **R10.** Physics: NewtonBench [D-F]: https://raw.githubusercontent.com/HKUST-KnowComp/NewtonBench/main/README.md; CRONOS [V]: https://arxiv.org/abs/2605.23699; QuantiPhy [V]: https://arxiv.org/abs/2512.19526
- **R11.** Tacit Communication Game [V]. https://www.researchgate.net/publication/271824613_Higher-order_theory_of_mind_in_the_Tacit_Communication_Game
- **R12.** Reference games and conventions: ICCA, "Talk Less, Interact Better" [V]: https://arxiv.org/abs/2408.01417; "Aligned but Not Partner-Specific" (Jun 2026) [V]: https://arxiv.org/abs/2606.08081; Convention-formation post-training [V]: https://arxiv.org/abs/2508.06482
- **R13.** ARC: ARC-AGI-3 [D-D]: https://arcprize.org/arc-agi/3; ARC-AGI-4 "open innovation" announcement [V2; uncertain]: https://www.kucoin.com/news/flash/arc-prize-announces-next-ai-benchmark-focused-on-open-innovation
- **R14.** Video-game benchmarks: OmniGameArena [V]: https://arxiv.org/abs/2606.09826; V-ICAL Bench [V]: https://arxiv.org/abs/2609.15683; VideoGameBench [D-D]: https://arxiv.org/abs/2505.18134
- **R15.** Real-Time Reasoning Gym / AgileThinker (ICLR 2026) [V]. https://arxiv.org/abs/2511.04898
- **R16.** 360CityArena [V]. https://pith.science/paper/2608.08814 (MindTopo, MindCube, VSI-Bench: [D-A])
- **R17.** Talk the Walk [V]; https://arxiv.org/abs/1807.03367; https://github.com/facebookresearch/talkthewalk
- **R18.** Learning from experience: Continual Learning Bench [V]: https://arxiv.org/abs/2606.05661; NetHack ascension [V]: https://kenforthewin.github.io/blog/posts/llm-nethack-ascension/; BALROG [D-D]
- **R19.** Calibration and betting: AA-Omniscience [D-B]: https://arxiv.org/abs/2511.13029; KellyBench [V]: https://arxiv.org/abs/2604.27865; LLM wagering, "Going All-In on LLM Accuracy" [V]: https://arxiv.org/abs/2512.05998
- **R20.** Self-knowledge and introspection: Looking Inward [V]: https://arxiv.org/abs/2410.13787; Masked by Consensus (ACL 2026) [V]: https://aclanthology.org/2026.acl-long.483/; Beyond Confidence [V]: https://arxiv.org/abs/2605.07806; Kadavath et al. [B]: https://arxiv.org/abs/2207.05221
- **R21.** MarketBench (Apr 2026) [V]. https://arxiv.org/abs/2604.23897
- **R22.** Sycophancy: lechmazur sycophancy board [D-B]: https://github.com/lechmazur/sycophancy; Sustained pressure [V]: https://arxiv.org/abs/2609.09090; "It's Not Always Sycophancy" [V]: https://arxiv.org/abs/2605.27288; FlipFlop [B]: https://arxiv.org/abs/2311.08596; SycEval [B]: https://arxiv.org/abs/2502.08177
- **R23.** Long-chain execution: Illusion of Diminishing Returns [V]: https://arxiv.org/abs/2509.09677; TMBench [V]: https://github.com/HaitaoWuTJU/Turing-Machine-Bench; METR [D-E]
- **R24.** Memory and compaction: The Compaction Cliff [V]: https://arxiv.org/abs/2608.22752; Memory-benchmark overview (vendor-authored) [V]: https://mem0.ai/blog/ai-memory-benchmarks-in-2026
- **R25.** Teaching weaker models: Teach2Eval [V]: https://arxiv.org/abs/2505.12259; Saha et al. [V]: https://arxiv.org/abs/2306.09299; StudentBench [D-B]
- **R26.** Auditing planted behaviours: AuditBench [V]: https://arxiv.org/abs/2602.22755; Auditing for hidden objectives [V]: https://arxiv.org/abs/2503.10965
- **R27.** BoxingGym, DiscoveryWorld, AutumnBench [D-F].
- **R28.** Forecasting: ForecastBench [V]: https://arxiv.org/abs/2409.19839 and https://epoch.ai/benchmarks/forecastbench; QuantSightBench [V]: https://arxiv.org/abs/2604.15859; Context is Key [B]: https://arxiv.org/abs/2410.18959
- **R29.** Predicting research outcomes: Wen et al. [V]: https://arxiv.org/abs/2506.00794; Forecasting research success [V]: https://arxiv.org/abs/2605.21491; BrainBench [B]: https://www.nature.com/articles/s41562-024-02046-9
- **R30.** KoLMogorov-Test [V]. https://arxiv.org/abs/2503.13992
- **R31.** Markets and collusion: LLM collusion in double auctions [V]: https://arxiv.org/abs/2507.01413; Institutional AI [V]: https://arxiv.org/abs/2601.11369
- **R32.** Alpha Arena [V2]. https://www.iweaver.ai/blog/alpha-arena-ai-trading-season-1-results/
- **R33.** Vending-Bench 2 / Arena and FLE [D-B, D-D].
- **R34.** Detective benchmarks: WhodunitBench [V]: https://openreview.net/forum?id=qmvtDIfbmS; TurnaboutLLM [V]: https://chatpaper.com/paper/139362; MuSR [B]: https://arxiv.org/abs/2310.16049; Murder-mystery environment [V]: https://arxiv.org/abs/2602.12342
- **R35.** Social deduction: MafiaScope [V]: https://arxiv.org/abs/2607.10645; Clocktower Radio [V]: https://clocktower-radio.com/how-it-works
- **R36.** Debate: Khan et al. [V]: https://arxiv.org/abs/2402.06782; Kenton et al. [V]: https://arxiv.org/abs/2407.04622; May 2026 follow-up [V]: https://arxiv.org/abs/2605.27483
- **R37.** Nomic: NomicLaw [V]: https://arxiv.org/abs/2508.05344; Self-amendment game [V]: https://dl.acm.org/doi/10.1145/3712255.3734367
- **R38.** GENSTRAT [V; site blocked, search summary only]. https://arxiv.org/abs/2605.23238 and https://genstrat.org/
- **R39.** Puzzle generation: SATBench [V]: https://arxiv.org/abs/2505.14615; Absolute Zero [B]: https://arxiv.org/abs/2505.03335
- **R40.** Game generation: GAVEL [V]: https://arxiv.org/abs/2407.09388; Mage [V]: https://arxiv.org/abs/2605.07342; gg-bench [D-D]
- **R41.** Competitive programming and bot contests: AtCoder WTF 2026 Heuristic [V2]: https://the-decoder.com/openais-ai-beats-every-human-at-atcoder-a-top-competitive-programming-contest/ and https://atcoder.jp/contests/awtf2026heuristic; ALE-Bench [V]: https://github.com/SakanaAI/ALE-Bench; CodeClash [V/V2]: https://arxiv.org/abs/2511.00839 and https://codeclash.ai/insights/20251105_human_ai/
- **R42.** Sabotage and control: ControlArena [V]: https://github.com/UKGovernmentBEIS/control-arena; SHADE-Arena [V]: https://www.anthropic.com/research/shade-arena-sabotage-monitoring; AI Control [B]: https://arxiv.org/abs/2312.06942
- **R43.** Transmission chains: Telephone game [V]: https://arxiv.org/abs/2407.04503; GlossoGen [V]: https://arxiv.org/abs/2609.01491
- **R44.** Rules and games: LudoBench [V2]: https://en.papernotes.org/ICLR2026/vlm_reasoning/llms_as_rules_oracles_exploring_real-world_multimodal_reasoning_in_tabletop_stra/; GVGAI-LLM [V]: https://arxiv.org/abs/2508.08501; CWM [D-D]
- **R45.** Hidden-rule learning: ZendoWorld [D-F]: https://arxiv.org/abs/2607.08233; FalsifyBench [D-F]: https://arxiv.org/abs/2606.04751; WILT [D-F]: https://raw.githubusercontent.com/RiotGames/WILT/main/README.md; WitnessBench [D-F]: arXiv 2609.32208 (via dossier F search excerpts); Eleusis cogame [D-F]: https://raw.githubusercontent.com/Metta-AI/cogame-eleusis/main/README.md
- **R46.** Cooperation and conventions: AH2AC2 [V]: https://openreview.net/forum?id=Kioojohsuy; The Convention Gap [V]: https://arxiv.org/abs/2609.11489; Interchangeability [V]: https://arxiv.org/abs/2609.05279
- **R47.** Predicting and coordinating with humans: Strategic Algorithmic Monoculture [V]: https://arxiv.org/abs/2604.09502; Divergent Minds, Convergent Baselines [V]: https://arxiv.org/abs/2605.26437; Subversion via Focal Points [V]: https://arxiv.org/abs/2507.03010; Centaur [B]: https://www.nature.com/articles/s41586-025-09215-4
- **R48.** Manipulation evaluations: MakeMePay [V]: https://github.com/openai/evals/tree/main/evals/elsuite/make_me_pay; o1 system card [V]: https://openai.com/index/openai-o1-system-card/
- **R49.** GPTNT (Jun 2026) [V]. https://arxiv.org/abs/2606.28514

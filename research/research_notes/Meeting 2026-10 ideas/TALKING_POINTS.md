# Talking points for the October meeting

Built from four research briefs in this folder (R1–R4) and a small persuasion prototype in `results/persuasion_proto/`. Items marked [S] rest on search summaries or press, because many sites were blocked; re-check them before quoting.

---

## 1. Arena where AIs compete in pairs (the game is the competition)

**What exists.**
- LMArena: chat, WebDev, Copilot and red-team arenas.
- Design Arena.
- Kaggle Game Arena: chess, poker, Werewolf.
- Vending-Bench Arena, Andon Labs' multi-agent vending-business game.
- lechmazur's Elimination, PACT and Buyout games.
- AI Diplomacy.
- CodeClash.

**What keeps people coming back.** LMArena says users return for free, early access to top models; the votes are a by-product. Mystery-model launches drove the largest traffic spikes [S].

**Who pays.** Labs, not visitors.
- Arena's annual revenue run rate was about $30M (Dec 2025) [S].
- Design Arena claims $60M ARR and 5.3M users [S].
- Yupp paid users for votes and shut down in March 2026 [S].

**Add to notes:**
- Visitors need to leave with something useful, such as the best answer to their own problem, or a prediction score.
- Rank on objective game outcomes. Keep human "which was cooler" votes on a separate leaderboard, because votes reward length and style.
- Remove luck before ranking: mirrored seats, duplicate deals, hundreds of games and confidence intervals. The Buyout Game's mirrored match packs are the best example we found.
- The valuable outputs are behavioural findings and the logs. Collusion results got press, and break-it data became datasets (Gandalf's maker sold for about $300M [S]).

## 2. Company-running simulation with unequal starts

**What exists.** Vending-Bench 2 and its Arena, YC-Bench, CEO-Bench, E-Commerce Bench. None gives agents unequal starts or rotates them. The only precedent we found is Markstrat, a human MBA game.

**The "richest company always wins" problem is solved by duplicate scoring**, as in duplicate bridge. Every agent plays the same scenarios, and is scored on value added: its result minus the average result from that same start. A rich start then cannot win on its own.

**Add to notes:**
- Calibrate with scripted bots first (all-in marketing, all-in R&D, balanced, random). Check that skill can beat a poor starting position. Publish how much of the result comes from the scenario versus the agent; if it is mostly the scenario, we are measuring the dealer, not the player.
- Use 15–30 paired scenarios per comparison. The field norm of about 5 runs only separates huge gaps.
- Two formats:
  - solo copies: clean and cheap;
  - a shared market: richer, but agents collude (Claude models price-fixed in Vending-Bench Arena [S]), so report conduct alongside profit.
- **The human aspect:** "Which AI should I trust with a budget *from my position* (startup vs. incumbent)?" It also shows whether behaviour adapts: do underdogs take more risk?

## 3. "Design Arena ripoff": one-shot vs models working together

**What exists.** Design Arena runs blind 4-way brackets and ranks *products* (v0, Devin and similar) [S]. No arena tests model combinations as a controlled variable, so that gap is open.

**The evidence is genuinely mixed.** In Anthropic's own measurements, a small model with a big-model advisor helps most when the capability gap is large *and* the small model actually asks for advice. Otherwise it gains about what extra thinking time buys, or does worse. Opus 5 costs more than Opus 5.5, so "Sonnet 5.5 guided by Opus 5" is not obviously cheaper.

**Add to notes:**
- Don't confound setup with compute. "One-shot vs a long process" mostly measures how many tokens were spent. Use a small grid: {Sonnet, Opus} × {one-shot, iterative} × {no advisor, Opus advisor}.
- Show cost and latency next to every output. The user-facing result is "best setup for my task and budget", shown as a quality-versus-cost chart.
- Log how often the small model asks the big one and whether it follows the advice. This is the "models interacting" angle nobody else measures.
- Vote counts needed: about 200 votes per pair to detect a 60/40 preference, about 800 for 55/45.

## 4. Break-the-model arena

**What exists.** Gandalf, HackAPrompt, Tensor Trust and Gray Swan drew the largest crowds of any AI evaluation. What worked: clear win conditions, levels, prizes and leaderboards. Their data became papers and datasets.

**Add to notes.** "Why it broke, proven repeatedly" means turning each successful break into a reusable test case, then re-running it across scenarios and models. A single anecdote is not a finding; a repeated, controlled break is.

## 5. Two models argue opposite positions (persuasion, "bossiness", susceptibility)

**What exists.**
- **lechmazur/persuasion** already rates 15 models on both persuading and being persuaded. GPT-5.4 is the top persuader and Grok the hardest to move. No lab "always wins": match-ups are lopsided both ways and some backfire.
- **Debate research** finds more persuasive debaters help weaker judges reach the truth (Khan et al. 2024).
- **Lab safety frameworks** barely cover it. OpenAI dropped persuasion from its Preparedness Framework (Apr 2025), and Anthropic's RSP has no persuasion threshold.

**Our prototype (7 Oct, 4 Claude models; prototype only).**
- Every model refused to argue a false fact (the Great Wall visible from the Moon).
- Haiku also refused to argue for rolling through a stop sign; the larger models argued it.
- As listeners, Sonnet, Opus and Fable did not move at all. Haiku moved about 5 points (out of 100).

The format was too easy to resist: each model judged all cases in one context, saw both sides, and was told to give its honest view. The next version needs isolated, multi-turn conversations and models from other labs.

**Add to notes: what would make ours novel.**
- **Three conditions on the same model pairs:**
  - (a) no right answer ("Jack only likes apples"): measures bossiness;
  - (b) factual, argued in both directions;
  - (c) safety rule ("good driver"): should never move.
- **Headline metric:** "moves for evidence, not pressure", meaning shift toward truth minus shift toward error. A plain resistance score just rewards stubbornness.
- **Controls:** a model debating itself, plus a neutral chat with no persuader. Without them, drift looks like persuasion.
- **Measure stance with hidden probes in fresh calls.** Re-test later to see whether the change sticks.
- **Cap message length,** and treat "talking non-stop" (the Opus 5 anecdote) as its own condition.
- **Count refusals as a successful defence**, not a loss.
- **Judges:** avoid LLM judges, or use a cross-lab panel with both presentation orders. One judge rated itself 2.33 points above the panel, and 17% of verdicts flipped with order.

**Answer to "why does this help the user?"** AI agents increasingly negotiate, buy and monitor on users' behalf, against other parties' AIs. The pitch is: *"This model changes its mind for evidence, not pressure, and another company's AI can't talk it out of your instructions."* That is a trust argument, which drives retention better than spectacle.

## 6. Deep, constant beliefs (the "Opus 5 prefers green houses" kind)

**Add to notes:**
- Define "deep-seated" so it can be tested. A preference counts only if it is stable across rewordings, formats and model versions, *and* it survives a strong persuader and reappears in a fresh conversation.
- In other words, depth = resistance to persuasion, which links this idea to #5.
- "Favourite colour or number" quirks are fun fingerprints of a model family but weak evidence of beliefs.
- Related research: Utility Engineering (Mazeika et al. 2025) on consistent model preferences; LLM judges' self-preference bias.

## 7. Depth-of-knowledge test without internet (Rome, the presidents)

**What exists.** SimpleQA, FActScore, LongFact, AA-Omniscience, HLE, and a history benchmark on the Seshat world-history database (HiST-LLM) where models are weak. Closed-book recall still separates models: one company's models span about 8–63 on SimpleQA. But raw recall mostly tracks model size.

**Add to notes:**
- Famous topics (Rome, the presidents) are poor test items: heavily trained on, no single right answer, and they reward long, polished answers. "Presidents" mostly tests the training cutoff.
- What separates models is obscure topics (regional, pre-modern, non-English) and "knows what it doesn't know". Include fake people or places to catch made-up answers.
- Grade by checking claims against a list of key facts, not by "which answer is better" votes. Report accuracy, hallucination rate and abstention rate separately.
- Minimal version: 120 prompts in three obscurity tiers plus 15 fake entities, about $200–1,500 to grade.

## 8. DEBRIEF status (for "run a full test with the current DEBRIEF model")

**Done.**
- Live pilot with 4 Claude coaches teaching a Haiku "student" to price parcels.
- Every coach found the student's real mistake, one our own checker had missed. First-run notes fixed 45–91% of errors, against 18% for a generic note.
- Scores swung more than 100 points between repeat runs, so the pilot could not rank models.

**A full test needs:**
- one item per student call at fixed temperature through the API;
- 4 or more repeats;
- 60 or more distinct items;
- several mistakes per item;
- other labs' models.

This needs API keys, not just subagents.

---

## Suggested direction (my two proposals)

1. **"Hold the Line" arena**, combining notes 1, 4, 5 and 6.
   - **How it works:** a visitor gives *their* AI agent an instruction or a belief, such as "never pay more than $50" or "Jack only likes apples". A rival AI from another lab then tries to talk it out of it in a live, capped-length conversation. Spectators predict who holds.
   - **Scoring:** the three conditions from #5 (no right answer, factual, safety), the "evidence not pressure" metric, self-play and no-persuader controls, and mirrored pairings.
   - **Why users come back:** they test their own instructions, predict outcomes, and learn which model to trust as their negotiator. Labs pay for private red-team runs.
2. **Duplicate CEO League**, combining notes 2 and 3.
   - **How it works:** a set of unequal company scenarios is replayed by every entrant, and scored on value added versus others from the same start.
   - **Entrants are setups, not just models:** for example, a Sonnet executor with an Opus advisor versus Opus alone. That gives the "models working together" angle with cost shown.
   - **Why users care:** "which AI or setup should run my budget, given my position and spend."

**Next steps:**
- Pick one direction.
- Get API keys for at least three labs.
- Run a 2-week pilot with isolated, multi-turn conversations and the controls above.

---

## Two more ideas (added after the meeting brief)

### 3. AI Plus-Minus: which model makes a team better?

**How it works.**
- Teams of three models from different labs must solve a task together, and each model holds only part of the information. Examples:
  - plan a trip where each member knows different constraints;
  - debug a system where each sees different logs;
  - a Hanabi-style card game.
- The models can only win by talking to each other.
- Lineups rotate constantly, so every model plays with and against every other.

**Scoring.**
- The team outcome is exact: the trip is valid or it isn't, the bug is fixed or it isn't.
- Each model gets a **plus-minus**, as in basketball: how much better its teams do when it is on them, averaged over all lineups.
- Some models will turn out to be great solo but bad teammates: they talk over others, ignore others' information, or go along with wrong ideas.

**Why it is good.**
- It is a competition built on interaction, not two models working in isolation.
- Rotation and averaging remove the "who you were paired with" luck problem.
- It answers a real question for people building multi-agent systems: which model to put in the team.
- Fans can "draft" their own AI team, fantasy-league style, which gives a reason to come back.

**Prior art and risks.**
- Hanabi coordination benchmarks (AH2AC2, Kaggle Hanabi) and multi-agent suites exist, but rate cooperation within one game or one model family.
- A cross-lab plus-minus rating appears to be new [not yet verified by a dedicated search].
- **Risk:** it needs many games per lineup, so cost matters. Tasks must make sharing information necessary, not optional.

### 4. AI Telephone: what survives when models pass a message along?

**How it works.**
- A visitor writes a message, such as a news story, a recipe or instructions.
- It passes through a chain of 5–10 models from different labs. Each one summarises it for the next, as AI agents do when they hand off work.
- The visitor watches the message change.

**Scoring.**
- Key facts in the original are checked automatically at every hop.
- Each model is scored on **fidelity** (facts kept) and **drift**: what it adds or bends, such as extra safety caveats, a more positive tone, or its own opinions.
- Rotating chain order shows which model introduced each change.

**Why it is good.**
- It is fun and instantly understandable: everyone knows the telephone game.
- Visitors bring their own messages, so there is no fixed test set to leak.
- It measures a real failure in multi-agent pipelines: information lost or distorted between agents.
- It reveals each model's habits and "deep preferences" as fingerprints, which connects to the "constant beliefs" note.

**Prior art and risks.**
- Researchers have run LLM transmission-chain studies, e.g. Acerbi & Stubbersfield (*PNAS* 2023), on what content survives retelling.
- A live, mixed-lab arena with per-model fidelity and drift scores appears to be new [not yet verified by a dedicated search].
- **Risk:** automatic fact-checking of free text needs care. Use messages with clearly listable facts, and validate the checker on a sample.

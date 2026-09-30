# Round-2 red team R7: measurement and value skeptic

As of 30 Sep 2026. Reviewer R7, working independently. For the designs I read only `phase4/revised_finalist_specs.md`. Evidence comes from `phase2/design_principles.md` (the §7 rubric and principles P1–P20), the fact-checked `phase1/` dossiers (cited as A–G §x), and web searches run on 30 Sep 2026. I did not open the phase3 files, the other phase4 red-team or revision files, `phase4/pilot/` or `phase4/probes/`. If there are pilot results, they could change the Q3 scores below.

**Conventions.** Scores use the §7 rubric anchors (1–5), Q2–Q6 only. arxiv.org was blocked, so "(search summary)" findings come from search abstracts. [computation] is my arithmetic from the spec's sample sizes under stated assumptions; [estimate] and [speculation] are my judgement.

---

## 1. Summary table

| Finalist | Q2 | Q3 | Q4 | Q5 | Q6 | Construct concern | Prior art found (2025–26) | Most fatal remaining flaw | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| **F1 Compaction Chronicle** (A2) | 3 | 3 | 2 | 4 | 3 | The score depends on guessing the query distribution and on packing text under a byte cap. A no-tools, no-files protocol does not match how deployed agents keep memory | BEAM (ICLR 2026, 10M tokens, contradictions and updates); LongMemEval(-V2); StreamMemBench (Jun 2026); The Compaction Cliff (Aug 2026); CliffCompaction (Sep 2026) | Only 5 seeds, so a cluster bootstrap on a nonlinear half-life fit has very wide and under-covering CIs. The human arm is a rigged mini-task | **Drop** (keep the half-life metric as a sub-score elsewhere) |
| **F2 Hidden-Rule Lab** (A1 headline) | 2 | 3 | 4 | 4 | 3 | The image-only headline mixes perception of contact, support and lean with experiment choice. The adversary's "simplest rule" prior may favour humans because 25% of primitives are human-authored | ZendoWorld (Jul 2026); Witness/WitnessGym (Sep 2026); AutumnBench; FalsifyBench; BoxingGym; WILT; ARC-AGI-3 | The A1 gap may be absent at the Sep 2026 frontier, or perceptual only. Exploration-efficiency gaps closed in about 5 months on ARC-AGI-3 | **Shortlist with conditions** |
| **F3 Patch Auditor** (A2) | 3 | 3 | 3 | 4 | 4 | Benign diffs are refactors that preserve behaviour, so "did behaviour change at all?" separates the two classes. A differential-fuzzing script can solve that | ASMR-Bench (Apr 2026); PRWeaver (Aug 2026); "Coding with Enemy" (Jun 2026); SWR-Bench; CR-Bench; CodeReviewBench | A scripted fuzz-and-check baseline may score high, and no gate covers it: the 200-line-script gate does not apply to tools-on tracks. The MDE is about 11–13 pp | **Shortlist with conditions** (fix is mandatory) |
| **F4 Season Forge** (A2) | 4 | 3 | 3 | 3 | 4 | Largely general agentic software engineering plus game-AI craft. That fits the user's A2 "strong in general", but the score is dominated by harness and budget | CodeClash; ALE-Bench; AtCoder WTF Heuristic 2026 (AI beat 12 human finalists); Sakana AHC058 win; NetHackers; Kaggle Game Arena | Attempt-to-attempt variance with only 5 attempts, at $1.5–4k per model. Whether bots may call the engine is unspecified, and an engine-plus-ISMCTS template would flatten the spread | **Shortlist with conditions** |
| **F5 Self-Knowledge Exam** (A2) | 3 | 2 | 2 | 4 | 3 | 2026 evidence says LLM confidence reduces to a shared difficulty heuristic. The headline does not subtract that heuristic, so it rewards difficulty estimation, not *self*-knowledge. It also measures lab policy, not general strength | Barkan et al.; "No Individuated Metacognition" (May 2026); Mirror; Metacognitive Monitoring Battery; Kaggle "Measuring AGI" metacognition track | Underpowered: triage SE is about 0.1–0.13 on a 0–1 scale, the Self-Resolution MDE is about 0.04 nats, and the 3-pp void rule falsely voids about 20–27% of honest runs | **Drop** |
| **F6 Stump Arena** (A1) | 4 | 4 | 3 | 4 | 4 | Measures a union of blind spots, not one ability. Some gaps will come from input pipelines (frame sampling, audio resampling), not cognition | HLE (adversarial filtering with bounties); Dynabench; Phang et al. 2021 on the unfairness of adversarial filtering; SimpleBench; BabyVision | The headline human rate is the same re-gate rate used to select items, so it is biased upward. Tranches are unpaired across labs. Crowd AI use strips out exactly the items that stump AI | **Shortlist with conditions** (rank 1) |
| **F7 Unrun Lab** (A2; Track S ranks) | 4 | 3 | 3 | 5 | 3 | Track S is mostly data science and system identification with code, so it is heavily general-factor-loaded. Track M is mostly ML-lore recall; effects are often near zero, so the "no change" prior is hard to beat | Wen et al. (NeurIPS 2025); research-success forecasting (ACL Findings 2026); ForecastBench parity (Jul 2026); BoxingGym; Model Discovery Agent | Only 20 simulators per run, so 1,000 forecasts are about 50–90 effective observations. A generic simulator-fitting pipeline may compress the spread | **Shortlist with conditions** (rank 5) |

**Rubric check.** Taking the specs as written, no finalist has 4 or more on both Q3 and Q5 except F6. (Q1 was out of scope.) F6 has the highest mean at 3.8, then F7 at 3.6, F3 and F4 at 3.4, F2 at 3.2, F1 at 3.0 and F5 at 2.8. My "shortlist with conditions" verdicts assume the named fixes are made.

---

## 2. Cross-cutting protocol issues

1. **Anchors contradict each other.** Rule 6 says "at least one anchor rung is rotated per evaluation window" and also that ladders are "extended, never replaced." Rotating a rung out breaks a fixed scale unless the windows are linked by common anchors, as Epoch's ECI re-anchors its bootstrap draws (G §3). *Fix:* never retire rungs. Rotate only which subset is disclosed or used, and equate windows through at least 3 overlapping rungs.

2. **Crowd AI use has archetype-specific effects.**
   - 33–46% of MTurk summarisation workers used LLMs ([Veselovsky et al.](https://arxiv.org/abs/2306.07899)); about 34% of Prolific participants self-report LLM use (2025, search summary). G §5 lists this as an open gap.
   - For human *scores*, AI use is conservative: it inflates humans on A2 tasks and deflates them on A1 tasks.
   - For human *gates* (F6's verifiers, F2's rule-authoring round), it is not conservative. A verifier who asks a model will fail exactly the items that stump models, so those items get dropped.
   - "Ask them not to" plus timing checks is weak. In-person or proctored strata should carry the headline.

3. **The validity report has no decision threshold.** Rule 13 publishes the correlation with a general-capability index and the residual, but no pre-registered bar.
   - For the user's A2 ("genuinely strong vs weak *in general*"), high general-factor loading is *desirable*, but the benchmark must then be right where it disagrees with the general index. Only F3, F4 (human percentiles) and F7 Track M have a natural external criterion; F1 and F5 have none.

4. **Rule 7 (paired comparisons) is violated** by F5 (difficulty tuned per model) and F6 (each lab scored on "the newest tranche its lab has not been shown").

---

## 3. Per-finalist assessments

### F1. Compaction Chronicle: drop

**Saturation and separation (Q2/Q3).** The length knob and cap sweep give renewable headroom, but three problems remain.
- **Too few seeds for the headline.** The headline is a nonlinear derived parameter (the half-life from a logistic fit) estimated from 5 paired seeds, with a cluster bootstrap by seed. Cluster bootstraps with 5 clusters under-cover badly: small-cluster inference needs roughly t₄ critical values (±2.78 SE) or a wild bootstrap [computation].
- **Correlated errors.** One bad compaction wipes out a whole entity class, so ~1,500 queries are far fewer independent observations.
- **A logistic curve may be the wrong shape.** The 2026 "Compaction Cliff" paper shows step-like loss: safety-rule recall of 53% after one compaction round and 10% after five, for Sonnet 4.6 ([arXiv 2608.22752](https://arxiv.org/html/2608.22752v1), search summary). A half-life fitted to a cliff is fragile.
- **Result:** Q3 = 3 (clear spread, overlapping frontier neighbours).

**Construct.**
- Query-relevant state is at least 4× the cap, so the ceiling depends on guessing *which* facts will be asked. The oracle-notes bot is given the query distribution.
  - If the prompt discloses the query types, the task becomes bookkeeping plus dense text encoding under a byte cap: an ingenuity contest in compression.
  - If it does not, the held-out query families are close to a lottery.
- Banning files and retrieval makes the protocol unlike real deployed agents. [interpretation] Much of the lab interest in memory is about native compaction, which can't be byte-capped. So the provider-native track is not comparable with the headline.

**Humans (Q4 = 2).** 60 adults get a 30k-token, 40-chunk version in 2 hours.
- Reading 30k tokens (about 22k words) takes about 90 minutes at 250 words per minute, which leaves about 30 minutes for 40 rewrites [estimate].
- AI will win (A2), but the baseline says nothing about the headline task.

**Cost (Q5 = 4).**
- Per seed at 16 KB: about 400 calls × (10k input + 4k notes + ~10k thinking), roughly $130, so about $650 for 5 seeds.
- The 4 KB and 64 KB sweeps roughly triple that, to about $2k [estimate]. The spec's $300–1,000 covers the headline track only.

**Interest and novelty (Q6 = 3).** Memory half-life is a legible headline, and memory plumbing is a real bottleneck: ARC-AGI-3 moved 62.7% → 98.6% on harness state handling (A §2.3). But the space is crowded:
- BEAM: 100 conversations up to 10M tokens, 2,000 questions, testing updates and contradictions ([repo](https://github.com/mohammadtavakoli78/BEAM));
- LongMemEval-V2;
- StreamMemBench ([2606.14571](https://arxiv.org/pdf/2606.14571));
- mem0's 2026 benchmark guide lists several more.

**Verdict: drop.** The half-life idea is worth keeping as a sub-score inside a long-horizon candidate (F4 build logs, F3 multi-diff sessions).

### F2. Hidden-Rule Lab: shortlist with conditions (A1 candidate 2)

**Saturation (Q2 = 2 for the A1 headline).** The evidence runs against a durable gap.
- Exploration and experiment efficiency is the design principles' top-ranked A1 target, but its record is poor once targeted. ARC-AGI-3 went from under 1% to 99.9%, with Astra using fewer actions than the median human on 96% of levels, in about 5 months (A §2.3).
- Every human-over-AI result in this family predates the Sep 2026 frontier:
  - ZendoWorld (Jul 2026, 19 humans): 73.3% vs 44.5% for VLM agents;
  - AutumnBench: models tested were o3, Gemini 2.5 Pro and Claude 4 Sonnet;
  - Witness: 24% of private level slots (F §2).
- ZendoWorld also reports that "labeling accuracy is often dissociated from true rule recovery" ([2607.08233](https://arxiv.org/abs/2607.08233), search summary). That supports F2's shortcut-separating probes.
- Public practice environments plus WitnessGym-style RL make the generic skill trainable. Rotating 30% of primitives slows this but does not stop it [speculation].

**Separation (Q3 = 3).** Power is adequate *if* a gap exists [computation]:
- Assume about 100 games per model and a spread of about 10 experiments. Then SE(median) is about 1.25 experiments, and the ratio SE is about 0.07 near a human median of about 20.
- So the 1.25× gate is resolvable.
- The real uncertainty is whether a gap exists at all. Success means at most 3 probe errors out of 30, a knife-edge threshold that adds variance between games.

**Construct.**
- The image-only headline is where P8 (perception) and P9 (experiment efficiency) collide. If the JSON-track ratio is at or below 1× while the image track is above 1.25×, the A1 gap is perceptual. Perceptual gaps close fast once targeted: VPCT is at 91%, and ClockBench went from 13% to 67% in about 12 months (A §2.9–2.10).
- The bounded adversary uses a "published, frozen prior over the season grammar," but the primitives are private during the season. Subjects therefore can't know what counts as "simplest."
  - Humans succeed to the extent their intuitive simplicity bias matches the designer's grammar, and 25% of primitives are human-authored.
  - That is a real construct (human-like concepts), but not "efficient experimentation." Report a model–human gap separately for primitives that were human-authored and those that were machine-generated.

**Humans (Q4 = 4).** 300 first-run adults is close to ARC-AGI-3 practice (458). But 10–15-minute games are inconsistent with the "median human succeeds within 30 experiments" gate: building 12-object scenes through a form at 30–60 s each makes 30 experiments take 15–30 minutes, plus about 5 minutes of probe labelling [estimate]. Humans are time-pressured while models are not, and the per-experiment pay penalty has no model counterpart.

**Cost (Q5 = 4).** Grading is deterministic; the SMT enumeration and adversary are heavy one-off engineering. About 40 turns with accumulating images is roughly 1.2M input and 0.3M output tokens per game, about $1,100 per 100 games against the spec's $200–800 [estimate].

**Interest (Q6 = 3).** "AI needs 1.6× more experiments than people" is legible, and the adversarial final phase is novel. But the niche is dominated by the ARC brand, and 2026 already has ZendoWorld, Witness, FalsifyBench and AutumnBench.

**Verdict: shortlist with conditions.**
1. Make the image-minus-JSON difference a co-headline.
2. Report JSON-track ratios before launch, so that a gap which is perceptual only gets labelled as such.
3. Use 30–45-minute human sessions, or cut the experiment budget.
4. Split results by human-authored and generated primitives.

### F3. Patch Auditor: shortlist with conditions (fix is mandatory)

**The fatal flaw is the construct: benign diffs come from refactoring generators.**
- Refactors preserve behaviour by definition, and every benign diff is *certified by differential fuzzing against the base version*. Sabotage diffs change behaviour.
- So "does any input change behaviour?" separates the classes, and the headline is tools-on with a fuzzer.
- A roughly 50-line pipeline would solve much of the task: differential-fuzz the diff, then test the differing inputs against the property to produce a witness.
- The release gates don't catch this:
  - the ≤200-line-script gate is waived because tools are declared part of the construct;
  - the AUROC ≤ 0.55 check runs a classifier on diff *text*, which can't execute code.
- Saboteurs will then drift toward fuzz-resistant triggers such as magic constants. That turns the task into spotting the classic backdoor pattern, a narrow and trainable construct [speculation].
- **Required fix:**
  - benign diffs must include property-preserving *behaviour changes* (bug fixes, features, performance or API changes) at realistic rates;
  - a scripted differential-fuzz anchor must be published as the floor.

**Separation (Q3 = 3).** Each run has 150 sabotaged and 350 benign diffs [computation]:
- Recall SE is about 4.1 pp.
- A 5% FPR threshold set from about 17 flagged benign diffs has an FPR SE of about 1.2 pp.
- Paired across models with a correlation of about 0.4–0.5, the MDE is about 11–13 pp.
- Existing evidence suggests a wide spread between weak and strong models, but frontier neighbours will overlap. Use about 1,000 diffs per run, or report AUROC and log score, which are more stable, as co-headlines.

**Humans (Q4 = 3).** 60 professionals × 6 diffs gives about 108 sabotaged and 250 benign audits. A 5% FPR threshold can't be set per person, and pooling different calibrations understates human ROC. Professionals routinely use AI assistants and remote enforcement is weak. AI already beats humans here, but not by much:
  - ASMR-Bench: Gemini 3.1 Pro AUROC 0.77 vs LLM-*assisted* humans 0.68 ([repo](https://github.com/ejcgan/auditing-sabotage-bench); [2604.16286](https://arxiv.org/abs/2604.16286), search summary);
  - "Coding with Enemy": 94% of developers missed sabotage (83 of 88 sessions) ([2606.05647](https://arxiv.org/abs/2606.05647), search summary).
- So A2 is plausible, but "clearly" needs the human arm to be proctored.

**Cost (Q5 = 4).** Witnesses are executed outside the sandbox, which is objective; benign labels can't prove absence of a violation, so keep the 5% expert audit. About $550 per model with caching, up to about $2.7k at list price for ~30-tool-call sessions [estimate].

**Interest (Q6 = 4).** This has the strongest link to buying decisions (P19): code-review tools and AI-control monitoring. "Catches X% of sabotaged patches, with proof, at 1-in-20 false alarms" is legible. But prior art is dense:
- PRWeaver: 208 execution-validated attacks; detection falls to 16–22% under whole-window review vs 50–60% per-PR ([2608.02693](https://arxiv.org/abs/2608.02693), search summary);
- SWR-Bench, CR-Bench and CodeReviewBench ([site](https://www.codereviewbench.com/)).

The witness requirement and FPR anchoring are F3's real novelty.

**Verdict: shortlist with conditions.** Conditions: the benign-distribution fix, the scripted fuzz anchor, 1,000 or more diffs, and a proctored human arm.

### F4. Season Forge: shortlist with conditions

**Saturation (Q2 = 4).** A new private game each season, a ladder that can be extended, and an uncapped Bradley–Terry rating are the best renewal design in the set. Two caveats:
1. Whether bots may call the engine binary at play time is unspecified. If they can, every season reduces to "wrap engine in ISMCTS and tune heuristics," a template that carries across seasons and compresses the spread. This is CWM's lesson that "write a simulator, plug into search" dominates (D §2.25).
2. A2 against humans is already established. At the AtCoder World Tour Finals Heuristic 2026, OpenAI's model finished far ahead of all 12 human finalists ([contest](https://atcoder.jp/contests/awtf2026heuristic); press summaries), and Sakana's agent won AHC058 outright ([Sakana](https://sakana.ai/ahc058/)). That is good for A2 validity and bad for novelty.

**Separation (Q3 = 3).** Each bot's rating from 2,000 or more games is tight, at roughly 0.2 doubling units [estimate]. The dominant variance is between attempts: some agentic builds end with buggy bots.
- If the attempt SD is 1–2 doubling units, 5 attempts give an SE of about 0.45–0.9 units [speculation].
- So frontier neighbours within about 1–2 units won't separate, even though weak and strong models will separate clearly.
- CodeClash found clear model ordering and that no model won a round against an expert human bot, as of Nov 2025 ([2511.00839](https://arxiv.org/abs/2511.00839), search summary). Its 2026 status is unknown.
- 2–4-player games with kingmaking need Plackett–Luce and seat effects, not plain Bradley–Terry. G §3 notes that no power analysis exists for multi-seat games.

**Construct.** The benchmark measures agentic software engineering plus game-AI craft plus management of the build budget. That is highly loaded on the general factor, which is acceptable for the user's A2 definition. But the BYOH delta will be large: 48-hour agentic runs are exactly where harnesses dominate (A §2.3; P18).

**Humans (Q4 = 3).** In-person, locked machines avoid AI contamination, but 50–100 veterans are an elite population, humans get 6 hours against the models' 48 hours and 8M output tokens, and the arm costs $20–50k a year.

**Cost (Q5 = 3).** Outcomes are deterministic, but $1.5–4k per model per season is the highest here, agentic builds are hard to reproduce, and the engine and operator bot are real engineering. Tournament CPU is modest: about 900 core-hours per attempt [estimate].

**Interest (Q6 = 4).**
- For the public it is the most spectator-friendly: replays, human-vs-AI exhibitions and prizes (Halite and Battlecode precedent).
- For labs it is weaker. Game arenas rarely enter lab reports; Google's Gemini 3 report omits its own Game Arena (P19).
- "Ladder-doubling units" is not legible; "beats N% of human veterans" is.

**Verdict: shortlist with conditions.**
1. Specify the engine-access policy, preferably no engine at play time, so dynamics must be inferred.
2. Use 8–10 attempts, or headline the Lite track, which is cheaper and allows more attempts.
3. Use a Plackett–Luce rating with seat effects.
4. Put the human percentile in the headline.

### F5. Self-Knowledge Exam: drop

**Construct (fatal).** "LLMs Show No Signs of Individuated Metacognition" tested 20 frontier LLMs on 6 benchmarks ([2605.24299](https://arxiv.org/abs/2605.24299), search summary):
- confidence "largely reduces to a shared difficulty heuristic";
- models "agree on which items are hard but fail to predict their own relative advantage";
- a surface-feature classifier matches or beats self-assessment on 3 of 6 benchmarks.

F5's Self-Resolution subtracts only the model's *per-family base rate*, not an item-difficulty predictor. A model that reads difficulty knobs (computation length, number of tool calls) scores well without any self-knowledge.
- *Required:* subtract a cross-model or knob-based difficulty predictor, so that only *individuated* resolution is scored.
- It also misfits the user's A2 goal. Calibration and abstention mainly reorder labs by policy (AA-Omniscience; E Q2), not by general strength. Calibration is directly trainable, per the 2026 fine-tuning results ([2602.02605](https://arxiv.org/pdf/2602.02605); [2609.33886](https://arxiv.org/abs/2609.33886), search summaries).

**Power (Q3 = 2)** [computation, assuming p ≈ 0.5]:
- **Void rule.** The run is voided if forecast items (1,350) and blind twins (450) differ by more than 3 pp. The SE of that difference is about 2.4–2.7 pp, so about 20–27% of *honest* runs are voided.
- **Base-rate noise.** With 40 twins per family, each base-rate SE is about 7.9 pp. That adds about +0.0125 nats of bias and about 0.007 nats of noise per item.
- **Self-Resolution MDE.** Item sampling adds an SE of about 0.008. Models are unpaired, because difficulty is tuned per model. The between-model MDE is therefore about 0.04 nats, while plausible signals are about 0.02–0.10 nats (AUROC 0.65 ≈ 0.046 nats).
- **Triage.** Over 3 blocks of 60, the numerator SD is about 3.9 against a denominator of about 30, so SE ≈ 0.13 and only differences of about 0.35 or more resolve. Outcomes are stochastic, so even an oracle can't reach 1.

**Humans (Q4 = 2).** Humans get different items, only the non-agentic families, and no per-person difficulty tuning. Whether AI beats humans on *resolution* is untested, and human feeling-of-knowing is not poor.

**Interest (Q6 = 3).** Abstention matters to labs, but the field is crowded: Barkan et al. (all LLMs overconfident; [OpenReview](https://openreview.net/forum?id=IPGR4uXxvg)), Mirror ([2604.19809](https://arxiv.org/html/2604.19809v1)), the Metacognitive Monitoring Battery ([2604.15702](https://arxiv.org/html/2604.15702v1)), and the $200k DeepMind/Kaggle "Measuring AGI" metacognition track, Mar–Apr 2026 ([Google](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/measuring-agi-cognitive-framework/)). "Nats per item" is not legible.

**Verdict: drop.** Keep forecast q and p as a reported sub-score in F3 (P(sabotaged)) and F7 (quantiles), where calibration comes naturally.

### F6. Stump Arena: shortlist with conditions (rank 1)

**Saturation (Q2 = 4).** Authoring renews the pool by construction, and "cost to stump" can't saturate: it is a thermometer. The gap headline can shrink. The 8 fixed clusters are trainable with synthetic data (ClockBench went from 13% to 67% in about 12 months; A §2.9). Publish the decay against the control pool, as the spec says.

**Separation (Q3 = 4).** Several perceptual gaps still hold into 2026: MindTopo 97.87 vs 61.42 on GPT-5.6 Sol (secondary source), and BabyVision 94.1 vs 49.7 (design principles §5a). A gap many times the CI is likely, at least on the hard pool. Three biases to fix:
1. **Winner's curse.** Items enter the pool only if the re-gate solve rate is ≥ 80% with n ≥ 10, and that *same* rate is the human side of the headline. The reported human rate is therefore biased upward, by about 3–6 pp for a realistic spread of true rates [computation, assuming true item rates spread over 60–95%]. *Fix:* use a third, independent human sample (for example, fresh adults or the in-lab stratum) for the headline only.
2. **Unpaired tranches.** Labs are scored on different tranches, so tranche difficulty is confounded with rank. *Fix:* score all models in a window on the same tranche.
3. **Fairness of adversarial filtering.** Phang et al. found rankings "unstable and highly sensitive to the choice of adversary model," with the adversary's own family disadvantaged ([2111.08181](https://arxiv.org/abs/2111.08181), search summary).
   - The hard pool is filtered by an open panel.
   - Bounty authors will pre-test on public chat apps, so the pool is also implicitly filtered against the most popular closed models.
   - Report results by author source, and restrict bounty payouts to items that fail a disclosed panel.

**Construct.** The benchmark is a union of blind spots, not one ability. The spec sets a spatial minimum feature size but none for time or audio. Sub-second video events and short audio cues will partly measure API frame-sampling and resampling defaults rather than perception. That is BlindTest's encoder-vs-decoder problem (A §2.8). *Fix:* freeze the frame rate and resolution in the harness, and set a minimum event duration of about 1 second or more.

**Humans (Q4 = 3).**
- Human gating is built in, with about 15 humans per item.
- The rule "drop items whose online rate exceeds in-lab by more than 15 pp" can't be applied per item with an in-lab n of about 30. Apply it per cluster or per author instead.
- Crowd AI use (point 2 of §2) removes exactly the stumps, so yield is biased downward, and the trend is confounded by changing crowd AI use. Proctor the 4-of-5 verifier stage.

**Cost (Q5 = 4).** Scoring is exact match at $50–300 per model, which is the cheapest here. But the social and intent cluster will produce answer disputes (compare HLE's 18–29% disputed chemistry and biology answers; C §3.1). Restrict that cluster to closed-form answers. The $25–40k programme cost is plausible: about 22,500 human judgements is about 375–1,100 hours of crowd work [estimate].

**Interest (Q6 = 4).** It has the most legible story in the set: "people solve 95%, the best AI solves Y%, and it now costs $Z of human effort to find each stump." Bounties give a participation path. Prior art: HLE (frontier-filtered crowdsourcing with bounties) and Dynabench ([2104.14337](https://arxiv.org/abs/2104.14337)); the easy-for-humans multimedia focus and stump-yield trend are new.

**Verdict: shortlist with conditions.** Conditions: an independent human-headline sample, simultaneous tranches, minimum temporal and audio feature sizes, a proctored verifier stage, and results by author source.

### F7. Unrun Lab: shortlist with conditions (rank 5)

**Saturation (Q2 = 4).** Track S has private mechanism grammars and a truth ceiling of 100. Track M is the most contamination-proof design in the set, because the truth doesn't exist until after predictions lock. Risk: a generic "fit a flexible stochastic simulator, then simulate interventions" pipeline that frontier coding agents can write may push everyone toward the same ceiling. The owner's generic-learner anchor should be as strong as the owner can make it [speculation].

**Separation (Q3 = 3).** The 1,000 forecasts are 20 simulators × 50 correlated questions [computation]:
- With an intra-simulator correlation of 0.2–0.4, the design effect is about 11–21, leaving about 50–90 effective observations.
- *Fix:* use 60 or more simulators with about 15 questions each, at roughly the same token cost.
- Track M's 150 experiments have many near-zero effects, which compresses skill against the "no change" prior. Twenty seeds per arm leaves truth noise, which reduces discriminability further.

**Construct.**
- Track S is data science plus system identification with code. It is highly loaded on the general factor, which suits the user's A2. It is not "forecasting unrun experiments" in the scientific sense until the interventional, out-of-support questions dominate the score. Report them as their own sub-score.
- Track M's no-code headline mostly tests recall of ML folklore. For example, Lion is commonly run at a learning rate 3–10× lower than AdamW's.

**Humans (Q4 = 3).** The expert panels are reasonable, but remote experts will use AI unless proctored. AI > humans is plausible: Wen et al.'s system scored 64.4% vs 48.9% for human experts on pairwise NLP idea outcomes ([2506.00794](https://arxiv.org/abs/2506.00794), search summary), and ForecastBench reports "likely parity" with superforecasters by Jul 2026 ([FRI](https://forecastingresearch.substack.com/p/ai-models-have-likely-reached-parity)).

**Cost (Q5 = 5).** CRPS against 10k rollouts is deterministic, at $100–500 per model. Track M adds $5–20k of owner compute per season.

**Interest (Q6 = 3).** Forecasting AI research outcomes is relevant to AI-R&D capability tracking, so labs' preparedness teams have a reason to care. A skill score from 0 to 100 is legible. Related 2026 work: [ACL Findings 2026](https://aclanthology.org/2026.findings-acl.1918/), BoxingGym ([2501.01540](https://arxiv.org/abs/2501.01540)), and Model Discovery Agent with CRPS scoring ([2608.09696](https://arxiv.org/abs/2608.09696)).

**Verdict: shortlist with conditions.** Conditions: 60 or more simulators, an interventional sub-score, and Track M reported as a research signal rather than a ranking.

---

## 4. Ranked recommendation

1. **F6 Stump Arena (A1).**
   - *Why first:* it is the only A1 design whose gap is renewed by construction rather than by hoping a fixed task family stays hard. ARC-AGI-3 showed fixed families fall in months. It is the cheapest to score and the most legible.
   - *Biggest remaining risk:* the headline is partly manufactured. The human rate is selected on, the pool is adversarially filtered in model-specific ways, and some stumps are artefacts of the input pipeline. Without an independent human sample and paired tranches, the gap figure is not trustworthy.
2. **F3 Patch Auditor (A2), only with the benign-diff fix.**
   - *Why:* it has the strongest adoption path (code review and AI-control monitoring), grading by an executed witness, moderate cost, and evidence that AI already beats humans by a margin.
   - *Biggest risk:* as specified, a differential-fuzz script separates the classes, and no gate catches it. The frontier MDE of about 12 pp is also coarse.
3. **F4 Season Forge (A2).**
   - *Why:* it is the best fit for the user's "genuinely strong in general" and the most durable renewal design. The human-vs-AI story is spectacular.
   - *Biggest risk:* between-attempt variance, and the ambiguity over engine access, at the highest cost in the set. Frontier neighbours won't separate with 5 attempts.
4. **F2 Hidden-Rule Lab (A1, with an A2 fallback).**
   - *Why:* it is the best-specified experiment-efficiency game and the only other A1 route. The adversarial end-game is a real novelty.
   - *Biggest risk:* at the Sep 2026 frontier the A1 gap may be absent, or perceptual only. Its own launch gate may turn it into an A2 benchmark in a crowded niche.
5. **F7 Unrun Lab, Track S (A2).**
   - *Why:* it is the most objective and cheapest per model, and Track M is uniquely contamination-proof.
   - *Biggest risk:* too few simulator clusters for a stable ranking, and a generic pipeline could flatten the spread.

**Drop:**
- **F5.** The construct is contradicted by 2026 metacognition evidence, and it is underpowered on both headlines.
- **F1.** The prior art is crowded, the headline is underpowered, the human arm is uninformative, and the construct is shaped by the protocol.

If only 3 are wanted, take F6, F3 and F4: one A1 and two A2 with different adoption paths. F2 is the alternate if the user wants a second A1 option and accepts a launch gate that may end as A2.

---

Web sources are linked inline; most are search summaries because arxiv.org was blocked. ALE-Bench: https://github.com/SakanaAI/ALE-Bench.

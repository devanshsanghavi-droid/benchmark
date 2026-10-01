# Blinded pilot results (Phase 4, 1 Oct 2026)

Small, blinded pilots of five finalists. Each pilot's answer key was encrypted with a passphrase that was never written to the repo. Four Claude model tiers attempted each pilot as agents: Haiku, Sonnet, Opus and Fable. Keys were decrypted only after solving and are published in each `F*/revealed/` folder.

**Caveats that apply to every pilot:**
- All solvers come from one lab.
- They ran in the Claude Code agent harness, not a frozen benchmark harness.
- Samples are tiny, and there were no human participants.
- Tool policies were honour-system.
- Solvers could in principle have read files outside `public/`: other solvers' answers, agent transcripts on disk, and, for F4, one tool-results file that held the passphrase.
- Usage-limit interruptions cut several runs short; they are marked below.

## F2 Hidden-Rule Lab (static, image-only, no code)

The pilot has 8 problems with 64 test labels in total. Score is test-label accuracy.

| Solver | Accuracy | Problems fully correct |
|---|---|---|
| Opus | 64/64 (100%) | 8/8 |
| Sonnet | 64/64 (100%) | 8/8 |
| Haiku | 31/64 (48.4%), at chance | 0/8 |
| Fable | not completed (usage-limit interruption) | — |

- **Baselines:** random scored 48–52%, always-fits 45.3%, and the best shallow script 59.4%.
- Opus and Sonnet also wrote out the hidden rules, and all 8 statements matched the key.
- **Implication:** recognising a rule in clean rendered scenes is not a human-over-AI moat for mid-tier and top models. The static form saturates now. Only the weakest tier is separated.

Files: `F2/RESULTS` are inline in this summary; scorer output is in `F2/revealed/scores.json`.

## F3 Patch Auditor (tools on)

The pilot has 20 patches, 6 of which are violations. The headline score is precision × recall (PWR). See `F3/RESULTS.md`.

| Solver | Hits / false alarms / misses | PWR |
|---|---|---|
| Fable | 6/0/0 | 1.000 |
| Opus | 6/0/0 | 1.000 |
| Sonnet | 6/0/0 | 1.000 |
| Haiku | 4/2/2 | 0.444 |

- A naive differential fuzzer scored 0.600. The scorer's quick normalised fuzzer scored 1.000.
- **Implication:** the design saturates with tools on, and a script solves it. This confirms the round-2 critique that harmless patches are refactors.

## F5 Self-Knowledge Exam (no tools)

The pilot has 60 items. See `F5/RESULTS.md`.

| Solver | Accuracy | Brier | Mean forecast vs accuracy |
|---|---|---|---|
| Haiku | 0.23 | 0.303 | 0.58 vs 0.20 |
| Sonnet | 1.00 | 0.007 | 0.76 vs 1.00 |
| Opus | 1.00 | 0.004 | 0.75 vs 1.00 |
| Fable | 1.00 | 0.018 | 0.75 vs 1.00 |

- Three solvers scored 100%, so self-knowledge could not be separated from accuracy.
- At the ceiling the metrics only reward confidence near 1. This produced a meaningless inversion that ranks Fable last.
- Haiku's AUROC (0.71) drops to 0.55 within a difficulty level, so its confidence tracks how hard an item looks, not self-knowledge.
- Deliberately failing 3 items lifts AUROC and triage to 1.00.
- **Implication:** the design is broken as specified.

## F4 Season Forge (novel 2-player fog-of-war game "Brackwater"; write a bot; tools on)

- **Sealed ladder:** L0 random < L1 < L2 < L3. Each higher rung beat the one below 76–100% of the time over 400 games per pair.
- **Scoring:** 100 games per rung, seat-balanced. Run in 163 s on 4 cores.

| Solver | vs L0 | vs L1 | vs L2 | vs L3 | Rung position (95% CI) | Status |
|---|---|---|---|---|---|---|
| Opus | 1.00 | 0.98 | 0.98 | 0.87 | 5.08 (extrapolated; above the ladder) [4.62, 5.61] | snapshot, interrupted |
| Sonnet | 1.00 | 0.31 | 0.03 | 0.00 | 0.81 [0.74, 0.87] | snapshot, interrupted |
| Fable | 1.00 | 0.29 | 0.01 | 0.00 | 0.79 [0.71, 0.85] | snapshot, interrupted (early version) |
| Haiku | 0.95 | 0.00 | 0.00 | 0.00 | 0.41 [0.36, 0.47] | completed |

- **Implication:** this pilot gave the widest model-to-model spread.
  - Opus's bot beat the strongest sealed reference bot 87% of the time. The ladder needs stronger top anchors, such as search bots or human-programmer bots.
  - Snapshots were taken at different stages of development, so the ordering among Sonnet, Fable and Opus is not a fair comparison.
- Files: `F4/revealed/scores_snapshot.json`.

## F7 Unrun Lab (forecast intervention outcomes in 5 secret simulators; tools on)

- Only Haiku completed. Its skill was 9.6, 90% CI [−23.1, 34.4], on a scale where 0 = no-change baseline and 100 = oracle.
- That is below the naive extrapolator baseline of 16.0. Sonnet, Opus and Fable were interrupted and did not finish.
- **Implication:** inconclusive. The pilot only shows that a weak tier does not clear naive baselines.

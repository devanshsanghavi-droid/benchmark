# Gap dossier: is an LLM student a valid instrument, and what human criterion could validate a teach-back gain?

Date: 2026-09-29. Scope: the validity of LLM-simulated students and users as measuring instruments, and a human-learning external criterion for teaching-gain metrics. This dossier feeds the teach-back niche (notes/prior_art_novel_methods.md, niches #1 and #8; briefs/D_theory_prior_art.md, Implications 4 and 11).

**Conventions.**
- Confidence per claim: **H** = read in a primary source (official repo, README, paper PDF or table); **M** = search-engine extract of the primary source, or two consistent secondary sources; **L** = one secondary source or my own inference.
- Source tags: [P] primary; [S] secondary or search extract; [C] my own computation from published numbers, with inputs stated.
- Access limits: WebFetch to arxiv.org, nature.com, pnas.org, pmc and most publisher pages was blocked. Primary text was read only from GitHub (READMEs, configs, one paper PDF) and through search-engine extracts. Every number marked M should be re-checked against the full text before it appears in a paper.

## Summary

- **Correction to a survey warning sign (H).** EducationQ's student ablation (Table 2 of the official ACL PDF) is a 3×3 teacher × student matrix. It does **not** show the Llama teacher's gain falling from +12.63 to +8.08 to +4.55 when the student changes.
  - With the **Llama student**, the **Llama, Qwen and Mistral teachers** gain +12.63, +8.08 and +4.55.
  - The **Llama teacher's** gain across the Llama, Qwen and Mistral students is +12.63, +8.59 and +7.07.
  - My two-way decomposition: teacher main effect 64% of variance, student main effect 35%, interaction under 1%. Same-model cells show no advantage beyond the main effects (residuals +0.39, −0.11, +0.05 pp) [C].
  - The real warning is different: the student is a large main effect (the same teacher's gain varies 1.8×), and one run on 198 items gives a gain SE of about 3 pp [C].
  - The survey's version came from a secondary paper note. briefs/D (item 6) and prior_art_novel_methods.md should be corrected.
- **Prompted LLM students are poor instruments for "not knowing".**
  - They match real students on coarse, item-level statistics: r = 0.72 for Generative Students; up to 0.75–0.82 for simulated-classroom item difficulty.
  - They fail at the level that teach-back needs: stable ignorance, stable misconceptions, and realistic uptake of instruction. Documented failures:
    - the "competence paradox";
    - near-zero selective flipping, i.e. sycophantic abandonment of any misconception on any corrective cue, across 7 LLMs;
    - over-coherent think-alouds that overestimate performance;
    - prompted simulators near chance at predicting real uptake (M).
  - Trained simulators (SFT/DPO, StudentSim, ParaStudent) do better but remain limited (M).
- **Student choice matters to absolute scores more than to rankings.** Rankings were stable in the few studies that vary the student (EducationQ, 3 teachers; Teach2Eval, leave-one-of-4-students-out; DAS2, 5 tutors across 5 student states). Every one of these tests has few teachers. Two of the two published learning-gain benchmarks with a single student family crowned a same-family teacher (EducationQ: Llama/Llama; TeachBench: Qwen3/Qwen2.5) (H/M).
  - The same holds for simulated users: agent success moves up to 9 pp across user LLMs [seshadri2026lostinsim] (M).
  - τ²-bench's own user simulator errs in 40–47% of conversations in free-text domains, against 16% when tool-constrained (M).
- **Telling beats teaching on immediate tests. This is now well evidenced in humans.**
  - Bastani et al.: unguarded GPT-4 raised practice scores by 48% but lowered unassisted exam scores by 17% (M).
  - Eedi/LearnLM RCT: immediate remediation saturated for human and AI tutors alike (91–95%). Only a later-unit transfer item separated LearnLM from humans (+5.5 pp) (M).
  - Existing benchmarks forbid leakage by hiding options or items from the teacher (EducationQ, Teach2Eval, TeachBench) or by judging and penalising disclosure (MathDial, PedagogicalRL, tutordiag2026).
- **A human criterion that compares many models now exists.** StudentBench (Handshake, arXiv 2609.28470, Sept 2026) randomised 2,383 learners across 13 AI tutor configurations per GRE section, human tutors and a no-tutor control, with 27-item pre- and post-tests (H, official repo).
  - Pooled AI vs control: +6.15 pp [4.08, 8.21].
  - None of 364 domain × tutor cells was significant, and seven different tutors won the seven domains.
  - At roughly 80–170 learners per configuration, human learning gains barely separate frontier tutors.
  - A human validation of a teach-back metric is feasible only with engineered teacher arms of widely different quality and about 120–350 learners per arm [C].
- **Bottom line for the protocol** (details under Implications):
  - ≥3 pinned student families with a leave-family-out headline;
  - genuinely novel material instead of role-played ignorance;
  - closed-book, isolated post-tests on transfer items the teacher never sees;
  - mandatory "teller", "raw material" and "no teaching" reference arms;
  - gain SE ≤1.5 pp per cell;
  - a pre-registered human falsification study of about 8–10 arms × about 150 learners.

## Findings

### 0. Correction: what EducationQ's student ablation actually shows

Source: the official PDF in the EducationQ repository (docs/2025.acl-long.1576.pdf), §4.1 and Table 2 "Student Agent Ablation Study Based on GPQA Diamond" [educationq2025] [P, H]. The text was extracted with PyMuPDF.

**Orientation of the table.** Rows are students and columns are teachers.
- The pre-test score is constant within each row: 46.97, 45.45 and 35.35.
- These equal the students' own GPQA-Diamond scores stated in §4.1: Llama 3.1 70B 46.97%, Qwen 2.5 72B 45.45%, Mistral Nemo 35.35%.

Absolute learning gain Δ (pp) on GPQA Diamond (198 items):

| Student \ Teacher | Llama 3.1 70B | Qwen 2.5 72B | Mistral Nemo |
|---|---|---|---|
| Llama 3.1 70B (pre 46.97) | **12.63** | 8.08 | 4.55 |
| Qwen 2.5 72B (pre 45.45) | 8.59 | **4.55** | 2.53 |
| Mistral Nemo (pre 35.35) | 7.07 | 2.53 | **0.00** |

- The paper states the ablation "showed negligible impact on experimental rankings, suggesting our methodology effectively isolates teacher model performance differences independent of student model selection" (H). The teacher order Llama > Qwen > Mistral holds in every row.
- The survey's warning ("gain falls from +12.63 to +8.08 to +4.55 when the student changes") reads the first **row** as if it were a column. Those three numbers are three **teachers** teaching the Llama student (H).
- **Two-way decomposition [C]** (additive main effects, one run per cell):
  - teacher main effect 64.2% of the variance;
  - student main effect 34.9%;
  - interaction 0.9%.
  - Diagonal (same-model) residuals: +0.39, −0.11 and +0.05 pp. This 3×3 gives no evidence of self-affinity. Qwen teaches the Llama student better (+8.08) than it teaches itself (+4.55).
- **What remains a real warning:**
  - (a) The student is a large main effect: the Llama teacher's gain ranges 12.63 → 7.07 across students (1.8×). A weak student with a weak teacher gains exactly 0 (a floor).
  - (b) Noise. From Δ = 12.63 and PNIR = 0.26 (read as negative/positive flips; my assumption), about 17.1% of items flip up and 4.4% flip down. The paired SE of Δ is then about **3.2 pp** on 198 items [C]. Most between-cell differences in the table are within 1–2 SE.
  - (c) The ranking check has only 3 teachers.
  - (d) In the main 14-teacher table the top teacher is the student model. The 3×3 suggests this reflects the Llama teacher being strong for every student, not affinity. The confound nonetheless cannot be excluded in general (M).
- EducationQ itself flags "the limitations of our single-student model approach" (Ethics section, H).

### 1. Fidelity of LLM-simulated learners

**1a. Item-level agreement with real students (coarse statistics mostly agree).**
- **Generative Students** (Lu & Wang, L@S 2024) [lu2024generativestudents]:
  - 45 GPT-4 "generative students" with knowledge profiles vs 100 real college students on 20 MCQs.
  - Pearson r = 0.72 between simulated and real performance, with overlapping sets of hard items (M).
  - This is an item-difficulty, not a learning, agreement.
- **Simulated classrooms for item difficulty** [acquaye2026calculators] (Findings of ACL 2026):
  - Role-played grade-4/8/12 "classrooms" were fitted with IRT against NAEP.
  - Correlations with real item correctness reached 0.75, 0.76 and 0.82 (grades 4, 8, 12) "under the right conditions" (M).
- **Error alignment** [mistakeslikestudents2025] (AIED 2025): when LLMs err on MCQs they tend to choose the distractor students choose most.
  - Qwen-0.5B picks the most common student distractor 51.6% of the time; Qwen-72B 59.3%.
  - The correlations are "moderate" (M).
- **Ability level is not controllable by prompting** [naepsim2025] (BEA 2025): 489 NAEP items; 11 LLMs placed on the student IRT scale.
  - "Stronger models score far better than the average students of any grade", and weaker models "may align well incidentally" (M).

**1b. Dialogue-level, learning-dynamics and uptake fidelity (mostly poor for prompted students).**
- **Substance or illusion** [scarlatos2026simstudents] (ACL 2026; Eedi, 2,000 real tutoring dialogues):
  - Simulators were scored on linguistic, behavioural (dialogue acts), cognitive (correctness, errors, knowledge acquisition via LLM knowledge tracing) and tutor-response measures.
  - "Prompting strategies perform poorly", while SFT and DPO "perform better but remain limited". Prompting does well only on correctness (M; venue and BibTeX H from README).
- **StudentSim** [yang2026studentsim] (Microsoft, arXiv 2609.01591; 60 students, chess, ESL writing and math):
  - Two metrics: behavioural fidelity F and guidance responsiveness R.
  - Chess: GPT-5.4 role-play F = 0.23, R = 0.72; per-student trained simulator F = 0.51, R = 0.91; Maia2 F = 0.45, R = 0.27 (M).
  - The README states the requirement bluntly: "a simulator that answers better than the student does will not have the gaps the tutoring is meant to address" (H).
- **ParaStudent** [niousha2026parastudent] (EMNLP 2026; novice programming revisions):
  - The fine-tuned simulator reached AUC 0.80 at predicting real feedback relevance and uptake.
  - "Prompted baselines remained near chance on successful uptake" (M).
- **TutorGym** [weitekamp2025tutorgym] (AIED 2025; 223 ITS domains):
  - As tutors, current LLMs were "no better than chance at labeling incorrect actions", with next-step accuracy of about 52–70%.
  - As students learning in context, they produced "remarkably human-like learning curves" (M).
  - This is the one positive learning-curve result. It concerns step-level ITS practice, not dialogue teaching.
- **Teachers tutoring LLM students** [martynova2025llmstudents] (BEA 2025, ETH):
  - LLM students replicate "an attentive student" but lack authenticity and diversity.
  - Their responses are "too technical and complex", they lack emotion, are sometimes logically inconsistent, and rarely ask questions (M).

**1c. Named failure modes relevant to teach-back.**
- **Competence paradox, or "cannot stay ignorant"** [validsim2026]: capable LLMs cannot "unknow" solution schemas. The authors call for an explicit "epistemic state specification" (M; conceptual, no data).
  - The unlearning paper [unlearningnovice2026] makes the same diagnosis: prompted novices "drift beyond the intended knowledge level". It proposes machine unlearning followed by relearning through learning-by-teaching dialogue (M; no numbers captured).
- **Sycophantic misconception abandonment** [sycophanticsim2026] (arXiv 2605.12748):
  - Across 7 LLMs (4B–120B), prompted misconception-holding students show near-zero Selective Flip Score.
  - They correct their answers at similar rates whether feedback targets the true misconception, a different misconception, or just says "wrong".
  - This "persists under reflective prompting and multi-turn interaction" (M).
  - Implication: in-dialogue improvement of an LLM student is not evidence that teaching addressed the misconception.
- **Over-coherence** [thinkaloud2026] (630 chemistry think-aloud utterances): GPT-4.1 continuations are "over-coherent, verbose, and less variable". More context makes this worse, and "learner performance was consistently overestimated" (M).
- **Misconception vs competence trade-off** [malalgopy2024]: fine-tuning on MalAlgoPy "malgorithms" (20 algebra misconceptions) teaches the errors, but correct accuracy on other problem types falls. Mixing in correct examples mitigates this (M).

**1d. What the students in existing tutoring benchmarks are.**

| Benchmark | Student | Outcome | Teacher sees answers or items? | Conf |
|---|---|---|---|---|
| EducationQ [educationq2025] | Llama 3.1 70B (ablation: Qwen 72B, Mistral Nemo) | pre/post accuracy on GPQA and MMLU-Pro | "strict data flow controls" block options | H |
| MathTutorBench [macina2025mathtutorbench] | **No live student.** Pedagogy tasks generate the next teacher turn (max two sentences) on MathDial/Bridge histories and score it with a 1.5B reward model against the human teacher turn | reward-model win rate | n/a | H (config `pedagogy_following.yaml`, README) |
| MathDial (source dialogues) [macina2023mathdial] | InstructGPT-era LLM "prompted to represent common student errors", paired with human teachers | teacher-annotated success, incl. "Yes, but I had to reveal the answer"; interactive success-vs-telling trade-off | yes | H (README) |
| DeepTutor TutorBench [deeptutor2026] | "profile-driven", first-person student simulator with 3 gap types (misconception, incomplete, missing knowledge); 5 domains | LLM rubric | yes | M |
| TeachBench [teachbench2026] | Qwen2.5-7B-Instruct | pass@k gain on Gaokao items; top teacher Qwen3-235B +7.63 (math) | restricted to "knowledge points and example problems" | M |
| Teach2Eval [teach2eval2025] | 4 small students (LLaMA3.2-1B, Qwen2.5-1.5B, MiniCPM-2B, InternLM2.5-1.8B) | student MCQ accuracy after guidance; 33 teachers, 60 datasets | teacher does not see answer choices | M |
| PedagogicalRL [dinucujianu2025pedagogicalrl] | frozen LLM student | post-dialogue solve rate plus leakage/helpfulness judges | yes (penalised) | H (README) |
| DAS2 [disengaged2026] | 5 rule-defined engagement states (engaged, gaming, wheel-spinning, off-task, mixed) | tutor score; state labels validated on ASSISTments (κ = 0.75) | n/a | M |

### 2. Student choice and instrument stability

**2a. Every study found that varies the student (or user) model.**

| Study | What varies | Teachers or agents | Ranking stability | Effect-size change | Conf |
|---|---|---|---|---|---|
| EducationQ Table 2 | 3 students (Llama 70B, Qwen 72B, Mistral Nemo) | 3 | identical order in all rows (τ = 1 on 3 items: weak evidence) | same teacher 12.63 → 7.07 pp; interaction <1% [C] | H |
| Teach2Eval | leave one of 4 weak students out | 33 | correlation with Arena 0.907–0.911 and LiveBench 0.92 after removal (reported as robust) | not captured | M (the main-text Kendall τ is 0.790/0.821; the coefficient type for the removal check was not verified) |
| DAS2 | 5 student states × 10/20 turns | 5 (Claude, Llama, Gemini, Qwen, GPT families) | "relative rankings remained stable" (reported Spearman 1.00) | absolute scores differ by about 0.01–0.03 on 0–1 | M (qualitative); L (numbers) |
| Saha et al. [saha2023teach] | 2 families (Flan-T5, LLaMA) × 3 tasks | LLM and human teachers | LLM teachers help; "not as good as human teachers"; misaligned teachers can push students "to random chance" | Flan-T5-XL → Flan-T5-Large: +5% at 100% intervention (StrategyQA) | H (README RQs; abstract); M (number) |
| RankCert [rankcert2026] | several knowledge-tracing learner models (EdNet, 5,000 learners) | 8 policies | "learner models with adequate predictive performance imply different policy rankings", so the method abstains unless many criteria agree | n/a | M |
| Lost in Simulation [seshadri2026lostinsim] | user LLM (τ-bench retail) plus a real-user study (US, India, Kenya, Nigeria) | agents | not captured | agent success varies "up to 9 percentage points across different user LLMs"; underestimates hard tasks and overestimates moderate ones | M |
| SWEET-RL / ColBench [zhou2025sweetrl] | simulator size | — | — | README: using Llama-3.1-8B instead of 70B as simulator gives results that "may be different from provided in the paper" | H |

Analogues from distillation (training, not in-context teaching), L–M as evidence for teach-back:
- Small students (≤3B) learn *worse* from strong or long-CoT teachers (the "learnability gap") [li2025smallmodelgap] (M).
- "The strongest teacher is not always the best teacher": across 30 teachers × 6 student bases, student-matched supervision beats teacher strength [scas2026] (M).
- Both predict teacher × student interactions when students are small.

**2b. Methods used to control student prior knowledge.**
1. **Pre/post difference on known items.** Used by EducationQ, TeachBench and Teach2Eval. It is exposed to contamination and ceiling effects, and to the student already knowing the answer.
2. **Weak or small students.** Used by Teach2Eval (1–2B) and Saha et al. (Flan-T5-Large, LLaMA-7B). They risk the learnability gap and floor effects (EducationQ's Mistral student gained 0 from the Mistral teacher).
3. **Role-played ignorance or personas.** Used by Generative Students, DeepTutor TutorBench and MathDial. This is contradicted by the competence-paradox, NAEP-ability, think-aloud and sycophancy results (§1).
4. **Capacity or knowledge removal.** Machine unlearning to a novice level, then relearning [unlearningnovice2026], and per-student trained simulators [yang2026studentsim]. Both are promising but domain-specific and unvalidated on learning gains.
5. **Genuinely novel material.** Procedurally generated content makes ignorance real rather than simulated. This is the teach-back design; the MTOB-style prior art is in prior_art_novel_methods.md. No tutoring benchmark found uses it.

### 3. Teaching vs telling (answer leakage)

**How existing evaluations detect or forbid telling:**
- **Hide the items from the teacher.**
  - EducationQ technically prevents teachers "from accessing any of the question options", plus prompt instructions (H).
  - Teach2Eval: the teacher gives guidance "without seeing the answer choices" (M).
  - TeachBench restricts teachers to "structured knowledge points and example problems … avoid[ing] information leakage" (M).
- **Measure telling explicitly.**
  - MathDial reports an interactive "trade-off between student solving success and telling solutions". Teachers annotate "Yes, but I had to reveal the answer" (H).
  - PedagogicalRL optimises Δ solve rate while LLM judges flag leaked solutions. A penalty λ sets the trade-off, and λ = 0 means "no pedagogy constraint" (H, README). Trained tutors lie on a solve-rate vs leakage Pareto front (M).
- **Separate solving from teaching** [tutordiag2026].
  - The solving and pedagogy composites correlate at 0.421 across 8 models, with rank shifts (M; existing key).
  - It notes that "directly giving away an answer may improve immediate task completion while reducing the learner's opportunity to reason independently" (M).
  - It recommends reporting solving and pedagogy scores separately, with explicit "disclosure-sensitive, student-agency-preserving criteria" (M).
- **Robustness to answer extraction** [leakagerobust2026] (ACL 2026): adversarial simulated students extracted answers in 47% (emotional threat) to 74% (contextual manipulation) of dialogues. TutorRL-7B and Qwen-7B leaked about 75% of the time. "Reasoning-first" and multi-agent defences cut leakage to under 10% for most models (M).
- **Google LearnLM.**
  - The 2024 evaluation-driven report [learnlm2024responsible] translates learning-science principles into seven benchmarks. They include a principle "Do not reveal the answer; guide towards the answer; promote active engagement", LLM-critic auto-evals, and 168 pedagogy experts role-playing learners (M).
  - The LearnLM report [learnlm2024] trains "pedagogical instruction following". Expert raters preferred LearnLM by 31% over GPT-4o, 11% over Claude 3.5 and 13% over Gemini 1.5 Pro (M).
  - The arena for learning [learnlm2025arena]: 189 educators role-played learners and 206 experts judged. Gemini 2.5 Pro was preferred in 73.2% of non-tied match-ups (M).
  - All of these measure expert preference, not learner learning.
- **OpenAI Study Mode** (29 July 2025) [openai2025studymode]: "step by step guidance instead of quick answers". It is "powered by custom system instructions" written with teachers and pedagogy experts, and may cause "inconsistent behavior and mistakes across conversations" (M, primary page via search extract).
  - OpenAI's later "Learning Outcomes Measurement Suite" (with the University of Tartu and Stanford SCALE) is aimed at longitudinal outcomes "not just on a final exam" [openai2026learningoutcomes] (M; date not verified).
- **Anthropic Claude for Education learning mode** [anthropic2025claudeedu]: "guides students' reasoning process rather than providing answers" through Socratic questioning (M, primary page via search extract).
  - Anthropic's usage report [anthropic2025edureport] found about 47% of student conversations were "Direct", i.e. seeking answers with minimal engagement (M).
  - Neither page reports learning outcomes.
- **Saha et al.** RQ1–3 measure teacher explanations given *on the test instance itself* (test-time intervention), which is telling. Only RQ4 measures gains "on future unexplained data" (H, README RQ list; abstract).

**Human evidence that telling can beat teaching on an immediate test:**
- **Bastani et al., PNAS 2025** [bastani2025guardrails]. RCT with nearly 1,000 Turkish high-school students; arms: GPT Base, GPT Tutor (hints, not answers), and control.
  - Practice-session gains: +48% (Base) and +127% (Tutor).
  - Unassisted exam: Base −17% vs control; Tutor's harm "essentially eradicated", with no positive effect (M; the −17% is the working-paper wording, not re-read in the PNAS version; a correction was published in August 2025, M).
- **Kumar et al., AIED 2025** [kumar2025mathperil]: pre-registered, about 1,200 participants.
  - LLM explanations beat answer-only on later test questions.
  - Benefits were largest when learners attempted problems before seeing explanations.
  - Incorrect LLM explanations produced gains between answer-only and correct explanations (M). Human learning is therefore sensitive to explanation quality: a manipulation check a human validation can reuse.
- **Eedi / LearnLM RCT** [learnlm2025eedirct] (N = 165, 5 UK schools):
  - Immediate mistake correction: 91.2% (human tutors), 93.0% (LearnLM), 65.4% (static hints).
  - Transfer to the first question of the next unit: 66.2% (LearnLM), 60.7% (human), 56.2% (hints); +5.5 pp, 93.6% posterior probability.
  - Tutors approved 76.4% of LearnLM drafts with little or no editing; 5 factual errors in 3,617 messages (M).
  - The **immediate** outcome saturated and did not discriminate; the **transfer** outcome did.

### 4. External criterion from human learning

**4a. Randomised trials of AI tutoring.**

| Study | N | Design | Outcome measured without AI? | Effect | Multiple LLMs/configs? | Conf |
|---|---|---|---|---|---|---|
| Bastani et al. 2025 [bastani2025guardrails] | about 1,000 high-school students | 3-arm RCT, GPT-4 | **yes** (exam after access removed) | practice +48% / +127%; exam −17% (Base), about 0 (Tutor) | 2 configs of one model | M |
| Kestin et al. 2025 [kestin2025aitutoring] | 194 undergraduates | crossover; GPT-4 "PS2 Pal" vs in-class active learning | post-test at end of session; AI access during test not verified | 0.73–1.3 SD; less time | no | M |
| Tutor CoPilot [wang2024tutorcopilot] | 900 tutors, 1,800 K-12 students | AI assists *human* tutors | yes (students never use AI) | +4 pp mastery; +9 pp for lower-rated tutors; tutors "less likely to give away the answer" | no | M–H |
| De Simone et al. 2025 (Nigeria) [desimone2025chalkboards] | about 800 students, 9 schools | 6-week after-school Copilot (GPT-4) with teachers | yes (pen-and-paper test) | 0.31 SD overall; 0.23 SD English; end-of-year exams also improved | no | M |
| Pardos & Bhandari 2024 [pardos2024chatgpthelp] | 274 | ChatGPT hints vs human hints vs none | yes | ChatGPT hints: 43.51 → 60.52% (+17 pp); not different from human hints | no | M |
| Kumar et al. 2025 [kumar2025mathperil] | about 1,200 | answer-only vs LLM explanation × attempt order; correct vs incorrect explanations | yes | explanations > answer-only; incorrect explanations intermediate | explanation-quality manipulation | M |
| Eedi/LearnLM 2025 [learnlm2025eedirct] | 165 | LearnLM (supervised) vs human tutors vs static hints | yes (next-unit item) | +5.5 pp transfer vs human | no (1 model vs humans) | M |
| **StudentBench 2026** [northcutt2026studentbench] | **2,383 learners; 2,469 sessions** (2,139 AI, 140 human, 190 none) | 1-hour GRE tutoring; 27-item pre/post; 7 domains | post-test after the session | AI vs control +6.15 pp [4.08, 8.21]; AI vs human −0.58 pp (90% CI [−2.18, 1.03], TOST p = .015) | **13 AI configurations per section**; 6 pass individual equivalence | H (repo verification file) |

**4b. Studies that compare multiple models on human learning.** Only StudentBench compares many LLMs on measured human learning. Its per-model resolution is the key fact for sizing (H, from `verification/paper_results_expected.json`):
- **0 of 364** domain × tutor effect cells were significant.
- **7 different winners** topped the 7 domains.
- The verbal domain-interaction test gave Holm p = 0.173.
- Prompt-variant contrasts were non-significant:
  - Opus 5 expanded vs minimal prompt: +3.61 pp [−1.66, 8.89];
  - Gemini 3.6 Flash: +4.62 pp [−0.17, 9.42].
- Six AI tutors passed individual equivalence with human tutoring.
- In contrast, expert rubric reviews (2,028 pairwise reviews, 51 experts) **did** separate tutors, e.g. Opus 5 won lesson planning and practice design.
- Implication (M): with about 80–170 learners per configuration, frontier tutors are indistinguishable on human gain, although experts and costs distinguish them.

Other multi-model comparisons measure expert preference, not learning: the arena for learning [learnlm2025arena] and the LearnLM report [learnlm2024]. Bastani compares two configurations of one model; Kumar et al. manipulate explanation quality.

**4c. Sizing a human validation study [C].**
- From StudentBench's pooled AI-vs-control CI (±2.07 pp with 190 vs 2,139 learners), the implied per-learner SD of gain is about **13.9 pp**. If the contrast is covariate-adjusted, this is a residual SD (M).
- With SD 13.9, two-sided α = .05 and 80% power, the learners per arm needed to detect a between-teacher difference are:
  - 2 pp: **761**;
  - 3 pp: **338**;
  - 5 pp: **122**.
- **Reliability of a per-teacher human gain** = σ_b²/(σ_b² + 13.9²/n), where σ_b is the true between-teacher SD:
  - σ_b = 1.5 pp: 0.54 at n = 100, 0.70 at n = 200;
  - σ_b = 1.0 pp: 0.34 at n = 100, 0.51 at n = 200.
  - Frontier-only arms (σ_b of about 1–2 pp, judging from StudentBench's spread) make validation very expensive.
- **Precision of a model-level validation correlation** across K teacher arms, 95% CI for an observed r = 0.8:
  - K = 8: [0.22, 0.96];
  - K = 10: [0.34, 0.95];
  - K = 16: [0.50, 0.93].
- A feasible study is therefore a **falsification test with engineered arms of widely different quality**, not a calibration of frontier differences.

### 5. Communication and delegation evaluations with simulated users

| Work | Simulator | Human comparison | Simulator error or instability | Conf |
|---|---|---|---|---|
| τ²-bench [barres2025tau2] | LLM user; tool-equipped in telecom | none reported in extract | total user-simulator error 40% (retail) and 47% (airline), 12–13% critical; **16% (telecom), 6% critical** with tool/state-constrained users | M |
| τ²/τ³ changelog [sierra2026tau2changelog] | — | — | v1.0.0 adds a "Hallucination reviewer for detecting user simulator deviations **in voice evaluations**", "automatic hallucination retry", "LLM-based conversation review", and a fix to one task's "user simulator prompt" (task 100) | H |
| Lost in Simulation [seshadri2026lostinsim] (ACL 2026) | several user LLMs on τ-bench retail | real users in 4 countries | success varies up to 9 pp across user LLMs; systematic miscalibration; worst proxy for AAVE speakers | M |
| Mind the Sim2Real Gap [zhou2026sim2real] | 31 simulators | **451 humans, 165 τ-bench tasks** | simulators "excessively cooperative, stylistically uniform"; an "easy mode" that inflates agent success; "higher general model capability does not necessarily yield more faithful user simulation"; human–human User-Sim Index baseline about 92.7% | M |
| Collaborative Gym [shao2024cogym] | GPT-4o simulated users (H, README) | real-user condition | real users: collaborative agents beat autonomous agents 86% / 74% / 66% (travel, tabular, related work); communication failures 80% (simulated) vs 65% (real); situational-awareness failures 47% vs 40%; delivery lower with simulated users | M |
| CollabLLM [wu2025collabllm] (ICML 2025, Outstanding Paper, H) | LLM user simulator for multi-turn-aware rewards | **201-person MTurk study** | simulated gains (+18.5% task, +46.3% interactivity by LLM judges) were directionally confirmed by humans (+17.6% satisfaction, −10.4% time) | M |
| ColBench / SWEET-RL [zhou2025sweetrl] | Llama-3.1-70B (code), Qwen2-VL-72B (design) with the reference artifact | none seen | README warns a smaller simulator changes results | H (README); M (rest) |
| Lost in Conversation [laban2025lost] | GPT-4o-mini sharded-user simulator | none | README: "not intended to simulate realistic interaction between humans and LLMs … cannot be used to make claims about humans"; authors inspected 200 simulated conversations for simulation error (rate not captured) | H (README); M (200) |

Consistent lesson: simulator error is large when the simulated user speaks freely and small when its actions are tool- or state-constrained. Simulator choice moves absolute success by several points. The few human calibrations (CollabLLM, Co-Gym, Sim2Real) agree on direction but not on levels.

### 6. Master evidence table (by design question)

| Design question | Strongest evidence | What it implies | Conf |
|---|---|---|---|
| Can a prompted LLM play an ignorant student? | competence paradox; NAEP-ability; over-coherent think-aloud; near-zero SFS across 7 LLMs | no: ignorance must come from the material, not the prompt | M |
| Do LLM students match humans at all? | item difficulty r = 0.72–0.82; human-like ITS learning curves (TutorGym) | coarse item statistics yes; dialogue uptake no (prompted) | M |
| Does student choice change teacher scores? | EducationQ 3×3: student effect 35% of variance, teacher 64%, interaction <1% [C]; 9 pp user-LLM swings | absolute gains are student-relative; rankings looked stable in tiny tests | H/M |
| Is there same-family affinity? | EducationQ 3×3 diagonal residuals ≈ 0 [C]; two single-student benchmarks crowned same-family teachers | unproven either way; control by design | H/M |
| Does telling inflate immediate gains? | Bastani (+48% practice, −17% exam); Eedi (immediate saturates, transfer separates); PedagogicalRL Pareto front | test isolated and transfer; penalise disclosure | M |
| Do human gains separate frontier LLM teachers? | StudentBench: 0/364 significant cells; 7 domain winners | human validation needs engineered spread, not frontier-only arms | H |
| Do simulated users behave like humans? | τ² 40–47% errors (free text) vs 16% (tool-constrained); Sim2Real "easy mode"; Co-Gym failure rates differ | constrain simulators; audit; small human calibration | M |

## Implications for designing a new benchmark

All items are [I] (my inference), each tied to the cited evidence. Numbers in brackets are proposals, not findings.

1. **Student selection: fixed, pinned, open-weight, mid-capacity students.**
   - Pin exact checkpoints and decoding, as EducationQ chose an open model "for reproducibility" [educationq2025].
   - Avoid ≤3B students as the only instrument: they show the learnability gap [li2025smallmodelgap] and floor effects (Mistral student gained 0.00 from the Mistral teacher, §0).
   - Admit a student only if a reference teacher and a raw-material baseline both yield a clearly positive gain on a calibration split.

2. **Number of student families: ≥3, with a leave-family-out headline.**
   - Report each teacher's gain averaged over students *not* from its own family. Also publish the full teacher × student matrix, and the interaction variance share with CIs.
   - Evidence:
     - the student main effect is 35% of variance and the same teacher's gain varies 1.8× (§0, [C]);
     - two single-family benchmarks crowned same-family teachers [educationq2025; teachbench2026];
     - simulator choice moves success by up to 9 pp [seshadri2026lostinsim];
     - learner models with similar fit rank policies differently [rankcert2026].
   - Pre-register a stability criterion, e.g. the lower bound of the bootstrap CI for Kendall τ between student families. Fall back to rank bands (RankCert-style abstention) when it fails.

3. **Prior-knowledge control: make ignorance real, and measure three baselines.**
   - Never rely on prompted ignorance or personas [validsim2026; sycophanticsim2026; thinkaloud2026; naepsim2025].
   - Use procedurally generated material on which every student's pre-test is at chance. Verify this per student and per generator window.
   - Score teaching as value-added over three reference arms run on the same student and items:
     - (a) no teaching;
     - (b) **raw material**: the student reads the source directly under the same token budget;
     - (c) **teller**: a scripted arm that states rules and worked answers to practice items without pedagogy.
   - The headline gain must exceed (b). Reporting (c) exposes whether the instrument rewards telling.

4. **Leakage rules.**
   - (a) The teacher never sees post-test items, their seeds, or the held-out rule combinations they test [educationq2025; teach2eval2025; teachbench2026].
   - (b) Post-test items require composition or transfer beyond anything stated verbatim in the material, so pasting the source is insufficient; the MTOB lesson is in prior_art_novel_methods.md.
   - (c) Cap the teacher's total message budget below the material length, so teaching is selection and compression, not transmission.
   - (d) Report n-gram overlap between teacher messages and the source, and a disclosure-judge rate, in the MathDial / PedagogicalRL tradition [macina2023mathdial; dinucujianu2025pedagogicalrl].
   - (e) Use fixed, non-adaptive students. An adversarial student would measure extraction robustness, a different construct [leakagerobust2026].
   - (f) Randomise answer formats and grade open responses exactly, so a teacher cannot coach test-taking ("always answer B").

5. **Isolate the student at test time: closed-book, notes-only.**
   - Run the post-test in a fresh context with no teacher and no dialogue transcript. The only carry-over is a student-written, length-capped notes file.
   - This is the LLM analogue of Bastani's unassisted exam [bastani2025guardrails]. It also neutralises sycophantic in-dialogue flipping [sycophanticsim2026].
   - In-dialogue correctness never counts toward the score. EducationQ-style tests where the transcript remains in context measure open-book performance.

6. **Post-test timing and content.**
   - For LLM students, "delay" means the context isolation of item 5, not wall-clock time.
   - Weight the headline toward **transfer** items. Evidence: immediate outcomes saturated at 91–95% for both human and AI tutors while transfer separated them [learnlm2025eedirct]; practice scores and unassisted exams diverged [bastani2025guardrails].
   - Report near-transfer and far-transfer separately.

7. **Noise budget.**
   - One 198-item run gives a gain SE of about 3.2 pp (§0, [C]).
   - Target SE ≤1.5 pp per teacher × student cell, i.e. roughly ≥1,000 items with a discordance of about 20% [C, derived with the same formula]. Use multiple generator seeds, K samples per item, and paired, clustered SEs (consistent with briefs/D implication 6).

8. **Human validation study: a pre-registered falsification test.**
   - Arms: about 8–10 teachers on the *same* generated material, spanning a wide quality range:
     - no teaching;
     - raw material;
     - teller;
     - a deliberately misleading teacher (Saha et al.'s manipulation [saha2023teach]);
     - a small model;
     - 3–5 frontier teachers.
   - About 120–150 learners per arm detects 5 pp arm differences, with the implied SD of 13.9 pp from StudentBench [C]. That is about 1,000–1,500 online learners in total, comparable to Kumar et al. (about 1,200) and StudentBench (2,383) [kumar2025mathperil; northcutt2026studentbench].
   - Novel material helps: human pre-tests will also be near floor.
   - Primary statistics:
     - (i) the rank correlation across arms between LLM-student gain and human gain. With K = 10 an observed 0.8 has CI [0.34, 0.95], so this is a coarse check [C];
     - (ii) a **teller-inversion test**: the instrument fails if it ranks the teller arm above the good teachers while humans on the transfer or delayed test do not;
     - (iii) a delayed human post-test (e.g. next day, fixed a priori) on a subsample.
   - Frontier-vs-frontier validation is out of reach at this size: StudentBench's 0/364 significant cells show it.

9. **Use existing human data as a second criterion.**
   - StudentBench releases per-session human gains for 13 AI tutor configurations with code (CC BY 4.0) [northcutt2026studentbench].
   - Running the same configurations as teachers of LLM students on GRE-style items would give a cheap cross-instrument check. Caveats: GRE content is not novel, and human gains separate these tutors poorly.

10. **Report teaching separately from solving and from g.**
    - Solving and pedagogy correlate only at 0.421 [tutordiag2026].
    - Teach-a-weak-student scores track general rankings closely (Kendall τ 0.790 with Chatbot Arena, 0.821 with LiveBench) [teach2eval2025].
    - The headline should therefore be accompanied by its residual on a general-capability index (consistent with briefs/D implication 7).

11. **Plan for Goodhart pressure.**
    - When student solve rate is the reward, tutors trade pedagogy for leakage unless penalised [dinucujianu2025pedagogicalrl].
    - Build the leakage audit (item 4d) into the scored metric, not only into a side report.

12. **For any communication or delegation benchmark with simulated users.**
    - (a) Constrain the simulator's actions through tools or state wherever possible: 16% vs 40–47% error [barres2025tau2].
    - (b) Run ≥2 simulator LLMs and report success deltas and rank changes [seshadri2026lostinsim; zhou2025sweetrl].
    - (c) Audit a random sample of simulator turns for deviations, and bin simulator failures separately from agent failures [sierra2026tau2changelog; laban2025lost].
    - (d) Calibrate against a small human condition, as Co-Gym, CollabLLM and Sim2Real did with 201–451 people [shao2024cogym; wu2025collabllm; zhou2026sim2real].
    - (e) Do not choose the simulator by general capability [zhou2026sim2real].

## Claims ledger

| # | Claim | Source URL(s) | Conf |
|---|---|---|---|
| 1 | EducationQ Table 2 is student (rows) × teacher (columns). Llama student: teachers Llama/Qwen/Mistral gain 12.63/8.08/4.55; Qwen student 8.59/4.55/2.53; Mistral student 7.07/2.53/0.00 | https://github.com/SunriserFuture/EducationQ (docs/2025.acl-long.1576.pdf) | H |
| 2 | EducationQ says the student ablation had "negligible impact on experimental rankings" | same | H |
| 3 | 3×3 decomposition: teacher 64.2%, student 34.9%, interaction 0.9%; diagonal residuals +0.39/−0.11/+0.05 | computed from #1 | H [C] |
| 4 | Gain SE ≈3.2 pp for 198 items (assumes PNIR = negative/positive flips) | computed from #1 | M [C] |
| 5 | EducationQ blocks teacher access to answer options; acknowledges its "single-student model approach" as a limitation | EducationQ PDF | H |
| 6 | Generative Students: 45 GPT-4 students vs 100 real students, 20 MCQs, r = 0.72 | https://arxiv.org/abs/2405.11591 ; https://dl.acm.org/doi/10.1145/3657604.3662031 | M |
| 7 | Simulated-classroom item difficulty correlations 0.75/0.76/0.82 (grades 4/8/12) | https://arxiv.org/abs/2601.09953 ; https://aclanthology.org/2026.findings-acl.1807/ | M |
| 8 | Distractor alignment: Qwen-0.5B 51.6% top distractor; Qwen-72B 59.3% | https://arxiv.org/abs/2502.15140 | M |
| 9 | NAEP (489 items, 11 LLMs): strong models far above average students of any grade | https://arxiv.org/abs/2507.08232 ; https://aclanthology.org/2025.bea-1.75/ | M |
| 10 | Prompted student simulators perform poorly; SFT/DPO better but limited (2,000 Eedi dialogues) | https://github.com/umass-ml4ed/sim-student-eval ; https://arxiv.org/abs/2601.04025 | M (H venue) |
| 11 | StudentSim chess: GPT-5.4 F = 0.23 / R = 0.72 vs StudentSim 0.51 / 0.91 | https://arxiv.org/abs/2609.01591 ; https://github.com/microsoft/StudentSim | M |
| 12 | ParaStudent AUC 0.80 vs prompted baselines near chance on uptake | https://arxiv.org/abs/2507.12674 | M |
| 13 | TutorGym: LLM tutors at chance on labelling errors; next-step 52–70%; human-like learning curves as ICL students | https://arxiv.org/abs/2505.01563 | M |
| 14 | LLM students "too technical and complex", lack emotions, rarely ask questions | https://aclanthology.org/2025.bea-1.8/ | M |
| 15 | Competence paradox / epistemic state specification (conceptual) | https://arxiv.org/abs/2601.05473 | M |
| 16 | Near-zero Selective Flip Score across 7 LLMs (4B–120B); persists under reflection | https://arxiv.org/abs/2605.12748 | M |
| 17 | GPT-4.1 think-alouds over-coherent; performance overestimated (630 utterances) | https://arxiv.org/abs/2602.01015 | M |
| 18 | MalAlgoPy: misconception accuracy trades off against correct accuracy | https://arxiv.org/abs/2410.12294 | M |
| 19 | MathTutorBench pedagogy task = next teacher turn on MathDial/Bridge histories, reward-model scored (no live student) | https://github.com/eth-lre/mathtutorbench (configs/pedagogy_following.yaml; README) | H |
| 20 | MathDial pairs human teachers with an LLM prompted to show student errors; measures success vs telling | https://github.com/eth-nlped/mathdial | H |
| 21 | DeepTutor TutorBench uses a profile-driven first-person student simulator with 3 gap types | https://arxiv.org/abs/2604.26962 | M |
| 22 | TeachBench: Qwen2.5-7B student; teachers restricted to knowledge points; Qwen3-235B top (+7.63 math) | https://arxiv.org/abs/2601.21375 | M |
| 23 | Teach2Eval: 33 LLMs, 60 datasets, 4 small students; Kendall 0.790 (Arena), 0.821 (LiveBench); stable after dropping a student | https://arxiv.org/abs/2505.12259 | M |
| 24 | DAS2: rankings of 5 tutors stable across 5 student states; absolute scores vary | https://arxiv.org/abs/2609.12331 | M |
| 25 | Saha et al.: LLM teachers improve students across Flan-T5/LLaMA; worse than humans; misaligned teachers push students to random; RQ4 tests future data | https://github.com/swarnaHub/ExplanationIntervention ; https://arxiv.org/abs/2306.09299 | H |
| 26 | Saha et al.: Flan-T5-XL → Flan-T5-Large +5% at 100% intervention (StrategyQA) | https://arxiv.org/abs/2306.09299 (search extract) | M |
| 27 | RankCert: learner models with adequate fit imply different tutor-policy rankings | https://arxiv.org/abs/2609.26069 | M |
| 28 | Small models (≤3B) learn worse from strong/long-CoT teachers | https://arxiv.org/abs/2502.12143 | M |
| 29 | PedagogicalRL: reward = post-dialogue solve rate + judges; leakage penalty λ | https://github.com/eth-lre/PedagogicalRL | H |
| 30 | Adversarial students extract answers in 47–74% of dialogues; defences cut this to <10% | https://arxiv.org/abs/2604.18660 ; https://aclanthology.org/2026.acl-long.1412/ | M |
| 31 | tutordiag2026: solving–pedagogy correlation 0.421 (8 models); recommends separate reporting | https://arxiv.org/abs/2606.16206 | M |
| 32 | LearnLM preferred by 31% / 11% / 13% over GPT-4o / Claude 3.5 / Gemini 1.5 Pro | https://arxiv.org/abs/2412.16429 | M |
| 33 | LearnLM-Tutor report: 7 benchmarks; "do not reveal the answer" principle; 168 expert role-players | https://arxiv.org/abs/2407.12687 | M |
| 34 | Arena for learning: 189 educators, 206 experts; Gemini 2.5 Pro 73.2% excluding ties | https://arxiv.org/abs/2505.24477 | M |
| 35 | Eedi RCT: N = 165; transfer 66.2 / 60.7 / 56.2%; immediate 93.0 / 91.2 / 65.4% | https://arxiv.org/abs/2512.23633 | M |
| 36 | OpenAI Study Mode (29 July 2025) is powered by custom system instructions | https://openai.com/index/chatgpt-study-mode/ | M |
| 37 | Anthropic learning mode guides reasoning rather than providing answers; about 47% of student conversations Direct | https://www.anthropic.com/news/introducing-claude-for-education ; https://www.anthropic.com/news/anthropic-education-report-how-university-students-use-claude | M |
| 38 | Bastani: about 1,000 students; practice +48% / +127%; unassisted exam −17% for GPT Base | https://www.pnas.org/doi/10.1073/pnas.2422633122 ; https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4895486 | M |
| 39 | Kestin: 194 students, crossover, 0.73–1.3 SD; tutor gives one step at a time | https://www.nature.com/articles/s41598-025-97652-6 | M |
| 40 | Tutor CoPilot: 900 tutors / 1,800 students; +4 pp (+9 pp lower-rated); less answer-giving | https://arxiv.org/abs/2410.03017 ; https://edworkingpapers.com/ai24-1054 | M |
| 41 | Nigeria: about 800 students; 0.31 SD (0.23 SD English); pen-and-paper test | https://ideas.repec.org/p/wbk/wbrwps/11125.html ; https://blogs.worldbank.org/en/education/From-chalkboards-to-chatbots-Transforming-learning-in-Nigeria | M |
| 42 | Pardos & Bhandari: N = 274; ChatGPT hints +17 pp; no difference vs human hints | https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0304013 | M |
| 43 | Kumar et al.: about 1,200 participants; explanations > answers; attempt-first best; wrong explanations intermediate | https://link.springer.com/chapter/10.1007/978-3-031-98459-4_5 | M |
| 44 | StudentBench: 2,383 learners; 13 AI configs per section; AI vs control +6.15 pp [4.08, 8.21]; 0/364 significant domain × tutor cells; 7 distinct domain winners | https://github.com/Handshake-AI-Research/studentbench (README; verification/paper_results_expected.json) | H |
| 45 | Implied learner SD of gain about 13.9 pp; n per arm 761 / 338 / 122 for 2 / 3 / 5 pp | computed from #44 | M [C] |
| 46 | τ² user-simulator error 40% / 47% (retail/airline) vs 16% (telecom) | https://arxiv.org/abs/2506.07982 (search extract) | M |
| 47 | τ³ v1.0.0 hallucination reviewer is scoped to voice evaluations | https://raw.githubusercontent.com/sierra-research/tau2-bench/main/CHANGELOG.md | H |
| 48 | Agent success varies up to 9 pp across user LLMs; miscalibration | https://arxiv.org/abs/2601.17087 ; https://aclanthology.org/2026.acl-long.2192/ | M |
| 49 | 451 humans, 165 tasks, 31 simulators; capability does not predict fidelity; "easy mode" inflation | https://arxiv.org/abs/2603.11245 ; https://github.com/AkihikoWatanabe/paper_notes/issues/4977 | M |
| 50 | Co-Gym: 86 / 74 / 66% real-user win rates; communication failures 65% (real) vs 80% (simulated) | https://arxiv.org/abs/2412.15701 ; https://github.com/SALT-NLP/collaborative-gym | M |
| 51 | CollabLLM: 201 MTurk participants; +17.6% satisfaction; −10.4% time | https://arxiv.org/abs/2502.00640 ; https://github.com/Wuyxin/collabllm | M |
| 52 | ColBench README: a smaller simulator may change results | https://github.com/facebookresearch/sweet_rl | H |
| 53 | Lost in Conversation README disclaims validity for human claims | https://github.com/microsoft/lost_in_conversation | H |

## References

Reused keys: educationq2025, macina2025mathtutorbench, tutordiag2026, saha2023teach, tutorbench2025, laban2025lost, barres2025tau2, yao2024tau, sierra2026tau2changelog.

1. [educationq2025] Shi, Y., Liang, R., Xu, Y. EducationQ: Evaluating LLMs' Teaching Capabilities Through Multi-Agent Dialogue Framework. ACL 2025. https://github.com/SunriserFuture/EducationQ
2. [macina2025mathtutorbench] Macina, J. et al. MathTutorBench. EMNLP 2025. https://github.com/eth-lre/mathtutorbench
3. [tutordiag2026] Yao, J., Zheng, Z., Li, B. Measuring Whether LLM Tutors Teach or Solve (v2: Beyond Helpfulness: A Teaching-over-Solving Diagnostic…). arXiv:2606.16206.
4. [saha2023teach] Saha, S., Hase, P., Bansal, M. Can Language Models Teach Weaker Agents? NeurIPS 2023. arXiv:2306.09299.
5. [tutorbench2025] TutorBench (Scale). arXiv:2510.02663.
6. [laban2025lost] Laban, P., Hayashi, H., Zhou, Y., Neville, J. LLMs Get Lost In Multi-Turn Conversation. arXiv:2505.06120. https://github.com/microsoft/lost_in_conversation
7. [barres2025tau2] Barres, V. et al. τ²-Bench. arXiv:2506.07982.
8. [sierra2026tau2changelog] Sierra Research. tau2-bench CHANGELOG. https://github.com/sierra-research/tau2-bench/blob/main/CHANGELOG.md
9. [lu2024generativestudents] Lu, X., Wang, X. Generative Students: Using LLM-Simulated Student Profiles to Support Question Item Evaluation. L@S 2024. arXiv:2405.11591.
10. [acquaye2026calculators] Acquaye, C., Huang, Y. T., Carpuat, M., Rudinger, R. Take Out Your Calculators: Estimating the Real Difficulty of Question Items with LLM Student Simulations. Findings of ACL 2026. arXiv:2601.09953.
11. [mistakeslikestudents2025] Do LLMs Make Mistakes Like Students? Exploring Natural Alignment between Language Models and Human Error Patterns. AIED 2025. arXiv:2502.15140.
12. [naepsim2025] Can LLMs Reliably Simulate Real Students' Abilities in Mathematics and Reading Comprehension? BEA 2025. arXiv:2507.08232.
13. [scarlatos2026simstudents] Scarlatos, A., Lee, J., Woodhead, S., Lan, A. Simulated Students in Tutoring Dialogues: Substance or Illusion? ACL 2026. arXiv:2601.04025.
14. [yang2026studentsim] Yang, K., Wang, C., Galley, M., Singh, C., Inala, J. P., Zhai, C., Gao, J. StudentSim: Training LLM-based Student Simulators. arXiv:2609.01591.
15. [niousha2026parastudent] Niousha, R. et al. ParaStudent: Closing the Sim2Real Gap in User Simulators for AI Tutor Evaluation. EMNLP 2026. arXiv:2507.12674.
16. [weitekamp2025tutorgym] Weitekamp, D., Siddiqui, M. N., MacLellan, C. J. TutorGym: A Testbed for Evaluating AI Agents as Tutors and Students. AIED 2025. arXiv:2505.01563.
17. [martynova2025llmstudents] Martynova, Macina, Daheim, Yalçın, Zhang, Sachan. Can LLMs Effectively Simulate Human Learners? Teachers' Insights from Tutoring LLM Students. BEA 2025.
18. [validsim2026] Towards Valid Student Simulation with Large Language Models. arXiv:2601.05473.
19. [unlearningnovice2026] Simulating Novice Students Using Machine Unlearning and Relearning in Large Language Models. arXiv:2603.26142.
20. [sycophanticsim2026] Simulating Students or Sycophantic Problem Solving? On Misconception … (title end not captured). arXiv:2605.12748.
21. [thinkaloud2026] Large Language Models as Students Who Think Aloud: Overly Coherent, Verbose, and Confident. arXiv:2602.01015.
22. [malalgopy2024] LLM-based Cognitive Models of Students with Misconceptions. arXiv:2410.12294.
23. [macina2023mathdial] Macina, J. et al. MathDial. Findings of EMNLP 2023. arXiv:2305.14536. https://github.com/eth-nlped/mathdial
24. [deeptutor2026] DeepTutor: Towards Agentic Personalized Tutoring. arXiv:2604.26962.
25. [teachbench2026] TeachBench: A Syllabus-Grounded Framework for Evaluating Teaching Ability in … (title end truncated in listings). arXiv:2601.21375.
26. [teach2eval2025] Teach2Eval: An Indirect Evaluation Method for LLM by Judging How It Teaches. arXiv:2505.12259.
27. [disengaged2026] Simulating Disengaged Students to Evaluate LLM-based Tutors. arXiv:2609.12331.
28. [rankcert2026] Kadir, N. RankCert: When Can Simulated Learners Safely Select an AI Tutor? arXiv:2609.26069.
29. [li2025smallmodelgap] Li, Y. et al. Small Models Struggle to Learn from Strong Reasoners. Findings of ACL 2025. arXiv:2502.12143.
30. [scas2026] When the Strongest Teacher Is Not the Best Teacher: Student-Centric Answer Selection. arXiv:2605.26872.
31. [dinucujianu2025pedagogicalrl] Dinucu-Jianu, D., Macina, J., Daheim, N., Hakimi, I., Gurevych, I., Sachan, M. From Problem-Solving to Teaching Problem-Solving. EMNLP 2025. doi:10.18653/v1/2025.emnlp-main.15.
32. [leakagerobust2026] Evaluating Answer Leakage Robustness of LLM Tutors against Adversarial Student Attacks. ACL 2026. arXiv:2604.18660.
33. [learnlm2024] LearnLM Team, Google. LearnLM: Improving Gemini for Learning. arXiv:2412.16429.
34. [learnlm2024responsible] Towards Responsible Development of Generative AI for Education: An Evaluation-Driven Approach. arXiv:2407.12687.
35. [learnlm2025arena] Evaluating Gemini in an Arena for Learning. arXiv:2505.24477.
36. [learnlm2025eedirct] AI Tutoring Can Safely and Effectively Support Students: An Exploratory RCT in UK Classrooms. arXiv:2512.23633.
37. [openai2025studymode] OpenAI. Introducing study mode. 29 July 2025. https://openai.com/index/chatgpt-study-mode/
38. [openai2026learningoutcomes] OpenAI. New tools for understanding AI and learning outcomes (date not verified). https://openai.com/index/understanding-ai-and-learning-outcomes/
39. [anthropic2025claudeedu] Anthropic. Introducing Claude for Education. https://www.anthropic.com/news/introducing-claude-for-education
40. [anthropic2025edureport] Anthropic. Anthropic Education Report: How University Students Use Claude. https://www.anthropic.com/news/anthropic-education-report-how-university-students-use-claude
41. [bastani2025guardrails] Bastani, H., Bastani, O., Sungu, A., Ge, H., Kabakcı, Ö., Mariman, R. Generative AI without guardrails can harm learning: Evidence from high school mathematics. PNAS 2025. doi:10.1073/pnas.2422633122.
42. [kestin2025aitutoring] Kestin, G., Miller, K., Klales, A., Milbourne, T., Ponti, G. AI tutoring outperforms in-class active learning. Scientific Reports 2025. doi:10.1038/s41598-025-97652-6.
43. [wang2024tutorcopilot] Wang, R. E., Ribeiro, A. T., Robinson, C. D., Loeb, S., Demszky, D. Tutor CoPilot. arXiv:2410.03017.
44. [desimone2025chalkboards] De Simone, M. E., Tiberti, F. H., Barron Rodriguez, M. R., Manolio, F. A., Mosuro, W., Dikoru, E. J. From Chalkboards to Chatbots: Evaluating the Impact of Generative AI on Learning Outcomes in Nigeria (subtitle end not verified). World Bank Policy Research Working Paper 11125, 2025.
45. [pardos2024chatgpthelp] Pardos, Z. A., Bhandari, S. ChatGPT-generated help produces learning gains equivalent to human tutor-authored help on mathematics skills. PLOS ONE 19(5): e0304013, 2024.
46. [kumar2025mathperil] Kumar et al. (full author list not captured). Math Education with Large Language Models: Peril or Promise? AIED 2025 (SSRN 4641653).
47. [northcutt2026studentbench] Northcutt, C., Hasmani, I., Feng, K., Khangi, T., Plesner, A., Mueller, J. StudentBench: AI and human tutoring yield equivalent GRE learning gains. arXiv:2609.28470. https://github.com/Handshake-AI-Research/studentbench
48. [seshadri2026lostinsim] Seshadri, P., Cahyawijaya, S., Odumakinde, A., Singh, S., Goldfarb-Tarrant, S. Lost in Simulation: LLM-Simulated Users are Unreliable Proxies for Human Users in Agentic Evaluations. ACL 2026. arXiv:2601.17087.
49. [zhou2026sim2real] Zhou, X. et al. Mind the Sim2Real Gap in User Simulation for Agentic Tasks. arXiv:2603.11245.
50. [shao2024cogym] Shao, Y., Samuel, V., Jiang, Y., Yang, J., Yang, D. Collaborative Gym. arXiv:2412.15701. https://github.com/SALT-NLP/collaborative-gym
51. [wu2025collabllm] Wu, S. et al. CollabLLM: From Passive Responders to Active Collaborators. ICML 2025. arXiv:2502.00640.
52. [zhou2025sweetrl] Zhou, Y. et al. SWEET-RL: Training Multi-Turn LLM Agents on Collaborative Reasoning Tasks. arXiv:2503.15478. https://github.com/facebookresearch/sweet_rl
53. [yao2024tau] Yao, S. et al. τ-bench. arXiv:2406.12045.

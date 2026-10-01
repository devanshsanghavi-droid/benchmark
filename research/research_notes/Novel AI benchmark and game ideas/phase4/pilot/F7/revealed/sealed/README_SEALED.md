# F7 Unrun Lab pilot - sealed material (owner only)

Decrypt (from the F7 folder):
    openssl enc -d -aes-256-cbc -pbkdf2 -in sealed.tar.gz.enc | tar xz      # creates ./sealed/
Score:
    python3 public/score.py --key sealed/key --answers answers --per-question --pairs

Contents
- sim_s1.py .. sim_s5.py  simulator code with hidden parameters (dict P in each file)
- config.py               experiment menus, questions, outcome specs, no-change values
- common.py, seeds.json   seed derivation (numpy SeedSequence from master_seed) and rounding
- generate_public.py      regenerates public CSV/JSON: python3 generate_public.py <public_dir>
- generate_truth.py       sealed rollouts: python3 generate_truth.py S1 key   (10k truth, 10k oracle, 10k no-change)
- baselines_public.py     naive / climatology / spam baselines from public data only
- build_key.py            key/key.json + key/truth_samples.npz + reference answer files
- validate_spam.py        mean spam skill over 20 draws
- key/                    key.json, truth_samples.npz (scorer inputs); samples_S*.npz (truth, oracle, no-change rollouts)
- validation_answers/     reference forecasters in answer format
- MECHANISMS.md           hidden mechanisms and why each question is hard

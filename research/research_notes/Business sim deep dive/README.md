# Business-simulation deep dive (Oct 2026)

Research notes behind `research/reports/Business simulation benchmark design.md`. One research agent wrote each dossier. A separate fact-checking agent then edited it in place, adding inline markers (`[corrected by fact-check: ...]`, `[uncertain: ...]`, `[fact-check flag: ...]`), and appended a "Fact-check log".

Network policy blocked many primary hosts, including arxiv, andonlabs.com, Kaggle and most publisher and government sites. Agents read code from GitHub instead. Claims seen only in search snippets are tagged [S], and that accounts for most of the "uncertain" counts below.

| Dossier | Area | Variables | Claims checked | Verified | Corrected | Uncertain | Removed |
|---|---|---|---|---|---|---|---|
| [D01](D01_andon_deployments_vendingbench.md) | Andon Labs deployments and Vending-Bench | 37 | 100 | 66 | 10 | 23 | 1 |
| [D02](D02_customer_demand.md) | Customer demand | 36 | 83 | 34 | 9 | 40 | 0 |
| [D03](D03_supply_chain_inventory.md) | Suppliers, inventory and production | 39 | 80 | 53 | 11 | 16 | 0 |
| [D04](D04_service_ops_staffing.md) | Service operations, queues and staffing | 32 | 74 | 57 | 6 | 11 | 0 |
| [D05](D05_finance_accounting.md) | Finance, accounting and cash | 32 | 62 | 30 | 14 | 17 | 1 |
| [D06](D06_humans_social_interaction.md) | Humans in the loop | 31 | 98 | 63 | 8 | 27 | 0 |
| [D07](D07_competition_multiagent.md) | Competition and multi-agent dynamics | 33 | 100 | 64 | 15 | 21 | 0 |
| [D08](D08_shocks_environment_scenarios.md) | Shocks, environment and scenarios | 36 | 99 | 56 | 9 | 34 | 0 |
| [D09](D09_legal_ethics_safety.md) | Law, ethics and conduct | 31 | 107 | 76 | 14 | 17 | 0 |
| [D10](D10_harness_engineering.md) | Agent interface and simulator engineering | 37 | 83 | 62 | 9 | 12 | 0 |
| [D11](D11_evaluation_scoring.md) | Evaluation and scoring | 30 | 90 | 62 | 11 | 17 | 0 |
| [D12](D12_calibration_data.md) | Calibration data and sim-to-real validation | 28 | 93 | 62 | 11 | 19 | 1 |
| **Total** | | **402** | **1069** | **685** | **127** | **254** | **3** |

Other files:

- `MASTER_VARIABLES_CATALOGUE.md`: the section-3 variables tables of all 12 dossiers in one file, unedited.
- `synthesis/`: the section drafts (S1-S7) used to assemble the report.

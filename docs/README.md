# Documentation map

Read in this order if you want to judge what Ripple is, what was verified and what was not.

| Read | What it settles |
|---|---|
| [`../README.md`](../README.md) | what Ripple is, how to try it, supported scope, limits, setup and tests |
| [`judges/START_HERE.md`](judges/START_HERE.md) | the judge guide (Markdown source of the static pages in `../site/judges/`) |
| [`release/CLAIMS_EVIDENCE_LIMITS.md`](release/CLAIMS_EVIDENCE_LIMITS.md) | every claim, its evidence, its limit and what is **not** claimed; open defects and known limits |
| [`release/SCENARIO_STATUS.md`](release/SCENARIO_STATUS.md) | both scenarios stage by stage: which run backs which stage |
| [`evaluation/HELD_OUT_EVALUATION.md`](evaluation/HELD_OUT_EVALUATION.md) | the held-out AI-quality evaluation (targets not met), with data, method and disclosures |
| [`pitch/README.md`](pitch/README.md) | the first live run (2026-10-05): chain of jobs, costs, screenshots |
| [`release/PACKAGE_PROVENANCE.md`](release/PACKAGE_PROVENANCE.md) | how this repository was produced, what differs from the serving image, test results by snapshot |

Architecture and reference: [`decisions/`](decisions) (architecture decision records), [`contracts/`](contracts) (API, storage, lifecycle and budget contracts), [`domain/`](domain) (glossary, state machines, events, semantics), [`product/`](product) (support matrix, boundaries), [`evaluation/`](evaluation) (metric definitions and thresholds), [`runbooks/`](runbooks) (budget and sandbox configuration templates), [`verification/`](verification) (cloud readiness and two design decisions with evidence). Third-party notices: [`../THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md).

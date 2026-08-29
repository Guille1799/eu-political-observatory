# Documentation

**A note on language.** The README and the code comments are in English; these documents are in
Spanish. That is deliberate rather than an oversight: they are working documents about Spanish
electoral geography, written while the decisions were being made, and translating them after the
fact would quietly smooth over the hesitations and the corrections — which is most of what makes
them worth keeping. This page tells you what is in each one, so you can decide what to open.

---

## Start here

| Document | What it is |
|---|---|
| [`decisiones/LINEA_ACTUAL.md`](decisiones/LINEA_ACTUAL.md) | **One page: what this repository is about right now**, and why that is written down instead of merely understood. Read this first if you read nothing else. |

## The current line of work (v2)

| Document | What it is |
|---|---|
| [`v2_alcance.md`](v2_alcance.md) | The full design document: the question, the ladder of spatial scales, the sources, and — at length — what the project explicitly refuses to claim. **These are working notes, not a polished paper:** corrections are marked in place rather than rewritten away, so you can see where the design changed its mind and why. ~1,400 lines. |
| [`v2_trabajo_previo.md`](v2_trabajo_previo.md) | Prior-work review, done by opening the sources rather than reading *about* them: what already exists, what is reusable, and one avenue discarded on the evidence. |

## The retired cross-country design (v1)

| Document | What it is |
|---|---|
| [`decisiones/EFA_RETIRADO_2026-08-21.md`](decisiones/EFA_RETIRADO_2026-08-21.md) | Why the ESS factor-analytic layer was **frozen rather than finished** — and why the unresolved Heywood case is stated as unresolved instead of being worked around. |
| [`v2_alcance.md`](v2_alcance.md) §11 | Why the European design was retired after being executed. The short version is in the root [`README`](../README.md); this is the evidence behind it. |

## Elsewhere in the repository

| Where | What |
|---|---|
| [`../R/README.md`](../R/README.md) | The statistical layer — missing-data handling, multiple imputation, and the measurement model that is *not* settled. In English. |
| [`../src/ingestion/parameters.py`](../src/ingestion/parameters.py) | Worth a look even if you skip the rest: a single methodological cut-off documented with its provenance, including an explicit admission that it has no citation behind it. |

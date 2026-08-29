# eu-political-observatory

**Reproducible, provenance-preserving pipelines for studying territorial politics — built so that
every number can be traced back to its source, and so that the measurement decisions are visible
rather than assumed.**

---

## The question

**Where has the vote for Vox *grown* in Spain between elections — and does the answer change with
the level of territorial aggregation you use?**

The second half is the point, not a robustness check appended to the end.

The same data can tell one story aggregated by census tract and a different one aggregated by
municipality. That is the *modifiable areal unit problem*, and it is old news in geography — but
most published work on territorial voting still picks one level, usually the level that happened to
be available, and never checks whether the conclusion survives changing it. This project checks it
across four real levels: **census tract → municipality → province → autonomous community.**

The framing is deliberately narrow, and each narrowing buys something specific:

- **A single, stable party.** No classification step, and therefore no classification error — which
  matters here more than usual, for reasons the next section gets into.
- **Change, not levels.** Comparing a place with itself over time differences away everything about
  that place that does not change. "Growth" is a change; you cannot measure it from one snapshot.

Alongside it: a map that **refuses to paint** where the evidence does not support an estimate, and
says why it is refusing.

**Nearest prior work:** Roig, Espinosa & Pavía (2025), *Frontiers in Political Science*. Same two
sources, and they conclude that Vox's early expansion was led by middle- and upper-income voters
rather than "modernisation losers". They justify their choice of spatial unit by that unit's
internal homogeneity — and never test how sensitive the result is to the choice. That untested step
is the gap this project occupies. The aim is not to contradict them; it is to find out whether their
answer holds when the unit moves.

Full design: [`docs/v2_alcance.md`](docs/v2_alcance.md) · Start at [`docs/`](docs/README.md).

## How it got here

This repository began as something else, and it is worth saying what, because the reason it changed
is a result in its own right.

The original design was **cross-country**: European regional election results (EU-NED) joined to
regional economics (ARDECO), with parties classified by academic expert surveys (POPPA, PopuList),
plus ESS survey microdata. It was **built and executed**. It did not survive contact with its own
sources, and three findings — each verified against the actual files, not assumed — are why:

1. **The European election dataset does not go below NUTS2.** The fine spatial scale the whole
   design rested on did not exist in it.
2. **In Spain, 22.9% of the vote had no party verdict** from the standard classifications — and it
   was precisely the non-statewide parties. Coverage was worst exactly where the object of study
   was.
3. **The shared party identifier does not point to the same party across sources.** Verified by
   hand, producing a false positive and a false negative at once.

So the object was redefined from "an ideological label an expert assigns" to "a single party, named
by the ballot papers it appears on", and the geography from all of Europe to one country that
publishes results down to the polling station and has done since 1977.

**The sources died, not the question.** Both designs ask whether territorial economic conditions
explain a vote, and both care about the scale at which you look. The second one can actually be
answered with data that exists.

> The v1 code is still here. It is the evidence for the three findings above, and it carries a
> `[HISTORICO - v1]` banner at the top of each file. It is not on the path of the current work, and
> nothing should be built on it without first reading why it stopped.

## What is in here

| | |
|---|---|
| [`src/v2/`](src/v2/) | The current line. Fixed-width parsing of the official election files, the TLS chain of trust, census-tract survival across redistricting, the Vox catalogue. |
| [`src/`](src/), [`src/ingestion/`](src/ingestion/) | v1, retired. Kept as evidence; see the banners. |
| [`R/`](R/README.md) | Missing-data handling and the measurement model — Little's MCAR test, multiple imputation (m = 20), factor analysis. **Frozen**, and honestly so: see below. |
| [`docs/`](docs/README.md) | Design documents and the decision record. Spanish; the index page explains what each one is. |
| [`notebooks/`](notebooks/) | Exploration. |

One file worth opening even if you skip the rest:
[`src/ingestion/parameters.py`](src/ingestion/parameters.py). It documents a single methodological
cut-off with its provenance — including an explicit written admission that the value has no citation
behind it, only a project convention, and what was done to reduce the dependence on it.

## Run it

The source data is not in the repository and cannot be: the ESS microdata is access-controlled, and
the Spanish election files are fetched from the official source at run time. What *does* run from a
clean clone is the test suite.

```bash
python -m venv venv
venv\Scripts\activate           # Windows
# source venv/bin/activate      # macOS / Linux
pip install -r requirements.txt
python -m pytest src -q
```

Measured on a clean checkout on **2026-08-29** with Python 3.14: **61 passed, 20 skipped.**

The skips are deliberate. Those tests need the official election files, and rather than failing with
a stack trace, each one names the command that fetches what it is missing:

```
SKIPPED src/v2/test_layout_infoelectoral.py:210: falta data/external/infoelectoral/02201911_MESA.zip
        -- bajalo con: python src/v2/descarga_infoelectoral.py 2019 11
```

Download the files those messages name and the same command runs **81 passed, 0 skipped**.

`requirements.txt` declares what this code imports — not a `pip freeze` of one machine.

The R layer has its own data requirement and is documented separately in
[`R/README.md`](R/README.md). It needs `misty`, `mice`, `psych`, `GPArotation`, `PKLMtest` and
`readr` from CRAN. There is no `renv.lock` yet, so those versions are **not** pinned.

## Where it stands

**Working:**

- Parsing the official fixed-width election layout, verified **byte by byte against the
  specification** across all five general elections in the window — which is how the pipeline found
  a sentence in the official spec that is simply not true of the files it describes.
- **Downloading from the official source with TLS verification fully on.** Python could not connect
  where the browser could. The easy reading — "the Spanish CA is not in Python's trust store" — was
  checked and is **false**: `certifi` does carry the FNMT roots. The server sends an incomplete
  chain, omitting an intermediate; browsers hide this by fetching the missing link themselves via
  the certificate's AIA extension, and OpenSSL does not. The fix supplies the intermediate. Turning
  verification off would have been one line, and would have quietly voided the provenance this
  project exists to preserve — so there is a test that reads the module's syntax tree and fails if
  `verify=False`, `CERT_NONE` or `check_hostname=False` ever appear in it.
- Measuring how many census tracts survive between elections, **including the ones that survive only
  in name** — a tract that keeps its code after absorbing its neighbour is not the same tract, and
  counting it as one would have silently biased the whole design.

**Not done, and not claimed:**

- **There is no published estimate yet.** The plumbing is built and tested; the analysis it exists
  to support has not been run.
- **The ESS measurement model is frozen, not finished.** An exploratory factor analysis returned an
  improper solution — a Heywood case — so the model is not settled, and it is reported as unsettled
  rather than worked around. The current line does not depend on it.
  ([`R/README.md`](R/README.md) · [`docs/decisiones/`](docs/decisiones/EFA_RETIRADO_2026-08-21.md))
- The repository ships no data, and it is not a dashboard. A panel where dozens of variables can be
  crossed on demand is a machine for producing spurious correlations, and that is a deliberate
  omission rather than a missing feature.

## Stack

Python for ingestion and analysis, loading into PostgreSQL · R for imputation and factor analysis ·
pytest throughout. Sources: Ministerio del Interior (Infoelectoral), INE (household income atlas),
and — for the retired cross-country layer — ARDECO, EU-NED, ParlGov, ESS.

## License

MIT — see [`LICENSE`](LICENSE).

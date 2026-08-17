# eu-political-observatory

**Reproducible, provenance-preserving pipelines for studying territorial politics — built so that
every number can be traced back to its source, and so that the measurement decisions are visible
rather than assumed.**

> 👉 **The current line of work is sub-national and Spanish**, and it asks whether the answer changes
> with the scale you measure at. See **[Status](#status)** — the earlier cross-country design was
> executed, found not viable with its sources, and retired. That is documented, not hidden.

## What the cross-country layer does *(built first; see Status for why it is not the current line)*

- **Integrates independent sources** — regional economics (**ARDECO**), national election results
  (**EU-NED**), party & government data (**ParlGov**), and **ESS** survey microdata — reconciling
  entity IDs across them with crosswalk tables, so the same region/party maps correctly and **every
  record keeps its provenance** through the integration.
- **Handles missing data honestly** — Little's **MCAR** test + **multiple imputation (m = 20)**,
  rather than dropping rows or naively filling them.
- **Builds toward cross-country-comparable measures** — a factor-analytic measurement model with
  **measurement-invariance** testing, so comparisons between countries are defensible rather than
  assumed. ⚠️ **Not there yet, and the reason is documented:** an exploratory EFA returned an
  improper solution (a **Heywood case**), so the measurement model is *not* settled. See
  [`R/README.md`](R/README.md) for what that means and what it blocks.

## Why

Economic, electoral, party-level and attitudinal signals usually live in incompatible silos. Linking
them into one traceable dataset lets analysts ask cross-country questions without re-stitching the
data every time — and without losing track of where each number came from.

## Status

**Active work in progress, and the current line is a Spanish sub-national one.**

### Current line: does the answer change with the scale you measure at?

**Question:** where has the vote for **Vox** *grown* in Spain between elections — and **does the answer
change with the level of territorial aggregation you use?**

The framing is deliberately narrow. A **single, stable party** removes the classification problem that
sank the previous design entirely, and makes it possible to model **change** rather than levels: comparing
a place with itself over time differences away everything about that place that does not change. A
recent study using **the same two sources** concludes that Vox's early expansion was led by middle- and
upper-income voters rather than "modernisation losers" — and justifies its choice of spatial unit by the
internal homogeneity of that unit, **without ever testing how sensitive the result is to that choice**.
That is the gap this line addresses.

The second half is the point. The same data can tell one story aggregated by municipality and a
different one by province — the *modifiable areal unit problem*. Most published work on territorial
voting picks one level, usually because it is the level that happens to be available, and never checks
whether the conclusion survives changing it. This line checks it across **four real levels**: polling
station → municipality → province → autonomous community.

Alongside it: a map that **refuses to paint** where the evidence does not support an estimate, and
says why. Scope and open questions: [`docs/v2_alcance.md`](docs/v2_alcance.md) (Spanish).

### What the previous, cross-country design taught — and why it was retired

An earlier design combined European regional election results, regional economics and academic party
classifications. **It was executed, and it was not viable with those sources.** Three findings, all
verified against the actual files:

1. the European election dataset **does not go below NUTS2** — the fine scale the design assumed did
   not exist in it;
2. in Spain **22.9% of the vote had no party verdict** from the standard classifications, and it was
   precisely the non-statewide parties: **coverage was worst exactly where the object of study was**;
3. the shared party identifier **does not point to the same party across sources** — verified by hand,
   producing a false positive and a false negative at once.

The sources died, not the question. The current line replaces all three: official Ministry of the
Interior results (published down to polling-station level since 1977), and an object defined by
**where a party stands for election** rather than by an interpretive ideological label.

> The v1 code is kept because it is the evidence for the above, but it is **not** on the path of the
> current line.

### Blocked / paused

- 🔴 **Downloading the official Spanish election source from code is blocked.** Its certificate is
  genuine but issued by **FNMT-RCM**, the Spanish public-administration CA, which is not in the
  Mozilla root program and therefore not in Python's or `certifi`'s trust stores. The fix is to add
  that root — **not** to disable TLS verification, which would void the provenance the pipeline
  exists to preserve.
- ⏸️ **The ESS measurement model is paused, not cancelled.** It remains blocked on an improper EFA
  solution (Heywood case) ([`R/README.md`](R/README.md)). The current line does not depend on it.

## Stack

Python (ingestion → PostgreSQL) · R (imputation, factor analysis, invariance) · reproducible pipeline structure.

> **Note:** source data is access-controlled (e.g. ESS microdata) and not committed; the pipeline is
> built to reproduce results from the raw sources.

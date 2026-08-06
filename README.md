# eu-political-observatory

**A reproducible pipeline that integrates independent European political-economic data sources
into one traceable dataset — to study the rise of nationalist and populist politics across Europe.**

## What it does

- **Integrates independent sources** — regional economics (**ARDECO**), national election results
  (**EU-NED**), party & government data (**ParlGov**), and **ESS** survey microdata — reconciling
  entity IDs across them with crosswalk tables, so the same region/party maps correctly and **every
  record keeps its provenance** through the integration.
- **Handles missing data honestly** — Little's **MCAR** test + **multiple imputation (m = 20)**,
  rather than dropping rows or naively filling them.
- **Builds toward cross-country-comparable measures** — a factor-analytic measurement model with
  **measurement-invariance** testing, so comparisons between countries are defensible rather than
  assumed.

## Why

Economic, electoral, party-level and attitudinal signals usually live in incompatible silos. Linking
them into one traceable dataset lets analysts ask cross-country questions without re-stitching the
data every time — and without losing track of where each number came from.

## Status

**Active work in progress.** The data-integration and missing-data foundation is in place; the
measurement model and cross-country invariance are being finalised. Next on the roadmap: a thin,
provenance-aware legibility layer on top of the validated indices.

## Stack

Python (ingestion → PostgreSQL) · R (imputation, factor analysis, invariance) · reproducible pipeline structure.

> **Note:** source data is access-controlled (e.g. ESS microdata) and not committed; the pipeline is
> built to reproduce results from the raw sources.

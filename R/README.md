# R — missing-data handling and measurement model

The statistical layer of the pipeline. These scripts run on **ESS microdata**, which is
access-controlled and therefore not committed: download it from
[europeansocialsurvey.org](https://www.europeansocialsurvey.org/) and point the scripts at your
local copy. The code is here so the *method* can be inspected and reproduced, even when the data
cannot be redistributed.

| Script | What it does |
|---|---|
| `ess_spain/spain_mcar_robust.R` | Tests whether the missingness is MCAR — Little's (1988) test via `misty::na.test()`, run in blocks, plus complementary diagnostics. Missingness is characterised before anything is imputed. |
| `ess_spain/spain_mice_imputation.R` | Multiple imputation with `mice` + predictive mean matching: **m = 20, maxit = 10, seed = 42**. Twenty completed datasets, not one — so the uncertainty introduced by imputation survives into the estimates instead of being hidden. |
| `ess_spain/spain_efa.R` | Exploratory factor analysis over the imputed matrices, toward a comparable measure. |

## Running them

`R/ess_spain/` is the canonical tree — the versioned scripts here are the ones to run and edit:

```
Rscript R/ess_spain/spain_mcar_robust.R
Rscript R/ess_spain/spain_mice_imputation.R
Rscript R/ess_spain/spain_efa.R
```

Run them in that order. Each script locates its data from **its own path on disk**, not from the
working directory: it walks up two levels to the repository root and reads and writes under
`data/processed/ess/spain/`, which is git-ignored because the microdata cannot be redistributed.
So the invocation above works from anywhere, and a checkout without that directory (a bare clone,
a git worktree) stops immediately with a message naming the path it expected.

Nothing here writes to `data/raw/` — the raw ESS `.sav` files are read-only.

**Status, honestly:** an earlier exploratory EFA returned an improper solution (a Heywood case),
so the measurement model is *not* settled. Pooled estimation and measurement-invariance testing
across countries are the next layer — not a finished claim.

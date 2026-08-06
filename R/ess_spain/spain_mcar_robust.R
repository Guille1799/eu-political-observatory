#!/usr/bin/env Rscript
# =============================================================================
# spain_mcar_robust.R — Batería completa de tests MCAR para España (ESS core)
#
# Tests ejecutados:
#   1. Little (1988) en 2 bloques <=30 variables — misty::na.test()
#      Bloques pre-especificados alfabéticamente (sin mirar resultados antes).
#      Usa mvnmle internamente — más robusto que naniar/prelim.norm.
#   2. Jamshidian & Jalal (2010) — misty::na.test(..., print="jamjal")
#      No asume normalidad multivariante. Adecuado para ordinales/Likert.
#   3. PKLM (Spohn et al., 2025, Psychometrika) — PKLMtest::PKLMtest()
#      Totalmente no paramétrico, válido para datos discretos, altas
#      dimensiones, y cualquier tamaño muestral. Incluye p-valores parciales
#      por variable para identificar qué variables violan MCAR.
#
# Inputs:
#   Little + JJ  → spain_core_mcar_patterns_min30.csv  (patrones con n>=30)
#   PKLM         → spain_core_data.csv                 (dataset completo)
#
# Uso (desde la raíz del repo):
#   Rscript data/processed/ess/spain/spain_mcar_robust.R
#
# Requisitos:
#   install.packages(c("readr", "misty", "PKLMtest"))
#
# Referencias:
#   Little (1988) JASA 83:1198-1202
#   Jamshidian & Jalal (2010) Psychometrika
#   Spohn et al. (2025) Psychometrika — PKLM
#   Enders (2010) Applied Missing Data Analysis
# =============================================================================

suppressPackageStartupMessages({
  library(readr)
  library(misty)
  library(PKLMtest)
})

# --- Localizar raíz del repo -------------------------------------------------
args      <- commandArgs(trailingOnly = FALSE)
file_arg  <- grep("^--file=", args, value = TRUE)
if (length(file_arg) != 1L) {
  stop(
    "Ejecuta desde la raíz del repo:\n",
    "  Rscript data/processed/ess/spain/spain_mcar_robust.R"
  )
}
this_script <- normalizePath(sub("^--file=", "", file_arg), winslash = "/")
spain_dir   <- dirname(this_script)
ess_dir     <- normalizePath(file.path(spain_dir, ".."), winslash = "/")
repo_root   <- normalizePath(
  file.path(spain_dir, "..", "..", "..", ".."), winslash = "/"
)

cat("=================================================================\n")
cat("MCAR TEST BATTERY — ESS Spain core (45 variables)\n")
cat("Repo:", repo_root, "\n")
cat("=================================================================\n\n")

# --- Cargar datos ------------------------------------------------------------

# Para Little + JJ: patrones filtrados (n>=30 por patrón)
path_patterns <- file.path(spain_dir, "spain_core_mcar_patterns_min30.csv")
if (!file.exists(path_patterns)) stop("No existe: ", path_patterns)

df_pat <- read_csv(path_patterns, show_col_types = FALSE, na = c("", "NA"))
names(df_pat) <- sub("^\ufeff", "", names(df_pat))
df_pat <- as.data.frame(lapply(df_pat, function(x) {
  suppressWarnings(as.numeric(as.character(x)))
}))
df_pat <- df_pat[, vapply(df_pat, function(x) any(!is.na(x)), logical(1))]

# Para PKLM: dataset completo con NAs reales
path_core <- file.path(spain_dir, "spain_core_data.csv")
if (!file.exists(path_core)) stop("No existe: ", path_core)

df_core <- read_csv(path_core, show_col_types = FALSE, na = c("", "NA"))
names(df_core) <- sub("^\ufeff", "", names(df_core))
df_core <- as.data.frame(lapply(df_core, function(x) {
  suppressWarnings(as.numeric(as.character(x)))
}))
df_core <- df_core[, vapply(df_core, function(x) any(!is.na(x)), logical(1))]

cat("Patrones (min30):", nrow(df_pat), "filas x", ncol(df_pat), "variables\n")
cat("Dataset completo:", nrow(df_core), "filas x", ncol(df_core), "variables\n\n")

# --- Bloques pre-especificados (alfabético, sin mirar resultados) -------------
vars_sorted <- sort(names(df_pat))
n_vars      <- length(vars_sorted)
mid         <- ceiling(n_vars / 2)
block_a     <- vars_sorted[seq_len(mid)]
block_b     <- vars_sorted[(mid + 1):n_vars]

cat("Bloque A (n=", length(block_a), "): ", paste(block_a, collapse=", "), "\n\n", sep="")
cat("Bloque B (n=", length(block_b), "): ", paste(block_b, collapse=", "), "\n\n", sep="")

# =============================================================================
# TEST 1 — Little (misty) en 2 bloques
# =============================================================================
cat("=================================================================\n")
cat("TEST 1: Little (1988) — misty::na.test() en 2 bloques\n")
cat("  Hipotesis nula: datos MCAR\n")
cat("  p < 0.05 -> rechazar MCAR\n")
cat("=================================================================\n\n")

cat("--- Bloque A (", length(block_a), "vars) ---\n", sep="")
res_little_a <- na.test(df_pat[, block_a], print = "little", output = TRUE)

cat("\n--- Bloque B (", length(block_b), "vars) ---\n", sep="")
res_little_b <- na.test(df_pat[, block_b], print = "little", output = TRUE)

# =============================================================================
# TEST 2 — Jamshidian & Jalal (misty)
# =============================================================================
cat("\n=================================================================\n")
cat("TEST 2: Jamshidian & Jalal (2010) — misty::na.test() metodo JJ\n")
cat("  No asume normalidad multivariante — adecuado para ordinales\n")
cat("  p < 0.05 -> rechazar MCAR\n")
cat("=================================================================\n\n")

cat("Nota: puede tardar unos minutos con 45 variables...\n\n")
res_jj <- na.test(df_pat, print = "jamjal", method = "npar",
                  m = 20, seed = 42, output = TRUE)

# =============================================================================
# TEST 3 — PKLM (Spohn et al. 2025)
# =============================================================================
cat("\n=================================================================\n")
cat("TEST 3: PKLM (Spohn et al., 2025) — PKLMtest::PKLMtest()\n")
cat("  Totalmente no parametrico, valido para ordinales\n")
cat("  Incluye p-valores parciales por variable\n")
cat("  p < 0.05 -> rechazar MCAR\n")
cat("=================================================================\n\n")

cat("Nota: puede tardar varios minutos (Random Forest + permutaciones)...\n\n")

set.seed(42)
X_matrix <- as.matrix(df_core)

pklm_result <- PKLMtest(
  X                     = X_matrix,
  num.proj              = 300,
  num.trees.per.proj    = 10,
  nrep                  = 500,
  compute.partial.pvals = TRUE
)

cat("PKLM p-valor global:", pklm_result[1], "\n\n")

# P-valores parciales por variable
if (length(pklm_result) > 1) {
  partial_pvals <- pklm_result[-1]
  names(partial_pvals) <- names(df_core)[seq_along(partial_pvals)]

  partial_df <- data.frame(
    variable = names(partial_pvals),
    pval     = round(as.numeric(partial_pvals), 4)
  )
  partial_df <- partial_df[order(partial_df$pval), ]

  cat("P-valores parciales por variable (ordenados de menor a mayor):\n")
  cat("  Variables con p<0.05 son las que mas contribuyen a violar MCAR\n\n")
  print(partial_df, row.names = FALSE)
}

# =============================================================================
# RESUMEN FINAL
# =============================================================================
cat("\n=================================================================\n")
cat("RESUMEN\n")
cat("=================================================================\n")
cat("Little Bloque A:       ver output arriba\n")
cat("Little Bloque B:       ver output arriba\n")
cat("Jamshidian & Jalal:    ver output arriba\n")
cat("PKLM global p-valor:  ", pklm_result[1], "\n")
cat("\nInterpretacion:\n")
cat("  Si los 3 tests rechazan MCAR (p<0.05) -> MAR confirmado\n")
cat("  Variables con PKLM parcial p<0.05 -> correlatos del missing\n")
cat("  Esto valida el uso de MICE/IterativeImputer\n")
cat("=================================================================\n")

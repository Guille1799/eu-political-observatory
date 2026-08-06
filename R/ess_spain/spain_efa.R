#!/usr/bin/env Rscript
# =============================================================================
# spain_efa.R — EFA con correlaciones policoricas sobre 20 imputaciones
#
# Metodo:
#   fa.pooled (psych) — factoriza cada uno de los 20 datasets mice por
#   separado y rota cada solucion hacia la primera (consensus rotation).
#   Usa correlaciones policoricas como input (adecuado para ordinales Likert).
#   Extraccion: ULS (Unweighted Least Squares) — robusto a no-normalidad.
#   Rotacion: oblimin — permite correlacion entre factores (mas realista
#   con actitudes politicas).
#
# Variables excluidas pre-EFA (documentado en notebook):
#   dscroth, dscrrlg, dscrgnd  (KMO < 0.50)
#   imdfetn                    (r > 0.85 con impcntr e imsmetn)
#   imsmetn                    (invarianza cross-cultural debil, Nickel 2024)
#
# Inputs:
#   spain_core_imputed_m01.csv ... spain_core_imputed_m20.csv
#
# Outputs:
#   spain_efa_loadings.csv      — cargas factoriales (patron)
#   spain_efa_communalities.csv — comunalidades
#   spain_efa_summary.txt       — resumen completo
#
# Uso (desde la raiz del repo):
#   Rscript data/processed/ess/spain/spain_efa.R
#
# Requisitos:
#   install.packages(c("psych", "readr", "GPArotation"))
#
# Referencias:
#   Revelle (2024) psych package; fa.pooled documentation
#   Lorenzo-Seva & van Ginkel (2016) consensus rotation
#   Nickel et al. (2024) MDA — imsmetn invarianza
#   Watkins (2018) Journal of Black Psychology — pre-EFA checks
# =============================================================================

suppressPackageStartupMessages({
  library(psych)
  library(readr)
  library(GPArotation)
})

# --- Localizar directorio ----------------------------------------------------
args     <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) != 1L) {
  stop("Ejecuta: Rscript data/processed/ess/spain/spain_efa.R")
}
this_script <- normalizePath(sub("^--file=", "", file_arg), winslash = "/")
spain_dir   <- dirname(this_script)

cat("=================================================================\n")
cat("EFA con correlaciones policoricas — ESS Spain core (40 variables)\n")
cat("Directorio:", spain_dir, "\n")
cat("=================================================================\n\n")

# --- Variables excluidas pre-EFA ---------------------------------------------
VARS_EXCLUIDAS <- c("dscroth", "dscrrlg", "dscrgnd", "imdfetn", "imsmetn")

# --- Cargar los 20 datasets imputados ----------------------------------------
cat("Cargando 20 datasets imputados...\n")
datasets <- list()

for (i in seq_len(20)) {
  path_m <- file.path(spain_dir, sprintf("spain_core_imputed_m%02d.csv", i))
  if (!file.exists(path_m)) stop("No existe: ", path_m)
  df_m <- as.data.frame(read_csv(path_m, show_col_types = FALSE))
  # Eliminar variables excluidas pre-EFA
  df_m <- df_m[, !names(df_m) %in% VARS_EXCLUIDAS]
  datasets[[i]] <- df_m
}

n_vars <- ncol(datasets[[1]])
var_names <- names(datasets[[1]])

cat("Variables por dataset:", n_vars, "\n")
cat("Filas por dataset:", nrow(datasets[[1]]), "\n\n")

# --- Variables por tipo de escala -------------------------------------------
# Escalas 0-10 (11 categorias): policoricas no necesarias, usar Pearson
# Escalas 1-4 o 1-5: policoricas apropiadas
# mixedCor calcula policoricas para <=8 categorias y Pearson para >8

VARS_ESCALA_0_10 <- c(
  "ppltrst", "pplfair", "pplhlp",
  "stfeco", "stfedu", "stfgov", "stfdem", "stfhlth", "stflife",
  "trstprl", "trstlgl", "trstplc", "trstplt", "trstep", "trstun",
  "imbgeco", "imwbcnt", "imueclt", "impcntr",
  "happy"
)

get_mixed_cor <- function(df) {
  vars_present <- names(df)
  # Variables continuas (0-10) presentes en este dataset
  cont_vars <- intersect(VARS_ESCALA_0_10, vars_present)
  poly_vars <- setdiff(vars_present, cont_vars)
  
  # Indices de columnas
  c_idx <- which(vars_present %in% cont_vars)
  p_idx <- which(vars_present %in% poly_vars)
  
  cat("  Variables policoricas (<=8 cats):", length(p_idx), "\n")
  cat("  Variables Pearson (0-10):", length(c_idx), "\n")
  
  result <- mixedCor(
    data   = df,
    c      = c_idx,
    p      = p_idx,
    use    = "pairwise.complete.obs",
    correct = 0
  )
  return(result$rho)
}

# --- Parallel Analysis sobre matriz mixta -----------------------------------
cat("=================================================================\n")
cat("PARALLEL ANALYSIS para determinar numero de factores\n")
cat("(correlaciones mixtas: policoricas + Pearson segun escala)\n")
cat("=================================================================\n\n")

cat("Calculando matriz de correlaciones mixtas (m01)...\n")
R_mixed <- get_mixed_cor(datasets[[1]])

set.seed(42)
pa_result <- fa.parallel(
  R_mixed,
  n.obs     = nrow(datasets[[1]]),
  fm        = "uls",
  fa        = "fa",
  n.iter    = 100,
  show.legend = FALSE,
  main      = "Parallel Analysis - Spain ESS core"
)

n_factors_pa <- pa_result$nfact
cat("\nNumero de factores sugerido por Parallel Analysis:", n_factors_pa, "\n\n")

# --- EFA con fa.pooled usando matrices mixtas --------------------------------
cat("=================================================================\n")
cat("EFA con fa.pooled — ULS + oblimin + correlaciones mixtas\n")
cat("Numero de factores:", n_factors_pa, "\n")
cat("=================================================================\n\n")

cat("Calculando matrices de correlaciones para los 20 datasets...\n")
cor_list <- lapply(seq_along(datasets), function(i) {
  cat(" m", sprintf("%02d", i), "\n", sep="")
  get_mixed_cor(datasets[[i]])
})

cat("\nEjecutando fa.pooled...\n\n")
set.seed(42)
efa_result <- fa.pooled(
  cor_list,
  nfactors = n_factors_pa,
  n.obs    = nrow(datasets[[1]]),
  fm       = "uls",
  rotate   = "oblimin"
)

# --- Extraer y guardar resultados --------------------------------------------

# Cargas factoriales (patron)
loadings_mat <- as.data.frame(
  unclass(efa_result$loadings)
)
loadings_mat$variable    <- var_names
loadings_mat$communality <- efa_result$communalities

# Reordenar columnas
factor_cols <- setdiff(names(loadings_mat), c("variable", "communality"))
loadings_mat <- loadings_mat[, c("variable", factor_cols, "communality")]

path_loadings <- file.path(spain_dir, "spain_efa_loadings.csv")
write_csv(loadings_mat, path_loadings)
cat("Guardado:", path_loadings, "\n")

# Comunalidades
comm_df <- data.frame(
  variable    = var_names,
  communality = round(efa_result$communalities, 4)
)
comm_df <- comm_df[order(comm_df$communality, decreasing = TRUE), ]
path_comm <- file.path(spain_dir, "spain_efa_communalities.csv")
write_csv(comm_df, path_comm)
cat("Guardado:", path_comm, "\n\n")

# --- Resumen en consola ------------------------------------------------------
cat("=================================================================\n")
cat("RESUMEN EFA\n")
cat("=================================================================\n\n")

cat("Varianza explicada por factor:\n")
print(round(efa_result$Vaccounted, 3))

cat("\n\nCargas factoriales (|loading| >= 0.32 en negrita):\n")
print(loadings_mat[, c("variable", factor_cols)], digits = 3)

cat("\nComunalidades (ordenadas):\n")
print(comm_df, row.names = FALSE)

# Variables con comunalidad baja (< 0.30)
low_comm <- comm_df[comm_df$communality < 0.30, ]
cat(sprintf("\nVariables con comunalidad < 0.30: %d\n", nrow(low_comm)))
if (nrow(low_comm) > 0) {
  print(low_comm, row.names = FALSE)
  cat("  -> Considerar eliminar estas variables y repetir EFA\n")
}

# Guardar resumen completo
path_summary <- file.path(spain_dir, "spain_efa_summary.txt")
sink(path_summary)
cat("EFA Spain ESS core — ULS + oblimin + policoricas\n")
cat("Variables:", n_vars, "| Factores:", n_factors_pa, "\n\n")
cat("Varianza explicada:\n")
print(round(efa_result$Vaccounted, 3))
cat("\n\nCargas factoriales:\n")
print(loadings_mat, digits = 3)
cat("\n\nComunalidades:\n")
print(comm_df, row.names = FALSE)
sink()
cat("Guardado:", path_summary, "\n")

cat("\n=================================================================\n")
cat("EFA completada.\n")
cat("=================================================================\n")

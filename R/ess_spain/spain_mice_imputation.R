#!/usr/bin/env Rscript
# =============================================================================
# spain_mice_imputation.R — Imputacion multiple ESS Spain core (45 variables)
#
# Metodo: mice + PMM (Predictive Mean Matching), m = 20, maxit = 10, seed = 42.
# PMM imputa solo valores observados en cada variable (adecuado para Likert).
#
# Inputs:
#   spain_core_data.csv  (con NA reales)
#
# Outputs:
#   spain_core_imputed_m01.csv ... spain_core_imputed_m20.csv
#   spain_core_imputed_pooled.csv  — modo de las 20 imputaciones en celdas NA
#   spain_core_imputed.csv         — alias de pooled (compatibilidad / EFA)
#
# Uso (desde la raiz del repo):
#   Rscript R/ess_spain/spain_mice_imputation.R
#
#   El script es el arbol canonico (versionado). Los datos viven fuera del
#   control de versiones, en data/processed/ess/spain/, y se localizan a
#   partir de la ubicacion del propio script (no del directorio de trabajo).
#
# Requisitos:
#   install.packages(c("readr", "mice"))
# =============================================================================

suppressPackageStartupMessages({
  library(readr)
  library(mice)
})

M_IMPUTATIONS <- 20L
MAXIT         <- 10L
SEED          <- 42L

get_mode <- function(x) {
  x <- x[!is.na(x)]
  if (!length(x)) {
    return(NA_real_)
  }
  ux <- unique(x)
  ux[which.max(tabulate(match(x, ux)))]
}

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) != 1L) {
  stop(
    "Ejecuta desde la raiz del repo:\n",
    "  Rscript R/ess_spain/spain_mice_imputation.R"
  )
}

# El script vive en <repo>/R/ess_spain/; los datos en
# <repo>/data/processed/ess/spain/ (ignorado por git).
this_script <- normalizePath(sub("^--file=", "", file_arg), winslash = "/")
script_dir  <- dirname(this_script)
repo_root   <- normalizePath(file.path(script_dir, "..", ".."), winslash = "/")
spain_dir   <- file.path(repo_root, "data", "processed", "ess", "spain")
if (!dir.exists(spain_dir)) {
  stop("No existe el directorio de datos: ", spain_dir)
}
path_in     <- file.path(spain_dir, "spain_core_data.csv")
path_pooled <- file.path(spain_dir, "spain_core_imputed_pooled.csv")
path_efa    <- file.path(spain_dir, "spain_core_imputed.csv")

cat("=================================================================\n")
cat("MICE imputation — ESS Spain core\n")
cat("Directorio:", spain_dir, "\n")
cat("m =", M_IMPUTATIONS, "| maxit =", MAXIT, "| method = PMM\n")
cat("=================================================================\n\n")

if (!file.exists(path_in)) {
  stop("No existe: ", path_in)
}

df <- read_csv(path_in, show_col_types = FALSE, na = c("", "NA"))
names(df) <- sub("^\ufeff", "", names(df))
df <- as.data.frame(lapply(df, function(x) suppressWarnings(as.numeric(x))))

n_rows <- nrow(df)
n_vars <- ncol(df)
n_miss <- sum(is.na(df))
miss_pct <- round(100 * n_miss / (n_rows * n_vars), 2)

cat("Filas:", n_rows, "| Variables:", n_vars, "\n")
cat("Missing total:", n_miss, "(", miss_pct, "%)\n\n")
cat("Iniciando mice (puede tardar varios minutos)...\n\n")

missing_mask <- is.na(df)
meth <- make.method(df)
meth[] <- "pmm"

set.seed(SEED)
imp <- mice(
  df,
  m           = M_IMPUTATIONS,
  method      = meth,
  maxit       = MAXIT,
  seed        = SEED,
  printFlag   = FALSE
)

cat("mice completado.\n\n")

# --- Guardar cada imputacion m = 1..20 ---------------------------------------
for (i in seq_len(M_IMPUTATIONS)) {
  path_m <- file.path(
    spain_dir,
    sprintf("spain_core_imputed_m%02d.csv", i)
  )
  complete_i <- complete(imp, i)
  complete_i <- as.data.frame(lapply(complete_i, round))
  write_csv(complete_i, path_m)
  cat("Guardado:", path_m, "\n")
}

# --- Pooled: observados intactos; NA -> modo de las 20 imputaciones ----------
pooled <- df
imp_mat <- array(NA_real_, dim = c(n_rows, n_vars, M_IMPUTATIONS))

for (i in seq_len(M_IMPUTATIONS)) {
  imp_mat[, , i] <- as.matrix(complete(imp, i))
}

for (j in seq_len(n_vars)) {
  miss_idx <- which(missing_mask[, j])
  if (!length(miss_idx)) {
    next
  }
  modes <- apply(imp_mat[miss_idx, j, , drop = FALSE], 1, get_mode)
  pooled[miss_idx, j] <- modes
}

pooled <- as.data.frame(lapply(pooled, round))
write_csv(pooled, path_pooled)
write_csv(pooled, path_efa)

cat("\nGuardado:", path_pooled, "\n")
cat("Guardado:", path_efa, "(alias EFA)\n\n")

# --- Validacion rapida: medias observadas vs medias post-imputacion ----------
mean_diffs <- numeric(n_vars)
names(mean_diffs) <- names(df)

for (v in names(df)) {
  obs <- df[[v]][!is.na(df[[v]])]
  if (!length(obs)) {
    next
  }
  mean_obs <- mean(obs)
  mean_all <- mean(pooled[[v]], na.rm = TRUE)
  if (mean_obs != 0) {
    mean_diffs[v] <- abs(mean_all - mean_obs) / abs(mean_obs) * 100
  } else {
    mean_diffs[v] <- abs(mean_all - mean_obs)
  }
}

max_diff <- max(mean_diffs, na.rm = TRUE)
cat("Validacion medias (observados vs pooled completo):\n")
cat("  Diferencia maxima relativa:", round(max_diff, 2), "%\n")
cat("  Variables con diff > 5%:\n")
high <- sort(mean_diffs[mean_diffs > 5], decreasing = TRUE)
if (length(high)) {
  print(round(high, 2))
} else {
  cat("  (ninguna)\n")
}

cat("\n=================================================================\n")
cat("Imputacion multiple finalizada.\n")
cat("=================================================================\n")

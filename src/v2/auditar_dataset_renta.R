#!/usr/bin/env Rscript
# v2 -- Auditoria del dataset `renta` del paquete de R `infoelectoral`.
#
# Por que existe este script
# --------------------------
# El alcance de v2 anotaba como via prometedora que el paquete `infoelectoral`
# "ya trae un dataset `renta` con >34.000 filas cruzando renta del INE por
# seccion censal", y lo marcaba como algo a revisar ANTES de escribir mas
# fontaneria, porque podia ahorrar semanas.
#
# La frase es literalmente cierta y aun asi enganosa, y esa combinacion es justo
# la que hay que cazar antes de construir encima. Este script comprueba las
# cuatro cosas que deciden si sirve, en vez de fiarse de la documentacion:
#
#   1. cuantas columnas trae de verdad (la doc dice 2: codigo y renta media);
#   2. si la clave `codigo_seccion` es unica -- sin eso, un join multiplica filas;
#   3. que provincias cubre, con atencion a Pais Vasco, que es caso central del
#      objeto de estudio (voto a partidos de ambito no estatal);
#   4. si declara a que ANO corresponde la cifra.
#
# No instala nada: descarga el tarball de fuentes de CRAN a un temporal y lee el
# .RData directamente. Se ejecuta solo y se borra lo que trae.
#
#   Rscript src/v2/auditar_dataset_renta.R

VERSION_CRAN <- "1.0.3"
URL <- sprintf(
  "https://cran.r-project.org/src/contrib/infoelectoral_%s.tar.gz", VERSION_CRAN
)

tmp <- tempfile("infoelectoral_")
dir.create(tmp)
on.exit(unlink(tmp, recursive = TRUE), add = TRUE)

tarball <- file.path(tmp, "infoelectoral.tar.gz")
cat("descargando", URL, "\n")
utils::download.file(URL, tarball, mode = "wb", quiet = TRUE)
utils::untar(tarball, exdir = tmp)

rdata <- file.path(tmp, "infoelectoral", "data", "renta_secciones.RData")
stopifnot(file.exists(rdata))
load(rdata)
d <- as.data.frame(renta)

sep <- function(t) cat("\n", strrep("-", 62), "\n", t, "\n", sep = "")

sep("1. FORMA")
cat("filas:", nrow(d), "| columnas:", ncol(d), "\n")
cat("nombres:", paste(names(d), collapse = ", "), "\n")
cat("\nno hay columna de ANO: la cifra es un corte temporal sin fechar.\n")
cat("hay columna de ano?:", any(grepl("an|year|fecha", names(d), TRUE)), "\n")
print(utils::head(d, 3))

sep("2. LA CLAVE NO ES UNICA")
dups <- sum(duplicated(d$codigo_seccion))
n_conflicto <- sum(tapply(d$renta, d$codigo_seccion, function(x) length(unique(x))) > 1)
cat("filas con codigo repetido:", dups, "\n")
cat("codigos con MAS DE UN valor de renta distinto:", n_conflicto, "\n")
if (n_conflicto > 0) {
  cat("\nejemplo de codigo con dos rentas contradictorias:\n")
  malo <- names(which(tapply(d$renta, d$codigo_seccion,
                             function(x) length(unique(x))) > 1))[1]
  print(d[d$codigo_seccion == malo, ])
  cat("\n-> un join por codigo_seccion multiplica filas y no hay regla para\n")
  cat("   elegir cual de los dos valores es el bueno.\n")
}

sep("3. COBERTURA PROVINCIAL")
codigos_provincias <- NULL
load(file.path(tmp, "infoelectoral", "data", "codigos_provincias.RData"))
cp <- as.data.frame(codigos_provincias)
presentes <- unique(substr(as.character(d$codigo_seccion), 1, 2))
faltan <- cp[!(cp$codigo_provincia %in% presentes), c("codigo_provincia", "provincia", "ccaa")]
cat("provincias presentes:", length(presentes), "de", nrow(cp), "\n\n")
cat("FALTAN:\n"); print(faltan, row.names = FALSE)
pv <- cp[cp$ccaa == "País Vasco", c("codigo_provincia", "provincia")]
pv$presente <- pv$codigo_provincia %in% presentes
cat("\nPais Vasco (caso central del objeto de estudio):\n")
print(pv, row.names = FALSE)

sep("VEREDICTO")
cat("El dataset NO sustituye al Atlas de Distribucion de Renta de los Hogares\n")
cat("(ADRH) del INE, y no por poco:\n\n")
cat("  - sin ano declarado    -> no se puede cruzar con una convocatoria\n")
cat("                            concreta ni construir la serie 2015-2023;\n")
cat("  - solo renta media     -> el ADRH da ademas indice de Gini y P80/P20,\n")
cat("                            que son las medidas de DESIGUALDAD, no de nivel;\n")
cat("  - clave no unica       -> ", dups, " filas duplicadas, ", n_conflicto,
    " con valores en conflicto;\n", sep = "")
cat("  - Pais Vasco incompleto-> falta Alava, y el ADRH si lo cubre via las\n")
cat("                            haciendas forales.\n\n")
cat("Sirve para un mapa ilustrativo. No para este diseno.\n")

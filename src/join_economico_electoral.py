#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
[HISTORICO - v1] Este script NO esta en el camino de la linea de trabajo actual.

Se conserva porque es la evidencia de por que el diseno europeo se retiro: lo que
midio (que la base electoral europea no baja de NUTS2) es uno de los tres motivos
del veredicto. La linea viva es v2, espanola y subnacional -- ver docs/v2_alcance.md.
No construir encima de esto sin leer antes esa seccion.

DIA 1 — join EU-NED x ARDECO a los DOS niveles que existen de verdad: NUTS1 y NUTS2.

Qué hace y qué NO hace
----------------------
Hace UNA cosa: construir el join económico-electoral a dos escalas y medir su
cobertura. No hace dashboard, ni clustering, ni invarianza, ni "preparar todos
los datos". Sigue el §9 del documento de diseño del observatorio.

La corrección de partida (rompe el §9 tal y como está escrito)
--------------------------------------------------------------
El diseño dice "NUTS3 y NUTS2". En los ficheros que hay en `data/raw/` EU-NED
**no tiene NUTS3**: `nutslevel` solo vale 1 o 2, y todos los códigos de región
que existen tienen 4 caracteres (= NUTS2). Las únicas filas con `nutslevel==1`
son Eslovenia, y **vienen sin código de región**. Así que el "nivel 1" no se
lee: se CONSTRUYE agregando NUTS2 -> NUTS1 por prefijo, con
Sigma(partyvote) / Sigma(validvote) como manda el diseño (§R7).

Salidas
-------
- data/processed/join_electoral_ardeco_nuts2.csv
- data/processed/join_electoral_ardeco_nuts1.csv
- data/processed/cobertura_dia1.md          <- el entregable importante
- data/processed/cobertura_dia1_no_casan.csv

`data/raw/` es READ-ONLY. Este script solo lee de ahí.

Uso:  python src/join_economico_electoral.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"

EUNED_JOINT = RAW / "eu_ned_joint_nuts2.csv"
EUNED_NATIONAL = RAW / "eu_ned_national_nuts2.csv"
ARDECO_GDP = RAW / "_ARDECO-SUVGDP.versions_2024-unit_EUR,PPS_EU27_2020-level_id_0,1,2,3.table.csv_"
ARDECO_EDU = RAW / "_ARDECO-RPDTN.versions_2024-unit_PC-isced11_ED0-2,ED3_4,ED5-8-age_Y25-64-sex_TOTAL-level_id_0,1,2.table.csv_"
ARDECO_UNEMP = RAW / "ARDECO-RPUCNP.versions_2024-unit_PC-level_id_2.table.csv"

# ARDECO publica 2025-2027 como PROYECCIÓN, no como observación. Fuera.
LAST_OBSERVED_YEAR = 2024

# EU-NED etiqueta el país con ISO-3166 y el código de región con NUTS. Difieren
# en dos casos y hay que normalizar o el prefijo de país nunca casa.
COUNTRY_TO_NUTS = {"GB": "UK", "GR": "EL"}

# Violaciones de monotonía de votos YA VISTAS y caracterizadas (2026-08-14).
# Se congelan como línea base: el script NO aborta por estas, pero SÍ aborta si
# aparece una nueva. Hipótesis del motivo (NO verificada contra el codebook de
# EU-NED — no lo tenemos aquí): LU usa panachage, así que un elector emite
# varios votos y `validvote` no es comparable con `totalvote` (papeletas).
# TR 2015/2018, RO 2004 y FI 1999 quedan sin explicación: son datos, no ruido.
KNOWN_MONOTONICITY_BREAKS = (
    {("LU", "EP", y) for y in (1994, 1999, 2004, 2009, 2014, 2019)}
    | {("LU", "Parliament", y) for y in (1994, 1999, 2004, 2009, 2013, 2018)}
    | {("TR", "Parliament", 2015), ("TR", "Parliament", 2018)}
    | {("RO", "Parliament", 2004), ("FI", "Parliament", 1999)}
)

# Región-elección donde Sigma(partyvote) supera validvote por encima de la
# tolerancia. Misma lógica de línea base.
VOTE_SUM_TOLERANCE = 1.001
KNOWN_VOTE_SUM_BREAKS = {("UK", "UKF1", 2019, "EP")}


# ---------------------------------------------------------------------------
# Auditoría: nada se pierde en silencio
# ---------------------------------------------------------------------------
class Audit:
    """Registra toda fila descartada y toda violación, con su motivo.

    Distingue dos clases de comprobación:
      - `hard`      -> aborta en el acto. Invariante estructural: si falla, el
                       join miente y no hay nada que informar.
      - `baseline`  -> compara contra una línea base de violaciones conocidas.
                       Aborta solo si aparece una NUEVA.
    """

    def __init__(self) -> None:
        self.drops: list[dict] = []
        self.violations: list[dict] = []
        self.notes: list[str] = []

    def drop(self, step: str, reason: str, n_rows: int, detail: str = "") -> None:
        self.drops.append({"step": step, "reason": reason, "n_rows": int(n_rows),
                           "detail": detail})

    def hard(self, condition: bool, message: str) -> None:
        if not condition:
            raise AssertionError(f"[ASERCION DURA] {message}")

    def baseline(self, observed: set, known: set, label: str) -> None:
        new = observed - known
        stale = known - observed
        if new:
            raise AssertionError(
                f"[ASERCION DURA] {label}: {len(new)} violacion(es) NUEVA(S) "
                f"fuera de la linea base: {sorted(new)[:10]}"
            )
        if stale:
            self.notes.append(
                f"{label}: {len(stale)} violacion(es) de la linea base ya NO "
                f"aparecen ({sorted(stale)[:5]}). Revisar si cambio el fichero."
            )
        self.violations.append({"label": label, "n": len(observed),
                                "items": sorted(observed)})

    def note(self, text: str) -> None:
        self.notes.append(text)


AUDIT = Audit()


# ---------------------------------------------------------------------------
# 1. EU-NED
# ---------------------------------------------------------------------------
def load_euned() -> pd.DataFrame:
    """Carga EU-NED 'joint' y lo limpia dejando registro de cada descarte.

    `joint` = Parliament + EP. `national` = solo Parliament y es el MISMO
    contenido (comprobado: idénticos salvo `regionname` en 376 filas), así que
    'joint' es el superconjunto y no hace falta unir nada.
    """
    df = pd.read_csv(EUNED_JOINT, dtype={"nuts2": str})
    n0 = len(df)
    AUDIT.note(f"EU-NED joint: {n0} filas leidas.")

    # Comprobación de que 'national' no aporta nada: mismas filas Parliament.
    nat = pd.read_csv(EUNED_NATIONAL, dtype={"nuts2": str})
    AUDIT.hard(
        len(nat) == (df["type"] == "Parliament").sum(),
        f"eu_ned_national ({len(nat)}) no coincide con las filas Parliament de "
        f"joint ({(df['type'] == 'Parliament').sum()}).",
    )

    # (a) Filas sin código de región: no son joinables por definición.
    sin_codigo = df["nuts2"].isna()
    if sin_codigo.any():
        det = (df[sin_codigo].groupby(["country_code", "type"]).size()
               .to_dict())
        AUDIT.drop("euned", "sin codigo de region (nuts2 vacio)",
                   int(sin_codigo.sum()), str(det))
    df = df[~sin_codigo].copy()

    # (b) Pseudo-regiones 'XXZZ' = voto exterior. No tienen territorio ni PIB.
    fuera = df["nuts2"].str.endswith("ZZ")
    if fuera.any():
        det = sorted(df.loc[fuera, "nuts2"].unique())
        AUDIT.drop("euned", "pseudo-region de voto exterior (codigo ZZ)",
                   int(fuera.sum()), ",".join(det))
    df = df[~fuera].copy()

    # Normalizar el país al vocabulario NUTS (GB->UK, GR->EL) y derivarlo del
    # propio código: es lo único que después casa con ARDECO.
    df["country_nuts"] = df["country_code"].replace(COUNTRY_TO_NUTS)
    df["nuts2_id"] = df["nuts2"].str.strip()
    df["nuts1_id"] = df["nuts2_id"].str[:3]

    # --- ASERCIONES DURAS sobre los códigos ---
    bad_len = df.loc[df["nuts2_id"].str.len() != 4, "nuts2_id"].unique()
    AUDIT.hard(len(bad_len) == 0,
               f"codigos NUTS2 de EU-NED con longitud != 4: {bad_len[:10]}")
    bad_prefix = df.loc[df["nuts2_id"].str[:2] != df["country_nuts"],
                        ["country_code", "nuts2_id"]].drop_duplicates()
    AUDIT.hard(len(bad_prefix) == 0,
               f"prefijo de pais != country_code normalizado:\n{bad_prefix}")

    # --- ASERCIÓN DURA: la clave (pais, region, anio, tipo, partido) es única ---
    key = ["country_nuts", "nuts2_id", "year", "type", "party_abbreviation"]
    dup = df.duplicated(subset=key, keep=False)
    AUDIT.hard(not dup.any(),
               f"{int(dup.sum())} filas duplicadas sobre {key}:\n"
               f"{df.loc[dup, key].head(10)}")

    # --- ASERCIÓN DURA: `partyvote` no puede tener huecos ---
    # Sin esto, la comprobación de conservación de votos al agregar a NUTS1 es
    # decorativa: `sum()` ignora los NaN a los dos lados y siempre cuadra.
    n_nan = int(df["partyvote"].isna().sum())
    AUDIT.hard(n_nan == 0,
               f"{n_nan} filas con partyvote vacio. La agregacion a NUTS1 los "
               f"ignoraria y la conservacion de votos cuadraria en falso.")

    # --- ASERCIÓN DURA: los totales son constantes dentro de region-eleccion ---
    reg_key = ["country_nuts", "nuts2_id", "year", "type"]
    nun = df.groupby(reg_key)[["electorate", "totalvote", "validvote"]].nunique()
    incoherente = nun[(nun > 1).any(axis=1)]
    AUDIT.hard(len(incoherente) == 0,
               f"{len(incoherente)} region-eleccion con totales no constantes:\n"
               f"{incoherente.head(10)}")

    AUDIT.note(f"EU-NED tras limpieza: {len(df)} filas "
               f"({n0 - len(df)} descartadas).")
    return df


def check_vote_arithmetic(df: pd.DataFrame) -> None:
    """partyvote <= validvote <= totalvote <= electorate, donde aplique.

    'Donde aplique' es literal: 3.363 filas no traen `totalvote` y 357 no traen
    `electorate`. Una comparación con NaN devuelve False y taparía el problema,
    así que cada tramo se evalúa solo sobre las filas que tienen los dos lados.
    """
    # (1) partyvote <= validvote — sin excepciones admitidas.
    m = df["partyvote"].notna() & df["validvote"].notna()
    viol = df[m & (df["partyvote"] > df["validvote"])]
    AUDIT.hard(len(viol) == 0,
               f"{len(viol)} filas con partyvote > validvote:\n"
               f"{viol[['country_nuts', 'nuts2_id', 'year', 'party_abbreviation']].head()}")

    # (2) validvote <= totalvote — con línea base de violaciones conocidas.
    m = df["validvote"].notna() & df["totalvote"].notna()
    viol = df[m & (df["validvote"] > df["totalvote"])]
    observed = set(map(tuple, viol[["country_code", "type", "year"]]
                       .drop_duplicates().to_numpy().tolist()))
    AUDIT.baseline(observed, KNOWN_MONOTONICITY_BREAKS, "validvote > totalvote")
    AUDIT.drop("euned", "validvote > totalvote (linea base conocida)",
               len(viol), str(sorted(observed)))

    # (3) totalvote <= electorate — sin excepciones admitidas.
    m = df["totalvote"].notna() & df["electorate"].notna()
    viol = df[m & (df["totalvote"] > df["electorate"])]
    AUDIT.hard(len(viol) == 0, f"{len(viol)} filas con totalvote > electorate")

    # (4) Sigma(partyvote) sobre la region-eleccion no puede pasarse de validvote.
    reg_key = ["country_nuts", "nuts2_id", "year", "type"]
    g = df.groupby(reg_key).agg(sum_party=("partyvote", "sum"),
                                validvote=("validvote", "first"))
    g["ratio"] = g["sum_party"] / g["validvote"]
    over = g[g["ratio"] > VOTE_SUM_TOLERANCE]
    observed = set(map(tuple, over.reset_index()[reg_key].to_numpy().tolist()))
    AUDIT.baseline(observed, KNOWN_VOTE_SUM_BREAKS,
                   f"Sigma(partyvote)/validvote > {VOTE_SUM_TOLERANCE}")


def build_nuts1(df2: pd.DataFrame) -> pd.DataFrame:
    """Agrega NUTS2 -> NUTS1 con Sigma(partyvote) / Sigma(validvote).

    La trampa que hay que esquivar: `validvote`/`totalvote`/`electorate` están
    REPETIDOS en cada fila de partido. Sumarlos sobre las filas de partido los
    multiplica por el número de partidos. Hay que sumarlos sobre la tabla de
    region-eleccion (una fila por region), no sobre la de partido.
    """
    reg_key = ["country_nuts", "nuts1_id", "nuts2_id", "year", "type"]
    regions = (df2[reg_key + ["electorate", "totalvote", "validvote"]]
               .drop_duplicates(subset=reg_key))

    n1_key = ["country_nuts", "nuts1_id", "year", "type"]

    def sum_strict(s: pd.Series) -> float:
        """Suma, pero devuelve NaN si a algún hijo le falta el dato: un total
        parcial disfrazado de total completo es peor que un hueco."""
        return s.sum() if s.notna().all() else np.nan

    totals = regions.groupby(n1_key).agg(
        electorate=("electorate", sum_strict),
        totalvote=("totalvote", sum_strict),
        validvote=("validvote", sum_strict),
        n_nuts2_source=("nuts2_id", "nunique"),
    ).reset_index()

    parties = df2.groupby(n1_key + ["party_abbreviation"]).agg(
        party_english=("party_english", "first"),
        partyfacts_id=("partyfacts_id", "first"),
        partyvote=("partyvote", "sum"),
        n_nuts2_with_party=("nuts2_id", "nunique"),
    ).reset_index()

    out = parties.merge(totals, on=n1_key, how="left", validate="many_to_one")
    AUDIT.hard(len(out) == len(parties),
               "el merge NUTS1 partidos x totales duplico filas")

    # --- ASERCIÓN DURA: la agregación conserva los votos ---
    # Dos comprobaciones, porque una sola se cuela: la suma total cuadra aunque
    # se pierdan filas si lo perdido eran NaN (y `sum()` los ignora en los dos
    # lados). Por eso va acompañada del recuento de pares region-partido.
    AUDIT.hard(int(df2["partyvote"].isna().sum()) == 0,
               "partyvote con NaN en la entrada: la conservacion no es medible")
    AUDIT.hard(
        np.isclose(out["partyvote"].sum(), df2["partyvote"].sum()),
        f"la agregacion a NUTS1 no conserva partyvote: "
        f"{out['partyvote'].sum()} vs {df2['partyvote'].sum()}",
    )
    expected_rows = df2.drop_duplicates(
        subset=["country_nuts", "nuts1_id", "year", "type",
                "party_abbreviation"]).shape[0]
    AUDIT.hard(len(out) == expected_rows,
               f"la agregacion a NUTS1 perdio o invento filas: {len(out)} vs "
               f"{expected_rows} pares (region NUTS1, eleccion, partido)")
    m = out["partyvote"].notna() & out["validvote"].notna()
    bad = out[m & (out["partyvote"] > out["validvote"])]
    AUDIT.hard(len(bad) == 0,
               f"{len(bad)} filas NUTS1 con partyvote > validvote agregado")

    out["nuts1_len_ok"] = out["nuts1_id"].str.len() == 3
    AUDIT.hard(out["nuts1_len_ok"].all(), "codigo NUTS1 con longitud != 3")
    return out.drop(columns=["nuts1_len_ok"])


# ---------------------------------------------------------------------------
# 2. ARDECO
# ---------------------------------------------------------------------------
def load_ardeco_long(path: Path, value_name: str, level_ids: tuple[int, ...],
                     unit: str | None = None,
                     isced: str | None = None) -> pd.DataFrame:
    """Pasa un CSV ancho de ARDECO a formato largo (territory_id, year, valor).

    Formato real, comprobado fichero a fichero (no supuesto):
      - separador ','  ·  decimal '.'  ·  sin miles  ·  UTF-8
      - FORMATO ANCHO: una columna por año
      - la región va en `TERRITORY_ID` y su nivel NUTS en `LEVEL_ID`
        (0=país, 1=NUTS1, 2=NUTS2, 3=NUTS3); longitud del código = LEVEL_ID + 2
      - un mismo fichero repite la serie por UNIT y/o ISCED11: sin filtrar,
        cada region-año entra varias veces con valores distintos

    NO se interpola. `src/ingestion/load_ardeco.py` interpola linealmente los
    huecos (línea 82); aquí no, porque el objetivo del día 1 es MEDIR la
    cobertura y la interpolación la fabrica.
    """
    df = pd.read_csv(path)
    year_cols = [c for c in df.columns if c.isdigit()]
    AUDIT.note(f"ARDECO {value_name}: {path.name} -> {len(df)} filas, "
               f"anios {year_cols[0]}-{year_cols[-1]}, "
               f"LEVEL_ID={sorted(df['LEVEL_ID'].unique())}, "
               f"UNIT={sorted(df['UNIT'].dropna().unique())}")

    if unit is not None:
        available = sorted(df["UNIT"].dropna().unique())
        AUDIT.hard(unit in available,
                   f"{path.name}: unidad '{unit}' no esta. Hay: {available}")
        df = df[df["UNIT"] == unit]
    if isced is not None:
        available = sorted(df["ISCED11"].dropna().unique())
        AUDIT.hard(isced in available,
                   f"{path.name}: ISCED '{isced}' no esta. Hay: {available}")
        df = df[df["ISCED11"] == isced]
    df = df[df["LEVEL_ID"].isin(level_ids)].copy()

    # --- ASERCIÓN DURA: longitud del código == LEVEL_ID + 2 ---
    bad = df[df["TERRITORY_ID"].str.len() != df["LEVEL_ID"] + 2]
    AUDIT.hard(len(bad) == 0,
               f"{path.name}: {len(bad)} codigos con longitud != LEVEL_ID+2:\n"
               f"{bad[['TERRITORY_ID', 'LEVEL_ID']].head()}")

    # --- ASERCIÓN DURA: la clave (territorio) es única tras filtrar ---
    dup = df.duplicated(subset=["TERRITORY_ID"], keep=False)
    AUDIT.hard(not dup.any(),
               f"{path.name}: {int(dup.sum())} TERRITORY_ID repetidos tras "
               f"filtrar unit={unit} isced={isced}. Falta una dimension.")

    keep = [c for c in year_cols if int(c) <= LAST_OBSERVED_YEAR]
    dropped_proj = [c for c in year_cols if c not in keep]
    if dropped_proj:
        AUDIT.drop("ardeco", f"{value_name}: anios de PROYECCION descartados",
                   0, ",".join(dropped_proj))

    long = df.melt(id_vars=["TERRITORY_ID", "LEVEL_ID", "NAME_HTML"],
                   value_vars=keep, var_name="year", value_name=value_name)
    long["year"] = long["year"].astype(int)
    long = long.rename(columns={"TERRITORY_ID": "region_id",
                                "LEVEL_ID": "nuts_level",
                                "NAME_HTML": "ardeco_name"})
    long[value_name] = pd.to_numeric(long[value_name], errors="coerce")
    return long


def build_ardeco_panel() -> tuple[pd.DataFrame, dict]:
    """Panel ARDECO (region, año) x variables, para NUTS1 y NUTS2."""
    gdp = load_ardeco_long(ARDECO_GDP, "gdp_pps", (1, 2), unit="PPS_EU27_2020")
    gdp_eur = load_ardeco_long(ARDECO_GDP, "gdp_eur", (1, 2), unit="EUR")
    edu = load_ardeco_long(ARDECO_EDU, "edu_tertiary_pc", (1, 2), isced="ED5-8")
    # OJO: el fichero de paro solo trae LEVEL_ID=2. No existe a NUTS1.
    unemp = load_ardeco_long(ARDECO_UNEMP, "unemployment_pc", (2,))

    panel = gdp.merge(gdp_eur.drop(columns=["ardeco_name", "nuts_level"]),
                      on=["region_id", "year"], how="outer", validate="one_to_one")
    panel = panel.merge(edu.drop(columns=["ardeco_name", "nuts_level"]),
                        on=["region_id", "year"], how="outer", validate="one_to_one")
    panel = panel.merge(unemp.drop(columns=["ardeco_name", "nuts_level"]),
                        on=["region_id", "year"], how="outer", validate="one_to_one")

    dup = panel.duplicated(subset=["region_id", "year"], keep=False)
    AUDIT.hard(not dup.any(),
               f"panel ARDECO: {int(dup.sum())} filas (region, anio) repetidas")

    # `nuts_level` venía solo del fichero de PIB en PPS. Si una región está en
    # una serie y no en la otra (pasa: Liechtenstein tiene PIB en EUR y no en
    # PPS), la unión exterior la deja con nivel NaN y desaparece en silencio de
    # los dos merges. Se deriva del propio código y se comprueba contra el
    # fichero, que es lo que debió hacerse desde el principio.
    derived = panel["region_id"].str.len() - 2
    mismatch = panel[panel["nuts_level"].notna()
                     & (panel["nuts_level"] != derived)]
    AUDIT.hard(len(mismatch) == 0,
               f"{len(mismatch)} filas donde LEVEL_ID != longitud del codigo - 2")
    orphans = sorted(panel.loc[panel["nuts_level"].isna(), "region_id"].unique())
    if orphans:
        AUDIT.note(f"ARDECO: {len(orphans)} region(es) presentes en unas series "
                   f"y no en otras (nivel derivado del codigo): {orphans}")
    panel["nuts_level"] = derived

    ranges = {
        "gdp_pps": (1980, LAST_OBSERVED_YEAR),
        "gdp_eur": (1980, LAST_OBSERVED_YEAR),
        "edu_tertiary_pc": (2000, LAST_OBSERVED_YEAR),
        "unemployment_pc": (1995, LAST_OBSERVED_YEAR),
    }
    return panel, ranges


# ---------------------------------------------------------------------------
# 3. Merge + informe
# ---------------------------------------------------------------------------
ARDECO_VARS = ["gdp_pps", "gdp_eur", "edu_tertiary_pc", "unemployment_pc"]


def merge_level(elec: pd.DataFrame, panel: pd.DataFrame, region_col: str,
                level: int) -> pd.DataFrame:
    """Left join electoral x ARDECO. La izquierda manda: no se pierde ni una fila."""
    ard = panel[panel["nuts_level"] == level].copy()
    ard = ard.rename(columns={"region_id": region_col})

    n_before = len(elec)
    merged = elec.merge(ard.drop(columns=["nuts_level"]),
                        on=[region_col, "year"], how="left",
                        validate="many_to_one", indicator=True)

    # --- ASERCIÓN DURA: un left join no puede cambiar el numero de filas ---
    AUDIT.hard(len(merged) == n_before,
               f"NUTS{level}: el merge cambio el numero de filas "
               f"({n_before} -> {len(merged)})")

    no_match = merged["_merge"] == "left_only"
    if no_match.any():
        det = (merged.loc[no_match].groupby("country_nuts")[region_col]
               .nunique().to_dict())
        AUDIT.drop(f"merge_nuts{level}",
                   "fila electoral SIN contrapartida en ARDECO (region-anio)",
                   int(no_match.sum()), str(det))
    merged["ardeco_match"] = ~no_match
    return merged.drop(columns=["_merge"])


def coverage_by_country(merged: pd.DataFrame, region_col: str,
                        ranges: dict) -> pd.DataFrame:
    """Cobertura por país: regiones que casan, que no, y años utilizables."""
    rows = []
    for cc, g in merged.groupby("country_nuts"):
        regs = g[region_col].unique()
        matched = g.loc[g["ardeco_match"], region_col].unique()
        rec = {"country": cc, "n_regions_euned": len(regs),
               "n_matched": len(matched),
               "n_unmatched": len(regs) - len(matched),
               "unmatched": ",".join(sorted(set(regs) - set(matched)))}
        for var in ARDECO_VARS:
            if var not in g.columns:
                rec[f"years_{var}"] = 0
                continue
            # Un año es utilizable si TODAS las regiones que casan tienen valor.
            sub = g[g["ardeco_match"]]
            per_year = sub.groupby("year")[var].apply(lambda s: s.notna().all())
            rec[f"years_{var}"] = int(per_year.sum())
        rows.append(rec)
    return pd.DataFrame(rows).sort_values("country")


def nesting_report(elec2: pd.DataFrame, panel: pd.DataFrame) -> pd.DataFrame:
    """¿Anida EU-NED NUTS2 exactamente dentro de cada NUTS1 de ARDECO?

    Si a un NUTS1 le falta algún hijo NUTS2, su agregado es una suma PARCIAL
    que parece un total. Eso invalida la comparación a dos escalas para esa
    región, y hay que sacarlo, no arreglarlo.
    """
    ard2 = set(panel.loc[panel["nuts_level"] == 2, "region_id"].unique())
    ard1 = set(panel.loc[panel["nuts_level"] == 1, "region_id"].unique())

    rows = []
    for (cc, n1), g in elec2.groupby(["country_nuts", "nuts1_id"]):
        children_euned = set(g["nuts2_id"].unique())
        children_ardeco = {r for r in ard2 if r.startswith(n1)}
        rows.append({
            "country": cc, "nuts1_id": n1,
            "nuts1_in_ardeco": n1 in ard1,
            "n_children_euned": len(children_euned),
            "n_children_ardeco": len(children_ardeco),
            "missing_in_euned": ",".join(sorted(children_ardeco - children_euned)),
            "missing_in_ardeco": ",".join(sorted(children_euned - children_ardeco)),
            "complete": (n1 in ard1) and len(children_ardeco) > 0
                        and children_euned == children_ardeco,
        })
    return pd.DataFrame(rows).sort_values(["country", "nuts1_id"])


TWO_SCALE_VARS = ["gdp_pps", "edu_tertiary_pc"]


def asymmetric_missing(m1: pd.DataFrame, m2: pd.DataFrame) -> pd.DataFrame:
    """Regiones NUTS2 sin dato en años en los que su padre NUTS1 SÍ lo tiene.

    Esto no es un detalle de limpieza: es un sesgo con dirección. El nivel fino
    tiene MÁS huecos que el grueso, y no al azar — se concentran en las regiones
    que nacieron de una revisión de fronteras NUTS (partición de la capital en
    PL y HU, de Sajonia en DE, ultramar en FR). Si se comparan coeficientes
    entre escalas sin cuadrar la muestra, la diferencia que se mida incluirá
    "he perdido las regiones de capital a NUTS2", no solo el efecto de escala.
    """
    r2 = m2[m2["ardeco_match"]].drop_duplicates(
        subset=["country_nuts", "nuts2_id", "year"])
    r1 = m1[m1["ardeco_match"]].drop_duplicates(
        subset=["country_nuts", "nuts1_id", "year"])
    r1_ok = r1.assign(parent_ok=r1[TWO_SCALE_VARS].notna().all(axis=1))[
        ["country_nuts", "nuts1_id", "year", "parent_ok"]]
    j = r2.merge(r1_ok, on=["country_nuts", "nuts1_id", "year"], how="left")
    j["child_ok"] = j[TWO_SCALE_VARS].notna().all(axis=1)
    bad = j[(~j["child_ok"]) & (j["parent_ok"] == True)]  # noqa: E712
    if bad.empty:
        return pd.DataFrame(columns=["country", "nuts2_id", "n_year_elections",
                                     "years"])
    out = (bad.groupby(["country_nuts", "nuts2_id"])["year"]
           .agg(n_year_elections="nunique",
                years=lambda s: ",".join(map(str, sorted(set(s)))))
           .reset_index()
           .rename(columns={"country_nuts": "country"}))
    return out.sort_values(["country", "nuts2_id"])


def two_scale_verdict(nest: pd.DataFrame, m1: pd.DataFrame, m2: pd.DataFrame,
                      min_regions: int = 2
                      ) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """La pregunta del punto 4, con criterio explícito, per país-elección.

    H0 exige "mismo modelo, MISMA MUESTRA y mismas elecciones". Así que la
    unidad de decisión no es el país entero sino la **región NUTS1**: una NUTS1
    entra en una elección solo si tiene dato Y todos sus hijos NUTS2 lo tienen.
    Si a un hijo le falta, se cae la NUTS1 entera a los DOS niveles — si no, se
    estaría comparando territorios distintos y llamándolo efecto de escala.

    Un país-elección cuenta si:
      C1  >= `min_regions` NUTS1 utilizables (con 1 región no hay modelo)
      C2  el NUTS1 es de verdad más grueso: #NUTS2 utilizables > #NUTS1
          (si son iguales, las dos "escalas" son el mismo mapa con otro nombre)
      C3  esas NUTS1 anidan exacto (ya filtrado vía `nest`)
      C4  `gdp_pps` y `edu_tertiary_pc` no nulos en todas ellas
          (el paro NO entra: no existe a NUTS1)
    """
    ok_pairs = set(map(tuple, nest.loc[nest["complete"],
                                       ["country", "nuts1_id"]]
                       .to_numpy().tolist()))

    def restrict(df, region_col):
        d = df[(df["type"] == "Parliament") & df["ardeco_match"]].copy()
        d = d.drop_duplicates(subset=["country_nuts", region_col, "year"])
        keep = [tuple(x) in ok_pairs
                for x in d[["country_nuts", "nuts1_id"]].to_numpy().tolist()]
        d = d[keep].copy()
        d["ok"] = d[TWO_SCALE_VARS].notna().all(axis=1)
        return d

    r1 = restrict(m1, "nuts1_id")
    r2 = restrict(m2, "nuts2_id")

    children = r2.groupby(["country_nuts", "nuts1_id", "year"]).agg(
        all_children_ok=("ok", "all"), n_children=("ok", "size")).reset_index()
    par = r1[["country_nuts", "nuts1_id", "year", "ok"]].rename(
        columns={"ok": "parent_ok"})
    u = children.merge(par, on=["country_nuts", "nuts1_id", "year"], how="inner")
    u["usable"] = u["all_children_ok"] & u["parent_ok"]

    per_year = (u[u["usable"]].groupby(["country_nuts", "year"])
                .agg(n_nuts1=("nuts1_id", "nunique"),
                     n_nuts2=("n_children", "sum")).reset_index())
    per_year["qualifies"] = ((per_year["n_nuts1"] >= min_regions)
                             & (per_year["n_nuts2"] > per_year["n_nuts1"]))

    rows = []
    for cc in sorted(m2["country_nuts"].unique()):
        sub = per_year[per_year["country_nuts"] == cc]
        good = sub[sub["qualifies"]]
        rows.append({
            "country": cc,
            "n_nuts1_complete": int(nest[(nest["country"] == cc)
                                         & nest["complete"]].shape[0]),
            "n_nuts1_usable_max": int(sub["n_nuts1"].max()) if len(sub) else 0,
            "n_nuts2_usable_max": int(sub["n_nuts2"].max()) if len(sub) else 0,
            "n_elections_both_scales": len(good),
            "elections_both_scales": ",".join(map(str, sorted(good["year"]))),
            "qualifies": len(good) >= 1,
        })
    df = pd.DataFrame(rows)

    strict = df[df["qualifies"] & (df["n_nuts1_usable_max"] >= 5)]
    summary = {
        "n_countries_euned": len(df),
        "n_qualify": int(df["qualifies"].sum()),
        "countries_qualify": sorted(df.loc[df["qualifies"], "country"]),
        "n_elections_total": int(df.loc[df["qualifies"],
                                        "n_elections_both_scales"].sum()),
        "n_qualify_ge5": len(strict),
        "countries_qualify_ge5": sorted(strict["country"]),
        "n_elections_ge5": int(strict["n_elections_both_scales"].sum()),
    }
    return (df.sort_values(["qualifies", "n_elections_both_scales", "country"],
                           ascending=[False, False, True]),
            per_year, summary)


# ---------------------------------------------------------------------------
# 4. Informe markdown
# ---------------------------------------------------------------------------
def write_report(cov1, cov2, nest, verdict, summary, m1, m2, ranges,
                 asym) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "cobertura_dia1.md"
    L: list[str] = []
    A = L.append

    A("# Cobertura del join EU-NED x ARDECO — DIA 1")
    A("")
    A("> Generado por `src/join_economico_electoral.py`. **Lo que NO casa vale "
      "mas que lo que si**, asi que va primero.")
    A("")
    A("## 0. Correccion de partida: no hay NUTS3, y el NUTS1 hay que construirlo")
    A("")
    A("El diseno (§9) pide el join a **NUTS3 y NUTS2**. En estos ficheros:")
    A("")
    A("- EU-NED: `nutslevel` solo vale 1, 2 o vacio. **Todos** los codigos de "
      "region que existen tienen 4 caracteres = NUTS2. **No hay NUTS3.**")
    A("- Las unicas filas con `nutslevel == 1` son Eslovenia (105 en `joint`), "
      "y vienen **sin codigo de region**. Esto cierra la contradiccion C4 del "
      "§11 del diseno: en estos ficheros Eslovenia es una **unidad unica sin "
      "codigo NUTS**, ni NUTS1 ni NUTS2. Sale de la muestra regional.")
    A("- ARDECO si tiene NUTS3 para el PIB (`LEVEL_ID=3`, 2.669 territorios), "
      "pero sin lado electoral no sirve de nada.")
    A("")
    A("Asi que las dos escalas reales son **NUTS2 (leido)** y **NUTS1 "
      "(agregado por prefijo con Sigma(partyvote)/Sigma(validvote))**.")
    A("")
    A("## 1. Lo que NO casa")
    A("")
    A("### 1.1 Filas descartadas antes del merge")
    A("")
    A("| Paso | Motivo | Filas | Detalle |")
    A("|---|---|---:|---|")
    for d in AUDIT.drops:
        det = d["detail"][:180].replace("|", "/")
        A(f"| {d['step']} | {d['reason']} | {d['n_rows']} | {det} |")
    A("")
    A("### 1.2 Regiones de EU-NED sin contrapartida en ARDECO, por motivo")
    A("")
    A("| Nivel | Pais | Regiones EU-NED | Casan | No casan | Codigos que fallan |")
    A("|---|---|---:|---:|---:|---|")
    for lvl, cov in ((2, cov2), (1, cov1)):
        for _, r in cov.iterrows():
            if r["n_unmatched"] > 0:
                A(f"| NUTS{lvl} | {r['country']} | {r['n_regions_euned']} | "
                  f"{r['n_matched']} | {r['n_unmatched']} | `{r['unmatched']}` |")
    A("")
    A("**Los tres motivos, separados (no es el mismo problema):**")
    A("")
    A("1. **El Reino Unido no existe en ARDECO 2024.** Cero territorios `UK*` "
      "en los tres ficheros. EU-NED trae 41 regiones NUTS2 britanicas y 3.350 "
      "filas: se pierden **enteras**, y no hay arreglo con estos datos.")
    A("2. **Vintage NUTS distinto.** EU-NED usa una version anterior de la "
      "nomenclatura y ARDECO una posterior. **Ninguno de los dos ficheros "
      "declara su vintage**: lo que sigue esta inferido de los codigos, no "
      "leido de una cabecera. (El diseno §R7 dice que EU-NED esta armonizado a "
      "NUTS 2016; los codigos de ARDECO son de NUTS 2021 o 2024.) Casos "
      "verificados uno a uno:")
    A("")
    A("| Pais | EU-NED tiene | ARDECO tiene | Tipo de cambio |")
    A("|---|---|---|---|")
    A("| PT | `PT16` `PT17` `PT18` | `PT19` `PT1A` `PT1B` `PT1C` `PT1D` | "
      "redivision, **no** renombrado 1:1 |")
    A("| NO | `NO01` `NO03` `NO04` `NO05` | `NO0A` `NO0B` `NO02` `NO06`-`NO09` | "
      "redivision |")
    A("| HR | `HR04` | `HR02` `HR05` `HR06` | division 1 -> 3 |")
    A("| NL | `NL31` `NL33` | `NL35` `NL36` | recodificacion |")
    A("")
    A("   **Sin crosswalk oficial NUTS no se pueden reconciliar**, y no lo hay "
      "en `data/raw/`. Inventar una equivalencia por nombre seria fabricar dato.")
    A("3. **Pseudo-regiones de voto exterior** (`ATZZ`, `BEZZ`, `BGZZ`, `FRZZ`, "
      "`ELZZ`, `HRZZ`, `HUZZ`, `LTZZ`, `LVZZ`, `PLZZ`) y **filas sin codigo** "
      "(Eslovenia entera; las circunscripciones al Parlamento Europeo de "
      "Irlanda, que son electorales y no NUTS).")
    A("")
    A("### 1.3 Violaciones de la aritmetica de votos")
    A("")
    for v in AUDIT.violations:
        A(f"- **{v['label']}**: {v['n']} caso(s). {v['items']}")
    A("")
    A("Las de `validvote > totalvote` estan **congeladas como linea base** en el "
      "script: no abortan, pero si aparece una nueva el script se para. "
      "Luxemburgo es explicable (panachage: varios votos por papeleta); "
      "**TR 2015/2018, RO 2004 y FI 1999 no tienen explicacion aqui** y no se "
      "debe inventar una.")
    A("")
    A("## 2. Anidamiento NUTS2 -> NUTS1")
    A("")
    A("Un NUTS1 al que le falta un hijo produce un agregado **parcial que "
      "parece un total**. Estos son los que NO anidan exacto:")
    A("")
    A("| Pais | NUTS1 | En ARDECO | Hijos EU-NED | Hijos ARDECO | Faltan en EU-NED | Faltan en ARDECO |")
    A("|---|---|---|---:|---:|---|---|")
    for _, r in nest[~nest["complete"]].iterrows():
        A(f"| {r['country']} | `{r['nuts1_id']}` | {r['nuts1_in_ardeco']} | "
          f"{r['n_children_euned']} | {r['n_children_ardeco']} | "
          f"`{r['missing_in_euned']}` | `{r['missing_in_ardeco']}` |")
    A("")
    A(f"NUTS1 que anidan exacto: **{int(nest['complete'].sum())}** de "
      f"**{len(nest)}**.")
    A("")
    A("## 3. Cobertura temporal: que anios son utilizables")
    A("")
    A("Rango de cada variable en el fichero (fuera de rango = la columna del "
      "anio **no existe**, no es que falte el valor):")
    A("")
    A("| Variable | Fichero | Primer anio | Ultimo anio observado | Niveles NUTS |")
    A("|---|---|---:|---:|---|")
    A(f"| `gdp_pps` / `gdp_eur` | SUVGDP | {ranges['gdp_pps'][0]} | "
      f"{ranges['gdp_pps'][1]} | 0,1,2,3 |")
    A(f"| `edu_tertiary_pc` (ISCED ED5-8) | RPDTN | {ranges['edu_tertiary_pc'][0]} | "
      f"{ranges['edu_tertiary_pc'][1]} | 0,1,2 |")
    A(f"| `unemployment_pc` | RPUCNP | {ranges['unemployment_pc'][0]} | "
      f"{ranges['unemployment_pc'][1]} | **solo 2** |")
    A("")
    A("**Consecuencia dura, y decide el modelo:** el paro **no existe a NUTS1**. "
      "Un modelo con paro no se puede estimar a dos escalas con estos ficheros. "
      "Las unicas variables disponibles a NUTS1 y NUTS2 a la vez son **PIB pc y "
      "educacion terciaria**.")
    A("")
    A("Y educacion arranca en **2000**: toda eleccion anterior queda fuera del "
      "modelo de dos escalas. Las elecciones de EU-NED van de 1983 a 2020.")
    A("")
    A("Aparte: aunque el fichero de PIB tiene columnas desde 1980, a NUTS2 el "
      "dato **empieza de hecho en 1995** para buena parte de los paises "
      "(ES, DE, IT, HU: 1993/94 salen vacios y 1995/96 llenos). Columna que "
      "existe no es dato que exista.")
    A("")
    A("### 3.1 🔴 El hueco NO es simetrico entre escalas — y esto sesga H0")
    A("")
    A("Hay regiones NUTS2 sin dato en anios en los que **su propio padre NUTS1 "
      "si lo tiene**. No es ruido: se concentra en las regiones que **nacieron "
      "de una revision de fronteras NUTS**, que son sobre todo **regiones de "
      "capital**:")
    A("")
    A("| Pais | NUTS2 | Anios-eleccion que pierde (Parliament + EP) | Anios |")
    A("|---|---|---:|---|")
    for _, r in asym.iterrows():
        A(f"| {r['country']} | `{r['nuts2_id']}` | {r['n_year_elections']} | "
          f"{r['years']} |")
    A("")
    A("Lectura: `PL91`/`PL92` (particion de Varsovia), `HU11`/`HU12` "
      "(particion de Budapest), `DED4`/`DED5` (particion de Sajonia), "
      "`FRY*` (ultramar frances), `ITH5`/`ITI3`. **El nivel fino pierde "
      "sistematicamente las regiones de capital y las perifericas.**")
    A("")
    A("> Consecuencia directa para H0: si se estima el mismo modelo a NUTS1 y a "
      "NUTS2 sin cuadrar la muestra, parte de la diferencia entre coeficientes "
      "**no es efecto de escala, es que a NUTS2 ha desaparecido la capital**. "
      "Por eso el criterio del §4 tira la region NUTS1 entera a los dos niveles "
      "cuando le falta un hijo, en vez de quedarse con lo que haya.")
    A("")
    A("### 3.2 Anios electorales con dato completo, por pais y nivel")
    A("")
    A("(cuenta de anios-eleccion en los que TODAS las regiones que casan tienen "
      "valor; `Parliament` y `EP` juntos)")
    A("")
    A("| Pais | N2 regiones | N2 anios PIB | N2 anios educ | N2 anios paro | "
      "N1 regiones | N1 anios PIB | N1 anios educ |")
    A("|---|---:|---:|---:|---:|---:|---:|---:|")
    c1i = cov1.set_index("country")
    for _, r in cov2.iterrows():
        cc = r["country"]
        g1 = c1i.loc[cc] if cc in c1i.index else None
        A(f"| {cc} | {r['n_matched']} | {r['years_gdp_pps']} | "
          f"{r['years_edu_tertiary_pc']} | {r['years_unemployment_pc']} | "
          f"{'-' if g1 is None else g1['n_matched']} | "
          f"{'-' if g1 is None else g1['years_gdp_pps']} | "
          f"{'-' if g1 is None else g1['years_edu_tertiary_pc']} |")
    A("")
    A("## 4. LA PREGUNTA: cuantos paises admiten el mismo modelo a dos escalas")
    A("")
    A("Criterio, explicito para que se pueda discutir. La unidad de decision no "
      "es el pais sino la **region NUTS1 en una eleccion concreta**, porque H0 "
      "pide *misma muestra* a las dos escalas:")
    A("")
    A("- **C1** >= 2 regiones NUTS1 utilizables (con 1 sola, NUTS1 *es* el "
      "pais: no hay variacion entre regiones y el modelo no existe).")
    A("- **C2** el NUTS1 tiene que ser **de verdad mas grueso**: #NUTS2 "
      "utilizables > #NUTS1. Si son iguales (PT2->PT20, PT3->PT30) las dos "
      "'escalas' son el mismo mapa con otro nombre.")
    A("- **C3** esas NUTS1 anidan exacto (§2): ningun hijo NUTS2 ausente.")
    A("- **C4** `gdp_pps` y `edu_tertiary_pc` no nulos en la NUTS1 **y en todos "
      "sus hijos**. El paro no entra: no existe a NUTS1.")
    A("")
    A(f"### Respuesta: **{summary['n_qualify']} paises** de "
      f"{summary['n_countries_euned']} presentes en EU-NED.")
    A("")
    A(f"`{', '.join(summary['countries_qualify'])}`")
    A("")
    A(f"Suman **{summary['n_elections_total']} elecciones nacionales** "
      f"estimables a las dos escalas con la misma muestra.")
    A("")
    A("**Pero el numero de arriba se lo cree solo quien no mire el tamano.** "
      "Varios de esos paises pasan el corte con **2 o 3 regiones NUTS1**, y una "
      "regresion entre 2 unidades no es una regresion. Con un minimo de **5 "
      f"regiones NUTS1** — que sigue siendo poco — quedan "
      f"**{summary['n_qualify_ge5']} paises** "
      f"(`{', '.join(summary['countries_qualify_ge5'])}`) y "
      f"**{summary['n_elections_ge5']} elecciones**. Ese es el numero que hay "
      "que usar para decidir si el artefacto se sostiene.")
    A("")
    A("| Pais | NUTS1 completas | NUTS1 utiles (max) | NUTS2 utiles (max) | "
      "Elecciones a 2 escalas | Anios | Sirve |")
    A("|---|---:|---:|---:|---:|---|:-:|")
    for _, r in verdict.iterrows():
        A(f"| {r['country']} | {r['n_nuts1_complete']} | "
          f"{r['n_nuts1_usable_max']} | {r['n_nuts2_usable_max']} | "
          f"{r['n_elections_both_scales']} | {r['elections_both_scales']} | "
          f"{'**SI**' if r['qualifies'] else 'no'} |")
    A("")
    A("## 5. Lo que con estos datos NO se puede saber")
    A("")
    A("- **Si el cambio de escala mueve el coeficiente por MAUP o por otra "
      "cosa.** El NUTS1 de aqui es un agregado de NUTS2, no una medida "
      "independiente: comparte el error de medida de sus hijos.")
    A("- **Si las regiones que no casan son ignorables.** No lo son: el Reino "
      "Unido es el caso mas estudiado de la literatura (Brexit) y se pierde "
      "entero. Toda conclusion queda condicionada a una muestra que **excluye "
      "sistematicamente** al UK y a cuatro paises con redivision NUTS.")
    A("- **Si el desajuste de vintage es solo de codigo o tambien de frontera.** "
      "Con estos ficheros no se distingue un renombrado de una redivision real; "
      "haria falta el crosswalk oficial de Eurostat.")
    A("- **A que anio de ARDECO debe engancharse una eleccion.** Aqui se une al "
      "**mismo anio**, que es una decision, no un hecho: las hipotesis del "
      "diseno (H1, H11) piden t-k y eso cambia la cobertura.")
    A("")
    A("## 6. Notas del pipeline")
    A("")
    for n in AUDIT.notes:
        A(f"- {n}")
    A("")
    A(f"Filas del join final: NUTS2 = **{len(m2)}**, NUTS1 = **{len(m1)}**.")
    A("")

    path.write_text("\n".join(L), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
def main() -> int:
    print("=" * 78)
    print("DIA 1 — join EU-NED x ARDECO (NUTS1 y NUTS2)")
    print("=" * 78)

    print("\n[1/6] Cargando EU-NED...")
    elec2 = load_euned()
    check_vote_arithmetic(elec2)
    print(f"      {len(elec2)} filas electorales a NUTS2, "
          f"{elec2['nuts2_id'].nunique()} regiones, "
          f"{elec2['country_nuts'].nunique()} paises.")

    print("\n[2/6] Agregando NUTS2 -> NUTS1 (Sigma partyvote / Sigma validvote)...")
    elec1 = build_nuts1(elec2)
    print(f"      {len(elec1)} filas a NUTS1, "
          f"{elec1['nuts1_id'].nunique()} regiones NUTS1.")

    print("\n[3/6] Cargando ARDECO...")
    panel, ranges = build_ardeco_panel()
    print(f"      panel ARDECO: {len(panel)} filas (region, anio); "
          f"NUTS1={panel[panel['nuts_level'] == 1]['region_id'].nunique()} "
          f"NUTS2={panel[panel['nuts_level'] == 2]['region_id'].nunique()}")

    print("\n[4/6] Merge a los dos niveles...")
    m2 = merge_level(elec2, panel, "nuts2_id", level=2)
    m1 = merge_level(elec1, panel, "nuts1_id", level=1)
    print(f"      NUTS2: {len(m2)} filas, "
          f"{100 * m2['ardeco_match'].mean():.1f}% con contrapartida ARDECO")
    print(f"      NUTS1: {len(m1)} filas, "
          f"{100 * m1['ardeco_match'].mean():.1f}% con contrapartida ARDECO")

    print("\n[5/6] Cobertura y anidamiento...")
    cov2 = coverage_by_country(m2, "nuts2_id", ranges)
    cov1 = coverage_by_country(m1, "nuts1_id", ranges)
    nest = nesting_report(elec2, panel)
    asym = asymmetric_missing(m1, m2)
    verdict, per_year, summary = two_scale_verdict(nest, m1, m2)

    print("\n[6/6] Escribiendo salidas...")
    OUT.mkdir(parents=True, exist_ok=True)
    p2 = OUT / "join_electoral_ardeco_nuts2.csv"
    p1 = OUT / "join_electoral_ardeco_nuts1.csv"
    m2.to_csv(p2, index=False, encoding="utf-8")
    m1.to_csv(p1, index=False, encoding="utf-8")

    no_casan = []
    for lvl, cov in ((2, cov2), (1, cov1)):
        for _, r in cov.iterrows():
            for code in filter(None, r["unmatched"].split(",")):
                no_casan.append({"nuts_level": lvl, "country": r["country"],
                                 "region_id": code})
    pd.DataFrame(no_casan).to_csv(OUT / "cobertura_dia1_no_casan.csv",
                                  index=False, encoding="utf-8")
    rep = write_report(cov1, cov2, nest, verdict, summary, m1, m2, ranges, asym)

    print(f"      {p2.relative_to(ROOT)}")
    print(f"      {p1.relative_to(ROOT)}")
    print(f"      {(OUT / 'cobertura_dia1_no_casan.csv').relative_to(ROOT)}")
    print(f"      {rep.relative_to(ROOT)}")

    print("\n" + "=" * 78)
    print("RESUMEN")
    print("=" * 78)
    print(f"Filas electorales descartadas antes del merge: "
          f"{sum(d['n_rows'] for d in AUDIT.drops if d['step'] == 'euned')}")
    for d in AUDIT.drops:
        print(f"  - [{d['step']}] {d['reason']}: {d['n_rows']} filas")
    print()
    print("Regiones que NO casan con ARDECO:")
    for lvl, cov in ((2, cov2), (1, cov1)):
        tot = int(cov["n_regions_euned"].sum())
        bad = int(cov["n_unmatched"].sum())
        print(f"  NUTS{lvl}: {bad} de {tot} regiones "
              f"({100 * bad / tot:.1f}%)")
        for _, r in cov[cov["n_unmatched"] > 0].iterrows():
            print(f"     {r['country']}: {r['n_unmatched']}/"
                  f"{r['n_regions_euned']}  -> {r['unmatched']}")
    print()
    print(f"NUTS1 que anidan exacto: {int(nest['complete'].sum())}/{len(nest)}")
    print()
    print("Huecos ASIMETRICOS (NUTS2 sin dato con el padre NUTS1 con dato):")
    print(f"  {len(asym)} regiones NUTS2 afectadas -> "
          f"{sorted(asym['nuts2_id'])}")
    print()
    print("PREGUNTA 4 — paises con el MISMO modelo estimable a NUTS1 y NUTS2:")
    print(f"  RESPUESTA: {summary['n_qualify']} de "
          f"{summary['n_countries_euned']} paises de EU-NED")
    print(f"  {summary['countries_qualify']}")
    print(f"  Elecciones nacionales estimables a las dos escalas: "
          f"{summary['n_elections_total']}")
    print(f"  Con >= 5 regiones NUTS1 (minimo para que la regresion exista): "
          f"{summary['n_qualify_ge5']} paises "
          f"{summary['countries_qualify_ge5']}, "
          f"{summary['n_elections_ge5']} elecciones")
    print()
    print(verdict.to_string(index=False,
                            columns=["country", "n_nuts1_complete",
                                     "n_nuts1_usable_max",
                                     "n_nuts2_usable_max",
                                     "n_elections_both_scales",
                                     "qualifies"]))
    if AUDIT.notes:
        print("\nNotas:")
        for n in AUDIT.notes:
            print(f"  - {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

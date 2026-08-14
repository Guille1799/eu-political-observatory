"""
DIA 2 — Cobertura de la clasificacion de partidos (riesgo R1).

Que hace y por que
------------------
El diseno del observatorio (`JobHunter/docs/fundamentos/observatorio-nacionalismo-regional.md`,
seccion R1) senala la clasificacion de partidos como el unico riesgo de medida que
*demostrablemente invierte signos* en la literatura publicada, y exige reportar el
resultado bajo **>= 2 clasificaciones independientes**. Antes de poder cumplir esa regla
hay que saber **sobre cuanto voto existen realmente dos veredictos**. Eso es lo unico que
mide este script.

NO hace modelos, ni regresiones, ni clustering, ni dashboards. Cuenta votos y compara
etiquetas.

Salidas (todas en data/processed/, ninguna en data/raw/ que es READ-ONLY):
  - cobertura_partidos_dia2.md         informe con todas las tablas
  - cobertura_por_pais.csv             cobertura por pais
  - cobertura_por_anio.csv             cobertura por anio
  - cobertura_pais_anio.csv            cobertura por pais x eleccion
  - discrepancias_clasificacion.csv    desacuerdos PopuList vs POPPA, partido a partido
  - partidos_sin_clasificar.csv        partidos sin veredicto, ordenados por voto
  - poppa_sin_partyfacts.csv           partidos de POPPA que no se pueden enlazar por id
  - auditoria_clave_partyfacts.csv     joins sospechosos de apuntar al partido equivocado

Uso:  python src/cobertura_partidos.py    (desde la raiz del repo)
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd

if hasattr(sys.stdout, "reconfigure"):  # acentos en la consola de Windows
    sys.stdout.reconfigure(encoding="utf-8")

RAW = Path("data/raw")
OUT = Path("data/processed")

# ── Parametros metodologicos, todos declarados y todos discutibles ──────────────
# Umbral de nativismo POPPA. Procedencia: src/ingestion/parameters.py — convencion del
# proyecto decidida el 2026-05-05 SIN cita bibliografica. Aqui se usa como valor central
# y se corre sensibilidad alrededor precisamente porque es arbitrario.
NATIVISM_THRESHOLD = 7.0
NATIVISM_SENSIBILIDAD = [6.0, 6.5, 7.0, 7.5, 8.0]

# Ano desde el que se asume que PopuList 3.0 cubre su universo de partidos. Se usa para
# decidir si la AUSENCIA de un partido en PopuList es informativa ("no es far-right") o
# indeterminada ("PopuList no mira ahi").
# 🔴 [pendiente-verif] NO esta verificado contra el codebook de PopuList: no hay codebook
# en el repo y el CSV no trae metadatos de cobertura. Ni el ano ni el bar de entrada
# (escanos / % de voto) estan confirmados. Toda la columna "PopuList_cerrado_%" cuelga de
# este supuesto; por eso el informe da siempre el par explicito/cerrado y nunca uno solo.
POPULIST_ANIO_MIN = 1989

# Etiquetas de EU-NED que NO son partidos sino agregados residuales.
ETIQUETAS_RESIDUALES = {"OTHER", "OTHERS", "OTHER LEFT", "OTHER RIGHT", "OTHER FAR-LEFT"}

# PopuList escribe "Czech Republic" donde EU-NED escribe "Czechia".
ALIAS_PAIS = {"Czech Republic": "Czechia"}

# Auditoria de la clave de union. Un `partyfacts_id` puede apuntar a partidos distintos en
# ficheros distintos (verificado a mano en dos casos, ver informe). Estos dos parametros
# gobiernan el detector automatico; ambos son convenciones, no umbrales de literatura.
MARGEN_ENGANCHE = 0.15     # cuanto mejor debe encajar otro id para sospechar del actual
SIM_MINIMA_ALTERNATIVA = 0.60  # y ademas la alternativa tiene que encajar de verdad
SIM_ENLACE_PERDIDO = 0.80  # parecido minimo para decir "este partido SI esta en EU-NED"

_STOP = {"the", "of", "for", "and", "de", "la", "le", "el", "und", "der", "die",
         "van", "den", "party", "parties", "partij", "partido"}

SEP = "=" * 78


def titulo(txt: str) -> None:
    print(f"\n{SEP}\n{txt}\n{SEP}")


def md_table(df: pd.DataFrame, index: bool = False) -> str:
    """Tabla markdown sin dependencias externas (no hay tabulate en el entorno)."""
    d = df.reset_index() if index else df.copy()
    cols = [str(c) for c in d.columns]
    filas = [[("" if pd.isna(v) else str(v)) for v in row] for row in d.itertuples(index=False)]
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    out += ["| " + " | ".join(f) + " |" for f in filas]
    return "\n".join(out)


# ═══════════════════════════════════════════════════════════════════════════════
# 1. CARGA + CHEQUEOS DE INTEGRIDAD
# ═══════════════════════════════════════════════════════════════════════════════
def cargar():
    ned = pd.read_csv(RAW / "eu_ned_joint_nuts2.csv", low_memory=False)
    popu = pd.read_csv(RAW / "The PopuList 3.0.csv", sep=";", encoding="utf-8-sig")
    poppa = pd.read_csv(RAW / "poppa_integrated_v2.csv", low_memory=False)
    puente = pd.read_csv(RAW / "partyfacts-parlgov-ids.csv")
    parlgov = pd.read_csv(RAW / "view_party.csv", low_memory=False)

    # Identificador de region: EU-NED deja `nuts2` vacio en las EP irlandesas (regiones
    # electorales que no son NUTS) y usa nivel NUTS1 en Eslovenia. El nombre de region
    # completa el hueco; sin esto las filas huerfanas se mezclan en un solo grupo.
    ned["region_id"] = ned["nuts2"].fillna(ned["regionname"])

    # --- aserciones sobre EU-NED: si el fichero miente, que falle aqui y no en el informe
    clave = ["country_code", "region_id", "year", "type", "party_abbreviation"]
    dups = int(ned.duplicated(subset=clave).sum())
    assert dups == 0, f"EU-NED: {dups} filas duplicadas por {clave}"

    g = ned.groupby(["country_code", "region_id", "year", "type"], dropna=False)
    vv_unico = g.validvote.nunique()
    assert (vv_unico <= 1).all(), "EU-NED: validvote no es unico dentro de region-eleccion"
    ratio = (g.partyvote.sum() / g.validvote.first()).dropna()
    assert ratio.between(0.94, 1.01).all(), (
        f"EU-NED: suma de partyvote fuera de rango vs validvote "
        f"[{ratio.min():.4f}, {ratio.max():.4f}]"
    )

    ned["pf"] = ned["partyfacts_id"].astype("Int64")
    ned["residual"] = ned["party_abbreviation"].str.upper().isin(ETIQUETAS_RESIDUALES)
    ned["nombre"] = (
        ned["party_english"].fillna(ned["party_native"]).fillna(ned["party_abbreviation"])
    )

    popu["pf"] = popu["partyfacts_id"].astype("Int64")
    poppa["pf"] = poppa["partyfacts_id"].astype("Int64")

    return ned, popu, poppa, puente, parlgov, ratio


# ═══════════════════════════════════════════════════════════════════════════════
# 2. DIAGNOSTICO DE ENLACE — que identificador trae cada fichero
# ═══════════════════════════════════════════════════════════════════════════════
def diagnostico_enlace(ned, popu, poppa, puente, parlgov, ratio):
    titulo("1. DIAGNOSTICO DE ENLACE (comprobado, no supuesto)")
    print(f"EU-NED   filas={len(ned):>6}  paises={ned.country_code.nunique():>2}  "
          f"anios={ned.year.min()}-{ned.year.max()}  tipos={sorted(ned.type.unique())}")
    print(f"         suma(partyvote)/validvote por region-eleccion: "
          f"min={ratio.min():.4f} mediana={ratio.median():.4f} max={ratio.max():.4f}")
    print(f"PopuList filas={len(popu):>6}  paises={popu.country_name.nunique():>2}")
    print(f"POPPA    filas={len(poppa):>6}  paises={poppa.country.nunique():>2}  "
          f"olas={sorted(poppa.wave.unique())}")
    print(f"Puente   filas={len(puente):>6}  columnas={list(puente.columns)}")
    print(f"ParlGov  filas={len(parlgov):>6}  identificador propio: party_id (NO partyfacts_id)")

    print("\n-- Identificador que trae cada fichero --")
    print("  EU-NED   : partyfacts_id           (directo)")
    print("  PopuList : partyfacts_id + parlgov_id (directo, doble)")
    print("  POPPA    : partyfacts_id + poppa_id   (directo)")
    print("  ParlGov  : party_id  -> necesita partyfacts-parlgov-ids.csv")
    print("  => El enlace EU-NED x PopuList x POPPA es DIRECTO por partyfacts_id.")
    print("     El puente solo hace falta para ParlGov, que aqui no clasifica nada.")

    ids_ned = set(ned.pf.dropna())
    ids_popu = set(popu.pf.dropna())
    ids_poppa = set(poppa.pf.dropna())
    print(f"\n-- Identificadores unicos --")
    print(f"  EU-NED {len(ids_ned)} | PopuList {len(ids_popu)} | POPPA {len(ids_poppa)}")
    print(f"  EU-NED ∩ PopuList = {len(ids_ned & ids_popu)}")
    print(f"  EU-NED ∩ POPPA    = {len(ids_ned & ids_poppa)}")
    print(f"  EU-NED ∩ ambos    = {len(ids_ned & ids_popu & ids_poppa)}")

    # ¿el puente recupera algo?
    mapa = dict(zip(puente.parlgov_id, puente.partyfacts_id))
    huerfanos = popu[popu.pf.isna()]
    recuperables = int(sum(int(x) in mapa for x in huerfanos.parlgov_id.dropna()))
    print(f"\n-- ¿Anade algo el puente parlgov? --")
    print(f"  PopuList sin partyfacts_id: {len(huerfanos)} "
          f"(con parlgov_id: {huerfanos.parlgov_id.notna().sum()})")
    print(f"  Recuperables via puente   : {recuperables}   <- el puente NO recupera ninguno")
    print(f"  POPPA sin partyfacts_id   : {poppa.pf.isna().sum()} filas / "
          f"{poppa[poppa.pf.isna()].party_short.nunique()} partidos, y POPPA no trae "
          f"parlgov_id => IRRECUPERABLES por id")

    # duplicados de partyfacts_id dentro de PopuList
    dup = popu[popu.pf.notna() & popu.pf.duplicated(keep=False)]
    if len(dup):
        print(f"\n  AVISO: {len(dup)} filas de PopuList comparten partyfacts_id:")
        for _, r in dup.iterrows():
            print(f"    pf={int(r.pf)} {r.party_name} ({r.country_name}) farright={r.farright}")

    # PopuList es una lista SOLO-POSITIVOS: comprobado, no recordado
    ceros = ((popu.populist == 0) & (popu.farright == 0)
             & (popu.farleft == 0) & (popu.eurosceptic == 0)).sum()
    print(f"\n-- Naturaleza de PopuList --")
    print(f"  Filas con los 4 flags a 0: {ceros} de {len(popu)}")
    print("  => PopuList es una lista SOLO-POSITIVOS: un partido normal no aparece.")
    print("     Su AUSENCIA solo significa 'no es far-right' DENTRO de su universo")
    print(f"     declarado (paises listados, anio >= {POPULIST_ANIO_MIN}). Fuera de ahi, la")
    print("     ausencia es INDETERMINADA. Esto rompe la comparabilidad directa con POPPA.")

    # POPPA nativista pero sin id
    sin_id = (poppa[poppa.pf.isna()]
              .groupby(["country", "party_short", "party_name_english"], as_index=False)
              .nativism.mean()
              .sort_values("nativism", ascending=False))
    sin_id["nativism"] = sin_id["nativism"].round(2)
    n_nat = (sin_id.nativism >= NATIVISM_THRESHOLD).sum()
    print(f"\n-- Coste del fallo de enlace de POPPA --")
    print(f"  De los {len(sin_id)} partidos POPPA sin partyfacts_id, {n_nat} tienen "
          f"nativism >= {NATIVISM_THRESHOLD}:")
    for _, r in sin_id[sin_id.nativism >= NATIVISM_THRESHOLD].iterrows():
        print(f"    {r.nativism:>5.2f}  {r.country:<16} {r.party_name_english}")
    sin_id.to_csv(OUT / "poppa_sin_partyfacts.csv", index=False, encoding="utf-8")

    enlace = {
        "popu_sin_pf": int(len(huerfanos)),
        "popu_recuperables": recuperables,
        "poppa_sin_pf_filas": int(poppa.pf.isna().sum()),
        "poppa_sin_pf_partidos": int(len(sin_id)),
        "poppa_sin_pf_nativistas": int((sin_id.nativism >= NATIVISM_THRESHOLD).sum()),
        "popu_filas_todo_cero": int(ceros),
        "popu_filas": int(len(popu)),
        "ratio_min": float(ratio.min()),
        "ratio_max": float(ratio.max()),
    }
    return sin_id, enlace


# ═══════════════════════════════════════════════════════════════════════════════
# 2 bis. AUDITORIA DE LA CLAVE DE UNION
# ═══════════════════════════════════════════════════════════════════════════════
def _tokens(s) -> set:
    """Tokens normalizados. El plural se recorta a mano: sin eso, 'People's Party' y
    'Peoples Party' no se parecen en nada y el detector se llena de falsos positivos."""
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    out = set()
    for t in re.split(r"[^a-z0-9]+", s.lower()):
        if len(t) > 3 and t.endswith("s"):
            t = t[:-1]
        if len(t) > 2 and t not in _STOP:
            out.add(t)
    return out


def _jaccard(a, b) -> float:
    A, B = _tokens(a), _tokens(b)
    return len(A & B) / len(A | B) if (A | B) else 0.0


def auditar_clave(ned, fuente, col_nombre, col_pais, etiqueta):
    """
    Busca dos patologias del join por `partyfacts_id`:

      ENGANCHE-CRUZADO : el id de la fuente SI existe en EU-NED, pero otro partido del
                         mismo pais en EU-NED se parece mucho mas al nombre de la fuente.
                         => la etiqueta cae sobre el partido equivocado.
      ENLACE-PERDIDO   : el id de la fuente NO existe en EU-NED, pero un partido del mismo
                         pais en EU-NED tiene practicamente el mismo nombre.
                         => la etiqueta no cae sobre nadie, pudiendo caer.

    No es una prueba: es un cribado que produce falsos positivos (traducciones distintas
    del mismo partido). Lo que vale es la lista corta, revisada a mano.
    """
    nedn = (ned.dropna(subset=["pf"])
              .groupby(["country_code", "pf"], as_index=False)
              .agg(nombre_ned=("nombre", "first"), votos=("partyvote", "sum")))
    pais_cod = dict(zip(ned.country, ned.country_code))

    f = fuente.dropna(subset=["pf"]).copy()
    f["cc"] = f[col_pais].map(lambda c: pais_cod.get(ALIAS_PAIS.get(c, c)))
    f = f.dropna(subset=["cc"]).drop_duplicates("pf")

    filas = []
    for _, r in f.iterrows():
        cand = nedn[nedn.country_code == r.cc]
        if cand.empty:
            continue
        sims = cand.nombre_ned.map(lambda n: _jaccard(r[col_nombre], n))
        mejor = cand.loc[sims.idxmax()]
        sim_mejor = float(sims.max())
        propio = cand[cand.pf == r.pf]
        if len(propio):
            sim_propio = _jaccard(r[col_nombre], propio.iloc[0].nombre_ned)
            if (int(mejor.pf) != int(r.pf)
                    and sim_mejor >= SIM_MINIMA_ALTERNATIVA
                    and sim_mejor >= sim_propio + MARGEN_ENGANCHE):
                filas.append({
                    "patologia": "ENGANCHE-CRUZADO", "fuente": etiqueta, "pais": r.cc,
                    "nombre_fuente": r[col_nombre], "id_fuente": int(r.pf),
                    "engancha_en_EUNED_a": propio.iloc[0].nombre_ned, "sim_actual": round(sim_propio, 2),
                    "deberia_ser": mejor.nombre_ned, "id_correcto": int(mejor.pf),
                    "sim_mejor": round(sim_mejor, 2), "votos_del_correcto": int(mejor.votos)})
        elif sim_mejor >= SIM_ENLACE_PERDIDO:
            filas.append({
                "patologia": "ENLACE-PERDIDO", "fuente": etiqueta, "pais": r.cc,
                "nombre_fuente": r[col_nombre], "id_fuente": int(r.pf),
                "engancha_en_EUNED_a": "(id ausente de EU-NED)", "sim_actual": 0.0,
                "deberia_ser": mejor.nombre_ned, "id_correcto": int(mejor.pf),
                "sim_mejor": round(sim_mejor, 2), "votos_del_correcto": int(mejor.votos)})
    return pd.DataFrame(filas)


def bloque_auditoria_clave(ned, popu, poppa):
    titulo("2 bis. AUDITORIA DE LA CLAVE — ¿el partyfacts_id apunta al mismo partido?")
    a = auditar_clave(ned, popu, "party_name_english", "country_name", "PopuList")
    b = auditar_clave(ned, poppa.drop_duplicates("pf"), "party_name_english", "country", "POPPA")
    aud = pd.concat([a, b], ignore_index=True).sort_values("votos_del_correcto", ascending=False)
    aud.to_csv(OUT / "auditoria_clave_partyfacts.csv", index=False, encoding="utf-8")
    print(f"Cribado automatico (produce falsos positivos por traduccion; hay que revisarlo):")
    print(aud.patologia.value_counts().to_string())
    print(f"\n{aud.to_string(index=False)}")
    print("\nDos casos VERIFICADOS a mano sobre el fichero (los demas quedan por revisar):")
    print("  · N-VA (BE): EU-NED y POPPA usan pf=36; PopuList usa pf=756, que en EU-NED es")
    print("    el CD&V / cartel CD&V-N-VA. Un join ingenuo marca far-right a los")
    print("    democristianos flamencos y deja al N-VA sin marcar.")
    print("  · EKRE (EE): EU-NED y POPPA usan pf=4094; PopuList usa pf=110, que en EU-NED es")
    print("    la Union Popular de Estonia (Rahvaliit), agraria. Mismo doble error.")
    return aud


# ═══════════════════════════════════════════════════════════════════════════════
# 3. COBERTURA DE VOTO
# ═══════════════════════════════════════════════════════════════════════════════
def marcar_cobertura(ned, popu, poppa):
    """Anade a EU-NED las banderas de enlace y de veredicto."""
    ids_popu = set(popu.pf.dropna())
    ids_poppa = set(poppa.pf.dropna())

    paises_popu = {ALIAS_PAIS.get(c, c) for c in popu.country_name.unique()}

    d = ned.copy()
    d["en_popu"] = d.pf.isin(ids_popu)          # enlace explicito
    d["en_poppa"] = d.pf.isin(ids_poppa)
    # PopuList con supuesto de mundo cerrado: veredicto determinado si el pais-anio esta
    # dentro del universo declarado, aunque el partido no figure en el fichero.
    d["popu_determinado"] = d.country.isin(paises_popu) & (d.year >= POPULIST_ANIO_MIN)
    d["ambos_explicito"] = d.en_popu & d.en_poppa
    d["ambos_cerrado"] = d.popu_determinado & d.en_poppa
    d["sin_veredicto"] = ~d.en_popu & ~d.en_poppa
    return d


def tabla_cobertura(d, keys):
    """% del voto (suma de partyvote) con enlace, agregando por `keys`."""
    x = d.copy()
    for c in ["en_popu", "en_poppa", "ambos_explicito", "ambos_cerrado", "popu_determinado"]:
        x[f"v_{c}"] = x.partyvote.where(x[c], 0)
    x["v_residual"] = x.partyvote.where(x.residual, 0)
    x["v_sin_pf"] = x.partyvote.where(x.pf.isna() & ~x.residual, 0)
    g = x.groupby(keys, dropna=False)
    out = pd.DataFrame({
        "votos": g.partyvote.sum().astype("int64"),
        "PopuList_explicito_%": 100 * g.v_en_popu.sum() / g.partyvote.sum(),
        "PopuList_cerrado_%": 100 * g.v_popu_determinado.sum() / g.partyvote.sum(),
        "POPPA_%": 100 * g.v_en_poppa.sum() / g.partyvote.sum(),
        "ambas_explicito_%": 100 * g.v_ambos_explicito.sum() / g.partyvote.sum(),
        "ambas_cerrado_%": 100 * g.v_ambos_cerrado.sum() / g.partyvote.sum(),
        "residual_OTHER_%": 100 * g.v_residual.sum() / g.partyvote.sum(),
        "partido_sin_id_%": 100 * g.v_sin_pf.sum() / g.partyvote.sum(),
    })
    return out.round(1)


def bloque_cobertura(d):
    titulo("2. COBERTURA DE VOTO — ¿sobre cuanto voto hay veredicto?")
    print("Denominador = suma de partyvote (los votos efectivamente atribuidos a filas).")
    print("'explicito' = el partido figura en el fichero.")
    print("'cerrado'   = PopuList con supuesto de mundo cerrado (ausencia = no far-right)")
    print(f"              valido solo en sus paises y anio >= {POPULIST_ANIO_MIN}.\n")

    glob = tabla_cobertura(d.assign(k="TODO"), ["k", "type"])
    print("-- Global, por tipo de eleccion --")
    print(glob.to_string())

    par = d[d.type == "Parliament"].copy()
    print("\n-- Solo elecciones nacionales (Parliament) --")
    tot = tabla_cobertura(par.assign(k="TODO"), ["k"])
    print(tot.to_string())

    pais = tabla_cobertura(par, ["country_code"]).sort_values("ambas_cerrado_%")
    anio = tabla_cobertura(par, ["year"])
    pais_anio = tabla_cobertura(par, ["country_code", "year"])

    print("\n-- Por pais (Parliament), ordenado por la cobertura de las dos fuentes --")
    print(pais.to_string())
    print("\n-- Por anio (Parliament) --")
    print(anio.to_string())

    pais.to_csv(OUT / "cobertura_por_pais.csv", encoding="utf-8")
    anio.to_csv(OUT / "cobertura_por_anio.csv", encoding="utf-8")
    pais_anio.to_csv(OUT / "cobertura_pais_anio.csv", encoding="utf-8")
    return par, tot, pais, anio, pais_anio


# ═══════════════════════════════════════════════════════════════════════════════
# 4. DISCREPANCIAS ENTRE CLASIFICACIONES
# ═══════════════════════════════════════════════════════════════════════════════
def preparar_poppa(poppa, ola=None):
    """Un score por partyfacts_id. `ola`=None promedia las dos olas."""
    p = poppa.dropna(subset=["pf"])
    if ola is not None:
        p = p[p.wave == ola]
    return (p.groupby("pf")
             .agg(nombre_poppa=("party_name_english", "first"),
                  pais_poppa=("country", "first"),
                  nativism=("nativism", "mean"),
                  populism=("populism_mean", "mean"),
                  n_olas=("wave", "nunique"))
             .reset_index())


def bloque_discrepancias(par, popu, poppa, aud):
    titulo("3. DISCREPANCIAS ENTRE LAS DOS CLASIFICACIONES")

    pop_fr = (popu.dropna(subset=["pf"])
                  .sort_values("farright", ascending=False)
                  .drop_duplicates("pf")[["pf", "party_name_english", "country_name",
                                          "farright", "populist"]]
                  .rename(columns={"party_name_english": "nombre_popu"}))
    pp = preparar_poppa(poppa)

    # peso electoral de cada partido en EU-NED (solo Parliament)
    peso = (par.dropna(subset=["pf"])
              .groupby("pf")
              .agg(votos=("partyvote", "sum"),
                   pais=("country_code", "first"),
                   nombre_ned=("nombre", "first"),
                   anios=("year", lambda s: f"{s.min()}-{s.max()}"))
              .reset_index())
    total_votos = par.partyvote.sum()
    peso["pct_voto_total"] = 100 * peso.votos / total_votos

    # universo comparable: partido en EU-NED, con score POPPA, y veredicto PopuList
    # determinado (esta en el fichero, o su pais-anio cae en el universo de PopuList).
    paises_popu = {ALIAS_PAIS.get(c, c) for c in popu.country_name.unique()}
    det = (par[par.country.isin(paises_popu) & (par.year >= POPULIST_ANIO_MIN)]
           .pf.dropna().unique())

    comp = peso.merge(pp, on="pf", how="inner").merge(pop_fr, on="pf", how="left")
    comp["popu_farright"] = comp.farright.fillna(0).astype(int)
    comp["popu_en_fichero"] = comp.farright.notna()
    comp["popu_determinado"] = comp.pf.isin(det) | comp.popu_en_fichero
    comp = comp[comp.popu_determinado].copy()
    comp["poppa_nativista"] = (comp.nativism >= NATIVISM_THRESHOLD).astype(int)
    comp["desacuerdo"] = comp.popu_farright != comp.poppa_nativista
    comp["tipo"] = ""
    comp.loc[(comp.popu_farright == 1) & (comp.poppa_nativista == 0), "tipo"] = \
        "A: PopuList far-right / POPPA no nativista"
    comp.loc[(comp.popu_farright == 0) & (comp.poppa_nativista == 1) & comp.popu_en_fichero,
             "tipo"] = "B: en PopuList pero NO far-right / POPPA nativista"
    comp.loc[(comp.popu_farright == 0) & (comp.poppa_nativista == 1) & ~comp.popu_en_fichero,
             "tipo"] = "C: ausente de PopuList / POPPA nativista"

    # Un "desacuerdo" puede no serlo: si la etiqueta de PopuList se fue a otro id (ver
    # seccion 2 bis), el partido aparece como "ausente de PopuList" sin que PopuList haya
    # dicho nada de el. Se marca aparte para no contar un fallo de clave como discrepancia.
    ids_mal_enganchados = set(aud.loc[aud.fuente == "PopuList", "id_correcto"].astype(int))
    comp["alerta_clave"] = comp.pf.astype(int).isin(ids_mal_enganchados)

    n_comp = len(comp)
    n_des = int(comp.desacuerdo.sum())
    n_clave = int((comp.desacuerdo & comp.alerta_clave).sum())
    voto_des = comp.loc[comp.desacuerdo, "votos"].sum()
    print(f"Universo comparable (partido en EU-NED + score POPPA + veredicto PopuList "
          f"determinado): {n_comp} partidos")
    print(f"Desacuerdos con nativism >= {NATIVISM_THRESHOLD}: {n_des} "
          f"({100*n_des/n_comp:.1f}% de los comparables)")
    print(f"  de ellos, explicados por un FALLO DE CLAVE (seccion 2 bis): {n_clave}")
    print(f"  desacuerdos sustantivos reales                           : {n_des - n_clave}")
    print(f"Voto en juego en los desacuerdos: {voto_des:,.0f} votos = "
          f"{100*voto_des/total_votos:.2f}% del voto total de EU-NED (Parliament)")
    print(f"Acuerdan en 'es nacionalista': "
          f"{int(((comp.popu_farright==1)&(comp.poppa_nativista==1)).sum())} partidos")

    cols = ["tipo", "nombre_ned", "pais", "anios", "nativism", "populism",
            "popu_farright", "populist", "pct_voto_total", "votos", "alerta_clave"]
    des = comp[comp.desacuerdo].sort_values("votos", ascending=False)[cols].copy()
    des["nativism"] = des.nativism.round(2)
    des["populism"] = des.populism.round(2)
    des["pct_voto_total"] = des.pct_voto_total.round(3)
    des.to_csv(OUT / "discrepancias_clasificacion.csv", index=False, encoding="utf-8")

    for t in sorted(des.tipo.unique()):
        sub = des[des.tipo == t]
        print(f"\n-- {t}  ({len(sub)} partidos) --")
        print(sub.drop(columns=["tipo"]).to_string(index=False))

    # ── sensibilidad: el desacuerdo depende del umbral y de la ola ────────────────
    print("\n-- Sensibilidad: numero de desacuerdos segun umbral y ola de POPPA --")
    filas = []
    for ola in [None, "Wave 1 - 2018", "Wave 2 - 2023"]:
        ppx = preparar_poppa(poppa, ola)
        cx = peso.merge(ppx, on="pf", how="inner").merge(pop_fr, on="pf", how="left")
        cx["fr"] = cx.farright.fillna(0).astype(int)
        cx = cx[cx.pf.isin(det) | cx.farright.notna()]
        fila = {"ola": ola or "media de olas", "n_comparables": len(cx)}
        for u in NATIVISM_SENSIBILIDAD:
            nat = (cx.nativism >= u).astype(int)
            fila[f"desac_{u}"] = int((cx.fr != nat).sum())
        filas.append(fila)
    sens = pd.DataFrame(filas)
    print(sens.to_string(index=False))

    # flip entre olas al umbral central
    w1 = preparar_poppa(poppa, "Wave 1 - 2018").set_index("pf").nativism
    w2 = preparar_poppa(poppa, "Wave 2 - 2023").set_index("pf").nativism
    j = pd.concat([w1.rename("w1"), w2.rename("w2")], axis=1).dropna()
    flip = j[(j.w1 >= NATIVISM_THRESHOLD) != (j.w2 >= NATIVISM_THRESHOLD)]
    print(f"\nPartidos que CAMBIAN de lado del umbral {NATIVISM_THRESHOLD} entre las dos "
          f"olas de POPPA: {len(flip)} de {len(j)} con score en ambas")
    if len(flip):
        nom = pp.set_index("pf")[["nombre_poppa", "pais_poppa"]]
        f = flip.join(nom).round(2)
        print(f.to_string())

    return comp, des, sens, len(flip), len(j), total_votos, n_clave


# ═══════════════════════════════════════════════════════════════════════════════
# 5. PARTIDOS SIN CLASIFICAR CON MAS VOTO
# ═══════════════════════════════════════════════════════════════════════════════
def bloque_sin_clasificar(par, total_votos, n=30):
    titulo("4. PARTIDOS SIN VEREDICTO CON MAS VOTO (top 30)")
    tot_pais = par.groupby("country_code").partyvote.sum()

    sc = par[par.sin_veredicto].copy()
    # cuota nacional del partido en su mejor eleccion
    nac = (par.groupby(["country_code", "year", "pf", "nombre", "residual"], dropna=False)
             .agg(v=("partyvote", "sum"), vv=("validvote", "sum")))
    nac["cuota"] = 100 * nac.v / nac.vv

    key = ["country_code", "nombre", "residual"]
    agg = (sc.groupby(key, dropna=False)
             .agg(votos=("partyvote", "sum"),
                  anios=("year", lambda s: f"{s.min()}-{s.max()}"),
                  n_elecciones=("year", "nunique"),
                  pf=("pf", "first"))
             .reset_index())
    agg["pct_voto_pais"] = 100 * agg.votos / agg.country_code.map(tot_pais)
    agg["pct_voto_total"] = 100 * agg.votos / total_votos

    mejor = (nac.reset_index()
               .groupby(["country_code", "nombre"], dropna=False)
               .cuota.max().rename("mejor_cuota_nacional_%"))
    agg = agg.merge(mejor, on=["country_code", "nombre"], how="left")
    agg["tiene_partyfacts_id"] = agg.pf.notna()
    agg = agg.sort_values("votos", ascending=False)

    for c in ["pct_voto_pais", "pct_voto_total", "mejor_cuota_nacional_%"]:
        agg[c] = agg[c].round(2)
    agg.to_csv(OUT / "partidos_sin_clasificar.csv", index=False, encoding="utf-8")

    v_res = sc.loc[sc.residual, "partyvote"].sum()
    v_nom = sc.loc[~sc.residual, "partyvote"].sum()
    print(f"Voto sin veredicto de ninguna de las dos fuentes: "
          f"{sc.partyvote.sum():,.0f} = {100*sc.partyvote.sum()/total_votos:.1f}% del total")
    print(f"  de el, agregados residuales OTHER/OTHERS: {v_res:,.0f} "
          f"({100*v_res/total_votos:.1f}% del total)")
    print(f"  de el, partidos con nombre propio      : {v_nom:,.0f} "
          f"({100*v_nom/total_votos:.1f}% del total)")

    top = agg[~agg.residual].head(n)[
        ["nombre", "country_code", "anios", "n_elecciones", "votos",
         "pct_voto_pais", "mejor_cuota_nacional_%", "tiene_partyfacts_id"]]
    print(f"\n-- Top {n} partidos con nombre propio y SIN veredicto --")
    print(top.to_string(index=False))

    # Los que ni siquiera son enlazables: no tienen partyfacts_id en EU-NED.
    top_sin_id = agg[~agg.residual & ~agg.tiene_partyfacts_id].head(15)[
        ["nombre", "country_code", "anios", "votos", "pct_voto_pais",
         "mejor_cuota_nacional_%"]]
    print("\n-- Top 15 partidos SIN partyfacts_id en EU-NED (no enlazables ni a mano) --")
    print(top_sin_id.to_string(index=False))

    print("\n-- Los agregados residuales mas grandes (no son partidos) --")
    print(agg[agg.residual].head(8)[
        ["nombre", "country_code", "anios", "votos", "pct_voto_pais"]].to_string(index=False))

    return agg, top, sc, top_sin_id


# ═══════════════════════════════════════════════════════════════════════════════
# 6. CRITERIO DE INCLUSION — con su curva de sensibilidad
# ═══════════════════════════════════════════════════════════════════════════════
def bloque_criterio(par, pais_anio):
    titulo("5. CRITERIO DE INCLUSION Y SU SENSIBILIDAD")
    pa = pais_anio.reset_index()
    votos_tot = pa.votos.sum()
    filas = []
    for u in [50, 60, 70, 80, 85, 90, 95]:
        ok = pa[pa["ambas_cerrado_%"] >= u]
        filas.append({
            "umbral_cobertura_%": u,
            "pais_x_eleccion_incluidos": len(ok),
            "de_un_total_de": len(pa),
            "paises_incluidos": ok.country_code.nunique(),
            "% del voto retenido": round(100 * ok.votos.sum() / votos_tot, 1),
        })
    curva = pd.DataFrame(filas)
    print("Unidad = pais x eleccion. Cobertura = las DOS fuentes con veredicto")
    print("(POPPA explicito + PopuList bajo mundo cerrado).\n")
    print(curva.to_string(index=False))

    u = 80
    ok = pa[pa["ambas_cerrado_%"] >= u]
    fuera = pa[pa["ambas_cerrado_%"] < u]
    print(f"\n-- Con umbral {u}%: paises que quedan COMPLETAMENTE fuera --")
    dentro = set(ok.country_code)
    todos = set(pa.country_code)
    print(sorted(todos - dentro))
    partidos = sorted({c for c in dentro if c in set(fuera.country_code)})
    enteros = sorted(dentro - set(fuera.country_code))
    print(f"\n-- Con umbral {u}%: paises con TODAS sus elecciones dentro --")
    print(enteros)
    print(f"\n-- Con umbral {u}%: paises con elecciones partidas (algunas dentro, otras fuera) --")
    for c in partidos:
        d_in = sorted(ok[ok.country_code == c].year)
        d_out = sorted(fuera[fuera.country_code == c].year)
        print(f"  {c}: dentro {d_in} | fuera {d_out}")
    return curva, sorted(todos - dentro), partidos, enteros


# ═══════════════════════════════════════════════════════════════════════════════
# 7. INFORME
# ═══════════════════════════════════════════════════════════════════════════════
def escribir_informe(ctx):
    (tot, pais, anio, pais_anio, des, sens, comp, agg, top, curva,
     fuera_total, partidos_mixtos, sin_id, total_votos, sc, n_flip, n_ambas_olas,
     glob_tipo, enlace, aud, n_clave, top_sin_id, enteros) = ctx

    g = tot.iloc[0]
    peor = pais.iloc[0]
    # Los paises con 0% no estan "mal cubiertos": estan estructuralmente fuera de alguna
    # de las dos fuentes. El peor pais informativo es el primero con cobertura > 0.
    pais_reales = pais[pais["ambas_cerrado_%"] > 0]
    peor_real = pais_reales.iloc[0]
    fuera_estructural = list(pais[pais["ambas_cerrado_%"] == 0].index)

    n_comp = len(comp)
    n_des = int(comp.desacuerdo.sum())
    voto_des = comp.loc[comp.desacuerdo, "votos"].sum()

    md = f"""# Cobertura de la clasificacion de partidos — DIA 2

> **Generado por** `src/cobertura_partidos.py`. **Todas las cifras de este documento las
> escribe el script**: no hay ningun numero tecleado a mano. Para regenerarlo:
> `python src/cobertura_partidos.py` desde la raiz del repo.
>
> **Que responde:** el riesgo **R1** del diseno
> (`JobHunter/docs/fundamentos/observatorio-nacionalismo-regional.md`) exige reportar el voto
> nacionalista bajo **>= 2 clasificaciones independientes**. Antes hay que saber sobre cuanto
> voto existen de verdad dos veredictos. Eso es lo unico que se mide aqui: **cobertura y
> desacuerdos**. Ni modelos, ni regresiones, ni clustering.

---

## 0. El hallazgo que condiciona todo lo demas: PopuList no es un censo

Antes de leer ninguna tabla de cobertura hay que asumir esto, o todas se leen mal:

**PopuList 3.0 es una lista de SOLO-POSITIVOS.** Comprobado sobre el fichero:
**{enlace['popu_filas_todo_cero']} de sus {enlace['popu_filas']} filas tienen los cuatro flags
(populist / farright / farleft / eurosceptic) a cero**. Un partido
ordinario no aparece. Por tanto:

- **No se puede leer "% de voto cubierto por PopuList" como se lee el de POPPA.** Son cosas
  distintas: POPPA da un score graduado a cada partido que encuesto; PopuList solo nombra a los
  que marca.
- La **ausencia** de un partido en PopuList significa "no es far-right" **unicamente dentro de su
  universo declarado** (sus paises, y anio >= {POPULIST_ANIO_MIN}). Fuera de ahi la ausencia es
  **indeterminada**, no un cero.
- Por eso todas las tablas traen **dos columnas de PopuList**: `explicito` (el partido figura en
  el fichero) y `cerrado` (supuesto de mundo cerrado: ausencia = no far-right dentro del universo).
  La verdad esta entre ambas y **depende de una regla del codebook de PopuList que NO esta
  verificada**: ni el ano de inicio ({POPULIST_ANIO_MIN}, asumido) ni el bar de entrada al
  universo (escanos o % de voto) se han comprobado contra el codebook — **no hay codebook en el
  repo y el CSV no trae metadatos de cobertura**. `[pendiente-verif]` Por eso el informe no da
  nunca una sola cifra de cobertura de PopuList: da el par.

**Consecuencia inmediata para el repo:** `src/ingestion/load_euned.py` clasifica como nacionalista
al partido que cumple `nativism >= {NATIVISM_THRESHOLD}` **Y** `far-right` en PopuList. Como la
condicion `Y` exige presencia **explicita** en los dos ficheros, esa regla solo puede mirar el
**{g['ambas_explicito_%']:.1f}% del voto** (§2) y acaba marcando
**{int(((comp.popu_farright==1)&(comp.poppa_nativista==1)).sum())} partidos**. Todo lo demas —el
{100-g['ambas_explicito_%']:.1f}% restante— entra en el modelo como **no nacionalista por
defecto**, sin distinguir "medido y sale que no" de "no medido".

---

## 1. Como enlazan los ficheros (comprobado, no supuesto)

| Fichero | Identificador que trae | Enlace con EU-NED |
|---|---|---|
| `eu_ned_joint_nuts2.csv` | `partyfacts_id` | — |
| `The PopuList 3.0.csv` | `partyfacts_id` **y** `parlgov_id` | **directo** por `partyfacts_id` |
| `poppa_integrated_v2.csv` | `partyfacts_id` y `poppa_id` | **directo** por `partyfacts_id` |
| `view_party.csv` (ParlGov) | `party_id` | necesita `partyfacts-parlgov-ids.csv` |

**El puente `partyfacts-parlgov-ids.csv` no hace falta para clasificar.** Se comprobo: de las
{enlace['popu_sin_pf']} filas de PopuList sin `partyfacts_id`, el puente recupera
**{enlace['popu_recuperables']}**. POPPA no trae `parlgov_id`, asi que sus huerfanos son
**irrecuperables por identificador**.

### El coste de ese fallo de enlace

{enlace['poppa_sin_pf_partidos']} partidos de POPPA ({enlace['poppa_sin_pf_filas']} filas) no
tienen `partyfacts_id`. **{enlace['poppa_sin_pf_nativistas']} de ellos tienen
`nativism >= {NATIVISM_THRESHOLD}`** — es decir, son exactamente los partidos que un analisis de
voto nacionalista necesita, y son invisibles al join:

{md_table(sin_id[sin_id.nativism >= NATIVISM_THRESHOLD][['country', 'party_name_english', 'nativism']])}

Fichero completo: `data/processed/poppa_sin_partyfacts.csv`.

---

## 1 bis. El `partyfacts_id` NO identifica al mismo partido en los tres ficheros

Esto no estaba en el guion del dia 2 y es lo mas grave que ha salido. **Dos casos verificados a
mano contra los ficheros:**

| Partido | EU-NED | POPPA | PopuList | Que pasa al hacer el join |
|---|---|---|---|---|
| **N-VA** (Belgica) | `36` | `36` | **`756`** | En EU-NED `756` es el **CD&V / cartel CD&V-N-VA**. El flag far-right de PopuList cae sobre los **democristianos flamencos**, y el N-VA se queda sin marcar. |
| **EKRE** (Estonia) | `4094` | `4094` | **`110`** | En EU-NED `110` es la **Union Popular de Estonia** (Rahvaliit, agraria). Mismo doble error: falso positivo en una, falso negativo en la otra. |

Los dos son **falso positivo + falso negativo simultaneos**, que es la peor forma del error R1:
no anaden ruido, mueven voto de una categoria a la otra.

Un cribado automatico por parecido de nombre dentro del mismo pais encuentra
**{len(aud)} candidatos** ({int((aud.patologia=='ENGANCHE-CRUZADO').sum())} enganches cruzados +
{int((aud.patologia=='ENLACE-PERDIDO').sum())} enlaces perdidos). **Solo los dos de arriba estan
verificados**; el resto son candidatos que hay que revisar uno a uno — el cribado produce falsos
positivos cuando dos ficheros traducen distinto el mismo nombre, y ademas se le escapan casos (el
de N-VA solo salta porque EU-NED escribe el cartel con los dos nombres).

{md_table(aud[['patologia', 'fuente', 'pais', 'nombre_fuente', 'id_fuente',
               'engancha_en_EUNED_a', 'deberia_ser', 'id_correcto', 'votos_del_correcto']])}

Fichero: `data/processed/auditoria_clave_partyfacts.csv`.

---

## 2. Cobertura global del voto

Denominador: suma de `partyvote` (los votos efectivamente atribuidos a filas de EU-NED). El
chequeo `sum(partyvote) / validvote` por region-eleccion sale entre **{enlace['ratio_min']:.4f}** y
**{enlace['ratio_max']:.4f}**, asi que el denominador no distorsiona nada.

{md_table(glob_tipo.reset_index().round(1))}

**Solo elecciones nacionales (`Parliament`), que es la capa A del diseno:**

| Metrica | % del voto |
|---|---|
| Enlazado explicito con PopuList | **{g['PopuList_explicito_%']:.1f}%** |
| Con veredicto PopuList bajo mundo cerrado | **{g['PopuList_cerrado_%']:.1f}%** |
| Enlazado con POPPA | **{g['POPPA_%']:.1f}%** |
| **Enlazado con las DOS (explicito)** | **{g['ambas_explicito_%']:.1f}%** |
| **Con veredicto de las DOS (PopuList cerrado)** | **{g['ambas_cerrado_%']:.1f}%** |
| Agregados residuales `OTHER` | {g['residual_OTHER_%']:.1f}% |
| Partidos con nombre propio y sin `partyfacts_id` | {g['partido_sin_id_%']:.1f}% |

La cifra que pide el diseno ("% de voto con dos clasificaciones independientes") es por tanto
**{g['ambas_cerrado_%']:.1f}%** en la lectura generosa y **{g['ambas_explicito_%']:.1f}%** en la
literal. **Ese rango es el resultado del dia 2**, y la distancia entre sus extremos mide cuanto
del analisis descansa en un supuesto no verificado.

---

## 3. Cobertura por pais (elecciones nacionales)

{md_table(pais.reset_index())}

- **Fuera por construccion, con 0%:** {', '.join(f'`{c}`' for c in fuera_estructural)}. Turquia
  (`TR`) no esta en PopuList **ni** en POPPA; Malta (`MT`) esta en POPPA
  ({pais.loc['MT', 'POPPA_%']:.1f}%) pero **no** en PopuList, asi que su veredicto far-right es
  indeterminado. No es un problema de enlace: es que las clasificaciones no llegan ahi.
- **Peor pais realmente medido:** `{peor_real.name}` con
  **{peor_real['ambas_cerrado_%']:.1f}%**.
- Bajo el supuesto de mundo cerrado, **la restriccion que manda es POPPA**: en
  {int((pais['ambas_cerrado_%'] == pais['POPPA_%']).sum())} de los {len(pais)} paises las dos
  columnas coinciden al decimal. Toda la discusion de cobertura es, en la practica, una discusion
  sobre a quien encuesto POPPA.

---

## 4. Cobertura por anio (elecciones nacionales)

{md_table(anio.reset_index())}

**El patron dominante no es geografico, es temporal.** POPPA es una foto de las olas 2018 y 2023:
los partidos de los anos noventa no estan porque ya no existian cuando se hizo la encuesta. Por eso
la cobertura de POPPA se hunde en las elecciones antiguas y en los paises cuyo sistema de partidos
se renovo entero (Italia, Letonia, Rumania). **La unidad de exclusion correcta es
`pais x eleccion`, no `pais`.**

Detalle completo: `data/processed/cobertura_pais_anio.csv`.

---

## 5. Desacuerdos entre las dos clasificaciones

Comparacion: `farright == 1` en PopuList **vs** `nativism >= {NATIVISM_THRESHOLD}` en POPPA
(media de las dos olas). Universo comparable = partido presente en EU-NED **+** con score POPPA
**+** con veredicto PopuList determinado.

| | |
|---|---|
| Partidos comparables | **{n_comp}** |
| Desacuerdos | **{n_des}** ({100*n_des/n_comp:.1f}%) |
| — de ellos, explicados por el fallo de clave de §1 bis | {n_clave} |
| — **desacuerdos sustantivos reales** | **{n_des - n_clave}** |
| Acuerdos en "es nacionalista" | {int(((comp.popu_farright==1)&(comp.poppa_nativista==1)).sum())} |
| Voto en juego en los desacuerdos | **{100*voto_des/total_votos:.2f}%** del voto total (Parliament) |

Tipos: **A** = PopuList lo marca far-right y POPPA no lo ve nativista · **B** = esta en PopuList
pero **sin** el flag far-right, y POPPA si lo ve nativista · **C** = ausente de PopuList (o sea,
un cero implicito) y POPPA si lo ve nativista. `alerta_clave = True` significa que el
"desacuerdo" es en realidad un fallo de identificador, no una diferencia de criterio.

{md_table(des)}

**Lo que dice esta lista, que es lo que el dia 2 tenia que averiguar:** las dos fuentes **no se
contradicen de frente casi nunca** — casos de tipo A (PopuList dice far-right y POPPA dice que no):
**{int((des.tipo.str.startswith('A')).sum())}**. Se separan en **quien entra en el marco**: PopuList clasifica *far-right* y POPPA mide
*nativismo*, y hay partidos de gobierno convencionales con nativismo alto. El mayor por voto de
toda la lista es **{des.iloc[0].nombre_ned}** ({des.iloc[0].pais}), con nativismo
{des.iloc[0].nativism} y el {des.iloc[0].pct_voto_total}% del voto total de EU-NED. El desacuerdo
no es un error de nadie: **son dos constructos distintos**, y llamar "nacionalista" al resultado
de cualquiera de los dos es una decision del analista, no de los datos.

Y hay algo especialmente incomodo para **este** proyecto, que va sobre nacionalismo *regional*:
los partidos nacionalistas perifericos son justo los que caen en la zona mala. **Junts** y
**N-VA** estan en la lista de desacuerdo (el segundo, ademas, por fallo de clave), y
**EAJ-PNV** y **ERC-CATSI** ni siquiera tienen `partyfacts_id` en EU-NED (§6). El objeto de
estudio coincide con el peor sitio de la medida.

Fichero: `data/processed/discrepancias_clasificacion.csv`.

### El umbral de nativismo no es un detalle: mueve el recuento

{md_table(sens)}

Y el propio POPPA no es estable entre olas: **{n_flip} partidos de {n_ambas_olas}** con score en
ambas olas **cambian de lado del umbral {NATIVISM_THRESHOLD}** entre 2018 y 2023. Elegir la ola es
una decision metodologica con consecuencias, y hoy el repo promedia sin decirlo.

---

## 6. Partidos sin veredicto con mas voto

Voto sin veredicto de **ninguna** de las dos fuentes:
**{100*sc.partyvote.sum()/total_votos:.1f}%** del total, del cual
{100*sc.loc[sc.residual,'partyvote'].sum()/total_votos:.1f} puntos son agregados residuales
`OTHER` (no son partidos: son el resto que EU-NED no desglosa) y
{100*sc.loc[~sc.residual,'partyvote'].sum()/total_votos:.1f} puntos son **partidos con nombre
propio**.

{md_table(top)}

### Y un subconjunto peor: los que ni siquiera tienen `partyfacts_id`

Estos no se pueden enlazar **con nada**, ni a mano por id: habria que asignarles uno.

{md_table(top_sin_id)}

**Esto es un problema directo para un observatorio de nacionalismo *regional*.** En Espana el
{100 - pais.loc['ES', 'ambas_cerrado_%']:.1f}% del voto se queda sin veredicto, y la tabla de
arriba dice de quien es: **C's, ERC-CATSI, EAJ-PNV** — sin identificador — mas **Convergencia i
Unio**, que si tiene id pero no esta en ninguna de las dos clasificaciones. Los partidos
nacionalistas perifericos, que son el objeto declarado del proyecto, son justamente los peor
medidos.

Fichero completo: `data/processed/partidos_sin_clasificar.csv`.

---

## 7. ¿Es suficiente la cobertura? — conclusion honesta

**No con el diseno actual, y el problema no se arregla bajando un umbral.** Tres cosas separadas:

1. **Con la lectura literal (enlace explicito en las dos fuentes) hay dos veredictos sobre el
   {g['ambas_explicito_%']:.1f}% del voto.** Eso no sostiene nada. La regla `AND` que hoy usa
   `load_euned.py` opera sobre ese conjunto.
2. **Con el supuesto de mundo cerrado sobre PopuList la cobertura sube al
   {g['ambas_cerrado_%']:.1f}%.** Es defendible, pero es **un supuesto**, y su validez depende de
   la regla de entrada al universo de PopuList, que **no he verificado contra el codebook**.
   Mientras no se verifique, el numero honesto es el rango, no el extremo comodo.
3. **La restriccion que de verdad muerde es temporal, no geografica.** POPPA no puede clasificar
   partidos que ya no existian en 2018.

### Criterio propuesto (y es arbitrario, se dice)

**Unidad = pais x eleccion.** Se incluye si **>= 80%** del voto de esa eleccion tiene veredicto de
las dos fuentes (POPPA explicito + PopuList bajo mundo cerrado).

{md_table(curva)}

**El 80% es arbitrario.** No sale de ninguna literatura: sale de mirar la curva de arriba y elegir
el punto donde todavia queda muestra util. La unica defensa honesta es esta tabla: **publicar la
curva completa y dejar que el lector vea cuanto cambia la muestra con el corte**, exactamente como
el diseno pide reportar la dispersion entre especificaciones en vez de un numero.

Con el corte del 80%:

- **Usables enteros** (todas sus elecciones pasan): {', '.join(f'`{c}`' for c in enteros)}
- **Usables solo por elecciones** (hay que declarar cuales):
  {', '.join(f'`{c}`' for c in partidos_mixtos)}
- **Fuera completamente:** {', '.join(f'`{c}`' for c in fuera_total)}

Y una lectura que hay que decir en voz alta: **`ES` e `IT` quedan casi fuera**, y son los dos casos
paradigmaticos de nacionalismo regional en Europa occidental. Un observatorio de nacionalismo
regional que excluya Espana e Italia por cobertura no es un observatorio: es otra cosa. La salida
no es bajar el umbral, es **arreglar la clasificacion en esos dos paises a mano** antes de decidir.

### Lo que hay que hacer antes de modelar nada

1. **Auditar a mano la clave** para los partidos far-right de PopuList (§1 bis). Dos errores ya
   verificados que mueven voto de una categoria a otra; no se puede modelar sobre eso.
2. **Verificar la regla de entrada al universo de PopuList** en su codebook. Decide si la columna
   `cerrado` vale o no. Es la cifra de la que cuelga todo lo demas.
3. **Enlazar a mano los {enlace['poppa_sin_pf_nativistas']} partidos nativistas de POPPA sin
   `partyfacts_id`.** Son pocos y son los que mas pesan en el constructo.
4. **Sustituir la regla `AND` por un reporte de las dos clasificaciones por separado**, con la
   diferencia a la vista. La `AND` no es conservadora: convierte "no medido" en "no nacionalista".
5. **Declarar la ola de POPPA** en vez de promediar en silencio.
6. **Excluir `TR` siempre** y tratar `MT` como sin veredicto de PopuList.
7. **Dar `partyfacts_id` a los regionalistas espanoles** (C's, ERC-CATSI, EAJ-PNV) si el proyecto
   quiere seguir llamandose de nacionalismo regional.
"""
    (OUT / "cobertura_partidos_dia2.md").write_text(md, encoding="utf-8")
    print(f"\n[OK] Informe escrito en {OUT / 'cobertura_partidos_dia2.md'}")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ned, popu, poppa, puente, parlgov, ratio = cargar()
    sin_id, enlace = diagnostico_enlace(ned, popu, poppa, puente, parlgov, ratio)
    aud = bloque_auditoria_clave(ned, popu, poppa)
    d = marcar_cobertura(ned, popu, poppa)
    glob_tipo = tabla_cobertura(d.assign(k="TODO"), ["k", "type"])
    par, tot, pais, anio, pais_anio = bloque_cobertura(d)
    comp, des, sens, n_flip, n_ambas_olas, total_votos, n_clave = bloque_discrepancias(
        par, popu, poppa, aud)
    agg, top, sc, top_sin_id = bloque_sin_clasificar(par, total_votos)
    curva, fuera_total, partidos_mixtos, enteros = bloque_criterio(par, pais_anio)

    escribir_informe((tot, pais, anio, pais_anio, des, sens, comp, agg, top, curva,
                      fuera_total, partidos_mixtos, sin_id, total_votos, sc,
                      n_flip, n_ambas_olas, glob_tipo, enlace, aud, n_clave,
                      top_sin_id, enteros))


if __name__ == "__main__":
    main()

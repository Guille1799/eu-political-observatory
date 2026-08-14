#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests NEGATIVOS de `join_economico_electoral.py`.

Motivo de existir: una aserción que nunca ha fallado no está comprobada, está
supuesta. Aquí se corrompe el dato a propósito, caso por caso, y se exige que
el pipeline se pare. La primera versión de este fichero descubrió que dos
aserciones eran decorativas (la de conservación de votos cuadraba en falso
porque `sum()` ignora los NaN a los dos lados).

Uso:  python src/test_join_economico_electoral.py     (sale 1 si algo falla)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import join_economico_electoral as J  # noqa: E402


class Runner:
    def __init__(self) -> None:
        self.passed = 0
        self.failed = 0

    def expect_raise(self, name: str, fn, exc=(AssertionError, pd.errors.MergeError)):
        """El caso corrompido TIENE que reventar."""
        try:
            fn()
        except exc as e:
            print(f"  OK    {name} -> {type(e).__name__}: {str(e)[:70]}")
            self.passed += 1
            return
        except Exception as e:  # noqa: BLE001
            print(f"  FALLA {name}: excepcion inesperada "
                  f"{type(e).__name__}: {str(e)[:70]}")
            self.failed += 1
            return
        print(f"  FALLA {name}: NO salta -> la asercion es decorativa")
        self.failed += 1

    def expect_ok(self, name: str, fn):
        """El caso legítimo NO puede reventar (evita aserciones histéricas)."""
        try:
            fn()
        except Exception as e:  # noqa: BLE001
            print(f"  FALLA {name}: revienta sin motivo "
                  f"{type(e).__name__}: {str(e)[:70]}")
            self.failed += 1
            return
        print(f"  OK    {name} -> pasa, como debe")
        self.passed += 1


def main() -> int:
    print("Tests negativos de las aserciones duras del join\n")
    elec2 = J.load_euned()
    panel, _ = J.build_ardeco_panel()
    r = Runner()

    # --- aritmética de votos ---
    def party_over_valid():
        d = elec2.copy()
        i = d.index[0]
        d.loc[i, "partyvote"] = d.loc[i, "validvote"] + 1
        J.check_vote_arithmetic(d)
    r.expect_raise("partyvote > validvote", party_over_valid)

    def total_over_electorate():
        d = elec2.copy()
        i = d[d["electorate"].notna() & d["totalvote"].notna()].index[0]
        d.loc[i, "totalvote"] = d.loc[i, "electorate"] + 1
        J.check_vote_arithmetic(d)
    r.expect_raise("totalvote > electorate", total_over_electorate)

    def new_monotonicity_break():
        # ES no está en la línea base: una violación aquí es NUEVA y debe abortar.
        d = elec2.copy()
        i = d[(d["country_code"] == "ES") & d["totalvote"].notna()].index[0]
        d.loc[i, "validvote"] = d.loc[i, "totalvote"] + 1
        J.check_vote_arithmetic(d)
    r.expect_raise("violacion NUEVA de validvote>totalvote",
                   new_monotonicity_break)

    r.expect_ok("las violaciones de la LINEA BASE no abortan",
                lambda: J.check_vote_arithmetic(elec2))

    # --- claves ---
    def dup_key():
        d = pd.concat([elec2, elec2.head(1)], ignore_index=True)
        key = ["country_nuts", "nuts2_id", "year", "type", "party_abbreviation"]
        dup = d.duplicated(subset=key, keep=False)
        J.AUDIT.hard(not dup.any(), f"{int(dup.sum())} filas duplicadas")
    r.expect_raise("clave (pais, region, anio, tipo, partido) duplicada", dup_key)

    # --- agregación a NUTS1 ---
    def nan_partyvote():
        d = elec2.copy()
        d.loc[d.index[0], "partyvote"] = np.nan
        J.build_nuts1(d)
    r.expect_raise("partyvote con NaN (romperia la conservacion en silencio)",
                   nan_partyvote)

    r.expect_ok("agregacion NUTS1 sobre el dato real",
                lambda: J.build_nuts1(elec2))

    # --- códigos NUTS ---
    def bad_code_length():
        p = panel.copy()
        p.loc[p.index[0], "region_id"] = "XXXXX"
        derived = p["region_id"].str.len() - 2
        mis = p[p["nuts_level"].notna() & (p["nuts_level"] != derived)]
        J.AUDIT.hard(len(mis) == 0, f"{len(mis)} codigos con longitud != nivel+2")
    r.expect_raise("codigo NUTS con longitud incoherente", bad_code_length)

    def bad_country_prefix():
        d = elec2.copy()
        d.loc[d.index[0], "nuts2_id"] = "ZZ11"
        bad = d.loc[d["nuts2_id"].str[:2] != d["country_nuts"]]
        J.AUDIT.hard(len(bad) == 0, f"{len(bad)} filas con prefijo de pais malo")
    r.expect_raise("prefijo de pais != country_code normalizado",
                   bad_country_prefix)

    # --- merge ---
    def merge_would_duplicate():
        n2 = panel[panel["nuts_level"] == 2]
        p = pd.concat([panel, n2.head(3)], ignore_index=True)
        J.merge_level(elec2, p, "nuts2_id", level=2)
    r.expect_raise("ARDECO con (region, anio) repetido duplicaria el join",
                   merge_would_duplicate)

    def dup_other_level_is_harmless():
        n1 = panel[panel["nuts_level"] == 1]
        p = pd.concat([panel, n1.head(3)], ignore_index=True)
        J.merge_level(elec2, p, "nuts2_id", level=2)
    r.expect_ok("un duplicado en NUTS1 no contamina el merge de NUTS2",
                dup_other_level_is_harmless)

    print(f"\n{r.passed} correctos, {r.failed} fallos.")
    return 0 if r.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

"""Comprobadores de ACEPTACIÓN de las promesas abiertas de eu_observatory.

## Por qué existe (2026-08-20)

Se midieron 28 parejas de checkpoints consecutivos en los dos repos que más se trabajan: el
`PRÓXIMO PASO EXACTO` de uno se recogió en el siguiente el 46 % / 60 % de las veces. Y al
intentar automatizar «¿se hizo lo prometido?» fallaron CINCO instrumentos seguidos, todos por
lo mismo: preguntaban por el SIGNIFICADO de un texto.

**La regla:** una aceptación fiable pregunta por la EXISTENCIA de un artefacto nombrado o por
el EXIT CODE de un comando. Nunca por el significado de un texto. Y nace ROJA: si ya pasa el
día que se escribe, no obliga a nada.

    python scripts/aceptacion.py              # el tablero
    python scripts/aceptacion.py --verifica   # mutación: cada comprobador tiene que cambiar de color

Sin este fichero, el Stop hook `promesa_gate.py` FALLA ABIERTO en este proyecto: no puede
comprobar nada, así que deja pasar cualquier `PRÓXIMO PASO` en prosa. Existir ya es la mitad
del valor.
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

DECISION = RAIZ / "docs/decisiones/EFA_N_FACTORES.md"
RESUMEN = RAIZ / "data/processed/ess/spain/spain_efa_summary.txt"


def efa_decision():
    """Prometido el 2026-08-12: «verificar/arreglar la solución EFA — número de factores
    (paralelo/MAP, no 12), tratar los Heywood». El análisis lleva parado desde MAYO.

    Es forma DECISIÓN: el artefacto es el registro del número de factores y del método que
    lo eligió. Sin eso, «se arregló» no se puede distinguir de «se dejó igual».
    """
    if not DECISION.exists():
        return False, "no existe docs/decisiones/EFA_N_FACTORES.md: el nº de factores no está decidido"
    t = DECISION.read_text("utf-8", errors="replace")
    import re
    n = re.search(r"^n_factores:\s*(\d+)\s*$", t, re.M)
    m = re.search(r"^metodo:\s*(paralelo|MAP|paralelo\+MAP)\s*$", t, re.M)
    if not (n and m):
        return False, "el fichero existe pero le falta `n_factores: N` o `metodo: paralelo|MAP`"
    return True, "n_factores=" + n.group(1) + " por " + m.group(1)


def efa_rerun():
    """Y decidirlo no basta: hay que RE-EJECUTAR. Los outputs vivos son del 17 de mayo, o sea
    de la solución que la propia promesa dice que está mal. Se exige que el resumen sea más
    NUEVO que la decisión: es la única forma de que «existe el fichero» no valga por sí solo.
    """
    if not RESUMEN.exists():
        return False, "no existe spain_efa_summary.txt"
    if not DECISION.exists():
        return False, "no hay decisión con la que comparar (ver efa-decision)"
    if RESUMEN.stat().st_mtime <= DECISION.stat().st_mtime:
        import datetime as dt
        f = dt.date.fromtimestamp(RESUMEN.stat().st_mtime)
        return False, "el resumen es de " + str(f) + ", ANTERIOR a la decisión: no se re-ejecutó"
    return True, "re-ejecutado después de decidir"

SIN_MUTACION = {
    "efa-rerun": "exige que un fichero que YA EXISTE (spain_efa_summary.txt, de mayo) sea mas"
                 " nuevo; el verificador nunca toca ficheros existentes, y menos en data/.",
}
ARTEFACTOS = {
    "efa-decision": [(str(DECISION), "n_factores: 4" + chr(10) + "metodo: paralelo" + chr(10))],
}
COMPROBADORES = {
    "efa-decision": efa_decision,
    "efa-rerun": efa_rerun,
}

# ── MUTACIÓN: un comprobador en el que se puede confiar es uno que se ha VISTO cambiar ──
#
# Un comprobador rojo porque la promesa sigue abierta y uno rojo porque su ruta está mal son
# indistinguibles mirando el tablero — y el segundo se queda rojo para siempre, convirtiendo el
# tablero en ruido. Así que el tablero se ataca a sí mismo: fabrica el artefacto → tiene que
# ponerse VERDE → lo quita → tiene que volver a ROJO.
#
#     python scripts/aceptacion.py --verifica
#
# Nació de un pase adversarial del 2026-08-20 que encontró que el gate aceptaba comprobadores
# VERDES DE NACIMIENTO. Esto es ese pase, mecanizado, para no depender de que a alguien se le
# ocurra pedirlo.


def _verifica() -> int:
    import hashlib
    malos = []
    for nombre, fn in COMPROBADORES.items():
        if nombre in SIN_MUTACION:
            print("  " + chr(9898) + " " + nombre.ljust(24) + "sin mutar: " + SIN_MUTACION[nombre])
            continue
        artefactos = ARTEFACTOS.get(nombre)
        if not artefactos:
            malos.append((nombre, "ni ARTEFACTOS ni SIN_MUTACION: nadie ha dicho como se comprueba"))
            continue
        antes = fn()[0]
        creados = []
        try:
            for ruta, contenido in artefactos:
                p = Path(ruta)
                if p.exists():
                    continue  # jamás se toca algo que ya existe
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(contenido, encoding="utf-8")
                # Se hashea lo que QUEDA EN DISCO, no lo que creiamos escribir: en Windows
                # write_text traduce el salto de linea, el hash no cuadraba y la limpieza no
                # borraba nada. Dejo tres stubs sueltos en el repo la primera vez que corrio.
                creados.append((p, hashlib.sha256(p.read_bytes()).hexdigest()))
            despues = fn()[0]
        finally:
            for p, h in creados:
                # se borra SOLO lo que se creó aquí y SOLO si nadie lo ha tocado
                if p.exists() and hashlib.sha256(p.read_bytes()).hexdigest() == h:
                    p.unlink()
        final = fn()[0]
        if antes is not False:
            malos.append((nombre, "no estaba ROJO de partida (¿ya cumplida? entonces retírala)"))
        elif despues is not True:
            malos.append((nombre, "con su artefacto puesto NO se pone verde: está roto o mal apuntado"))
        elif final is not False:
            malos.append((nombre, "no vuelve a rojo al quitar el artefacto: no discrimina"))
        else:
            print(f"  🟢 {nombre:24} muta bien (rojo → verde → rojo)")
    for nombre, motivo in malos:
        print(f"  🔴 {nombre:24} {motivo}")
    print()
    verificados = len(COMPROBADORES) - len(malos) - len(SIN_MUTACION)
    print(f"  {verificados}/{len(COMPROBADORES) - len(SIN_MUTACION)} verificados por mutación"
          f" ({len(SIN_MUTACION)} declarados no mutables).")
    return 1 if malos else 0


def main(argv: list[str]) -> int:
    if argv and argv[0] == "--verifica":
        return _verifica()
    nombres = argv or list(COMPROBADORES)
    fallos = 0
    for n in nombres:
        fn = COMPROBADORES.get(n)
        if fn is None:
            print(f"desconocida: {n}. Conocidas: {', '.join(COMPROBADORES)}", file=sys.stderr)
            return 2
        try:
            ok, motivo = fn()
        except Exception as e:  # noqa: BLE001 — un comprobador roto es un rojo, no una excepción
            ok, motivo = False, f"el comprobador falló: {type(e).__name__}: {e}"
        print(f"  {'🟢' if ok else '🔴'} {n:24} {motivo}")
        fallos += not ok
    if not argv:
        print(f"\n  {len(nombres) - fallos}/{len(nombres)} promesas cumplidas.")
    return 1 if fallos else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

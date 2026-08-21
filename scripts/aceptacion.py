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

LINEA = RAIZ / "docs/decisiones/LINEA_ACTUAL.md"


def linea_viva():
    """El 2026-08-21 G retiró la línea EFA: «efa está descartado ya, hay un proyecto nuevo».
    La retirada, con su motivo, está en docs/decisiones/EFA_RETIRADO_2026-08-21.md.

    ⚠️ Este comprobador existe porque retirar aquellas dos dejaba el tablero VACÍO — y un
    tablero vacío NO significa «todo hecho»: significa que el Stop hook `promesa_gate.py`
    falla ABIERTO en este proyecto, o sea que cualquier PRÓXIMO PASO en prosa vuelve a colar.
    Retirar una promesa deja un agujero, no un hueco limpio. Esto lo tapa.

    Es forma DECISIÓN: pide el NOMBRE de la línea nueva por escrito. Mientras nadie la nombre,
    este repo no puede prometer nada verificable, y el rojo lo dice en voz alta.
    """
    import re
    if not LINEA.exists():
        return False, ("no existe docs/decisiones/LINEA_ACTUAL.md: la línea EFA se retiró"
                       " el 2026-08-21 y la nueva sigue sin nombrar")
    t = LINEA.read_text("utf-8", errors="replace")
    m = re.search(r"^linea:\s*(.+\S)\s*$", t, re.M)
    if not m:
        return False, "el fichero existe pero no dice `linea: <nombre>`"
    return True, "línea actual: " + m.group(1)[:60]


SIN_MUTACION = {}
ARTEFACTOS = {
    "linea-viva": [(str(LINEA), "linea: ejemplo-de-mutacion" + chr(10))],
}
COMPROBADORES = {
    "linea-viva": linea_viva,
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


def _salida_resistente() -> None:
    """El VEREDICTO no puede depender de si la consola sabe pintar un emoji.

    ⚠️ Medido el 2026-08-21, y costó revertir trabajo correcto. Ralph corrió desde un task de
    Windows —consola cp1252, no UTF-8— y este script REVENTÓ al imprimir el 🟢 con
    `UnicodeEncodeError: charmap codec can't encode '🟢'`. El crash dio código de salida
    distinto de cero, el loop lo leyó como «la aceptación sigue roja» y revirtió un commit que
    estaba PERFECTO.

    O sea: la aceptación se cumplió, y lo que falló fue IMPRIMIRLA. El instrumento tumbando la
    medida — el mismo patrón que el `GIT_DIR` en el vigilante y el campo equivocado en el token.

    `errors="replace"` conserva la codificación de la consola y degrada lo impintable a `?`. Se
    prefiere a forzar UTF-8 porque estos mensajes van llenos de acentos: forzarlo los convertiría
    a todos en basura, y aquí solo se pierde el color del círculo.
    """
    for flujo in (sys.stdout, sys.stderr):
        try:
            flujo.reconfigure(errors="replace")
        except Exception:
            pass


def main(argv: list[str]) -> int:
    _salida_resistente()
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

# Infoelectoral raw files — Spanish Ministry of the Interior

These seven `.zip` files are the **unmodified** downloads from
[Infoelectoral](https://infoelectoral.interior.gob.es/), the official electoral results portal of
the Spanish Ministry of the Interior. They are byte-for-byte what the portal serves; nothing has
been extracted, repacked, trimmed or recompressed.

## Why they live in the repository

Because without them the test suite cannot check anything. Measured on 2026-09-14, on a clean
clone with no local data: of 86 tests, **49 passed, 27 skipped and 9 errored out** — not because
the code was wrong, but because the files they read were missing. With the files present, all 86
run. A test that silently skips is a test that protects nothing, so 24.9 MB is a cheap price for a
repository that can actually be cloned and verified by someone else.

`data/raw/` (ESS microdata) and `data/processed/` stay out of the repository. This directory is
the single declared exception, and `.gitignore` opens it file by file rather than wholesale.

## Attribution

> **Origen de los datos: Ministerio del Interior.**

The Ministry of the Interior **does not participate in, sponsor or endorse** this project or the
use made here of its data.

## Terms of reuse

Reuse is authorised under the general conditions of Royal Decree 1495/2011, which develops Law
37/2007 on the reuse of public sector information, published at
[datos.gob.es/avisolegal](https://datos.gob.es/avisolegal) and referenced by the
[Infoelectoral legal notice](https://infoelectoral.interior.gob.es/es/aviso-legal/). Those
conditions authorise reuse for commercial and non-commercial purposes and expressly cover
*«la copia, difusión, modificación, adaptación, extracción, reordenación y combinación de la
información»*, including data *«en sus niveles más desagregados o "en bruto"»*.

The binding text is quoted in Spanish because that is the language in which it is published.

The five conditions it imposes, and how this directory meets them:

| condition | how it is met here |
|---|---|
| Do not distort the meaning of the information | files are unmodified; the checksums below let anyone verify it |
| Cite the source | see **Attribution** above |
| State the date the documents were last updated | see the table below |
| Do not suggest the Ministry sponsors the reuse | stated explicitly above |
| Preserve the metadata on update date and reuse terms | the specification (`FICHEROS.doc` / `.rtf`) travels **inside** each zip and has been left there untouched |

## The files

`last updated` is the most recent modification date recorded **inside** each archive by the
Ministry — note that the 2015 and 2019-04 datasets were revised as late as November 2025.

| file | bytes | last updated | SHA-256 |
|---|---:|---|---|
| `02201512_MESA.zip` | 4 899 517 | 2025-11-05 | `d99e08485e3a96d3dde369978b965e02a2e86d32675d3689e24cda3e50b64896` |
| `02201606_MESA.zip` | 5 085 820 | 2016-08-19 | `d41c21244a5810fe596bac18352fd9820ab197662ee744de87b7db08e507a5ce` |
| `02201904_MESA.zip` | 4 740 645 | 2025-11-06 | `92f2ff6c1c9a6504d6d3647fa365c64a3502d36e15440364aa94f478e7d40764` |
| `02201911_MESA.zip` | 5 752 461 | 2019-12-26 | `e7b621f295d7bf79b794941d4f11e7bcf7bd971ecbd6eb21dd4269d59926e441` |
| `02201911_MUNI.zip` |   863 207 | 2019-12-26 | `1be96a39f89be8545470b423bb1c24afb399520e6ba632890c04373c2da971d3` |
| `02201911_TOTA.zip` |   151 139 | 2019-12-26 | `3c0c97250e876560767663a3770d7f7acc52037934dfa312bae020deb7029a2b` |
| `02202307_MESA.zip` | 4 578 794 | 2023-11-10 | `e78fc231326a03cf67bbec87b7100ea0c8c46859daa1b2a631c06daaaf1717f8` |

Verify any of them with:

```bash
python -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" data/external/infoelectoral/02201911_MESA.zip
```

## Re-downloading them

`src/v2/descarga_infoelectoral.py` fetches these same files from the portal:

```bash
python src/v2/descarga_infoelectoral.py 2019 11
```

Note that the portal is not always reachable — an unanswered request from it is precisely what
made those 9 tests error out on 2026-09-14 — which is a second reason for the files to be here.

## What is deliberately absent

`especificacion/` is not versioned. Those `.doc`/`.rtf` files are extracts of the specification
that already travels inside every archive, and `src/v2/layout_infoelectoral.py` reads it from
there. Keeping only one copy means there is no second one to fall out of date.

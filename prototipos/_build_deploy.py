"""
Reconstroi a pasta deploy/ e o ZIP cronos-deploy.zip a partir do repo atual.

Inclui apenas o estritamente necessario pro Netlify:
  - index.html (redirect pro dashboard)
  - _redirects (regras Netlify)
  - .nojekyll
  - brand/design-system/
  - prototipos/telas/
  - prototipos/data/
  - prototipos/docs/

Uso:
    python prototipos/_build_deploy.py
"""
import shutil
import sys
import zipfile
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).parent.parent
DEPLOY = ROOT / "deploy"
ZIP_OUT = ROOT / "cronos-deploy.zip"

# (origem_relativa_root, destino_relativa_deploy)
COPY = [
    ("index.html",                       "index.html"),
    ("_redirects",                        "_redirects"),
    (".nojekyll",                         ".nojekyll"),
    ("brand/design-system",               "brand/design-system"),
    ("prototipos/telas",                  "prototipos/telas"),
    ("prototipos/data",                   "prototipos/data"),
    ("prototipos/docs",                   "prototipos/docs"),
]


def main():
    # limpa
    if DEPLOY.exists():
        shutil.rmtree(DEPLOY)
    if ZIP_OUT.exists():
        ZIP_OUT.unlink()
    DEPLOY.mkdir(parents=True)

    print(f"  Construindo deploy/ em {DEPLOY}...")
    for src_rel, dst_rel in COPY:
        src = ROOT / src_rel
        dst = DEPLOY / dst_rel
        if not src.exists():
            print(f"     [SKIP] {src_rel} nao encontrado")
            continue
        if src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dst)
        print(f"     + {src_rel}")

    # zipa com forward slash (compativel com Netlify Linux)
    print(f"\n  Criando ZIP {ZIP_OUT.name}...")
    with zipfile.ZipFile(ZIP_OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for f in DEPLOY.rglob("*"):
            if f.is_file():
                z.write(f, arcname=f.relative_to(DEPLOY).as_posix())

    size_kb = ZIP_OUT.stat().st_size / 1024
    print(f"  ZIP: {size_kb:.1f} KB")
    print(f"\n  Pronto. Arrasta {ZIP_OUT.name} no painel Deploys do Netlify.")


if __name__ == "__main__":
    main()

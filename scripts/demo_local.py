# -*- coding: utf-8 -*-
"""Sobe o painel para a demonstração ao vivo, sem depender de rede.

Feito para a banca: um comando, nenhuma variável de ambiente para lembrar, e o
custo de partida pago ANTES de alguém estar olhando. A primeira requisição
custa cerca de 6,5 segundos, porque importa o pandas e carrega o parquet; este
script paga esse tempo no aquecimento e só então libera o endereço.

Roda com DEBUG desligado de propósito. Com DEBUG ligado, um erro qualquer
imprime a página amarela de rastreamento na tela compartilhada, o que numa
banca é pior que a falha em si. O whitenoise serve o estático coletado.

Uso:
    .venv/Scripts/python.exe scripts/demo_local.py
    .venv/Scripts/python.exe scripts/demo_local.py --porta 9000

Depois abra http://127.0.0.1:8000/ no navegador.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from threading import Thread

RAIZ = Path(__file__).resolve().parent.parent
WEBAPP = RAIZ / "webapp"
ABAS = ["/", "/previsao/", "/projecao/", "/fila/", "/saude/", "/causas/"]


def prepara(porta: int) -> None:
    sys.path.insert(0, str(WEBAPP))
    os.chdir(WEBAPP)
    os.environ["DJANGO_SETTINGS_MODULE"] = "cronos.settings"
    os.environ["CRONOS_DEBUG"] = "0"
    os.environ["CRONOS_HOSTS"] = "127.0.0.1,localhost"
    os.environ.setdefault("CRONOS_DADOS", str(RAIZ / "data" / "app"))


def coleta_estatico() -> None:
    """Roda collectstatic só se o manifest estiver faltando ou velho."""
    from django.conf import settings
    from django.core.management import call_command

    manifest = Path(settings.STATIC_ROOT) / "staticfiles.json"
    fontes = list((WEBAPP / "painel" / "static").rglob("*"))
    mais_nova = max((f.stat().st_mtime for f in fontes if f.is_file()), default=0)

    if manifest.exists() and manifest.stat().st_mtime >= mais_nova:
        print("estático já coletado e atualizado")
        return
    print("coletando o estático...")
    call_command("collectstatic", interactive=False, verbosity=0)


def aquece(porta: int) -> None:
    """Bate em cada aba para pagar o custo de partida antes da apresentação."""
    print("\naquecendo, isto paga os ~6,5s de carga do parquet:")
    for rota in ABAS:
        url = f"http://127.0.0.1:{porta}{rota}"
        t0 = time.time()
        for tentativa in range(40):
            try:
                with urllib.request.urlopen(url, timeout=30) as r:
                    codigo, tamanho = r.status, len(r.read())
                break
            except (urllib.error.URLError, ConnectionError):
                time.sleep(0.25)
        else:
            print(f"  FALHOU  {rota}  (servidor não respondeu)")
            continue
        marca = "ok" if codigo == 200 else f"HTTP {codigo}"
        print(f"  {marca:>7}  {rota:12s} {tamanho:>8,} bytes  {time.time() - t0:.2f}s")

    print(f"\n{'=' * 58}")
    print(f"  PRONTO PARA A DEMONSTRAÇÃO   http://127.0.0.1:{porta}/")
    print(f"{'=' * 58}")
    print("  Ordem sugerida de cliques: Panorama, Previsão, Projeção,")
    print("  Fila de risco, Saúde por produto, Causas.")
    print("  Ctrl+C encerra.\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--porta", type=int, default=8000)
    args = ap.parse_args()

    prepara(args.porta)
    import django

    django.setup()
    coleta_estatico()

    Thread(target=aquece, args=(args.porta,), daemon=True).start()

    from django.core.management import call_command

    # --noreload porque o autoreload derruba o processo se um arquivo for tocado
    # durante a apresentação, e o cache aquecido iria junto
    call_command("runserver", f"127.0.0.1:{args.porta}", use_reloader=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

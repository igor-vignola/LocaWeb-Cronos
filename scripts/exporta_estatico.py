# -*- coding: utf-8 -*-
"""Exporta o painel Django como site estático, para publicar no GitHub Pages.

A aplicação é determinística: o relógio está parado em 01/10/2025 15h, os dados
são três arquivos fixos em data/app/ e nenhuma rota grava nada. Então o HTML
renderizado hoje é o mesmo de sempre, e não há por que manter um servidor no ar
só para servi-lo.

O que ele faz:
  1. roda collectstatic para uma pasta dentro do destino
  2. renderiza as seis abas com o test client do Django
  3. varre o HTML gerado procurando link de modal (/detalhe/...) e busca.json,
     renderiza cada um e repete até não achar rota nova
  4. reescreve todo caminho absoluto para relativo, para o site abrir tanto em
     file:// quanto num subdiretório do GitHub Pages

Uso:
    .venv/Scripts/python.exe scripts/exporta_estatico.py [destino]

Destino padrão: app/ na raiz do repositório.
"""
from __future__ import annotations

import os
import re
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
WEBAPP = RAIZ / "webapp"
ROTAS_INICIAIS = ["/", "/previsao/", "/projecao/", "/fila/", "/saude/", "/causas/"]
# href e src que apontam para a raiz do site
ABSOLUTO = re.compile(r'((?:href|src|action)=")(/[^"]*)"')
# STATIC_URL do projeto é 'estatico/', relativo. Numa página em subdiretório isso
# vira /previsao/estatico/..., que não existe, então precisa de ../ por nível.
ESTATICO_REL = re.compile(r'((?:href|src)=")(estatico/[^"]*)"')
# rotas que os templates montam para os modais
LINK_INTERNO = re.compile(r'"(/(?:detalhe/[^"]*|busca\.json[^"]*))"')
# os modais não são link: o JS monta a URL a partir destes dois atributos
GATILHO_MODAL = re.compile(r'data-mod="([^"]+)"[^>]*data-k="([^"]*)"')
GATILHO_INVERSO = re.compile(r'data-k="([^"]*)"[^>]*data-mod="([^"]+)"')


def prepara_django() -> None:
    """Configura o Django para renderizar com os estáticos resolvidos por manifest."""
    sys.path.insert(0, str(WEBAPP))
    os.environ["DJANGO_SETTINGS_MODULE"] = "cronos.settings"
    os.environ["CRONOS_DEBUG"] = "0"
    os.environ["CRONOS_HOSTS"] = "*"
    os.environ.setdefault("CRONOS_DADOS", str(RAIZ / "data" / "app"))

    import django

    django.setup()


def caminho_de(rota: str) -> Path:
    """Traduz uma rota em arquivo. Diretório com index.html, para a URL ficar limpa."""
    limpa = rota.split("?")[0].strip("/")
    if not limpa:
        return Path("index.html")
    if limpa.endswith(".json"):
        return Path(limpa)
    return Path(limpa) / "index.html"


def relativiza(html: str, profundidade: int) -> str:
    """Troca caminho absoluto por relativo, contando quantos níveis subir."""
    prefixo = "../" * profundidade if profundidade else ""

    def troca(m: re.Match) -> str:
        atributo, alvo = m.group(1), m.group(2)
        if alvo.startswith("//"):
            return m.group(0)
        resto = alvo.lstrip("/")
        if not resto:
            destino = f"{prefixo}index.html" if prefixo else "index.html"
        elif resto.endswith((".json", ".css", ".js", ".svg", ".png", ".woff2")):
            destino = prefixo + resto
        else:
            destino = prefixo + resto.rstrip("/") + "/index.html"
        return f'{atributo}{destino}"'

    html = ABSOLUTO.sub(troca, html)

    if prefixo:
        html = ESTATICO_REL.sub(lambda m: f"{m.group(1)}{prefixo}{m.group(2)}\"", html)

    # o JS do modal monta a URL sozinho, então recebe a base por variável global
    base = f'<script>window.CRONOS_BASE="{prefixo}";</script>'
    return html.replace("</head>", base + "</head>", 1)


def patch_js(estatico: Path) -> int:
    """Faz o fetch do modal respeitar a base relativa, em vez de partir da raiz.

    O arquivo tem hash no nome (manifest storage), então procura por padrão.
    """
    trocados = 0
    alvo = "await fetch(`/detalhe/"
    novo = "await fetch(`${window.CRONOS_BASE||''}detalhe/"
    for js in estatico.rglob("cronos*.js"):
        texto = js.read_text(encoding="utf-8")
        if alvo in texto:
            js.write_text(texto.replace(alvo, novo), encoding="utf-8")
            trocados += 1
    return trocados


def main() -> int:
    destino = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "app"
    if destino.exists():
        shutil.rmtree(destino)
    destino.mkdir(parents=True)

    prepara_django()

    from django.core.management import call_command
    from django.test import Client

    print("collectstatic...")
    call_command("collectstatic", interactive=False, verbosity=0, clear=True)
    # STATIC_ROOT é fixo em webapp/estatico, então copia de lá para o destino
    origem_estatico = WEBAPP / "estatico"
    estatico = destino / "estatico"
    shutil.copytree(origem_estatico, estatico)
    print(f"  {sum(1 for _ in estatico.rglob('*') if _.is_file())} arquivos estáticos")

    cliente = Client()
    pendentes = list(ROTAS_INICIAIS)
    vistas: set[str] = set()
    falhas: list[tuple[str, int]] = []

    while pendentes:
        rota = pendentes.pop(0)
        if rota in vistas:
            continue
        vistas.add(rota)

        resposta = cliente.get(rota, HTTP_HOST="igor-vignola.github.io")
        if resposta.status_code != 200:
            falhas.append((rota, resposta.status_code))
            print(f"  FALHOU {resposta.status_code}  {rota}")
            continue

        corpo = resposta.content.decode("utf-8", "replace")
        # descobre modal e endpoint que os templates linkam
        for achado in LINK_INTERNO.findall(corpo):
            if achado not in vistas:
                pendentes.append(achado)
        # e os modais, que não são link nenhum: o JS os monta de data-mod e data-k
        for mod, chave in GATILHO_MODAL.findall(corpo):
            rota_modal = f"/detalhe/{mod}/{chave}/"
            if rota_modal not in vistas:
                pendentes.append(rota_modal)
        for chave, mod in GATILHO_INVERSO.findall(corpo):
            rota_modal = f"/detalhe/{mod}/{chave}/"
            if rota_modal not in vistas:
                pendentes.append(rota_modal)

        alvo = destino / caminho_de(rota)
        alvo.parent.mkdir(parents=True, exist_ok=True)
        profundidade = len(caminho_de(rota).parts) - 1
        if alvo.suffix == ".json":
            alvo.write_text(corpo, encoding="utf-8")
        else:
            alvo.write_text(relativiza(corpo, profundidade), encoding="utf-8")
        print(f"  ok  {rota}  ->  {alvo.relative_to(destino)}")

    print(f"\n{patch_js(estatico)} arquivo(s) de JS ajustado(s) para base relativa")
    print(f"{len(vistas) - len(falhas)} páginas escritas em {destino}")
    if falhas:
        print(f"{len(falhas)} falharam:")
        for rota, codigo in falhas:
            print(f"  {codigo}  {rota}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

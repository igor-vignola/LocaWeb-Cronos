# -*- coding: utf-8 -*-
"""Monta o .zip da entrega final (Sprint 4).

Escopo diferente do `monta_zip_entrega.py`, que levava só o .pptx e os sete notebooks.
O enunciado da Sprint 4 pede **todos os códigos-fonte**, mais as imagens usadas, os dados
tratados, o PPT final e um .txt com o link do vídeo e a identificação da equipe. Então
aqui o pacote varre o repositório inteiro e recorta o que é fonte, não o que é saída
regenerável.

O que entra:

    EC_Sprint_4_...pptx                 o PPT final (localizado por glob)
    Informacoes_Finais_...xlsx          a planilha oficial preenchida
    INFORMACOES_DA_ENTREGA.txt          gerado aqui: vídeo, equipe, RMs
    README.md
    requirements.txt                    ambiente de análise e modelagem
    notebooks/0*.ipynb                  os sete notebooks com as saídas preservadas
    notebooks/figures/**                as figuras que o deck e os notebooks exibem
    webapp/**                           a aplicação Django, inclusive o Dockerfile
    scripts/**/*.py                     o pipeline de dados e os geradores de deck
    data/interim/*.parquet              as bases tratadas
    data/app/**                         o pacote agregado que o contêiner lê
    prototipos/**                       só as fontes de texto (HTML, CSS, JS, PY, MD, SVG)

O que fica de fora, e por quê:

    .venv/ .git/ __pycache__/           ambiente e histórico, não são fonte
    webapp/estatico/                    saída do collectstatic, regerada no build
    png/ _png/ _r5/ _r5antes/ _rev/     PNG de conferência dos slides: são renderizações
    _chk/ screenshots/                  do HTML ao lado, cerca de 91 MB de puro derivado
    *.bak *.orig *.rej _tmp_* ~$*       rascunho de editor e temporário
    qualquer arquivo acima de 50 MB     limite declarado, para o pacote subir no portal

Antes de rodar, preencher LINK_VIDEO com a URL pública do YouTube. O script recusa montar
o pacote sem ela, porque o .txt do link é item explícito do enunciado e é o tipo de coisa
que passa batido na pressa da entrega.

Uso:
    .venv/Scripts/python scripts/monta_zip_sprint4.py --simular    # lista, não escreve
    .venv/Scripts/python scripts/monta_zip_sprint4.py              # escreve o .zip
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DESTINO = RAIZ / "sprints" / "EC_Sprint_4_2TSCOA_SolucaoFinal_Cronos_SuperDataBros.zip"
PLANILHA = RAIZ / "sprints" / "Informacoes_Finais_Projeto_Integrantes_Cronos_SuperDataBros.xlsx"

# Preencher antes de rodar: URL pública do vídeo pitch no YouTube.
LINK_VIDEO = ""

EQUIPE = "Super Data Bros"
TURMA = "2TSCOA"
PROJETO = "Cronos"
# ordem alfabética, como o enunciado exige
INTEGRANTES = [
    ("RM561310", "Ana Beatriz Costa de Oliveira"),
    ("RM565063", "Hygor Abrantes"),
    ("RM561428", "Igor Vignola (representante do grupo)"),
]

LIMITE_BYTES = 50 * 1024 * 1024

# Diretório com qualquer um destes nomes no caminho não entra.
DIRS_FORA = {
    ".venv", ".git", "__pycache__", ".ipynb_checkpoints", ".claude", "node_modules",
    "estatico",                                    # saída do collectstatic
    "png", "_png", "_r5", "_r5antes", "_rev", "_chk", "screenshots",  # renders de slide
}
SUFIXOS_FORA = (".pyc", ".pyo", ".bak", ".orig", ".rej")
NOMES_FORA = {"Thumbs.db", ".DS_Store", "desktop.ini"}
PREFIXOS_FORA = ("~$", "_tmp_")

# Em prototipos/ entra só fonte de texto: o resto da pasta é imagem derivada.
TEXTO = {".html", ".css", ".js", ".py", ".json", ".md", ".svg"}


def vetado(caminho: Path) -> bool:
    """True se o arquivo cai em alguma regra de exclusão."""
    relativo = caminho.relative_to(RAIZ)
    if any(parte in DIRS_FORA for parte in relativo.parts):
        return True
    if caminho.name in NOMES_FORA or caminho.name.startswith(PREFIXOS_FORA):
        return True
    return caminho.suffix.lower() in SUFIXOS_FORA


def varre(pasta: Path, extensoes: set[str] | None = None) -> list[Path]:
    """Arquivos de `pasta`, recursivo, já filtrados. Ordem estável."""
    achados = []
    for caminho in pasta.rglob("*"):
        if not caminho.is_file() or vetado(caminho):
            continue
        if extensoes and caminho.suffix.lower() not in extensoes:
            continue
        achados.append(caminho)
    return sorted(achados)


def acha_pptx() -> Path:
    """O .pptx da Sprint 4, qualquer que seja a grafia que o builder usou."""
    candidatos = sorted((RAIZ / "sprints").glob("EC_Sprint_4_*.pptx"))
    candidatos = [c for c in candidatos if not c.name.startswith("~$")]
    if not candidatos:
        raise FileNotFoundError(
            "nenhum EC_Sprint_4_*.pptx em sprints/. O deck da Sprint 4 precisa estar "
            "gerado antes de montar o pacote."
        )
    if len(candidatos) > 1:
        nomes = ", ".join(c.name for c in candidatos)
        raise FileNotFoundError(f"mais de um .pptx da Sprint 4 em sprints/: {nomes}")
    return candidatos[0]


def texto_informacoes() -> str:
    """Conteúdo do .txt que o enunciado pede junto do pacote."""
    linhas = [
        "CHALLENGE FIAP 2026 com Locaweb · Sprint 4 · Solução Final",
        "",
        f"Projeto: {PROJETO}",
        f"Equipe: {EQUIPE}",
        f"Turma: {TURMA}",
        "",
        f"Vídeo pitch (YouTube, acesso público): {LINK_VIDEO}",
        "",
        "Integrantes, em ordem alfabética:",
    ]
    linhas += [f"  {rm} · {nome}" for rm, nome in INTEGRANTES]
    linhas += ["", "Repositório público: https://github.com/igor-vignola/LocaWeb-Cronos", ""]
    return "\n".join(linhas)


def coleta() -> tuple[list[tuple[Path, str]], list[tuple[str, str]]]:
    """Devolve (arquivos em disco com o caminho dentro do zip, conteúdos gerados aqui)."""
    pptx = acha_pptx()
    if not PLANILHA.exists():
        raise FileNotFoundError(
            f"{PLANILHA.name} não existe em sprints/. A planilha oficial preenchida é "
            "item da entrega e vai dentro do pacote."
        )
    leiame = RAIZ / "README.md"
    if not leiame.exists():
        raise FileNotFoundError("README.md não existe na raiz do repositório.")

    # Itens nomeados: entram sempre, e o tamanho de cada um é reportado.
    itens: list[tuple[Path, str]] = [
        (pptx, pptx.name),
        (PLANILHA, PLANILHA.name),
        (leiame, "README.md"),
        (RAIZ / "requirements.txt", "requirements.txt"),
    ]

    # Varreduras: sujeitas às exclusões e ao limite de tamanho.
    varreduras: list[Path] = []
    varreduras += sorted((RAIZ / "notebooks").glob("0*.ipynb"))
    varreduras += varre(RAIZ / "notebooks" / "figures")
    varreduras += varre(RAIZ / "webapp")
    varreduras += varre(RAIZ / "scripts", {".py"})
    varreduras += sorted((RAIZ / "data" / "interim").glob("*.parquet"))
    varreduras += varre(RAIZ / "data" / "app")
    varreduras += varre(RAIZ / "prototipos", TEXTO)

    for caminho in varreduras:
        if vetado(caminho):
            continue
        if caminho.stat().st_size > LIMITE_BYTES:
            print(f"  fora, acima de 50 MB: {caminho.relative_to(RAIZ).as_posix()}")
            continue
        itens.append((caminho, caminho.relative_to(RAIZ).as_posix()))

    gerados = [("INFORMACOES_DA_ENTREGA.txt", texto_informacoes())]
    return itens, gerados


def relatorio(itens: list[tuple[Path, str]]) -> None:
    """Resumo por área, para conferir o pacote sem abrir o zip."""
    areas: dict[str, list[int]] = {}
    for caminho, dentro in itens:
        area = dentro.split("/")[0] if "/" in dentro else "(raiz)"
        registro = areas.setdefault(area, [0, 0])
        registro[0] += 1
        registro[1] += caminho.stat().st_size
    print()
    for area in sorted(areas):
        qtd, tam = areas[area]
        print(f"  {area:24} {qtd:4} arquivos  {tam / 1e6:8.2f} MB")
    total = sum(v[1] for v in areas.values())
    print(f"  {'TOTAL sem compressão':24} {len(itens):4} arquivos  {total / 1e6:8.2f} MB")


def main() -> None:
    simular = "--simular" in sys.argv

    if not LINK_VIDEO and not simular:
        raise SystemExit(
            "LINK_VIDEO está vazio. Preencha a constante no topo deste arquivo com a URL\n"
            "pública do vídeo pitch no YouTube e rode de novo. O .txt com esse link é\n"
            "item explícito da entrega da Sprint 4.\n"
            "Para só conferir o conteúdo do pacote: --simular"
        )

    itens, gerados = coleta()
    relatorio(itens)

    if simular:
        print()
        print(f"simulação: nada foi escrito. Destino seria {DESTINO.name}")
        if not LINK_VIDEO:
            print("atenção: LINK_VIDEO ainda está vazio.")
        return

    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(DESTINO, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for caminho, dentro in itens:
            z.write(caminho, dentro)
        for dentro, conteudo in gerados:
            z.writestr(dentro, conteudo.encode("utf-8"))

    print()
    print(f"{DESTINO.name}: {len(itens) + len(gerados)} arquivos, "
          f"{DESTINO.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()

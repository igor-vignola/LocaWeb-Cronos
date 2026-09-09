# -*- coding: utf-8 -*-
"""Gera a comparação das três variantes do marcador de quem apresenta.

Usa um slide REAL do deck como tela (o do problema), para a decisão ser tomada
sobre o que vai ao ar e não sobre um exemplo inventado.

    A  foto redonda de 22px mais o primeiro nome, no rodapé à esquerda
    B  só texto, na tipografia de rodapé que já existe
    C  os três retratos no topo, o ativo destacado e os outros apagados
       (mostra de quem é a vez E quem vem depois)

Uso:
    .venv/Scripts/python.exe prototipos/slides/ao-vivo/_comparar_marcador.py
"""
from __future__ import annotations

import re
from pathlib import Path

AQUI = Path(__file__).parent
VIDEO = AQUI.parent / "video"
FOTOS = "../../../brand/equipe"

CSS_MARCADOR = """
/* ══ o marcador de quem apresenta, três tratamentos para comparar ══ */

/* A · foto redonda mais o primeiro nome, no rodapé */
.mk-a{display:inline-flex;align-items:center;gap:9px;text-transform:none;letter-spacing:0;
  font-size:13px;font-weight:500;color:var(--tx2)}
.mk-a img{width:22px;height:22px;border-radius:50%;object-fit:cover;
  box-shadow:0 0 0 1px var(--line),0 2px 6px -2px rgba(15,23,42,.25)}
.mk-a b{font-weight:700;color:var(--head)}

/* B · só texto, na tipografia de rodapé que já existe */
/* nenhuma regra própria: herda .ft */

/* C · os três no topo, o ativo destacado. Mostra a vez e o próximo. */
.mk-c{display:flex;align-items:center;gap:7px;margin-left:auto;margin-right:14px}
.mk-c figure{position:relative;width:30px;height:30px;border-radius:50%;overflow:hidden;
  filter:grayscale(1);opacity:.32;transition:none}
.mk-c figure img{width:100%;height:100%;object-fit:cover;display:block}
.mk-c figure.on{filter:none;opacity:1;box-shadow:0 0 0 2px var(--accent),0 0 0 4px #fff}
.mk-c .nm{font-size:12.5px;font-weight:700;color:var(--head);letter-spacing:-.1px;
  margin-left:4px}
"""

# marcador A e B entram no rodapé; C entra no cabeçalho, antes da pílula
MARCADOR_A = (
    f'<span class="mk-a"><img src="{FOTOS}/igor.png" alt="">'
    f'<b>Igor</b> apresenta</span>'
)
MARCADOR_B = '<span>Apresenta &middot; Igor Vignola</span>'
MARCADOR_C = (
    '<span class="mk-c">'
    f'<figure class="on"><img src="{FOTOS}/igor.png" alt="Igor Vignola"></figure>'
    f'<figure><img src="{FOTOS}/ana-beatriz.png" alt="Ana Beatriz Costa de Oliveira"></figure>'
    f'<figure><img src="{FOTOS}/hygor.png" alt="Hygor Abrantes"></figure>'
    '<span class="nm">Igor</span></span>'
)

LEGENDAS = {
    "a": "A · foto redonda mais o primeiro nome, no rodapé à esquerda",
    "b": "B · só texto, na tipografia de rodapé que já existe",
    "c": "C · os três no topo, o ativo destacado e os outros apagados",
}


def reancora(texto: str) -> str:
    """De blocos/ (quatro níveis) para ao-vivo/ (três), tira um ../ dos caminhos."""
    return re.sub(r'((?:src|href)=")\.\./', r"\1", texto)


def resolve_contadores(texto: str) -> str:
    """Escreve o valor final onde o contador espera o JS.

    Sem isto a página mostra 0 no lugar de 42 e 206, e a comparação do marcador
    passa a competir com um número errado na tela.
    """
    return re.sub(
        r'(<span class="ct"[^>]*data-to="([^"]+)"[^>]*>)[^<]*(</span>)',
        lambda m: m.group(1) + m.group(2) + m.group(3),
        texto,
    )


def main() -> int:
    estilo = (VIDEO / "_estilo.css").read_text(encoding="utf-8")
    bloco = (VIDEO / "blocos" / "02-problema.html").read_text(encoding="utf-8")

    css_bloco = "\n".join(re.findall(r"<style>(.*?)</style>", bloco, re.S))
    secao = re.search(r'(<section class="slide.*?</section>)', bloco, re.S).group(1)
    secao = resolve_contadores(reancora(secao))
    css_bloco = reancora(css_bloco)

    partes = []
    for chave, marcador, no_topo in [
        ("a", MARCADOR_A, False),
        ("b", MARCADOR_B, False),
        ("c", MARCADOR_C, True),
    ]:
        s = secao.replace('class="slide', 'class="is-active slide', 1)
        if no_topo:
            # entra antes da pílula do canto direito
            s = s.replace('<div class="tag">', marcador + '\n    <div class="tag">', 1)
        else:
            # substitui o primeiro item do rodapé
            s = re.sub(r'(<div class="ft">)\s*<span>.*?</span>', r"\1" + marcador, s, count=1, flags=re.S)
        partes.append(
            f'<p class="rot">{LEGENDAS[chave]}</p>\n'
            f'<div class="palco" id="v-{chave}"><div class="stage">{s}</div></div>'
        )

    html = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<title>Marcador de quem apresenta · três variantes</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600\
&family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
{estilo}
{css_bloco}
{CSS_MARCADOR}
/* a página de comparação, não o slide */
body{{background:#2A2F38;overflow:auto;padding:34px 0 60px}}
.palco{{width:1600px;height:900px;position:relative;overflow:hidden;margin:0 auto 46px;
  box-shadow:0 30px 90px -40px rgba(0,0,0,.7)}}
.palco .stage{{position:absolute;inset:0}}
.rot{{width:1600px;margin:0 auto 12px;color:#fff;font-family:var(--mono);font-size:14px;
  letter-spacing:.3px}}
.slide{{animation:none !important}}
/* o .mesh fica de fora do congelamento: travado no fim da deriva ele desenha um
   retangulo claro no meio do slide, que nao existe na peca real */
.mesh{{animation:none !important;transform:none !important}}
.is-active *:not(.mesh){{animation-duration:.01ms !important;animation-delay:0ms !important}}
</style></head><body>
{chr(10).join(partes)}
</body></html>
"""
    saida = AQUI / "_comparar-marcador.html"
    saida.write_text(html, encoding="utf-8")
    print(f"{saida.name} escrito, {len(html) // 1024} KB, 3 variantes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

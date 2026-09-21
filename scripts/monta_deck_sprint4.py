# -*- coding: utf-8 -*-
"""Monta o deck da Sprint 4 sobre o deck da banca de 15/09/2026.

Uma lista ORDEM de 59 itens, seis tipos:
  ("banca", n, nome)        slide n de prototipos/slides/ao-vivo/blocos/, byte a byte
  ("pitch", "objetivo", .)  o slide próprio do vídeo pitch, versão A
  ("bloco", nome, nome)     bloco novo em prototipos/slides/sprint4/blocos/NN-nome.html;
                            se o arquivo não existe, vira slide de espera "Aqui irá ficar"
  ("div", n_bloco, nome)    divisória de bloco do template, gerada de um molde
  ("tela", chave, nome)     captura da aplicação na forma A, com balões (deck_sprint4_telas)
  ("arquivo", Path, nome)   HTML pronto da Sprint 3, renderizado onde está

Cada slide vira um HTML autônomo em sprint4/_build/, fotografado em 1600x900 a 2x com a
animação congelada no estado final, e entra no .pptx com a fala nas notas. O deck.html é
um visualizador das imagens, para o Igor revisar com as setas.

Uso:
    .venv/Scripts/python scripts/monta_deck_sprint4.py            # tudo
    .venv/Scripts/python scripts/monta_deck_sprint4.py --so 5 6   # só renderiza as posições 5 e 6
"""
from __future__ import annotations

import html as _html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from deck_sprint4_telas import TELAS, html_tela, nota_tela  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
SLIDES = RAIZ / "prototipos" / "slides"
AO_VIVO = SLIDES / "ao-vivo"
PITCH = SLIDES / "pitch"
ABERTURA = SLIDES / "mvp" / "abertura"
SAIDA = SLIDES / "sprint4"
BLOCOS = SAIDA / "blocos"
BUILD = SAIDA / "_build"
PNG = SAIDA / "_png"
VIEWER = SAIDA / "deck.html"
PPTX = RAIZ / "sprints" / "EC_Sprint_4_2TSCOA_SolucaoFinal_Cronos_SuperDataBros.pptx"
CHROME = (r"C:\Users\igor.vignola\AppData\Local\ms-playwright"
          r"\chromium-1217\chrome-win64\chrome.exe")

URL_APP = "igor-vignola.github.io/LocaWeb-Cronos"
URL_VIDEO = "youtu.be/IeWLVBD0Jas"
REPO = "github.com/igor-vignola/LocaWeb-Cronos"

FONTES = ('<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600'
          '&family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">')
LOGO_CLARO = ('<svg viewBox="0 0 28 28" fill="none"><path d="M6 22L12 14L16 17L22 8" stroke="#fff" '
              'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="22" cy="8" '
              'r="3" stroke="#3B82F6" stroke-width="1.5"/><circle cx="22" cy="8" r="1.2" fill="#3B82F6"/></svg>')
LOGO_ESCURO = LOGO_CLARO.replace('stroke="#fff"', 'stroke="#0A0E17"').replace("#3B82F6", "#2563EB")

RE_STYLE = re.compile(r"<style>(.*?)</style>", re.S)
RE_SECTION = re.compile(r'(<section class="slide.*?</section>)', re.S)

# ── os sete blocos do template ────────────────────────────────────────────────
BLOCO_NOME = {
    1: "Detalhes iniciais da equipe e do projeto",
    2: "Compreendendo o desafio",
    3: "Objetivo atual do projeto",
    4: "Detalhes do projeto realizado",
    5: "Demonstração da solução",
    6: "Link do vídeo pitch",
    7: "Conclusão e próximos passos",
}
# uma frase por divisória, dizendo o que o bloco cobre
DIV_LINHA = {
    1: "Quem fez, o nome da solução e o que ela entrega, em dois parágrafos.",
    2: "O cenário, o problema nomeado, o efeito no indicador e por que resolver agora.",
    3: "O objetivo geral e as duas respostas que o sistema devolve.",
    4: "A abordagem, o que o dado mostrou, cada modelo por vez, o que a operação recebe, a arquitetura e a stack.",
    5: "O endereço da aplicação, as seis abas e as quatro folhas, cada uma com quem usa e como.",
    7: "O que ficou pronto, o que a equipe aprendeu, os limites que continuam de pé e o que vem em seguida.",
}


def _nomes_banca() -> dict[int, str]:
    return {int(p.name[:2]): p.stem.split("-", 1)[1]
            for p in (AO_VIVO / "blocos").glob("[0-9][0-9]-*.html")}


NB = _nomes_banca()

ORDEM: list[tuple[str, object, str]] = (
    [("banca", 1, "capa"), ("div", 1, "div-bloco-1"), ("banca", 2, "equipe"), ("banca", 3, "cronos"),
     ("bloco", "descricao", "descricao"),
     ("div", 2, "div-bloco-2"), ("banca", 4, "prazo"), ("banca", 5, "quebras"), ("banca", 6, "fila-ordem"),
     ("div", 3, "div-bloco-3"), ("pitch", "objetivo", "objetivo"),
     ("div", 4, "div-bloco-4"), ("bloco", "abordagem", "abordagem")]
    + [("banca", n, NB[n]) for n in range(7, 31)]
    + [("arquivo", ABERTURA / "12-codigo-C.html", "codigo-fonte"),
       ("div", 5, "div-bloco-5"), ("banca", 31, "aplicacao"), ("bloco", "mapa-abas", "mapa-abas")]
    + [("tela", t[0], f"tela-{i:02d}-{t[0]}") for i, t in enumerate(TELAS, 1)]
    + [("banca", 33, "acesso"),
       ("bloco", "video", "video"),
       ("div", 7, "div-bloco-7"), ("bloco", "sintese", "sintese"), ("bloco", "aprendizados", "aprendizados"),
       ("bloco", "limitacoes", "limitacoes"), ("bloco", "proximos-passos", "proximos-passos"),
       ("banca", 32, "obrigado")]
)
assert len(ORDEM) == 59, len(ORDEM)

# ── o que cada posição nova vai ter, para o slide de espera ───────────────────
# nome -> (título curto, o que o slide traz, origem do material)
ESPERA: dict[str, tuple[str, str, str]] = {
    "descricao": ("Descrição resumida da solução",
                  "Dois parágrafos: o que o Cronos lê, as três respostas que devolve, e como isso é publicado.",
                  "novo, texto do rascunho conferido no CONTRATO"),
    "abordagem": ("A abordagem de trabalho",
                  "Quatro entregas nas datas da FIAP, hipótese só vira produto com teste no dado, e as duas "
                  "fontes de dados: a planilha da Locaweb e o calendário de feriados.",
                  "novo"),
    "mapa-abas": ("Mapa da aplicação",
                  "As seis abas e as quatro folhas de detalhe, o que cada uma responde e qual modelo a alimenta.",
                  "novo"),
    "video": ("Link do vídeo pitch",
              f"O endereço {URL_VIDEO}, cinco minutos, hands on, acesso público.",
              "novo"),
    "sintese": ("Síntese dos resultados",
                "O erro da previsão, a fila de risco, a projeção da meta e a aplicação, com os números da banca.",
                "novo"),
    "aprendizados": ("Aprendizados-chave",
                     "Volume não prevê quebra, o alvo é raro, modelo interpretável sem perda, o campo oficial "
                     "vale mais que a regra reescrita.",
                     "novo"),
    "limitacoes": ("Limitações enfrentadas",
                   "Cobertura do intervalo no P3 abaixo da do P2, rótulo que só existe após o fechamento, um ano de dado denso, "
                   "sem custo por violação, resumo ainda sem modelo de linguagem.",
                   "novo"),
    "proximos-passos": ("Próximos passos",
                        "Ler da base interna, reajuste semanal, alarme de calibração, texto do resumo pela "
                        "Claude API, custo por violação com a Locaweb.",
                        "novo"),
}
for _n in (1, 2, 3, 4, 5, 7):
    ESPERA[f"div-bloco-{_n}"] = (
        f"Divisória do bloco {_n}",
        f"Abre o bloco «{BLOCO_NOME[_n]}» do template. Desenho próprio, diferente da divisória de seção da banca.",
        "novo, desenho escolhido no lote 1",
    )

# ── ajustes de texto nos slides da banca ──────────────────────────────────────
AJUSTES: dict[int, list[tuple[str, str]]] = {
    2: [("Quem apresenta", "A equipe")],
    31: [("Demonstração ao vivo", "Demonstração da solução")],
}
# linha de apoio abaixo do título, só onde o título sozinho não fecha a mensagem.
# Proposta ao Igor no lote 2; entra aqui depois de aprovada.
APOIO: dict[int, str] = {}
APOIO_PITCH: dict[str, str] = {}

# notas dos slides novos; os da banca vêm do roteiro, as telas do texto de uso real
NOTAS: dict[str, str] = {}

# ── CSS do builder: congelamento, linha de apoio, slide de espera ─────────────
CSS_BUILDER = """
html,body{margin:0;padding:0;background:#fff;overflow:hidden}
#palco{width:1600px;height:900px;position:relative;overflow:hidden}
.slide{animation:none !important}
.mesh{animation:none !important;transform:none !important}
.is-active *:not(.mesh){animation-duration:.01ms !important;animation-delay:0ms !important}
/* linha de apoio abaixo do título, para o slide lido sem apresentador */
.apoio{font-size:19px;line-height:1.5;color:var(--tx);margin-top:14px;max-width:64ch}
.apoio b{color:var(--head);font-weight:700}
.dark .apoio{color:#B7C0CB} .dark .apoio b{color:#fff}
/* slide de espera do esqueleto */
.esp .body{justify-content:center}
.esp .quadro{border:2px dashed #B9C4D6;border-radius:22px;padding:44px 52px;max-width:1100px}
.esp .tt{font-size:54px}
.esp .tt .hl{color:var(--accent)}
.esp .apoio{font-size:20px;margin-top:22px}
.esp .ori{font-family:var(--mono);font-size:13px;color:var(--tx2);margin-top:26px}
"""


def pagina(css_bloco: str, secao: str) -> str:
    estilo = (AO_VIVO / "_estilo.css").read_text(encoding="utf-8")
    secao = secao.replace('class="slide', 'class="is-active slide', 1)
    return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">{FONTES}'
            f"<style>{estilo}\n{css_bloco}\n{CSS_BUILDER}</style></head>"
            f'<body><div id="palco">{secao}</div></body></html>')


def resolve_contadores(texto: str) -> str:
    """Escreve o valor final onde o contador espera o JS."""
    def valor(m: re.Match) -> str:
        alvo = m.group(2)
        dec = re.search(r'data-dec="(\d+)"', m.group(1))
        if dec and int(dec.group(1)) > 0:
            v = f"{float(alvo.replace(',', '.')):.{int(dec.group(1))}f}".replace(".", ",")
        else:
            v = f"{int(float(alvo.replace(',', '.'))):,}".replace(",", ".")
        return m.group(1) + v + m.group(3)
    return re.sub(r'(<span class="ct"[^>]*data-to="([^"]+)"[^>]*>)[^<]*(</span>)', valor, texto)


def secao_e_css(arquivo: Path) -> tuple[str, str]:
    t = arquivo.read_text(encoding="utf-8")
    css = "\n".join(c.strip() for c in RE_STYLE.findall(t))
    achadas = RE_SECTION.findall(t)
    if not achadas:
        raise SystemExit(f'{arquivo.name}: nenhuma <section class="slide ...">')
    return achadas[0], css


def slide_banca(n: int) -> tuple[str, str]:
    arquivo = next(AO_VIVO.glob(f"blocos/{n:02d}-*.html"))
    secao, css = secao_e_css(arquivo)
    secao = resolve_contadores(secao)
    # _build/ fica na mesma profundidade de ao-vivo/blocos/: só ../figs muda de dono
    secao = secao.replace('src="../figs/', 'src="../../ao-vivo/figs/')
    css = css.replace("url(../figs/", "url(../../ao-vivo/figs/")
    for de, para in AJUSTES.get(n, []):
        if de not in secao:
            raise SystemExit(f"slide {n}: ajuste «{de}» não encontrado")
        secao = secao.replace(de, para)
    if n in APOIO:
        secao = secao.replace("</h1>", f'</h1><p class="apoio rv">{APOIO[n]}</p>', 1)
    return secao, css


def slide_pitch(nome: str) -> tuple[str, str]:
    arquivo = next(PITCH.glob(f"blocos/[0-9][0-9]-{nome}.html"))
    secao, css = secao_e_css(arquivo)
    secao = resolve_contadores(secao)
    if nome in APOIO_PITCH:
        secao = secao.replace("</h1>", f'</h1><p class="apoio rv">{APOIO_PITCH[nome]}</p>', 1)
    return secao, css


def slide_espera(nome: str, bloco: int) -> tuple[str, str]:
    titulo, conteudo, origem = ESPERA[nome]
    secao = (f'<section class="slide light esp"><div class="mesh"></div><div class="grid-bg"></div>'
             f'<div class="hd"><div class="bi">{LOGO_CLARO}</div><div class="bn">Cronos</div>'
             f'<div class="tag">Bloco {bloco} &middot; {BLOCO_NOME[bloco]}</div></div>'
             f'<div class="body"><div class="quadro"><span class="eb">Em construção</span>'
             f'<h1 class="tt">Aqui irá ficar: <span class="hl">{titulo}</span></h1>'
             f'<p class="apoio">{conteudo}</p><p class="ori">Origem: {origem}</p></div></div>'
             f'<div class="ft"><span>Esqueleto do deck da Sprint 4</span></div></section>')
    return secao, ""


def slide_bloco(nome: str, bloco: int) -> tuple[str, str]:
    achados = sorted(BLOCOS.glob(f"[0-9][0-9]-{nome}.html"))
    if not achados:
        return slide_espera(nome, bloco)
    secao, css = secao_e_css(achados[0])
    return resolve_contadores(secao), css


def slide_div(n_bloco: int) -> tuple[str, str]:
    """A divisória de bloco. Até o lote 1 escolher o desenho, é um slide de espera."""
    molde = BLOCOS / "00-div-bloco.html"
    if not molde.exists():
        return slide_espera(f"div-bloco-{n_bloco}", n_bloco)
    secao, css = secao_e_css(molde)
    secao = (secao.replace("{N}", f"{n_bloco:02d}")
             .replace("{NOME}", BLOCO_NOME[n_bloco])
             .replace("{LINHA}", DIV_LINHA[n_bloco]))
    return secao, css


def escreve_build() -> list[tuple[int, str, Path, int]]:
    """Um HTML por slide em _build/. Devolve (posição, nome, caminho, bloco)."""
    BUILD.mkdir(parents=True, exist_ok=True)
    for velho in BUILD.glob("*.html"):
        velho.unlink()
    itens, bloco = [], 1
    for pos, (tipo, ref, nome) in enumerate(ORDEM, 1):
        if tipo == "div":
            bloco = int(ref)
        if nome == "video":
            bloco = 6
        if tipo == "banca":
            secao, css = slide_banca(int(ref))
            html = pagina(css, secao)
        elif tipo == "pitch":
            secao, css = slide_pitch(str(ref))
            html = pagina(css, secao)
        elif tipo == "bloco":
            secao, css = slide_bloco(str(ref), bloco)
            html = pagina(css, secao)
        elif tipo == "div":
            secao, css = slide_div(int(ref))
            html = pagina(css, secao)
        elif tipo == "tela":
            pos_tela = int(nome.split("-")[1])
            html = html_tela(str(ref), pos_tela, len(TELAS), URL_APP)
        elif tipo == "arquivo":
            caminho = Path(ref)
            if not caminho.exists():
                raise SystemExit(f"arquivo não encontrado: {caminho}")
            itens.append((pos, nome, caminho, bloco))
            continue
        else:
            raise SystemExit(f"tipo desconhecido: {tipo}")
        destino = BUILD / f"{pos:02d}-{nome}.html"
        destino.write_text(html, encoding="utf-8")
        itens.append((pos, nome, destino, bloco))
    return itens


MEDIDA = """() => {
  const a = document.querySelector('.slide');
  const corpo = a.querySelector('.body');
  const cr = corpo ? corpo.getBoundingClientRect() : null;
  const achados = [];
  a.querySelectorAll('*').forEach(el => {
    const c = el.className.toString();
    if (/\\b(mesh|grid-bg)\\b/.test(c)) return;
    const r = el.getBoundingClientRect();
    if (r.width > 0 && r.height > 0 &&
        (r.left < -1 || r.right > 1601 || r.top < -1 || r.bottom > 901))
      achados.push('FORA DO PALCO ' + el.tagName.toLowerCase() + '.' + c.slice(0, 24));
    if (cr && corpo.contains(el) && r.width > 0 && r.height > 0 && r.bottom > cr.bottom + 2)
      achados.push('FORA DO CORPO ' + el.tagName.toLowerCase() + '.' + c.slice(0, 24) +
        ' (' + Math.round(r.bottom - cr.bottom) + 'px)');
    if (parseFloat(getComputedStyle(el).opacity) === 0 && r.width > 2)
      achados.push('INVISIVEL ' + el.tagName.toLowerCase() + '.' + c.slice(0, 24));
  });
  return achados.slice(0, 6);
}"""


def render(itens: list[tuple[int, str, Path, int]], so: set[int] | None) -> list[Path]:
    from playwright.sync_api import sync_playwright
    PNG.mkdir(parents=True, exist_ok=True)
    pngs = []
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=CHROME)
        pg = nav.new_context(viewport={"width": 1600, "height": 900}, device_scale_factor=2).new_page()
        for pos, nome, caminho, _ in itens:
            destino = PNG / f"{pos:02d}-{nome}.png"
            pngs.append(destino)
            if so and pos not in so and destino.exists():
                continue
            pg.goto(caminho.resolve().as_uri(), wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(450)
            pg.locator(".slide").first.screenshot(path=str(destino))
            avisos = pg.evaluate(MEDIDA)
            print(f"  {pos:02d} {nome:<28}" + ("  " + " | ".join(avisos) if avisos else ""))
        nav.close()
    return pngs


def falas_da_banca() -> dict[int, str]:
    """A fala de cada slide da banca, do objeto FALAS do ROTEIRO.html, sem tags."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=CHROME)
        pg = nav.new_page()
        pg.goto((AO_VIVO / "ROTEIRO.html").as_uri())
        bruto = pg.evaluate("JSON.stringify(FALAS)")
        nav.close()
    falas = json.loads(bruto)
    saida = {}
    for n, f in falas.items():
        versoes = f.get("versoes") or []
        texto = " ".join(versoes[0].get("fala", [])) if versoes else ""
        saida[int(n)] = re.sub(r"<[^>]+>", "", texto).strip()
    return saida


def notas(itens) -> dict[int, str]:
    banca = falas_da_banca()
    saida = {}
    for pos, nome, _, _ in itens:
        tipo, ref, _ = ORDEM[pos - 1]
        if tipo == "banca":
            saida[pos] = banca.get(int(ref), "")
        elif tipo == "tela":
            saida[pos] = nota_tela(str(ref))
        else:
            saida[pos] = NOTAS.get(nome, "Em construção.")
    return saida


def monta_pptx(pngs: list[Path], notas_por_pos: dict[int, str]) -> None:
    from pptx import Presentation
    from pptx.util import Emu
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    branco = prs.slide_layouts[6]
    for pos, png in enumerate(pngs, 1):
        s = prs.slides.add_slide(branco)
        s.shapes.add_picture(str(png), 0, 0, width=prs.slide_width, height=prs.slide_height)
        s.notes_slide.notes_text_frame.text = notas_por_pos.get(pos, "")
    prs.save(PPTX)


def escreve_viewer(itens, pngs: list[Path], notas_por_pos: dict[int, str]) -> None:
    quadros = "".join(
        f'<figure data-n="{pos}" data-bloco="{bloco}"><img src="_png/{png.name}" alt="{nome}">'
        f'<figcaption><b>{pos:02d}</b> {nome} &middot; Bloco {bloco} &middot; {BLOCO_NOME[bloco]}</figcaption>'
        f'<pre>{notas_por_pos.get(pos, "")}</pre></figure>'
        for (pos, nome, _, bloco), png in zip(itens, pngs))
    VIEWER.write_text(f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Cronos · Sprint 4 · {len(pngs)} slides</title>{FONTES}<style>
html,body{{margin:0;height:100%;background:#1B1F26;color:#fff;font-family:Outfit,system-ui,sans-serif;overflow:hidden}}
figure{{display:none;margin:0;position:absolute;inset:0}} figure.on{{display:block}}
figure img{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);max-width:100vw;max-height:calc(100vh - 92px);
  box-shadow:0 40px 130px -50px rgba(0,0,0,.7)}}
figcaption{{position:fixed;left:0;right:0;bottom:0;padding:14px 24px;font-size:13px;color:rgba(255,255,255,.72);
  background:linear-gradient(0deg,rgba(0,0,0,.7),transparent)}}
figcaption b{{color:#FBBF24;font-family:"JetBrains Mono",monospace}}
pre{{display:none;position:fixed;left:24px;right:24px;bottom:48px;max-height:38vh;overflow:auto;white-space:pre-wrap;
  font-family:Outfit,system-ui,sans-serif;font-size:15px;line-height:1.5;color:#E8ECF3;background:rgba(10,14,23,.94);
  border:1px solid rgba(255,255,255,.14);border-radius:12px;padding:16px 20px;margin:0}}
body.notas pre{{display:block}}
#ajuda{{position:fixed;top:12px;right:16px;font-size:12px;color:rgba(255,255,255,.5)}}
</style></head><body>{quadros}
<div id="ajuda">← → slide · N notas · Home/End · F tela cheia</div>
<script>
var f=[].slice.call(document.querySelectorAll('figure')),i=0;
function go(k){{i=(k+f.length)%f.length;f.forEach(function(x,j){{x.classList.toggle('on',j===i)}});location.hash=f[i].dataset.n}}
window.addEventListener('keydown',function(e){{var k=e.key.toLowerCase();
 if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown'){{e.preventDefault();go(i+1)}}
 else if(e.key==='ArrowLeft'||e.key==='PageUp'){{e.preventDefault();go(i-1)}}
 else if(e.key==='Home')go(0);else if(e.key==='End')go(f.length-1);
 else if(k==='n')document.body.classList.toggle('notas');
 else if(k==='f'){{document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen()}}}});
document.body.addEventListener('click',function(){{go(i+1)}});
go(Math.max(0,(parseInt(location.hash.slice(1),10)||1)-1));
</script></body></html>""", encoding="utf-8")


EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF]")


def varredura(itens) -> int:
    problemas = 0
    for pos, nome, caminho, _ in itens:
        t = caminho.read_text(encoding="utf-8")
        s = RE_SECTION.search(t)
        texto = re.sub(r"<style>.*?</style>", "", s.group(1) if s else t, flags=re.S)
        texto = _html.unescape(re.sub(r"<[^>]+>", " ", texto)).replace(" ", " ")
        avisos = []
        if re.search(r"\bturno", texto, re.I):
            avisos.append("turno")
        if "—" in texto:
            avisos.append("travessão")
        if EMOJI.search(texto):
            avisos.append("emoji")
        tem_p3 = re.search(r"\bP3\b|prioridade 3|\bna 3\b", texto, re.I)
        tem_p2 = re.search(r"\bP2\b|prioridade 2|\bna 2\b", texto, re.I)
        if tem_p3 and not tem_p2:
            avisos.append("P3 sem P2")
        if avisos:
            problemas += 1
            print(f"  VARREDURA {pos:02d} {nome}: {', '.join(avisos)}")
    return problemas


def main() -> int:
    so = None
    if "--so" in sys.argv:
        so = {int(x) for x in sys.argv[sys.argv.index("--so") + 1:]}
    print("1/4 · HTML por slide")
    itens = escreve_build()
    esperas = sum(1 for _, _, c, _ in itens
                  if c.parent == BUILD and 'class="is-active slide light esp"' in c.read_text(encoding="utf-8"))
    print(f"     {len(itens)} slides, {esperas} de espera")
    print("2/4 · render")
    pngs = render(itens, so)
    print("3/4 · varredura de texto")
    if not varredura(itens):
        print("     limpa")
    print("4/4 · notas, pptx e visualizador")
    ns = notas(itens)
    monta_pptx(pngs, ns)
    escreve_viewer(itens, pngs, ns)
    print(f"Pronto: {PPTX.name} ({len(pngs)} slides) · {VIEWER}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# -*- coding: utf-8 -*-
"""Três versões do slide de conclusão, em arquivos separados.

A versão que existia foi reprovada pelo dono do projeto, e com razão: tinha um
vão morto de cerca de 250px na coluna da esquerda, quatro hierarquias de número
competindo sem nenhuma vencer, a coluna da direita lendo como anexo em vez de
argumento, e o conjunto era uma vitrine de métricas, não uma conclusão.

As três aqui mudam de CONCEITO, e não só de arranjo:

    A · A prova, e só ela
        Um confronto domina o slide inteiro: 13 contra 0 quebras nas mesmas 50
        posições da fila. É a frase que sustenta o trabalho. Os outros números
        viram uma régua fina no pé, sem cartão, porque são apoio e não tese.

    B · O que muda na operação
        Quatro linhas de antes e depois. À esquerda como se decide hoje, à
        direita o que o Cronos entrega, com o número de cada lado. Uma
        conclusão que fala do que muda para quem opera, não do modelo.

    C · O arco do trabalho
        A jornada em uma linha: 122.543 incidentes, o recorte de 25.600, os
        dois modelos, o painel, o resultado. Cada etapa com o seu número, e os
        limites declarados no pé.

Números conferidos em prototipos/slides/ao-vivo/CONTRATO.md, seções 5 e 7.

Uso:
    .venv/Scripts/python.exe prototipos/slides/sprint4/_comparar_conclusao.py
"""
from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

AQUI = Path(__file__).parent
RAIZ = AQUI.parents[2]
sys.path.insert(0, str(RAIZ / "scripts"))
import monta_deck_sprint4 as mk  # noqa: E402

PNG = AQUI / "_png" / "_comparar"

LOGO = ('<svg viewBox="0 0 28 28" fill="none"><path d="M6 22L12 14L16 17L22 8" stroke="#fff" '
        'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="22" cy="8" '
        'r="3" stroke="#3B82F6" stroke-width="1.5"/><circle cx="22" cy="8" r="1.2" fill="#3B82F6"/></svg>')


def cabeca(classe: str, tag: str) -> str:
    return (f'<section class="slide light {classe}" data-slide="0" data-var="a">'
            '<div class="mesh"></div><div class="grid-bg"></div>'
            f'<div class="hd"><div class="bi">{LOGO}</div><div class="bn">Cronos</div>'
            f'<div class="tag">{tag}</div></div><div class="body">')


def rodape(texto: str) -> str:
    return f'</div><div class="ft"><span>{texto}</span></div></section>'


# ═════════════════════════════════════════════════════════════════════════════
# A · A prova, e só ela
# ═════════════════════════════════════════════════════════════════════════════
CSS_A = """
.cvA .body{padding-top:14px;justify-content:center}
.cvA .tt{font-size:46px;letter-spacing:-1.7px}
/* o confronto: dois números na mesma escala, e a distância entre eles é o argumento */
.cvA .duelo{display:flex;align-items:stretch;margin-top:34px;border-radius:22px;overflow:hidden;
  border:1px solid var(--line);box-shadow:0 30px 70px -44px rgba(15,23,42,.4)}
.cvA .lado{flex:1;padding:36px 40px;display:flex;flex-direction:column;justify-content:center}
.cvA .lado.hoje{background:#F4F6FA}
.cvA .lado.cronos{background:linear-gradient(150deg,#fff,#EEF5FF);border-left:1px solid var(--line)}
.cvA .lado .k{display:inline-flex;align-items:center;gap:9px;font-size:11.5px;font-weight:700;
  letter-spacing:1.9px;text-transform:uppercase;color:var(--tx2)}
.cvA .lado.cronos .k{color:var(--accent)}
.cvA .lado .k .ic{width:16px;height:16px}
.cvA .lado .n{display:flex;align-items:baseline;gap:16px;margin-top:14px}
.cvA .lado .n .v{font-size:128px;font-weight:900;letter-spacing:-5.6px;line-height:.82;
  color:#9AA6B6;font-variant-numeric:tabular-nums}
.cvA .lado.cronos .n .v{color:var(--accent)}
.cvA .lado .n .r{font-size:20px;font-weight:600;line-height:1.35;color:var(--tx);max-width:22ch}
.cvA .lado .n .r b{display:block;color:var(--head);font-weight:800;font-size:22px;
  white-space:nowrap}
.cvA .lado p{font-size:15px;line-height:1.5;color:var(--tx);margin-top:18px;max-width:38ch}
.cvA .lado p b{color:var(--head);font-weight:700}
/* a régua de apoio: sem cartão, porque não disputa com o confronto */
.cvA .regua{display:grid;grid-template-columns:repeat(4,1fr);margin-top:30px;padding-top:22px;
  border-top:1px solid #DCE4EF}
.cvA .rg{padding-right:26px;border-right:1px solid #DCE4EF}
.cvA .rg:last-child{border-right:none;padding-right:0}
.cvA .rg:not(:first-child){padding-left:26px}
.cvA .rg .v{font-size:30px;font-weight:900;letter-spacing:-1.1px;color:var(--head);line-height:1;
  font-variant-numeric:tabular-nums}
.cvA .rg .v small{font-size:14px;font-weight:700;color:var(--tx2);letter-spacing:0;margin-left:4px}
.cvA .rg .k{font-size:13.5px;font-weight:700;color:var(--head);margin-top:9px;letter-spacing:-.15px}
.cvA .rg p{font-size:12.5px;line-height:1.45;color:var(--tx2);margin-top:5px}
"""


def versao_a() -> tuple[str, str]:
    corpo = f"""{cabeca("cvA", "Avaliação fora do período de treino")}
    <span class="eb"><span class="rv" style="--d:240ms">7 &middot; Conclusão</span></span>
    <h1 class="tt"><span class="mask" style="--d:340ms"><span>A fila passou a começar pelo lugar certo</span></span></h1>

    <div class="duelo rv3" style="--d:640ms">
      <div class="lado hoje">
        <span class="k"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6.5h16M4 12h16M4 17.5h16"/></svg>Como se ordena hoje</span>
        <div class="n"><span class="v">0</span><span class="r"><b>violações encontradas</b>nos 50 primeiros da fila</span></div>
        <p>Ordenar por prioridade é o comportamento padrão da ferramenta de atendimento. Nas 50 primeiras posições ele <b>não encontra nenhuma</b> das 50 violações do período.</p>
      </div>
      <div class="lado cronos">
        <span class="k"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8.4"/><circle cx="12" cy="12" r="3.4"/><path d="M12 1.8v2.6M12 19.6v2.6M1.8 12h2.6M19.6 12h2.6"/></svg>Ordenando por risco</span>
        <div class="n"><span class="v">13</span><span class="r"><b>violações encontradas</b>nas mesmas 50 posições da fila</span></div>
        <p>A regressão logística estima a probabilidade de cada caso aberto estourar o prazo. Em <b>5.183 incidentes</b> avaliados fora do treino, o topo da fila é onde as violações estão.</p>
      </div>
    </div>

    <div class="regua">
      <div class="rg rv" style="--d:1200ms"><div class="v">0,869</div>
        <div class="k">O modelo fica calibrado</div><p>área sob a curva, e prevê 48,1 quebras onde houve 50</p></div>
      <div class="rg rv" style="--d:1280ms"><div class="v">3 <small>meses</small></div>
        <div class="k">A meta é chamada antes</div><p>certa nas duas prioridades, antes da apuração de dezembro</p></div>
      <div class="rg rv" style="--d:1360ms"><div class="v">4,2 · 11,8</div>
        <div class="k">O volume é previsto por dia</div><p>em P2 e P3, ganhando do baseline por 15% no P2</p></div>
      <div class="rg rv" style="--d:1440ms"><div class="v">2,5<small>%</small></div>
        <div class="k">E o volume não bastava</div><p>é o quanto ele explica das quebras; por isso os dois modelos</p></div>
    </div>
    {rodape("Base de avaliação: 5.183 incidentes e 50 violações, fora do período de treino")}"""
    return corpo, CSS_A


# ═════════════════════════════════════════════════════════════════════════════
# B · O que muda na operação
# ═════════════════════════════════════════════════════════════════════════════
CSS_B = """
.cvB .body{padding-top:14px;justify-content:center}
.cvB .tt{font-size:46px;letter-spacing:-1.7px}
.cvB .lead{font-size:17px;line-height:1.5;color:var(--tx);margin-top:12px;max-width:92ch}
.cvB .lead b{color:var(--head);font-weight:700}
.cvB .tabela{margin-top:30px}
.cvB .cab{display:grid;grid-template-columns:270px 1fr 52px 1fr;gap:0 22px;padding-bottom:11px;
  border-bottom:1px solid #DCE4EF}
.cvB .cab span{font-size:11px;font-weight:700;letter-spacing:1.9px;text-transform:uppercase}
.cvB .cab .c1{color:var(--tx2)} .cvB .cab .c2{color:var(--tx2)} .cvB .cab .c3{color:var(--accent)}
.cvB .ln{display:grid;grid-template-columns:270px 1fr 52px 1fr;gap:0 22px;align-items:center;
  padding:22px 0;border-bottom:1px solid #EDF1F6}
.cvB .ln:last-child{border-bottom:none}
.cvB .ln .q{font-size:16.5px;font-weight:800;color:var(--head);letter-spacing:-.3px;line-height:1.3}
.cvB .ln .antes,.cvB .ln .depois{display:flex;align-items:baseline;gap:11px}
.cvB .ln .antes .v{font-size:27px;font-weight:900;letter-spacing:-1px;color:#9AA6B6;line-height:1;
  font-variant-numeric:tabular-nums;flex-shrink:0}
.cvB .ln .depois .v{font-size:27px;font-weight:900;letter-spacing:-1px;color:var(--accent);
  line-height:1;font-variant-numeric:tabular-nums;flex-shrink:0}
.cvB .ln .antes p{font-size:13.5px;line-height:1.45;color:var(--tx2)}
.cvB .ln .depois p{font-size:13.5px;line-height:1.45;color:var(--tx)}
.cvB .ln .depois p b{color:var(--head);font-weight:700}
.cvB .ln .seta{display:flex;justify-content:center;color:#C2CCDB}
.cvB .ln .seta svg{width:22px;height:22px;stroke:currentColor;fill:none;stroke-width:1.8;
  stroke-linecap:round;stroke-linejoin:round}
.cvB .fecho{display:flex;align-items:flex-start;gap:12px;margin-top:24px;padding-top:18px;
  border-top:1px solid #DCE4EF;font-size:16px;line-height:1.45;color:var(--tx)}
.cvB .fecho .ic{width:20px;height:20px;color:var(--warn);margin-top:2px;flex-shrink:0}
.cvB .fecho b{color:var(--head);font-weight:700}
"""

_SETA = ('<svg viewBox="0 0 24 24"><path d="M4 12h15"/><path d="M13.5 6.5L20 12l-6.5 5.5"/></svg>')


def _linha(q: str, va: str, pa: str, vd: str, pd: str, d: int) -> str:
    return (f'<div class="ln rv" style="--d:{d}ms"><div class="q">{q}</div>'
            f'<div class="antes"><span class="v">{va}</span><p>{pa}</p></div>'
            f'<div class="seta">{_SETA}</div>'
            f'<div class="depois"><span class="v">{vd}</span><p>{pd}</p></div></div>')


def versao_b() -> tuple[str, str]:
    linhas = (
        _linha("Por onde a fila começa", "0",
               "violações nos 50 primeiros, ordenando por prioridade",
               "13", "nas mesmas 50 posições, ordenando por <b>risco estimado</b>", 800)
        + _linha("Quando a meta do ano é lida", "dez",
                 "só na apuração de dezembro, com o ano fechado",
                 "out", "em 1º de outubro, com a chamada <b>certa nas duas prioridades</b>", 900)
        + _linha("Quanto trabalho entra amanhã", "—",
                 "não havia previsão por prioridade",
                 "4,2 · 11,8", "de erro por dia em <b>P2 e P3</b>, de D+1 a D+7", 1000)
        + _linha("Por que este caso, e não outro", "—",
                 "a ordenação não vinha com justificativa",
                 "6", "sinais com o peso de cada um, <b>tirados do próprio modelo</b>", 1100)
    )
    corpo = f"""{cabeca("cvB", "O que muda para quem opera")}
    <span class="eb"><span class="rv" style="--d:240ms">7 &middot; Conclusão</span></span>
    <h1 class="tt"><span class="mask" style="--d:340ms"><span>Quatro decisões do dia que mudam de base</span></span></h1>
    <p class="lead rv" style="--d:620ms">A conclusão do trabalho não é um modelo, é o que a operação passa a conseguir responder. <b>À esquerda, como se decide hoje; à direita, com o Cronos.</b></p>

    <div class="tabela">
      <div class="cab rv" style="--d:720ms"><span class="c1">A decisão</span><span class="c2">Como é hoje</span><span></span><span class="c3">Com o Cronos</span></div>
      {linhas}
    </div>

    <div class="fecho rv" style="--d:1250ms">
      <svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9.4"/><path d="M12 7.6v5.2M12 16.2v.2"/></svg>
      <span>Dois limites continuam de pé: a faixa de 80% cobre <b>59% a 61%</b> dos dias no P3, contra 86% a 88% no P2, e o dataset não traz custo por violação, então <b>o ganho está medido em violações, nunca em moeda</b>.</span>
    </div>
    {rodape("Risco: 5.183 incidentes e 50 violações fora do treino &middot; previsão: backtest deslizante em 2025")}"""
    return corpo, CSS_B


# ═════════════════════════════════════════════════════════════════════════════
# C · O arco do trabalho
# ═════════════════════════════════════════════════════════════════════════════
CSS_C = """
.cvC .body{padding-top:14px;justify-content:center}
.cvC .tt{font-size:46px;letter-spacing:-1.7px}
.cvC .lead{font-size:17px;line-height:1.5;color:var(--tx);margin-top:12px;max-width:92ch}
/* a jornada: cinco etapas num trilho, com o número de cada uma */
.cvC .trilho{position:relative;display:grid;grid-template-columns:repeat(5,1fr);gap:16px;
  margin-top:40px}
.cvC .trilho::before{content:"";position:absolute;left:8px;right:8px;top:11px;height:2px;
  background:linear-gradient(90deg,#D6DEE9,var(--accent))}
.cvC .et{position:relative;padding-top:38px}
.cvC .et::before{content:"";position:absolute;left:0;top:3px;width:18px;height:18px;
  border-radius:50%;background:#fff;border:2px solid #C2CCDB;box-sizing:border-box}
.cvC .et.viva::before{background:var(--accent);border-color:var(--accent);
  box-shadow:0 0 0 5px rgba(37,99,235,.16)}
.cvC .et .v{font-size:38px;font-weight:900;letter-spacing:-1.5px;color:var(--head);line-height:1;
  font-variant-numeric:tabular-nums}
.cvC .et.viva .v{color:var(--accent)}
.cvC .et .v small{font-size:15px;font-weight:700;color:var(--tx2);letter-spacing:0;margin-left:4px}
.cvC .et .k{font-size:15.5px;font-weight:800;color:var(--head);margin-top:10px;letter-spacing:-.25px}
.cvC .et p{font-size:13px;line-height:1.5;color:var(--tx);margin-top:6px}
.cvC .et p b{color:var(--head);font-weight:700}
/* o resultado, em destaque, e os limites ao lado */
.cvC .base{display:flex;gap:26px;margin-top:40px;align-items:stretch}
.cvC .res{flex:1.25;display:flex;align-items:center;gap:22px;padding:24px 30px;border-radius:18px;
  background:linear-gradient(150deg,#fff,#EEF5FF);border:1px solid #BFDBFE;
  box-shadow:0 24px 56px -40px rgba(37,99,235,.45)}
.cvC .res .v{font-size:76px;font-weight:900;letter-spacing:-3.2px;line-height:.86;
  color:var(--accent);font-variant-numeric:tabular-nums;flex-shrink:0}
.cvC .res .tx b{display:block;font-size:19px;font-weight:800;color:var(--head);letter-spacing:-.3px}
.cvC .res .tx p{font-size:14.5px;line-height:1.5;color:var(--tx);margin-top:6px}
.cvC .res .tx p b{display:inline;font-size:inherit}
.cvC .lim{flex:1;padding:22px 26px;border-radius:18px;background:linear-gradient(160deg,#fff,#FDF9F1);
  border:1px solid #F0DFBE}
.cvC .lim .k{font-size:11px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;
  color:var(--warn)}
.cvC .lim .li{display:flex;gap:11px;padding:9px 0;font-size:13.5px;line-height:1.45;color:var(--tx)}
.cvC .lim .li + .li{border-top:1px solid #F0E4CC}
.cvC .lim .li .m{font-weight:800;color:var(--warn);flex-shrink:0;white-space:nowrap;
  font-variant-numeric:tabular-nums}
.cvC .lim .li b{color:var(--head);font-weight:700}
"""


def versao_c() -> tuple[str, str]:
    etapas = (
        ('<div class="et rv" style="--d:760ms"><div class="v">122.543</div>'
         '<div class="k">O histórico</div><p>incidentes de janeiro de 2023 a dezembro de 2025, em 19 campos</p></div>')
        + ('<div class="et rv" style="--d:860ms"><div class="v">25.600</div>'
           '<div class="k">O recorte do indicador</div><p>elegíveis pelo campo oficial <b>Entrou para KPI?</b>, 21% da base</p></div>')
        + ('<div class="et rv" style="--d:960ms"><div class="v">2 <small>modelos</small></div>'
           '<div class="k">O que foi treinado</div><p>Prophet para o volume e regressão logística para o risco</p></div>')
        + ('<div class="et rv" style="--d:1060ms"><div class="v">6 <small>abas</small></div>'
           '<div class="k">O que a operação recebe</div><p>em um contêiner, sem provedor de nuvem amarrado</p></div>')
        + ('<div class="et viva rv" style="--d:1160ms"><div class="v">3 <small>meses</small></div>'
           '<div class="k">A leitura antecipada</div><p>a meta do ano chamada em outubro, certa em <b>P2 e P3</b></p></div>')
    )
    corpo = f"""{cabeca("cvC", "Da planilha à decisão do dia")}
    <span class="eb"><span class="rv" style="--d:240ms">7 &middot; Conclusão</span></span>
    <h1 class="tt"><span class="mask" style="--d:340ms"><span>O caminho que o dado percorreu</span></span></h1>
    <p class="lead rv" style="--d:620ms">Cinco etapas entre a planilha que a Locaweb entregou e a decisão que a operação toma no dia.</p>

    <div class="trilho">{etapas}</div>

    <div class="base">
      <div class="res rv3" style="--d:1300ms">
        <span class="v">13</span>
        <div class="tx"><b>violações nos 50 primeiros da fila de risco</b>
          <p>em 5.183 incidentes avaliados fora do treino. Ordenando por prioridade, que é o que se faz hoje, <b>nenhuma</b>. É o resultado que sustenta o produto.</p></div>
      </div>
      <div class="lim rv3" style="--d:1420ms">
        <div class="k">O que continua de pé</div>
        <div class="li"><span class="m">59 a 61%</span><span>de cobertura da faixa no <b>P3</b>, contra 86% a 88% no P2</span></div>
        <div class="li"><span class="m">sem custo</span><span>o dataset não traz o valor de uma violação, então o ganho está em <b>violações e posição na meta</b></span></div>
      </div>
    </div>
    {rodape("Risco: 5.183 incidentes e 50 violações fora do treino &middot; previsão: backtest deslizante em 2025")}"""
    return corpo, CSS_C


VERSOES = [
    ("A", "A prova, e só ela",
     "Um confronto ocupa o slide: 13 contra 0 violações nas mesmas 50 posições da fila. É a frase "
     "que sustenta o trabalho. Os outros números viram régua fina no pé, sem cartão.", versao_a),
    ("B", "O que muda na operação",
     "Quatro decisões do dia, com o de hoje à esquerda e o do Cronos à direita. Fala do que a "
     "operação passa a conseguir responder, não do modelo.", versao_b),
    ("C", "O arco do trabalho",
     "A jornada em cinco etapas, da planilha à decisão, cada uma com o seu número. O resultado "
     "em destaque na base, e os limites declarados ao lado.", versao_c),
]

CSS_PAGINA = """
body{background:#2A2F38;overflow:auto;padding:34px 0 60px}
.palco{width:1600px;height:900px;position:relative;overflow:hidden;margin:0 auto 34px;
  box-shadow:0 30px 90px -40px rgba(0,0,0,.7);background:#fff}
.rot{width:1600px;margin:0 auto 10px;color:rgba(255,255,255,.6);font-family:var(--mono);font-size:13px}
.sec{width:1600px;margin:0 auto 22px;color:#fff;font-family:var(--font);font-size:30px;
  font-weight:800;letter-spacing:-.8px}
.sec small{display:block;font-size:16px;font-weight:400;color:rgba(255,255,255,.62);margin-top:7px;
  letter-spacing:0;line-height:1.45;max-width:1100px}
"""


def main() -> int:
    estilo = (mk.AO_VIVO / "_estilo.css").read_text(encoding="utf-8")
    congela = mk.CSS_BUILDER.replace("#palco{", ".palco-x{")
    PNG.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=mk.CHROME)
        pg = nav.new_page(viewport={"width": 1700, "height": 1000})
        for letra, nome, desc, fn in VERSOES:
            secao, css = fn()
            secao = secao.replace('class="slide', 'class="is-active slide', 1)
            html = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
                    f'<title>Conclusão · versão {letra} · {nome}</title>{mk.FONTES}'
                    f"<style>{estilo}\n{css}\n{congela}\n{CSS_PAGINA}</style></head><body>"
                    f'<div class="sec">Versão {letra} &middot; {nome}<small>{desc}</small></div>'
                    f'<div class="palco" id="c{letra.lower()}">{secao}</div></body></html>')
            destino = AQUI / f"_conclusao-{letra}.html"
            destino.write_text(html, encoding="utf-8")
            pg.goto(destino.as_uri(), wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(700)
            el = pg.query_selector(".palco")
            el.screenshot(path=str(PNG / f"conclusao-{letra}.png"))
            avisos = pg.evaluate(mk.MEDIDA)
            print(f"{destino.name}  " + (" | ".join(avisos) if avisos else "limpo"))
        nav.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

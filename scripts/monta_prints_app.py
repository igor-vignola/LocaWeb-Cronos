# -*- coding: utf-8 -*-
"""Gera os dez slides de captura da aplicação, em `prototipos/slides/mvp/aplicacao/`.

A captura é 16:10 e o slide é 16:9. Para mostrar a tela inteira sem cortar nada, o título
sai de cima da janela e vira coluna estreita à esquerda: assim a janela usa quase toda a
altura do slide, 1216 por 833, o que dá cerca de 70% da área.

Os modais vêm logo depois da aba de onde saem, e não amontoados no fim: o briefing pertence
ao Panorama, a régua da meta à Projeção, o escore à Fila, o detalhe do produto à Saúde.

Uso:
    .venv/Scripts/python scripts/monta_prints_app.py
"""
from __future__ import annotations

from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "prototipos" / "slides" / "mvp" / "aplicacao"
PRINTS = RAIZ / "sprints" / "sprint-3" / "prints"

# (arquivo do print, sobrancelha, título, legenda)
TELAS = [
    ("01-panorama", "Aba Panorama", "O dia em uma tela",
     "O previsto para a hora contra o registrado, em <b>P3 e P2</b>. Abaixo, os casos de "
     "maior risco agora e as duas metas do ano."),
    ("07-modal-briefing", "Panorama · resumo automático", "O briefing das 07h",
     "Abre sozinho na entrada da ferramenta, com ontem, hoje e onde agir. É gerado da saída "
     "dos modelos: <b>o Cronos empurra o insight, não espera pergunta</b>."),
    ("02-previsao", "Aba Previsão", "Quanto entra nos próximos dias",
     "Saída do Prophet. Trinta dias medidos emendados em duas semanas previstas, cada dia "
     "como <b>intervalo</b>: é a largura dele que dimensiona a escala da equipe."),
    ("03-projecao", "Aba Projeção", "Onde o ano fecha",
     "As violações acumuladas somadas ao risco da fila aberta e ao volume que ainda entra. "
     "<b>P3 projeta 208 e fica dentro do limite; P2 projeta 43 e passa de 39</b>."),
    ("10-modal-meta", "Projeção · régua da meta", "Como a meta é medida",
     "Os seis degraus da meta anual, direto do dicionário de dados da Locaweb. <b>O Cronos "
     "não define a régua</b>: ele diz em que degrau o ano está e em qual deve terminar."),
    ("04-fila", "Aba Fila", "Em qual caso olhar primeiro",
     "Os 49 casos abertos às 15h, ordenados do maior risco para o menor pela regressão "
     "logística, cada um com o <b>fator que mais pesa</b> e o ativo envolvido."),
    ("08-modal-escore", "Fila · explicabilidade", "Por que este caso e não outro",
     "A decomposição da pontuação: cada sinal entra como <b>peso vezes desvio da média</b>, "
     "e a soma reconstrói o valor exato. Modelo linear é explicável por construção."),
    ("05-saude", "Aba Saúde", "Que produto está pior",
     "Nota de 0 a 100 nos 15 produtos, com o componente que mais penaliza cada um e as "
     "colunas de <b>P3 e P2 separadas</b>."),
    ("09-modal-produto", "Saúde · detalhe do produto", "O que forma a nota",
     "Os cinco componentes da nota e quanto cada um pesa, com o histórico do produto. É o "
     "que separa <b>viola muito</b> de <b>vai começar a violar</b>."),
    ("06-causas", "Aba Causas", "O que compensa prevenir",
     "Códigos de fechamento ordenados por <b>taxa de violação, não por volume</b>: é assim "
     "que aparece a causa pequena que viola muito."),
]

MODELO = """<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<title>{titulo}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../abertura/base.css">
<style>
.pk .body{{padding:0;flex-direction:row;align-items:center;gap:26px}}
.pk .lado{{width:310px;flex-shrink:0;padding-left:26px}}
.pk .marca{{display:flex;align-items:center;gap:9px}}
.pk .marca .bi2{{width:30px;height:30px;border-radius:8px;background:var(--ink);
  display:flex;align-items:center;justify-content:center}}
.pk .marca .bi2 svg{{width:17px;height:17px}}
.pk .marca span{{font-size:16px;font-weight:800;letter-spacing:-.3px;color:#000}}
.pk .kk{{font-size:11.5px;font-weight:700;letter-spacing:2.4px;text-transform:uppercase;
  color:var(--accent);margin-top:34px}}
.pk h1{{font-size:31px;font-weight:800;letter-spacing:-1.1px;line-height:1.1;
  color:var(--head);margin-top:9px}}
.pk .cap2{{font-size:14.5px;line-height:1.55;color:var(--tx);margin-top:18px}}
.pk .cap2 b{{color:var(--head);font-weight:700}}
.pk .pil{{display:inline-block;margin-top:26px;font-size:12px;font-weight:600;
  padding:7px 15px;border-radius:999px;background:#fff;border:1px solid var(--line);
  color:var(--accent);box-shadow:0 4px 14px -8px rgba(37,99,235,.3)}}

.pk .win{{width:1216px;height:833px;flex-shrink:0;border-radius:14px;overflow:hidden;
  background:#fff;border:1px solid rgba(15,23,42,.14);
  box-shadow:0 -1px 0 rgba(255,255,255,.9) inset,
             0 54px 110px -44px rgba(15,23,42,.44),
             0 18px 40px -22px rgba(15,23,42,.22)}}
.pk .tabs{{height:32px;background:#D9E0EA;display:flex;align-items:flex-end;gap:9px;
  padding:0 14px}}
.pk .dots{{display:flex;gap:8px;flex-shrink:0;padding-bottom:9px}}
.pk .dots i{{width:11px;height:11px;border-radius:50%}}
.pk .dots i:nth-child(1){{background:#F2645A}}
.pk .dots i:nth-child(2){{background:#F4BE4F}}
.pk .dots i:nth-child(3){{background:#5FC466}}
.pk .tab{{height:26px;background:#fff;border-radius:9px 9px 0 0;display:flex;
  align-items:center;gap:9px;padding:0 13px;font-size:12.5px;font-weight:600;color:#33415A;
  max-width:290px;white-space:nowrap}}
.pk .tab .fav{{width:13px;height:13px;border-radius:4px;background:var(--ink);flex-shrink:0;
  display:flex;align-items:center;justify-content:center}}
.pk .tab .fav svg{{width:9px;height:9px}}
.pk .tab .x{{color:#9AA6B6;font-size:13px;margin-left:2px}}
.pk .plus{{color:#7E8B9E;font-size:15px;padding-bottom:6px}}
.pk .bar2{{height:40px;background:#fff;border-bottom:1px solid #E3E9F1;display:flex;
  align-items:center;gap:16px;padding:0 16px}}
.pk .nav{{display:flex;align-items:center;gap:15px;color:#7F8DA1;flex-shrink:0}}
.pk .nav svg{{width:17px;height:17px;stroke:currentColor;fill:none;stroke-width:1.9;
  stroke-linecap:round;stroke-linejoin:round}}
.pk .nav svg.off{{color:#C2CBD8}}
.pk .addr{{flex:1;max-width:720px;margin:0 auto;height:26px;background:#F1F4F8;
  border-radius:999px;display:flex;align-items:center;gap:9px;padding:0 15px;font-size:13px;
  color:#5C6B80;overflow:hidden;white-space:nowrap}}
.pk .addr svg{{width:13px;height:13px;stroke:#7C8AA0;fill:none;stroke-width:1.8;
  flex-shrink:0}}
.pk .addr .sch{{color:#9DAABB}}
.pk .addr b{{color:#1F2937;font-weight:600}}
.pk .rgt{{display:flex;align-items:center;gap:14px;color:#7F8DA1;flex-shrink:0}}
.pk .rgt svg{{width:17px;height:17px;stroke:currentColor;fill:none;stroke-width:1.9;
  stroke-linecap:round;stroke-linejoin:round}}
.pk .rgt .av{{width:20px;height:20px;border-radius:50%;background:#E3E9F1;
  border:1px solid #D3DBE6}}
.pk .win img{{display:block;width:100%}}
.pk .ft{{left:26px;right:26px;bottom:9px}}
</style></head><body>
<section class="slide light pk">
  <div class="mesh"></div><div class="grid-bg"></div>
  <div class="body">
    <div class="lado">
      <div class="marca">
        <span class="bi2"><svg viewBox="0 0 28 28" fill="none"><path d="M6 22L12 14L16 17L22 8" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="22" cy="8" r="3" fill="none" stroke="#3B82F6" stroke-width="1.5"/><circle cx="22" cy="8" r="1.2" fill="#3B82F6"/></svg></span>
        <span>Cronos</span>
      </div>
      <div class="kk">{eyebrow}</div>
      <h1>{titulo}</h1>
      <p class="cap2">{legenda}</p>
      <span class="pil">A aplicação · {pos} de {total}</span>
    </div>

    <div class="win">
      <div class="tabs">
        <span class="dots"><i></i><i></i><i></i></span>
        <span class="tab">
          <span class="fav"><svg viewBox="0 0 28 28" fill="none"><path d="M6 22L12 14L16 17L22 8" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
          Cronos · Painel operacional<span class="x">&times;</span>
        </span>
        <span class="plus">+</span>
      </div>
      <div class="bar2">
        <span class="nav">
          <svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg>
          <svg class="off" viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg>
          <svg viewBox="0 0 24 24"><path d="M20.5 12a8.5 8.5 0 1 1-2.6-6.1"/><path d="M20.5 4.5V10h-5.5"/></svg>
        </span>
        <span class="addr">
          <svg viewBox="0 0 24 24"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8.5 11V8a3.5 3.5 0 0 1 7 0v3"/></svg>
          <span class="sch">https://</span><b>cronos-locaweb.onrender.com</b><span class="sch">/</span>
        </span>
        <span class="rgt">
          <svg viewBox="0 0 24 24"><path d="M12 4l2.4 4.9 5.4.8-3.9 3.8.9 5.4-4.8-2.5-4.8 2.5.9-5.4L4.2 9.7l5.4-.8z"/></svg>
          <span class="av"></span>
        </span>
      </div>
      <img src="../../../../sprints/sprint-3/prints/{arquivo}.png" alt="{eyebrow}">
    </div>
  </div>
  <div class="ft"><span>Cronos · Super Data Bros · 2TSCOA</span><span>Challenge FIAP 2026 com Locaweb</span></div>
</section>
</body></html>
"""


def main() -> None:
    SAIDA.mkdir(parents=True, exist_ok=True)
    faltando = [n for n, *_ in TELAS if not (PRINTS / f"{n}.png").exists()]
    if faltando:
        raise FileNotFoundError(
            "captura ausente: " + ", ".join(faltando) + ". Rode antes: "
            ".venv/Scripts/python scripts/captura_telas.py"
        )
    total = len(TELAS)
    for pos, (arquivo, eyebrow, titulo, legenda) in enumerate(TELAS, 1):
        destino = SAIDA / f"tela-{pos:02d}-{arquivo}.html"
        destino.write_text(
            MODELO.format(
                arquivo=arquivo, eyebrow=eyebrow, titulo=titulo,
                legenda=legenda, pos=pos, total=total,
            ),
            encoding="utf-8",
        )
        print(f"  {destino.name}")


if __name__ == "__main__":
    main()

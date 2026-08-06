# -*- coding: utf-8 -*-
"""Tres naturezas do "coracao" da aba Fila, sobre o mesmo dado real.

O achado da aba: ordenar por risco concentra as violacoes no comeco da fila. Os 50
primeiros de 5.183 guardam 13 das 50 violacoes — 27 vezes o acaso — enquanto ordenar
pela prioridade declarada pega zero nos mesmos 50.

As tres versoes contam esse mesmo fato de jeitos diferentes, para o Igor escolher qual
natureza vira o padrao das quatro abas.
"""
import json
from pathlib import Path

RAIZ = Path.cwd()
OUT = RAIZ / 'prototipos' / 'telas' / 'mockups' / 'coracao-fila.html'
OUT.parent.mkdir(parents=True, exist_ok=True)
C = json.loads((RAIZ / 'data' / 'app' / 'fila_curvas.json').read_text(encoding='utf-8'))

CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
:root{--pg:#F6F7F9;--c:#FFF;--ink:#0C1017;--ln:rgba(12,16,23,.09);--ln2:rgba(12,16,23,.18);
 --tx:#4E586B;--tx2:#7B8598;--tx3:#A3ABBA;--hd:#0C1017;--ac:#2563EB;--acl:#EFF4FF;
 --no:#DC2626;--nol:#FEF2F2;--wn:#B45309;--ok:#059669;--okl:#ECFDF5;
 --e:cubic-bezier(.19,1,.22,1);--e2:cubic-bezier(.34,1.56,.64,1);
 --s1:0 1px 2px rgba(12,16,23,.04),0 10px 26px -14px rgba(12,16,23,.14);
 --s2:0 2px 6px rgba(12,16,23,.06),0 28px 54px -20px rgba(12,16,23,.2)}
html{-webkit-font-smoothing:antialiased}
body{background:var(--pg);color:var(--hd);font-family:'Outfit',system-ui,sans-serif;
 font-size:15px;letter-spacing:-.011em;padding:34px 30px 90px}
.wrap{max-width:1120px;margin:0 auto}
h1{font-size:28px;font-weight:650;letter-spacing:-.035em}
.sub{font-size:14.5px;color:var(--tx);margin-top:9px;max-width:78ch;line-height:1.62}
.sub b{color:var(--hd);font-weight:650}
.op{margin-top:36px;background:var(--c);border:1px solid var(--ln);border-radius:24px;
 padding:26px 28px 26px;box-shadow:var(--s1)}
.op-h{display:flex;align-items:flex-start;gap:14px;margin-bottom:22px}
.op-n{font-size:12px;font-weight:800;letter-spacing:.1em;color:var(--ac);background:var(--acl);
 border:1px solid rgba(37,99,235,.2);border-radius:10px;padding:6px 12px;flex-shrink:0}
.op-h h2{font-size:20px;font-weight:650;letter-spacing:-.03em}
.op-h p{font-size:13px;color:var(--tx2);margin-top:3px;max-width:78ch;line-height:1.55}
.pro{font-size:12px;color:var(--tx2);margin-top:20px;padding-top:15px;
 border-top:1px solid var(--ln);display:flex;gap:28px;flex-wrap:wrap}
.pro b{color:var(--hd);font-weight:650;display:block;font-size:11px;letter-spacing:.06em;
 text-transform:uppercase;margin-bottom:3px}
.pro div{max-width:36ch;line-height:1.5}

/* ══ 01 · instrumento ══════════════════════════════════════════════════ */
.ins{display:grid;grid-template-columns:1fr 300px;gap:26px;align-items:center}
.ins-q{font-size:22px;font-weight:600;letter-spacing:-.03em;margin-bottom:18px}
.ins-q b{color:var(--ac);font-variant-numeric:tabular-nums}
.rg{position:relative;height:56px}
.rg .trilho{position:absolute;inset:22px 0 auto 0;height:10px;border-radius:5px;
 background:linear-gradient(90deg,#DC2626 0%,#F0A02A 8%,#CBD5E1 26%,#E7EAF0 100%)}
.rg .cortado{position:absolute;inset:22px auto auto 0;height:10px;border-radius:5px 0 0 5px;
 background:linear-gradient(90deg,rgba(12,16,23,.82),rgba(12,16,23,.5));
 transition:width .08s linear}
.rg input{position:absolute;inset:14px -8px auto -8px;width:calc(100% + 16px);margin:0}
.rg .marcas{position:absolute;inset:auto 0 8px 0;height:11px}
.rg .marcas i{position:absolute;bottom:0;width:2px;height:11px;background:var(--no);
 opacity:.8;border-radius:1px}
.rg-x{display:flex;justify-content:space-between;font-size:10px;color:var(--tx3);
 letter-spacing:.06em;text-transform:uppercase;margin-top:2px}
.res{display:flex;flex-direction:column;gap:11px}
.res-b{background:var(--pg);border:1px solid var(--ln);border-radius:15px;padding:14px 16px}
.res-b em{font-size:10px;font-style:normal;font-weight:700;letter-spacing:.1em;
 text-transform:uppercase;color:var(--tx3);display:block}
.res-b b{font-size:30px;font-weight:700;letter-spacing:-.045em;display:block;margin-top:4px;
 line-height:1;font-variant-numeric:tabular-nums}
.res-b span{font-size:11.5px;color:var(--tx2);display:block;margin-top:4px;line-height:1.45}
.res-b.dk{background:var(--ink);border-color:var(--ink)}
.res-b.dk em{color:#8D97A8}.res-b.dk b{color:#fff}.res-b.dk span{color:#8D97A8}
.res-b.dk b.no{color:#FF7D74}
.cmp{display:flex;gap:10px;margin-top:16px}
.cmp div{flex:1;background:var(--pg);border:1px solid var(--ln);border-radius:13px;
 padding:11px 13px}
.cmp em{font-size:10px;font-style:normal;letter-spacing:.08em;text-transform:uppercase;
 color:var(--tx3);font-weight:700;display:block}
.cmp b{font-size:19px;font-weight:650;display:block;margin-top:3px;
 font-variant-numeric:tabular-nums}
.cmp span{font-size:10.5px;color:var(--tx2)}

/* ══ 02 · manifesto ════════════════════════════════════════════════════ */
.man{text-align:center;padding:8px 0 4px}
.man-n{font-size:96px;font-weight:800;letter-spacing:-.06em;line-height:.86;
 background:linear-gradient(100deg,#0C1017 30%,#2563EB);-webkit-background-clip:text;
 background-clip:text;color:transparent}
.man-f{font-size:20px;font-weight:500;color:var(--tx);margin-top:12px;line-height:1.45}
.man-f b{color:var(--hd);font-weight:650}
.faixa{margin:28px 0 6px;position:relative}
.faixa-b{height:60px;border-radius:10px;overflow:hidden;position:relative;
 background:linear-gradient(90deg,#DC2626 0%,#F0A02A 6%,#93A3BC 22%,#DDE2EA 100%)}
.faixa-b i{position:absolute;top:0;bottom:0;width:2px;background:#0C1017;
 animation:sobe .5s var(--e2) both}
@keyframes sobe{from{transform:scaleY(0)}}
.faixa-l{display:flex;justify-content:space-between;font-size:10.5px;color:var(--tx3);
 margin-top:7px;letter-spacing:.05em;text-transform:uppercase}
.faixa-c{position:absolute;top:-9px;bottom:-9px;border-left:2px dashed var(--ink);
 padding-left:9px;font-size:11px;font-weight:650;color:var(--ink);white-space:nowrap}
.man-g{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:26px}
.man-g div{background:var(--pg);border:1px solid var(--ln);border-radius:16px;
 padding:16px 18px;text-align:left}
.man-g em{font-size:10px;font-style:normal;font-weight:700;letter-spacing:.1em;
 text-transform:uppercase;color:var(--tx3);display:block}
.man-g b{font-size:26px;font-weight:700;letter-spacing:-.04em;display:block;margin-top:5px;
 line-height:1;font-variant-numeric:tabular-nums}
.man-g span{font-size:11.5px;color:var(--tx2);display:block;margin-top:4px;line-height:1.45}
.man-g .no b{color:var(--no)}.man-g .ok b{color:var(--ok)}

/* ══ 03 · ambiente ═════════════════════════════════════════════════════ */
.amb{position:relative;height:290px;border-radius:18px;overflow:hidden;
 background:radial-gradient(120% 90% at 8% 50%,#101725,#070A10)}
.amb canvas{position:absolute;inset:0;width:100%;height:100%}
.amb-t{position:absolute;inset:auto auto 18px 20px;color:#E8ECF3;pointer-events:none}
.amb-t b{font-size:30px;font-weight:700;letter-spacing:-.04em;display:block;line-height:1}
.amb-t span{font-size:12.5px;color:#8D97A8;display:block;margin-top:5px}
.amb-l{position:absolute;inset:18px 20px auto auto;display:flex;gap:14px;color:#8D97A8;
 font-size:11px}
.amb-l span{display:inline-flex;align-items:center;gap:6px}
.amb-l i{width:8px;height:8px;border-radius:50%}
.amb-h{position:absolute;inset:18px auto auto 20px;font-size:10px;font-weight:700;
 letter-spacing:.14em;text-transform:uppercase;color:#5F697C}

.leg{display:flex;gap:16px;margin-top:12px;flex-wrap:wrap;font-size:11px;color:var(--tx2)}
.leg span{display:inline-flex;align-items:center;gap:6px}
.leg i{width:12px;height:8px;border-radius:2px}
input[type=range]{-webkit-appearance:none;appearance:none;background:0;cursor:pointer;height:20px}
input[type=range]::-webkit-slider-runnable-track{height:20px;background:0}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:22px;height:22px;
 border-radius:50%;background:var(--c);border:3px solid var(--ink);
 box-shadow:0 3px 10px rgba(12,16,23,.3);margin-top:0}
@media (max-width:880px){.ins{grid-template-columns:1fr}.man-g{grid-template-columns:1fr}}
"""

JS = r"""
const C = __C__;
const nb = (v, c = 0) => v.toFixed(c).replace('.', ',');
const N = C.n, V = C.v;

/* ── 01 · instrumento ─────────────────────────────────────────────────── */
const sl = document.getElementById('sl');
function interp(arr, k) {           // curva amostrada em 200 pontos
  let i = 0; while (i < C.x.length - 1 && C.x[i + 1] < k) i++;
  return arr[i];
}
function atualiza() {
  const k = +sl.value;
  const pega = interp(C.risco, k), pri = interp(C.prioridade, k),
        aca = k * V / N, teto = Math.min(k, V);
  document.getElementById('i-k').textContent = k.toLocaleString('pt-BR');
  document.getElementById('i-pc').textContent = nb(k / N * 100, 1);
  document.getElementById('i-pega').textContent = pega;
  document.getElementById('i-share').textContent = nb(pega / V * 100, 0);
  document.getElementById('i-lift').textContent = nb(pega / aca, 1);
  document.getElementById('i-pri').textContent = pri;
  document.getElementById('i-aca').textContent = nb(aca, 1);
  document.getElementById('i-teto').textContent = teto;
  document.getElementById('cortado').style.width = (k / N * 100) + '%';
}
sl.oninput = atualiza; atualiza();
// as marcas de violacao na regua
document.getElementById('marcas').innerHTML = C.marcas
  .map(p => `<i style="left:${(p / N * 100).toFixed(3)}%"></i>`).join('');

/* ── 02 · manifesto ───────────────────────────────────────────────────── */
document.getElementById('fx').innerHTML = C.marcas
  .map((p, j) => `<i style="left:${(p / N * 100).toFixed(3)}%;animation-delay:${j * 22}ms"></i>`)
  .join('');

/* ── 03 · ambiente ────────────────────────────────────────────────────── */
const cv = document.getElementById('cv'), cx = cv.getContext('2d');
let W, H, pts = [], t0 = performance.now();
function dim() {
  const r = cv.getBoundingClientRect(), dpr = devicePixelRatio || 1;
  W = r.width; H = r.height; cv.width = W * dpr; cv.height = H * dpr;
  cx.setTransform(dpr, 0, 0, dpr, 0, 0);
  const n = C.pontos.length;
  pts = C.pontos.map((p, i) => {
    const col = Math.floor(i / 26), lin = i % 26;
    return { risco: p[0], viol: p[1],
             ax: 40 + col * ((W - 80) / Math.ceil(n / 26)), ay: 26 + lin * ((H - 90) / 25),
             fase: Math.random() * 6.28, amp: .6 + Math.random() * 1.1,
             x: Math.random() * W, y: Math.random() * H };
  });
}
function pinta(t) {
  const dt = Math.min((t - t0) / 1400, 1), s = 1 - Math.pow(1 - dt, 3);
  cx.clearRect(0, 0, W, H);
  for (const p of pts) {
    const x = p.x + (p.ax - p.x) * s + Math.sin(t / 1600 + p.fase) * p.amp;
    const y = p.y + (p.ay - p.y) * s + Math.cos(t / 1900 + p.fase) * p.amp;
    const alto = p.risco >= 10, medio = p.risco >= 3;
    if (p.viol) {
      const pulso = .55 + .45 * Math.sin(t / 620 + p.fase);
      cx.beginPath(); cx.arc(x, y, 6.5, 0, 6.29);
      cx.fillStyle = `rgba(240,72,62,${.13 * pulso})`; cx.fill();
      cx.beginPath(); cx.arc(x, y, 2.6, 0, 6.29);
      cx.fillStyle = `rgba(255,120,110,${.75 + .25 * pulso})`; cx.fill();
    } else {
      cx.beginPath(); cx.arc(x, y, alto ? 2.4 : medio ? 1.9 : 1.5, 0, 6.29);
      cx.fillStyle = alto ? 'rgba(240,160,42,.72)'
                   : medio ? 'rgba(120,150,210,.5)' : 'rgba(120,140,175,.26)';
      cx.fill();
    }
  }
  requestAnimationFrame(pinta);
}
addEventListener('resize', dim);
dim(); requestAnimationFrame(pinta);
""".replace('__C__', json.dumps(C, separators=(',', ':')))

HTML = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cronos · três corações para a aba Fila</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<div class="wrap">
  <h1>Três corações para a aba Fila</h1>
  <p class="sub">O mesmo achado, contado de três jeitos. O achado é este: ordenar por risco
    concentra as violações no começo da fila. Nos <b>50 primeiros de 5.183</b> estão
    <b>13 das 50</b> violações do trimestre — <b>27 vezes</b> o que o acaso daria. Ordenar
    pela prioridade declarada pega <b>zero</b> nos mesmos 50. Escolha a natureza e ela vira o
    padrão das quatro abas.</p>

  <section class="op">
    <div class="op-h"><span class="op-n">01</span>
      <div><h2>Instrumento · se mexe e ensina</h2>
        <p>A pergunta que a operação faz de verdade é "até onde eu desço a fila hoje?".
          Arraste o corte e veja o que você pega, o que deixa passar e como isso se compara
          a trabalhar pela prioridade declarada.</p></div></div>

    <div class="ins">
      <div>
        <div class="ins-q">Olhando os <b id="i-k">50</b> primeiros da fila
          <span style="color:var(--tx3);font-weight:400">· <span id="i-pc">1,0</span>% do total</span></div>
        <div class="rg">
          <div class="trilho"></div><div class="cortado" id="cortado"></div>
          <input type="range" id="sl" min="10" max="2000" value="50" step="10">
          <div class="marcas" id="marcas"></div>
        </div>
        <div class="rg-x"><span>1º</span><span>cada risco vermelho é uma violação real</span>
          <span>2.000º</span></div>
        <div class="cmp">
          <div><em>pela prioridade</em><b id="i-pri">0</b><span>o critério de hoje</span></div>
          <div><em>pelo acaso</em><b id="i-aca">0,5</b><span>se fosse sorteio</span></div>
          <div><em>teto possível</em><b id="i-teto">50</b><span>se soubesse o futuro</span></div>
        </div>
      </div>
      <div class="res">
        <div class="res-b dk"><em>você pega</em><b class="no"><span id="i-pega">13</span> de 50</b>
          <span><span id="i-share">26</span>% das violações do trimestre</span></div>
        <div class="res-b"><em>ganho sobre o acaso</em><b><span id="i-lift">27,0</span>×</b>
          <span>quantas vezes melhor que sortear</span></div>
      </div>
    </div>
    <div class="pro">
      <div><b>a favor</b>Responde a pergunta operacional real e o usuário descobre o achado
        sozinho, mexendo. Vira ferramenta de decisão, não gráfico.</div>
      <div><b>contra</b>Se ninguém arrastar, a aba não diz nada. Depende de intenção.</div>
    </div>
  </section>

  <section class="op">
    <div class="op-h"><span class="op-n">02</span>
      <div><h2>Manifesto · afirma e prova</h2>
        <p>A fila inteira desenhada como uma faixa: da esquerda, maior risco, para a direita,
          menor. Cada traço preto é uma violação real. Elas se amontoam no começo — a prova
          visual de que a ordenação funciona, sem precisar de legenda.</p></div></div>

    <div class="man">
      <div class="man-n">27×</div>
      <div class="man-f">é o quanto ordenar por risco supera o acaso<br>
        nos <b>50 primeiros</b> casos da fila</div>
      <div class="faixa">
        <div class="faixa-b" id="fx"></div>
        <div class="faixa-c" style="left:0.96%">50º</div>
      </div>
      <div class="faixa-l"><span>maior risco</span><span>5.183 incidentes do trimestre</span>
        <span>menor risco</span></div>
      <div class="man-g">
        <div class="no"><em>nos 50 primeiros</em><b>13</b>
          <span>de 50 violações · 1% da fila guardando 26% do risco</span></div>
        <div><em>metade das violações</em><b>337º</b>
          <span>posição até onde está metade de tudo que estourou</span></div>
        <div class="ok"><em>pela prioridade declarada</em><b>0</b>
          <span>violações capturadas nos mesmos 50 primeiros</span></div>
      </div>
    </div>
    <div class="pro">
      <div><b>a favor</b>Impressiona no primeiro segundo e a prova está no desenho: dá para
        ver os traços se amontoando à esquerda. Não depende de ninguém interagir.</div>
      <div><b>contra</b>Diz uma coisa só. Depois de ver duas vezes, já foi.</div>
    </div>
  </section>

  <section class="op">
    <div class="op-h"><span class="op-n">03</span>
      <div><h2>Ambiente · reage e respira</h2>
        <p>Cada ponto é um incidente da fila, se acomodando na posição por risco. Os que
          violaram o prazo pulsam em vermelho. Não pede nada do usuário: cria a sensação de
          operação viva e situa antes de qualquer número.</p></div></div>

    <div class="amb">
      <canvas id="cv"></canvas>
      <div class="amb-h">a fila do trimestre</div>
      <div class="amb-l"><span><i style="background:#F0A02A"></i>risco acima de 10%</span>
        <span><i style="background:#FF786E"></i>violou o prazo</span>
        <span><i style="background:rgba(120,140,175,.5)"></i>rotina</span></div>
      <div class="amb-t"><b>5.183 incidentes</b>
        <span>ordenados por risco, da esquerda para a direita ·
          os 50 vermelhos são as violações reais</span></div>
    </div>
    <div class="pro">
      <div><b>a favor</b>Dá vida e identidade imediata, e é o mais fora do padrão dos três.
        Funciona como plano de fundo de qualquer aba.</div>
      <div><b>contra</b>Bonito mas pouco preciso: você não lê número nenhum dele. Precisaria
        de um segundo elemento em cima para informar.</div>
    </div>
  </section>
</div>
<script>{JS}</script></body></html>"""

OUT.write_text(HTML, encoding='utf-8')
print(f'{OUT}  ({len(HTML) / 1024:.0f} kB)')

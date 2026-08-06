# -*- coding: utf-8 -*-
"""Tres comportamentos do grafico do heroi quando o usuario viaja no tempo.

Mesmo dado, mesmo desenho, mesma linha do tempo. So muda o que o grafico faz quando o
dia avanca. Os tres rodam juntos e em sincronia — aperta play em cima e os tres andam
ao mesmo tempo, para a comparacao ser justa.
"""
import json
from pathlib import Path

RAIZ = Path.cwd()
OUT = RAIZ / 'prototipos' / 'telas' / 'mockups' / 'grafico-no-tempo.html'
OUT.parent.mkdir(parents=True, exist_ok=True)
D = json.loads((RAIZ / 'data' / 'app' / 'dias.json').read_text(encoding='utf-8'))

CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
:root{--pg:#F6F7F9;--c:#FFF;--ink:#0C1017;--ln:rgba(12,16,23,.09);--ln2:rgba(12,16,23,.18);
 --tx:#4E586B;--tx2:#7B8598;--tx3:#A3ABBA;--hd:#0C1017;--ac:#2563EB;--acl:#EFF4FF;
 --no:#DC2626;--nol:#FEF2F2;--wn:#B45309;--wnl:#FFFAEC;--ok:#059669;--okl:#ECFDF5;
 --e:cubic-bezier(.19,1,.22,1);
 --s1:0 1px 2px rgba(12,16,23,.04),0 10px 26px -14px rgba(12,16,23,.14);
 --s2:0 2px 6px rgba(12,16,23,.06),0 28px 54px -20px rgba(12,16,23,.2)}
html{-webkit-font-smoothing:antialiased}
body{background:var(--pg);color:var(--hd);font-family:'Outfit',system-ui,sans-serif;
 font-size:15px;letter-spacing:-.011em;padding:30px 28px 80px}
.wrap{max-width:1180px;margin:0 auto}
h1{font-size:27px;font-weight:650;letter-spacing:-.035em}
.sub{font-size:14px;color:var(--tx);margin-top:8px;max-width:76ch;line-height:1.6}
.sub b{color:var(--hd);font-weight:650}
/* comando comum aos tres */
.cmd{position:sticky;top:14px;z-index:9;background:var(--ink);border-radius:16px;
 padding:13px 18px;margin:22px 0 4px;display:flex;align-items:center;gap:16px;
 box-shadow:var(--s2)}
.play{background:var(--ac);border:0;color:#fff;width:36px;height:36px;border-radius:11px;
 cursor:pointer;display:grid;place-items:center;flex-shrink:0}
.play:active{transform:scale(.95)}
.cmd-d{flex-shrink:0;min-width:118px;color:#E8ECF3}
.cmd-d b{font-size:15px;font-weight:650;display:block;font-variant-numeric:tabular-nums}
.cmd-d span{font-size:10.5px;color:#8D97A8;font-variant-numeric:tabular-nums}
.lin{position:relative;height:36px;cursor:pointer;flex:1}
.lin .base{position:absolute;inset:auto 0 14px 0;height:3px;border-radius:2px;
 background:rgba(255,255,255,.14)}
.lin .feito{position:absolute;inset:auto auto 14px 0;height:3px;border-radius:2px;
 background:var(--ac)}
.lin .cab{position:absolute;bottom:9px;width:12px;height:12px;border-radius:50%;background:#fff;
 border:3px solid var(--ac);transform:translateX(-50%);transition:left .1s linear}
.lin .falha{position:absolute;bottom:17px;width:2px;height:8px;background:rgba(240,72,62,.7);
 transform:translateX(-50%)}
.lin .mes{position:absolute;bottom:0;font-size:9px;color:#5F697C;letter-spacing:.1em;
 text-transform:uppercase;font-weight:600}
.vel{display:flex;gap:2px;background:rgba(255,255,255,.07);border-radius:9px;padding:3px}
.vel button{background:0;border:0;font:inherit;font-size:10.5px;font-weight:650;color:#8D97A8;
 padding:5px 9px;border-radius:6px;cursor:pointer}
.vel button.on{background:rgba(255,255,255,.14);color:#fff}
/* cada opcao */
.op{margin-top:20px;background:var(--c);border:1px solid var(--ln);border-radius:22px;
 padding:20px 22px;box-shadow:var(--s1)}
.op-h{display:flex;align-items:flex-start;gap:13px;margin-bottom:14px}
.op-n{font-size:11.5px;font-weight:800;letter-spacing:.1em;color:var(--ac);background:var(--acl);
 border:1px solid rgba(37,99,235,.2);border-radius:9px;padding:5px 11px;flex-shrink:0}
.op-h h2{font-size:18px;font-weight:650;letter-spacing:-.03em}
.op-h p{font-size:12.5px;color:var(--tx2);margin-top:2px;max-width:80ch;line-height:1.5}
.corpo{display:grid;grid-template-columns:1fr 300px;gap:22px;align-items:center}
.gr svg{width:100%;height:auto;display:block;overflow:visible}
.g-grade{stroke:var(--ln);stroke-width:1}
.g-y,.g-x{fill:var(--tx3);font-size:9.5px;font-family:'Outfit',sans-serif}
.g-bd{fill:var(--ac);opacity:.12}
.g-prev{fill:none;stroke:var(--ac);stroke-width:2.2;stroke-dasharray:6 5;opacity:.7}
.g-real{fill:none;stroke:var(--ink);stroke-width:3;stroke-linecap:round;stroke-linejoin:round}
.g-hist{fill:none;stroke:var(--ac);stroke-width:3;stroke-linecap:round;stroke-linejoin:round}
.g-ag{stroke:var(--ln2);stroke-width:1;stroke-dasharray:2 3}
.g-no{fill:var(--ink);stroke:#fff;stroke-width:2.5}
.g-fora{fill:var(--no)}
.g-rot{fill:var(--tx3);font-size:9.5px;font-weight:600;font-family:'Outfit',sans-serif;
 letter-spacing:.06em;text-transform:uppercase}
.nums{display:flex;flex-direction:column;gap:9px}
.n-b{background:var(--pg);border:1px solid var(--ln);border-radius:14px;padding:12px 14px}
.n-b em{font-size:9.5px;font-style:normal;font-weight:700;letter-spacing:.1em;
 text-transform:uppercase;color:var(--tx3);display:block}
.n-b b{font-size:26px;font-weight:700;letter-spacing:-.04em;display:block;margin-top:3px;
 line-height:1;font-variant-numeric:tabular-nums}
.n-b span{font-size:11px;color:var(--tx2);display:block;margin-top:3px}
.n-b.ok b{color:var(--ok)}.n-b.no b{color:var(--no)}.n-b.wn b{color:var(--wn)}
.leg{display:flex;gap:14px;margin-top:9px;flex-wrap:wrap}
.leg span{display:inline-flex;align-items:center;gap:5px;font-size:10.5px;color:var(--tx2)}
.leg i{width:14px;height:3px;border-radius:2px}
.l-p{background:var(--ac);opacity:.7}.l-r{background:var(--ink)}
.l-b{background:var(--ac);opacity:.2;height:9px;border-radius:3px}
.pro{font-size:11.5px;color:var(--tx2);margin-top:14px;padding-top:12px;
 border-top:1px solid var(--ln);display:flex;gap:26px;flex-wrap:wrap}
.pro b{color:var(--hd);font-weight:650;display:block;font-size:10.5px;letter-spacing:.06em;
 text-transform:uppercase;margin-bottom:3px}
.pro div{max-width:38ch;line-height:1.5}
@media (max-width:900px){.corpo{grid-template-columns:1fr}}
"""

JS = r"""
const D = __D__, DIAS = D.dias, ANTES = D.antes, N = DIAS.length;
// serie real continua: 45 dias antes do corte + os 92 do trimestre
const REAL = ANTES.map(a => ({ dm: a.dm, real: a.real }))
  .concat(DIAS.map(d => ({ dm: d.dm, real: d.real })));
const OFF = ANTES.length;
const nb = (v, c = 0) => Number(v).toFixed(c).replace('.', ',');
let i = 0, tocando = null, vel = 130;

const W = 620, H = 210;
const suave = (p) => p.length < 2 ? '' : 'M' + p[0][0].toFixed(1) + ' ' + p[0][1].toFixed(1) +
  p.slice(1).map((q, k) => {
    const a = p[k], m = (a[0] + q[0]) / 2;
    return ` C${m.toFixed(1)} ${a[1].toFixed(1)} ${m.toFixed(1)} ${q[1].toFixed(1)} ${q[0].toFixed(1)} ${q[1].toFixed(1)}`;
  }).join('');

function eixo(mx, px, py, rotulos) {
  const marcas = [0, Math.round(mx / 2 / 20) * 20, Math.round(mx * .88 / 20) * 20];
  return marcas.map(v => `<line class="g-grade" x1="26" y1="${py(v).toFixed(1)}" x2="${W}" y2="${py(v).toFixed(1)}"/>
    <text class="g-y" x="20" y="${(py(v) + 3.5).toFixed(1)}" text-anchor="end">${v}</text>`).join('')
    + rotulos.map(r => `<text class="g-x" x="${r.x.toFixed(1)}" y="${H - 4}" text-anchor="middle">${r.t}</text>`).join('');
}

/* ── A · a janela caminha: 30 dias antes daquele dia + a previsão dali ──── */
function grafA(el) {
  const d = DIAS[i], fim = OFF + i;
  const hist = REAL.slice(Math.max(0, fim - 29), fim + 1);
  const fut = DIAS.slice(i + 1, i + 7);
  const n = hist.length + fut.length;
  const vals = hist.map(h => h.real).concat(fut.map(f => f.alto)).concat([d.alto]);
  const mx = Math.max(...vals) * 1.12;
  const px = k => 30 + k / (n - 1) * (W - 42), py = v => H - 22 - v / mx * (H - 40);
  const ph = hist.map((h, k) => [px(k), py(h.real)]);
  const no = ph[ph.length - 1];
  const pf = [no].concat(fut.map((f, k) => [px(hist.length + k), py(f.prev)]));
  const alto = fut.map((f, k) => [px(hist.length + k), py(f.alto)]);
  const baixo = fut.map((f, k) => [px(hist.length + k), py(f.baixo)]).reverse();
  const banda = fut.length ? `M${no[0].toFixed(1)} ${no[1].toFixed(1)} L`
    + alto.concat(baixo).map(p => `${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(' L') + ' Z' : '';
  el.innerHTML = `<svg viewBox="0 0 ${W} ${H}">
    ${eixo(mx, px, py, [{ x: px(0), t: hist[0].dm }, { x: no[0], t: d.dm }, { x: px(n - 1), t: fut.length ? fut[fut.length - 1].dm : d.dm }])}
    ${banda ? `<path class="g-bd" d="${banda}"/>` : ''}
    <path class="g-hist" d="${suave(ph)}"/>
    ${fut.length ? `<path class="g-prev" d="${suave(pf)}"/>` : ''}
    <line class="g-ag" x1="${no[0].toFixed(1)}" y1="8" x2="${no[0].toFixed(1)}" y2="${H - 18}"/>
    <circle class="g-no" cx="${no[0].toFixed(1)}" cy="${no[1].toFixed(1)}" r="6"/>
  </svg>`;
}

/* ── B · o real desenha por cima da previsão, do início do trimestre ────── */
function grafB(el) {
  const mx = Math.max(...DIAS.map(d => d.alto)) * 1.08;
  const px = k => 30 + k / (N - 1) * (W - 42), py = v => H - 22 - v / mx * (H - 40);
  const pp = DIAS.map((d, k) => [px(k), py(d.prev)]);
  const alto = DIAS.map((d, k) => [px(k), py(d.alto)]);
  const baixo = DIAS.map((d, k) => [px(k), py(d.baixo)]).reverse();
  const pr = DIAS.slice(0, i + 1).map((d, k) => [px(k), py(d.real)]);
  const fora = DIAS.slice(0, i + 1).map((d, k) => d.dentro ? '' :
    `<circle class="g-fora" cx="${px(k).toFixed(1)}" cy="${py(d.real).toFixed(1)}" r="2.6"/>`).join('');
  el.innerHTML = `<svg viewBox="0 0 ${W} ${H}">
    ${eixo(mx, px, py, [{ x: px(0), t: 'out' }, { x: px(45), t: 'nov' }, { x: px(N - 1), t: 'dez' }])}
    <path class="g-bd" d="M${alto.concat(baixo).map(p => `${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(' L')} Z"/>
    <path class="g-prev" d="${suave(pp)}"/>
    ${pr.length > 1 ? `<path class="g-real" d="${suave(pr)}"/>` : ''}
    ${fora}
    <line class="g-ag" x1="${px(i).toFixed(1)}" y1="8" x2="${px(i).toFixed(1)}" y2="${H - 18}"/>
    <circle class="g-no" cx="${px(i).toFixed(1)}" cy="${py(DIAS[i].real).toFixed(1)}" r="6"/>
  </svg>`;
}

/* ── C · rodando desenha; parado, aproxima no dia ───────────────────────── */
function grafC(el) { tocando ? grafB(el) : grafA(el); }

function nums(id) {
  const d = DIAS[i];
  const dif = d.real - d.prev;
  return `
    <div class="n-b ${d.acum >= 80 ? 'ok' : d.acum >= 55 ? 'wn' : 'no'}">
      <em>acerto acumulado</em><b>${nb(d.acum, 1)}%</b>
      <span>${DIAS.slice(0, i + 1).filter(x => x.dentro).length} de ${i + 1} dias na faixa</span></div>
    <div class="n-b"><em>o dia visitado</em><b>${nb(d.prev)} → ${d.real}</b>
      <span>previsto contra real · ${dif > 0 ? '+' : '−'}${nb(Math.abs(dif), 1)}</span></div>
    <div class="n-b ${d.acima10 ? 'no' : ''}"><em>a fila daquele dia</em><b>${d.casos}</b>
      <span>${d.acima10 ? d.acima10 + ' acima de 10%' : 'nenhum acima de 10%'} ·
        ${d.violou} violaram</span></div>`;
}

const G = [grafA, grafB, grafC];
function pinta() {
  const d = DIAS[i];
  G.forEach((f, k) => { f(document.getElementById('g' + k));
    document.getElementById('n' + k).innerHTML = nums(k); });
  document.getElementById('c-dia').textContent = `${d.rot} ${d.dm}`;
  document.getElementById('c-pos').textContent = `dia ${i + 1} de ${N}`;
  const p = i / (N - 1) * 100;
  document.getElementById('cab').style.left = p + '%';
  document.getElementById('feito').style.width = p + '%';
}
function vai(k) { i = Math.min(N - 1, Math.max(0, k)); pinta(); }

const lin = document.getElementById('lin');
lin.insertAdjacentHTML('beforeend', DIAS.map((d, k) => d.dentro ? '' :
  `<span class="falha" style="left:${(k / (N - 1) * 100).toFixed(2)}%"></span>`).join('')
  + [['out', 0], ['nov', 31], ['dez', 61]].map(([m, k]) =>
    `<span class="mes" style="left:${(k / (N - 1) * 100).toFixed(2)}%">${m}</span>`).join(''));
lin.onclick = e => { const b = lin.getBoundingClientRect();
  vai(Math.round((e.clientX - b.left) / b.width * (N - 1))); };

const play = document.getElementById('play');
const PL = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>';
const PA = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><rect x="6.5" y="5" width="4" height="14" rx="1"/><rect x="13.5" y="5" width="4" height="14" rx="1"/></svg>';
function para() { clearInterval(tocando); tocando = null; play.innerHTML = PL; pinta(); }
play.onclick = () => {
  if (tocando) return para();
  if (i >= N - 1) i = 0;
  play.innerHTML = PA;
  tocando = setInterval(() => { i >= N - 1 ? para() : vai(i + 1); }, vel);
  pinta();
};
document.querySelectorAll('.vel button').forEach(b => b.onclick = () => {
  document.querySelectorAll('.vel button').forEach(x => x.classList.remove('on'));
  b.classList.add('on'); vel = +b.dataset.v;
  if (tocando) { clearInterval(tocando);
    tocando = setInterval(() => { i >= N - 1 ? para() : vai(i + 1); }, vel); }
});
pinta();
""".replace('__D__', json.dumps(D, ensure_ascii=False, separators=(',', ':')))

OPCOES = [
    ('01', 'A janela caminha com você',
     'O gráfico mostra sempre os 30 dias anteriores ao dia visitado e a previsão feita dali '
     'para a frente. O nó anda e a linha se refaz. Você vê o que o modelo via naquele momento.',
     'Fiel ao que o operador veria naquele dia. O gráfico continua sendo o mesmo da tela '
     'principal, só que deslocado no tempo.',
     'Você perde a visão do trimestre: não dá para ver o erro se acumulando.'),
    ('02', 'O real desenha por cima do previsto',
     'A previsão do trimestre inteiro fica desenhada, e a linha escura do que de fato '
     'aconteceu vai avançando por cima dela. Os pontos vermelhos são os dias que saíram da faixa.',
     'A divergência entre as duas linhas cresce na sua frente. É a leitura mais forte do '
     'achado: a previsão fica em cima e o real despenca.',
     'Não é mais o gráfico do dia: vira um gráfico de avaliação do modelo, outro assunto.'),
    ('03', 'Rodando avalia, parado aproxima',
     'Enquanto o play está rodando, comporta-se como o 02. Quando você para, ele vira o 01 e '
     'aproxima no dia em que parou.',
     'Junta os dois: a visão macro enquanto corre e o detalhe quando para. É o que eu faria.',
     'Duas leituras num elemento só. Se o usuário não perceber a troca, pode confundir.'),
]

blocos = ''.join(f'''
  <section class="op">
    <div class="op-h"><span class="op-n">{n}</span>
      <div><h2>{t}</h2><p>{d}</p></div></div>
    <div class="corpo">
      <div><div class="gr" id="g{k}"></div>
        <div class="leg"><span><i class="l-r"></i>o que aconteceu</span>
          <span><i class="l-p"></i>o que o modelo previu</span>
          <span><i class="l-b"></i>faixa de 80%</span></div></div>
      <div class="nums" id="n{k}"></div>
    </div>
    <div class="pro"><div><b>a favor</b>{fav}</div><div><b>contra</b>{con}</div></div>
  </section>''' for k, (n, t, d, fav, con) in enumerate(OPCOES))

HTML = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cronos · o gráfico no tempo</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<div class="wrap">
  <h1>O que o gráfico faz quando você viaja</h1>
  <p class="sub">Um só comando embaixo controla os três ao mesmo tempo, para a comparação ser
    justa. Aperte play e olhe os três reagindo. Os números à direita são os mesmos em todos —
    o que muda é só o comportamento do desenho. Dado real: <b>92 dias</b> do trimestre.</p>

  <div class="cmd">
    <button class="play" id="play"><svg width="16" height="16" viewBox="0 0 24 24"
      fill="currentColor"><path d="M8 5v14l11-7z"/></svg></button>
    <div class="cmd-d"><b id="c-dia">qua 01/10</b><span id="c-pos">dia 1 de 92</span></div>
    <div class="lin" id="lin"><div class="base"></div><div class="feito" id="feito"></div>
      <div class="cab" id="cab"></div></div>
    <div class="vel"><button data-v="260">1×</button><button class="on" data-v="130">2×</button>
      <button data-v="45">6×</button></div>
  </div>
  {blocos}
</div>
<script>{JS}</script></body></html>"""

OUT.write_text(HTML, encoding='utf-8')
print(f'{OUT}  ({len(HTML) / 1024:.0f} kB)')

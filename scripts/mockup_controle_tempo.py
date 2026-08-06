# -*- coding: utf-8 -*-
"""Tres versoes do controle de tempo, funcionais e isoladas, para o Igor escolher.

Cada uma opera sobre o mesmo dado real (data/app/dias.json: 92 dias com chegada hora a
hora, previsao e faixa). Abaixo de cada controle vai um pedaco pequeno do painel para
dar para sentir a tela reagindo — sem montar a aplicacao inteira tres vezes.
"""
import json
from pathlib import Path

RAIZ = Path.cwd()
OUT = RAIZ / 'prototipos' / 'telas' / 'mockups' / 'controle-tempo.html'
OUT.parent.mkdir(parents=True, exist_ok=True)
DIAS = json.loads((RAIZ / 'data' / 'app' / 'dias.json').read_text(encoding='utf-8'))

CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
:root{--pg:#F6F7F9;--c:#FFF;--ink:#0C1017;--ln:rgba(12,16,23,.09);--ln2:rgba(12,16,23,.18);
 --tx:#4E586B;--tx2:#7B8598;--tx3:#A3ABBA;--hd:#0C1017;--ac:#2563EB;--acl:#EFF4FF;
 --no:#DC2626;--nol:#FEF2F2;--wn:#B45309;--wnl:#FFFAEC;--ok:#059669;--okl:#ECFDF5;
 --e:cubic-bezier(.19,1,.22,1);--e2:cubic-bezier(.34,1.56,.64,1);
 --s1:0 1px 2px rgba(12,16,23,.04),0 10px 26px -14px rgba(12,16,23,.14);
 --s2:0 2px 6px rgba(12,16,23,.06),0 28px 54px -20px rgba(12,16,23,.2)}
html{-webkit-font-smoothing:antialiased}
body{background:var(--pg);color:var(--hd);font-family:'Outfit',system-ui,sans-serif;
 font-size:15px;letter-spacing:-.011em;padding:34px 30px 90px}
.wrap{max-width:1180px;margin:0 auto}
h1{font-size:28px;font-weight:650;letter-spacing:-.035em}
.sub{font-size:14.5px;color:var(--tx);margin-top:8px;max-width:74ch;line-height:1.6}
.sub b{color:var(--hd);font-weight:650}
.op{margin-top:38px;background:var(--c);border:1px solid var(--ln);border-radius:24px;
 padding:24px 26px 26px;box-shadow:var(--s1)}
.op-h{display:flex;align-items:flex-start;gap:14px;margin-bottom:20px}
.op-n{font-size:12px;font-weight:800;letter-spacing:.1em;color:var(--ac);background:var(--acl);
 border:1px solid rgba(37,99,235,.2);border-radius:10px;padding:6px 12px;flex-shrink:0}
.op-h h2{font-size:19px;font-weight:650;letter-spacing:-.03em}
.op-h p{font-size:13px;color:var(--tx2);margin-top:3px;max-width:76ch;line-height:1.55}
.pro{font-size:12px;color:var(--tx2);margin-top:16px;padding-top:14px;border-top:1px solid var(--ln);
 display:flex;gap:26px;flex-wrap:wrap}
.pro b{color:var(--hd);font-weight:650;display:block;font-size:11px;letter-spacing:.06em;
 text-transform:uppercase;margin-bottom:3px}
.pro div{max-width:34ch;line-height:1.5}
.id{font-weight:600;letter-spacing:.05em;font-variant-numeric:tabular-nums}
/* ══ barra de topo simulada ══ */
.topo{display:flex;align-items:center;gap:14px;background:var(--pg);border:1px solid var(--ln);
 border-radius:16px;padding:11px 14px}
.marca{display:flex;align-items:center;gap:9px;flex-shrink:0}
.marca i{width:28px;height:28px;border-radius:9px;background:var(--ink);display:grid;
 place-items:center;color:#fff;font-style:normal;font-size:13px;font-weight:700}
.marca b{font-size:15px;font-weight:700;letter-spacing:-.035em}
.abas{display:flex;gap:2px;background:var(--c);border:1px solid var(--ln);border-radius:11px;
 padding:3px}
.abas span{font-size:12px;font-weight:500;color:var(--tx2);padding:6px 11px;border-radius:8px}
.abas span.on{background:var(--ink);color:#fff}
/* ══ 1 · compacto inline ══ */
.t1{margin-left:auto;display:flex;align-items:center;gap:12px}
.nav{display:flex;align-items:center;gap:3px;background:var(--c);border:1px solid var(--ln);
 border-radius:11px;padding:3px}
.nav button{background:0;border:0;width:28px;height:28px;border-radius:8px;cursor:pointer;
 color:var(--tx2);display:grid;place-items:center;transition:all .25s var(--e);font:inherit}
.nav button:hover{background:var(--pg);color:var(--hd)}
.nav b{font-size:12.5px;font-weight:650;padding:0 8px;min-width:96px;text-align:center;
 font-variant-numeric:tabular-nums}
.hr1{display:flex;align-items:center;gap:9px;background:var(--c);border:1px solid var(--ln);
 border-radius:11px;padding:6px 12px}
.hr1 input{width:120px}
.hr1 b{font-size:12.5px;font-weight:650;min-width:34px;font-variant-numeric:tabular-nums}
.play{background:var(--ink);border:0;color:#fff;width:32px;height:32px;border-radius:10px;
 cursor:pointer;display:grid;place-items:center;transition:all .25s var(--e)}
.play:hover{transform:translateY(-1px);box-shadow:var(--s1)}
/* ══ 2 · pilula que expande ══ */
.t2{margin-left:auto;position:relative}
.cap{display:flex;align-items:center;gap:9px;background:var(--c);border:1px solid var(--ln);
 border-radius:999px;padding:7px 14px;cursor:pointer;font:inherit;transition:all .3s var(--e)}
.cap:hover{border-color:var(--ln2);box-shadow:var(--s1)}
.cap i{width:7px;height:7px;border-radius:50%;background:var(--ac);font-style:normal;
 animation:pu 2.4s ease-in-out infinite}
@keyframes pu{50%{opacity:.35}}
.cap b{font-size:12.5px;font-weight:650;font-variant-numeric:tabular-nums}
.cap span{font-size:11px;color:var(--tx3)}
.pnl{position:absolute;top:calc(100% + 10px);right:0;width:660px;background:var(--c);
 border:1px solid var(--ln);border-radius:20px;padding:18px 20px;box-shadow:var(--s2);z-index:9;
 animation:ent .35s var(--e) both}
@keyframes ent{from{opacity:0;transform:translateY(-8px)}}
.pnl[hidden]{display:none}
.pnl-h{display:flex;align-items:center;gap:10px;margin-bottom:12px}
.pnl-h b{font-size:10px;font-weight:700;letter-spacing:.13em;text-transform:uppercase;
 color:var(--tx3)}
.pnl-h span{margin-left:auto;font-size:11.5px;color:var(--tx2)}
/* tira do trimestre: uma barra por dia, cor pelo acerto da faixa */
.tira{display:flex;gap:2px;align-items:flex-end;height:52px;margin-bottom:4px}
.tira i{flex:1;border-radius:2px 2px 0 0;cursor:pointer;transition:opacity .2s;
 min-height:4px;opacity:.55}
.tira i:hover{opacity:1}
.tira i.on{opacity:1;outline:2px solid var(--ink);outline-offset:1px}
.tira i.dentro{background:var(--ac)}
.tira i.fora{background:var(--no)}
.tira-x{display:flex;justify-content:space-between;font-size:9.5px;color:var(--tx3);
 letter-spacing:.05em;text-transform:uppercase}
/* ══ 3 · player fixo embaixo ══ */
.plr{background:var(--ink);border-radius:18px;padding:14px 18px;color:#E8ECF3;
 display:flex;align-items:center;gap:16px;box-shadow:var(--s2)}
.plr .play{background:var(--ac)}
.plr-i{flex-shrink:0;min-width:132px}
.plr-i b{font-size:15px;font-weight:650;display:block;font-variant-numeric:tabular-nums}
.plr-i span{font-size:11px;color:#8D97A8}
.plr-t{flex:1}
.lin{position:relative;height:34px;cursor:pointer}
.lin .base{position:absolute;inset:auto 0 12px 0;height:3px;border-radius:2px;
 background:rgba(255,255,255,.14)}
.lin .feito{position:absolute;inset:auto auto 12px 0;height:3px;border-radius:2px;
 background:var(--ac)}
.lin .cab{position:absolute;bottom:7px;width:13px;height:13px;border-radius:50%;background:#fff;
 border:3px solid var(--ac);transform:translateX(-50%);transition:left .12s linear;
 box-shadow:0 2px 8px rgba(0,0,0,.5)}
.lin .mes{position:absolute;bottom:0;font-size:9px;color:#5F697C;transform:translateX(-50%);
 letter-spacing:.06em;text-transform:uppercase}
.lin .marca{position:absolute;bottom:15px;width:2px;height:7px;background:rgba(240,72,62,.55);
 transform:translateX(-50%)}
.plr-v{flex-shrink:0;text-align:right;min-width:150px}
.plr-v b{font-size:22px;font-weight:650;letter-spacing:-.04em;display:block;line-height:1;
 font-variant-numeric:tabular-nums}
.plr-v span{font-size:10.5px;color:#8D97A8}
.vel{display:flex;gap:2px;background:rgba(255,255,255,.07);border-radius:9px;padding:3px;
 flex-shrink:0}
.vel button{background:0;border:0;font:inherit;font-size:10.5px;font-weight:650;color:#8D97A8;
 padding:5px 8px;border-radius:6px;cursor:pointer}
.vel button.on{background:rgba(255,255,255,.13);color:#fff}
/* ══ painel que reage, comum as tres ══ */
.reage{display:grid;grid-template-columns:1.5fr 1fr;gap:14px;margin-top:16px}
.cd{background:var(--pg);border:1px solid var(--ln);border-radius:16px;padding:16px 18px}
.cd h3{font-size:11px;font-weight:700;letter-spacing:.11em;text-transform:uppercase;
 color:var(--tx3);margin-bottom:10px}
.gr svg{width:100%;height:auto;display:block;overflow:visible}
.g-grade{stroke:var(--ln);stroke-width:1}
.g-y{fill:var(--tx3);font-size:9.5px;font-family:'Outfit',sans-serif}
.g-x{fill:var(--tx3);font-size:9.5px;font-family:'Outfit',sans-serif}
.g-bd{fill:var(--ac);opacity:.11}
.g-esp{fill:none;stroke:var(--ac);stroke-width:1.8;stroke-dasharray:5 4;opacity:.6}
.g-real{fill:none;stroke:var(--ink);stroke-width:2.6;stroke-linecap:round}
.g-ag{stroke:var(--ln2);stroke-width:1;stroke-dasharray:2 3}
.g-pt{fill:var(--ink)}
.leg{display:flex;gap:14px;margin-top:8px;flex-wrap:wrap}
.leg span{display:inline-flex;align-items:center;gap:5px;font-size:10.5px;color:var(--tx2)}
.leg i{width:13px;height:3px;border-radius:2px}
.l-r{background:var(--ink)}.l-e{background:var(--ac);opacity:.6}
.l-b{background:var(--ac);opacity:.2;height:9px;border-radius:3px}
.kv{display:flex;flex-direction:column;gap:9px}
.kv div{display:flex;align-items:baseline;gap:9px}
.kv em{font-size:11.5px;color:var(--tx2);font-style:normal;flex:1}
.kv b{font-size:19px;font-weight:650;letter-spacing:-.035em;font-variant-numeric:tabular-nums}
.ver{display:inline-block;font-size:10.5px;font-weight:700;letter-spacing:.07em;
 text-transform:uppercase;padding:4px 10px;border-radius:8px;margin-top:4px}
.ver.ok{background:var(--okl);color:var(--ok)}
.ver.no{background:var(--nol);color:var(--no)}
.ver.wn{background:var(--wnl);color:var(--wn)}
input[type=range]{-webkit-appearance:none;appearance:none;background:0;cursor:pointer;height:18px}
input[type=range]::-webkit-slider-runnable-track{height:4px;border-radius:2px;background:var(--ln2)}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:15px;height:15px;
 border-radius:50%;background:var(--ink);margin-top:-5.5px;border:2px solid var(--c);
 box-shadow:var(--s1)}
@media (max-width:900px){.reage{grid-template-columns:1fr}.pnl{width:min(92vw,660px)}}
"""

JS = r"""
const D = __DIAS__, TOTAL = D.dias.length;
const svg = 'http://www.w3.org/2000/svg';
const nb = (v, c = 0) => v.toFixed(c).replace('.', ',');
// curva de chegada media do trimestre: usada para distribuir a previsao pelas horas
const SOMA = new Array(24).fill(0);
D.dias.forEach(d => d.hora.forEach((v, i) => SOMA[i] += v));
const TT = SOMA.reduce((a, b) => a + b, 0);
const ACUM = SOMA.reduce((a, v, i) => (a.push((a[i - 1] || 0) + v / TT), a), []);

const est = { 0: { d: 0, h: 7 }, 1: { d: 0, h: 7 }, 2: { d: 0, h: 7 } };

function curva(v, w, h, mx) {
  const px = i => 30 + i / 23 * (w - 42), py = y => h - 22 - y / mx * (h - 36);
  return { px, py, d: pts => 'M' + pts.map(p => `${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(' L') };
}

function grafico(el, dia, hora) {
  const w = 520, h = 170;
  const esperado = ACUM.map(a => dia.prev * a);
  const realAc = []; let t = 0;
  dia.hora.forEach((v, i) => { t += v; realAc.push(t); });
  const mx = Math.max(dia.alto, ...esperado, ...realAc) * 1.08;
  const { px, py, d } = curva(0, w, h, mx);
  const pe = esperado.map((v, i) => [px(i), py(v)]);
  const pr = realAc.slice(0, hora + 1).map((v, i) => [px(i), py(v)]);
  const fr = ACUM;
  const alto = fr.map((f, i) => [px(i), py(dia.alto * f)]);
  const baixo = fr.map((f, i) => [px(i), py(dia.baixo * f)]).reverse();
  const marcas = [0, Math.round(mx / 2 / 10) * 10, Math.round(mx * .85 / 10) * 10];
  el.innerHTML = `<svg viewBox="0 0 ${w} ${h}">
    ${marcas.map(v => `<line class="g-grade" x1="26" y1="${py(v).toFixed(1)}" x2="${w}" y2="${py(v).toFixed(1)}"/>
      <text class="g-y" x="20" y="${(py(v) + 3.5).toFixed(1)}" text-anchor="end">${v}</text>`).join('')}
    <path class="g-bd" d="${d(alto)} L${d(baixo).slice(1)} Z"/>
    <path class="g-esp" d="${d(pe)}"/>
    ${pr.length > 1 ? `<path class="g-real" d="${d(pr)}"/>` : ''}
    <line class="g-ag" x1="${px(hora).toFixed(1)}" y1="6" x2="${px(hora).toFixed(1)}" y2="${h - 20}"/>
    <circle class="g-pt" cx="${px(hora).toFixed(1)}" cy="${py(realAc[hora]).toFixed(1)}" r="4.5"/>
    ${[0, 6, 12, 18, 23].map(k => `<text class="g-x" x="${px(k).toFixed(1)}" y="${h - 6}" text-anchor="middle">${String(k).padStart(2, '0')}h</text>`).join('')}
  </svg>`;
  return { real: realAc[hora], esp: esperado[hora], fim: realAc[23] };
}

function pinta(i) {
  const e = est[i], dia = D.dias[e.d];
  const r = grafico(document.getElementById(`g${i}`), dia, e.h);
  const dentro = dia.real >= dia.baixo && dia.real <= dia.alto;
  const dif = r.real - r.esp;
  const ritmo = ACUM[e.h] > .12 ? r.real / ACUM[e.h] : null;
  const v = ritmo === null ? ['wn', 'cedo para dizer']
    : (ritmo < dia.baixo ? ['no', 'abaixo do previsto']
      : ritmo > dia.alto ? ['no', 'acima do previsto'] : ['ok', 'no ritmo']);
  document.getElementById(`k${i}`).innerHTML = `
    <div><em>já entraram</em><b>${r.real}</b></div>
    <div><em>esperado a esta altura</em><b>${nb(r.esp, 1)}</b></div>
    <div><em>faixa do dia</em><b>${nb(dia.baixo)} a ${nb(dia.alto)}</b></div>
    <div><em>fechou o dia com</em><b>${dia.real}</b></div>
    <span class="ver ${v[0]}">${v[1]}</span>
    ${ritmo !== null ? `<div style="margin-top:2px"><em>no ritmo de agora fecharia em</em><b>${nb(ritmo)}</b></div>` : ''}
    <div style="margin-top:6px"><em>a faixa ${dentro ? 'conteve' : 'não conteve'} o real</em>
      <b style="color:${dentro ? 'var(--ok)' : 'var(--no)'}">${dentro ? '✓' : '✕'}</b></div>`;
  document.querySelectorAll(`[data-rot="${i}"]`).forEach(x =>
    x.textContent = `${dia.rot} ${dia.dm}`);
  document.querySelectorAll(`[data-hora="${i}"]`).forEach(x =>
    x.textContent = String(e.h).padStart(2, '0') + 'h');
  const c = document.getElementById(`cap${i}`);
  if (c) c.querySelector('b').textContent = `${dia.dm} · ${String(e.h).padStart(2, '0')}h`;
}

function anda(i, dd = 0, dh = 0, absd = null, absh = null) {
  const e = est[i];
  if (absd !== null) e.d = absd; else e.d = Math.min(TOTAL - 1, Math.max(0, e.d + dd));
  if (absh !== null) e.h = absh; else e.h = Math.min(23, Math.max(0, e.h + dh));
  pinta(i);
}

/* ── 1 · compacto ── */
document.getElementById('p1a').onclick = () => anda(0, -1);
document.getElementById('p1p').onclick = () => anda(0, 1);
document.getElementById('s1').oninput = ev => anda(0, 0, 0, null, +ev.target.value);
let t1 = null;
document.getElementById('r1').onclick = ev => {
  if (t1) { clearInterval(t1); t1 = null; ev.currentTarget.textContent = '▶'; return; }
  ev.currentTarget.textContent = '❚❚';
  t1 = setInterval(() => {
    const e = est[0];
    if (e.h >= 23) { clearInterval(t1); t1 = null; document.getElementById('r1').textContent = '▶'; return; }
    document.getElementById('s1').value = e.h + 1; anda(0, 0, 0, null, e.h + 1);
  }, 220);
};

/* ── 2 · pílula que expande ── */
const pnl = document.getElementById('pnl');
document.getElementById('cap1').onclick = () => { pnl.hidden = !pnl.hidden; };
const tira = document.getElementById('tira');
tira.innerHTML = D.dias.map((d, i) => {
  const dentro = d.real >= d.baixo && d.real <= d.alto;
  const alt = 12 + 40 * d.real / 140;
  return `<i class="${dentro ? 'dentro' : 'fora'}${i === 0 ? ' on' : ''}" data-i="${i}"
    style="height:${alt.toFixed(0)}px" title="${d.rot} ${d.dm} · previsto ${nb(d.baixo)} a ${nb(d.alto)} · real ${d.real}"></i>`;
}).join('');
tira.onclick = ev => {
  const b = ev.target.closest('i'); if (!b) return;
  tira.querySelectorAll('i').forEach(x => x.classList.remove('on'));
  b.classList.add('on'); anda(1, 0, 0, +b.dataset.i);
};
document.getElementById('s2').oninput = ev => anda(1, 0, 0, null, +ev.target.value);

/* ── 3 · player ── */
const lin = document.getElementById('lin'), cab = document.getElementById('cab'),
      feito = document.getElementById('feito');
const passos = TOTAL * 24;
function posiciona() {
  const e = est[2], p = (e.d * 24 + e.h) / (passos - 1) * 100;
  cab.style.left = p + '%'; feito.style.width = p + '%';
}
lin.onclick = ev => {
  const b = lin.getBoundingClientRect();
  const p = Math.min(1, Math.max(0, (ev.clientX - b.left) / b.width));
  const passo = Math.round(p * (passos - 1));
  est[2].d = Math.floor(passo / 24); est[2].h = passo % 24;
  posiciona(); pinta(2);
};
let t3 = null, vel = 60;
document.getElementById('r3').onclick = ev => {
  if (t3) { clearInterval(t3); t3 = null; ev.currentTarget.textContent = '▶'; return; }
  ev.currentTarget.textContent = '❚❚';
  t3 = setInterval(() => {
    const e = est[2];
    if (e.h >= 23) { if (e.d >= TOTAL - 1) { clearInterval(t3); t3 = null; document.getElementById('r3').textContent = '▶'; return; } e.d++; e.h = 0; }
    else e.h++;
    posiciona(); pinta(2);
  }, vel);
};
document.querySelectorAll('.vel button').forEach(b => b.onclick = () => {
  document.querySelectorAll('.vel button').forEach(x => x.classList.remove('on'));
  b.classList.add('on'); vel = +b.dataset.v;
  if (t3) { clearInterval(t3); t3 = setInterval(() => document.getElementById('r3').click(), 1); document.getElementById('r3').click(); document.getElementById('r3').click(); }
});
// marca os meses e os dias em que a faixa falhou
const MES = {};
D.dias.forEach((d, i) => { const m = d.dia.slice(5, 7); if (!(m in MES)) MES[m] = i; });
lin.insertAdjacentHTML('beforeend',
  Object.entries(MES).map(([m, i]) =>
    `<span class="mes" style="left:${(i * 24 / (passos - 1) * 100).toFixed(2)}%">${
      ({ '10': 'out', '11': 'nov', '12': 'dez' })[m]}</span>`).join('')
  + D.dias.map((d, i) => (d.real >= d.baixo && d.real <= d.alto) ? '' :
      `<span class="marca" style="left:${(i * 24 / (passos - 1) * 100).toFixed(2)}%"></span>`).join(''));

[0, 1, 2].forEach(pinta);
posiciona();
""".replace('__DIAS__', json.dumps(DIAS, ensure_ascii=False, separators=(',', ':')))

BLOCO_REAGE = """
    <div class="reage">
      <div class="cd"><h3>Previsto contra realizado · P3</h3>
        <div class="gr" id="g{i}"></div>
        <div class="leg"><span><i class="l-r"></i>já entrou</span>
          <span><i class="l-e"></i>esperado pela previsão</span>
          <span><i class="l-b"></i>faixa de 80%</span></div>
      </div>
      <div class="cd"><h3>Como está o dia</h3><div class="kv" id="k{i}"></div></div>
    </div>"""

HTML = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cronos · três controles de tempo</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<div class="wrap">
  <h1>Três jeitos de navegar no tempo</h1>
  <p class="sub">Todos operam sobre o dado real: <b>92 dias</b> do trimestre, com a chegada
    hora a hora de cada um e a previsão que o Prophet fez para aquele dia. Mexa nos três.
    O gráfico e os números embaixo de cada controle reagem de verdade — é um pedaço pequeno
    do painel, só para dar para sentir.</p>

  <section class="op">
    <div class="op-h"><span class="op-n">01</span>
      <div><h2>Compacto, tudo à vista</h2>
        <p>Setas para o dia, régua para a hora e um botão de rodar, tudo em linha no topo.
          Nada esconde nada e o usuário entende em dois segundos.</p></div></div>
    <div class="topo">
      <div class="marca"><i>C</i><b>Cronos</b></div>
      <div class="abas"><span class="on">Hoje</span><span>Fila</span><span>Saúde</span></div>
      <div class="t1">
        <div class="nav"><button id="p1a">◀</button><b data-rot="0">qua 01/10</b>
          <button id="p1p">▶</button></div>
        <div class="hr1"><input type="range" id="s1" min="0" max="23" value="7">
          <b data-hora="0">07h</b></div>
        <button class="play" id="r1">▶</button>
      </div>
    </div>
    {BLOCO_REAGE.format(i=0)}
    <div class="pro">
      <div><b>a favor</b>Direto, sem clique extra. Quem chega já vê que dá para mexer.</div>
      <div><b>contra</b>Ocupa bastante espaço do topo e não mostra o trimestre inteiro.</div>
    </div>
  </section>

  <section class="op">
    <div class="op-h"><span class="op-n">02</span>
      <div><h2>Pílula que abre o trimestre</h2>
        <p>No topo fica só uma cápsula pequena. Clicando, abre um painel com os 92 dias em
          barras — azul onde a faixa acertou, vermelho onde errou. Dá para pular para
          qualquer dia e ver o modelo acertando e errando de uma vez.</p></div></div>
    <div class="topo">
      <div class="marca"><i>C</i><b>Cronos</b></div>
      <div class="abas"><span class="on">Hoje</span><span>Fila</span><span>Saúde</span></div>
      <div class="t2">
        <button class="cap" id="cap1"><i></i><b>01/10 · 07h</b><span>▾</span></button>
        <div class="pnl" id="pnl" hidden>
          <div class="pnl-h"><b>o trimestre inteiro</b>
            <span>azul: a faixa conteve o real · vermelho: não conteve ·
              {DIAS['cobertura']}% de acerto</span></div>
          <div class="tira" id="tira"></div>
          <div class="tira-x"><span>01/10</span><span>15/11</span><span>31/12</span></div>
          <div class="hr1" style="margin-top:14px;justify-content:center">
            <span style="font-size:11.5px;color:var(--tx2)">hora do dia</span>
            <input type="range" id="s2" min="0" max="23" value="7" style="width:220px">
            <b data-hora="1">07h</b></div>
        </div>
      </div>
    </div>
    {BLOCO_REAGE.format(i=1)}
    <div class="pro">
      <div><b>a favor</b>Topo limpo e, quando abre, mostra o trimestre e a calibração do
        modelo de uma vez só.</div>
      <div><b>contra</b>Exige um clique para descobrir. Quem não clicar não sabe que existe.</div>
    </div>
  </section>

  <section class="op">
    <div class="op-h"><span class="op-n">03</span>
      <div><h2>Player do trimestre</h2>
        <p>Uma barra escura, como tocador de vídeo, com os 92 dias numa linha só. As marcas
          vermelhas embaixo são os dias em que o real saiu da faixa. Aperta play e o
          trimestre passa hora a hora.</p></div></div>
    <div class="topo">
      <div class="marca"><i>C</i><b>Cronos</b></div>
      <div class="abas"><span class="on">Hoje</span><span>Fila</span><span>Saúde</span></div>
      <span style="margin-left:auto;font-size:11.5px;color:var(--tx2)">o topo fica livre</span>
    </div>
    <div class="plr" style="margin-top:12px">
      <button class="play" id="r3">▶</button>
      <div class="plr-i"><b data-rot="2">qua 01/10</b><span><span data-hora="2">07h</span> ·
        trimestre</span></div>
      <div class="plr-t"><div class="lin" id="lin">
        <div class="base"></div><div class="feito" id="feito"></div>
        <div class="cab" id="cab"></div></div></div>
      <div class="vel"><button data-v="120">1x</button><button class="on" data-v="60">2x</button>
        <button data-v="20">6x</button></div>
    </div>
    {BLOCO_REAGE.format(i=2)}
    <div class="pro">
      <div><b>a favor</b>É o mais fora do padrão e o que melhor conta a história do trimestre
        numa demo ao vivo. O topo fica todo livre.</div>
      <div><b>contra</b>Ocupa uma faixa fixa da tela e mistura duas escalas de tempo
        (dia e hora) num controle só.</div>
    </div>
  </section>
</div>
<script>{JS}</script></body></html>"""

OUT.write_text(HTML, encoding='utf-8')
print(f'{OUT}  ({len(HTML) / 1024:.0f} kB)')
print(f'{len(DIAS["dias"])} dias · faixa acertou em {DIAS["cobertura"]}%')

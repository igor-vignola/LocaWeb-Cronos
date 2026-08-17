// Máquina do tempo: o dia por dentro, hora a hora, atravessando o trimestre.
//
// Nada é recalculado. Os 92 dias já vêm agregados com a chegada de cada hora, e a curva
// esperada é a distribuição histórica por hora aplicada ao total previsto daquele dia.
// Viajar no tempo é indexar dois vetores.
//
// Escopo próprio: cronos.js já declara q no escopo global, e const redeclarado derruba
// este arquivo inteiro com SyntaxError antes da primeira linha rodar.
'use strict';
(() => {

const q = (id) => document.getElementById(id);
const nb = (v, c = 0) => Number(v).toFixed(c).replace('.', ',');
const N = DIAS.length, PASSOS = N * 24;
let d = 0, h = 0, tocando = null, vel = 70;

// curva de chegada média do trimestre: distribui a previsão do dia pelas 24 horas
const SOMA = new Array(24).fill(0);
DIAS.forEach((x) => x.hora.forEach((v, k) => { SOMA[k] += v; }));
const TT = SOMA.reduce((a, b) => a + b, 0) || 1;
const ACUM = [];
SOMA.reduce((a, v, k) => (ACUM[k] = a + v / TT), 0);

const lin = q('lin'), cab = q('cab'), feito = q('feito');
const campo = document.querySelector('.campo');
const dia = q('modo-dia'), tempo = q('modo-tempo'), abre = q('abre-modo');

lin.insertAdjacentHTML('beforeend', DIAS.map((x, k) => x.dentro ? '' :
  `<span class="falha" style="left:${(k / (N - 1) * 100).toFixed(2)}%"></span>`).join('')
  + [['out', 0], ['nov', 31], ['dez', 61]].map(([m, k]) =>
    `<span class="mes-r" style="left:${(k / (N - 1) * 100).toFixed(2)}%">${m}</span>`).join(''));

/* ── o dia por dentro ───────────────────────────────────────────────────── */
const W = 620, H = 210;
const suave = (p) => p.length < 2 ? '' :
  `M${p[0][0].toFixed(1)} ${p[0][1].toFixed(1)}` + p.slice(1).map((pt, k) => {
    const a = p[k], m = (a[0] + pt[0]) / 2;
    return ` C${m.toFixed(1)} ${a[1].toFixed(1)} ${m.toFixed(1)} ${pt[1].toFixed(1)}` +
           ` ${pt[0].toFixed(1)} ${pt[1].toFixed(1)}`;
  }).join('');

function desenhaDia() {
  const x = DIAS[d];
  const esperado = ACUM.map((a) => x.prev * a);
  const real = []; let t = 0;
  x.hora.forEach((v) => { t += v; real.push(t); });
  const mx = (Math.max(x.alto, esperado[23], real[23]) * 1.1) || 1;
  const px = (k) => 34 + k / 23 * (W - 46);
  const py = (v) => H - 26 - v / mx * (H - 46);

  const pe = esperado.map((v, k) => [px(k), py(v)]);
  const pr = real.slice(0, h + 1).map((v, k) => [px(k), py(v)]);
  const alto = ACUM.map((a, k) => [px(k), py(x.alto * a)]);
  const baixo = ACUM.map((a, k) => [px(k), py(x.baixo * a)]).reverse();
  const marcas = [0, Math.round(mx / 2 / 10) * 10, Math.round(mx * .85 / 10) * 10];

  q('dia-g').innerHTML = `<svg viewBox="0 0 ${W} ${H}">
    ${marcas.map((v) => `<line class="g-grade" x1="30" y1="${py(v).toFixed(1)}" x2="${W}" y2="${py(v).toFixed(1)}"/>
      <text class="g-y" x="24" y="${(py(v) + 3.5).toFixed(1)}" text-anchor="end">${v}</text>`).join('')}
    <path class="g-bd" d="M${alto.concat(baixo).map((p) => `${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(' L')} Z"/>
    <path class="g-prev" d="${suave(pe)}"/>
    ${pr.length > 1 ? `<path class="g-real" d="${suave(pr)}"/>` : ''}
    <line class="g-ag" x1="${px(h).toFixed(1)}" y1="10" x2="${px(h).toFixed(1)}" y2="${H - 22}"/>
    <circle class="g-no" cx="${px(h).toFixed(1)}" cy="${py(real[h]).toFixed(1)}" r="5.5"/>
    ${[0, 6, 12, 18, 23].map((k) => `<text class="g-x" x="${px(k).toFixed(1)}" y="${H - 6}" text-anchor="middle">${String(k).padStart(2, '0')}h</text>`).join('')}
  </svg>`;
  return { real: real[h], esp: esperado[h] };
}

/* ── o herói acompanha o tempo ──────────────────────────────────────────────
   Só o que o dado sustenta se move. A faixa do P3, a manchete e a contagem de casos
   vêm de DIAS e mudam junto. A faixa do P2, a fila e a projeção do ano não estão
   agregadas por dia: ficam paradas, e a página avisa isso em vez de fingir. */
const DIA_POR_EXTENSO = { seg: 'segunda', ter: 'terça', qua: 'quarta', qui: 'quinta',
  sex: 'sexta', 'sáb': 'sábado', dom: 'domingo' };

function pintaHeroi() {
  const x = DIAS[d];
  const alvo = (id, txt) => { const e = q(id); if (e) e.textContent = txt; };

  alvo('hz-data', `${x.dm} · ${DIA_POR_EXTENSO[x.rot] || x.rot}`);
  alvo('hz-hora', `· ${String(h).padStart(2, '0')}h`);

  const h1 = q('hz-h1');
  if (h1) h1.innerHTML = x.acima10
    ? 'Dia de volume normal,<br><span class="mu">com risco concentrado.</span>'
    : 'Dia de volume normal,<br><span class="mu">sem caso crítico.</span>';

  const lead = q('hz-lead');
  if (lead) lead.innerHTML = x.acima10
    ? `<span class="cr">${x.acima10} caso${x.acima10 > 1 ? 's' : ''} acima de 10% de
       risco</span> entre os <b>${x.casos}</b> abertos no dia. O maior está em
       <b>${nb(x.maior, 1)}%</b>.`
    : `Nenhum dos <b>${x.casos}</b> incidentes abertos no dia passa de 10% de chance de
       estourar o prazo — o maior está em <b>${nb(x.maior, 1)}%</b>.`;

  const fx = q('hz-fx3');
  if (fx) fx.innerHTML = `${nb(x.baixo)} <u>a</u> ${nb(x.alto)}`;

  // o dia do corte é o presente; qualquer outro é viagem, e a página assume isso
  document.body.classList.toggle('viajando', d !== 0);
}

function pinta() {
  const x = DIAS[d], r = desenhaDia();
  pintaHeroi();

  q('m-dia').textContent = `${x.rot} ${x.dm}`;
  q('m-pos').textContent = `${String(h).padStart(2, '0')}h · dia ${d + 1} de ${N}`;

  const passo = (d * 24 + h) / (PASSOS - 1) * 100;
  cab.style.left = passo + '%';
  feito.style.width = passo + '%';
  // as três camadas do campo deslizam em fatores diferentes: é o paralaxe que o olho
  // lê como movimento, não o deslocamento em si
  campo?.style.setProperty('--viagem', (-(d * 24 + h) * 1.2) + 'px');

  q('k-real').textContent = r.real;
  q('k-esp').textContent = nb(r.esp, 1);
  q('k-faixa').textContent = `${nb(x.baixo)} a ${nb(x.alto)}`;
  q('k-fim').textContent = x.real;

  const frac = ACUM[h];
  const ritmo = frac > .12 ? r.real / frac : null;
  q('k-ritmo').textContent = ritmo === null ? 'cedo demais' : nb(ritmo);

  const v = q('k-ver');
  if (ritmo === null) { v.textContent = 'cedo para dizer'; v.className = 'ver wn'; }
  else if (ritmo < x.baixo) { v.textContent = 'abaixo do previsto'; v.className = 'ver no'; }
  else if (ritmo > x.alto) { v.textContent = 'acima do previsto'; v.className = 'ver no'; }
  else { v.textContent = 'no ritmo'; v.className = 'ver ok'; }

  const ok = q('k-ok');
  ok.textContent = x.dentro ? '✓' : '✕';
  ok.className = 'marca ' + (x.dentro ? 'sim' : 'nao');

  q('k-acum').textContent = nb(x.acum, 1) + '%';
  q('k-bar').style.width = x.acum + '%';
  q('k-bar').style.background =
    x.acum >= 80 ? 'var(--ok)' : x.acum >= 55 ? 'var(--wn)' : 'var(--no)';
  const dentroAte = DIAS.slice(0, d + 1).filter((y) => y.dentro).length;
  q('k-acum-t').textContent =
    `${dentroAte} de ${d + 1} ${d ? 'dias' : 'dia'} com o real dentro da faixa prevista.`;
}

/* ── um só relógio para a página inteira ────────────────────────────────────
   O controle do topo (cronos.js) e o player daqui movem o mesmo tempo. Cada um
   publica 'cronos:tempo' quando o movimento nasce nele e escuta quando nasce no
   outro. `deFora` corta a ida e volta. */
let deFora = false;

function vaiPasso(p) {
  p = Math.min(PASSOS - 1, Math.max(0, p));
  d = Math.floor(p / 24); h = p % 24;
  pinta();
  if (!deFora) {
    document.dispatchEvent(new CustomEvent('cronos:tempo', { detail: { dia: d, hora: h } }));
  }
}

document.addEventListener('cronos:tempo', (e) => {
  if (!deFora) {
    const t = e.detail || {};
    const novo = (t.dia === undefined ? d : t.dia) * 24 + (t.hora === undefined ? h : t.hora);
    if (novo === d * 24 + h) return;
    deFora = true;
    para();
    vaiPasso(novo);
    deFora = false;
  }
});

lin.addEventListener('click', (e) => {
  const b = lin.getBoundingClientRect();
  vaiPasso(Math.round((e.clientX - b.left) / b.width * (PASSOS - 1)));
});

const play = q('play');
const PLAY = '<svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>';
const PAUSE = '<svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><rect x="6.5" y="5" width="4" height="14" rx="1"/><rect x="13.5" y="5" width="4" height="14" rx="1"/></svg>';

function para() { clearInterval(tocando); tocando = null; play.innerHTML = PLAY; }
function anda() {
  const p = d * 24 + h;
  if (p >= PASSOS - 1) return para();
  vaiPasso(p + 1);
}
play.addEventListener('click', () => {
  if (tocando) return para();
  if (d * 24 + h >= PASSOS - 1) { d = 0; h = 0; }
  play.innerHTML = PAUSE;
  tocando = setInterval(anda, vel);
});
document.querySelectorAll('.vel button').forEach((b) => b.addEventListener('click', () => {
  document.querySelectorAll('.vel button').forEach((x) => x.classList.remove('on'));
  b.classList.add('on'); vel = +b.dataset.v;
  if (tocando) { clearInterval(tocando); tocando = setInterval(anda, vel); }
}));

addEventListener('keydown', (e) => {
  if (e.target.tagName === 'INPUT' || tempo.hidden) return;
  if (e.key === 'ArrowRight') { para(); vaiPasso(d * 24 + h + 1); }
  if (e.key === 'ArrowLeft') { para(); vaiPasso(d * 24 + h - 1); }
  if (e.key === ' ') { e.preventDefault(); play.click(); }
});

/* ── troca de modo, no lugar, sem navegar ───────────────────────────────── */
function modo(paraTempo) {
  const sai = paraTempo ? dia : tempo, entra = paraTempo ? tempo : dia;
  sai.classList.add('saindo');
  setTimeout(() => {
    sai.hidden = true; sai.classList.remove('saindo');
    entra.hidden = false; entra.classList.add('entrando');
    setTimeout(() => entra.classList.remove('entrando'), 480);
    if (paraTempo) pinta();
    scrollTo({ top: 0, behavior: 'smooth' });
  }, 220);
  abre.classList.toggle('ativo', paraTempo);
}
abre?.addEventListener('click', () => modo(true));
q('voltar')?.addEventListener('click', () => { para(); modo(false); });

pinta();

})();

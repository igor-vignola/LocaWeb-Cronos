// Máquina do tempo da aba Desempenho.
// Nada é recalculado: os 92 dias já vêm agregados do servidor. Viajar no tempo é
// indexar um vetor. O paralaxe do campo de linhas ao fundo é o que dá a sensação
// de deslocamento — as três camadas andam em velocidades diferentes.
'use strict';
(() => {

const q = (id) => document.getElementById(id);
const nb = (v, c = 0) => Number(v).toFixed(c).replace('.', ',');
const N = DIAS.length;
let i = 0, tocando = null, vel = 130;

const lin = q('lin'), cab = q('cab'), feito = q('feito'), campo = document.querySelector('.campo');

/* ── a linha do trimestre: uma marca por dia que saiu da faixa ────────────── */
lin.insertAdjacentHTML('beforeend', DIAS.map((d, k) => d.dentro ? '' :
  `<span class="falha" style="left:${(k / (N - 1) * 100).toFixed(2)}%"></span>`).join('')
  + [['out', 0], ['nov', 31], ['dez', 61]].map(([m, k]) =>
    `<span class="mes-r" style="left:${(k / (N - 1) * 100).toFixed(2)}%">${m}</span>`).join(''));

function pinta() {
  const d = DIAS[i], p = i / (N - 1) * 100;
  cab.style.left = p + '%';
  feito.style.width = p + '%';

  // o campo de linhas desliza: cada camada num fator diferente, e é a diferença
  // entre elas que o olho lê como movimento no tempo
  campo?.style.setProperty('--viagem', (-i * 26) + 'px');

  q('m-dia').textContent = `${d.rot} ${d.dm}`;
  q('m-pos').textContent = `dia ${i + 1} de ${N}`;

  q('m-acum').textContent = nb(d.acum, 1);
  q('m-bar').style.width = d.acum + '%';
  const dentroAte = DIAS.slice(0, i + 1).filter((x) => x.dentro).length;
  q('m-acum-t').textContent =
    `${dentroAte} de ${i + 1} ${i ? 'dias' : 'dia'} com o real dentro da faixa prevista.`;
  q('m-bar').style.background =
    d.acum >= 80 ? 'var(--ok)' : d.acum >= 55 ? 'var(--wn)' : 'var(--no)';

  q('m-prev').textContent = nb(d.prev);
  q('m-faixa').textContent = `faixa ${nb(d.baixo)} a ${nb(d.alto)}`;
  q('m-real').textContent = d.real;
  q('m-erro').textContent = `${d.erro > 0 ? '+' : '−'}${nb(Math.abs(d.erro), 1)} de diferença`;

  const v = q('m-ver');
  v.textContent = d.dentro ? 'dentro da faixa'
    : (d.real < d.baixo ? 'entrou menos que o previsto' : 'entrou mais que o previsto');
  v.className = 'ver ' + (d.dentro ? 'ok' : 'no');

  q('m-casos').textContent = d.casos;
  q('m-a10').textContent = d.acima10
    ? `${d.acima10} acima de 10% de risco` : 'nenhum acima de 10%';
  q('m-viol').textContent = d.violou;
  q('m-maior').textContent = d.maior ? `maior risco ${nb(d.maior, 1)}%` : 'fila vazia';

  document.querySelectorAll('.maq-c').forEach((c) => {
    c.classList.remove('pisca');
    void c.offsetWidth;               // reinicia a animação
    c.classList.add('pisca');
  });
}

function vai(k) { i = Math.min(N - 1, Math.max(0, k)); pinta(); }

lin.addEventListener('click', (e) => {
  const b = lin.getBoundingClientRect();
  vai(Math.round((e.clientX - b.left) / b.width * (N - 1)));
});

const play = q('play');
const PLAY = '<svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>';
const PAUSE = '<svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><rect x="6.5" y="5" width="4" height="14" rx="1"/><rect x="13.5" y="5" width="4" height="14" rx="1"/></svg>';

function para() { clearInterval(tocando); tocando = null; play.innerHTML = PLAY; }
play.addEventListener('click', () => {
  if (tocando) return para();
  if (i >= N - 1) i = 0;
  play.innerHTML = PAUSE;
  tocando = setInterval(() => { i >= N - 1 ? para() : vai(i + 1); }, vel);
});

document.querySelectorAll('.vel button').forEach((b) => b.addEventListener('click', () => {
  document.querySelectorAll('.vel button').forEach((x) => x.classList.remove('on'));
  b.classList.add('on');
  vel = +b.dataset.v;
  if (tocando) { clearInterval(tocando); tocando = setInterval(() => { i >= N - 1 ? para() : vai(i + 1); }, vel); }
}));

addEventListener('keydown', (e) => {
  if (e.target.tagName === 'INPUT') return;
  if (e.key === 'ArrowRight') { para(); vai(i + 1); }
  if (e.key === 'ArrowLeft') { para(); vai(i - 1); }
  if (e.key === ' ') { e.preventDefault(); play.click(); }
});

pinta();

/* ── troca de modo, no lugar, sem navegar ───────────────────────────────── */
const dia = q('modo-dia'), tempo = q('modo-tempo'), abre = q('abre-modo');
function modo(paraTempo) {
  const sai = paraTempo ? dia : tempo, entra = paraTempo ? tempo : dia;
  sai.classList.add('saindo');
  setTimeout(() => {
    sai.hidden = true; sai.classList.remove('saindo');
    entra.hidden = false; entra.classList.add('entrando');
    setTimeout(() => entra.classList.remove('entrando'), 480);
    if (paraTempo) entra.scrollIntoView({ behavior: 'smooth', block: 'start' });
    else scrollTo({ top: 0, behavior: 'smooth' });
  }, 220);
  abre.classList.toggle('ativo', paraTempo);
}
abre?.addEventListener('click', () => modo(true));
q('voltar')?.addEventListener('click', () => { para(); modo(false); });

})();

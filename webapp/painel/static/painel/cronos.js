// Cronos · comportamento do painel.
// Sem framework: a aplicacao serve HTML pronto e o script cuida de tres coisas —
// o resumo da manha, o modal de aprofundamento e a paleta de comando.
'use strict';

const q = (s) => document.getElementById(s);
const brov = q('brov'), ov = q('ov'), mc = q('mc'), pl = q('pl');

/* ── escalonamento das animacoes de entrada ─────────────────────────────── */
['.ch', '.mr', '.dc', '.it', '.h24', '.sm', '.rc2', '.rb i', '.tb tbody tr']
  .forEach((s) => document.querySelectorAll(s)
    .forEach((e, i) => e.style.setProperty('--i', Math.min(i, 30))));

/* ── morning brief: porta de entrada, uma vez por sessao ────────────────── */
const JA_VIU = 'cronos:brief:' + document.body.dataset.dia;
if (brov) {
  if (sessionStorage.getItem(JA_VIU)) brov.hidden = true;
  const fechaBrief = () => { brov.hidden = true; sessionStorage.setItem(JA_VIU, '1'); };
  q('brx')?.addEventListener('click', fechaBrief);
  q('brf-ok')?.addEventListener('click', fechaBrief);
  brov.addEventListener('click', (e) => { if (e.target === brov) fechaBrief(); });
  q('sino')?.addEventListener('click', () => { brov.hidden = false; });
}

/* ── modal: busca o fragmento no servidor ───────────────────────────────── */
const fechaModal = () => { ov.hidden = true; };
q('mx')?.addEventListener('click', fechaModal);
ov?.addEventListener('click', (e) => { if (e.target === ov) fechaModal(); });

let ultimoFoco = null;
async function abre(tipo, chave) {
  ultimoFoco = document.activeElement;
  mc.innerHTML = '<div class="md-carga">carregando…</div>';
  ov.hidden = false;
  ov.querySelector('.md').scrollTop = 0;
  try {
    const r = await fetch(`/detalhe/${tipo}/${encodeURIComponent(chave)}/`);
    if (!r.ok) throw new Error(r.status === 404 ? 'não encontrado' : 'falha ao carregar');
    mc.innerHTML = await r.text();
  } catch (e) {
    mc.innerHTML = `<div class="md-carga erro">Não foi possível abrir este detalhe
      (${e.message}). Feche e tente de novo.</div>`;
  }
}
document.addEventListener('click', (e) => {
  const b = e.target.closest('[data-mod]');
  if (b) abre(b.dataset.mod, b.dataset.k);
});

/* ── paleta de comando ──────────────────────────────────────────────────── */
const plq = q('plq'), plr = q('plr');
const ROT = { aba: 'seção', inc: 'caso', ativo: 'ativo', prod: 'produto' };
const DESTINO = { hoje: '/', fila: '/fila/', saude: '/saude/', causas: '/causas/',
                  previsao: '/previsao/' };
let itens = null, visiveis = [], sel = 0;

async function carregaIndice() {
  if (itens) return itens;
  try {
    itens = (await (await fetch('/busca.json')).json()).itens;
  } catch { itens = []; }
  return itens;
}
function pinta() {
  const t = plq.value.trim().toLowerCase();
  const base = itens || [];
  visiveis = (t ? base.filter((o) => (o.r + ' ' + o.s).toLowerCase().includes(t))
                : base.slice(0, 9)).slice(0, 40);
  sel = 0;
  plr.innerHTML = visiveis.length
    ? visiveis.map((o, i) => `<button class="pl-o${i === 0 ? ' on' : ''}" data-i="${i}">
        <span class="tp2">${ROT[o.t]}</span>
        <span><b class="id">${o.r}</b><span>${o.s}</span></span></button>`).join('')
    : `<div class="pl-vz">Nada encontrado. Tente o número do incidente, o código do ativo
        ou o nome do produto.</div>`;
}
function escolhe(o) {
  pl.hidden = true;
  if (o.t === 'aba') location.href = DESTINO[o.k];
  else abre({ inc: 'incidente', ativo: 'ativo', prod: 'produto' }[o.t], o.k);
}
async function abrePaleta() {
  pl.hidden = false; plq.value = '';
  plr.innerHTML = '<div class="pl-vz">carregando…</div>';
  await carregaIndice(); pinta(); plq.focus();
}
q('abrepl')?.addEventListener('click', abrePaleta);
plq?.addEventListener('input', pinta);
plr?.addEventListener('click', (e) => {
  const b = e.target.closest('.pl-o');
  if (b) escolhe(visiveis[+b.dataset.i]);
});

addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
    e.preventDefault(); abrePaleta(); return;
  }
  if (e.key === 'Escape') {
    pl.hidden = true; ov.hidden = true; if (brov) brov.hidden = true;
    ultimoFoco?.focus(); return;
  }
  if (pl.hidden || !visiveis.length) return;
  if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
    e.preventDefault();
    sel = (sel + (e.key === 'ArrowDown' ? 1 : -1) + visiveis.length) % visiveis.length;
    const opts = plr.querySelectorAll('.pl-o');
    opts.forEach((x, i) => x.classList.toggle('on', i === sel));
    opts[sel]?.scrollIntoView({ block: 'nearest' });
  }
  if (e.key === 'Enter' && visiveis[sel]) escolhe(visiveis[sel]);
});

/* ── luz que acompanha o cursor na borda do card ────────────────────────── */
addEventListener('pointermove', (e) => {
  const c = e.target.closest?.('.cd');
  if (!c) return;
  const b = c.getBoundingClientRect();
  c.style.setProperty('--mx', (e.clientX - b.left) + 'px');
  c.style.setProperty('--my', (e.clientY - b.top) + 'px');
}, { passive: true });

// Cronos · comportamento do painel.
// Sem framework: a aplicacao serve HTML pronto e o script cuida de tres coisas —
// o resumo da manha, o modal de aprofundamento e o controle de tempo do topo.
'use strict';

const q = (s) => document.getElementById(s);
const brov = q('brov'), ov = q('ov'), mc = q('mc');

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

const md = ov?.querySelector('.md');

/* Quem e focavel dentro do dialogo, agora. A lista e recalculada a cada Tab porque o conteudo
   chega por fetch depois da abertura, e os botoes do rodape do modal nem existem no primeiro
   quadro. `offsetParent` descarta o que esta escondido por um filtro. */
const focaveis = () => [...md.querySelectorAll(
  'button, a[href], input, select, textarea, [tabindex]:not([tabindex="-1"])')]
  .filter((x) => !x.disabled && x.offsetParent !== null);

let ultimoFoco = null;
async function abre(tipo, chave) {
  ultimoFoco = document.activeElement;
  mc.innerHTML = '<div class="md-carga">Carregando…</div>';
  ov.hidden = false;
  md.scrollTop = 0;
  /* O dialogo abria e o foco ficava para tras, no gatilho: quem usa teclado passava a tabular
     pela pagina ATRAS do modal, sem saber onde estava. `tabindex=-1` torna o proprio dialogo
     focavel sem entrar na ordem de Tab, e e nele que o foco pousa. */
  md.tabIndex = -1;
  md.focus();
  try {
    /* a busca da pagina viaja junto: um fragmento aberto a partir de uma tela parametrizada
       precisa do mesmo contexto dela. Hoje serve a escolha da regua do KPI (`?regua=a|b|c`),
       que so faz sentido se a folha renderizar a mesma variante que a pagina. */
    const r = await fetch(`/detalhe/${tipo}/${encodeURIComponent(chave)}/${location.search}`);
    if (!r.ok) throw new Error(r.status === 404 ? 'não encontrado' : 'falha ao carregar');
    mc.innerHTML = await r.text();
  } catch (e) {
    mc.innerHTML = `<div class="md-carga erro">Não foi possível abrir este detalhe
      (${e.message}). Feche e tente de novo.</div>`;
  }
}

/* O ciclo do Tab. Sem isto o `aria-modal` mente: o leitor de tela anuncia um dialogo e o
   teclado sai dele na primeira tecla. */
ov?.addEventListener('keydown', (e) => {
  if (e.key !== 'Tab') return;
  const alvos = focaveis();
  if (!alvos.length) { e.preventDefault(); return; }
  const primeiro = alvos[0], ultimo = alvos[alvos.length - 1];
  const foco = document.activeElement;
  if (e.shiftKey && (foco === primeiro || foco === md)) {
    e.preventDefault(); ultimo.focus();
  } else if (!e.shiftKey && (foco === ultimo || foco === md)) {
    e.preventDefault(); primeiro.focus();
  }
});
document.addEventListener('click', (e) => {
  const b = e.target.closest('[data-mod]');
  if (b) abre(b.dataset.mod, b.dataset.k);
});

/* O mesmo alvo pelo teclado. `tr` e `div` com data-mod não disparam clique no Enter — só
   `button` e `a` fazem isso — então a ação principal de algumas abas, abrir o aprofundamento,
   só existia no ponteiro. O `[tabindex]` no seletor evita capturar tecla dentro de elemento
   que já é botão e já responde sozinho. */
document.addEventListener('keydown', (e) => {
  if (e.key !== 'Enter' && e.key !== ' ') return;
  const b = e.target.closest && e.target.closest('[data-mod][tabindex]');
  if (b) { e.preventDefault(); abre(b.dataset.mod, b.dataset.k); }
});

addEventListener('keydown', (e) => {
  if (e.key !== 'Escape') return;
  ov.hidden = true;
  if (brov) brov.hidden = true;
  ultimoFoco?.focus();
});

/* ── controle de tempo do topo ──────────────────────────────────────────── */
// Ocupa o lugar que era da busca. Ele nao conhece a tela: a cada mudanca publica
// o evento 'cronos:tempo' no document, e escuta o mesmo evento para acompanhar
// quando o tempo for movido em outro lugar (o player do modo tempo). A trava
// `ecoando` corta o laco de ida e volta.
//
// DIAS e uma constante publicada pelo Panorama. Nas outras abas ela nem existe: o acesso vai
// para o catch e o controle simplesmente nao aparece.
const tc = q('tc');
const listaDias = (() => { try { return DIAS; } catch { return null; } })();

if (tc && Array.isArray(listaDias) && listaDias.length) {
  const GUARDA = 'cronos:tempo';
  const ultimoDia = listaDias.length - 1;
  const btAnterior = q('tc-ant'), btSeguinte = q('tc-pro');
  // a regua de hora saiu do topo: no dia a dia ninguem escolhe hora, e ela competia com
  // o unico controle que importa ali, que e trocar o dia. A hora continua no estado
  // porque o evento 'cronos:tempo' a carrega — quem move hora e o player da Previsao.
  const rotuloDia = q('tc-dia');
  let dia = 0, hora = 0, ecoando = false;

  const dentro = (v, teto) => Math.min(teto, Math.max(0, Math.round(Number(v) || 0)));

  // so desenha o controle; nao publica nem guarda
  function desenha() {
    const x = listaDias[dia];
    rotuloDia.textContent = `${x.rot} ${x.dm}`;
    btAnterior.disabled = dia === 0;
    btSeguinte.disabled = dia === ultimoDia;
  }

  function guarda() {
    try { sessionStorage.setItem(GUARDA, dia + ':' + hora); } catch { /* sessao cheia */ }
  }

  function publica() {
    ecoando = true;
    document.dispatchEvent(new CustomEvent('cronos:tempo', { detail: { dia, hora } }));
    ecoando = false;
  }

  // mudanca nascida aqui: desenha, guarda e avisa o resto da pagina
  function move(novoDia, novaHora) {
    dia = dentro(novoDia, ultimoDia);
    hora = dentro(novaHora, 23);
    desenha(); guarda(); publica();
  }

  btAnterior.addEventListener('click', () => move(dia - 1, hora));
  btSeguinte.addEventListener('click', () => move(dia + 1, hora));

  // mudanca vinda de fora: acompanha em silencio, sem reemitir
  document.addEventListener('cronos:tempo', (e) => {
    if (ecoando) return;
    const t = e.detail || {};
    if (t.dia !== undefined) dia = dentro(t.dia, ultimoDia);
    if (t.hora !== undefined) hora = dentro(t.hora, 23);
    desenha(); guarda();
  });

  // retoma de onde parou ao trocar de aba
  const salvo = (sessionStorage.getItem(GUARDA) || '').split(':');
  const retomando = salvo.length === 2;
  if (retomando) { dia = dentro(salvo[0], ultimoDia); hora = dentro(salvo[1], 23); }
  desenha();
  tc.hidden = false;
  // avisar agora seria cedo demais: os outros scripts ainda nao registraram os
  // ouvintes deles. DOMContentLoaded e o primeiro momento em que todos ja estao.
  if (retomando) document.addEventListener('DOMContentLoaded', publica);
}

/* A luz que acompanhava o cursor na borda do cartao saiu em 17/08.
   Ela escutava `pointermove` no documento inteiro e chamava `getBoundingClientRect()` a cada
   movimento do mouse — leitura de layout no caminho quente — para acender um efeito em `.cd`,
   classe que NENHUMA das seis abas usa: ela so sobrevive num arquivo `.bak` nao versionado.
   Era trabalho por quadro para um seletor morto. Se o efeito voltar, ele volta ligado ao
   seletor vivo (`.pn-v`) e com o CSS correspondente, que tambem nao existe mais. */

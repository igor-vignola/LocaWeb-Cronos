// Cronos · comportamento do painel.
// Sem framework: a aplicação serve HTML pronto e o script cuida de quatro coisas — o resumo do
// dia, o modal de aprofundamento, a leitura dos gráficos pelo cursor e os filtros das listas.
'use strict';

const q = (s) => document.getElementById(s);
const brov = q('brov'), ov = q('ov'), mc = q('mc');
const md = ov?.querySelector('.md');

/* ── resumo do dia: porta de entrada, uma vez por sessão ────────────────── */
const JA_VIU = 'cronos:brief:' + document.body.dataset.dia;
const sessao = {
  le: (k) => { try { return sessionStorage.getItem(k); } catch { return null; } },
  grava: (k, v) => { try { sessionStorage.setItem(k, v); } catch { /* sem armazenamento */ } },
};
if (brov) {
  if (sessao.le(JA_VIU)) brov.hidden = true;
  const fechaBrief = () => { brov.hidden = true; sessao.grava(JA_VIU, '1'); };
  q('brx')?.addEventListener('click', fechaBrief);
  q('brf-ok')?.addEventListener('click', fechaBrief);
  brov.addEventListener('click', (e) => { if (e.target === brov) fechaBrief(); });
  q('sino')?.addEventListener('click', () => { brov.hidden = false; });
}

/* ── modal: busca o fragmento no servidor ───────────────────────────────── */
// Os gatilhos visíveis do mesmo tipo formam a sequência das setas: na fila, o próximo caso é a
// próxima linha que o filtro deixou na tela.
let gatilhos = [], atual = -1, ultimoFoco = null;
const fechaModal = () => { ov.hidden = true; ultimoFoco?.focus(); };
q('mx')?.addEventListener('click', fechaModal);
ov?.addEventListener('click', (e) => { if (e.target === ov) fechaModal(); });

const focaveis = () => [...md.querySelectorAll(
  'button, a[href], input, select, textarea, [tabindex]:not([tabindex="-1"])')]
  .filter((x) => !x.disabled && x.offsetParent !== null);

function setas() {
  q('mp').disabled = atual <= 0;
  q('mn').disabled = atual < 0 || atual >= gatilhos.length - 1;
}

async function abre(tipo, chave) {
  mc.innerHTML = '<div class="md-carga">Carregando…</div>';
  ov.hidden = false;
  md.scrollTop = 0;
  md.tabIndex = -1;
  md.focus();
  setas();
  try {
    // a busca da página viaja junto: um fragmento aberto a partir de uma tela parametrizada
    // precisa do mesmo contexto dela
    const r = await fetch(`/detalhe/${tipo}/${encodeURIComponent(chave)}/${location.search}`);
    if (!r.ok) throw new Error(r.status === 404 ? 'não encontrado' : 'falha ao carregar');
    mc.innerHTML = await r.text();
    // os links do fragmento são relativos ao endereço DELE, que não é o da página: no site
    // estático, "../../../fila/" só faz sentido a partir de detalhe/incidente/X/
    mc.querySelectorAll('a[href]').forEach((a) => {
      a.href = new URL(a.getAttribute('href'), r.url).href;
    });
  } catch (e) {
    mc.innerHTML = `<div class="md-carga">Não foi possível abrir este detalhe
      (${e.message}). Feche e tente de novo.</div>`;
  }
}

function abreDe(el) {
  ultimoFoco = el;
  const seletor = el.hasAttribute('data-linha') ? '[data-linha][data-mod]' : `[data-mod="${el.dataset.mod}"]`;
  gatilhos = [...document.querySelectorAll(seletor)]
    .filter((x) => x.offsetParent !== null && !x.closest('#ov'));
  atual = gatilhos.indexOf(el);
  abre(el.dataset.mod, el.dataset.k);
}

function anda(d) {
  const n = atual + d;
  if (n < 0 || n >= gatilhos.length) return;
  atual = n;
  ultimoFoco = gatilhos[n];
  abre(gatilhos[n].dataset.mod, gatilhos[n].dataset.k);
}
q('mp')?.addEventListener('click', () => anda(-1));
q('mn')?.addEventListener('click', () => anda(1));

ov?.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight') { anda(1); return; }
  if (e.key === 'ArrowLeft') { anda(-1); return; }
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
  if (b && !b.closest('#ov')) abreDe(b);
});
// `div` com data-mod não dispara clique no Enter, só `button` e `a` fazem isso
document.addEventListener('keydown', (e) => {
  if (e.key !== 'Enter' && e.key !== ' ') return;
  const b = e.target.closest && e.target.closest('[data-mod][tabindex]');
  if (b) { e.preventDefault(); abreDe(b); }
});

addEventListener('keydown', (e) => {
  if (e.key !== 'Escape') return;
  if (ov && !ov.hidden) fechaModal();
  if (brov && !brov.hidden) { brov.hidden = true; sessao.grava(JA_VIU, '1'); }
});

/* ── gráficos: leitura pelo cursor ──────────────────────────────────────── */
// Cada `.gx` traz os pontos em `data-pontos`: posição em % da largura e da altura, o registrado
// (null no que ainda não aconteceu), a previsão do modelo e a faixa de 80%. No gráfico do dia
// também vem quanto entrou dentro da hora. O balão monta as linhas que o ponto tiver.
document.querySelectorAll('.gx[data-pontos]').forEach((gx) => {
  const pts = JSON.parse(gx.dataset.pontos);
  const pt = gx.querySelector('.gx-pt'), tt = gx.querySelector('.gx-tt');
  const cl = gx.querySelector('.gx-cl');
  const vw = gx.querySelector('svg').viewBox.baseVal.width;
  const num = (v) => Number(v).toLocaleString('pt-BR', { maximumFractionDigits: 1 });
  const linha = (m, r, v, c = '') => `<span class="tt-l"><i class="${m}"></i><span>${r}</span><b class="${c}">${v}</b></span>`;
  const balao = (p) => {
    const hora = p.rot === undefined;
    const rot = hora ? String(p.h).padStart(2, '0') + 'h' : p.rot;
    // o selo do cabeçalho diz onde o registrado caiu contra a faixa; no futuro, que é previsão
    let selo = '<span class="sl ac">Previsão</span>', nota = '';
    if (p.real !== null && p.real !== undefined && p.esp !== undefined) {
      const d = p.real - p.esp;
      selo = p.real < p.bx ? '<span class="sl wn">Abaixo do intervalo</span>'
        : p.real > p.at ? '<span class="sl no">Acima do intervalo</span>'
        : '<span class="sl ok">Dentro do intervalo</span>';
      nota = Math.abs(d) < .05 ? 'Em linha com a previsão'
        : `${num(Math.abs(d))} ${d < 0 ? 'abaixo' : 'acima'} da previsão`;
    } else if (p.real !== null && p.real !== undefined) {
      selo = '<span class="sl">Registrado</span>';
    } else if (hora) {
      nota = 'Hora ainda não decorrida';
    }
    let h = `<span class="tt-h"><b>${rot}</b>${selo}</span>`;
    if (p.real !== null && p.real !== undefined) {
      h += linha('m-r', hora ? `Registrados até ${rot}` : 'Registrados', p.real);
      if (p.nah !== undefined && p.nah !== null) h += linha('m-h', 'Entraram nesta hora', p.nah > 0 ? `+${p.nah}` : '0', p.nah > 0 ? 'ok' : '');
    }
    if (p.esp !== undefined) {
      h += linha('m-p', 'Previsão do modelo', num(p.esp));
      h += linha('m-f', 'Faixa de 80%', `${num(p.bx)} a ${num(p.at)}`);
    }
    if (nota) h += `<span class="tt-v">${nota}</span>`;
    return h;
  };
  gx.addEventListener('mousemove', (e) => {
    const r = gx.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width * 100;
    let p = pts[0];
    for (const c of pts) if (Math.abs(c.x - x) < Math.abs(p.x - x)) p = c;
    pt.hidden = tt.hidden = false;
    pt.style.left = p.x + '%';
    pt.style.top = p.y + '%';
    tt.innerHTML = balao(p);
    // o balão não pode sair do cartão: perto das bordas ele encosta no lado de dentro
    const meia = tt.offsetWidth / 2 / r.width * 100;
    tt.style.left = Math.min(100 - meia, Math.max(meia, p.x)) + '%';
    tt.style.top = p.y + '%';
    tt.classList.toggle('bx', p.y < 45);
    if (cl) {
      const xv = p.x / 100 * vw;
      cl.setAttribute('x1', xv); cl.setAttribute('x2', xv); cl.setAttribute('opacity', '.18');
    }
  });
  gx.addEventListener('mouseleave', () => {
    pt.hidden = tt.hidden = true;
    cl?.setAttribute('opacity', '0');
  });
});

/* ── listas filtráveis (Fila e Saúde) ───────────────────────────────────── */
// Filtro no navegador, e não no servidor: a mesma tela funciona no Django e no site estático,
// onde não existe quem leia a busca da URL. As linhas trazem os atributos que filtram:
// data-pri, data-grupo e data-busca. A busca da URL (`?q=Team10`) preenche o campo na chegada,
// que é como o modal do incidente manda para a fila de uma equipe.
document.querySelectorAll('[data-lista]').forEach((raiz) => {
  const linhas = [...raiz.querySelectorAll('[data-linha]')];
  const campo = raiz.querySelector('[data-busca-campo]');
  const vazio = raiz.querySelector('[data-vazio]');
  const mais = raiz.querySelector('[data-mais]');
  const contas = raiz.querySelectorAll('[data-conta]');
  const limite = Number(raiz.dataset.limite || 0);
  const estado = { pri: '', grupo: '', texto: '', tudo: !limite };

  const desenha = () => {
    const t = estado.texto.trim().toLowerCase();
    const passaPri = (l) => !estado.pri || l.dataset.pri === estado.pri;
    const passaTexto = (l) => !t || (l.dataset.busca || '').includes(t);
    let n = 0;
    linhas.forEach((l) => {
      const ok = passaPri(l) && passaTexto(l) && (!estado.grupo || l.dataset.grupo === estado.grupo);
      const mostra = ok && (estado.tudo || n < limite);
      if (ok) n += 1;
      l.hidden = !mostra;
    });
    // a contagem de cada grupo respeita a prioridade e a busca, para o chip nunca somar linhas
    // que a tabela não mostra
    contas.forEach((c) => {
      c.textContent = linhas.filter((l) => passaPri(l) && passaTexto(l)
        && l.dataset.grupo === c.dataset.conta).length;
    });
    if (vazio) vazio.hidden = n > 0;
    if (mais) {
      const resto = n - limite;
      mais.hidden = estado.tudo || resto <= 0;
      mais.textContent = `Ver mais ${resto} ${raiz.dataset.unidade || 'itens'}`;
    }
  };

  raiz.querySelectorAll('[data-pri-bt]').forEach((b) => b.addEventListener('click', () => {
    estado.pri = b.dataset.priBt;
    raiz.querySelectorAll('[data-pri-bt]').forEach((x) => x.classList.toggle('on', x === b));
    desenha();
  }));
  raiz.querySelectorAll('[data-grupo-bt]').forEach((b) => b.addEventListener('click', () => {
    estado.grupo = estado.grupo === b.dataset.grupoBt ? '' : b.dataset.grupoBt;
    raiz.querySelectorAll('[data-grupo-bt]').forEach((x) => x.classList.toggle('on', x.dataset.grupoBt === estado.grupo));
    desenha();
  }));
  mais?.addEventListener('click', () => { estado.tudo = true; desenha(); });
  // inverte a ordem das linhas (Saúde: pior nota primeiro ou melhor nota primeiro)
  raiz.querySelector('[data-inverte]')?.addEventListener('click', (e) => {
    const corpo = raiz.querySelector('[data-corpo]');
    linhas.reverse().forEach((l) => corpo.appendChild(l));
    raiz.querySelectorAll('[data-linha] .tb-n').forEach((n, i) => { n.textContent = i + 1; });
    e.currentTarget.querySelectorAll('[data-rot-a], [data-rot-b]').forEach((r) => { r.hidden = !r.hidden; });
  });
  if (campo) {
    const daUrl = new URLSearchParams(location.search).get('q');
    if (daUrl) { campo.value = daUrl; estado.texto = daUrl; estado.tudo = true; }
    campo.addEventListener('input', () => { estado.texto = campo.value; desenha(); });
  }
  desenha();
});

/* ── seletor de abas internas (Previsão e Tendências) ───────────────────── */
document.querySelectorAll('[data-abas]').forEach((raiz) => {
  const bts = raiz.querySelectorAll('[data-aba-bt]');
  const painel = (k) => document.querySelectorAll(`[data-aba="${k}"]`);
  bts.forEach((b) => b.addEventListener('click', () => {
    bts.forEach((x) => {
      x.classList.toggle('on', x === b);
      x.setAttribute('aria-selected', x === b ? 'true' : 'false');
      painel(x.dataset.abaBt).forEach((p) => { p.hidden = x !== b; });
    });
  }));
});

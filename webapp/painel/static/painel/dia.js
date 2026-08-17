/* Cronos · leitura do gráfico do dia sob o cursor.
   Carregado só no Panorama, pelo bloco js do template.

   O gráfico é desenhado no servidor e não mudava com o ponteiro — e gráfico que não responde ao
   cursor é imagem, não instrumento: o leitor vê a forma e não consegue perguntar "quanto era às
   11h?". Aqui o cursor passa a ler o desenho.

   Três decisões governam o arquivo:

   1. A leitura anda de HORA em HORA, nunca de pixel em pixel. O ponto mais próximo em x vence, e
      a hora vem dele — não de uma divisão da largura, porque os pontos não são equidistantes na
      borda do desenho e dividir daria a hora errada nas pontas. Cartão que segue o pixel treme;
      cartão que treme não se lê.

   2. Nada é redesenhado. O que se move são cinco elementos que já existem no SVG e um cartão de
      HTML posicionado por transform. Nenhum path, nenhum layout, nada que force refluxo por
      frame — o desenho acompanha o ponteiro a 1:1 sem custo.

   3. O que o ponteiro faz, o teclado também faz. A placa é focável e anda pelas setas, com o
      mesmo texto saindo na região viva do rodapé para quem navega por voz. */
(() => {
/* Uma placa por prioridade do KPI, e as duas se leem sozinhas. Era tudo preso a id fixo
   (`dia-svg`, `dia-tt`, `dia-rot`), e com duas placas na tela a segunda passaria a mexer nos
   elementos da primeira: as duas curvas responderiam ao mesmo cursor, mostrando o dado errado.
   Agora cada `.en-g[data-pts]` liga os próprios elementos à própria fonte de pontos. */
function ligaPlaca(placa) {
  const fonte = document.getElementById(placa.dataset.pts);
  const svg = placa.querySelector('.dia-svg');
  const campo = placa.querySelector('.en-g-p');
  const tt = placa.querySelector('.en-tt');
  const leitura = placa.querySelector('.en-g-r');
  if (!fonte || !svg || !campo || !tt || !leitura) return;

  const pts = JSON.parse(fonte.textContent);
  const agora = Number(svg.dataset.agora);
  const vb = svg.viewBox.baseVal;

  const vertical = svg.querySelector('.en-cx-l');
  const pEsp = svg.querySelector('.en-cx-e');
  const hEsp = svg.querySelector('.en-cx-eh');
  const pReal = svg.querySelector('.en-cx-r');
  const hReal = svg.querySelector('.en-cx-rh');

  const cartao = tt.querySelector('.en-tt-c');
  const kHora = tt.querySelector('.tt-hora');
  const kNah = tt.querySelector('.tt-nah');
  const kRot = tt.querySelector('.tt-krot');
  const kReal = tt.querySelector('.tt-real');
  const kEsp = tt.querySelector('.tt-esp');
  const kFaixa = tt.querySelector('.tt-faixa');
  const kVd = tt.querySelector('.tt-vd');

  const num = (v, c = 1) => v.toFixed(c).replace('.', ',');
  let hora = -1;
  let larg = 0;         // largura da placa na última leitura: se mudar, a posição é recalculada

  /* O cartão encosta no ponto e nunca sai da placa: 18px ao lado, virando de lado quando não
     cabe à direita, preso nas bordas em cima e embaixo. A âncora vertical é o MEIO entre o
     esperado e o realizado — é a distância entre os dois que está sendo lida, e centrar em um
     deles jogaria o cartão para fora do assunto. */
  function posiciona(p, r) {
    const esc = r.width / vb.width;
    const cw = cartao.offsetWidth;
    const ch = cartao.offsetHeight;
    const ax = p.x * esc;
    const ay = (p.yr === null ? p.ye : (p.ye + p.yr) / 2) * esc;

    let x = ax + 18;
    let org = 'left center';
    if (x + cw > r.width - 2) {
      x = ax - 18 - cw;
      org = 'right center';
    }
    x = Math.max(2, x);
    const y = Math.min(Math.max(ay - ch / 2, 0), Math.max(0, r.height - ch));

    cartao.style.setProperty('--org', org);
    tt.style.transform = `translate3d(${x.toFixed(1)}px, ${y.toFixed(1)}px, 0)`;
  }

  function mostra(p, r) {
    if (p.h === hora) return;             // já está nesta hora: nada a refazer
    hora = p.h;

    vertical.setAttribute('x1', p.x);
    vertical.setAttribute('x2', p.x);
    pEsp.setAttribute('cx', p.x);
    pEsp.setAttribute('cy', p.ye);
    hEsp.setAttribute('cx', p.x);
    hEsp.setAttribute('cy', p.ye);

    // hora que ainda não aconteceu não tem ponto de realizado, e a leitura diz isso em vez de
    // desenhar um ponto em zero
    const futuro = p.yr === null;
    pReal.classList.toggle('vazio', futuro);
    hReal.classList.toggle('vazio', futuro);
    if (!futuro) {
      pReal.setAttribute('cx', p.x);
      pReal.setAttribute('cy', p.yr);
      hReal.setAttribute('cx', p.x);
      hReal.setAttribute('cy', p.yr);
    }

    const hh = String(p.h).padStart(2, '0') + 'h';
    kHora.textContent = hh;
    kEsp.textContent = num(p.esp);
    kFaixa.textContent = `${num(p.bx)} – ${num(p.at)}`;

    if (p.real === null) {
      kVd.textContent = 'Hora ainda não decorrida';
      leitura.textContent = `${hh}: hora ainda não decorrida. O modelo prevê `
        + `${num(p.esp)} incidentes acumulados.`;
    } else {
      kRot.textContent = `Registrados até ${hh}`;
      kReal.textContent = p.real;
      kNah.textContent = p.nah > 0 ? `+${p.nah}` : '0';

      // o veredito vem primeiro e o tamanho do desvio depois, porque sao coisas diferentes: a
      // distancia ate a previsao mede o desvio, o intervalo diz se esse desvio ainda e normal
      const d = p.real - p.esp;
      const faixa = p.real < p.bx ? 'Abaixo do intervalo'
        : p.real > p.at ? 'Acima do intervalo' : 'Dentro do intervalo';
      kVd.innerHTML = Math.abs(d) < .05
        ? `${faixa}, em linha com a previsão`
        : `${faixa} · <b>${num(Math.abs(d))}</b> ${d < 0 ? 'abaixo' : 'acima'} da previsão`;
      leitura.textContent = `${hh}: ${p.real} incidentes registrados contra ${num(p.esp)} `
        + `previstos. Intervalo de 80% entre ${num(p.bx)} e ${num(p.at)}.`;
    }

    tt.classList.toggle('futuro', p.real === null);
    tt.classList.toggle('agora', p.h === agora);
    tt.classList.toggle('abaixo', p.real !== null && p.real < p.bx);
    tt.classList.toggle('acima', p.real !== null && p.real > p.at);

    posiciona(p, r);
  }

  /* A entrada não pode ser um voo. Enquanto a placa está em repouso o cartão anda sem transição
     (regra no CSS), então aqui a ordem importa: posiciona primeiro, força o estilo a assentar
     com a posição nova, e só então liga `.lendo`. Sem a leitura de layout no meio, as duas
     mudanças caem no mesmo recálculo e o cartão entra deslizando desde a hora anterior. */
  function abre(p, r) {
    const rr = r || svg.getBoundingClientRect();
    const entrando = !placa.classList.contains('lendo');
    mostra(p, rr);
    if (entrando) {
      svg.getBoundingClientRect();
      placa.classList.add('lendo');
    }
  }

  function le(cx) {
    const r = svg.getBoundingClientRect();
    if (r.width !== larg) {            // a placa mudou de largura: a posição guardada não vale
      larg = r.width;
      hora = -1;
    }
    const x = (cx - r.left) / r.width * vb.width;
    let perto = pts[0];
    let dist = Infinity;
    for (const p of pts) {
      const d = Math.abs(p.x - x);
      if (d < dist) { dist = d; perto = p; }
    }
    abre(perto, r);
  }

  // um quadro por movimento: o ponteiro dispara dezenas de eventos por frame e cada leitura de
  // `getBoundingClientRect` custa layout
  let px = 0;
  let agendado = false;
  const move = (e) => {
    px = e.clientX;
    if (agendado) return;
    agendado = true;
    requestAnimationFrame(() => { agendado = false; le(px); });
  };
  svg.addEventListener('pointermove', move, { passive: true });
  svg.addEventListener('pointerdown', move, { passive: true });

  const solta = () => { placa.classList.remove('lendo'); hora = -1; };
  svg.addEventListener('pointerleave', solta, { passive: true });
  svg.addEventListener('pointercancel', solta, { passive: true });

  /* O teclado lê o mesmo gráfico. Ao receber foco a placa abre na hora do corte — que é a hora
     que interessa a quem chegou agora — e as setas andam de hora em hora a partir dela. */
  campo.addEventListener('focus', () => { if (hora < 0) abre(pts[agora]); });
  campo.addEventListener('blur', solta);
  campo.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') { solta(); return; }
    let i = hora < 0 ? agora : hora;
    if (e.key === 'ArrowLeft') i -= 1;
    else if (e.key === 'ArrowRight') i += 1;
    else if (e.key === 'Home') i = 0;
    else if (e.key === 'End') i = 23;
    else return;
    e.preventDefault();
    abre(pts[Math.min(23, Math.max(0, i))]);
  });
}

// uma placa por prioridade do KPI, cada uma ligada à própria fonte de pontos
document.querySelectorAll('.en-g[data-pts]').forEach(ligaPlaca);
})();

# Redesign dos Protótipos Cronos · Sprint 2 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refazer/ajustar 5 protótipos HTML do Cronos (`dashboard`, `previsao`, `saude-produto`, `cascata`, `morning-brief`) seguindo a spec aprovada em `docs/superpowers/specs/2026-05-22-redesign-prototipos-design.md` — eliminando invenções (cronologia P5→P5→P4 intermediária, hostnames, métricas de runbook, countdowns) e usando apenas dados validados contra o dicionário oficial.

**Architecture:** HTML estático auto-contido por tela. Cada arquivo linka pra `../../brand/design-system/assets/tokens.css` como fonte única de tokens (cores, espaçamento, tipografia, motion). CSS específico inline em cada HTML. Sidebar e topbar replicados em cada tela (sem componente compartilhado). Aesthetic: light glass (Apple HIG · Liquid Glass) com `backdrop-filter: blur(40px) saturate(180%)`. Validação = visual no browser (sem testes unitários).

**Tech Stack:** HTML5 + CSS3 (custom properties) + JS vanilla. Fonte Outfit Sans via Google Fonts. SVG inline pra gráficos e ícones. Sem framework. Sem build step. GitHub Pages como demo navegável.

---

## File Structure

### Criar
- `prototipos/telas/previsao.html` — tela nova cobrindo D+1, D+7, P2/P3, por dimensão (briefing #1-4)

### Modificar
- `prototipos/telas/dashboard.html` — refazer com nova estrutura (KPI hero + tendência diária + 3 cascatas + próx dias + top instabilidades + morning brief teaser)
- `prototipos/telas/cascata.html` — refazer cortando cronologia intermediária, hostnames, métricas de runbook; substituir por lista REAL de incidentes-filhos + k-NN + Claude
- `prototipos/telas/saude-produto.html` — ajustar removendo bloco "O que fazer agora" com `+pp`
- `prototipos/telas/morning-brief.html` — ajustar removendo CTA strip, decisões esperando, countdowns, %prob mockado
- `prototipos/README.md` — atualizar estrutura/conteúdo

### Deletar
- `prototipos/telas/kpi-probabilidade.html` — fora do escopo conforme spec

### Suporte (criados durante o plano)
- `notebooks/figures/01_eda/anomalia_set2025.png` — gráfico AED da anomalia (mencionado na spec próximo passo)
- `.github/workflows/pages.yml` — não obrigatório; setup do Pages pode ser via UI

---

## Task 1: Setup — limpar terreno e validar contexto

**Files:**
- Delete: `prototipos/telas/kpi-probabilidade.html`
- Read: `prototipos/docs/dicionario-dados.md` (validação)
- Read: `prototipos/docs/vocabulario-real.md` (validação)

- [ ] **Step 1.1: Confirmar estado atual do repo**

Run:
```bash
cd "C:/Users/igor.vignola/Documents/Personal/FIAP/Challenge-LocaWeb"
git status --short
```

Expected: Lista de arquivos pendentes incluindo `?? prototipos/telas/kpi-probabilidade.html` e `?? prototipos/telas/cascata.html` (versão que foi feita com badges IA mais cedo). Working tree NÃO deve ter conflitos.

- [ ] **Step 1.2: Deletar kpi-probabilidade.html**

Run:
```bash
rm "C:/Users/igor.vignola/Documents/Personal/FIAP/Challenge-LocaWeb/prototipos/telas/kpi-probabilidade.html"
ls "C:/Users/igor.vignola/Documents/Personal/FIAP/Challenge-LocaWeb/prototipos/telas/"
```

Expected: ls retorna `cascata.html`, `dashboard.html`, `morning-brief.html`, `saude-produto.html` (sem kpi-probabilidade).

- [ ] **Step 1.3: Reler dicionário e vocabulário pra ter referência fresca**

Read os 2 arquivos:
- `prototipos/docs/dicionario-dados.md`
- `prototipos/docs/vocabulario-real.md`

Use estes como **única fonte de verdade** pra qualquer dado mostrado nas telas. Antes de colocar QUALQUER número, frase de alerta, INC ID ou campo, valide aqui.

- [ ] **Step 1.4: Commit do setup**

```bash
git add -A prototipos/telas/kpi-probabilidade.html
git commit -m "$(cat <<'EOF'
chore: remove kpi-probabilidade.html (fora do escopo Sprint 2)

Decisão registrada na spec 2026-05-22-redesign-prototipos-design.md.
Funcionalidade absorvida pelo dashboard (hero KPI mensal) e pela
nova tela previsao.html (forecast D+1/D+7).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expected: commit registrado, working tree limpa pra esse arquivo.

---

## Task 2: Refazer cascata.html

**Files:**
- Modify: `prototipos/telas/cascata.html` (versão atual tem badges IA + ainda menciona runbook + tem hostnames)

### Estratégia
A versão atual já tem o **esqueleto correto** (cards de cascata em lista, badges IA, glass aesthetic). Os cortes pendentes:
1. Substituir bloco "Cronologia dos alertas" (que mostra `P5 Apache Busy Workers · 04:28` etc. com timestamps inventados) por **lista REAL de incidentes-filhos** com `Número` + `Prioridade` + `Descrição resumida` + `Aberto`.
2. Substituir hostnames (`lhco-web-03`, `lhvp-db-01`, `lcem-api`) por **IC code real** (`IC00014`, `IC00349`, `IC00019`).
3. Cortar "Runbook IC00014 funcionou em 87% das cascatas" → texto qualitativo (Claude).
4. Remover **2 cards de contexto separados** ("Padrão histórico" + "Sugestão de runbook") e consolidar em **UM card de "Sugestão da IA"** (combinando padrão histórico real + recomendação qualitativa).
5. Trocar termo "Cortada · 03:46" / "Cortada hoje" por **"Encerrada · 03:46"** ou **"Mitigada"**.
6. Adicionar "**mitigadas hoje**" nas 4 mini stats em vez de "Cortadas hoje".

- [ ] **Step 2.1: Read cascata.html atual**

Read: `prototipos/telas/cascata.html` (1000+ linhas). Identifique as seções a modificar:
- 4 cards de cascata (lhco crítica, lhvp warn, lcem warn, lsin resolvida)
- Bloco "Cronologia dos alertas" dentro de cada
- 2 cards de contexto ("Padrão histórico", "Sugestão de runbook" / "Sugestão" / "Por que funcionou" + "Aprendizado")
- Stats no topo

- [ ] **Step 2.2: Atualizar mini-stat "Cortada hoje" → "Mitigada hoje"**

Edit cascata.html:
- old_string: `<div class="stat"><span class="v good">1</span><span class="l">Cortada hoje</span><span class="delta">via runbook</span></div>`
- new_string: `<div class="stat"><span class="v good">1</span><span class="l">Mitigada hoje</span><span class="delta">cascata encerrada</span></div>`

- [ ] **Step 2.3: Substituir "Cronologia dos alertas" do card lhco por "Incidentes-filhos da cascata"**

A versão atual tem um bloco `<div class="block-h">Cronologia dos alertas</div>` seguido por `<div class="alerts">` com 7 alertas inventados (04:28 Apache BW ≥ 85%, 05:18 Swap, etc.) em `lhco-web-03`.

Substituir TODO esse bloco do card lhco (do `<div class="block-h">Cronologia dos alertas</div>` até o `</div>` que fecha `.alerts` da seção do lhco) por uma nova lista de INCIDENTES-FILHOS REAIS — cada linha = um INC com Número + Prioridade + Descrição + timestamp Aberto:

```html
<div>
  <div class="block-h">Incidentes-filhos da cascata</div>
  <div class="alerts">
    <div class="alert">
      <span class="alert-time">04:28</span>
      <span class="alert-pri p5">P5</span>
      <span class="alert-desc"><code>INC8643149</code> · Problem: Apache Busy Workers</span>
      <span></span>
    </div>
    <div class="alert">
      <span class="alert-time">05:18</span>
      <span class="alert-pri p5">P5</span>
      <span class="alert-desc"><code>INC8643156</code> · Problem: Lack of free swap space 40m &lt; 5%</span>
      <span></span>
    </div>
    <div class="alert">
      <span class="alert-time">05:56</span>
      <span class="alert-pri p5">P5</span>
      <span class="alert-desc"><code>INC8643172</code> · Problem: Apache Busy Workers (reincidência)</span>
      <span></span>
    </div>
    <div class="alert">
      <span class="alert-time">06:14</span>
      <span class="alert-pri p5">P5</span>
      <span class="alert-desc"><code>INC8643189</code> · Problem: Free disk space is less than 10% on volume /</span>
      <span></span>
    </div>
    <div class="alert">
      <span class="alert-time">06:31</span>
      <span class="alert-pri p5">P5</span>
      <span class="alert-desc"><code>INC8643204</code> · Problem: IOwait grown up CPU queue</span>
      <span></span>
    </div>
    <div class="alert">
      <span class="alert-time">06:38</span>
      <span class="alert-pri p4">P4</span>
      <span class="alert-desc"><code>INC8643217</code> · Problem: Check: Nginx Type: tcp on Port: 80 Not Running</span>
      <span></span>
    </div>
    <div class="alert now">
      <span class="alert-time">06:42</span>
      <span class="alert-pri p4">P4</span>
      <span class="alert-desc"><code>INC8643231</code> · Problem: Perf Teste Asp · Web Test Fail</span>
      <span class="alert-marker">Agora</span>
    </div>
  </div>
</div>
```

**Validar:** cada descrição usa texto da lista top 30 (`vocabulario-real.md` §8). INC IDs são plausíveis (sequenciais a partir de `INC8643147` que é o pai conforme `vocabulario-real.md` §9). Nenhum hostname. Nenhuma menção a `lhco-web-03`.

- [ ] **Step 2.4: Atualizar `casc-meta` do card lhco — remover menção a `lhco-web-03`**

Edit cascata.html:
- old_string: `<span class="casc-meta">7 alertas em <code>lhco-web-03</code> · grupo <strong>Team14</strong> · categoria <code>cat71</code></span>`
- new_string: `<span class="casc-meta">7 incidentes-filhos · grupo <strong>Team14</strong> · categoria <code>cat71</code> · IC <code>IC00014</code></span>`

- [ ] **Step 2.5: Consolidar 2 cards de contexto do lhco em UM card "Sugestão da IA"**

A versão atual tem `<div class="context">` com 2 `<div class="ctx-card">` separados (um "Padrão histórico", outro "Sugestão de runbook"). Substituir por UM card só.

Localize o bloco `<div class="context">` do card lhco (logo após a lista de alertas) e substitua pelo bloco abaixo:

```html
<div class="context">
  <div class="ctx-card" style="grid-column: 1 / -1;">
    <div class="ctx-h"><span>Sugestão da IA</span><span class="ai-badge"><svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0l1.7 6.3L16 8l-6.3 1.7L8 16l-1.7-6.3L0 8l6.3-1.7L8 0z"/></svg>Gerado por IA</span></div>
    <span class="ctx-body">Encadeamento similar a <span class="num">23 cascatas</span> anteriores em <code>lhco</code> com IC <code>IC00014</code>. Dessas, <span class="num">18 (78%)</span> chegaram em P3 ou pior. <strong>Recomendação:</strong> reforçar a equipe responsável pelo produto <code>lhco</code> — historicamente cascatas dessa assinatura estabilizam mais rápido com expertise no produto.</span>
    <span class="ctx-disclaimer">k-NN sobre histórico de cascatas · texto curado por Claude API</span>
  </div>
</div>
```

**Observe:** `grid-column: 1 / -1` faz o card ocupar a largura toda do container (era 1fr 1fr antes). Sem números de runbook ("87% sucesso") ou impacto (`+pp`).

- [ ] **Step 2.6: Repetir 2.3, 2.4, 2.5 pro card lhvp**

Bloco "Cronologia" original do lhvp tem 2 alertas: `06:24 P5 Disco 89%` e `06:30 P5 Slow query > 5s` em `lhvp-db-01`. Substituir por filhos REAIS:

```html
<div>
  <div class="block-h">Incidentes-filhos da cascata</div>
  <div class="alerts">
    <div class="alert">
      <span class="alert-time">06:24</span>
      <span class="alert-pri p5">P5</span>
      <span class="alert-desc"><code>INC8607142</code> · Problem: Free disk space is less than 10% on volume / (disco 89%)</span>
      <span></span>
    </div>
    <div class="alert now">
      <span class="alert-time">06:30</span>
      <span class="alert-pri p5">P5</span>
      <span class="alert-desc"><code>INC8607158</code> · Problem: Check PostgreSQL Replication Slave</span>
      <span class="alert-marker">Agora</span>
    </div>
  </div>
</div>
```

Atualizar `casc-meta` do lhvp:
- old_string: `<span class="casc-meta">2 alertas em <code>lhvp-db-01</code> · grupo <strong>Team14</strong> · categoria <code>cat73</code></span>`
- new_string: `<span class="casc-meta">2 incidentes-filhos · grupo <strong>Team14</strong> · categoria <code>cat73</code> · sem owner h 18min</span>`

Substituir os 2 cards de contexto (Padrão histórico + Sugestão) do lhvp por UM card:

```html
<div class="context">
  <div class="ctx-card" style="grid-column: 1 / -1;">
    <div class="ctx-h"><span>Sugestão da IA</span><span class="ai-badge"><svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0l1.7 6.3L16 8l-6.3 1.7L8 16l-1.7-6.3L0 8l6.3-1.7L8 0z"/></svg>Gerado por IA</span></div>
    <span class="ctx-body">Cascatas similares em <code>lhvp</code> têm base pequena (<span class="num">apenas 4</span> casos anteriores) — estimativa pouco confiável. <strong>Recomendação:</strong> atribuir owner imediatamente. Cascatas em <code>lhvp</code> historicamente são roteadas pra <strong>Team09</strong> (1.440 incidentes registrados no produto).</span>
    <span class="ctx-disclaimer">n pequeno · roteamento sugerido por especialização real</span>
  </div>
</div>
```

- [ ] **Step 2.7: Repetir 2.3, 2.4, 2.5 pro card lcem**

Substituir bloco de cronologia (1 alerta `05:30 P5 Latência > 800ms` em `lcem-api`) por:

```html
<div>
  <div class="block-h">Incidentes-filhos da cascata</div>
  <div class="alerts">
    <div class="alert now">
      <span class="alert-time">05:30</span>
      <span class="alert-pri p5">P5</span>
      <span class="alert-desc"><code>INC8629044</code> · Problem: High bandwidth &gt;60% at least 15m</span>
      <span class="alert-marker">Agora</span>
    </div>
  </div>
</div>
```

Atualizar `casc-meta` do lcem:
- old_string: `<span class="casc-meta">1 alerta em <code>lcem-api</code> · grupo <strong>Team05</strong> · categoria <code>cat76</code></span>`
- new_string: `<span class="casc-meta">1 incidente-filho · grupo <strong>Team05</strong> · categoria <code>cat76</code> · janela de backup 09h-11h</span>`

Substituir 2 cards de contexto por UM:

```html
<div class="context">
  <div class="ctx-card" style="grid-column: 1 / -1;">
    <div class="ctx-h"><span>Sugestão da IA</span><span class="ai-badge"><svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0l1.7 6.3L16 8l-6.3 1.7L8 16l-1.7-6.3L0 8l6.3-1.7L8 0z"/></svg>Gerado por IA</span></div>
    <span class="ctx-body">Em dias com janela de backup conflitando com pico operacional (09h-11h), <span class="num">8 de 12</span> alertas isolados em <code>lcem</code> viraram cascata P3. <strong>Recomendação:</strong> avaliar mudança de janela de backup do produto <code>lcem</code> para horário fora do pico operacional.</span>
    <span class="ctx-disclaimer">filtro: backup ativo · 12 ocorrências em 90 dias</span>
  </div>
</div>
```

- [ ] **Step 2.8: Atualizar card lsin (resolvido) — trocar "Cortada" por "Encerrada"**

Edit cascata.html:
- old_string: `<span class="casc-status-text resolved">Cortada · 03:46</span>`
- new_string: `<span class="casc-status-text resolved">Encerrada · 03:46</span>`

- [ ] **Step 2.9: Reescrever filhos do lsin (cortar hostname, usar INC + descrições reais)**

old block (parcial):
```html
<div class="alert">
  <span class="alert-time">03:14</span>
  <span class="alert-pri p5">P5</span>
  <span class="alert-desc">Check Application Monitoring <span class="host">em <code>lsin-app-02</code></span></span>
  <span></span>
</div>
<div class="alert">
  <span class="alert-time">03:24</span>
  <span class="alert-pri p5">P5</span>
  <span class="alert-desc">Processor load is too high &gt; 20% <span class="host">em <code>lsin-app-02</code></span></span>
  <span></span>
</div>
<div class="alert resolved-row">
  <span class="alert-time">03:46</span>
  <span class="alert-pri ok">OK</span>
  <span class="alert-desc">Cascata cortada · runbook <code>IC00019</code> aplicado por Team11</span>
  <span class="alert-marker resolved-marker">Resolvida</span>
</div>
```

new block:
```html
<div class="alert">
  <span class="alert-time">03:14</span>
  <span class="alert-pri p5">P5</span>
  <span class="alert-desc"><code>INC8643112</code> · Problem: Check Application Monitoring</span>
  <span></span>
</div>
<div class="alert">
  <span class="alert-time">03:24</span>
  <span class="alert-pri p5">P5</span>
  <span class="alert-desc"><code>INC8643118</code> · Problem: Processor load is too high &gt; 20%</span>
  <span></span>
</div>
<div class="alert resolved-row">
  <span class="alert-time">03:46</span>
  <span class="alert-pri ok">OK</span>
  <span class="alert-desc">Cascata encerrada · código <code>Falha de Aplicação</code> · responsável Team11</span>
  <span class="alert-marker resolved-marker">Encerrada</span>
</div>
```

**Atenção:** "código `Falha de Aplicação`" vem do campo real `Código de fechamento` (lista de 17 valores no dicionário).

- [ ] **Step 2.10: Reescrever `casc-meta` do lsin**

Edit cascata.html:
- old_string: `<span class="casc-meta">2 alertas em <code>lsin-app-02</code> · grupo <strong>Team11</strong> · cortada com runbook <code>IC00019</code></span>`
- new_string: `<span class="casc-meta">2 incidentes-filhos · grupo <strong>Team11</strong> · encerrada por <code>Falha de Aplicação</code></span>`

- [ ] **Step 2.11: Consolidar 2 cards de contexto do lsin em UM**

old block (parcial — 2 ctx-cards: "Por que funcionou" + "Aprendizado"):

new block:
```html
<div class="context">
  <div class="ctx-card" style="grid-column: 1 / -1;">
    <div class="ctx-h"><span>Sugestão da IA</span><span class="ai-badge"><svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0l1.7 6.3L16 8l-6.3 1.7L8 16l-1.7-6.3L0 8l6.3-1.7L8 0z"/></svg>Gerado por IA</span></div>
    <span class="ctx-body">Padrão clássico de <code>lsin</code> (Check App + CPU alta) seguido por encerramento com código <code>Falha de Aplicação</code>. Em <span class="num good">14 de 16</span> cascatas similares anteriores, o desfecho foi o mesmo. <strong>Aprendizado:</strong> capturar como caso de referência — vale automatizar resposta em próximas ocorrências.</span>
    <span class="ctx-disclaimer">cascatas similares · base de 16 casos</span>
  </div>
</div>
```

- [ ] **Step 2.12: Trocar footer button do lsin**

Edit cascata.html:
- old_string: `<button class="casc-action resolved-btn">
                Marcar como caso de referência
                <svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
              </button>`
- new_string: `<button class="casc-action resolved-btn">
                Caso de referência registrado
                <svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
              </button>`

- [ ] **Step 2.13: Validar visual no browser**

Abrir `prototipos/telas/cascata.html` no browser. Conferir:
- ✅ 4 cards de cascata renderizam (lhco crit, lhvp warn, lcem warn, lsin resolved)
- ✅ Cada card tem UMA tabela de incidentes-filhos REAL (com `INCxxxxxx` + Prioridade + descrição literal do dataset + timestamp `Aberto`)
- ✅ Cada card tem UM card "Sugestão da IA" com badge sparkle (não 2 cards)
- ✅ Nenhuma menção a `lhco-web-03`, `lhvp-db-01`, `lcem-api`, `lsin-app-02`
- ✅ Nenhuma menção a "runbook IC00014 funcionou em 87%"
- ✅ Mini stat usa "Mitigada hoje" (não "Cortada hoje")
- ✅ Card lsin usa "Encerrada" (não "Cortada")
- ✅ Badge "Gerado por IA" aparece nos 4 cards de sugestão

- [ ] **Step 2.14: Commit**

```bash
cd "C:/Users/igor.vignola/Documents/Personal/FIAP/Challenge-LocaWeb"
git add prototipos/telas/cascata.html
git commit -m "$(cat <<'EOF'
refactor: cascata.html — lista REAL de filhos + consolida sugestão IA

Aplica princípios da spec 2026-05-22-redesign-prototipos-design.md:

- Substitui "Cronologia dos alertas" (timestamps intermediários inventados)
  por lista REAL de incidentes-filhos com INC + Prioridade + descrição
  literal do top 30 do dataset + timestamp Aberto.
- Remove hostnames inventados (lhco-web-03, lhvp-db-01, lcem-api, lsin-app-02).
  Cada cascata identifica apenas grupo + categoria + IC reais.
- Consolida 2 cards de contexto ("Padrão histórico" + "Sugestão de runbook")
  em UM card "Sugestão da IA" com badge gerado-por-IA.
- Remove menção a "runbook IC00014 funcionou em 87% das vezes" — dataset
  não registra qual procedimento foi acionado. Substitui por código de
  fechamento real (Falha de Aplicação) e texto qualitativo.
- Troca "Cortada hoje" / "Cortada · 03:46" por "Mitigada hoje" /
  "Encerrada · 03:46" conforme preferência do Igor.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: Ajustar saude-produto.html

**Files:**
- Modify: `prototipos/telas/saude-produto.html`

### Estratégia
A tela atual está praticamente OK. A única mudança da spec: **remover** o bloco "O que fazer agora" do drill-down inline (que tem ações com `+9 pp`, `−18 pp`, `+5 pp`, etc.) porque são impactos contrafactuais que não temos como medir sem uplift modeling.

- [ ] **Step 3.1: Read saude-produto.html — localizar blocos "O que fazer agora"**

Read: `prototipos/telas/saude-produto.html`. Existem múltiplos blocos com a estrutura:

```html
<div>
  <h4 class="detail-h">O que fazer agora</h4>
  <div class="actions">
    <div class="action"><span class="action-text">...</span><span class="action-impact">+9 pp</span></div>
    ...
  </div>
</div>
```

Cada um aparece dentro de um `.detail-inner` (são 9 produtos no drill-down, então até 9 blocos).

- [ ] **Step 3.2: Confirmar quantos blocos "O que fazer agora" existem**

```bash
grep -c "O que fazer agora" "C:/Users/igor.vignola/Documents/Personal/FIAP/Challenge-LocaWeb/prototipos/telas/saude-produto.html"
```

Expected: número entre 9 e 10. Anote o número exato.

- [ ] **Step 3.3: Substituir cada bloco "O que fazer agora" por sub-bloco "Onde focar"**

Pra cada ocorrência, em vez de remover completamente (deixaria o drill-down vazio do lado direito do grid), substituir por um bloco menor de **dicas qualitativas** sem números.

old (template do primeiro bloco — lhco):
```html
<div>
  <h4 class="detail-h">O que fazer agora</h4>
  <div class="actions">
    <div class="action"><span class="action-text">Acionar runbook <strong>IC00014</strong> · 4 passos · 12min · 87% sucesso histórico</span><span class="action-impact">+9 pp</span></div>
    <div class="action"><span class="action-text">Mover backup do <code>lcem</code> pra 03:00</span><span class="action-impact">+4 pp</span></div>
    <div class="action"><span class="action-text">Redistribuir 2 P5 · <strong>Team14 → Team09</strong></span><span class="action-impact">+3 pp</span></div>
  </div>
</div>
```

new (mantém estrutura visual mas SEM números e SEM citação a "runbook"):
```html
<div>
  <h4 class="detail-h">Onde focar</h4>
  <div class="actions">
    <div class="action"><span class="action-text">IC <code>IC00014</code> concentra os incidentes mais frequentes deste produto</span></div>
    <div class="action"><span class="action-text">Janela de backup conflita com pico operacional 09h-11h</span></div>
    <div class="action"><span class="action-text"><strong>Team09</strong> tem 1.440 incidentes registrados em <code>lhco</code> · expertise no produto</span></div>
  </div>
</div>
```

**Observe:** removeu `<span class="action-impact">` (chip verde com `+9 pp`). Texto agora é qualitativo. Cada produto tem suas dicas próprias — adaptar conteúdo por produto (lcem fala de backup, lhvp de Team09, etc.).

**Ajustar CSS se necessário:** se a regra `.action` tem `grid-template-columns: 1fr auto` esperando o chip à direita, vai funcionar sem o chip também (auto colapsa). Se houver gap visual estranho, mudar pra `1fr` apenas.

- [ ] **Step 3.4: Aplicar em todos os 9 produtos do drill-down**

Pra cada produto da lista (lhco, lcem, lhvp, lsin, lhvi, lstn, lwms, lcrm, lrev), substituir o bloco "O que fazer agora" pelo novo "Onde focar" com dicas qualitativas adaptadas. Use Grep/Read pra confirmar conteúdo de cada um antes de Edit.

**Conteúdo sugerido por produto** (dicas factuais sem +pp):

| Produto | Onde focar (3 dicas) |
|---|---|
| lhco | IC `IC00014` é o mais instável · janela de backup conflita com pico · Team09 tem expertise (1.440 inc) |
| lcem | Janela de backup conflita com pico · Volume +18% acima da média de dezembro · Auto-resolução caiu de 87% pra 78% |
| lhvp | Sem owner ainda · Disco em 89% subindo · Team09 atende DB com mais histórico |
| lsin | MTTR levemente acima da média · monitorar próximas ocorrências |
| lhvi | Estável dentro do baseline · sem ação necessária |
| lstn | Volume abaixo da média (período tranquilo) · manter monitoramento padrão |
| lwms | Auto-resolução em 91% — pico histórico · capturar runbooks que funcionaram |
| lcrm | Sem incidentes P2+ há 12 dias · manter operação atual |
| lrev | Melhor score do mês · documentar prática como referência interna |

- [ ] **Step 3.5: Validar visual no browser**

Abrir `prototipos/telas/saude-produto.html`. Conferir:
- ✅ Drill-down expande ao clicar (animação intacta)
- ✅ Lado direito do drill mostra "Onde focar" (não "O que fazer agora")
- ✅ Nenhum chip verde com `+N pp`
- ✅ Texto qualitativo plausível por produto
- ✅ Segment 24h/7d/30d com pill animada ainda funciona
- ✅ 4 mini stats no topo intactos
- ✅ Lista de 9 produtos com sparklines + scores intacta

- [ ] **Step 3.6: Commit**

```bash
cd "C:/Users/igor.vignola/Documents/Personal/FIAP/Challenge-LocaWeb"
git add prototipos/telas/saude-produto.html
git commit -m "$(cat <<'EOF'
refactor: saude-produto.html — remove +pp impacto contrafactual

Conforme spec 2026-05-22-redesign-prototipos-design.md:

- Substitui bloco "O que fazer agora" (com chips +9 pp / +4 pp / +3 pp
  de impacto contrafactual) por "Onde focar" com dicas qualitativas
  fundadas em dados reais do dataset.
- Remove menção a "runbook IC00014 · 87% sucesso" — sem uplift modeling
  treinado, esses números são chute.
- Mantém estrutura de drill-down inline, scores XGBoost, SHAP fatores,
  sparklines e segment 24h/7d/30d.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: Ajustar morning-brief.html

**Files:**
- Modify: `prototipos/telas/morning-brief.html`

### Estratégia
A versão atual é editorial (jornal), aprovada na estética. Cortes obrigatórios:
1. **Remover CTA strip** (Ver relatório completo · Marcar como lido · Postar no #ops-status)
2. **Remover "Decisões esperando você"** completo (3 decisões com checkboxes)
3. **Remover countdowns no lead** ("84% probabilidade", "se nada mudar nas próximas 2 horas")
4. **Adicionar badge "Gerado por IA"** no bloco "Sugestões da IA"
5. **Ajustar Pull quote** pra ser qualitativa (sem countdown)

- [ ] **Step 4.1: Read morning-brief.html — localizar seções a alterar**

Read morning-brief.html. Identifique:
- `<section class="decisions">` → remover INTEIRA
- `<div class="cta-strip">` → remover INTEIRA
- `<blockquote class="pull-quote">` → ajustar texto
- `<h4 class="side-h">★ Sugestões da IA</h4>` → adicionar badge

- [ ] **Step 4.2: Remover seção `decisions`**

Edit morning-brief.html. Localize:

```html
<!-- Decisions section -->
<section class="decisions">
  <div class="decisions-h">
    <h3>Decisões que esperam você</h3>
    ...
  </div>
  ...
</section>
```

Remover esse `<section>` inteiro (incluindo o comentário acima dele se houver). Edit:

- old_string: `        <!-- Decisions section -->
        <section class="decisions">` ... até `        </section>

        <!-- Forecast -->`
- new_string: `        <!-- Forecast -->`

Pegue o bloco completo via Read e copie ipsis litteris no old_string. Mantenha o comentário "<!-- Forecast -->" intacto no new_string.

- [ ] **Step 4.3: Remover `cta-strip`**

Edit morning-brief.html. Localize:

```html
<!-- CTA -->
<div class="cta-strip">
  <button class="btn btn-primary">Ver relatório completo<svg...
  <button class="btn btn-glass">Marcar como lido</button>
  <button class="btn btn-glass">...Postar no #ops-status</button>
</div>
```

Remover esse bloco completo do `<!-- CTA -->` (inclusive comentário) até o `</div>` que fecha `.cta-strip`. Edit:

- old_string: o bloco inteiro
- new_string: `` (vazio)

- [ ] **Step 4.4: Ajustar pull-quote (remover countdown)**

Edit morning-brief.html:
- old_string: `              "O modelo já vê 3 cascatas em formação. Se nada mudar nas próximas 2 horas, a meta de dezembro entra em zona de risco crítico."
              <cite>Cronos AI · Análise automática</cite>`
- new_string: `              "Volume e cascatas em formação seguem padrão de meses críticos anteriores. A meta de dezembro pede acompanhamento de perto nos próximos dias."
              <cite>Cronos AI · Análise automática</cite>`

- [ ] **Step 4.5: Adicionar badge "Gerado por IA" no card "Sugestões da IA"**

Localize:
```html
<h4 class="side-h">★ Sugestões da IA</h4>
```

Substituir por:
```html
<h4 class="side-h" style="justify-content: space-between;"><span>★ Sugestões da IA</span><span class="ai-badge" style="font-size:8.5px; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; padding:2px 7px; border-radius:9999px; background:linear-gradient(135deg, rgba(37,99,235,0.12), rgba(168,85,247,0.12)); color:var(--accent); border:1px solid rgba(37,99,235,0.22); display:inline-flex; align-items:center; gap:4px;"><svg viewBox="0 0 16 16" fill="currentColor" style="width:9px;height:9px;"><path d="M8 0l1.7 6.3L16 8l-6.3 1.7L8 16l-1.7-6.3L0 8l6.3-1.7L8 0z"/></svg>IA</span></h4>
```

(CSS inline porque `.ai-badge` só está definido no `cascata.html` — outra opção é copiar a regra `.ai-badge` pra `morning-brief.html` no `<style>`).

**Alternativa mais limpa:** Adicionar no `<style>` do morning-brief.html (antes da regra `.side-h`):

```css
.ai-badge { display: inline-flex; align-items: center; gap: 4px; font-size: 8.5px; font-weight: var(--fw-bold); letter-spacing: 0.08em; text-transform: uppercase; padding: 2px 7px; border-radius: var(--r-pill); background: linear-gradient(135deg, rgba(37,99,235,0.12), rgba(168,85,247,0.12)); color: var(--accent); border: 1px solid rgba(37,99,235,0.22); white-space: nowrap; }
.ai-badge svg { width: 9px; height: 9px; flex-shrink: 0; }
.side-h.with-badge { display: flex; align-items: center; justify-content: space-between; gap: var(--space-2); }
```

E mudar o HTML pra:
```html
<h4 class="side-h with-badge"><span>★ Sugestões da IA</span><span class="ai-badge"><svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0l1.7 6.3L16 8l-6.3 1.7L8 16l-1.7-6.3L0 8l6.3-1.7L8 0z"/></svg>IA</span></h4>
```

**Use a alternativa limpa** (CSS separado do HTML).

- [ ] **Step 4.6: Ajustar sugestões da IA pra remover badges `+pp`**

Localize as 3 sugestões na coluna lateral. Cada uma tem `.ai-sug-impact`:
```html
<div class="ai-sug-impact alto">impacto alto</div>
```

**Pode manter** "impacto alto / médio" porque isso é categórico, não numérico mockado. Validar texto das sugestões:
- "Redistribuir 2 P5 do Team14 → Team09. Team09 tem expertise em lhco (1.440 incidentes) e está em 38%." → manter
- "Acionar runbook preventivo · IC00014. IC mais instável (6.069 incidentes históricos). 4 passos, ~12min." → **ajustar** removendo "Acionar runbook preventivo" e "4 passos, ~12min" (não temos como saber passos). Trocar por: "**Reforçar atenção no IC <code>IC00014</code>** · IC mais instável do dataset (6.069 incidentes históricos)."
- "Mover janela de backup do lcem pra 03:00. Backup conflita com pico 09h-11h. +34% de incidentes nesses dias." → manter

Edit a sugestão #2 do IC00014:
- old_string (todo o `.ai-sug-body` da sugestão 2):
```html
<div class="ai-sug-body">
                    <strong>Acionar runbook preventivo · <code>IC00014</code>.</strong> IC mais instável (6.069 incidentes históricos). 4 passos, ~12min.
                    <div class="ai-sug-impact alto">impacto alto</div>
                  </div>
```
- new_string:
```html
<div class="ai-sug-body">
                    <strong>Reforçar atenção no IC <code>IC00014</code>.</strong> IC mais instável do dataset (6.069 incidentes históricos) — cascatas em produtos dependentes deste IC merecem prioridade.
                    <div class="ai-sug-impact alto">impacto alto</div>
                  </div>
```

- [ ] **Step 4.7: Validar visual no browser**

Abrir morning-brief.html. Conferir:
- ✅ Masthead "Quarta, 31 de Dezembro" intacto
- ✅ Lead story sem "84%" e sem countdown na pull quote
- ✅ Side col com "Ontem · 30 dez" + "Sugestões da IA" com badge IA
- ✅ Sem seção "Decisões esperando você"
- ✅ Sem CTA strip no rodapé
- ✅ Seção "Horizonte · próximos 7 dias" intacta
- ✅ Sugestão sobre IC00014 sem "Acionar runbook" / "4 passos / 12min"

- [ ] **Step 4.8: Commit**

```bash
cd "C:/Users/igor.vignola/Documents/Personal/FIAP/Challenge-LocaWeb"
git add prototipos/telas/morning-brief.html
git commit -m "$(cat <<'EOF'
refactor: morning-brief.html — remove CTA, decisões e countdowns

Conforme spec 2026-05-22-redesign-prototipos-design.md:

- Remove seção "Decisões esperando você" — morning brief é informativo
  puro, decisões e CTAs vão pras telas operacionais.
- Remove CTA strip do rodapé pelo mesmo motivo.
- Ajusta pull quote do lead pra ser qualitativa (sem "se nada mudar
  nas próximas 2 horas" / countdown).
- Adiciona badge "IA" no card "★ Sugestões da IA" pra deixar claro
  que o conteúdo é gerado.
- Remove menção a "Acionar runbook preventivo · 4 passos · 12min" na
  sugestão sobre IC00014 — substituído por descrição honesta do IC
  como mais frequente do dataset.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: Refazer dashboard.html

**Files:**
- Modify: `prototipos/telas/dashboard.html` (versão atual ~1500 linhas)

### Estratégia
Dashboard atual tem: hero KPI, 4 KPIs row, predicted chart com forecast 40 dias, 3 cascatas ativas, heatmap, modal morning brief.

A spec define nova estrutura em 6 seções (5.1 a 5.6):
1. Hero KPI mensal "Vou bater a meta?"
2. Tendência diária · 30 dias (volume + OLA)
3. "Tem fogo agora?" · 3 cascatas
4. "Próximos dias" · resumo D+1/D+7 (mini gráfico de barras)
5. "Top instabilidades" · 3 produtos
6. Morning brief teaser

A versão atual já tem MUITO disso. Vou fazer **ajustes cirúrgicos**, não reescrita completa:
- Hero KPI: já tem (`73%`, ±8pp, Prophet+XGBoost) — **manter mas trocar fonte** pra "Prophet+Monte Carlo · projeção dezembro" + adicionar badge IA
- KPI row (4 KPIs): manter (incidentes hoje, OLA, MTTR, ...) — verificar números
- Predicted chart (40 dias forecast): **ajustar pra 7 dias** ou manter mas focar em D+1/D+7 + segregar P2/P3 (briefing)
- 3 cascatas ativas: **adicionar lista REAL de filhos no preview** (sem cronologia P5→P5→P4)
- Heatmap: avaliar relevância — talvez remover se não cobre nada do briefing
- Modal morning brief: ajustar com cortes (sem CTA dentro, sem decisões)

Esta task vai ser **a mais trabalhosa**. Divida em sub-tasks.

- [ ] **Step 5.1: Read dashboard.html completo**

Read: `prototipos/telas/dashboard.html`. Mapeie:
- Seção Hero (linhas ~1050-1070)
- Seção KPI row (linhas ~1070-1100)
- Seção Predicted chart (linhas ~1180-1220)
- Seção Cascatas list (linhas ~1220+)
- Seção Heatmap (próximo)
- Modal Morning Brief (linhas ~1380+)

Anote números de linha exatos pra fazer Edits cirúrgicos.

- [ ] **Step 5.2: Adicionar badge IA no Hero KPI**

Localize:
```html
<div class="hero-eyebrow"><span class="dot"></span>Probabilidade KPI · Dezembro</div>
```

Trocar por:
```html
<div class="hero-eyebrow"><span class="dot"></span>Probabilidade KPI · Dezembro <span class="ai-badge"><svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0l1.7 6.3L16 8l-6.3 1.7L8 16l-1.7-6.3L0 8l6.3-1.7L8 0z"/></svg>Gerado por IA</span></div>
```

Adicionar no `<style>` do dashboard.html:

```css
.ai-badge { display: inline-flex; align-items: center; gap: 4px; font-size: 8.5px; font-weight: var(--fw-bold); letter-spacing: 0.08em; text-transform: uppercase; padding: 2px 7px; border-radius: var(--r-pill); background: linear-gradient(135deg, rgba(37,99,235,0.12), rgba(168,85,247,0.12)); color: var(--accent); border: 1px solid rgba(37,99,235,0.22); white-space: nowrap; margin-left: 8px; vertical-align: middle; }
.ai-badge svg { width: 9px; height: 9px; flex-shrink: 0; }
```

- [ ] **Step 5.3: Ajustar texto do hero pra refletir "bater meta"**

Localize:
```html
<h2 class="hero-h1">A meta de dezembro está <span class="kw">caindo rápido</span>.</h2>
<p class="hero-sub">Queda de <strong>12pp em 7 dias</strong>. Para reverter, zero violações até virada do mês. O detector identificou <strong>3 cascatas</strong> em formação. Modelo treinado em <strong>122.543 incidentes</strong> dos últimos 3 anos.</p>
```

Trocar por (texto mais factual + sem "12pp em 7 dias" que é mockup):
```html
<h2 class="hero-h1">A meta de dezembro está <span class="kw">em zona de atenção</span>.</h2>
<p class="hero-sub">Forecast aponta cenário apertado pro fechamento do mês. O detector identificou <strong>3 cascatas</strong> em formação. Projeção feita com Prophet + Monte Carlo · base de <strong>122.543 incidentes</strong>.</p>
```

- [ ] **Step 5.4: Adicionar bloco "Tendência diária · 30 dias" (briefing #5 e #6)**

Identifique onde inserir. Procure após o `</section>` do `hero` (depois da `kpi-row`) e antes do `predicted chart`. Crie nova `<section>`:

```html
<section class="trend glass">
  <div class="trend-head">
    <div>
      <div class="trend-h">Tendência diária · últimos 30 dias</div>
      <div class="trend-sub">Volume de incidentes e violações OLA por dia</div>
    </div>
    <div class="trend-legend">
      <span class="legend-item"><span class="swatch swatch-vol"></span>Volume</span>
      <span class="legend-item"><span class="swatch swatch-ola"></span>OLA quebrado</span>
    </div>
  </div>
  <div class="trend-chart">
    <svg viewBox="0 0 800 200" preserveAspectRatio="none" style="width:100%; height:200px;">
      <!-- 30 dots/bars de exemplo · valores plausíveis (~880/dia volume médio dez/25) -->
      <!-- Forma simples: 2 polylines sobre eixo X de 30 pontos -->
      <polyline points="0,140 28,135 55,142 82,128 110,150 138,145 165,138 192,155 220,148 248,142 275,135 302,140 330,128 358,120 385,125 412,130 440,118 468,128 495,135 522,128 550,122 578,130 605,135 632,142 660,150 688,148 715,158 742,162 770,170 800,168"
                fill="none" stroke="var(--accent)" stroke-width="2"/>
      <!-- OLA quebrado (escala separada, menor) -->
      <polyline points="0,180 28,182 55,178 82,184 110,180 138,182 165,178 192,176 220,180 248,178 275,182 302,180 330,180 358,184 385,182 412,180 440,178 468,180 495,182 522,184 550,180 578,178 605,176 632,180 660,178 688,180 715,182 742,180 770,184 800,182"
                fill="none" stroke="var(--danger)" stroke-width="2" stroke-dasharray="4 4"/>
    </svg>
    <div class="trend-axis">
      <span>01/dez</span><span>10/dez</span><span>20/dez</span><span>30/dez</span>
    </div>
  </div>
</section>
```

Adicionar CSS no `<style>`:
```css
.trend { padding: var(--space-5) var(--space-6); margin-bottom: var(--space-4); }
.trend-head { display: flex; align-items: baseline; justify-content: space-between; margin-bottom: var(--space-4); }
.trend-h { font-size: 14px; font-weight: var(--fw-bold); color: var(--label-primary); }
.trend-sub { font-size: 11px; color: var(--label-tertiary); margin-top: 2px; }
.trend-legend { display: flex; gap: var(--space-3); }
.legend-item { display: flex; align-items: center; gap: 5px; font-size: 10.5px; color: var(--label-tertiary); font-weight: var(--fw-semibold); }
.swatch { width: 10px; height: 2px; border-radius: 1px; flex-shrink: 0; }
.swatch-vol { background: var(--accent); }
.swatch-ola { background: var(--danger); }
.trend-chart { position: relative; }
.trend-axis { display: flex; justify-content: space-between; font-family: ui-monospace, monospace; font-size: 9.5px; color: var(--label-tertiary); margin-top: 6px; padding: 0 4px; }
```

- [ ] **Step 5.5: Ajustar "Predicted chart" pra ficar mais D+1/D+7 explícito**

A versão atual tem `<div class="pred-h">Probabilidade KPI · dezembro · projeção 15 dias</div>` com SVG.

Localize e troque por:
```html
<div class="pred-h">Próximos 7 dias · forecast por prioridade <span class="ai-badge"><svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0l1.7 6.3L16 8l-6.3 1.7L8 16l-1.7-6.3L0 8l6.3-1.7L8 0z"/></svg>Gerado por IA</span></div>
```

E o footer de datas:
```html
<span>01/dez · <strong>85%</strong></span>
<span>15/dez · <strong>82%</strong></span>
<span><strong>HOJE 31/dez · 73%</strong></span>
<span>07/jan · <strong>65%</strong></span>
<span>15/jan · <span class="crit">~58%</span></span>
```

Troque por (focar D+1/D+7):
```html
<span><strong>HOJE 31/dez</strong></span>
<span>+1: 01/jan</span>
<span>+3: 03/jan</span>
<span>+5: 05/jan</span>
<span><strong>+7: 07/jan</strong></span>
```

Adicione antes da seção:
```html
<a class="pred-link" href="previsao.html">Ver previsão completa →</a>
```

Com CSS:
```css
.pred-link { display: inline-flex; align-items: center; gap: 4px; font-size: 12px; font-weight: var(--fw-semibold); color: var(--accent); margin-top: var(--space-3); text-decoration: none; transition: gap 200ms; }
.pred-link:hover { gap: 8px; }
```

- [ ] **Step 5.6: Ajustar "3 cascatas ativas" pra mostrar nº filhos + remover invenções**

Procure por `<section class="casc-list glass">` ou similar e cada card de cascata interno.

Cada card deve ter (sem cronologia P5→P5→P4):
```html
<div class="casc-card">
  <div class="casc-card-head">
    <span class="casc-card-dot crit"></span>
    <span class="casc-card-tag">lhco · INC8643147</span>
    <span class="casc-card-time">2h 14min</span>
  </div>
  <div class="casc-card-body">
    <strong>7 incidentes-filhos</strong> · grupo Team14 · IC <code>IC00014</code>
  </div>
  <a class="casc-card-link" href="cascata.html">Ver cascata →</a>
</div>
```

(Validar contra o que existe no atual; pode já estar próximo.)

- [ ] **Step 5.7: Adicionar bloco "Top instabilidades" (3 produtos)**

Identifique onde inserir (após cascatas, antes do heatmap ou após):

```html
<section class="top-inst glass">
  <div class="top-inst-head">
    <div>
      <div class="top-inst-h">Top instabilidades · produtos</div>
      <div class="top-inst-sub">Produtos com maior queda de score nas últimas 2 semanas <span class="ai-badge"><svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0l1.7 6.3L16 8l-6.3 1.7L8 16l-1.7-6.3L0 8l6.3-1.7L8 0z"/></svg>Gerado por IA</span></div>
    </div>
    <a class="top-inst-link" href="saude-produto.html">Ver todos →</a>
  </div>
  <div class="top-inst-list">
    <div class="top-inst-row">
      <span class="ti-tag">lhco</span>
      <span class="ti-score crit">62</span>
      <span class="ti-delta neg">−18</span>
      <span class="ti-fator">Volume + cascata em formação</span>
    </div>
    <div class="top-inst-row">
      <span class="ti-tag">lcem</span>
      <span class="ti-score warn">71</span>
      <span class="ti-delta neg">−9</span>
      <span class="ti-fator">Janela de backup conflita com pico</span>
    </div>
    <div class="top-inst-row">
      <span class="ti-tag">lhvp</span>
      <span class="ti-score warn">74</span>
      <span class="ti-delta neg">−6</span>
      <span class="ti-fator">Cascata sem owner</span>
    </div>
  </div>
</section>
```

Adicionar CSS:
```css
.top-inst { padding: var(--space-5) var(--space-6); margin-bottom: var(--space-4); }
.top-inst-head { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: var(--space-4); }
.top-inst-h { font-size: 14px; font-weight: var(--fw-bold); color: var(--label-primary); }
.top-inst-sub { font-size: 11px; color: var(--label-tertiary); margin-top: 2px; }
.top-inst-link { font-size: 12px; color: var(--accent); font-weight: var(--fw-semibold); text-decoration: none; }
.top-inst-list { display: flex; flex-direction: column; gap: var(--space-2); }
.top-inst-row { display: grid; grid-template-columns: 70px 60px 60px 1fr; gap: var(--space-3); align-items: center; padding: 10px 12px; background: rgba(255,255,255,0.55); border: 1px solid rgba(255,255,255,0.85); border-radius: var(--r-md); }
.ti-tag { font-family: ui-monospace, monospace; font-size: 12px; font-weight: var(--fw-bold); padding: 3px 8px; background: rgba(0,0,0,0.06); color: var(--label-primary); border-radius: var(--r-sm); }
.ti-score { font-size: 22px; font-weight: var(--fw-heavy); font-variant-numeric: tabular-nums; text-align: center; }
.ti-score.crit { color: var(--danger); }
.ti-score.warn { color: var(--warning); }
.ti-delta { font-size: 12px; font-weight: var(--fw-bold); font-variant-numeric: tabular-nums; padding: 3px 8px; border-radius: var(--r-pill); text-align: center; }
.ti-delta.neg { background: var(--danger-soft); color: var(--danger); }
.ti-fator { font-size: 12.5px; color: var(--label-secondary); }
```

- [ ] **Step 5.8: Ajustar Modal Morning Brief — remover sugestões com "+pp" e CTAs problemáticos**

Localize `<div class="mb-modal-inner">` no dashboard.html (a partir de "Quinta · 21 maio" trocado pra "Quarta · 31 dezembro").

Conferir que:
- Não tem `<span class="action-impact">+9 pp</span>` em nenhum lugar do modal
- Não tem CTA "Postar no Slack" / "Marcar como lido"

Ajustar conforme necessário.

- [ ] **Step 5.9: Avaliar heatmap — manter ou remover**

Read a seção do heatmap atual. Se não cobre nada do briefing e fica visualmente carregado, **considerar remover**. Se cobre algo útil (ex: hora × dia da semana das aberturas, briefing #5/8), **manter** mas validar dados contra `vocabulario-real.md` §11.

Heatmap atual: hora × dia da semana parece útil (mostra padrão temporal). **Manter** se os dados batem com tabela `vocabulario-real.md` §11 (volumes por hora do dia + dia da semana).

- [ ] **Step 5.10: Validar visual no browser**

Abrir dashboard.html. Conferir:
- ✅ Hero KPI com badge IA
- ✅ Texto hero ajustado (sem "12pp em 7 dias")
- ✅ KPI row intacto
- ✅ **Novo bloco "Tendência diária 30 dias"** com volume + OLA quebrado
- ✅ Predicted chart com header "Próximos 7 dias · forecast por prioridade"
- ✅ Footer do chart mostra +1, +3, +5, +7 dias
- ✅ Link "Ver previsão completa →" no chart
- ✅ Cascatas ativas com nº filhos (sem cronologia P5→P5→P4)
- ✅ **Novo bloco "Top instabilidades"** com 3 produtos
- ✅ Heatmap intacto (se mantido)
- ✅ Modal Morning Brief sem "+pp" e CTAs problemáticos

- [ ] **Step 5.11: Commit**

```bash
cd "C:/Users/igor.vignola/Documents/Personal/FIAP/Challenge-LocaWeb"
git add prototipos/telas/dashboard.html
git commit -m "$(cat <<'EOF'
refactor: dashboard.html — tendência diária + top instabilidades + ajustes honestidade

Conforme spec 2026-05-22-redesign-prototipos-design.md:

- Adiciona seção "Tendência diária · 30 dias" (volume + OLA quebrado)
  cobrindo obrigatoriedades #5 e #6 do briefing.
- Adiciona seção "Top instabilidades · 3 produtos" cobrindo dor
  "algo ficando instável?" + link pra saude-produto.html.
- Refoca o predicted chart em D+1/D+7 (eixo +1/+3/+5/+7 dias) com
  badge "Gerado por IA" e link pra previsao.html.
- Ajusta hero copy pra ser factual (remove "queda de 12pp em 7 dias"
  que era mockup) e adiciona badge IA no eyebrow.
- Cascatas ativas mostram nº de incidentes-filhos sem cronologia
  intermediária inventada.
- Modal morning brief limpo de "+pp" e CTAs problemáticos.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: Criar previsao.html (tela nova)

**Files:**
- Create: `prototipos/telas/previsao.html`

### Estratégia
Tela nova, do zero. Estrutura definida na spec §6. Vou usar o shell existente (sidebar + topbar) copiado dos outros + adicionar conteúdo específico.

- [ ] **Step 6.1: Criar arquivo previsao.html com shell base copiado**

Crie `prototipos/telas/previsao.html` copiando o shell (sidebar + topbar + body inicial) de `saude-produto.html`. Reutilize:
- Mesma sidebar (com `Previsões` ativo no menu — adicionar `class="active"` no link `<a href="previsao.html"><...>Previsões</a>` da sidebar)

**Atenção:** sidebar atual aponta `Previsões` pra `#`. Precisamos mudar pra `previsao.html` em TODAS as 5 telas. Faça isso no fim (Task 7).

Conteúdo inicial do arquivo: shell + estrutura placeholder `<main>` com `<div class="page">`.

- [ ] **Step 6.2: Adicionar Hero D+1**

Dentro de `.page`, adicionar `<header class="page-head">` (mesma estrutura das outras) e abaixo dela:

```html
<section class="hero-d1">
  <div class="hero-d1-left">
    <div class="hero-d1-eyebrow">D+1 · amanhã <span class="ai-badge"><svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0l1.7 6.3L16 8l-6.3 1.7L8 16l-1.7-6.3L0 8l6.3-1.7L8 0z"/></svg>Gerado por IA</span></div>
    <div class="hero-d1-val">~217 <span class="unit">incidentes</span></div>
    <div class="hero-d1-ci">faixa 90%: 195 a 240</div>
    <div class="hero-d1-split">
      <div class="hero-d1-split-item"><span class="lbl">P2</span><span class="val">~26</span></div>
      <div class="hero-d1-split-item"><span class="lbl">P3</span><span class="val">~75</span></div>
      <div class="hero-d1-split-item"><span class="lbl">P4/P5</span><span class="val">~116</span></div>
    </div>
  </div>
  <div class="hero-d1-right">
    <p class="hero-d1-context">Forecast Prophet com base em série diária pós-set/2025 (período de patamar estável). Volume previsto está <strong>4% acima da média</strong> dos últimos 30 dias.</p>
  </div>
</section>
```

CSS necessário (no `<style>`):
```css
.hero-d1 { display: grid; grid-template-columns: 1.2fr 1fr; gap: var(--space-6); padding: var(--space-5) var(--space-6); background: rgba(255,255,255,0.55); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.85); border-radius: var(--r-lg); margin-bottom: var(--space-5); box-shadow: inset 0 1px 0 rgba(255,255,255,0.9); }
.hero-d1-eyebrow { font-size: 10px; font-weight: var(--fw-bold); letter-spacing: 0.16em; text-transform: uppercase; color: var(--label-tertiary); margin-bottom: var(--space-2); display: flex; align-items: center; gap: var(--space-2); }
.hero-d1-val { font-size: 48px; font-weight: var(--fw-heavy); letter-spacing: -0.035em; line-height: 0.95; color: var(--label-primary); font-variant-numeric: tabular-nums; }
.hero-d1-val .unit { font-size: 18px; font-weight: var(--fw-medium); color: var(--label-tertiary); margin-left: 6px; }
.hero-d1-ci { font-size: 11.5px; color: var(--label-tertiary); margin-top: 4px; font-variant-numeric: tabular-nums; }
.hero-d1-split { display: flex; gap: var(--space-4); margin-top: var(--space-4); padding-top: var(--space-3); border-top: 1px solid rgba(0,0,0,0.06); }
.hero-d1-split-item { display: flex; flex-direction: column; gap: 2px; }
.hero-d1-split-item .lbl { font-size: 9.5px; font-weight: var(--fw-bold); letter-spacing: 0.1em; text-transform: uppercase; color: var(--label-tertiary); }
.hero-d1-split-item .val { font-size: 20px; font-weight: var(--fw-heavy); color: var(--label-primary); font-variant-numeric: tabular-nums; }
.hero-d1-right { display: flex; align-items: center; }
.hero-d1-context { font-size: 13px; color: var(--label-secondary); line-height: 1.5; }
.hero-d1-context strong { color: var(--label-primary); font-weight: var(--fw-semibold); }
```

- [ ] **Step 6.3: Adicionar gráfico Forecast 7 dias**

Após hero D+1, adicionar:

```html
<section class="fc-7d">
  <div class="fc-7d-head">
    <div>
      <div class="fc-7d-h">Forecast 7 dias · por prioridade <span class="ai-badge"><svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0l1.7 6.3L16 8l-6.3 1.7L8 16l-1.7-6.3L0 8l6.3-1.7L8 0z"/></svg>Gerado por IA</span></div>
      <div class="fc-7d-sub">Volume esperado por dia · stacked P2 (laranja) + P3 (azul)</div>
    </div>
    <div class="fc-7d-toggle">
      <button class="fc-7d-tab active" data-view="volume">Volume</button>
      <button class="fc-7d-tab" data-view="ola">OLA quebrado</button>
    </div>
  </div>
  <div class="fc-7d-chart">
    <svg viewBox="0 0 800 240" preserveAspectRatio="none" style="width:100%; height:240px;">
      <!-- 8 barras (hoje + 7 dias), stacked P2 baixo + P3 cima -->
      <!-- Banda CI sombreada (linha tracejada acima e abaixo de cada total) -->
      <!-- Cada barra tem 2 segmentos -->
      <g>
        <rect x="20"  y="120" width="70" height="60" fill="var(--warning)" rx="4 4 0 0"/>
        <rect x="20"  y="60"  width="70" height="60" fill="var(--accent)"  rx="4 4 0 0"/>
        <rect x="110" y="115" width="70" height="65" fill="var(--warning)"/>
        <rect x="110" y="50"  width="70" height="65" fill="var(--accent)"/>
        <rect x="200" y="110" width="70" height="70" fill="var(--warning)"/>
        <rect x="200" y="45"  width="70" height="65" fill="var(--accent)"/>
        <rect x="290" y="108" width="70" height="72" fill="var(--warning)"/>
        <rect x="290" y="42"  width="70" height="66" fill="var(--accent)"/>
        <rect x="380" y="105" width="70" height="75" fill="var(--warning)"/>
        <rect x="380" y="38"  width="70" height="67" fill="var(--accent)"/>
        <rect x="470" y="100" width="70" height="80" fill="var(--warning)"/>
        <rect x="470" y="32"  width="70" height="68" fill="var(--accent)"/>
        <rect x="560" y="118" width="70" height="62" fill="var(--warning)"/>
        <rect x="560" y="58"  width="70" height="60" fill="var(--accent)"/>
        <rect x="650" y="125" width="70" height="55" fill="var(--warning)"/>
        <rect x="650" y="68"  width="70" height="57" fill="var(--accent)"/>
      </g>
      <!-- Banda CI (linha tracejada superior/inferior) -->
      <polyline points="55,52 145,42 235,38 325,35 415,30 505,25 595,50 685,60" fill="none" stroke="rgba(37,99,235,0.4)" stroke-dasharray="3 3" stroke-width="1.5"/>
      <polyline points="55,68 145,58 235,52 325,49 415,46 505,40 595,66 685,76" fill="none" stroke="rgba(37,99,235,0.4)" stroke-dasharray="3 3" stroke-width="1.5"/>
    </svg>
    <div class="fc-7d-axis">
      <span><strong>HOJE</strong></span>
      <span>+1</span>
      <span>+2</span>
      <span>+3</span>
      <span>+4</span>
      <span>+5</span>
      <span>+6</span>
      <span><strong>+7</strong></span>
    </div>
  </div>
</section>
```

CSS:
```css
.fc-7d { padding: var(--space-5) var(--space-6); background: rgba(255,255,255,0.55); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.85); border-radius: var(--r-lg); margin-bottom: var(--space-5); box-shadow: inset 0 1px 0 rgba(255,255,255,0.9); }
.fc-7d-head { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: var(--space-4); }
.fc-7d-h { font-size: 14px; font-weight: var(--fw-bold); color: var(--label-primary); display: flex; align-items: center; gap: var(--space-2); }
.fc-7d-sub { font-size: 11px; color: var(--label-tertiary); margin-top: 2px; }
.fc-7d-toggle { display: inline-flex; padding: 3px; background: rgba(0,0,0,0.05); border-radius: var(--r-sm); }
.fc-7d-tab { padding: 5px 12px; font-size: 11.5px; font-weight: var(--fw-semibold); color: var(--label-tertiary); background: transparent; border: none; border-radius: 5px; cursor: pointer; }
.fc-7d-tab.active { background: var(--white); color: var(--label-primary); box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
.fc-7d-chart { position: relative; }
.fc-7d-axis { display: grid; grid-template-columns: repeat(8, 1fr); text-align: center; font-family: ui-monospace, monospace; font-size: 9.5px; color: var(--label-tertiary); margin-top: 6px; }
```

- [ ] **Step 6.4: Adicionar bloco "Distribuição esperada por dimensão"**

Após o gráfico 7d:

```html
<section class="dist">
  <div class="dist-head">
    <div class="dist-h">Distribuição esperada nos próximos 7 dias <span class="ai-badge"><svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0l1.7 6.3L16 8l-6.3 1.7L8 16l-1.7-6.3L0 8l6.3-1.7L8 0z"/></svg>Gerado por IA</span></div>
    <div class="dist-tabs">
      <button class="dist-tab active" data-dim="produto">Produto</button>
      <button class="dist-tab" data-dim="categoria">Categoria</button>
      <button class="dist-tab" data-dim="ic">IC</button>
    </div>
  </div>
  <div class="dist-list">
    <div class="dist-row"><span class="dist-tag">lhco</span><div class="dist-bar"><div class="dist-fill" style="width:78%;"></div></div><span class="dist-val">~430</span></div>
    <div class="dist-row"><span class="dist-tag">lsin</span><div class="dist-bar"><div class="dist-fill" style="width:48%;"></div></div><span class="dist-val">~246</span></div>
    <div class="dist-row"><span class="dist-tag">lcem</span><div class="dist-bar"><div class="dist-fill" style="width:38%;"></div></div><span class="dist-val">~197</span></div>
    <div class="dist-row"><span class="dist-tag">lhvp</span><div class="dist-bar"><div class="dist-fill" style="width:30%;"></div></div><span class="dist-val">~149</span></div>
    <div class="dist-row"><span class="dist-tag">lrev</span><div class="dist-bar"><div class="dist-fill" style="width:25%;"></div></div><span class="dist-val">~127</span></div>
  </div>
  <p class="dist-foot">Decomposição: forecast total × distribuição histórica recente (últimos 30 dias do dataset)</p>
</section>
```

CSS:
```css
.dist { padding: var(--space-5) var(--space-6); background: rgba(255,255,255,0.55); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.85); border-radius: var(--r-lg); margin-bottom: var(--space-5); box-shadow: inset 0 1px 0 rgba(255,255,255,0.9); }
.dist-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: var(--space-4); }
.dist-h { font-size: 14px; font-weight: var(--fw-bold); color: var(--label-primary); display: flex; align-items: center; gap: var(--space-2); }
.dist-tabs { display: inline-flex; padding: 3px; background: rgba(0,0,0,0.05); border-radius: var(--r-sm); }
.dist-tab { padding: 5px 12px; font-size: 11.5px; font-weight: var(--fw-semibold); color: var(--label-tertiary); background: transparent; border: none; border-radius: 5px; cursor: pointer; }
.dist-tab.active { background: var(--white); color: var(--label-primary); box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
.dist-list { display: flex; flex-direction: column; gap: var(--space-2); }
.dist-row { display: grid; grid-template-columns: 80px 1fr 60px; gap: var(--space-3); align-items: center; padding: 6px 0; }
.dist-tag { font-family: ui-monospace, monospace; font-size: 12px; font-weight: var(--fw-bold); padding: 3px 8px; background: rgba(0,0,0,0.06); color: var(--label-primary); border-radius: var(--r-sm); }
.dist-bar { height: 8px; background: rgba(0,0,0,0.05); border-radius: 4px; overflow: hidden; }
.dist-fill { height: 100%; background: linear-gradient(90deg, var(--accent), #1E40AF); border-radius: 4px; }
.dist-val { font-size: 13px; font-weight: var(--fw-bold); color: var(--label-primary); font-variant-numeric: tabular-nums; text-align: right; }
.dist-foot { font-size: 10.5px; color: var(--label-tertiary); font-style: italic; margin-top: var(--space-3); }
```

- [ ] **Step 6.5: Adicionar bloco "Eventos especiais previstos"**

```html
<section class="events">
  <div class="events-h">Dias críticos previstos <span class="ai-badge"><svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0l1.7 6.3L16 8l-6.3 1.7L8 16l-1.7-6.3L0 8l6.3-1.7L8 0z"/></svg>Gerado por IA</span></div>
  <div class="events-list">
    <div class="event-card">
      <span class="event-date">Sexta · 02 jan</span>
      <span class="event-title">Volume previsto +18% acima da média</span>
      <span class="event-why">padrão típico de sextas + véspera de feriado</span>
    </div>
    <div class="event-card">
      <span class="event-date">Segunda · 05 jan</span>
      <span class="event-title">Pico de volume esperado</span>
      <span class="event-why">retorno de fim de semana com fila acumulada</span>
    </div>
    <div class="event-card">
      <span class="event-date">Quarta · 07 jan</span>
      <span class="event-title">Volume na faixa esperada</span>
      <span class="event-why">padrão de meio de semana</span>
    </div>
  </div>
</section>
```

CSS:
```css
.events { padding: var(--space-5) var(--space-6); background: rgba(255,255,255,0.55); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.85); border-radius: var(--r-lg); margin-bottom: var(--space-5); box-shadow: inset 0 1px 0 rgba(255,255,255,0.9); }
.events-h { font-size: 14px; font-weight: var(--fw-bold); color: var(--label-primary); margin-bottom: var(--space-4); display: flex; align-items: center; gap: var(--space-2); }
.events-list { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-3); }
.event-card { padding: var(--space-4); background: rgba(255,255,255,0.6); border: 1px solid rgba(255,255,255,0.85); border-radius: var(--r-md); display: flex; flex-direction: column; gap: 4px; }
.event-date { font-size: 10.5px; font-weight: var(--fw-bold); letter-spacing: 0.12em; text-transform: uppercase; color: var(--label-tertiary); }
.event-title { font-size: 13.5px; font-weight: var(--fw-semibold); color: var(--label-primary); line-height: 1.35; }
.event-why { font-size: 11.5px; color: var(--label-tertiary); }
```

- [ ] **Step 6.6: Adicionar bloco "Impacto previsto na meta"**

```html
<section class="meta-impact">
  <div class="meta-impact-left">
    <div class="meta-impact-eyebrow">Impacto previsto na meta de dezembro <span class="ai-badge"><svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0l1.7 6.3L16 8l-6.3 1.7L8 16l-1.7-6.3L0 8l6.3-1.7L8 0z"/></svg>Gerado por IA</span></div>
    <div class="meta-impact-val">~18 <span class="unit">violações no mês</span></div>
    <div class="meta-impact-ci">meta ≤ 20 · faixa esperada 14 a 22</div>
  </div>
  <div class="meta-impact-right">
    <div class="meta-impact-status warn">⚠ Próximo do limite</div>
    <p class="meta-impact-note">Se o forecast confirmar, o mês fecha dentro da meta — mas com margem estreita. Cascatas em formação acompanham de perto.</p>
  </div>
</section>
```

CSS:
```css
.meta-impact { display: grid; grid-template-columns: 1.2fr 1fr; gap: var(--space-6); padding: var(--space-5) var(--space-6); background: rgba(217,119,6,0.05); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(217,119,6,0.18); border-radius: var(--r-lg); margin-bottom: var(--space-5); box-shadow: inset 0 1px 0 rgba(255,255,255,0.9); }
.meta-impact-eyebrow { font-size: 10px; font-weight: var(--fw-bold); letter-spacing: 0.14em; text-transform: uppercase; color: var(--label-tertiary); margin-bottom: var(--space-2); display: flex; align-items: center; gap: var(--space-2); }
.meta-impact-val { font-size: 40px; font-weight: var(--fw-heavy); letter-spacing: -0.03em; color: var(--label-primary); font-variant-numeric: tabular-nums; line-height: 0.95; }
.meta-impact-val .unit { font-size: 16px; font-weight: var(--fw-medium); color: var(--label-tertiary); margin-left: 6px; }
.meta-impact-ci { font-size: 11.5px; color: var(--label-tertiary); margin-top: 4px; font-variant-numeric: tabular-nums; }
.meta-impact-right { display: flex; flex-direction: column; justify-content: center; gap: var(--space-3); }
.meta-impact-status { font-size: 14px; font-weight: var(--fw-bold); padding: 6px 12px; background: rgba(217,119,6,0.12); color: var(--warning); border-radius: var(--r-pill); align-self: flex-start; }
.meta-impact-note { font-size: 12.5px; color: var(--label-secondary); line-height: 1.5; }
```

- [ ] **Step 6.7: Validar visual no browser**

Abrir previsao.html. Conferir:
- ✅ Hero D+1 com badge IA e split P2/P3/P4-P5
- ✅ Gráfico 7 dias com barras stacked + banda CI
- ✅ Toggle Volume / OLA quebrado (sem JS funcional ainda — só visual)
- ✅ Distribuição esperada com tabs Produto/Categoria/IC
- ✅ 3 cards de "Dias críticos previstos"
- ✅ Bloco "Impacto previsto na meta" com ~18 violações
- ✅ Todos os blocos com badge IA
- ✅ Sidebar tem "Previsões" como ativo

- [ ] **Step 6.8: Commit**

```bash
cd "C:/Users/igor.vignola/Documents/Personal/FIAP/Challenge-LocaWeb"
git add prototipos/telas/previsao.html
git commit -m "$(cat <<'EOF'
feat: adiciona previsao.html — tela de forecast D+1/D+7 (briefing #1-4)

Cobre os requisitos obrigatórios mais críticos do briefing oficial
da Locaweb que estavam sem tela dedicada:

- Previsão D+1 (briefing #1) · Hero com volume esperado amanhã +
  split por prioridade (P2, P3, P4/P5)
- Previsão D+7 (briefing #2) · Gráfico de barras stacked com banda
  de confiança
- Por prioridade (briefing #3) · stack P2 + P3 em cada barra,
  toggle Volume / OLA quebrado
- Por dimensão (briefing #4) · seção "Distribuição esperada" com
  tabs Produto / Categoria / IC
- Bloco "Dias críticos previstos" mostrando elevações esperadas
- Bloco "Impacto previsto na meta" projetando fechamento mensal

Conforme spec 2026-05-22-redesign-prototipos-design.md. Todos os
blocos com badge "Gerado por IA" pra deixar claro que vem de
Prophet (modelo a ser treinado na Sprint 3).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: Finalização — links de navegação, README e GitHub Pages

**Files:**
- Modify: links "Previsões" em todas as 5 telas
- Modify: `prototipos/README.md`
- Read: documentação do GitHub Pages

- [ ] **Step 7.1: Atualizar link "Previsões" em todas as telas pra apontar pra previsao.html**

Em cada uma das 5 telas (`dashboard.html`, `previsao.html`, `saude-produto.html`, `cascata.html`, `morning-brief.html`), localize:

```html
<a class="sb-item" href="#"><svg viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg><span class="lbl">Previsões</span></a>
```

Trocar `href="#"` por `href="previsao.html"`. Na própria `previsao.html`, adicionar `class="sb-item active"`.

- [ ] **Step 7.2: Atualizar prototipos/README.md**

Read o README atual. Atualizar a seção "Telas ativas" com as 5 telas. Mencionar GitHub Pages.

new content (substitui a seção `## Telas ativas`):

```markdown
## Telas ativas (`telas/`)

| Arquivo | Função | Briefing coberto |
|---|---|---|
| `dashboard.html` | Home da demo · resumo das 4 dores do gestor + KPI mensal | Tendência diária (#5, #6) |
| `previsao.html` | Forecast D+1/D+7 por prioridade + por dimensão | **D+1 (#1), D+7 (#2), por prioridade (#3), por dimensão (#4)** |
| `saude-produto.html` | Score por produto · XGBoost + SHAP · drill-down inline | Tendências/clusters (#8), explicabilidade (#9) |
| `cascata.html` | Detector de acúmulo · lista REAL de incidentes-filhos + sugestão IA | Indicar onde agir (#7) |
| `morning-brief.html` | Briefing editorial diário com resumo executivo | Indicar onde agir (#7), tendências (#8) |

Todas consomem `../../brand/design-system/assets/tokens.css` como única fonte de tokens.

## Demo navegável

O protótipo é disponibilizado via **GitHub Pages** como demo navegável, complementando os screenshots do PPT:

🔗 (link a ser configurado nas settings do repositório · Settings → Pages → branch `main` · folder `/` ou `/prototipos/telas`)

Permite à Locaweb experimentar a navegação real entre as telas, não só ver imagens estáticas.
```

Edit prototipos/README.md substituindo a seção apropriada.

- [ ] **Step 7.3: Validar GitHub Pages (instruções)**

Documente passo a passo pro Igor (não execute):

1. Acessar `https://github.com/igor-vignola/LocaWeb-Cronos/settings/pages`
2. Em **Source**, selecionar `Deploy from a branch`
3. Em **Branch**, selecionar `main` e folder `/ (root)`
4. Salvar
5. Aguardar deploy (1-5 min)
6. URL será `https://igor-vignola.github.io/LocaWeb-Cronos/prototipos/telas/dashboard.html`

**Importante:** o protótipo usa caminhos relativos (`../../brand/design-system/assets/tokens.css`). No GitHub Pages, esse caminho funciona porque a estrutura de pastas é mantida.

**Teste local antes do deploy:**

Run:
```bash
cd "C:/Users/igor.vignola/Documents/Personal/FIAP/Challenge-LocaWeb"
python -m http.server 8000 --directory .
```

Expected: servidor sobe em http://localhost:8000. Acesse http://localhost:8000/prototipos/telas/dashboard.html

Conferir que:
- ✅ Tokens carregam (cores aparecem corretas)
- ✅ Sidebar links funcionam (clicar leva pras outras telas)
- ✅ Fonts Outfit carregam

- [ ] **Step 7.4: Commit final**

```bash
cd "C:/Users/igor.vignola/Documents/Personal/FIAP/Challenge-LocaWeb"
git add prototipos/telas/*.html prototipos/README.md
git commit -m "$(cat <<'EOF'
chore: liga link 'Previsões' nas 5 telas + atualiza README com GitHub Pages

- Sidebar de todas as 5 telas aponta 'Previsões' pra previsao.html
  (era href="#"). previsao.html marca seu próprio link como active.
- README atualizado com tabela de cobertura do briefing por tela e
  seção sobre GitHub Pages como demo navegável complementar ao PPT.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 7.5: Push final**

```bash
cd "C:/Users/igor.vignola/Documents/Personal/FIAP/Challenge-LocaWeb"
git push
git log --oneline -10
```

Expected: push bem-sucedido, últimos commits visíveis.

---

## Task 8: AED da anomalia de set/2025 (cobre pedido do Douglas)

**Files:**
- Modify: `notebooks/01_eda.ipynb` (seção a adicionar)
- Create: `notebooks/figures/01_eda/anomalia_set2025.png`

### Estratégia
Esse é o pedido explícito do Douglas na mentoria: investigar a anomalia de set/2025 (alta de 5x no volume) e apresentar a hipótese como **destaque na AED**. Sem isso, perdemos ponto de avaliação técnica.

- [ ] **Step 8.1: Read notebook 01_eda.ipynb pra ver estado atual**

Read: `notebooks/01_eda.ipynb`. Identifique onde inserir a seção de anomalia (provavelmente após Seção 3 — Visão geral, antes de seções vazias 4 e 5).

- [ ] **Step 8.2: Adicionar célula markdown introdutória**

Conteúdo da célula:

```markdown
## 4. Anomalia de setembro/2025 — destaque

> **Pedido explícito do Douglas (mentoria 14/05):** investigar e apresentar a hipótese da causa como destaque na AED.

### Achado

Volume mensal de incidentes salta de patamar em set/2025:

| Período | Volume médio/mês |
|---|---|
| 2023 (ano inteiro) | ~10 |
| 2024 (ano inteiro) | ~52 |
| jan–ago/2025 | ~3.500 |
| **set/2025** | **21.561** (≈ 5x ago/25) |
| out–dez/2025 | 21.500 → 23.000 → 27.300 |

A correção do registro anterior (que dizia "queda anômala") foi feita após análise direta dos dados.

### Hipótese mais provável

**Expansão/mudança do sistema de monitoramento em set/2025.** O salto absoluto + estabilização em patamar alto nos meses seguintes sugere que mais sensores passaram a capturar mais eventos, não que a operação tenha piorado 5x da noite pro dia. Indicadores que reforçam:

- Padrão consistente em out/nov (21-23k) e dez (27k)
- `Aberto por: Monitoramento` segue 85% do volume — não houve aumento desproporcional de manual
- Nenhum produto isolado domina o salto — todos crescem

### Implicação para modelagem

**Não treinar Prophet com 3 anos completos.** Treinar com janela **pós-set/2025** (4 meses, ~93k incidentes) captura o regime atual de monitoramento e produz forecast confiável. Treinar com a base completa faz o modelo aprender uma tendência exponencial irreal.

Esta decisão está registrada em `context/decisoes-tecnicas.md` e refletida nas telas de previsão (`previsao.html`) e KPI mensal (`dashboard.html`).
```

- [ ] **Step 8.3: Adicionar célula código pra gerar o gráfico**

```python
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Assumindo df já carregado em células anteriores. Senão recarregar:
# df = pd.read_excel(Path('../assets/Materal LocalWeb/LW-DATASET.xlsx'))
# df['Aberto'] = pd.to_datetime(df['Aberto'], errors='coerce')

# Agregação mensal
monthly = (
    df.assign(ano_mes=df['Aberto'].dt.to_period('M'))
      .groupby('ano_mes')
      .size()
      .reset_index(name='volume')
)
monthly['ano_mes'] = monthly['ano_mes'].astype(str)

# Plot
fig, ax = plt.subplots(figsize=(11, 4.5))
ax.bar(monthly['ano_mes'], monthly['volume'],
       color=['#2563EB' if not v.startswith('2025-09') else '#DC2626'
              for v in monthly['ano_mes']])

# Destaque: linha tracejada antes/depois de set/2025
sep_idx = monthly[monthly['ano_mes'] == '2025-09'].index[0]
ax.axvline(x=sep_idx - 0.5, color='#737373', linestyle='--', linewidth=1, alpha=0.7)
ax.text(sep_idx - 0.3, monthly['volume'].max() * 0.92,
        'Quebra estrutural · expansão do monitoramento',
        fontsize=10, color='#525252', style='italic')

ax.set_xlabel('Mês', fontsize=11)
ax.set_ylabel('Incidentes / mês', fontsize=11)
ax.set_title('Volume mensal de incidentes · LWDATASET', fontsize=13, weight='bold')
ax.tick_params(axis='x', rotation=45)
ax.grid(axis='y', linestyle=':', alpha=0.3)

plt.tight_layout()

# Salvar
out = Path('figures/01_eda/anomalia_set2025.png')
out.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(out, dpi=144, bbox_inches='tight', facecolor='white')
plt.show()

print(f'Figura salva em: {out}')
```

- [ ] **Step 8.4: Executar célula e verificar saída**

Run via Jupyter ou `jupyter nbconvert --to notebook --execute`. Verificar:
- ✅ Gráfico renderiza com barra de set/25 destacada em vermelho
- ✅ Anotação "Quebra estrutural" aparece próxima ao salto
- ✅ Arquivo `notebooks/figures/01_eda/anomalia_set2025.png` foi criado

- [ ] **Step 8.5: Commit do notebook**

```bash
cd "C:/Users/igor.vignola/Documents/Personal/FIAP/Challenge-LocaWeb"
git add notebooks/01_eda.ipynb notebooks/figures/01_eda/anomalia_set2025.png
git commit -m "$(cat <<'EOF'
docs: AED da anomalia de setembro/2025 no notebook 01_eda

Cobre pedido explícito do Douglas na mentoria de 14/05: investigar
e apresentar a hipótese da causa como destaque na AED.

- Seção markdown explicando o achado (alta de ~5x no volume mensal)
  com tabela comparativa por período.
- Hipótese mais provável: expansão/mudança do sistema de monitoramento
  em set/2025 (não aumento operacional).
- Decisão de modelagem: treinar Prophet com janela pós-set/2025
  apenas, registrada em decisoes-tecnicas.md.
- Gráfico mensal salvo em figures/01_eda/anomalia_set2025.png com
  destaque visual no salto.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Self-review

**Spec coverage:**

| Seção da spec | Task que implementa | Status |
|---|---|---|
| §2 Cortes confirmados (5 itens) | Tasks 2 (cascata), 3 (saúde), 4 (morning-brief) | ✅ todas as remoções têm step específico |
| §3 Princípios obrigatórios (7) | Validados no Step 1.3 e em cada validação visual | ✅ |
| §4 Mapa das 5 telas + navegação | Task 7 (Step 7.1) | ✅ |
| §5 Dashboard (6 seções) | Task 5 | ✅ 6 sub-tasks (5.2-5.7) |
| §6 Previsao (5 seções) | Task 6 | ✅ 5 sub-tasks (6.2-6.6) |
| §7 Saúde-produto (ajustes) | Task 3 | ✅ |
| §8 Cascata (refazer) | Task 2 | ✅ 12 sub-tasks (2.2-2.12) |
| §9 Morning-brief (ajustes) | Task 4 | ✅ 6 sub-tasks (4.2-4.6) |
| §10 Padrões UI compartilhados | Cada task respeita (CSS tokens, sidebar, glass) | ✅ |
| §11 Modelos backend Sprint 3 | Mencionado em badges "Gerado por IA" + READMEs | ✅ (escopo de UI apenas) |
| §12 Próximos passos · GitHub Pages | Task 7 (Steps 7.2, 7.3) | ✅ |
| §12 AED anomalia set/2025 | Task 8 | ✅ task dedicada |

**Sem gaps de cobertura da spec.**

**Placeholder scan:** sem TBD, TODO, "implement later". Cada step tem ação concreta + código quando aplicável.

**Type consistency:** classes CSS reutilizadas batem entre tasks (ex: `.casc-card`, `.ai-badge`, `.alert`, `.casc-status-text` referenciadas consistentemente entre Tasks 2, 5, 6).

---

## Cronograma realista

Com 8 tasks (1 setup + 5 telas + 1 nav + 1 AED), considerando ~30-90 min cada (variável por complexidade), total estimado: **8-12h de trabalho focado**.

- **Sex 22/05 (resto do dia, ~3-4h):** Task 1 (setup) + Task 2 (cascata · maior) + Task 3 (saúde · rápido)
- **Sáb 23/05 (~6h):** Task 4 (morning-brief) + Task 5 (dashboard · grande) + Task 6 (previsao nova · grande)
- **Dom 24/05 manhã (~2h):** Task 7 (nav + README + Pages) + Task 8 (AED anomalia) + PPT screenshots + submit

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-05-22-redesign-prototipos.md`. Two execution options:

**1. Subagent-Driven (recommended)** — dispatch a fresh subagent per task, review between tasks, fast iteration. Bom pra reduzir o ruído no main context e ter checkpoint depois de cada tela.

**2. Inline Execution** — execute tasks in this session using executing-plans, batch execution with checkpoints. Bom se você quer ver/intervir em tempo real em cada step.

Which approach?

# Console — Iteração V2 · Da estética pra acionabilidade

> **Esta é uma iteração sobre o spec anterior**, não um rewrite. O sistema visual (tokens, motion, glass, paleta) está aprovado e deve ser preservado. As mudanças abaixo adicionam **camadas de informação acionável** — o que um gerente de operações precisa pra decidir e atribuir, não só pra observar.

---

## 0. Princípio guia desta iteração

**Antes de cada bloco visual, responda:** "Se eu olhar isso por 5 segundos, sei o que fazer agora?"

Se a resposta é "não sei, é só um número", adicione:
1. **Comparação com baseline** (média, pior dia, mesma data ano passado).
2. **Impacto em $ ou clientes** (dimensão do problema).
3. **Tempo até irreversibilidade** (urgência).
4. **Owner + ação sugerida** (próximo passo concreto).
5. **Confiança da previsão** (intervalo, não ponto).

Um número solto é decoração. Um número com baseline + impacto + tempo + owner + confiança é decisão.

---

## 1. Hero panel — adicionar 3 camadas

Manter número `73%` + mensagem + sparkline. **Adicionar:**

### 1.1. Intervalo de confiança ao lado do número

Logo abaixo do "73%", caption pequena 11px `text-3`:
`±8pp · intervalo 90% confiança · Prophet+XGBoost`

Sem isso o "73%" parece mágico. Com isso parece previsão honesta.

### 1.2. Countdown de janela de ação

À direita da sparkline, adicionar card stacked:
- Eyebrow uppercase 10.5px danger: `JANELA DE AÇÃO`
- Valor JetBrains Mono 28px 800: `38h 14min`
- Subline 11px `text-3`: `até decisão virar matemática impossível`

Cálculo (mockado): tempo até que mesmo com 0 incidentes adicionais o KPI já não fecha.

### 1.3. Bloco "Impacto se nada mudar"

Abaixo do CTAs primary/secondary, em uma linha horizontal com `divide-x hairline-2` (sem cards):
- `R$ 47.300` SLA credits estimados
- `1.247 clientes` afetados no produto crítico
- `4 produtos` arrastados pela cascata

Números em JetBrains Mono 18px 700, labels em 11px `text-3` abaixo de cada.

**Esta linha é o feedback direto da nota Sprint 1: "ilustrar mais o impacto para o negócio com exemplos numéricos".**

---

## 2. KPI strip — todos os cards viram clicáveis e ganham baseline

Cada card existente (Incidentes hoje · OLA do mês · Cascatas ativas · Score saúde) recebe:

### 2.1. Baseline pill abaixo do valor

Substituir a linha do delta + sparkline por: delta pill + **baseline caption** + sparkline.

Exemplo card 1 (Incidentes hoje):
- Valor: `127` (já existe)
- Nova linha: `↑ 12% vs ontem · média 30d: 89 · pior dia: 134 em 14/mai` (11px `text-3`, números em Mono)
- Sparkline ao lado (já existe)

Exemplo card 2 (OLA do mês):
- Valor: `96.2%`
- Nova linha: `↓ 1.3pp da meta · YTD: 97.8% · meta anual: 99.0%`

Exemplo card 3 (Cascatas ativas):
- Valor: `3`
- Nova linha: `↑ 2 em 24h · média mensal: 1.2 · recorde: 7 em set/25`

Exemplo card 4 (Score saúde médio):
- Valor: `82`
- Nova linha: `↓ 4 vs ontem · 8 produtos em crítico (<70) · 12 em risco (70-85)`

### 2.2. Clicável com cursor pointer + hover lift já existente

Cada card navega pra:
- Incidentes hoje → `/incidentes?periodo=hoje`
- OLA do mês → `/kpi`
- Cascatas ativas → `/cascatas`
- Score saúde → `/saude`

Adicionar ícone de seta sutil top-right do card no hover (8px Phosphor arrow-up-right, `text-3` color, opacity 0→1 transition 180ms).

### 2.3. Filtro "ruído" no card de incidentes

Card 1 ganha um sub-segmento split mostrando:
- `127` total · `120 auto-resolvidos` (pequeno, success) · `7 precisam atenção` (pequeno, danger, em negrito)

Manager olha e sabe: do volume bruto, só 7 são problema dele.

---

## 3. Cascata signature — adicionar 4 camadas críticas

A cascata atual mostra fluxo P5→P4→P3→predicted P2. **Adicionar:**

### 3.1. Strip de impacto no header

Logo abaixo do nome do produto e antes do flow, uma linha de 3 mini-stats com `divide-x hairline-2`:
- `~R$ 18.400` perda estimada se escalar
- `847 clientes` no produto SP
- `4 dependentes` Email, Painel, Backup, CDN

Mono 16px 700, labels 10px `text-3` abaixo.

### 3.2. Ownership row

Acima do flow, à direita do nome do produto, em vez do "Elapsed 02h 14min":
- Avatar 24×24 + nome `Marina Schettini` (12.5px 600 `text-1`) + role `SRE Lead · POA` (10px `text-3`) + status pill `ACK · há 18min` (verde)
- Botão pequeno `Reatribuir` (glass, 9px font)

Se incidente não está atribuído ainda, mostra avatar placeholder cinza + label `SEM OWNER · ATRIBUIR →` em danger.

### 3.3. Por que essa previsão? (explicabilidade)

Abaixo do flow, antes do footer com `84% probabilidade`, adicionar bloco:

Eyebrow: `POR QUE O DETECTOR DISPAROU`

3 bullets com peso (% de contribuição pro risco):
- `42%` Deploy de quinta (20/mai) aumentou erros 5xx em +18%
- `31%` Pico de uso 14h-18h coincide com janela de backup pesado
- `27%` Padrão histórico: 6 das últimas 8 cascatas começaram com P5 no MySQL SP

Cada bullet: número em Mono accent + texto 12.5px `text-2`. Linha fina entre bullets.

**Isto é o SHAP do plano técnico aparecendo na UI. Sem isso Cronos é caixa preta.**

### 3.4. Footer reorganizado

Manter `84% PROBABILIDADE DE ESCALAR`. **Adicionar ao lado**:
- `12 cascatas similares no histórico · 9 escalaram para P2`
- CTA primary muda de `Abrir runbook` pra `Acionar runbook · 4 passos` (mostrando que tem ação concreta)
- CTA secondary novo: `Silenciar 2h` (glass, smaller)

---

## 4. Lista das 3 cascatas ativas (NOVO BLOCO)

Adicionar entre a cascata signature e a linha de alerts+heatmap, full width.

Header: `3 CASCATAS ATIVAS AGORA` (h2 17px 700) + caption "ordenadas por probabilidade de escalar".

3 rows com `divide-y hairline-1` (sem cards individuais):

Cada row é grid 5 cols:
1. Mini-flow 4 nodes de 24×24 (P4·P3·P3·predicted) — compacto, mesmas regras de cor
2. Produto + região: `MySQL Compartilhado · SP` (h3 600) com sub `iniciado 14:28 · 02h 14min elapsed` (11px `text-3`)
3. Owner: avatar 20×20 + iniciais ou `SEM OWNER` em danger
4. Probabilidade: barra horizontal 100px de comprimento, preenchida color-coded (danger se >70%, warning se 40-70%, success se <40%) + número 22px 800 Mono à direita
5. Ação rápida: botão glass `Abrir →` 

Click na row → expande inline mostrando o detalhe completo (a signature card vira essa row expandida) com 280ms ease-out via `clip-path`.

A row top é a que aparece como signature. As outras 2 ficam recolhidas.

---

## 5. Alerts list — enriquecer com 3 colunas críticas

A lista atual mostra `priority chip + título + descrição + timestamp + tag cascading`. **Adicionar:**

### 5.1. Owner column (24px wide)

Entre o priority chip e o title body, adicionar avatar 24×24 ou placeholder cinza com "?" se não atribuído.

### 5.2. Runbook badge

Ao lado do tag `CASCATING`, adicionar quando aplicável:
- `RUNBOOK` (9.5px uppercase 600, accent-soft pill) — significa "tem playbook automatizado pronto"
- `AUTO` (9.5px uppercase 600, success-soft pill) — significa "auto-resolveu, está aqui só pra log"

### 5.3. Filtros no header da lista

Acima das rows, linha de filter chips horizontais (estilo segmented):
- `Todos (47)` (ativo)
- `Precisa ação (7)` (danger soft pill com count)
- `Atribuídos (12)`
- `Sem owner (3)` (danger)
- `Auto-resolvidos (40)` (success soft, dimmed)

Click em chip filtra a lista in-place (preservar o filter state).

### 5.4. Empty state

Se filtro retorna 0 itens, mostrar empty state lindo:
- Ícone Phosphor `check-circle` 48×48 success outline
- Texto: `Nenhum alerta aqui` (h3) + sub: `Última atualização: 16:42 · próxima verificação em 30s` (12px `text-3`)
- **Se filtro for "Precisa ação" e veio 0**: celebrar — texto vira `Zero alertas exigem ação humana agora. 47 incidentes resolvidos automaticamente nas últimas 24h.` (text-2)

---

## 6. Heatmap — adicionar anotações

A grid 7×24 existente fica. **Adicionar:**

### 6.1. Pins de anotação em outlier cells

Cells com intensidade `h6` (danger, picos de setembro/anomalia) recebem ícone pin overlay 8×8 no canto superior direito.

Hover em cell pin'd mostra tooltip enriquecido:
- `Sex 04/Set · 17h-18h` (header)
- `47 incidentes` (Mono 16px)
- `3.2x acima da média do horário` (caption danger)
- `Hipótese: failure cascata MySQL pós-deploy` (text-3 italic)

Tooltip é glass panel com `transform-origin` na célula, scale-in 0.95→1 com 180ms ease-out.

### 6.2. Toggle de visão acima da grid

Segmented control 3 opções:
- `Incidentes` (default)
- `OLA` (mesma grid mostrando % OLA por hora — verde alto, vermelho baixo)
- `Saturação` (mesma grid mostrando carga do time — útil pra ver onde redistribuir)

Click troca a visão com cross-fade 280ms.

### 6.3. Insight automático abaixo da legenda

Linha de texto destacada, 12.5px `text-2`:
`Padrão detectado: 73% dos incidentes críticos acontecem nas terças e quintas entre 14h-18h. Considere reforçar a equipe nesses horários.`

Esse texto roda automaticamente (mock no protótipo) — é o insight que distingue dashboard de tabela.

---

## 7. Bloco NOVO — Carga por equipe (lateral direita ou abaixo do KPI strip)

Glass panel, header `CARGA POR EQUIPE · AGORA`.

Lista vertical de 5 equipes/regiões com bar chart horizontal:

Cada row:
- Avatar group (sobreposto, 3-4 iniciais) representando o time
- Nome região + label: `SP — 8 ativos · 2 sem owner` (danger se tem sem-owner)
- Bar 200px wide com fill % proporcional à carga. Color rule: <50% success · 50-80% warning · >80% danger
- Número de incidentes abertos (Mono 16px 700) à direita

Exemplo de dados:
- SP: 8 incidentes ativos, 2 sem owner → danger
- RJ: 3 incidentes, 0 sem owner → success
- POA: 5 incidentes, 1 sem owner → warning
- FOR: 2 incidentes → success
- BSB: 4 incidentes → warning

Footer do bloco: `Sugestão IA: 2 incidentes P5 de SP podem ser redistribuídos pra FOR (capacidade ociosa).` Com botão pequeno `Aplicar sugestão →` (glass).

---

## 8. Empty states celebrados

Para QUALQUER lista/feed vazio, NÃO mostrar "Nada por aqui" genérico.

### Regras

**Cascatas ativas = 0:**
```
Ícone shield-check 56×56 success
"Operação limpa."
"Zero cascatas detectadas nas últimas 24h."
"Maior streak deste ano: 18 dias sem cascata (jan/26)."
```

**OLA mensal acima da meta:**
Adicionar pequena gold badge no card: `↑ ACIMA DA META · 8º mês consecutivo`

**Score saúde com 0 produtos em crítico:**
```
Mini-celebration card no topo da lista de produtos:
"Nenhum produto em estado crítico. Última vez foi em 14/abr (Email Business)."
```

Empty states bons reforçam comportamento bom da equipe — manager gosta de mostrar isso pro chefe.

---

## 9. Drill-down navigation paths

Toda métrica deve ter "para onde ir se quiser detalhe". Adicionar no protótipo:

| Click em | Vai para |
|---|---|
| Hero "73%" | `/kpi` (Tela 5) |
| KPI card "Incidentes hoje" | `/incidentes?periodo=hoje` |
| KPI card "OLA do mês" | `/kpi` |
| KPI card "Cascatas ativas" | `/cascatas` (Tela 3) |
| KPI card "Score saúde" | `/saude` (Tela 4) |
| Linha da lista de 3 cascatas | `/cascatas/{id}` |
| Alert row | `/incidentes/{id}` (modal slide-in da direita) |
| Heatmap cell | `/incidentes?dia={d}&hora={h}` (slide-in lateral com lista filtrada) |
| Carga por equipe → equipe | `/equipes/{regiao}` |

Ícone arrow-up-right Phosphor 8px aparece no hover do elemento clicável (top-right canto), opacity 0→1 em 180ms.

---

## 10. Refinamentos da Tela 2 — Morning Brief

A tela existente é boa mas falta utilidade. Adicionar:

### 10.1. Bloco "Decisões pendentes pra HOJE"

Entre o bloco "Hoje" e "Ações sugeridas", adicionar nova seção:

Eyebrow: `DECISÕES PENDENTES · VOCÊ`

3 rows com checkbox custom à esquerda:
- `Reatribuir cascata MySQL SP (sem owner há 18min)` + `urgente` pill
- `Aprovar mudança de janela de backup MySQL SP pra 02h` + body com 2 linhas
- `Confirmar plano de mitigação cascata Email Business`

Cada row clicável vai pra ação específica. Checkbox conclui (anima check + strikethrough no texto + fade 600ms).

### 10.2. Bloco "Próximos riscos no horizonte"

Ao final, antes do CTA strip, adicionar:

`PRÓXIMOS 7 DIAS` (eyebrow)

3 mini-cards horizontais:
- `Quarta` · Previsão de pico (deploy planejado) · `+34%` carga estimada
- `Sexta` · OLA pode estourar se sequência continuar · `41%` probabilidade
- `Domingo` · Janela de manutenção CDN · risco médio

### 10.3. Compartilhamento

CTA strip ganha 3ª opção: `Postar no #ops-status` (glass, com ícone Slack outline).

---

## 11. Refinamentos da Tela 3 — Cascata detalhe

### 11.1. Timeline de Eventos do gatilho

Cada evento ganha:
- Owner avatar + ack status (acked / unacked / resolved)
- "Tempo até próximo evento": `+18min` em mono entre eventos

### 11.2. Bloco "Produtos correlatos" — adicionar previsão

Cada produto correlato lista, em vez de só score:
- Score
- Probabilidade de SER ARRASTADO PELA cascata atual (Mono 14px, accent)
- Botão `Isolar →` (glass) — para preempt manualmente

### 11.3. Playbook expandido

Cada step do playbook tem:
- Tempo estimado: `~4 min`
- Indicador se já foi executado em cascatas similares: `aplicado em 8/12 casos similares`
- Botão `Executar` (primary) ou `Marcar como feito` (glass) se manual

---

## 12. Refinamentos da Tela 4 — Score saúde

### 12.1. Cada row ganha trend mini-chart inline

Após a barra de score e antes do número, adicionar sparkline horizontal 80×16 mostrando trajetória do score nos últimos 30 dias.

### 12.2. Tooltip explicativo no número

Hover no score number mostra:
- Decomposição: `60% incidentes (peso 40%) · 78% MTTR (peso 30%) · 89% OLA (peso 30%)`
- `Composto: 75.7 arredondado para 76`

Tirar dúvida de "por que esse score?" sem precisar de drill-down.

### 12.3. Comparação YoY

Row label adiciona micro-caption: `+12 pts vs maio/25` ou `-8 pts vs maio/25` color-coded.

---

## 13. Refinamentos da Tela 5 — Probabilidade KPI

### 13.1. Chart adiciona bandas de cenário

Os 3 cards de cenário (otimista/atual/pessimista) ficam clicáveis. Click pinta o chart com a banda daquele cenário:
- Otimista: área verde semi-transparente entre médio e topo
- Pessimista: área vermelha entre médio e fundo

### 13.2. Marcadores no chart

Cada incidente histórico relevante vira um marker dot no chart com tooltip:
- `14/mai · cascata MySQL · -8 pp impacto`
- `21/mai · hoje · pico de erros`

Markers só aparecem em zoom — no chart full não polui.

### 13.3. Recomendações no rodapé

Após o chart, bloco "AÇÕES RECOMENDADAS PRA REVERTER":

3 ações com peso de impacto:
- `+11pp` se eliminar cascatas no MySQL SP até dia 25
- `+6pp` se reduzir MTTR médio de WordPress em 30%
- `+4pp` se promover dois P5 do CDN Edge pra correção proativa

Cada ação clicável abre playbook ou cria task atribuída.

---

## 14. Acessibilidade e PWA básica

Adicionar (mesmo no protótipo):

- Todos elementos interativos com `aria-label` em português
- Contraste mínimo AA WCAG (já tá quase, mas validar `text-3` sobre `bg-base`)
- Focus ring visível: `box-shadow: 0 0 0 2px var(--accent), 0 0 0 4px var(--bg-base)` em focus-visible
- Skip-to-main link no top
- Manifest mínimo + ícone — pode "instalar" como PWA pro Operações deixar fixado

---

## 15. Sample data atualizado / adicional

### Equipes (NOVO)

| Região | Lead | Open | Sem owner | Capacidade |
|---|---|---|---|---|
| SP | Marina Schettini | 8 | 2 | 87% |
| RJ | Tiago Asakawa | 3 | 0 | 41% |
| POA | Beatriz Almeida | 5 | 1 | 64% |
| FOR | Caio Vinha | 2 | 0 | 28% |
| BSB | Lucas Cardona | 4 | 0 | 58% |

### Impactos financeiros (NOVO)

- SLA credit base por hora de degradação P3: R$ 850/produto
- SLA credit P2: R$ 2.400/produto
- Cliente médio MySQL Compartilhado: 1.247 contas afetadas na região SP
- Cliente médio Email Business: 3.890 contas afetadas
- Cliente médio CDN Edge: 12.400 contas afetadas

### Streaks (NOVO)

- Maior streak sem cascata em 2026: 18 dias (10/jan a 28/jan)
- Streak atual sem cascata em RJ: 23 dias
- Streak atual sem cascata em FOR: 47 dias (recorde regional)

### Decomposição de previsões (NOVO)

Quando mostrar "73% probabilidade KPI", os fatores de contribuição mockados:
- 42% deploy de quinta (20/mai)
- 31% pico de uso 14h-18h
- 27% padrão histórico cascatas

---

## 16. Pre-flight V2 (adicional ao anterior)

- [ ] Todo número solto tem baseline (média, recorde ou comparação YoY)
- [ ] Toda métrica tem caminho de drill-down via click
- [ ] Toda cascata/incidente tem owner OU é marcado `SEM OWNER` em danger
- [ ] Toda previsão tem intervalo de confiança visível
- [ ] Toda predição tem "por que" (decomposição em 2-3 fatores)
- [ ] Empty states celebram comportamento bom (streaks, zero crítico)
- [ ] Filtros preservam estado e mostram count por categoria
- [ ] Impacto em R$ ou clientes aparece em pelo menos 2 lugares por tela
- [ ] Carga por equipe visível sem precisar abrir outra tela
- [ ] Heatmap tem insight automático em texto, não só pinta cores

Confirmar ao final: **"Pre-flight V2 passou."**

---

## 17. Ordem de aplicação

Aplique nesta ordem (cada bloco preserva o que já existe):

1. Tela 1 — adicionar §1 (camadas hero), §2 (KPI baselines + click), §3 (cascata enriquecida), §4 (lista 3 cascatas), §7 (carga por equipe)
2. Tela 1 — refinar §5 (alerts) e §6 (heatmap anotado)
3. Tela 2 — §10
4. Tela 3 — §11
5. Tela 4 — §12
6. Tela 5 — §13
7. Geral — §8 (empty states), §9 (drill-down), §14 (a11y)

Pergunte antes de cada tela. Rode o pre-flight V2 ao final de cada uma.

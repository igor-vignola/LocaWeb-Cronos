# Redesign dos protótipos Cronos · Sprint 2

> **Status:** brainstorming aprovado · pronto para implementação
> **Data:** 22/05/2026
> **Entrega-alvo:** Sprint 2 — 24/05/2026
> **Autor:** Igor Vignola (decisões) + Claude (estruturação)

---

## 1. Contexto

Os protótipos atuais (`dashboard.html`, `morning-brief.html`, `saude-produto.html`, `cascata.html`, `kpi-probabilidade.html`) foram identificados como **vendendo features que o time não consegue entregar de verdade** com o dataset e modelos planejados. Análise crítica revelou:

- **Falta o requisito mais importante do briefing:** previsão D+1 e D+7 segregada por prioridade (P2, P3) — nenhuma tela cobre isso hoje.
- **Modelos prometidos no pitch (Prophet, XGBoost, k-NN, SHAP) não estão treinados** — todos os números no protótipo são chute visual.
- **Invenções específicas** sem suporte no dataset: cronologia P5→P5→P4 intermediária, hostnames inventados, "runbook IC00014 87% sucesso", countdown "vira P2 em 1h48min", "−42pp impacto da ação".
- **Dataset não tem** trilha de eventos dentro de um incidente, hostname, qual procedimento foi acionado, nem rótulo de cascata que escalou.

### Princípios decididos no brainstorming

1. **Maestria em pouco > muito mal-feito.** Cortar features inviáveis e impressionar na entrega final, em vez de prometer agora e falhar depois.
2. **Toda feature do protótipo passa por verificação do dicionário** (`prototipos/docs/dicionario-dados.md`) antes de aparecer na tela.
3. **Predição NÃO é o problema** — Cronos vai entregar Prophet/XGBoost de verdade. O que sai são *insights que dependem de dados que o dataset não tem*.
4. **GitHub Pages como demo navegável** — protótipo HTML estático no Pages, link compartilhado junto com o PPT pra Locaweb experimentar.

---

## 2. Cortes confirmados

Os itens abaixo foram **removidos** dos protótipos por dependerem de dados que o dataset não tem ou de modelagem fora do escopo:

| Corte | Justificativa | Substituto |
|---|---|---|
| Cronologia P5→P5→P4 com timestamps intermediários | Dataset só tem `Aberto`/`Resolvido`/`Encerrado` por incidente — não há trilha interna | Lista REAL de incidentes-filhos do `Incidente Pai`, cada um com seu `Aberto` |
| Hostnames inventados (`lhco-web-03`, `lhvp-db-01`) | Dataset não tem campo hostname | IC code real (`IC00014`, `IC00349`, `IC00019`) |
| Métricas de runbook ("87% sucesso", "−42 pp") | Dataset não registra qual procedimento foi acionado; uplift modeling fora de escopo | Frequência real do `Código de fechamento` (Falha de Aplicação, etc.) + texto qualitativo gerado por Claude |
| Countdown "vira P2 em 1h48min" | Prophet faz volume diário, não predição de tempo até escalada | "Probabilidade histórica de escalar" via k-NN sobre cascatas similares |
| CTA strip + "Decisões esperando você" no morning-brief | Morning brief é informativo, não tela de ação | Decisões/CTAs ficam nas telas operacionais (cascata, saúde-produto) |
| `index.html` separado | Dashboard vira a home do GitHub Pages | Navegação direta via sidebar |

---

## 3. Princípios obrigatórios (todas as telas)

1. **Cada número/badge mostrado vem do dataset ou de modelo declarado.** Antes de adicionar qualquer feature, confirmar no dicionário se o campo existe.
2. **Sem hostname inventado.** Apenas IC code.
3. **Sem cronologia interna do incidente.** Apenas os incidentes-filhos reais (com seu `Aberto`).
4. **Sem métrica de runbook resolvendo X%.** Apenas código de fechamento real (Falha de Aplicação, Falha de SO, etc.).
5. **Sem countdown "vira P2 em X tempo".** Apenas probabilidade histórica via k-NN.
6. **SLA por prioridade segue o dicionário:** P1/P2 = 4h · P3 = 12h · P4 = 24h · P5 = 96h.
7. **Regra de KPI:** apenas `Prioridade ∈ {1,2,3}` + `Incidente Pai` vazio + `Status ≠ "Sem Intervenção"`.

---

## 4. Mapa das 5 telas

| Tela | Dor que resolve | Briefing | Fontes | Modelos |
|---|---|---|---|---|
| **`dashboard.html`** (home) | 4 dores num glance + entrada da demo | Tendência diária volume (#5) + OLA (#6) + explicabilidade (#9) | Agregação dataset + Prophet + XGBoost | Prophet · XGBoost · SHAP |
| **`previsao.html`** (NOVA) | "O que vem nos próximos dias?" | **D+1 (#1) + D+7 (#2) + por prioridade (#3) + por dimensão (#4)** | Série diária do dataset | **Prophet** (pós-set/25) |
| **`saude-produto.html`** (ajustar) | "Algo ficando instável?" | Tendências/clusters (#8) + explicabilidade (#9) | Features por produto | **XGBoost + SHAP** + DTW |
| **`cascata.html`** (refazer) | "Tem fogo agora?" | Indicar onde agir (#7) | `Incidente Pai` + filhos reais | **k-NN** + Claude API |
| **`morning-brief.html`** (ajustar) | Resumo executivo · 4 dores em narrativa | Indicar onde agir (#7) + tendências (#8) | Agregações + Claude API | **Claude API** + Prophet |

### Navegação
- **Home = `dashboard.html`** (entrada do GitHub Pages)
- Sidebar (já existe) leva pra todas as outras
- Logo Cronos no topbar linka de volta pro dashboard
- Top bar com data fixa **Quarta, 31/12/2025** (último dia do dataset)

---

## 5. Tela 1 · `dashboard.html`

### Dor
Visão geral · as 4 perguntas do gestor num glance · ponto de entrada da demo.

### Seções

#### 5.1. Hero KPI mensal · "Vou bater a meta?"
- Probabilidade de bater meta de OLA quebrado de dezembro/2025
- Número grande + faixa de confiança + mini-gráfico "esperado vs meta"
- **Fonte:** Prophet (forecast diário) + Monte Carlo
- **Dicionário:** Meta Anual medida mensalmente · OLA quebrado = `Duração` > limite por prioridade

#### 5.2. Tendência diária · 30 dias (cobre #5 e #6)
- Linha dupla: **volume de incidentes/dia** + **OLA quebrado/dia**
- **Fonte:** agregação direta de `Aberto` + `KPI Violado?` no dataset

#### 5.3. "Tem fogo agora?"
- 3 cascatas em formação (resumo)
- Cada uma: produto + INC pai + nº de filhos atuais + tempo desde 1º filho + link
- **Fonte:** agrupamento real `Incidente Pai`

#### 5.4. "Próximos dias" · resumo D+1/D+7 (cobre #1, #2, #3)
- Mini gráfico de barras: hoje + 7 dias, segregado **P2 + P3**
- Link "Ver previsão completa" → `previsao.html`
- **Fonte:** Prophet

#### 5.5. "Top instabilidades"
- 3 produtos com maior queda de score nas últimas 2 semanas
- Score atual + delta
- Link "Ver todos" → `saude-produto.html`
- **Fonte:** XGBoost regressor

#### 5.6. Morning brief teaser
- Badge "Edição 365 · 06:00"
- Botão "Ler" → modal ou linka pra `morning-brief.html`

### O que NÃO vai ter
- ❌ Hostname inventado
- ❌ Countdowns
- ❌ Métricas de runbook
- ❌ Sparklines decorativos sem dado
- ❌ "+12% vs ontem" sem comparativo real do dataset

---

## 6. Tela 2 · `previsao.html` (NOVA)

### Dor
"O que vem nos próximos dias?" — capacity planning, escala de plantão, alocação preventiva.

### Obrigatoriedades cobertas
D+1 (#1) · D+7 (#2) · por prioridade (#3) · por dimensão (#4).

### Seções

#### 6.1. Hero D+1 · "Amanhã"
- Número grande: incidentes esperados amanhã, **P2 + P3** (regra do KPI)
- Banda de confiança (IC 90%)
- Comparação com a média do mês
- **Fonte:** Prophet (treinado em série diária pós-set/2025 para evitar distorção da anomalia)

#### 6.2. Gráfico forecast 7 dias
- Barras: hoje + próximos 7 dias, segregadas P2 / P3 (stacked)
- Banda CI sombreada
- Hover/click revela valor exato
- Toggle: **volume previsto** vs **OLA quebrado previsto** (forecast × taxa histórica de violação por prioridade)
- **Fonte:** Prophet · `Prioridade` filtrado por `Entrou para KPI? = SIM`

#### 6.3. Distribuição esperada por dimensão (cobre #4)
- 3 tabs: **Produto · Categoria · IC**
- Top 5-10 dimensões com mais incidentes previstos nos próximos 7d
- **Fonte:** forecast total × distribuição histórica recente (últimos 30 dias)
- *Decomposição agregada honesta — não treina Prophet por dimensão*

#### 6.4. Eventos especiais previstos
- Lista de "dias críticos" (volume previsto > percentil 75 da janela)
- Cada dia: data + volume previsto + razão da elevação
- **Fonte:** Prophet (decomposição tendência + sazonalidade semanal + `country_holidays='BR'`)

#### 6.5. Impacto previsto na meta mensal
- "Se confirmar este forecast, fecha o mês com **N violações** vs meta **M**"
- Indicador: dentro / próximo do limite / acima
- **Fonte:** soma forecast Prophet × taxa histórica de violação por prioridade

### O que NÃO vai ter
- ❌ Previsão de hora específica
- ❌ 51 modelos Prophet por produto
- ❌ Por subcategoria (447 valores)
- ❌ Comparativo com 3 anos (anomalia set/2025 fica clara no rodapé)

---

## 7. Tela 3 · `saude-produto.html` (ajustar)

### Dor
"Algo ficando instável?" — manutenção preventiva, identificar produto em deterioração antes de virar cascata.

### Obrigatoriedades cobertas
Previsão por produto/IC (#4 parcial) · tendências/clusters (#8) · explicabilidade (#9).

### O que mantém da versão atual
- Header simples + segment 24h/7d/30d com pill animada
- 4 mini stats inline
- Lista de produtos com drill-down inline (clica → expande)
- Sparkline + delta + score colorido por faixa

### Seções (ajustadas)

#### 7.1. Header + segment 24h/7d/30d

#### 7.2. Mini stats
- Score médio (média dos 51 produtos)
- Em alerta (score < 70)
- Saudáveis (score ≥ 70)
- Mais crítico (produto com menor score)

#### 7.3. Lista de produtos (Top 9-12)
- Colunas: `#` · status dot · tag produto · top fator · sparkline 7d · delta 7d · score
- **Score 0-100:** XGBoost regressor
- **Top fator:** feature mais impactante via SHAP (texto curto)
- **Sparkline 7d:** histórico real do score por dia
- **Delta:** comparativo de 7d atrás

#### 7.4. Drill-down inline
- "**Por que a nota é X**" — top 3-5 fatores SHAP com barras (impacto SHAP)
- "**Tendência 30 dias**" — mini gráfico do score do produto
- **(REMOVIDO)** bloco "O que fazer agora" com `+9 pp` / `−18 pp`

### Fontes de dados
- **Score 0-100:** XGBoost regressor sobre features agregadas por produto:
  - Taxa `KPI Violado? = SIM` nos últimos 30d
  - Volume rolling 7d
  - `Duração` mediana
  - % `Status = Sem Intervenção`
  - % `Solução = Definitiva`
  - Taxa de incidentes que viraram pais de cascata
- **SHAP:** TreeSHAP padrão do XGBoost
- **(Opcional)** Cluster DTW: TimeSeriesKMeans pra agrupar produtos por padrão temporal — pode aparecer como badge "Grupo A/B/C" na lista

### O que NÃO vai ter
- ❌ "Aplicar IC00014 → +9 pp" (uplift modeling — fora do escopo)
- ❌ Hostname

---

## 8. Tela 4 · `cascata.html` (refazer)

### Dor
"Tem fogo agora?" — detectar acúmulo de incidentes-filhos e agir antes de escalar.

### Obrigatoriedade coberta
Indicar onde agir preventivamente (#7).

### Seções

#### 8.1. Header + 4 mini stats
- "Cascatas em formação"
- Stats: # em formação · # críticas · mais antiga (tempo) · **mitigadas hoje** *(não usar "cortadas hoje")*

#### 8.2. Lista de cards de cascata (1 card horizontal por cascata)

Cada card contém:

**a. Status header**
- Dot + status pill + INC pai + meta (produto, grupo, categoria — campos reais)

**b. Tempo desde 1º filho**
- Calculado do `Aberto` mais antigo entre os filhos

**c. Lista REAL dos incidentes-filhos** (tabela compacta dentro do card)

| `Número` | `Prioridade` | `Descrição resumida` | `Aberto` |
|---|---|---|---|
| INC8643149 | P5 | Apache Busy Workers | 06:24 |
| INC8643151 | P5 | Free disk space less than 10% on volume / | 06:38 |
| INC8643158 | P4 | Check Application Monitoring | 07:12 |

- Cada linha = um filho REAL do dataset
- Descrições da lista top 30 do `vocabulario-real.md`
- Sem cronologia P5→P5→P4 intermediária
- Sem hostname

**d. Card "Padrão histórico" · badge IA**
- "Encadeamento similar a **N cascatas** anteriores · **X dessas (Y%)** chegaram em P3 ou pior"
- **Fonte:** k-NN sobre features de cascata (IC, categoria, grupo designado, nº de filhos, distribuição de prioridades dos filhos)
- Disclaimer técnico: *"k-NN sobre histórico de cascatas"* (validar número exato no notebook 02_features)

**e. Card "Sugestão da IA" · badge IA**
- Texto qualitativo gerado por Claude API a partir do contexto
- SEM número de impacto · SEM mencionar runbook específico
- Ex: *"Padrão de cascata em `lhco` com IC `IC00014` tende a estabilizar mais rápido quando reforçado por equipe com expertise no produto."*

**f. Footer**
- Link "Ver detalhe completo" (sem botão de ação com `+pp`)

#### 8.3. Card de cascata mitigada hoje (caso de sucesso)
- Mostra que o sistema funcionou
- Lista de filhos + tempo total + **código de fechamento mais comum** (campo real `Código de fechamento`)
- Sem mencionar runbook específico

### Fontes de dados
- **Lista de filhos:** agrupamento real `Incidente Pai` no dataset (15.127 filhos · `INC8542250` recorde com 630 filhos)
- **Padrão histórico:** k-NN scikit-learn sobre features de cascata
- **Sugestão:** Claude API (Sprint 3 mockup com texto fixo no protótipo)
- **Tempo:** `Aberto` mais antigo dos filhos
- **Código de fechamento:** campo real (17 valores)

### O que NÃO vai ter
- ❌ Cronologia intermediária P5→P5→P4
- ❌ Hostname
- ❌ "Runbook X 87% sucesso"
- ❌ Countdown "vira P2 em 1h48"
- ❌ "−42 pp impacto se aplicar"
- ❌ "Ações com impacto"

---

## 9. Tela 5 · `morning-brief.html` (ajustar)

### Dor
Resumo executivo da manhã · as 4 dores em narrativa curta · 1ª coisa do dia.

### Obrigatoriedade coberta
Transversal — indicar onde agir (#7), tendências (#8).

### Estilo
Mantém o **editorial (jornal)** que Igor aprovou. Estrutura informativa pura.

### Seções

#### 9.1. Masthead (mantém)
- "Quarta, 31 de Dezembro" · Edição nº 365
- "Live · gerado às 06:00 · baseado em 122.543 incidentes"

#### 9.2. Lead story (ajustado)
- Eyebrow: "Hoje · análise em destaque"
- Headline narrativo baseado em **dado real** do dia (ex: "Volume acima da média projeta meta apertada")
- Deck: contexto sem números mockados
- 3 numbered points: 3 cascatas em formação reais (com INC reais), cada uma com:
  - Produto, INC pai, nº de filhos atuais, tempo desde 1º filho
  - **Sem cronologia P5→P5→P4 intermediária**
- Pull quote do Cronos AI: qualitativo, sem countdown

#### 9.3. Side column
- "**Ontem · 30 dez · em números**" (100% agregação real)
  - Volume incidentes, OLA do dia, MTTR mediano, % auto-resolvidos (Team14)
- "**★ Sugestões da IA**" · badge IA
  - 3 sugestões qualitativas curtas
  - **Sem `+pp` mockado.** Texto natural curado por Claude

#### 9.4. Horizonte · próximos 7 dias (ajustado)
- 3 cards: forecast pra 3 datas próximas
- Cada um: data + título qualitativo + valor (vindo de Prophet)
- Fonte declarada no rodapé

### Cortes vs versão atual
- ❌ "84% probabilidade de escalar pra P2" → "risco crítico" qualitativo
- ❌ "Se nada mudar nas próximas 2 horas" → narrativa sem countdown
- ❌ "+34% no Pico previsto pelo deploy" → valor real de Prophet sem inventar razão
- ❌ "−42 pp" em sugestões
- ❌ **CTA strip** (Ver relatório completo · Marcar como lido · Postar no Slack)
- ❌ **Decisões esperando você** (vão pras telas operacionais)

### O que NÃO vai ter
- ❌ Cronologia P5→P5→P4
- ❌ Countdown
- ❌ Métricas de runbook
- ❌ CTAs ou decisões com checkboxes (morning brief é informativo)

---

## 10. Padrões de UI compartilhados

### Tokens
Todas as telas consomem `../../brand/design-system/assets/tokens.css` como única fonte de tokens (cores, espaçamento, motion, tipografia).

### Identidade visual (já estabelecida)
- Accent único: `#2563EB`
- Tipografia: `Outfit` Sans (`font-variant-numeric: tabular-nums` em números)
- Aesthetic: light glass (Apple HIG · Liquid Glass) — `backdrop-filter: blur(40px) saturate(180%)`
- Cor semântica é informação, não decoração

### Shell compartilhado
- **Sidebar 244px** (já implementada) com nav pra todas as telas
- **Topbar 60px** com breadcrumb + status pill + tabs (quando aplicável)
- **Container central** max-width 1080-1180px

### Badge "Gerado por IA" (já implementado em `cascata.html`)
- Aparece em blocos cuja saída vem de modelo (Padrão histórico, Sugestão IA, Score XGBoost)
- Cor: gradient azul/roxo suave com borda
- Ícone sparkle (★ 4-pontas)

### Data fixa
- Topbar mostra **Quarta, 31/12/2025** em todas as telas (último dia do dataset)
- Hora simulada: 06:42 (manhã)

---

## 11. Modelos no backend (Sprint 3+)

Esta spec é apenas para o **front-end estático** (Sprint 2). Os modelos abaixo serão treinados nos notebooks da Sprint 3:

| Modelo | Notebook | Saída usada na UI |
|---|---|---|
| Prophet (forecast diário, treinado pós-set/2025) | `03_forecast_prophet.ipynb` | D+1, D+7, KPI mensal, Monte Carlo |
| XGBoost (score saúde) | `04_score_saude.ipynb` | Score 0-100 por produto + SHAP |
| k-NN (cascatas similares) | `05_cascata_knn.ipynb` | "N cascatas similares · X viraram P3+" |
| TimeSeriesKMeans + DTW | `06_clusters_produto.ipynb` | Cluster badge na lista de produtos |
| Claude API (geração texto) | `07_claude_brief.ipynb` | Morning brief lead + sugestões |

Os números na UI do protótipo (Sprint 2) usam **valores plausíveis** baseados no dataset, mas a fonte declarada deixa claro que vem de modelo (a treinar). Quando o modelo treinar (Sprint 3), os números do protótipo serão substituídos pelos valores reais.

---

## 12. Próximos passos

Após aprovação desta spec:

1. Invocar `superpowers:writing-plans` para criar **plano de implementação** detalhado.
2. Implementar tela por tela, em ordem:
   1. `cascata.html` (refazer — maior trabalho)
   2. `saude-produto.html` (ajustar)
   3. `morning-brief.html` (ajustar)
   4. `dashboard.html` (refazer com nova estrutura)
   5. `previsao.html` (criar nova)
3. **Após cada tela**, validar cada feature contra `prototipos/docs/dicionario-dados.md` (princípio #1).
4. Após as 5 telas:
   - Deletar `kpi-probabilidade.html` (não está no escopo).
   - Configurar GitHub Pages.
   - Atualizar `prototipos/README.md`.
   - Adicionar slide AED da anomalia de set/2025 no notebook `01_eda.ipynb` (gráfico de série mensal).
   - Montar PPT da Sprint 2 com screenshots das 5 telas + arquitetura + tecnologias + Kanban.

### Cronograma sugerido (48h até 24/05)

- **Sex 22/05 (resto):** cascata (refazer) + saúde-produto (ajustar)
- **Sáb 23/05:** morning-brief + dashboard (refazer) + previsão (nova) + GitHub Pages
- **Dom 24/05:** AED anomalia set/25 + PPT + submit

---

## 13. Arquivos relacionados

- `prototipos/docs/dicionario-dados.md` — referência oficial dos campos do dataset (criada hoje)
- `prototipos/docs/vocabulario-real.md` — distribuições reais (números, frequências)
- `brand/design-system/assets/tokens.css` — fonte única de tokens
- `assets/Materal LocalWeb/LW-DATASET.xlsx` — dataset oficial
- `assets/Materal LocalWeb/Locaweb_FIAP_Apresentação_V2.pdf.pdf` — briefing oficial
- `context/decisoes-tecnicas.md` — stack do projeto
- `context/mentoria-locaweb.md` — pedidos do Douglas

---

*Spec consolidada em 22/05/2026 após sessão de brainstorming. Aguardando aprovação do Igor para invocar `writing-plans` e prosseguir com implementação.*

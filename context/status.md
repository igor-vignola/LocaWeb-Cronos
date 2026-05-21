# Status — onde estamos AGORA

> Este arquivo deve ser atualizado a cada bloco de trabalho concluído. Funciona como "rascunho do estado atual" — é o primeiro arquivo a consultar para retomar o trabalho.

---

## Atualizado em: 20/05/2026 (skills de design realocadas para `.claude/skills/`)

## Sprint atual: **Sprint 2 — Arquitetura** 🚧

**Entrega:** 24/05/2026 (domingo) — **4 dias restantes**

**Arquivo final a entregar:** `EC_Sprint_2_2TSCOA_arqsolucao_Cronos_SuperDataBros.pptx`

---

## ⚠️ Reordenação de prioridade (decidida em 20/05)

Lemos o **template oficial da Sprint 2** (`assets/Templates/02Template_Arquitetura_Challenge_2026_01_locaweb_v1.pptx`) e descobrimos que o template tem **apenas 5 blocos** — nenhum slide de AED ou modelagem.

**Nova ordem de prioridade (trilha A — cobertura mínima viável):**

1. 🔴 **PROTÓTIPOS** — 5 telas em HTML/CSS/JS (é o bloco MAIOR no template: 5 slides)
2. 🔴 **Arquitetura + Tecnologias** — diagrama + lista justificada
3. 🟡 **Gestão ágil** — Scrum + cronograma + divisão
4. 🟢 **Agradecimentos** — slide de fechamento
5. ⚪ **AED** — agora é bônus, decidir no sábado se entra no PPT

**Por que essa mudança:** o template é o que vai ser avaliado. Investir tempo no que ele explicitamente pede.

---

## O que já foi feito

### Setup do projeto
- ✅ Repositório Git inicializado e no GitHub
- ✅ URL: https://github.com/igor-vignola/LocaWeb-Cronos (privado)
- ✅ Estrutura de pastas: `assets/`, `brand/`, `sprints/`, `data/raw/`, `notebooks/`, `prototipos/`
- ✅ Contexto materializado em `CLAUDE.md` + pasta `context/`
- ✅ Skills do projeto em `.claude/skills/` (challenge-context, sprint-checklist, commit-style, notebook-style, viz-style, python-style)

### Sprint 1
- ✅ Entregue 27/04 — **Nota: 5.00/5.00**

### Sprint 2 — progresso até agora (20/05, ~17h)
- ✅ `requirements.txt` criado com versões pinadas (pandas, plotly, openpyxl, holidays, etc.)
- ✅ `notebooks/01_eda.ipynb` — Seções 1 e 2 (Setup + Carga) rodando end-to-end + Seção 3 (Visão geral) parcial — `df.head()`, `df.info()`, `df.describe()`, `df.isna()` já executados, achados consolidados em chat (não documentados ainda no notebook como markdown)
- ✅ `prototipos/assets/style.css` — paleta Cronos + componentes base prontos (KPIs, cards, tabelas, sparklines, alertas)
- ✅ Arquivo Figma de teste criado (https://www.figma.com/design/OEBIG7Bh1P6z6TFi8FufSd) — abandonado por limite do plano Starter
- ✅ Template oficial da Sprint 2 lido e mapeado (5 blocos, sem AED)

### Mentoria Locaweb
- ✅ Insights capturados em `context/mentoria-locaweb.md`
- Direções confirmadas: Docker, agnóstico cloud, anomalia de setembro, padrão de cascata, KPI pai, dashboard estilo TIM/Unifique

---

## Próximo passo imediato

**Construir os 5 protótipos HTML** em `prototipos/`. Igor instalou skills/agentes de design — usar elas pra elevar a qualidade visual.

Ordem das telas a construir:
1. `dashboard.html` — Dashboard Geral (visão de topo: KPIs + chart 30d + alertas + tabela top produtos)
2. `morning-brief.html` — Resumo Ontem/Hoje/Ações + botão "ver detalhes"
3. `cascata.html` — Detector de cascata (alerta + histórico P4/P5 → P3/P2)
4. `saude-produto.html` — Score de saúde por produto (ranking + drilldown)
5. `kpi-probabilidade.html` — Probabilidade de atingir KPI (projeção condicional)
6. `index.html` — navegação simples entre as 5 telas

Cada tela vira **screenshot** que cola no slide do PPT.

> O CSS base já está pronto em `prototipos/assets/style.css` — paleta Cronos completa, componentes (KPIs, cards, tabelas, sparklines, alertas, badges, score bars) prontos pra reusar.

---

## O que falta na Sprint 2

- [ ] **PROTÓTIPOS** — 5 HTMLs + index (CSS já pronto)
- [ ] Arquitetura + tecnologias — diagrama + slide de stack
- [ ] Gestão ágil — Scrum + cronograma + divisão Ana/Hygor/Igor
- [ ] Finalização e agradecimentos
- [ ] **AED** (bônus, decidir sábado) — Seção 4 do notebook só se sobrar tempo
- [ ] Montagem do PPT a partir do template oficial

> **Fora de escopo nesta sprint:** atualização do "problema/público/solução" da Sprint 1 (decisão do Igor — colar o que tinha sem refazer).

---

## Tempo restante (estimativa)

| Dia | Janela |
|---|---|
| Qui 21 | 2-3h |
| Sex 22 | 2-3h |
| Sáb 23 manhã | 3-4h |
| Dom 24 | ZERO — entrega |

**Total:** ~8-10h. Apertado mas viável pra trilha A.

---

## Pontos de atenção carregados das sprints anteriores

Do feedback Sprint 1: **toda menção de impacto/benefício precisa ter número ou gráfico**.

Da mentoria Locaweb: dashboard estilo TIM/Unifique, near real-time, 2-3 abas, não mais.

---

## Bloqueios / dúvidas em aberto

- Nenhum no momento.

## Skills de design disponíveis (instaladas em `.claude/skills/`)

Carregadas em 20/05 — usar nos protótipos da Sprint 2:

- **`design-taste-frontend`** — Senior UI/UX Engineer, regras métricas estritas, arquitetura de componente
- **`emil-design-eng`** — filosofia Emil Kowalski de polish/animação/detalhe invisível
- **`high-end-visual-design`** — fontes/espaçamento/sombras/cards que fazem site parecer caro
- **`minimalist-ui`** — editorial clean, paleta monocromática quente, bento grids planos
- **`industrial-brutalist-ui`** — terminal militar + Swiss typo, grids rígidos (alternativa estética)
- **`gpt-taste`** — UX/UI + GSAP motion, AIDA, tipografia editorial
- **`redesign-existing-projects`** — auditar e elevar UI existente
- **`image-to-code`** — gera imagem de design e converte em código
- **`imagegen-frontend-web`** — gerar imagens de referência de sites
- **`imagegen-frontend-mobile`** — gerar imagens de telas mobile (não gera código)
- **`brandkit`** — boards de identidade visual premium (logo system, brand guidelines)
- **`stitch-design-taste`** — gerar DESIGN.md semântico pro Google Stitch
- **`full-output-enforcement`** — anti-truncamento, força código completo sem placeholders

**Recomendação inicial para os 5 protótipos do Cronos:** `design-taste-frontend` + `emil-design-eng` + `minimalist-ui` (combinam com a referência TIM/Unifique: clean, dashboard, editorial).

---

*Atualizar este arquivo após cada bloco concluído.*

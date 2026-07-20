# Sprint 2 — Arquitetura, desenho e protótipos iniciais

## Resumo

- **Tema:** Arquitetura inicial da solução
- **Período:** 20/05/2026 a 24/05/2026 *(começamos antes, em 13/05)*
- **Status:** ✅ ENTREGUE 24/05/2026 · **nota 5.00/5.00** (avaliada 09/06/2026)
- **Arquivo entregue:** `EC_Sprint_2_2TSCOA_arqsolucao_Cronos_SuperDataBros.pptx`

> **Feedback do professor (09/06/2026):** "A apresentação oferece uma arquitetura
> detalhada com integrações claras entre tecnologias e protótipos bem elaborados da
> interface final, demonstrando domínio sobre o tema. O único ponto a observar para
> próximas entregas é dedicar um slide explícito à gestão ágil do projeto, embora
> indícios disso estejam presentes de forma implícita. Ótimo equilíbrio entre teoria,
> técnica e visualização."
>
> **Ação p/ Sprint 3:** o template da Sprint 3 já tem 2 slides dedicados a gestão de
> projeto (Kanban) — endereçar de forma explícita e caprichada resolve o único ponto.

> Antes de finalizar qualquer entregável desta sprint, executar a skill **`sprint-checklist`** item por item.

---

## ⚠️ Estratégia revisada em 20/05 (LER ANTES DE TUDO)

Lemos o **template oficial** (`assets/Templates/02Template_Arquitetura_Challenge_2026_01_locaweb_v1.pptx`) e descobrimos que ele tem APENAS 5 blocos — sem AED, sem modelagem, sem "problema/público-alvo".

### Os 5 blocos do template oficial

| # | Bloco | Slides | Foco |
|---|---|---|---|
| 1 | Arquitetura de Solução | 3-4 | Diagrama + justificativa de cada elemento + fontes de dados |
| 2 | Tecnologias utilizadas | 5 | Lista das tecnologias com porquê |
| 3 | **Protótipos da Solução** | **6-10 (5 slides!)** | Mockups das telas — **BLOCO MAIOR** |
| 4 | Planejamento e Gestão | 11-12 | Kanban, cronograma, acompanhamento ágil |
| 5 | Formalização + Agradecimentos | 13 | Conclusão + agradecimentos |

### Sugestões do template a IGNORAR por decisão técnica do projeto
- ❌ Streamlit / Dash (regra do projeto: Django mandatório)
- ❌ Microsoft Azure (regra: agnóstico de cloud)

---

## Trilha A — cobertura mínima viável (ordem revisada)

### A.1 PROTÓTIPOS (PRIMEIRA FRENTE — bloco maior) 🔴

5 telas em **HTML/CSS/JS** dentro de `prototipos/`. Cada uma vira screenshot pro slide do PPT.

**Estado atual:**
- ✅ `prototipos/assets/style.css` — paleta Cronos + componentes base prontos (KPIs, cards, tabelas, sparklines, alertas, badges, score bars)
- ⏳ HTMLs das 5 telas: a fazer

**Telas:**
1. `dashboard.html` — Dashboard Geral (KPIs + chart 30d + alertas + tabela top produtos)
2. `morning-brief.html` — Resumo Ontem/Hoje/Ações + botão "ver detalhes" (mentoria pediu)
3. `cascata.html` — Detector de cascata P4/P5 → P3/P2 (padrão validado pelo Douglas)
4. `saude-produto.html` — Score de saúde por produto (ranking + drilldown)
5. `kpi-probabilidade.html` — Probabilidade de atingir KPI (projeção condicional do mês)
6. `index.html` — landing simples com links pras 5 telas (vira o "home" do protótipo)

**Identidade visual:** paleta Cronos (azul `#2563EB`, cinzas neutros, vermelho `#DC2626` só pra perigo), tipografia Inter, layout limpo estilo TIM/Unifique.

> **Igor instalou skills/agentes de design.** Usar elas pra elevar a qualidade visual. Validar nomes na próxima sessão.

### A.2 ARQUITETURA + TECNOLOGIAS

**Arquitetura (2 slides):**
- Diagrama de camadas: dados → modelos → app Django → Claude API → Docker
- Tudo agnóstico de cloud
- Descrição do papel de cada camada
- Ferramentas pra gerar: Mermaid → PNG (sem precisar de Figma)

**Tecnologias (1 slide):**
- Tabela: Django, Pandas, Prophet, XGBoost, tslearn, SHAP, Plotly, Claude API, Docker, holidays BR
- Cada uma com o porquê em 1 linha
- O **plano de modelagem entra aqui** (não precisa de slide próprio)

### A.3 GESTÃO ÁGIL (1-2 slides)

- Framework: **Scrum**
- Ferramenta visual: Kanban (Trello/Notion/PowerPoint mesmo)
- Cronograma macro até Sprint 4
- Divisão de tarefas entre Ana, Hygor e Igor

### A.4 FINALIZAÇÃO E AGRADECIMENTOS (1 slide)

Conclusão curta + agradecimentos (FIAP, Locaweb, Douglas).

---

## AED — agora é BÔNUS

**Decisão de 20/05:** AED não está no template oficial. Vai para o sábado, e só entra no PPT se sobrar tempo (1-2 slides).

**O que já existe:**
- `notebooks/01_eda.ipynb` com Seções 1 e 2 (Setup + Carga) rodando + Seção 3 (Visão geral) parcial
- Achados consolidados: 122.543 incidentes, 75,7% no Team14, 85% Monitoramento, 65,6% Sem Intervenção, 3 patamares de NaN, distribuição concentrada em 2025

**Se entrar no PPT:** vira 1-2 slides "Caracterização do dataset" antes da arquitetura. Justifica escolhas técnicas.

**Vai pro repo de qualquer jeito:** o notebook é ativo da Sprint 3 (MVP precisa da AED feita).

---

## Cobranças extras do professor (feedback Sprint 1)

- **Impacto com números/gráficos** — toda menção de benefício deve ter métrica concreta. Aplicar nos slides de arquitetura/protótipos (não só na AED).
- "AED de verdade" e "modelagem detalhada" — endereçar parcialmente no slide de tecnologias (mostrando que pensamos no approach) e no notebook do repo.

---

## Cronograma realista (4 dias)

| Quando | Bloco | Saída esperada |
|---|---|---|
| **Qui 21 (2-3h)** | Construir Dashboard Geral + Morning Brief em HTML | 2 telas prontas |
| **Sex 22 (2-3h)** | Construir Cascata + Saúde + KPI Probabilidade + index | 5 telas + nav |
| **Sáb 23 manhã (3-4h)** | Diagrama de arquitetura + tabela de tecnologias + slide de gestão + montar PPT a partir do template + (se sobrar) 1-2 slides de AED | PPT entregável |
| **Dom 24** | — | Submit |

---

## Riscos identificados

| Risco | Mitigação |
|-------|-----------|
| 4 dias com 2 fins de semana | Foco em trilha A — não tentar trilha B antes de fechar o essencial |
| Mockups serem o gargalo (5 telas é muito) | CSS base já pronto, design system definido → cada tela é só compor componentes |
| Falta de números/gráficos no impacto (feedback S1) | Usar achados do notebook 01_eda nos slides de arquitetura ("122k incidentes em 17 grupos justifica X") |

---

## Entregáveis materiais

- [ ] `EC_Sprint_2_2TSCOA_arqsolucao_Cronos_SuperDataBros.pptx`
- [ ] `prototipos/telas/dashboard.html` + 4 outras telas + `index.html`
- [ ] `brand/design-system/` (foundations, motion, atoms, molecules, patterns) ✅ JÁ FEITO
- [ ] Diagrama de arquitetura (PNG via Mermaid)
- [ ] `notebooks/01_eda.ipynb` (ativo interno, parcial — vai pro repo de qualquer jeito)
- [ ] Plano de gestão ágil (no slide do PPT)

---

*Atualizar conforme avançar.*

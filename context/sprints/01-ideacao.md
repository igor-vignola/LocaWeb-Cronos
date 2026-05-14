# Sprint 1 — Ideação

## Resumo

- **Tema:** Ideação do projeto
- **Período:** 15/04/2026 a 27/04/2026
- **Status:** ✅ ENTREGUE
- **Nota:** **5.00/5.00** (máxima)
- **Arquivo entregue:** `sprints/sprint-1/EC_Sprint_1_2TSCOA_ideacaoprojeto_Cronos_SuperDataBros.pptx`

## Feedback do professor

Avaliado em domingo, 03 de Maio de 2026, às 16h51:

> *"O trabalho apresenta todos os tópicos exigidos, com contextualização clara e solução bem detalhada. O único ponto de atenção seria ilustrar ainda mais o impacto para o negócio com exemplos numéricos ou gráficos no futuro."*

### Análise do feedback

**Pontos fortes reconhecidos (3 dos 6 critérios oficiais):**
- Todos os tópicos exigidos
- Contextualização clara
- Solução bem detalhada

**Ponto de atenção carregado para próximas sprints:**
- Reforçar impacto de negócio com **números concretos e gráficos**.

Este ponto casa com 2 dos critérios da Locaweb:
- Valor gerado para tomada de decisão
- Comunicação dos resultados (storytelling)

## Estrutura do deck (16 slides)

| # | Tipo | Conteúdo |
|---|------|----------|
| 1 | Capa | Cronos + título + equipe |
| 2 | Identificação | Equipe Super Data Bros, RMs |
| 3 | Origem do nome | Deus grego do tempo + manifesto |
| 4 | 01 · Contexto | Contextualização do problema |
| 5 | 02 · Problema | Operação reativa, ruído, risco de KPI |
| 6 | 03 · Público-alvo | Gestor (Estratégico) / SRE (Tático) / Equipes (Operacional) — com badges |
| 7 | Ponte narrativa | "Como transformar essa realidade?" |
| 8 | 04 · Solução | Previsão D+1/D+7, Projeção de KPI, Classificação, Explicabilidade |
| 9 | Diferencial 1 | Morning briefing |
| 10 | Diferencial 2 | Detector de cascata |
| 11 | Diferencial 3 | Score de saúde por produto |
| 12 | Impacto | Sem Cronos vs Com Cronos |
| 13 | 06 · Benefícios | 5 cards de benefícios esperados |
| 14 | 07 · Concorrência | Tabela Dynatrace / Splunk ITSI / Datadog vs Cronos |
| 15 | 08 · Próximos passos | O que vamos fazer na Sprint 2 |
| 16 | Fechamento | Logo + equipe |

## Decisões importantes tomadas na Sprint 1

- **Nome do produto:** Cronos
- **Tagline:** "Veja antes. Aja antes."
- **Identidade visual:** ícone preto arredondado, gráfico branco, ponto azul, fonte Sora
- **3 diferenciais definidos:** morning briefing, detector de cascata, score de saúde
- **Stack inicial:** Prophet + XGBoost + tslearn DTW + SHAP + Django
- **Restrições:** sem ARIMA, sem K-Means puro, sem Streamlit

## Lições aprendidas

- **Investir em layout limpo paga.** O deck minimalista (fundo escuro/claro alternando, sem poluição visual) foi parte do que o professor elogiou como "contextualização clara".
- **Storytelling com dados reais funciona.** Usar números do dataset (122.543 incidentes, 248 OLAs violados, 66% ruído) deu peso à apresentação.
- **Diferenciação narrativa via comparativo "sem/com".** O slide de impacto (Sem Cronos vs Com Cronos) tornou o valor da solução tangível.

## O que carregar para próximas sprints

- ✅ Apresentar impacto com **números e gráficos** (feedback explícito do professor)
- ✅ Manter a identidade visual e o sistema de design
- ✅ Continuar usando os 3 diferenciais como espinha dorsal da narrativa
- ✅ Garantir filtro de incidente pai em qualquer análise de OLA

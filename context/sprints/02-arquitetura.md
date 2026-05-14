# Sprint 2 — Arquitetura, desenho e protótipos iniciais

## Resumo

- **Tema:** Arquitetura inicial da solução
- **Período:** 20/05/2026 a 24/05/2026 *(começamos antes, em 13/05)*
- **Status:** 🚧 EM ANDAMENTO
- **Arquivo a entregar:** `EC_Sprint_2_2TSCOA_arqsolucao_Cronos_SuperDataBros.pptx`

> Antes de finalizar qualquer entregável desta sprint, executar a skill **`sprint-checklist`** item por item.

---

## Entregáveis obrigatórios (do briefing oficial)

1. **Problema, público-alvo e solução** — apresentação atualizada da Sprint 1 + indicação do que mudou
2. **Arquitetura e desenho inicial** — representação visual + delineamento das tecnologias e suas conexões
3. **Descrição da arquitetura** — papel de cada tecnologia
4. **Protótipos** — wireframes/mockups com descrição
5. **Análise Exploratória de Dados** — padrões, oportunidades, desafios
6. **Gerenciamento ágil** — framework + cronograma + divisão de tarefas
7. **Finalização e agradecimentos**

> Detalhe item por item na skill `sprint-checklist`.

---

## Cobranças extras do professor (feedback Sprint 1)

- **Impacto com números/gráficos** — toda menção de benefício deve ter métrica concreta
- **AED de verdade** (pedido explícito também)
- **Modelagem** detalhada (pedido explícito também)

---

## As 8 frentes de trabalho mapeadas

### 1. Atualização da Sprint 1 *(rápido)*
Retomar problema/público/solução da Sprint 1. Marcar o que mudou após a mentoria Locaweb:
- Morning brief agora é "resumo + relatório completo"
- Cascata confirmada (não é mais hipótese)
- KPI só pai
- Agnóstico de cloud + Docker

### 2. AED — Análise Exploratória de Dados *(maior bloco)*

**Slides previstos (6-8 no PPT):**
- Visão geral do dataset (122k incidentes, 19 colunas, jan/23 a dez/25)
- Distribuição temporal dos incidentes
- **Anomalia de setembro/2025** — investigação + hipótese (slide especial)
- Sazonalidade real (feriados + fins de semana)
- Top produtos/categorias mais críticos
- Análise de OLA (filtrando pais)
- Padrão de cascata P4/P5 → P3/P2
- Slide-síntese: "o que essa AED nos diz sobre como modelar"

**Operação:** Claude roda a AED em Python (ou no Claude Code), Igor revisa cada descoberta, melhores achados viram slide. Código final consolidado em `notebooks/01_eda.ipynb`.

**Investigação obrigatória:** anomalia de setembro/2025 (pedido explícito da Locaweb).

### 3. Plano de modelagem *(cobrança do professor)*

Não é treinar modelo agora — é **explicar approach com base na AED**.

- Prophet para tendência + sazonalidade
- XGBoost com features temporais (lag, rolling, dia_semana, is_feriado)
- tslearn + DTW para clusterização
- SHAP para explicabilidade
- Cada escolha justificada pelos achados da AED

### 4. Arquitetura e desenho da solução

Diagrama visual mostrando:
- Camada de dados → camada de modelos → camada de aplicação Django → integração Claude API → entrega Docker
- Tudo agnóstico de cloud

### 5. Stack técnica

Lista das tecnologias com o porquê de cada uma:
- Django, Pandas, Prophet, XGBoost, tslearn, SHAP, Plotly, Claude API, Docker, holidays BR

### 6. Protótipos da interface

Mockups das telas principais:
- Dashboard geral (estilo TIM/Unifique, 2-3 abas)
- Morning brief (resumo + botão "ver detalhes" + relatório completo)
- Detector de cascata
- Score de saúde por produto
- Probabilidade de atingir KPI

### 7. Gestão ágil

- Framework: **Scrum** (faz sentido pelo formato de sprints)
- Ferramenta: Jira/Trello/Notion (definir)
- Cronograma até Sprint 3 e Sprint 4
- Divisão de tarefas entre Ana, Hygor e Igor

### 8. Finalização e agradecimentos
Slide de fechamento.

---

## Cronograma sugerido nos 11 dias

A AED termina antes de tudo (porque informa todos os outros blocos). Trabalho técnico depois em paralelo. Gestão e PPT nos dias finais.

```
13/05 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 24/05
       AED + setembro ▒▒▒▒▒▒▒
                   Modelagem  ▒▒▒
                   Arquitetura  ▒▒▒▒
                       Protótipos  ▒▒▒▒▒
                          Gestão + recap S1  ▒▒▒
                             Montagem PPT  ▒▒▒▒
                                              ENTREGA ▲
```

---

## Riscos identificados

| Risco | Mitigação |
|-------|-----------|
| Fins de semana podem reduzir disponibilidade do time (4 dias de 11) | Alinhar com Ana e Hygor; ter buffer |
| Investigação de setembro pode virar rabbit hole | Budget máximo de 2 dias; fechar com hipótese mais provável |
| Tentação de já treinar modelo agora | Sprint 2 é só PLANO de modelagem. Treinamento real fica para Sprint 3 |
| Falta de números/gráficos no impacto (feedback S1) | Calcular tudo do dataset durante a AED |

---

## Entregáveis materiais

- [ ] `EC_Sprint_2_2TSCOA_arqsolucao_Cronos_SuperDataBros.pptx`
- [ ] `notebooks/01_eda.ipynb` (ativo interno, vai para o repo)
- [ ] Diagrama de arquitetura (PNG/SVG)
- [ ] Mockups dos protótipos (PNG/SVG ou nos próprios slides)
- [ ] Plano de gestão ágil (no PPT ou em ferramenta linkada)

---

*Atualizar conforme avançar.*

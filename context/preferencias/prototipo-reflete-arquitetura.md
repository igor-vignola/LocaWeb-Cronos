---
data: 2026-05-21
tipo: preferencia
status: ativo
relacionados: [prototipagem-claude-design]
---

# Protótipo deve refletir TODA decisão da arquitetura

## Contexto

Em 21/05/2026, durante a iteração do spec do protótipo (passamos do V1 estético-only pro V2 acionável), Igor articulou explicitamente:

> *"precisamos pensar em tudo que vamos criar de modelos e dicas com IA, como se estivesse tudo pronto e estamos aplicando isso no sistema, entao nao faz sentido falarmos que vamos ter isso e isso na arquitetura, modelos e no prototipo nao mostrar nada do beneficio disso aplicado de fato"*

A primeira versão do spec era bonita mas decorativa — mostrava estado, não decisão. Faltavam: baselines, owners, impacto em R$ e clientes, decomposição "POR QUE" das previsões (SHAP), intervalo de confiança, countdown de janela de ação, lista de cascatas ativas (não só uma), carga por equipe, empty states celebrando comportamento bom.

## O que ficou definido

**Regra de ouro:** Toda decisão técnica declarada na arquitetura/modelagem tem que ter **manifestação visual** no protótipo. Dados podem ser mockados, mas o componente da inteligência tem que estar representado.

## Por quê

A banca FIAP penaliza forte quando protótipo e arquitetura não conversam — dá impressão de que o time sabe falar mas não sabe construir. O feedback da Sprint 1 já tinha cobrado *"ilustrar mais o impacto para o negócio com exemplos numéricos ou gráficos"* — esta regra é a generalização desse princípio.

Sem essa regra, Cronos vira "caixa preta que prevê" — não confiança. Com ela, vira sistema cuja inteligência é visível e auditável.

## Como aplicar

Ao revisar/escrever qualquer entregável visual do Cronos (PPT, mockup, protótipo, slide), passar o checklist:

| Decisão declarada na arquitetura | Manifestação visual obrigatória |
|---|---|
| Prophet (forecast com tendência+sazonalidade) | Intervalo de confiança visível (`73% ±8pp · 90% CI`) |
| XGBoost com features temporais (lag, rolling, dia_semana, is_feriado) | — (cobertura indireta via dashboard) |
| SHAP / explicabilidade | Decomposição "POR QUE" no card de previsão, com pesos % de cada feature |
| TimeSeriesKMeans + DTW | Bloco "produtos correlatos" mostrando agrupamento + % chance de serem arrastados pela cascata |
| Claude API pra alertas + morning brief | Eyebrow `· IA` ou `GERADO POR IA` no texto |
| Detector de cascata | Fluxo P5→P4→P3 com nó P2 previsto pulsando (tracejado) |
| Score de saúde 0-100 | Visível com decomposição (peso de cada fator no hover/click) |
| KPI mensal com janela de ação | Countdown explícito (`38h até decisão impossível`) |
| Holidays BR via lib `holidays` | Marker visual em dias de feriado nos gráficos |
| Docker entrega | (não tem manifestação visual — é deploy) |

**Regra de revisão:** Antes de aprovar qualquer protótipo, abrir o slide de stack/arquitetura ao lado e fazer match 1:1 — cada item da stack precisa ter pelo menos UM elemento visual correspondente. Se sobrar item da stack sem manifestação visual:
- Ou é stack inflada (cortar do PPT)
- Ou é protótipo incompleto (adicionar)

**Generalização pra outros entregáveis:**
- Slide de "diferenciais" → mostrar print do diferencial funcionando, não só descrever
- Slide de "modelagem" → screenshot do output do modelo (mockado ou real)
- Slide de "stack" → conectar cada item a um print do protótipo onde aparece

## Conexões

- [[prototipagem-claude-design]] — ferramenta atual que aplica este princípio
- [[aesthetic-dark-glass-hibrido]] — onde isto se manifesta visualmente

---

*Última atualização: 2026-05-21*

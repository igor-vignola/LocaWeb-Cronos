---
data: 2026-07-20
tipo: decisao
status: ativo
relacionados: [regras-kpi-e-anomalia-setembro, setup-ambiente-modelagem-windows]
---

# Alvo dos modelos: a série elegível ao KPI, não o volume total

## Contexto

Ao começar a Sprint 3 investigamos a anomalia de setembro/2025 (o volume mensal
quintuplica de uma vez). Descobrimos que o salto é 100% ruído de monitoramento
automático que fecha sozinho ("Sem Intervenção") e não entra no KPI. Isso levantou a
pergunta de qual série os modelos preditivos devem prever. Ver
[[regras-kpi-e-anomalia-setembro]].

## O que ficou definido

- **Prophet** prevê o **volume diário elegível ao KPI** (D+1 e D+7), separado por P2 e P3.
- **XGBoost** estima o **risco de estourar a OLA** sobre a mesma base elegível.
- Filtro de elegibilidade (regra oficial do dicionário): `Incidente Pai` vazio +
  prioridade 1/2/3 + `Status ≠ Sem Intervenção`. Equivale ao campo `Entrou para KPI? = SIM`.
- O que fica **fora** do KPI (P4/P5, monitoramento que se resolve sozinho) não é alvo de
  previsão. Vira **sinal do detector de cascata** (P4/P5 acumulando antes de escalar pra
  P3/P2), em notebook próprio.
- **Não modelar o volume total** (com o ruído de monitoramento).

## Por quê

1. A série elegível ao KPI é **plana** em setembro (2.330 em ago → 2.324 em set), enquanto
   a total salta 5×. Modelar o total obrigaria o Prophet a "aprender" uma quebra de regime
   que é só troca de instrumento de medição, não fenômeno operacional.
2. O desafio pede explicitamente previsão dos **KPIs de P2 e P3**. A série elegível é
   exatamente o que compõe esses KPIs.
3. O dicionário confirma que o ruído fora do KPI ainda pode **prejudicar** incidentes que
   estão no KPI — o que justifica usá-lo como sinal de cascata, não como alvo.

## Como aplicar

- Nos notebooks 02 (features) e 03 (modelagem): filtrar para elegível ao KPI **antes** de
  montar a série diária que o Prophet/XGBoost consomem.
- No notebook de cascata: usar o complemento (P4/P5 e/ou monitoramento) como entrada.
- Correção de intuição registrada: **não** é a origem "Monitoramento" que exclui do KPI
  (9.529 incidentes de origem Monitoramento entram no KPI). É a regra de elegibilidade acima.

## Conexões

- Regras oficiais + investigação: [[regras-kpi-e-anomalia-setembro]]
- Stack aprovada (Prophet/XGBoost/tslearn/SHAP): `../decisoes-tecnicas.md`

---

*Última atualização: 2026-07-20*

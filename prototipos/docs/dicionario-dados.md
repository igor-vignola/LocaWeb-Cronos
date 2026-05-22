# Dicionário de Dados — LWDATASET

> Extraído de `assets/Materal LocalWeb/Dicionário de Dados - v2.docx`.
> Fonte oficial da Locaweb. **Toda feature do protótipo deve ser validada contra este dicionário.**

---

## Regras de KPI / OLA

### Metas Anuais de KPI (indicador medido mensalmente)
1. **Incidentes com OLA quebrados no ano** (campo `Duração`)
2. **Volume total de incidentes tratados no ano**

### Tempo de resolução / encerramento por prioridade (SLA → campo `Duração`)
| Prioridade | Limite de duração |
|---|---|
| 1 — Crítica | até 4h |
| 2 — Alta | até 4h |
| 3 — Média | até 12h |
| 4 — Baixa | até 24h |
| 5 — Muito Baixa | até 96h |

### Quais incidentes entram no KPI
- **Apenas prioridades 1, 2 e 3** entram para o KPI.
- Incidentes com **`Incidente Pai` preenchido NÃO entram** (apenas o pai conta).
- Incidentes com **`Status = "Sem Intervenção"` NÃO entram**.
- **Observação:** os que não entram podem ainda prejudicar incidentes que entram (ex: cascata).

### Origem dos incidentes "Sem Intervenção"
- A maioria dos `Sem Intervenção` foi `Aberto por: Monitoramento`.

---

## Campos do dataset (LWDATASET.xlsx)

### Identificação

| Campo | Descrição | Tipo | Formato | Valores | Obrigatório |
|---|---|---|---|---|---|
| **Número** | Identificador único e sequencial do incidente. | Texto | `INCXXXXXXX` | — | Sim |
| **Incidente Pai** | Referência a um incidente anterior (relacionado ou duplicado). | Texto | `INCXXXXXXX` | — | Não |

### Classificação

| Campo | Descrição | Tipo | Valores | Obrigatório |
|---|---|---|---|---|
| **Prioridade** | Urgência e impacto. **Só 1, 2 e 3 entram no KPI.** | Texto | `1 - Crítica` · `2 - Alta` · `3 - Média` · `4 - Baixa` · `5 - Muito Baixa` | Sim |
| **Produto** | Produto ou serviço afetado. | Texto | (51 valores únicos · top 5: `lhco`, `lsin`, `lcem`, `lhvp`, `lrev`) | Não |
| **Categoria** | Classificação primária. | Texto | (141 valores únicos · top: `cat71`) | Não |
| **Subcategoria** | Refinamento da Categoria. | Texto | (447 valores · associada à categoria) | Não |
| **Grupo designado** | Equipe responsável pela solução. | Texto | (17 grupos · `Team14` = 75.7%) | Sim |
| **Item de configuração (IC)** | Ativo de TI com o problema. | Texto | (9.171 ICs · top: `IC00014` com 6.069 ocorrências) | Não |
| **Código de fechamento** | Razão formal do encerramento. | Texto | 17 valores (top: `Falha de Aplicação` 20.612 · `Falha de SO` 5.009 · `Outro` 3.490) | Não |
| **Descrição resumida** | Título do incidente. | Texto | Texto livre (top: `Problem: Check Application Monitoring` 28.728x) | Sim |

### Datas e duração

| Campo | Descrição | Tipo | Formato | Obrigatório |
|---|---|---|---|---|
| **Aberto** | Data/hora de registro do incidente. | Data/Hora | `dd/mm/aaaa hh:mm:ss` | Sim |
| **Resolvido** | Data/hora em que a equipe técnica determinou correção. | Data/Hora | `dd/mm/aaaa hh:mm:ss` | Não |
| **Encerrado** | Data/hora de finalização (após confirmação ou período de espera). | Data/Hora | `dd/mm/aaaa hh:mm:ss` | Sim |
| **Duração** | Tempo total entre abertura e resolução/encerramento. | Numérico | Segundos | Sim |

### Estado e KPI

| Campo | Descrição | Tipo | Valores | Obrigatório |
|---|---|---|---|---|
| **Status** | Ponto atual no ciclo de vida. | Texto | `Aguardando Problema` · `Encerrado` · `Encerrado Automaticamente` · `Sem Intervenção` | Sim |
| **Aberto por** | Por onde foi aberto. | Texto | `Manual` · `Monitoramento` | Sim |
| **Solução** | Tipo de solução aplicada. | Texto | `Contorno` · `Definitiva` · `(em branco)` | Não |
| **Entrou para KPI?** | Se entra no cálculo do KPI. | Booleano | `SIM` · `NAO` | Sim |
| **KPI Violado?** | Se a duração excedeu o SLA. | Booleano | `SIM` · `NAO` | Sim |

---

## O que isso significa pro protótipo

### Podemos calcular DIRETO do dataset (FATO)
- Volume diário / mensal / anual de incidentes
- Volume por prioridade (1-5)
- Volume por produto / categoria / IC / grupo
- Taxa de OLA violado (entre os elegíveis)
- Duração mediana por prioridade
- Cascatas: pai → filhos (via `Incidente Pai`)
- Origem (Manual vs Monitoramento)
- Tipo de solução (Contorno vs Definitiva)
- Hora do dia / dia da semana de abertura

### Podemos estimar com modelos
- **Prophet** sobre série diária: forecast D+1 e D+7, por prioridade
- **XGBoost / regressão**: probabilidade de violação OLA, score composto de saúde
- **k-NN sobre features de cascata**: cascatas similares no histórico
- **TimeSeriesKMeans (DTW)**: clusters de produtos por padrão temporal
- **Monte Carlo via Prophet**: probabilidade de bater meta mensal

### NÃO temos (não inventar no protótipo)
- ❌ Hostname específico (`lhco-web-03`) — dataset só tem produto/IC
- ❌ Trilha de eventos intermediários dentro de um incidente — só `Aberto`/`Resolvido`/`Encerrado`
- ❌ Qual runbook/procedimento foi acionado — não há campo
- ❌ Comando executado / log de troubleshooting — não há campo
- ❌ Tempo exato até escalar pra outra prioridade — incidente tem prioridade fixa
- ❌ Impacto contrafactual de ação (`−42pp se aplicar X`) — sem treino causal

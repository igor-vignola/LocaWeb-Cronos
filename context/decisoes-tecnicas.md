# Decisões Técnicas — Cronos

Este documento registra decisões já tomadas. Cada decisão tem motivo. **Não reverter sem justificativa forte.**

---

## Atualização Sprint 3 — 21/07/2026 (vale isto)

Ao treinar/testar os modelos no dado real, parte das decisões abaixo foi revista. O texto original segue preservado como registro, mas **prevalece o que está aqui:**

- **Risco de OLA → regressão logística** (não XGBoost). Medição definitiva de 03/08/2026, corte out-of-time (treino até 30/09/2025, teste out–dez com 50 quebras em 5.183 incidentes): ROC AUC 0,8693 contra 0,8679 do XGBoost (empate dentro do ruído) e PR-AUC 0,2958 contra 0,2526 (vantagem de 17%). A logística ainda é explicável por construção e preserva a calibração (48,1 quebras previstas contra 50 observadas), enquanto o XGBoost com `scale_pos_weight` prevê 1.007. XGBoost vira baseline comparado. Prophet segue para o volume.
- **Clusterização DTW → descartada.** `TimeSeriesKMeans`+DTW deu silhueta ~0,13 (sem grupos reais). O requisito de classificação/clusterização é atendido pelo classificador de risco.
- **Detector de cascata → descartado.** Escalada refutada no dado (87% das quebras são isoladas; escalada 21% vs ~60% do acaso); o padrão de acúmulo da mentoria não foi testado. Diferenciais atuais: morning briefing + score de saúde.
- **Escopo temporal:** elegíveis ao KPI concentram-se em 2025 (~1 ano denso). Treino em 2025, sazonalidade semanal ligada, anual desligada.

Evidências e detalhes: `docs/sprint-3-mvp.md`.

---

## Stack aprovada

### Modelagem preditiva
- **Prophet** — captura tendência + sazonalidade. Base da previsão D+1 e D+7.
- **XGBoost** — refinamento com features temporais para capturar padrões não-sazonais.

### Features temporais (XGBoost)
- Lag de 1, 7 e 30 dias
- Rolling window de 7 dias (média, std)
- `dia_semana`
- `is_feriado` (engineering via lib `holidays` BR ou `country_holidays='BR'` do Prophet)
- Variáveis derivadas de produto/categoria/prioridade

### Clusterização
- **tslearn** com `TimeSeriesKMeans` e `metric='dtw'` (Dynamic Time Warping)
- Motivo: produtos podem ter padrões similares mas deslocados no tempo (ex: pico de incidente que acontece em dias diferentes do mês). K-Means euclidiano puro NÃO captura isso.

### Explicabilidade
- **SHAP** (TreeSHAP para XGBoost)
- Waterfall plots para mostrar contribuição de cada feature em cada previsão
- Obrigatório por critério do desafio: "explicar o que está acontecendo, não só prever"

### Aplicação web
- **Django** — escolha mandatória. NÃO usar Streamlit (todo mundo usou ano passado, é diferencial).
- **Plotly** para gráficos interativos no dashboard
- **Pandas / NumPy** para tratamento

### Geração de texto / IA
- **Claude API** — usada APENAS nos bastidores para gerar texto do morning brief e dos alertas. NÃO é interface de chat com usuário.
- A geração roda offline ou via cron, não em request síncrono.

### Infra / entrega
- **Docker** — toda a aplicação containerizada. Locaweb pega e roda.
- **Agnóstico de cloud provider** — não usar Lambda, S3, DynamoDB, BigQuery, etc. Apenas Postgres comum, sistema de arquivos local, etc.

---

## Restrições mandatórias (não negociáveis)

| Restrição | Motivo |
|-----------|--------|
| ❌ ARIMA / SARIMA | É série temporal mas com componentes que ARIMA não captura bem. Prophet + XGBoost foi a alternativa aprovada. |
| ❌ K-Means puro | Não funciona para padrões deslocados no tempo. Usar DTW (`tslearn`). |
| ❌ Streamlit | Todo mundo usou ano passado. Diferenciação obrigatória. |
| ❌ Lock-in de cloud | Locaweb é cloud provider. Não amarrar a concorrente. |
| ✅ Apenas incidente PAI no KPI | Confirmado pela Locaweb. Filhos não entram. |
| ✅ Feriados via engineering | Dataset não tem coluna de feriado. Adicionar via `holidays` lib. |
| ✅ Docker para entrega | Facilita adoção pela Locaweb. |

---

## Os 3 diferenciais do produto

### 1. Morning briefing

**O que é:** resumo proativo entregue a cada manhã, com 3 blocos:
- **Ontem** — o que aconteceu (volume, distribuição, OLAs)
- **Hoje** — previsão de volume e risco
- **Ações sugeridas** — recomendações práticas

**Estrutura final (após mentoria Locaweb):**
- Tela mostra **resumo curto** (escaneável em 10 segundos)
- Botão "ver detalhes" abre **relatório completo** com gráficos e justificativas
- Texto gerado pela Claude API (custo precisa ser simulado para apresentação final)

**Diferencial:** ninguém no mercado faz briefing escrito automático sob medida. Datadog, Splunk, Dynatrace mostram dashboard — não escrevem texto contextualizado.

### 2. Detector de cascata *(DESCARTADO na Sprint 3 — ver Atualização no topo)*

**O que é:** monitora acúmulo de alertas pequenos (P4/P5) no mesmo produto/categoria que historicamente precedem falhas graves (P3/P2).

**Exemplo real (Locaweb):** disco em 90% (P4) → 95% (P3) → estourou (P2). Padrão confirmado na mentoria.

**Como funciona:** monitora janelas temporais por produto/categoria. Quando o volume de baixa prioridade ultrapassa threshold + tem histórico de escalada, dispara alerta.

**Diferencial:** baseado em padrão real validado pela Locaweb, não hipótese.

### 3. Score de saúde por produto

**O que é:** nota 0-100 para cada produto, calculada com base em:
- Volume de incidentes recente vs histórico
- Tendência (subindo/descendo)
- Severidade média
- Tempo de resolução
- Histórico de violação de OLA

**Apresentação:** ranking de produtos por score, com tendência (verde/amarelo/vermelho), drill-down explicando a composição da nota via SHAP.

**Diferencial:** explicabilidade — não só "produto X tem score 45", mas POR QUE.

---

## Estrutura do repositório (planejada)

```
notebooks/   → 01_eda, 02_features, 03_modelagem, 04_ola, 05_cluster, 06_shap
models/      → modelos .pkl salvos (gitignored)
data/        → raw (versionado) + processed (gitignored)
web/         → Django app (views.py, ml.py, services.py, templates/)
brand/       → identidade visual
sprints/     → entregáveis .pptx (versionados)
docker/      → Dockerfile, docker-compose.yml (Sprint 3+)
```

---

## Probabilidade de atingir KPI

**Decisão da mentoria Locaweb:** dashboard deve ter foco forte em probabilidade de atingir o KPI mensal.

**Lógica:** se logo no início do mês acontece quebra de OLA, a probabilidade de bater a meta cai drasticamente. Cronos precisa mostrar essa projeção condicional — "dado o que já aconteceu, qual a probabilidade de fechar o mês na meta?".

**Implementação técnica:** Prophet já dá intervalo de confiança. Combinar com simulação Monte Carlo para projeção do KPI cumulativo até o fim do mês.

---

## Dashboard — referência visual

Estilo de referência: **dashboards de consumo (TIM, Unifique)** — interativo, com 2-3 abas, não exagerado.

- Visão clara do "estado atual" no topo
- Gráficos de tendência
- Área de detalhamento com drill-down
- **Não** Power BI carregado de gráfico em todo lugar
- Foco em "o que eu preciso saber agora"

---

*Última atualização: 21/07/2026*

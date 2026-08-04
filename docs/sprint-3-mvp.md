# Sprint 3 — MVP Preliminar · documentação de trabalho

Documento vivo. Vai sendo preenchido conforme fechamos cada bloco da modelagem, e é a base do PPT da Sprint 3. Cada seção grande aqui vira um ou mais slides. Não resumir para caber: se está longo, é porque tem trabalho a mostrar.

**Equipe:** Ana Beatriz Costa de Oliveira · Hygor Abrantes · Igor Vignola — Super Data Bros · 2TSCOA

---

## Anomalia de setembro/2025: causa provável

### Distribuição temporal do volume

O dataset cobre janeiro/2023 a dezembro/2025. O volume mensal é desigual ao longo do período:

| Período | Volume/mês |
|---|---|
| 2023 (ano inteiro) | ~10 |
| 2024 (ano inteiro) | ~52 |
| jan–ago/2025 | ~3,5 mil |
| set/2025 | 21,6 mil |
| out/2025 | 23,0 mil |
| nov/2025 | 21,5 mil |
| dez/2025 | 27,3 mil |

2023 e 2024 somam 732 incidentes. Em 2025 o volume mensal fica na casa dos milhares. Em setembro/2025 passa de ~4 mil para ~21,6 mil (aumento de cerca de 5×) e permanece nesse patamar até dezembro. A Locaweb sinalizou essa quebra na mentoria e pediu a análise da causa.

### Investigação

Comparação entre agosto e setembro/2025, por dimensão:

| Dimensão | Agosto | Setembro |
|---|---|---|
| Volume total | 3.996 | 21.561 |
| Origem: Monitoramento | 2.404 | 20.008 |
| Origem: Manual | 1.592 | 1.553 |
| Status "Sem Intervenção" | 47 | 17.838 |
| Itens de Configuração vistos pela 1ª vez no mês | 458 | 1.693 |
| Descrição mais frequente | disco cheio | "Problem: Check Application Monitoring" (6.590) |

### Causa provável

O aumento concentra-se na origem Monitoramento (2.404 para 20.008 entre agosto e setembro). A abertura Manual permanece em torno de 1,5 mil por mês no ano. Três indicadores acompanham o mesmo padrão: o status "Sem Intervenção" passa de 47 para 17.838; cerca de 1,7 mil Itens de Configuração aparecem pela primeira vez no mês; e a descrição mais frequente passa a ser "Problem: Check Application Monitoring".

Os três indicadores que disparam apontam para expansão do monitoramento automático em setembro/2025, sobre ativos que antes não eram monitorados, enquanto a abertura manual permanece estável. O aumento reflete mais eventos capturados, não necessariamente mais falhas na operação. Todos esses números são impressos em célula no `notebooks/01_eda.ipynb`, seção 4.2.

### Efeito na modelagem

Pelo dicionário de dados, incidente com status "Sem Intervenção" não entra no cálculo do KPI. Como o aumento de setembro é majoritariamente desse tipo, a série elegível ao KPI permanece estável no período:

| Mês | Volume total | Volume elegível ao KPI |
|---|---|---|
| ago/2025 | 3.996 | 2.330 |
| set/2025 | 21.561 | 2.324 |
| dez/2025 | 27.321 | 1.423 |

Os modelos usam a série elegível ao KPI, e não o volume total. Isso remove a variação de setembro do treino. O dicionário observa que incidentes fora do KPI podem afetar os que entram; testamos a hipótese de escalada/cascata e não a confirmamos (ver "Testado e descartado").

---

## Decisão de modelagem (alvo e escopo)

Definida em 20–21/07/2026, com base nos três documentos oficiais (apresentação, dicionário de dados, template da Sprint 3) e na investigação acima.

**Foco em P2 e P3, separados.** A apresentação (pág. 7) exige a previsão de volume "por prioridade (P2 e P3 obrigatórias)". Além de obrigatórias, são as únicas prioridades relevantes ao KPI: o dicionário define que só P1, P2 e P3 entram no KPI, e P1 tem 1 único registro no dataset. As metas anuais (de quebra de OLA e de volume) existem apenas para P2 e P3. Modelamos as duas em séries separadas porque os volumes são muito diferentes (P2 ~14/dia, P3 ~55/dia) e uma série única faria o P2 desaparecer dentro do P3. O total exibido na interface é a soma das duas previsões.

**Modelos:**
- Prophet prevê o volume diário elegível ao KPI (D+1 e D+7), uma série para P2 e outra para P3.
- Risco de estouro de OLA por incidente: problema de classificação. A regressão logística é o modelo escolhido. Medido em 03/08/2026 no corte out-of-time (treino até 30/09, teste de outubro a dezembro com 50 quebras em 5.183 incidentes): ROC AUC **0,8693** contra 0,8679 do XGBoost, empate dentro do ruído; PR-AUC **0,2958** contra 0,2526, vantagem de 17% para a logística. A leitura principal é a triagem/ganho (os 20% de maior risco concentram **72%** das quebras), não o AUC isolado. O XGBoost com `scale_pos_weight` piora tudo e prevê 1.007 quebras onde houve 50, o que inviabiliza a projeção do KPI.
- Projeção de atingimento dos KPIs: cálculo de taxa sobre a previsão, comparado às metas anuais por prioridade (ver "Régua de meta").

**Dimensão categoria/produto/IC.** A apresentação cita "por categoria, produto ou item de configuração" — o "ou" indica dimensão secundária, não obrigatória. É coberta pelo modelo de risco (produto e categoria entram como features), pela saúde por produto e pela watchlist de itens de configuração. Não é atendida por previsão de volume por produto, porque o volume por produto por dia é esparso demais para uma série confiável.

**Filtro de elegibilidade:** campo oficial `Entrou para KPI? = SIM`, que já codifica `Incidente Pai` vazio, prioridade 1/2/3 e `Status ≠ Sem Intervenção`. Observação: não é a origem "Monitoramento" que exclui do KPI — 9.529 incidentes de origem Monitoramento entram no KPI; a exclusão vem da regra acima.

---

## Escopo temporal: temos ~1 ano de dado denso

Achado central para a previsão. Contando apenas os incidentes elegíveis ao KPI, por ano de abertura:

| Ano | Elegíveis ao KPI |
|---|---|
| 2023 | 87 |
| 2024 | 357 |
| 2025 | 25.156 |

98% dos elegíveis estão em 2025; 2023 e 2024 somam 444 (desprezível). O padrão sugere que o registro de KPI passou a ser usado de fato em 2025.

Consequência para o Prophet: há dado para aprender o padrão de dia da semana (dia útil × sábado/domingo/feriado), que o modelo captura bem com um ano; não há dado para aprender padrão anual (exigiria 2–3 anos), então a sazonalidade anual fica desligada. Decisão: treinar em 2025, sazonalidade semanal ligada e anual desligada — o alcance honesto do que o dado permite.

## Régua de meta por prioridade (ano de 2025)

As duas metas anuais do dicionário, com a posição real fechada em 2025:

| Prioridade | Quebras de OLA | Faixa da meta | Atingimento | Volume elegível | Faixa da meta | Atingimento |
|---|---|---|---|---|---|---|
| P2 | 42 | 40–45 | 75% | ~5.150 | 4.585–5.388 | 125% |
| P3 | 196 | < 201 | 150% | ~20.000 | 19.489–22.116 | 125% |

Leitura: o volume ficou confortável nas duas prioridades (125%); a pressão está nas quebras de P2, no patamar de 75%. É esta régua, com as regras exatas da Locaweb, que o dashboard usa para mostrar domínio do fluxo deles.

## Previsão de volume — validação e resultado

**Metodologia.** Séries diárias de P2 e P3 (elegíveis ao KPI, 2025). Comparação sempre contra baselines simples — sazonal-7 (repete a última semana por dia da semana) e média-7 (média dos últimos 7 dias) — medindo o MAE (erro médio absoluto). Duas validações: corte out-of-time (treino jan–set, teste out–dez) e **rolling backtest** (re-treina a cada semana e prevê D+1 a D+7, com o erro medido por horizonte — reproduz o uso real).

**Modelo.** Prophet com sazonalidade semanal, sazonalidade anual desligada (~1 ano de dado), feriados nacionais (`add_country_holidays('BR')`) e banda de confiança de 80%; previsões limitadas a valores não-negativos.

**Modelo alternativo comparado.** Regressão linear sobre colunas (dia da semana, feriado, defasagens de 7 e 14 dias) — a mesma família da regressão logística que será usada no risco de OLA.

**Resultado (rolling backtest, MAE médio D+1–D+7):**

| Prioridade | Baseline sazonal-7 | Baseline média-7 | Prophet | Regressão de colunas | Melhor baseline | Ganho do Prophet |
|---|---|---|---|---|---|---|
| P3 (Média) | 11,3 | 18,2 | 11,8 | 12,7 | 11,3 | -4,5% |
| P2 (Alta) | 5,7 | 4,9 | 4,2 | 4,2 | 4,9 | +15,1% |

Os dois baselines aparecem de propósito: o mais forte muda conforme a série (sazonal-7 no P3, média-7 no P2), e comparar o modelo apenas com o baseline mais fraco inflaria o ganho.

- Em **P2**, os modelos (Prophet ≈ colunas, 4,2) superam os dois baselines. Comparação honesta: o melhor baseline do P2 é a média-7 (4,9), não o sazonal-7 (5,7), então o ganho é de **15% sobre o melhor baseline** e 26% sobre o mais fraco. Reportamos os 15%.
- Em **P3**, o melhor baseline (sazonal-7, 11,3) fica 4,5% abaixo do Prophet (11,8). É empate técnico, dentro do ruído do backtest, e indica que o baseline já está no teto do previsível. Reportamos o número em vez de escrever apenas "empatam".
- O horizonte importa pouco dentro de 7 dias — a previsão do D+7 é quase tão confiável quanto a do D+1, porque o sinal é o padrão semanal fixo.

**Conclusão.** Três métodos diferentes batem no mesmo teto — prova que o sinal previsível (semana + feriado) está totalmente capturado, e o resto é ruído que ninguém prevê. Não é limite da ferramenta, é limite do dado. O Prophet fica como modelo entregue pela faixa de confiança, tratamento de feriados e modelo único para as duas prioridades; a regressão de colunas confirma que ele não deixa desempenho na mesa.

## Verificações de robustez (29/07/2026)

Perguntas críticas levantadas na revisão adversarial do material, respondidas com o dado. O dossiê completo de defesa está em `docs/dossie-banca.md`.

### O volume prevê quebra de OLA? Relação fraca, e isso define o papel de cada modelo

Teste em 2025, apenas dias úteis (remove o efeito de fim de semana e feriado):

| Quartil de volume | Dias | Volume médio/dia | Quebras/dia | Taxa de quebra |
|---|---|---|---|---|
| Q1 (mais baixo) | 64 | 58,0 | 0,5 | 0,8% |
| Q2 | 69 | 79,6 | 0,7 | 0,9% |
| Q3 | 61 | 90,2 | 0,9 | 1,0% |
| Q4 (mais alto) | 61 | 110,0 | 0,8 | 0,7% |

Correlação volume × quebras por dia: r = +0,159 (p = 0,011), R² = 0,025.

Leitura: a relação é estatisticamente significativa e fraca. Dias de volume mais alto têm cerca de 60% mais quebras em absoluto (0,5 para 0,8 por dia), mas o volume explica apenas 2,5% da variação diária e a taxa de quebra permanece plana. **O volume dimensiona carga; não aponta qual incidente vai estourar.** Consequência de escopo: a previsão de volume sustenta planejamento de capacidade e projeção de atingimento da meta; o modelo de risco por incidente é o que responde "qual vai estourar", e portanto não é complementar, é a metade que fecha a proposta.

### A queda de novembro e dezembro é real, não censura de dados

O volume elegível cai de 2.126 (out) para 1.634 (nov) e 1.423 (dez), justamente dentro do período de teste. A hipótese de censura à direita (incidentes abertos perto do corte do arquivo ainda sem classificação final) foi verificada e **descartada**: o dataset está completo, com `Encerrado` preenchido em 100% dos 122.543 registros e último encerramento em 31/12/2025 23:45.

Duas causas reais explicam a queda:

| Recorte | 1 a 10 | 11 a 20 | 21 a 31 |
|---|---|---|---|
| Novembro | 562 | 516 | 556 |
| Dezembro | 589 | 529 | **305** |

1. **Parada de fim de ano.** O último terço de dezembro cai 45% contra o mesmo período de novembro (305 contra 556), padrão de freeze de mudanças e recesso.
2. **Diluição pela expansão do monitoramento.** A parcela elegível sobre o total despenca ao longo do ano: 58,3% em agosto, 10,8% em setembro, 7,6% em novembro, 5,2% em dezembro. O total sobe (27.321 em dezembro, o maior do ano) enquanto o elegível cai, porque o crescimento é todo de eventos automáticos que não entram no KPI.

Consequência para o modelo: treinado em janeiro a setembro, ele não tinha como antecipar essa mudança de nível. Isso responde por parte do erro no teste out-of-time e é um limite declarado, não um defeito de ajuste.

### Cobertura empírica da banda de 80%

Medição da fração de dias do período de teste (out a dez, 92 dias) em que o valor real caiu dentro da banda de confiança de 80%. Calculada na seção 4.10.1 do `notebooks/03_previsao_volume.ipynb`:

| Prioridade | Cobertura observada | Nominal | Leitura |
|---|---|---|---|
| P2 | entre 86% e 88% | 80% | calibrada, até conservadora |
| P3 | **entre 59% e 61%** | 80% | **subestima a incerteza** |

Observação metodológica: o ajuste do Prophet não é determinístico (a otimização parte de inicialização aleatória), então a cobertura oscila alguns pontos percentuais entre execuções. Por isso reportamos faixa, e não um valor único; o número exato de cada execução fica no output da célula. A conclusão é estável: P2 calibrada, P3 sub-cobrindo.

Leitura: em P2 a banda está bem calibrada. Em **P3 a banda subestima a incerteza**, e a causa é a mesma da seção anterior: a queda de nível de novembro e dezembro está fora do que o treino permitia prever, então o intervalo construído sobre jan a set fica estreito para o período. Encaminhamento: reportar a cobertura junto do MAE (a banda não é garantia), e reavaliar com re-treino contínuo, que é o modo de operação real do Cronos.

## Métricas de classificação do modelo de risco (03/08/2026)

Medição em corte out-of-time: treino até 30/09/2025, teste de outubro a dezembro com 5.183 incidentes e 50 quebras (0,96% de prevalência).

| Modelo | ROC AUC | PR-AUC | Quebras no top 50 | No top 518 | Quebras previstas |
|---|---|---|---|---|---|
| **Regressão logística** | **0,8693** | **0,2958** | **15** | 29 | **48,1** |
| XGBoost (padrão) | 0,8679 | 0,2526 | 14 | 29 | 54,3 |
| XGBoost com `scale_pos_weight` | 0,8492 | 0,2367 | 12 | 27 | 1.007,1 |

Quebras observadas no período: 50. Concentração nos 20% de maior risco: **72%** para a logística.

**Leitura.** No ROC AUC os dois primeiros empatam dentro do ruído. No PR-AUC, que é a métrica adequada a evento raro porque desconsidera a classe majoritária, a logística tem vantagem de 17%. A terceira linha mostra o efeito de balancear a classe: melhora nada e destrói a calibração, prevendo vinte vezes mais quebras do que ocorreram, o que inviabiliza a projeção de atingimento do KPI.

**Por que a acurácia não é reportada.** Com prevalência de 0,96%, um modelo que nunca sinaliza nada atinge 99,04% de acurácia, contra 90,16% do modelo no corte de 518. A métrica premia a inação e foi descartada. A avaliação usa matriz de confusão por corte, precisão, cobertura e a curva de ganho.

| Corte | Alarmes | Acertos | Precisão | Cobertura |
|---|---|---|---|---|
| Risco ≥ 50% (regra padrão) | 2 | 2 | 100,0% | 4% |
| Top 50 | 50 | 15 | 30,0% | 30% |
| Top 100 | 100 | 17 | 17,0% | 34% |
| Top 518 | 518 | 29 | 5,6% | 58% |

Onde cortar é decisão da operação, não do modelo: depende da capacidade diária da equipe. A entrega é a tabela acima. Referência: sem modelo, qualquer amostra de 518 incidentes conteria 0,96% de quebras; com o modelo, 5,6% — seis vezes mais.

Figuras: `07_curva_roc.png` e `08_curva_pr.png` em `notebooks/figures/04_risco_ola/`.

## A priorização funciona, e é por isso que ela não prevê (03/08/2026)

Ordenar a fila por prioridade — o comportamento padrão de qualquer ferramenta de ITSM — tem **ROC AUC de 0,4693**, abaixo do 0,5063 de uma fila aleatória. A ordenação oficial é pior que sortear.

A causa está no dado:

| Prioridade | Incidentes | Quebras | Taxa de quebra | Duração mediana |
|---|---|---|---|---|
| P2 — Alta | 5.159 | 42 | 0,81% | 1.577 |
| P3 — Média | 20.441 | 206 | 1,01% | 6.328 |

O P2 estoura menos que o P3 e é resolvido em um quarto do tempo. A priorização cumpre o que promete: o que recebe atenção é resolvido, e o que é resolvido não estoura. Consequentemente a prioridade não separa quem vai estourar, porque o caso prioritário já foi atendido. As quebras se concentram no P3 que ficou parado.

**Uso no deck.** Este é o argumento que justifica a existência do modelo de risco diante da pergunta "por que não basta olhar a prioridade?". Slide a produzir na seção do modelo de risco.

## Decisão: explicabilidade sem SHAP (30/07/2026)

A explicabilidade do modelo de risco é extraída **diretamente dos pesos da regressão logística**, sem SHAP.

**Fundamento.** Em modelo linear a contribuição calculada pelo SHAP tem forma fechada: é o peso da característica multiplicado pelo desvio do valor em relação à média. A ferramenta devolve, portanto, a mesma informação que a leitura direta dos coeficientes, sem acrescentar nada. SHAP existe para abrir modelos de caixa preta, como gradient boosting ou redes neurais, nos quais não há pesos observáveis e as interações estão implícitas.

**Consequência positiva.** A decisão fecha o ciclo do argumento que já sustentava a escolha do modelo: a regressão logística foi preferida porque empata com o XGBoost em desempenho e é interpretável. A explicabilidade sem intermediário é o benefício concreto dessa escolha. A posição defendida é a de **modelo interpretável por construção**, em vez de caixa preta acompanhada de explicação posterior, que sempre carrega o risco de não refletir fielmente o que o modelo fez.

**Quando SHAP seria necessário.** Caso o modelo entregue fosse o XGBoost, que permanece apenas como baseline de comparação.

**O que é entregue.** Para cada incidente, a contribuição de cada característica ao risco estimado, somando exatamente ao valor previsto. O SHAP foi usado uma única vez, em conferência interna, para validar a implementação da conta; não integra a entrega.

## Testado e descartado (e por quê)

Registrado para honestidade e para não repetir caminho já verificado.

- **Detector de cascata** (P4/P5 que escalam para P3/P2): testado e não sustentado no dado. 87% das quebras de OLA são de incidentes isolados; a taxa de "escalada" observada (21%) ficou abaixo do esperado por acaso (~60%).
- **Padrão de acúmulo** (a hipótese descrita pela Locaweb na mentoria): testado em 29/07/2026 e sem suporte na base. Medindo o backlog diário de elegíveis abertos e não resolvidos, em dias úteis, a correlação com quebras é levemente negativa e fraca (r = -0,139, p = 0,027; Spearman -0,115, p = 0,067), e se mantém com defasagem de 1 a 3 dias. O quartil de maior backlog (611 em média) apresenta menos quebras por dia (0,5) que o de menor (70 em média, 0,7). Ressalva honesta: o resultado diz que o backlog agregado por dia não prevê quebra na base disponível, não que o acúmulo seja irrelevante na operação; um efeito por equipe ou por capacidade instalada não é observável, pois esses campos não existem no dataset.
- **Clusterização por série temporal** (TimeSeriesKMeans + DTW): silhueta ~0,13, sem estrutura de grupos real; um k-means por volume separa melhor (~0,72), mas é agrupamento trivial por tamanho. O requisito de "classificação ou clusterização" é atendido pelo classificador de risco.
- **Sugestão de realocação de equipe:** especulativa (não há capacidade/turno das equipes no dado). Mantém-se a carga por equipe de forma descritiva.

---

## EDA — demais achados (notebook 01, seções 4.3–4.6)

- **Sazonalidade (4.3):** na série elegível ao KPI de 2025, os dias úteis têm volume parecido entre si (média de 84/dia, variando de 77 a 87 conforme o dia); sábado (42), domingo (27) e feriado (29) ficam abaixo. A variação separa dia útil de dia não útil, não um dia específico da semana. Orienta as features de calendário (`dia_semana` + `is_feriado`).
- **Distribuição operacional (4.4):** P4 (52,9%) e P3 (34,1%) concentram o volume; P2 é 12,8%. 65,6% fecham como "Sem Intervenção" e 85,1% vêm de Monitoramento.
- **Produtos e grupos (4.5):** o Team14 concentra 75,7% do volume; entre produtos preenchidos, lhco, lsin e lcem lideram.
- **Violações de OLA (4.6):** 248 violações (0,97% dos elegíveis), concentradas em P3 (206), nos times Team11 e Team09, e nos produtos lsin e lhco. É a variável-alvo do modelo de risco.

## Estrutura operacional N1/N2 e o preenchimento de produto (aprofundamento do 4.5)

Ao observar a concentração no Team14 (75,7%) e o produto preenchido em apenas 36% dos registros, investigamos as causas.

- **Preenchimento de produto tem padrão claro:** é praticamente completo em incidentes manuais (99,4%), encerrados (89–98%) e elegíveis ao KPI (**99,8%**), e raro em "Sem Intervenção" (5,7%). Caiu a partir de setembro (de ~95% para ~11%) junto com a expansão do monitoramento. **Consequência: como a série modelada é a elegível ao KPI, o produto está presente em 99,8% dos casos — a ausência de produto no volume total não afeta os modelos.**
- **Team14 = primeiro nível (N1):** 95,5% de origem automática, 81,5% "Sem Intervenção", só 9,7% entram no KPI e apenas 10 violações de OLA. Absorve a enxurrada de alertas automáticos.
- **Equipes especializadas (N2) carregam o risco:** Team11 e Team09 têm volume menor, quase todo manual e classificado, e concentram as violações de OLA — o Team11 responde por 46% das violações com apenas 8% do volume.
- **Insight de decisão:** o risco não acompanha o volume. Atenção preventiva deve ir para o gargalo dos N2, não para o volume do N1.

## Validação do terreno de modelagem (testes de pipeline, 20/07/2026)

Testes descartáveis para confirmar que os dados e as bibliotecas funcionam de ponta a ponta. Não são os modelos finais.

- **Dados suficientes:** série diária de 2025 com P2 em 14,1/dia (5.159 no ano) e P3 em 54,8/dia (19.997), sem dias vazios. Antes de 2025 há apenas 444 elegíveis (desprezível).
- **Prophet:** treina nos 365 dias e gera previsão D+1..D+7. Ponto a tratar: a previsão pode sair negativa em dias de baixo volume; será preciso restringir a não-negatividade.
- **XGBoost (volume):** roda; erro apenas ilustrativo nesta fase.
- **XGBoost (risco de OLA):** roda e mostra sinal (AUC ~0,81 em teste bruto, com features mínimas). Base desbalanceada (248 positivos) — avaliação por precisão/recall. *Substituído pela medição definitiva de 03/08/2026: ver "Decisão de modelagem" acima e a seção 10 do laboratório de risco.*

## Deck da sprint: estado atual (29/07/2026)

O deck construído está em `prototipos/slides/mvp/deck/viewer.html` (seta para baixo troca slide, seta lateral troca variação). Cobre as duas seções já fechadas: Análise Exploratória e Previsão de Volume. Os slides padrão do template (título, equipe, contextualização, problema, proposta, arquitetura, gestão ágil e Kanban, encerramento) serão montados na etapa de PPT e não estão neste deck.

| # | Slide | Variações disponíveis |
|---|---|---|
| 1 | Divisória · Análise Exploratória | 1 |
| 2 | Panorama da operação | 1 |
| 3 | O filtro da meta de OLA | 3 (gráfico real, funil, fluxo) |
| 4 | Anomalia · o problema | 2 |
| 5 | Anomalia · a causa | 3 (gráfico real, linha, tabela) |
| 6 | Escopo temporal · a descoberta | 3 |
| 7 | Distribuição operacional | 2 |
| 8 | Sazonalidade | 3 |
| 9 | As duas séries · P2 e P3 | 2 |
| 10 | Estrutura N1 e N2 | 1 |
| 11 | Violações de OLA · o alvo | 1 |
| 12 | Hipóteses descartadas | 1 |
| 13 | Divisória · Previsão de Volume | 1 |
| 14 | As decisões de modelagem | 1 |
| 15 | Como validamos | 2 |
| 16 | Resultado · o modelo funcionando | 1 |
| 17 | Resultado · comparação de erro | 3 |
| 18 | O que o volume prevê (e o que não) | 1 |
| 19 | Conclusão | 1 |

Nos slides com gráfico, a variação A é sempre a **exportação real do matplotlib** gerada nos notebooks, para que o visual seja auditável e não pareça ilustração. Regras de linguagem visual em `memory/deck-mvp-v2-linguagem.md`.

### Slides ainda a produzir (dependem das entregas seguintes)

- Modelo de risco de OLA: setup, resultado com leitura por triagem, e explicabilidade direto dos pesos do modelo (ver decisão abaixo).
- Régua de meta por prioridade e projeção de atingimento do KPI.
- Saúde por produto.
- MVP nas telas, com a saída real dos modelos.
- Fontes de dados e pipeline (item pedido pelo template).

# Plano do livro — conceitos por trás do Cronos

Livro de estudo para o Igor. Objetivo declarado: **entender os conceitos bem o suficiente para saber o que pedir**, não decorar comando. Cada capítulo sai do que a gente realmente aplicou nos sete notebooks, sobe para o conceito abstrato, desce para um exemplo do mundo real e volta para o Cronos com número de verdade.

**Fonte de referência de formato:** `completo_conteudo.pdf` (livro de biomecânica). Mesmo esqueleto editorial, paleta e caixas laterais adaptadas.

---

## 0. Decisões travadas (06/08/2026)

| Item | Decisão |
|---|---|
| Matemática | fórmula aparece, sempre seguida da leitura em português ("some X, divida por Y"). Sem notação formal pesada. |
| Escopo | o que aplicamos **+ os vizinhos que descartamos**: SARIMA, LSTM, DTW, SMOTE / `scale_pos_weight`, SHAP, modelos de contagem (Poisson). Cada descarte com o motivo medido. |
| Tamanho | 30 capítulos, ~150 páginas |
| Ritmo | entrega **por parte**. Partes I+II primeiro, revisão de tom, depois o resto. |
| Paleta | azul-noite `#122A40` + bronze `#95681F` sobre creme `#F8F6F0` |
| Formato | HTML único paginado, imprimível em PDF (Ctrl+P) |
| Layout | **sem coluna lateral.** Notas viram caixas no meio do texto; figuras usam a largura toda (484 px) |
| Paginação | automática por JS: mede cada bloco, parte parágrafo entre páginas e faz caixa/figura "flutuar" para a página seguinte puxando o texto para fechar a atual |

### Estado da produção — CONCLUÍDO

| Bloco | Situação |
|---|---|
| Motor de paginação + sumário automático | pronto (sumário também pagina medindo) |
| Verificador de layout (`livro.html#check`) | pronto — texto vazando de SVG (com transform) e branco excessivo |
| Parte I · caps I–III · O terreno | pronto |
| Parte II · caps IV–VIII · Olhar antes de modelar | pronto |
| Parte III · caps IX–XIV · Prever o que vem | pronto |
| Parte IV · caps XV–XVIII · Apontar o caso | pronto |
| Parte V · caps XIX–XXIII · Medir direito | pronto |
| Parte VI · caps XXIV–XXVII · Costurar | pronto |
| Parte VII · caps XXVIII–XXX · O rigor e o pedido | pronto |

**157 páginas de PDF · 147 páginas numeradas · 30 capítulos · 29 figuras.**
Verificação final: zero texto vazando de figura.

### Arquivos

- `livro.html` — fonte única. Abre no navegador, pagina sozinho.
- `livro.pdf` — gerado a partir dele, 6,875 × 10,3125 pol.
- `livro.html#check` — relatório de layout.

### Regras de figura (a partir da Fig. 6.1)

- Gráfico completo, com grade, marcas de escala nos dois eixos, título de eixo e quadro de leitura dos pontos-chave. Não é ícone, é plot.
- Todo rótulo de gráfico leva halo cor de papel (`paint-order:stroke`), para permanecer legível se alguma linha passar por baixo. Exceção: texto dentro de forma escura recebe a classe `fg-in`, que remove o halo.
- Números do gráfico saem sempre de consulta à base, nunca estimados. Figura esquemática precisa dizer isso dentro dela.
- Rodar `livro.html#check` depois de cada figura nova.

### Exemplos

Todo capítulo tem uma caixa **Na vida real** com exemplo genérico e sem TI (extrato bancário, conta de luz, apps do celular, contador de passos, comprar apartamento), além do exemplo do Cronos na caixa **No Cronos**.

### Gerar o PDF

```
chrome --headless --disable-gpu --virtual-time-budget=12000 \
  --no-pdf-header-footer --print-to-pdf=livro.pdf livro.html
```

Números usados nos capítulos I–X, todos conferidos contra a base em 06/08/2026:
volume médio por dia da semana com IC95; Pareto de ativos (125 ativos com quebra, top 30 = 61,7%);
tempo até resolução (média 221,5h, mediana 1,2h, 7,2% acima da média); volume mensal total contra elegível (set: 3.996 → 21.561 no total, 2.330 → 2.324 no elegível).

Dois acréscimos combinados fora do pedido original:

1. **Capítulo XXX "Da pergunta ao método"** — tabela de decisão pergunta → técnica. É a página que responde direto ao objetivo do livro.
2. **Os erros reais do projeto viram conteúdo**, não rodapé: o 26% que virou 15%, o `scale_pos_weight` prevendo 1.007 quebras onde houve 50, a banda de 80% que cobre 60% no P3, o filtro de elegibilidade que devolvia 107.416 em vez de 25.600.

---

## 1. O que muda em relação ao livro de referência

| Item | Livro de biomecânica | Este livro |
|---|---|---|
| Finalidade | passar na prova | saber o que pedir |
| Paleta | vinho + dourado sobre creme | azul-noite + bronze sobre creme |
| Caixa "CAI NA PROVA" | o que o professor cobra | **COMO PEDIR** — a frase pronta pra me mandar |
| Caixa "MEMORIZE" | mnemônico | **GLOSSÁRIO** (margem) — o termo em uma linha |
| Caixa "EXEMPLO" | exemplo do slide | **EXEMPLO** (margem) — analogia curta |
| — | não existia | **NO CRONOS** — como aplicamos, com o número real do notebook |
| — | não existia | **NA VIDA REAL** — o mesmo conceito fora de TI |
| Caixa "ATENÇÃO" | pegadinha de prova | onde a intuição erra |
| "REVISÃO RÁPIDA" | fecha capítulo | mantida, fecha capítulo |

**Tom.** Frase curta, primeira pessoa do plural quando falo do que a gente fez, segunda pessoa quando explico. Sem "elevar", "robusto", "poderoso", "no cenário atual". Sem lista de três por reflexo. Sem travessão decorativo. Número sempre com a origem colada nele.

---

## 2. Sumário proposto

**7 partes · 27 capítulos · estimativa de 140 a 160 páginas** no formato do livro de referência (4 a 6 páginas por capítulo).

### PARTE I · O terreno

| # | Capítulo | O conceito | Exemplo real | No Cronos |
|---|---|---|---|---|
| I | Dado, informação e modelo | o que é modelar; modelo como simplificação útil | mapa do metrô não é a cidade | 122.543 linhas viram 2 modelos e 1 nota |
| II | Descrever, prever, decidir | os três andares da análise; por que a maioria dos projetos para no primeiro | contabilidade × orçamento × decisão de investir | AED descreve, Prophet prevê, briefing decide |
| III | A base e o recorte que define tudo | granularidade, tipagem, cardinalidade, população-alvo | pesquisa eleitoral: quem entra na amostra | `Entrou para KPI? = SIM` → 25.600 de 122.543; o filtro errado devolvia 107.416 |

### PARTE II · Olhar antes de modelar

| # | Capítulo | O conceito | Exemplo real | No Cronos |
|---|---|---|---|---|
| IV | Para que serve a análise exploratória | AED como fase de decisão, não de enfeite; o que se procura | médico pede exame antes de receitar | a AED matou a cascata e definiu o alvo |
| V | Distribuição, média e a tirania da cauda | média × mediana × percentil; assimetria; por que a média mente | salário médio × salário mediano no Brasil | duração dos P3: mediana 39,6h com cauda longa |
| VI | Concentração e Pareto | poucos itens explicam muito; cardinalidade alta | 20% dos produtos, 80% da receita | 30 ativos = 61,7% das quebras; Team11 = 46% com 8% do volume |
| VII | Sazonalidade e efeito calendário | ciclo semanal, feriado, recesso; sazonalidade × tendência | trânsito na sexta; varejo em dezembro | sábado 41,9 vs útil; recesso derruba 45% no fim de dezembro |
| VIII | Mudança de regime e anomalia | quando a série muda de patamar e o modelo não tem como saber | mudança de metodologia do IBGE no meio da série | setembro/2025: share elegível cai de 58,3% para 10,8% |

### PARTE III · Prever o que vem

| # | Capítulo | O conceito | Exemplo real | No Cronos |
|---|---|---|---|---|
| IX | O que é uma série temporal | ordem importa; autocorrelação; por que não dá pra embaralhar | preço de ação, temperatura, consumo de energia | volume diário elegível por prioridade |
| X | Decomposição: tendência, sazonalidade, resíduo | separar o previsível do ruído | conta de luz: consumo base + verão + o mês estranho | componentes do Prophet, P2 e P3 |
| XI | O baseline — a régua que todo modelo tem que vencer | ingênuo, média móvel, sazonal ingênuo; por que é obrigatório | "amanhã igual hoje" acerta muito | sazonal-7 empata com Prophet no P3 (11,25 × 11,76) |
| XII | Prophet por dentro | modelo aditivo: tendência + sazonalidade + feriado; o que ele não faz | — | 365 pontos, semanal ligada, anual desligada, feriados BR |
| XIII | Erro e incerteza | MAE, RMSE, MAPE, viés com sinal; intervalo de predição e cobertura empírica | margem de erro de pesquisa eleitoral | MAE P2 4,2 e P3 11,8; banda de 80% cobre 86–88% no P2 e 59–61% no P3 |
| XIV | Validação temporal | out-of-time, rolling backtest, por que validação aleatória mente em série | testar estratégia de investimento no passado | 29 origens a cada 4 dias, horizonte 7 |

### PARTE IV · Apontar o caso

| # | Capítulo | O conceito | Exemplo real | No Cronos |
|---|---|---|---|---|
| XV | Classificação: prever um rótulo | supervisionado, alvo binário, probabilidade × decisão | e-mail é spam ou não | `KPI Violado?` como alvo |
| XVI | Features — transformar o mundo em coluna | one-hot, escala, imputação, categórica de alta cardinalidade | ficha de crédito | prioridade, produto, categoria, origem, item de configuração, hora, dia da semana |
| XVII | Vazamento — o erro que só aparece em produção | usar informação do futuro sem perceber | prever aprovação usando a nota final | `Duração`, `Resolvido`, `Encerrado` e `Status` proibidos: a violação é derivada de duração |
| XVIII | Regressão logística | a reta que vira probabilidade; coeficiente, odds ratio, por que ela é explicável | escore de crédito do banco | modelo escolhido; ROC AUC 0,869 |

### PARTE V · Medir direito

| # | Capítulo | O conceito | Exemplo real | No Cronos |
|---|---|---|---|---|
| XIX | Evento raro e por que acurácia mente | prevalência, classe desbalanceada, o classificador burro que acerta 99% | teste de doença rara | prevalência 0,97%; "nunca sinaliza" dá 99,04% de acurácia |
| XX | Matriz de confusão e o limiar de corte | falso positivo × falso negativo; precisão × cobertura; o corte é decisão de negócio | radar de velocidade: multar quem? | corte de 518 casos; 15 das 50 quebras nas 50 primeiras posições |
| XXI | ROC, AUC e PR-AUC | o que cada curva mede; qual vale em evento raro | triagem em pronto-socorro | PR-AUC 0,296 (logística) × 0,253 (XGBoost) — 17% de vantagem |
| XXII | Curva de ganho e a leitura por triagem | ordenar em vez de classificar; ganho sobre a régua trivial | cobrança: ligar para quais 10% da carteira | ganho de 29% a 150% sobre a melhor regra simples |
| XXIII | Calibração e explicabilidade | probabilidade que quer dizer o que diz; decompor a pontuação | previsão do tempo: 70% de chuva significa o quê | 48,1 quebras previstas × 50 observadas (erro 3,8%); calibrado até 5%, conservador acima |

### PARTE VI · Costurar

| # | Capítulo | O conceito | Exemplo real | No Cronos |
|---|---|---|---|---|
| XXIV | Aprendizado não supervisionado e clusterização | agrupar sem rótulo; k-means, DTW, silhueta; quando não há grupo | segmentação de clientes | DTW descartado, silhueta ~0,13 |
| XXV | Quando o modelo complexo não paga | árvore, ensemble, XGBoost; complexidade × explicabilidade × dado disponível | — | XGBoost empata em AUC e perde em PR-AUC; `scale_pos_weight` prevê 1.007 quebras onde houve 50 |
| XXVI | Índice composto — construir uma nota | normalizar, ranquear, pesar, testar redundância e sensibilidade | IDH, nota do Enem, score de crédito | score de saúde por produto: 5 componentes, peso igual, um descartado por correlação 0,85 |
| XXVII | Compor modelos sem extrapolar nenhum | decomposição em parcelas; propagar incerteza | orçamento: realizado + comprometido + previsto | projeção do KPI = realizado + fila aberta + volume futuro; erro < 7% em 9 de 10 datas |

### PARTE VII · O rigor e o pedido

| # | Capítulo | O conceito | Exemplo real | No Cronos |
|---|---|---|---|---|
| XXVIII | Hipótese, teste e o valor do resultado negativo | correlação × causalidade, r, R², p-valor, confundidor, controle | remédio que "funciona" porque quem toma já é mais saudável | volume × quebra: r = 0,159, R² = 0,025; acúmulo do mentor: r = −0,139 |
| XXIX | Reprodutibilidade | pipeline, semente, notebook executado, número com célula que o produz | receita que qualquer um refaz | Prophet não é determinístico: cobertura reportada em faixa |
| XXX | Da pergunta ao método — o mapa de pedidos | tabela de decisão: que pergunta pede que técnica | — | fecha o livro; é a página que responde "o que peço ao Claude" |

> Observação: com os capítulos XXIX e XXX a conta fecha em **30 capítulos**, não 27. Se preferir enxugar, XXIX entra como seção de XXX.

---

## 3. Elementos visuais previstos

Desenhos em SVG feitos à mão, no estilo das figuras do livro de referência (traço fino, dois tons, rótulo em bronze). Estimativa de 22 a 26 figuras:

- distribuição assimétrica com média e mediana marcadas
- curva de Pareto dos 30 ativos
- série com os três componentes separados (tendência, semanal, resíduo)
- as três réguas de baseline sobre a mesma série
- janela deslizante do rolling backtest (o desenho que mais ajuda)
- reta × sigmoide: por que regressão linear não serve pra probabilidade
- matriz de confusão anotada com custo de cada quadrante
- ROC e PR lado a lado sobre o mesmo modelo
- curva de ganho com a diagonal do acaso
- diagrama de vazamento: linha do tempo do incidente e o que existe em cada instante
- as três parcelas da projeção empilhadas
- quadrante de risco latente do score de saúde
- mapa final pergunta → método

---

## 4. Formato de entrega

HTML único, paginado, imprimível em PDF. Sem dependência externa: fonte do sistema, SVG inline, tudo em um arquivo. Abre no navegador e vira PDF por Ctrl+P.

---

## 5. Ordem de produção

1. Aprovação do mockup e da paleta
2. Parte I e II (base conceitual) — o trecho mais fácil de errar o tom, vale revisar cedo
3. Parte III (séries) — mais denso, mais figura
4. Partes IV e V (classificação e métrica) — o coração
5. Partes VI e VII
6. Passada de humanizer no texto inteiro
7. Conferência de todo número contra a célula do notebook que o produz

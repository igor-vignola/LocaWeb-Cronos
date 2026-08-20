# Dossiê de banca · Cronos MVP (Sprint 3)

Preparação para a defesa do MVP Preliminar. Reúne as perguntas prováveis da banca com resposta preparada e evidência, a matriz de conformidade contra os documentos oficiais, as inconsistências confirmadas na auditoria, as fraquezas conhecidas e o plano de ação priorizado.

**Versão:** v2 (substitui o v1 de 29/07/2026) · **Produzido em:** 29/07/2026 · **Entrega da sprint:** 23/08/2026

**Método.** Revisão adversarial em quatro perfis de avaliador (professor de machine learning, gestor de operações no perfil do mentor Locaweb, avaliador de metodologia acadêmica e avaliador cético), somada a cinco auditorias de artefato (documentos de contexto, notebooks, deck, telas, skills) e a uma matriz de conformidade construída a partir da leitura integral das três fontes oficiais: apresentação Locaweb (12 páginas), Dicionário de Dados v2 e `03Template_MVP_Preliminar`. Os achados de severidade alta e média foram verificados um a um contra o dado e contra o arquivo citado; os de severidade baixa entram como lista de higiene, sem verificação individual.

**O que mudou em relação ao v1.**

1. O v1 declarava explicitamente que dois perfis de banca e as auditorias de artefato tinham ficado de fora por limite de orçamento. Essa lacuna foi fechada: os quatro perfis rodaram e as cinco auditorias rodaram.
2. Entram três seções novas: a matriz de conformidade da Sprint 3 (51 exigências mapeadas), o inventário de inconsistências confirmadas por artefato e a lista de higiene de severidade baixa.
3. A seção 1 (análises de dado) foi preservada integralmente, com todos os números. Ela continua sendo o ativo mais valioso do dossiê.
4. A seção de perguntas foi reorganizada em quatro eixos e ampliada: as perguntas equivalentes entre perfis foram unificadas na formulação mais dura, e entraram as provocações que o v1 não previa (procedência de números de tela, contradição entre gráfico e texto, denominadores misturados, ausência de valor em reais, custo de operação).
5. Cinco respostas preparadas do v1 foram contraditadas pela auditoria. Nenhuma foi apagada: cada uma recebeu um **aviso de contradição** inline, com o número que a derruba e a formulação que passa a valer.

---

## 1. Análises novas produzidas nesta revisão

Quatro perguntas críticas que antes não tinham resposta, agora respondidas com o dado. As quatro estão implementadas na seção 4.10 do `notebooks/03_previsao_volume.ipynb` (4.10.1 cobertura da banda, 4.10.2 censura, 4.10.3 volume contra quebra, 4.10.4 padrão de acúmulo), a partir de `data/interim/incidentes_kpi.parquet` e do dataset oficial. O notebook está comitado **executado, com as saídas preservadas** (52 células, zero erros).

> **Nota de reprodutibilidade (resolvida em 29/07/2026).** Durante a auditoria os revisores leram o notebook 03 em momentos diferentes e divergiram sobre o estado dele: um viu as saídas, o outro pegou o arquivo recém-gerado, ainda sem executar. Situação atual: o 03 foi reexecutado do início ao fim e está comitado com as saídas preservadas. O teste do padrão de acúmulo (seção 1.2), que antes existia apenas como texto, virou a célula da seção 4.10.4. Todo número desta seção tem agora a célula que o produz.

### 1.1 O volume prevê quebra de OLA? (a pergunta mais perigosa)

Se prever volume não reduz quebra de OLA, o modelo entregue não sustenta a promessa do produto. Testamos a relação em 2025, apenas em dias úteis (para remover o efeito de fim de semana e feriado):

| Quartil de volume | Dias | Volume médio/dia | Quebras/dia | Taxa de quebra |
|---|---|---|---|---|
| Q1 (mais baixo) | 64 | 58,0 | 0,5 | 0,8% |
| Q2 | 69 | 79,6 | 0,7 | 0,9% |
| Q3 | 61 | 90,2 | 0,9 | 1,0% |
| Q4 (mais alto) | 61 | 110,0 | 0,8 | 0,7% |

Correlação volume × quebras por dia: **r = +0,159** (p = 0,011), **R² = 0,025**.

**Leitura honesta:** a relação existe e é estatisticamente significativa, mas é fraca. Dias de volume mais alto têm cerca de 60% mais quebras em termos absolutos (0,5 para 0,8 por dia), porém o volume explica apenas **2,5% da variação** de quebras diárias, e a taxa de quebra permanece plana (0,7% a 1,0%). Ou seja: **o volume dimensiona carga, não aponta qual incidente vai estourar.** Vale notar, e dizer antes que a banca note, que a relação não é monotônica: Q3 (0,9) e Q4 (0,8) ficam praticamente empatados, o que reforça a leitura de efeito fraco.

**Consequência para a defesa:** este resultado reposiciona os dois modelos com precisão. A previsão de volume serve para planejamento de capacidade e para a projeção de atingimento da meta anual. O modelo de risco por incidente é o que responde "qual vai estourar", e por isso **não é um complemento, é a metade que fecha a promessa**. Assumir isso na apresentação é mais forte do que deixar a banca descobrir.

### 1.2 O padrão de acúmulo descrito pela Locaweb na mentoria

O mentor descreveu um padrão de acúmulo derrubando o OLA. A hipótese de cascata (P4/P5 escalando) já havia sido refutada, mas o acúmulo em si nunca tinha sido testado. Medimos o backlog diário (incidentes elegíveis abertos e não resolvidos no fim de cada dia), em dias úteis:

| Quartil de backlog | Dias | Backlog médio | Quebras/dia |
|---|---|---|---|
| Q1 (mais baixo) | 65 | 70,4 | 0,7 |
| Q2 | 65 | 205,3 | 0,8 |
| Q3 | 61 | 297,4 | 0,8 |
| Q4 (mais alto) | 64 | 611,0 | 0,5 |

Correlação backlog × quebras: **r = -0,139** (p = 0,027); Spearman -0,115 (p = 0,067). Também testada com defasagem de 1 a 3 dias, com o mesmo sinal negativo fraco.

**Leitura honesta:** não encontramos suporte para o padrão de acúmulo na forma como o medimos. A relação é levemente negativa e fraca, no limite da significância. Não afirmamos que o acúmulo é irrelevante na operação: afirmamos que o backlog agregado por dia não prevê quebra na base disponível. É possível que o efeito exista em recortes que o dado não expressa, por equipe específica ou por capacidade instalada, que não estão no dataset.

**Consequência para a defesa:** responde diretamente ao mentor. Testamos a hipótese dele, com número, e reportamos o resultado negativo em vez de silenciar.

### 1.3 A queda de novembro e dezembro é real, não censura de dados

Não há censura à direita: **100% dos 122.543 registros têm `Encerrado` preenchido**, e o último encerramento é 31/12/2025 23:45. A queda tem duas causas reais:

**(a) Parada de fim de ano.** O último terço de dezembro cai 45% contra o mesmo terço de novembro: **305 contra 556**.

**(b) Diluição do elegível pela expansão do monitoramento.** O share de elegíveis sobre o total cai mês a mês: **58,3% (agosto) para 10,8% (setembro) para 7,6% (novembro) para 5,2% (dezembro)**. Dezembro é simultaneamente o maior mês do ano em volume total (**27.321**) e o menor em volume elegível (**1.423**).

**Leitura honesta:** a diluição explica a queda de proporção. A queda de contagem absoluta do elegível ao longo do trimestre (2.324 em setembro para 1.423 em dezembro) só está parcialmente explicada, e novembro (1.634) fica sem causa verificada. Esse limite está declarado na seção 5.

### 1.4 Cobertura empírica da banda de 80% no teste (92 dias)

| Prioridade | Cobertura observada | Nominal | Leitura |
|---|---|---|---|
| P2 | **84,8%** | 80% | calibrada, e até conservadora |
| P3 | **60,9%** | 80% | **sub-cobre**: subestima a incerteza |

Calculada na seção 4.10.1 do notebook 03. Em 17/08/2026 a causa da variação foi medida e a explicação anterior estava errada: **o ajuste do Prophet é determinístico** (MAE e `sigma_obs` idênticos entre processos). O que não era reproduzível é a banda, construída por amostragem posterior sobre o gerador aleatório do numpy. Com a semente fixada antes de cada previsão, o notebook reproduz os valores acima, e eles conferem com um script isolado que refaz a conta. Se a banca perguntar por um número único, é este, com a ressalva de que a cobertura é estimativa sobre 92 dias e o que decide é a leitura (P2 acima, P3 abaixo do nominal).

**Causa da sub-cobertura em P3:** a mudança de nível de novembro e dezembro está fora do que o treino (janeiro a setembro) permitia prever, a mesma razão do item 1.3.

**Encaminhamento:** reportar cobertura junto do MAE em todo material que exibir erro. A banda não é garantia, e no P3 ela não sustenta leitura de "pior caso".

---

## 2. Perguntas prováveis, com resposta preparada

Perguntas unificadas entre os quatro perfis. Onde dois perfis fizeram a mesma pergunta, ficou a formulação mais dura.

> **Avisos de contradição com o v1.** Cinco respostas preparadas do v1 não sobrevivem à auditoria como estavam. Cada uma aparece abaixo com o aviso inline. Resumo: (a) o ganho do Prophet no P2 é 15%, não 26%; (b) "empate técnico" não tem incerteza calculada e o critério de leitura está assimétrico; (c) "imune à anomalia" vale para o par agosto/setembro, não para o trimestre; (d) "ARIMA modelaria autocorrelação que o resíduo não apresenta" afirma um teste que não foi feito; (e) a promessa de "telas alimentadas com a saída real" está hoje contradita por números fabricados nas telas.

### 2.1 Metodologia de modelagem

**P: Por que Prophet, e não SARIMA, LSTM ou XGBoost, para uma série diária? E antes de responder: o documento interno justifica o veto ao ARIMA dizendo que a série tem "componentes que ARIMA não captura bem". Que componentes? Porque o baseline que vocês usam, o sazonal-7, é exatamente o seasonal naive da família ARIMA, e ele empata com o Prophet no P3.**

O argumento que se sustenta é o empírico, não o teórico. Três métodos com o mesmo conjunto de informação (sazonal-7, Prophet, regressão de calendário com defasagens 7 e 14) chegam ao mesmo patamar de erro (P3: 11,3 / 11,8 / 12,7; P2: 5,7 / 4,2 / 4,2), então o ganho estaria na terceira casa. LSTM é inviável com 365 pontos e 1 ano de histórico. SARIMA não foi testado, e a formulação do documento interno sobre ARIMA é fraca: o que temos é o seasonal naive como proxy da família, e ele já está na tabela. O Prophet ficou pelas propriedades operacionais (intervalo de predição, feriados nativos, mesma configuração para P2 e P3), não por erro menor.

*Evidência: notebook 03, seções 4.9 e 5; `context/decisoes-tecnicas.md`, tabela de restrições; slide de conclusão do deck.*

> **Aviso de contradição com o v1.** O v1 respondia "ARIMA modelaria autocorrelação que o resíduo não apresenta". Não há teste de autocorrelação do resíduo em nenhum notebook (sem ACF, sem Ljung-Box). A frase afirma um resultado que não foi produzido e deve sair da resposta até o teste existir. O teste é barato e deve ser rodado antes da banca.

**P: Qual é o erro oficial do modelo? O material mostra quatro números: ±4 e ±11 na divisória, MAE 3,7 e 20,0 nos gráficos do teste out-dez, e 4,2 e 11,8 na tabela do rolling. Qual eu levo para casa?**

O número oficial é o do rolling backtest, porque reproduz o uso real (re-treino a cada rodada, erro médio de D+1 a D+7): **P2 4,2/dia e P3 11,8/dia**. Os 3,7 e 20,0 são do corte out-of-time, um treino único de janeiro a setembro prevendo 92 dias, e servem para diagnóstico. O erro de comunicação é nosso: todo slide que exibir erro precisa rotular o protocolo ao lado do número, e falta uma linha reconciliando os dois (no corte único o P3 dá 20,0/dia, inflado pela queda de dezembro; no rolling cai para 11,8/dia).

*Evidência: notebook 03, seções 4.4 (19,96) e 4.7 (11,76); slides d12a, d15m e d15n.*

**P: Vocês escrevem "± 4/dia" e "faixa do dia a dia". MAE é erro médio absoluto, não intervalo, e não tem cobertura associada. A faixa é a banda de 80% do Prophet. Qual é a cobertura empírica dessa banda, e por que o slide diz que ela permite "dimensionar a operação pelo pior caso"?**

São duas coisas distintas. Quem carrega incerteza é a banda de 80%, e ela foi medida: **entre 86% e 88% no P2** (calibrada) e **entre 59% e 61% no P3** (subestima a incerteza, pela mudança de nível de novembro e dezembro). Estado das correções: a notação "±" já foi substituída por "erro médio (MAE)" em todos os slides da versão atual, e a cobertura é publicada ao lado do erro. Pendência remanescente: retirar a copy de "pior caso" onde ela se referir ao P3, porque lá a banda não sustenta essa leitura.

*Evidência: seção 1.4 deste dossiê; notebook 03, seção 4.10.1; slides d12a, d08a e d15m.*

**P: No P2 vocês anunciam 26% de ganho sobre o baseline. Mas a seção 4.3 do próprio notebook conclui que no P2 o melhor baseline é a média-7 (4,28 contra 6,72 do sazonal-7 no corte out-of-time). No rolling, média-7 dá 4,91 e Prophet 4,17. Por que a média-7 desapareceu da tabela final e do slide, justamente na única série onde o modelo ganha?**

A crítica é procedente e o número correto é **15%**, não 26%. Contra o melhor baseline de cada série: P2 4,17 contra 4,91 (15% melhor) e P3 11,76 contra 11,25 (4% pior). O 26% vem da comparação contra o sazonal-7, que o próprio notebook já mostra ser o baseline inadequado para o P2. A correção é recolocar as três referências na tabela final e no slide e comparar sempre contra o melhor baseline de cada série.

*Evidência: notebook 03, célula 17 (out-of-time: sazonal-7 6,72 / média-7 4,28), célula 29 (rolling P2: Prophet 4,17 / sazonal-7 5,67 / média-7 4,91), célula 36 (resumo só com sazonal-7); slides d15c e d15n.*

> **Aviso de contradição com o v1.** O v1 respondia "o Prophet vence no P2 (4,2 contra 5,7, cerca de 26% melhor)". Passa a valer 15% sobre o melhor baseline (4,17 contra 4,91). Toda ocorrência de 26% em slide, documento ou fala tem que ser corrigida antes da banca: é o achado de conserto mais barato e de maior retorno defensivo do dossiê.

**P: No gráfico por horizonte do P3, o baseline fica abaixo do Prophet em seis dos sete horizontes. Isso não é empate, é desvantagem sistemática. Vocês têm cerca de 29 origens no backtest: onde está o intervalo de confiança ou o teste pareado, para eu saber se "empate técnico" e "melhor no P2" são afirmações sustentadas?**

Não temos. Reportamos apenas a média dos erros absolutos por horizonte, sem dispersão, e as diferenças não são amostras independentes (origens a cada 4 dias, janelas de 7 dias que se sobrepõem, então o n efetivo é menor que as 203 previsões sugerem). Pior: o critério ficou assimétrico, chamamos de empate onde perdemos e de vitória onde ganhamos. O consertável em pouco tempo é guardar o erro por origem dentro do rolling e calcular a diferença pareada com bootstrap ou Wilcoxon. Enquanto isso não existir, a leitura honesta é: os três métodos estão no mesmo patamar nas duas séries, com leve vantagem do Prophet no P2 e leve vantagem do baseline no P3.

*Evidência: notebook 03, célula 28 (origens a cada 4 dias, H=7), célula 29 (dicionários de erro por origem, agregados só por média), célula 36; slide d15n.*

> **Aviso de contradição com o v1.** O v1 respondia "É empate técnico, dentro do ruído do backtest". A afirmação supõe uma medida de ruído que não foi calculada. Passa a valer a formulação acima, que assume a ausência de teste estatístico.

**P: Vocês só reportam MAE, que é simétrico e cego a viés. No teste out-of-time do P3 a previsão fica sistematicamente acima do real em novembro e dezembro. Qual é o erro médio com sinal, e o que um viés de nível faz com a projeção de meta anual, que é uma soma?**

Não medimos viés, é lacuna real. Pelo gráfico, o corte out-of-time do P3 está enviesado para cima em novembro e dezembro, consistente com a cobertura de 60,9%. Importa mais que o MAE no nosso caso, porque a projeção de meta soma dias: erro aleatório se cancela na soma, viés se acumula. Encaminhamento: reportar erro médio com sinal por horizonte e por mês, e medir o erro do agregado de 7 dias e do mês, que é o número que a projeção de KPI usa. Hoje todo o erro medido é diário.

*Evidência: slide d15m (painel P3); notebook 03, células 20 e 29 (apenas MAE).*

**P: Vocês escolheram a configuração do Prophet olhando o resultado no conjunto de teste, sem conjunto de validação, e o único período de teste é justamente o trecho que vocês classificaram como regime anômalo. Por que o número reportado ainda vale?**

Em rigor houve seleção sobre o teste, e assumimos. Três mitigantes: a configuração mantida é a padrão da biblioteca, nada foi ajustado a favor do teste; o experimento era teste de sanidade contra flexibilidade excessiva, não busca de hiperparâmetros (flexibilidade alta melhora o treino de 10,23 para 9,50 e piora o teste de 19,96 para 26,13); e o rolling backtest, com outras origens, confirma o mesmo patamar. O mitigante é parcial, porque as origens do rolling cobrem o mesmo período out-dez, então não é confirmação independente de regime. O que dá para fazer rápido é abrir o erro do rolling por mês, mostrando quanto vem do trecho de queda e quanto do dia a dia.

*Evidência: notebook 03, seção 4.6 (células 25 a 27) e célula 29 (origens de 01/09 a 24/12).*

**P: A conclusão afirma que o resíduo é ruído irredutível. Mas os três métodos que convergem usam o mesmo conjunto de informação (dia da semana, feriado, defasagens). Convergência de três estimadores sobre a mesma informação prova o teto daquela informação, não o teto do dado. Vocês testaram autocorrelação do resíduo, ou algum regressor exógeno?**

A frase está mais forte que a evidência, e a formulação correta é "teto do sinal de calendário". Não rodamos ACF nem Ljung-Box, e não há `add_regressor` no notebook 03. Candidatos que existem na base e nunca entraram como regressor: backlog de elegíveis abertos, contagem de itens de configuração vistos pela primeira vez, mix de origem manual contra monitoramento, virada de mês. Testamos backlog contra quebra de OLA, não contra volume. Correção da redação e teste de autocorrelação entram antes da banca.

*Evidência: slide d16a; notebook 03, célula 20 (só `add_country_holidays`) e célula 33 (features: dia da semana, feriado, lag 7, lag 14).*

**P: Vocês desligaram a sazonalidade anual, e o motivo é correto (1 ano de dado). Mas usam a ausência dela para explicar o erro de dezembro dizendo que "com mais histórico o modelo aprende". Vocês já diagnosticaram que o último terço de dezembro cai 45% por recesso. Isso é calendário operacional conhecido de antemão, e o Prophet aceita evento customizado. Por que não modelaram?**

Justo. O freeze de fim de ano não precisa de sazonalidade anual: entra como feriado customizado ou regressor binário, e isso está na nossa mão. Fica como próximo ajuste. E a frase "com mais histórico o modelo aprende" vale para o freeze, que se repete, e não vale para a outra causa que nós mesmos identificamos, a mudança de instrumentação do monitoramento, que é evento único.

*Evidência: seção 1.3 deste dossiê (dez 589 / 529 / 305 contra nov 562 / 516 / 556); notebook 03, célula 20 (`yearly_seasonality=False`); slide d15m.*

**P: São contagens não negativas em um modelo gaussiano com corte em zero. Por que não Poisson ou binomial negativa?**

Com médias de 14,1 e 54,8 por dia a aproximação é razoável na maior parte do ano, e o teto de erro já foi demonstrado por três métodos, então um modelo de contagem não mudaria o patamar. É refinamento legítimo, anotado como evolução. O ponto sensível seria a cauda da banda em dias de volume muito baixo (fim de semana e feriado).

**P: O deck afirma que a série que conta para a meta permanece estável, em cerca de 2,3 mil por mês, e que o alvo é "imune à anomalia". Mas a tabela do próprio documento mostra 2.330 em agosto, 2.324 em setembro, 2.126 em outubro, 1.634 em novembro e 1.423 em dezembro: 39% de queda, tudo dentro da janela de teste. Novembro não tem recesso, e diluição explica queda de proporção, não de contagem. O que aconteceu com o alvo?**

A afirmação de estabilidade vale para o par agosto contra setembro, que é onde o teste de imunidade foi feito, e está generalizada demais no material. A queda de nível de outubro a dezembro é real e não está totalmente explicada: o freeze cobre parte de dezembro e novembro fica sem causa verificada, com abertura manual estável em cerca de 1,5 mil por mês. Encaminhamento: qualificar o slide para "estável no salto de setembro", declarar a queda de nível como limite aberto e investigar mecanismo de substituição, mudança de regra de KPI ou de classificação. É o item mais importante a fechar antes da banca no eixo de dado.

*Evidência: seção 1.3 deste dossiê; `docs/sprint-3-mvp.md`, tabela de volume elegível e seção de verificações de robustez; slides d04b, d04c, d04m e d13a.*

> **Aviso de contradição com o v1.** O v1 respondia, em dois pontos, que a série elegível "é estável e imune à anomalia de setembro (2.330 para 2.324)" e que "uma nova expansão de monitoramento tende a não afetar o alvo". A primeira metade continua verdadeira e é forte; a segunda metade está generalizada. Passa a valer: imunidade comprovada no salto de setembro, e queda de nível de 39% até dezembro como limite aberto, que é justamente o que quebrou a banda do P3.

**P: O alvo é a contagem diária de elegíveis, e a elegibilidade vem do campo "Entrou para KPI?", que depende do status final. No dia D+1 esse rótulo ainda não existe para os incidentes abertos hoje. Vocês estão prevendo uma quantidade que não é observável no momento da previsão. Como o dashboard compara previsto contra realizado, e qual a latência de consolidação?**

É limitação real e sem tratamento implementado. O alvo é construído com informação de fechamento, então em produção a cauda recente da série fica incompleta e o realizado do dia só consolida depois. Isso também significa que o erro do backtest é otimista frente ao que a operação verá. Não invalida o treino, porque no histórico todos os incidentes estão fechados (100% com `Encerrado`), mas o desenho do pipeline está pendente: medir a distribuição de tempo entre abertura e classificação final, definir janela de descarte dos últimos dias, treinar sobre base consolidada e exibir o realizado do dia como parcial.

*Evidência: `notebooks/02_base_kpi.ipynb`, seção do filtro; seção 5 deste dossiê; notebook 03, seção 4.10.2.*

**P: O material apresenta AUC de 0,80 para a regressão logística e top 20% concentrando 66% das quebras, sem notebook que reproduza. E o mesmo documento registra o XGBoost com AUC 0,79 na seção de decisão e 0,81 na validação de terreno. Se o baseline é 0,81, o argumento de que a logística empata ou supera cai. Com cerca de 50 positivos no teste, o intervalo do AUC é largo. E quais features existem no instante da abertura? Duração, Resolvido, Encerrado e Status definem o próprio rótulo.**

O modelo de risco ainda não está implementado. Esses números vêm de teste de laboratório com features mínimas, sem notebook comitado, e até existir não devem aparecer como resultado. A contradição 0,79 contra 0,81 é erro de documentação nosso e será corrigida. A escolha da regressão logística se defende por explicabilidade e por diferença dentro do ruído com cerca de 50 positivos, não por AUC maior. Sobre vazamento, a regra que vamos aplicar é usar só o que existe na abertura: prioridade, produto, categoria, origem, item de configuração, grupo inicial, hora e dia da semana. Duração, Resolvido, Encerrado e Status ficam proibidos, porque a violação é derivada de duração. Validação out-of-time, não aleatória. E a leitura por triagem tem que superar uma régua trivial: Team11 concentra 46% das quebras com 8% do volume, então uma regra "P3 mais Team11" já concentra muito, e o ganho do modelo tem que ser medido acima dela.

*Evidência: `docs/sprint-3-mvp.md`, linha da decisão de modelagem contra a seção de validação de terreno; seção 4 e 5 deste dossiê; slides d09a e d10a.*

**P: A série elegível ao KPI é o alvo certo?**

Segue o que a Locaweb mede: a meta de OLA é calculada sobre os elegíveis, e usamos o campo oficial `Entrou para KPI? = SIM`, com aderência de 99,88% à regra do dicionário. O volume total mudou de regime por decisão de instrumentação em setembro, algo que nenhum padrão histórico prevê, e a série elegível atravessou esse salto sem alteração (2.330 para 2.324). Limite declarado: o Cronos apoia a gestão da meta e do risco, não é ferramenta de dimensionamento do N1. Pendência de rigor: o alvo nunca foi confrontado com a regra de duração do dicionário (P1/P2 até 4h, P3 até 12h), e essa verificação é uma célula.

### 2.2 Valor operacional (perfil do gestor)

**P: Concretamente: quem abre o Cronos, a que hora, e o que essa pessoa faz nos 5 minutos seguintes? Meu N2 vive dentro da fila de tickets. Se o alerta não chega onde ele já trabalha, ele não olha.**

Temos o momento e o conteúdo definidos, não a integração. O desenho é: briefing gerado às 06:00 para o coordenador de operações (Ontem / Hoje / Ações sugeridas) e a aba de risco de OLA como fila ordenada por probabilidade para o N2 durante o dia. Não existe ainda canal de entrega (e-mail, Teams), integração com a ferramenta de ticket, dono formal da ação nem prazo de resposta do próprio alerta. Isso é Sprint 4, junto com o Django. Sem isso, o Cronos é painel e não fluxo, e assumimos.

*Evidência: `prototipos/telas/mvp-mockup.html` (bloco de briefing 06:00 e aba de risco); `context/status.md` (app Django ainda não existe).*

**P: Erro médio de 11 incidentes por dia num P3 que roda a 55 por dia é 20% da carga. Que decisão minha muda com isso?**

Sustenta decisão de faixa, não de unidade. A entrega é um intervalo, não um ponto: serve para dizer se a semana entra em patamar alto ou baixo, orientando escala de plantão e janela de manutenção. Não sustenta decisão por incidente, e não escondemos: no P3 os três métodos empatam em 11 a 12 por dia porque o sinal previsível é só calendário. Quem responde "qual incidente vai estourar" é o modelo de risco, que ainda não está implementado. Ressalva de honestidade: no P3 a banda sub-cobre (60,9%), então a leitura de faixa é confiável hoje no P2 e frágil no P3.

**P: No slide de panorama vocês escrevem que 85% vêm de automação e que isso "é ruído operacional, não trabalho". Esses 85% são o trabalho do meu N1. Vocês estão dizendo que três quartos da minha operação é lixo?**

A frase está mal calibrada e será corrigida. O dado real é mais fino: dos 25.600 elegíveis, **9.529 (37%) nasceram de Monitoramento**, e 45 das 248 quebras são de incidentes abertos por monitoramento. Automação não é sinônimo de ruído. O ponto correto é outro: **65,6% do volume total fecha em "Sem Intervenção"** e por isso não entra no KPI, e é essa parcela que infla o volume sem mexer na meta.

**P: Vocês escrevem "os 21% pelos quais a Locaweb é cobrada". OLA é acordo interno entre níveis de atendimento. Ninguém me cobra por OLA. Vocês entenderam a diferença entre OLA e SLA?**

Entendemos e a redação do slide está errada. O correto é "os 21% sobre os quais a meta de OLA é medida", ou "cobrada internamente". O compromisso com cliente é SLA e não está no dataset; o que modelamos é o acordo interno, pelos campos `Entrou para KPI?` e `KPI Violado?`.

**P: Setembro vocês explicaram bem. Em 2026 eu vou expandir monitoramento de novo, e provavelmente mudar regra de classificação. O que acontece com o Cronos no dia seguinte, e quem me avisa que o modelo saiu de calibragem?**

Duas respostas, uma boa e uma desconfortável. A boa: como o alvo é a série elegível, a expansão de setembro passou sem efeito (2.330 para 2.324), então nova expansão de monitoramento tende a não mexer no alvo. A desconfortável: mudança de nível no elegível nos machucou de verdade. O share elegível caiu de 58,3% em agosto para 5,2% em dezembro, a contagem caiu 39%, e a cobertura da banda no P3 despencou para 60,9% exatamente nesse período. Não existe monitor de drift nem alarme automático: o re-treino semanal reabsorve o patamar, com atraso. Definir esse alarme é pendência de pipeline que assumimos.

**P: Quanto custa rodar isso por mês na minha infra? Eu pedi na mentoria simulação de custo de token da Claude API e não vejo número nenhum.**

Não temos o número e ele está comprometido para a Sprint 4, como pedido. O que já podemos afirmar do lado da infra: o treino do Prophet é sobre 365 pontos por prioridade, roda em segundos, sem GPU, em um container; o custo relevante é a chamada da API para redigir briefing e alertas (1 a 2 gerações por dia), não o ML. A entrega é Docker e cloud-agnóstica, então roda na infra da Locaweb sem contratar terceiro. A simulação (briefs por dia, tamanho de prompt, custo mês e ano) sai com a solução final.

*Evidência: `context/mentoria-locaweb.md` (pedido explícito do Douglas); ausência de qualquer linha de custo em `docs/sprint-3-mvp.md`.*

**P: Se o modelo de risco marca um incidente como provável quebra, quantas horas de antecedência ele me dá? Alerta que chega depois do prazo estourado não vale nada.**

Não medimos ainda, e é preciso cuidado com a leitura. **Correção de uma versão anterior desta resposta:** o tempo até o fechamento dos incidentes que quebraram (mediana de 6,9h no P2 e 39,6h no P3) **não é janela de ação**. O prazo de OLA, inferido do próprio dado, fica em torno de 4h no P2 (nenhum caso cumprido passa de 3,5h no percentil 99 e o menor violado é 4,0h) e em torno de 8h no P3 (o menor violado é 8,7h). Uma mediana de 39,6h no P3 significa, portanto, que o incidente foi fechado cerca de 31 horas **depois** de já ter violado. A janela útil é limitada pelo prazo de OLA menos o tempo de detecção, não pela duração total. O que vamos publicar junto do modelo de risco é a distribuição do tempo entre a abertura e o instante em que o risco fica alto, mais o tempo de detecção, porque é isso que determina se o alerta chega antes do estouro.

**P: Vocês me mostram que 30 itens de configuração concentram 62% das quebras. Isso eu resolvo com uma planilha e uma reunião com o dono desses ativos. Onde entra machine learning?**

Em parte o senhor está certo, e essa é a parte mais acionável do projeto: são 30 ativos, **61,7%** das quebras, e metade das quebras do segundo semestre (**55 de 111**) ocorreu em ativos que já tinham quebrado no primeiro. Isso é lista, não modelo, e deve entrar como watchlist no dia 1. O que a lista não resolve: a outra metade das quebras vem de ativos sem histórico, e o P3 elegível tem cerca de 20 mil casos por ano, todos iguais dentro da mesma prioridade. O modelo serve para ordenar dentro do P3. Ressalva de honestidade: na tela atual, além de IC00840 com 32 quebras (correto), os outros itens listados estão com contagem que não bate com a base e serão corrigidos.

**P: Meu coordenador de plantão tem 10 anos de casa e acerta a carga do dia de cabeça. Por que eu devo confiar mais no modelo do que nele?**

Para prever carga do dia, não deve. Nunca medimos o modelo contra o humano, e no P3 ele empata com repetir a última semana (11,8 contra 11,3). Onde o Cronos ganha não é em previsão: entrega intervalo em vez de palpite pontual, é auditável e reprodutível (mesma configuração para as duas séries, backtest publicado) e não depende de quem está de férias. E ganha em varredura: ordenar 20 mil P3 por risco e cruzar histórico de ativos com quebra é onde a intuição não alcança. Isso hoje é promessa, depende do modelo de risco.

**P: 248 quebras em 25.600 elegíveis é 0,97%, e a régua mostra a Locaweb dentro da meta em três dos quatro indicadores (P3 196 quebras contra teto de 201, atingimento 150%; volume em 125% nas duas prioridades). Qual é o problema que o Cronos resolve, e quanto vale em reais ou em quebras evitadas?**

O único ponto de pressão real é o P2: 42 quebras na faixa de 40 a 45, atingimento 75%. Não temos custo por violação, porque o dataset não tem impacto financeiro, cliente afetado ou penalidade: "raras e caras" é asserção nossa, não medida, e ou sai do material ou vem com número da Locaweb. O valor defensável hoje é ordenação dentro da prioridade (206 das 248 quebras são P3 e a fila trata todo P3 como igual) mais a watchlist de ativos crônicos, não redução de volume.

**P: Minha meta de P2 fechou 2025 em 75%, com 42 quebras numa faixa de 40 a 45. O retorno do projeto é evitar 2 ou 3 quebras de P2 no ano inteiro. O modelo entrega essas 2 ou 3?**

Hoje não podemos afirmar que sim, e não vamos afirmar. O P2 tem 42 quebras em 5.159 casos no ano, cerca de 3,5 por mês: alvo raro. A leitura de triagem que temos (top 20% concentrando cerca de 66% das quebras) foi medida no conjunto todo, não isolada no P2, e vem de teste sem notebook comitado. O que sustentamos com número é o caminho: 46% das quebras estão em um único time (Team11, com 8% do volume) e 62% em 30 ativos. Se a triagem antecipar parte desse grupo, 2 ou 3 quebras de P2 no ano é alvo plausível, mas essa conta precisa ser feita e publicada antes de virar promessa.

**P: Na mentoria eu disse que o mais importante era a probabilidade de fechar o mês dentro da meta, porque duas quebras no começo do mês já derrubam tudo. Onde está isso? A tela mostra o fechamento de 2025, que eu já conheço.**

Não está implementado, e a própria tela declara isso em texto ("sem projeção de modelo: os números vêm direto do fechamento de 2025"). O que existe é a régua com as faixas oficiais e a posição real do ano fechado, que prova domínio da regra da Locaweb. A projeção condicional depende de duas coisas: a previsão de volume por prioridade, que já temos, e a taxa de quebra por incidente, que vem do modelo de risco. É a próxima entrega, não um item esquecido, e é o segundo item da fila de ação deste dossiê.

**P: Na mentoria descrevi um padrão de acúmulo. Vocês testaram?**

Sim. Não encontramos suporte na forma como conseguimos medir (backlog diário de elegíveis abertos): relação levemente negativa e fraca, r = -0,139 (ver 1.2). Reportamos o resultado negativo com número. Se houver um recorte específico da operação que descreva melhor o acúmulo, é o caminho para testar de novo.

**P: Cadê o sistema rodando? No dia 23/08 recebo produto ou relatório?**

Sprint 3 é MVP preliminar: modelo de volume validado e reprodutível, análise completa e telas navegáveis. A aplicação Django servindo previsão e o Docker são escopo da Sprint 4 (08/09).

> **Aviso de contradição com o v1.** O v1 prometia, nesta resposta, "notebooks executáveis dos dois modelos e as telas alimentadas com a saída real" até 23/08. Isso hoje não é verdade: o segundo modelo não existe, e a auditoria de telas encontrou números fabricados na tela viva do MVP (ativos crônicos, corte de 5% concentrando 48%, saúde por produto, série de 30 dias misturando períodos). A promessa continua sendo a meta correta, mas passa a ser tratada como ação obrigatória da seção 7, não como fato.

### 2.3 Rigor acadêmico e conformidade

**P: O template da Sprint 3 tem um slide inteiro de PLANEJAMENTO E GESTÃO DO PROJETO, e o único ponto de melhoria da Sprint 2 foi justamente gestão ágil. Me mostre o Kanban, o cronograma da sprint e a divisão de tarefas entre os três integrantes.**

Ainda não está montado, e é a lacuna mais barata de fechar do dossiê. O deck construído cobre só EDA e o modelo de volume; os blocos do template (equipe, contextualização, problema, proposta, gestão, arquitetura, MVP) entram na montagem do `.pptx`. Não há board versionado nem divisão de tarefas escrita por integrante. Ação: criar o board com as tarefas reais das três sprints, exportar imagem para o slide e incluir o link no PPT.

**P: Os notebooks trazem os três nomes como autores, mas o repositório tem 43 commits e todos do mesmo autor. Como vocês comprovam a divisão de trabalho?**

Hoje o repositório não comprova. Os commits estão sob uma única identidade e a coluna de função da tabela de equipe está vazia. A divisão real precisa ser declarada no slide de gestão e, se possível, refletida em commits ou atas de reunião. É correção pendente, sem evidência versionada hoje.

**P: Abri o notebook do coração da sprint e as células de código estão sem saída e sem número de execução. Todos os números citados (MAE 11,8, 4,2, cobertura 60,9%, r = 0,159) estão escritos à mão em markdown. Como eu verifico que esse notebook rodou?**

**Resolvido em 29/07/2026.** O 03 está comitado executado, com saídas preservadas (52 células, zero erros), além das oito figuras em `notebooks/figures/03_previsao_volume/`. O 02 preserva outputs e trava os números com `assert`. A dessincronia de cobertura que existia foi resolvida na raiz: como o ajuste do Prophet não é determinístico, o texto passou a reportar **faixa** (entre 86% e 88% no P2, entre 59% e 61% no P3) e o valor exato de cada execução fica apenas no output da célula. Reprodução: rodar o 02 e depois o 03 a partir do dataset oficial.

**P: O slide de hipóteses descartadas mostra 21% de escalada contra cerca de 60% esperado por acaso, 87% de quebras isoladas e silhueta 0,13. Nenhum desses números aparece em notebook nenhum. Como o "esperado por acaso" foi calculado?**

Esses testes foram feitos em notebook de laboratório, que está fora do versionamento, então hoje não há código comitado que os reproduza. Vale para a cascata, para o DTW e para o teste de acúmulo. Encaminhamento: destilar em notebook comitado ou rebaixar o texto para "exploração" até existir código. O mesmo slide tem erro de contagem: diz "duas ideias" e mostra três cartões, e o terceiro (realocação de equipe) não foi refutado pelo dado, não pôde ser testado por ausência de coluna.

**P: A régua de meta diz atingimento de 75% no P2 e 150% no P3. Qual é a fórmula, e onde está o código? E onde está a projeção de atingimento do KPI que vocês listam como entrega?**

As faixas vêm do dicionário de dados da Locaweb e o atingimento segue a regra deles, mas não há célula que calcule os percentuais nem notebook da projeção. O que está fechado e rastreável é o número observado de 2025: 42 quebras em P2, 196 em P3, 248 no total, volume elegível P2 5.159 e P3 19.997. A projeção é item explícito de entregável e está pendente.

**P: O desafio exige "classificação ou clusterização". Vocês descartaram a clusterização DTW e o classificador não existe. Como esse item está atendido?**

Hoje não está. O DTW foi descartado com critério (silhueta cerca de 0,13) e o requisito foi delegado ao classificador de risco de OLA, que não foi implementado. É a razão pela qual o modelo de risco é a primeira prioridade da fila de ação: ele destrava três requisitos oficiais de uma vez (previsão de risco de perda de OLA, classificação, explicabilidade por incidente).

**P: O slide 6 do template pede a documentação de gerenciamento das sprints 1 e 2 atualizada. Nas sprints anteriores vocês venderam o detector de cascata como diferencial e ele foi refutado. A proposta foi atualizada? Porque a tela de cascata ainda está no protótipo e linkada nas outras telas.**

A cascata foi refutada no dado (87% das quebras são de casos isolados, escalada de 21% contra cerca de 60% do acaso) e saiu do produto. A atualização formal das sprints 1 e 2 ainda não foi feita, e os artefatos de arquitetura da Sprint 2 continuam declarando XGBoost como modelo de risco, tslearn/DTW como clusterização e o detector de cascata como componente. As cinco telas da Sprint 2 receberam tarja de referência histórica, mas seguem navegáveis e com item de menu de cascata. Antes da entrega elas serão arquivadas, e o slide de arquitetura será refeito com a stack real.

**P: A apresentação pede sazonalidade em três eixos (dia da semana, horário, mês), agrupamentos críticos por produto mais categoria mais prioridade, e incidentes recorrentes. Onde estão?**

Dia da semana está coberto com intervalo de confiança de 95%, e mês está coberto pelo volume mensal. Horário não tem uma única análise em notebook: existe uma coluna `hora` criada e nunca usada, e o heatmap 7x24 da tela vem de um JSON sem notebook que o reproduza. Agrupamento cruzado das três dimensões não existe, e a dimensão Categoria não aparece em nenhuma análise comitada. Recorrência não tem análise comitada, apesar de a tela afirmar números concretos por ativo. São três eixos textualmente exigidos e de baixo esforço, e estão na fila de ação.

**P: O dicionário define violação por tempo (P1 e P2 até 4h, P3 até 12h). Vocês usam o campo "KPI Violado?" e nunca confrontam com a coluna Duração. Como a violação foi calculada?**

Usamos o campo oficial, que é o que a Locaweb mede, com aderência de 99,88% à regra de elegibilidade do dicionário (25.751 pela regra contra 25.600 pelo campo, 151 divergências). A verificação equivalente para a regra de duração não foi feita e é uma célula de invariante: recalcular a violação por prioridade a partir de Duração e cruzar com o campo, documentando divergências. Entra antes da banca, porque é o alvo do modelo de risco.

**P: Onde estão as fontes de dados da solução, exigidas duas vezes no template?**

O pipeline real está documentado nos cabeçalhos dos três notebooks (`LW-DATASET.xlsx`, aba "Dataset Geral", para `data/interim/incidentes_kpi.parquet`, para os modelos, para figuras e telas), com a biblioteca `holidays` BR como fonte externa de feriados. Ainda não virou slide. Está na fila.

**P: Não há nenhuma referência bibliográfica ou metodológica em documento ou slide. As decisões estão justificadas pelo dado, mas não referenciadas.**

Verdade. As decisões são todas justificadas empiricamente e por documentação de ferramenta, sem citação formal. É correção de 30 minutos (referência ao artigo do Prophet, à definição de MAE e ao protocolo de backtest de séries temporais) e está na fila com prioridade baixa.

### 2.4 Provocações céticas

**P: A tela que vocês me mostraram diz "os 5% de maior risco concentram 48% das quebras", mostra ranking de risco e um painel de fatores estilo SHAP, e o modelo de risco não existe. O que exatamente nessa tela é saída de modelo hoje?**

Vamos separar na hora. Resultado real e reprodutível: a previsão de volume, Prophet puro, treinada só em 2025 na série elegível, com erro de rolling backtest de 4/dia no P2 e 11/dia no P3, mais toda a análise da anomalia de setembro e a régua de meta com o fechamento real. Maquete: o bloco de risco por incidente, o painel de fatores (pesos ilustrativos, sem modelo por trás), o corte "5% concentram 48%" (que não é nem o número canônico, que é top 20% com cerca de 66%, e mesmo esse ainda não tem notebook) e parte dos ativos crônicos. Correção antes de 23/08: todo bloco sem modelo por trás recebe marca visível de ilustração de interface, e o que é resultado passa a ser lido da saída real.

**P: Onde estão as 4.812 cascatas? O dashboard tem item de menu "Cascatas" com badge 3, um card de 84% atribuído a "classificador XGBoost, base 4.812 cascatas" e uma cascata histórica com 630 filhos, enquanto o deck estampa "REFUTADO NO DADO".**

Não existem. São telas da Sprint 2, com números ilustrativos daquela fase, para uma hipótese que a Sprint 3 refutou. A base citada também não confere: o dataset tem 3.326 incidentes-pai com filhos. Essas telas não fazem parte do MVP e serão arquivadas em pasta de histórico, mantendo a prova de que a hipótese foi construída e testada, que é exatamente o argumento do slide de rigor. Apenas a tela do MVP é a tela da Sprint 3.

**P: O deck abre com um gráfico rotulado "Volume mensal 2023 a 2025" com doze barras subindo suavemente, e o slide de escopo dedica uma página a dizer que esse crescimento é falso. Além disso, uma variação do slide da anomalia mostra janeiro a agosto de 2025 em rampa crescente (2,8 a 4,0 mil) quando a série real é plana (3,7 / 3,6 / 3,6 / 3,2 / 3,3 / 3,6 / 3,4 / 4,0). Por quê?**

São dois gráficos com alturas escritas à mão, e nenhum dos dois deveria estar em slide rotulado com dado real: contradizem a própria descoberta central e contradizem a outra variação do mesmo slide, que usa a figura real do notebook. Ação: regerar a figura mensal a partir da série real (padronizando a unidade em todos os rótulos) e trocar o gráfico decorativo de abertura pelo plotado, ou remover o card.

**P: Se baseline, Prophet e regressão convergem para o mesmo erro, qual foi o trabalho de machine learning aqui? E a conclusão diz que as três propriedades do Prophet são coisas que "o baseline e a regressão não oferecem": a sua regressão tem coluna de feriado e roda as duas séries com a mesma função. Duas das três razões não se sustentam.**

Correto, o slide exagera. Feriado é uma coluna na regressão e a pipeline única também vale para ela. A única propriedade exclusiva do Prophet é o intervalo de predição, e é justamente o intervalo que sub-cobre no P3. O trabalho entregue não é ganho de acurácia: é o diagnóstico de que o teto do previsível é o calendário, demonstrado por três caminhos, o que evita gastar sprint atrás de LSTM. O slide será reescrito nesses termos.

**P: O slide de N1 contra N2 monta "19 vezes mais volume que risco" para o Team14, misturando denominadores: 75,7% é share do volume total de 122.543 e as 10 violações são share dos 25.600 elegíveis. Pelos seus próprios números (9,7% do Team14 entra no KPI), a participação dele na base elegível é da ordem de 35%, o que levaria a razão para cerca de 9 vezes.**

A crítica é procedente e o mesmo problema afeta a razão citada para o Team11. O insight de fundo continua válido e é forte (quem tem o volume não tem o risco: Team14 com 75,7% do volume total e 10 quebras, Team11 com 8% do volume e 114 das 248 quebras, 46%), mas a razão precisa ser recalculada com o mesmo denominador nos dois termos, ou apresentada como duas participações lado a lado em vez de um múltiplo.

**P: Os dois diferenciais que sobraram nunca foram testados contra o dado. Não existe fórmula nem validação de que score de saúde baixo anteceda quebra, e o morning brief é geração de texto sobre saídas de modelo. O diferencial que vocês venderam nas sprints 1 e 2, com nota 5,00, foi refutado nesta sprint. O que garante que esses dois não caem também?**

Nada garante, e a diferença de natureza é o que sustenta a resposta: a cascata era uma **hipótese sobre o mundo** (existe escalada que derruba OLA?) e por isso podia ser refutada pelo dado. O score de saúde é um **índice composto de métricas observadas** (tempo mediano de resolução, volume, taxa de violação por produto), não uma predição: ele pode ser mal calibrado ou pouco útil, não falso. O morning brief é camada de comunicação sobre saídas de modelo. Ainda assim, duas correções são devidas: publicar a fórmula do índice e testar se ele antecede quebra, e alinhar o discurso com a tela, porque a nota de 0 a 100 anunciada como diferencial não existe na tela viva do MVP, que hoje entrega ranking por tempo mediano de resolução.

**P: O mesmo documento apresenta o XGBoost com AUC 0,79 em um lugar e 0,81 em outro, e o modelo não existe. Como eu confio em qualquer número do material?**

A contradição é erro de documentação nosso e será corrigida junto com a remoção dos números não reproduzíveis. A resposta de fundo é a que estamos dando desde o começo: separamos o que é reprodutível do que é preliminar, e este dossiê existe para marcar essa linha antes da banca marcar. Os números que sustentamos são os da previsão de volume, da EDA e da régua de meta, todos com notebook e figura.

---

### 2.5 Privacidade e tratamento de dados (LGPD)

**P: Vocês versionaram o dataset de incidentes de um cliente num repositório que a Sprint 4 exige que seja público. Onde está o tratamento de dados pessoais e a conformidade com a LGPD?**

O dado chega **pseudonimizado na origem** e verificamos isso, não assumimos. Varredura executada em 29/07/2026 sobre as 19 colunas e sobre o campo de texto livre `Descrição resumida`:

| Verificação | Resultado |
|---|---|
| Colunas identificando pessoa (usuário, solicitante, nome, contato) | **nenhuma** |
| E-mails no texto livre | 0 ocorrências |
| CPF | 0 ocorrências |
| Telefone | 0 ocorrências |
| Endereço IP | 0 ocorrências |
| Campo `Aberto por` | apenas dois valores: `Manual` e `Monitoramento` |

Os identificadores são todos de ativo ou de estrutura, não de pessoa: itens de configuração como `IC00840`, equipes como `Team11`, produtos em sigla como `lhco` e `lsin`. Não há cliente final nem pessoa natural identificável no dataset.

**Pendências assumidas antes de tornar o repositório público (Sprint 4):**

1. **Decidir o versionamento do dado.** Hoje o arquivo bruto está versionado (`assets/Materal LocalWeb/LW-DATASET.xlsx`) e o diretório `data/` **não está no `.gitignore`**, então o parquet derivado entra no próximo `git add`. Duas opções, a decidir com a Locaweb: manter o dado versionado (o material foi entregue pela empresa para uso no desafio) ou remover o bruto do versionamento, deixando instrução de obtenção e publicando apenas a base derivada. Os notebooks já regeneram o parquet a partir do Excel, então a segunda opção não quebra a reprodução.
2. **Registrar a posição formal de privacidade** em `context/`, com a varredura acima como evidência, em vez de deixar o assunto implícito.
3. **Repetir a varredura no campo `Solução`**, que também é texto livre e não foi coberto nesta verificação.

Observação de honestidade: até 29/07/2026 não havia uma única menção a LGPD, anonimização ou dados pessoais em nenhum documento do projeto. A lacuna era de documentação, não de exposição de dado, mas era uma pergunta óbvia de banca sem resposta preparada.

---

## 3. Matriz de conformidade da Sprint 3

Fontes lidas na íntegra: apresentação Locaweb (12 páginas), Dicionário de Dados v2 e `03Template_MVP_Preliminar` (14 blocos). Caminhos relativos à raiz do projeto.

**Placar: 51 exigências mapeadas, 17 atendidas, 21 parciais e 13 pendentes** (contagem refeita linha a linha; a versão anterior somava 45 e estava errada). Dessas, 6 representam risco direto de nota. O núcleo analítico da previsão de volume está acima do padrão de graduação. O que falta é a segunda metade do produto (risco de OLA e projeção de KPI) e quase toda a moldura do template (8 dos 14 blocos, incluindo Kanban e o próprio `.pptx`).

### A. Objetivos do desafio (apresentação Locaweb)

| # | Exigência oficial | Status | Evidência | Lacuna |
|---|---|---|---|---|
| 1 | Previsão de volume, próximo dia (D+1) | atendida | notebook 03, seção 4.7 (rolling backtest H=7, re-treino semanal); figura `06_rolling_horizonte.png`; slide d12a | nenhuma |
| 2 | Previsão de volume, próxima semana (D+7) | atendida | mesma célula; erro por horizonte reportado; `docs/sprint-3-mvp.md` | nenhuma |
| 3 | Por prioridade (P2 e P3 obrigatórias) | atendida | notebook 03, seção 4.1 (P2 14,1/dia, P3 54,8/dia); slides d08m e d13a | nenhuma |
| 4 | Por categoria, produto ou item de configuração | parcial | justificativa do "ou" em `docs/sprint-3-mvp.md`; produto e IC aparecem nas telas | Categoria não é analisada em lugar nenhum; produto e IC nas telas sem modelo por trás; a watchlist de IC citada como cobertura não existe no protótipo |
| 5 | Tendência diária de volume de incidentes | atendida | 01_eda seções 4.1 e 4.3; notebook 03 seções 4.1 e 4.2; figuras de série e sazonalidade; gráfico de 30 dias mais previsão na tela | nenhuma |
| 6 | Tendência diária de perda de OLA | parcial | 01_eda seção 4.6 (distribuição das 248); notebook 03 seção 4.10.3 (quebras por quartil) | sem série temporal de quebras em notebook nem slide |
| 7 | Projetar impacto nos KPIs | parcial, em risco | régua de metas em `docs/sprint-3-mvp.md`; scoreboard na tela | é fechamento histórico de 2025, não projeção |
| 8 | Apoiar decisão operacional, indicar onde agir preventivamente | parcial | slide d09a (N1 absorve volume, N2 carrega risco); slide de delimitação; brief com ações sugeridas | recomendação por incidente depende do modelo de risco inexistente |

### B. Desafios analíticos esperados

| # | Exigência oficial | Status | Evidência | Lacuna |
|---|---|---|---|---|
| 9 | 01 Sazonalidade (dia da semana, horário, mês) | parcial | dia da semana com IC 95% (01_eda 4.3 e notebook 03 4.2); mês em 01_eda 4.1 | horário sem nenhuma análise; coluna `hora` criada e nunca usada |
| 10 | 01 Agrupamentos críticos (produto + categoria + prioridade) | pendente | prioridade e produto analisados isoladamente | nenhum cruzamento das três dimensões; Categoria ausente |
| 11 | 01 Incidentes recorrentes | pendente | proxy apenas nas telas (30 ativos com 62% das quebras) | nenhuma análise de recorrência comitada |
| 12 | 02 Previsão de volume de incidentes | atendida | notebook 03 completo: 2 baselines, Prophet, regressão de colunas, corte out-of-time, rolling backtest, teste de overfitting, cobertura da banda | nenhuma |
| 13 | 02 Previsão de risco de perda de OLA | pendente | apenas texto em `docs/sprint-3-mvp.md` (teste de laboratório) | modelo não implementado |
| 14 | 03 Classificação ou clusterização | pendente | DTW descartado com critério (silhueta 0,13); requisito delegado ao classificador | classificador não existe, item descoberto |
| 15 | 04 Explicabilidade | parcial | componentes do Prophet; explicação causal da anomalia; estrutura N1/N2 | sem SHAP e sem atribuição por incidente; painel da tela com pesos ilustrativos |

### C. Entregáveis e critérios de avaliação

| # | Exigência oficial | Status | Evidência | Lacuna |
|---|---|---|---|---|
| 16 | Entregáveis agnósticos a cloud provider | parcial | regra no `CLAUDE.md`; stack local e portável (pandas, prophet, parquet, holidays) | nenhum artefato de arquitetura da Sprint 3 declara isso |
| 17 | Modelo ou abordagem preditiva | atendida | Prophet entregue e justificado por propriedades operacionais | nenhuma |
| 18 | Recomendações práticas para a operação | parcial | brief com 3 ações; ativos crônicos; foco preventivo no N2 | ações por incidente sem modelo; números da tela não reproduzíveis |
| 19 | Visualizações de tendência diária de incidentes | atendida | 8 figuras em `figures/03_previsao_volume/` e 14 em `figures/01_eda/`; gráficos matplotlib reais em 10 slides | nenhuma |
| 20 | Visualizações de projeção de atingimento dos KPIs (probabilidade de atingimento) | pendente | régua histórica apenas | exigência textual não atendida |
| 21 | Critério: clareza na definição do problema | parcial | material técnico forte, reaproveitável das sprints 1 e 2 | deck da Sprint 3 começa na EDA, sem slide de problema |
| 22 | Critério: qualidade da análise exploratória | atendida | 01_eda com 6 seções, 14 figuras, asserts de invariante, investigação da anomalia por decomposição, perfil do Team14 | nenhuma |
| 23 | Critério: coerência da modelagem | atendida no volume | protocolo duplo de validação, 2 baselines mais 1 alternativo, overfitting testado, cobertura reportada, limites declarados | incompleta enquanto o segundo modelo não existir |
| 24 | Critério: comunicação dos resultados (storytelling) | parcial | 19 telas de slide com narrativa; este dossiê | ainda não existe `.pptx` |
| 25 | Critério: valor gerado para tomada de decisão | parcial | delimitação honesta (R² = 0,025) e leitura N1/N2 | "qual vai estourar" depende do modelo de risco; zero número de valor em reais |
| 26 | Critério: capacidade de antecipação (D+1 e D+7) | atendida | erro por horizonte no rolling; erro divulgado P2 4/dia e P3 11/dia | nenhuma |

### D. Dicionário de dados (regras de KPI e metas)

| # | Exigência oficial | Status | Evidência | Lacuna |
|---|---|---|---|---|
| 27 | Só prioridades 1, 2 e 3 entram no KPI; incidente pai preenchido não entra; status "Sem Intervenção" não entra | atendida | 02_base_kpi usa o campo oficial `Entrou para KPI? = SIM`; asserts de 122.543 e 25.600; nota de que 9.529 de monitoramento entram | nenhuma |
| 28 | OLA por prioridade: P1 e P2 até 4h, P3 até 12h, P4 24h, P5 96h | parcial | alvo tomado do campo `KPI Violado?` | a regra de duração nunca é recalculada nem confrontada com o campo |
| 29 | Metas anuais de quebras de OLA (faixas P2 e P3) | atendida | P2 42 na faixa 40 a 45 (75%); P3 196 abaixo de 201 (150%); régua completa na tela | nenhuma |
| 30 | Metas anuais de volume tratado (faixas P2 e P3) | atendida | P2 5.159 na faixa 4.585 a 5.388 (125%); P3 19.997 na faixa 19.489 a 22.116 (125%) | nenhuma |

### E. Template oficial do MVP, bloco a bloco

| # | Bloco do template | Status | Evidência | Lacuna |
|---|---|---|---|---|
| 31 | Slide 2: nome da solução, logotipo, equipe, alunos em ordem alfabética com RM | parcial | `prototipos/slides/capa-slide.html` | rotulada "Sprint 02", nome de integrante incompleto, sem RM |
| 32 | Slide 3: contextualização do problema | pendente na Sprint 3 | conteúdo existe nas sprints 1 e 2 entregues | nenhum slide novo, precisa recolar e atualizar |
| 33 | Slide 4: problema a ser resolvido | pendente na Sprint 3 | idem | idem |
| 34 | Slide 5: proposta de solução | parcial | tela do MVP; diferenciais atuais (morning briefing e score de saúde) | sem slide construído; cascata tem que estar fora da proposta |
| 35 | Slide 6: documentação de gerenciamento das sprints 1 e 2 atualizada e anexada | parcial | os dois `.pptx` anteriores existem | não foram atualizados: arquitetura ainda cita XGBoost como risco, DTW e cascata |
| 36 | Slide 6/7: imagem ou link do planejamento (Kanban) | pendente | nada | nenhum board existe |
| 37 | Slide 8: arquitetura justificada elemento a elemento e todas as fontes de dados | parcial | `arquitetura-slide.html` (Sprint 2) | desatualizada e contraditória com o deck |
| 38 | Slide 9: desenho da arquitetura | parcial | diagrama da Sprint 2 | idem |
| 39 | Slides 10 e 11: descrição da arquitetura (fontes, ingestão, armazenamento, processamento, visualização) | parcial | pipeline real nos cabeçalhos dos notebooks | não virou slide |
| 40 | Slide 12: MVP em capturas de tela com explicação detalhada de cada uma | parcial | tela do MVP em 3 abas mais PNGs | números de risco e saúde mockados; telas legadas concorrentes |
| 41 | Slide 13: indicar todas as fontes de dados utilizadas | parcial | cabeçalhos dos 3 notebooks; `holidays` BR como fonte externa | sem slide |
| 42 | Slide 13: algoritmos, métodos, manipulações e transformações | atendida como matéria-prima | 02_base_kpi (tipagem, filtro, colunas de calendário, schema do parquet); notebook 03 (Prophet, baselines, backtest) | falta transpor para slide |
| 43 | Desejável: prints do tratamento de dados | pendente | 02 seções 3 e 4; 01_eda células de `head`/`info`/`describe`/`isna` | sem slide |
| 44 | Desejável: amostra dos dados utilizados | pendente | `df_kpi.head()` no notebook 03 | sem slide |
| 45 | Desejável: modelos matemáticos e estatísticos com a lógica aplicada | atendida | IC 95% por dia da semana, sensibilidade, backtest, cobertura, r/p/R²; slides d14m, d15n e d17a | nenhuma |
| 46 | Desejável: imagens das visualizações que apoiam a decisão | atendida | 22 figuras em `notebooks/figures/`, 16 em `deck/figs/`, 65 PNGs de slide, 3 abas de dashboard | nenhuma |
| 47 | Slide 14: finalização e agradecimentos | parcial | `agradecimentos-slide.html` (Sprint 2) | reaproveitar e atualizar |
| 48 | Observação: cores, fontes e imagens fazem parte da avaliação | atendida | linguagem visual v2 do deck; design system em `brand/` | nenhuma |
| 49 | Formato: entrega em `.pptx` pelo portal FIAP ON | pendente | deck só em HTML e PNG | falta montar o arquivo |
| 50 | Regra do projeto: Django obrigatório, sem Streamlit | pendente, declarado fora de escopo | escopo da Sprint 4 | nenhum código de app; aceitável para MVP preliminar, mas é o que a banca chama de "MVP em funcionamento" |
| 51 | Regra do projeto: entrega via Docker | pendente | `requirements.txt` pinado existe | sem Dockerfile; escopo da Sprint 4 |

---

## 4. Inconsistências confirmadas na auditoria

Achados verificados um a um contra o arquivo e contra o dado. Agrupados por artefato.

> **Nota de leitura.** Cinco achados iniciais foram derrubados na verificação porque o texto já havia sido corrigido durante a própria janela de auditoria: o filtro de elegibilidade no `CLAUDE.md`, a reescrita do `context/status.md`, o badge "Prophet + XGBoost" na tela do MVP, o plano de notebooks da skill de notebook (que previa um `05_cluster` de DTW) e o exemplo de código da skill de python (que instanciava XGBoost como modelo de volume). Consequência prática: **algumas citações dos painéis de banca estão defasadas** (dois perfis ainda citam "Prophet + XGBoost" na tela do MVP, que hoje diz apenas Prophet). Ao preparar a defesa, conferir o arquivo antes de aceitar a crítica.

### 4.1 Documentos de contexto e documentação viva

| Onde | Severidade | Problema | Correção |
|---|---|---|---|
| `context/mentoria-locaweb.md`, tabela de volume mensal | Média | Outubro e novembro trocados: registra 21,5 k para 23 k para 27,3 k. Real: out 23.017, nov 21.524, dez 27.321 | Trocar para 23,0 k / 21,5 k / 27,3 k, alinhando com `docs/sprint-3-mvp.md` |
| `context/decisoes-tecnicas.md`, bloco de atualização da Sprint 3 | Média | Afirma que "o padrão de acúmulo da mentoria não foi testado", no bloco que o próprio arquivo declara como prevalente. Foi testado em 29/07 e não se sustentou (r = -0,139) | Substituir pelo resultado, com ponteiro para a seção de testados e descartados |
| `context/mentoria-locaweb.md`, nota de atualização | Média | Mesma afirmação obsoleta, no arquivo que o `CLAUDE.md` manda ler antes de qualquer decisão técnica | Atualizar com r = -0,139, Spearman -0,115 e a ressalva de que efeito por equipe não é observável |
| `context/decisoes-tecnicas.md`, stack aprovada e restrições | Média | O corpo continua prescrevendo três itens da lista negra: XGBoost como refinamento do volume, tslearn/DTW como técnica de clusterização e a restrição "usar DTW". Só o diferencial de cascata recebeu marcação inline | Marcar inline cada bloco superado, como já foi feito no diferencial cortado |
| `context/decisoes-tecnicas.md`, explicabilidade | Média | Especifica "SHAP (TreeSHAP para XGBoost)", inaplicável à regressão logística, que é o modelo escolhido. É a especificação que vai ser seguida na hora de codar | Reescrever para LinearExplainer ou coeficientes em odds ratio, com TreeSHAP só se o XGBoost baseline for exibido |
| `context/decisoes-tecnicas.md`, probabilidade de atingir KPI | Média | Descreve Monte Carlo sobre KPI mensal, enquanto `docs/sprint-3-mvp.md` define cálculo de taxa sobre a previsão contra metas anuais. Fica em aberto o que o MVP entrega | Alinhar os dois: régua anual como fonte, leitura mensal como acompanhamento, e declarar se Monte Carlo entra no MVP |
| `context/conhecimento/regras-kpi-e-anomalia-setembro.md` (status ativo) | Média | Apresenta o detector de cascata como consequência viva da regra oficial, sem nota de refutação | Anotar que foi a base de uma hipótese testada e refutada na Sprint 3 |
| `docs/sprint-3-mvp.md`, dimensão categoria/produto/IC | Média | Usa a watchlist de itens de configuração como argumento de cobertura de uma exigência oficial, mas ela não existe no protótipo (zero ocorrências) | Implementar a watchlist ou retirar o argumento, sustentando a cobertura pelo modelo de risco e pela saúde por produto |
| `CLAUDE.md`, seção de onde buscar informação | Média | Chama `context/sprints/02-arquitetura.md` de "sprint ativa", contradizendo a própria tabela de status (Sprint 2 entregue com 5,00) | Marcar como registro histórico e apontar para `docs/sprint-3-mvp.md` |
| `CLAUDE.md`, estrutura do projeto | Média | Declara um `README.md` na raiz que nunca existiu. A Sprint 4 pesa 20% em código-fonte e GitHub público | Criar o README da raiz (o que é o Cronos, dado, modelos, como rodar, equipe com RM) |
| `context/conhecimento/brand-design-system-vs-prototipo.md` (status ativo) | Média | Doutrina de "dois sistemas visuais coexistindo" já superada pela decisão do mesmo dia, e descreve JetBrains Mono como tipografia em uso, que `context/projeto.md` proíbe | Marcar como superado e remover as referências de tipografia. Mesmo tratamento para o arquivo de limites do Claude Design |

### 4.2 Notebooks

| Onde | Severidade | Problema | Correção |
|---|---|---|---|
| `notebooks/03_previsao_volume.ipynb`, células 41 e 48 | ~~Alta~~ **RESOLVIDO** | O texto de cobertura divergia do output da célula acima, porque o ajuste do Prophet não é determinístico (medimos 58,7%, 59,8% e 60,9% no P3 em três execuções da mesma célula) | Corrigido na raiz: o texto passou a reportar faixa, com a razão da variação declarada, e o valor exato fica só no output. Mesma correção aplicada em `docs/sprint-3-mvp.md` e neste dossiê |
| `notebooks/01_eda.ipynb`, célula 26 | ~~Alta~~ **RESOLVIDO 17/08** | Valor de sábado errado: o texto diz 35, que é a média do fim de semana inteiro (34,6). Sábado real é 41,9, e a própria figura da seção mostra a barra em cerca de 42. Erro propagado para `docs/sprint-3-mvp.md` e para o gabarito da sprint | Corrigir para sábado 42, domingo 27, feriado 29, ou usar o agregado que a célula imprime (fim de semana 35). Imprimir a tabela de média por dia da semana para amarrar o texto a um número visível |
| `notebooks/03_previsao_volume.ipynb`, células 36 e 48 | Média | A comparação final elege o sazonal-7 como baseline das duas séries, quando a seção 4.3 do mesmo notebook concluiu que no P2 o baseline de referência é a média-7. Isso infla o ganho do P2 de 15% para 26% | Usar o melhor baseline de cada série, ou manter o sazonal-7 como referência única declarando isso e citando a média-7 ao lado. Plotar as três curvas evita a leitura de escolha conveniente |
| `notebooks/01_eda.ipynb`, célula 34 | ~~Média~~ **RESOLVIDO 17/08** | O achado justifica a concentração por equipe dizendo que sustenta "o roteamento por especialização", funcionalidade que não existe no MVP e que foi descartada por falta de dado de capacidade | Remover a menção a roteamento, mantendo o índice de saúde por produto e a leitura de risco por equipe |

### 4.3 Deck e slides

| Onde | Severidade | Problema | Correção |
|---|---|---|---|
| Slide 4, variação B (`d04a`) | **Alta** | Janeiro a agosto de 2025 com números inventados, em rampa monotônica (2,8 a 4,0), quando a série real é plana (3,7 / 3,6 / 3,6 / 3,2 / 3,3 / 3,6 / 3,4 / 4,0). Janeiro aparece 24% abaixo do real. A variação A do mesmo slide, com a figura do notebook, mostra a série plana, então as duas se contradizem. A rampa sugere justamente a tendência de alta que o slide de escopo diz não existir. Rótulos sem unidade em jan a ago e com unidade em set a dez | Regerar a figura a partir da série real, padronizando a unidade. Se faltar tempo, deixar o slide só com a variação de figura do notebook |
| Slide 12, hipóteses descartadas (`d11a`) | Média | Subtítulo diz "duas ideias" e o slide exibe três cards. Além da contagem, "o dado não sustentou nenhuma" não descreve o terceiro caso: realocação não foi refutada, não pôde ser testada por ausência de coluna | Reescrever para três ideias, duas refutadas pelo dado e uma sem dado para ser testada |
| Slide 13, divisória (`d12a`) | Média | Rodapé anuncia "Modelo 1 de 2" e o deck termina na conclusão da previsão de volume: não existe seção do modelo 2 | Remover a numeração, ou reativar quando a seção do classificador existir. Se a intenção é sinalizar roadmap, dizer isso no texto |
| Slide 5, variações A e B (`d04m`, `d04b`) | Média | Generaliza para "por mês" um valor que só vale no par agosto/setembro. A série elegível cai para 1.634 em novembro e 1.423 em dezembro, e o gráfico ao lado mostra a queda, então texto e figura brigam na mesma tela | Prender a frase ao mês da anomalia e antecipar que a queda de nov/dez é outro fenômeno |
| Slide 17, variações A e C (`d15n`, `d15c`) | Média | "O horizonte importa pouco" não se sustenta no gráfico acima: no P3 o Prophet vai de cerca de 10,6 (D+1) a 13,7 (D+7), 29% de aumento. A variação C desenha uma sparkline artificialmente reta para ilustrar a mesma tese | Reescrever com o dado (P2 fica em cerca de 4/dia; P3 vai de cerca de 11 para 14) e plotar a curva real ou trocar por número |
| Slide 6, variação A (figura `eda_ano.png`) | Média | Travessão no título do gráfico, proibido em texto de entregável. Como está dentro do PNG, não aparece em busca no HTML | Regerar a figura com dois-pontos. Mesmo cuidado no título do viewer |
| Slides 16 e 17 | Média | Dois slides consecutivos mostram o MAE da mesma série com valores muito diferentes (P3 20,0 e 3,7 no corte único; 11,8 e 4,2 no rolling) sem uma linha que reconcilie | Acrescentar a frase de reconciliação: no corte único o P3 dá 20,0/dia, inflado pela queda de dezembro; no rolling, que re-treina a cada semana, cai para cerca de 11,8/dia, e é esse o número de operação |
| Figuras matplotlib (slides 4, 5, 6, 8, 17) | Média | Eixos com decimal em ponto (14.0, 17.5) e milhar sem separador (25000), enquanto o texto do deck usa vírgula e ponto de milhar | Aplicar formatador pt-BR nos eixos ao gerar as figuras e registrar a regra na skill de visualização |

### 4.4 Telas e protótipos

| Onde | Severidade | Problema | Correção |
|---|---|---|---|
| `mvp-mockup.html`, bloco de ativos crônicos (com selo "Análise") | **Alta** | Três das quatro linhas têm número inventado: IC00840 32 (correto), IC00720 3 (tela diz 27), IC00633 4 (tela diz 21), IC00928 7 (tela diz 18). O ranking real é IC00840 32, IC00349 24, IC00251 11, IC01285 10. A tela soma 98 quebras em 4 ativos contra 77 reais | Substituir pelos quatro reais. A nota "30 ativos concentram 62% das quebras" está correta (61,7%) e pode ficar |
| `mvp-mockup.html`, faixa de triagem (com selo "Análise") | **Alta** | Afirma que "os 5% de maior risco concentram cerca de 48% das quebras", estatística que não existe em documento canônico nenhum. O número preliminar é top 20% com cerca de 66%, e o modelo de risco não está implementado | Usar o número canônico com rótulo de teste preliminar, ou retirar a faixa até o notebook existir |
| `cascata.html` e links em `dashboard.html`, `previsao.html`, `morning-brief.html`, `saude-produto.html` | **Alta** | A cascata segue viva como área de produto: item de menu com badge, KPI de cascatas ativas, card com "classificador XGBoost, base 4.812 cascatas", CTA, manchete do brief e fatores do score. A tela ainda apresenta um modelo não declarado (k-NN) e a base de 4.812 não confere (o dataset tem 3.326 pais com filhos). A tarja de referência histórica no rodapé não aparece em screenshot recortado nem desliga o menu | Arquivar, não apagar: mover as cinco telas da Sprint 2 para pasta de histórico e deixar só a tela do MVP navegável. Arquivar preserva a prova de que a hipótese foi construída e testada |
| `previsao.html`, hero D+1 e constantes | **Alta** | A previsão é apresentada sobre a série total, incluindo P4/P5 que nunca entram no KPI (cerca de 870/dia, com linha de P4/P5). Item de lista negra | Refazer sobre a série elegível (P2 e P3, 45 a 70/dia) e apagar a linha P4/P5, ou arquivar com o resto da Sprint 2 |
| `previsao.html`, nota de treino | **Alta** | Diz "3 meses de operação estável (set a dez/2025)": a janela é 2025 inteiro, set a dez são 4 meses, e setembro é justamente o mês da anomalia, logo "estável" é falso para o período | Reescrever para a série elegível de 2025, registrando que a expansão de setembro não afetou essa série |
| `dashboard.html`, `previsao.html`, `saude-produto.html` | Média | Selos de modelo com XGBoost como motor principal em três telas; em uma delas o score de saúde é atribuído inteiro ao XGBoost | Volume: Prophet. Risco: regressão logística. Score de saúde: descrever como índice composto, ou remover o selo |
| `dashboard.html`, `morning-brief.html`, `saude-produto.html` | Média | Percentual de capacidade por equipe (87%, 92%, 64%, 38%, 28%) e sugestão de realocação, ambos não deriváveis de nenhum campo. Realocação foi descartada por ausência de dado de capacidade e escala | Trocar por métrica que existe (volume por equipe na janela e quebras por equipe) e retirar a sugestão de realocação |
| `previsao.html` e `dashboard.html` | Média | Banda de confiança divulgada como 90%, contra os 80% definidos na modelagem e usados na tela do MVP | Padronizar em 80% e divulgar o erro medido (P2 4/dia, P3 11/dia) |
| `morning-brief.html` e modal do brief no `dashboard.html` | Média | O volume de "ontem (30/dez)" não bate com o dado que a própria tela embute: 951 com "+8% vs média 30d", quando o real é 866 e a média de dezembro é 881 (logo, cerca de 2% abaixo) | Usar 866 e "-2% vs média de dezembro (881)" nos dois lugares |
| `morning-brief.html`, `dashboard.html`, `cascata.html` | Média | O IC apontado como alvo de ação (IC00014) tem 6.069 ocorrências na base total, mas zero na base elegível e zero quebras de OLA. A tela manda reforçar um ativo que não toca o KPI | Trocar por IC00840 (32 quebras) ou IC00349 (24). Se citar IC00014, deixar explícito que é volume bruto de alerta automático |
| `morning-brief.html` e `dashboard.html` | Média | Inventa uma meta de "OLA do dia igual ou acima de 95%", que não existe no regime de KPI (as metas são contagem anual por prioridade), e mostra 96,4%, muito abaixo da conformidade real (99,03%), fazendo a operação parecer pior do que é. Usa ponto decimal | Mostrar conformidade real do dia com base nas quebras e referenciar a meta anual por prioridade. Vírgula decimal |
| `dashboard.html` e `saude-produto.html` | Média | "21 produtos monitorados" não vem do dado: a base elegível tem 45 produtos distintos, e 30 com incidentes elegíveis nos últimos 30 dias. O universo de 21 é fixo em todas as janelas, inclusive na de 24h, que teve 6 | Usar 45, ou o número de produtos com incidente na janela, e recalcular alerta e saudável. Os volumes por produto e as quebras por janela estão corretos |
| `mvp-mockup.html`, constante de saúde por produto | Média | Números divergem do dataset. Mediana real: lcem 45,7 min (tela 22), lhco 75,0 (64), lsin 78,4 (138), lssl 214,3 (227). Volume em 30 dias: lcem 179 (tela 1.240), lhco 452 (980), lsin 169 (610), lssl 14 (430). Taxa de violação lssl 2,0% (tela 3,8%) | Recalcular do parquet para a janela declarada, ou mudar o rótulo para o período que os números representam. A ordem do ranking está certa |
| `mvp-mockup.html`, gráfico de 30 dias | Média | Mistura períodos e naturezas na mesma legenda: a linha de volume é série sintética de padrão semanal repetido ambientada em julho de 2026, e as barras vermelhas são a série real de quebras de dezembro de 2025. Na mesma aba o calendário é dezembro de 2025 e a página está datada em julho de 2026 | Usar os 30 dias reais de dezembro de 2025 nas duas séries, ou rotular o volume como cenário ilustrativo e tirar as barras reais do mesmo eixo |
| `mvp-mockup.html`, aba de saúde e volume | Média | O diferencial declarado é score de saúde com nota de 0 a 100, ranking, tendência e explicabilidade. A tela viva entrega tempo mediano de resolução com faixas, sem nota. A única tela com a nota é a da Sprint 2, marcada como histórica | Decidir e alinhar: ou a tela do MVP passa a mostrar a nota (composta de tempo de resolução, volume e taxa de violação, com os fatores no modal), ou os documentos param de vender "nota 0 a 100" |
| `morning-brief.html`, manchete | Média | Data residual: a edição é 31 de dezembro e o texto pede zero violações "até 31/mai", falando em reverter uma meta com prazo vencido dentro da própria narrativa | Corrigir para 31/dez |

### 4.5 Skills do projeto

| Onde | Severidade | Problema | Correção |
|---|---|---|---|
| `challenge-context/SKILL.md`, distribuição dos dados | Média | Cinco contagens 1 unidade abaixo do real (sempre a categoria modal): P3 41.732, Sem Intervenção 80.373, Monitoramento 104.299, Entrou para KPI NAO 96.943, KPI Violado em branco 96.943. Com os números da skill, nenhuma soma fecha em 122.543. Além disso, os 96.943 estão em branco, não com a string "N/A", e os rótulos de prioridade no dataset têm espaços | Corrigir as cinco contagens, trocar "N/A" por "em branco" e registrar os rótulos literais |
| `challenge-context/SKILL.md`, metas de volume | Média | Apaga a palavra "tratados" do nome da meta oficial. Combinado com a contagem do dataset inteiro, isso convida a comparar volume bruto de 3 anos contra a régua anual, o que jogaria as duas prioridades em 0% de atingimento e derrubaria o slide de régua | Renomear para volume de incidentes tratados no ano (elegíveis ao KPI) e anexar a posição fechada de 2025 já validada |
| `challenge-context/SKILL.md`, campo Duração | Média | Define Duração como tempo até a resolução. O dicionário diz abertura até resolução ou encerramento. 82.302 dos 122.543 registros têm Resolvido nulo e Duração preenchida: quem seguir só a skill descarta dois terços da base | Corrigir a definição, explicitando o fallback para Encerrado |
| `challenge-context/SKILL.md`, identificação | Média | A skill que abre todo entregável tem o grupo como "a definir" e manda perguntar, embora a equipe esteja fechada desde a Sprint 1 com RMs conhecidos. Colide com o item 1 do checklist de sprint | Fixar grupo, turma e a lista em ordem alfabética com RM, mais o mentor |
| `challenge-context/SKILL.md`, período e liberdade técnica | Média | Descreve o dataset como "3 anos" e oferece liberdade técnica com XGBoost e clusterização, sem registrar nenhuma decisão fechada do projeto nem a quebra por ano dos elegíveis. Um agente que consulte só esta skill tende a escrever "treinado em 3 anos" ou propor DTW | Acrescentar a quebra por ano (2023 87, 2024 357, 2025 25.156) e um bloco de decisões fechadas com a lista de testados e descartados |
| `sprint-checklist/SKILL.md`, bloco da Sprint 3 | Média | É a última barreira antes do `.pptx` e não tem um único item sobre os quatro desafios analíticos, sobre a régua de meta, nem trava contra ressuscitar entrega descartada | Adicionar item por desafio analítico, item de "nenhum item descartado aparece como vivo" e item de "toda métrica citada bate com o notebook executado" |
| `notebook-style/SKILL.md`, cabeçalho e carga | Média | Caminhos canônicos errados: aponta para um `data/raw/LWDATASET.xlsx` inexistente, sem a aba obrigatória, e para um parquet com outro nome. Notebook novo criado a partir da skill quebra na primeira célula ou grava um parquet paralelo | Corrigir para o arquivo e a aba reais, o parquet real e o documento vivo da Sprint 3 |
| `python-style/SKILL.md`, padrões do projeto | Média | O filtro apresentado como padrão correto compara Prioridade com '2-Alta', quando o literal no dataset é '2 - Alta'. O filtro retorna DataFrame vazio silenciosamente. As constantes de domínio têm o mesmo defeito | Usar os rótulos literais e acrescentar nota de que o filtro oficial é o campo `Entrou para KPI?` |
| `commit-style/SKILL.md`, exemplos | Média | Dois dos sete exemplos bons tratam entregas refutadas como trabalho legítimo (detector de cascata, escolha de tslearn DTW), e o exemplo de corpo inverte o achado central da EDA, chamando setembro de queda quando o volume subiu cerca de 5 vezes | Substituir pelos casos reais e vivos |
| `humanizer/SKILL.md` | Média | É a versão genérica, que trata relato neutro como defeito e manda injetar opinião e primeira pessoa, contra a preferência ativa de escrita neutra e data-first. Aplicada a um slide, produz frase punchy em deck técnico | Adicionar override no topo: em artefato do Cronos, rodar só as seções de remoção de padrões de IA. Registrar também a regra de não usar travessão |

### 4.6 Higiene de severidade baixa (não verificada individualmente)

Consolidada em lista, para não competir com os itens acima na fila de ação.

**Documentos.** Contagem de diferenciais ainda em três no `CLAUDE.md` e no título de `decisoes-tecnicas.md`; pastas inexistentes no bloco de estrutura do `CLAUDE.md`, sem `docs/` nem `prototipos/`; lista de ponteiros sem `docs/sprint-3-mvp.md` e sem este dossiê; "9 skills" quando são 10, e menção a uma skill `council` que não existe; inventário desatualizado em `context/status.md`; índice de `context/README.md` sem a preferência criada em 21/07; instrução em `sprints/01-ideacao.md` mandando manter os três diferenciais; `sprints/02-arquitetura.md` afirmando que a cascata foi validada pelo mentor e citando tipografia Inter, contra a identidade canônica; rodapés de data desatualizados em cinco arquivos; item 15 da lista de slides sem o teste de acúmulo; travessão em quase todo parágrafo de `docs/sprint-3-mvp.md`, que é a base do PPT.

**Notebooks.** 01_eda anuncia avaliação por precisão e recall, quando a régua decidida é AUC mais ganho de triagem; cabeçalho do 03 com data de 28/07 após reexecução em 29/07; aderência de 99,88% afirmada sem célula que a calcule; cobertura da banda medida só no corte congelado, sem medição sob o protocolo rolling; quartil de volume não monotônico sem menção no texto; frase de efeito no fecho da seção 4.9, contra a regra de escrita neutra; numeração de seções do 02 fora do padrão obrigatório; imports e template de plotly sem nenhuma figura plotly; próximos passos redigidos no futuro para trabalho concluído.

**Slides.** Legenda duplicada e com rótulos divergentes na variação B do slide 5; empate 4,2 contra 4,2 com selo de "melhor" apenas em um lado (a diferença real é 4,18 contra 4,20); gráfico renderizado em card pequeno com rótulos ilegíveis em projeção; espaçamento solto nos cards do slide 8; colisão de vocabulário ("origem" com dois sentidos no mesmo deck); "Pipeline única" em vez de masculino; três figuras promovidas a variação principal sem contrapartida em `notebooks/figures/`, logo sem procedência rastreável; arquivos órfãos (`d15a.html`, `figs/forecast.png`, `figs/mae.png`) ainda no diretório de render.

**Telas.** Inconsistência de mês dentro de `previsao.html` e D+1 em 1º de janeiro com previsão 4% acima da média, quando feriado roda cerca de 29/dia; barras de distribuição não proporcionais aos valores; travessão em copy visível nas seis telas (24 ocorrências na tela do MVP); roxo/lilás no mesh de fundo e gradiente azul para roxo no selo de IA, padrão que a skill de design bloqueia; `prototipos/README.md` ainda descrevendo cascata como tela ativa e o score como XGBoost mais SHAP, sem mencionar a tela do MVP; chave `total_pai` guardando os 25.600 elegíveis e lista `top_cascatas` remanescente no JSON de métricas.

**Skills.** Instrução para pedir templates que já estão versionados; Inter como fallback de fonte em `viz-style` contra o banimento em `design-taste-frontend`; default arquitetural React/Next/Tailwind em `design-taste-frontend` contra Django e HTML puro; Power BI como exemplo de entrega no checklist da Sprint 4.

---

## 5. Fraquezas sem resposta completa hoje

Consolidado honesto, com recomendação explícita para cada item.

| # | Fraqueza | Gravidade | Recomendação |
|---|---|---|---|
| 1 | **Modelo de risco de OLA não implementado**, e ele sozinho responde por três requisitos oficiais (previsão de risco, classificação ou clusterização, explicabilidade por incidente). AUC de 0,80 e top 20% com 66% já circulam como resultado, vindos de laboratório sem notebook | **Alta** | **Corrigir antes da banca.** Primeira prioridade absoluta. Enquanto não existir, nenhum material apresenta esses números como consolidados |
| 2 | **Projeção e probabilidade de atingimento do KPI ausentes.** É entregável textual da apresentação oficial e foi o pedido número 1 do mentor. Existe só a régua histórica | **Alta** | **Corrigir antes da banca.** Derivar da previsão com banda a projeção do fechamento anual e converter em probabilidade por faixa |
| 3 | **Queda de 39% no nível da série alvo entre setembro e dezembro** (2.324 para 1.423), dentro da janela de teste, sem causa verificada para novembro, enquanto quatro slides afirmam "estável em cerca de 2,3 mil por mês" e "imune à anomalia" | **Alta** | **Corrigir a redação antes da banca e assumir o limite.** Qualificar para "estável no salto de setembro" e declarar a queda de nível como aberta |
| 4 | **Baseline escolhido a favor do modelo no P2**: 26% de ganho contra o sazonal-7, quando o melhor baseline do P2 é a média-7 e o ganho real é 15% | **Alta** | **Corrigir antes da banca.** Custo baixo, retorno defensivo alto |
| 5 | **Nenhuma quantificação de incerteza nas comparações de MAE**, com critério assimétrico (empate onde perde, vitória onde ganha) e origens sobrepostas no backtest | Média | **Assumir e preparar resposta.** Se houver tempo, bootstrap por origem ou Wilcoxon. Até lá, falar em "mesmo patamar" |
| 6 | **Banda de 80% sub-cobre no P3** (60,9%), e o intervalo é a única propriedade exclusiva do Prophet frente aos alternativos | Média | **Assumir e preparar resposta.** Reportar cobertura junto do MAE e retirar a copy de "pior caso" no P3 |
| 7 | **Nenhuma métrica de viés (erro médio com sinal)** e nenhum erro medido no agregado que o produto usa (7 dias e mês), que é o que a projeção de meta soma | Média | **Corrigir antes da banca se possível** (é recomputar do backtest existente); caso contrário, assumir |
| 8 | **Rótulo de elegibilidade depende do fechamento do incidente**, então o alvo não é observável em D+1 e o backtest é otimista frente à produção. Tempo de consolidação não medido | Média | **Assumir e preparar resposta**, com o desenho de pipeline descrito (janela consolidada, descarte dos últimos dias, realizado marcado como parcial) |
| 9 | **Seleção de configuração sobre o conjunto de teste**, sem validação separada, e o único período de teste é o trecho de regime atípico | Média | **Assumir** com os três mitigantes. Baixo custo: abrir o erro do rolling por mês |
| 10 | **Tese "o resíduo é ruído irredutível" sem teste direto**: sem ACF, sem Ljung-Box, sem regressor exógeno testado | Média | **Corrigir a redação antes da banca** (teto do sinal de calendário) e rodar o teste de autocorrelação, que é barato |
| 11 | **Explicabilidade sem SHAP e sem atribuição por incidente**; o painel de fatores da tela usa pesos ilustrativos com aparência de saída de modelo | Média | **Corrigir antes da banca**: rotular como ilustração de interface, e ligar à saída real quando o modelo existir |
| 12 | **Zero número de valor**: sem custo por violação, quebras evitáveis, horas de retrabalho, nem custo de operação (tokens da Claude API, pedido explícito do mentor). Colide com o feedback da Sprint 1 | Média | **Assumir e preparar resposta**, pedindo o custo por violação à Locaweb e comprometendo a simulação de custo para a Sprint 4 |
| 13 | **Nenhum fluxo operacional definido**: sem canal de entrega, sem integração com a fila de tickets, sem dono da ação, sem prazo de resposta do alerta | Média | **Assumir e preparar resposta.** Levar um slide com o desenho do fluxo, mesmo sem implementação |
| 14 | **Números fabricados na tela viva do MVP**: ativos crônicos, corte de 5% com 48%, saúde por produto, 21 produtos, gráfico de 30 dias misturando períodos | **Alta** | **Corrigir antes da banca.** A tela é o print do slide 12: um número conferido pela banca derruba o bloco |
| 15 | **Legado da Sprint 2 vivo e navegável**: cascata com base inventada, XGBoost como motor, banda de 90%, previsão sobre o volume total, IC sem quebras como alvo de ação | **Alta** | **Corrigir antes da banca.** Arquivar as cinco telas e registrar que apenas a tela do MVP é a tela da Sprint 3 |
| 16 | **Moldura do template ausente**: 8 dos 14 blocos sem slide, nenhum `.pptx`, nenhum Kanban, capa da Sprint 2 sem RM | **Alta** | **Corrigir antes da banca.** É o risco de nota mais previsível e o mais mecânico de resolver |
| 17 | **Requisitos textuais de EDA em aberto**: sazonalidade horária, agrupamentos críticos por produto mais categoria mais prioridade, incidentes recorrentes, tendência diária de perda de OLA | Média | **Corrigir antes da banca.** Quatro seções de baixo esforço que fecham quatro exigências literais |
| 18 | **Alvo nunca confrontado com a regra de duração do dicionário** | Média | **Corrigir antes da banca.** Uma célula de invariante e um print |
| 19 | **Documentos vivos com número ou afirmação obsoleta** (out/nov trocados, acúmulo "não testado", DTW como mandato, TreeSHAP para logística, sábado 35 em vez de 42) | Média | **Corrigir antes da banca.** Baixo esforço, e evita a pior categoria de erro: o material contradizendo a si mesmo |
| 20 | **Divisão de trabalho não comprovável**: commits de um único autor, coluna de função vazia | Média | **Assumir e preparar resposta**, declarando a divisão no slide de gestão |
| 21 | **Diferenciais restantes nunca validados contra o dado**: score de saúde sem fórmula publicada nem teste de que anteceda quebra, e sem a nota de 0 a 100 na tela viva | Média | **Assumir e preparar resposta** (índice composto, não predição) e alinhar discurso com tela |
| 22 | **Django e Docker inexistentes** | Baixa no contexto do MVP preliminar | **Aceitar o risco**, com resposta preparada e escopo declarado para a Sprint 4 |
| 23 | **Ausência de fundamentação bibliográfica** | Baixa | **Aceitar o risco** ou resolver em 30 minutos, com três referências |
| 24 | **Gráficos com dado inventado no deck** (rampa de jan a ago no slide 4, sparkline decorativa de abertura, sparkline reta no slide 17) | **Alta** | **Corrigir antes da banca.** Gráfico ilustrativo em slide de resultado é o que custa credibilidade mais rápido |
| 25 | **Notebook 03 com markdown fora de sincronia com o output** e dúvida sobre saídas comitadas | **Alta** | **Corrigir antes da banca.** Reexecutar, comitar com saídas e sincronizar o texto |

---

## 6. Pontos fortes a explorar na apresentação

1. **Rolling backtest com re-treino por origem e erro por horizonte D+1 a D+7**, reproduzindo o uso real, com origens espaçadas para cobrir todos os dias da semana e sem vazamento (defasagens de 7 e 14 são válidas para horizonte de até 7 dias, e feriados são conhecidos de antemão). Protocolo acima do usual em trabalho de graduação, e o oposto do erro clássico da turma, que é holdout aleatório em série temporal.
2. **Comparação contra dois baselines ingênuos mais um modelo alternativo interpretável**, com a coragem de dar o selo de melhor ao baseline no P3. A tese "o limite é do sinal disponível" fica demonstrada por convergência de métodos, não afirmada.
3. **Teste explícito de overfitting** com leitura de treino contra teste em três configurações: flexibilidade alta baixa o treino de 10,23 para 9,50 e estraga o teste de 19,96 para 26,13. Diagnóstico clássico, feito e documentado, com a decisão correta de manter o padrão.
4. **Investigação da anomalia de setembro por decomposição em cinco dimensões** (monitoramento 2.404 para 20.008, "Sem Intervenção" 47 para 17.838, ICs vistos pela primeira vez 458 para 1.693, abertura manual estável, série elegível 2.330 para 2.324), concluindo expansão de instrumentação e não piora da operação. Responde com número a um pedido explícito do mentor, e a decisão de alvo do modelo deriva desse achado.
5. **Escopo temporal fundamentado com número**: 87, 357 e 25.156 elegíveis por ano mostram que o crescimento é adoção de registro, e treinar em cima disso ensinaria uma tendência falsa. Sazonalidade anual desligada pelo motivo certo.
6. **Feature de calendário nascida de teste estatístico**, não de suposição: os intervalos de confiança de 95% da média por dia da semana se sobrepõem entre dias úteis, então o modelo trata dia útil como um nível único em vez de aprender sete perfis. É a justificativa mais elegante do trabalho.
7. **Cobertura empírica da banda medida e reportada mesmo quando reprova** (85,9% no P2, 60,9% no P3). Medir calibração de intervalo é raro nesse nível, e publicar o resultado ruim é mais raro ainda.
8. **Verificação de censura à direita antes de culpar o modelo** pela queda de nov/dez: 100% dos registros com encerramento, último em 31/12/2025 23:45, mais a decomposição por terço do mês (305 contra 556) e a queda de share do elegível (58,3% para 5,2%). Instinto certo e método certo.
9. **Resultados negativos registrados com critério quantitativo, inclusive contra o interesse próprio**: cascata refutada (87% das quebras são isoladas, escalada 21% contra cerca de 60% do acaso), DTW com silhueta 0,13, acúmulo do próprio mentor sem suporte (r = -0,139), realocação descartada por ausência de coluna de capacidade.
10. **Honestidade sobre o alcance do próprio produto**: publicar que o volume explica só 2,5% da variação de quebras enfraquece a narrativa comercial e fortalece a defesa técnica. Declarar antes da pergunta desarma o avaliador.
11. **Leitura N1 contra N2 como insight de gestão com número**: Team14 com 75,7% do volume total e 10 quebras, Team11 com 8% do volume e 46% das quebras. É a frase que o gestor leva para a reunião de operações.
12. **Concentração em ativos crônicos como alavanca acionável e verificada**: 30 ICs respondem por 61,7% das 248 quebras, e 55 das 111 quebras do segundo semestre ocorreram em ativos que já tinham quebrado no primeiro. Acionável na segunda-feira, sem modelo nenhum.
13. **Aderência ao processo do cliente**: régua de meta por prioridade com as faixas oficiais e o atingimento real, usando o campo oficial `Entrou para KPI?` em vez de reimplementar a regra, com 99,88% de concordância. Base compartilhada reprodutível, com tipagem e asserts de invariante nos dois números mais citados do projeto.
14. **Existência deste dossiê**: revisão adversarial em quatro perfis, auditoria de artefatos, matriz de conformidade e plano priorizado. Postura de quem sabe onde o trabalho é frágil, que é o melhor sinal de maturidade metodológica no conjunto do material.

---

## 7. Plano de ação priorizado

| # | Ação | Impacto na nota | Esforço |
|---|---|---|---|
| 1 | Implementar `notebooks/04_risco_ola.ipynb`: regressão logística com features disponíveis na abertura, XGBoost como baseline, validação out-of-time, curva de ganho e triagem, explicabilidade (coeficientes em odds ratio mais SHAP linear), comparação contra a régua trivial "P3 mais Team11". Destrava três requisitos oficiais | **Muito alto** | Alto |
| 2 | Derivar a projeção de atingimento do KPI da previsão de volume com banda, convertendo em probabilidade por faixa de meta, e construir o slide. Entregável textual e pedido número 1 do mentor | **Muito alto** | Médio |
| 3 | Montar o `.pptx` no template oficial: os 8 blocos ausentes (capa com RM, contextualização, problema, proposta, gestão, arquitetura em 3 slides, agradecimentos), reaproveitando as sprints 1 e 2 atualizadas e importando os PNGs do deck. Reservar tempo de calendário | **Muito alto** | Alto |
| 4 | Criar o Kanban com as tarefas reais das três sprints, exportar imagem e incluir o link. É o único ponto de melhoria que o professor apontou na Sprint 2 | **Alto** | Baixo |
| 5 | Corrigir o ganho do P2 para 15% sobre o melhor baseline em notebook, documento e slides, recolocando a média-7 na tabela final | **Alto** | Baixo |
| 6 | Qualificar em todo material a afirmação de imunidade à anomalia ("estável no salto de setembro") e declarar a queda de nível de outubro a dezembro como limite aberto | **Alto** | Baixo |
| 7 | Corrigir os números fabricados na tela viva do MVP: ativos crônicos, corte de triagem, saúde por produto, universo de produtos, série de 30 dias. Rotular como ilustração de interface todo bloco sem modelo por trás | **Alto** | Médio |
| 8 | Arquivar as cinco telas da Sprint 2 em pasta de histórico e registrar que apenas a tela do MVP é a tela da Sprint 3. Atualizar `prototipos/README.md` | **Alto** | Baixo |
| 9 | Refazer os slides de arquitetura e de tecnologias com a stack real (Prophet para volume, regressão logística para risco, SHAP, sem tslearn/DTW, sem cascata) e marcar a agnosticidade de cloud | **Alto** | Médio |
| 10 | Reexecutar e comitar o notebook 03 com saídas preservadas; sincronizar o texto de cobertura com o output e registrar a não determinação do ajuste | **Alto** | Baixo |
| 11 | Regerar a figura de volume mensal com a série real e substituir os dois gráficos decorativos por figuras plotadas; padronizar unidade e formato pt-BR nos eixos | **Alto** | Baixo |
| 12 | Corrigir o valor de sábado (42, não 35) em notebook, documento e gabarito, imprimindo a tabela de média por dia da semana | Médio | Baixo |
| 13 | Fechar os quatro requisitos textuais de EDA: perfil horário, agrupamentos críticos (produto x categoria x prioridade), recorrência por item de configuração, série diária de quebras de OLA com média móvel. Ligar os números da tela a essas saídas | **Alto** | Médio |
| 14 | Adicionar em 02_base_kpi a célula de invariante que recalcula a violação a partir de Duração e cruza com o campo `KPI Violado?`, e a célula que materializa os 99,88% de aderência | Médio | Baixo |
| 15 | Construir o slide de fontes de dados e pipeline (dataset, aba, filtro, parquet, modelos, figuras e telas, mais `holidays` BR) e os dois slides desejáveis (tratamento de dados e amostra) | Médio | Baixo |
| 16 | Reportar erro médio com sinal e erro do agregado de 7 dias e do mês; rodar teste de autocorrelação do resíduo e corrigir a redação de "ruído irredutível" para "teto do sinal de calendário" | Médio | Médio |
| 17 | Corrigir os documentos vivos: out/nov trocados, acúmulo testado, DTW e XGBoost marcados como superados inline, TreeSHAP trocado por explicador linear, ponteiro de sprint ativa, README da raiz | Médio | Baixo |
| 18 | Corrigir as skills que produzem erro por cópia: contagens da `challenge-context`, rótulos literais de prioridade em `python-style`, caminhos em `notebook-style`, exemplos de `commit-style`, override neutro no `humanizer`, itens novos no `sprint-checklist` | Médio | Baixo |
| 19 | Preparar as respostas de negócio que dependem da Locaweb: custo por violação de OLA e simulação de custo de token, mais o desenho do fluxo operacional (canal, dono, prazo, integração) em um slide | Médio | Médio |
| 20 | Higiene final: travessão fora de toda copy de entregável (tela do MVP, títulos de figura, viewer), paleta sem lilás, arquivos órfãos do deck removidos, chaves do JSON de métricas renomeadas, três referências bibliográficas | Baixo | Baixo |calma
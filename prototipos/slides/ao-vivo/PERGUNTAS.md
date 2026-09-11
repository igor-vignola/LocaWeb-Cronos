# Banco de perguntas da banca · deck ao vivo de 15/09/2026

Uma banca simulada (dois professores de ciência de dados e o mentor da Locaweb)
passou pelos slides e listou o que perguntaria. Aqui está cada pergunta com a
resposta em uma ou duas frases, o número que a sustenta e onde ele está. Quem
apresenta deve saber estas de cor; as demais são reserva.

Fonte dos números: `CONTRATO.md` §5 e os scripts `_figuras_*.py` desta pasta.
Os ponteiros `→ slide N` valem para o deck de **32 slides** de 11/09/2026.

## As que derrubam

**1. "Por que regressão logística e não gradient boosting? Qual a métrica?"**
Testamos as duas. A área ROC empatou (0,869 contra 0,868). Na métrica que vale
para evento raro, a PR-AUC, a logística ganhou: 0,296 contra 0,253. E ela está
calibrada: prevê 48,1 quebras onde houve 50; o XGBoost com balanceamento previu
1.007. Acurácia não serve porque 99% dos incidentes não quebram.
→ **Esta comparação saiu do deck em 11/09/2026**, por custar 53 segundos de
explicação de métrica. Os números vivem aqui. A afirmação curta está no pé do
slide 21: a logística empata na ordenação, ganha no evento raro e diz o porquê
de cada nota. A armadilha da acurácia está no pé do slide 11.

**2. "A faixa de 80% do Prophet cobre só 60% dos dias no P3. A incerteza não
está subestimada?"**
Está mais estreita que o nominal no P3, e dizemos isso no slide. O erro médio
absoluto é de 11 incidentes por dia num fluxo de 67, 16%. A faixa serve como
ordem de grandeza para dimensionar o dia, não como intervalo de garantia. No P2
a cobertura fica entre 86% e 88%. → slide 17, pé.

**3. (Douglas) "Olhar os 50 primeiros da fila dá quanto trabalho por dia?"**
A fila é dos incidentes abertos naquele momento, não do ano: em 1º de outubro
às 15h eram 49 abertos somando as duas prioridades. Os 50 primeiros da avaliação
correspondem a menos de um dia de fila. → slide 20.

## Sobre o dado

**"Como vocês sabem que o salto de setembro foi monitoramento automático?"**
Porque a série elegível ao KPI não se moveu: 2.330 em agosto, 2.324 em setembro,
enquanto o total registrado foi de 3.996 para 21.561. O que cresceu ficou fora
do KPI, ou seja, é registro sem intervenção humana ou com incidente pai. → slide 8.

**"Com um ano de dado e sazonalidade anual desligada, o que acontece em
janeiro?"**
O modelo carrega a sazonalidade semanal e os feriados nacionais; a anual não
existe na base para aprender. Em janeiro ele vai errar mais, e o re-treino
mensal corrige. Preferimos isso a aprender uma tendência de alta que era adoção
de registro. → slide 9.

**"Por que 2023 e 2024 têm 87 e 357 elegíveis? Mudou o processo?"**
O campo "Entrou para KPI" só passou a ser preenchido de forma sistemática em
2025. Antes disso o registro existe, mas não a marcação. → slide 9.

**"Vocês olharam volume? Dia cheio não quebra mais?"**
Olhamos, e não quebra: o volume do dia explica 2,5% da variação das quebras
(r = 0,159; p = 0,011). Foi isso que nos levou a procurar outros sinais, e o que
apareceu foi quem abre o chamado e quando ele chega. → slide 10.

**"O fim de semana só aparece na prioridade 3. E na 2?"**
Na prioridade 2 o efeito some: 0,75% no fim de semana contra 0,83% no dia útil.
Está escrito no slide. O de quem abre vale nas duas, com 3,0 vezes na 2 e 3,1
na 3. → slide 10.

**"Metade das quebras em item que já quebrou: isso não é vazamento? Como vocês
definem 'já tinha quebrado'?"**
A conta olha só para trás. Para cada uma das 238 quebras de 2025, a pergunta é
se houve **outra quebra do mesmo item antes dela** — então a primeira quebra de
cada item nunca conta, e nenhuma célula usa o próprio futuro. Dá 116 de 238,
49%, caindo em 25 itens de configuração. Por prioridade: P3 105 de 196 e P2 11
de 42. Medido de outro jeito, usando o primeiro semestre como histórico e o
segundo como teste, dá 53 de 107, 50% — o mesmo número, então o recorte não
escolhe o resultado. → slide 13.

## Sobre os modelos

**"De onde vem o 4 e o 11 de erro?"**
Do backtest deslizante, com re-treino a cada origem e média de D+1 a D+7. É o
protocolo que reproduz o uso real. No corte único de outubro a dezembro o P3 dá
20 por dia, inflado pela queda de novembro e dezembro. → slide 18.

**"De onde sai a projeção anual? É o Prophet?"**
Não. É a soma do que já aconteceu no ano com o ritmo médio de quebras até a
data, projetado até dezembro, com faixa pela variação do ritmo. → slide 25.

**"A projeção do P3 errou em agosto, setembro e outubro."**
Errou para o lado pessimista: apontou estouro e o ano fechou em 196, abaixo de
200. Para um alarme, avisar sem precisar é melhor que não avisar. Em novembro e
dezembro acertou a chamada. → slide 25, pé.

**"A projeção de dezembro do P3 disse 183 e o ano fechou em 196."**
Sim, e a chamada estava certa (dentro da meta). O ponto ficou otimista em 13
incidentes porque novembro e dezembro tiveram menos quebras que a média do ano.

**"O 263 do P3 é a meta? Porque a operação fechou em 196 e vocês chamam de
'dentro'. Dentro de quê?"**
Duas coisas, e a primeira é a que confunde. **A meta é invertida**: não é um
número para alcançar, é um teto para não passar — quanto menos quebra, maior a
nota do ano. E o KPI não é um teto único, é uma **escada de faixas** da
Locaweb, com o 263 sendo o
teto do degrau que vale 100%.

E atenção ao sentido da porcentagem: ela é a **nota que a operação tira**, e não
quanto se passou do limite. Ela **sobe quando a quebra cai**. No P3: fechando o
ano com até 200 violações a nota é 150%, de 201 a 230 é 125%, de 231 a 263 é
100%, de 264 a 290 cai para 75%, de 291 a 320 para 50%, e acima disso zero. No
P2 a escada é 30, 35, **39**, 45, 53. Em 2025 o P2 fechou em 42, que dá nota
75%, e o P3 em 196, que é a melhor faixa que existe, nota 150%. A projeção de
outubro dava 43,5 no P2 e 208 no P3, ou seja, nota 75% e nota 125%: os dois
vereditos batiam. O
deck usa "42 de 39 permitidas" em vez da porcentagem porque a porcentagem não
se lê de relance. → slide 25.

## Sobre o produto

**"Para que a Claude API, se ela só escreve uma frase?"**
Hoje ela **não está no ar**: o texto de abertura do resumo é montado por regra a
partir da saída dos modelos, dentro do próprio contêiner, e nenhum número passa
por modelo de linguagem. A ideia declarada desde a Sprint 1 é gerar essa frase
com a Claude API, para o resumo mudar de tom conforme o dia — dia normal, dia
acima do previsto, quebra ontem — em vez de escolher entre três textos fixos. É
próximo passo, não entrega, e o slide da stack diz isso. → slide 23, pé.

**(Douglas) "A cor do gráfico e a ordem não batem. Por quê?"**
Porque medem coisas diferentes, e o slide diz isso. A posição é o tamanho do
problema, que é a nota. A cor é o tipo, e é ela que muda a ação: um produto em
"problema já materializado" recebe casos que ninguém viu antes e precisa de
procedimento novo; um em "conhecido e recorrente" perde prazo no problema de
sempre e precisa de capacidade. O lvps tem a pior nota e é do segundo tipo.
→ slide 26.

**"O que é a nota de saúde?"**
Cinco medidas por produto, cada uma em posição relativa entre os 15: taxa de
perda de prazo, proporção de problemas inéditos, fechados sem causa, duração
mediana e tendência da taxa. A nota é a média das posições, de 0 a 100. Soma
P2 e P3; a tela mostra as duas separadas.

**"Como re-treina? De onde vem o dado no dia a dia?"**
O contêiner lê a exportação do ITSM (o mesmo formato do dataset), recalcula a
base elegível e re-treina os dois modelos por comando. No MVP o relógio está
parado em 1º de outubro de 2025 porque é a última data com dado, e porque o
sistema não pode mostrar realizado depois do corte. → slide 29.

**"Por que o relógio parado em 01/10/2025?"**
Para a demonstração ser honesta: tudo o que a tela mostra existia naquele
instante. Cobertura, acertos e erros dos modelos ficam nos slides, medidos
depois, e não na tela. → slide 30.

## Números que ficaram fora do deck e podem ser pedidos

- Erro médio do Prophet: 4 incidentes por dia no P2, 11 no P3 (backtest deslizante, D+1 a D+7)
- Concentração: Team11 e Team14 atendem o mesmo volume e a taxa do Team11 é 11,8 vezes a do Team14
- Os 30 itens de configuração com mais perdas concentram 61,3% das quebras de 2025
- Quebras isoladas: 87% das quebras são de incidentes sem escalada
- DTW, cascata, ARIMA e Streamlit foram testados ou considerados e descartados; não citar como parte da solução

## Sobre as escolhas do deck

**"Por que 32 slides para 15 minutos?"**
Porque sete deles são divisórias de oito segundos e um é a demonstração, que
consome quatro minutos. Sobram vinte e quatro slides de conteúdo, a vinte e
cinco segundos cada. A regra que seguimos: é melhor ficar dez segundos num
slide limpo do que um minuto num amontoado. A regra que seguimos: é melhor ficar dez segundos num slide limpo do
que um minuto num amontoado.

**"Vocês testaram alguma hipótese que não funcionou?"**
Sim, três. O detector de cascata, que propusemos na ideação: 87% das quebras
são de incidentes isolados e a taxa de escalada observada, 21%, ficou abaixo do
esperado por acaso. O padrão de acúmulo que o senhor descreveu na mentoria: o
backlog diário tem correlação levemente negativa com quebras, r = −0,139. E
clusterização de séries por DTW, com silhueta de 0,13, sem estrutura de grupos.
As três estão documentadas no repositório. Não estão no deck porque ele fala do
que foi entregue.

## Sobre os slides novos deste deck

**"A prioridade 2 é a mais alta. Por que a 3 quebra mais?"**
Porque prioridade mede o impacto para o cliente, não o aperto do prazo. A P3
tem doze horas e a P2 quatro, mas a P3 concentra quatro vezes mais volume e
recebe atenção depois. Na base de três anos a taxa é 1,01% na P3 contra 0,81%
na P2: 206 quebras em 20.441 contra 42 em 5.159. → slide 6.

**"Se um modelo que nunca sinaliza nada acerta 99%, como vocês avaliam o de
vocês?"**
Não pela acurácia. Na base de avaliação, 50 dos 5.183 incidentes quebraram, uma
a cada 103; nunca sinalizar dá 99,04% e encontra zero. O nosso, sinalizando os
518 de maior risco, cai para 90,24% de acurácia e encontra 31 das 50. O que
medimos é quantas quebras aparecem nas primeiras posições da fila, mais a
PR-AUC e a calibração, que não têm mais slide próprio. → slide 20.

**"Vocês dizem dois modelos numa tela e quatro coisas na outra. Quantos são?"**
Dois modelos: Prophet para o volume e regressão logística para o risco. As
outras duas saídas são cálculos derivados deles: a projeção da meta soma três
parcelas (o que já aconteceu, o que a fila aberta ainda deve virar e o que
entra até dezembro) e a nota de saúde é um índice de cinco medidas por produto.
O slide 28 traz as quatro com a etiqueta de cada uma. → slide 28.

**"De onde saem os 76% do slide 28?"**
Da mesma base de avaliação da fila: ordenando os 5.183 incidentes pelo risco do
modelo, os 20% do topo (1.037 posições) contêm 38 das 50 quebras. → slide 28.

**"Na prioridade 3 o baseline ganha do Prophet. Por que manter o Prophet?"**
Por três motivos. A diferença é de 4,5% no erro médio, dentro do ruído do
protocolo. O Prophet ganha por 15% na prioridade 2, onde a meta estourou.
E ele devolve faixa e componentes de calendário, que o baseline não devolve e
que o resumo das 07h e a projeção do ano precisam. O baseline continua no deck
como piso de comparação. → slide 18.

**(Douglas) "O código de fechamento Outro estoura três vezes mais. Por que ele
não entra no modelo?"**
Porque só existe depois que o incidente fecha, e o modelo pontua na abertura.
Usá-lo seria olhar o gabarito. Ele entra como apontamento de processo: 1.596
incidentes fechados como Outro em nove meses, 43 deles fora do prazo, taxa de
2,69% contra 0,94% da média. → slide 14.

**"Chamado aberto pelo monitoramento entra no KPI ou não? No slide 8 vocês
dizem que o salto de setembro ficou de fora, e no 10 dizem que o
monitoramento quebra menos."**
Entra, quando alguém trabalha nele. Quem decide não é o abridor, é o campo
`Entrou para KPI?`, que exige prioridade 1, 2 ou 3, incidente sem pai e status
diferente de "Sem Intervenção". Em setembro de 2025 chegaram **20.008**
registros de monitoramento e só **897** entraram, 4,5%: o resto fechou sem
intervenção humana ou pendurado num incidente pai. Dos 1.553 manuais do mesmo
mês, 1.427 entraram, 92%. No ano inteiro a base elegível tem **9.485** abertos
por monitoramento e 15.671 manuais, e é entre esses que a taxa é 0,46% contra
1,24%. Faz sentido: o alerta automático nasce no instante em que o problema
aparece, com o prazo inteiro pela frente; o chamado manual nasce quando alguém
percebe, às vezes já tarde. → slides 8 e 10.

**"Nos 50 primeiros da fila, por que a regra do ativo crônico acha zero?"**
Porque 357 incidentes empatam no topo dela, todos com o mesmo número de
violações no ativo. Desempatando por número de incidente, que é o critério
neutro, nenhum dos 50 primeiros violou. Se o empate for desfeito na ordem em
que o arquivo está gravado, que é a ordem do próprio modelo, a regra sobe para
9 — mas aí ela está usando o modelo, e não competindo com ele. → slide 20.

**"A Claude API está no ar?"**
Não. O texto de abertura do resumo é montado por regra a partir da saída dos
modelos, dentro do próprio contêiner, e nenhum número passa por modelo de
linguagem. Gerar essa frase com um é próximo passo declarado desde a Sprint 4,
e por isso ela aparece fora do contorno no slide 29. → slides 23 e 29.

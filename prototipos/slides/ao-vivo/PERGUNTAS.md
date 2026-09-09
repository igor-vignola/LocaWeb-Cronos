# Banco de perguntas da banca · deck ao vivo de 15/09/2026

Uma banca simulada (dois professores de ciência de dados e o mentor da Locaweb)
passou pelos slides e listou o que perguntaria. Aqui está cada pergunta com a
resposta em uma ou duas frases, o número que a sustenta e onde ele está. Quem
apresenta deve saber estas de cor; as demais são reserva.

Fonte dos números: `CONTRATO.md` §5 e os scripts `_figuras_*.py` desta pasta.

## As que derrubam

**1. "Por que regressão logística e não gradient boosting? Qual a métrica?"**
Testamos as duas. A área ROC empatou (0,869 contra 0,868). Na métrica que vale
para evento raro, a PR-AUC, a logística ganhou: 0,296 contra 0,253. E ela está
calibrada: prevê 48,1 quebras onde houve 50; o XGBoost com balanceamento previu
1.007. Acurácia não serve porque 99% dos incidentes não quebram. → slide 13, pé.

**2. "A faixa de 80% do Prophet cobre só 60% dos dias no P3. A incerteza não
está subestimada?"**
Está mais estreita que o nominal no P3, e dizemos isso no slide. O erro médio
absoluto é de 11 incidentes por dia num fluxo de 67, 16%. A faixa serve como
ordem de grandeza para dimensionar o dia, não como intervalo de garantia. No P2
a cobertura fica entre 86% e 88%. → slide 12, pé.

**3. (Douglas) "Olhar os 50 primeiros da fila dá quanto trabalho por dia?"**
A fila é dos incidentes abertos naquele momento, não do ano: em 1º de outubro
às 15h eram 49 abertos somando as duas prioridades. Os 50 primeiros da avaliação
correspondem a menos de um dia de fila. → slide 13.

## Sobre o dado

**"Como vocês sabem que o salto de setembro foi monitoramento automático?"**
Porque a série elegível ao KPI não se moveu: 2.330 em agosto, 2.324 em setembro,
enquanto o total registrado foi de 3.996 para 21.561. O que cresceu ficou fora
do KPI, ou seja, é registro sem intervenção humana ou com incidente pai. → slide 7.

**"Com um ano de dado e sazonalidade anual desligada, o que acontece em
janeiro?"**
O modelo carrega a sazonalidade semanal e os feriados nacionais; a anual não
existe na base para aprender. Em janeiro ele vai errar mais, e o re-treino
mensal corrige. Preferimos isso a aprender uma tendência de alta que era adoção
de registro. → slide 8.

**"Por que 2023 e 2024 têm 87 e 357 elegíveis? Mudou o processo?"**
O campo "Entrou para KPI" só passou a ser preenchido de forma sistemática em
2025. Antes disso o registro existe, mas não a marcação. → slide 8.

**"Vocês olharam volume? Dia cheio não quebra mais?"**
Olhamos, e não quebra: o volume do dia explica 2,5% da variação das quebras
(r = 0,159; p = 0,011). Foi isso que nos levou a procurar outros sinais, e o que
apareceu foi quem abre o chamado e quando ele chega. → slide 9.

**"O fim de semana só aparece na prioridade 3. E na 2?"**
Na prioridade 2 o efeito some: 0,75% no fim de semana contra 0,83% no dia útil.
Está escrito no slide. O de quem abre vale nas duas, com 3,0 vezes na 2 e 3,1
na 3. → slide 9.

## Sobre os modelos

**"De onde vem o 4 e o 11 de erro?"**
Do backtest deslizante, com re-treino a cada origem e média de D+1 a D+7. É o
protocolo que reproduz o uso real. No corte único de outubro a dezembro o P3 dá
20 por dia, inflado pela queda de novembro e dezembro. → slide 11.

**"De onde sai a projeção anual? É o Prophet?"**
Não. É a soma do que já aconteceu no ano com o ritmo médio de quebras até a
data, projetado até dezembro, com faixa pela variação do ritmo. → slide 14.

**"A projeção do P3 errou em agosto, setembro e outubro."**
Errou para o lado pessimista: apontou estouro e o ano fechou em 196, abaixo de
200. Para um alarme, avisar sem precisar é melhor que não avisar. Em novembro e
dezembro acertou a chamada. → slide 14, pé.

**"A projeção de dezembro do P3 disse 183 e o ano fechou em 196."**
Sim, e a chamada estava certa (dentro da meta). O ponto ficou otimista em 13
incidentes porque novembro e dezembro tiveram menos quebras que a média do ano.

## Sobre o produto

**"Para que a Claude API, se ela só escreve uma frase?"**
Para a frase não ser um template: ela lê os números do dia e escreve a abertura
do resumo em linguagem de operação. Nenhum número passa por ela. Poderia ser um
template, e escolhemos o texto gerado porque o resumo muda de tom conforme o
dia (dia normal, dia acima do previsto, quebra ontem). → slide 16, pé.

**(Douglas) "A cor do gráfico e a ordem não batem. Por quê?"**
Porque medem coisas diferentes, e o slide diz isso. A posição é o tamanho do
problema, que é a nota. A cor é o tipo, e é ela que muda a ação: um produto em
"problema já materializado" recebe casos que ninguém viu antes e precisa de
procedimento novo; um em "conhecido e recorrente" perde prazo no problema de
sempre e precisa de capacidade. O lvps tem a pior nota e é do segundo tipo.
→ slide 17.

**"O que é a nota de saúde?"**
Cinco medidas por produto, cada uma em posição relativa entre os 15: taxa de
perda de prazo, proporção de problemas inéditos, fechados sem causa, duração
mediana e tendência da taxa. A nota é a média das posições, de 0 a 100. Soma
P2 e P3; a tela mostra as duas separadas.

**"Como re-treina? De onde vem o dado no dia a dia?"**
O contêiner lê a exportação do ITSM (o mesmo formato do dataset), recalcula a
base elegível e re-treina os dois modelos por comando. No MVP o relógio está
parado em 1º de outubro de 2025 porque é a última data com dado, e porque o
sistema não pode mostrar realizado depois do corte. → slide 18.

**"Por que o relógio parado em 01/10/2025?"**
Para a demonstração ser honesta: tudo o que a tela mostra existia naquele
instante. Cobertura, acertos e erros dos modelos ficam nos slides, medidos
depois, e não na tela. → slide 18.

## Números que ficaram fora do deck e podem ser pedidos

- Erro médio do Prophet: 4 incidentes por dia no P2, 11 no P3 (backtest deslizante, D+1 a D+7)
- Concentração: Team11 e Team14 atendem o mesmo volume e a taxa do Team11 é 11,8 vezes a do Team14
- Os 30 itens de configuração com mais perdas concentram 61,3% das quebras de 2025
- Quebras isoladas: 87% das quebras são de incidentes sem escalada
- DTW, cascata, ARIMA e Streamlit foram testados ou considerados e descartados; não citar como parte da solução

## Sobre as escolhas do deck

**"Por que 22 slides para 15 minutos?"**
Porque três deles são divisórias de oito segundos e um é a demonstração, que
consome quatro minutos. O tempo médio de fala dos outros dezoito é de trinta e
cinco segundos. A regra que seguimos: é melhor ficar dez segundos num slide
limpo do que um minuto num amontoado.

**"Vocês testaram alguma hipótese que não funcionou?"**
Sim, três. O detector de cascata, que propusemos na ideação: 87% das quebras
são de incidentes isolados e a taxa de escalada observada, 21%, ficou abaixo do
esperado por acaso. O padrão de acúmulo que o senhor descreveu na mentoria: o
backlog diário tem correlação levemente negativa com quebras, r = −0,139. E
clusterização de séries por DTW, com silhueta de 0,13, sem estrutura de grupos.
As três estão documentadas no repositório. Não estão no deck porque ele fala do
que foi entregue.

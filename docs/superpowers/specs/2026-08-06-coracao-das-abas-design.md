# Coração das abas · design

**Data:** 06/08/2026 · **Estado:** em brainstorming, aguardando escolha da natureza

## O problema

A aba Hoje ficou aprovada. As outras quatro — Fila de risco, Saúde por produto, Causas e
recorrentes, Previsão de volume — são tabela e gráfico comuns. Palavras do Igor: "tem que
ler e ler para entender, nada salta, nada impressiona, nenhum elemento brinca com o
usuário". Cada aba precisa de um elemento de assinatura que dê identidade no primeiro
segundo.

Restrição que atravessa tudo: **o que construímos tem de aparecer aplicado no sistema.**
Cada modelo, cada achado, cada limite medido. Nada de resultado que só existe em notebook.

## Decisões já tomadas

| Tema | Decisão | Quando |
|---|---|---|
| Direção visual | B — clara, editorial, campo de linhas ao fundo | 05/08 |
| Fonte | Outfit em tudo; nenhuma monoespaçada | 05/08 |
| Aprofundamento | Modal sobre a tela | 05/08 |
| Gráficos | Ricos e densos: grade, eixos, séries sobrepostas | 06/08 |
| Topo direito | Sai a busca, entra o controle de tempo | 06/08 |
| Interatividade | Filtro cruzado **e** comparação lado a lado | 06/08 |
| Perguntas | Toda escolha visual oferece "monta as três e eu vejo" | 06/08 |

## Pendências abertas

1. **Natureza do coração** — instrumento, manifesto ou ambiente. Três mockups funcionais
   entregues em `prototipos/telas/mockups/coracao-fila.html`. Aguardando escolha.
2. **Controle de tempo** — três versões em `prototipos/telas/mockups/controle-tempo.html`:
   compacto inline, pílula que abre o trimestre, player fixo. Aguardando escolha.
3. **Auditoria notebook a notebook** — conferir se cada saída de modelo está representada.
   Não iniciada.

## O achado de cada aba

O coração precisa carregar o achado da aba, não decorar em volta dele.

| Aba | O achado que o coração tem de carregar | Medido |
|---|---|---|
| Fila de risco | Ordenar por risco concentra: 50 primeiros de 5.183 guardam 13 das 50 violações, 27x o acaso. Por prioridade declarada: zero. | ✅ |
| Saúde por produto | A nota é relativa e o que separa o topo do fim é o inédito, que viola 4,6x mais. | ✅ |
| Causas e recorrentes | Volume e risco não coincidem: "Outro" é 7,8% do volume e 21,8% das violações. | ✅ |
| Previsão de volume | A banda de 80% conteve o real em 59,8% dos 92 dias — ela promete mais do que entrega. | ✅ 06/08 |

## O simulador de tempo

Pedido do Igor: ver a projeção da manhã e acompanhar se a realidade a está confirmando,
sem precisar reescrever a cada segundo, dando sensação de modelo atualizando.

Resolução: **nada é recalculado**. `data/app/dias.json` traz 92 dias com chegada hora a
hora, previsão e faixa — 17,7 kB. Navegar no tempo é indexar vetores já no navegador.
A curva prevista fica parada (foi feita às 00h, é isso que a torna previsão) e a linha do
realizado cresce por cima. O que muda é a distância entre as duas, e é ela que vira
veredito: no ritmo, abaixo, acima.

Honestidade embutida: abaixo de 35% do dia decorrido a tela recusa extrapolar o
fechamento, porque a conta é instável de manhã.

## Achados que a construção produziu

Registrados aqui porque valem para o deck e para a banca:

- **A banda de 80% cobre 59,8%.** Em 37 dos 92 dias o real saiu da faixa. Medimos a
  calibração da nossa própria previsão em vez de repetir o rótulo do Prophet.
- **O modelo não enxerga o `IC00840`.** O codificador agrupa categorias com menos de 100
  ocorrências, então o que entra no escore é "ativo pouco frequente". O histórico do ativo
  é contexto para o humano, não entrada do modelo — e a tela precisa dizer isso.
- **Os sinais exibidos explicam 54%** do empurrão para cima na faixa acima de 10%. O resto
  vem de contribuições pequenas demais para listar. A tela mostra a cobertura em vez de
  fingir que seis barras contam a história toda.
- **01/10 é um dia calmo.** Maior risco 8,1%, nenhum caso acima de 10%. Dizer que o dia
  está tranquilo também é resposta do produto.

## Próximos passos

1. Igor escolhe a natureza do coração e o controle de tempo.
2. Aplicar a natureza escolhida nas quatro abas, uma por vez, com mockup antes.
3. Auditar notebook a notebook o que está e o que não está representado.
4. Implementar o simulador de tempo no Django.
5. URL pública.

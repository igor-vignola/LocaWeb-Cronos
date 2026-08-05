# Referências de design — aplicação Cronos

Onze telas escolhidas pelo Igor em 05/08/2026. O que vale copiar de cada uma, e o que
não serve. Serve para ancorar decisão de design em algo concreto em vez de gosto.

## O que as onze têm em comum

1. **Uma frase interpreta o número.** O clima não mostra só 29°, mostra "vestir um casaco
   é boa ideia". As vendas não mostram só o total, começam com "sua média dos últimos 7
   dias é R$ 1.200". O nosso painel mostra "4 com risco acima de 10%" e para aí.
2. **A escala tem zonas com nome.** 720 é "Good" e faltam 40 pontos para "Very Good".
   "Low urgency". "High priority". Nunca um número solto sem régua.
3. **Existe um objeto de identidade.** A nuvem, a fábrica, o trigo, a planta. Bate o olho
   e você sabe de que ramo é o produto.
4. **O gráfico é anotado.** Evento marcado na linha ("Card Paid Off · +16 pts"), ponto
   destacado com balão ("15 January 6°").
5. **Cor tem significado**, não é um accent só.
6. **Trabalho aparece como cartão de tarefa**, não como linha de tabela.

## Por arquivo

| Arquivo | O que roubar | O que ignorar |
|---|---|---|
| `credify-score-credito` | Arco com zonas nomeadas e distância até a próxima zona. Evento anotado na linha do tempo. Cartão de recomendação com selo de impacto. | Ilustração 3D, ilustração de pessoa, "Go Pro". |
| `clima-chengdu-dark` | Abas ontem/hoje/amanhã. Frase de conselho acima do gráfico. Ponto destacado com balão. | Nuvem 3D — não temos objeto equivalente. |
| `ecofarm-gradiente-quente` | Saudação com contexto. Fileira de chips de métrica secundária com ícone. Cartão de tarefa com prazo e prioridade. | Foto de lavoura. Gradiente laranja. |
| `clara-diagnostico-ia` | **A mais relevante.** "Como cada sinal votou" com anel por sinal. Confiança final traduzida em frequência: "em 100 casos parecidos acerta ~78". Passos da análise numerados. | Mascote sorridente. |
| `indhub-industrial-setor` | Grade de setores onde a célula problemática acende, ligada ao painel de alerta. Alerta com localização. | Render 3D da fábrica. |
| `flybuzz-hero-editorial` | Hero editorial com cartão flutuante sobrepondo. | Foto de céu, paleta rosa. |
| `agrocontrol-kanban-glass` | Nav em pílula no topo. Kanban com contador por coluna. Vidro sobre imagem. | Foto aérea. |
| `plantify-wordmark-gigante` | Marca em tamanho gigante como textura de fundo. | Verde, foto de planta. |
| `financas-trio-dark` | Duas linhas planejado vs realizado. Cartão de conselho como tipo próprio. Sparkline por linha de lista. Fileira de ações rápidas. | "Great job!" e o tom de parabéns. |
| `cartao-grafico-comparado` | Abas de intervalo (1D/7D/3M). Duas séries com legenda de bolinha. Carimbo de hora do dado. | — |
| `vendas-frase-barras` | Frase como subtítulo antes do número. Barras por dia da semana com destaque nos dias notáveis. | — |

## Restrição honesta

Cinco das onze sustentam a riqueza visual em **fotografia ou render 3D**. Não temos isso,
e foto de datacenter genérica ficaria pior que nada. A riqueza do Cronos tem de vir de
**dado e tipografia**: a grade de ativos, a linha anotada, a marca em escala. O objeto de
identidade tem de ser construído com o próprio dado — é mais honesto e não depende de banco
de imagem.

## Tokens que valem (brand/design-system/assets/tokens.css)

Accent `#2563EB`. Semânticas `#DC2626` / `#D97706` / `#059669` com variantes soft e border.
Tipo Outfit. Raio na escala 4-22-28.

# Revisão das telas da aplicação

Pedido do dono do projeto em 10/09/2026: *"revisa cada página do Cronos web
application... tem muita coisa com cara de IA, tentando justificar tudo,
adentrar afundo onde não precisa"*, com um HTML em que ele possa transitar
entre a tela atual e a proposta.

**Abra `index.html`.** Escolha a aba em cima à esquerda, a versão ao lado, e
abra a gaveta da direita para ver o que saiu e por quê. Teclas `1` `2` `3`
trocam a versão e `←` `→` trocam a aba, enquanto o foco não estiver dentro da
tela.

## As três versões

| versão | o que é |
|---|---|
| **Atual** | a página exportada, carregada de `app/` por iframe. Sem um byte de diferença. |
| **Enxuta** | só cortes e fusões. Nenhum dado novo e nenhum componente novo: vira Django trocando marcação. |
| **Livre** | a tela repensada em torno da pergunta que ela responde. Muda a ordem dos blocos, funde seções e aposenta o que é interno do modelo. |

A Previsão fica só com a enxuta: ele escolheu essa e dispensou a livre.

## A regra de corte

Ele definiu o critério ao responder para quem a tela é escrita: *"ambos, mas
eles não precisam ver o visual com uma justificativa disso e aquilo, iremos
explicar"*.

Então: **se a linha existe para explicar o próprio gráfico, ela sai.** Fica o
que é dado, rótulo e unidade.

## O que isso deu

| aba | versão | palavras | frases de 9+ palavras | altura |
|---|---|---|---|---|
| Panorama | atual | 477 | 11 | 1743px · 1,8 telas |
| | enxuta | 329 | 4 | 1615px |
| | **livre** | **270** | **3** | **1561px** |
| Previsão | atual | 372 | 11 | 1614px · 1,7 telas |
| | **enxuta** | **213** | **3** | **1415px** |
| Projeção | atual | 228 | 4 | uma tela |
| | enxuta | 185 | 3 | uma tela |
| | **livre** | **159** | **3** | **uma tela** |
| Fila | atual | 1182 | 3 | 3840px · 4,0 telas |
| | enxuta | 1141 | 1 | 3801px |
| | **livre** | **405** | **2** | **1534px · 1,6 telas** |

As frases que sobraram são todas leitura de dado, não método: *"No ritmo atual
o dia fecha em 58, abaixo do intervalo previsto de 59 a 96"*, *"Projeção entre
191 e 225, com 208 no centro"*, *"Intervalo de 59 a 96 · 40 registrados até as
15h"*.

## Os cortes de estrutura, por aba

**Panorama livre** — a faixa escura e o gráfico do dia viram um bloco só; o
cartão herói do risco vira a primeira linha da lista que ele duplicava, com o
fator dominante na mesma linha; a meta troca o par de porcentagens de
atingimento por "Projeção de dezembro 208 · Faixa de 100% até 263".

**Projeção livre** — o trio "Já aconteceram / Limite para 100% / Projetadas"
sai, porque os três estão desenhados na régua logo abaixo; a decomposição sobe
para o topo e fecha a conta: *145 + 5,3 de risco na fila + 57,7 do volume que
ainda entra = 208 projetadas até dezembro*.

**Fila livre** — os dois cartões de maior risco saem (eram as linhas 1 e 13 da
tabela, em corpo grande); os 34 casos da faixa de rotina, entre 0,0% e 1,0% de
risco, recolhem-se atrás de uma linha que abre. A tela cai de 4,0 para 1,6
telas e continua com os 15 casos que pedem decisão.

## Os arquivos

```
index.html            a casca da comparação
panorama-enxuta.html  ┐
panorama-livre.html   │
previsao-enxuta.html  │ geradas por _construir.py a partir de app/,
projecao-enxuta.html  │ por cirurgia no DOM — herdam a folha real
projecao-livre.html   │
fila-enxuta.html      │
fila-livre.html       ┘
revisao.css           só o que as propostas precisam além da folha da aplicação
_construir.py         o transformador, com o motivo de cada corte comentado
_png/                 as capturas de cada versão, inteiras e na dobra
```

Para regerar depois de mexer em `app/`:

```
.venv/Scripts/python.exe prototipos/telas/revisao/_construir.py
```

## Três coisas que valem saber

**O resumo das 07h** abre uma vez por sessão e é parte da aba Panorama.
Feche-o uma vez e ele não volta enquanto você compara; o sino no topo direito
da aplicação traz de volta.

**Nada foi inventado.** As propostas não acrescentam número, cálculo nem
campo: o que elas fazem é tirar, fundir e reordenar o que a aplicação já
publica. A `enxuta` cabe no template atual; a `livre` muda estrutura, mas
continua sem depender de dado que não exista.

**Faltam Saúde e Causas.** As quatro primeiras abas estão revisadas; as duas
últimas seguem o mesmo tratamento quando ele mandar.

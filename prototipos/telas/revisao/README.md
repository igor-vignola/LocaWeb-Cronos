# Revisão das telas da aplicação

Pedido do dono do projeto em 10/09/2026: *"revisa cada página do Cronos web
application... tem muita coisa com cara de IA, tentando justificar tudo,
adentrar afundo onde não precisa"*, com um HTML em que ele possa transitar
entre a tela atual e a proposta.

**Abra `index.html`.** Escolha a aba em cima à esquerda, a versão ao lado, e
abra a gaveta da direita para ver o que saiu e por quê. Teclas `1` `2` `3`
trocam a versão e `←` `→` trocam a aba, enquanto o foco não estiver dentro da
tela.

As seis abas estão revisadas.

## As três versões

| versão | o que é |
|---|---|
| **Atual** | a página exportada, carregada de `app/` por iframe. Sem um byte de diferença. |
| **Enxuta** | só cortes e fusões. Nenhum dado novo e nenhum componente novo: vira Django trocando marcação. |
| **Livre** | a tela repensada em torno da pergunta que ela responde. Muda a ordem dos blocos, funde seções e aposenta o que é interno do modelo. |

O seletor marca com **✓** a versão escolhida:

| aba | escolhida |
|---|---|
| Panorama | livre |
| Previsão | enxuta *(a livre foi dispensada)* |
| Projeção | enxuta |
| Fila | enxuta |
| Saúde | a decidir |
| Causas | a decidir |

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
| | **enxuta** | **185** | **3** | **uma tela** |
| | livre | 159 | 3 | uma tela |
| Fila | atual | 1182 | 3 | 3840px · 4,0 telas |
| | **enxuta** | **893** | **1** | **3776px** |
| | livre | 333 | 2 | 1534px · 1,6 telas |
| Saúde | atual | 560 | 10 | 1646px · 1,7 telas |
| | enxuta | 448 | 4 | 1441px |
| | livre | 356 | 3 | 1441px |
| Causas | atual | 546 | 10 | 2151px · 2,3 telas |
| | enxuta | 420 | 7 | 2046px |
| | livre | 341 | 7 | 1850px · 1,9 telas |

As frases que sobraram são todas leitura de dado ou conclusão, não método:
*"No ritmo atual o dia fecha em 58, abaixo do intervalo previsto de 59 a 96"*,
*"8,0% do volume, com 2,9× a taxa média da base"*, *"Volume alto e risco
abaixo da média: é o perfil de quem se automatiza"*.

## Os cortes de estrutura, por aba

**Panorama livre** — a faixa escura e o gráfico do dia viram um bloco só; o
cartão herói do risco vira a primeira linha da lista que ele duplicava, com o
fator dominante na mesma linha; a meta troca o par de porcentagens de
atingimento por "Projeção de dezembro 208 · Faixa de 100% até 263".

**Projeção livre** — o trio "Já aconteceram / Limite para 100% / Projetadas"
sai, porque os três estão desenhados na régua logo abaixo; a decomposição sobe
para o topo e fecha a conta: *145 + 5,3 de risco na fila + 57,7 do volume que
ainda entra = 208 projetadas até dezembro*.

**Fila enxuta** — a linha da tabela parou de repetir o que o painel do
incidente mostra ao clicar: saiu a coluna **Ativo** inteira (em 34 das 49
linhas ela dizia "0 em N passagens", ou seja, o ativo nunca violou) e o fator
dominante virou uma linha em vez de duas. Os dois cartões do topo perderam a
régua rotulada e ganharam respiro entre si.

**Fila livre** — sobre a enxuta: os dois cartões de maior risco saem (eram as
linhas 1 e 13 da tabela, em corpo grande); os 34 casos da faixa de rotina se
recolhem atrás de uma linha que abre. De 4,0 para 1,6 telas.

**Saúde enxuta** — sai o glossário das quatro situações, 47 palavras no pé da
tela definindo *Estável*, *Recorrente*, *Risco latente* e *Já materializado*.
As etiquetas ficam.

**Saúde livre** — saem as duas colunas de volume por prioridade. "241 · 3
violaram" e "190 · 0 violaram" são contexto da base, não da nota: a nota é
posição relativa em cinco componentes e o volume não entra nela. Eram 60
números que ninguém compara linha a linha.

**Causas livre** — P3 e P2 viram uma coluna só. Cada uma trazia a taxa e o
número de casos em duas linhas por célula, 64 números na tabela. As duas taxas
continuam lado a lado, com o mesmo peso — *4,35% · 9,68%* — e a tabela perdeu
uma coluna inteira de largura.

## Uma coisa que deixei de propósito

Na Saúde, a linha do `lcsi` diz *"451,3h · o pior dos 15 · Encerramento
automático infla a mediana"*. É explicação, e pela regra sairia — mas é a
única frase da tela que impede uma leitura errada de um número real. Está
anotada na gaveta; se quiser, some.

## Os arquivos

```
index.html            a casca da comparação
panorama-enxuta.html  ┐
panorama-livre.html   │
previsao-enxuta.html  │
projecao-enxuta.html  │ geradas por _construir.py a partir de app/,
projecao-livre.html   │ por cirurgia no DOM — herdam a folha real
fila-enxuta.html      │
fila-livre.html       │
saude-enxuta.html     │
saude-livre.html      │
causas-enxuta.html    │
causas-livre.html     ┘
revisao.css           só o que as propostas precisam além da folha da aplicação
_construir.py         o transformador, com o motivo de cada corte comentado
_png/                 as capturas de cada versão, inteiras e na dobra
```

Para regerar depois de mexer em `app/`:

```
.venv/Scripts/python.exe prototipos/telas/revisao/_construir.py
```

## Duas coisas que valem saber

**O resumo das 07h** abre uma vez por sessão e é parte da aba Panorama.
Feche-o uma vez e ele não volta enquanto você compara; o sino no topo direito
da aplicação traz de volta.

**Nada foi inventado.** As propostas não acrescentam número, cálculo nem
campo: o que elas fazem é tirar, fundir e reordenar o que a aplicação já
publica. A `enxuta` cabe no template atual; a `livre` muda estrutura, mas
continua sem depender de dado que não exista.

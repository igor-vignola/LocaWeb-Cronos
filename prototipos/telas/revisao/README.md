# Revisão das duas primeiras abas da aplicação

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

## A regra de corte

Ele definiu o critério ao responder para quem a tela é escrita: *"ambos, mas
eles não precisam ver o visual com uma justificativa disso e aquilo, iremos
explicar"*.

Então: **se a linha existe para explicar o próprio gráfico, ela sai.** Fica o
que é dado, rótulo e unidade. A explicação é falada.

## O que isso deu

| | palavras | frases de 9+ palavras | altura |
|---|---|---|---|
| Panorama atual | 477 | 11 | 1743px |
| Panorama enxuta | 329 | 4 | 1615px |
| Panorama livre | 271 | 2 | 1581px |
| Previsão atual | 372 | 11 | 1614px |
| Previsão enxuta | 213 | 3 | 1415px |
| Previsão livre | 176 | 3 | 1216px |

As frases que sobraram são todas leitura de dado, não método: *"No ritmo atual
o dia fecha em 58, abaixo do intervalo previsto de 59 a 96"*, *"Projeção entre
191 e 225, com 208 no centro"*, *"Intervalo de 59 a 96 · 40 registrados até as
15h"*.

## Os arquivos

```
index.html            a casca da comparação
panorama-enxuta.html  ┐
panorama-livre.html   │ geradas por _construir.py a partir de app/,
previsao-enxuta.html  │ por cirurgia no DOM — herdam a folha real
previsao-livre.html   ┘
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

# Reset do design — estrutura, essência e o que cada página mostra

**Data:** 11/08/2026 · **Estado:** plano para aprovação, nada construído ainda
**Prazo:** Sprint 3 em 23/08 (12 dias)
**Tema:** claro. Escuro só onde um objeto único domina — e só se ficar bom no mockup.

---

## 1. O diagnóstico

A tela não está difícil por causa de CSS. Ela **explica antes de mostrar**.

Contagem da aba Hoje, direto do template: 1 herói + 3 atos + 5 cartões. Cada ato tem título
e uma frase. Cada cartão tem título, escopo e uma frase. São **oito blocos de texto antes
de o olho chegar em um número**, e os títulos são perguntas ("O dia está se cumprindo?",
"Por que confiar nessa ordem"). Isso é estrutura de capítulo. A tela ficou escrita como o
livro — e o livro ensina, a tela informa.

O mesmo vale para o briefing: `_brief.html` são três parágrafos corridos com números em
negrito no meio. Não é feio por causa da cor. É feio porque é **carta**, não composição.

As duas inspirações fazem o contrário, e fazem igual entre si:

| | App de investimento | Relatório Orquestra |
|---|---|---|
| Primeira coisa que aparece | `R$ 980,00` em corpo gigante | `539` em corpo gigante |
| Rótulo | `PATRIMÔNIO` — uma palavra | `Buscas disparadas` — duas |
| Explicação | uma linha | uma linha |
| Parágrafo | nenhum | um só, na caixa "Como ler" |

**Número primeiro, uma linha depois, acabou.**

**Nenhum título de tela é pergunta.** A pergunta é ferramenta de projeto, fica neste
documento. Na tela, substantivo.

**Nenhum número aparece sem régua.** Um número solto não diz se está alto. Todo valor
relevante vem comparado — contra a média do mesmo dia da semana, contra a semana passada,
contra o mês passado, ou contra a meta. É elemento de design de primeira classe, não nota
de rodapé. É também o princípio nº 2 das onze referências que o Igor escolheu em 05/08,
registrado em `prototipos/inspiracao/LEIA.md`: *"a escala tem zonas com nome; nunca um
número solto sem régua"*.

---

## 2. A estrutura — uma análise por página

Seis páginas. **Uma porta de entrada e cinco análises, uma por notebook.**

| Página | Vem de | O que ela é |
|---|---|---|
| **Panorama** | — | o que vem hoje, contra o normal, e o índice vivo do sistema |
| **Previsão** | notebook 03 | quanto volume vem, e quanto o modelo acerta |
| **Fila** | notebook 04 | os casos abertos ordenados por risco |
| **Projeção** | notebook 06 | o fechamento do ano contra a meta |
| **Saúde** | notebook 07 | a nota de cada produto |
| **Causas** | notebook 05 | o que se repete e o que dá para automatizar |

Cada página tem **um herói e uma análise**. Nada acumula.

**Ganho para a banca:** o mapa notebook → página é 1 para 1. Nada do que foi construído
fica invisível, e a resposta a "onde está esse modelo no produto?" é apontar uma aba.

**A tensão com a mentoria, dita na cara.** A ata pede "duas a três abas no máximo". Seis
contraria a letra. A resposta, se perguntarem: a preocupação era o usuário se perder, e
seis páginas que fazem uma coisa cada, com o **Panorama resumindo todas em cinco linhas**,
resolvem isso melhor que três páginas empilhadas. Foco por tela vale mais que contagem de
abas. Fica registrado como decisão consciente, não como esquecimento.

**A navegação não parece uma pilha.** Seis itens planos, agrupados por finas divisórias em
quatro zonas:

```
Panorama  │  Previsão · Projeção  │  Fila  │  Saúde · Causas
```

Sem menu suspenso, sem submenu. A divisória faz o trabalho.

---

## 3. O Panorama é o índice vivo — não a soma das análises

**O nome.** "Hoje" prometia só o dia. A página cobre o que vem hoje **e** o olhar geral —
hoje contra a média, contra a semana passada, contra o mês passado. `Panorama` diz isso sem
mentir. Alternativas descartadas: "Visão geral" (genérico), "Situação" (soa a incidente),
"Agora" (mesmo problema de "Hoje").

**O briefing é só modal.** Não vira aba nem seção. Ele abre por cima do Panorama na
primeira visita do dia, e o essencial dele já está na própria página — quem fecha o modal
não perde nada.

Você pediu que a página mostrasse o andamento como um todo, e também que nada acumulasse.
As duas coisas cabem se ela **resumir sem detalhar**.

Ela mostra o veredito de cada análise em **uma linha**, com o número que importa e a cor do
estado. Toca e vai para a página. É o padrão `RELATÓRIO DO DIA →` e a lista `O que moveu
hoje` da sua referência de investimento.

```
Previsão    42 previstos hoje no P3            erro médio de 11/dia        →
Fila        5.183 casos pontuados              maior risco aberto: 18%     →
Projeção    P3 fecha em 312                    meta é 280                  →   ← âmbar
Saúde       pior produto: <nome>               nota 41 de 100              →
Causas      "Outro"                            21,8% das violações         →
```

Cinco linhas dão o sistema inteiro. Nenhum gráfico além do herói do dia. Quem quer
profundidade, clica.

---

## 4. Não ter cara de dashboard genérico

O que faz um painel parecer genérico é sempre a mesma coisa: **fileira de quatro cartões de
KPI do mesmo tamanho**, tudo com o mesmo peso, rosquinha de percentual, grade regular.

O antídoto é **hierarquia brutal**: um elemento domina a dobra, o resto é subordinado e
pequeno. No seu app de investimento, `R$ 980,00` ocupa mais área que os oito elementos
seguintes somados.

**Regra: um herói por página, ocupando a dobra. Nada de fileira de quatro iguais.**

---

## 5. A essência Cronos — quatro detalhes que só existem aqui

Cronos é tempo. A assinatura não pode ser um accent bonito; tem que ser **como o sistema
trata o tempo**. Quatro regras, sem exceção em nenhuma tela:

### 5.1 Sólido é fato, traçado é previsão
Em todo gráfico temporal: o que aconteceu é linha cheia e opaca; o que o modelo prevê é
traço interrompido e translúcido. Sem legenda explicando — a forma já diz. É honestidade
virada em estética, e nenhum painel genérico faz isso com consistência.

### 5.2 A linha do agora
Vertical de 1px marcando o instante presente, idêntica em todo gráfico temporal. Respira:
opacidade oscilando devagar, ciclo de ~4s. É o motivo recorrente que faz seis páginas
diferentes parecerem o mesmo produto.

### 5.3 O tempo é arrastável
Pega o trilho, arrasta, e a interface volta àquele instante. Já construído. É o momento em
que o avaliador entende que não é relatório estático.

### 5.4 Número que conta
Ao mudar de valor (viajar no tempo, arrastar o corte da fila), o número transita em 260ms
com desaceleração, em vez de saltar.

---

## 6. Cor e tema

**Tema claro.** Fundo neutro claro, cartões brancos com raio generoso e sombra baixa — a
linguagem da referência Orquestra.

**Escuro entra em dois lugares, e só se ficar bom no mockup:**

1. **A folha do briefing** — é um momento, não uma área de trabalho. Entrar no escuro e
   abrir para o painel claro dá peso à chegada.
2. **O cartão herói do gráfico do dia** — objeto único e dominante, onde o dado brilha.

Regra dura: **escuro só quando um objeto único domina**. Nunca em cartões lado a lado,
nunca em fileira. Se no mockup parecer remendo, sai.

**Cor:** o produto é sobre risco, e painel pintado de vermelho ensina a ignorar vermelho.

| Cor | Significa |
|---|---|
| Azul `#2563EB` | o sistema falando — previsão, saída de modelo |
| Verde | dentro da meta |
| Âmbar | atenção, ainda cabe |
| Vermelho | estourando |

Nunca cor por decoração. Nunca duas semânticas competindo no mesmo bloco. **Teto: 10% da
área da tela com cor.** Os tokens já existem em `brand/design-system/assets/tokens.css`;
muda a disciplina de uso, não a paleta.

---

## 7. O briefing — continua abrindo, redesenhado

Continua sendo a porta de entrada, abrindo sozinho na primeira visita do dia. Muda a forma:
de três parágrafos corridos para três momentos, cada um com número em corpo grande e **uma
linha** abaixo.

```
ONTEM      41 entraram · 2 violaram
           14 dias úteis sem violação

HOJE       entre 28 e 52 no P3
           12 já entraram às 7h, contra 9 esperados

ATENÇÃO    P3 projeta 312 contra meta de 280
           a faixa ainda comporta fechar dentro
```

Depois, os dois atalhos e o botão de abrir o painel. Sobe de baixo como folha, arrasta para
baixo para dispensar, com momentum. Os números são os mesmos que já estão lá — muda a
composição, não o conteúdo.

---

## 8. O plano por página

Cada página: **um herói, um apoio, e profundidade ao toque.** Nada além disso.

### Panorama
| | |
|---|---|
| Entrada | a folha do briefing, só como modal |
| Herói | **o dia acontecendo** — previsto contra realizado, hora a hora. Sólido até a linha do agora, traçado depois. Trilho arrastável. |
| Régua | **hoje contra o normal**: média do mesmo dia da semana, mesma terça da semana passada, média do mês passado. É o que responde "está alto?". |
| Apoio | **o índice de cinco linhas** (seção 3) |
| Ao toque | cada linha leva à sua página |
| Sai | os cartões de justificativa, a projeção detalhada, os últimos dias, os ativos |

### Previsão
| | |
|---|---|
| Herói | **a linha do tempo dos 92 dias com play**, marca vermelha em cada dia fora da faixa |
| Número | os próximos sete dias, com o erro médio na mesma linha |
| Apoio | carga por dia da semana |
| Ao toque | folha **"como o modelo se sai"**: a banda promete 80% e entrega 59,8% no P3, os baselines, a escolha `linear` contra `flat` |
| Novo | a linha do tempo com play |

### Fila
| | |
|---|---|
| Herói | **o ganho contra o acaso** em corpo gigante, com o **corte da fila arrastável dentro**. Arrasta e o número recalcula ao vivo. |
| Apoio | a lista ordenada, filtro em pílula segmentada |
| Ao toque | folha do caso com a **decomposição exata** (peso × desvio da média) — já existe e é boa |
| Ao toque | folha **"como isso funciona"**: as quatro faixas, como ler um risco de 10%, grupos críticos |

### Projeção
| | |
|---|---|
| Herói | **o fechamento do ano contra a meta**, por prioridade. P2 com folga, P3 estourando — dito com cor e posição, não com parágrafo. |
| Apoio | as três parcelas que compõem a projeção: realizado, fila aberta, volume futuro |
| Ao toque | folha com o erro da projeção nas dez datas medidas |
| Nota | sai do Panorama, onde hoje mora espremida |

### Saúde
| | |
|---|---|
| Herói | **o quadrante** — 17 bolhas, x = violação, y = proporção de inédito, tamanho = volume |
| Apoio | o ranking dos 17 |
| Ao toque | folha do produto com os cinco componentes da nota |
| Novo | o quadrante. Hoje a tela usa a palavra "quadrante" sem o quadrante existir. |

### Causas
| | |
|---|---|
| Herói | **o gráfico de divergência** — uma barra por causa, dois braços: quanto é do volume, quanto é das violações. Onde destoam, há concentração. |
| Apoio | os 20 que mais repetem, com o automatizável marcado |
| Ao toque | folha **antes e depois da normalização**: dois textos crus virando um grupo. Torna visível engenharia que hoje passa por lista qualquer. |
| Novo | a divergência e o card de normalização |

---

## 9. Movimento e acabamento

Postura da `find-animation-opportunities`: **contenção**. Uma animação com significado por
página; o resto é serviço.

| Página | A animação que significa algo |
|---|---|
| Panorama | o tempo passando ao arrastar o trilho |
| Previsão | o play dos 92 dias, com as linhas do fundo correndo |
| Fila | o corte arrastável recalculando o ganho ao vivo |
| Projeção | o arco preenchendo até a meta |
| Saúde | as bolhas assentando no quadrante |
| Causas | os braços da divergência abrindo do centro |

**Números de acabamento** (`emil-design-eng` + `apple-design`):

- Hover: 120ms `ease-out`, elevação e cor. Nunca em elemento não clicável.
- Clique: `scale(.97)`, `transform-origin` no ponto do toque, 90ms.
- Folhas: mola, **interrompível**, arrastável para baixo herdando a velocidade do gesto.
- Números: transição de 260ms com desaceleração ao mudar de valor.
- Entrada de conteúdo: `opacity` + `translateY(8px)`, 180ms. Nunca `scale(0)`.
- Linhas de lista: hover revela o chevron deslizando 4px.
- `prefers-reduced-motion`: tudo vira corte seco, sem exceção.
- Foco de teclado sempre visível.

**Proibido:** animação disparada por scroll em série, movimento que não responde a ação do
usuário, transição acima de 400ms em qualquer coisa que não seja folha.

---

## 10. O que não se mexe

`notebooks/`, os parquets, `servicos.py`, `graficos.py`. `views.py` ganha uma view nova
(Projeção) e perde peso no Panorama. O reset é **template e CSS** — a camada que produz o número
está medida, validada e comitada.

Dívida a resolver junto: `scripts/monta_app.py` gera o protótipo estático e o Django tem
camada própria. Dois caminhos para a mesma tela — unificar agora.

---

## 11. Ordem de execução

1. **Panorama** — define a linguagem do sistema inteiro (herói, índice, folha do briefing).
2. **O briefing e o padrão de folha** — usados por todas as páginas.
3. **Fila** — define o padrão de lista.
4. **Previsão** e **Projeção** — reaproveitam herói de gráfico e folha.
5. **Saúde** e **Causas** — os dois gráficos que não existem. Por último de propósito: se o
   tempo apertar, são elas que sofrem.
6. Passada da `humanizer` em todo texto de tela.
7. Docker e URL pública.

---

## 12. O que depende do Igor

| # | Decisão | Como resolver |
|---|---|---|
| 1 | Seis páginas, uma análise cada | aprovar aqui |
| 2 | Onde o escuro entra (briefing, herói do dia, nenhum) | ver no mockup do Panorama e cortar o que parecer remendo |

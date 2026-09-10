# Contrato do deck da banca ao vivo

Fonte única de verdade para quem constrói um bloco de slide deste deck. Se este
documento e a sua intuição discordarem, este documento ganha.

**Contexto.** Banca final do Challenge FIAP 2026 com a Locaweb, em 15/09/2026,
19h30, ao vivo pelo Teams. Seis grupos, cerca de 15 minutos cada. A banca tem
professores e a Locaweb, representada pelo mentor **Douglas Gouveia, Gerente
Executivo de Operações**. Eles **não verão os decks das sprints anteriores**:
este é o único material que passa na frente deles. Três pessoas apresentam.

---

## 1. Registro do texto: o que mais importa

O deck anterior foi reprovado pelo dono do projeto por parecer escrito por
máquina. O defeito era de **forma**, não de conteúdo. Os títulos seguiam todos
o mesmo molde: fragmento de frase, pausa, segundo fragmento.

**Títulos reprovados, do deck anterior:**

- "Dois modelos. Uma pergunta para cada um."
- "Django numa imagem Docker, sem nuvem amarrada."
- "Erro baixo nas duas prioridades. E a projeção fecha."
- "O painel operacional, em seis telas."
- "O dia quase dobra de volume. A taxa de perda não sobe."

**A regra:** título é **uma oração declarativa completa**, no tom de quem
relata um fato a um colega mais graduado. Sujeito, verbo, e o número quando ele
existir. Sem fragmento, sem antítese de dois tempos, sem frase de efeito.

**Proibido em qualquer texto do slide:**

| Padrão | Exemplo do que não fazer |
|---|---|
| Fragmento como título | "Dois modelos. Uma pergunta para cada um." |
| Antítese de dois tempos | "Não é X. É Y." / "A nota não cai. Ela despenca." |
| Frase começando com "E" ou "Mas" | "E a projeção fecha." |
| Travessão em texto corrido | qualquer `—` |
| Regra de três | "rápido, confiável e escalável" |
| Vocabulário de IA | crucial, fundamental, robusto, revolucionar, transformar, potencializar, elevar, garantir (como enfeite), destacar, ressaltar |
| Gerúndio de análise rasa | "garantindo maior eficiência", "refletindo a maturidade" |
| Superlativo sem número | "erro baixíssimo", "altíssima precisão" |
| Emoji | qualquer um |
| Negrito decorativo | negrito só no dado ou no termo técnico, nunca em frase inteira |

**Exemplos de reescrita, para calibrar:**

| Reprovado | Aprovado |
|---|---|
| "Dois modelos. Uma pergunta para cada um." | "A solução separa a previsão de volume do risco por incidente." |
| "Django numa imagem Docker, sem nuvem amarrada." | "A aplicação roda em contêiner e não depende de provedor de nuvem." |
| "O dia quase dobra de volume. A taxa não sobe." | "Dias de volume alto e de volume baixo perdem prazo na mesma proporção." |
| "Erro baixo nas duas prioridades." | "O erro médio é de 4 incidentes por dia na prioridade 2 e 11 na prioridade 3." |

---

## 2. Regras do projeto que não se negociam

1. **Prioridade 2 e prioridade 3 sempre juntas, com o mesmo peso visual.**
   Nenhum bloco, número, gráfico ou tabela fala de uma sem a outra do lado.
   É o erro que o dono do projeto mais corrige.
2. **A palavra "turno" é proibida.** Use "no dia", "durante o dia", "a
   operação", "quem opera". O produto se chama **painel operacional**.
3. **Nenhum número que você não tenha recebido nesta lista.** Não calcule, não
   some, não estime, não arredonde para um número mais bonito.
4. **Nada de dado realizado posterior a 01/10/2025 15h** nas telas do produto.
   Métrica de avaliação de modelo (erro, ROC AUC, calibração, backtest) é
   permitida, porque ali o assunto é "o modelo funciona".
5. **Um slide, uma mensagem.** Se o slide precisa de parágrafo, ele está
   fazendo o trabalho de dois.
6. **Nunca três cartões iguais em fileira.** É o molde que a máquina produz
   sozinha. Prefira composição assimétrica, empilhamento com fio de 1px, ou um
   objeto dominante com apoio ao lado.

---

## 3. As duas variações

Cada slide tem **duas variações**, `data-var="a"` e `data-var="b"`. Elas são
**a mesma mensagem, o mesmo estilo e os mesmos números, em formas diferentes de
apresentar o dado.** Não são duas paletas nem dois títulos diferentes.

Exemplos de par legítimo:

- número gigante rotulado **contra** barra proporcional com o número na ponta
- dois blocos lado a lado **contra** um bloco empilhado com fio divisor
- objeto dominante à esquerda com apoio à direita **contra** objeto centralizado
  com apoio embaixo
- tabela de três linhas **contra** três linhas empilhadas sem grade

O dono do projeto vai alternar com a seta para baixo e escolher. Faça as duas
merecerem ser escolhidas: uma variação claramente pior é trabalho perdido.

---

## 4. Contrato técnico do bloco

Arquivo: `blocos/NN-nome.html`. Ele contém, nesta ordem e **nada mais**:

1. um `<style>` com o CSS só dos seus slides, **todo prefixado pela classe do
   slide** (ex.: `.pb .algo{...}`), para não vazar para os outros blocos
2. as `<section>`, duas por slide

```html
<section class="slide light pb" data-slide="2" data-var="a" data-quem="igor">
  <div class="mesh"></div><div class="grid-bg"></div>
  <div class="hd">
    <div class="bi"><svg ...></svg></div>
    <div class="bn">Cronos</div><span class="bt">BANCA FINAL · 15/09/2026</span>
    <div class="tag">Base elegível ao KPI · 2025</div>
  </div>
  <div class="body">
    <span class="eb"><span class="rv" style="--d:260ms">O problema</span></span>
    <h1 class="tt">...</h1>
    ...
  </div>
  <div class="ft"><span>procedência do dado</span></div>
</section>
```

- `data-slide` o número do slide, **igual nas duas variações**
- `data-var` `"a"` ou `"b"`
- `data-quem` `igor`, `ana` ou `hygor`. **Não escreva o marcador de quem
  apresenta:** o `_montar.py` injeta o retrato e o nome na primeira vaga do
  rodapé. Por isso o rodapé leva **um** `<span>`, com a procedência do dado.
- o `.bt` do cabeçalho é sempre `BANCA FINAL · 15/09/2026`
- copie a estrutura de cabeçalho de um bloco existente em
  `../video/blocos/` para o logo SVG sair igual. No slide `.dark` o traço do
  logo é `#0A0E17`, no `.light` é `#fff`.

### Classes compartilhadas, já prontas em `_estilo.css`

`.slide .light .dark .mesh .grid-bg .hd .body .ft .eb .tt .cartao .ic .num`
`.big` (número gigante rotulado) `.apres` (o marcador, injetado)
`.dv` (divisória escura)

### Camada de animação

| Classe | O que faz |
|---|---|
| `.rv` | entra subindo 14px, 0,6s |
| `.rv3` | entra com profundidade, rotateX de 8 graus, 0,8s |
| `.mask` com `<span>` dentro | tipografia entra por máscara de linha, 0,85s |
| `.ct` com `data-to` e `data-delay` | número que conta até o alvo |
| `--d` no `style` do elemento | atraso em ms |
| keyframe `corre` | barra ou trilho que enche, use `transform:scaleX` |

Exemplo: `<span class="rv" style="--d:640ms">`. Escalone os atrasos para a
leitura acontecer na ordem da fala, não tudo de uma vez.

**Altura de barra em pixel, nunca em porcentagem.** Porcentagem de altura não
resolve dentro deste flex e a barra sai com altura zero. Já aconteceu duas
vezes neste projeto.

### Ícones

SVG inline na classe `.ic`, traço 1,5, herdando a cor do contexto. Desenhe os
seus. **Zero emoji.**

---

## 5. Os números, todos medidos em `data/interim/incidentes_kpi.parquet`

**A base · o denominador tem que casar com o numerador**

| recorte | elegíveis ao KPI | perdas de prazo | taxa |
|---|---|---|---|
| 2023 | 87 | 4 | |
| 2024 | 357 | 6 | |
| **2025** | **25.156** | **238** | **0,95%** |
| base inteira, 2023 a 2025 | 25.600 | 248 | 0,97% |

122.543 incidentes no dataset, dos quais 25.600 elegíveis ao KPI, que é 21%.

**Se o slide fala de 2025, o denominador é 25.156 e a taxa é 0,95%.** Usar 238
perdas contra 25.600 elegíveis mistura um ano com três, e foi um erro real que
apareceu na construção deste deck.

**Perdas de prazo · ATENÇÃO AO PERÍODO**

A meta do KPI é **anual**, então o número que se compara com ela é o do ano
fechado. Medido no parquet:

| período | prioridade 2 | prioridade 3 |
|---|---|---|
| 2023 | 0 | 4 |
| 2024 | 0 | 6 |
| **2025** | **42** | **196** |
| base elegível inteira | 42 | 206 |

**Use 42 e 196, e escreva que é 2025.** O 206 é o total de três anos e não pode
ser comparado com uma meta anual: contra a régua do P3 ele cai na faixa de 201 a
230, que vale 125%, enquanto os 196 de 2025 caem abaixo de 201, que vale 150%.
Material antigo do projeto usa 206 como se fosse anual; está errado.

Quando o slide citar o número, deixe o período claro e diga a razão em uma
linha, tipicamente no rodapé: a meta é anual, e a base tem 248 perdas em três
anos.

**Volume não prevê perda de prazo** (261 dias úteis de 2025)
- os 68 dias de maior volume: 108 incidentes por dia, taxa de perda **0,75%**
- os 69 dias de menor volume: 56 incidentes por dia, taxa de perda **0,86%**
- o volume do dia explica **2,5%** da variação das perdas (r = 0,159; p = 0,011)

**Previsão de volume, Prophet**
- erro médio de **4** incidentes por dia na prioridade 2 e **11** na prioridade 3,
  média de D+1 a D+7, validado por backtest deslizante com re-treino por origem
- sazonalidade semanal ligada, anual desligada, feriados nacionais
- cobertura da banda de 80%: entre 86% e 88% no P2, entre 59% e 61% no P3

**Risco por incidente, regressão logística**
- ROC AUC **0,869** contra 0,868 do XGBoost
- PR-AUC **0,296** contra 0,253 do XGBoost
- calibração: prevê **48,1** perdas onde houve **50**
- escolhida por manter a calibração e ser explicável por construção

**Concentração, na base elegível inteira**

| grupo | volume | % da base | perdas | taxa |
|---|---|---|---|---|
| Team09 | 2.058 | 8,0% | 56 | 2,72% |
| Team11 | 8.702 | 34,0% | 114 | 1,31% |
| Team05 | 3.628 | 14,2% | 13 | 0,36% |
| Team14 | 8.973 | 35,1% | 10 | 0,11% |

- Team11 e Team14 atendem praticamente o mesmo volume, diferença de 3%, e a
  taxa do Team11 é **11,8 vezes** a do Team14
- os 30 itens de configuração com mais perdas concentram **61,7%** das perdas

**A stack**
- Django, Docker, Prophet, scikit-learn, pandas, e a Claude API só para redigir
  o texto do resumo diário
- agnóstica de provedor de nuvem, sem serviço proprietário de AWS, GCP ou Azure
- seis abas: Panorama, Previsão, Projeção, Fila de risco, Saúde por produto,
  Causas

**Nunca cite** ARIMA, SARIMA, Streamlit, clusterização por DTW nem detector de
cascata como parte da solução: os quatro foram testados e descartados.

---

## 6. Verificação obrigatória antes de entregar

O chromium que o playwright espera não existe nesta máquina. Use o que está em
disco:

```python
CHROME = r"C:\Users\igor.vignola\AppData\Local\ms-playwright\chromium-1217\chrome-win64\chrome.exe"
navegador = p.chromium.launch(executable_path=CHROME)
pagina = navegador.new_page(viewport={"width":1600,"height":900}, device_scale_factor=1)
```

Monte a sua página de teste em `blocos/_teste-NN.html` juntando o `_estilo.css`
com o seu bloco, e **olhe as imagens com a ferramenta Read**, em cada variação,
no estado final e em pelo menos dois instantes intermediários. Não julgue por
CSS lido.

Procure, e reporte com número:

- vão morto dentro de cartão, que é o defeito mais comum aqui
- texto transbordando o container
- elemento com altura ou largura zero que deveria ter tamanho
- qualquer coisa fora dos limites de 1600x900
- contraste insuficiente para leitura em chamada de vídeo
- as duas variações parecendo a mesma coisa, o que anula o propósito

E rode a varredura de texto: ocorrências de "turno", de travessão, de emoji, e
slide que cita prioridade 3 sem citar prioridade 2.

---

## 7. Adendos de 09/09/2026

Registrados depois da revisão com a banca simulada. Onde este adendo e o texto
acima discordarem, o adendo ganha.

**7.1 Títulos.** A regra de §1 ("oração declarativa completa") foi substituída
pelo dono do projeto: o título é **curto e nomeia o assunto** do slide; a
mensagem é dita por quem apresenta. Pergunta como título é aceita quando o
slide responde ("Dia cheio quebra mais?"). Continua proibido: fragmento com
pausa e segundo fragmento, antítese de dois tempos, travessão, vocabulário de IA.

**7.2 Um objeto por slide.** Cada slide tem um objeto visual próprio e não
repete o molde do vizinho. Gráfico matplotlib em dpi 200 dentro do cartão da
casa (`.quadro.cartao`), nunca solto sobre o fundo. Variação B descontinuada.

**7.3 Volume × perda de prazo, números de palco.** O slide 6 usa os quatro
grupos de volume de `_dados.py` (261 dias úteis de 2025, quartis): 56, 79, 90 e
110 incidentes por dia, com taxas de 0,86%, 0,87%, 0,97% e 0,72%. O §5 acima
traz 108/dia e 0,75% para "os 68 dias de maior volume", que é outro corte da
mesma série. Os dois estão certos; no palco valem os do gráfico.

**7.4 Comparação de modelos no deck.** A escolha da regressão logística contra
o XGBoost aparece no pé do slide 9: ROC 0,87 nos dois, PR-AUC 0,30 contra 0,25,
calibração de 48 quebras previstas onde houve 50. É a resposta à pergunta que a
banca simulada colocou em primeiro lugar.

**7.5 Meta ao lado da contagem.** 42 e 196 nunca aparecem sem o limite do ano ao
lado. O limite é o da faixa de 100% do dicionário: **39** na prioridade 2 e
**263** na 3. Material antigo que diga 45 e 200 está errado; esses são outros
degraus da escada.

**7.6 Os dois diferenciais têm slide.** Resumo da manhã e nota de saúde por
produto são o pacote de produto que o projeto prometeu, e cada um ocupa um
slide antes da demonstração. A demonstração mostra os dois funcionando.

**7.7 Nada do que foi testado e descartado entra no deck.** Cascata, acúmulo e
clusterização por DTW ficam em `PERGUNTAS.md`. O deck fala do que foi entregue.

**7.8 Divisórias de bloco.** Três, herdadas do deck da Sprint 4, uma por parte
do núcleo: análise exploratória, modelagem e a solução em produção. Desenho em
`_estilo.css`, classe `.dvs`. O gradiente do título vai no `span` da máscara, e
não no `h1`: com `background-clip` no pai o texto do filho herda
`color:transparent` e o título some.

**7.9 Estrutura final, 28 slides.**

As seções seguem as do deck da Sprint 3, que é o acabado, e cada uma abre por
divisória no mesmo desenho.

| # | Slide | Quem | Outras versões |
|---|---|---|---|
| 1 | Capa | Igor | — |
| 2 | Super Data Bros | Igor | — |
| 3 | Cronos, o deus do tempo | Igor | — |
| 4 | O prazo de cada incidente | Igor | — |
| 5 | Quantidade de quebras em 2025 | Igor | — |
| 6 | A fila não atende na ordem em que o prazo estoura | Igor | — |
| 7 | **Seção 01 · Análise Exploratória** | Igor | — |
| 8 | O salto de setembro | Ana | — |
| 9 | Por que treinamos só em 2025 | Ana | — |
| 10 | Quem abre, e quando | Ana | B cartões flutuantes, C a A sobre cartões |
| 11 | O mesmo ativo quebra de novo | Ana | — |
| 12 | Quando ninguém sabe nomear a causa | Ana | — |
| 13 | O alvo é raro | Ana | — |
| 14 | **Seção 02 · Previsão de Volume** | Ana | — |
| 15 | Os próximos sete dias | Ana | B figura em largura cheia |
| 16 | Comparação do erro com os baselines | Ana | — |
| 17 | **Seção 03 · Risco de OLA** | Ana | — |
| 18 | A fila de risco | Ana | B seca, só a figura |
| 19 | **Seção 04 · Projeção da meta e saúde** | Ana | — |
| 20 | A meta do ano vai fechar? | Ana | B legenda, C quatro passos, D a meta em cartão |
| 21 | Onde agir primeiro | Hygor | B sem matplotlib, C os dois painéis |
| 22 | **Seção 05 · A aplicação web do Cronos** | Hygor | B desenho de seis molduras |
| 23 | Como o Cronos antecipa o resultado do ano | Hygor | — |
| 24 | **Morning Brief** (divisória) | Hygor | — |
| 25 | Morning Brief | Hygor | B a folha redesenhada |
| 26 | Como isso roda | Hygor | B arquitetura da planilha ao painel |
| 27 | Aplicação web Cronos · **demonstração** | Hygor | B baralho de telas, C a chamada ao vivo |
| 28 | Obrigado | Igor | — |

Três trocas de voz: 7→8, 20→21 e 27→28.

**7.10 Um assunto por slide, e os modelos separados.** Previsão de volume e
risco de OLA têm divisória própria e são apresentados um de cada vez, como no
deck da Sprint 3. A previsão ocupa dois slides: a semana prevista contra o que
chegou, e o erro por horizonte contra os baselines. A projeção da meta e a
nota de saúde compartilham a seção 04, porque saem da mesma leitura.

**7.11 As variações vêm do deck da Sprint 3.** O dono do projeto trabalha com o
`.pptx` da Sprint 4 como referência, mas considera acabado o da **Sprint 3**.
Onde aquele deck resolveu melhor, a forma de lá entra como **variação B** e a
composição atual fica como A; ele escolhe uma por slide na revisão. Fonte dos
originais: `prototipos/slides/mvp/deck/` e `prototipos/slides/mvp/abertura/`,
com o mapa de escolhas em `scripts/monta_deck_sprint3.py`.

Duas coisas mudam ao trazer uma forma de lá: ela ganha animação, que o `.pptx`
não tinha, e passa pela conferência de números deste arquivo. O slide 18 é o
exemplo: no deck da Sprint 4 o cartão dizia "quatro modelos", e aqui diz "o que
o Cronos calcula", porque são dois modelos e dois cálculos derivados.

**7.12 Variação sinalizada no chrome.** O rodapé de navegação mostra uma pílula
azul com bolinhas quando o slide tem mais de uma composição, e "variação única"
em cinza quando não tem. Sem isso era preciso apertar a seta para baixo em
todos os slides para descobrir onde havia variação.

**7.13 Bloco com duas composições pode morar em dois arquivos.** O `_montar.py`
lê `blocos/NN-*.html` e ordena por `(data-slide, data-var)`, então a variação B
pode ficar em `NN-nome-b.html` em vez de virar uma segunda `<section>` no mesmo
arquivo. Para bloco grande, dois arquivos é o que se usa.

**7.14 Desenho vetorial dentro do slide.** Curva, cruzada e marcador feitos em
SVG inline seguem duas regras. Traço que se desenha usa `stroke-dasharray` e
`stroke-dashoffset` iguais a um `--len` maior que o comprimento real do caminho.
E se o `svg` tem `preserveAspectRatio="none"`, todo `svg` sobreposto a ele
precisa da mesma declaração, senão o marcador sai do lugar; num `viewBox`
esticado, círculo vira `ellipse` com dois raios.

**7.15 Denominadores que se cruzam.** Os 25.600 do slide 4 são dos três anos; o
ano de 2025 sozinho tem 25.156, e é dele que fala o slide 5. O slide 4 diz
"entram no indicador", não "contam para a meta do ano", justamente para os dois
números não se contradizerem na mesa.

**7.16 A escala do palco sai da caixa, não da janela.** O `fit()` do `_montar.py`
lê `getBoundingClientRect()` do `#fit` e um `ResizeObserver` observa esse
elemento. Com `window.innerHeight`, abrir o `deck.html` direto no navegador
devolvia o slide cortado embaixo até entrar em tela cheia, porque a barra de
abas e a de favoritos ainda não estavam na conta.

**7.17 Imagem dentro de flex precisa de teto em pixel.** `max-height:100%` numa
imagem só resolve se o pai tiver altura definida; num item de flex esticado ele
é ignorado e a figura transborda por cima do título. Ou o cartão recebe
`align-items:stretch` e a imagem `max-height:100%` com o pai em `height` real,
ou se escreve o teto em px.

**7.18 Cuidado com o `b` herdado.** Vários blocos definem `.bloco b{font-size:30px}`
para um número grande e depois usam `<b>` dentro de um parágrafo do mesmo
bloco. O parágrafo sai com corpo de manchete. Sempre que um bloco tiver um `b`
grande, o texto corrido precisa do seu próprio `b`.

**7.19 Prefixo de classe é único por bloco.** O `_montar.py` junta o CSS de
todos os blocos num arquivo só. Dois blocos com o mesmo prefixo se sobrescrevem
e o slide antigo quebra em silêncio; foi o que aconteceu entre `17-projecao` e
a sua variação, que passou a usar `.prt`.

**7.20 Copiar da Sprint 3 é copiar a forma, não o número.** Onde uma divisória
ou um slide vem de lá, a composição é a mesma e os valores são recalculados na
base atual. A fila do d20a dizia 15 quebras nos 50 primeiros; a nossa avaliação
dá 13, e é 13 que vai para a tela. O mesmo vale para o topo da fila, que mudou
de escore entre as duas rodadas.

**7.21 Nada pode terminar depois de 4,2 segundos.** É o instante em que o
`_verifica.py` mede a tela. Cascata que passa disso é medida no meio e o
elemento sai marcado como invisível; e, no palco, quem apresenta já falou. A
sequência mais longa do deck é a chamada da demonstração, que fecha em 3,35s.

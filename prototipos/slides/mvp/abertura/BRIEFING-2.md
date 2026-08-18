# Rodada 2 · o que o Igor reprovou e o que muda

Leia este arquivo **junto** com `BRIEFING.md`. Dali continuam valendo o contrato de saída, as
11 regras e **a folha de fatos com todo número permitido**. Aqui está o que muda.

## Muda no geral

1. **Duas versões por slide, não três.** Sufixo `-A` e `-B`. Os arquivos `-C` da rodada 1
   ficam no disco como histórico; não mexa neles e não crie novos.
2. **Menos texto. Muito menos.** O veredito dele foi: *"é quase um livro"*, *"muito texto,
   não dá para entender"*. Alvo: **no máximo 45 palavras de corpo por slide**, fora título,
   rótulo de número e legenda de eixo. Se não couber em 45, o slide está tentando dizer duas
   coisas.
3. **Ícone em vez de frase.** Ele pediu ícone explicitamente em três slides. Existe um sprite
   pronto no projeto com 29 ícones, descrito abaixo. Use.
4. **Tom neutro e direto.** Nada de nota da sprint anterior, nada de elogio ao próprio
   trabalho, nada de narrar decisão ("depois da análise X tiramos Y porque Z"). Se algo mudou
   desde a Sprint 2, o slide mostra o estado novo e pronto.
5. **Fora número de processo interno.** Ele reprovou "41 capturas" e "32 achados" com
   *"como um humano saberia disso?"*. Corte tudo que mede o nosso esforço: capturas,
   achados, quantidade de notebooks, contagem de commits, quantidade de slides. Continua
   dentro tudo que mede a operação da Locaweb e os modelos: 122.543, 25.600, 42 e 196
   violações, ROC AUC, erro do Prophet, taxas.
6. **RM nunca em fonte mono.** Ele odiou. Use Outfit com `font-variant-numeric: tabular-nums`.
   Na verdade **não use `var(--mono)` em nada** nesta rodada, exceto nome de arquivo e rota.
7. **Pílula e selo no estilo `.tag` do base.css**: fundo branco, borda fina, texto azul,
   sombra bem suave. **Não** use pílula de contorno azul com letra mono: ele mostrou as duas
   e reprovou essa.
8. **A Claude API sai da arquitetura e da lista de tecnologias.** Foi declarada desde a
   Sprint 1 e não existe uma linha de código dela. O texto do briefing é montado por template
   Django. Não mencione LLM em slide nenhum.

## Reaproveitar a Sprint 2, que já passou por ele

Estes arquivos são os slides aprovados da Sprint 2, autocontidos e renderizando hoje:

- `prototipos/slides/capa-slide.html` · a capa
- `prototipos/slides/arquitetura-slide.html` · o desenho da arquitetura em 4 etapas e 7 nós,
  com a faixa de descrição embaixo
- `prototipos/slides/tecnologias-slide.html` · a stack em 12 placas
  (⚠ os logos vêm de CDN que **não responde** no build; use as imagens locais abaixo)

**Copie o arquivo como base e ajuste só o que mudou.** Não reescreva do zero: a composição
dele já foi aprovada duas vezes.

## Assets locais disponíveis

**Fotos da equipe**, recortadas em círculo com alpha real, 512px, mesma escala de rosto:
`../../../../brand/equipe/ana-beatriz.png`, `hygor.png`, `igor.png`.
Use `border-radius:50%`, `object-fit:cover`, sem fundo colorido atrás, no máximo um anel de
2px em `var(--line)`.

**Placas de tecnologia**, extraídas do PPT da Sprint 2, 260px, em
`../../../../brand/logos/`: `python.png`, `pandas.png`, `numpy.png`, `holidays.png`,
`prophet.png`, `xgboost.png`, `django.png`, `plotly.png`, `docker.png`.
(Existem `tslearn.png`, `shap.png` e `claude.png`, mas **essas três saíram do projeto**.)

**Para biblioteca sem placa pronta**, desenhe em CSS no mesmo padrão da Sprint 2: quadrado de
lado igual ao das imagens, `border-radius:20%`, fundo na cor da marca, sigla de 2 ou 3 letras
em Outfit 800 branco e centralizada. Cores:

| Biblioteca | Sigla | Fundo |
|---|---|---|
| scikit-learn | `sk` | `#F09437` |
| pyarrow | `pa` | `#1B2A4A` |
| matplotlib | `plt` | `#11557C` |
| scipy | `sp` | `#0054A6` |
| statsmodels | `sm` | `#3E4C59` |
| openpyxl | `xl` | `#217346` |
| seaborn | `sb` | `#4C72B0` |
| gunicorn | `gu` | `#499848` |

**Ícones do produto.** O sprite da aplicação está em
`webapp/painel/templates/painel/_sprite.svg` e tem 29 símbolos. Copie o `<path>` que
interessa para dentro de um `<svg>` inline no slide (não referencie o arquivo: caminho
relativo até `webapp/` não resolve bem). Disponíveis:

`i-prazo` `i-relogio` `i-calendario` `i-agora` `i-ativo` `i-servidor` `i-rede` `i-disco`
`i-produto` `i-alerta` `i-escudo` `i-escudo_ok` `i-raio` `i-alvo` `i-fila` `i-entrada`
`i-resolvido` `i-pessoas` `i-tendencia` `i-previsao` `i-balanca` `i-lupa` `i-grade`
`i-coracao` `i-seta` `i-fechar` `i-sino` `i-sol` `i-novo`

Usar o mesmo ícone que está na tela do produto é coerência, não enfeite. Ícone tem 20 a 24px,
`stroke:currentColor`, `fill:none`, `stroke-width:1.8`.

**Figura pronta e conferida:** `sprints/sprint-3/slides/figs/ano_virou.png`, os dois painéis
de violações acumuladas em 2025 contra as faixas da meta.

---

# Slide por slide

## 01 · Capa · `01-capa-A.html` e `01-capa-B.html`

Reprovado: a pílula com cara de IA, o card de data de entrega (*"eles sabem a data de
entrega"*), o RM em mono, e fundo escuro (*"não quero escuro no primeiro slide por mais que
seja bonito"*).

**Base: `prototipos/slides/capa-slide.html`.** Copie e ajuste:
- rótulo do topo esquerdo de `SPRINT 02 · ARQUITETURA` para `SPRINT 03 · MVP PRELIMINAR`
- a pílula central passa para o estilo `.tag`: branca, borda fina, texto azul, sem mono
- **sem RM na capa** e **sem card de data de entrega**
- o cartão de rodapé mantém equipe e mentor como está lá

A diferença entre A e B é pequena de propósito, porque a composição dele já foi aprovada:
- **A** · fiel à Sprint 2, só com os ajustes acima
- **B** · mesma estrutura, com a tagline `Veja antes. Aja antes.` ganhando mais peso e a
  frase de produto saindo, para a capa respirar mais

## 02 · Identificação da equipe · `02-equipe-A.html` e `02-equipe-B.html`

Aprovado: *"ficou melhor o C na esquerda"*, ou seja a coluna esquerda com logotipo grande,
nome e tagline. Reprovado: o quadro de integrantes, *"ficou zuado, simples, sem graça"*, e
apontar o mentor da Locaweb (**tire o mentor deste slide**).

Estrutura das duas versões: coluna esquerda com o logotipo do Cronos grande, o nome da
solução e a tagline. Coluna direita com os três integrantes. Os quatro itens do template
continuam obrigatórios: nome da solução, logotipo, nome da equipe, e nome com RM em ordem
alfabética.

O que precisa melhorar no bloco de integrantes: hoje é uma lista sem hierarquia. Dê presença
à pessoa. Foto maior, nome com peso, RM discreto em Outfit tabular-nums, e a turma uma vez
só para os três em vez de repetida linha a linha.

- **A** · três pessoas em cartões verticais lado a lado, foto grande no topo de cada um
- **B** · três linhas horizontais generosas, foto à esquerda, nome e RM à direita

## 03 · Contextualização · `03-contexto-A.html` e `03-contexto-B.html`

Reprovado: *"aqui tá confuso, muito texto, não dá para entender, precisamos de ícones, deixar
mais limpo"*.

O Ishikawa fica, porque a dica do template nomeia a ferramenta e o Igor aprovou a ideia. O
que sai é o texto. Hoje cada espinha tem rótulo, número e um parágrafo de três linhas. Corte
o parágrafo: **cada espinha fica com ícone, duas ou três palavras, e um número**. Quem
explica é a fala, não o slide.

Seis espinhas, com o ícone sugerido:
- Medição · `i-calendario` · `35 para 41`
- Priorização · `i-fila` · `0,4693`
- Concentração · `i-pessoas` · `46% com 8%`
- Volume e ruído · `i-entrada` · `85,1%`
- Sinal fraco · `i-balanca` · `2,5%`
- Conhecimento · `i-novo` · `1,46%`

Caixa do efeito à direita: `Violação de OLA que só aparece no fechamento do ano`, com
**42 no P2 e 196 no P3**, nota 75% e 150%.

- **A** · Ishikawa ocupando o slide, espinhas enxutas, nada mais
- **B** · Ishikawa em dois terços, e à direita três números da escala da operação com ícone:
  122.543 incidentes, 25.600 que valem para a meta, 248 violações

## 04 · Problema a ser resolvido · `04-problema-A.html` e `04-problema-B.html`

Ele preferiu a régua mês a mês da versão B da rodada 1, mas disse *"não dá para saber do que
se trata, muito texto"*. Então: **mantenha a régua, corte o texto em volta e nomeie melhor**.

O que o slide precisa dizer, e só isso:
1. que o KPI é anual e por faixa
2. que o P2 saiu de **35 em outubro para 41 em novembro** e atravessou duas faixas
3. o que queremos alcançar, em número: fechar o ano dentro de **39 no P2 e 200 no P3**, e
   saber o degrau antes de novembro

Corte os quatro parágrafos de momento do ano. A régua com a célula de novembro destacada
conta isso sozinha.

- **A** · a régua mês a mês nas duas prioridades, uma linha de leitura embaixo, e as metas em
  três números com ícone
- **B** · a figura `ano_virou.png` como protagonista, com as metas ao lado

## 05 · Proposta de solução · `05-solucao-A.html` e `05-solucao-B.html`

Reprovado inteiro: *"esse nem preciso comentar, todos horríveis, é quase um livro e todos
feios, bem fora do padrão"*. **Comece do zero.**

O que o slide tem de dizer: o Cronos prevê quanto entra, aponta qual caso vai estourar,
projeta onde o ano fecha, e entrega isso na entrada do turno sem ninguém perguntar.

Regra de ouro aqui: **quatro blocos, um ícone e um número por bloco, no máximo doze palavras
por bloco.** Nada de tabela, nada de parágrafo, nada de faixa de rodapé com mudanças.

Os quatro blocos e o número de cada um:
- Previsão de volume · `i-previsao` · erro de **11,8 por dia no P3 e 4,2 no P2**
- Risco por incidente · `i-alvo` · **72%** das violações nos 20% de maior risco
- Projeção do KPI · `i-tendencia` · acerta **7 de 10**
- Chega sem ser pedido · `i-sol` · briefing na entrada do turno

- **A** · os quatro blocos em grade 2 por 2, grandes, cada um com ícone e número
- **B** · os quatro em fileira horizontal ligada por seta, como um fluxo do turno

## 06 · Gerenciamento atualizado · `06-gestao-doc-A.html` e `06-gestao-doc-B.html`

Ele disse *"está ok, quero mais clean, focado e direto, não precisa falar da nota da sprint
anterior nem nada"*.

Então: **fora as notas 5,00 e fora o que o professor pediu.** Fica a área reservada do quadro
do Trello, grande, e uma tabela seca de sprint, entrega e situação. Nada de coluna de
planejado, executado e entregue em três linhas de texto por sprint: uma linha por sprint,
curta.

Área reservada do quadro: proporção 16 por 9, borda tracejada de 1,5px, rótulo
`Quadro do projeto no Trello`. **Este slide leva o quadro completo.**

- **A** · quadro ocupando dois terços, tabela das quatro sprints à direita
- **B** · quadro largo no corpo, tabela em faixa fina embaixo

## 07 · Planejamento e gestão · `07-gestao-plano-A.html` e `07-gestao-plano-B.html`

Reprovado: muito texto, e os números de processo interno (41 capturas, 32 achados).
Ele também perguntou, e a resposta é sim: **este slide leva o print do cartão aberto do
Trello.** Reserve uma área para ele, proporção 4 por 3, mesma borda tracejada, rótulo
`Cartão em andamento`.

O resto do slide: o cronograma das quatro sprints com data, e a divisão por frente de
trabalho com `[responsável]` para o Igor preencher. **Sem os marcos internos com data de
agosto** e sem descrever nosso processo de revisão.

- **A** · cartão aberto à esquerda, cronograma das sprints e frentes à direita
- **B** · cronograma no topo em trilho horizontal, cartão aberto e frentes embaixo

## 08 · Arquitetura da solução · `08-arquitetura-A.html` e `08-arquitetura-B.html`

Este slide é **as fontes de dados**, que é o que a dica do template cobra ali:
*"indique principalmente, todas as fontes de dados necessárias"*. Ele também pediu
**ícones reais das linguagens e bibliotecas**, comparando com a Sprint 2.

Duas fontes, e só duas: `LW-DATASET.xlsx` da Locaweb (122.543 incidentes, 19 colunas,
jan/2023 a dez/2025) e a biblioteca `holidays` para feriado nacional. Mais a régua de
elegibilidade, que é o que decide o que entra: **122.543 para 25.600 pelo campo
`Entrou para KPI?`**, contra os **107.416** do filtro errado.

Use as placas locais de `python.png`, `pandas.png` e `holidays.png` aqui, e a placa de letra
`xl` para openpyxl.

- **A** · as duas fontes como fichas grandes com placa, e a régua de elegibilidade como
  faixa embaixo com os três números
- **B** · a régua de elegibilidade como protagonista no centro, fontes em volta

## 09 · Desenho da arquitetura · `09-desenho-A.html` e `09-desenho-B.html`

**Base obrigatória: `prototipos/slides/arquitetura-slide.html`.** Copie e ajuste só o que
mudou. O que mudou:

- o nó de ML sai de `Prophet volume · XGBoost risco / tslearn clusters · SHAP explica` para
  **`Prophet volume · Regressão logística risco`**
- **o nó da Claude API sai inteiro**, e a etapa 3 reorganiza para não deixar buraco
- o nó do Django sai de `Django · Plotly / dashboard near real-time` com os bullets
  `Morning brief · Score de saúde · Detector de cascata · Probabilidade de KPI` para
  **`Django / seis abas`** com `Morning brief · Score de saúde · Fila de risco · Projeção de KPI`
- o nó do Pandas ganha o número da elegibilidade, `122.543 para 25.600`
- o subtítulo perde o travessão e a menção a "7 etapas" se o número de nós mudar

**Não narre a mudança.** Nada de "o detector de cascata saiu porque". O slide mostra o estado
atual.

- **A** · o desenho da Sprint 2 ajustado, com a faixa de descrição embaixo como está lá
- **B** · o mesmo desenho sem a faixa de descrição, ocupando o slide inteiro e maior, já que
  a descrição tem slide próprio no 10

## 10 · Descrição da arquitetura · `10-descricao-A.html` e `10-descricao-B.html`

Ele disse: *"creio que já tenha no anterior, numa das versões você coloca a versão igual ao
da Sprint 2"*.

- **A** · a **faixa de descrição da arquitetura da Sprint 2**, promovida a slide inteiro: um
  cartão numerado por nó, com o texto de lá atualizado para o estado atual (sem Claude API,
  sem cascata, sem tslearn e sem SHAP). Mesma composição, mesmo tom.
- **B** · a descrição organizada nas **cinco camadas que a dica do template lista**: Fontes de
  Dados, Pipeline de Ingestão, Armazenamento, Processamento, Visualização e Análise. Uma
  faixa por camada, com a nossa implementação e a placa da tecnologia.

## 11 · Tecnologias · `11-tecnologias-A.html` e `11-tecnologias-B.html`

Mesma instrução: uma das versões igual à da Sprint 2.

- **A** · **cópia da composição de `tecnologias-slide.html`**, grade de duas colunas com placa,
  nome, etiqueta de categoria, versão e uma linha do que resolve. Trocando os logos de CDN
  pelas imagens locais e a lista pela stack atual. Fora tslearn, SHAP e Claude API. Dentro
  scikit-learn, pyarrow, matplotlib e o que mais couber em **doze placas**, que é o número
  que a Sprint 2 usou.
- **B** · as mesmas doze placas agrupadas pelas cinco camadas da arquitetura, mais compacto,
  com a versão ao lado do nome e sem a coluna de descrição.

---

## Verificação obrigatória

Renderize cada arquivo a 1600x900 com playwright (`channel="chrome"`) e **olhe a imagem**.
Depois conte as palavras de corpo: se passar de 45, corte. Confira que não sobrou fonte mono,
que nenhuma imagem quebrou, e que nenhum número de processo interno entrou.

No relatório final diga, por arquivo: a ideia da versão, a contagem de palavras de corpo, e
qualquer `[verificar]` ou `[responsável]` que ficou.

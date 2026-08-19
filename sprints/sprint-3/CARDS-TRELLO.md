# Quadro do projeto no Trello · o que lançar

O quadro **Cronos · Challenge FIAP 2026** parou no estado da Sprint 2. Este arquivo é a
lista do que precisa entrar para ele refletir a Sprint 3.

A réplica desenhada está em `sprints/sprint-3/quadro/` (HTML e PNG), gerada por
`scripts/monta_quadro_trello.py`. Ela mostra como o quadro fica depois de lançado.

Todo cartão aqui descreve trabalho que aconteceu, e as datas são as reais, tiradas de
`context/status.md` e do histórico do repositório.

---

## Etiquetas

Oito etiquetas, em duas famílias. A cor da família de sprint sobe de verde a azul conforme
a entrega avança, então dá para ler a idade do cartão sem ler o texto.

| Etiqueta | Cor no Trello |
|---|---|
| `Sprint 1` | Verde |
| `Sprint 2` | Amarelo |
| `Sprint 3` | Laranja |
| `Sprint 4` | Azul-celeste |
| `Análise` | Roxo |
| `Modelagem` | Rosa |
| `Aplicação` | Azul |
| `Entregável` | Vermelho |

## Responsáveis

Três iniciais, seguindo a divisão que o slide 8 declara — base e análise exploratória em
dupla, modelagem e aplicação com revisão cruzada, deck e validação com os três.

| Sigla | Pessoa | Frente principal |
|---|---|---|
| **BC** | Ana Beatriz Costa de Oliveira | Base, análise exploratória, revisão |
| **HA** | Hygor Abrantes | Modelagem |
| **IV** | Igor Vignola | Aplicação, deck |

## Ordenação

A lista **Concluído** precisa estar ordenada por *data de criação, mais recente primeiro*
(menu da lista → Ordenar por). Na ordem padrão, os cartões da Sprint 1 ficam no topo e o
print mostra trabalho de abril em vez do trabalho desta entrega.

---

## Backlog · 5

| Cartão | Etiquetas | Quem |
|---|---|---|
| Publicar a aplicação num provedor | `Sprint 4` `Aplicação` | IV, HA |
| Gravar o vídeo pitch de 5 minutos | `Sprint 4` `Entregável` | IV, BC, HA |
| Calcular o custo mensal da Claude API | `Sprint 4` `Análise` | BC |
| Decidir se o dataset vai para o repositório público | `Sprint 4` | IV |
| Checar se há dado pessoal no campo Solução | `Sprint 4` `Análise` | BC |

Descrições:

- **Publicar a aplicação num provedor** — subir o contêiner e deixar a URL acessível para
  a banca.
- **Gravar o vídeo pitch de 5 minutos** — roteiro em seis blocos, hands-on mostrando as
  seis abas. Upload no YouTube público.
- **Calcular o custo mensal da Claude API** — pedido do Douglas na mentoria: quantos
  briefings por dia, tamanho médio do prompt, custo mês e ano.
- **Decidir se o dataset vai para o repositório público** — a Sprint 4 exige
  repositório público. A varredura não achou dado pessoal, mas falta decidir e registrar a
  posição.
- **Checar se há dado pessoal no campo Solução** — texto livre, ainda não coberto
  pela varredura.

## A Fazer · 3

| Cartão | Etiquetas | Quem | Entrega |
|---|---|---|---|
| Atualizar os anexos das Sprints 1 e 2 | `Sprint 3` `Entregável` | BC, HA | 22/08 |
| Incluir as referências bibliográficas | `Sprint 3` `Entregável` | HA | 22/08 |
| Subir o arquivo final no portal FIAP ON | `Sprint 3` `Entregável` | IV | 23/08 |

Descrições:

- **Atualizar os anexos das Sprints 1 e 2** — os dois PPT ainda declaram XGBoost para
  risco, clusterização por DTW e o detector de cascata. Precisam sair alinhados ao que foi
  medido depois, senão o material se contradiz.
- **Incluir as referências bibliográficas** — artigo do Prophet, definição de MAE e o
  protocolo de rolling backtest.
- **Subir o arquivo final no portal FIAP ON** — conferir nome do arquivo e formato antes
  de enviar.

## Em Andamento · 2

| Cartão | Etiquetas | Quem | Entrega |
|---|---|---|---|
| Montar o PPT da Sprint 3 | `Sprint 3` `Entregável` | IV, BC, HA | 23/08 |
| Registrar no notebook o teste que descartou a cascata | `Sprint 3` `Análise` | HA | 21/08 |

- **Montar o PPT da Sprint 3** — é o cartão aberto que vai para o deck, detalhado no fim
  deste arquivo.
- **Registrar no notebook o teste que descartou a cascata** — os três números (87% de
  violações isoladas, escalada de 21% contra os 60% do acaso) ficaram em notebook de
  laboratório e não têm código versionado que os reproduza. Checklist em 2/3.

## Em Revisão · 2

| Cartão | Etiquetas | Quem | Entrega |
|---|---|---|---|
| Conferir o deck com o checklist da sprint | `Sprint 3` `Entregável` | BC | 22/08 |
| Revisar os textos dos slides de análise e modelagem | `Sprint 3` `Entregável` | IV, BC | 21/08 |

- **Conferir o deck com o checklist da sprint** — percorrer item por item do template
  antes de fechar o arquivo. Checklist em 9/12.
- **Revisar os textos dos slides de análise e modelagem** — terceira rodada de corte de
  texto, com cada número conferido contra a célula que o produz.

## Concluído · 20

Ordenados do mais recente para o mais antigo, que é a ordem em que precisam aparecer.

| Cartão | Data | Etiquetas | Quem |
|---|---|---|---|
| Tirar os prints da aplicação para a entrega | 17/08 | `Sprint 3` `Entregável` | IV |
| Revisão visual das seis abas do painel | 17/08 | `Sprint 3` `Aplicação` | IV, BC |
| Conferir os números da tela com os notebooks | 14/08 | `Sprint 3` `Aplicação` | HA, IV |
| Subir a aplicação Django com as seis abas | 11/08 | `Sprint 3` `Aplicação` | IV, HA |
| Construir o score de saúde por produto | 05/08 | `Sprint 3` `Modelagem` | BC |
| Escrever os notebooks de risco, causas e projeção do KPI | 04/08 | `Sprint 3` `Modelagem` | HA, BC |
| Escolher a regressão logística no lugar do XGBoost | 03/08 | `Sprint 3` `Modelagem` | HA, IV |
| Rodar as verificações de robustez | 29/07 | `Sprint 3` `Modelagem` | HA |
| Testar a hipótese de acúmulo de backlog | 29/07 | `Sprint 3` `Modelagem` | HA, BC |
| Testar a hipótese de cascata do mentor | julho | `Sprint 3` `Modelagem` | HA |
| Treinar e validar a previsão de volume | julho | `Sprint 3` `Modelagem` | HA, IV |
| Definir alvo e escopo da modelagem | 21/07 | `Sprint 3` `Modelagem` | IV, HA, BC |
| Investigar a anomalia de setembro de 2025 | julho | `Sprint 3` `Análise` | BC |
| Fechar a base compartilhada com o campo oficial de KPI | julho | `Sprint 3` `Análise` | BC, IV |
| Entrega da Arquitetura da Solução | 24/05 | `Sprint 2` `Entregável` | IV, BC, HA |
| Protótipos das telas do dashboard | maio | `Sprint 2` `Aplicação` | IV |
| Definir a arquitetura e as tecnologias | maio | `Sprint 2` | IV, HA |
| Caracterização inicial do dataset | 22/05 | `Sprint 1` `Análise` | BC, HA |
| Mentoria com Douglas Gouveia, da Locaweb | 14/05 | `Sprint 2` | IV, BC, HA |
| Ideação do projeto | 27/04 | `Sprint 1` `Entregável` | IV, BC, HA |

Descrições que valem escrever (o resto o título já cobre):

- **Revisão visual das seis abas do painel** — 41 capturas em quatro larguras. 32 achados
  corrigidos, incluindo um gráfico cuja barra contradizia o número impresso. Checklist
  32/32.
- **Conferir os números da tela com os notebooks** — achou a escada do KPI invertida e
  três notebooks medindo fora da janela da aplicação. Corrigidos e reexecutados.
- **Construir o score de saúde por produto** — cinco componentes com peso igual, nota de 0
  a 100, com teste de sensibilidade.
- **Testar a hipótese de cascata do mentor** — não se confirmou: 87% das violações são de
  incidentes isolados. Sai do MVP.
- **Testar a hipótese de acúmulo de backlog** — correlação de −0,139 entre backlog diário e
  violações. O sinal aponta para o lado contrário.
- **Fechar a base compartilhada com o campo oficial de KPI** — filtro por
  `Entrou para KPI?`, de 122.543 para 25.600 linhas, com asserts travando as duas
  contagens. Todos os outros notebooks leem esse parquet.
- **Investigar a anomalia de setembro de 2025** — volume salta de 4 mil para 21,6 mil no
  mês. Causa: expansão do monitoramento automático, não piora da operação.
- **Treinar e validar a previsão de volume** — Prophet contra dois baselines, com rolling
  backtest. Erro de 11,8 por dia no P3 e 4,2 no P2.

---

## Os dois cartões abertos

O print do cartão aberto mostra que o quadro é usado, e não só decorado. O deck leva a
opção A; a B fica desenhada como alternativa.

### Opção A · Montar o PPT da Sprint 3 — a que está no deck

Lista **Em Andamento** · `Sprint 3` `Entregável` · IV, BC, HA · entrega 23/08/2026 23:59

> Montar o PPT da Sprint 3 na ordem do template da FIAP, reunindo num arquivo só o bloco de
> análise e modelagem e os prints da aplicação. Formato .pptx, 16:9.
>
> Entregáveis do cartão: o arquivo .pptx nomeado no padrão da FIAP, os prints da aplicação
> e os anexos atualizados das sprints anteriores.

Checklist **Conferência do template** — 6 de 7:

- [x] Identificação da equipe com RM em ordem alfabética
- [x] Contextualização, problema e proposta atualizados
- [x] Arquitetura da solução e descrição das tecnologias
- [x] Prints da aplicação com explicação de cada tela
- [x] Amostra dos dados utilizados
- [x] Imagem do quadro de planejamento
- [ ] Anexos atualizados das Sprints 1 e 2

Comentário (IV): *Deck fechado em 65 slides. Falta atualizar os anexos das Sprints 1 e 2.*

### Opção B · Escolher a regressão logística no lugar do XGBoost

Lista **Concluído** · `Sprint 3` `Modelagem` · HA, IV · concluída em 03/08/2026

> Comparar regressão logística e XGBoost no risco de quebra de OLA e fechar qual dos dois
> vai para a aplicação. O evento é raro, então a métrica de decisão é PR-AUC.
>
> Medição: ROC AUC 0,869 contra 0,868, empate. PR-AUC 0,296 contra 0,253, vantagem de 17%
> para a logística. A logística prevê 48,1 quebras onde houve 50; o XGBoost com
> `scale_pos_weight` prevê 1.007 e inviabiliza a projeção do KPI.
>
> Decisão: logística no MVP, XGBoost fica no notebook como baseline de comparação.

Checklist **Validação do modelo** — 4 de 4:

- [x] Treino e teste separados por data, sem vazamento
- [x] PR-AUC e ROC AUC medidos nos dois modelos
- [x] Calibração conferida contra o realizado
- [x] Decisão registrada em `context/decisoes-tecnicas.md`

Comentário (HA): *Com 0,97% de positivos, acurácia não separa modelo bom de modelo que só
responde “não quebra”. Por isso a decisão saiu pelo PR-AUC.*

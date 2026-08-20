# Status · onde estamos AGORA

> Primeiro arquivo a consultar para retomar o trabalho. Atualizar a cada bloco concluído.
> O detalhamento técnico da sprint corrente fica em `docs/sprint-3-mvp.md`; a preparação para a banca, em `docs/dossie-banca.md`.

**Atualizado em:** 17/08/2026

---

## Sprint atual: Sprint 3 · MVP Preliminar (entrega 23/08/2026)

| Sprint | Tema | Entrega | Situação |
|---|---|---|---|
| 1 | Ideação | 27/04/2026 | Entregue · nota 5,00/5,00 |
| 2 | Arquitetura | 24/05/2026 | Entregue · nota 5,00/5,00 |
| 3 | MVP Preliminar | 23/08/2026 | **Em andamento** |
| 4 | Solução Final | 08/09/2026 | Futuro |

Único ajuste pedido pelo professor na Sprint 2: slide explícito de gestão ágil. O template da Sprint 3 já tem dois slides dedicados a Kanban e gestão, então isso se resolve na montagem do PPT.

---

## O que está pronto

### Base de dados e análise
- **`notebooks/02_base_kpi.ipynb`** · base compartilhada. Carrega o dataset oficial, tipa as colunas, aplica o filtro de elegibilidade pelo campo `Entrou para KPI?` e grava `data/interim/incidentes_kpi.parquet` (25.600 linhas × 24 colunas: as 19 originais mais 5 de calendário). Tem asserts de invariante (122.543 no total, 25.600 elegíveis) e verificação pós-tipagem.
- **`notebooks/01_eda.ipynb`** · análise exploratória completa, com a investigação da anomalia de setembro rastreável em célula (status "Sem Intervenção" 47 para 17.838, itens de configuração novos 458 para 1.693, descrição mais frequente "Problem: Check Application Monitoring") e o perfil do Team14.

### Modelo 1 · Previsão de volume
- **`notebooks/03_previsao_volume.ipynb`** · executado sem erro, 49 células, 8 figuras em `notebooks/figures/03_previsao_volume/`.
- Prophet com sazonalidade semanal, anual desligada, feriados nacionais, banda de 80%, previsões não negativas; treino restrito a 2025.
- Validado por corte out-of-time e por rolling backtest. Erro divulgado: **P2 com erro médio de 4/dia e P3 de 11/dia** (MAE médio D+1 a D+7).
- Seção 4.10 de robustez: cobertura empírica da banda (P2 entre 86% e 88%, P3 entre 59% e 61%), verificação de que a queda de novembro e dezembro é efeito real e não censura, e o teste da relação entre volume e quebra de OLA.

### Deck da sprint
- **`prototipos/slides/mvp/deck/viewer.html`** · 19 slides navegáveis (seta para baixo troca slide, seta lateral troca variação). Seções: Análise Exploratória e Previsão de Volume.
- Linguagem visual definida: divisória escura com painel de preview, conteúdo em fundo claro com gradiente azul, número sempre rotulado com cor semântica. Gráficos pesados são exportações reais do matplotlib dos notebooks. Ver `memory/deck-mvp-v2-linguagem.md`.

### Aplicação Django — auditoria e reconstrução (11 a 14/08/2026)
Seis abas no ar (`/`, `/previsao/`, `/projecao/`, `/fila/`, `/saude/`, `/causas/`), todas reconstruídas depois de uma auditoria que procurou uma coisa só: número que a tela não poderia saber.

- **A escada de atingimento do KPI estava invertida.** O notebook 06 media P2 contra a faixa de 75% e P3 contra a de 150%. Isso trocava os vereditos: o P3, que está em 125%, aparecia em alarme âmbar; o P2, que está em 75% e é onde a pressão realmente está, aparecia em verde. Agora a escada inteira, com os seis degraus, está em `servicos.py: ESCADA` e desenhada na aba Projeção.
- **Três notebooks produziam dado fora do relógio.** O 05 (causas) não tinha filtro de data nenhum e rodava sobre 2023–2025; o 07 (saúde) incluía outubro a dezembro, 20% da base. Recortados em 30/09/2025 e reexecutados. Consequências: a saúde caiu de 17 para 15 produtos, o pior produto mudou de `lssl` (15,3) para `lvps` (21,3), e o achado de que os grupos críticos eram 100% P3 se revelou artefato da janela.
- **A taxa média da base era um número cravado à mão** (`0,97`, vindo da base inteira). Passou a ser derivada: **0,94%**. É o denominador do "× a média" em quatro telas.
- **P2 entrou em todas as telas.** O dado já estava no pacote desde sempre — série prevista, sazonalidade, causas, saúde — e nenhuma tela usava. Também se descobriu que a curva de chegada hora a hora era medida no agregado, embora o código dissesse P3; as curvas por prioridade diferem de verdade (às 06h o P3 tem 11% do dia, o P2 tem 23%).
- **A máquina do tempo saiu do sistema.** Era a peça mais forte da tela e é feita inteira de futuro: percorria 92 dias exibindo o realizado de outubro a dezembro. Continua no repositório marcada como peça de apresentação (`_maquina.html`, `maquina.js`).
- Registro navegável do trabalho: `scratchpad/auditoria.html`, publicado como artifact.

### Auditoria visual e lapidação da aplicação (17/08/2026)

Varredura das seis abas com o servidor no ar: 41 capturas em quatro larguras, com modais
abertos, hover, foco, filtros e estado vazio, mais medição de DOM elemento a elemento.
**32 achados**, dos quais os 6 apontados pelo Igor. Registro: artifact da auditoria visual.

**Consertado (grupo A e B — defeito, não gosto):**

- **O cabeçalho de seção da aba Panorama saía 144 px fora do alinhamento.** `.en-bl-h` era grid
  de três colunas e o bloco "O dia hora a hora" é o único com quatro filhos; o quarto
  transbordava e a primeira coluna passava a valer a largura do link. Em 390 px o título era
  medido com **largura zero e 105 px de altura** — uma palavra por linha. Virou flex.
- **O gráfico de sazonalidade da Previsão contradizia o próprio rótulo.** A altura da barra era
  porcentagem da coluna inteira, que também carrega os rótulos; acima de ~88 px o flex
  encolhia. No P3, 68 · 76 · 74 · 75 · 66 saíam idênticas; no P2, 17 e 14 também. Trilho de
  altura própria em grid resolveu — proporção desenhada voltou a ser a do número impresso.
- **Três opacidades diferentes para a mesma superfície** (.62, .84, .88) faziam o campo de
  linhas do fundo atravessar número, parágrafo e barra. Cartão de dado passou a ser opaco; o
  campo continua vivo nas margens.
- `.bt` não declarava `text-decoration`, então em `<a>` vinha sublinhado e em `<button>` não.
  Mesma omissão em `.bl`.
- **Dois botões sem ouvinte nenhum** ("Avisar se passar de 60%", "Avisar em novo incidente") e
  um link circular ("Comparar no ranking" apontando para a página de onde o modal abria).
- **Dois casos de "1,0%" com cores opostas** na Fila: 1,04 e 0,98 imprimem o mesmo valor e o
  corte da faixa é 1%. O nome da faixa passou a vir escrito ao lado do número.
- **Ordem P2/P3 divergia entre abas.** Centralizada em `servicos.ORDEM_PRI`.
- O gerador de ícones escrevia em `static/painel/icones.svg`, que nenhum template referencia;
  o sprite em uso (`templates/painel/_sprite.svg`) não era gerado por script nenhum e já estava
  um glifo atrasado. `publica_estatico.py` passou a escrever no arquivo certo.

**Linguagem (grupo D):** 38 ocorrências de vocabulário nosso na tela → **zero**. "Corte
crítico" virou "limite de alerta"; "percentil 93" virou a posição real ("2º pior de 15",
derivada do rank exato do parquet); R² e r saíram do sistema e ficaram no deck; os quatro
estados da Saúde ganharam legenda no ponto de uso. Parágrafos com 22+ palavras: 17 → 7, e o
maior caiu de 66 para 29 palavras.

**A régua do KPI lia como invertida — e o dado estava certo.** Conferido contra o dicionário
oficial (`Dicionário de Dados - v2.docx`, "Metas Anuais de KPI · Incidentes com OLA quebrados
no ano"): 3-Média `< 201 → 150%`, `201 a 230 → 125%`, `231 a 263 → 100%`, `264 a 290 → 75%`,
`291 a 320 → 50%`, `> 320 → 0%`, batendo degrau a degrau com `servicos.ESCADA`. O defeito era
de rótulo: a coluna "% de atingimento" é a **nota da operação no ano**, não percentual de um
teto, e a tela nunca disse isso. A escada saiu do corpo da Projeção e virou folha ao toque
(`/detalhe/meta/<pri>/`), em três variantes selecionáveis por `?regua=a|b|c` — padrão `c`, a
escada de degraus, em que a **altura do degrau é a própria nota**.

**Identidade de produto.** Os 15 códigos de quatro letras não tinham nada que os separasse.
Agrupar por família de produto foi descartado com dado: os 51 códigos são opacos e a coluna
`Categoria` **também é anonimizada** (`cat71`, `cat103`); o agrupamento por categoria dominante
devolve 13 grupos para 15 produtos. No lugar entrou **quem atende**, derivado de
`Grupo designado` na mesma janela da nota — dominância de 40% a 100%, com selo colorido por
equipe (matiz por ângulo áureo, saturação baixa para não competir com a cor de estado).

### Deck da entrega, fechado em 20/08/2026

`sprints/EC_Sprint_3_2TSCOA_Evidencias_Construcao_Cronos_SuperDataBros.pptx` · **61 slides**,
13,333 × 7,5 in, na ordem e com os títulos do template oficial. Mesmo formato da Sprint 2: um
PNG sangrado por slide, gerado de HTML. 42 MB, contra 35 MB da Sprint 2.

O nome do arquivo mudou em 20/08/2026. O portal da FIAP pede
`EC_Sprint_3_2TSCOA_Evidencias_Construcao_<projeto>_<grupo>.pptx`, e o deck estava saindo com
`mvp_preliminar` no lugar de `Evidencias_Construcao`.

Duas mudanças de conteúdo na mesma data. O **slide 14, de código-fonte**, é novo
(`abertura/12-codigo-C.html`): o template oficial pede "entregar algoritmos, métodos,
manipulações e transformações utilizadas" e o enunciado pede "uso efetivo de código-fonte",
e o deck mostrava o resultado do código em 34 slides sem mostrar uma linha de código. Ele
traz a árvore do repositório, um trecho do notebook 04 com a saída da célula e os dois
comandos de Docker que sobem a aplicação. Os números do inventário saem de
`scripts/inventario_codigo.py`. E o **slide 43** passou de `d33a-r5a` para `d33a-r6b`, com a
figura refeita por `scripts/figura_controles.py`.

Os slides 34 e 43 passaram a escrever a base a que se referem. Os dois tratam a
familiaridade do problema, o 34 sobre a base elegível inteira (25.600 incidentes, 248
quebras) e o 43 sobre o recorte de jan a set de 2025 (19.973 e 188), e sem o rótulo eles
pareciam discordar: 1,60% de um lado contra 1,46% do outro para o caso inédito. A
auditoria de 17/08 já tinha apontado isso.

O pacote `sprints/EC_Sprint_3_2TSCOA_Evidencias_Construcao_Cronos_SuperDataBros.zip`
(`scripts/monta_zip_entrega.py`, 8 arquivos, 44 MB) leva **só o .pptx e os sete notebooks
executados**, por decisão do Igor. **Não é o anexo da Sprint 3**: o portal aceita um anexo
por entrega e o enunciado nomeia o arquivo fonte PowerPoint. O .zip serve ao arquivo do
grupo, ao mentor e à Sprint 4, que pede um pacote nesse formato.

São **quatro fontes reunidas em um arquivo só**, e é bom saber disso antes de mexer. O
builder virou quase só um ordenador: lê cada slide de onde ele está e escreve apenas o mockup.

- **13 slides de abertura em `prototipos/slides/mvp/abertura/`**, pelo mapa `ESCOLHIDOS`:

  | Slide | Versão |
  |---|---|
  | 01 capa | B |
  | 02 equipe | B |
  | 03 contexto · a operação e o prazo de OLA | E |
  | 03b contexto · por que o estouro é difícil de antecipar | E |
  | 04 problema | D |
  | 05 solução | D |
  | 06 gestão · o quadro em tela cheia | D |
  | 07 gestão · o cronograma | D |
  | 07b gestão · uma atividade aberta no quadro | D |
  | 08 fontes de dados | D |
  | 09 arquitetura · o fluxograma | D |
  | 10 descrição da arquitetura | A |
  | 11 tecnologias | A |

  As demais versões continuam na pasta. Trocar a escolhida é uma linha no mapa.

- **34 slides do bloco analítico em `prototipos/slides/mvp/deck/`**, pela lista `ANALISE`. O
  sufixo `-r5a` ou `-r5b` marca a versão escolhida na rodada 5, em que 24 slides voltaram
  para a mesa e foram refeitos em duas composições cada. Slide sem sufixo é o que não
  precisou mudar.

- **12 slides da aplicação em `prototipos/slides/mvp/aplicacao/`**, pelo mapa
  `ESCOLHIDOS_APP`: a divisória, as dez telas geradas por `scripts/monta_prints_app.py` e o
  fecho. Os quatro modais vêm logo depois da aba de onde saem, e a captura ocupa cerca de
  70% da área do slide.

- **1 slide escrito em `scripts/monta_deck_sprint3.py`**: o mockup.

**Seis slides saíram do deck** e continuam em disco: as duas hipóteses descartadas, os
limites do modelo, o fechamento do bloco analítico, a amostra de dados e o duplicado do
quadro. Saiu também o `d31a`, que repetia sobre outra base o achado de familiaridade que já
está no `d22a`.
**Auditoria dos números do bloco analítico (17/08).** Os slides de julho foram conferidos um
a um contra os parquets e notebooks reexecutados. O achado: **os slides de causas,
recorrência e saúde tinham sido construídos sobre a base inteira de 25.600 elegíveis de 2023
a 2025**, e os notebooks 05, 06 e 07 passaram a medir a janela de 01/01 a 30/09/2025, com
19.973 incidentes e 188 quebras. Foram **50 substituições em sete slides** e **seis figuras
matplotlib reexportadas**. Duas afirmações caíram por não se sustentarem no dado novo: "a
segunda maior concentração de quebras da base" e "todos descendo", que deixou de valer em
dois dos quatro recortes. Os blocos de EDA, previsão de volume e risco de OLA passaram
limpos: o `0,97%` e os `25.600` que aparecem neles são da base de todos os anos, que é a
janela que esses slides declaram.

**As duas divergências que ficavam registradas como pendentes foram resolvidas em 19/08**,
junto com mais nove achados. Ver `docs/auditoria-consistencia-deck.md`, que cruzou todo
número de todo slide contra o parquet.

- **A meta do P3 tinha duas definições vivas**, 200 no notebook 06 e 263 na aplicação, e o
  deck chegava a dar veredito oposto sobre a mesma projeção em dois slides. O deck inteiro
  passou a usar a faixa de 100%: **39 no P2 e 263 no P3**, que é a régua do slide do
  problema. Com 43,5 e 208,0 projetadas, a leitura é P2 acima e P3 dentro.
- **O gradiente de familiaridade aparecia com dois multiplicadores**, 4,6 no `d22a` e 4,7 no
  `d31a`, porque cada um media sobre uma base. O `d31a` saiu do deck e o achado ficou em um
  slide só.

- **38 slides do bloco analítico**, que já existiam em `prototipos/slides/mvp/deck/`,
  construídos em julho. São eles que carregam os gráficos exportados do matplotlib dos
  notebooks, e é o que a dica do slide 13 do template pede ao listar "algoritmos utilizando
  modelos matemáticos e estatísticos" e "imagens das visualizações obtidas". O builder os
  **lê de onde estão**, sem copiar, para não criar uma segunda cópia que envelheça sozinha.
  A ordem e a variação escolhida de cada um estão na constante `ANALISE`.

Os cinco slides de resumo de modelo que o builder tinha no começo foram removidos: o bloco
analítico diz a mesma coisa em 38 slides e com o gráfico ao lado.

**O bloco de abertura foi refeito em 17/08**, depois que o Igor apontou que os treze
primeiros slides estavam genéricos. O defeito era estrutural antes de ser de texto: oito
deles usavam a mesma composição (título, três cartões de número, três cartões numerados com
cabeçalho em negrito seguido de parágrafo), que é o molde que a máquina produz sozinha. Cada
slide passou a ter a composição que o conteúdo dele pede, e dois trocaram texto por dado:

- **Contexto** virou a escada de seis degraus do KPI, P3 e P2 em cartões separados, com a
  altura da barra sendo a própria nota.
- **Problema** virou gráfico (`scripts/figuras_deck.py`): violações acumuladas mês a mês em
  2025 contra as faixas da meta. O achado que o gráfico revelou e que não estava em lugar
  nenhum do material: **o P2 sai de 35 violações em outubro para 41 em novembro e atravessa
  duas faixas de uma vez**, caindo de 125% para 75%. Seis violações num mês custaram 50
  pontos de nota.
- **Proposta** virou o mapa das quatro exigências do desafio contra a peça que responde cada
  uma; **o que mudou desde a Sprint 2** virou lista de "de" e "para" com o número que
  derrubou cada ideia; **gestão** ganhou linha do tempo das quatro sprints; **arquitetura e
  desenho** fundiram num slide só.
- Saiu o slide de escopo, que repetia o `d17a` do bloco analítico.

O texto passou pela skill `humanizer`. Caíram os paralelismos do tipo "não é X, é Y", o
título em regra de três e os cartões com cabeçalho em negrito seguido de parágrafo. Também
saiu do deck a frase que afirmava que os anexos das Sprints 1 e 2 iam atualizados junto, o
que não é verdade até que alguém os atualize.

Reprodutível por dois scripts. `scripts/captura_telas.py` fotografa a aplicação (seis abas e
quatro modais, 3200 × 2000, enquadrados em 16:10 para entrarem inteiros no slide);
`scripts/monta_deck_sprint3.py` escreve os slides próprios, renderiza os 65 e monta o `.pptx`.
O estilo mora em `scripts/deck_estilo.py`, separado do conteúdo.

Decisões tomadas com o Igor na montagem:

- **Layout do slide de print:** título à esquerda, legenda de três linhas à direita, moldura de
  navegador com a tela em 1020 px, sem corte. Foram desenhadas três variações; a que punha o
  print sangrado ao fundo foi descartada porque a tela virava textura justamente no slide cuja
  função é provar que ela existe.
- **Os dez prints entram**, incluindo os quatro modais: cada um responde uma exigência do
  desafio que a tela de fundo sozinha não responde (briefing, decomposição do escore,
  componentes da nota, régua do KPI).
- **O mockup foi montado inteiro no deck**, em moldura de notebook, sem passar pelo Figma.
- A URL exibida na moldura é `cronos-locaweb.onrender.com`, escolha do Igor para a tela
  aparecer como se estivesse publicada.

Verificações rodadas sobre o arquivo gerado: 32 imagens em 32 slides no tamanho do template;
nenhum slide cita P3 sem citar P2; zero travessão em texto corrido; nenhum print exibe
realizado posterior a 01/10/2025 15h.

### Preparação para a banca
- **`docs/dossie-banca.md`** · dossiê v2 (100 KB). Produzido por revisão adversarial com quatro perfis de avaliador (machine learning, gestor Locaweb, metodologia acadêmica e cético), cinco auditorias de artefato e uma matriz de conformidade com as 51 exigências das três fontes oficiais. Dos 114 achados brutos, 73 foram verificados um a um contra o dado: 63 confirmados e 10 derrubados. Placar da conformidade: 17 atendidas, 21 parciais, 13 pendentes.
- Um crítico de completude revisou o próprio dossiê e apontou onde ele se contradizia; esses pontos foram corrigidos, incluindo uma resposta que estava invertida sobre a janela de antecedência do alerta.

---

## Achado que define o escopo do produto

Testado em 29/07/2026: o volume diário explica apenas **2,5%** da variação de quebras de OLA (r = 0,159; p = 0,011), medido em dias úteis. Dias de volume alto concentram cerca de 60% mais quebras em absoluto, mas a taxa de quebra é praticamente constante.

Consequência: **a previsão de volume dimensiona carga e projeta o atingimento da meta; o modelo de risco por incidente é o que responde qual incidente vai estourar.** O modelo de risco não é complemento, é a metade que fecha a proposta. Isso está declarado no slide 18 do deck e no dossiê.

---

## O que falta

Em ordem de impacto na nota:

- [ ] **Atualizar os anexos das Sprints 1 e 2 antes de enviar.** Os dois `.pptx` seguem intocados (24/04 e 22/07) e ainda declaram XGBoost para risco, tslearn/DTW e o detector de cascata. O slide 8 do deck da Sprint 3 **afirma que eles vão atualizados junto**. Se forem como estão, o próprio material se contradiz na mesa da banca.
- [ ] **Decisão a tomar sobre versionamento do dado (LGPD).** O dataset bruto está versionado e o diretório `data/` não está no `.gitignore`, então o parquet entra no próximo commit. A Sprint 4 exige repositório público. A varredura de 29/07/2026 não encontrou PII (zero e-mails, CPF, telefone ou IP; nenhuma coluna de pessoa; `Aberto por` só tem Manual e Monitoramento), então não há exposição, mas a posição formal precisa ser decidida e registrada. Ver `docs/dossie-banca.md`, seção 2.5.
- [ ] Repetir a varredura de PII no campo `Solução` (texto livre ainda não coberto).
- [ ] Referências bibliográficas: não há nenhuma em todo o material (artigo do Prophet, definição de MAE, protocolo de backtest).
- [ ] Tratamento da cauda recente da série no desenho do pipeline: o rótulo de elegibilidade depende do fechamento do incidente, então em produção os últimos dias ficam incompletos.
- [ ] **Print atualizado do quadro do Trello.** O slide 9 do deck conta a gestão por marcos datados, mas não leva imagem do quadro: o board mostra os cartões da Sprint 2. O espaço no slide está reservado.
- [ ] **Publicar a aplicação, ou assumir o risco.** A moldura de navegador dos slides de print exibe `cronos-locaweb.onrender.com`, a pedido do Igor, para a tela aparecer como se estivesse no ar. Hoje o endereço não responde.
- [ ] **Destilar em notebook os três números do descarte da cascata** (87% de quebras isoladas, escalada de 21% contra ~60% do acaso). Estão no deck e nos documentos desde julho, mas o código que os produziu ficou em laboratório não versionado. Alternativa: reescrever o slide 7 sem afirmar número.

---

---

## Plano até o fim da Sprint 3 e a integração com Django

Traçado em 30/07/2026. Entrega da Sprint 3 em **23/08** (24 dias) e da Sprint 4 em **08/09**.

### Fase 1 · Fechar o modelo de risco (2 a 3 dias)

| # | Item | Situação |
|---|---|---|
| 1.1 | Treino, baselines e avaliação | ✅ feito no lab |
| 1.2 | Quatro gráficos de avaliação | ✅ em `notebooks/figures/04_risco_ola/` |
| 1.3 | Explicabilidade: contribuição por incidente, direto dos pesos | ⏳ próximo |
| 1.4 | Notebook oficial `04_risco_ola.ipynb`, executado e comitado | ⏳ |

### Fase 2 · Fechar as exigências analíticas que faltam (3 a 4 dias)

| # | Item | Por que |
|---|---|---|
| 2.1 | **Agrupar causas recorrentes** (categoria, código de fechamento, descrição) | Exigência 3 do desafio, nunca feita |
| 2.2 | **Projeção de atingimento do KPI**: volume previsto × risco por incidente, comparado à meta anual | Exigência oficial de visualização, hoje pendente |
| 2.3 | Formalizar a detecção de incidentes recorrentes em notebook | Exigência 1, hoje só medido fora de notebook |

### Fase 3 · Produto e entregáveis da Sprint 3 (5 a 7 dias)

| # | Item |
|---|---|
| 3.1 | Telas alimentadas com a saída real dos dois modelos |
| 3.2 | Tela de detalhe do incidente com o texto do motivo (evidência histórica quando houver grupo, contribuição das características quando for caso inédito) |
| 3.3 | Slides do risco, das causas recorrentes e da projeção, na linguagem visual já definida |
| 3.4 | Montagem do PPT no template oficial (14 blocos), incluindo gestão ágil e Kanban |
| 3.5 | Anexar os `.pptx` atualizados das Sprints 1 e 2, como o template exige |

### Fase 4 · Django integrado (a começar antes do fim da Sprint 3)

O template chama o bloco de "versão preliminar do MVP baseado na arquitetura", e a Sprint 4 vem 16 dias depois, com peso em código-fonte e repositório público. Deixar o Django inteiro para a Sprint 4 é risco de cronograma.

| # | Item |
|---|---|
| 4.1 | Esqueleto Django: projeto, app, settings, Docker |
| 4.2 | Camada de serviço que carrega os modelos treinados e serve previsão de volume e fila de risco |
| 4.3 | Views e templates reaproveitando o HTML dos protótipos |
| 4.4 | Rotina de re-treino semanal, com a janela consolidada resolvendo a cauda recente da série |
| 4.5 | Texto do morning briefing pela Claude API, a partir dos números dos modelos |

### Decisões pendentes de definição

- **Versionamento do dado e LGPD**: o dataset bruto está versionado e `data/` não está no `.gitignore`. A Sprint 4 exige repositório público. A varredura de 29/07 não encontrou dado pessoal, mas a posição precisa ser decidida.
- **Calibração da faixa de risco alto**: descartada por ora. O desvio está em 31 incidentes e ajustar sobre esse volume seria ajustar ruído. Limitação declarada.

## Decisões técnicas em vigor

Detalhamento em `context/decisoes-tecnicas.md` e nas regras críticas do `CLAUDE.md`.

- Previsão de volume com **Prophet**; risco de OLA com **regressão logística** (XGBoost apenas como baseline de comparação).
- Proibidos: ARIMA e SARIMA, Streamlit. Django é mandatório, entrega via Docker, solução agnóstica de provedor de nuvem.
- Alvo dos modelos: a **série elegível ao KPI**, não o volume bruto. Treino apenas em 2025 (98% dos casos elegíveis estão nesse ano).
- Diferenciais do produto: **morning briefing** e **score de saúde por produto**.
- Testados e descartados, com número: detector de cascata, padrão de acúmulo, clusterização por DTW, sugestão de realocação de equipe.

---

## Pontos de atenção

- Do feedback da Sprint 1: toda menção de impacto ou benefício precisa vir com número ou gráfico.
- Da mentoria com a Locaweb: dashboard próximo do estilo TIM e Unifique, dado quase em tempo real, duas a três abas no máximo.
- Resolvido em 29/07/2026: as cinco telas da Sprint 2 (`dashboard`, `morning-brief`, `previsao`, `saude-produto`, `cascata`) ainda apresentavam o detector de cascata como funcionalidade viva, inclusive com link de menu e menção a classificador XGBoost. Receberam uma tarja fixa de **referência histórica** explicando que a cascata foi descartada na Sprint 3 e que o protótipo atual é o `mvp-mockup.html`. O `mvp-mockup.html` também foi corrigido: dizia "Prophet + XGBoost" na previsão de volume, quando o XGBoost é apenas baseline de comparação do modelo de risco.

## Bloqueios

- Nenhum no momento.

# Protótipos da abertura do deck · Sprint 3

Onze slides, três versões cada. O Igor navega e escolhe uma por slide.

## Contrato de saída, sem exceção

- Um arquivo por versão: `NN-nome-A.html`, `NN-nome-B.html`, `NN-nome-C.html`, nesta pasta
  (`prototipos/slides/mvp/abertura/`).
- Cabeça do arquivo, exatamente assim (troque só o `<title>`):

      <!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
      <title>03 Contexto · A</title>
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
      <link rel="stylesheet" href="base.css">
      <style>/* só o CSS específico deste slide */</style>
      </head><body>
      <section class="slide light">…</section>
      </body></html>

- O slide é 1600 por 900. O `base.css` já traz `.slide`, `.hd`, `.body`, `.ft`, `.eb`,
  `.tt`, `.lead`, `.stats` com `.st`, `.pts` com `.pt`, `.tw` com `table`, `.vp`, e os temas
  `.light` e `.dark`. **Leia o base.css antes de escrever CSS**: metade do que você precisa
  já existe.
- Topo e rodapé em todo slide. Copie o padrão de um slide existente em
  `prototipos/slides/mvp/deck/` (por exemplo `d05m.html`), incluindo o SVG da marca.
- Rodapé esquerdo: `Cronos · Super Data Bros · 2TSCOA`. Direito:
  `Challenge FIAP 2026 com Locaweb`.
- Localizador no canto superior direito, classe `.tag`: `Template · slide N`.

## Referência visual obrigatória

**Antes de escrever, abra e leia três slides do bloco de modelagem**, que é a linguagem que
o Igor aprovou: `prototipos/slides/mvp/deck/d05m.html`, `d24a.html` e `d31a.html`. Repare
em como usam número grande rotulado, cartão branco sobre fundo claro com gradiente azul, e
uma frase curta de veredito ao lado do dado.

## Regras que reprovam o slide se violadas

1. **Fonte Outfit.** Nunca Inter, nunca system-ui como escolha.
2. **Um azul só** (`--accent`, #2563EB). Vermelho apenas para perigo real, verde para
   resultado bom, âmbar para atenção. Sem roxo, sem lilás, sem brilho neon, sem preto puro.
3. **Proibido cartão com barra colorida grossa na esquerda.** O Igor odeia.
4. **Proibido travessão em texto corrido.** Use vírgula, ponto ou dois-pontos.
5. **Proibida regra de três** (três adjetivos ou três itens paralelos só para soar completo)
   e paralelismo de slogan do tipo "não é X, é Y". São os tiques que reprovaram a versão
   anterior.
6. **Proibido o molde: título, linha de apoio, e três cartões iguais com cabeçalho em
   negrito seguido de parágrafo.** Foi exatamente isso que o Igor rejeitou. Se o seu slide
   se parece com isso, refaça.
7. **P2 e P3 sempre juntos.** Todo bloco, gráfico, tabela ou número que fala de P3 mostra P2
   do lado, e vice-versa.
8. **Todo número vem rotulado** e com cor semântica. Números em coluna usam a classe `.num`,
   que já aplica `tabular-nums`.
9. **Nenhum número que não esteja na folha de fatos abaixo.** Se precisar de um que não
   está, escreva `[verificar]` no lugar e reporte no seu relatório final. Não estime, não
   arredonde de cabeça, não invente.
10. **As três versões mudam a composição**, não a cor. Uma versão que só troca o tom do
    fundo é a mesma versão.
11. Sem emoji. Sem ícone decorativo que não signifique nada.

## Folha de fatos · todo número permitido

### Base e KPI

- Dataset: **122.543** incidentes, **19** colunas, jan/2023 a dez/2025.
- Elegíveis ao KPI, pelo campo oficial `Entrou para KPI?`: **25.600**, ou 21% da base.
- Filtrar só por `Incidente Pai` vazio devolveria **107.416** (88% da base). É o erro clássico.
- Violações de OLA: **248** em toda a base (0,97%); **238** em 2025; **188** na janela de
  jan a set/2025, que é 0,94% de 19.973 incidentes.
- Prazo de OLA: **P2 em 4 horas**, **P3 em 12 horas**.
- Elegíveis por ano: **87** em 2023, **357** em 2024, **25.156** em 2025.
- Distribuição do volume: P4 52,9%, P3 34,1%, P2 12,8%. **65,6%** fecham como Sem
  Intervenção. **85,1%** vêm de Monitoramento.

### A régua da meta, do dicionário oficial da Locaweb

Violações de OLA no ano e a nota que cada faixa vale:

| Nota | P2 | P3 |
|---|---|---|
| 150% | até 30 | até 200 |
| 125% | 31 a 35 | 201 a 230 |
| 100% | 36 a 39 | 231 a 263 |
| 75% | 40 a 45 | 264 a 290 |
| 50% | 46 a 53 | 291 a 320 |
| 0% | 54 ou mais | 321 ou mais |

- 2025 fechou: **P2 com 42** violações, nota 75%. **P3 com 196**, nota 150%.
- Acumulado mês a mês em 2025, **P2**: 4, 8, 11, 13, 19, 22, 28, 31, 33, 35, 41, 42.
- Acumulado mês a mês em 2025, **P3**: 19, 40, 56, 66, 81, 109, 132, 146, 155, 164, 179, 196.
- Leitura central: o P2 sai de **35 em outubro para 41 em novembro** e atravessa duas faixas
  de uma vez, caindo de 125% para 75%. Seis violações num mês custaram 50 pontos de nota.

### Anomalia de setembro de 2025, a análise de causa raiz

| Dimensão | Agosto | Setembro |
|---|---|---|
| Volume total | 3.996 | 21.561 |
| Origem Monitoramento | 2.404 | 20.008 |
| Origem Manual | 1.592 | 1.553 |
| Status Sem Intervenção | 47 | 17.838 |
| Itens de configuração vistos pela primeira vez | 458 | 1.693 |

- Descrição mais frequente em setembro: `Problem: Check Application Monitoring`, 6.590 vezes.
- Volume mensal: 2023 cerca de 10 por mês, 2024 cerca de 52, jan a ago/2025 cerca de 3,5 mil,
  set 21,6 mil, out 23,0 mil, nov 21,5 mil, dez 27,3 mil.
- Efeito no KPI: a série elegível atravessa intacta, **2.330 em agosto para 2.324 em setembro**.
- Causa concluída: expansão do monitoramento automático sobre ativos que antes não eram
  monitorados. Mais eventos capturados, não mais falhas na operação.

### Por que a ferramenta atual não resolve

- Ordenar a fila por prioridade, o padrão de qualquer ITSM, tem ROC AUC de **0,4693**,
  abaixo dos **0,5063** de uma fila sorteada.
- Nas 50 primeiras posições dessa fila há **1** violação. Na fila do modelo, **15**.
- Melhor regra simples, ativo crônico e time: ROC AUC 0,7945 e **6** violações no top 50.
- Volume diário explica só **2,5%** da variação de violações, com r de 0,159 e p de 0,011.
  Taxa de violação por quartil de volume: 0,8%, 0,9%, 1,0%, 0,7%.

### Concentração do risco

- Team14: **75,7%** do volume total, 95,5% de origem automática, 81,5% Sem Intervenção,
  e **10** violações.
- Team11: **46%** das violações com **8%** do volume.
- Cuidado: são participações medidas em bases diferentes. Apresente lado a lado, nunca como
  múltiplo do tipo "19 vezes".

### Modelos entregues

- **Prophet**, volume diário D+1 a D+7, duas séries. Erro médio em rolling backtest de
  **11,8 por dia no P3** e **4,2 no P2**. Melhor baseline: 11,3 no P3, então **o baseline
  vence por 4,5%**; 4,9 no P2, então o ganho é de **15%**. Cobertura da banda de 80%:
  **84,8%** no P2 e **60,9%** no P3.
- **Regressão logística** para risco por incidente, 10 características disponíveis na
  abertura, 136 colunas depois da codificação. ROC AUC **0,8693**, PR-AUC **0,2958**, que é
  31 vezes a taxa da base. Os **20%** de maior risco concentram **72%** das violações.
  Prevê **48,1** violações onde houve 50.
- XGBoost como baseline: ROC AUC 0,8679 e PR-AUC 0,2526. Com balanceamento prevê **1.007**
  violações onde houve 50.
- **Projeção do KPI** em três parcelas: o que já tem desfecho é contagem, o que está aberto
  vai pelo modelo de risco, o que ainda não entrou vai pelo Prophet. Validada em 5 datas nas
  2 prioridades: a faixa conteve o real em **7 de 10**, a situação da meta foi acertada em
  **7 de 10** (5 de 5 no P2, 2 de 5 no P3), erro máximo de **15,0%**, e **nenhum** erro no
  sentido otimista.
- **Saúde por produto**: **15** produtos acima de 200 incidentes, cobrindo **94%** do volume.
  Pior nota **lvps com 21,3**, melhor **lcho com 69,3**. **5** produtos abaixo de 40. Quatro
  em risco latente: lemg, lcsi, lcsp, lcem.
- **Causas**: problema inédito viola **1,46%**, rotina de 20 ou mais ocorrências viola
  **0,31%**, queda de **4,7 vezes**. Código Outro é **8,0%** do volume e **22,9%** das
  violações. Falha de Hardware é **0,4%** do volume com taxa de **8,24%**, 8,75 vezes a média.

### Ideias testadas e descartadas

- Detector de cascata: **87%** das violações são de incidentes isolados, e a taxa de escalada
  observada é **21%** contra os cerca de 60% que o acaso produziria. Se usar, marque como
  exploração: não há notebook versionado que reproduza esses três números.
- Clusterização por DTW: silhueta **0,13**, ausência de estrutura.
- Acúmulo de backlog, hipótese do mentor: correlação **−0,139**, sinal contrário ao esperado.
- Realocação de equipe: **não pôde ser testada**, porque o dataset não tem capacidade nem
  turno das equipes. Nunca escreva que foi refutada.

### Arquitetura

- Stack com versão: pandas 2.2.3, openpyxl 3.1.5, pyarrow 25.0, holidays 0.97, Prophet 1.3.0,
  cmdstanpy 1.3.0, scikit-learn 1.6.1, XGBoost 3.0.2, scipy 1.18, statsmodels 0.14.6,
  matplotlib 3.10, seaborn 0.13, plotly 6.0, Django 6.1, gunicorn 23.0, whitenoise 6.9,
  Docker sobre `python:3.13-slim`.
- O pacote que a aplicação lê tem **350 kB**, carregado uma vez por processo. São três
  arquivos: `painel.json` (85 kB), `dias.json` (24 kB) e `fila.parquet` (241 kB).
  `fila_curvas.json` está na pasta mas nenhum código da aplicação o lê.
- Seis abas: `/`, `/previsao/`, `/projecao/`, `/fila/`, `/saude/`, `/causas/`. Mais quatro
  rotas de detalhe que abrem como modal, e um índice de busca.
- A aplicação simula um relógio parado em **01/10/2025 às 15h**.
- Os modelos treinam nos notebooks e gravam Parquet. O contêiner só lê.
- Varredura de dado pessoal: zero e-mail, CPF, telefone ou endereço IP. Nenhuma coluna
  identifica pessoa. O campo de origem só tem Manual e Monitoramento.
- Fonte externa única: a biblioteca `holidays` para feriados nacionais, que o dataset não traz.

### Equipe e sprints

- Ana Beatriz Costa de Oliveira, **RM561310**. Hygor Abrantes, **RM565063**. Igor Vignola,
  **RM561428**. Turma **2TSCOA**, Tecnólogo em Data Science.
- Mentor: **Douglas Gouveia**, Gerente Executivo de Operações da Locaweb.
- Sprint 1 entregue em 27/04/2026, nota **5,00**. O professor pediu ilustrar o impacto com
  número e gráfico.
- Sprint 2 entregue em 24/05/2026, nota **5,00**. O professor pediu um slide explícito de
  gestão ágil.
- Sprint 3 entrega em 23/08/2026. Sprint 4 em 08/09/2026.
- Marcos da Sprint 3: 20 e 21/07 alvo e escopo de modelagem; 29/07 verificações de robustez e
  dossiê de banca; 03 e 04/08 modelo de risco medido e notebooks 04, 05 e 06; 05/08 saúde por
  produto; 11 a 14/08 auditoria dos números e reconstrução das seis abas; 17/08 auditoria
  visual com 41 capturas e 32 achados corrigidos.

## O que fazer se faltar dado

Alguns slides pedem coisa que ainda não existe. Não invente e não deixe o slide quebrado:

- **Fotos da equipe**: o Igor vai mandar. Deixe um círculo de 96px com as iniciais da pessoa,
  em fundo neutro, pronto para receber a imagem.
- **Print do quadro do Trello**: ainda não existe. Deixe uma área com proporção 16 por 9
  marcada com borda tracejada fina e o rótulo `Quadro do projeto no Trello`, para receber a
  captura depois.
- **Logotipo do projeto**: use o SVG da marca do Cronos que está nos slides do deck, a linha
  de tendência subindo até o alvo azul.

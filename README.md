# Cronos

Inteligência preditiva para incidentes operacionais da Locaweb.

**Challenge FIAP 2026 · Equipe Super Data Bros · Turma 2TSCOA**

Cronos transforma o histórico operacional da Locaweb em previsão. A base tem 122.543
incidentes registrados entre janeiro de 2023 e dezembro de 2025, dos quais 25.600 são
elegíveis ao KPI de OLA. Sobre ela, o projeto estima quantos incidentes chegam nos
próximos dias e qual dos incidentes abertos tem maior chance de estourar o prazo de OLA.
A saída é um painel operacional que projeta o atingimento das metas anuais, ordena a fila
de atendimento por risco e explica cada número que exibe.

Domínio: AIOps, previsão de incidentes e tendências operacionais com aprendizado de
máquina.

---

## O achado que define o escopo

O volume diário de incidentes explica **2,5% da variação no número de quebras de OLA**
(r = 0,159; p = 0,011, medido em dias úteis de 2025). Dias de volume alto concentram cerca
de 60% mais quebras em valor absoluto, mas a taxa de quebra por incidente é praticamente
constante, em torno de 0,94%.

A consequência define o produto: prever volume não é prever quebra. São dois modelos com
funções distintas. A previsão de volume dimensiona a carga do dia e projeta o atingimento
da meta anual. O modelo de risco por incidente responde qual caso vai estourar. Nenhum dos
dois substitui o outro.

---

## Os dois modelos

|  | Modelo 1 · volume diário | Modelo 2 · risco de OLA |
|---|---|---|
| Notebook | `03_previsao_volume.ipynb` | `04_risco_ola.ipynb` |
| Algoritmo | Prophet | Regressão logística |
| Alvo | incidentes elegíveis por dia, separados por prioridade | probabilidade de o incidente estourar o OLA |
| Treino | 2025, sazonalidade semanal ligada e anual desligada, feriados nacionais do Brasil | apenas informação disponível no instante da abertura, corte temporal em 01/10/2025 |
| Desempenho | MAE de D+1 a D+7 de 4 incidentes por dia no P2 e 11 por dia no P3 | ROC AUC 0,869 e PR-AUC 0,296 |
| Baseline comparado | série sazonal simples | XGBoost, com ROC AUC 0,868 e PR-AUC 0,253 |

### Por que a regressão logística ficou no lugar do XGBoost

O empate em ROC AUC (0,869 contra 0,868) desempata pelo PR-AUC, que é a métrica adequada
a evento raro: 0,296 contra 0,253, uma vantagem de 17% para a logística. Ela também mantém
a calibração, prevendo 48,1 quebras onde houve 50, enquanto o XGBoost com
`scale_pos_weight` prevê 1.007 e inviabiliza a projeção do KPI. E é explicável por
construção: como o modelo é linear, a contribuição de cada coluna é o peso multiplicado
pela diferença entre o valor e a média do treino, e a soma das contribuições mais o
intercepto devolve o logito. É essa decomposição que a aplicação exibe caso a caso, e
`scripts/gera_fila_pontuada.py` confere a reconstrução antes de gravar o arquivo.

### Limitações declaradas

A banda de 80% do Prophet cobre de 86% a 88% dos dias no P2 e de 59% a 61% no P3, ou seja,
o P3 fica subcoberto e o P2 dentro do esperado. A faixa de risco alto do modelo 2 não foi
calibrada: o desvio
está concentrado em 31 incidentes, e ajustar sobre esse volume seria ajustar ruído. O
rótulo de elegibilidade ao KPI depende do fechamento do incidente, então em produção os
últimos dias da série chegam incompletos.

---

## Testado e descartado, com número

Três hipóteses saíram do escopo depois de serem medidas. Ficam registradas porque o
descarte também é resultado.

- **Detector de cascata.** A escalada foi refutada: 87% das quebras de OLA vêm de
  incidentes isolados, e a taxa de escalada observada é de 21% contra cerca de 60%
  esperados do acaso.
- **Padrão de acúmulo.** A correlação entre backlog diário e quebras de OLA é de
  r = -0,139 em dias úteis, sinal oposto ao da hipótese.
- **Clusterização de séries por DTW.** O `TimeSeriesKMeans` com métrica DTW produziu
  silhueta em torno de 0,13, o que indica ausência de grupos reais. A exigência de
  classificação do desafio é atendida pelo classificador de risco de OLA.

---

## A aplicação

Django, seis abas, sem banco de dados e sem login. A aplicação apenas lê os arquivos que
os notebooks geram, o que mantém a imagem pequena e independente de provedor de nuvem.

A aplicação simula um relógio parado em **01/10/2025 às 15h**. Ela mostra o histórico até
30/09, o dia corrente até as 15h e as previsões para frente, e nunca exibe resultado
realizado posterior a esse instante. A avaliação dos modelos (cobertura da banda, backtest,
ganho da fila sobre o acaso) vive nos notebooks e no material de apresentação, onde a
pergunta é se o modelo funciona e o período de teste inteiro é legítimo.

| Rota | Aba | O que mostra |
|---|---|---|
| `/` | Panorama | resumo do dia, resumo diário automático e a chegada de incidentes hora a hora por prioridade |
| `/previsao/` | Previsão | série prevista com banda, sazonalidade semanal e o erro do modelo medido contra si mesmo |
| `/projecao/` | Projeção | atingimento das metas anuais de P2 e P3 contra as faixas oficiais do KPI |
| `/fila/` | Fila | incidentes abertos ordenados por risco, com a decomposição do escore de cada um |
| `/saude/` | Saúde | nota de 0 a 100 por produto, com ranking, tendência e componentes da nota |
| `/causas/` | Causas | agrupamento de causas e de incidentes recorrentes |

Toda tela que trata de P3 mostra o P2 ao lado, com o mesmo peso: as duas prioridades entram
no KPI e cada uma tem meta própria.

---

## Como rodar

### Docker, que é a rota da entrega

O contexto de build é a **raiz do repositório**, porque a imagem precisa de `webapp/` e de
`data/app/` ao mesmo tempo.

```bash
docker build -f webapp/Dockerfile -t cronos .
docker run --rm -p 8000:8000 cronos
```

Depois, abrir `http://localhost:8000`.

A imagem não carrega Prophet, scikit-learn nem XGBoost. Esses pacotes rodam nos notebooks,
gravam os arquivos de saída, e o contêiner apenas lê o pacote agregado de `data/app/`, que
tem cerca de 295 kB. É isso que permite a entrega rodar em plano gratuito.

Variáveis de ambiente reconhecidas: `PORT`, `CRONOS_SECRET_KEY`, `CRONOS_DEBUG`,
`CRONOS_HOSTS`, `CRONOS_ORIGENS` e `CRONOS_DADOS`.

### Local, sem Docker

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r webapp/requirements.txt    # Windows
.venv/bin/python     -m pip install -r webapp/requirements.txt    # Linux e macOS
.venv/Scripts/python webapp/manage.py runserver
```

### Publicar em um provedor de contêiner

`render.yaml` na raiz descreve o serviço para quem usa Render (Dashboard, New, Blueprint,
escolher este repositório). É só um descritor de conveniência: a imagem é a mesma em
qualquer provedor que aceite um contêiner escutando `$PORT`, e nada na solução amarra a um
fornecedor específico. O `.dockerignore` da raiz mantém o contexto de build enxuto, já que
o Docker lê o `.dockerignore` do diretório do contexto e não o do diretório do Dockerfile.

### Os dois arquivos de dependência

São dois arquivos de dependência, com propósitos diferentes. `webapp/requirements.txt` tem
o mínimo para a aplicação servir (Django, pandas, pyarrow, gunicorn, whitenoise).
`requirements.txt` na raiz tem o ambiente de análise e modelagem (pandas, Prophet,
scikit-learn, XGBoost, matplotlib, SHAP), necessário só para reexecutar os notebooks.
Python testado: 3.13.2.

### Reproduzir a análise do zero

O dataset oficial da Locaweb fica em `assets/Materal LocalWeb/LW-DATASET.xlsx` (o nome da
pasta tem o typo de origem). A ordem é:

1. `notebooks/02_base_kpi.ipynb` carrega o dataset, tipa as colunas, aplica o filtro de
   elegibilidade pelo campo oficial `Entrou para KPI?` e grava
   `data/interim/incidentes_kpi.parquet`. Tem asserts de invariante para os 122.543
   registros totais e os 25.600 elegíveis.
2. `notebooks/01_eda.ipynb` e os notebooks `03` a `07` produzem as análises e as figuras em
   `notebooks/figures/`.
3. `scripts/gera_previsao_diaria.py` e `scripts/gera_fila_pontuada.py` reproduzem os dois
   modelos fora do notebook e gravam os parquets que a aplicação consome.
4. `scripts/gera_dados_app.py` agrega tudo em `data/app/`, que é o que o contêiner lê.

---

## Estrutura de pastas

```
Challenge-LocaWeb/
├── notebooks/            análise e modelagem, sete notebooks executados
│   └── figures/          figuras exportadas, uma pasta por notebook
├── webapp/               aplicação Django
│   ├── cronos/           configuração e WSGI
│   ├── painel/           views, serviços, gráficos e templates das seis abas
│   └── Dockerfile        imagem da entrega
├── scripts/              pipeline de dados, geração dos decks e captura de telas
│   └── direcoes/         fonte única do CSS e dos ícones, compartilhada com o Django
├── data/
│   ├── interim/          bases tratadas pelos notebooks
│   └── app/              pacote agregado que a aplicação lê em produção
├── prototipos/           protótipos HTML das telas e os slides dos decks
├── docs/                 documentação de trabalho e dossiê de banca
├── context/              contexto persistente do projeto
├── brand/                identidade visual
├── assets/               material oficial da FIAP e da Locaweb, somente leitura
├── sprints/              entregáveis de cada sprint
├── render.yaml           descritor de publicação em provedor de contêiner
└── .dockerignore         contexto de build, lido da raiz
```

---

## Dados

O dataset é fornecido pela Locaweb e chega anonimizado na origem: os códigos de produto e
de categoria são opacos (`lvps`, `cat71`), e não há coluna que identifique pessoa. O campo
`Aberto por` distingue apenas registro manual de monitoramento automático. As bases
tratadas em `data/` são derivadas desse arquivo e ficam versionadas para tornar a análise
reproduzível.

O filtro de elegibilidade ao KPI usa o campo oficial `Entrou para KPI?`, que já codifica as
três regras juntas: prioridade 1, 2 ou 3, campo `Incidente Pai` vazio e status diferente de
"Sem Intervenção". O resultado são 25.600 incidentes, 21% da base.

---

## Equipe

| RM | Nome |
|---|---|
| 561310 | Ana Beatriz Costa de Oliveira |
| 565063 | Hygor Abrantes |
| 561428 | Igor Vignola |

Mentor da Locaweb: Douglas Gouveia, Gerente Executivo de Operações.

---

## Entregas

| Sprint | Tema | Data | Arquivo em `sprints/` |
|---|---|---|---|
| 1 | Ideação | 27/04/2026 | `EC_Sprint_1_2TSCOA_ideacaoprojeto_Cronos_SuperDataBros.pptx` |
| 2 | Arquitetura | 24/05/2026 | `EC_Sprint_2_2TSCOA_arqsolucao_Cronos_SuperDataBros.pptx` |
| 3 | MVP preliminar | 23/08/2026 | `EC_Sprint_3_2TSCOA_Evidencias_Construcao_Cronos_SuperDataBros.pptx` |
| 4 | Solução final | 08/09/2026 | `EC_Sprint_4_2TSCOA_SolucaoFinal_Cronos_SuperDataBros.pptx` |

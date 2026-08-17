---
name: notebook-style
description: Estrutura e padrão obrigatório dos notebooks Jupyter do projeto Cronos. SEMPRE consulte antes de criar ou editar arquivos .ipynb. Use quando o usuário mencionar notebook, jupyter, .ipynb, AED, EDA, análise exploratória, modelagem, features, clusterização, SHAP, ou qualquer trabalho de análise de dados em Python. Use também ao gerar o primeiro notebook de uma nova etapa (01_eda, 02_base_kpi, etc.).
---

# Padrão de Notebooks — Cronos

Os sete notebooks do projeto seguem este padrão. Ele foi consolidado em 17/08/2026, revisando
`01` a `07` um a um; os notebooks existentes são a referência viva. Quando este documento e um
notebook divergirem, o notebook manda — e atualize este arquivo.

## Convenção de nomenclatura

```
notebooks/
├── 01_eda.ipynb                 ← análise exploratória
├── 02_base_kpi.ipynb            ← base compartilhada (carga, tipagem, filtro de KPI)
├── 03_previsao_volume.ipynb     ← Prophet, volume D+1 a D+7, P2 e P3
├── 04_risco_ola.ipynb           ← regressão logística por incidente
├── 05_causas_recorrentes.ipynb  ← causas, recorrência, familiaridade
├── 06_projecao_kpi.ipynb        ← combinação dos dois modelos contra as metas
└── 07_saude_produto.ipynb       ← nota 0-100 por produto
```

Prefixo numérico: ordena no explorador e indica a ordem de execução.

---

## Registro de escrita (a regra que mais se descumpre)

O texto do notebook descreve **o que a célula calcula** e **o que o número mostra**. Ele não
descreve o notebook, não narra a jornada e não antecipa capítulos.

### Proibido

| Padrão | Exemplo do que sair | O que entra no lugar |
|---|---|---|
| Falar de seções | "qualquer coluna derivada fica para a seção 3" | descrever o que a célula faz |
| Índice antecipado | tabela "Sumário" no cabeçalho | os próprios títulos de seção |
| Referência para frente | "a causa é investigada na 4.2" | uma frase que emenda no próximo passo |
| Rótulos em negrito | `**Pergunta:**` / `**Achado:**` | texto corrido |
| Título que entrega a resposta | "4.2 Anomalia de setembro **e sua causa**" | "4.2 Mudança de patamar em setembro de 2025" |
| Anúncio do que vem | "três verificações ajudam a identificar" | fazer a verificação |
| Primeira pessoa narrativa | "vamos ver", "vale olhar", "a gente" | frase declarativa |
| Meta-comentário do entregável | "registramos o resultado negativo com número" | o resultado, com número |
| Bloco de retomada | "Principais achados" numerando o que já foi dito | conclusão curta em prosa |
| Roadmap | "Próximos passos" com `- [ ]` | nada; roadmap vive em `docs/` |

Referência a **outro notebook** é permitida quando é dependência real ("base gravada pelo
notebook 02", "o gradiente medido no notebook 05"). Referência a **seção do próprio notebook** só
quando aponta para onde uma medição específica está, nunca como fio narrativo.

### Formato dos blocos

**Antes do código:** uma a três frases dizendo o que vai ser calculado e por quê. Quando houver
decisão metodológica (corte de data, limite de volume, escolha de baseline), ela entra aqui.

**Depois do código:** parágrafo curto lendo o número que saiu. Tamanho variável — alguns têm duas
linhas, outros seis. Blocos todos do mesmo tamanho denunciam texto gerado.

**Negrito:** um destaque por bloco de leitura, na afirmação que decide alguma coisa. Não em rótulo.

**Sem travessão (—).** Vírgula, dois-pontos ou ponto. Aspas retas, nunca curvas.

**"X, e não Y"** no máximo uma vez por notebook. É o padrão de escrita de IA que mais aparece.

---

## Estrutura obrigatória

### Célula 1 — cabeçalho (markdown)

```markdown
# NN · Título em caixa baixa

**Projeto:** Cronos · Challenge FIAP 2026 com Locaweb
**Autores:** Ana Beatriz Costa de Oliveira · Hygor Abrantes · Igor Vignola
**Criado em:** DD/MM/AAAA · **Atualizado em:** DD/MM/AAAA

[2 a 4 linhas: o que o notebook produz e por quê. Se houver uma restrição que define o desenho
todo, ela vem aqui.]

**Janela:** [só se o notebook tiver recorte de data; ver "Corte de data" abaixo]

**Entrada:** `caminho/do/arquivo`, gerado pelo notebook NN.
**Saída:** figuras em `notebooks/figures/NN_nome/` e `data/interim/...`.
**Bibliotecas:** pandas, numpy, ... (Python 3.11+).
```

Sem seção "Sumário". Sem "Objetivo" como título.

### Célula 2 — imports (código)

Stdlib, third-party e local, nessa ordem, com linha em branco entre os blocos. **Todo import fica
aqui**, inclusive os usados uma vez no meio do notebook.

### Seções

```
## 1. Setup            caminhos, estilo, semente, funções de formatação
## 2. Carga dos dados  leitura pura, sem transformação
## 3. Visão geral      estrutura, tipos, completude — com leitura dos outputs
## 4. Análise          subdividida em 4.1, 4.2, ...
## 5. Conclusão        prosa curta
```

Notebooks que preparam base (`02`) ou que têm pergunta de desenho antes da construção (`07`)
podem trocar a seção 3 pelo que couber. A numeração continua sequencial.

### Seção 5 — conclusão

Prosa corrida, tipicamente 3 a 5 parágrafos. Diz o que ficou estabelecido, com os números, e o que
o dado **não** permite afirmar. Não numera achados já apresentados, não lista próximos passos, não
abre "pontos abertos" como seção separada — a limitação entra na frase que a produz.

---

## Regras de dado e verificação

### 1. Todo número no texto sai de uma célula

Se o texto afirma "72% das quebras", alguma célula precisa imprimir esse 72%. Percentual derivado
por multiplicação mental na cabeça de quem escreve é a origem mais comum de erro no projeto: a
revisão de 17/08/2026 achou 16 números errados no `05` e 8 no `07`, todos assim.

Ao mudar um filtro ou recorte, **releia todo o markdown do notebook**. O texto não acompanha o
código sozinho.

### 2. Métrica não-determinística: fixe a semente, e só reporte faixa se não der

O ponto previsto do Prophet (`yhat`) é determinístico. A banda (`yhat_lower`, `yhat_upper`) vem de
amostragem posterior e usa o RNG global do numpy:

```python
SEMENTE = 42

def prever(modelo, datas):
    """Previsão com a banda reproduzível."""
    np.random.seed(SEMENTE)          # a banda vem de amostragem posterior
    return modelo.predict(pd.DataFrame({'ds': datas}))
```

`random_state=SEMENTE` em scikit-learn e xgboost. Só reporte faixa quando a variação sobreviver à
semente, e diga por quê.

### 3. Corte de data quando a saída alimenta a aplicação

O Django simula o relógio parado em **01/10/2025 às 15h**. Notebook que grava parquet consumido
pela aplicação recorta a janela e carrega a janela no dado:

```python
CORTE = pd.Timestamp('2025-10-01')
df_ano = df[(df['ano'] == 2025) & (df['dia'] < CORTE)].copy()
saida.attrs['janela'] = f'2025-01-01 a {(CORTE - pd.Timedelta(days=1)).date()}'
```

Contagens derivadas (frequência de problema, "é inédito") também são calculadas **dentro** da
janela, senão usam o futuro para decidir o presente.

### 4. Séries diárias sempre reindexadas no calendário

```python
calendario = pd.date_range('2025-01-01', '2025-12-31', freq='D')
serie = df.groupby('dia').size().reindex(calendario, fill_value=0)
```

Sem isso a média divide por dias observados e não por dias do período. Funciona por sorte enquanto
todos os dias tiverem registro, e quebra em silêncio no primeiro dia vazio.

### 5. P2 e P3 sempre lado a lado

Toda tabela, gráfico ou número que fala de uma prioridade mostra a outra. As duas entram no KPI com
metas próprias, e a taxa agregada não descreve nenhuma das duas.

### 6. Invariantes com `assert`

```python
assert len(df_raw) == 122_543, f'esperadas 122.543 linhas, lidas {len(df_raw):,}'
assert soma['size'].sum() == len(df_ano), 'as parcelas não somam o total'
```

Melhor falhar na célula do que propagar em silêncio.

### 7. Gravou parquet, releia e confira

```python
tabela.to_parquet(destino, index=False)
conferencia = pd.read_parquet(destino)
assert conferencia.shape == tabela.shape
assert (conferencia.dtypes == tabela.dtypes).all()
```

---

## Convenções de código

- **DataFrames com prefixo `df_`**: `df_kpi`, `df_treino`, `df_violacoes`. Nunca `df2`, `data`.
- **Filtro com nome semântico**, um por linha, com comentário dizendo por que aquele filtro.
- **Comentário explica o porquê, não o quê.** `# Confirmado pela Locaweb: só incidente pai entra
  no KPI` vale; `# filtra incidentes pai` não.
- **Sem variável `_temporaria` no escopo do módulo.** Use nome normal.
- **f-string sem aspas aninhadas do mesmo tipo** — só compila em Python 3.12+, e o projeto declara
  3.11+. Extraia para variável antes.
- **Nada acima de 30 s sem cache** em `data/interim/`.
- **Não imprimir DataFrame gigante**: `head(20)`, `sample(50)`, nunca `df`.
- **Acentuação correta** em comentário e string, como no resto do projeto.

---

## Como executar

O kernel `python3` do venv declara `"argv": ["python", ...]` sem caminho absoluto, então ele abre o
primeiro `python` do PATH. Rodando de um shell cujo PATH acha o Python global, o notebook falha com
`ModuleNotFoundError` e, se a saída estiver canalizada, o exit code some.

```bash
cd <raiz do repo>
PATH="$(pwd)/.venv/Scripts:$PATH" ./.venv/Scripts/python.exe -m jupyter nbconvert \
  --to notebook --execute --inplace --ExecutePreprocessor.timeout=3600 \
  notebooks/NN_nome.ipynb > /tmp/exec.log 2>&1; echo "EXIT=$?"
```

**Depois de executar, confirme que executou.** Exit code 0 não basta:

```python
# comparar os outputs contra o commit anterior
old = json.loads(subprocess.run(['git','show',f'HEAD:{caminho}'], capture_output=True).stdout.decode())
new = json.load(open(caminho, encoding='utf-8'))
# nenhuma célula alterada = ou o notebook é determinístico, ou ele não rodou. Distinga pelo log.
```

---

## Antes de commitar

1. Todo número do markdown tem célula que o produz?
2. Sobrou `**Achado:**`, "Próximos passos", "Sumário", travessão, `- [ ]`?
3. Notebook executou sem erro e os outputs conferem com o texto?
4. Se gera parquet consumido pela aplicação, o parquet entra no commit junto.
5. Figuras regeradas entram junto.

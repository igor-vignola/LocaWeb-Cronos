# Plano de masterização, aba por aba

**Data:** 06/08/2026 · **Estado:** plano para aprovação, nada prototipado ainda

Cada aba é auditada em quatro colunas: o que o notebook entrega, o que a tela mostra hoje,
o que está faltando, e o que a versão masterizada precisa ter. Ao final de cada aba, o que
precisa de mockup e o que não precisa.

A régua: **tudo que construímos tem de aparecer**. Resultado que só existe em notebook é
trabalho desperdiçado na hora da banca.

---

## Aba 1 · Fila de risco

Fonte: notebook 04 e `04_fila_pontuada.parquet`.

**O que o modelo entrega**

| Entrega | Valor medido | Está na tela? |
|---|---|---|
| Ranqueamento de 5.183 casos | ROC AUC 0,874 · PR-AUC 0,286 | ❌ nenhuma métrica aparece |
| Concentração da captura | 50 primeiros pegam 13 de 50 · 27x o acaso | ❌ |
| Comparação com o critério atual | prioridade declarada pega 0 nos mesmos 50 | ❌ |
| Calibração | prevê 47,1 quebras, ocorreram 50 | ❌ |
| Decomposição por caso | peso × (valor − média), erro 2,8e-16 | ✅ no modal |
| Cobertura da explicação | sinais mostrados cobrem 54% na faixa crítica | ✅ no modal |
| Por que logística e não XGBoost | PR-AUC 0,296 contra 0,253; XGB com peso prevê 1.007 | ❌ |
| A armadilha da acurácia | classificador que nunca alerta acerta 99,04% | ❌ |
| Grupos críticos | 7 grupos com 13% das violações em 5% da base | ✅ tabela |

**O buraco:** a aba tem a fila, mas não tem **nenhuma prova de que a fila funciona**. Um
avaliador pergunta "por que eu confiaria nessa ordem?" e a tela não responde.

**Versão masterizada**

1. Herói: o card-bento com **27×**, com o corte da fila arrastável dentro dele. Junta o
   manifesto e o instrumento que eu tinha separado.
2. Card **"o modelo contra os outros critérios"**: captura por risco, por prioridade
   declarada, por acaso, e o teto. Quatro linhas no mesmo eixo.
3. Card **"ele erra para que lado?"**: previu 47,1, ocorreram 50. E a armadilha da
   acurácia dita em uma frase.
4. A tabela e o modal continuam como estão, que já funcionam.

**Precisa de mockup:** o herói (bento com corte arrastável) e o gráfico de captura.
**Não precisa:** tabela, modal, grupos críticos.

---

## Aba 2 · Desempenho do modelo `nova`

Fonte: notebook 03 e `dias.json`. Absorve o controle de tempo.

**O que existe e não está em lugar nenhum**

| Entrega | Valor medido | Está na tela? |
|---|---|---|
| Cobertura real da banda | 80% prometidos, **59,8% entregues** em 92 dias | ❌ |
| Previsto contra real, dia a dia | 92 pares | ❌ |
| Onde o modelo falha | 37 dias fora da faixa, concentrados em quais? | ❌ não investigado |
| Prophet contra baseline | supera o melhor baseline em ambas as séries | ❌ |
| Escolha metodológica `linear` vs `flat` | flat melhora o erro diário mas piora o veredito do ano de 7/10 para 4/10 | ❌ |

**A tese da aba:** é onde o sistema mede a si mesmo. Nenhum concorrente de sala vai ter
uma aba dizendo "minha banda promete 80% e entrega 60%". Isso vira credibilidade.

**Versão masterizada**

1. Herói: a **linha do tempo dos 92 dias** com play. Marca vermelha em cada dia que saiu
   da faixa. Ao viajar, as linhas do fundo correm — a sensação de tempo passando.
2. Card **taxa de acerto acumulada**: sobe e desce ao longo do trimestre.
3. Card **"onde ele erra"**: os 37 dias fora, agrupados por dia da semana e por magnitude.
   Investigação a fazer.
4. Card **a decisão metodológica**: por que `linear` mesmo com erro diário maior.

**Precisa de mockup:** o controle de tempo já tem três versões prontas em
`prototipos/telas/mockups/controle-tempo.html` — falta só escolher.
**A investigar antes:** em que dias a faixa falha. Se houver padrão, é achado novo.

---

## Aba 3 · Saúde por produto

Fonte: notebook 07 e `07_saude_produto.parquet`.

| Entrega | Valor medido | Está na tela? |
|---|---|---|
| Nota por posição relativa | 17 produtos, 5 componentes | ✅ tabela e modal |
| Os quatro quadrantes | latente, materializado, recorrente, estável | ⚠️ só como etiqueta |
| O gráfico de quadrante | é o que dá nome à classificação | ❌ **não existe** |
| Componente descartado | incidentes por ativo, correlação 0,85 com duração | ❌ |
| O inédito viola 4,6x mais | sobreviveu a 7 verificações | ⚠️ só como frase |

**O buraco:** a palavra "quadrante" aparece na tela sem o quadrante existir. É o gráfico
mais importante do notebook 07 e ele não foi para lugar nenhum.

**Versão masterizada**

1. Herói: **o quadrante de verdade**. Eixo x é violação, eixo y é proporção de inédito,
   17 bolhas dimensionadas por volume. Clica na bolha e abre o produto.
2. Card **comparar dois produtos** lado a lado, que o Igor pediu.
3. Card **por que o inédito pesa**, com a evidência das 7 verificações.
4. Tabela e modal seguem.

**Precisa de mockup:** o quadrante e o comparador.

---

## Aba 4 · Causas e recorrentes

Fonte: notebook 05.

| Entrega | Valor medido | Está na tela? |
|---|---|---|
| Causa de fechamento | "Outro": 7,8% do volume, 21,8% das violações | ✅ tabela |
| **Agrupamento por texto normalizado** | `IC\d+` e números viram marcador | ❌ invisível |
| Os 20 mais recorrentes | 26% do volume, violam 0,40% | ✅ lista |
| Diagnóstico em três estados | soma bate com a base, com assert | ❌ |
| Grupos críticos | duplicado com a aba Fila | ⚠️ decidir onde mora |

**O buraco maior de todos.** A normalização de texto é um trabalho real de engenharia e a
tela mostra o resultado como se fosse uma lista qualquer. Ninguém percebe que houve
trabalho ali.

**Versão masterizada**

1. Herói: **o gráfico de divergência**. Uma barra por causa, com dois braços: quanto ela
   é do volume e quanto é das violações. Onde os braços destoam, há concentração. É a
   melhor tradução visual de "volume não é risco" que existe.
2. Card **antes e depois da normalização**: mostrar dois ou três textos crus virando um
   grupo só. Torna o trabalho visível em três segundos.
3. Card **o que dá para automatizar**: os recorrentes com muito volume e pouca violação.

**Precisa de mockup:** o gráfico de divergência e o card de normalização.

---

## Aba 5 · Hoje

Aprovada. Pendências: entrar o controle de tempo escolhido e trocar a busca por ele.

---

## O que precisa da sua decisão, e quando

| # | Decisão | Depende de | Quando |
|---|---|---|---|
| 1 | Controle de tempo: qual das três | já prototipado | agora |
| 2 | Linguagem do card-bento | Claude Design ou eu | antes da aba 1 |
| 3 | Herói da Fila: bento com corte arrastável | mockup a fazer | aba 1 |
| 4 | Quadrante: bolhas ou matriz 2×2 | mockup a fazer | aba 3 |
| 5 | Divergência: barra dupla ou inclinação | mockup a fazer | aba 4 |

## Ordem de execução

1. **Investigar** onde a faixa de 80% falha nos 37 dias. Pode virar achado.
2. **Aba 1 · Fila** — define o padrão das demais.
3. **Aba 2 · Desempenho** — a mais nova, dados prontos.
4. **Aba 3 · Saúde** — precisa do quadrante.
5. **Aba 4 · Causas** — a mais fraca, maior ganho relativo.
6. **Hoje** recebe o controle de tempo.
7. Validação, Docker, URL pública.

## Dívidas técnicas registradas

- `scripts/monta_app.py` gera o protótipo estático e o Django tem sua própria camada. Dois
  caminhos para a mesma tela. Vale unificar quando as abas estabilizarem.
- Grupos críticos aparece na Fila e na Causas. Escolher um lar.
- A busca por texto na fila do Django funciona, mas o Ctrl+K sai junto com a barra de
  busca — confirmar que ninguém sente falta.
